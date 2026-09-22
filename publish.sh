#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
repo='devdogfish/cityhelpers'
site_url='https://devdogfish.github.io/cityhelpers/'
# Keep output in the terminal; never open a pager or interactive prompt.
export GH_PAGER=cat GIT_PAGER=cat PAGER=cat GH_PROMPT_DISABLED=1
unset GH_FORCE_TTY
started=$SECONDS
stage='Starting'
log_file=$(mktemp "${TMPDIR:-/tmp}/cityhelpers-publish.XXXXXX")
success=false
active_pid=''
finish() {
  code=$?
  if [[ -n "$active_pid" ]]; then
    kill "$active_pid" 2>/dev/null || true
    wait "$active_pid" 2>/dev/null || true
  fi
  if [[ "$success" == true ]]; then
    rm -f "$log_file"
  else
    printf '\nPublish stopped: %s (exit %s).\nDetails: %s\n' "$stage" "$code" "$log_file" >&2
  fi
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf 'Publishing City Helpers\n%s\nProgress updates appear below; no keys or clicks needed.\n' "$site_url"
step() {
  stage=$2
  printf '\n[%s/8] %s\n' "$1" "$stage"
}
fail() { printf '%s\n' "$*" | tee -a "$log_file" >&2; exit 1; }
run() {
  local pid code began=$SECONDS next=$((SECONDS + 10))
  printf '\n--- %s ---\n' "$*" >>"$log_file"
  "$@" >>"$log_file" 2>&1 &
  pid=$!
  active_pid=$pid
  while kill -0 "$pid" 2>/dev/null; do
    if (( SECONDS >= next )); then
      printf '  Still working… %ss elapsed\n' "$((SECONDS - began))"
      next=$((SECONDS + 10))
    fi
    sleep 1
  done
  if wait "$pid"; then
    active_pid=''
    printf '  Done (%ss)\n' "$((SECONDS - began))"
  else
    code=$?
    active_pid=''
    tail -n 25 "$log_file" >&2
    exit "$code"
  fi
}
step 1 'Checking tools, branch, and GitHub login'
for command in python3 git gh curl pdftotext; do
  command -v "$command" >/dev/null || fail "Missing required command: $command"
done
[[ "$(git branch --show-current)" == main ]] || fail 'Publish from the main branch.'
[[ -z "$(git diff --name-only --diff-filter=U)" ]] || fail 'Resolve merge conflicts before publishing.'
run gh api user --jq .login
step 2 'Checking remote changes'
run git fetch origin main --quiet
git merge-base --is-ancestor origin/main HEAD || fail 'Remote has new commits. Run git pull --rebase, then publish again.'
step 3 'Checking notes and navigation'
run python3 test-sync-notes.py
step 4 'Generating pages, sources, and LLM exports'
run python3 sync-notes.py
run git diff --check
step 5 'Saving changes'
run git add -A
if git diff --cached --quiet; then
  printf '  No new changes to commit.\n'
else
  run git commit -m 'Publish latest project notes'
fi
revision=$(git rev-parse HEAD)
printf '  Commit: %.8s\n' "$revision"
step 6 'Pushing to GitHub'
run git push origin main
step 7 'Building and deploying GitHub Pages'
run_id=''
for attempt in {1..24}; do
  run_id=$(gh run list --repo "$repo" --commit "$revision" --workflow pages-build-deployment --limit 1 --json databaseId --jq '.[0].databaseId // empty')
  [[ -n "$run_id" ]] && break
  printf '  Waiting for GitHub to queue the build… %ss total\n' "$((SECONDS - started))"
  sleep 5
done
[[ -n "$run_id" ]] || fail 'GitHub did not start a Pages build within two minutes. Check repository Actions.'
printf '  Build details: https://github.com/%s/actions/runs/%s\n' "$repo" "$run_id"
deadline=$((SECONDS + 1200))
while true; do
  state=$(gh run view "$run_id" --repo "$repo" --json status,conclusion,jobs --jq '[.status, (.conclusion // ""), ([.jobs[] | select(.status != "completed") | (.name + ": " + .status)] | join("; "))] | join("|")')
  IFS='|' read -r status conclusion jobs <<<"$state"
  printf '  %s%s — %ss total\n' "$status" "${jobs:+ ($jobs)}" "$((SECONDS - started))"
  if [[ "$status" == completed ]]; then
    [[ "$conclusion" == success ]] || fail "GitHub Pages ended with: $conclusion. See build details above."
    break
  fi
  (( SECONDS < deadline )) || fail 'Deployment is still running after 20 minutes. Check the build details above.'
  sleep 10
done
step 8 'Verifying live pages and source downloads'
run python3 verify-published.py
success=true
printf '\nPublished and verified in %ss\n%s\n' "$((SECONDS - started))" "$site_url"

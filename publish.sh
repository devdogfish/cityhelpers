#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
repo='devdogfish/cityhelpers'
for command in python3 git gh curl pdftotext; do
  command -v "$command" >/dev/null || { echo "Missing required command: $command" >&2; exit 1; }
done
[[ "$(git branch --show-current)" == main ]] || { echo 'Publish from the main branch.' >&2; exit 1; }
[[ -z "$(git diff --name-only --diff-filter=U)" ]] || { echo 'Resolve merge conflicts before publishing.' >&2; exit 1; }
gh api user --jq .login >/dev/null
# Refuse to overwrite remote changes; reconcile them before regenerating pages.
git fetch origin main --quiet
git merge-base --is-ancestor origin/main HEAD || { echo 'Remote has new commits. Run git pull --rebase, then publish again.' >&2; exit 1; }
python3 test-sync-notes.py
python3 sync-notes.py
git diff --check
git add -A
git commit -m 'Publish latest project notes'
git push origin main
revision=$(git rev-parse HEAD)
echo 'Waiting for GitHub Pages to build and deploy…'
run_id=''
for attempt in {1..24}; do
  run_id=$(gh run list --repo "$repo" --commit "$revision" --workflow pages-build-deployment --limit 1 --json databaseId --jq '.[0].databaseId // empty')
  [[ -n "$run_id" ]] && break
  sleep 5
done
[[ -n "$run_id" ]] || { echo 'GitHub did not start a Pages build within two minutes. Check repository Actions.' >&2; exit 1; }
gh run watch "$run_id" --repo "$repo" --exit-status --interval 10
python3 verify-published.py
echo 'Published: https://devdogfish.github.io/cityhelpers/'

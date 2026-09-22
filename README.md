# City Helpers team notes

Live site: https://devdogfish.github.io/cityhelpers/

## Edit and publish

Edit or add Markdown files beside `CONTEXT.md`, `OBJECTIVE.md`, and `TARGET_AUDIENCE.md` in the parent `cityhelpers.ca` folder. Then, from that folder, run:

```bash
./site/publish.sh
```

Or run this from anywhere:

```bash
bash '/Users/devdogfish/Documents/10-19 Projects/12 Client projects/cityhelpers.ca/site/publish.sh'
```

The command discovers the notes, generates pages and navigation, commits and pushes this site repository, waits for GitHub Pages to build and deploy, and checks every live page against the current publication. It exits unsuccessfully if any step fails. The final `Published:` message confirms completion.

## File rules

- Root-level `.md` notes in the parent folder become public pages automatically.
- `README.md`, `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, symlinks, and filenames beginning with `_` or `.` are excluded.
- PDFs, transcripts, and other file types are not published by the sync command.
- New notes use their first `# Heading` as their title, or their filename if no heading exists.
- Adding, renaming, or removing a note updates the menu and generated pages. Duplicate or reserved page names are rejected.
- Links such as `[Related](OTHER_NOTE.md)` between discovered notes are converted to site links.
- Edit original notes in the parent folder: the copies inside `site/` are generated and overwritten on publishing.
- Logo and design live in `assets/` and `_layouts/`. Website changes in this repository are included in publishing.

Requires Python 3, Git, GitHub CLI (`gh`) authenticated with access to `devdogfish/cityhelpers`, and curl. GitHub performs the Jekyll build; no local Ruby or Node installation is needed. If the remote contains changes missing locally, the command stops and asks you to reconcile them before publishing.

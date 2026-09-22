# City Helpers team notes

Live site: https://devdogfish.github.io/cityhelpers/

## Edit and publish

Edit or add Markdown files in the project root or one folder deep, for example `current-business/`, `looking-ahead/`, or `brainstorming/`. Then, from the parent `cityhelpers.ca` folder, run:

```bash
./publish.sh
```

Or run this from anywhere:

```bash
bash '/Users/devdogfish/Documents/10-19 Projects/12 Client projects/cityhelpers.ca/publish.sh'
```

The command discovers the notes, generates pages and navigation, commits and pushes this site repository, waits for GitHub Pages to build and deploy, and checks every live page against the current publication. It exits unsuccessfully if any step fails. The final `Published:` message confirms completion.

## File rules

- `source-material/` holds untouched originals. Its eligible direct children (`.md`, `.txt`, `.pdf`) appear alphabetically on Sources & transcripts, never as separate navigation pages. Keep analysis and edits in the topic folders; the publisher only reads originals.
- Root-level `.md` notes and notes one folder deep become public pages automatically. A new immediate folder containing eligible notes automatically creates a navigation group.
- Sections appear as Current business, Looking ahead, Brainstorming, then other folders alphabetically. Files are sorted alphabetically (case-insensitive, with a case-sensitive tie break). Group labels come from folder names. No manually maintained navigation list is needed.
- Root notes appear in a `Project notes` group. Empty groups disappear. Deeper folders are not scanned.
- `site/`, `work/`, `outputs/`, `node_modules/`, hidden/underscore folders, and symlink folders are excluded.
- `README.md`, `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, symlinks, and filenames beginning with `_` or `.` are excluded.
- Eligible `.txt` and `.pdf` files in the root or one folder deep are published as originals under `raw/`, together with original Markdown notes. PDFs also get extracted `.pdf.txt` copies. Other file types remain excluded. Hidden/underscore files and symlinks remain excluded.
- Use lowercase, hyphenated filenames (e.g. `business-context.md`, `team-meeting-01-transcript.txt`). The renamed business context and objectives notes retain their original public URLs through explicit aliases.
- New notes use their first `# Heading` as their title, or their filename if no heading exists.
- Adding, renaming, or removing a note updates the menu and generated pages. Duplicate or reserved page names are rejected.
- URLs derive from filenames, not folders: moving `customer-journey.md` into `current-business/` preserves `/customer-journey.html`. Renaming a filename changes its URL. Duplicate filenames/slugs across folders are rejected.
- Relative note links, including `../looking-ahead/business-objectives.md#anchor`, are converted to site links. Missing Markdown targets fail before generated pages are replaced. Legacy bare-filename links still resolve when their target moves folders.
- Edit original notes in the project folders: the copies inside `site/` are generated and overwritten on publishing.
- Logo and design live in `assets/` and `_layouts/`. Website changes in this repository are included in publishing.

Requires Python 3, Poppler (`pdftotext`), Git, GitHub CLI (`gh`) authenticated with access to `devdogfish/cityhelpers`, and curl. GitHub performs the Jekyll build; no local Ruby or Node installation is needed. If the remote contains changes missing locally, the command stops and asks you to reconcile them before publishing.

`python3 test-sync-notes.py` verifies folder discovery, ordering, stable URLs after moves, cross-links, private-file exclusions, duplicate rejection, and deleted-page cleanup. Publishing runs these tests first and verifies folder navigation on every live page afterward.

Mermaid code fences render in the browser through `assets/mermaid.js`, using a pinned Mermaid release from jsDelivr. If it cannot load, the source remains readable. Large diagrams scroll within the page.

Optional rendering check (separate from the publication-marker check): install Playwright with `npm install --no-save playwright` and its browser with `npx playwright install chromium`, then run `node verify-diagrams.cjs`. Pass a local customer-journey URL to check a preview. Set `CHROME_PATH` to use an existing Chrome executable.

## Sources and LLM access

One Sources & transcripts navigation link opens `/sources.html`. `/llms.txt` is the file index; `/llms-full.txt` combines original Markdown, complete text sources, and PDF text. These outputs are generated on every publish. The homepage links to them without JavaScript. Originals retain their project paths beneath `/raw/`. Generated publication checks verify every exported file byte-for-byte, including the PDF. Removed source files disappear from the export on the next publication.

The menu labels this entry **Sources & transcripts**, directly below Overview. Every published page must appear inside the Notes navigation on every page; a link in the article body does not satisfy the publish check. Sync rejects manually added top-level HTML/Jekyll pages outside the generated page inventory so they cannot silently publish without a menu entry. Original transcripts and PDFs appear on Sources with readable labels. Raw Markdown downloads are indexed in `llms.txt`.

The repository and GitHub Pages are public. All HTML pages carry `noindex, nofollow` metadata to discourage search indexing. Direct links and LLM retrieval remain available. Raw text/PDF responses cannot have custom `X-Robots-Tag` headers on GitHub Pages, so search invisibility is not guaranteed. A project-level robots.txt would not control crawlers because robots rules belong at the origin root; none is added.

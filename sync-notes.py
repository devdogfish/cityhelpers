"""Copy project Markdown notes into the site and generate its navigation."""
from datetime import datetime
from pathlib import Path
import json
import re
import uuid

root = Path(__file__).resolve().parent
known = {
    'OBJECTIVE.md': ('objective', 'Business problem and objective', 'Objective'),
    'TARGET_AUDIENCE.md': ('target-audience', 'Target audience', 'Target audience'),
    'CONTEXT.md': ('context', 'Business context', 'Business context'),
}
excluded = {'README.md', 'AGENTS.md', 'CLAUDE.md', 'SKILL.md'}
sources = sorted((p for p in root.parent.glob('*.md')
                  if p.name not in excluded and not p.name.startswith(('.', '_')) and not p.is_symlink()),
                 key=lambda p: (list(known).index(p.name) if p.name in known else len(known), p.name))
if not sources:
    raise SystemExit('No Markdown notes found in the parent project folder.')
notes = []
slugs = {'index', 'readme'}
for source in sources:
    body = source.read_text(encoding='utf-8').strip()
    heading = re.match(r'^#\s+(.+?)\n', body + '\n')
    slug, title, label = known.get(source.name, (
        re.sub(r'[^a-z0-9]+', '-', source.stem.lower()).strip('-'),
        heading.group(1) if heading else source.stem.replace('_', ' ').replace('-', ' ').capitalize(),
        heading.group(1) if heading else source.stem.replace('_', ' ').replace('-', ' ').capitalize()))
    if not slug or slug in slugs:
        raise SystemExit(f'Duplicate or reserved page name: {source.name}')
    slugs.add(slug)
    if heading:
        body = body[heading.end():].lstrip()
    notes.append(dict(source=source.name, file=slug + '.md', url='/' + slug + '.html',
                      title=title, label=label, body=body,
                      updated=datetime.fromtimestamp(source.stat().st_mtime).date().isoformat()))
# Rewrite links between project notes to their generated pages.
for note in notes:
    for other in notes:
        note['body'] = re.sub(r'\]\((?:\./)?' + re.escape(other['source']) + r'(#[^)]*)?\)',
                             lambda m: '](' + other['url'].lstrip('/') + (m.group(1) or '') + ')', note['body'])
manifest = root / '_data/notes.json'
previous = json.loads(manifest.read_text()) if manifest.exists() else []
current = {n['file'] for n in notes}
for old in previous:
    name = old['file']
    if name not in current and Path(name).name == name and name.endswith('.md'):
        (root / name).unlink(missing_ok=True)
for note in notes:
    frontmatter = '\n'.join(f'{key}: {json.dumps(note[key], ensure_ascii=False)}'
                            for key in ('title', 'updated'))
    (root / note['file']).write_text('---\n' + frontmatter + '\n---\n\n' + note['body'] + '\n', encoding='utf-8')
    print('Synced ' + note['source'])
manifest.parent.mkdir(exist_ok=True)
manifest.write_text(json.dumps([{k: v for k, v in n.items() if k != 'body'} for n in notes], indent=2, ensure_ascii=False) + '\n')
(root / '_data/publication.json').write_text(json.dumps({'id': uuid.uuid4().hex}) + '\n')
(root / 'index.md').write_text('''---
title: Marketing project notes
---
Our shared reference for developing a practical customer acquisition plan for City Helpers in Toronto/GTA.

{% for note in site.data.notes %}
- [{{ note.label }}]({{ note.url | relative_url }})
{% endfor %}

These are working notes. Sources are linked throughout; assumptions and details needing client confirmation are identified in the text.
''')

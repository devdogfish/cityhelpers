"""Publish root notes and notes one folder deep, with deterministic navigation."""
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import posixpath
import re
import uuid
import knowledge_exports

KNOWN = {
    'business-context.md': ('context', 'Business context', 'Business context'),
    'business-objectives.md': ('objective', 'Business objectives', 'Business objectives'),
    'OBJECTIVE.md': ('objective', 'Business problem and objective', 'Objective'),
    'TARGET_AUDIENCE.md': ('target-audience', 'Target audience', 'Target audience'),
    'CONTEXT.md': ('context', 'Business context', 'Business context'),
}
EXCLUDED = {'README.md', 'AGENTS.md', 'CLAUDE.md', 'SKILL.md'}
SECTION_ORDER = {'current-business': 0, 'brainstorming': 1}
REDIRECTS = {'success-and-measurement.md': '/objective.html'}
INFRASTRUCTURE = {'site', 'node_modules', 'work', 'outputs'}


def visible(path):
    return not path.name.startswith(('.', '_')) and not path.is_symlink()


def sort_key(value):
    return (value.casefold(), value)


def discover(project, site, extensions={'.md'}):
    sources = []
    for path in project.iterdir():
        if not visible(path):
            continue
        if path.is_file() and path.suffix.lower() in extensions and path.name not in EXCLUDED:
            sources.append(path)
        elif path.is_dir() and path.resolve() != site.resolve() and path.name not in INFRASTRUCTURE:
            sources.extend(p for p in path.iterdir()
                           if visible(p) and p.is_file() and p.suffix.lower() in extensions and p.name not in EXCLUDED)
    return sorted(sources, key=lambda p: (sort_key(p.relative_to(project).parent.as_posix()), sort_key(p.name)))


def sync(root):
    root = Path(root)
    project = root.parent
    sources = [source for source in discover(project, root)
               if source.relative_to(project).parts[0] != "source-material"]
    if not sources:
        raise ValueError('No Markdown notes found in the project root or immediate folders.')
    notes = []
    slugs = {'index', 'readme', 'sources', 'llms', 'llms-full'}
    for source in sources:
        body = source.read_text(encoding='utf-8').strip()
        heading = re.match(r'^#\s+(.+?)\n', body + '\n')
        title = heading.group(1) if heading else source.stem.replace('_', ' ').replace('-', ' ').capitalize()
        label = re.sub(r'^City Helpers\s*[—–-]\s*', '', title, flags=re.I)
        label = label[:1].upper() + label[1:]
        slug, title, label = KNOWN.get(source.name, (
            re.sub(r'[^a-z0-9]+', '-', source.stem.lower()).strip('-'), title, label))
        if not slug or slug in slugs:
            raise ValueError(f'Duplicate or reserved page name: {source.relative_to(project)}')
        slugs.add(slug)
        if heading:
            body = body[heading.end():].lstrip()
        relative = source.relative_to(project)
        folder = '' if relative.parent == Path('.') else relative.parent.as_posix()
        notes.append(dict(source=relative.as_posix(), folder=folder, file=slug + '.md',
                          url='/' + slug + '.html', title=title, label=label, body=body,
                          updated=datetime.fromtimestamp(source.stat().st_mtime).date().isoformat()))
    by_source = {note['source']: note for note in notes}
    by_name = {Path(note['source']).name: note for note in notes}
    for note in notes:
        def rewrite(match):
            target = match.group(1).strip('<>')
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path.lower().endswith('.md'):
                return match.group(0)
            path = unquote(parts.path)
            relative = posixpath.normpath(posixpath.join(posixpath.dirname(note['source']), path))
            other = by_source.get(relative)
            # Preserve old bare-filename links when an existing note changes folder.
            if other is None and '/' not in path:
                other = by_name.get(path)
            if other is None:
                raise ValueError(f"Unresolved note link in {note['source']}: {target}")
            suffix = ('?' + parts.query if parts.query else '') + ('#' + parts.fragment if parts.fragment else '')
            return '](' + other['url'].lstrip('/') + suffix + ')'
        note['body'] = re.sub(r'\]\((<[^>]+>|[^\s)]+)\)', rewrite, note['body'])
    exports = knowledge_exports.prepare(project, discover(project, root, {'.md', '.txt', '.pdf'}))
    # Complete validation and extraction before replacing generated pages.
    manifest = root / '_data/notes.json'
    previous = json.loads(manifest.read_text()) if manifest.exists() else []
    current = {note['file'] for note in notes}
    registered = current | {n['file'] for n in previous} | {'index.md', 'sources.md'} | set(REDIRECTS)
    # A manually added HTML/Jekyll page must not silently become an orphan.
    for path in root.iterdir():
        if not path.is_file() or not visible(path) or path.name in registered or path.name in EXCLUDED:
            continue
        if path.suffix == '.html' or (path.suffix == '.md' and path.read_text().startswith('---')):
            raise ValueError(f'Unregistered site page: {path.name}. Add its source note to a project folder so navigation includes it.')
    for old in previous:
        name = old['file']
        if name not in current and Path(name).name == name and name.endswith('.md'):
            (root / name).unlink(missing_ok=True)
    for filename, target in REDIRECTS.items():
        (root / filename).write_text('---\nlayout: null\n---\n<!doctype html>\n'
            '<html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">'
            '<meta http-equiv="refresh" content="0; url={{ \'' + target + '\' | relative_url }}">'
            '<title>Moved to Business objectives</title></head><body>'
            '<a href="{{ \'' + target + '\' | relative_url }}">Continue to Business objectives</a>'
            '</body></html>\n')
    for note in notes:
        frontmatter = '\n'.join(f'{key}: {json.dumps(note[key], ensure_ascii=False)}'
                                for key in ('title', 'updated'))
        (root / note['file']).write_text('---\n' + frontmatter + '\n---\n\n' + note['body'] + '\n', encoding='utf-8')
        print('Synced ' + note['source'])
    public = [{k: v for k, v in n.items() if k != 'body'} for n in notes]
    navigation = []
    for folder in sorted({n['folder'] for n in public}, key=lambda folder: (SECTION_ORDER.get(folder, 3), sort_key(folder))):
        label = folder.replace('-', ' ').replace('_', ' ').capitalize() if folder else 'Project notes'
        navigation.append(dict(folder=folder, label=label, notes=[n for n in public if n['folder'] == folder]))
    manifest.parent.mkdir(exist_ok=True)
    manifest.write_text(json.dumps(public, indent=2, ensure_ascii=False) + '\n')
    (root / '_data/navigation.json').write_text(json.dumps(navigation, indent=2, ensure_ascii=False) + '\n')
    (root / '_data/publication.json').write_text(json.dumps({'id': uuid.uuid4().hex}) + '\n')
    knowledge_exports.write(root, *exports)
    (root / 'index.md').write_text('''---
title: City Helpers knowledge base
---
Our shared reference for understanding City Helpers and developing practical ways to help the business in Toronto/GTA.

**For LLMs:** [Read all context in one text file]({{ '/llms-full.txt' | relative_url }}), including original transcripts and PDF text. [Browse sources and downloads]({{ '/sources.html' | relative_url }}) or use the [compact index]({{ '/llms.txt' | relative_url }}).

{% for group in site.data.navigation %}
## {{ group.label }}

{% for note in group.notes %}
- [{{ note.label }}]({{ note.url | relative_url }})
{% endfor %}
{% endfor %}

Evidence, assumptions, proposals, and results are distinguished within each topic. Browse the topics above or use the navigation menu.
''', encoding='utf-8')
    return public


if __name__ == '__main__':
    sync(Path(__file__).resolve().parent)

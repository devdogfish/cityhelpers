"""Check every published page against this publication's unique marker."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from html.parser import HTMLParser
import json
import subprocess
import time
from hashlib import sha256

root = Path(__file__).resolve().parent
base = 'https://devdogfish.github.io/cityhelpers'
build = json.loads((root / '_data/publication.json').read_text())['id']
notes = json.loads((root / '_data/notes.json').read_text())
groups = ['Knowledge base'] + [g['label'] for g in json.loads((root / '_data/navigation.json').read_text())]
pages = ['/', '/sources.html'] + [note['url'] for note in notes]
sources = json.loads((root / '_data/sources.json').read_text())
context_files = json.loads((root / '_data/context-files.json').read_text())

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.marker = None
        self.links = set()
        self.nav_links = set()
        self.download_links = set()
        self.in_nav = False
        self.groups = []
        self.in_group = False
        self.robots = ''
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('name') == 'notes-publication':
            self.marker = attrs.get('content')
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.robots = attrs.get('content', '')
        if tag == 'nav' and attrs.get('aria-label') == 'Notes':
            self.in_nav = True
        if tag == 'a':
            if 'download' in attrs:
                self.download_links.add(attrs.get('href', ''))
            self.links.add(attrs.get('href', ''))
            if self.in_nav:
                self.nav_links.add(attrs.get('href', ''))
        if tag == 'h2' and 'nav-group-title' in attrs.get('class', '').split():
            self.groups.append('')
            self.in_group = True
    def handle_data(self, data):
        if self.in_group:
            self.groups[-1] += data
    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_nav = False
        if tag == 'h2':
            self.in_group = False

def verify(path):
    for attempt in range(18):
        result = subprocess.run(['curl', '--fail', '--silent', '--show-error', '--max-time', '20',
                                 base + path + '?publication=' + build], capture_output=True, text=True)
        page = Page()
        page.feed(result.stdout)
        if result.returncode == 0 and page.marker == build:
            missing = [p for p in pages if '/cityhelpers' + p not in page.nav_links]
            if missing:
                raise RuntimeError(f'{path}: navigation missing {missing}')
            if page.groups != groups:
                raise RuntimeError(f'{path}: navigation folders differ: {page.groups}')
            if 'noindex' not in page.robots:
                raise RuntimeError(f'{path}: missing search indexing opt-out')
            if path == '/sources.html':
                expected = {'/cityhelpers' + source[key] for source in sources
                            if source['kind'] == 'source' for key in ('url', 'text_url') if key in source}
                if not expected.issubset(page.download_links):
                    raise RuntimeError(f'Sources missing download links: {expected - page.download_links}')
            return 'Verified ' + path
        time.sleep(5)
    raise RuntimeError(f'{path}: latest publication was not visible after retries')

def verify_context(item):
    for attempt in range(18):
        result = subprocess.run(['curl', '--fail', '--silent', '--show-error', '--max-time', '20',
                                 base + item['url']], capture_output=True)
        if result.returncode == 0 and sha256(result.stdout).hexdigest() == item['sha256']:
            return 'Verified context ' + item['file']
        time.sleep(5)
    raise RuntimeError(f"{item['url']}: published bytes differ from local source/export")


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        for message in pool.map(verify, pages):
            print(message)
        for message in pool.map(verify_context, context_files):
            print(message)

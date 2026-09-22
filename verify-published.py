"""Check every published page against this publication's unique marker."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from html.parser import HTMLParser
import json
import subprocess
import time

root = Path(__file__).resolve().parent
base = 'https://devdogfish.github.io/cityhelpers'
build = json.loads((root / '_data/publication.json').read_text())['id']
notes = json.loads((root / '_data/notes.json').read_text())
groups = [g['label'] for g in json.loads((root / '_data/navigation.json').read_text())]
pages = ['/'] + [note['url'] for note in notes]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.marker = None
        self.links = set()
        self.groups = []
        self.in_group = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('name') == 'notes-publication':
            self.marker = attrs.get('content')
        if tag == 'a':
            self.links.add(attrs.get('href', ''))
        if tag == 'h2' and 'nav-group-title' in attrs.get('class', '').split():
            self.groups.append('')
            self.in_group = True
    def handle_data(self, data):
        if self.in_group:
            self.groups[-1] += data
    def handle_endtag(self, tag):
        if tag == 'h2':
            self.in_group = False

def verify(path):
    for attempt in range(18):
        result = subprocess.run(['curl', '--fail', '--silent', '--show-error', '--max-time', '20',
                                 base + path + '?publication=' + build], capture_output=True, text=True)
        page = Page()
        page.feed(result.stdout)
        if result.returncode == 0 and page.marker == build:
            missing = [p for p in pages if '/cityhelpers' + p not in page.links]
            if missing:
                raise RuntimeError(f'{path}: navigation missing {missing}')
            if page.groups != groups:
                raise RuntimeError(f'{path}: navigation folders differ: {page.groups}')
            return 'Verified ' + path
        time.sleep(5)
    raise RuntimeError(f'{path}: latest publication was not visible after retries')

with ThreadPoolExecutor(max_workers=4) as pool:
    for message in pool.map(verify, pages):
        print(message)

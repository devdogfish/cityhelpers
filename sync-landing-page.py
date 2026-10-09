"""Copy the local landing-page prototype into the GitHub Pages repository."""

from pathlib import Path
from shutil import copy2, copytree, rmtree
from tempfile import TemporaryDirectory


site = Path(__file__).resolve().parent
source = site.parent / 'work' / 'landing-page'
destination = site / 'landing-page'
web_files = ('index.html', 'styles.css', 'script.js')

for name in web_files:
    if not (source / name).is_file():
        raise FileNotFoundError(source / name)
if not (source / 'assets').is_dir():
    raise FileNotFoundError(source / 'assets')

with TemporaryDirectory(prefix='.landing-page-', dir=site) as temp:
    staged = Path(temp) / 'landing-page'
    staged.mkdir()
    for name in web_files:
        copy2(source / name, staged / name)
    copytree(source / 'assets', staged / 'assets')
    if destination.exists():
        rmtree(destination)
    staged.rename(destination)

print('Synced work/landing-page to site/landing-page')

"""Regression tests for folder discovery, stable URLs, and generated navigation."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('sync_notes', Path(__file__).with_name('sync-notes.py'))
sync_notes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_notes)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        self.site = self.project / 'site'
        self.site.mkdir()
        # Discovery fixtures are text files, not real PDF documents.
        extractor = patch('knowledge_exports.extract_pdf', return_value='Extracted fixture PDF text.')
        extractor.start()
        self.addCleanup(extractor.stop)

    def note(self, name, body='# Example\n\nText.\n'):
        p = self.project / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
        return p

    def test_navigation_matches_folders_and_is_deterministic(self):
        self.note('looking-ahead/Z.md')
        self.note('current-business/B.md')
        self.note('current-business/A.md')
        self.note('ideas-and-work/C.md')
        sync_notes.sync(self.site)
        before = (self.site / '_data/navigation.json').read_text()
        groups = json.loads(before)
        self.assertEqual([g['folder'] for g in groups], ['current-business', 'ideas-and-work', 'looking-ahead'])
        self.assertEqual([n['source'] for n in groups[0]['notes']], ['current-business/A.md', 'current-business/B.md'])
        sync_notes.sync(self.site)
        self.assertEqual(before, (self.site / '_data/navigation.json').read_text())

    def test_move_preserves_url_and_rewrites_cross_folder_links(self):
        p = self.note('OBJECTIVE.md')
        sync_notes.sync(self.site)
        (self.project / 'looking-ahead').mkdir()
        p.rename(self.project / 'looking-ahead/OBJECTIVE.md')
        self.note('ideas-and-work/TEST.md', '# Test\n\n[Objective](../looking-ahead/OBJECTIVE.md#goal)\n')
        notes = sync_notes.sync(self.site)
        self.assertEqual(next(n['url'] for n in notes if n['file'] == 'objective.md'), '/objective.html')
        self.assertIn('[Objective](objective.html#goal)', (self.site / 'test.md').read_text())
        # A new folder becomes a navigation group automatically.
        self.note('new-topic/EXTRA.md')
        sync_notes.sync(self.site)
        self.assertIn('new-topic', [g['folder'] for g in json.loads((self.site / '_data/navigation.json').read_text())])

    def test_excludes_private_and_infrastructure_files(self):
        self.note('current-business/PUBLIC.md')
        for name in ['current-business/_PRIVATE.md', '.private/HIDDEN.md', 'current-business/meeting.txt',
                     'current-business/brief.pdf', 'current-business/README.md', 'site/INTERNAL.md',
                     'work/SCRATCH.md', 'current-business/deep/NOTE.md']:
            self.note(name)
        (self.project / 'current-business/LINK.md').symlink_to(self.project / 'current-business/PUBLIC.md')
        notes = sync_notes.sync(self.site)
        self.assertEqual([n['source'] for n in notes], ['current-business/PUBLIC.md'])

    def test_duplicate_slugs_and_missing_links_fail_before_writes(self):
        self.note('first/SAME.md')
        self.note('second/SAME.md')
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            sync_notes.sync(self.site)
        self.assertFalse((self.site / '_data/notes.json').exists())
        (self.project / 'second/SAME.md').unlink()
        self.note('first/SAME.md', '# Same\n\n[Missing](MISSING.md)\n')
        with self.assertRaisesRegex(ValueError, 'Unresolved'):
            sync_notes.sync(self.site)

    def test_removed_note_is_removed_from_generated_site(self):
        self.note('current-business/KEEP.md')
        p = self.note('ideas-and-work/REMOVE.md')
        sync_notes.sync(self.site)
        p.unlink()
        sync_notes.sync(self.site)
        self.assertFalse((self.site / 'remove.md').exists())
        self.assertEqual(len(json.loads((self.site / '_data/navigation.json').read_text())), 1)

    def test_source_exports_preserve_full_context_and_cleanup(self):
        self.note('current-business/CONTEXT.md', '# Context\n\nA complete note.\n')
        transcript = self.note('source-material/meeting.txt', 'First speaker.\nLast speaker.\n')
        self.note('source-material/brief.pdf', 'PDF fixture')
        self.note('source-material/_PRIVATE.txt', 'Do not publish')
        self.note('source-material/original.md', '# Original document\n\nUnedited source.\n')
        notes = sync_notes.sync(self.site)
        self.assertEqual(len(notes), 1)
        self.assertEqual((self.site / 'raw/source-material/meeting.txt').read_bytes(), transcript.read_bytes())
        full = (self.site / 'llms-full.txt').read_text()
        for text in ['A complete note.', 'First speaker.\nLast speaker.', 'Extracted fixture PDF text.']:
            self.assertIn(text, full)
        self.assertNotIn('Do not publish', full)
        self.assertTrue((self.site / 'raw/source-material/brief.pdf.txt').exists())
        manifest = json.loads((self.site / '_data/sources.json').read_text())
        self.assertEqual(len(manifest), 4)
        originals = [entry for entry in manifest if entry['kind'] == 'source']
        self.assertEqual([entry['source'] for entry in originals], ['source-material/brief.pdf', 'source-material/meeting.txt', 'source-material/original.md'])
        transcript.unlink()
        sync_notes.sync(self.site)
        self.assertFalse((self.site / 'raw/source-material/meeting.txt').exists())
        self.assertNotIn('Last speaker.', (self.site / 'llms-full.txt').read_text())

    def test_previous_download_urls_keep_original_bytes(self):
        self.note('current-business/business-context.md')
        original = self.note('source-material/ceo-discussion-transcript.txt', 'Original words.\n')
        sync_notes.sync(self.site)
        for name in ['ceo-discussion-transcript.txt', 'raw-transcript-context.txt']:
            self.assertEqual((self.site / 'raw/current-business' / name).read_bytes(), original.read_bytes())
        sources = json.loads((self.site / '_data/sources.json').read_text())
        self.assertEqual(sum(s['kind'] == 'source' for s in sources), 1)

    def test_unregistered_page_cannot_be_published_without_navigation(self):
        self.note('current-business/CONTEXT.md')
        (self.site / 'orphan.html').write_text('<h1>Not in navigation</h1>')
        with self.assertRaisesRegex(ValueError, 'Unregistered site page'):
            sync_notes.sync(self.site)

    def test_body_link_cannot_mask_missing_navigation_entry(self):
        spec = importlib.util.spec_from_file_location('verify_published', Path(__file__).with_name('verify-published.py'))
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        page = verifier.Page()
        page.feed('<nav aria-label="Notes"><a href="/cityhelpers/">Home</a></nav>'
                  '<main><a href="/cityhelpers/sources.html">Sources</a></main>')
        self.assertIn('/cityhelpers/sources.html', page.links)
        self.assertNotIn('/cityhelpers/sources.html', page.nav_links)
        page.feed('<nav aria-label="Notes"><a href="/cityhelpers/sources.html">Sources</a></nav>')
        self.assertIn('/cityhelpers/sources.html', page.nav_links)


if __name__ == '__main__':
    unittest.main()

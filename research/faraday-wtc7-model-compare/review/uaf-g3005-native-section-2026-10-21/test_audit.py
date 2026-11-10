"""Synthetic inventory controls only; these are not UAF model tests."""
from pathlib import Path
import tempfile
import unittest
import zipfile

from audit import archive_directory_summary, classify, digest, inventory, zip_manifest


class InventoryTests(unittest.TestCase):
    def test_case_insensitive_native_suffixes(self):
        names = ['case.INP', 'case.odb', 'job.CAE', 'frame.S2K', 'notes.inp.html', 'case.txt']
        self.assertEqual(classify(names)['native_suffix_candidates'], ['case.INP', 'case.odb', 'frame.S2K', 'job.CAE'])

    def test_unavailable_root_is_not_empty_inventory(self):
        with tempfile.TemporaryDirectory() as folder:
            result = inventory(Path(folder) / 'absent')
            self.assertFalse(result['available'])
            self.assertIsNone(result['path_count'])
            self.assertTrue(result['errors'])

    def test_inventory_does_not_follow_links_or_git(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'real.inp').touch()
            (root / '.git').mkdir()
            (root / '.git' / 'not-a-model.odb').touch()
            (root / 'link').symlink_to(root, target_is_directory=True)
            result = inventory(root)
            self.assertEqual(result['path_count'], 1)
            self.assertEqual(result['native_suffix_candidates'], ['real.inp'])
            self.assertNotIn('link/real.inp', result['native_suffix_candidates'])

    def test_archive_member_recognition_without_extraction(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'sample.zip'
            with zipfile.ZipFile(target, 'w') as archive:
                archive.writestr('nested/MODEL.INP', '*NODE\n')
                archive.writestr('readme.txt', 'synthetic fixture')
            result = zip_manifest(target)
            self.assertEqual(result['native_suffix_candidates'], ['nested/MODEL.INP'])
            self.assertEqual(result['members'][1]['sha256'], digest(b'synthetic fixture'))
            self.assertFalse((Path(folder) / 'nested').exists())

    def test_missing_native_candidate_does_not_assign_section(self):
        self.assertEqual(classify(['model.png', 'report.pdf'])['native_suffix_candidates'], [])
        self.assertNotIn('actual_native_section', classify(['model.png']))

    def test_archive_summary_reports_nested_archives(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'sample.zip'
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('nested.zip', b'not extracted')
            summary = archive_directory_summary(path)
            self.assertEqual(summary['nested_archive_candidates'], ['nested.zip'])
            self.assertEqual(summary['member_count'], 1)
            self.assertIsNotNone(summary['archive_sha256'])


if __name__ == '__main__':
    unittest.main()

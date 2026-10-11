"""Synthetic/mock controls only: never open the historical PDF or renderer."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
import derive


class Page:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class Reader:
    def __init__(self):
        self.is_encrypted = False
        self.pages = [Page(f'Synthetic page\n{n - 15}\n') for n in range(1, 292)]
        self.pages[91] = Page('Chapter 3\nRobustness Analysis of Plasco Tower\nunder Fire Conditions\n77\n')
        self.pages[132] = Page('Chapter 4\nAnother chapter\n118\n')


class Controls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='plasco-derive-controls-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / 'synthetic.pdf'
        self.source.write_bytes(b'SYNTHETIC, not a historical PDF')
        (self.base / 'PROTOCOL.md').write_text('synthetic protocol')
        (self.base / 'fonts.conf').write_text('synthetic config; no font process executed')
        self.reader = Reader()
        self.calls = []
        self.failure = None
        self.failure_page = 92
        self.missing_png = False
        self.patches = [
            patch.object(derive, 'HERE', self.base),
            patch.object(derive, 'SOURCE', self.source),
            patch.object(derive, 'SOURCE_PIN', derive.pin(self.source)),
            patch.object(derive, 'PROTOCOL_SHA', derive.pin(self.base / 'PROTOCOL.md')['sha256']),
            patch.object(derive, 'RENDERER', self.source),
            patch.object(derive, 'RENDERER_WRAPPER', self.source),
            patch.object(derive, 'RENDERER_BINARY', self.source),
            patch.object(derive.pypdf, 'PdfReader', return_value=self.reader),
            patch.object(derive.subprocess, 'run', side_effect=self.fake_process)]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def fake_process(self, argv, **kwargs):
        self.calls.append((argv, kwargs))
        self.assertEqual(kwargs['timeout'], 60)
        self.assertEqual(kwargs['env']['XDG_CACHE_HOME'], str(self.base / 'run01/font-cache'))
        self.assertNotIn('HOME', kwargs['env'])
        if '-v' in argv:
            return subprocess.CompletedProcess(argv, 0, b'', b'synthetic renderer version\n')
        page = int(argv[argv.index('-f') + 1])
        if self.failure is not None and page == self.failure_page:
            if self.failure == 'timeout':
                raise subprocess.TimeoutExpired(argv, 60, output=b'partial output', stderr=b'partial diagnostic')
            if self.failure == 'launch':
                raise OSError('synthetic launch refusal')
            return subprocess.CompletedProcess(argv, 7, b'failed output', b'failed diagnostic')
        if not self.missing_png:
            Image.new('RGB', (32, 40), 'white').save(Path(argv[-1]).with_suffix('.png'))
        return subprocess.CompletedProcess(argv, 0, b'', b'synthetic warning retained\n')

    def saved(self):
        return json.loads((self.base / 'run01/receipt.json').read_text())

    def test_fixed_range_complete_and_exact_commands(self):
        result = derive.run('run01')
        self.assertEqual(result['status'], 'complete')
        self.assertEqual([p['physical_page'] for p in result['pages']], list(range(92, 133)))
        self.assertEqual([p['printed_page'] for p in result['pages']], list(range(77, 118)))
        self.assertEqual(len(self.calls), 42)
        for page, (argv, _) in zip(range(92, 133), self.calls[1:]):
            self.assertEqual(argv, [str(self.source), '-f', str(page), '-l', str(page), '-r', '110', '-singlefile', '-png', str(self.source), str(self.base / 'run01' / f'page-{page:03d}')])
        self.assertEqual([x['printed_page'] for x in result['boundaries']], [77, 117, 118])
        self.assertTrue(result['pins_unchanged'])
        self.assertEqual(result, self.saved())
        self.assertTrue((self.base / 'run01/page-132.txt').exists())
        self.assertFalse((self.base / 'run01/page-133.txt').exists())
        self.assertEqual((self.base / 'run01/page-092-render.stderr').read_bytes(), b'synthetic warning retained\n')

    def test_existing_output_and_symlink_refused_untouched(self):
        existing = self.base / 'run01'; existing.mkdir()
        marker = existing / 'keep'; marker.write_bytes(b'keep')
        with self.assertRaises(FileExistsError): derive.run('run01')
        self.assertEqual(marker.read_bytes(), b'keep')
        (self.base / 'link01').symlink_to(existing, target_is_directory=True)
        with self.assertRaises(FileExistsError): derive.run('link01')
        self.assertEqual(self.calls, [])
        self.assertFalse((existing / 'receipt.json').exists())

    def test_run_name_refusal(self):
        for value in ('', '../escape', '/tmp/example', '.', 'has space', True, 'é'):
            with self.subTest(value=value), self.assertRaises(ValueError): derive.run(value)
        self.assertEqual(self.calls, [])

    def test_wrong_source_preserves_failed_receipt_without_render(self):
        self.source.write_bytes(b'changed source')
        result = derive.run('run01')
        self.assertEqual(result['status'], 'failed')
        self.assertIn('source baseline', result['failure']['message'])
        self.assertEqual(self.calls, [])
        self.assertEqual(result, self.saved())

    def test_wrong_protocol_refuses(self):
        (self.base / 'PROTOCOL.md').write_text('changed')
        result = derive.run('run01')
        self.assertEqual(result['status'], 'failed')
        self.assertIn('Protocol', result['failure']['message'])
        self.assertEqual(self.calls, [])

    def test_boundary_labels_count_encryption_title_and_next_chapter(self):
        edits = [('first', lambda r: setattr(r.pages[91], 'text', 'Chapter 3\nwrong\n76')),
                 ('last', lambda r: setattr(r.pages[131], 'text', 'wrong\n118')),
                 ('next', lambda r: setattr(r.pages[132], 'text', 'Chapter 5\n118')),
                 ('title', lambda r: setattr(r.pages[91], 'text', 'Chapter 3\nwrong title\n77')),
                 ('count', lambda r: r.pages.pop()),
                 ('encrypted', lambda r: setattr(r, 'is_encrypted', True))]
        for name, edit in edits:
            reader = Reader(); edit(reader)
            with self.subTest(name=name), self.assertRaises(ValueError): derive.boundaries(reader)

    def test_bad_boundary_preserves_receipt_before_render(self):
        self.reader.pages[132].text = 'Chapter 4\n119'
        result = derive.run('run01')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['pages'], [])
        self.assertEqual(self.calls, [])
        self.assertEqual(result, self.saved())

    def test_timeout_keeps_prior_page_and_partial_diagnostics(self):
        self.failure = 'timeout'; self.failure_page = 93
        result = derive.run('run01')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual([p['status'] for p in result['pages']], ['complete', 'incomplete'])
        self.assertEqual(result['pages'][1]['render']['status'], 'timeout')
        self.assertEqual((self.base / 'run01/page-093-render.stdout').read_bytes(), b'partial output')
        self.assertEqual((self.base / 'run01/page-093-render.stderr').read_bytes(), b'partial diagnostic')
        self.assertTrue((self.base / 'run01/page-092.png').exists())
        self.assertTrue((self.base / 'run01/page-093.txt').exists())
        self.assertFalse((self.base / 'run01/page-094.txt').exists())
        self.assertEqual(result, self.saved())

    def test_nonzero_preserves_status_text_and_diagnostics(self):
        self.failure = 'nonzero'
        result = derive.run('run01')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['pages'][0]['render']['returncode'], 7)
        self.assertEqual((self.base / 'run01/page-092-render.stderr').read_bytes(), b'failed diagnostic')
        self.assertEqual(result, self.saved())

    def test_launch_failure_preserved(self):
        self.failure = 'launch'
        result = derive.run('run01')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['pages'][0]['render']['status'], 'launch_error')
        self.assertEqual(result, self.saved())

    def test_missing_product_zero_exit_not_success(self):
        self.missing_png = True
        result = derive.run('run01')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['pages'][0]['render']['returncode'], 0)
        self.assertEqual(result, self.saved())

    def test_dependency_change_is_not_success(self):
        original = self.fake_process
        def changed(argv, **kwargs):
            result = original(argv, **kwargs)
            if '-f' in argv and argv[argv.index('-f')+1] == '132':
                (self.base / 'PROTOCOL.md').write_text('changed during run')
            return result
        with patch.object(derive.subprocess, 'run', side_effect=changed):
            result = derive.run('run01')
        self.assertEqual(result['status'], 'failed')
        self.assertFalse(result['pins_unchanged'])
        self.assertIn('protocol', result['changed_dependencies'])


if __name__ == '__main__':
    unittest.main()

"""Invented fixtures only; no new historical annotation or comparison execution."""
import ast
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import independent_check_v2 as check
from test_independent_check import source


class VersionedControls(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='f7-v2-check-')
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name).resolve()

    def write(self, name, raw=b'synthetic fixture only\n'):
        path = self.root / name
        path.write_bytes(raw)
        return path

    def readers(self):
        shas = {}
        for role, name in check.READER_FILES.items():
            script = self.write(name.replace('.json', '.py'))
            data = source(role)
            data['script_pin'] = check.pin(script)
            data['inputs'] = {}
            path = self.write(name, check.encoded(data))
            shas[role] = check.pin(path)['sha256']
        return shas

    def mutate_reader(self, shas, role, mutate):
        path = self.root / check.READER_FILES[role]
        data = check.load(path)
        mutate(data)
        path.write_bytes(check.encoded(data))
        shas[role] = check.pin(path)['sha256']

    def test_fixed_filenames_and_original_region_unchanged(self):
        self.assertEqual(check.READER_FILES, {'primary': 'reader-primary.json',
                                             'peer': 'reader-peer-v2.json'})
        shas = self.readers()
        before = {}
        data, paths = check.bound_readers(shas, before, self.root)
        self.assertEqual([p.name for p in paths.values()],
                         ['reader-primary.json', 'reader-peer-v2.json'])
        self.assertEqual(len(before), 4)
        self.assertTrue(all(d['region_id'] == 'F7-Im2-early' for d in data.values()))
        self.assertTrue(all(d['source'] == 'Im2.jpg' for d in data.values()))
        self.assertFalse((self.root / 'reader-peer.json').exists())

    def test_bound_reader_no_rewrite(self):
        shas = self.readers()
        originals = {p.name: p.read_bytes() for p in self.root.iterdir()}
        data, _ = check.bound_readers(shas, {}, self.root)
        book = check.old.helper('bookkeeping')
        for role in check.ROLES:
            snapshot = check.encoded(data[role])
            check.old.annotation(data[role], role, book)
            self.assertEqual(snapshot, check.encoded(data[role]))
        self.assertEqual(originals, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_old_peer_filename_not_fallback(self):
        shas = self.readers()
        (self.root / 'reader-peer-v2.json').rename(self.root / 'reader-peer.json')
        with self.assertRaisesRegex(ValueError, 'fixed reader path'):
            check.bound_readers(shas, {}, self.root)

    def test_missing_sibling_script(self):
        shas = self.readers()
        (self.root / 'reader-peer-v2.py').unlink()
        with self.assertRaisesRegex(ValueError, 'fixed reader path'):
            check.bound_readers(shas, {}, self.root)

    def test_reader_json_symlink_rejected(self):
        shas = self.readers()
        path = self.root / 'reader-peer-v2.json'
        path.rename(self.root / 'alias.json')
        path.symlink_to(self.root / 'alias.json')
        with self.assertRaisesRegex(ValueError, 'fixed reader path'):
            check.bound_readers(shas, {}, self.root)

    def test_reader_script_symlink_rejected(self):
        shas = self.readers()
        path = self.root / 'reader-peer-v2.py'
        path.rename(self.root / 'alias.py')
        path.symlink_to(self.root / 'alias.py')
        with self.assertRaisesRegex(ValueError, 'fixed reader path'):
            check.bound_readers(shas, {}, self.root)

    def test_wrong_missing_and_extra_reader_hashes(self):
        shas = self.readers()
        for altered in ({'primary': shas['primary']}, shas | {'other': '0'*64},
                        shas | {'peer': '0'*64}, shas | {'peer': True}):
            with self.subTest(altered=altered):
                with self.assertRaises(ValueError):
                    check.bound_readers(altered, {}, self.root)

    def test_script_hash_and_boolean_bytes_rejected(self):
        for field, value in [('sha256', '0'*64), ('bytes', True)]:
            shas = self.readers()
            self.mutate_reader(shas, 'peer',
                               lambda d: d['script_pin'].__setitem__(field, value))
            with self.assertRaises(ValueError):
                check.bound_readers(shas, {}, self.root)

    def test_role_and_source_identity_are_not_aliased(self):
        for field, value in [('reader', 'primary'), ('source', 'Im3.jpg'),
                             ('pair', 'F6'), ('region_id', 'F7-Im2')]:
            shas = self.readers()
            self.mutate_reader(shas, 'peer', lambda d: d.__setitem__(field, value))
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, 'identity/role'):
                    check.bound_readers(shas, {}, self.root)

    def test_explicit_reader_provenance(self):
        shas = self.readers()
        _, paths = check.bound_readers(shas, {}, self.root)
        rows = [{'reader_path': os.path.relpath(paths[r], check.BASE)} for r in check.ROLES]
        check.reader_paths(rows, paths)
        for changed in ([], rows[::-1], [rows[0], rows[0]],
                        [rows[0], {'reader_path': rows[1]['reader_path'].replace('-v2', '')}]):
            with self.assertRaisesRegex(ValueError, 'v2 reader provenance'):
                check.reader_paths(changed, paths)

    def test_frozen_preservation_roster(self):
        self.assertEqual(set(check.PRESERVED), {
            'reader-primary.py', 'reader-primary.json', 'reader-primary-notes.md',
            'reader-peer.py', 'assess.py', 'test_assess.py', 'independent_check.py',
            'test_independent_check.py', 'report.md', 'validation.md',
            'peer-reread-2026-10-08.md', 'COMPLETION-V2.md'})
        self.assertEqual(check.PRESERVED['reader-primary.json'],
                         '4a3c323f83b25b93a88dd8db1b31fdcc77935e90b1494e3b3dc8f7eb40f8b734')
        self.assertEqual(set(check.PRODUCER_PINS), {'assess_v2.py', 'test_assess_v2.py'})
        for sha in check.PRESERVED.values():
            check.digest(sha)

    def test_fixed_inputs_require_actual_freeze(self):
        path = self.write('preserved.txt')
        expected = {'preserved.txt': check.pin(path)['sha256']}
        self.assertEqual(len(check.fixed_inputs(self.root, expected)), 1)
        for sha in (None, '', '0'*63, True, 'G'*64):
            with self.assertRaisesRegex(ValueError, 'frozen SHA256'):
                check.fixed_inputs(self.root, {'preserved.txt': sha})

    def test_changed_preserved_bytes_rejected(self):
        path = self.write('preserved.txt')
        expected = {'preserved.txt': check.pin(path)['sha256']}
        path.write_bytes(b'changed synthetic fixture')
        with self.assertRaisesRegex(ValueError, 'changed fixed input'):
            check.fixed_inputs(self.root, expected)

    def test_missing_or_symlink_fixed_input_rejected(self):
        with self.assertRaisesRegex(ValueError, 'plain fixed file'):
            check.fixed_inputs(self.root, {'absent.txt': '0'*64})
        path = self.write('target.txt')
        alias = self.root / 'alias.txt'
        alias.symlink_to(path)
        with self.assertRaisesRegex(ValueError, 'plain fixed file'):
            check.fixed_inputs(self.root, {'alias.txt': check.pin(path)['sha256']})

    def test_required_pin_omission_and_wrong_name(self):
        required = {name: {'bytes': 1, 'sha256': sha} for name, sha in check.PRESERVED.items()}
        check.old.require_map(required, required)
        for name in required:
            bad = copy.deepcopy(required)
            value = bad.pop(name)
            bad['wrong-' + name] = value
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    check.old.require_map(bad, required)
        changed = copy.deepcopy(required)
        changed['reader-peer.py']['sha256'] = '0'*64
        with self.assertRaises(ValueError):
            check.old.require_map(changed, required)

    def prior(self):
        prior = {'candidate_cells': [{'pair': 'F6', 'id': 'outside'},
                                     {'pair': 'F7', 'id': 'old', 'render_x': ['0', '1']}],
                 'pairs': [{'pair': 'F7', 'scenarios': [
                     {'solid_reader': s, 'dash_reader': d} for s in check.ROLES for d in check.ROLES]}]}
        actual = {'preserved_old_F7_candidate_cells': copy.deepcopy(prior['candidate_cells'][1:]),
                  'before_scenarios': copy.deepcopy(prior['pairs'][0]['scenarios']),
                  'unchanged_other_pairs_reference': os.path.relpath(check.OLD/'run01.json', check.HERE)}
        return prior, actual

    def test_old_state_exact_preservation(self):
        prior, actual = self.prior()
        snapshot = check.encoded(prior)
        cells, scenarios = check.old_state(actual, prior)
        self.assertEqual(len(cells), 1)
        self.assertEqual(len(scenarios), 4)
        self.assertEqual(check.encoded(prior), snapshot)

    def test_changed_old_cell_scenario_or_reference_rejected(self):
        for key in ('preserved_old_F7_candidate_cells', 'before_scenarios',
                    'unchanged_other_pairs_reference'):
            prior, actual = self.prior()
            actual[key] = [] if key != 'unchanged_other_pairs_reference' else 'wrong.json'
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    check.old_state(actual, prior)

    def test_identical_runs_and_fixed_hash(self):
        a, b = self.write('one.json', b'{}\n'), self.write('two.json', b'{}\n')
        self.assertEqual(check.identical_runs(a, b, check.pin(a)['sha256']), (a, b))
        with self.assertRaisesRegex(ValueError, 'frozen result hash'):
            check.identical_runs(a, b, '0'*64)
        b.write_bytes(b'{ }\n')
        with self.assertRaisesRegex(ValueError, 'distinct identical'):
            check.identical_runs(a, b, check.pin(a)['sha256'])

    def test_same_run_or_hardlink_is_not_two_copies(self):
        a = self.write('one.json', b'{}\n')
        with self.assertRaises(ValueError):
            check.identical_runs(a, a, check.pin(a)['sha256'])
        b = self.root/'hardlink.json'
        os.link(a, b)
        with self.assertRaises(ValueError):
            check.identical_runs(a, b, check.pin(a)['sha256'])

    def test_symlink_run_rejected(self):
        a = self.write('one.json', b'{}\n')
        b = self.root/'alias.json'
        b.symlink_to(a)
        with self.assertRaisesRegex(ValueError, 'plain producer run'):
            check.identical_runs(a, b, check.pin(a)['sha256'])

    def test_exclusive_receipt_preserves_existing_and_wrong_name_absent(self):
        receipt = {'status': 'synthetic_only', 'coverage': {}}
        path = check.save_receipt(receipt, self.root)
        self.assertEqual(path.name, 'independent-check-v2.json')
        self.assertEqual(path.read_bytes(), check.encoded(receipt))
        with self.assertRaises(FileExistsError):
            check.save_receipt({'different': True}, self.root)
        self.assertEqual(path.read_bytes(), check.encoded(receipt))
        self.assertFalse((self.root / 'independent-check.json').exists())

    def test_receipt_symlink_not_followed(self):
        target = self.write('existing.json', b'preserve me')
        (self.root/'independent-check-v2.json').symlink_to(target)
        with self.assertRaises(FileExistsError):
            check.save_receipt({}, self.root)
        self.assertEqual(target.read_bytes(), b'preserve me')

    def test_cli_defaults_and_hash_dispatch_without_historical_execution(self):
        receipt = {'status': 'synthetic_only', 'coverage': {}}
        with mock.patch.object(check, 'verify', return_value=receipt) as verify:
            with contextlib.redirect_stdout(io.StringIO()) as stream:
                check.main(['--expected-sha', 'a'*64, '--primary-sha', 'b'*64, '--peer-sha', 'c'*64])
            self.assertEqual(json.loads(stream.getvalue()), receipt)
            verify.assert_called_once_with(check.HERE/'run-v2-01.json', check.HERE/'run-v2-02.json',
                                           'a'*64, {'primary': 'b'*64, 'peer': 'c'*64})

    def test_cli_requires_all_hashes(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                check.main(['--expected-sha', 'a'*64])

    def test_legacy_import_hash_checked_before_execution(self):
        path = self.write('bad.py', b'raise RuntimeError("must never execute")\n')
        with self.assertRaisesRegex(ValueError, 'prior independent checker changed'):
            check.import_legacy(path)

    def test_no_producer_import_or_legacy_global_assignment(self):
        tree = ast.parse(Path(check.__file__).read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = ([n.name for n in node.names] if isinstance(node, ast.Import)
                         else [node.module or ''])
                self.assertFalse(any(any(part in n for part in
                    ('assess', 'reader-', 'compare', 'calculate', 'adapter')) for n in names))
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                self.assertFalse(any(isinstance(t, ast.Attribute) and
                    isinstance(t.value, ast.Name) and t.value.id == 'old' for t in targets))


if __name__ == '__main__':
    unittest.main()


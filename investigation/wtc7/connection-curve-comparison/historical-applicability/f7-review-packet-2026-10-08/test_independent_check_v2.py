"""Synthetic-only dependency-repair gates; historical outputs are not loaded."""
import ast
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import independent_check_v2 as c


def fixture():
    required = {name: {'sha256': 'a'*64, 'bytes': 5} for name in c.MISSING_PRIOR}
    required['retained'] = {'sha256': 'b'*64, 'bytes': 8}
    candidate = {'slots': [{'human_accepted': False, 'native_x': '3/2'}],
                 'version': 2, 'status': 'pending', 'limits': 'synthetic only',
                 'inputs': {'retained': copy.deepcopy(required['retained'])}}
    candidate['inputs_after'] = copy.deepcopy(candidate['inputs'])
    actual = copy.deepcopy(candidate)
    actual['inputs'] = copy.deepcopy(required)
    actual['inputs_after'] = copy.deepcopy(required)
    return candidate, actual, required


class RepairControls(unittest.TestCase):
    def test_only_pin_maps_change_without_mutation(self):
        candidate, actual, required = fixture()
        before = c.encoded([candidate, actual, required])
        self.assertEqual(c.require_rejected_omissions(candidate, required), c.MISSING_PRIOR)
        c.require_dependency_only(actual, candidate, required)
        self.assertEqual(c.encoded([candidate, actual, required]), before)

    def test_every_required_pin_omission_rejected(self):
        candidate, actual, required = fixture()
        for name in required:
            damaged = copy.deepcopy(actual)
            del damaged['inputs'][name]
            damaged['inputs_after'] = copy.deepcopy(damaged['inputs'])
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'missing/changed'):
                c.require_dependency_only(damaged, candidate, required)

    def test_wrong_pin_and_wrong_type_rejected(self):
        for field, value in (('sha256', 'c'*64), ('bytes', 9), ('bytes', True)):
            candidate, actual, required = fixture()
            actual['inputs']['retained'][field] = value
            actual['inputs_after'] = copy.deepcopy(actual['inputs'])
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                c.require_dependency_only(actual, candidate, required)

    def test_extra_pin_rejected_even_when_all_required_present(self):
        candidate, actual, required = fixture()
        actual['inputs']['unreviewed'] = {'sha256': 'd'*64, 'bytes': 0}
        actual['inputs_after'] = copy.deepcopy(actual['inputs'])
        with self.assertRaisesRegex(ValueError, 'exactly the required'):
            c.require_dependency_only(actual, candidate, required)

    def test_every_non_input_field_preserved(self):
        for key, value in (('version', 3), ('status', 'accepted'), ('limits', 'less limited'),
                            ('slots', []), ('unreviewed', True)):
            candidate, actual, required = fixture()
            actual[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'non-input'):
                c.require_dependency_only(actual, candidate, required)
        candidate, actual, required = fixture()
        del actual['limits']
        with self.assertRaisesRegex(ValueError, 'non-input'):
            c.require_dependency_only(actual, candidate, required)

    def test_nested_mapping_and_human_changes_rejected(self):
        for field, value in (('native_x', '7/2'), ('human_accepted', True)):
            candidate, actual, required = fixture()
            actual['slots'][0][field] = value
            with self.assertRaisesRegex(ValueError, 'non-input'):
                c.require_dependency_only(actual, candidate, required)

    def test_before_after_mismatch_rejected_for_both_versions(self):
        candidate, actual, required = fixture()
        actual['inputs_after'] = {}
        with self.assertRaisesRegex(ValueError, 'before/after'):
            c.require_dependency_only(actual, candidate, required)
        candidate['inputs_after'] = {}
        with self.assertRaisesRegex(ValueError, 'before/after'):
            c.require_rejected_omissions(candidate, required)

    def test_original_failure_cannot_be_retroactively_repaired(self):
        candidate, _, required = fixture()
        candidate['inputs'][c.MISSING_PRIOR[0]] = required[c.MISSING_PRIOR[0]]
        candidate['inputs_after'] = copy.deepcopy(candidate['inputs'])
        with self.assertRaisesRegex(ValueError, 'four-pin failure'):
            c.require_rejected_omissions(candidate, required)

    def test_original_changed_or_additional_pin_rejected(self):
        for mode in ('changed', 'extra'):
            candidate, _, required = fixture()
            if mode == 'changed': candidate['inputs']['retained']['bytes'] += 1
            else: candidate['inputs']['unexpected'] = {'sha256': 'e'*64, 'bytes': 2}
            candidate['inputs_after'] = copy.deepcopy(candidate['inputs'])
            with self.assertRaisesRegex(ValueError, 'listed pins'):
                c.require_rejected_omissions(candidate, required)

    def test_new_repair_pin_roster_exact(self):
        self.assertEqual(set(c.REPAIR_PINS), {'DEPENDENCY-REPAIR.md', 'packet_v2.py',
                         'test_packet_v2.py', 'packet01.json', 'packet02.json'})
        self.assertEqual(c.REPAIR_PINS['packet01.json'], c.CANDIDATE_SHA)
        self.assertEqual(c.REPAIR_PINS['packet02.json'], c.CANDIDATE_SHA)
        self.assertEqual(c.REPAIR_PINS['DEPENDENCY-REPAIR.md'], c.REPAIR_SHA)

    def test_required_count_and_five_additions_synthetic_only(self):
        original = {f'synthetic-{i}': {'bytes': i, 'sha256': 'a'*64} for i in range(264)}
        def add(target, path, sha):
            target[path.name] = {'bytes': 1, 'sha256': sha}
        with mock.patch.object(c.previous, 'frozen_inputs', return_value=(original, {}, {}, {})), \
             mock.patch.object(c.old, 'add_pin', side_effect=add):
            required, prior = c.required_inputs()
        self.assertEqual(len(required), 269)
        self.assertEqual(len(prior), 264)
        for size in (263, 265):
            with mock.patch.object(c.previous, 'frozen_inputs',
                                   return_value=({str(i): {} for i in range(size)}, {}, {}, {})):
                with self.assertRaisesRegex(ValueError, '264'):
                    c.required_inputs()

    def test_alias_or_duplicate_addition_cannot_reduce_required_count(self):
        original = {f'synthetic-{i}': {} for i in range(264)}
        with mock.patch.object(c.previous, 'frozen_inputs', return_value=(original, {}, {}, {})), \
             mock.patch.object(c.old, 'add_pin', return_value=None):
            with self.assertRaisesRegex(ValueError, '269'):
                c.required_inputs()

    def test_import_guard_precedes_execution(self):
        with tempfile.TemporaryDirectory(prefix='f7-repair-import-') as directory:
            path = Path(directory)
            (path / 'independent_check.py').write_text('raise RuntimeError("do not execute")')
            (path / 'test_independent_check.py').write_text('synthetic')
            with self.assertRaisesRegex(ValueError, 'checker/test changed'):
                c.import_previous(path)

    def test_import_guard_checks_test_pin_too(self):
        with tempfile.TemporaryDirectory(prefix='f7-repair-test-pin-') as directory:
            path = Path(directory)
            # Saved independent code, not a producer; its test pin must pass before execution.
            (path / 'independent_check.py').write_bytes((c.HERE / 'independent_check.py').read_bytes())
            (path / 'test_independent_check.py').write_text('not the preserved test')
            with self.assertRaisesRegex(ValueError, 'test_independent_check.py'):
                c.import_previous(path)

    def test_exclusive_new_receipt_never_uses_original_name(self):
        with tempfile.TemporaryDirectory(prefix='f7-repair-receipt-') as directory:
            path = Path(directory)
            sentinel = path / 'independent-check.json'
            sentinel.write_bytes(b'preserved')
            saved = c.save_receipt({'synthetic': True}, path)
            self.assertEqual(saved.name, 'independent-check-v2.json')
            self.assertEqual(saved.read_bytes(), c.encoded({'synthetic': True}))
            with self.assertRaises(FileExistsError):
                c.save_receipt({}, path)
            self.assertEqual(sentinel.read_bytes(), b'preserved')

    def test_cli_uses_repaired_names_without_historical_execution(self):
        with mock.patch.object(c, 'verify', return_value={'status': 'synthetic'}) as verify, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            c.main(['--expected-sha', 'a'*64])
        verify.assert_called_once_with(c.HERE / 'packet-v2-01.json',
                                       c.HERE / 'packet-v2-02.json', 'a'*64)
        self.assertEqual(json.loads(output.getvalue()), {'status': 'synthetic'})

    def test_no_producer_import_or_previous_global_mutation(self):
        tree = ast.parse(Path(c.__file__).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse(any(n.name in ('packet', 'packet_v2', 'assess') for n in node.names))
            if isinstance(node, ast.ImportFrom):
                self.assertNotIn(node.module, ('packet', 'packet_v2', 'assess'))
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                self.assertFalse(any(isinstance(t, ast.Attribute) and
                    isinstance(t.value, ast.Name) and t.value.id in ('previous', 'old') for t in targets))


if __name__ == '__main__':
    unittest.main()

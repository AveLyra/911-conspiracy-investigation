"""Synthetic geometry and schema controls; not historical containment tests."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import screen


def entry(**changes):
    value = {'route': 'solid', 'column': 300, 'core_rows': [3, 4],
             'fringe_rows': [2, 5], 'status': 'identified_local_fragment',
             'note': 'Synthetic fixture.', 'fragment_id': 'one', 'boundary_flags': []}
    value.update(changes)
    return value


class GeometryTests(unittest.TestCase):
    def test_single_identifier_without_map(self):
        r = screen.classify(entry())
        self.assertTrue(r['eligible'])
        self.assertEqual(r['native_cell_rectangle'], [300, 2, 301, 6])

    def test_explicit_map(self):
        e = entry(fragment_membership={'one': {'core_rows': [3, 4], 'fringe_rows': [2, 5]}})
        self.assertTrue(screen.classify(e)['eligible'])

    def test_hole_is_not_filled(self):
        r = screen.classify(entry(fringe_rows=[2, 6]))
        self.assertEqual(r['reasons'], ['disconnected_outer'])
        self.assertIsNone(r['native_cell_rectangle'])

    def test_contiguous_multiple_members_are_not_merged(self):
        e = entry(fragment_id=None, fragment_membership={
            'a': {'core_rows': [3], 'fringe_rows': [2]},
            'b': {'core_rows': [4], 'fringe_rows': [5]}})
        self.assertEqual(screen.classify(e)['reasons'], ['missing_identifier', 'multiple_fragment_members'])

    def test_inconsistent_identity(self):
        e = entry(fragment_membership={'other': {'core_rows': [3, 4], 'fringe_rows': [2, 5]}})
        self.assertEqual(screen.classify(e)['reasons'], ['inconsistent_single_fragment_identity'])

    def test_all_reasons_preserved(self):
        e = entry(core_rows=[], fringe_rows=[0, 2], status='fringe_only', fragment_id=None,
                  boundary_flags=['strip_top'])
        self.assertEqual(screen.classify(e)['reasons'],
                         ['nonidentified_status', 'empty_core', 'disconnected_outer', 'boundary', 'missing_identifier'])

    def test_empty_not_zero_or_rectangle(self):
        e = entry(core_rows=[], fringe_rows=[], status='no_attributable_cells',
                  fragment_id=None, fragment_membership={})
        self.assertEqual(screen.classify(e)['reasons'],
                         ['nonidentified_status', 'empty_core', 'empty_outer', 'missing_identifier'])

    def test_other_statuses_and_target_boundary(self):
        for status in ('boundary_truncated', 'identity_conflict'):
            self.assertIn('nonidentified_status', screen.classify(entry(status=status))['reasons'])
        self.assertEqual(screen.classify(entry(column=270, boundary_flags=['target_left']))['reasons'], ['boundary'])

    def test_no_mutation_and_exact_summary(self):
        e = entry()
        original = copy.deepcopy(e)
        r = screen.classify(e)
        self.assertEqual(e, original)
        self.assertEqual(r['source_record'], original)
        self.assertEqual(screen.summarize([r])['all'],
                         {'entries': 1, 'eligible': 1, 'excluded': 0, 'reason_counts_nonexclusive': {}})

    def test_pinned_validator_negative_controls(self):
        validate = screen.validator()
        fixture = {'reader': 'synthetic',
                   'source_sha256': '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd',
                   'protocol_sha256': '12525bcb149368f18d85e3611f32137ccdeef723cc95df93cf2b5d9b13f2aa27',
                   'observations': [entry(route=r, column=x, core_rows=[], fringe_rows=[],
                                         status='no_attributable_cells', fragment_id=None)
                                    for r in ('solid', 'dash') for x in range(270, 360)]}
        self.assertEqual(len(validate(fixture)), 180)
        for changes in ({'core_rows': [True]}, {'core_rows': [88]}, {'core_rows': [2, 2]},
                        {'core_rows': [3, 2]}, {'core_rows': [2], 'fringe_rows': [2]},
                        {'core_rows': [0], 'fragment_id': 'one'},
                        {'core_rows': [2], 'fragment_membership': {}}):
            changed = copy.deepcopy(fixture)
            changed['observations'][1].update(changes)
            with self.assertRaises(ValueError):
                validate(changed)
        changed = copy.deepcopy(fixture)
        changed['observations'].pop()
        with self.assertRaises(ValueError):
            validate(changed)

    def test_overwrite_refused(self):
        with tempfile.TemporaryDirectory(prefix='annotation-screen-test-') as folder:
            target = Path(folder) / 'result.json'
            screen.save(target, {'synthetic': True})
            original = target.read_bytes()
            with self.assertRaises(FileExistsError):
                screen.save(target, {'replacement': True})
            with self.assertRaises(FileExistsError):
                screen.run(target)
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(json.loads(original), {'synthetic': True})


if __name__ == '__main__':
    unittest.main()

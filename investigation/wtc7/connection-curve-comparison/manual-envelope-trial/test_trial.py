"""Synthetic checks of annotation validation/scoring, not measurement validity."""
import copy
import unittest

import trial


def entry(x, core=None, fringe=None, status='identified'):
    return {'x': x, 'core': [4, 5] if core is None else core,
            'fringe': [] if fringe is None else fringe,
            'status': status, 'cue': 'invented control'}


def fixture(endpoints=(9, 11), support=True):
    reader = {'tiles': {'X': [entry(x) for x in trial.COLUMNS]},
              'refusals': {'R': {'answer': 'unresolved', 'reason': 'invented ambiguity'}}}
    truth = {'tiles': [{'id': 'X', 'columns': [
        {'x': x, 'support': support, 'endpoint_y2': list(endpoints)} for x in trial.COLUMNS]}],
        'refusals': [{'id': 'R'}]}
    return reader, truth


class TrialTests(unittest.TestCase):
    def test_contiguous_and_fringe(self):
        self.assertEqual(trial.envelope(entry(20)), [4, 6])
        self.assertEqual(trial.envelope(entry(20, [4], [5])), [4, 6])

    def test_unresolved_has_no_numeric_envelope(self):
        self.assertIsNone(trial.envelope(entry(20, [], [], 'unresolved')))
        self.assertIsNone(trial.envelope(entry(20, [4, 6], [], 'unresolved')))

    def test_reject_malformed_rows(self):
        for rows in [[], [4, 6], [4, 4], [5, 4], [True], [-1], [96], [4.0]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                trial.envelope(entry(20, rows))

    def test_reject_overlap_or_invalid_field(self):
        with self.assertRaises(ValueError):
            trial.envelope(entry(20, [4], [4]))
        for key, value in [('x', True), ('x', 21), ('status', 'accepted'), ('cue', '')]:
            item = entry(20); item[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                trial.envelope(item)

    def test_both_slopes_and_boundary_equality(self):
        for endpoints in [(8, 12), (12, 8), (9, 11), (11, 9)]:
            reader, truth = fixture(endpoints)
            result = trial.score(reader, truth)
            self.assertEqual(result['counts']['contained'], 6)
            self.assertTrue(result['method_passes_this_reader'])

    def test_midpoint_inside_whole_column_outside(self):
        reader, truth = fixture((7, 13))
        result = trial.score(reader, truth)
        self.assertEqual(result['counts']['containment_failure'], 6)
        self.assertFalse(result['method_passes_this_reader'])

    def test_gap_ink_is_false_admission(self):
        reader, truth = fixture(support=False)
        result = trial.score(reader, truth)
        self.assertEqual(result['counts']['false_admission'], 6)
        self.assertFalse(result['method_passes_this_reader'])

    def test_refusing_everything_is_not_pass(self):
        reader, truth = fixture()
        for item in reader['tiles']['X']:
            item['status'] = 'unresolved'
        result = trial.score(reader, truth)
        self.assertEqual(result['counts']['withheld'], 6)
        self.assertFalse(result['method_passes_this_reader'])

    def test_false_refusal_answer_fails(self):
        reader, truth = fixture()
        reader['refusals']['R']['answer'] = 'established'
        self.assertFalse(trial.score(reader, truth)['method_passes_this_reader'])

    def test_coverage_and_nonmutation(self):
        reader, truth = fixture()
        before = copy.deepcopy((reader, truth))
        trial.score(reader, truth)
        self.assertEqual((reader, truth), before)
        reader['tiles']['X'].pop()
        with self.assertRaises(ValueError):
            trial.score(reader, truth)


if __name__ == '__main__':
    unittest.main()

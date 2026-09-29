#!/usr/bin/env python3
"""Synthetic-only interval controls. No historical inputs or measurement CLI."""
import itertools
import unittest


def envelope(value):
    if value is None:
        return None
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise ValueError('invalid_envelope')
    low, high = value
    if type(low) is not int or type(high) is not int or not 0 <= low <= high <= 719:
        raise ValueError('invalid_envelope')
    return low, high


def difference(rt, bt, r0, b0):
    bounds = [envelope(v) for v in (rt, bt, r0, b0)]
    if any(v is None for v in bounds):
        return None
    rt, bt, r0, b0 = bounds
    return rt[0] - bt[1] - r0[1] + b0[0], rt[1] - bt[0] - r0[0] + b0[1]


def qualified_difference(rt, bt, r0, b0):
    """Each point is (identity_state, envelope); null is never zero."""
    points = (rt, bt, r0, b0)
    allowed = {'localizable', 'ambiguous', 'unlocalizable'}
    for state, bounds in points:
        if state not in allowed:
            raise ValueError('invalid_identity_state')
        envelope(bounds)
    if any(state != 'localizable' for state, _ in points):
        return None
    return difference(*(bounds for _, bounds in points))


def both_positive(first, second):
    return first is not None and second is not None and first[0] > 0 and second[0] > 0


def confirmed_runs(rows):
    """Return three-frame starts; require distinct increasing native indices."""
    indices = [row[0] for row in rows]
    if any(type(i) is not int for i in indices) or indices != sorted(set(indices)):
        raise ValueError('invalid_source_indices')
    return [rows[i][0] for i in range(len(rows) - 2)
            if rows[i + 1][0] == rows[i][0] + 1
            and rows[i + 2][0] == rows[i][0] + 2
            and all(both_positive(a, b) for _, a, b in rows[i:i + 3])]


class SyntheticControls(unittest.TestCase):
    def test_zero_singletons(self):
        self.assertEqual(difference((10, 10), (30, 30), (10, 10), (30, 30)), (0, 0))

    def test_common_translation(self):
        self.assertEqual(difference((17, 17), (37, 37), (10, 10), (30, 30)), (0, 0))

    def test_positive(self):
        self.assertEqual(difference((16, 18), (30, 32), (10, 12), (30, 32)), (2, 10))

    def test_zero_lower_bound_fails(self):
        self.assertFalse(both_positive((0, 8), (1, 9)))

    def test_reference_disagreement(self):
        self.assertFalse(both_positive((2, 8), (-1, 9)))

    def test_missing_each_operand(self):
        for i in range(4):
            values = [(10, 12)] * 4
            values[i] = None
            self.assertIsNone(difference(*values))
        self.assertFalse(both_positive(None, (1, 2)))

    def test_identity_loss(self):
        p = ('localizable', (10, 12))
        for state in ('ambiguous', 'unlocalizable'):
            self.assertIsNone(qualified_difference((state, (20, 22)), p, p, p))

    def test_bad_envelopes(self):
        for v in ((True, 2), (1.0, 2), (-1, 2), (4, 3), (1, 720), (1,), '1,2'):
            with self.assertRaises(ValueError):
                envelope(v)

    def test_bad_identity(self):
        p = ('localizable', (10, 12))
        with self.assertRaises(ValueError):
            qualified_difference(('probably', (10, 12)), p, p, p)

    def test_consecutive_and_nonconsecutive(self):
        p = (1, 3)
        self.assertEqual(confirmed_runs([(i, p, p) for i in (1, 5, 6, 7, 8)]), [5, 6])
        self.assertEqual(confirmed_runs([(i, p, p) for i in (1, 3, 5)]), [])

    def test_missing_middle(self):
        p = (1, 3)
        self.assertEqual(confirmed_runs([(5, p, p), (6, None, p), (7, p, p)]), [])

    def test_duplicate_or_reordered_indices(self):
        p = (1, 3)
        for indices in ((1, 1, 2), (2, 1, 3), (True, 2, 3)):
            with self.assertRaises(ValueError):
                confirmed_runs([(i, p, p) for i in indices])

    def test_independent_extrema_enumeration(self):
        choices = [(0, 0), (0, 2), (3, 5), (7, 7)]
        for bounds in itertools.product(choices, repeat=4):
            values = [r - b - r0 + b0 for r, b, r0, b0 in itertools.product(*bounds)]
            self.assertEqual(difference(*bounds), (min(values), max(values)))


if __name__ == '__main__':
    unittest.main()

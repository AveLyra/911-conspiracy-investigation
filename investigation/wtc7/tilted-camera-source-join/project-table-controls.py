#!/usr/bin/env python3
"""Synthetic controls only; run before accessing historical point coordinates."""
from fractions import Fraction as F
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('compare_project_table', Path(__file__).with_name('compare_project_table.py'))
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)


def saved(frame, time, value, key=True):
    nominal = subject.nearest_grid(F(time))
    return {'frame': frame, 'step': frame//6, 'saved_keyFrame_member': key,
            'source_row_xml_path': '/*[1]', 'source_coordinate_xml_paths': {'x': '/*[1]', 'y': '/*[1]'},
            'world': {'X': value, 'Y': value}, 'uniform_time_s': subject.rational(F(time)),
            'nominal_grid_time_s': subject.rational(nominal),
            'nominal_time_residual_s': subject.rational(F(time)-nominal),
            'printed_time_rounding_0_01s_compatible': abs(F(time)-nominal) <= F('0.005')}


class Controls(unittest.TestCase):
    def test_degree_quarter_turn_and_y_sign(self):
        self.assertAlmostEqual(subject.inverse(2, 6, 0, 0, 0, 2, 3)['Y'], -2)
        result = subject.inverse(2, 6, 0, 0, 90, 2, 3)
        self.assertAlmostEqual(result['X'], -2)
        self.assertAlmostEqual(result['Y'], -1)

    def test_unequal_scales_roundtrip_separate_forward_matrix(self):
        for angle in [0, 30, -2.5913472025433153, 90]:
            for X, Y in [(2, 5), (-1, 3), (0, 0)]:
                c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
                x, y = 7+2*c*X-2*s*Y, -4-3*s*X-3*c*Y
                result = subject.inverse(x, y, 7, -4, angle, 2, 3)
                self.assertAlmostEqual(result['X'], X, places=12)
                self.assertAlmostEqual(result['Y'], Y, places=12)

    def test_uniform_clock_and_irregular_endpoint_clock_differ(self):
        self.assertEqual(subject.uniform_clock(1, F(30), F(0)), F('0.03'))
        self.assertEqual(subject.endpoint_clock(1, [F(0), F(10), F(100)], 0, 2, F(30), F(0)), F('0.006'))
        self.assertEqual(subject.endpoint_clock(2, [F(0), F(10), F(100)], 0, 2, F(30), F(0)), F('0.06'))

    def test_loaded_endpoint_not_full_video_final_frame(self):
        times = [F(0), F(10), F(100), F(101)]
        self.assertEqual(subject.endpoint_clock(1, times, 0, 2, F(30), F(0)), F('0.006'))
        self.assertNotEqual(subject.endpoint_clock(1, times, 0, 2, F(30), F(0)), subject.endpoint_clock(1, times, 0, 3, F(30), F(0)))

    def test_uniform_pts_stretch_agrees_with_uniform_assignment(self):
        times = [F(7)+i*F('33.333') for i in range(5)]
        for i in range(4):
            self.assertEqual(subject.endpoint_clock(i, times, 0, 3, F('33.4'), F(-2020)), subject.uniform_clock(i, F('33.4'), F(-2020)))

    def test_negative_time_and_half_grid_ties(self):
        for value, expected in [('-0.1', '-0.2'), ('0.1', '0.2'), ('-0.3', '-0.4'), ('0.3', '0.4'), ('-0.099', '0'), ('-2.02', '-2'), ('12.7948', '12.8')]:
            self.assertEqual(subject.nearest_grid(F(value)), F(expected))

    def test_print_enclosures_and_separate_tolerance(self):
        for width in [F('0.005'), F('0.010')]:
            for sign in [-1, 1]:
                self.assertTrue(subject.enclosure(sign*float(width), width)['print_enclosure_compatible'])
                boundary = subject.enclosure(sign*float(width+F('0.0000000005')), width)
                self.assertFalse(boundary['print_enclosure_compatible'])
                self.assertTrue(boundary['with_arithmetic_tolerance_compatible'])
                self.assertFalse(subject.enclosure(sign*float(width+F('0.000000002')), width)['with_arithmetic_tolerance_compatible'])

    def test_sparse_rows_and_blanks_retained_with_no_fill(self):
        rows = [saved(0, '0', 2, False), saved(12, '0.4', 4), saved(18, '0.6', 6)]
        paper = [{'row': 1, 'time_s': '0.0', 'ref_x': '1'}, {'row': 2, 'time_s': '0.2', 'ref_x': '2'}, {'row': 3, 'time_s': '0.4', 'ref_x': None}]
        result = subject.join_pair('synthetic01', rows, paper, 'X', 'ref_x', 'synthetic')
        self.assertEqual(result['counts']['shared_finite_nominal_time'], 1)
        self.assertEqual(result['counts']['published_row_missing_saved'], 1)
        self.assertEqual(result['counts']['published_cell_missing'], 1)
        self.assertEqual(result['counts']['saved_row_outside_published_times'], 1)
        self.assertEqual(result['counts']['shared_finite_nonkey_rows'], 1)
        self.assertEqual(result['baseline']['original_saved_minus_printed_offset'], 1)

    def test_first_shared_finite_baseline_and_offset_diagnostic(self):
        rows = [saved(0, '0', 100), saved(6, '0.2', 12), saved(12, '0.4', 14)]
        paper = [{'row': 1, 'time_s': '0.0', 'ref_x': None}, {'row': 2, 'time_s': '0.2', 'ref_x': '2'}, {'row': 3, 'time_s': '0.4', 'ref_x': '4'}]
        result = subject.join_pair('synthetic01', rows, paper, 'X', 'ref_x', 'synthetic')
        self.assertEqual(result['baseline']['frame'], 6)
        self.assertEqual(result['baseline']['original_saved_minus_printed_offset'], 10)
        self.assertFalse(result['absolute_summary']['all_available_compatible'])
        self.assertTrue(result['displacement_summary']['all_available_compatible'])

    def test_no_overlap_has_no_baseline(self):
        result = subject.join_pair('synthetic01', [saved(0, '0', 2)], [{'row': 1, 'time_s': '1', 'ref_x': '2'}], 'X', 'ref_x', 'synthetic')
        self.assertIsNone(result['baseline'])
        self.assertFalse(result['displacement_summary']['all_available_compatible'])
        self.assertIsNone(result['absolute_summary']['maximum_absolute_residual'])

    def test_nominal_join_does_not_clear_strict_time(self):
        result = subject.join_pair('synthetic01', [saved(0, '-0.02', 2)], [{'row': 1, 'time_s': '0', 'ref_x': '2'}], 'X', 'ref_x', 'synthetic')
        self.assertTrue(result['absolute_summary']['all_available_compatible'])
        self.assertEqual(result['counts']['shared_finite_printed_time_0_01s_compatible'], 0)
        self.assertEqual(result['complete_row_compatibility']['absolute_position_and_strict_printed_time_count'], 0)

    def test_ambiguous_grid_is_not_silently_joined(self):
        with self.assertRaisesRegex(ValueError, 'ambiguous_saved_grid_join'):
            subject.join_pair('synthetic01', [saved(0, '0', 2), saved(1, '0.01', 3)], [], 'X', 'ref_x', 'synthetic')

    def test_keyframe_flags_survive_conversion(self):
        coordinates = {axis: {'occurrences': [{'xml_path': '/*[1]', 'saved_text': '2.0', 'value': 2.0}]} for axis in ['x', 'y']}
        track = {'framedata': [{'duplicate_indices': [], 'rows': [{'finite_complete': True, 'index': 0, 'saved_keyFrame_member': False, 'xml_path': '/*[1]', 'objects': [{'coordinates': coordinates}]}]}]}
        result = subject.convert_rows(track, {'xo': 0, 'yo': 0, 'degrees': 0, 'sx': 1, 'sy': 1}, F(30), F(0), [F(0), F(30)], 0, 1, 1)
        self.assertEqual(len(result), 1)
        self.assertIs(result[0]['saved_keyFrame_member'], False)


if __name__ == '__main__':
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    print(json.dumps({'status': 'pass' if result.wasSuccessful() else 'fail', 'tests_run': result.testsRun,
                      'failures': [test.id() for test, _ in result.failures],
                      'errors': [test.id() for test, _ in result.errors],
                      'scope': 'synthetic_only_before_historical_calculation'}, sort_keys=True))
    if not result.wasSuccessful():
        print(stream.getvalue(), file=sys.stderr)
        sys.exit(1)

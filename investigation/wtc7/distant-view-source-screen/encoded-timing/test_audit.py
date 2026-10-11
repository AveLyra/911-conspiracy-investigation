#!/usr/bin/env python3
"""Synthetic controls only. Importing audit never probes or reads historical inputs."""
import copy
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import audit


def fixture():
    source = b'abcdefghijkl'
    frames = [dict(type='frame', stream_index=0, width=4, height=2, pix_fmt='yuv420p',
                   pict_type=kind, key_frame=int(kind == 'I'), duration=1, pkt_pos=str(i * 3),
                   pts=i, pkt_dts=i, best_effort_timestamp=i)
              for i, kind in enumerate(('I', 'B', 'P', 'B'))]
    packets = [dict(type='packet', stream_index=0, pos=str(i * 3), size='3',
                    pts=i, dts=i, duration=1, flags='K_' if i == 0 else '__',
                    data_hash='SHA256:' + audit.sha(source[i * 3:i * 3 + 3])) for i in range(4)]
    return {'streams': [dict(index=0, codec_type='video', codec_name='mpeg4',
                             width=4, height=2, pix_fmt='yuv420p', time_base='1/30')],
            'frames': frames, 'packets': packets}, source


def wrapped(records):
    return [{'ordinal': i, 'record': row} for i, row in enumerate(records)]


class MetadataControls(unittest.TestCase):
    def test_combined_and_separate_ordinals_preserve_raw_type(self):
        data, source = fixture()
        combined = {'streams': data['streams'], 'packets_and_frames': [
            data['packets'][0], data['packets'][1], data['frames'][0], data['frames'][1],
            data['packets'][2], data['frames'][2], data['packets'][3], data['frames'][3]]}
        result = audit.analyze_arm(combined, source)
        self.assertEqual(result, audit.analyze_arm(data, source))
        self.assertEqual([r['ordinal'] for r in result['frames']], list(range(4)))
        self.assertEqual(result['frames'][0]['record']['type'], 'frame')
        self.assertEqual(result['packets'][0]['record']['type'], 'packet')

    def test_ambiguous_or_malformed_shape_rejected(self):
        data, _ = fixture()
        data['packets_and_frames'] = []
        with self.assertRaises(ValueError):
            audit.split_probe(data)
        del data['frames'], data['packets']
        data['packets_and_frames'] = [{'type': 'subtitle'}]
        with self.assertRaises(ValueError):
            audit.split_probe(data)

    def test_null_zero_omission_and_negative_preserved(self):
        rows = wrapped([{'pts': 0}, {'pts': None}, {}, {'pts': -2}])
        result = audit.timestamp_summary(rows, 'pts', Fraction(1, 30))
        self.assertEqual(result['missing_ordinals'], [1, 2])
        self.assertEqual(result['null_ordinals'], [1])
        self.assertEqual(result['absent_ordinals'], [2])
        self.assertEqual(result['pairs'][0], dict(from_ordinal=0, to_ordinal=3, ordinal_gap=3,
                         from_value=0, to_value=-2, delta=-2, delta_seconds_exact='-1/15',
                         delta_per_ordinal_exact='-2/3'))
        self.assertFalse(result['known_pairs_positive'])
        self.assertFalse(result['all_ordinals_present'])

    def test_malformed_timestamps_rejected(self):
        for value in ('0', 'N/A', 1.0, True, [], {}):
            data, _ = fixture()
            data['frames'][0]['pts'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                audit.split_probe(data)
        data, _ = fixture()
        data['packets'][0]['dts'] = '1'
        with self.assertRaises(ValueError):
            audit.split_probe(data)

    def test_json_duplicates_and_nonfinite_rejected(self):
        for value in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}'):
            with self.assertRaises(ValueError):
                audit.load_json(value)

    def test_gaps_irregular_nonmonotone_and_zero_deltas(self):
        rows = wrapped([{'pts': 0}, {}, {'pts': 4}, {'pts': 5}, {'pts': 5}, {'pts': 3}])
        result = audit.timestamp_summary(rows, 'pts', Fraction(1, 25))
        self.assertEqual([p['delta'] for p in result['pairs']], [4, 1, 0, -2])
        self.assertEqual([p['ordinal_gap'] for p in result['pairs']], [2, 1, 1, 1])
        self.assertEqual(len(result['gap_pairs']), 1)
        self.assertEqual(len(result['adjacent_pairs']), 3)
        self.assertFalse(result['constant_delta_per_ordinal_on_known_pairs'])
        self.assertFalse(result['known_pairs_positive'])

    def test_regular_only_on_known_labels_does_not_fill_gap(self):
        rows = wrapped([{'pts': 0}, {}, {'pts': 2}, {'pts': 3}])
        result = audit.timestamp_summary(rows, 'pts', Fraction(1, 30))
        self.assertTrue(result['constant_delta_per_ordinal_on_known_pairs'])
        self.assertEqual(result['missing_ordinals'], [1])
        self.assertEqual(result['delta_counts'], {'1': 1, '2': 1})
        self.assertEqual(result['delta_per_ordinal_counts'], {'1': 2})
        self.assertIsNone(audit.timestamp_summary(wrapped([{}]), 'pts', Fraction(1))['known_pairs_positive'])

    def test_tabs_and_selected_bounds_keep_original_ordinals(self):
        data, source = fixture()
        data['frames'] = [dict(data['frames'][i % 4]) for i in range(413)]
        for i, row in enumerate(data['frames']):
            row['pts'] = i if i % 2 else None
            row['best_effort_timestamp'] = None if i == 300 else i
        result = audit.analyze_arm(data, source)
        selected = result['frame_summaries']['selected_274_411']
        self.assertEqual(selected['ordinals'], list(range(274, 412)))
        self.assertEqual(selected['count'], 138)
        self.assertEqual(selected['timestamps']['best_effort_timestamp']['missing_ordinals'], [300])
        tabs = selected['picture_type_tabs']
        self.assertEqual(sum(r['count'] for r in tabs.values()), 138)
        self.assertEqual(tabs['B']['pts_present'], 69)
        self.assertEqual(tabs['I']['pts_missing'] + tabs['P']['pts_missing'], 69)

    def test_zero_unique_multiple_and_unknown_joins(self):
        data, source = fixture()
        data['packets'][1]['pos'] = '0'
        data['frames'][2]['pkt_pos'] = None
        data['frames'][3]['pkt_pos'] = '-1'
        data['frames'].append(dict(data['frames'][0], pkt_pos='9'))
        result = audit.analyze_arm(data, source)
        self.assertEqual([r['disposition'] for r in result['joins']],
                         ['multiple', 'zero', 'zero', 'zero', 'unique'])
        self.assertEqual(result['joins'][0]['packet_ordinals'], [0, 1])
        self.assertFalse(result['packet_summary']['known_nonnegative_positions_unique'])
        self.assertEqual(result['joins'][3]['reason'], 'negative_position')

    def test_payload_valid_mismatch_missing_malformed_and_bounds(self):
        data, source = fixture()
        data['packets'][1]['data_hash'] = 'SHA256:' + '0' * 64
        data['packets'][2]['size'] = '99'
        data['packets'][3]['pos'] = None
        result = audit.analyze_arm(data, source)['payload_checks']
        self.assertTrue(result[0]['hash_matches'])
        self.assertFalse(result[1]['hash_matches'])
        self.assertEqual(result[2]['range_status'], 'out_of_bounds')
        self.assertEqual(result[3]['range_status'], 'missing')
        self.assertIsNone(result[2]['computed_sha256'])
        for pos, size, expected in (('-1', '1', 'out_of_bounds'), ('0', '-1', 'out_of_bounds'),
                                    ('12', '0', 'valid'), ('13', '0', 'out_of_bounds')):
            data['packets'] = [dict(data['packets'][0], pos=pos, size=size, data_hash='bad')]
            check = audit.analyze_arm(data, source)['payload_checks'][0]
            self.assertEqual(check['range_status'], expected)
            self.assertEqual(check['hash_status'], 'malformed')
        data['packets'][0].pop('data_hash')
        self.assertEqual(audit.analyze_arm(data, source)['payload_checks'][0]['hash_status'], 'missing')

    def test_packet_dts_missing_and_duplicate_are_results(self):
        data, source = fixture()
        data['packets'][1]['dts'] = None
        data['packets'][3]['dts'] = 2
        data['packets'][1]['pos'] = None
        data['packets'][3]['pos'] = '-1'
        result = audit.analyze_arm(data, source)['packet_summary']
        self.assertEqual(result['dts']['missing_ordinals'], [1])
        self.assertEqual([p['delta'] for p in result['dts']['pairs']], [2, 0])
        self.assertEqual(result['missing_position_ordinals'], [1])
        self.assertEqual(result['negative_position_ordinals'], [3])
        self.assertEqual(result['null_counts']['pos'], 1)

    def test_all_arm_changes_and_separate_identity_changes(self):
        left, source = fixture()
        right = copy.deepcopy(left)
        right['frames'][0]['pts'] = 20
        right['frames'][1]['pict_type'] = 'P'
        right['frames'][2]['pkt_pos'] = '9'
        right['packets'][0]['data_hash'] = 'SHA256:' + '0' * 64
        result = audit.analyze(left, right, [], source)['arm_differences']
        self.assertEqual(len(result['all']), 4)
        self.assertEqual(len(result['identity']), 3)
        self.assertNotIn('pts', [r['field'] for r in result['identity']])
        right['frames'].pop()
        result = audit.analyze(left, right, [], source)['arm_differences']
        self.assertIn('__record__', [r['field'] for r in result['identity']])

    def test_presence_type_and_nested_differences(self):
        left, _ = fixture()
        right = copy.deepcopy(left)
        right['streams'][0]['side_data_list'] = [{'rotation': 90}]
        right['frames'][0]['key_frame'] = True
        right['frames'][1]['new_field'] = None
        result = audit.differences(left, right)
        self.assertEqual({r['field'] for r in result}, {'side_data_list', 'key_frame', 'new_field'})
        presence = next(r for r in result if r['field'] == 'new_field')
        self.assertFalse(presence['left_present'])
        self.assertTrue(presence['right_present'])

    def test_baseline_compares_only_old_requested_fields(self):
        fresh, source = fixture()
        old = copy.deepcopy(fresh)
        old['packets'] = []
        for frame in old['frames']:
            frame.pop('type')
            frame.pop('pkt_pos')
            frame.pop('pkt_dts')
        self.assertEqual(audit.analyze(fresh, fresh, [('prior', old)], source)
                         ['baseline_comparisons'][0]['differences'], [])
        old['frames'][0].pop('pts')
        old['streams'][0]['width'] = 8
        result = audit.analyze(fresh, fresh, [('prior', old)], source)['baseline_comparisons'][0]
        self.assertEqual({r['field'] for r in result['differences']}, {'width', 'pts'})
        self.assertEqual(result['baseline_path'], 'prior')


class PreservationControls(unittest.TestCase):
    def test_argv_only_genpts_difference_and_no_media_output(self):
        default = audit.probe_argv()
        generated = audit.probe_argv(True)
        del generated[3:5]
        self.assertEqual(default, generated)
        self.assertIn('-show_packets', default)
        self.assertIn('-show_frames', default)
        self.assertIn('-show_data_hash', default)
        self.assertEqual(default[-1], str(audit.SOURCE))
        self.assertNotIn('-read_intervals', default)

    def test_output_name_existing_directory_file_and_symlink_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            for name in ('../run01', '/tmp/run01', 'run03', '.', 'run01/nested'):
                with self.assertRaises(ValueError):
                    audit.output_directory(name, parent)
            audit.output_directory('run01', parent)
            with self.assertRaises(FileExistsError):
                audit.output_directory('run01', parent)
            (parent / 'run02').symlink_to(parent / 'missing')
            with self.assertRaises(FileExistsError):
                audit.output_directory('run02', parent)

    def test_exclusive_json_write_and_strict_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'fixture.json'
            audit.dump(path, {'value': 0})
            before = path.read_bytes()
            with self.assertRaises(FileExistsError):
                audit.dump(path, {'value': 1})
            self.assertEqual(path.read_bytes(), before)
            link = Path(tmp) / 'link'
            link.symlink_to(path)
            with self.assertRaises(ValueError):
                audit.pin(link)

    def test_real_synthetic_nonzero_diagnostics_retained_before_parsing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'nonzero'
            argv = [sys.executable, '-c', 'import sys;sys.stdout.write("{bad");sys.stderr.write("warning");sys.exit(3)']
            result = audit.capture(path, argv)
            self.assertEqual(result['returncode'], 3)
            self.assertFalse(result['analysis_eligible'])
            self.assertEqual((path / 'stdout.json').read_bytes(), b'{bad')
            self.assertEqual((path / 'stderr.bin').read_bytes(), b'warning')
            self.assertEqual(json.loads((path / 'execution.json').read_bytes())['argv'], argv)

    def test_timeout_partial_stdout_and_stderr_retained(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch('audit.TIMEOUT', 0.1):
            path = Path(tmp) / 'timeout'
            argv = [sys.executable, '-u', '-c',
                    'import sys,time;sys.stdout.write("partial");sys.stdout.flush();sys.stderr.write("pending");sys.stderr.flush();time.sleep(3)']
            result = audit.capture(path, argv)
            self.assertEqual(result['status'], 'timeout')
            self.assertFalse(result['analysis_eligible'])
            self.assertEqual((path / 'stdout.json').read_bytes(), b'partial')
            self.assertEqual((path / 'stderr.bin').read_bytes(), b'pending')

    def test_oversized_complete_outputs_retained(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch('audit.OUTPUT_LIMIT', 5), \
                mock.patch('audit.subprocess.run', return_value=SimpleNamespace(returncode=0, stdout=b'1234', stderr=b'56')):
            path = Path(tmp) / 'oversize'
            result = audit.capture(path, ['synthetic'])
            self.assertTrue(result['oversized'])
            self.assertFalse(result['analysis_eligible'])
            self.assertEqual((path / 'stdout.json').read_bytes(), b'1234')
            self.assertEqual((path / 'stderr.bin').read_bytes(), b'56')

    def test_warning_and_launch_error_are_retained_not_waived(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch('audit.subprocess.run', return_value=SimpleNamespace(returncode=0, stdout=b'{}', stderr=b'notice')):
                warning = audit.capture(Path(tmp) / 'warning', ['synthetic'])
            self.assertTrue(warning['warning_review_required'])
            self.assertFalse(warning['analysis_eligible'])
            with mock.patch('audit.subprocess.run', side_effect=OSError('synthetic launch failure')):
                error = audit.capture(Path(tmp) / 'error', ['synthetic'])
            self.assertEqual(error['status'], 'launch_error')
            self.assertEqual(error['stdout']['bytes'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)

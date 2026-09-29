#!/usr/bin/env python3
"""Fixed R1 replication adapter; no image processing or parameter selection."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import re
import unittest

import interval_controls as arithmetic

HERE = Path(__file__).resolve().parent
FRAMES = (239, 434, 441, 442, 443, 444)
FEATURES = ('R1', 'B1', 'B2')
PINS = {
    'PROTOCOL.md': '2bbc5777dd39dde42a2945d1d049a1a46f8c4b61678308e328e803f0ffa2331a',
    'EXECUTION-2026-09-27.md': '16533732f0d4a9e02b295d46398e5c5fbe8b04f9250dd2eb8130c3373fd86f1f',
    'root-observations.md': 'd8d9bfb77b51780e1cef47e7a41577509d37bbfbd7189667e2eb69693fb51352',
    'observer-observations.md': '240a1849e927bebb38803037cc28253132186ddb5049577bab467d7e1769846d',
    'human-observations-2026-09-26.md': 'c7714d0abad6d9806a9f3f4a80abacdf9f6404b6ad11cc59b26b2429e45c842d',
    'interval_controls.py': '19de6bc2227005053397a1d3c26d9a1920108a0759bada60d22e4ee036c840a0',
}
MAP_PIN = '14c72246559d79812c1eef4b42d977c64d1f28bc97d0f034a945cddb8db5561a'
PTS_PIN = 'd8496f26d271eda8955e0fc46b3ff98754c2b5bc06793e8729adf0840a387c3b'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_ai(text):
    parts = re.split(r'^## Frame (\d+)\s*$', text, flags=re.M)
    indices = tuple(int(parts[i]) for i in range(1, len(parts), 2))
    require(indices == FRAMES, 'annotation_frame_contract')
    result = {}
    for i, frame in zip(range(1, len(parts), 2), indices):
        matches = re.findall(r'^\| ([A-Z]\d+) \| ([^|]+) \| ([^|]+) \|',
                             parts[i + 1], flags=re.M)
        require(tuple(row[0] for row in matches) == FEATURES, 'annotation_feature_contract')
        result[frame] = {}
        for feature, state, raw in matches:
            state, raw = state.strip(), raw.strip()
            require(state in ('localizable', 'ambiguous', 'unlocalizable'), 'annotation_state')
            if raw == 'null':
                bounds = None
            else:
                match = re.fullmatch(r'\[(\d+), (\d+)\]', raw)
                require(match is not None, 'annotation_bounds_syntax')
                bounds = arithmetic.envelope(tuple(map(int, match.groups())))
            result[frame][feature] = (state, bounds)
    return result


def parse_human(text):
    rows = re.findall(r'^\| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$',
                      text, flags=re.M)
    rows = [tuple(map(int, row)) for row in rows]
    require(tuple(row[0] for row in rows) == FRAMES, 'human_frame_contract')
    points, result = {}, {}
    for frame, *xy in rows:
        points[frame], result[frame] = {}, {}
        for k, feature in enumerate(FEATURES):
            x, y = xy[2*k:2*k+2]
            require(0 <= x <= 1279 and 0 <= y <= 719, 'human_coordinate_bounds')
            bounds = arithmetic.envelope((y - 1, y + 1))
            points[frame][feature] = [x, y]
            result[frame][feature] = ('localizable', bounds)
    return result, points


def clocks(mapping, inventory):
    require(len(mapping) == 242, 'selected_map_length')
    require([row['source_index'] for row in mapping] == list(range(239, 481)), 'selected_map_indices')
    require(len(inventory['frames']) == 1350, 'whole_inventory_length')
    result = {}
    for frame in FRAMES:
        row = mapping[frame - 239]
        original = inventory['frames'][frame]
        require(type(row['source_pts']) is int, 'integer_pts')
        require(row['source_pts'] == original['pts'] == original['best_effort_timestamp'], 'pts_join')
        require(row['source_time_base'] == '1/30000', 'time_base')
        t = Fraction(row['source_pts']) * Fraction(row['source_time_base'])
        require(t == Fraction(row['source_seconds_exact']), 'exact_time_join')
        result[frame] = {'source_pts': row['source_pts'], 'time_base': row['source_time_base'],
                         'seconds_exact': str(t), 'png': row['png'], 'png_sha256': row['sha256']}
    baseline = Fraction(result[239]['seconds_exact'])
    for row in result.values():
        row['seconds_from_baseline_exact'] = str(Fraction(row['seconds_exact']) - baseline)
    return result


def evaluate(annotations, time_rows):
    output, helper_rows = [], []
    for frame in FRAMES[1:]:
        by_reference = {}
        for ref in ('B1', 'B2'):
            value = arithmetic.qualified_difference(annotations[frame]['R1'], annotations[frame][ref],
                                                    annotations[239]['R1'], annotations[239][ref])
            by_reference[ref] = list(value) if value is not None else None
        positive = arithmetic.both_positive(by_reference['B1'], by_reference['B2'])
        status = ('unresolved' if any(v is None for v in by_reference.values()) else
                  'positive_both' if positive else 'non_detection')
        output.append({'source_index': frame, 'clock': time_rows[frame],
                       'intervals_px': by_reference, 'positive_both': positive, 'status': status})
        helper_rows.append((frame, by_reference['B1'], by_reference['B2']))
    triplets = []
    for i in range(len(output) - 2):
        rows = output[i:i+3]
        indices = [row['source_index'] for row in rows]
        consecutive = indices == list(range(indices[0], indices[0] + 3))
        triplets.append({'source_indices': indices, 'consecutive': consecutive,
                         'confirmed': consecutive and all(row['positive_both'] for row in rows)})
    starts = arithmetic.confirmed_runs(helper_rows)
    require(starts == [t['source_indices'][0] for t in triplets if t['confirmed']], 'triplet_consistency')
    return {'annotations': annotations, 'comparisons': output, 'triplets': triplets,
            'confirmed_run_starts': starts}


def synthetic_ai():
    return '\n'.join(f'## Frame {f}\n' + '\n'.join(
        f'| {feature} | localizable | [10, 12] | synthetic |' for feature in FEATURES) for f in FRAMES)


def synthetic_human():
    return '\n'.join(f'| {f} | 20 | 10 | 30 | 10 | 40 | 10 |' for f in FRAMES)


class AdapterControls(unittest.TestCase):
    def test_ai_exact_contract(self):
        self.assertEqual(tuple(parse_ai(synthetic_ai())), FRAMES)

    def test_ai_missing_duplicate_and_wrong_frames(self):
        s = synthetic_ai()
        for altered in (s.replace('## Frame 239', '## Frame 238'), s + '\n## Frame 444',
                        s.replace('| B2 | localizable | [10, 12] | synthetic |', '', 1)):
            with self.assertRaises(ValueError):
                parse_ai(altered)

    def test_ai_invalid_state_and_bounds(self):
        for a, b in (('localizable', 'likely'), ('[10, 12]', '[12, 10]'),
                     ('[10, 12]', '[10, 720]'), ('B2', 'R2')):
            with self.assertRaises(ValueError):
                parse_ai(synthetic_ai().replace(a, b, 1))

    def test_null_and_ambiguous_preserved(self):
        a = parse_ai(synthetic_ai().replace('localizable | [10, 12]', 'ambiguous | null', 1))
        self.assertEqual(a[239]['R1'], ('ambiguous', None))

    def test_human_radius_and_coverage(self):
        a, points = parse_human(synthetic_human())
        self.assertEqual(a[239]['R1'], ('localizable', (9, 11)))
        self.assertEqual(points[239]['R1'], [20, 10])

    def test_human_bad_coverage_and_bounds(self):
        s = synthetic_human()
        for altered in (s.replace('| 239 |', '| 238 |', 1), s + '\n' + s.splitlines()[0],
                        s.replace('| 20 | 10 |', '| 1280 | 10 |', 1),
                        s.replace('| 20 | 10 |', '| 20 | 0 |', 1)):
            with self.assertRaises(ValueError):
                parse_human(altered)

    def test_full_pipeline_zero_and_missing(self):
        a = parse_ai(synthetic_ai())
        times = {f: {'synthetic': True} for f in FRAMES}
        out = evaluate(a, times)
        self.assertEqual(len(out['comparisons']), 5)
        self.assertEqual(out['confirmed_run_starts'], [])
        self.assertTrue(all(r['intervals_px']['B1'] == [-4, 4] for r in out['comparisons']))
        a[239]['R1'] = ('ambiguous', None)
        self.assertTrue(all(r['status'] == 'unresolved' for r in evaluate(a, times)['comparisons']))


def run_controls():
    suite = unittest.TestSuite((unittest.defaultTestLoader.loadTestsFromTestCase(arithmetic.SyntheticControls),
                               unittest.defaultTestLoader.loadTestsFromTestCase(AdapterControls)))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    require(result.wasSuccessful(), 'controls_failed')
    return result.testsRun


def calculate():
    pins = {}
    for name, expected in PINS.items():
        pins[name] = digest(HERE / name)
        require(pins[name] == expected, 'input_pin:' + name)
    source_note = HERE / 'numerical-source-recheck.md'
    require(source_note.is_file(), 'source_recheck_not_saved')
    pins[source_note.name] = digest(source_note)
    pins[Path(__file__).name] = digest(Path(__file__))
    source = HERE.parent / 'comparator-roof-onset' / 'run02'
    for name, expected in (('comparator-selected.json', MAP_PIN), ('comparator-all-frame-pts.json', PTS_PIN)):
        pins['../comparator-roof-onset/run02/' + name] = digest(source / name)
        require(digest(source / name) == expected, 'clock_pin:' + name)
    time_rows = clocks(json.loads((source / 'comparator-selected.json').read_text()),
                       json.loads((source / 'comparator-all-frame-pts.json').read_text()))
    human, points = parse_human((HERE / 'human-observations-2026-09-26.md').read_text())
    arms = {'ai_root': parse_ai((HERE / 'root-observations.md').read_text()),
            'ai_observer': parse_ai((HERE / 'observer-observations.md').read_text()), 'human': human}
    results = {name: evaluate(a, time_rows) for name, a in arms.items()}
    require(sum(len(a['comparisons']) for a in results.values()) == 15, 'comparison_coverage')
    return {'schema': 'r1-declared-replication-v1', 'python': platform.python_version(), 'input_pins': pins,
            'units': 'native downward y pixels; encoded PTS seconds only',
            'limits': 'Set enclosures, not statistical confidence. No physical onset/stationarity/cause inference.',
            'baseline_source_index': 239, 'clocks': time_rows, 'human_reported_points': points, 'arms': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--controls', action='store_true')
    mode.add_argument('--output', type=Path)
    args = parser.parse_args()
    count = run_controls()  # Always before opening historical annotation inputs.
    if args.controls:
        return
    require(not args.output.exists(), 'output_already_exists')
    result = calculate()
    result['synthetic_tests_passed'] = count
    encoded = json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + '\n'
    with args.output.open('x', encoding='utf-8') as stream:
        stream.write(encoded)
    print(json.dumps({'output': str(args.output), 'sha256': digest(args.output), 'intervals': 30}))


if __name__ == '__main__':
    main()

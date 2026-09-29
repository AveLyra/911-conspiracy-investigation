#!/usr/bin/env python3
"""Frozen-grid foreground texture diagnostic, not a camera calibration."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import sys
import time

import numpy as np
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
INDICES = [258] + list(range(288, 349, 3))
REFERENCES = [('R1', 272, 400), ('R2', 168, 348), ('R3', 673, 292)]
SIDES = (21, 31)
OFFSETS = list(range(-6, 7))
PINS = {
    'protocol': ('PROTOCOL.md', '7b13e006ab382121452f6e7c59f37d7f586b57f297a7e1c7154b86b2aae06c2f'),
    'preflight': ('reference-preflight.md', '7417b2600ec7ca6f4a1464a7ee918bceb23962d09d3ea8708b8565b49cf73015'),
    'preparation_code': ('prepare.py', '0b7baeb81236a7ab8fdb5435ed7d86e10c754e22fd35f94051d96538ae29d139'),
    'views_receipt': ('views01/receipt.json', '8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161'),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': digest(data)}


def write_json(path, data):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def patch(array, cx, cy, side):
    h = side // 2
    answer = array[cy-h:cy+h+1, cx-h:cx+h+1]
    if answer.shape != (side, side):
        raise ValueError('patch_out_of_bounds')
    return answer


def score_grid(baseline, current, cx, cy, side):
    template = patch(baseline, cx, cy, side).astype(np.float64)
    centered = template - template.mean()
    energy = float(np.sum(centered * centered))
    standard_deviation = math.sqrt(energy / template.size)
    grid = []
    current_standard_deviation = []
    finite = []
    for dy in OFFSETS:
        row, sdrow = [], []
        for dx in OFFSETS:
            candidate = patch(current, cx+dx, cy+dy, side).astype(np.float64)
            cc = candidate - candidate.mean()
            candidate_energy = float(np.sum(cc * cc))
            sdrow.append(math.sqrt(candidate_energy / candidate.size))
            value = None
            if energy > 0 and candidate_energy > 0:
                value = float(np.sum(centered * cc) / math.sqrt(energy * candidate_energy))
                finite.append((value, dx, dy))
            row.append(value)
        grid.append(row)
        current_standard_deviation.append(sdrow)
    winner = None
    alternatives = []
    margin = None
    tied = []
    if finite:
        best = max(item[0] for item in finite)
        # Stable traversal order selects a representative even for failed ties.
        winner_tuple = next(item for item in finite if item[0] == best)
        _, wx, wy = winner_tuple
        winner = {'dx': wx, 'dy': wy, 'x': cx+wx, 'y': cy+wy, 'ncc': best}
        tied = [{'dx': dx, 'dy': dy, 'ncc': value} for value, dx, dy in finite
                if abs(best-value) <= 1e-12]
        far = [item for item in finite if max(abs(item[1]-wx), abs(item[2]-wy)) >= 3]
        if far:
            far_best = max(item[0] for item in far)
            margin = best - far_best
            alternatives = [{'dx': dx, 'dy': dy, 'ncc': value} for value, dx, dy in far
                            if abs(far_best-value) <= 1e-12]
    gates = {
        'baseline_population_sd_at_least_10': standard_deviation >= 10,
        'winner_ncc_at_least_0_85': winner is not None and winner['ncc'] >= 0.85,
        'far_margin_at_least_0_02': margin is not None and margin >= 0.02,
        'unique_best_within_1e_minus_12': len(tied) == 1,
        'winner_not_on_search_boundary': winner is not None and abs(winner['dx']) < 6 and abs(winner['dy']) < 6,
    }
    return {
        'center': [cx, cy], 'side': side,
        'grid_axes': {'outer_rows_dy': OFFSETS, 'inner_columns_dx': OFFSETS},
        'baseline_mean': float(template.mean()), 'baseline_population_sd': standard_deviation,
        'scores': grid, 'candidate_population_sds': current_standard_deviation,
        'undefined_score_count': 169-len(finite), 'winner': winner,
        'best_ties_within_tolerance': tied,
        'best_chebyshev_at_least_3_alternatives': alternatives, 'far_margin': margin,
        'gates': gates, 'pass': all(gates.values()),
        'failed_gates': [name for name, okay in gates.items() if not okay],
    }


def translated(source, dx, dy):
    target = np.full(source.shape, 33.0)
    h, w = source.shape
    x0, x1, y0, y1 = max(0, dx), min(w, w+dx), max(0, dy), min(h, h+dy)
    target[y0:y1, x0:x1] = source[y0-dy:y1-dy, x0-dx:x1-dx]
    return target


def controls():
    rng = np.random.default_rng(20260912)
    rich = rng.integers(20, 181, size=(65, 65)).astype(np.float64)
    yy, xx = np.indices((65, 65))
    repeating = (50 + 80*((xx+yy) % 2)).astype(np.float64)
    flat = np.full((65, 65), 80.0)
    cases = []
    definitions = [
        ('identity', rich, rich.copy(), [0, 0], True, []),
        ('translated', rich, translated(rich, -3, 2), [-3, 2], True, []),
        ('intensity_offset', rich, translated(rich, -3, 2)+37, [-3, 2], True, []),
        ('positive_gain', rich, 1.75*translated(rich, -3, 2)+17, [-3, 2], True, []),
        ('flat_template', flat, rich, None, False, ['baseline_population_sd_at_least_10']),
        ('repeating_texture', repeating, repeating.copy(), None, False,
         ['far_margin_at_least_0_02', 'unique_best_within_1e_minus_12']),
        ('boundary_translation', rich, translated(rich, 6, 0), [6, 0], False,
         ['winner_not_on_search_boundary']),
    ]
    for side in SIDES:
        for label, base, current, expected_winner, expected_pass, expected_failures in definitions:
            result = score_grid(base, current, 32, 32, side)
            observed_winner = None if result['winner'] is None else [result['winner']['dx'], result['winner']['dy']]
            checks = {
                'expected_pass_state': result['pass'] is expected_pass,
                'expected_winner_when_specified': expected_winner is None or observed_winner == expected_winner,
                'expected_failed_gates': all(name in result['failed_gates'] for name in expected_failures),
                'unit_ncc_when_exact_winner_specified': expected_winner is None or abs(result['winner']['ncc']-1) <= 1e-12,
                'flat_scores_all_undefined': label != 'flat_template' or result['undefined_score_count'] == 169,
            }
            cases.append({'name': label, 'side': side,
                          'input_baseline': base.tolist(), 'input_current': current.tolist(),
                          'expected': {'winner_dx_dy_or_unspecified': expected_winner, 'pass': expected_pass,
                                       'required_failed_gates': expected_failures},
                          'result': result, 'checks': checks, 'checks_pass': all(checks.values())})
    return {'generator': 'numpy default_rng seed20260912; full realized inputs retained',
            'clipping': False, 'cases': cases, 'pass': all(c['checks_pass'] for c in cases)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    if not re.fullmatch('[a-z0-9_-]+', args.out):
        raise ValueError('invalid_output_name')
    out = HERE/args.out
    if out.exists():
        print(json.dumps({'status': 'refused_existing_output'}))
        return 2
    out.mkdir()
    started = time.monotonic()
    inputs = {name: HERE/rel for name, (rel, _) in PINS.items()}
    inputs['code'] = Path(__file__).resolve()
    inputs.update({f'native_{index:04d}': HERE/f'views01/frame-{index:04d}.png' for index in INDICES})
    before, after, products = {}, {}, []
    stage = 'pin_inputs'
    try:
        before = {name: pin(path) for name, path in inputs.items()}
        for name, (_, expected) in PINS.items():
            if before[name]['sha256'] != expected:
                raise ValueError('control_input_pin_mismatch')
        receipt = json.loads(inputs['views_receipt'].read_text())
        if receipt['status'] != 'pass_diagnostic_only' or not receipt['execution']['all_frames_match']:
            raise ValueError('unaccepted_source_receipt')
        if receipt['inputs_before'] != receipt['inputs_after']:
            raise ValueError('source_receipt_input_change')
        if receipt['inputs_before']['protocol'] != before['protocol'] or receipt['inputs_before']['code'] != before['preparation_code']:
            raise ValueError('source_receipt_control_mismatch')
        prows = {p['name']: p for p in receipt['products'] if p['role'] == 'native_unmarked'}
        rrows = {r['index']: r for r in receipt['rows']}
        if set(prows) != {f'frame-{i:04d}.png' for i in INDICES} or set(rrows) != set(INDICES):
            raise ValueError('native_coverage_mismatch')
        frames, checks = {}, []
        for index in INDICES:
            name = f'frame-{index:04d}.png'
            actual = before[f'native_{index:04d}']
            if actual != {k: prows[name][k] for k in ('bytes', 'sha256')}:
                raise ValueError('native_file_mismatch')
            with Image.open(inputs[f'native_{index:04d}']) as image:
                if image.mode != 'L' or image.size != (720, 480):
                    raise ValueError('native_shape_mismatch')
                pixel_digest = digest(image.tobytes())
                if pixel_digest != rrows[index]['pixel_sha256']:
                    raise ValueError('native_pixel_mismatch')
                frames[index] = np.array(image, dtype=np.uint8)
            checks.append({'frame': index, 'file_match': True, 'pixel_match': True,
                           'pixel_sha256': pixel_digest})
        stage = 'controls_before_real_scoring'
        tests = controls()
        write_json(out/'controls.json', tests)
        products.append({'name': 'controls.json', **pin(out/'controls.json')})
        if not tests['pass']:
            raise ValueError('synthetic_control_failure')
        stage = 'real_scoring'
        rows, translations = [], []
        for side in SIDES:
            for index in INDICES:
                current_rows = []
                for label, cx, cy in REFERENCES:
                    result = score_grid(frames[288], frames[index], cx, cy, side)
                    row = {'frame': index, 'reference': label, **result}
                    rows.append(row)
                    current_rows.append(row)
                all_pass = all(row['pass'] for row in current_rows)
                translation = {'frame': index, 'side': side, 'all_three_pass': all_pass,
                               'mean_dx_dy': None, 'residual_dx_dy': None,
                               'failed_references': [r['reference'] for r in current_rows if not r['pass']]}
                if all_pass:
                    vectors = np.array([[r['winner']['dx'], r['winner']['dy']] for r in current_rows], dtype=np.float64)
                    mean = vectors.mean(axis=0)
                    translation.update({'mean_dx_dy': mean.tolist(),
                                        'residual_dx_dy': [{'reference': r['reference'], 'vector': v.tolist()}
                                                           for r, v in zip(current_rows, vectors-mean)]})
                translations.append(translation)
        scores = {'baseline': 288, 'status': 'diagnostic_not_calibration',
                  'population_sd_denominator': 'side squared',
                  'ncc_definition': 'sum((T-mean(T))*(C-mean(C)))/sqrt(sum((T-mean(T))^2)*sum((C-mean(C))^2))',
                  'undefined_score_representation': None, 'rows': rows, 'translations': translations}
        write_json(out/'scores.json', scores)
        products.append({'name': 'scores.json', **pin(out/'scores.json')})
        summary_rows = []
        for label, _, _ in REFERENCES:
            for side in SIDES:
                selected = [r for r in rows if r['reference'] == label and r['side'] == side]
                summary_rows.append({'reference': label, 'side': side, 'rows': len(selected),
                                     'passed': sum(r['pass'] for r in selected),
                                     'baseline_population_sd': selected[0]['baseline_population_sd'],
                                     'failures_per_gate': {name: sum(not r['gates'][name] for r in selected)
                                                           for name in selected[0]['gates']},
                                     'winner_dx_values': sorted({r['winner']['dx'] for r in selected if r['winner']}),
                                     'winner_dy_values': sorted({r['winner']['dy'] for r in selected if r['winner']})})
        summary = {'status': 'pass_computation_not_landmark_acceptance', 'native_frames': len(frames),
                   'synthetic_cases': len(tests['cases']), 'synthetic_checks_pass': tests['pass'],
                   'real_rows': len(rows), 'real_candidate_scores': len(rows)*169,
                   'real_passed_rows': sum(r['pass'] for r in rows), 'groups': summary_rows,
                   'all_three_translation_groups_passed': sum(t['all_three_pass'] for t in translations),
                   'translation_groups_total': len(translations)}
        write_json(out/'summary.json', summary)
        products.append({'name': 'summary.json', **pin(out/'summary.json')})
        stage = 'post_input_pin_check'
        after = {name: pin(path) for name, path in inputs.items()}
        if before != after:
            raise ValueError('input_change_during_run')
        final = {'status': 'pass_computation_not_physical_validation',
                 'command': ['python3', 'reference_diagnostic.py', '--out', args.out],
                 'runtime': {'python': platform.python_version(), 'numpy': np.__version__, 'pillow': pillow_version,
                             'implementation': platform.python_implementation(), 'elapsed_seconds': time.monotonic()-started},
                 'inputs_before': before, 'inputs_after': after, 'native_checks': checks,
                 'controls_completed_before_real_scoring': True, 'products': products,
                 'source_warning_status_preserved': 'diagnostic source retains three corrupt-frame mentions; not clean certification',
                 'limitations': ['integer-offset image texture diagnostic only', 'no target-track input',
                                 'references not established as physically stationary',
                                 'no camera, depth or perspective calibration', 'no human landmark approval']}
        write_json(out/'receipt.json', final)
        print(json.dumps(summary, sort_keys=True, allow_nan=False))
        return 0
    except Exception as error:
        for name, path in inputs.items():
            try:
                after[name] = pin(path)
            except Exception:
                after[name] = {'unavailable': True}
        failure = {'status': 'failed', 'stage': stage, 'exception_type': type(error).__name__,
                   'inputs_before': before, 'inputs_after': after, 'partial_products': products,
                   'elapsed_seconds': time.monotonic()-started,
                   'error_text_not_exported': True}
        write_json(out/'failure.json', failure)
        print(json.dumps({'status': 'failed', 'stage': stage, 'exception_type': type(error).__name__}))
        return 1


if __name__ == '__main__':
    sys.exit(main())

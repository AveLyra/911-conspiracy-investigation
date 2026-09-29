"""Separate arithmetic audit of saved arrays; preprocessing is shared, not replicated."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
from pathlib import Path
import platform
import signal
import sys
import time

import numpy as np

BASE = Path(__file__).resolve().parent
OLD = BASE.parent / 'peskin-figure-correspondence'
GAMMAS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]
LEVELS = [64, 128, 192, 224]
PRODUCER_PIN = 'eff2aa28a85d303ec6f17b47be312bfc13de35dbaa1c117a2d8ade5a7a03041a'
PROTOCOL_PIN = 'edbc10c984c45e915d40853ea1ea0e9aa97f256af47643afa944dda278a8b7ed'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def emit(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')


def average(x):
    return float(np.sum(x, dtype=np.float64) / len(x))


def variance(x):
    center = x - average(x)
    return float(np.sum(center * center, dtype=np.float64) / len(x))


def quantile(x, probability):
    ordered = np.sort(x)
    location = (len(ordered) - 1) * probability
    lower, upper = math.floor(location), math.ceil(location)
    return float(ordered[lower] + (ordered[upper] - ordered[lower]) * (location - lower))


def ranks(x):
    order = np.argsort(x, kind='stable')
    sorted_x = x[order]
    boundaries = np.r_[0, np.flatnonzero(sorted_x[1:] != sorted_x[:-1]) + 1, len(x)]
    ranked = np.empty(len(x), dtype=float)
    for first, stop in zip(boundaries[:-1], boundaries[1:]):
        ranked[order[first:stop]] = (int(first) + int(stop) + 1) / 2
    return ranked


def threshold_support(x, y, source_threshold, target_threshold):
    left = np.greater_equal(x, source_threshold)
    right = np.greater_equal(y, target_threshold)
    source_count = int(np.count_nonzero(left))
    target_count = int(np.count_nonzero(right))
    intersection = int(np.count_nonzero(np.logical_and(left, right)))
    union = source_count + target_count - intersection
    return {
        'source_fraction': source_count / len(x), 'target_fraction': target_count / len(x),
        'source_ties': int(np.count_nonzero(x == source_threshold)),
        'target_ties': int(np.count_nonzero(y == target_threshold)),
        'intersection': intersection, 'union': union,
        'iou': intersection / union if union else None,
    }


def diagnostic_error(x, y):
    residual = np.subtract(x, y)
    absolute = np.abs(residual)
    result = {
        'bias': average(residual), 'mae': average(absolute),
        'rmse': math.sqrt(average(np.square(residual))),
        'abs_residual_gt_25_5': int(np.count_nonzero(absolute > 25.5)) / len(x),
        'abs_residual_gt_51': int(np.count_nonzero(absolute > 51)) / len(x),
    }
    for label, array in [('source', x), ('target', y)]:
        for suffix, selected in [('low', array <= 5), ('high', array >= 250),
                                 ('zero', array == 0), ('255', array == 255)]:
            result[label + '_' + suffix] = int(np.count_nonzero(selected)) / len(x)
    result['levels'] = {str(level): threshold_support(x, y, level, level) for level in LEVELS}
    return result


def diagnostic_rank(x, y):
    if len(x) < 32 or variance(x) <= 1e-8 or variance(y) <= 1e-8:
        return {'spearman': None, 'quantiles': None, 'reason': 'insufficient or flat gray values'}
    rank_x, rank_y = ranks(x), ranks(y)
    centered_x, centered_y = rank_x - average(rank_x), rank_y - average(rank_y)
    numerator = float(np.sum(centered_x * centered_y))
    denominator = math.sqrt(float(np.sum(centered_x ** 2) * np.sum(centered_y ** 2)))
    quantiles = {}
    for q in [0.1, 0.2, 0.3]:
        tx, ty = quantile(x, 1 - q), quantile(y, 1 - q)
        quantiles[str(q)] = {'source_threshold': tx, 'target_threshold': ty,
                            **threshold_support(x, y, tx, ty)}
    return {'spearman': numerator / denominator, 'quantiles': quantiles, 'reason': None}


def regression(x, y, gamma):
    if len(x) < 32 or variance(x) <= 1e-8 or variance(y) <= 1e-8:
        return {'status': 'uninformative', 'reason': 'insufficient or flat training values'}
    powered = np.power(x / 255, gamma)
    if variance(powered) <= 1e-14:
        return {'status': 'uninformative', 'reason': 'powered source variance'}
    # Independent solver: least-squares design matrix, not producer covariance formula.
    coefficients = np.linalg.lstsq(np.column_stack([powered, np.ones(len(x))]), y / 255, rcond=None)[0]
    a, b = map(float, coefficients)
    if not math.isfinite(a) or not math.isfinite(b) or a <= 0:
        return {'status': 'rejected', 'reason': 'nonpositive or nonfinite slope'}
    return {'status': 'fitted', 'a': a, 'b': b, 'gamma': gamma}


def coverage(mask, valid):
    chosen = np.logical_and(mask, valid)
    selected, observed = int(np.count_nonzero(mask)), int(np.count_nonzero(chosen))
    fraction = observed / selected if selected else 0.0
    return chosen, {'selected': selected, 'observed': observed, 'coverage': fraction,
                    'eligible': observed >= 32 and fraction >= 0.85}


def extrapolation(x, train):
    low, high = float(np.min(train)), float(np.max(train))
    p01, p99 = quantile(train, 0.01), quantile(train, 0.99)
    return {'training_min': low, 'training_max': high, 'training_p01': p01, 'training_p99': p99,
            'outside_min_max': int(np.count_nonzero((x < low) | (x > high))) / len(x),
            'outside_p01_p99': int(np.count_nonzero((x < p01) | (x > p99))) / len(x)}


def extract_literal(path, variable):
    tree = ast.parse(path.read_text())
    assignments = [node for node in tree.body if isinstance(node, ast.Assign)
                   and any(isinstance(target, ast.Name) and target.id == variable for target in node.targets)]
    if len(assignments) != 1:
        raise ValueError('literal assignment: ' + variable)
    return ast.literal_eval(assignments[0].value)


def rectangle_mask(boxes, factor):
    # Separate coordinate implementation: select complete row/column index sets.
    width, height = 180 * factor, 120 * factor
    result = np.zeros((height, width), dtype=bool)
    for left, top, right, bottom in boxes:
        columns = [i for i in range(width) if left <= (2 * i + 1) * 720 / (2 * width) < right]
        rows = [j for j in range(height) if top <= (2 * j + 1) * 478 / (2 * height) < bottom]
        result[np.ix_(rows, columns)] = True
    return result


class Comparator:
    def __init__(self):
        self.failures = []
        self.leaves = 0
        self.maximum_absolute_difference = 0.0

    def compare(self, expected, actual, label):
        if isinstance(expected, dict):
            if not isinstance(actual, dict) or set(expected) != set(actual):
                self.failures.append(label + ': dictionary keys')
                return
            for key in expected:
                self.compare(expected[key], actual[key], label + '/' + key)
        elif isinstance(expected, (float, np.floating)):
            self.leaves += 1
            if not isinstance(actual, (int, float)) or not math.isfinite(actual):
                self.failures.append(label + ': nonfinite or nonnumeric')
                return
            difference = abs(expected - actual)
            self.maximum_absolute_difference = max(self.maximum_absolute_difference, difference)
            tolerance = 1e-10 if label.endswith(('/a', '/b')) else 1e-9
            if difference > tolerance:
                self.failures.append(label + ': float difference ' + str(difference))
        else:
            self.leaves += 1
            if expected != actual:
                self.failures.append(label + ': exact value mismatch')


def controls():
    x = np.arange(80, dtype=float) + 10
    checks = {}
    for gamma in GAMMAS:
        target = 255 * (0.8 * (x / 255) ** gamma + 0.05)
        fit = regression(x, target, gamma)
        prediction = fit['a'] * (x / 255) ** gamma + fit['b']
        checks['gamma_' + str(gamma)] = bool(np.max(np.abs(prediction - target / 255)) <= 1e-10)
    checks['tie_ranks'] = np.array_equal(ranks(np.array([9., 2., 2., 7.])), [4, 1.5, 1.5, 3])
    checks['linear_quantile'] = quantile(np.array([0., 10., 20., 30.]), 0.25) == 7.5
    checks['empty_union_null'] = threshold_support(np.zeros(32), np.zeros(32), 64, 64)['iou'] is None
    checks['flat_rank_null'] = diagnostic_rank(np.ones(80), x)['spearman'] is None
    checks['flat_fit_null'] = regression(np.ones(80), x, 1)['status'] == 'uninformative'
    checks['negative_slope'] = regression(x, 255 - x, 1)['status'] == 'rejected'
    checks['monotone_ranks'] = abs(diagnostic_rank(x, x ** 3)['spearman'] - 1) < 1e-10
    checks['signed_error'] = diagnostic_error(np.arange(80, dtype=float), np.arange(80, dtype=float) + 2)['bias'] == -2
    checks['known_error'] = diagnostic_error(np.array([0., 3., 4.]), np.zeros(3))['rmse'] == math.sqrt(25 / 3)
    checks['minimum_sample_gate'] = not coverage(np.ones((1, 31), bool), np.ones((1, 31), bool))[1]['eligible']
    checks['coverage_gate'] = not coverage(np.ones((10, 10), bool), np.indices((10, 10))[0] > 1)[1]['eligible']
    checks['mask_factor1'] = int(rectangle_mask([(0, 0, 4, 478)], 1).sum()) == 120
    checks['mask_factor2'] = int(rectangle_mask([(0, 0, 4, 478)], 2).sum()) == 480
    checks['extrapolation'] = extrapolation(np.array([0., 10., 20., 30.]), np.array([10., 20.]))['outside_min_max'] == 0.5
    altered = np.zeros(80); altered[10:20] = 200
    shifted = np.zeros(80); shifted[30:40] = 200
    checks['displaced_patch'] = threshold_support(altered, shifted, 128, 128)['iou'] == 0 and diagnostic_error(altered, shifted)['mae'] == 50
    check = Comparator(); check.compare({'n': 1, 'x': 1.}, {'n': 2, 'x': 1.01}, 'mutant')
    checks['comparison_detects_corruption'] = len(check.failures) == 2
    checks = {key: bool(value) for key, value in checks.items()}
    return {'checks': checks, 'passed': all(checks.values()), 'count': len(checks)}


def audit(folder):
    control_path = BASE / 'independent-controls01.json'
    control = json.loads(control_path.read_text())
    if not control['passed'] or control['checker_sha256'] != digest(__file__) or control['protocol_sha256'] != PROTOCOL_PIN:
        raise ValueError('separate checker controls stale or failed')
    receipt_path = folder / 'receipt.json'
    receipt = json.loads(receipt_path.read_text())
    if receipt['status'] != 'completed' or receipt['script_sha256'] != PRODUCER_PIN or digest(BASE / 'measure.py') != PRODUCER_PIN:
        raise ValueError('producer code/completion gate')
    if receipt['protocol_sha256'] != PROTOCOL_PIN or digest(BASE / 'PROTOCOL.md') != PROTOCOL_PIN:
        raise ValueError('producer protocol gate')
    for name in ['arrays.npz', 'results.json']:
        pin = receipt['outputs'][name]
        if digest(folder / name) != pin['sha256'] or (folder / name).stat().st_size != pin['bytes']:
            raise ValueError('producer output pin: ' + name)
    for name, pin in receipt['prior_pins'].items():
        if digest(OLD / name) != pin:
            raise ValueError('prior dependency pin: ' + name)
    results = json.loads((folder / 'results.json').read_text())
    for path, pin in results['inputs'].items():
        if digest(path) != pin['sha256'] or Path(path).stat().st_size != pin['bytes']:
            raise ValueError('preserved source pin')
    region_boxes = extract_literal(OLD / 'check_regions.py', 'REGIONS')
    exclusions = extract_literal(OLD / 'check_regions.py', 'EXCLUSIONS')
    targets = extract_literal(OLD / 'match_screen.py', 'TARGETS')
    summary = json.loads((OLD / 'primary-summary.json').read_text())
    expected_rows = {}
    for key in ['148', '149']:
        candidates = {row['source_pts']: row for group in summary['results'][key].values() for row in group['top_four']}
        for pts, candidate in candidates.items():
            for factor in [1, 2]:
                for kernel in ['BILINEAR', 'BOX']:
                    branch = str(180 * factor) + '_' + kernel
                    expected_rows[(key, pts, branch)] = (factor, candidate)
    comparator = Comparator()
    comparator.compare(12, results['pair_count'], 'pair_count')
    comparator.compare(48, results['branch_count'], 'branch_count')
    comparator.compare(672, results['fit_attempts'], 'fit_attempts')
    comparator.compare(48, len(results['results']), 'actual_branch_rows')
    expected_array_keys = set()
    seen_rows = set()
    counts = {'branch_rows': 0, 'masks': 0, 'baseline_regions': 0, 'rank_regions': 0,
              'fit_rows': 0, 'fitted_rows': 0, 'fitted_regions': 0, 'foreground_baselines': 0}
    with np.load(folder / 'arrays.npz', allow_pickle=False) as arrays:
        for row in results['results']:
            identity = (row['target'], row['source_pts'], row['branch'])
            if identity not in expected_rows or identity in seen_rows:
                raise ValueError('unknown or duplicate branch row')
            seen_rows.add(identity)
            factor, candidate = expected_rows[identity]
            key, pts, branch = identity
            prefix = f'T{key}_{pts}_{branch}'
            comparator.compare(factor, row['factor'], prefix + '/factor')
            comparator.compare(prefix, row['array_prefix'], prefix + '/array_prefix')
            comparator.compare(candidate['frame_index'], row['frame_index'], prefix + '/frame_index')
            geometry = candidate['geometry_candidates'][0]
            comparator.compare(geometry, row['geometry'], prefix + '/geometry')
            source, target, valid = [arrays[prefix + suffix] for suffix in ['_source', '_target', '_valid']]
            expected_array_keys.update(prefix + suffix for suffix in ['_source', '_target', '_valid'])
            shape = (120 * factor, 180 * factor)
            if source.shape != shape or target.shape != shape or valid.shape != shape or valid.dtype != bool:
                raise ValueError('saved array shape/type')
            if not np.isfinite(source).all() or not np.isfinite(target).all() or np.any((source < 0) | (source > 255)) or np.any((target < 0) | (target > 255)):
                raise ValueError('saved gray domain')
            columns = np.arange(shape[1]) + geometry['left'] * factor
            rows = np.arange(shape[0]) + geometry['top'] * factor
            x0, y0 = geometry['canvas_x'] * factor, geometry['canvas_y'] * factor
            valid_oracle = ((rows[:, None] >= y0) & (rows[:, None] < y0 + geometry['raster_height'] * factor)
                            & (columns[None, :] >= x0) & (columns[None, :] < x0 + geometry['raster_width'] * factor))
            if not np.array_equal(valid, valid_oracle):
                raise ValueError('independent validity geometry')
            guard = rectangle_mask([(3, 3, 717, 475)], factor)
            expanded = [(left - 4, top - 4, right + 4, bottom + 4) for left, top, right, bottom in exclusions[key]]
            guard &= ~rectangle_mask(expanded, factor)
            masks = {name: rectangle_mask([box], factor) & guard for name, box in region_boxes[key].items()}
            union = np.zeros(shape, dtype=bool)
            for mask in masks.values():
                union |= mask
            masks['F'] = rectangle_mask(targets[key][2], factor) & guard & ~union
            if np.any(masks['F'] & union):
                raise ValueError('independent fit/evaluation overlap')
            baseline = {}; rank_results = {}
            for name, mask in masks.items():
                mask_key = f'T{key}_{branch}_{name}'
                expected_array_keys.add(mask_key)
                if not np.array_equal(mask, arrays[mask_key]):
                    raise ValueError('independent mask mismatch: ' + mask_key)
                comparator.compare(hashlib.sha256(mask.tobytes()).hexdigest(), results['mask_hashes'][mask_key], mask_key + '/hash')
                chosen, meta = coverage(mask, valid)
                baseline[name] = {**meta, 'metrics': diagnostic_error(source[chosen], target[chosen]) if meta['eligible'] else None}
                rank_results[name] = diagnostic_rank(source[chosen], target[chosen]) if meta['eligible'] else None
                counts['masks'] += 1; counts['baseline_regions'] += 1; counts['rank_regions'] += 1
            comparator.compare(baseline, row['baseline'], prefix + '/baseline')
            comparator.compare(rank_results, row['rank_diagnostics'], prefix + '/rank_diagnostics')
            tiles = np.fromfunction(lambda y, x: (np.floor(x / (8 * factor)) + np.floor(y / (8 * factor))) % 2, shape)
            expected_fits = [(fold, gamma) for fold in [0, 1] for gamma in GAMMAS]
            comparator.compare(14, len(row['fits']), prefix + '/fit_count')
            for fit_index, fit_row in enumerate(row['fits']):
                if fit_index >= len(expected_fits):
                    break
                fold, gamma = expected_fits[fit_index]
                fit_label = prefix + '/fit_' + str(fit_index)
                comparator.compare(fold, fit_row['fold'], fit_label + '/fold')
                comparator.compare(gamma, fit_row['gamma'], fit_label + '/gamma')
                train_mask = masks['F'] & (tiles == fold)
                hold_mask = masks['F'] & (tiles != fold)
                train, meta = coverage(train_mask, valid)
                hold, hold_meta = coverage(hold_mask, valid)
                comparator.compare(meta, fit_row['training'], fit_label + '/training')
                comparator.compare(diagnostic_error(source[train], target[train]) if meta['eligible'] else None,
                                   fit_row['baseline_train'], fit_label + '/baseline_train')
                comparator.compare(diagnostic_error(source[hold], target[hold]) if hold_meta['eligible'] else None,
                                   fit_row['baseline_hold'], fit_label + '/baseline_hold')
                fitted = regression(source[train], target[train], gamma) if meta['eligible'] else {'status': 'uninformative', 'reason': 'training coverage'}
                comparator.compare(fitted, fit_row['fit'], fit_label + '/fit')
                counts['fit_rows'] += 1; counts['foreground_baselines'] += 2
                evaluations = {}
                if fitted['status'] == 'fitted' and fit_row['fit']['status'] == 'fitted':
                    counts['fitted_rows'] += 1
                    # Use the separately verified serialized coefficients to keep exact endpoint
                    # classifications distinct from roundoff in the independent regression solver.
                    saved = fit_row['fit']
                    raw_prediction = (saved['a'] * np.power(source / 255, gamma) + saved['b']) * 255
                    prediction = np.maximum(0, np.minimum(255, raw_prediction))
                    for name, mask in {**masks, 'F_train': train_mask, 'F_hold': hold_mask}.items():
                        chosen, region_meta = coverage(mask, valid)
                        eligible = region_meta['eligible']
                        n = region_meta['observed']
                        evaluations[name] = {
                            **region_meta,
                            'metrics': diagnostic_error(prediction[chosen], target[chosen]) if eligible else None,
                            'clipped_below': int(np.count_nonzero(raw_prediction[chosen] < 0)) / n if eligible else None,
                            'clipped_above': int(np.count_nonzero(raw_prediction[chosen] > 255)) / n if eligible else None,
                            'extrapolation': extrapolation(source[chosen], source[train]) if eligible else None,
                        }
                        counts['fitted_regions'] += 1
                comparator.compare(evaluations, fit_row['regions'], fit_label + '/regions')
            counts['branch_rows'] += 1
        if set(arrays.files) != expected_array_keys:
            raise ValueError('saved array coverage')
    if seen_rows != set(expected_rows):
        raise ValueError('incomplete branch coverage')
    return {
        'passed': not comparator.failures, 'failures': comparator.failures,
        'counts': counts, 'compared_leaves': comparator.leaves,
        'maximum_absolute_difference': comparator.maximum_absolute_difference,
        'tolerances': {'fit_a_b_absolute': 1e-10, 'other_float_absolute': 1e-9, 'counts_and_nulls': 'exact'},
        'input_pins': {'receipt': digest(receipt_path), 'results': digest(folder / 'results.json'),
                       'arrays': digest(folder / 'arrays.npz'), 'checker_controls': digest(control_path)},
        'coefficient_use': 'OLS coefficients independently recomputed by np.linalg.lstsq, then verified saved coefficients used for diagnostic predictions to avoid endpoint classification changes from solver roundoff.',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--run', choices=['run01', 'run02'])
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.controls == (args.run is not None):
        raise ValueError('choose synthetic controls or saved run')
    output = BASE / args.output
    if output.parent != BASE or not output.name.startswith('independent-') or output.suffix != '.json':
        raise ValueError('scoped output filename')
    if output.exists():
        raise FileExistsError('create-only output')
    started = time.monotonic()
    def timeout(signum, frame):
        raise TimeoutError('300-second independent-check cap')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(300)
    try:
        result = controls() if args.controls else audit(BASE / args.run)
        record = {'status': 'completed' if result['passed'] else 'failed',
                  'checker_sha256': digest(__file__), 'protocol_sha256': digest(BASE / 'PROTOCOL.md'),
                  'python': platform.python_version(), 'numpy': np.__version__,
                  'elapsed_seconds': time.monotonic() - started, 'argv': sys.argv,
                  'independence': 'Separate arithmetic implementation; shared saved historical arrays, NumPy and Python. No independent image decoding, camera calibration or source family.',
                  **result}
        emit(output, record)
        print(json.dumps({'status': record['status'], 'output': output.name, 'passed': result['passed']}))
        if not result['passed']:
            raise ValueError('independent checks failed; see preserved output')
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()

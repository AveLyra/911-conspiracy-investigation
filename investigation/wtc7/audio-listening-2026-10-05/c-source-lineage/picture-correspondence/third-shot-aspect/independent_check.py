#!/usr/bin/env python3
"""Separate direct-arithmetic audit. Read-only unless --receipt is explicit.

No producer/core imports. The prior independent checker supplies only its
SHA-guarded pixel-center mask, Pillow working-image and long-double direct-sum
helpers. Shared Pillow is not an independent resampling implementation. The
saved FFT surface is searched in full; its every score is NOT recomputed.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np
from PIL import Image, _imaging

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
CORE = PARENT.parents[2] / 'peskin-figure-correspondence/match_screen.py'
CHARTER = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md')
HELPER = PARENT / 'independent_check.py'
HELPER_SHA = '56784c9f63ea2f8fc775e0d6d77635a80ea1dc3b4aff5dd9326d954272afa2ef'
SCORE_TOL, COVERAGE_TOL = 1e-9, 1e-12
ARMS = ('baseline', 'native_relative_aspect')
SCALES = [j / 20 for j in range(15, 36)]
EARLY = [(30000 * second + 1000) // 1001 for second in range(38)]
REFERENCES = [13320, 13470, 13620]
METRICS = ('fit', 'static_evaluation', 'dynamic')
RECTANGLES = {'fit': [790, 80, 1060, 630],
              'static_evaluation': [190, 490, 440, 665],
              'dynamic': [475, 60, 695, 335]}
CROP = [165, 0, 1115, 720]
FIXED = {
    PARENT / 'config.json': '56efd21495ef21b37df9137438f0b53183a120b59b1b43eb0f498b4ac47d65b2',
    PARENT / 'PROTOCOL.md': 'd0609694559608ffa87ab517e4b4ca3ea2c0e5bc9556a0458ee0faee103fd120',
    PARENT / 'picture_screen.py': 'f5d2c75f758da5f3bdf63bd4b8b38d2eba1897aa6a52c37e93f6f91559d44f86',
    PARENT / 'test_picture_screen.py': '8225adf3e4fbc15292e9e439927a8e581a4c15a1ad819c625d584674e67f7c43',
    PARENT / 'picture01/receipt.json': 'c459b4009d011291144086581c90afed3181328c63bfc54318ca5c8755a721ae',
    PARENT / 'picture02/receipt.json': '6ecd59e3d6f7a8d27f39ff1367c17f2ba9abb923de0fc22afc41d865efc63835',
    PARENT / 'independent-check.json': '6e8f7907f9bacc9ed99b92c01c5cd3986ccf4b7a82bcae8e0b5e66ed90729392',
    CORE: '06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8',
    CHARTER: '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
    HERE / 'PROTOCOL.md': 'bc369159ff6aa3f71e204e72f9c01eb8749e81008f8271b83f8f31d0ca7ddc25',
    HERE / 'preparation-review.json': '3abb5b6a30e2bb371b51ca7b6b6c2853d4a647ded9bcec3a7ead20b8e6a3f078',
    HERE / 'aspect_screen.py': 'e835362b4677b83770bc55fb7fc69dcdca0b20f0a98fd17ef2d7350ab66ac535',
    HERE / 'test_aspect_screen.py': '262959c4ae8afaca5f388d336e892129bbd214668af2d3eaef23bd2a725f12f4',
}


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def pin(path):
    path = Path(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'sha256': digest, 'bytes': path.stat().st_size}


def check_pin(path, expected):
    actual = pin(path)
    require(isinstance(expected, dict) and 'sha256' in expected, ('pin schema', str(path)))
    for key in ('sha256', 'bytes'):
        if key in expected:
            require(actual[key] == expected[key], ('pin mismatch', str(path), key))
    return actual


def load_helper():
    check_pin(HELPER, {'sha256': HELPER_SHA})
    spec = importlib.util.spec_from_file_location('prior_separate_direct_checker', HELPER)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    return helper


def same(actual, expected, label='value'):
    """Structural equality with declared numerical tolerances, not key omission."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and actual.keys() == expected.keys(), (label, 'keys'))
        for key in expected:
            same(actual[key], expected[key], f'{label}.{key}')
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected), (label, 'length'))
        for index, value in enumerate(expected):
            same(actual[index], value, f'{label}[{index}]')
    elif isinstance(expected, float):
        tol = COVERAGE_TOL if 'coverage' in label else SCORE_TOL
        require(type(actual) in (float, int) and np.isfinite(actual)
                and abs(actual - expected) <= tol, (label, actual, expected))
    else:
        require(type(actual) is type(expected) and actual == expected, (label, actual, expected))


def geometry(arm, scale_index):
    """Integer-grid oracle, independent of producer Fraction/round sizing."""
    require(arm in ARMS and type(scale_index) is int and 0 <= scale_index < 21, 'fixed geometry only')
    j = scale_index + 15
    width = 9 * j
    height = 6 * j if arm == 'baseline' else (133 * j + 12) // 24
    x, y = (230 - width) // 2, (170 - height) // 2
    left, top, right, bottom = max(x, 0), max(y, 0), min(x + width, 230), min(y + height, 170)
    factor = Fraction(1) if arm == 'baseline' else Fraction(133, 144)
    return {'requested_scale': j / 20, 'requested_scale_exact': str(Fraction(j, 20)),
            'height_factor': str(factor), 'unrounded_width': str(Fraction(9 * j)),
            'unrounded_height': str(Fraction(6 * j) * factor),
            'raster_width': width, 'raster_height': height,
            'canvas_x': x, 'canvas_y': y, 'scale_x': width / 180, 'scale_y': height / 120,
            'canvas_intersection': [left, top, right, bottom],
            'scaled_raster_intersection': [left - x, top - y, right - x, bottom - y],
            'native_magnification_x': str(Fraction(950 * width, 180 * 320)),
            'native_magnification_y': str(Fraction(720 * height, 120 * 224))}


def make_canvas(image, arm, scale_index):
    meta = geometry(arm, scale_index)
    a = np.asarray(image)
    require(a.shape == (120, 180) and np.isfinite(a).all()
            and a.min() >= 0 and a.max() <= 255, 'working image geometry/range')
    raster = np.asarray(Image.fromarray(a.astype(np.uint8)).resize(
        (meta['raster_width'], meta['raster_height']), Image.Resampling.BILINEAR))
    out, valid = np.zeros((170, 230), float), np.zeros((170, 230), bool)
    l, t, r, b = meta['canvas_intersection']
    sl, st, sr, sb = meta['scaled_raster_intersection']
    out[t:b, l:r] = raster[st:sb, sl:sr]
    valid[t:b, l:r] = True
    return out, valid, meta


def native_coordinates(i, j, left, top, meta):
    """Exact geometric pixel-center positions; not single-stage intensity samples."""
    return {'reference_x': Fraction(165) + Fraction(950, 180) * (Fraction(i) + Fraction(1, 2)),
            'reference_y': Fraction(720, 120) * (Fraction(j) + Fraction(1, 2)),
            'early_x': Fraction(320, meta['raster_width']) * (left + Fraction(i) + Fraction(1, 2) - meta['canvas_x']),
            'early_y': Fraction(224, meta['raster_height']) * (top + Fraction(j) + Fraction(1, 2) - meta['canvas_y'])}


def top_two(scores, coverage):
    require(scores.shape == coverage.shape == (21, 51, 51), 'surface shape')
    require(np.isfinite(coverage).all() and coverage.min() >= -COVERAGE_TOL
            and coverage.max() <= 1 + COVERAGE_TOL, 'surface coverage range')
    require(not np.isinf(scores).any(), 'infinite score')
    finite = np.argwhere(np.isfinite(scores))
    require(not len(finite) or np.abs(scores[np.isfinite(scores)]).max() <= 1 + SCORE_TOL, 'Pearson range')
    # Enumerate entire saved surface; no per-scale truncation copied from producer.
    return sorted((tuple(map(int, p)) for p in finite),
                  key=lambda p: (-float(scores[p]), p[0], p[1], p[2]))[:2]


def direct_record(helper, patch, target, mask, valid):
    score, coverage, reason, count = helper.direct(patch, target, mask, valid)
    return {'score': score, 'coverage': coverage, 'pixels': count, 'missing_reason': reason}


def primary(row, metric):
    if not row['transforms']:
        return {'score': None, 'coverage': None, 'pixels': None, 'missing_reason': 'all_fit_transforms_invalid'}
    selected = row['transforms'][0]
    if metric != 'fit':
        return selected['evaluations'][metric]
    return {'score': selected['fit_score'], 'coverage': selected['fit_coverage'],
            'pixels': selected['fit_pixels'], 'missing_reason': None}


def comparison(first, second):
    present = [x['score'] is not None for x in (first, second)]
    availability = ['neither', 'alternative_only', 'baseline_only', 'both'][2 * present[0] + present[1]]
    return {'baseline': first, 'alternative': second, 'availability': availability,
            'score_delta': second['score'] - first['score'] if all(present) else None,
            'coverage_delta': second['coverage'] - first['coverage']
            if first['coverage'] is not None and second['coverage'] is not None else None}


def common_diagnostic(helper, target, mask, patches):
    if patches is None:
        return {'valid_sets_equal': None, 'baseline_pixels': None, 'alternative_pixels': None,
                'intersection_pixels': None, 'intersection_coverage': None,
                'diagnostic': None, 'missing_reason': 'one_or_both_primary_fit_transforms_missing'}
    (a, av), (b, bv) = patches
    # Positions, not cardinalities; coverage always uses the full original mask.
    first, second = mask & av, mask & bv
    overlap = first & second
    return {'valid_sets_equal': bool(np.array_equal(first, second)),
            'baseline_pixels': int(first.sum()), 'alternative_pixels': int(second.sum()),
            'intersection_pixels': int(overlap.sum()), 'intersection_coverage': float(overlap.sum() / mask.sum()),
            'diagnostic': comparison(direct_record(helper, a, target, mask, overlap),
                                     direct_record(helper, b, target, mask, overlap)), 'missing_reason': None}


def expected_ranking(rows):
    result, selected = {}, set()
    for metric in METRICS:
        present = sorted((row for row in rows if primary(row, metric)['score'] is not None),
                         key=lambda row: (-primary(row, metric)['score'], row['source_index']))
        absent = sorted((row for row in rows if primary(row, metric)['score'] is None),
                        key=lambda row: row['source_index'])
        leaders = [row['source_index'] for row in present[:2]]
        selected.update(leaders)
        near = {str(d): [row['source_index'] for row in present
                         if primary(present[0], metric)['score'] - primary(row, metric)['score'] <= d]
                for d in (.005, .01, .02)}
        result[metric] = {'ranking': [{'source_index': row['source_index'], **primary(row, metric),
                                      'sample_boundary': row['source_index'] in (EARLY[0], EARLY[-1])}
                                     for row in present],
                          'unavailable': [{'source_index': row['source_index'], **primary(row, metric)}
                                          for row in absent], 'top_two': leaders, 'near_best': near}
    result['shortlist_union'] = sorted(selected)
    return result


def expected_keys():
    return [(arm, ref, source) for ref in REFERENCES for source in EARLY for arm in ARMS]


def check_rows(rows):
    require([(r['arm'], r['reference_index'], r['source_index']) for r in rows] == expected_keys(),
            'exact ordered 228-pair roster')
    required = {'arm', 'reference_index', 'source_index', 'source_pts', 'source_time_base',
                'reference_pts', 'reference_time_base', 'sample_boundary', 'surface_file', 'transforms', 'missing_reason'}
    for row in rows:
        require(row.keys() == required, 'result row schema')
        require(row['surface_file'] == f"surfaces-{row['arm']}-C{row['reference_index']}-E{row['source_index']}.npz",
                'surface identity')
        require(type(row['sample_boundary']) is bool
                and row['sample_boundary'] == (row['source_index'] in (EARLY[0], EARLY[-1])), 'sample boundary')


def required_method_paths():
    return {*map(str, FIXED), str(HERE / 'aspect_screen.py'), str(HERE / 'test_aspect_screen.py'),
            str(Path(sys.executable)), str(Path(np.__file__)), str(Path(Image.__file__)),
            str(Path(_imaging.__file__)), str(Path(np._core._multiarray_umath.__file__)),
            str(Path(np.fft._pocketfft_umath.__file__))}


def check_state(state, config):
    require(state.get('schema_version') == 1, 'state version')
    required_versions = {'python': '3.13.7', 'numpy': '2.3.4', 'pillow': '12.0.0'}
    require({key: state.get(key) for key in required_versions} == required_versions, 'recorded runtime')
    require({'python': platform.python_version(), 'numpy': np.__version__, 'pillow': Image.__version__}
            == required_versions, 'checker runtime')
    require(required_method_paths() <= state['pins'].keys(), 'missing mandatory method/runtime dependency')
    require(state['source_specs'] == {k: config[k] for k in ('early_video', 'c_video', 'early_map', 'c_map')},
            'source specs')
    for path, value in state['pins'].items():
        require(Path(path).is_absolute(), 'absolute dependency')
        check_pin(path, value)
    for path, digest in FIXED.items():
        require(state['pins'][str(path)]['sha256'] == digest, ('fixed dependency changed', str(path)))


def safe_product(directory, relative):
    path = Path(relative)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == relative, 'product path')
    target = directory / path
    require(target.resolve().is_relative_to(directory.resolve()), 'product escapes run')
    return target


def check_products(directory, declared, required):
    actual = {str(path.relative_to(directory)) for path in directory.rglob('*')
              if path.is_file() and path.name not in ('start.json', 'receipt.json')}
    require(actual == set(declared) == set(required), ('exact products', str(directory)))
    for name, value in declared.items():
        check_pin(safe_product(directory, name), value)


def check_gates(receipt, state, config):
    command = receipt['command']
    require(command[:3] == [sys.executable, '-B', str(HERE / 'aspect_screen.py')]
            and len(command) == 8 and command[3] == 'screen' and command[4] == '--run'
            and command[6] == '--controls', 'screen command')
    control_name = command[7]
    require(len(control_name) == 10 and control_name.startswith('controls') and control_name[8:].isdigit(), 'control path')
    directory = HERE / control_name
    check_pin(directory / 'receipt.json', receipt['controls_receipt'])
    control = json.loads((directory / 'receipt.json').read_text())
    require(control['mode'] == 'controls' and control['status'] == 'complete'
            and control['before'] == control['after'] == state, 'successful same-state controls')
    check_state(control['before'], config)
    require({'controls.json', 'inherited/summary.json'} <= control['products'].keys(), 'controls product coverage')
    check_products(directory, control['products'], control['products'])
    summary = json.loads((directory / 'controls.json').read_text())
    require(summary['pass'] is True and summary['inherited'] == {'controls': 11, 'pass': True}, 'inherited controls')
    for group, count in [('adapter', 9), ('aspect', 18)]:
        require(summary[group]['pass'] is True and summary[group]['tests_run'] == count, group + ' controls')
    freeze_path = HERE / 'method-freeze.json'
    check_pin(freeze_path, receipt['method_freeze'])
    freeze = json.loads(freeze_path.read_text())
    require(freeze['schema_version'] == 1 and freeze['status'] == 'ready_for_historical'
            and freeze['method_state'] == state and freeze['controls_receipt'] == receipt['controls_receipt'], 'method freeze')
    return {str(directory / 'receipt.json'): pin(directory / 'receipt.json'), str(freeze_path): pin(freeze_path)}


def select_sources(config, helper):
    source_pins, chosen, files, work = {}, {}, {}, {}
    for key in ('early_video', 'c_video', 'early_map', 'c_map'):
        source_pins[key] = check_pin(config[key]['path'], config[key])
    for key, indices, size in [('early_map', EARLY, [320, 224]), ('c_map', REFERENCES, [1280, 720])]:
        path = Path(config[key]['path'])
        raw = json.loads(path.read_text())
        require(all(type(row['source_index']) is int for row in raw), 'source index type')
        by_index = {row['source_index']: row for row in raw}
        require(len(by_index) == len(raw), 'duplicate map index')
        chosen[key] = [by_index[index] for index in indices]
        for ordinal, row in enumerate(chosen[key]):
            require(Fraction(row['source_pts']) * Fraction(row['source_time_base']) == Fraction(row['source_seconds_exact']), 'rational PTS')
            if key == 'early_map':
                require(type(row['quarter_bin']) is int and row['quarter_bin'] == ordinal, 'early sample bin')
                require(Fraction(row['source_seconds_exact']) == Fraction(row['source_index'] * 1001, 30000), 'early PTS/index')
                require(ordinal <= Fraction(row['source_seconds_exact']) < ordinal + Fraction(1001, 30000), 'at-or-after integer sample')
            else:
                require(Fraction(row['source_seconds_exact']) == Fraction(row['source_index'], 30), 'C PTS/index')
            relative = Path(row['png'])
            require(not relative.is_absolute() and '..' not in relative.parts, 'map PNG path')
            image_path = path.parent / relative
            files[str(image_path)] = check_pin(image_path, row)
            with Image.open(image_path) as image:
                require(list(image.size) == size, 'source PNG dimensions')
            work[(key, row['source_index'])] = helper.working(image_path, CROP if key == 'c_map' else None)
    require(len(files) == 41, '41 distinct selected images')
    record = {'source_pins': source_pins, 'early': chosen['early_map'], 'references': chosen['c_map'],
              'early_map': config['early_map']['path'], 'c_map': config['c_map']['path'],
              'dimensions': {'early': [320, 224], 'C': [1280, 720]}}
    return record, files, work


def verify(first, second):
    """Historical entry point: call only after explicit GO for frozen outputs."""
    first, second = Path(first).resolve(), Path(second).resolve()
    require(first == HERE / 'aspect01' and second == HERE / 'aspect02', 'fixed run paths')
    start = time.monotonic()
    audit_pins = {str(path): pin(path) for path in (HELPER, Path(__file__).resolve(), HERE / 'test_independent_check.py')}
    helper = load_helper()
    check_pin(PARENT / 'config.json', {'sha256': FIXED[PARENT / 'config.json']})
    config = json.loads((PARENT / 'config.json').read_text())
    required_products = {'input-map.json', 'input-map-after.json', 'results.json', 'rankings.json', 'paired-summary.json'}
    required_products.update(f'surfaces-{arm}-C{ref}-E{early}.npz' for arm, ref, early in expected_keys())
    receipts, gate_pins = [], {}
    for directory in (first, second):
        receipt = json.loads((directory / 'receipt.json').read_text())
        require(receipt['schema_version'] == 1 and receipt['status'] == 'complete' and receipt['mode'] == 'screen', 'run completed')
        require(receipt['before'] == receipt['after'], 'method before/after')
        require(receipt['command'][5] == directory.name, 'command run directory')
        check_state(receipt['before'], config)
        gate_pins.update(check_gates(receipt, receipt['before'], config))
        require(0 <= receipt['elapsed_s'] <= config['max_seconds'], 'run elapsed bound')
        check_products(directory, receipt['products'], required_products)
        require(sum(p.stat().st_size for p in directory.rglob('*') if p.is_file()) <= config['max_bytes'], 'run byte bound')
        start_record = json.loads((directory / 'start.json').read_text())
        require(start_record['status'] == 'started', 'start receipt status')
        for key, value in start_record.items():
            if key != 'status':
                require(receipt[key] == value, ('start receipt preserved', key))
        receipts.append(receipt)
    require(receipts[0]['before'] == receipts[1]['before'], 'two-run method state')
    require(receipts[0]['products'] == receipts[1]['products'], 'two-run product pins')
    for name in required_products:
        require((first / name).read_bytes() == (second / name).read_bytes(), ('two-run bytes', name))
    method_pins = receipts[0]['before']['pins']
    imap, image_pins, work = select_sources(config, helper)
    for name in ('input-map.json', 'input-map-after.json'):
        require(json.loads((first / name).read_text()) == imap, name + ' exact original rows')
    regions = {key: helper.mask([rectangle], CROP) for key, rectangle in RECTANGLES.items()}
    require([int(regions[key].sum()) for key in METRICS] == [4784, 1363, 1886], 'mask pixel counts')
    require(not any((regions[a] & regions[b]).any() for i, a in enumerate(METRICS) for b in METRICS[i + 1:]), 'mask separation')
    expected_result = {'pairs': 228, 'pairs_per_arm': 114, 'paired_comparisons': 114,
                       'frames_verified_before_and_after': 41, 'surface_shape': [21, 51, 51],
                       'mask_pixels': {k: int(v.sum()) for k, v in regions.items()}, 'human_accepted': False}
    for receipt in receipts:
        same(receipt['result'], expected_result, 'run result')
    rows = json.loads((first / 'results.json').read_text())
    check_rows(rows)
    source_rows = {r['source_index']: r for r in imap['early']}
    ref_rows = {r['source_index']: r for r in imap['references']}
    primary_patches, transformed = {}, {}
    counts = {'pairs': len(rows), 'selected_transforms': 0, 'fitless_pairs': 0,
              'selected_static_evaluation_nulls': 0, 'selected_dynamic_nulls': 0,
              'selected_direct_scores': 0, 'selected_direct_nulls': 0}
    max_error = {'score': 0., 'coverage': 0.}
    for row in rows:
        key = (row['arm'], row['reference_index'], row['source_index'])
        target = work[('c_map', row['reference_index'])]
        for label, original in [('source', source_rows[row['source_index']]), ('reference', ref_rows[row['reference_index']])]:
            for field in ('pts', 'time_base'):
                require(row[label + '_' + field] == original['source_' + field], ('row PTS', key, field))
        with np.load(first / row['surface_file'], allow_pickle=False) as saved:
            require(set(saved.files) == {'fit_scores', 'fit_coverage'}, 'surface fields')
            scores, coverage = saved['fit_scores'], saved['fit_coverage']
        winners = top_two(scores, coverage)
        require(len(row['transforms']) == len(winners), ('transform count', key))
        require(row['missing_reason'] == (None if winners else 'all_fit_transforms_invalid'), 'fit missing reason')
        counts['fitless_pairs'] += not bool(winners)
        primary_patches[key] = None
        for ordinal, ((scale_index, top, left), selected) in enumerate(zip(winners, row['transforms'])):
            counts['selected_transforms'] += 1
            cache_key = (row['arm'], row['source_index'], scale_index)
            if cache_key not in transformed:
                transformed[cache_key] = make_canvas(work[('early_map', row['source_index'])], row['arm'], scale_index)
            canvas, valid, meta = transformed[cache_key]
            patch, pv = canvas[top:top + 120, left:left + 180], valid[top:top + 120, left:left + 180]
            if ordinal == 0:
                primary_patches[key] = (patch, pv)
            fit = direct_record(helper, patch, target, regions['fit'], pv)
            require(fit['score'] is not None, ('selected fit independently invalid', key))
            evaluations = {metric: direct_record(helper, patch, target, regions[metric], pv) for metric in METRICS[1:]}
            expected = {**meta, 'top': top, 'left': left, 'dx': left - 25, 'dy': top - 25,
                        'translation_boundary': left in (0, 50) or top in (0, 50), 'scale_boundary': scale_index in (0, 20),
                        'fit_score': fit['score'], 'fit_coverage': fit['coverage'], 'fit_pixels': fit['pixels'], 'evaluations': evaluations}
            same(selected, expected, f'transform.{key}.{ordinal}')
            require(selected['fit_score'] == float(scores[scale_index, top, left])
                    and selected['fit_coverage'] == float(coverage[scale_index, top, left]), 'selected surface fields')
            for metric, record in [('fit', fit), *evaluations.items()]:
                observed = primary({'transforms': [selected]}, metric)
                max_error['coverage'] = max(max_error['coverage'], abs(observed['coverage'] - record['coverage']))
                if record['score'] is None:
                    counts['selected_direct_nulls'] += 1
                    counts['selected_' + metric + '_nulls'] += 1
                else:
                    counts['selected_direct_scores'] += 1
                    max_error['score'] = max(max_error['score'], abs(observed['score'] - record['score']))
    by_key = {(row['arm'], row['reference_index'], row['source_index']): row for row in rows}
    rankings = {arm: {str(ref): expected_ranking([by_key[(arm, ref, source)] for source in EARLY])
                      for ref in REFERENCES} for arm in ARMS}
    same(json.loads((first / 'rankings.json').read_text()), rankings, 'rankings')
    paired = []
    counts.update(common_support_records=0, common_support_unequal_sets=0, common_support_missing_transform=0,
                  common_support_null_scores=0, common_support_numeric_scores=0)
    for ref in REFERENCES:
        for source in EARLY:
            baseline, alternative = [by_key[(arm, ref, source)] for arm in ARMS]
            patches = [primary_patches[(arm, ref, source)] for arm in ARMS]
            if any(patch is None for patch in patches):
                patches = None
            diagnostics = {metric: common_diagnostic(helper, work[('c_map', ref)], regions[metric], patches)
                           for metric in METRICS[1:]}
            for diagnostic in diagnostics.values():
                counts['common_support_records'] += 1
                if diagnostic['diagnostic'] is None:
                    counts['common_support_missing_transform'] += 1
                else:
                    counts['common_support_unequal_sets'] += diagnostic['valid_sets_equal'] is False
                    for arm in ('baseline', 'alternative'):
                        suffix = 'null_scores' if diagnostic['diagnostic'][arm]['score'] is None else 'numeric_scores'
                        counts['common_support_' + suffix] += 1
            paired.append({'reference_index': ref, 'source_index': source,
                           'metrics': {metric: comparison(primary(baseline, metric), primary(alternative, metric)) for metric in METRICS},
                           'common_support': diagnostics})
    same(json.loads((first / 'paired-summary.json').read_text()), paired, 'paired summary')
    # Recheck current dependency/source/product bytes at the end, not just listed hashes.
    closure = {**method_pins, **gate_pins, **image_pins,
               **{config[k]['path']: imap['source_pins'][k] for k in imap['source_pins']},
               **audit_pins}
    for path, expected in closure.items():
        check_pin(path, expected)
    for directory, receipt in zip((first, second), receipts):
        check_products(directory, receipt['products'], required_products)
        require(json.loads((directory / 'receipt.json').read_text()) == receipt, 'receipt changed during check')
    return {'schema_version': 1, 'status': 'passed', 'human_accepted': False,
            'scope': 'all selected-score direct sums; full saved-surface top-two search, not all FFT scores recomputed',
            'shared_implementation': 'Pillow grayscale/bilinear and pinned prior independent direct/mask helpers; no producer/core imports',
            'runtime': {'python': platform.python_version(), 'numpy': np.__version__, 'pillow': Image.__version__},
            'run_receipts': {str(directory / 'receipt.json'): pin(directory / 'receipt.json') for directory in (first, second)},
            'input_pins': closure, 'method_required_paths': sorted(required_method_paths()),
            'counts': {**counts, 'products_per_run': len(required_products), 'rank_groups': 18,
                       'paired_records': len(paired), 'selected_images': len(image_pins), 'input_pins': len(closure)},
            'maximum_selected_direct_difference': max_error, 'tolerances': {'score': SCORE_TOL, 'coverage': COVERAGE_TOL},
            'two_run_products_byte_identical': True, 'elapsed_s': time.monotonic() - start}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--first', type=Path, default=HERE / 'aspect01')
    parser.add_argument('--second', type=Path, default=HERE / 'aspect02')
    parser.add_argument('--receipt', type=Path, help='Explicit exclusive local receipt; omit for read-only check')
    args = parser.parse_args()
    if args.receipt is not None:
        require(args.receipt.resolve().parent == HERE and not args.receipt.exists(), 'exclusive local receipt only')
    result = verify(args.first, args.second)
    if args.receipt is not None:
        result['command'] = [sys.executable, '-B', str(Path(__file__).resolve()), *sys.argv[1:]]
        with args.receipt.open('x') as stream:
            json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
            stream.write('\n')
    print(json.dumps({key: result[key] for key in ('status', 'counts', 'maximum_selected_direct_difference')}, sort_keys=True))


if __name__ == '__main__':
    main()

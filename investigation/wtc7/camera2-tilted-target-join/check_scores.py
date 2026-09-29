#!/usr/bin/env python3
"""Independent integer-moment replay; no producer/helper imports or video decode."""
import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import re
import sys
import warnings

import numpy as np
from PIL import Image, __version__ as PILLOW_VERSION

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'tilted-camera-source-join'
QUERIES = (6924, 6925, 6926, 6969, 6970, 6971)
RECTANGLES = {'right_half': (320, 16, 632, 464),
              'target_right': (320, 64, 480, 320),
              'right_background': (500, 160, 630, 320)}
FILTERS = {'nearest': Image.Resampling.NEAREST,
           'bilinear': Image.Resampling.BILINEAR}
PROTOCOL_SHA = 'e9345fd05579cfcc7f45b1fa850271eeea8f3f7abe23a80dfb70bc6063364503'
OLD_PINS = {
    'source/TiltedCameraWTC7Clip.mp4': '393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f',
    'source/receipt.json': 'a100331b8e5e66ebb41959811e3ff650750e8284fdba0e4c8dcebdd736ed8ea9',
    'probe01/probe.json': '778c35d099158ddc669316d88ee779cf89f5f5aa9c094cd5e1d5bed596bee1de',
    'probe01/selection.json': 'afd9abc4bd64a0422a749715a8dbb727f7e23447f1c6bf45e9c93d32030f7f6b',
    'views01/frames.json': '2988d1347bd55cba704530c6d3996dcab1cfa6d5b4beebe6d0ad912ccd4d3a15',
    'views01/receipt.json': '4570095ea9c35fac86302f2443969a87261130175edb0de1b7eafa4eefefad29',
    'candidates01/selection.json': '360d4646eb9318da7dd741f3c6be4d57c6c7c6879313514c98826257c7f89552',
    'candidates01/receipt.json': '7032350a5ce8de9297def16dc163c53dae055f16d6f5a18f703b9a3f5f54b778',
}
TOLERANCE = 1e-12


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(data):
    return {'bytes': len(data), 'sha256': sha(data)}


def strict_json(data):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            need(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    def bad_number(value):
        raise ValueError('non-finite JSON number')
    return json.loads(data, object_pairs_hook=unique, parse_constant=bad_number)


def exact(got, expected, label):
    need(type(got) is type(expected), label + ': type')
    if isinstance(expected, dict):
        need(got.keys() == expected.keys(), label + ': keys')
        for key in expected:
            exact(got[key], expected[key], label + '/' + str(key))
    elif isinstance(expected, list):
        need(len(got) == len(expected), label + ': length')
        for i, (a, b) in enumerate(zip(got, expected)):
            exact(a, b, label + '/' + str(i))
    else:
        need(got == expected, label + ': value')


def close(actual, expected, label):
    if expected is None:
        need(actual is None, label + ': null')
        return 0.0
    need(type(actual) in (int, float) and math.isfinite(actual), label + ': finite numeric')
    difference = abs(actual - expected)
    need(difference <= TOLERANCE, label + ': tolerance')
    return difference


def coordinates(rectangle):
    x0, y0, x1, y1 = rectangle
    need(0 <= x0 < x1 <= 640 and 0 <= y0 < y1 <= 480, 'rectangle')
    # Enumerate native coordinates independently of producer's grid-array mask.
    return [(y, x) for y in range(480) for x in range(640)
            if y % 4 == 0 and x % 4 == 0 and x0 <= x < x1 and y0 <= y < y1]


def integer_scores(candidates, query):
    need(isinstance(candidates, np.ndarray) and isinstance(query, np.ndarray), 'arrays')
    need(candidates.dtype == np.uint8 and query.dtype == np.uint8, 'uint8')
    need(candidates.ndim == 2 and query.ndim == 1 and
         candidates.shape[1] == query.size and 0 < query.size <= 307200, 'shape')
    c = candidates.astype(np.int64)
    q = query.astype(np.int64)
    n = int(query.size)
    delta = c - q
    sad = np.maximum(delta, -delta).sum(axis=1, dtype=np.int64)
    sx, sxx = int(q.sum(dtype=np.int64)), int(q @ q)
    sy = c.sum(axis=1, dtype=np.int64)
    syy = np.einsum('ij,ij->i', c, c, dtype=np.int64)
    sxy = c @ q
    vx = n * sxx - sx * sx
    correlations = []
    for y, yy, xy in zip(sy, syy, sxy):
        vy = n * int(yy) - int(y) ** 2
        need(vx >= 0 and vy >= 0, 'integer variance')
        # Products below are Python integers, not overflowing NumPy int64.
        correlations.append(None if vx == 0 or vy == 0 else
                            (n * int(xy) - sx * int(y)) / math.sqrt(vx * vy))
    sums = [int(v) for v in sad]
    return sums, [s / n for s in sums], correlations


def ranking(sums, domain):
    need(len(sums) == len(domain) >= 2 and len(set(domain)) == len(domain), 'rank domain')
    need(all(type(i) is int for i in domain) and
         all(type(s) is int and s >= 0 for s in sums), 'rank values')
    ordered = sorted(zip(sums, domain))
    least, first = ordered[0]
    second_score, second = ordered[1]
    cutoff = ordered[min(4, len(ordered) - 1)][0]
    retained = sorted(i for value, i in ordered if value <= cutoff)
    possible = set(domain)
    neighbors = sorted({j for i in retained for j in (i - 1, i, i + 1) if j in possible})
    ties = sorted(i for value, i in ordered if value == least)
    return {'minimum': first, 'minimum_sad': least, 'minimum_ties': ties,
            'runner_up': second, 'gap_sad': second_score - least,
            'boundary_minimum': min(domain) in ties or max(domain) in ties,
            'rank5_cutoff_sad': cutoff, 'rank5_with_ties': retained,
            'shortlist_with_neighbors': neighbors,
            'rank_order': [i for value, i in ordered]}


def flags(winners):
    repeated, reversed_ = [], []
    for i in range(1, len(winners)):
        previous, current = winners[i - 1], winners[i]
        if previous == current:
            repeated.append([previous, current])
        if current < previous:
            reversed_.append([previous, current])
    return {'repeated_pairs': repeated, 'reversed_pairs': reversed_}


def png_pixels(raw, png_pin, luma_pin, size):
    exact(identity(raw), png_pin, 'PNG identity')
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        with Image.open(io.BytesIO(raw)) as im:
            need(im.format == 'PNG' and im.mode == 'L' and im.size == size and
                 getattr(im, 'n_frames', 1) == 1, 'native PNG contract')
            pixels = im.tobytes()
        need(not seen, 'PNG warning')
    need(len(pixels) == size[0] * size[1] and sha(pixels) == luma_pin, 'luma identity')
    return pixels


def local_dir(name):
    need(type(name) is str and re.fullmatch(r'[a-z][a-z0-9_-]*', name), 'directory name')
    p = HERE / name
    need(p.is_dir() and not p.is_symlink(), 'input directory')
    return p


def output_file(name):
    need(name == 'independent-check01.json', 'only declared output admitted')
    p = HERE / name
    need(not p.exists() and not p.is_symlink(), 'output already exists')
    return p


def self_test():
    tests = []
    def passed(name, condition):
        need(condition, 'self-test ' + name)
        tests.append(name)
    def refusal(name, call):
        try:
            call()
        except (ValueError, TypeError):
            tests.append(name)
        else:
            raise ValueError('self-test refusal failed: ' + name)
    q = np.array([10, 20, 30, 40], dtype=np.uint8)
    c = np.array([[10, 20, 30, 40], [15, 25, 35, 45],
                  [5, 15, 25, 35], [40, 30, 20, 10], [7, 7, 7, 7]], dtype=np.uint8)
    sad, mae, cor = integer_scores(c, q)
    passed('known_copy', sad[0] == 0 and mae[0] == 0 and cor[0] == 1)
    passed('signed_shifts', sad[1:3] == [20, 20] and cor[1:3] == [1, 1])
    passed('reversed_correlation', sad[3] == 80 and cor[3] == -1)
    passed('constant_null', cor[4] is None and integer_scores(c, np.full(4, 2, dtype=np.uint8))[2] == [None]*5)
    extreme = integer_scores(np.array([[255, 0]], dtype=np.uint8), np.array([0, 255], dtype=np.uint8))
    passed('unsigned_wrap_prevention', extreme == ([510], [255.0], [-1.0]))
    x = np.array([2, 4, 9, 1, 8], dtype=np.uint8)
    y = np.array([[3, 1, 7, 9, 2]], dtype=np.uint8)
    got = integer_scores(y, x)
    scalar_sad = sum(abs(int(a)-int(b)) for a, b in zip(x, y[0]))
    xm = sum(map(int, x))/len(x); ym = sum(map(int, y[0]))/len(x)
    numerator = sum((int(a)-xm)*(int(b)-ym) for a, b in zip(x, y[0]))
    denominator = math.sqrt(sum((int(a)-xm)**2 for a in x)*sum((int(b)-ym)**2 for b in y[0]))
    passed('scalar_reference', got[0] == [scalar_sad] and abs(got[2][0]-numerator/denominator) < 1e-15)
    localized = np.array([[0, 0, 0, 255]], dtype=np.uint8)
    passed('localized_difference', integer_scores(localized, np.zeros(4, dtype=np.uint8))[:2] == ([255], [63.75]))
    ranks = ranking([8, 1, 1, 3, 4, 4, 9, 10], list(range(8)))
    passed('rank5_ties', ranks['rank_order'] == [1, 2, 3, 4, 5, 0, 6, 7] and
           ranks['minimum_ties'] == [1, 2] and ranks['rank5_with_ties'] == [1, 2, 3, 4, 5] and
           ranks['shortlist_with_neighbors'] == [0, 1, 2, 3, 4, 5, 6] and ranks['gap_sad'] == 0)
    passed('boundary_neighbors', ranking([0, 1], [0, 1])['shortlist_with_neighbors'] == [0, 1] and
           ranking([0, 1], [0, 1])['boundary_minimum'])
    passed('nonmonotone_repeated', flags([3, 3, 2, 4]) == {'repeated_pairs': [[3, 3]], 'reversed_pairs': [[3, 2]]})
    coords = {k: coordinates(r) for k, r in RECTANGLES.items()}
    passed('explicit_global_grid', {k: len(v) for k, v in coords.items()} ==
           {'right_half': 8736, 'target_right': 2560, 'right_background': 1320} and
           coords['right_half'][0] == (16, 320) and coords['right_half'][-1] == (460, 628) and
           coords['right_background'][-1] == (316, 628))
    native = np.tile(np.arange(720, dtype=np.int64) % 256, (480, 1)).astype(np.uint8)
    perturbed = native.copy(); perturbed[:, :320] = 255-perturbed[:, :320]
    for name, filt in FILTERS.items():
        a = Image.fromarray(native).resize((640, 480), filt).tobytes()
        b = Image.fromarray(perturbed).resize((640, 480), filt).tobytes()
        passed('excluded_left_' + name, all(a[y*640+x] == b[y*640+x]
               for positions in coords.values() for y, x in positions))
    refusal('bad_array_dtype', lambda: integer_scores(c.astype(float), q))
    refusal('empty_samples', lambda: integer_scores(c[:, :0], q[:0]))
    refusal('duplicate_rank_ids', lambda: ranking([1, 2], [0, 0]))
    refusal('boolean_rank_id', lambda: ranking([1, 2], [False, 1]))
    refusal('duplicate_JSON', lambda: strict_json('{"a":1,"a":2}'))
    refusal('nonfinite_JSON', lambda: strict_json('{"a":NaN}'))
    refusal('typed_exact_bool', lambda: exact(True, 1, 'control'))
    refusal('changed_numeric', lambda: close(1e-3, 0, 'control'))
    refusal('changed_null', lambda: close(0, None, 'control'))
    refusal('undeclared_output', lambda: output_file('check_scores.py'))
    return {'status': 'synthetic_controls_pass', 'count': len(tests), 'tests': tests,
            'python': platform.python_version(), 'numpy': np.__version__, 'pillow': PILLOW_VERSION,
            'historical_files_read': False}


def replay(args):
    need(args.reviewed_historical, 'explicit historical gate')
    need(all(isinstance(h, str) and re.fullmatch('[0-9a-f]{64}', h) for h in
             (args.expect_code_sha256, args.extraction_receipt_sha256, args.score_receipt_sha256)), 'explicit pins')
    out = output_file(args.out)
    extraction, score_dir = local_dir(args.extraction), local_dir(args.scores)
    tracked = {}
    def read(path, digest=None, byte_identity=None):
        p = Path(path)
        need(p.is_file() and not p.is_symlink(), 'regular pinned file')
        raw = p.read_bytes(); actual = identity(raw)
        if digest is not None:
            need(actual['sha256'] == digest, 'file digest ' + p.name)
        if byte_identity is not None:
            exact(actual, byte_identity, 'file identity ' + p.name)
        if str(p) in tracked:
            exact(actual, tracked[str(p)], 'input changed between reads')
        tracked[str(p)] = actual
        return raw
    def doc(path, digest=None, byte_identity=None):
        return strict_json(read(path, digest, byte_identity))
    read(Path(__file__).resolve(), args.expect_code_sha256)
    read(HERE/'PROTOCOL.md', PROTOCOL_SHA)
    for name, pin in OLD_PINS.items():
        read(OLD/name, pin)
    er = doc(extraction/'receipt.json', args.extraction_receipt_sha256)
    sr = doc(score_dir/'receipt.json', args.score_receipt_sha256)
    need(er['status'] == 'prepared_pending_independent_verification', 'extraction status')
    exact(er['frame_count'], 476, 'frame count'); exact(er['geometry'], [720, 480], 'geometry')
    need(er['mode'] == 'L' and er['time_base'] == '1/60000' and
         er['sample_aspect_ratio_unapplied'] == '131:144', 'extraction representation')
    exact(er['inputs_before'], er['inputs_after'], 'extraction input repeat')
    need(er['all_full_frame_luma_hashes_and_saved_clocks_match'] is True, 'extraction full checks')
    expected_names = {f'frame-{i:04d}.png' for i in range(476)}
    expected_products = expected_names | {'frames.json', 'inputs-before.json', 'inputs-after.json',
                                         'execution.json', 'decode.stderr', 'python-warnings.json'}
    need(set(er['products']) == expected_products, 'complete extraction products')
    need({p.name for p in extraction.iterdir()} == expected_products | {'receipt.json'}, 'extraction directory membership')
    for name, pin in er['products'].items():
        read(extraction/name, byte_identity=pin)
    exact(doc(extraction/'inputs-before.json'), er['inputs_before'], 'before snapshot')
    exact(doc(extraction/'inputs-after.json'), er['inputs_after'], 'after snapshot')
    need(read(extraction/'decode.stderr') == b'', 'recorded decoder stderr')
    exact(doc(extraction/'python-warnings.json'), [], 'recorded PNG warnings')
    execution = doc(extraction/'execution.json')
    need(execution['failure'] is None and execution['returncode'] == 0 and
         execution['retained_streams_complete'] is True and
         execution['stdout_bytes_retained'] == 246758400 and
         execution['stdout_sha256_retained'] == '164f5725bde62da7da479f46aeea355c4a4bea86411be6c486734330578d2524', 'saved full stream')
    # Review receipt input files only in the declared code/runtime/source scopes.
    permitted_roots = [HERE, OLD, Path('/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies')]
    permitted_exact = {Path('/opt/homebrew/bin/ffmpeg'),
                       Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md')}
    for mapping, with_sizes in ((er['inputs_before'], True), (sr['inputs'], False)):
        for name, pin in mapping.items():
            p = Path(name)
            need(p.is_absolute() and '..' not in p.parts and
                 (p in permitted_exact or any(p.is_relative_to(root) for root in permitted_roots)), 'receipt path outside scope')
            # Runtime binaries may be declared symlinks; hash their resolved file.
            if p.is_symlink():
                resolved = p.resolve()
                raw = resolved.read_bytes(); actual = identity(raw)
                if with_sizes: exact(actual, pin, 'runtime identity')
                else: need(actual['sha256'] == pin, 'runtime digest')
                tracked[str(resolved)] = actual
            else:
                read(p, byte_identity=pin if with_sizes else None, digest=None if with_sizes else pin)
    need(set(sr['outputs']) == {'scores.json', 'summary.json'}, 'score output names')
    scores = doc(score_dir/'scores.json', sr['outputs']['scores.json'])
    summary = doc(score_dir/'summary.json', sr['outputs']['summary.json'])
    exact(scores['candidate_indices'], list(range(476)), 'candidate order')
    maps = doc(extraction/'frames.json'); prior = doc(OLD/'views01/frames.json')
    need(type(maps) is list and len(maps) == len(prior) == 476, 'map domain')
    coordinates_by_region = {k: coordinates(v) for k, v in RECTANGLES.items()}
    flat_indices = {k: np.array([y*640+x for y, x in xy], dtype=np.int64)
                    for k, xy in coordinates_by_region.items()}
    samples = {(branch, region): [] for branch in FILTERS for region in RECTANGLES}
    for i, (row, old) in enumerate(zip(maps, prior)):
        need(set(row) == set(old) | {'time_base', 'png', 'png_identity', 'size', 'mode'}, 'frame fields')
        exact({k: row[k] for k in old}, old, 'old frame identity')
        exact(row['index'], i, 'frame order')
        need(row['png'] == f'frame-{i:04d}.png' and row['time_base'] == '1/60000'
             and row['mode'] == 'L' and row['size'] == [720, 480], 'native row')
        exact(row['png_identity'], er['products'][row['png']], 'PNG product join')
        pixels = png_pixels(read(extraction/row['png']), row['png_identity'], row['luma_sha256'], (720, 480))
        with Image.frombytes('L', (720, 480), pixels) as native:
            for branch, filt in FILTERS.items():
                with native.resize((640, 480), filt) as resized:
                    flat = np.frombuffer(resized.tobytes(), dtype=np.uint8)
                    for region, indices in flat_indices.items():
                        samples[branch, region].append(flat[indices].copy())
    samples = {k: np.stack(v) for k, v in samples.items()}
    selected = doc(OLD/'candidates01/selection.json')
    own_receipt = doc(OLD/'candidates01/receipt.json')
    exact(tracked[str(OLD/'candidates01/selection.json')], own_receipt['selection_pin'], 'Camera2 map receipt')
    need([int(r['frame_index_zero_based']) for r in selected['images']] == list(range(6500, 7201)), 'Camera2 source order')
    by_index = {int(r['frame_index_zero_based']): r for r in selected['images']}
    expected_keys = [(q, b, r) for q in QUERIES for b in FILTERS for r in RECTANGLES]
    need([(r['query'], r['branch'], r['region']) for r in scores['results']] == expected_keys, 'all result rows/order')
    recomputed, maximum_mae, maximum_corr = [], 0.0, 0.0
    for q in QUERIES:
        row = by_index[q]
        need(row['png'] == f'f{q:06d}.png', 'Camera2 name')
        pixels = png_pixels(read(OLD/'candidates01'/row['png']), row['png_identity'], row['luma_sha256'], (640, 480))
        query_flat = np.frombuffer(pixels, dtype=np.uint8)
        for branch in FILTERS:
            for region, indices in flat_indices.items():
                sad, mae, corr = integer_scores(samples[branch, region], query_flat[indices])
                calculated = {'query': q, 'branch': branch, 'region': region, 'samples': len(indices),
                              'sad': sad, 'mae': mae, 'correlation': corr,
                              'ranking': ranking(sad, list(range(476)))}
                produced = scores['results'][len(recomputed)]
                need(set(produced) == set(calculated), 'result fields')
                for key in ('query', 'branch', 'region', 'samples', 'sad', 'ranking'):
                    exact(produced[key], calculated[key], key)
                need(len(produced['mae']) == len(produced['correlation']) == 476, 'metric array length')
                for a, b in zip(produced['mae'], mae): maximum_mae = max(maximum_mae, close(a, b, 'MAE'))
                for a, b in zip(produced['correlation'], corr): maximum_corr = max(maximum_corr, close(a, b, 'correlation'))
                recomputed.append(calculated)
    result_summary = {'queries': list(QUERIES), 'candidate_count': 476, 'score_pairs': 17136,
                      'regions': {k: list(v) for k, v in RECTANGLES.items()},
                      'shortlists': {}, 'branch_region': []}
    for q in QUERIES:
        result_summary['shortlists'][str(q)] = sorted({i for r in recomputed if r['query'] == q
                                                     for i in r['ranking']['shortlist_with_neighbors']})
    for branch in FILTERS:
        for region in RECTANGLES:
            rows = [r for r in recomputed if r['branch'] == branch and r['region'] == region]
            winners = [r['ranking']['minimum'] for r in rows]
            result_summary['branch_region'].append({'branch': branch, 'region': region,
                'winners': winners, 'gaps_mae': [r['ranking']['gap_sad']/r['samples'] for r in rows],
                **flags(winners)})
    exact(summary, result_summary, 'complete summary')
    for path, before in tracked.items():
        exact(identity(Path(path).read_bytes()), before, 'final input pin')
    report = {'status': 'pass_independent_arithmetic_not_historical_authentication',
              'argv': sys.argv, 'checker': tracked[str(Path(__file__).resolve())],
              'python': platform.python_version(), 'numpy': np.__version__, 'pillow': PILLOW_VERSION,
              'absolute_tolerance': TOLERANCE, 'maximum_mae_difference': maximum_mae,
              'maximum_correlation_difference': maximum_corr, 'score_pairs': 17136,
              'native_pngs_checked': 482, 'inputs_before_and_after': tracked,
              'summary': result_summary, 'recomputed_results': recomputed,
              'limits': 'Shared source/Pillow resizing/NumPy; no producer imports, video decode, visual review, independent exposure, light attribution, calibration or human acceptance.'}
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'w') as handle:
        json.dump(report, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')
    return {'status': report['status'], 'output': str(out), 'output_identity': identity(out.read_bytes()),
            'maximum_mae_difference': maximum_mae, 'maximum_correlation_difference': maximum_corr,
            'score_pairs': 17136, 'native_pngs_checked': 482}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--reviewed-historical', action='store_true')
    parser.add_argument('--expect-code-sha256')
    parser.add_argument('--extraction', default='extract01')
    parser.add_argument('--extraction-receipt-sha256')
    parser.add_argument('--scores', default='scores01')
    parser.add_argument('--score-receipt-sha256')
    parser.add_argument('--out', default='independent-check01.json')
    args = parser.parse_args()
    result = self_test() if args.self_test else replay(args)
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Fixed right-side source-content diagnostic, never an exposure authenticator."""
import argparse
import hashlib
import importlib.util
import json
from numbers import Integral
from pathlib import Path
import platform
import re

import numpy as np
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'tilted-camera-source-join'
QUERIES = [6924, 6925, 6926, 6969, 6970, 6971]
REGIONS = {'right_half': (320, 16, 632, 464),
           'target_right': (320, 64, 480, 320),
           'right_background': (500, 160, 630, 320)}
BRANCHES = {'nearest': Image.Resampling.NEAREST,
            'bilinear': Image.Resampling.BILINEAR}
PINS = {
    'PROTOCOL.md': 'e9345fd05579cfcc7f45b1fa850271eeea8f3f7abe23a80dfb70bc6063364503',
    '../tilted-camera-source-join/compare_scenes.py': '80f5e15b66940a3db3f9fc91e52e84a8c3d706f10c3b8cd756ec923884bd73a5',
    '../tilted-camera-source-join/candidates01/selection.json': '360d4646eb9318da7dd741f3c6be4d57c6c7c6879313514c98826257c7f89552',
    '../tilted-camera-source-join/candidates01/receipt.json': '7032350a5ce8de9297def16dc163c53dae055f16d6f5a18f703b9a3f5f54b778',
    '../tilted-camera-source-join/views01/frames.json': '2988d1347bd55cba704530c6d3996dcab1cfa6d5b4beebe6d0ad912ccd4d3a15',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def write_json(path, value):
    with path.open('x') as handle:
        json.dump(value, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')


def safe_dir(name, existing=False):
    require(isinstance(name, str) and re.fullmatch(r'[a-z][a-z0-9_-]*', name), 'unsafe name')
    path = HERE / name
    require(path.is_dir() if existing else not path.exists(), 'output/input existence')
    return path


def mask(rect):
    x0, y0, x1, y1 = rect
    y, x = np.mgrid[0:480:4, 0:640:4]
    return (x >= x0) & (x < x1) & (y >= y0) & (y < y1)


def sampled(native, branch):
    require(native.dtype == np.uint8 and native.shape == (480, 720), 'Tilted raster')
    return np.asarray(Image.fromarray(native).resize((640, 480), BRANCHES[branch]))[::4, ::4]


def absolute_sums(candidates, query):
    c, q = np.asarray(candidates), np.asarray(query)
    require(c.dtype == q.dtype == np.uint8, 'native byte arrays')
    require(c.ndim == 2 and q.ndim == 1 and c.shape[1] == q.size and q.size > 0, 'array shape')
    return np.abs(c.astype(np.int16) - q.astype(np.int16)).sum(axis=1, dtype=np.int64)


def rank_and_retain(sums, ids):
    sums, ids = list(sums), list(ids)
    require(all(isinstance(s, Integral) and not isinstance(s, (bool, np.bool_)) and s >= 0 for s in sums), 'integer nonnegative scores')
    sums = list(map(int, sums))
    require(len(ids) == len(sums) and len(ids) >= 2 and len(set(ids)) == len(ids), 'candidate identities')
    require(all(type(i) is int for i in ids) and all(s >= 0 for s in sums), 'invalid score/identity')
    order = sorted(range(len(ids)), key=lambda k: (sums[k], ids[k]))
    cutoff = sums[order[min(4, len(order)-1)]]
    retained = sorted(ids[k] for k in order if sums[k] <= cutoff)
    domain = set(ids)
    neighbors = sorted({i+d for i in retained for d in (-1, 0, 1) if i+d in domain})
    best, second = order[:2]
    return {'minimum': ids[best], 'minimum_sad': sums[best],
            'minimum_ties': sorted(ids[k] for k in order if sums[k] == sums[best]),
            'runner_up': ids[second], 'gap_sad': sums[second]-sums[best],
            'boundary_minimum': any(ids[k] in (min(ids), max(ids)) for k in order if sums[k] == sums[best]),
            'rank5_cutoff_sad': cutoff, 'rank5_with_ties': retained,
            'shortlist_with_neighbors': neighbors,
            'rank_order': [ids[k] for k in order]}


def ordering_flags(winners):
    return {'repeated_pairs': [[a, b] for a, b in zip(winners, winners[1:]) if a == b],
            'reversed_pairs': [[a, b] for a, b in zip(winners, winners[1:]) if b < a]}


def read_native(path, expected_png, expected_luma, size):
    require(sha(path) == expected_png, 'PNG pin')
    with Image.open(path) as image:
        require(image.format == 'PNG' and image.mode == 'L' and image.size == size and getattr(image, 'n_frames', 1) == 1, 'PNG format')
        pixels = image.tobytes()
        require(hashlib.sha256(pixels).hexdigest() == expected_luma, 'luma pin')
        return np.asarray(image).copy()


def inherited_metrics():
    path = OLD / 'compare_scenes.py'
    require(sha(path) == PINS['../tilted-camera-source-join/compare_scenes.py'], 'helper pin')
    spec = importlib.util.spec_from_file_location('held_scene_metrics', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.metrics


def run(input_name, input_receipt_hash, output_name):
    source = safe_dir(input_name, existing=True)
    out = safe_dir(output_name)
    pins = {str((HERE/p).resolve()): h for p, h in PINS.items()}
    require(re.fullmatch(r'[0-9a-f]{64}', input_receipt_hash), 'receipt hash grammar')
    pins[str(source/'receipt.json')] = input_receipt_hash
    for path, expected in pins.items():
        require(sha(path) == expected, 'input pin')
    for path in (Path(__file__), HERE/'test_match.py', HERE/'mask-sanity.md'):
        pins[str(path)] = sha(path)
    metrics = inherited_metrics()
    receipt = json.loads((source/'receipt.json').read_text())
    # The extractor's generated contract is checked here, never inferred from filenames.
    frame_map = source/'frames.json'
    require(sha(frame_map) == receipt['products']['frames.json']['sha256'], 'frame-map pin')
    pins[str(frame_map)] = sha(frame_map)
    require(receipt['frame_count'] == 476 and receipt['geometry'] == [720, 480], 'extraction contract')
    rows = json.loads(frame_map.read_text())
    prior = json.loads((OLD/'views01/frames.json').read_text())
    require([r['index'] for r in rows] == list(range(476)), 'complete Tilted domain')
    require(len(prior) == 476, 'prior frame domain')
    tilted = {branch: [] for branch in BRANCHES}
    for row, old in zip(rows, prior):
        require(all(row[k] == old[k] for k in ('index', 'pts', 'time_seconds_exact', 'decoded_sha256', 'luma_sha256')), 'Tilted frame identity')
        require(row['png'] == f"frame-{row['index']:04d}.png", 'Tilted basename')
        path = source/row['png']
        require(row['png_identity'] == receipt['products'][row['png']], 'PNG receipt join')
        native = read_native(path, row['png_identity']['sha256'], row['luma_sha256'], (720, 480))
        pins[str(path)] = row['png_identity']['sha256']
        for branch in BRANCHES:
            tilted[branch].append(sampled(native, branch))
    tilted = {branch: np.stack(images) for branch, images in tilted.items()}
    doc = json.loads((OLD/'candidates01/selection.json').read_text())
    require([int(r['frame_index_zero_based']) for r in doc['images']] == list(range(6500, 7201)), 'Camera2 candidate domain')
    query_rows = {int(r['frame_index_zero_based']): r for r in doc['images']}
    results = []
    for qi in QUERIES:
        row = query_rows[qi]
        require(row['png'] == f'f{qi:06d}.png', 'Camera2 basename')
        path = OLD/'candidates01'/row['png']
        query = read_native(path, row['png_identity']['sha256'], row['luma_sha256'], (640, 480))[::4, ::4]
        pins[str(path)] = row['png_identity']['sha256']
        for branch, images in tilted.items():
            for region, rect in REGIONS.items():
                m = mask(rect)
                c, q = images[:, m], query[m]
                sad = absolute_sums(c, q)
                mae, corr = metrics(c, q)
                require(np.allclose(mae, sad/int(m.sum()), rtol=0, atol=1e-12), 'MAE arithmetic disagreement')
                results.append({'query': qi, 'branch': branch, 'region': region,
                                'samples': int(m.sum()), 'sad': sad.tolist(), 'mae': mae.tolist(),
                                'correlation': [float(v) if np.isfinite(v) else None for v in corr],
                                'ranking': rank_and_retain(sad, list(range(476)))})
    summary = {'queries': QUERIES, 'candidate_count': 476, 'score_pairs': len(results)*476,
               'regions': REGIONS, 'shortlists': {}, 'branch_region': []}
    for qi in QUERIES:
        summary['shortlists'][str(qi)] = sorted({i for row in results if row['query'] == qi
                        for i in row['ranking']['shortlist_with_neighbors']})
    for branch in BRANCHES:
        for region in REGIONS:
            matching = [r for r in results if r['branch'] == branch and r['region'] == region]
            winners = [r['ranking']['minimum'] for r in matching]
            summary['branch_region'].append({'branch': branch, 'region': region, 'winners': winners,
                'gaps_mae': [r['ranking']['gap_sad']/r['samples'] for r in matching],
                **ordering_flags(winners)})
    require(all(sha(p) == h for p, h in pins.items()), 'input changed during run')
    out.mkdir()
    write_json(out/'scores.json', {'candidate_indices': list(range(476)), 'results': results})
    write_json(out/'summary.json', summary)
    write_json(out/'receipt.json', {'inputs': pins, 'python': platform.python_version(),
               'numpy': np.__version__, 'pillow': pillow_version,
               'outputs': {n: sha(out/n) for n in ('scores.json', 'summary.json')},
               'limits': 'Candidate shortlist only, not exact exposure identity or light comparison.'})
    print(json.dumps(summary))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--receipt-sha256', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    run(args.input, args.receipt_sha256, args.out)

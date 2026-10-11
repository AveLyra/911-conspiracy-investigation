"""Clip 7 direct-sum check of every retained transform; not full search.
Derived from Clip 3 checker d3bf3a4ef52063344824bea381d5fb41777546d2846f136f13bffd54dd0325a4.
Only population/target paths and explicit terminal/input gates differ.
No image display, matcher import, causal interpretation or data modification.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

if sys.flags.optimize:
    raise RuntimeError('Direct-sum verification requires assertions enabled')

BASE = Path(__file__).resolve().parent
C = BASE.parent
HELPER = C/'verify_selected_scores.py'
assert hashlib.sha256(HELPER.read_bytes()).hexdigest() == '60f9e76c0f469baa6751407226cc5d7baf4350a298fd6c0f6f42d748cdbe59b7'
spec = importlib.util.spec_from_file_location('independent_direct_sums', HELPER)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


PINS = {}


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def pin(path, expected=None):
    path = Path(path)
    assert path.is_file() and not path.is_symlink()
    key, actual = str(path.resolve()), sha(path)
    assert expected is None or expected == actual
    assert key not in PINS or PINS[key] == actual
    PINS[key] = actual
    return actual


def read(path):
    pin(path)
    return json.loads(path.read_bytes())


def main():
    # Terminal gates precede historical score or pixel loading.
    supervisor = read(BASE/'guard-aggregate-a/receipt.json')
    end = read(BASE/'guard-aggregate-a/wrapper-end-checks.json')
    terminal = read(BASE/'aggregate-a/receipt.json')
    assert supervisor['status'] == 'completed' and supervisor['returncode'] == 0
    assert not supervisor.get('shutdown_error') and not supervisor.get('snapshot_errors')
    assert end['status'] == 'passed' and end['changed_dependencies'] == []
    assert end['supervisor_status'] == 'completed' and terminal['status'] == 'completed'
    pin(__file__); pin(HELPER)
    manifest = read(BASE/'manifest.json')
    assert sha(BASE/'manifest.json') == 'ece7d7fbae14d3ec043c16eb845d74af617a06854c267b1e686e7b33d4e6e3ad'
    source = manifest['sources'][0]
    assert source['id'] == 'vince-clip7' and source['indices'] == list(range(1128))
    pin(source['path'], source['sha256'])
    fixture = np.arange(36, dtype=float).reshape(4, 9)
    full = np.ones_like(fixture, dtype=bool)
    assert abs(v.rho(fixture, 7+3*fixture, full)-1) < 1e-12
    assert abs(v.rho(fixture, -fixture, full)+1) < 1e-12
    assert v.rho(fixture, np.ones_like(fixture), full) is None
    regions = C/'regions.json'
    assert hashlib.sha256(regions.read_bytes()).hexdigest() == '5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694'
    t = next(t for t in read(regions)['targets'] if t['id'] == '142')
    assert (t['id'], t['paired_clip']) == ('142', 7)
    target_path = C/t['path']
    pin(target_path, t['sha256'])
    with Image.open(target_path) as im:
        target = np.asarray(im.convert('L').resize((180, 120), Image.Resampling.BILINEAR), dtype=float)
    static, dynamic = [v.mask(t[k], *t['size']) for k in ('static', 'dynamic')]
    pin(BASE/'score-a-01/masks.npz')
    with np.load(BASE/'score-a-01/masks.npz', allow_pickle=False) as masks:
        assert np.array_equal(static, masks['static_142']) and np.array_equal(dynamic, masks['dynamic_142'])
    frames = read(BASE/'extract01/vince-clip7/frames.json')
    assert [r['source_index'] for r in frames] == list(range(1128))
    rows = read(BASE/'aggregate-a/results.json')
    assert [(r['source_index'], r['arm']) for r in rows] == [(i, a) for i in range(1128) for a in ('full', 'even', 'odd')]
    differences, nulls, transforms = [], 0, 0
    for row in rows:
        assert row['target'] == '142' and row['clip'] == 7 and row['paired'] is True
        frame = frames[row['source_index']]
        path = BASE/'extract01/vince-clip7'/frame['file']
        assert frame['png_sha256'] == row['png_sha256']
        pin(path, frame['png_sha256'])
        with Image.open(path) as im:
            assert im.mode == 'RGB' and im.size == (720, 480)
            assert hashlib.sha256(im.tobytes()).hexdigest() == frame['rgb_sha256'] == row['rgb_sha256']
            raster = np.asarray(im)
        if row['arm'] != 'full':
            raster = raster[0 if row['arm'] == 'even' else 1::2]
        working = Image.fromarray(raster).convert('L').resize((180, 120), Image.Resampling.BILINEAR)
        for best in row['best']:
            sw, sh = best['raster_width'], best['raster_height']
            assert best['requested_scale'] in [0.85+i*.025 for i in range(13)]
            assert (sw, sh) == (round(180*best['requested_scale']), round(120*best['requested_scale']))
            scaled = np.asarray(working.resize((sw, sh), Image.Resampling.BILINEAR), dtype=float)
            valid_rows = np.floor((np.arange(sh)+.5)*120/sh).astype(int) < 88
            valid_rows[np.flatnonzero(valid_rows)[-2:]] = False
            canvas = np.zeros((170, 230)); valid = np.zeros_like(canvas, dtype=bool)
            cx, cy = best['canvas_x'], best['canvas_y']
            assert (cx, cy) == (25+(180-sw)//2, 25+(120-sh)//2)
            canvas[cy:cy+sh, cx:cx+sw] = scaled
            valid[cy:cy+sh, cx:cx+sw] = valid_rows[:, None]
            x, y = best['left'], best['top']
            assert 0 <= x <= 50 and 0 <= y <= 50
            a, observed = canvas[y:y+120, x:x+180], valid[y:y+120, x:x+180]
            for region, key in ((static, 'static'), (dynamic, 'dynamic')):
                good = region & observed
                coverage = float(good.sum()/region.sum())
                assert abs(coverage-best[key+'_overlap']) < 1e-10
                calculated = v.rho(a, target, good) if coverage >= .85 else None
                stored = best[key+'_score']
                assert (calculated is None) == (stored is None)
                if calculated is None:
                    nulls += 1
                else:
                    differences.append(abs(calculated-stored))
            transforms += 1
    assert differences and max(differences) < 1e-9
    for path, digest in PINS.items():
        assert sha(path) == digest, 'Dependency changed during direct check'
    print(json.dumps(dict(status='passed', synthetic_checks=3, frames=1128, comparisons=len(rows),
        selected_transforms=transforms, verified_dependencies=len(PINS), code_sha256=sha(__file__), finite_score_checks=len(differences), null_score_checks=nulls,
        max_score_error=max(differences), tolerance=1e-9,
        scope='Every retained transform; direct sums and separate mask indexing; shared Pillow/NumPy; not full-surface recomputation, new image display or historical authentication')))


if __name__ == '__main__':
    main()


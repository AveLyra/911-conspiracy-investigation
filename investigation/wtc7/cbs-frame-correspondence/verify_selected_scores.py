"""Read-only root check of selected pilot scores, without importing its matcher."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parent


def read(name):
    return json.loads((BASE / name).read_text())


def mask(boxes, width, height):
    return np.array([[any(x0 <= (x+.5)*width/180 < x1 and
                         y0 <= (y+.5)*height/120 < y1
                         for x0, y0, x1, y1 in boxes)
                      for x in range(180)] for y in range(120)])


def rho(a, b, valid):
    a, b = a[valid], b[valid]
    if len(a) < 32:
        return None
    a, b = a-a.mean(), b-b.mean()
    va, vb = np.sum(a*a), np.sum(b*b)
    if va/len(a) <= 1e-8 or vb/len(b) <= 1e-8:
        return None
    return float(np.sum(a*b)/np.sqrt(va*vb))


def main():
    inputs = read('pilot01/verified-inputs.json')
    frames = {(r['clip'], r['source_index']): r for r in inputs['frames']}
    targets = {}
    with np.load(BASE/'pilot01/masks.npz', allow_pickle=False) as masks:
        for t in inputs['regions']['targets']:
            with Image.open(BASE/t['path']) as im:
                a = np.asarray(im.convert('L').resize((180, 120), Image.Resampling.BILINEAR), dtype=float)
            s, d = [mask(t[key], *t['size']) for key in ('static', 'dynamic')]
            assert np.array_equal(s, masks['static_'+t['id']])
            assert np.array_equal(d, masks['dynamic_'+t['id']])
            targets[t['id']] = a, s, d
    differences, candidates, nulls = [], 0, 0
    for row in read('pilot01/results.json'):
        frame = frames[row['clip'], row['source_index']]
        path = Path(frame['path'])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == frame['png_sha256']
        with Image.open(path) as image:
            raster = np.asarray(image)
        if row['arm'] != 'full':
            raster = raster[0 if row['arm'] == 'even' else 1::2]
        working = Image.fromarray(raster).convert('L').resize((180, 120), Image.Resampling.BILINEAR)
        target, static, dynamic = targets[row['target']]
        for best in row['best']:
            sw, sh = best['raster_width'], best['raster_height']
            scaled = np.asarray(working.resize((sw, sh), Image.Resampling.BILINEAR), dtype=float)
            valid_rows = np.floor((np.arange(sh)+.5)*120/sh).astype(int) < 88
            valid_rows[np.flatnonzero(valid_rows)[-2:]] = False
            canvas = np.zeros((170, 230)); valid = np.zeros_like(canvas, dtype=bool)
            cx, cy = best['canvas_x'], best['canvas_y']
            canvas[cy:cy+sh, cx:cx+sw] = scaled
            valid[cy:cy+sh, cx:cx+sw] = valid_rows[:, None]
            x, y = best['left'], best['top']
            a, v = canvas[y:y+120, x:x+180], valid[y:y+120, x:x+180]
            for region, key in ((static, 'static'), (dynamic, 'dynamic')):
                good = region & v
                coverage = float(good.sum()/region.sum())
                assert abs(coverage-best[key+'_overlap']) < 1e-10
                calculated = rho(a, target, good) if coverage >= .85 else None
                stored = best[key+'_score']
                assert (calculated is None) == (stored is None)
                if calculated is None:
                    nulls += 1
                else:
                    differences.append(abs(calculated-stored))
            candidates += 1
    assert max(differences) < 1e-9
    print(json.dumps(dict(status='passed', compared_candidates=candidates,
        finite_score_checks=len(differences), null_score_checks=nulls,
        max_score_error=max(differences), scope='Selected transforms only; independent direct sums and mask indexing, shared Pillow/NumPy; not full-surface recomputation or historical authentication')))


if __name__ == '__main__':
    main()

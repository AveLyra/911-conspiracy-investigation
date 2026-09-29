"""Bounded masked image correspondence screening; never a clock authenticator."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import platform
import re
import time
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parent
MAIN = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation')
SIZE = (180, 120)
SCALES = [0.85 + i * 0.025 for i in range(13)]
TARGETS = {
    '148': ('A-370a6ef2789a', '8afb62b6dce6e4618075c66576ef9fdf88295d636427893dc36064afb37a1253',
            [(5, 5, 242, 435), (660, 5, 715, 425)], [(265, 130, 590, 350)]),
    '149': ('A-e43e4088a4a2', '6129afd898a56282579832595715ef2e1093b55d299b693810ac05c72af53469',
            [(5, 95, 265, 435), (660, 5, 715, 425)], [(265, 275, 590, 350)]),
}


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as stream:
        for b in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def save(p, value):
    with Path(p).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def correlate_valid(a, b):
    """sum a[y+i,x+j]*b[i,j] for every fully enclosed b-sized window."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if a.ndim != 2 or b.ndim != 2 or any(x < y for x, y in zip(a.shape, b.shape)):
        raise ValueError('invalid correlation geometry')
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError('nonfinite correlation input')
    shape = tuple(1 << (x + y - 2).bit_length() for x, y in zip(a.shape, b.shape))
    out = np.fft.irfft2(np.fft.rfft2(a, s=shape) * np.fft.rfft2(b[::-1, ::-1], s=shape), s=shape)
    return out[b.shape[0]-1:a.shape[0], b.shape[1]-1:a.shape[1]]


def pearson_surface(image, template, mask, valid, min_coverage=0.85, min_pixels=32):
    """Masked overlapping-pixel means, not a fixed full-template mean."""
    image, template, mask, valid = map(lambda a: np.asarray(a, dtype=float), (image, template, mask, valid))
    if mask.shape != template.shape or valid.shape != image.shape:
        raise ValueError('mask shape')
    if not np.isin(mask, [0, 1]).all() or not np.isin(valid, [0, 1]).all() or mask.sum() == 0:
        raise ValueError('nonbinary or empty mask')
    n = correlate_valid(valid, mask)
    st = correlate_valid(valid, template * mask)
    stt = correlate_valid(valid, template * template * mask)
    sc = correlate_valid(image * valid, mask)
    scc = correlate_valid(image * image * valid, mask)
    stc = correlate_valid(image * valid, template * mask)
    safe = np.maximum(n, 1)
    vt, vc = stt - st * st / safe, scc - sc * sc / safe
    ok = (n >= min_pixels - 1e-7) & (n >= min_coverage * mask.sum() - 1e-7) & (vt/safe > 1e-8) & (vc/safe > 1e-8)
    score = np.full(n.shape, np.nan)
    score[ok] = (stc[ok] - st[ok] * sc[ok] / n[ok]) / np.sqrt(vt[ok] * vc[ok])
    return score, n / mask.sum()


def mask_for(boxes):
    # A working pixel is selected by its corresponding target-pixel center.
    xs = (np.arange(SIZE[0]) + .5) * 720 / SIZE[0]
    ys = (np.arange(SIZE[1]) + .5) * 478 / SIZE[1]
    mask = np.zeros((SIZE[1], SIZE[0]), bool)
    for x0, y0, x1, y1 in boxes:
        mask |= (xs[None, :] >= x0) & (xs[None, :] < x1) & (ys[:, None] >= y0) & (ys[:, None] < y1)
    return mask


def working(im):
    return np.asarray(im.convert('L').resize(SIZE, Image.Resampling.BILINEAR), dtype=float)


def canvas_for(image, scale):
    w, h = SIZE
    sw, sh = round(w * scale), round(h * scale)
    small = Image.fromarray(np.asarray(image, np.uint8)).resize((sw, sh), Image.Resampling.BILINEAR)
    canvas = np.zeros((h + 50, w + 50), float)
    valid = np.zeros_like(canvas)
    x0, y0 = 25 + (w-sw)//2, 25 + (h-sh)//2
    canvas[y0:y0+sh, x0:x0+sw] = np.asarray(small)
    valid[y0:y0+sh, x0:x0+sw] = 1
    return canvas, valid, {'requested_scale': scale, 'raster_width': sw, 'raster_height': sh,
                           'scale_x': sw/w, 'scale_y': sh/h, 'canvas_x': x0, 'canvas_y': y0}


def scalar_pearson(a, b, mask):
    a, b = a[mask], b[mask]
    if len(a) < 32:
        return None
    a, b = a-a.mean(), b-b.mean()
    va, vb = float(np.dot(a,a)), float(np.dot(b,b))
    return float(np.dot(a,b)/np.sqrt(va*vb)) if va/len(a) > 1e-8 and vb/len(b) > 1e-8 else None


def register(image, target, static, dynamic):
    surfaces, overlaps, possibilities = [], [], []
    for scale in SCALES:
        canvas, valid, transform = canvas_for(image, scale)
        scores, coverage = pearson_surface(canvas, target, static, valid)
        surfaces.append(scores)
        overlaps.append(coverage)
        finite = np.flatnonzero(np.isfinite(scores))
        order = sorted(finite, key=lambda i: (-scores.flat[i], i))[:2]
        for index in order:
            y, x = np.unravel_index(index, scores.shape)
            region = canvas[y:y+SIZE[1], x:x+SIZE[0]]
            good = dynamic & valid[y:y+SIZE[1], x:x+SIZE[0]].astype(bool)
            fraction = float(good.sum()/dynamic.sum())
            possibilities.append({'static_score': float(scores[y,x]), 'static_overlap': float(coverage[y,x]),
                                  'dynamic_score': scalar_pearson(region, target, good) if fraction >= .85 else None,
                                  'dynamic_overlap': fraction, 'left': int(x), 'top': int(y),
                                  'dx': int(x)-25, 'dy': int(y)-25, **transform})
    possibilities.sort(key=lambda d: (-d['static_score'], d['requested_scale'], d['top'], d['left']))
    return possibilities[:2], np.array(surfaces), np.array(overlaps)


def controls(out):
    rng = np.random.default_rng(81493)
    a = rng.normal(size=(11, 13)); b = rng.normal(size=(5, 7))
    direct = np.array([[np.sum(a[y:y+5,x:x+7]*b) for x in range(7)] for y in range(7)])
    correlation_error = float(np.max(np.abs(correlate_valid(a,b)-direct)))
    im = rng.uniform(20, 230, (170, 230)); target = im[19:139, 31:211].copy()
    mask = np.ones_like(target, bool); valid = np.ones_like(im, bool)
    score, _ = pearson_surface(im, target, mask, valid)
    y, x = np.unravel_index(np.nanargmax(score), score.shape)
    translated = (int(y), int(x)) == (19,31) and abs(score[y,x]-1) < 1e-10
    gain, _ = pearson_surface(im*1.3+17, target, mask, valid)
    photometric = np.max(np.abs(gain-score)) < 1e-10
    flat, _ = pearson_surface(np.ones_like(im), target, mask, valid)
    rejected_flat = not np.isfinite(flat).any()
    rejected = False
    try:correlate_valid(np.array([[np.nan]]), np.ones((1,1)))
    except ValueError:rejected = True
    # Exact duplicate windows cannot yield unique identity.
    tile = rng.uniform(20,230,(8,8)); repeated = np.tile(tile,(3,3))
    rep, _ = pearson_surface(repeated,tile,np.ones_like(tile),np.ones_like(repeated))
    repeat_peaks = int(np.sum(np.abs(rep-1)<1e-10))
    static = mask_for(TARGETS['149'][2]); dyn=mask_for(TARGETS['149'][3])
    scene = rng.integers(20,230,(120,180),dtype=np.uint8)
    changed = scene.copy();changed[dyn]=rng.integers(20,230,int(dyn.sum()),dtype=np.uint8)
    st_same = scalar_pearson(scene.astype(float),changed.astype(float),static)
    dyn_different = scalar_pearson(scene.astype(float),changed.astype(float),dyn)
    identity_best, _, _ = register(scene.astype(float),scene.astype(float),static,dyn)
    identity = identity_best[0]
    translated_image = Image.fromarray(scene).transform(SIZE,Image.Transform.AFFINE,(1,0,3,0,1,2),
                                                      resample=Image.Resampling.BILINEAR)
    crop_best, _, _ = register(scene.astype(float),np.asarray(translated_image,dtype=float),static,dyn)
    crop = crop_best[0]
    scaled = Image.fromarray(scene).resize((184,123),Image.Resampling.BILINEAR).crop((2,1,182,121))
    buf=io.BytesIO();scaled.save(buf,format='JPEG',quality=65);buf.seek(0)
    with Image.open(buf) as encoded: scaled_target=np.asarray(encoded,dtype=float)
    scaled_best, _, _ = register(scene.astype(float),scaled_target,static,dyn)
    scaled_match = scaled_best[0]
    checks={'linear_correlation_oracle':correlation_error < 1e-10,'known_translation':bool(translated),
            'linear_gain_offset_invariance':bool(photometric),'flat_candidate_rejected':rejected_flat,
            'nonfinite_rejected':rejected,'repeated_geometry_not_unique':repeat_peaks>=9,
            'static_and_dynamic_masks_disjoint':not bool((static&dyn).any()),
            'dynamic_change_not_geometry_evidence':st_same is not None and abs(st_same-1)<1e-10 and abs(dyn_different)<.1,
            'registration_identity':identity['static_score']>1-1e-10 and identity['dx']==0 and identity['dy']==0 and abs(identity['requested_scale']-1)<1e-10,
            'registration_crop_translation':crop['static_score']>1-1e-10 and crop['dx']==3 and crop['dy']==2 and abs(crop['requested_scale']-1)<1e-10,
            'resize_jpeg_geometry':scaled_match['static_score']>.85 and scaled_match['dx']==0 and scaled_match['dy']==-1 and abs(scaled_match['requested_scale']-1.025)<1e-10}
    save(out/'summary.json',{'checks':checks,'correlation_error':correlation_error,'repeat_peaks':repeat_peaks,
                            'static_unchanged_score':st_same,'dynamic_changed_score':dyn_different,
                            'registration_identity':identity,'registration_crop_translation':crop,'resize_jpeg_geometry':scaled_match,
                            'script_sha256':sha(__file__),'pass':all(checks.values())})
    if not all(checks.values()):raise ValueError('synthetic control failure')
    return {'controls':len(checks),'pass':True}


def screen(out, control_run):
    gate=json.loads((BASE/control_run/'summary.json').read_text())
    if not gate['pass'] or gate['script_sha256']!=sha(__file__):raise ValueError('control gate stale or failed')
    frames_path=MAIN/'fire-originals/peskin/derivatives/run01/frames.json'
    rows=[r for r in json.loads(frames_path.read_text()) if 2502<=r['integer_second_bin']<2534]
    if [r['integer_second_bin'] for r in rows]!=list(range(2502,2534)):raise ValueError('frame coverage')
    targets={};inputs={};results=[];start=time.monotonic()
    for key,(asset,digest,sboxes,dboxes) in TARGETS.items():
        p=MAIN/'fire-annotation/assets/run-01/images'/f'{asset}.jpg'
        if sha(p)!=digest:raise ValueError('target pin')
        with Image.open(p) as im:
            if im.size!=(720,478):raise ValueError('target size')
            targets[key]=(working(im),mask_for(sboxes),mask_for(dboxes))
        inputs[asset]=digest
    for r in rows:
        if time.monotonic()-start>290:raise ValueError('wall time cap')
        p=MAIN/'fire-originals/peskin/derivatives/run01'/r['png']
        if sha(p)!=r['sha256'] or p.stat().st_size!=r['bytes']:raise ValueError('sample pin')
        with Image.open(p) as im:
            if im.size!=(1620,1080):raise ValueError('sample geometry')
            work=working(im)
        for key,args in targets.items():
            best,scores,overlap=register(work,*args)
            with (out/f"scores-{key}-{r['integer_second_bin']}.npz").open('xb') as stream:
                np.savez_compressed(stream,scores=scores,overlap=overlap)
            results.append({'target':key,'integer_second_bin':r['integer_second_bin'],
                            'source_pts':r['source_pts'],'source_time_base':r['source_time_base'],
                            'source_sample_sha256':r['sha256'],'geometry_candidates':best})
    save(out/'results.json',results)
    short={}
    for key in targets:
        rr=[r for r in results if r['target']==key and r['geometry_candidates']]
        by_static=sorted(rr,key=lambda r:-r['geometry_candidates'][0]['static_score'])[:4]
        by_dynamic=sorted([r for r in rr if r['geometry_candidates'][0]['dynamic_score'] is not None],
                          key=lambda r:-r['geometry_candidates'][0]['dynamic_score'])[:4]
        short[key]={'static':[r['integer_second_bin'] for r in by_static],
                    'dynamic':[r['integer_second_bin'] for r in by_dynamic]}
    return {'samples':len(rows),'comparisons':len(results),'shortlist':short,'frame_index_sha256':sha(frames_path),
            'target_pins':inputs,'elapsed_seconds':time.monotonic()-start}


def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['controls','screen']);p.add_argument('--run',required=True)
    p.add_argument('--controls',default='controls01');a=p.parse_args()
    if not all(re.fullmatch(r'[a-z][a-z0-9]{1,24}',s) for s in (a.run,a.controls)):raise ValueError('run name')
    out=BASE/a.run;out.mkdir(exist_ok=False)
    receipt={'mode':a.mode,'script_sha256':sha(__file__),'protocol_sha256':sha(BASE/'PROTOCOL.md'),
             'method_sha256':sha(BASE/'METHOD-01.md'),'python':platform.python_version(),
             'numpy':np.__version__,'pillow':Image.__version__,'status':'started'}
    save(out/'start.json',receipt)
    try:
        receipt['result']=controls(out) if a.mode=='controls' else screen(out,a.controls)
        receipt['status']='completed';save(out/'receipt.json',receipt)
        print(json.dumps({'status':'completed','mode':a.mode,'result':receipt['result']}))
    except Exception as e:
        receipt['status']='failed';receipt['exception_type']=type(e).__name__
        receipt['message']=str(e) if isinstance(e,ValueError) else 'Inspect local context; no source metadata printed'
        save(out/'failure.json',receipt);print(json.dumps({'status':'failed','type':type(e).__name__}));raise SystemExit(1)


if __name__=='__main__':main()

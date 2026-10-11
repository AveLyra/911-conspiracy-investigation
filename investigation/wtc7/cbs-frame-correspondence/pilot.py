"""Bounded CBS correspondence pilot; existing PNG inputs only, never a decoder.

Numerical primitives are imported from the hash-pinned, unchanged Peskin core.
Importing this module reads code only; historical input verification is explicit.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import platform
import re
import signal
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parent
CORE_PATH = BASE.parent / 'peskin-figure-correspondence/match_screen.py'
CORE_SHA = '06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8'
SAMPLER_SHA = 'c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d'
ARMS = ('full', 'even', 'odd')
EPSILONS = (.005, .01, .02)
TIME_BASE = '333673/10000000'
MAX_SECONDS, MAX_BYTES = 240, 256 * 1024**2
INHERITED = {
    'core-controls01/summary.json': '175019b3d873ea8632ea14dd4cec1fd4dc35b6c3f9557dab7503491d4e7ffcc7',
    'direct-controls01.json': 'a25c649085119b697318719f9d402413f5fa9dedf2f42762379273b8b7365830',
    'core-comparison01.json': '6787f9fee58c22733d71ac6d2cd587953eb86a8f63b27bbb8f408135e0aaed2a',
}
CLIPS = (
    dict(clip=3, stage=2, count=189, bytes=23621148,
         source_sha256='ced46b4c4318ef53c38eaf9485b76efa4d4d2c155b7194871a8479f0841a993d',
         frames_sha256='e854216730cab2613a15408742d840a2ceff0f71956362715d3d219e83f5129e',
         receipt_sha256='7bbcfacf93d4d9d9000e9e45f8227e9c41b27493a1118148e1c1e21fa55a8afe',
         manifest_sha256='5689b7a6ec0c0969d36d8140db041dc7d47874ddb808f28b62845cb4e0203cb6'),
    dict(clip=7, stage=4, count=1128, bytes=140334936,
         source_sha256='a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b',
         frames_sha256='15a0d0ae2b7d0f650688abf90bd474f7f1dafdb8f6a595a3ad9e046b980d9e0f',
         receipt_sha256='3e262eee0d72b9e9e495192014a1daee061e30505fb09104dd01a07404fad0c8',
         manifest_sha256='8cfc8ac6ce67b0c1ca15c874b3663a638585798bb3aba8461bfe2b5c4fbc4fd6'),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def pin(path, expected, pins):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), 'missing or symbolic-link input')
    digest = sha(path)
    require(digest == expected, 'input hash mismatch')
    pins[str(path.resolve())] = digest


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def nonfinite(_):
        raise ValueError('nonfinite JSON value')
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs, parse_constant=nonfinite)


require(sha(CORE_PATH) == CORE_SHA, 'numerical core hash mismatch')
_spec = importlib.util.spec_from_file_location('cbs_pinned_core', CORE_PATH)
core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(core)


def mask_for(boxes, size):
    require(len(size) == 2 and all(type(n) is int and n > 0 for n in size), 'target dimensions')
    w, h = size
    xs = (np.arange(180) + .5) * w / 180
    ys = (np.arange(120) + .5) * h / 120
    mask = np.zeros((120, 180), bool)
    for box in boxes:
        require(len(box) == 4 and all(type(n) is int for n in box), 'rectangle coordinates')
        x0, y0, x1, y1 = box
        require(0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h, 'rectangle bounds')
        mask |= (xs[None, :] >= x0) & (xs[None, :] < x1) & (ys[:, None] >= y0) & (ys[:, None] < y1)
    require(mask.any(), 'empty working mask')
    return mask


def representations(image):
    require(image.mode == 'RGB' and image.size == (720, 480), 'native candidate geometry/mode')
    raster = np.asarray(image)
    return {arm: core.working(Image.fromarray(rows)) for arm, rows in
            (('full', raster), ('even', raster[::2]), ('odd', raster[1::2]))}


def working_validity():
    mask = np.zeros((120, 180), bool)
    mask[:88] = True
    return mask


def guarded_canvas(image, scale):
    canvas, _, transform = core.canvas_for(image, scale)
    sw, sh = transform['raster_width'], transform['raster_height']
    scaled = np.array(Image.fromarray(working_validity()).resize((sw, sh), Image.Resampling.NEAREST))
    valid_rows = np.flatnonzero(scaled.any(axis=1))
    require(len(valid_rows) >= 2, 'guard validity geometry')
    scaled[valid_rows[-2:]] = False
    valid = np.zeros_like(canvas, dtype=bool)
    x, y = transform['canvas_x'], transform['canvas_y']
    valid[y:y+sh, x:x+sw] = scaled
    return canvas, valid, transform


def register(image, target, static, dynamic, check=lambda: None):
    for raster in (image, target):
        require(raster.shape == (120, 180) and np.isfinite(raster).all(), 'working image geometry/nonfinite')
    for mask in (static, dynamic):
        require(mask.shape == (120, 180) and mask.dtype == bool and mask.any(), 'working mask')
    require(not (static & dynamic).any(), 'overlapping static/dynamic masks')
    possibilities, surfaces, overlaps = [], [], []
    for scale in core.SCALES:
        check()
        canvas, valid, transform = guarded_canvas(image, scale)
        scores, coverage = core.pearson_surface(canvas, target, static, valid)
        surfaces.append(scores)
        overlaps.append(coverage)
        order = sorted(np.flatnonzero(np.isfinite(scores)), key=lambda i: (-scores.flat[i], i))[:2]
        for index in order:
            y, x = np.unravel_index(index, scores.shape)
            region = canvas[y:y+120, x:x+180]
            good = dynamic & valid[y:y+120, x:x+180]
            fraction = float(good.sum() / dynamic.sum())
            possibilities.append(dict(static_score=float(scores[y, x]), static_overlap=float(coverage[y, x]),
                dynamic_score=core.scalar_pearson(region, target, good) if fraction >= .85 else None,
                dynamic_overlap=fraction, left=int(x), top=int(y), dx=int(x)-25, dy=int(y)-25, **transform))
    possibilities.sort(key=lambda d: (-d['static_score'], d['requested_scale'], d['top'], d['left']))
    check()
    return possibilities[:2], np.array(surfaces), np.array(overlaps)


def verify_clip(spec, source_root, pins):
    """Verify received-byte identity and stored products; not camera authenticity."""
    n = spec['clip']
    stage = Path(source_root) / f"stage{spec['stage']}"
    source = stage / f'raw/clip{n}-attempt1.avi'
    directory = stage / f'run01/vince-clip{n}'
    for path, key in ((source, 'source_sha256'), (directory/'frames.json', 'frames_sha256'),
                      (directory/'receipt.json', 'receipt_sha256'),
                      (stage/'run01/manifest.input.json', 'manifest_sha256')):
        pin(path, spec[key], pins)
    require(source.stat().st_size == spec['bytes'], 'source byte count')
    # Existing sampler selects first PTS at or after each rational eighth.
    indices = [(j*(spec['count']-1)+7)//8 for j in range(9)]
    expected_source = dict(id=f'vince-clip{n}', path=str(source.resolve()), sha256=spec['source_sha256'],
                           bytes=spec['bytes'], count=spec['count'], indices=indices)
    receipt = load(directory/'receipt.json')
    source_entries = [s for s in load(stage/'run01/manifest.input.json')['sources'] if s['id'] == expected_source['id']]
    require(source_entries == [expected_source] and receipt['source'] == expected_source, 'source manifest join')
    require(receipt['schema'] == 'late-fire-sequence-v1' and not receipt['reasons'] and
            receipt['structure'] == 'inventory_and_products_checked' and
            receipt['admission'] == 'descriptive_candidate_pending_independent_and_human_review' and
            receipt['scientific_or_human_acceptance'] is False, 'source receipt status')
    require(receipt['pins']['manifest_sha256'] == spec['manifest_sha256'] and
            receipt['pins']['code_sha256'] == SAMPLER_SHA, 'source receipt pins')
    identity = dict(bytes=spec['bytes'], sha256=spec['source_sha256'])
    require(receipt['source_identity'] == dict(before=identity, after=identity, status='matched_before_and_after'),
            'source before/after identity')
    for kind in ('probe', 'decode'):
        diagnostic = receipt[kind+'_diagnostics']
        require(diagnostic['status'] == 'clean' and not diagnostic['rejected'], 'saved diagnostic status')
    probe_path = directory/'probe.stdout'
    pin(probe_path, sha(probe_path), pins)
    probe = load(probe_path)
    require(len(probe['frames']) == spec['count'], 'probe frame count')
    streams = probe['streams']
    require(len(streams) == 1 and streams[0]['time_base'] == TIME_BASE, 'probe time base')
    for index, frame in enumerate(probe['frames']):
        require(type(frame['pts']) is int and frame['pts'] == index and frame['width'] == 720 and
                frame['height'] == 480 and frame['sample_aspect_ratio'] == '8:9' and
                frame['interlaced_frame'] == 1 and frame['top_field_first'] == 0, 'probe frame identity')
    rows = load(directory/'frames.json')
    require([r['source_index'] for r in rows] == indices, 'missing/duplicate/out-of-order frame')
    for ordinal, row in enumerate(rows, 1):
        index = row['source_index']
        require(type(index) is int and type(row['pts']) is int and row['pts'] == probe['frames'][index]['pts'] and
                row['time_base'] == TIME_BASE and row['pts_seconds_exact'] == str(row['pts']*Fraction(TIME_BASE)),
                'frame PTS join')
        require((row['width'], row['height'], row['sample_aspect_ratio'], row['interlaced_frame'],
                 row['top_field_first']) == (720, 480, '8:9', 1, 0), 'frame geometry/field metadata')
        require(row['file'] == f'native/frame-{ordinal:06d}.png', 'unexpected PNG path')
        path = directory/row['file']
        pin(path, row['png_sha256'], pins)
        with Image.open(path) as image:
            require(image.format == 'PNG' and image.mode == 'RGB' and image.size == (720, 480), 'PNG format/mode/size')
            require(hashlib.sha256(image.tobytes()).hexdigest() == row['rgb_sha256'], 'decoded RGB hash')
    return [dict(clip=n, path=str(directory/r['file']), **r) for r in rows]


def summarize(results):
    groups, shortlist = [], set()
    keys = sorted({(r['target'], r['clip'], r['arm'], r['paired']) for r in results})
    for target, clip, arm, paired in keys:
        rows = [r for r in results if (r['target'], r['clip'], r['arm'], r['paired']) == (target, clip, arm, paired)]
        for metric in ('static_score', 'dynamic_score'):
            ranked = [(r['source_index'], r['best'][0][metric]) for r in rows
                      if r['best'] and r['best'][0][metric] is not None]
            require(all(np.isfinite(score) for _, score in ranked), 'nonfinite summary score')
            ranked.sort(key=lambda pair: (-pair[1], pair[0]))
            best = ranked[0][1] if ranked else None
            groups.append(dict(target=target, clip=clip, arm=arm, paired=paired, metric=metric,
                compared_frames=len(rows), finite_frames=len(ranked), best_score=best,
                reason=None if ranked else 'no valid score at best static transform',
                ranked=[dict(source_index=i, score=s) for i, s in ranked],
                epsilon_sets={str(e): sorted(i for i, s in ranked if best-s <= e) for e in EPSILONS}))
            if paired:
                shortlist.update((clip, index) for index, _ in ranked[:2])
    require(len(shortlist) <= 24, 'pilot shortlist cap')
    return dict(groups=groups, shortlist=[dict(clip=c, source_index=i) for c, i in sorted(shortlist)])


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()


class Output:
    """Create-only writes; reserve one MiB for a terminal receipt after failure."""
    def __init__(self, path, seconds=MAX_SECONDS, byte_cap=MAX_BYTES):
        require(0 < seconds <= MAX_SECONDS and 1024**2 < byte_cap <= MAX_BYTES, 'invalid execution caps')
        self.path, self.seconds, self.byte_cap = Path(path), seconds, byte_cap
        self.path.mkdir(exist_ok=False)
        self.started, self.written = time.monotonic(), 0

    def check(self):
        require(time.monotonic()-self.started <= self.seconds, 'elapsed-time cap exceeded')

    def write(self, name, payload, terminal=False):
        require(Path(name).name == name, 'output name')
        limit = self.byte_cap if terminal else self.byte_cap-1024**2
        require(self.written+len(payload) <= limit, 'output-byte cap exceeded')
        with (self.path/name).open('xb') as stream:
            stream.write(payload)
        self.written += len(payload)

    def json(self, name, value, terminal=False):
        self.write(name, json_bytes(value), terminal)

    def npz(self, name, **arrays):
        buffer = io.BytesIO()
        np.savez_compressed(buffer, **arrays)
        self.write(name, buffer.getvalue())


def gate_controls(path, pins):
    path = Path(path)
    pin(path, sha(path), pins)
    result = load(path)
    require(result['status'] == 'passed' and result['tests_run'] > 0 and result['failures'] == [] and
            result['errors'] == [] and result['skipped'] == [] and result['pilot_sha256'] == sha(__file__) and
            result['tests_sha256'] == sha(BASE/'test_pilot.py') and result['core_sha256'] == CORE_SHA,
            'adapter controls failed or stale')
    for name, digest in INHERITED.items():
        pin(BASE/name, digest, pins)
    require(load(BASE/'core-controls01/summary.json')['pass'] is True and
            load(BASE/'direct-controls01.json')['status'] == 'passed' and
            load(BASE/'core-comparison01.json')['status'] == 'passed', 'inherited control gate')


def comparisons(frames, targets, output):
    results = []
    for frame in frames:
        output.check()
        # All files were verified before the first score; recheck each PNG at use.
        require(sha(frame['path']) == frame['png_sha256'], 'PNG changed before score')
        with Image.open(frame['path']) as image:
            arms = representations(image)
        for target, data in targets.items():
            for arm in ARMS:
                best, scores, overlap = register(arms[arm], *data['arrays'], check=output.check)
                name = f"scores-{target}-clip{frame['clip']}-{frame['source_index']:06d}-{arm}.npz"
                output.npz(name, scores=scores, coverage=overlap)
                results.append(dict(target=target, clip=frame['clip'], arm=arm,
                    paired=frame['clip'] == data['paired_clip'], source_index=frame['source_index'],
                    pts=frame['pts'], time_base=frame['time_base'], pts_seconds_exact=frame['pts_seconds_exact'],
                    png_sha256=frame['png_sha256'], rgb_sha256=frame['rgb_sha256'],
                    surfaces=name, surfaces_sha256=sha(output.path/name), best=best,
                    invalid_reason=None if best else 'no static transform passed count/coverage/variance gates'))
    return results


def run(output, controls, protocol_sha, regions_sha):
    pins = {}
    for path, digest in ((BASE/'PROTOCOL.md', protocol_sha), (BASE/'regions.json', regions_sha),
                         (CORE_PATH, CORE_SHA), (Path(__file__), sha(__file__)),
                         (BASE/'test_pilot.py', sha(BASE/'test_pilot.py'))):
        pin(path, digest, pins)
    gate_controls(controls, pins)
    regions = load(BASE/'regions.json')
    require(regions['schema'] == 'cbs-correspondence-regions-v1' and
            [(t['id'], t['paired_clip']) for t in regions['targets']] == [('143', 3), ('142', 7)], 'target population')
    frames = []
    for spec in CLIPS:
        output.check()
        frames.extend(verify_clip(spec, BASE.parent/'cbs-vince-source-screen', pins))
    require(len(frames) == 18, 'pilot population')
    targets, mask_arrays = {}, {'working_valid': working_validity()}
    for t in regions['targets']:
        path = BASE/t['path']
        pin(path, t['sha256'], pins)
        with Image.open(path) as image:
            require(image.format == 'JPEG' and list(image.size) == t['size'], 'target format/size')
            arrays = (core.working(image), mask_for(t['static'], t['size']), mask_for(t['dynamic'], t['size']))
        require(not (arrays[1] & arrays[2]).any(), 'overlapping target masks')
        targets[t['id']] = dict(paired_clip=t['paired_clip'], arrays=arrays)
        mask_arrays['static_'+t['id']], mask_arrays['dynamic_'+t['id']] = arrays[1:]
    transforms = []
    for index, scale in enumerate(core.SCALES):
        _, valid, transform = guarded_canvas(np.zeros((120, 180)), scale)
        mask_arrays[f'scaled_canvas_valid_{index:02d}'] = valid
        transforms.append(transform)
    output.json('verified-inputs.json', dict(pins=pins, frames=frames, regions=regions,
        transforms=transforms, receipt_scope='Stored product checks and received-byte identity, not historical authenticity'))
    output.npz('masks.npz', **mask_arrays)
    results = comparisons(frames, targets, output)
    require(len(results) == 108, 'comparison population')
    summary = summarize(results)
    output.json('results.json', results)
    output.json('summary.json', summary)
    for path, digest in pins.items():
        output.check()
        require(sha(path) == digest, 'input changed during pilot')
    output.check()
    return dict(comparisons=len(results), frames=len(frames), shortlist=summary['shortlist'],
                scientific_or_human_acceptance=False, status='descriptive_candidates_only')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    parser.add_argument('--controls', required=True)
    parser.add_argument('--protocol-sha256', required=True)
    parser.add_argument('--regions-sha256', required=True)
    args = parser.parse_args()
    require(re.fullmatch(r'pilot[0-9]{2,3}', args.run), 'run name must be pilotNN')
    require(all(re.fullmatch(r'[a-f0-9]{64}', value) for value in
                (args.protocol_sha256, args.regions_sha256)), 'protocol/regions pin format')
    output = Output(BASE/args.run)
    receipt = dict(argv=sys.argv, pilot_sha256=sha(__file__), core_sha256=CORE_SHA,
        protocol_sha256=args.protocol_sha256, regions_sha256=args.regions_sha256,
        python=platform.python_version(), numpy=np.__version__, pillow=Image.__version__,
        requested_seconds=MAX_SECONDS, requested_output_bytes=MAX_BYTES,
        timer_limit='Wall timer plus between-operation checks; a native call may delay Python signal handling.',
        status='started')
    output.json('start.json', receipt)
    def timeout(_signum, _frame):
        raise TimeoutError('elapsed-time cap exceeded')
    previous = signal.signal(signal.SIGALRM, timeout)
    signal.setitimer(signal.ITIMER_REAL, max(.001, MAX_SECONDS-(time.monotonic()-output.started)))
    try:
        receipt['result'] = run(output, args.controls, args.protocol_sha256, args.regions_sha256)
        output.check()
        receipt['status'] = 'completed'
    except Exception as exc:
        receipt.update(status='failed', exception_type=type(exc).__name__, message=str(exc)[:500])
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
    receipt['elapsed_seconds'] = time.monotonic()-output.started
    receipt['output_bytes_before_terminal_receipt'] = sum(p.stat().st_size for p in output.path.iterdir())
    output.json('receipt.json' if receipt['status'] == 'completed' else 'failure.json', receipt, terminal=True)
    print(json.dumps(dict(status=receipt['status'], elapsed_seconds=receipt['elapsed_seconds'])))
    return 0 if receipt['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())

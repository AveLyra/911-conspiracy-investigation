"""Read-only post-aggregate audit. No image decoder/viewer or numerical matcher.

Default mode refuses before loading any score/result file unless aggregate,
supervisor and wrapper terminal records all report successful completion.
--self-test uses tiny synthetic arrays/records only. Output is stdout JSON.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

import numpy as np

V = Path(__file__).resolve().parent
C = V.parents[1]
ARMS = ('full', 'even', 'odd')
SCALES = [0.85+i*.025 for i in range(13)]
COVERAGE_ATOL = 1e-10  # FFT count fractions versus direct integer-count fractions.
COUNT_GATE_TOLERANCE = 1e-7  # Explicit inherited numerical-core convention.
PLAN = 'e25d3568d8dbdd5f66d4d3004fb334d8eda2025cc3021860f64534d399902abe'
MANIFEST = 'fc5b819e2079a2d7675e174f93b8584e733d5b735f9cc70f708ff1f2c54c752b'
PINS = {}


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def pin(path, digest=None):
    path = Path(path)
    need(path.is_file() and not path.is_symlink(), 'missing/symlink input: '+str(path))
    key = str(path.resolve())
    actual = sha(path)
    need(digest is None or actual == digest, 'hash mismatch: '+key)
    need(key not in PINS or actual == PINS[key], 'changed input: '+key)
    PINS[key] = actual
    return actual


def read(path):
    pin(path)
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError('nonfinite JSON '+value)
    return json.loads(Path(path).read_bytes(), object_pairs_hook=pairs, parse_constant=nonfinite)


def tree_bytes(path):
    files = list(Path(path).rglob('*'))
    need(not any(p.is_symlink() for p in files), 'symlink in output tree')
    return sum(p.stat().st_size for p in files if p.is_file())


def top_indices(scores):
    indices = np.flatnonzero(np.isfinite(scores))
    # C-order is scale, top, left: exactly the declared tie order.
    return indices[np.lexsort((indices, -scores.ravel()[indices]))][:2].tolist()


def check_coverage(saved, direct):
    need(np.isfinite(saved).all() and np.allclose(saved, direct, rtol=0, atol=COVERAGE_ATOL), 'surface coverage/nonfinite')


def independent_summary(rows):
    groups, shortlist = [], set()
    for target, clip, arm, paired in sorted({(r['target'], r['clip'], r['arm'], r['paired']) for r in rows}):
        selected = [r for r in rows if (r['target'], r['clip'], r['arm'], r['paired']) == (target, clip, arm, paired)]
        for metric in ('static_score', 'dynamic_score'):
            ranked = [(r['source_index'], r['best'][0][metric]) for r in selected
                      if r['best'] and r['best'][0][metric] is not None]
            need(all(np.isfinite(score) for _, score in ranked), 'nonfinite ranking')
            ranked.sort(key=lambda item: (-item[1], item[0]))
            best = ranked[0][1] if ranked else None
            groups.append(dict(target=target, clip=clip, arm=arm, paired=paired, metric=metric,
                compared_frames=len(selected), finite_frames=len(ranked), best_score=best,
                reason=None if ranked else 'no valid score at best static transform',
                ranked=[dict(source_index=i, score=s) for i, s in ranked],
                epsilon_sets={str(e): sorted(i for i, s in ranked if best-s <= e) for e in (.005, .01, .02)}))
            if paired:
                shortlist.update((clip, i) for i, _ in ranked[:2])
    return dict(groups=groups, shortlist=[dict(clip=c, source_index=i) for c, i in sorted(shortlist)])


def self_test():
    a = np.array([[[.5, .9], [np.nan, .9]], [[.9, .3], [.1, .2]]])
    need(top_indices(a) == [1, 3], 'top-two tie control')
    need(top_indices(np.full((2, 2), np.nan)) == [], 'all-invalid control')
    rows = [dict(target='143', clip=3, arm='full', paired=True, source_index=i,
                 best=[dict(static_score=s, dynamic_score=None)]) for i, s in ((2, .9), (0, .9), (1, .895))]
    summary = independent_summary(rows)
    need(summary['shortlist'] == [dict(clip=3, source_index=0), dict(clip=3, source_index=2)], 'frame tie order')
    need(summary['groups'][0]['epsilon_sets']['0.01'] == [0, 1, 2], 'epsilon set')
    need(summary['groups'][1]['best_score'] is None and summary['groups'][1]['ranked'] == [], 'null group')
    need(summary == independent_summary(list(reversed(rows))), 'input-order independence')
    check_coverage(np.array([1-1e-15, .5]), np.array([1., .5]))
    for bad in (np.array([1., .5001]), np.array([np.nan, .5])):
        try:
            check_coverage(bad, np.array([1., .5]))
        except ValueError:
            pass
        else:
            raise ValueError('bad coverage control admitted')
    return dict(status='passed', synthetic_checks=9, historical_files_opened=0)


def fixed_masks(target):
    masks = {'working_valid': np.arange(120)[:, None] < 88}
    masks['working_valid'] = np.repeat(masks['working_valid'], 180, axis=1)
    w, h = target['size']
    for kind in ('static', 'dynamic'):
        masks[kind+'_143'] = np.array([[any(x0 <= (x+.5)*w/180 < x1 and y0 <= (y+.5)*h/120 < y1
            for x0, y0, x1, y1 in target[kind]) for x in range(180)] for y in range(120)])
    transforms = []
    for n, scale in enumerate(SCALES):
        sw, sh = round(180*scale), round(120*scale)
        cx, cy = 25+(180-sw)//2, 25+(120-sh)//2
        rows = np.floor((np.arange(sh)+.5)*120/sh).astype(int) < 88
        rows[np.flatnonzero(rows)[-2:]] = False
        valid = np.zeros((170, 230), dtype=bool)
        valid[cy:cy+sh, cx:cx+sw] = rows[:, None]
        masks[f'scaled_canvas_valid_{n:02d}'] = valid
        transforms.append(dict(requested_scale=scale, raster_width=sw, raster_height=sh,
            scale_x=sw/180, scale_y=sh/120, canvas_x=cx, canvas_y=cy))
    return masks, transforms


def arrays(path):
    pin(path)
    with np.load(path, allow_pickle=False) as values:
        return {key: values[key] for key in values.files}


def equal_arrays(a, b):
    need(set(a) == set(b), 'array key disagreement')
    need(all(a[k].dtype == b[k].dtype and np.array_equal(a[k], b[k], equal_nan=True) for k in a), 'array value disagreement')


def extraction(number, v, source):
    d, s = v.api, v.sample_v2.api
    run = V/f'extract{number:02d}'; directory = run/'vince-clip3'
    pin(run/'manifest.input.json', MANIFEST); pin(run/'plan.input', PLAN)
    pins = dict(code_sha256=d.SAMPLER_SHA, parent_code_sha256=s.PARENT_SHA256,
        manifest_sha256=MANIFEST, plan_sha256=PLAN, python=sys.version, pillow=v.p.Image.__version__)
    receipt = read(directory/'receipt.json')
    need(read(run/'run-receipt.json') == dict(schema=s.SCHEMA, status='descriptive_candidates_only', reasons=[],
        sources=[dict(id='vince-clip3', admission=d.ADMISSION)], pins=pins), 'sampler run receipt')
    need(receipt['source'] == source and receipt['pins'] == pins and receipt['reasons'] == [] and
        receipt['structure'] == 'inventory_and_products_checked' and receipt['admission'] == d.ADMISSION and
        receipt['scientific_or_human_acceptance'] is False, 'source admission receipt')
    identity = dict(bytes=source['bytes'], sha256=source['sha256'])
    need(receipt['source_identity'] == dict(before=identity, after=identity, status='matched_before_and_after'), 'source identities')
    for tool, binary in (('ffmpeg', s.FFMPEG), ('ffprobe', s.FFPROBE)):
        need(read(run/f'{tool}-version.command.json') == [binary, '-version'], 'version command')
        need(read(run/f'{tool}-version.status.json') == dict(returncode=0, launch_error=None), 'version status')
        for suffix in ('stdout', 'stderr'): pin(run/f'{tool}-version.{suffix}')
        need((run/f'{tool}-version.stdout').read_bytes().startswith(f'{tool} version 7.1.1 '.encode()) and
             not (run/f'{tool}-version.stderr').read_bytes().strip(), 'version diagnostic')
    for kind, command in d.expected_commands(source, directory).items():
        need(read(directory/f'{kind}.command.json') == command, 'extraction command')
        need(read(directory/f'{kind}.status.json') == dict(returncode=0, launch_error=None), 'extraction status')
        for suffix in ('stdout', 'stderr'): pin(directory/f'{kind}.{suffix}')
    inventory, stream, tb = s.inventory(read(directory/'probe.stdout'), 189)
    need(tb == Fraction('333673/10000000') and (stream['codec_name'], stream['width'], stream['height'],
        stream['sample_aspect_ratio'], stream['pix_fmt']) == ('dvvideo', 720, 480, '8:9', 'yuv411p'), 'inventory stream')
    raw = (directory/'decode.stderr').read_bytes()
    diagnostic = s.decode_diagnostics(raw, Path(source['path']), directory/'native/frame-%06d.png')
    need(diagnostic['status'] == 'clean' and diagnostic == receipt['decode_diagnostics'] and
        diagnostic['accepted_line_kinds']['show_frame'] == diagnostic['accepted_line_kinds']['show_color'] == 189,
        'decode diagnostics')
    probe = s.probe_diagnostics((directory/'probe.stderr').read_bytes())
    need(probe['status'] == 'clean' and probe == receipt['probe_diagnostics'] and
        not (directory/'decode.stdout').read_bytes(), 'probe diagnostics')
    s.check_showinfo(raw, inventory, list(range(189)), tb)
    # Bind metadata-only RGB reliance to the separately completed pixel audit.
    pin(directory/'frames.json', '224f41b92074b8b0c98dec6ec83e276da60a6af55c4907db0f308bb7c2bf7f90')
    rows = read(directory/'frames.json')
    need([r['source_index'] for r in rows] == list(range(189)), 'native population')
    need(sorted(p.name for p in (directory/'native').iterdir()) == [f'frame-{i:06d}.png' for i in range(1, 190)], 'native names')
    for i, row in enumerate(rows):
        need(type(row['source_index']) is int and type(row['pts']) is int and
            (row['pts'], row['time_base'], row['pts_seconds_exact'], row['file']) ==
            (i, str(tb), str(i*tb), f'native/frame-{i+1:06d}.png'), 'PTS/path join')
        need((row['width'], row['height'], row['sample_aspect_ratio'], row['interlaced_frame'], row['top_field_first']) ==
            (720, 480, '8:9', 1, 0), 'native metadata')
        need((inventory[i]['pts'], inventory[i]['sample_aspect_ratio'], inventory[i]['pix_fmt'],
              inventory[i]['interlaced_frame'], inventory[i]['top_field_first']) == (i, '8:9', 'yuv411p', 1, 0), 'inventory frame join')
        need(re.fullmatch('[0-9a-f]{64}', row['rgb_sha256']) is not None, 'RGB digest syntax')
        pin(directory/row['file'], row['png_sha256'])  # Bytes only: no Image.open or RGB decoding.
    return rows


def material(row):
    return {k: value for k, value in row.items() if k not in ('surfaces', 'surfaces_sha256')}


def audit():
    # No chunk/aggregate scores or rankings may be read before this terminal gate.
    g = read(V/'guard-aggregate-a/receipt.json')
    end = read(V/'guard-aggregate-a/wrapper-end-checks.json')
    terminal = read(V/'aggregate-a/receipt.json')
    need(g['status'] == 'completed' and g['returncode'] == 0 and not g.get('shutdown_error') and not g.get('snapshot_errors') and
        end['status'] == 'passed' and end['changed_dependencies'] == [] and end['supervisor_status'] == 'completed' and
        terminal['status'] == 'completed', 'aggregate terminal gate not satisfied')
    import dense_v2 as v
    import run as runner
    pin(V/'extraction-review.md', '301a8f00a05ce6dd817fd8ca9fe91dc6a696e34fea4af7e60d958c69394fd206')
    pin(V/'PLAN.md', PLAN); pin(V/'manifest.json', MANIFEST)
    for path, digest in v.dependencies().items(): pin(path, digest)
    controls = V/'controls-root01/summary.json'; pilot_controls = controls.parent/'pilot-controls/summary.json'
    gate_pins = {}; v.gate(controls, pilot_controls, gate_pins)
    for path, digest in gate_pins.items(): pin(path, digest)
    gate_pins.update({str(V/'PLAN.md'): PLAN, str(V/'manifest.json'): MANIFEST})
    jobs = ['extract01', 'extract02']+[f'score-{r}-{n:02d}' for r in 'ab' for n in range(1, 4)]+['aggregate-a']
    resource_rows = []
    for name in jobs:
        records = V/('guard-'+name)
        receipt, end = read(records/'receipt.json'), read(records/'wrapper-end-checks.json')
        spec = runner.job_spec(name, controls, pilot_controls, PLAN, MANIFEST)
        need(receipt['status'] == 'completed' and receipt['returncode'] == 0 and not receipt.get('shutdown_error') and
            not receipt.get('snapshot_errors') and receipt['scientific_acceptance'] is False, 'supervisor failure '+name)
        need(receipt['argv'] == spec['argv'] and receipt['target'] == str(spec['target']) and
            receipt['supervisor_sha256'] == v.GUARD_SHA, 'supervisor command/identity')
        need(end['status'] == 'passed' and end['changed_dependencies'] == [] and end['supervisor_status'] == 'completed' and
            end['parent_lane'] == str(V.parent) and end['before_pins'] == gate_pins and
            end['runner_sha256'] == sha(V/'run.py') and end['supervisor_sha256'] == v.GUARD_SHA, 'wrapper end checks')
        need((receipt['requested_seconds'], receipt['job_cap_bytes'], receipt['job_reserve_bytes']) ==
            (spec['seconds'], spec['job_cap'], spec['reserve']), 'job limits')
        need((receipt['lane_cap_bytes'], receipt['lane_reserve_bytes'], receipt['free_floor_bytes'], receipt['poll_seconds'],
              receipt['termination_grace_seconds']) == (1536*1024**2, 32*1024**2, 4096*1024**2, .1, 1), 'lane limits')
        actual = tree_bytes(V/name)
        need(actual == receipt['job_bytes'] and actual < spec['job_cap']-spec['reserve'] and
            receipt['elapsed_seconds'] < spec['seconds'] and receipt['lane_bytes_before_receipt'] < 1504*1024**2 and
            receipt['before']['lane_bytes'] < 1504*1024**2 and
            min(receipt['before']['free_bytes'], receipt['free_bytes_after']) >= 4096*1024**2, 'recorded resource breach')
        resource_rows.append(dict(job=name, bytes=actual, seconds=receipt['elapsed_seconds']))
    source = read(V/'manifest.json')['sources'][0]
    need(source['count'] == 189 and source['indices'] == list(range(189)), 'manifest population')
    pin(source['path'], source['sha256']); need(Path(source['path']).stat().st_size == source['bytes'], 'source bytes')
    first, second = extraction(1, v, source), extraction(2, v, source)
    need(first == second, '189 repeated frame records disagree')
    pilot_dir = C.parent/'cbs-vince-source-screen/stage2/run01/vince-clip3'
    pin(pilot_dir/'frames.json', v.p.CLIPS[0]['frames_sha256'])
    pilot_frames = read(pilot_dir/'frames.json')
    v.api.check_repeat_and_pilot(first, second, pilot_frames)
    for row in pilot_frames: pin(pilot_dir/row['file'], row['png_sha256'])
    regions = read(C/'regions.json'); target = next(t for t in regions['targets'] if t['id'] == '143')
    pin(C/target['path'], target['sha256'])
    masks, transforms = fixed_masks(target)
    static = masks['static_143']
    coverage = np.array([[[float((static & masks[f'scaled_canvas_valid_{n:02d}'][y:y+120, x:x+180]).sum()/static.sum())
        for x in range(51)] for y in range(51)] for n in range(13)])
    methods = v.method_pins(PLAN, MANIFEST)
    passes, finite_cells, transforms_checked, null_dynamic = [], 0, 0, 0
    for repeat, frames in (('a', first), ('b', second)):
        results = []
        for chunk in range(1, 4):
            indices = range((chunk-1)*63, chunk*63)
            directory = V/f'score-{repeat}-{chunk:02d}'
            receipt = read(directory/'receipt.json'); inputs = read(directory/'verified-inputs.json')
            need(receipt['status'] == 'completed' and receipt['mode'] == 'score' and receipt['repeat'] == repeat and
                receipt['chunk'] == chunk and receipt['method_pins'] == methods and receipt['result']['indices'] == list(indices) and
                receipt['result']['comparisons'] == 189 and receipt['result']['scientific_or_human_acceptance'] is False, 'chunk receipt')
            need(inputs['repeat_equal_frames'] == 189 and inputs['pilot_equal_frames'] == 9 and inputs['transforms'] == transforms and
                inputs['scientific_or_human_acceptance'] is False, 'chunk inputs')
            expected_frames = [dict(clip=3, path=str(V/f'extract{1 if repeat == "a" else 2:02d}'/'vince-clip3'/r['file']), **r)
                               for r in frames if r['source_index'] in indices]
            need(inputs['frames'] == expected_frames, 'chunk frame input joins')
            for path, digest in inputs['pins'].items(): pin(path, digest)
            equal_arrays(arrays(directory/'masks.npz'), masks)
            pin(directory/'results.json', receipt['result']['results_sha256'])
            rows = read(directory/'results.json')
            need([(r['source_index'], r['arm']) for r in rows] == [(i, a) for i in indices for a in ARMS], 'chunk population')
            expected_files = set()
            for row in rows:
                frame = frames[row['source_index']]
                need(row['target'] == '143' and row['clip'] == 3 and row['paired'] is True and
                    all(row[k] == frame[k] for k in ('pts', 'time_base', 'pts_seconds_exact', 'png_sha256', 'rgb_sha256')), 'score source join')
                filename = f"scores-143-clip3-{row['source_index']:06d}-{row['arm']}.npz"
                need(row['surfaces'] == filename, 'surface path'); expected_files.add(filename)
                pin(directory/filename, row['surfaces_sha256']); surface = arrays(directory/filename)
                need(set(surface) == {'scores', 'coverage'} and surface['scores'].shape == surface['coverage'].shape == (13, 51, 51), 'surface schema')
                need(not np.isinf(surface['scores']).any(), 'infinite score surface')
                check_coverage(surface['coverage'], coverage)
                counts = coverage*static.sum()
                invalid_count = (counts < 32-COUNT_GATE_TOLERANCE) | (counts < .85*static.sum()-COUNT_GATE_TOLERANCE)
                need(not (np.isfinite(surface['scores']) & invalid_count).any(), 'finite static score without count/coverage')
                expected_best = top_indices(surface['scores'])
                need(len(row['best']) == len(expected_best) and row['invalid_reason'] ==
                    (None if expected_best else 'no static transform passed count/coverage/variance gates'), 'best/invalid cardinality')
                for best, flat in zip(row['best'], expected_best):
                    n, y, x = (int(a) for a in np.unravel_index(flat, surface['scores'].shape))
                    expected = dict(transforms[n], left=x, top=y, dx=x-25, dy=y-25,
                        static_score=float(surface['scores'][n, y, x]), static_overlap=float(surface['coverage'][n, y, x]))
                    need(all(best[k] == value for k, value in expected.items()), 'independent top-two ordering/transform')
                    dynamic = masks['dynamic_143']; valid = masks[f'scaled_canvas_valid_{n:02d}'][y:y+120, x:x+180]
                    dynamic_coverage = float((dynamic & valid).sum()/dynamic.sum())
                    need(best['dynamic_overlap'] == dynamic_coverage and
                        (best['dynamic_score'] is None or (dynamic_coverage >= .85 and np.isfinite(best['dynamic_score']))), 'dynamic coverage/null')
                    null_dynamic += best['dynamic_score'] is None
                    transforms_checked += 1
                finite_cells += int(np.isfinite(surface['scores']).sum())
                results.append(dict(row, surfaces=str((directory/filename).relative_to(V))))
            need({p.name for p in directory.glob('scores-*.npz')} == expected_files, 'extra/missing surface')
        need(len(results) == 567, 'pass population'); passes.append(results)
    need([material(r) for r in passes[0]] == [material(r) for r in passes[1]], 'A/B material records')
    for a, b in zip(*passes): equal_arrays(arrays(V/a['surfaces']), arrays(V/b['surfaces']))
    pin(C/'pilot01/results.json', v.api.PILOT_RESULTS_SHA)
    old = [r for r in read(C/'pilot01/results.json') if r['target'] == '143' and r['clip'] == 3 and r['paired'] is True]
    need([(r['source_index'], r['arm']) for r in old] == [(i, a) for i in (0, 24, 47, 71, 94, 118, 141, 165, 188) for a in ARMS], 'pilot population')
    lookup = {(r['source_index'], r['arm']): r for r in passes[0]}
    for row in old:
        current = lookup[row['source_index'], row['arm']]
        need(material(row) == material(current), 'pilot material result')
        pin(C/'pilot01'/row['surfaces'], row['surfaces_sha256'])
        equal_arrays(arrays(C/'pilot01'/row['surfaces']), arrays(V/current['surfaces']))
    pilot_masks = arrays(C/'pilot01/masks.npz')
    equal_arrays({k: pilot_masks[k] for k in masks}, masks)
    aggregate = V/'aggregate-a'
    need(read(aggregate/'results.json') == passes[0] and read(aggregate/'repeat-results.json') == passes[1], 'aggregate result joins')
    summary = independent_summary(passes[0])
    need(read(aggregate/'summary.json') == summary and len(summary['groups']) == 6 and len(summary['shortlist']) <= 12, 'independent global ranking')
    need(terminal['mode'] == 'aggregate' and terminal['repeat'] == 'a' and terminal['chunk'] is None and
        terminal['method_pins'] == methods and terminal['result'] == dict(comparisons=567, frames=189,
        repeated_comparisons_equal=567, pilot_comparisons_equal=27, shortlist=summary['shortlist'], scientific_or_human_acceptance=False), 'aggregate terminal counts')
    aggregate_inputs = read(aggregate/'verified-inputs.json')
    need(aggregate_inputs['scientific_or_human_acceptance'] is False, 'aggregate acceptance boundary')
    for path, digest in aggregate_inputs['pins'].items(): pin(path, digest)
    old_pins = {'extract01/run-receipt.json': 'a061b18402e9d30e639bda4716d81e49753aeebc2cb657e8a7b00c74049692b8',
        'extract01/vince-clip3/receipt.json': '41d592cc774190e1f70e0e3250e92f53d44ee2d14dd8a08d836cb0e354848184',
        'extract01/vince-clip3/decode.stderr': '76ae78cabb327c0c7b9d18cccbf9d2366030d3396ebe02cc9138182db2213a98',
        'guard-extract01/receipt.json': '37dcdbccb50e9f2d8b1e3f0322504b283d76bf62794915207c1e1d79a71a3ac8'}
    for name, digest in old_pins.items(): pin(V.parent/name, digest)
    need(not (V.parent/'extract01/vince-clip3/frames.json').exists(), 'old refusal retrofitted')
    old_native = V.parent/'extract01/vince-clip3/native'
    need(sorted(p.name for p in old_native.iterdir()) == [f'frame-{i:06d}.png' for i in range(1, 190)] and
        tree_bytes(old_native) == 130737499 and tree_bytes(V.parent/'extract01') == 131007165, 'old failed-product count/bytes')
    for path, digest in PINS.items(): need(sha(path) == digest, 'input changed during audit')
    lane_bytes, free_bytes = tree_bytes(V.parent), shutil.disk_usage(V.parent).free
    need(lane_bytes < 1504*1024**2 and free_bytes >= 4096*1024**2, 'audit-end lane/free-space boundary')
    return dict(status='passed', scope='Artifact, saved-surface ranking and provenance audit; no image decoding, numerical correlation recomputation or historical authentication',
        frames=189, passes=2, comparisons_per_pass=567, score_cells_both_passes=2*567*13*51*51,
        finite_cells_both_passes=finite_cells, best_transforms_checked_both_passes=transforms_checked,
        null_dynamic_at_retained_transforms_both_passes=null_dynamic, global_groups=6, epsilon_sets=18,
        pilot_joins=27, repeated_frame_records=189, input_hashes=len(PINS), shortlist=summary['shortlist'],
        coverage_comparison_atol=COVERAGE_ATOL, inherited_count_gate_tolerance=COUNT_GATE_TOLERANCE,
        resources=resource_rows, parent_lane_bytes=lane_bytes, free_bytes=free_bytes, audit_code_sha256=sha(__file__))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    print(json.dumps(self_test() if args.self_test else audit(), indent=2, sort_keys=True, allow_nan=False))

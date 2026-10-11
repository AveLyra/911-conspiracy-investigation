"""Read-only post-aggregate audit. No image decoder/viewer or numerical matcher.

Default mode requires caller-supplied hashes of the actual independent extraction
review and both frame manifests. It refuses before loading any score/result file
unless aggregate, supervisor and wrapper terminal records report completion.
Derived from dense-clip3/v2/audit_artifacts.py, SHA-256
3bcc92ea0f6b73d6b7253cbe7733d24b0fb1ff0313d63d05d6854ea1d160cb2b.
--self-test uses synthetic arrays/records and temporary byte fixtures only.
Output is stdout JSON. No numerical matching or image decoding is performed.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

import numpy as np

V = Path(__file__).resolve().parent
C = V.parent
COUNT, CLIP, TARGET = 1128, 7, '142'
SOURCE_ID = 'vince-clip7'
PILOT_INDICES = (0, 141, 282, 423, 564, 705, 846, 987, 1127)
CHUNKS = tuple(range(i, min(i+63, COUNT)) for i in range(0, COUNT, 63))
MIB = 1024**2
JOBS = ['extract01', 'extract02']+[f'score-{r}-{n:02d}' for r in 'ab' for n in range(1, 19)]+['aggregate-a']
ARMS = ('full', 'even', 'odd')
SCALES = [0.85+i*.025 for i in range(13)]
COVERAGE_ATOL = 1e-10  # FFT count fractions versus direct integer-count fractions.
COUNT_GATE_TOLERANCE = 1e-7  # Explicit inherited numerical-core convention.
PLAN = '0404e0a819e7d8392ad3a320a4cb018ecef02c4d9d3f72337d4b3d1d131f6d70'
MANIFEST = 'ece7d7fbae14d3ec043c16eb845d74af617a06854c267b1e686e7b33d4e6e3ad'
PINS = {}


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require_digest(value):
    need(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None,
         'lowercase SHA-256 required')
    return value


def merge_dependencies(combined, incoming):
    need(isinstance(incoming, dict), 'dependency map required')
    for raw, expected in incoming.items():
        path = Path(raw)
        need(path.is_absolute() and not path.is_symlink(), 'dependency path/symlink')
        key = str(path.resolve())
        require_digest(expected)
        need(key not in combined or combined[key] == expected, 'conflicting dependency pin: '+key)
        combined[key] = expected


def require_complete_dependencies(saved, required):
    canonical = {}
    merge_dependencies(canonical, saved)
    need(all(canonical.get(path) == expected for path, expected in required.items()),
         'chunk missing required input identity')


def fresh_required_inputs(gate_pins, source, pair, pilot_directory, pilot_rows, target, clip_spec):
    """Independently enumerate prepare's input contract, without decoding images.

    Do not infer completeness from the saved chunk maps or their union. Actual
    byte identity is pinned here; RGB identity relies on the required separately
    completed extraction review and its explicitly supplied frame-manifest pins.
    """
    required = {}
    merge_dependencies(required, gate_pins)
    def remember(path, expected=None):
        actual = pin(path, expected)
        merge_dependencies(required, {str(Path(path).resolve()): actual})
    remember(source['path'], source['sha256'])
    remember(C/target['path'], target['sha256'])
    for number, rows in enumerate(pair, 1):
        run = V/f'extract{number:02d}'
        directory = run/SOURCE_ID
        for name, expected in (('manifest.input.json', MANIFEST), ('plan.input', PLAN), ('run-receipt.json', None)):
            remember(run/name, expected)
        for tool in ('ffmpeg', 'ffprobe'):
            for suffix in ('command.json', 'status.json', 'stdout', 'stderr'):
                remember(run/f'{tool}-version.{suffix}')
        for name in ('receipt.json', 'frames.json'):
            remember(directory/name)
        for kind in ('probe', 'decode'):
            for suffix in ('command.json', 'status.json', 'stdout', 'stderr'):
                remember(directory/f'{kind}.{suffix}')
        for row in rows:
            remember(directory/row['file'], row['png_sha256'])
    remember(pilot_directory/'frames.json', clip_spec['frames_sha256'])
    remember(pilot_directory/'receipt.json', clip_spec['receipt_sha256'])
    remember(pilot_directory.parent/'manifest.input.json', clip_spec['manifest_sha256'])
    remember(pilot_directory/'probe.stdout')
    for row in pilot_rows:
        remember(pilot_directory/row['file'], row['png_sha256'])
    return required


def pin(path, expected=None):
    """One pre-read hash per unique resolved path, followed by a final full recheck."""
    path = Path(path)
    need(path.is_file() and not path.is_symlink(), 'missing/symlink input: '+str(path))
    key = str(path.resolve())
    if expected is not None:
        require_digest(expected)
    if key not in PINS:
        PINS[key] = sha(path)
    need(expected is None or PINS[key] == expected, 'hash mismatch/conflicting pin: '+key)
    return PINS[key]


def recheck_pins():
    for path, expected in PINS.items():
        need(Path(path).is_file() and not Path(path).is_symlink() and sha(path) == expected,
             'input changed during audit: '+path)


def terminal_gate(supervisor, wrapper, terminal):
    need(supervisor['status'] == 'completed' and supervisor['returncode'] == 0 and
         not supervisor.get('shutdown_error') and not supervisor.get('snapshot_errors') and
         wrapper['status'] == 'passed' and wrapper['changed_dependencies'] == [] and
         wrapper['supervisor_status'] == 'completed' and terminal['status'] == 'completed' and
         terminal['mode'] == 'aggregate' and terminal['repeat'] == 'a' and terminal['chunk'] is None and
         terminal['result']['comparisons'] == 3*COUNT and terminal['result']['frames'] == COUNT and
         terminal['result']['repeated_comparisons_equal'] == 3*COUNT and
         terminal['result']['scientific_or_human_acceptance'] is False,
         'aggregate terminal gate not satisfied')


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
    """Synthetic controls only; temporary byte fixtures are deleted on exit."""
    from unittest.mock import patch
    checks = []
    def check(condition, name):
        need(condition, name)
        checks.append(name)
    def refuses(call, name):
        try:
            call()
        except (ValueError, KeyError):
            checks.append(name)
        else:
            raise ValueError('bad control admitted: '+name)

    a = np.array([[[.5, .9], [np.nan, .9]], [[.9, .3], [.1, .2]]])
    check(top_indices(a) == [1, 3], 'top-two transform tie order')
    check(top_indices(np.full((2, 2), np.nan)) == [], 'all-invalid transforms')
    rows = [dict(target=TARGET, clip=CLIP, arm='full', paired=True, source_index=i,
                 best=[dict(static_score=value, dynamic_score=None)])
            for i, value in ((63, .9), (62, .9), (1127, .895))]
    summary = independent_summary(rows)
    check(summary['shortlist'] == [dict(clip=CLIP, source_index=62), dict(clip=CLIP, source_index=63)],
          'cross-boundary frame tie order')
    check(summary['groups'][0]['epsilon_sets']['0.01'] == [62, 63, 1127], 'global epsilon set')
    check(summary['groups'][1]['best_score'] is None and summary['groups'][1]['ranked'] == [] and
          summary['groups'][1]['epsilon_sets'] == {'0.005': [], '0.01': [], '0.02': []},
          'all-null dynamic group')
    check(summary == independent_summary(list(reversed(rows))), 'input-order independence')
    rows[-1]['best'][0]['dynamic_score'] = .99
    check(dict(clip=CLIP, source_index=1127) in independent_summary(rows)['shortlist'], 'late dynamic winner')
    check_coverage(np.array([1-1e-15, .5]), np.array([1., .5]))
    checks.append('accepted FFT coverage rounding')
    refuses(lambda: check_coverage(np.array([1., .5001]), np.array([1., .5])), 'material coverage change')
    refuses(lambda: check_coverage(np.array([np.nan, .5]), np.array([1., .5])), 'nonfinite coverage')
    check(len(CHUNKS) == 18 and [i for chunk in CHUNKS for i in chunk] == list(range(COUNT)), 'complete chunk population')
    check(list(CHUNKS[-1]) == list(range(1071, 1128)) and len(CHUNKS[-1]) == 57, 'last partial chunk')
    check(sum(3*len(chunk) for chunk in CHUNKS) == 3384 and 2*3*COUNT == 6768, 'comparison populations')
    check(len(JOBS) == len(set(JOBS)) == 39 and JOBS[-1] == 'aggregate-a', 'serial job population')
    good_g = dict(status='completed', returncode=0)
    good_e = dict(status='passed', changed_dependencies=[], supervisor_status='completed')
    good_t = dict(status='completed', mode='aggregate', repeat='a', chunk=None,
                  result=dict(comparisons=3384, frames=1128, repeated_comparisons_equal=3384,
                              scientific_or_human_acceptance=False))
    terminal_gate(good_g, good_e, good_t)
    checks.append('complete terminal gate')
    refuses(lambda: terminal_gate(dict(good_g, status='started'), good_e, good_t), 'incomplete supervisor')
    refuses(lambda: terminal_gate(dict(good_g, shutdown_error='uncertain'), good_e, good_t), 'shutdown uncertainty')
    refuses(lambda: terminal_gate(good_g, dict(good_e, changed_dependencies=['changed']), good_t), 'failed wrapper identity')
    refuses(lambda: terminal_gate(good_g, good_e, dict(good_t, mode='score')), 'wrong terminal mode')
    bad_t = dict(good_t, result=dict(good_t['result'], comparisons=3383))
    refuses(lambda: terminal_gate(good_g, good_e, bad_t), 'incomplete aggregate population')

    PINS.clear()
    try:
        with tempfile.TemporaryDirectory(prefix='clip7-audit-selftest-') as temporary:
            root = Path(temporary).resolve()
            fixture = root/'fixture'; fixture.write_bytes(b'permitted synthetic bytes')
            (root/'child').mkdir()
            expected = sha(fixture)
            merged = {}
            merge_dependencies(merged, {str(fixture): expected})
            merge_dependencies(merged, {str(root/'child/../fixture'): expected})
            check(merged == {str(fixture): expected}, 'matching resolved-path aliases')
            refuses(lambda: merge_dependencies(merged, {str(fixture): '0'*64}), 'conflicting expected pin')
            refuses(lambda: merge_dependencies({}, {'relative': expected}), 'relative dependency path')
            refuses(lambda: merge_dependencies({}, {str(fixture): 'not-a-hash'}), 'invalid dependency digest')
            source_key, target_key = str(root/'source'), str(root/'target142')
            required = {source_key: '1'*64, target_key: '2'*64}
            require_complete_dependencies(dict(required), required)
            checks.append('complete per-chunk required map')
            require_complete_dependencies(dict(required, **{str(root/'extra'): '3'*64}), required)
            checks.append('complete required map retains extra pins')
            incomplete_source = {target_key: '2'*64}
            incomplete_target = {source_key: '1'*64}
            union = {}
            merge_dependencies(union, incomplete_source)
            merge_dependencies(union, incomplete_target)
            check(union == required, 'incomplete chunks can have complete union')
            refuses(lambda: require_complete_dependencies(incomplete_source, required), 'missing per-chunk source')
            refuses(lambda: require_complete_dependencies(incomplete_target, required), 'missing per-chunk paired target')
            refuses(lambda: require_complete_dependencies({source_key: '0'*64, target_key: '2'*64}, required),
                    'wrong per-chunk required identity')
            with patch(__name__+'.sha', wraps=sha) as hashing:
                pin(fixture, expected); pin(fixture, expected)
                check(hashing.call_count == 1, 'unique pre-read hashing')
                recheck_pins()
                check(hashing.call_count == 2, 'unique final hashing')
            refuses(lambda: pin(fixture, '0'*64), 'conflicting previously observed pin')
            fixture.write_bytes(b'changed synthetic bytes')
            refuses(recheck_pins, 'changed underlying dependency bytes')
    finally:
        PINS.clear()
    return dict(status='passed', synthetic_checks=len(checks), checks=checks,
                historical_files_opened=0, synthetic_temporary_fixtures_removed=True)


def fixed_masks(target):
    masks = {'working_valid': np.arange(120)[:, None] < 88}
    masks['working_valid'] = np.repeat(masks['working_valid'], 180, axis=1)
    w, h = target['size']
    for kind in ('static', 'dynamic'):
        masks[kind+'_'+TARGET] = np.array([[any(x0 <= (x+.5)*w/180 < x1 and y0 <= (y+.5)*h/120 < y1
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


def extraction(number, v, source, frames_sha256):
    d, s = v, v.s
    run = V/f'extract{number:02d}'; directory = run/SOURCE_ID
    pin(run/'manifest.input.json', MANIFEST); pin(run/'plan.input', PLAN)
    pins = dict(code_sha256=d.SAMPLER_SHA, parent_code_sha256=s.PARENT_SHA256,
        manifest_sha256=MANIFEST, plan_sha256=PLAN, python=sys.version, pillow=v.p.Image.__version__)
    receipt = read(directory/'receipt.json')
    need(read(run/'run-receipt.json') == dict(schema=s.SCHEMA, status='descriptive_candidates_only', reasons=[],
        sources=[dict(id=SOURCE_ID, admission=d.ADMISSION)], pins=pins), 'sampler run receipt')
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
    inventory, stream, tb = s.inventory(read(directory/'probe.stdout'), COUNT)
    need(tb == Fraction('333673/10000000') and (stream['codec_name'], stream['width'], stream['height'],
        stream['sample_aspect_ratio'], stream['pix_fmt']) == ('dvvideo', 720, 480, '8:9', 'yuv411p'), 'inventory stream')
    raw = (directory/'decode.stderr').read_bytes()
    diagnostic = s.decode_diagnostics(raw, Path(source['path']), directory/'native/frame-%06d.png')
    need(diagnostic['status'] == 'clean' and diagnostic == receipt['decode_diagnostics'] and
        diagnostic['accepted_line_kinds']['show_frame'] == diagnostic['accepted_line_kinds']['show_color'] == COUNT,
        'decode diagnostics')
    probe = s.probe_diagnostics((directory/'probe.stderr').read_bytes())
    need(probe['status'] == 'clean' and probe == receipt['probe_diagnostics'] and
        not (directory/'decode.stdout').read_bytes(), 'probe diagnostics')
    s.check_showinfo(raw, inventory, list(range(COUNT)), tb)
    # Bind metadata-only RGB reliance to the separately completed pixel audit.
    pin(directory/'frames.json', frames_sha256)
    rows = read(directory/'frames.json')
    need([r['source_index'] for r in rows] == list(range(COUNT)), 'native population')
    need(sorted(p.name for p in (directory/'native').iterdir()) == [f'frame-{i:06d}.png' for i in range(1, COUNT+1)], 'native names')
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


def audit(extraction_review_sha256, frame_hashes):
    require_digest(extraction_review_sha256)
    need(len(frame_hashes) == 2, 'both independently verified frame-manifest pins required')
    for expected in frame_hashes: require_digest(expected)
    PINS.clear()
    pin(__file__)
    # No chunk/aggregate scores or rankings may be read before this terminal gate.
    g = read(V/'guard-aggregate-a/receipt.json')
    end = read(V/'guard-aggregate-a/wrapper-end-checks.json')
    terminal = read(V/'aggregate-a/receipt.json')
    terminal_gate(g, end, terminal)
    import dense as v
    import run as runner
    pin(V/'extraction-review.md', extraction_review_sha256)
    pin(V/'PLAN.md', PLAN); pin(V/'manifest.json', MANIFEST)
    for path, expected in v.dependencies().items(): pin(path, expected)
    guard_sha = pin(V/'guard.py')
    runner_sha = pin(V/'run.py')
    # Root01 was interrupted by overlapping synthetic-fixture cleanup; it is
    # preserved as incomplete, not silently selected as an acceptable run.
    controls = V/'controls-root02/summary.json'; pilot_controls = controls.parent/'pilot-controls/summary.json'
    gate_pins = {}; v.gate(controls, pilot_controls, gate_pins)
    for path, digest in gate_pins.items(): pin(path, digest)
    gate_pins.update({str(V/'PLAN.md'): PLAN, str(V/'manifest.json'): MANIFEST})
    jobs = JOBS
    resource_rows = []
    for position, name in enumerate(jobs):
        records = V/('guard-'+name)
        receipt, end = read(records/'receipt.json'), read(records/'wrapper-end-checks.json')
        start = read(records/'start.json')
        for stream in ('stdout', 'stderr'): pin(records/stream)
        spec = runner.job_spec(name, controls, pilot_controls, PLAN, MANIFEST)
        need(receipt['status'] == 'completed' and receipt['returncode'] == 0 and not receipt.get('shutdown_error') and
            not receipt.get('snapshot_errors') and receipt['scientific_acceptance'] is False, 'supervisor failure '+name)
        need(receipt['argv'] == spec['argv'] and receipt['target'] == str(spec['target']) and
            receipt['supervisor_sha256'] == guard_sha and
            receipt['parent_supervisor_sha256'] == v.GUARD_PARENT_SHA, 'supervisor command/identity')
        need(start['status'] == 'started' and all(start[k] == receipt[k] for k in start if k != 'status'),
             'supervisor start/end identity')
        need(end['status'] == 'passed' and end['changed_dependencies'] == [] and end['supervisor_status'] == 'completed' and
            end['parent_lane'] == str(V) and end['before_pins'] == gate_pins and
            end['runner_sha256'] == runner_sha and end['supervisor_sha256'] == guard_sha and
            end['scientific_acceptance'] is False, 'wrapper end checks')
        predecessor_pins = {}
        merge_dependencies(predecessor_pins, end['predecessor_pins'])
        expected_predecessors = set()
        for prior in jobs[:position]:
            expected_predecessors.update(str((V/('guard-'+prior)/filename).resolve())
                                         for filename in ('receipt.json', 'wrapper-end-checks.json'))
            expected_predecessors.add(str((V/prior/('run-receipt.json' if prior.startswith('extract') else 'receipt.json')).resolve()))
        need(set(predecessor_pins) == expected_predecessors, 'serial predecessor pin population')
        for path, expected in predecessor_pins.items(): pin(path, expected)
        need((receipt['requested_seconds'], receipt['job_cap_bytes'], receipt['job_reserve_bytes']) ==
            (spec['seconds'], spec['job_cap'], spec['reserve']), 'job limits')
        need((receipt['lane_cap_bytes'], receipt['lane_reserve_bytes'], receipt['free_floor_bytes'], receipt['poll_seconds'],
              receipt['termination_grace_seconds']) == (3584*MIB, 128*MIB, 4096*MIB, .1, 1), 'lane limits')
        actual = tree_bytes(V/name)
        need(actual == receipt['job_bytes'] and actual < spec['job_cap']-spec['reserve'] and
            receipt['elapsed_seconds'] < spec['seconds'] and receipt['lane_bytes_before_receipt'] < 3456*MIB and
            receipt['before']['lane_bytes'] < 3456*MIB and
            min(receipt['before']['free_bytes'], receipt['free_bytes_after']) >= 4096*1024**2, 'recorded resource breach')
        resource_rows.append(dict(job=name, bytes=actual, seconds=receipt['elapsed_seconds']))
    # Read all declared dependency maps, reject cross-chunk/pass conflicts, then
    # verify each unique dependency before opening any historical score surface.
    dependency_map, chunk_inputs = {}, {}
    for repeat in ('a', 'b'):
        for chunk in range(1, 19):
            name = f'score-{repeat}-{chunk:02d}'
            chunk_inputs[name] = read(V/name/'verified-inputs.json')
            merge_dependencies(dependency_map, chunk_inputs[name]['pins'])
    aggregate_inputs = read(V/'aggregate-a/verified-inputs.json')
    aggregate_dependencies = {}
    merge_dependencies(aggregate_dependencies, aggregate_inputs['pins'])
    need(all(aggregate_dependencies.get(path) == expected for path, expected in dependency_map.items()),
         'aggregate omitted or changed a chunk dependency')
    merge_dependencies(dependency_map, aggregate_dependencies)
    for path, expected in dependency_map.items(): pin(path, expected)
    source = read(V/'manifest.json')['sources'][0]
    need(source['count'] == COUNT and source['id'] == SOURCE_ID and source['indices'] == list(range(COUNT)), 'manifest population')
    pin(source['path'], source['sha256']); need(Path(source['path']).stat().st_size == source['bytes'], 'source bytes')
    first, second = extraction(1, v, source, frame_hashes[0]), extraction(2, v, source, frame_hashes[1])
    need(first == second, '1128 repeated frame records disagree')
    pilot_dir = C.parent/'cbs-vince-source-screen/stage4/run01/vince-clip7'
    pin(pilot_dir/'frames.json', v.p.CLIPS[1]['frames_sha256'])
    pilot_frames = read(pilot_dir/'frames.json')
    v.check_repeat_and_pilot(first, second, pilot_frames)
    for row in pilot_frames: pin(pilot_dir/row['file'], row['png_sha256'])
    regions = read(C/'regions.json'); target = next(t for t in regions['targets'] if t['id'] == TARGET)
    pin(C/target['path'], target['sha256'])
    required_inputs = fresh_required_inputs(gate_pins, source, (first, second), pilot_dir,
                                           pilot_frames, target, v.p.CLIPS[1])
    for inputs in chunk_inputs.values():
        require_complete_dependencies(inputs['pins'], required_inputs)
    masks, transforms = fixed_masks(target)
    static = masks['static_142']
    coverage = np.array([[[float((static & masks[f'scaled_canvas_valid_{n:02d}'][y:y+120, x:x+180]).sum()/static.sum())
        for x in range(51)] for y in range(51)] for n in range(13)])
    methods = v.method_pins(PLAN, MANIFEST)
    passes, finite_cells, transforms_checked, null_dynamic = [], 0, 0, 0
    for repeat, frames in (('a', first), ('b', second)):
        results = []
        for chunk, indices in enumerate(CHUNKS, 1):
            directory = V/f'score-{repeat}-{chunk:02d}'
            receipt = read(directory/'receipt.json'); inputs = chunk_inputs[directory.name]
            for filename in ('receipt.json', 'results.json', 'verified-inputs.json', 'masks.npz'):
                path = directory/filename
                need(aggregate_dependencies.get(str(path.resolve())) == pin(path),
                     'aggregate missing chunk-artifact pin')
            need(receipt['status'] == 'completed' and receipt['mode'] == 'score' and receipt['repeat'] == repeat and
                receipt['chunk'] == chunk and receipt['method_pins'] == methods and receipt['result']['indices'] == list(indices) and
                receipt['result']['comparisons'] == 3*len(indices) and receipt['result']['scientific_or_human_acceptance'] is False, 'chunk receipt')
            need(inputs['repeat_equal_frames'] == COUNT and inputs['pilot_equal_frames'] == 9 and inputs['transforms'] == transforms and
                inputs['scientific_or_human_acceptance'] is False, 'chunk inputs')
            expected_frames = [dict(clip=CLIP, path=str(V/f'extract{1 if repeat == "a" else 2:02d}'/SOURCE_ID/r['file']), **r)
                               for r in frames if r['source_index'] in indices]
            need(inputs['frames'] == expected_frames, 'chunk frame input joins')
            # Every saved pin was included in the complete unique map above.
            equal_arrays(arrays(directory/'masks.npz'), masks)
            pin(directory/'results.json', receipt['result']['results_sha256'])
            rows = read(directory/'results.json')
            need([(r['source_index'], r['arm']) for r in rows] == [(i, a) for i in indices for a in ARMS], 'chunk population')
            expected_files = set()
            for row in rows:
                frame = frames[row['source_index']]
                need(row['target'] == TARGET and row['clip'] == CLIP and row['paired'] is True and
                    all(row[k] == frame[k] for k in ('pts', 'time_base', 'pts_seconds_exact', 'png_sha256', 'rgb_sha256')), 'score source join')
                filename = f"scores-142-clip7-{row['source_index']:06d}-{row['arm']}.npz"
                need(row['surfaces'] == filename, 'surface path'); expected_files.add(filename)
                pin(directory/filename, row['surfaces_sha256']); surface = arrays(directory/filename)
                need(aggregate_dependencies.get(str((directory/filename).resolve())) == row['surfaces_sha256'],
                     'aggregate missing surface pin')
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
                    dynamic = masks['dynamic_142']; valid = masks[f'scaled_canvas_valid_{n:02d}'][y:y+120, x:x+180]
                    dynamic_coverage = float((dynamic & valid).sum()/dynamic.sum())
                    need(best['dynamic_overlap'] == dynamic_coverage and
                        (best['dynamic_score'] is None or (dynamic_coverage >= .85 and np.isfinite(best['dynamic_score']))), 'dynamic coverage/null')
                    null_dynamic += best['dynamic_score'] is None
                    transforms_checked += 1
                finite_cells += int(np.isfinite(surface['scores']).sum())
                results.append(dict(row, surfaces=str((directory/filename).relative_to(V))))
            need({p.name for p in directory.glob('scores-*.npz')} == expected_files, 'extra/missing surface')
        need(len(results) == 3*COUNT, 'pass population'); passes.append(results)
    need([material(r) for r in passes[0]] == [material(r) for r in passes[1]], 'A/B material records')
    for a, b in zip(*passes): equal_arrays(arrays(V/a['surfaces']), arrays(V/b['surfaces']))
    pin(C/'pilot01/results.json', v.PILOT_RESULTS_SHA)
    old = [r for r in read(C/'pilot01/results.json') if r['target'] == TARGET and r['clip'] == CLIP and r['paired'] is True]
    need([(r['source_index'], r['arm']) for r in old] == [(i, a) for i in PILOT_INDICES for a in ARMS], 'pilot population')
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
        terminal['method_pins'] == methods and terminal['result'] == dict(comparisons=3*COUNT, frames=COUNT,
        repeated_comparisons_equal=3*COUNT, pilot_comparisons_equal=27, shortlist=summary['shortlist'], scientific_or_human_acceptance=False), 'aggregate terminal counts')
    need(read(aggregate/'verified-inputs.json') == aggregate_inputs, 'aggregate inputs changed')
    need(aggregate_inputs['scientific_or_human_acceptance'] is False, 'aggregate acceptance boundary')
    # Aggregate dependencies are already included, never omitted or re-blessed.
    old_pins = {'extract01/run-receipt.json': 'a061b18402e9d30e639bda4716d81e49753aeebc2cb657e8a7b00c74049692b8',
        'extract01/vince-clip3/receipt.json': '41d592cc774190e1f70e0e3250e92f53d44ee2d14dd8a08d836cb0e354848184',
        'extract01/vince-clip3/decode.stderr': '76ae78cabb327c0c7b9d18cccbf9d2366030d3396ebe02cc9138182db2213a98',
        'guard-extract01/receipt.json': '37dcdbccb50e9f2d8b1e3f0322504b283d76bf62794915207c1e1d79a71a3ac8'}
    old_lane = C/'dense-clip3'
    for name, digest in old_pins.items(): pin(old_lane/name, digest)
    need(not (old_lane/'extract01/vince-clip3/frames.json').exists(), 'old refusal retrofitted')
    old_native = old_lane/'extract01/vince-clip3/native'
    need(sorted(p.name for p in old_native.iterdir()) == [f'frame-{i:06d}.png' for i in range(1, 190)] and
        tree_bytes(old_native) == 130737499 and tree_bytes(old_lane/'extract01') == 131007165, 'old failed-product count/bytes')
    recheck_pins()
    lane_bytes, free_bytes = tree_bytes(V), shutil.disk_usage(V).free
    need(lane_bytes < 3456*MIB and free_bytes >= 4096*1024**2, 'audit-end lane/free-space boundary')
    return dict(status='passed', scope='Artifact, saved-surface ranking and provenance audit; no image decoding, numerical correlation recomputation or historical authentication',
        frames=COUNT, passes=2, comparisons_per_pass=3*COUNT, score_cells_both_passes=2*3*COUNT*13*51*51,
        finite_cells_both_passes=finite_cells, best_transforms_checked_both_passes=transforms_checked,
        null_dynamic_at_retained_transforms_both_passes=null_dynamic, global_groups=6, epsilon_sets=18,
        pilot_joins=27, repeated_frame_records=COUNT, input_hashes=len(PINS), unique_saved_dependencies=len(dependency_map),
        required_dependencies_per_chunk=len(required_inputs), complete_chunk_maps_checked=len(chunk_inputs),
        shortlist=summary['shortlist'],
        coverage_comparison_atol=COVERAGE_ATOL, inherited_count_gate_tolerance=COUNT_GATE_TOLERANCE,
        extraction_review_sha256=extraction_review_sha256, frames_sha256=list(frame_hashes),
        resources=resource_rows, lane_bytes=lane_bytes, free_bytes=free_bytes, audit_code_sha256=sha(__file__))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--extraction-review-sha256')
    parser.add_argument('--frames01-sha256')
    parser.add_argument('--frames02-sha256')
    args = parser.parse_args()
    pins = (args.extraction_review_sha256, args.frames01_sha256, args.frames02_sha256)
    if args.self_test:
        need(not any(pins), 'self-test does not accept historical pins')
        result = self_test()
    else:
        need(all(pins), 'historical audit requires actual extraction review and both frame-manifest pins')
        result = audit(args.extraction_review_sha256, pins[1:])
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))

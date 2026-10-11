"""Clip 3-only dense adapter. Reads saved extractions; never launches a decoder.

Scoring is three fixed chunks per extraction repeat. No chunk makes a shortlist.
The root-owned external watchdog supplements inherited per-process output limits.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parent
DENSE = BASE/'dense-clip3'
PILOT_SHA = 'b561aaae16cb1d68f1252f7ca496c6de2fe0407f79219fa096bdd437cd00cee8'
PROTOCOL_SHA = '4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa'
REGIONS_SHA = '5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694'
SAMPLER_SHA = 'c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d'
PILOT_RESULTS_SHA = '8058581b27d454bfb8b30624e620fdaecf266aa2af7d08207531aa8c903870e3'
PILOT_RECEIPT_SHA = 'a90edf094f3d7511bba53c5d840b5df9bff27d6c54a0fd779e5eecb8b8c0d747'
CHUNKS = (range(0, 63), range(63, 126), range(126, 189))
ADMISSION = 'descriptive_candidate_pending_independent_and_human_review'


def import_pinned(name, path, expected):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    if digest != expected:
        raise ValueError('imported code pin mismatch')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p = import_pinned('dense_pilot', BASE/'pilot.py', PILOT_SHA)
s = import_pinned('dense_sampler', BASE.parent/'late-fire-sequence/sample_sequence.py', SAMPLER_SHA)
require = p.require


def snapshot(path, pins):
    """Capture current generated-file identity, not a claim of prior authentication."""
    p.pin(path, p.sha(path), pins)


def expected_commands(source, directory):
    selection = '+'.join(f'eq(n,{n})' for n in range(189))
    return {
        'probe': [s.FFPROBE, '-v', 'warning', '-select_streams', 'v:0', '-show_frames',
                  '-show_streams', '-show_format', '-of', 'json', source['path']],
        'decode': [s.FFMPEG, '-nostdin', '-hide_banner', '-nostats', '-loglevel', 'level+info',
            '-n', '-copyts', '-noautorotate', '-guess_layout_max', '0', '-i', source['path'],
            '-map', '0:v:0', '-an', '-sn', '-dn', '-map_metadata', '-1', '-map_chapters', '-1',
            '-vf', f"select='{selection}',showinfo", '-noautoscale', '-pix_fmt', 'rgb24',
            '-fps_mode', 'passthrough', '-enc_time_base:v', 'demux', str(directory/'native/frame-%06d.png')],
    }


def verify_extraction(run, source, manifest_sha, plan_sha, pins, check=lambda: None):
    """Reparse saved diagnostics with the unchanged sampler; check every product."""
    s.validate_source(source)
    require(source['id'] == 'vince-clip3' and source['count'] == 189 and source['indices'] == list(range(189)),
            'dense source population')
    p.pin(Path(source['path']), source['sha256'], pins)
    require(Path(source['path']).stat().st_size == source['bytes'], 'source bytes')
    directory = run/'vince-clip3'
    for name, digest in (('manifest.input.json', manifest_sha), ('plan.input', plan_sha)):
        p.pin(run/name, digest, pins)
    require(p.load(run/'manifest.input.json') == dict(schema=s.SCHEMA, sources=[source]), 'run source manifest')
    for path in (run/'run-receipt.json', directory/'receipt.json', directory/'frames.json'):
        snapshot(path, pins)
    run_receipt, receipt = p.load(run/'run-receipt.json'), p.load(directory/'receipt.json')
    expected_pins = dict(code_sha256=SAMPLER_SHA, parent_code_sha256=s.PARENT_SHA256,
        manifest_sha256=manifest_sha, plan_sha256=plan_sha, python=sys.version, pillow=Image.__version__)
    require(run_receipt == dict(schema=s.SCHEMA, status='descriptive_candidates_only', reasons=[],
        sources=[dict(id='vince-clip3', admission=ADMISSION)], pins=expected_pins), 'sampler run receipt')
    require(receipt['schema'] == s.SCHEMA and receipt['source'] == source and receipt['pins'] == expected_pins and
        receipt['reasons'] == [] and receipt['structure'] == 'inventory_and_products_checked' and
        receipt['admission'] == ADMISSION and receipt['scientific_or_human_acceptance'] is False, 'source receipt')
    identity = dict(bytes=source['bytes'], sha256=source['sha256'])
    require(receipt['source_identity'] == dict(before=identity, after=identity, status='matched_before_and_after'),
            'source receipt before/after identity')
    for tool, binary in (('ffmpeg', s.FFMPEG), ('ffprobe', s.FFPROBE)):
        for suffix in ('command.json', 'status.json', 'stdout', 'stderr'):
            snapshot(run/f'{tool}-version.{suffix}', pins)
        require(p.load(run/f'{tool}-version.command.json') == [binary, '-version'] and
            p.load(run/f'{tool}-version.status.json') == dict(returncode=0, launch_error=None) and
            (run/f'{tool}-version.stdout').read_bytes().startswith(f'{tool} version 7.1.1 '.encode()) and
            not (run/f'{tool}-version.stderr').read_bytes().strip(), 'saved decoder version receipt')
    for kind, argv in expected_commands(source, directory).items():
        for suffix in ('command.json', 'status.json', 'stdout', 'stderr'):
            snapshot(directory/f'{kind}.{suffix}', pins)
        require(p.load(directory/f'{kind}.command.json') == argv and
                p.load(directory/f'{kind}.status.json') == dict(returncode=0, launch_error=None), 'saved command/status')
    probe = p.load(directory/'probe.stdout')
    frames, stream, tb = s.inventory(probe, 189)
    require(tb == Fraction(p.TIME_BASE) and (stream['width'], stream['height']) == (720, 480) and
            stream['codec_name'] == 'dvvideo' and stream['sample_aspect_ratio'] == '8:9' and
            stream['pix_fmt'] == 'yuv411p', 'native stream metadata')
    for index, frame in enumerate(frames):
        require(type(frame['pts']) is int and frame['pts'] == index and frame['sample_aspect_ratio'] == '8:9' and
                frame['interlaced_frame'] == 1 and frame['top_field_first'] == 0 and
                frame['pix_fmt'] == 'yuv411p', 'native frame PTS/SAR/field metadata')
    raw = (directory/'decode.stderr').read_bytes()
    probe_diagnostic = s.probe_diagnostics((directory/'probe.stderr').read_bytes())
    diagnostic = s.decode_diagnostics(raw, Path(source['path']), directory/'native/frame-%06d.png')
    require(probe_diagnostic['status'] == 'clean' and diagnostic['status'] == 'clean' and
            receipt['probe_diagnostics'] == probe_diagnostic and receipt['decode_diagnostics'] == diagnostic and
            not (directory/'decode.stdout').read_bytes(), 'saved diagnostics reparse')
    s.check_showinfo(raw, frames, list(range(189)), tb)
    require(diagnostic['accepted_line_kinds'].get('show_frame') == 189 and
            diagnostic['accepted_line_kinds'].get('show_color') == 189, 'showinfo cardinality')
    rows = p.load(directory/'frames.json')
    require([row['source_index'] for row in rows] == list(range(189)), 'missing/duplicate/wrong index')
    require(sorted(path.name for path in (directory/'native').iterdir()) ==
            [f'frame-{n:06d}.png' for n in range(1, 190)], 'native product population')
    for index, row in enumerate(rows):
        check()
        require(type(row['source_index']) is int and type(row['pts']) is int and row['pts'] == index and
            row['time_base'] == p.TIME_BASE and row['pts_seconds_exact'] == str(index*tb) and
            row['file'] == f'native/frame-{index+1:06d}.png' and
            (row['width'], row['height'], row['sample_aspect_ratio'], row['interlaced_frame'], row['top_field_first']) ==
            (720, 480, '8:9', 1, 0), 'frame PTS/metadata join')
        path = directory/row['file']
        p.pin(path, row['png_sha256'], pins)
        with Image.open(path) as image:
            require(image.format == 'PNG' and image.mode == 'RGB' and image.size == (720, 480), 'PNG format/mode/size')
            require(hashlib.sha256(image.tobytes()).hexdigest() == row['rgb_sha256'], 'PNG/RGB join')
    return rows


def check_repeat_and_pilot(first, second, pilot):
    require(first == second and len(first) == 189, 'extraction repeat mismatch')
    require([r['source_index'] for r in pilot] == [0, 24, 47, 71, 94, 118, 141, 165, 188], 'pilot index population')
    for row in pilot:
        # File ordinal differs: e.g. pilot's second PNG is dense frame index 24.
        require({k: v for k, v in row.items() if k not in ('clip', 'path', 'file')} ==
                {k: v for k, v in first[row['source_index']].items() if k != 'file'},
                'pilot/dense frame join')


def verify_inputs(dense, manifest_sha, plan_sha, pins, check=lambda: None):
    for name, digest in (('manifest.json', manifest_sha), ('PLAN.md', plan_sha)):
        p.pin(dense/name, digest, pins)
    manifest = p.load(dense/'manifest.json')
    s.validate_manifest(manifest)
    old = p.CLIPS[0]
    source = dict(id='vince-clip3', path=str(BASE.parent/'cbs-vince-source-screen/stage2/raw/clip3-attempt1.avi'),
        sha256=old['source_sha256'], bytes=old['bytes'], count=189, indices=list(range(189)))
    require(manifest == dict(schema=s.SCHEMA, sources=[source]), 'dense source manifest population')
    p.pin(Path(source['path']), source['sha256'], pins)
    require(Path(source['path']).stat().st_size == source['bytes'], 'source bytes')
    pair = [verify_extraction(dense/f'extract{n:02d}', source, manifest_sha, plan_sha, pins, check) for n in (1, 2)]
    pilot = p.verify_clip(old, BASE.parent/'cbs-vince-source-screen', pins)
    check_repeat_and_pilot(*pair, pilot)
    return pair


def gate(controls, pilot_controls, pins):
    p.gate_controls(pilot_controls, pins)
    snapshot(controls, pins)
    result = p.load(controls)
    require(result['status'] == 'passed' and result['tests_run'] > 0 and result['failures'] == [] and
        result['errors'] == [] and result['skipped'] == [] and
        result['code_sha256'] == p.sha(__file__) and result['tests_sha256'] == p.sha(BASE/'test_dense_clip3.py') and
        result['pilot_sha256'] == PILOT_SHA and result['sampler_sha256'] == SAMPLER_SHA and
        result['python'] == platform.python_version() and result['numpy'] == np.__version__ and
        result['pillow'] == Image.__version__, 'dense controls failed or stale')


def method_pins(plan_sha, manifest_sha):
    return dict(code_sha256=p.sha(__file__), tests_sha256=p.sha(BASE/'test_dense_clip3.py'),
        pilot_sha256=PILOT_SHA, sampler_sha256=SAMPLER_SHA, core_sha256=p.CORE_SHA,
        protocol_sha256=PROTOCOL_SHA, regions_sha256=REGIONS_SHA, plan_sha256=plan_sha, manifest_sha256=manifest_sha)


def prepare(output, controls, pilot_controls, plan_sha, manifest_sha):
    pins = {}
    for path, digest in ((Path(__file__), p.sha(__file__)), (BASE/'test_dense_clip3.py', p.sha(BASE/'test_dense_clip3.py')),
        (BASE/'pilot.py', PILOT_SHA), (Path(s.__file__), SAMPLER_SHA), (p.CORE_PATH, p.CORE_SHA),
        (BASE/'PROTOCOL.md', PROTOCOL_SHA), (BASE/'regions.json', REGIONS_SHA)):
        p.pin(path, digest, pins)
    gate(controls, pilot_controls, pins)
    pair = verify_inputs(DENSE, manifest_sha, plan_sha, pins, output.check)
    output.check()
    return pair, pins


def recheck(pins, output):
    for path, digest in pins.items():
        output.check()
        require(p.sha(path) == digest, 'dependency changed during run')


def score(output, repeat, chunk, pair, pins):
    directory = DENSE/f'extract{1 if repeat == "a" else 2:02d}'/'vince-clip3'
    selected = [dict(clip=3, path=str(directory/row['file']), **row) for row in pair[0 if repeat == 'a' else 1]
                if row['source_index'] in CHUNKS[chunk-1]]
    require([r['source_index'] for r in selected] == list(CHUNKS[chunk-1]), 'score chunk population')
    regions = p.load(BASE/'regions.json')
    t = next(t for t in regions['targets'] if t['id'] == '143')
    path = BASE/t['path']; p.pin(path, t['sha256'], pins)
    with Image.open(path) as image:
        require(image.format == 'JPEG' and list(image.size) == t['size'], 'target format/size')
        arrays = (p.core.working(image), p.mask_for(t['static'], t['size']), p.mask_for(t['dynamic'], t['size']))
    require(not (arrays[1] & arrays[2]).any(), 'overlapping target masks')
    masks = dict(working_valid=p.working_validity(), static_143=arrays[1], dynamic_143=arrays[2])
    transforms = []
    for n, scale in enumerate(p.core.SCALES):
        _, masks[f'scaled_canvas_valid_{n:02d}'], transform = p.guarded_canvas(np.zeros((120, 180)), scale)
        transforms.append(transform)
    output.json('verified-inputs.json', dict(pins=pins, frames=selected, transforms=transforms,
        repeat_equal_frames=189, pilot_equal_frames=9, scientific_or_human_acceptance=False))
    output.npz('masks.npz', **masks)
    results = p.comparisons(selected, {'143': dict(paired_clip=3, arrays=arrays)}, output)
    require(len(results) == 189, 'score comparison population')
    output.json('results.json', results)
    # Deliberately no summarize/shortlist here: a chunk is not full-clip coverage.
    recheck(pins, output)
    return dict(indices=list(CHUNKS[chunk-1]), comparisons=189, results_sha256=p.sha(output.path/'results.json'),
                scientific_or_human_acceptance=False)


def validate_result_population(results, indices, frames):
    expected = [(i, arm) for i in indices for arm in p.ARMS]
    require([(r['source_index'], r['arm']) for r in results] == expected, 'incomplete/duplicate score population')
    for row in results:
        source = frames[row['source_index']]
        require(row['target'] == '143' and row['clip'] == 3 and row['paired'] is True and
            all(row[key] == source[key] for key in ('pts', 'time_base', 'pts_seconds_exact', 'png_sha256', 'rgb_sha256')),
            'score source join')


def collect_pass(output, repeat, frames, pins, methods):
    results = []
    for chunk, indices in enumerate(CHUNKS, 1):
        directory = DENSE/f'score-{repeat}-{chunk:02d}'
        for name in ('receipt.json', 'results.json', 'verified-inputs.json', 'masks.npz'):
            snapshot(directory/name, pins)
        receipt = p.load(directory/'receipt.json')
        require(receipt['status'] == 'completed' and receipt['mode'] == 'score' and receipt['repeat'] == repeat and
            receipt['chunk'] == chunk and receipt['method_pins'] == methods and
            receipt['result']['indices'] == list(indices) and receipt['result']['comparisons'] == 189 and
            receipt['result']['results_sha256'] == p.sha(directory/'results.json'), 'incomplete/stale chunk receipt')
        saved_inputs = p.load(directory/'verified-inputs.json')
        require(saved_inputs['repeat_equal_frames'] == 189 and saved_inputs['pilot_equal_frames'] == 9,
                'chunk verification counts')
        for path, digest in saved_inputs['pins'].items():
            output.check(); p.pin(Path(path), digest, pins)
        chunk_results = p.load(directory/'results.json')
        validate_result_population(chunk_results, indices, frames)
        for row in chunk_results:
            output.check()
            name = f"scores-143-clip3-{row['source_index']:06d}-{row['arm']}.npz"
            require(row['surfaces'] == name, 'surface path')
            p.pin(directory/name, row['surfaces_sha256'], pins)
            with np.load(directory/name, allow_pickle=False) as arrays:
                require(set(arrays.files) == {'scores', 'coverage'} and
                    arrays['scores'].shape == arrays['coverage'].shape == (13, 51, 51) and
                    np.isfinite(arrays['coverage']).all() and not np.isinf(arrays['scores']).any(), 'surface schema')
            results.append(dict(row, surfaces=str((directory/name).relative_to(DENSE))))
    validate_result_population(results, range(189), frames)
    return results


def equal_arrays(first, second, keys=None):
    with np.load(first, allow_pickle=False) as a, np.load(second, allow_pickle=False) as b:
        if keys is None:
            require(set(a.files) == set(b.files), 'repeat array keys disagree')
            keys = a.files
        require(set(keys) <= set(a.files) and set(keys) <= set(b.files), 'repeat array keys missing')
        require(all(np.array_equal(a[k], b[k], equal_nan=True) for k in keys), 'repeat array values disagree')


def material(row):
    return {k: v for k, v in row.items() if k not in ('surfaces', 'surfaces_sha256')}


def reconcile(first, second, pilot, output, pins, *, dense, pilot_dir):
    require(len(first) == len(second) == 567 and
            [material(r) for r in first] == [material(r) for r in second], 'repeat score records disagree')
    for a, b in zip(first, second):
        output.check()
        equal_arrays(dense/a['surfaces'], dense/b['surfaces'])
    mask = dense/'score-a-01/masks.npz'
    for repeat in ('a', 'b'):
        for chunk in range(1, 4):
            equal_arrays(mask, dense/f'score-{repeat}-{chunk:02d}/masks.npz')
    paired = [r for r in pilot if r['target'] == '143' and r['clip'] == 3 and r['paired'] is True]
    expected = [(index, arm) for index in [0, 24, 47, 71, 94, 118, 141, 165, 188] for arm in p.ARMS]
    require([(r['source_index'], r['arm']) for r in paired] == expected, 'pilot paired score population')
    lookup = {(r['source_index'], r['arm']): r for r in first}
    for row in paired:
        output.check()
        other = lookup[row['source_index'], row['arm']]
        require(material(row) == material(other), 'pilot/dense score records disagree')
        require(row['surfaces'] == f"scores-143-clip3-{row['source_index']:06d}-{row['arm']}.npz", 'pilot surface path')
        p.pin(pilot_dir/row['surfaces'], row['surfaces_sha256'], pins)
        equal_arrays(pilot_dir/row['surfaces'], dense/other['surfaces'])
    snapshot(pilot_dir/'masks.npz', pins)
    with np.load(mask, allow_pickle=False) as arrays:
        equal_arrays(mask, pilot_dir/'masks.npz', arrays.files)


def aggregate(output, pair, pins, methods):
    passes = [collect_pass(output, repeat, pair[n], pins, methods) for n, repeat in enumerate(('a', 'b'))]
    pilot_dir = BASE/'pilot01'
    p.pin(pilot_dir/'results.json', PILOT_RESULTS_SHA, pins)
    p.pin(pilot_dir/'receipt.json', PILOT_RECEIPT_SHA, pins)
    pilot_receipt = p.load(pilot_dir/'receipt.json')
    require(pilot_receipt['status'] == 'completed' and pilot_receipt['pilot_sha256'] == PILOT_SHA and
            pilot_receipt['protocol_sha256'] == PROTOCOL_SHA and pilot_receipt['regions_sha256'] == REGIONS_SHA,
            'pilot completion/code pins')
    reconcile(*passes, p.load(pilot_dir/'results.json'), output, pins, dense=DENSE, pilot_dir=pilot_dir)
    results = passes[0]
    summary = p.summarize(results)
    require(len(results) == 567 and len(summary['groups']) == 6 and len(summary['shortlist']) <= 12,
            'full-clip aggregate population')
    output.json('verified-inputs.json', dict(pins=pins, scientific_or_human_acceptance=False))
    output.json('results.json', results)
    output.json('repeat-results.json', passes[1])
    output.json('summary.json', summary)
    recheck(pins, output)
    return dict(comparisons=567, frames=189, repeated_comparisons_equal=567, pilot_comparisons_equal=27,
                shortlist=summary['shortlist'], scientific_or_human_acceptance=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('score', 'aggregate'))
    parser.add_argument('--repeat', choices=('a', 'b'), required=True)
    parser.add_argument('--chunk', type=int, choices=(1, 2, 3))
    parser.add_argument('--controls', type=Path, required=True)
    parser.add_argument('--pilot-controls', type=Path, required=True)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    require((args.mode == 'score') == (args.chunk is not None), 'chunk only and always required for score')
    require(args.mode == 'score' or args.repeat == 'a', 'single combined aggregation uses --repeat a')
    for digest in (args.plan_sha256, args.manifest_sha256): s.digest_string(digest)
    name = f'score-{args.repeat}-{args.chunk:02d}' if args.mode == 'score' else f'aggregate-{args.repeat}'
    seconds, byte_cap = (240, 256*1024**2) if args.mode == 'score' else (60, 16*1024**2)
    output = p.Output(DENSE/name, seconds=seconds, byte_cap=byte_cap)
    methods = method_pins(args.plan_sha256, args.manifest_sha256)
    receipt = dict(argv=sys.argv, mode=args.mode, repeat=args.repeat, chunk=args.chunk, method_pins=methods,
        python=platform.python_version(), numpy=np.__version__, pillow=Image.__version__,
        requested_seconds=seconds, requested_output_bytes=byte_cap,
        cap_scope='Inherited between-operation clock checks and pre-write byte cap; root external watchdog required.',
        status='started')
    output.json('start.json', receipt)
    try:
        pair, pins = prepare(output, args.controls, args.pilot_controls, args.plan_sha256, args.manifest_sha256)
        receipt['result'] = (score(output, args.repeat, args.chunk, pair, pins) if args.mode == 'score' else
                             aggregate(output, pair, pins, methods))
        output.check()
        receipt['status'] = 'completed'
    except Exception as exc:
        receipt.update(status='failed', exception_type=type(exc).__name__, message=str(exc)[:500])
    receipt['elapsed_seconds'] = time.monotonic()-output.started
    receipt['output_bytes_before_terminal_receipt'] = sum(path.stat().st_size for path in output.path.iterdir())
    output.json('receipt.json' if receipt['status'] == 'completed' else 'failure.json', receipt, terminal=True)
    print(p.json_bytes(dict(status=receipt['status'], elapsed_seconds=receipt['elapsed_seconds'])).decode(), end='')
    return 0 if receipt['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())

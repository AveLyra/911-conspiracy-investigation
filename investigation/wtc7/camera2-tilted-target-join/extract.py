#!/usr/bin/env python3
"""All-native Tilted Y-plane extraction; no image selection or correspondence.

Import is inert apart from loading the byte-verified existing media helper.
The historical CLI requires explicit reviewed code/protocol pins and a gate
flag. Those are computational execution controls, not human acceptance.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import selectors
import subprocess
import sys
import time
import types
import warnings

from PIL import Image, PngImagePlugin, __version__ as PILLOW_VERSION

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
JOIN = HERE.parent / 'tilted-camera-source-join'
HELPER = JOIN / 'prepare_media.py'
HELPER_SHA = 'b8d2010b99001dba79d10b887571ffdfa53b13d8b6800f26a1ed4442c11ba0d5'


def load_helper(path=HELPER, expected=HELPER_SHA):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('helper hash mismatch BEFORE execution')
    module = types.ModuleType('held_tilted_media_helper')
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


held = load_helper()
require, sha, pin, write_json = held.require, held.sha, held.pin, held.write_json
SOURCE_PINS = {
    'prepare_media.py': HELPER_SHA,
    'source/TiltedCameraWTC7Clip.mp4': '393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f',
    'source/receipt.json': 'a100331b8e5e66ebb41959811e3ff650750e8284fdba0e4c8dcebdd736ed8ea9',
    'probe01/probe.json': '778c35d099158ddc669316d88ee779cf89f5f5aa9c094cd5e1d5bed596bee1de',
    'probe01/selection.json': 'afd9abc4bd64a0422a749715a8dbb727f7e23447f1c6bf45e9c93d32030f7f6b',
    'probe01/execution.json': '548965fa3f7de60fd71fb42b2d211e63143502e041743db32d3df6a9b5ac25fd',
    'views01/frames.json': '2988d1347bd55cba704530c6d3996dcab1cfa6d5b4beebe6d0ad912ccd4d3a15',
    'views01/receipt.json': '4570095ea9c35fac86302f2443969a87261130175edb0de1b7eafa4eefefad29',
    'views01/execution.json': 'afc698e4f6215018fa821108270ba13012ae82459cc9893b747445a96003db59',
}
DECODER_SHA = '7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569'
CHARTER = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md')
CHARTER_SHA = '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd'


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique)


def output_path(name):
    require(type(name) is str and re.fullmatch(r'[a-z][a-z0-9_-]*', name), 'unsafe output name')
    out = HERE / name
    require(not out.exists() and not out.is_symlink(), 'output already exists')
    return out


def snapshot(paths):
    return {str(p): pin(p) for p in paths}


def check_pins(expected):
    actual = snapshot(expected)
    for p, digest in expected.items():
        require(actual[str(p)]['sha256'] == digest, 'input pin mismatch: ' + p.name)
    return actual


def validate_map(probe, selection, baseline, shape=(720, 480), count=476,
                 time_base='1/60000', sar='131:144'):
    stream, rows = held.parse_map(probe)
    require((stream['width'], stream['height']) == shape, 'fixed geometry changed')
    require(stream['time_base'] == time_base and stream.get('sample_aspect_ratio') == sar,
            'fixed clock/aspect changed')
    require(type(baseline) is list and len(rows) == len(baseline) == count, 'frame count changed')
    require(selection['n'] == count and type(selection['n']) is int
            and selection['geometry'] == list(shape) and selection['time_base'] == time_base
            and selection['frames'] == rows
            and selection['indices'] == held.selected_indices(count), 'saved selection/map changed')
    for i, (row, old) in enumerate(zip(rows, baseline)):
        require(type(old) is dict and set(old) == set(row) | {'decoded_sha256', 'luma_sha256'},
                'baseline fields changed')
        require(type(old['index']) is int and old['index'] == i and type(old['pts']) is int
                and {k: old[k] for k in row} == row, 'baseline index/PTS/order changed')
        for key in ('decoded_sha256', 'luma_sha256'):
            require(type(old[key]) is str and re.fullmatch('[0-9a-f]{64}', old[key]),
                    'invalid recorded digest')
    return stream, rows


def decoder_argv(decoder, media):
    # Exact argv contract in the inspected held helper; no seek/filter/rate/scale.
    return [str(decoder), '-nostdin', '-nostats', '-hide_banner', '-v', 'warning',
            '-copyts', '-noautorotate', '-i', str(media), '-map', '0:v:0', '-an',
            '-noautoscale', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough',
            '-enc_time_base:v', 'demux', '-f', 'rawvideo', '-']


def bounded_process(argv, max_stdout, timeout=60, max_stderr=1024*1024):
    """Bound wall time and retained pipe bytes; preserve prefixes on failure."""
    buffers = {'stdout': bytearray(), 'stderr': bytearray()}
    limits = {'stdout': max_stdout, 'stderr': max_stderr}
    failure = None
    with subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as proc, selectors.DefaultSelector() as selector:
        for label, pipe in [('stdout', proc.stdout), ('stderr', proc.stderr)]:
            os.set_blocking(pipe.fileno(), False)
            selector.register(pipe, selectors.EVENT_READ, label)
        deadline = time.monotonic() + timeout
        while selector.get_map() and failure is None:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                failure = 'timeout'
                break
            for key, _ in selector.select(min(remaining, 0.1)):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                label = key.data
                room = limits[label] + 1 - len(buffers[label])
                buffers[label].extend(chunk[:room])
                if len(buffers[label]) > limits[label]:
                    failure = label + '_limit'
                    break
        if failure is not None:
            proc.kill()
        try:
            code = proc.wait(timeout=max(0.01, deadline-time.monotonic()) if failure is None else 5)
        except subprocess.TimeoutExpired:
            failure = 'timeout'
            proc.kill()
            code = proc.wait(timeout=5)
    return {'stdout': bytes(buffers['stdout']), 'stderr': bytes(buffers['stderr']),
            'returncode': code, 'failure': failure,
            'retained_streams_complete': failure is None}


def validate_raw(raw, rows, baseline, shape):
    y_bytes = shape[0] * shape[1]
    frame_bytes = y_bytes * 3 // 2
    require(len(raw) == frame_bytes * len(rows), 'decoded byte/frame count mismatch')
    for i, (row, expected) in enumerate(zip(rows, baseline)):
        frame = raw[i*frame_bytes:(i+1)*frame_bytes]
        actual = {**row, 'decoded_sha256': sha(frame), 'luma_sha256': sha(frame[:y_bytes])}
        require(actual == expected, 'full-frame/luma/clock mismatch at index ' + str(i))


def extract_to(output, paths, expected, shape=(720, 480), count=476,
               time_base='1/60000', sar='131:144', runner=bounded_process):
    """Shared narrow execution path; test-only fixtures supply tiny source maps."""
    require(not output.exists() and not output.is_symlink(), 'output already exists')
    before = check_pins(expected)  # Before metadata parsing and any decoder call.
    probe, selection, baseline = (read_json(paths[k]) for k in ('probe', 'selection', 'frames'))
    stream, rows = validate_map(probe, selection, baseline, shape, count, time_base, sar)
    source, prior = read_json(paths['source_receipt']), read_json(paths['views_receipt'])
    argv = decoder_argv(paths['decoder'], paths['media'])
    require(source['media'] == pin(paths['media']) == prior['media'], 'media receipt mismatch')
    require(prior['probe'] == pin(paths['probe']) and prior['selection'] == pin(paths['selection'])
            and prior['binary'] == pin(paths['decoder']), 'probe/selection/binary receipt mismatch')
    require(argv == prior['execution']['argv'], 'held decode argv changed')
    raw_size = shape[0] * shape[1] * 3 // 2 * count
    require(0 < raw_size <= 1024*1024*1024, 'raw bound')
    output.mkdir()
    write_json(output/'inputs-before.json', before)
    stage = 'decode'
    try:
        result = runner(argv, raw_size)
        raw, stderr = result['stdout'], result['stderr']
        with (output/'decode.stderr').open('xb') as f:
            f.write(stderr)
        execution = {k: v for k, v in result.items() if k not in ('stdout', 'stderr')}
        execution.update({'argv': argv, 'timeout_seconds': 60, 'stdout_limit': raw_size,
                          'stderr_limit': 1024*1024, 'stdout_bytes_retained': len(raw),
                          'stdout_sha256_retained': sha(raw), 'stderr_bytes_retained': len(stderr),
                          'stderr_sha256_retained': sha(stderr)})
        write_json(output/'execution.json', execution)
        require(result['failure'] is None and result['retained_streams_complete'] is True
                and result['returncode'] == 0 and not stderr, 'decoder warning/error/bound refusal')
        stage = 'raw_identity'
        validate_raw(raw, rows, baseline, shape)
        require(sha(raw) == prior['execution']['raw_sha256'], 'full-stream hash mismatch')
        stage = 'native_pngs'
        frames = []
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            y_bytes = shape[0] * shape[1]
            frame_bytes = y_bytes * 3 // 2
            for i, row in enumerate(baseline):
                y = raw[i*frame_bytes:i*frame_bytes+y_bytes]
                name = f'frame-{i:04d}.png'
                with (output/name).open('xb') as f:
                    Image.frombytes('L', shape, y).save(f, format='PNG')
                with Image.open(output/name) as im:
                    require(im.format == 'PNG' and im.mode == 'L' and im.size == shape
                            and im.n_frames == 1 and im.tobytes() == y, 'saved native pixels mismatch')
                frames.append({**row, 'time_base': time_base, 'png': name,
                               'png_identity': pin(output/name), 'size': list(shape), 'mode': 'L'})
        write_json(output/'python-warnings.json', [{'category': w.category.__name__,
                                                   'message': str(w.message)} for w in caught])
        require(not caught, 'Python warning requires review')
        write_json(output/'frames.json', frames)
        stage = 'post_pins'
        after = snapshot(expected)
        write_json(output/'inputs-after.json', after)
        require(after == before, 'inputs/code/runtime changed during run')
        require(len(frames) == count and len(list(output.glob('frame-*.png'))) == count,
                'output native membership mismatch')
        products = {p.name: pin(p) for p in sorted(output.iterdir()) if p.is_file()}
        write_json(output/'receipt.json', {'status': 'prepared_pending_independent_verification',
                   'frame_count': count, 'geometry': list(shape), 'mode': 'L',
                   'time_base': time_base, 'sample_aspect_ratio_unapplied': sar,
                   'inputs_before': before, 'inputs_after': after, 'products': products,
                   'python': platform.python_version(), 'pillow': PILLOW_VERSION,
                   'all_full_frame_luma_hashes_and_saved_clocks_match': True,
                   'no_visual_review_or_source_authentication_implied': True})
        return {'status': 'prepared_pending_independent_verification', 'frames': count,
                'receipt': pin(output/'receipt.json')}
    except Exception as error:
        write_json(output/'failure.json', {'status': 'failed_not_admitted', 'stage': stage,
                   'exception_type': type(error).__name__,
                   'message': 'Preserved output is incomplete; no completion receipt admitted.'})
        raise


def historical(out_name, code_sha, protocol_sha, reviewed):
    require(reviewed is True, 'explicit reviewed historical execution flag required')
    output = output_path(out_name)
    require(pin(__file__)['sha256'] == code_sha, 'reviewed producer pin mismatch')
    require(pin(HERE/'PROTOCOL.md')['sha256'] == protocol_sha, 'reviewed protocol pin mismatch')
    require(platform.python_version() == '3.12.14' and PILLOW_VERSION == '12.3.0',
            'reviewed Python/Pillow versions changed')
    expected = {JOIN/n: h for n, h in SOURCE_PINS.items()}
    expected.update({held.DECODER: DECODER_SHA, CHARTER: CHARTER_SHA,
                     Path(__file__): code_sha, HERE/'PROTOCOL.md': protocol_sha})
    for p in [HERE/'test_extract.py', Path(sys.executable), Path(Image.__file__),
              Path(Image.core.__file__), Path(PngImagePlugin.__file__)]:
        expected[p] = pin(p)['sha256']
    paths = {'media': held.MEDIA, 'decoder': held.DECODER, 'probe': JOIN/'probe01/probe.json',
             'selection': JOIN/'probe01/selection.json', 'frames': JOIN/'views01/frames.json',
             'source_receipt': JOIN/'source/receipt.json', 'views_receipt': JOIN/'views01/receipt.json'}
    return extract_to(output, paths, expected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    parser.add_argument('--expect-code-sha256', required=True)
    parser.add_argument('--expect-protocol-sha256', required=True)
    parser.add_argument('--reviewed-historical', action='store_true')
    args = parser.parse_args()
    print(json.dumps(historical(args.out, args.expect_code_sha256,
                                args.expect_protocol_sha256, args.reviewed_historical)))

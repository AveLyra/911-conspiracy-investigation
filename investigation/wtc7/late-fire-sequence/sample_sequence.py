"""Versioned native descriptive sampling; diagnostic clearance is not science acceptance."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from PIL import Image, __version__ as pillow_version

SCHEMA = 'late-fire-sequence-v1'
PARENT_SHA256 = 'bd4267da1f80cb565322caa67a0ab8b8e5de181e31eaf0b68e4505e8a4258a68'
FFMPEG = '/opt/homebrew/bin/ffmpeg'
FFPROBE = '/opt/homebrew/bin/ffprobe'


class Refusal(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Refusal(reason)


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def save(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write('\n')


def absolute(value):
    require(isinstance(value, str) and not any(c in value for c in '\r\n\x00'), 'invalid path')
    path = Path(value)
    require(path.is_absolute() and '..' not in path.parts, 'absolute non-traversing path required')
    return path


def digest_string(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None,
            'lowercase SHA-256 required')


def validate_source(item):
    require(isinstance(item, dict) and set(item) == {'id', 'path', 'sha256', 'bytes', 'count', 'indices'},
            'source schema mismatch')
    require(isinstance(item['id'], str) and re.fullmatch('[a-z0-9][a-z0-9_-]{0,63}', item['id']) is not None,
            'invalid source id')
    absolute(item['path'])
    digest_string(item['sha256'])
    for key in ['bytes', 'count']:
        require(type(item[key]) is int and item[key] > 0, 'positive integer ' + key + ' required')
    indices = item['indices']
    require(isinstance(indices, list) and len(indices) > 0, 'nonempty explicit indices required')
    require(all(type(n) is int and 0 <= n < item['count'] for n in indices), 'invalid source index')
    require(all(a < b for a, b in zip(indices, indices[1:])), 'indices must strictly increase')


def validate_manifest(doc):
    require(isinstance(doc, dict) and set(doc) == {'schema', 'sources'} and doc['schema'] == SCHEMA,
            'manifest schema mismatch')
    require(isinstance(doc['sources'], list) and len(doc['sources']) > 0, 'nonempty sources required')
    for item in doc['sources']:
        validate_source(item)
    require(len({item['id'] for item in doc['sources']}) == len(doc['sources']), 'duplicate source id')


def observed_identity(path):
    require(path.is_file() and not path.is_symlink(), 'regular non-symlink source required')
    return {'bytes': path.stat().st_size, 'sha256': sha(path)}


def identity_matches(actual, item):
    return actual == {'bytes': item['bytes'], 'sha256': item['sha256']}


def inventory(doc, count):
    frames, streams = doc['frames'], doc['streams']
    require(isinstance(frames, list) and len(frames) == count, 'decoded frame count mismatch')
    require(isinstance(streams, list) and len(streams) == 1, 'exactly one selected video stream required')
    stream = streams[0]
    require(stream.get('codec_type') == 'video', 'selected stream is not video')
    tb = Fraction(stream['time_base'])
    require(tb > 0, 'nonpositive time base')
    geometry = (stream['width'], stream['height'])
    require(all(type(n) is int and n > 0 for n in geometry), 'invalid native geometry')
    previous = None
    for frame in frames:
        pts = frame.get('pts')
        require(type(pts) is int, 'missing/non-integer PTS')
        require(previous is None or pts > previous, 'non-increasing PTS')
        require((frame['width'], frame['height']) == geometry, 'changing native geometry')
        previous = pts
    return frames, stream, tb


def run_command(args, dest, name, stdin=None):
    """Preserve exact arguments, streams and numeric status, including nonzero/launch failure."""
    save(dest / (name + '.command.json'), args)
    status = {'returncode': None, 'launch_error': None}
    stdout = stderr = b''
    try:
        result = subprocess.run(args, input=stdin, capture_output=True, check=False)
        stdout, stderr = result.stdout, result.stderr
        status['returncode'] = result.returncode
    except OSError as exc:
        status['launch_error'] = type(exc).__name__ + ': ' + str(exc)
    finally:
        with (dest / (name + '.stdout')).open('xb') as handle:
            handle.write(stdout)
        with (dest / (name + '.stderr')).open('xb') as handle:
            handle.write(stderr)
        save(dest / (name + '.status.json'), status)
    return stdout, stderr, status


def probe_diagnostics(raw):
    # At -v warning, any stderr byte is a refusal; no message allowlist.
    text = raw.decode('utf-8', errors='strict')
    lines = [line for line in text.splitlines() if line.strip()]
    return {'status': 'refused' if raw else 'clean', 'bytes': len(raw),
            'nonempty_lines': len(lines), 'rejected': lines}


NUMBER = r'-?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?'
TOKEN = r'[a-zA-Z0-9_?/-]+'
SHOW_FRAME = re.compile(
    rf'n:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:({NUMBER})\s+'
    rf'duration:\s*\d+\s+duration_time:{NUMBER}\s+fmt:(?:bgr0|yuv411p)\s+cl:(?:unspecified|topleft)\s+'
    r'sar:\d+/\d+\s+s:\d+x\d+\s+i:[PBT]\s+iskey:[01]\s+type:[A-Z?]\s+'
    r'checksum:[0-9A-F]{8}\s+plane_checksum:\[[0-9A-F]{8}(?: [0-9A-F]{8})*\]\s+'
    r'mean:\[\d+(?: \d+)*\]\s+stdev:\[\d+(?:\.\d+)?(?: \d+(?:\.\d+)?)*\]')
SHOW_CONFIG = re.compile(r'config (in|out) time_base: (\d+/\d+), frame_rate: \d+/\d+')
SHOW_COLOR = re.compile(r'color_range:(?:pc color_space:gbr|unknown color_space:unknown)'
                        r' color_primaries:unknown color_trc:unknown')
# Fixed producer vocabulary for this DV/FFV1 -> PNG lane, not generic FFmpeg acceptance.
BARE_INFO = [
    r'(?:  |      )Metadata:',
    r'    (?:software        |encoder         ): Lavf61\.7\.100',
    r'        encoder         : Lavc61\.19\.101 png',
    rf'  Duration: \d+:\d+:\d+\.\d+, start: {NUMBER}, bitrate: \d+ kb/s',
    r'  Stream #0:0: Video: dvvideo \(dvsd / 0x64737664\), yuv411p, \d+x\d+ '
    r'\[SAR \d+:\d+ DAR \d+:\d+\], \d+ kb/s, [0-9.]+ fps, [0-9.]+ tbr, [0-9.]+ tbn',
    r'  Stream #0:0: Video: ffv1 \(FFV1 / 0x31564646\), bgr0, \d+x\d+, \d+ kb/s, '
    r'SAR \d+:\d+ DAR \d+:\d+, [0-9.]+ fps, [0-9.]+ tbr, [0-9.]+ tbn',
    r'  Stream #0:1: Audio: pcm_s16le \(\[1\]\[0\]\[0\]\[0\] / 0x0001\), '
    r'\d+ Hz, 2 channels, s16, \d+ kb/s',
    r'Stream mapping:',
    r'  Stream #0:0 -> #0:0 \((?:ffv1|dvvideo) \(native\) -> png \(native\)\)',
    r'  Stream #0:0: Video: png, rgb24\(pc, gbr/unknown/unknown, '
    r'(?:progressive|(?:bottom|top) coded first \(swapped\))\), \d+x\d+ '
    r'\[SAR \d+:\d+ DAR \d+:\d+\], q=2-31, 200 kb/s, [0-9.]+ fps, [0-9.]+ tbn',
    rf'frame=\s*\d+ fps={NUMBER} q={NUMBER} Lsize=N/A time=\d+:\d+:\d+\.\d+ '
    rf'bitrate=N/A speed=\s*{NUMBER}x\s*',
]
OUT_INFO = re.compile(r'video:\d+KiB audio:0KiB subtitle:0KiB other streams:0KiB '
                      r'global headers:0KiB muxing overhead: unknown')


def decode_diagnostics(raw, source, destination):
    text = raw.decode('utf-8', errors='strict')
    rejected, counts = [], Counter()
    section = None
    if any((ord(c) < 32 and c != '\n') or ord(c) == 127 for c in text):
        return {'status': 'refused', 'accepted_line_kinds': {}, 'rejected': [{'reason': 'unexpected control character'}]}
    for number, line in enumerate(text.split('\n'), 1):
        if line == '':
            continue
        if re.search(r'\[(?:warning|error|fatal|panic)\]', line):
            rejected.append({'line': number, 'reason': 'diagnostic severity', 'text': line})
            continue
        show = re.fullmatch(r'\[Parsed_showinfo_1 @ 0x[0-9a-fA-F]+\] \[info\] (.*)', line)
        out = re.fullmatch(r'\[out#0/image2 @ 0x[0-9a-fA-F]+\] \[info\] (.*)', line)
        kind = None
        if show:
            body = show[1]
            config = SHOW_CONFIG.fullmatch(body)
            if config and (config[1] == 'in' or body == 'config out time_base: 0/0, frame_rate: 0/0'):
                kind = 'show_config_' + config[1]
            elif SHOW_FRAME.fullmatch(body):
                kind = 'show_frame'
            elif SHOW_COLOR.fullmatch(body):
                kind = 'show_color'
        elif out and OUT_INFO.fullmatch(out[1]):
            kind = 'output_summary'
        elif line.startswith('[info] '):
            body = line[7:]
            if body == f"Input #0, avi, from '{source}':":
                kind = 'input'
                section = 'input'
            elif body == f"Output #0, image2, to '{destination}':":
                kind = 'output'
                section = 'output'
            else:
                names = ['metadata', 'metadata_entry', 'metadata_entry', 'duration',
                         'input_video', 'input_video', 'input_audio', 'mapping',
                         'video_mapping', 'output_video', 'final_summary']
                for key, pattern in zip(names, BARE_INFO):
                    if re.fullmatch(pattern, body):
                        kind = key
                        break
                if kind in ['metadata', 'metadata_entry']:
                    if section is None or ('software' in body and section != 'input') or ('encoder' in body and section != 'output'):
                        kind = None
        if kind is None:
            rejected.append({'line': number, 'reason': 'unparsed nonempty line', 'text': line})
        else:
            counts[kind] += 1
    for key in ['input', 'output', 'input_video', 'input_audio', 'mapping', 'video_mapping',
                'output_video', 'final_summary', 'show_config_in', 'show_config_out', 'output_summary']:
        if counts[key] != 1:
            rejected.append({'reason': 'unexpected cardinality', 'kind': key, 'count': counts[key]})
    return {'status': 'refused' if rejected else 'clean', 'accepted_line_kinds': dict(counts),
            'rejected': rejected}


def check_showinfo(raw, frames, selected, tb):
    text = raw.decode('utf-8', errors='strict')
    configs = re.findall(r'config in time_base: (\d+/\d+)', text)
    require(len(configs) == 1 and Fraction(configs[0]) == tb, 'showinfo time-base mismatch')
    logged = [(int(a), int(b)) for a, b in re.findall(r'\bn:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:', text)]
    require(logged == [(i, frames[n]['pts']) for i, n in enumerate(selected)], 'showinfo PTS mismatch')
    final = re.findall(r'^\[info\] frame=\s*(\d+) ', text, re.MULTILINE)
    require(final == [str(len(selected))], 'final frame count mismatch')
    bodies = [line.split(' [info] ', 1)[1] for line in text.split('\n')
              if line.startswith('[Parsed_showinfo_1 @ ') and ' [info] n:' in line]
    for body, n in zip(bodies, selected):
        frame = frames[n]
        geometry = re.search(r'\bs:(\d+)x(\d+)', body)
        require(geometry is not None and tuple(map(int, geometry.groups())) == (frame['width'], frame['height']),
                'showinfo geometry mismatch')
        sar = re.search(r'\bsar:(\d+/\d+)', body)
        require(sar is not None and Fraction(sar[1]) == Fraction(frame['sample_aspect_ratio'].replace(':', '/')),
                'showinfo SAR mismatch')
        fmt = re.search(r'\bfmt:(\w+)', body)
        require(fmt is not None and fmt[1] == frame['pix_fmt'], 'showinfo format mismatch')
        interlace = 'P' if frame['interlaced_frame'] == 0 else ('T' if frame['top_field_first'] else 'B')
        require(f' i:{interlace} ' in body, 'showinfo interlace mismatch')


def sample_source(item, dest, pins):
    dest.mkdir()  # No catch: do not write into any existing destination.
    receipt = {'schema': SCHEMA, 'source': item, 'pins': pins,
               'source_identity': {'status': 'unverified'}, 'structure': 'not_attempted',
               'probe_diagnostics': {'status': 'not_attempted'},
               'decode_diagnostics': {'status': 'not_attempted'},
               'admission': 'refused', 'scientific_or_human_acceptance': False, 'reasons': []}
    source = None
    rows = None
    try:
        validate_source(item)
        source = absolute(item['path'])
        receipt['source_identity']['before'] = observed_identity(source)
        require(identity_matches(receipt['source_identity']['before'], item), 'source identity mismatch before')
        stdout, stderr, status = run_command([FFPROBE, '-v', 'warning', '-select_streams', 'v:0',
            '-show_frames', '-show_streams', '-show_format', '-of', 'json', str(source)], dest, 'probe')
        receipt['probe_diagnostics'] = {'status': 'parse_failed'}
        receipt['probe_diagnostics'] = probe_diagnostics(stderr)
        require(status['returncode'] == 0, 'probe process nonzero or launch failure')
        require(receipt['probe_diagnostics']['status'] == 'clean', 'probe diagnostics refused')
        frames, stream, tb = inventory(json.loads(stdout), item['count'])
        receipt['structure'] = 'inventory_checked'
        selected = item['indices']
        native = dest / 'native'
        native.mkdir()
        pattern = native / 'frame-%06d.png'
        selection = '+'.join(f'eq(n,{n})' for n in selected)
        command = [FFMPEG, '-nostdin', '-hide_banner', '-nostats', '-loglevel', 'level+info',
            '-n', '-copyts', '-noautorotate', '-guess_layout_max', '0', '-i', str(source),
            '-map', '0:v:0', '-an', '-sn', '-dn', '-map_metadata', '-1', '-map_chapters', '-1',
            '-vf', f"select='{selection}',showinfo", '-noautoscale', '-pix_fmt', 'rgb24',
            '-fps_mode', 'passthrough', '-enc_time_base:v', 'demux', str(pattern)]
        stdout, stderr, status = run_command(command, dest, 'decode')
        receipt['decode_diagnostics'] = {'status': 'parse_failed'}
        receipt['decode_diagnostics'] = decode_diagnostics(stderr, source, pattern)
        require(status['returncode'] == 0, 'decode process nonzero or launch failure')
        require(not stdout, 'unexpected decode stdout')
        require(receipt['decode_diagnostics']['status'] == 'clean', 'decode diagnostics refused')
        check_showinfo(stderr, frames, selected, tb)
        kinds = receipt['decode_diagnostics']['accepted_line_kinds']
        require(kinds.get('show_color') == len(selected), 'showinfo color-line count mismatch')
        files = sorted(native.glob('*.png'))
        require(len(files) == len(selected), 'PNG count mismatch')
        rows = []
        for order, (n, file) in enumerate(zip(selected, files), 1):
            require(file.name == f'frame-{order:06d}.png', 'PNG name mismatch')
            with Image.open(file) as im:
                im.load()
                require(im.mode == 'RGB' and im.size == (stream['width'], stream['height']), 'PNG native mode/size mismatch')
                pixel_hash = hashlib.sha256(im.tobytes()).hexdigest()
            frame = frames[n]
            rows.append({'source_index': n, 'pts': frame['pts'], 'time_base': str(tb),
                'pts_seconds_exact': str(frame['pts'] * tb), 'file': str(file.relative_to(dest)),
                'width': stream['width'], 'height': stream['height'], 'rgb_sha256': pixel_hash,
                'png_sha256': sha(file), 'sample_aspect_ratio': frame.get('sample_aspect_ratio'),
                'interlaced_frame': frame.get('interlaced_frame'), 'top_field_first': frame.get('top_field_first')})
        receipt['structure'] = 'inventory_and_products_checked'
    except Exception as exc:
        receipt['reasons'].append(type(exc).__name__ + ': ' + str(exc))
    finally:
        if source is not None:
            try:
                actual = observed_identity(source)
                receipt['source_identity']['after'] = actual
                require(identity_matches(actual, item), 'source identity mismatch after')
                require(receipt['source_identity'].get('before') == actual, 'source changed during run')
                receipt['source_identity']['status'] = 'matched_before_and_after'
            except Exception as exc:
                receipt['source_identity']['status'] = 'refused'
                receipt['reasons'].append(type(exc).__name__ + ': ' + str(exc))
        if not receipt['reasons'] and rows is not None:
            save(dest / 'frames.json', rows)
            receipt['admission'] = 'descriptive_candidate_pending_independent_and_human_review'
        save(dest / 'receipt.json', receipt)
    return receipt


def execute(manifest_path, manifest_digest, plan_path, plan_digest, out):
    for path in [manifest_path, plan_path, out]:
        absolute(str(path))
    out.mkdir()
    result = {'schema': SCHEMA, 'status': 'refused', 'sources': [], 'reasons': []}
    try:
        digest_string(manifest_digest)
        digest_string(plan_digest)
        require(sha(manifest_path) == manifest_digest, 'manifest hash mismatch')
        require(sha(plan_path) == plan_digest, 'plan hash mismatch')
        for source, name in [(manifest_path, 'manifest.input.json'), (plan_path, 'plan.input')]:
            with (out / name).open('xb') as handle:
                handle.write(source.read_bytes())
        require(sha(out / 'manifest.input.json') == manifest_digest and sha(out / 'plan.input') == plan_digest,
                'declaration snapshot mismatch')
        manifest = json.loads((out / 'manifest.input.json').read_bytes())
        validate_manifest(manifest)
        pins = {'code_sha256': sha(Path(__file__)), 'parent_code_sha256': PARENT_SHA256,
                'manifest_sha256': manifest_digest, 'plan_sha256': plan_digest,
                'python': sys.version, 'pillow': pillow_version}
        result['pins'] = pins
        for name, binary in [('ffmpeg', FFMPEG), ('ffprobe', FFPROBE)]:
            stdout, stderr, status = run_command([binary, '-version'], out, name + '-version')
            require(status['returncode'] == 0 and not stderr.strip(), name + ' version command refused')
            require(stdout.startswith((name + ' version 7.1.1 ').encode()), name + ' undeclared version')
        for item in manifest['sources']:
            receipt = sample_source(item, out / item['id'], pins)
            result['sources'].append({'id': item['id'], 'admission': receipt['admission']})
        require(sha(manifest_path) == manifest_digest and sha(plan_path) == plan_digest, 'declaration changed during run')
        if all(row['admission'] != 'refused' for row in result['sources']):
            result['status'] = 'descriptive_candidates_only'
    except Exception as exc:
        result['reasons'].append(type(exc).__name__ + ': ' + str(exc))
    finally:
        save(out / 'run-receipt.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['manifest', 'plan', 'out']:
        parser.add_argument('--' + name, required=True, type=Path)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--plan-sha256', required=True)
    args = parser.parse_args()
    result = execute(args.manifest, args.manifest_sha256, args.plan, args.plan_sha256, args.out)
    print(json.dumps({'status': result['status'], 'source_count': len(result['sources'])}))
    return 0 if result['status'] == 'descriptive_candidates_only' else 1


if __name__ == '__main__':
    sys.exit(main())

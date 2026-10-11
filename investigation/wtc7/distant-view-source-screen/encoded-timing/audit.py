#!/usr/bin/env python3
"""Finite encoded-metadata audit. No pixels, clock authentication or source repair.

Analysis ordinals are zero-based and separate for frames and packets. Raw record
objects are retained unchanged; omission and explicit null remain distinguishable.
The source-byte hash check accounts for reported payloads, not MPEG4 pictures.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source' / 'DistantViewWTC7.avi'
PROBE = Path('/opt/homebrew/Cellar/ffmpeg/7.1.1_3/bin/ffprobe')
BASELINES = [HERE.parent / f'probe0{i}-diagnostics' / 'probe-stdout.json' for i in (2, 3)]
TIMEOUT = 60
OUTPUT_LIMIT = 16 * 1024 * 1024  # Post-capture stdout+stderr; oversized bytes retained.
EXPECTED = {
    HERE / 'PROTOCOL.md': '85570f004474538ac5cd9e3bf9dfb40e84cafc391671a62103ccca5323d45ba9',
    SOURCE: 'a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e',
    PROBE: 'fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad',
    HERE / 'avidec.c': '893124119820815ac6a06e78d644cc5f1a20344a518a2b04191337c5a029cd4f',
    HERE / 'demux.c': '8e1fe18d7b89000fbea67542821132daac1531e7de8d7e02b1332850fefbb009',
    HERE / 'decode.c': 'dd46da605bbbae807b0c03ea0015be0faea490a6343e31a112d3c0373ef8612c',
    **{p: 'c0c7ce905e0f3e96a4ce9fedbc8b4309d9c9a13c43d5f86afbe0d176e2e5ac84' for p in BASELINES},
}
STREAM_FIELDS = ('index', 'codec_name', 'codec_type', 'width', 'height', 'pix_fmt',
                 'sample_aspect_ratio', 'display_aspect_ratio', 'r_frame_rate',
                 'avg_frame_rate', 'time_base', 'start_pts', 'start_time',
                 'duration_ts', 'duration', 'nb_frames')
OLD_FRAME_FIELDS = ('stream_index', 'best_effort_timestamp', 'pts', 'duration',
                    'pkt_duration', 'width', 'height', 'pix_fmt', 'key_frame', 'pict_type')
FRAME_FIELDS = OLD_FRAME_FIELDS + ('pkt_dts', 'pkt_pos')
PACKET_FIELDS = ('stream_index', 'pts', 'dts', 'duration', 'pos', 'size', 'flags', 'data_hash')
BASELINE_FIELDS = {'streams': list(STREAM_FIELDS) + ['side_data_list'],
                   'frames': list(OLD_FRAME_FIELDS)}
IDENTITY_FIELDS = {
    'streams': list(STREAM_FIELDS) + ['side_data_list'],
    'frames': ['stream_index', 'key_frame', 'pict_type', 'width', 'height', 'pix_fmt',
               'duration', 'pkt_duration', 'pkt_pos'],
    'packets': ['stream_index', 'duration', 'pos', 'size', 'flags', 'data_hash'],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    with Path(path).open('xb') as handle:
        handle.write((json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode())


def pin(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), f'not a regular unsymlinked file: {path}')
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha(data)}


def snapshot():
    paths = list(EXPECTED) + [HERE / 'audit.py', HERE / 'test_audit.py']
    return {str(p): pin(p) for p in paths}


def check_expected(pins):
    for path, digest in EXPECTED.items():
        require(pins[str(path)]['sha256'] == digest, f'input pin changed: {path}')
    require(pins[str(SOURCE)]['bytes'] == 4749520, 'source size changed')


def output_directory(name, parent=HERE):
    require(name in ('run01', 'run02'), 'only literal run01/run02 are authorized')
    output = Path(parent) / name
    output.mkdir()  # Exclusive: includes refusal of preexisting symlinks and directories.
    return output


def probe_argv(genpts=False):
    entries = ('stream=' + ','.join(STREAM_FIELDS) +
               ':stream_side_data=side_data_type,rotation,displaymatrix' +
               ':frame=' + ','.join(FRAME_FIELDS) + ':packet=' + ','.join(PACKET_FIELDS))
    return ([str(PROBE), '-v', 'warning'] + (['-fflags', '+genpts'] if genpts else []) +
            ['-select_streams', 'v:0', '-show_packets', '-show_frames', '-show_data_hash',
             'sha256', '-show_entries', entries, '-of', 'json', str(SOURCE)])


def capture(directory, argv, stdout_name='stdout.json'):
    """Save complete diagnostics before eligibility checks; never parse here."""
    directory.mkdir()
    receipt = {'argv': argv, 'timeout_seconds': TIMEOUT, 'postcapture_limit_bytes': OUTPUT_LIMIT}
    stdout = stderr = b''
    started = time.monotonic()
    try:
        result = subprocess.run(argv, capture_output=True, timeout=TIMEOUT, check=False)
        stdout, stderr = result.stdout, result.stderr
        receipt.update(status='returned', returncode=result.returncode)
    except subprocess.TimeoutExpired as exc:
        stdout, stderr = exc.stdout or b'', exc.stderr or b''
        receipt.update(status='timeout', returncode=None)
    except OSError as exc:
        receipt.update(status='launch_error', returncode=None, error=str(exc))
    receipt['elapsed_seconds'] = time.monotonic() - started
    require(isinstance(stdout, bytes) and isinstance(stderr, bytes), 'binary subprocess output required')
    with (directory / stdout_name).open('xb') as handle:
        handle.write(stdout)
    with (directory / 'stderr.bin').open('xb') as handle:
        handle.write(stderr)
    receipt.update(stdout={'path': stdout_name, 'bytes': len(stdout), 'sha256': sha(stdout)},
                   stderr={'path': 'stderr.bin', 'bytes': len(stderr), 'sha256': sha(stderr)},
                   oversized=len(stdout) + len(stderr) > OUTPUT_LIMIT,
                   warning_review_required=bool(stderr))
    receipt['analysis_eligible'] = (receipt['status'] == 'returned' and
                                    receipt['returncode'] == 0 and not receipt['oversized'] and
                                    not receipt['warning_review_required'])
    dump(directory / 'execution.json', receipt)
    return receipt


def load_json(data):
    def reject_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f'duplicate JSON key: {key}')
            result[key] = value
        return result
    def reject_constant(value):
        raise ValueError('nonfinite JSON constant: ' + value)
    return json.loads(data, object_pairs_hook=reject_pairs, parse_constant=reject_constant)


def integer(value, label, string_ok=False):
    if value is None or type(value) is int:
        return value
    if string_ok and type(value) is str and re.fullmatch(r'-?\d+', value):
        return int(value)
    raise ValueError(f'{label}: expected integer or missing, got {value!r}')


def split_probe(data):
    """Accept ffprobe's combined shape or split arrays without changing raw fields."""
    require(type(data) is dict and type(data.get('streams')) is list, 'missing stream array')
    streams = data['streams']
    require(len(streams) == 1 and type(streams[0]) is dict, 'exactly one selected video stream')
    require(streams[0].get('codec_type') == 'video', 'selected stream is not video')
    tick = Fraction(streams[0]['time_base'])
    require(tick > 0, 'positive exact time base required')
    if 'packets_and_frames' in data:
        require('frames' not in data and 'packets' not in data, 'ambiguous mixed JSON shapes')
        combined = data['packets_and_frames']
        require(type(combined) is list, 'combined record array required')
        frames, packets = [], []
        for row in combined:
            require(type(row) is dict and row.get('type') in ('frame', 'packet'), 'unknown record type')
            (frames if row['type'] == 'frame' else packets).append(row)
    else:
        frames, packets = data.get('frames', []), data.get('packets', [])
        require(type(frames) is list and type(packets) is list, 'record arrays required')
    for kind, rows in (('frame', frames), ('packet', packets)):
        for row in rows:
            require(type(row) is dict, f'invalid {kind} record')
            require('type' not in row or row['type'] == kind, 'record type disagrees with array')
            for key in (('pts', 'pkt_dts', 'best_effort_timestamp', 'duration', 'pkt_duration')
                        if kind == 'frame' else ('pts', 'dts', 'duration')):
                integer(row.get(key), f'{kind}.{key}')
            for key in (('pkt_pos',) if kind == 'frame' else ('pos', 'size')):
                integer(row.get(key), f'{kind}.{key}', string_ok=True)
            if kind == 'frame':
                require(row.get('pict_type') is None or type(row['pict_type']) is str, 'invalid picture type')
    return {'streams': streams, 'frames': frames, 'packets': packets}, tick


def timestamp_summary(rows, field, tick):
    known, missing, absent, null = [], [], [], []
    for row in rows:
        ordinal, record = row['ordinal'], row['record']
        value = integer(record.get(field), field)
        if value is None:
            missing.append(ordinal)
            (null if field in record else absent).append(ordinal)
        else:
            known.append((ordinal, value))
    pairs = []
    for (left, a), (right, b) in zip(known, known[1:]):
        gap, delta = right - left, b - a
        require(gap > 0, 'strictly increasing record ordinals required')
        pairs.append({'from_ordinal': left, 'to_ordinal': right, 'ordinal_gap': gap,
                      'from_value': a, 'to_value': b, 'delta': delta,
                      'delta_seconds_exact': str(delta * tick),
                      'delta_per_ordinal_exact': str(Fraction(delta, gap))})
    adjacent = [r for r in pairs if r['ordinal_gap'] == 1]
    gaps = [r for r in pairs if r['ordinal_gap'] != 1]
    counts = dict(sorted(Counter(str(r['delta']) for r in pairs).items()))
    slopes = dict(sorted(Counter(r['delta_per_ordinal_exact'] for r in pairs).items()))
    return {'present_count': len(known), 'missing_ordinals': missing,
            'absent_ordinals': absent, 'null_ordinals': null,
            'pairs': pairs, 'adjacent_pairs': adjacent, 'gap_pairs': gaps,
            'delta_counts': counts, 'delta_per_ordinal_counts': slopes,
            'known_pairs_positive': all(r['delta'] > 0 for r in pairs) if pairs else None,
            'constant_delta_per_ordinal_on_known_pairs': len(slopes) == 1 if pairs else None,
            'all_ordinals_present': not missing,
            'regularity_limit': 'Known-output labels only; gap ratios do not fill missing labels or establish exposures.'}


def frame_summary(rows, tick):
    tabs = {}
    for row in rows:
        record = row['record']
        key = record.get('pict_type')
        key = '<missing>' if key is None else key
        entry = tabs.setdefault(key, dict(count=0, pts_present=0, pts_missing=0,
                                         best_effort_present=0, best_effort_missing=0))
        entry['count'] += 1
        entry['pts_missing' if record.get('pts') is None else 'pts_present'] += 1
        entry['best_effort_missing' if record.get('best_effort_timestamp') is None
              else 'best_effort_present'] += 1
    return {'count': len(rows), 'ordinals': [r['ordinal'] for r in rows],
            'picture_type_tabs': tabs,
            'timestamps': {key: timestamp_summary(rows, key, tick)
                           for key in ('pts', 'pkt_dts', 'best_effort_timestamp')}}


def positional_analysis(frames, packets, source, tick):
    positions = defaultdict(list)
    missing, negative, payloads = [], [], []
    for row in packets:
        i, record = row['ordinal'], row['record']
        pos = integer(record.get('pos'), 'pos', True)
        size = integer(record.get('size'), 'size', True)
        if pos is None:
            missing.append(i)
        elif pos < 0:
            negative.append(i)
        else:
            positions[pos].append(i)
        status = ('missing' if pos is None or size is None else
                  'valid' if pos >= 0 and size >= 0 and pos <= len(source) and size <= len(source) - pos
                  else 'out_of_bounds')
        digest = sha(source[pos:pos + size]) if status == 'valid' else None
        reported = record.get('data_hash')
        hash_valid = type(reported) is str and re.fullmatch(r'SHA256:[0-9a-fA-F]{64}', reported) is not None
        match = (digest == reported[7:].lower()) if digest is not None and hash_valid else None
        payloads.append({'packet_ordinal': i, 'position': pos, 'size': size,
                         'range_status': status, 'reported_data_hash': reported,
                         'computed_sha256': digest, 'hash_matches': match,
                         'hash_status': ('missing' if reported is None else 'malformed' if not hash_valid else
                                         'unchecked_range' if digest is None else 'match' if match else 'mismatch')})
    joins = []
    for row in frames:
        raw = row['record'].get('pkt_pos')
        pos = integer(raw, 'pkt_pos', True)
        matches = positions.get(pos, []) if pos is not None and pos >= 0 else []
        disposition = 'zero' if not matches else 'unique' if len(matches) == 1 else 'multiple'
        reason = ('missing_position' if pos is None else 'negative_position' if pos < 0 else
                  'no_packet_at_position' if not matches else 'unique_position' if len(matches) == 1
                  else 'duplicate_packet_position')
        joins.append({'frame_ordinal': row['ordinal'], 'raw_pkt_pos': raw, 'position': pos,
                      'disposition': disposition, 'packet_ordinals': matches, 'reason': reason})
    summary = {'count': len(packets),
               'null_counts': {key: sum(r['record'].get(key) is None for r in packets)
                               for key in PACKET_FIELDS},
               'position_groups': [{'position': p, 'packet_ordinals': ids} for p, ids in sorted(positions.items())],
               'missing_position_ordinals': missing, 'negative_position_ordinals': negative,
               'known_nonnegative_positions_unique': all(len(ids) == 1 for ids in positions.values()),
               'dts': timestamp_summary(packets, 'dts', tick)}
    return summary, joins, payloads


def analyze_arm(raw, source):
    data, tick = split_probe(raw)
    frames = [{'ordinal': i, 'record': r} for i, r in enumerate(data['frames'])]
    packets = [{'ordinal': i, 'record': r} for i, r in enumerate(data['packets'])]
    packet_summary, joins, payloads = positional_analysis(frames, packets, source, tick)
    return {'streams': data['streams'], 'time_base_exact': str(tick),
            'frames': frames, 'packets': packets,
            'frame_summaries': {'all': frame_summary(frames, tick),
                                'selected_274_411': frame_summary([r for r in frames if 274 <= r['ordinal'] <= 411], tick)},
            'packet_summary': packet_summary, 'joins': joins, 'payload_checks': payloads}


def differences(left, right, fields=None):
    """Field-level raw-value/presence diffs; changed/missing whole records stay explicit."""
    result = []
    for section in (fields if fields is not None else ('streams', 'frames', 'packets')):
        a, b = left[section], right[section]
        for i in range(max(len(a), len(b))):
            x, y = a[i] if i < len(a) else {}, b[i] if i < len(b) else {}
            names = sorted(set(x) | set(y)) if fields is None else sorted(fields[section])
            if i >= len(a) or i >= len(b):
                result.append({'section': section, 'ordinal': i, 'field': '__record__',
                               'left_present': i < len(a), 'left_value': None,
                               'right_present': i < len(b), 'right_value': None})
            for field in names:
                if ((field in x) != (field in y) or
                        json.dumps(x.get(field), sort_keys=True) != json.dumps(y.get(field), sort_keys=True)):
                    result.append({'section': section, 'ordinal': i, 'field': field,
                                   'left_present': field in x, 'left_value': x.get(field),
                                   'right_present': field in y, 'right_value': y.get(field)})
    return result


def analyze(default, genpts, baselines, source):
    raw_default, _ = split_probe(default)
    raw_genpts, _ = split_probe(genpts)
    changes = differences(raw_default, raw_genpts)
    identity = [r for r in changes if r['field'] == '__record__' or r['field'] in IDENTITY_FIELDS[r['section']]]
    previous = []
    for path, raw in baselines:
        old, _ = split_probe(raw)
        previous.append({'baseline_path': path, 'compared_fields': BASELINE_FIELDS,
                         'old_counts': {k: len(old[k]) for k in BASELINE_FIELDS},
                         'new_counts': {k: len(raw_default[k]) for k in BASELINE_FIELDS},
                         'differences': differences(old, raw_default, BASELINE_FIELDS)})
    return {'schema_version': 1, 'ordinal_basis': 'zero-based separately within each record type',
            'scope_limits': ['FFprobe output labels are not original exposure timestamps.',
                             'Positional/payload accounting does not parse MPEG4 pictures or prove one exposure per packet.',
                             'Metadata identity does not establish decoded-pixel or picture-order identity.'],
            'arms': {'default': analyze_arm(default, source), 'genpts': analyze_arm(genpts, source)},
            'arm_differences': {'all': changes, 'identity_fields': IDENTITY_FIELDS, 'identity': identity},
            'baseline_comparisons': previous}


def run_audit(name):
    output = output_directory(name)
    receipt = {'schema_version': 1, 'runtime': {'python': sys.version, 'executable': sys.executable},
               'pins_before': None, 'pins_after': None, 'processes': {}, 'status': 'started'}
    error = None
    try:
        receipt['pins_before'] = snapshot()
        dump(output / 'pins-before.json', receipt['pins_before'])
        check_expected(receipt['pins_before'])
        receipt['processes']['version'] = capture(output / 'version', [str(PROBE), '-version'], 'stdout.txt')
        for arm in ('default', 'genpts'):
            receipt['processes'][arm] = capture(output / arm, probe_argv(arm == 'genpts'))
        require(all(r['analysis_eligible'] for r in receipt['processes'].values()),
                'process output excluded: see complete retained diagnostics')
        receipt['pins_after'] = snapshot()
        check_expected(receipt['pins_after'])
        require(receipt['pins_before'] == receipt['pins_after'], 'inputs/code changed during probes')
        result = analyze(load_json((output / 'default' / 'stdout.json').read_bytes()),
                         load_json((output / 'genpts' / 'stdout.json').read_bytes()),
                         [('../' + p.parent.name + '/' + p.name, load_json(p.read_bytes())) for p in BASELINES],
                         SOURCE.read_bytes())
        # Catch changes during parsing and payload accounting before saving the analysis.
        final_pins = snapshot()
        require(final_pins == receipt['pins_before'], 'inputs/code changed during analysis')
        receipt['pins_after'] = final_pins
        dump(output / 'analysis.json', result)
        receipt['analysis'] = pin(output / 'analysis.json')
        receipt['status'] = 'analyzed_with_scope_limits'
    except Exception as exc:
        error = exc
        receipt.update(status='failed_preserved', error_type=type(exc).__name__, error=str(exc))
    finally:
        try:
            receipt['pins_after'] = snapshot()
            receipt['pins_unchanged'] = receipt['pins_before'] == receipt['pins_after']
            if not receipt['pins_unchanged']:
                receipt['status'] = 'failed_preserved'
                receipt['after_pin_error'] = 'final input/code pins differ'
                error = error or ValueError('final input/code pins differ')
        except Exception as exc:
            receipt['after_pin_error'] = str(exc)
            receipt['status'] = 'failed_preserved'
            error = error or exc
        receipt['output_pins'] = {str(p.relative_to(output)): pin(p) for p in sorted(output.rglob('*')) if p.is_file()}
        dump(output / 'receipt.json', receipt)
    if error is not None:
        raise error
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', choices=('run01', 'run02'), required=True)
    args = parser.parse_args()
    receipt = run_audit(args.out)
    print(json.dumps({'status': receipt['status'], 'analysis': receipt['analysis']}))


if __name__ == '__main__':
    main()

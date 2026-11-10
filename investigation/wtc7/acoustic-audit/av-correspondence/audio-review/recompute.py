#!/usr/bin/env python3
"""Independent exact-window check of retained float WAVs, not sound attribution."""
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import struct

HERE = Path(__file__).resolve().parent
AV = HERE.parent
AUDIO = AV.parent / 'run01'
RATE = 44100
TOLERANCE = 1e-10
SOURCES = {
    'edited': ('edited-stereo.wav', 430, 1102500,
               'b8557ab9a0f2ac6dc9d3d59d0334de96431340ad34f2e5642c47a5a51a3a09dd'),
    'msnbc': ('msnbc-stereo.wav', 578, 1675800,
              'b9758e82432a354fc584b22529b03c84aefc7b192d8579d5b8f95de3b715b292'),
}
EVENTS = [('edit435', 'edited', Fraction(435)),
          ('edit441', 'edited', Fraction(13256, 30)),
          ('edit580', 'msnbc', Fraction(17423, 30))]

def sha_bytes(value):
    return hashlib.sha256(value).hexdigest()

def ieee_wave(blob):
    if blob[:4] != b'RIFF' or blob[8:12] != b'WAVE' or struct.unpack_from('<I', blob, 4)[0] + 8 != len(blob):
        raise ValueError('Unexpected RIFF/WAVE header or byte count')
    position, fmt, data, chunks = 12, None, None, []
    while position < len(blob):
        kind, size = struct.unpack_from('<4sI', blob, position)
        first, end = position + 8, position + 8 + size
        if end > len(blob):
            raise ValueError('Truncated RIFF chunk')
        content = blob[first:end]
        if kind == b'fmt ':
            if fmt is not None:
                raise ValueError('Duplicate format chunk')
            fmt = struct.unpack_from('<HHIIHH', content, 0)
        elif kind == b'data':
            if data is not None:
                raise ValueError('Duplicate data chunk')
            data = content
        chunks.append({'id': kind.decode('ascii'), 'size': size, 'payload_offset': first})
        position = end + size % 2
    if fmt != (3, 2, RATE, RATE * 8, 8, 32) or data is None or len(data) % 8:
        raise ValueError('Expected 44.1kHz stereo IEEE-float32 contract')
    return data, chunks

def calculate(data, first, last):
    if not 0 <= first < last <= len(data) // 8:
        raise ValueError('Invalid half-open sample interval')
    columns = list(zip(*struct.iter_unpack('<ff', data[first*8:last*8])))
    if not all(math.isfinite(value) for col in columns for value in col):
        raise ValueError('Nonfinite sample')
    rms = [math.sqrt(math.fsum(value*value for value in col) / len(col)) for col in columns]
    peaks = [max(abs(value) for value in col) for col in columns]
    db = lambda values: [20*math.log10(value) if value else None for value in values]
    return {'first_sample': first, 'end_sample_exclusive': last, 'frames': last-first,
            'rms': rms, 'peak': peaks, 'rms_dbfs': db(rms), 'peak_dbfs': db(peaks)}

def integer_sample(time, origin):
    result = (time - Fraction(origin)) * RATE
    if result.denominator != 1:
        raise ValueError('Sample boundary is nonintegral')
    return result.numerator

def synthetic():
    pcm = b''.join(struct.pack('<ff', *frame) for frame in
                   [(0.25, -0.5)] * 4 + [(0.5, -0.25)] * 4)
    fmt = struct.pack('<HHIIHH', 3, 2, RATE, RATE*8, 8, 32)
    payload = b'WAVE' + b'JUNK' + struct.pack('<I', 1) + b'X\0' + b'fmt ' + struct.pack('<I', len(fmt)) + fmt + b'data' + struct.pack('<I', len(pcm)) + pcm
    blob = b'RIFF' + struct.pack('<I', len(payload)) + payload
    decoded, _ = ieee_wave(blob)
    first, last = calculate(decoded, 0, 4), calculate(decoded, 4, 8)
    checks = {'riff_unknown_odd_chunk': decoded == pcm,
              'known_pre_halfopen': first['frames'] == 4 and first['rms'] == first['peak'] == [.25, .5],
              'known_post_halfopen': last['frames'] == 4 and last['rms'] == last['peak'] == [.5, .25],
              'known_db': abs(first['rms_dbfs'][1] - (-6.020599913279624)) < 1e-14,
              'silence_null_db': calculate(b'\0'*32, 0, 4)['rms_dbfs'] == [None, None]}
    for label, action in [('reject_nonintegral', lambda: integer_sample(Fraction(1, 17), 0)),
                          ('reject_empty', lambda: calculate(decoded, 2, 2)),
                          ('reject_negative', lambda: calculate(decoded, -1, 2)),
                          ('reject_truncated_riff', lambda: ieee_wave(blob[:-1]))]:
        try:
            action()
        except ValueError:
            checks[label] = True
        else:
            checks[label] = False
    if not all(checks.values()):
        raise RuntimeError('Independent synthetic prerequisite failed')
    return checks

def main():
    destination = HERE / 'result.json'
    if destination.exists():
        raise FileExistsError('Refusing existing independent result')
    checks = synthetic()
    root_path = AV / 'audio01/measurements.json'
    root_bytes = root_path.read_bytes()
    root = json.loads(root_bytes)
    by_id = {row['id']: row for row in root['edits']}
    if len(by_id) != 3 or root['sample_rate'] != RATE or root['channel_order'] != ['L', 'R']:
        raise ValueError('Unexpected comparison scope')
    samples, source_records = {}, {}
    for label, (name, start, count, expected) in SOURCES.items():
        blob = (AUDIO / name).read_bytes()
        fingerprint = sha_bytes(blob)
        if fingerprint != expected or root['sources'][label] != {'sha256': expected, 'bytes': len(blob)}:
            raise ValueError('Retained derivative pin mismatch')
        data, chunks = ieee_wave(blob)
        if len(data)//8 != count:
            raise ValueError('Retained derivative frame count mismatch')
        samples[label] = data
        source_records[label] = {'filename': name, 'sha256': fingerprint, 'bytes': len(blob),
                                 'sample_frames': count, 'chunks': chunks}
    comparisons, records = [], []
    def compare(label, got, expected, exact=False):
        if exact or got is None or expected is None:
            comparisons.append({'field': label, 'mode': 'exact', 'pass': got == expected,
                                'actual': got, 'root': expected})
        else:
            err = abs(got-expected)
            comparisons.append({'field': label, 'mode': 'floating', 'absolute_error': err,
                                'tolerance': TOLERANCE, 'pass': err <= TOLERANCE})
    for event, label, at in EVENTS:
        reference = by_id[event]
        origin = SOURCES[label][1]
        compare(event+'/boundary_sample', integer_sample(at, origin), reference['boundary_sample'], True)
        compare(event+'/source_coordinate', str(at), reference['visual_first_new_frame_pts_seconds'], True)
        compare(event+'/source', label, reference['wav'], True)
        compare(event+'/wav_start', origin, reference['wav_start_seconds'], True)
        windows = [('before_0.1s', at-Fraction(1,10), at), ('after_0.1s', at, at+Fraction(1,10))]
        windows += [(f'bin_{i:02d}', at+Fraction(i-10,50), at+Fraction(i-9,50)) for i in range(20)]
        if set(reference['windows']) != {window[0] for window in windows}:
            raise ValueError('Unexpected reference window names')
        actual_windows = {}
        for name, begin, end in windows:
            actual = calculate(samples[label], integer_sample(begin, origin), integer_sample(end, origin))
            actual.update({'source_begin_exact': str(begin), 'source_end_exact': str(end)})
            ref = reference['windows'][name]
            for key in ['first_sample', 'end_sample_exclusive', 'frames', 'source_begin_exact', 'source_end_exact']:
                compare(event+'/'+name+'/'+key, actual[key], ref[key], True)
            for key in ['rms', 'peak', 'rms_dbfs', 'peak_dbfs']:
                for channel in range(2):
                    compare(event+'/'+name+'/'+key+'/'+str(channel), actual[key][channel], ref[key][channel])
            actual_windows[name] = actual
        records.append({'id': event, 'wav': label, 'coordinate': str(at), 'boundary_sample': integer_sample(at, origin), 'windows': actual_windows})
    after = {label: sha_bytes((AUDIO / item[0]).read_bytes()) for label, item in SOURCES.items()}
    before = {label: row['sha256'] for label, row in source_records.items()}
    if after != before or root_path.read_bytes() != root_bytes:
        raise ValueError('Input/comparison result changed during independent check')
    floats = [item for item in comparisons if item['mode'] == 'floating']
    result = {'scope': 'Independent numeric crosswalk only, shared retained derivatives; no fresh audio decode, listening, visual validation or physical timing assertion',
              'runtime': {'python': platform.python_version(), 'implementation': platform.python_implementation()},
              'procedure_sha256': sha_bytes(Path(__file__).read_bytes()),
              'root_measurements_sha256': sha_bytes(root_bytes),
              'root_code_sha256': sha_bytes((AV / 'audio_crosswalk.py').read_bytes()),
              'protocol_sha256': sha_bytes((AV / 'PROTOCOL.md').read_bytes()),
              'refinement_sha256': sha_bytes((AV / 'REFINEMENT.md').read_bytes()),
              'sources': source_records, 'sources_after': after, 'synthetic_checks': checks,
              'events': records, 'comparisons': comparisons,
              'summary': {'events': 3, 'windows': 66, 'scalar_comparisons': len(comparisons),
                          'floating_comparisons': len(floats), 'exact_comparisons': len(comparisons)-len(floats),
                          'max_absolute_floating_error': max(item['absolute_error'] for item in floats),
                          'floating_tolerance': TOLERANCE, 'all_pass': all(item['pass'] for item in comparisons)}}
    destination.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps(result['summary']))

if __name__ == '__main__':
    main()

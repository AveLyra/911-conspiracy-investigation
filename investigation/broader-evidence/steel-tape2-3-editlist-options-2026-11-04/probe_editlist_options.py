"""Compare MOV reader settings without modifying inputs or exporting media.

Callers must resolve media using their repository's storage guard first.
Outputs contain only JSON metadata, hashes and diagnostic text.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

MODES = {'default': [], 'advanced-off': ['-advanced_editlist', '0'],
         'ignore-edits': ['-ignore_editlist', '1']}
EXPECTED_SOURCE = '4beeea4b0e66c5fcaf68f5336ea4b76518f89c6d1cfbba6833915e359f8a4bcb'
EXPECTED_CONTROL = '4d99495157834a3913d610c0868086adf05c7088bff41f315ce57fc6728e0bc1'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def save(path, value):
    with path.open('x') as handle:
        json.dump(value, handle, indent=2)
        handle.write('\n')


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--control', required=True, type=Path)
    parser.add_argument('--native-map', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--ffprobe', default='ffprobe')
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(exist_ok=False)
    status = {'utc': datetime.now(timezone.utc).isoformat(), 'runs': [],
              'media_exported': False, 'source_written': False,
              'independent_decoder_test': False}
    before = args.source.stat()
    try:
        print('Hashing source and existing control before reads', flush=True)
        status['source_sha256_before'] = digest(args.source)
        assert status['source_sha256_before'] == EXPECTED_SOURCE
        assert before.st_size == 815698448
        assert digest(args.control) == EXPECTED_CONTROL
        for option, filename in [('-version', 'FFPROBE-VERSION.txt'),
                                 ('-h', 'MOV-HELP.txt')]:
            command = [args.ffprobe, option] if option == '-version' else [args.ffprobe, '-hide_banner', '-h', 'demuxer=mov']
            result = subprocess.run(command, capture_output=True, timeout=20)
            assert result.returncode == 0
            with (out / filename).open('xb') as handle:
                handle.write(result.stdout + result.stderr)
        assert b'ffprobe version 7.1.1' in (out / 'FFPROBE-VERSION.txt').read_bytes()
        results = {}
        for label, source in [('control', args.control), ('source', args.source)]:
            for mode, options in MODES.items():
                print('Running ' + label + ' / ' + mode, flush=True)
                command = [args.ffprobe, '-v', 'error', *options,
                           '-select_streams', 'v:0', '-count_packets', '-count_frames',
                           '-show_packets', '-show_streams', '-show_data_hash', 'sha256',
                           '-show_entries', 'packet=pts,dts,duration,pos,size,flags,data_hash:stream=codec_name,codec_tag_string,time_base,duration,nb_frames,nb_read_packets,nb_read_frames',
                           '-of', 'json', str(source)]
                result = subprocess.run(command, capture_output=True, timeout=120)
                prefix = label + '-' + mode
                with (out / (prefix + '.json')).open('xb') as handle:
                    handle.write(result.stdout)
                with (out / (prefix + '-stderr.txt')).open('xb') as handle:
                    handle.write(result.stderr)
                status['runs'].append({'label': label, 'mode': mode,
                                       'input_options': options,
                                       'exit_code': result.returncode,
                                       'stderr_bytes': len(result.stderr),
                                       'stdout_bytes': len(result.stdout),
                                       'stdout_sha256': hashlib.sha256(result.stdout).hexdigest()})
                assert result.returncode == 0
                decoded = json.loads(result.stdout)
                assert len(decoded['streams']) == 1
                if label == 'control':
                    stream = decoded['streams'][0]
                    assert len(decoded['packets']) == int(stream['nb_read_packets']) == int(stream['nb_read_frames']) == 3
                results[(label, mode)] = decoded
        with args.native_map.open(newline='') as handle:
            native = list(csv.DictReader(handle))
        assert len(native) == 11607
        by_pos = {int(row['file_offset']): row for row in native}
        assert len(by_pos) == len(native)
        analysis = {'control_all_three_settings_passed': True,
                    'native_map_rows': len(native), 'source_modes': {},
                    'common_packet_hash_comparisons': {},
                    'limited_independent_payload_reads': []}
        for mode in MODES:
            data = results[('source', mode)]
            packets = data['packets']
            stream = data['streams'][0]
            assert int(stream['nb_read_packets']) == len(packets)
            for packet in packets:
                row = by_pos[int(packet['pos'])]
                assert int(packet['size']) == int(row['size'])
                assert packet['data_hash'].startswith('SHA256:')
            indices = [int(by_pos[int(p['pos'])]['sample_index']) for p in packets]
            analysis['source_modes'][mode] = {
                'options': MODES[mode], 'stream': stream,
                'returned_packet_rows': len(packets),
                'native_address_size_matches': len(packets),
                'native_indices_first_last': [indices[0], indices[-1]],
                'native_indices_strictly_increasing': all(a < b for a, b in zip(indices, indices[1:])),
                'missing_native_indices': sorted(set(range(len(native))) - set(indices)),
                'first_packet': packets[0], 'last_three_packets': packets[-3:]}
        baseline = {int(p['pos']): p for p in results[('source', 'default')]['packets']}
        for mode in ['advanced-off', 'ignore-edits']:
            packets = {int(p['pos']): p for p in results[('source', mode)]['packets']}
            common = sorted(baseline.keys() & packets.keys())
            equal = all(baseline[pos]['data_hash'] == packets[pos]['data_hash'] for pos in common)
            assert equal
            analysis['common_packet_hash_comparisons'][mode] = {
                'common_offsets': len(common), 'all_common_hashes_equal': equal,
                'additional_offsets': sorted(packets.keys() - baseline.keys()),
                'absent_default_offsets': sorted(baseline.keys() - packets.keys())}
        with args.source.open('rb') as handle:
            for row in native[-3:]:
                pos, size = int(row['file_offset']), int(row['size'])
                handle.seek(pos)
                raw = handle.read(size)
                assert len(raw) == size
                sha = hashlib.sha256(raw).hexdigest()
                observed = []
                for mode in MODES:
                    matches = [p for p in results[('source', mode)]['packets'] if int(p['pos']) == pos]
                    if matches:
                        assert matches[0]['data_hash'] == 'SHA256:' + sha
                        observed.append(mode)
                analysis['limited_independent_payload_reads'].append({
                    'native_index': int(row['sample_index']), 'file_offset': pos,
                    'bytes': size, 'sha256': sha, 'matching_modes': observed})
        save(out / 'ANALYSIS.json', analysis)
        status['completed'] = True
    except Exception as error:
        status['completed'] = False
        status['error_type'] = type(error).__name__
        status['error'] = str(error)
    finally:
        print('Checking unchanged source after reads', flush=True)
        status['source_sha256_after'] = digest(args.source)
        after = args.source.stat()
        status['source_hash_size_mtime_unchanged'] = (
            status.get('source_sha256_before') == status['source_sha256_after'] == EXPECTED_SOURCE
            and (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns))
        status['control_sha256_after'] = digest(args.control)
        status['control_unchanged'] = status['control_sha256_after'] == EXPECTED_CONTROL
        save(out / 'RUN-STATUS.json', status)
        print(json.dumps({'completed': status['completed'],
                          'source_unchanged': status['source_hash_size_mtime_unchanged'],
                          'control_unchanged': status['control_unchanged'],
                          'runs': len(status['runs'])}), flush=True)
    if not status['completed'] or not status['source_hash_size_mtime_unchanged'] or not status['control_unchanged']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

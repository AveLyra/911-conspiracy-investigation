"""Separate tail-only diagnostic; does not complete the failed full-source test."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
from probe_editlist_options import MODES, EXPECTED_SOURCE, EXPECTED_CONTROL, digest, save


def main():
    parser = argparse.ArgumentParser(__doc__)
    for name in ['source', 'control', 'native-map', 'output-dir']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--ffprobe', default='ffprobe')
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(exist_ok=False)
    status = {'utc': datetime.now(timezone.utc).isoformat(), 'runs': [],
              'scope': 'Separate tail-only reader test; full-source timeout retained',
              'full_source_test_completed': False, 'media_exported': False}
    before = args.source.stat()
    try:
        print('Tail diagnostic: source/control full hashes before', flush=True)
        status['source_sha256_before'] = digest(args.source)
        assert status['source_sha256_before'] == EXPECTED_SOURCE
        assert digest(args.control) == EXPECTED_CONTROL
        results = {}
        for label, source, interval in [('control', args.control, '2%4'),
                                        ('source', args.source, '774%800')]:
            for mode, options in MODES.items():
                print('Tail diagnostic: ' + label + ' / ' + mode, flush=True)
                command = [args.ffprobe, '-v', 'error', *options,
                           '-read_intervals', interval, '-select_streams', 'v:0',
                           '-count_packets', '-count_frames', '-show_packets', '-show_streams',
                           '-show_data_hash', 'sha256', '-show_entries',
                           'packet=pts,dts,duration,pos,size,flags,data_hash:stream=codec_name,codec_tag_string,time_base,duration,nb_frames,nb_read_packets,nb_read_frames',
                           '-of', 'json', str(source)]
                prefix = label + '-' + mode
                try:
                    result = subprocess.run(command, capture_output=True, timeout=120)
                except subprocess.TimeoutExpired as error:
                    for kind, data in [('stdout', error.stdout), ('stderr', error.stderr)]:
                        with (out / (prefix + '-partial-' + kind + '.txt')).open('xb') as handle:
                            handle.write(data or b'')
                    status['runs'].append({'label': label, 'mode': mode,
                                           'input_options': options, 'read_interval': interval,
                                           'terminal_status': 'timeout120s', 'complete': False})
                    raise
                with (out / (prefix + '.json')).open('xb') as handle:
                    handle.write(result.stdout)
                with (out / (prefix + '-stderr.txt')).open('xb') as handle:
                    handle.write(result.stderr)
                status['runs'].append({'label': label, 'mode': mode,
                                       'input_options': options, 'read_interval': interval,
                                       'exit_code': result.returncode,
                                       'stderr_bytes': len(result.stderr), 'stdout_bytes': len(result.stdout),
                                       'stdout_sha256': hashlib.sha256(result.stdout).hexdigest()})
                assert result.returncode == 0
                decoded = json.loads(result.stdout)
                assert len(decoded['streams']) == 1
                packets = decoded['packets']
                assert packets
                if label == 'control':
                    stream = decoded['streams'][0]
                    assert len(packets) == int(stream['nb_read_packets']) == int(stream['nb_read_frames']) == 1
                    numerator, denominator = map(int, stream['time_base'].split('/'))
                    assert int(packets[0]['pts']) * numerator / denominator == 2
                results[(label, mode)] = decoded
        with args.native_map.open(newline='') as handle:
            native = list(csv.DictReader(handle))
        assert len(native) == 11607
        by_pos = {int(row['file_offset']): row for row in native}
        analysis = {'scope': 'Actual returned tails; requested seek not exact presentation/calibrated clock',
                    'tail_control_all_three_settings_passed': True,
                    'source_modes': {}, 'common_packet_hash_comparisons': {},
                    'limited_independent_payload_reads': []}
        for mode in MODES:
            data = results[('source', mode)]
            packets = data['packets']
            stream = data['streams'][0]
            assert len(packets) == int(stream['nb_read_packets'])
            indices = []
            for packet in packets:
                row = by_pos[int(packet['pos'])]
                assert int(packet['size']) == int(row['size'])
                indices.append(int(row['sample_index']))
            analysis['source_modes'][mode] = {
                'stream': stream, 'returned_tail_packet_rows': len(packets),
                'native_address_size_matches': len(packets),
                'native_indices': indices, 'packets': packets}
        default = {int(p['pos']): p for p in results[('source', 'default')]['packets']}
        for mode in ['advanced-off', 'ignore-edits']:
            other = {int(p['pos']): p for p in results[('source', mode)]['packets']}
            common = sorted(default.keys() & other.keys())
            assert common
            assert all(default[p]['data_hash'] == other[p]['data_hash'] for p in common)
            analysis['common_packet_hash_comparisons'][mode] = {
                'common_offsets': len(common), 'all_common_hashes_equal': True,
                'additional_offsets': sorted(other.keys() - default.keys()),
                'absent_default_offsets': sorted(default.keys() - other.keys())}
        with args.source.open('rb') as handle:
            for row in native[-3:]:
                pos, size = int(row['file_offset']), int(row['size'])
                handle.seek(pos)
                raw = handle.read(size)
                assert len(raw) == size
                sha = hashlib.sha256(raw).hexdigest()
                modes = []
                for mode in MODES:
                    found = [p for p in results[('source', mode)]['packets'] if int(p['pos']) == pos]
                    if found:
                        assert found[0]['data_hash'] == 'SHA256:' + sha
                        modes.append(mode)
                analysis['limited_independent_payload_reads'].append({
                    'native_index': int(row['sample_index']), 'file_offset': pos,
                    'bytes': size, 'sha256': sha, 'matching_modes': modes})
        save(out / 'ANALYSIS.json', analysis)
        status['completed'] = True
    except Exception as error:
        status['completed'] = False
        status['error_type'] = type(error).__name__
        status['error'] = str(error)
    finally:
        print('Tail diagnostic: source/control full hashes after', flush=True)
        status['source_sha256_after'] = digest(args.source)
        after = args.source.stat()
        status['source_hash_size_mtime_unchanged'] = (
            status.get('source_sha256_before') == status['source_sha256_after'] == EXPECTED_SOURCE
            and (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns))
        status['control_unchanged'] = digest(args.control) == EXPECTED_CONTROL
        save(out / 'RUN-STATUS.json', status)
        print(json.dumps({'completed': status['completed'], 'source_unchanged': status['source_hash_size_mtime_unchanged'],
                          'runs': len(status['runs'])}), flush=True)
    if not status['completed'] or not status['source_hash_size_mtime_unchanged'] or not status['control_unchanged']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

"""Capture raw diagnostics only; no scientific or historical-authenticity acceptance."""
import importlib.util
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
PARENT = BASE.parent / 'late-fire-sequence/sample_sequence.py'
spec = importlib.util.spec_from_file_location('prior_capture', PARENT)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def main():
    source = BASE / 'sources/CBS-VMS-Wtc7.wmv'
    out = BASE / 'diagnostics'
    out.mkdir()  # Existing results are never overwritten.
    identity = prior.observed_identity(source)
    result = {'source_before': identity, 'parent_code_sha256': prior.sha(PARENT),
              'code_sha256': prior.sha(Path(__file__)), 'python': sys.version,
              'scientific_or_human_acceptance': False, 'steps': []}
    try:
        prior.require(identity['bytes'] == 8717690, 'catalog-size mismatch')
        commands = [
            ('ffmpeg-version', [prior.FFMPEG, '-version']),
            ('ffprobe-version', [prior.FFPROBE, '-version']),
            ('container', [prior.FFPROBE, '-v', 'warning', '-show_streams',
                           '-show_format', '-of', 'json', str(source)]),
            ('probe', [prior.FFPROBE, '-v', 'warning', '-select_streams', 'v:0',
                       '-show_frames', '-show_streams', '-show_format', '-of', 'json', str(source)]),
        ]
        decode = [prior.FFMPEG, '-nostdin', '-hide_banner', '-nostats', '-v', 'warning',
                  '-copyts', '-noautorotate', '-guess_layout_max', '0', '-i', str(source),
                  '-map', '0:v:0', '-an', '-sn', '-dn', '-map_metadata', '-1',
                  '-map_chapters', '-1', '-fps_mode', 'passthrough',
                  '-enc_time_base:v', 'demux', '-pix_fmt', 'rgb24', '-c:v', 'rawvideo',
                  '-f', 'framemd5', '-']
        commands.extend([('decode01', decode), ('decode02', decode)])
        for name, command in commands:
            stdout, stderr, status = prior.run_command(command, out, name)
            result['steps'].append({'name': name, **status, 'stderr_bytes': len(stderr),
                                    'stdout_bytes': len(stdout)})
        result['source_after'] = prior.observed_identity(source)
        prior.require(result['source_after'] == identity, 'source changed')
        result['all_processes_zero_stderr_empty'] = all(
            r['returncode'] == 0 and r['stderr_bytes'] == 0 for r in result['steps'])
        result['repeat_stdout_identical'] = ((out/'decode01.stdout').read_bytes()
                                             == (out/'decode02.stdout').read_bytes())
        result['status'] = 'awaiting_inventory_review' if result[
            'all_processes_zero_stderr_empty'] else 'diagnostics_require_review'
    except Exception as exc:
        result['status'] = 'refused'
        result['error'] = type(exc).__name__ + ': ' + str(exc)
    finally:
        prior.save(out / 'receipt.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

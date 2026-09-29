#!/usr/bin/env python3
"""One create-only public acquisition; raw diagnostics stay local."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
TOOL = Path('/opt/homebrew/bin/yt-dlp')
TOOL_SHA = 'd6375f29058ce3bdd760e1d384e491a6dab454632bca7936dac045da1a6d93c1'
TOOL_PYTHON = Path('/opt/homebrew/Cellar/yt-dlp/2025.6.9/libexec/bin/python')
TOOL_PACKAGE = Path('/opt/homebrew/Cellar/yt-dlp/2025.6.9/libexec/lib/python3.13/site-packages/yt_dlp')
CHILD_ENV = {'PATH': '/opt/homebrew/bin:/usr/bin:/bin', 'LANG': 'C.UTF-8',
             'PYTHONNOUSERSITE': '1', 'PYTHONDONTWRITEBYTECODE': '1'}
ITEM = '83cFWPY07dI'


def identity(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(p, value):
    with p.open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def pin_inputs():
    files = [Path(__file__), HERE/'PROTOCOL.md', HERE/'ACQUISITION-CONTROLS.md',
             TOOL, Path(sys.executable), TOOL_PYTHON]
    package = {str(p.relative_to(TOOL_PACKAGE)): identity(p)
               for p in sorted(TOOL_PACKAGE.rglob('*.py'))}
    required = {'version.py', 'extractor/youtube/__init__.py', 'extractor/youtube/_video.py'}
    if not required <= package.keys():
        raise ValueError('Incomplete downloader package pin')
    return {'files': {str(p): identity(p) for p in files}, 'yt_dlp_python_files': package}


def run_preserved(command, out, timeout):
    record = {'argv': command, 'timeout_seconds': timeout}
    with (out/'stdout.local.txt').open('xb') as stdout, (out/'stderr.local.txt').open('xb') as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                   start_new_session=True, env=CHILD_ENV)
        try:
            record['exit'] = process.wait(timeout=timeout)
            record['status'] = 'returned'
        except subprocess.TimeoutExpired:
            # Only this newly created process group; do not leave descendants.
            os.killpg(process.pid, signal.SIGKILL)
            record['exit'] = process.wait()
            record['status'] = 'timeout'
    return record


def main():
    if len(sys.argv) != 1:
        raise ValueError('No overrides accepted')
    if identity(TOOL)['sha256'] != TOOL_SHA:
        raise ValueError('Downloader identity changed')
    if TOOL.read_text().splitlines()[0] != f'#!{TOOL_PYTHON}':
        raise ValueError('Unexpected downloader runtime')
    out = HERE/'acquisition01'
    if out.exists():
        raise FileExistsError('Refusing existing acquisition')
    pins = pin_inputs()
    out.mkdir()  # Refuse existing destination before network or file writes.
    record = {'started_utc': datetime.now(timezone.utc).isoformat(), 'pins_before': pins,
              'requested_id': ITEM, 'url': f'https://www.youtube.com/watch?v={ITEM}',
              'child_environment': CHILD_ENV, 'tool_version': '2025.06.09',
              'tool_python_version': '3.13.9',
              'pin_scope': 'launcher, two runtimes and yt_dlp Python sources; not all transitive libraries or loaded-code attestation'}
    command = [str(TOOL), '--ignore-config', '--no-plugin-dirs', '--no-cache-dir',
               '--proxy', '', '--fixup', 'warn', '--abort-on-unavailable-fragments',
               '--keep-fragments',
               '--no-playlist', '--abort-on-error', '--retries', '0', '--fragment-retries', '0',
               '--extractor-retries', '0', '--socket-timeout', '20', '--no-continue',
               '--no-overwrites', '--no-progress', '--no-colors', '--write-info-json',
               '--match-filters', f"id = '{ITEM}' & duration <= 30 & !is_live",
               '--max-filesize', '64M', '--format',
               'bestvideo[ext=mp4][height<=1080]/best[ext=mp4][height<=1080]',
               '--output', str(out/'source.%(ext)s'), record['url']]
    record['argv'] = command
    save(out/'start.json', record)
    try:
        record['process'] = run_preserved(command, out, 120)
    except Exception as e:
        # Exception class only in summary; preserve source diagnostics in files.
        record['exception_class'] = type(e).__name__
    finally:
        record['finished_utc'] = datetime.now(timezone.utc).isoformat()
        record['pins_after'] = pin_inputs()
        record['pins_unchanged'] = record['pins_after'] == pins
        record['products'] = {p.name: identity(p) for p in sorted(out.iterdir()) if p.is_file()}
        record['admission'] = 'unreviewed; process completion is not source admission'
        save(out/'receipt.json', record)
    print(json.dumps({'directory': out.name, 'process_status': record.get('process', {}).get('status'),
                      'exit': record.get('process', {}).get('exit'),
                      'exception_class': record.get('exception_class'),
                      'pins_unchanged': record['pins_unchanged'],
                      'products': {k: v['bytes'] for k, v in record['products'].items()}}))
    if record.get('process', {}).get('exit') != 0 or not record['pins_unchanged']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

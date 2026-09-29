"""Preserve full-page reading derivatives for the fixed nine-page source audit."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf')
SOURCE_SHA = '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f'
POPPLER = Path('/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler')
PAGES = (333, 334, 399, 400, 401, 772, 773, 774, 775)
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8',
       'DYLD_FALLBACK_LIBRARY_PATH': str(POPPLER/'lib')}


def identity(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(p, value):
    with p.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')


def run(command, prefix):
    record = {'argv': list(map(str, command)), 'timeout_seconds': 60}
    try:
        r = subprocess.run(command, capture_output=True, env=ENV, timeout=60)
        out, err = r.stdout, r.stderr
        record.update(status='returned', exit=r.returncode)
    except subprocess.TimeoutExpired as e:
        out, err = e.stdout or b'', e.stderr or b''
        record.update(status='timeout', exit=None)
    with prefix.with_suffix('.stdout').open('xb') as f:
        f.write(out)
    with prefix.with_suffix('.stderr').open('xb') as f:
        f.write(err)
    save(prefix.with_suffix('.json'), record)
    if record['exit'] != 0:
        raise RuntimeError('Preserved failed source-render command')


def main():
    out = HERE/'render01'
    if out.exists():
        raise FileExistsError('Refusing existing render directory')
    assert identity(SOURCE)['sha256'] == SOURCE_SHA
    pins = {str(p): identity(p) for p in (
        SOURCE, Path(__file__), HERE/'PROTOCOL.md', Path(sys.executable),
        POPPLER/'bin/pdftoppm', POPPLER/'bin/pdftotext')}
    out.mkdir()
    save(out/'start.json', {'pins': pins, 'pages': PAGES, 'dpi': 120,
                           'environment': ENV, 'python': sys.version})
    status = 'incomplete'
    try:
        for page in PAGES:
            run([POPPLER/'bin/pdftoppm', '-f', str(page), '-l', str(page),
                 '-singlefile', '-r', '120', '-png', SOURCE, out/f'p{page}'],
                out/f'p{page}-render')
            run([POPPLER/'bin/pdftotext', '-f', str(page), '-l', str(page),
                 '-layout', SOURCE, out/f'p{page}.txt'], out/f'p{page}-text')
        status = 'commands_complete_not_visual_review'
    finally:
        after = {p: identity(Path(p)) for p in pins}
        save(out/'receipt.json', {'status': status, 'pins_before': pins,
                                 'pins_after': after, 'pins_unchanged': pins == after,
                                 'products': {p.name: identity(p) for p in sorted(out.iterdir())}})
    assert pins == after
    print(json.dumps({'status': status, 'pages': len(PAGES),
                      'pngs': len(list(out.glob('*.png'))),
                      'nonempty_stderr': sum(bool(p.stat().st_size) for p in out.glob('*.stderr'))}))


if __name__ == '__main__':
    main()

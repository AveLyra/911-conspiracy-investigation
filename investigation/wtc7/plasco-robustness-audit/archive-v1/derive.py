#!/usr/bin/env python3
"""Create-only static Chapter 3 derivatives; no historical work on import."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

import pypdf
from PIL import Image, __version__ as PILLOW_VERSION

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/'
              'comparator-expansion/plasco-thesis/sources/domada-2025-plasco-thesis-8358.pdf')
SOURCE_PIN = {'bytes': 12229604,
              'sha256': '0d76577bbf898dfa2d1587d02f1cc51378d531e3b59983fc0d4db8665fd575b4'}
PROTOCOL_SHA = 'c53267b049e8241465a224825c32aabbe82e0cce59c2cce85da5174fcf30c304'
RUNTIME = Path('/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies')
RENDERER = RUNTIME / 'bin/override/pdftoppm'
RENDERER_WRAPPER = RUNTIME / 'native/poppler/bin/pdftoppm'
RENDERER_BINARY = RUNTIME / 'native/poppler/poppler/bin/pdftoppm'
PAGES = tuple(range(92, 133))
DPI = 110
TIMEOUT = 60


def pin(path):
    path = Path(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def write_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def dependencies():
    return {'source': SOURCE, 'code': Path(__file__).resolve(),
            'protocol': HERE / 'PROTOCOL.md', 'fontconfig': HERE / 'fonts.conf',
            'python': Path(sys.executable).resolve(), 'renderer': RENDERER,
            'renderer_wrapper': RENDERER_WRAPPER, 'renderer_binary': RENDERER_BINARY}


def snapshot(paths):
    result = {}
    for name, path in paths.items():
        try:
            result[name] = {'path': str(path), **pin(path)}
        except OSError as error:
            result[name] = {'path': str(path), 'error': type(error).__name__}
    return result


def environment(target):
    # Both wrapper scripts exec the next program. Font caches stay in this run.
    return {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8',
            'FONTCONFIG_FILE': str(HERE / 'fonts.conf'),
            'FONTCONFIG_PATH': str(HERE),
            'XDG_CACHE_HOME': str(target / 'font-cache')}


def command(argv, prefix, env):
    """Preserve stdout, stderr and status even for timeout/launch failure."""
    record = {'argv': [str(x) for x in argv], 'timeout_seconds': TIMEOUT,
              'returncode': None, 'status': 'launch_error'}
    stdout = stderr = b''
    try:
        result = subprocess.run(record['argv'], capture_output=True,
                                timeout=TIMEOUT, env=env, check=False)
        stdout, stderr = result.stdout, result.stderr
        record.update(returncode=result.returncode, status='returned')
    except subprocess.TimeoutExpired as error:
        stdout, stderr = error.stdout or b'', error.stderr or b''
        record['status'] = 'timeout'
    except OSError as error:
        record['error'] = {'type': type(error).__name__, 'message': str(error)}
    for suffix, data in ('.stdout', stdout), ('.stderr', stderr):
        with Path(str(prefix) + suffix).open('xb') as stream:
            stream.write(data)
    write_json(Path(str(prefix) + '.json'), record)
    return record


def boundaries(reader):
    if reader.is_encrypted or len(reader.pages) != 291:
        raise ValueError('Unexpected PDF encryption/page count')
    rows = []
    for physical, printed, chapter in ((92, 77, 3), (132, 117, None), (133, 118, 4)):
        text = reader.pages[physical - 1].extract_text()
        if not isinstance(text, str):
            raise ValueError(f'Missing boundary text at physical page {physical}')
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines or lines[-1] != str(printed):
            raise ValueError(f'Unexpected terminal printed label at physical page {physical}')
        if chapter is not None and not re.search(r'\bChapter\s+' + str(chapter) + r'\b', text, re.I):
            raise ValueError(f'Missing chapter boundary at physical page {physical}')
        if chapter == 3 and 'robustness analysis of plasco tower under fire conditions' not in ' '.join(text.lower().split()):
            raise ValueError('Unexpected Chapter 3 title')
        data = text.encode('utf-8')
        rows.append({'physical_page': physical, 'printed_page': printed,
                     'chapter': chapter, 'text_bytes': len(data),
                     'text_sha256': hashlib.sha256(data).hexdigest()})
    return rows


def run(name):
    if not isinstance(name, str) or re.fullmatch(r'[A-Za-z0-9]{1,40}', name) is None:
        raise ValueError('Run name must be 1-40 ASCII alphanumeric characters')
    target = HERE / name
    target.mkdir(exist_ok=False)  # Never write a refusal receipt into old output.
    receipt = {'created_utc': datetime.now(timezone.utc).isoformat(),
               'purpose': 'Static Chapter 3 derivatives; not model execution or scientific acceptance',
               'status': 'failed', 'pages': [], 'boundaries': [],
               'physical_pages': list(PAGES), 'dpi': DPI,
               'python': platform.python_version(), 'pypdf': pypdf.__version__,
               'pillow': PILLOW_VERSION, 'command': [sys.executable, *sys.argv],
               'limits': ['Rendering success does not establish pixel/glyph fidelity or source authenticity.',
                          'System font files and shared libraries are not completely pinned; no cross-machine pixel equivalence claimed.']}
    paths = dependencies()
    before = snapshot(paths)
    receipt['pins_before'] = before
    env = environment(target)
    receipt['environment'] = env
    try:
        write_json(target / 'start.json', {k: receipt[k] for k in
                   ('created_utc', 'physical_pages', 'dpi', 'python', 'pypdf', 'pillow', 'pins_before', 'environment')})
        if any('error' in value for value in before.values()):
            raise ValueError('Missing or unreadable dependency')
        if {key: before['source'][key] for key in ('bytes', 'sha256')} != SOURCE_PIN:
            raise ValueError('Unexpected source baseline')
        if before['protocol']['sha256'] != PROTOCOL_SHA:
            raise ValueError('Protocol differs from reviewed scope')
        reader = pypdf.PdfReader(SOURCE)
        receipt['boundaries'] = boundaries(reader)
        (target / 'font-cache').mkdir()
        version = command([RENDERER, '-v'], target / 'renderer-version', env)
        receipt['renderer_version_command'] = version
        if version['status'] != 'returned' or version['returncode'] != 0:
            raise RuntimeError('Renderer version command failed')
        for number in PAGES:
            stem = target / f'page-{number:03d}'
            row = {'physical_page': number, 'printed_page': number - 15,
                   'status': 'incomplete'}
            receipt['pages'].append(row)
            text = reader.pages[number - 1].extract_text()
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f'Missing text at physical page {number}')
            with stem.with_suffix('.txt').open('x', encoding='utf-8') as stream:
                stream.write(text)
            row['text'] = {'path': stem.with_suffix('.txt').name, **pin(stem.with_suffix('.txt'))}
            argv = [RENDERER, '-f', str(number), '-l', str(number), '-r', str(DPI),
                    '-singlefile', '-png', SOURCE, stem]
            result = command(argv, Path(str(stem) + '-render'), env)
            row['render'] = result
            png = stem.with_suffix('.png')
            if png.is_file():
                row['png'] = {'path': png.name, **pin(png)}
            if result['status'] != 'returned' or result['returncode'] != 0 or not png.is_file():
                raise RuntimeError(f'Render failed at physical page {number}')
            with Image.open(png) as image:
                if image.format != 'PNG':
                    raise ValueError('Unexpected render format')
                row['dimensions'] = list(image.size)
                image.verify()
            row['status'] = 'complete'
        receipt['status'] = 'complete'
    except Exception as error:
        receipt['failure'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        receipt['pins_after'] = snapshot(paths)
        receipt['pins_unchanged'] = receipt['pins_after'] == before
        if not receipt['pins_unchanged']:
            receipt['status'] = 'failed'
            receipt['changed_dependencies'] = [key for key in before if before[key] != receipt['pins_after'][key]]
        receipt['products'] = {p.name: pin(p) for p in sorted(target.iterdir()) if p.is_file()}
        write_json(target / 'receipt.json', receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    parser.add_argument('--authorized-render', action='store_true',
                        help='Required after explicit root review and historical-render GO')
    args = parser.parse_args()
    if not args.authorized_render:
        parser.error('Historical rendering requires review and explicit GO')
    result = run(args.run)
    print(json.dumps({'status': result['status'], 'pages': len(result['pages']),
                      'receipt': str(HERE / args.run / 'receipt.json')}))
    return 0 if result['status'] == 'complete' else 1


if __name__ == '__main__':
    raise SystemExit(main())

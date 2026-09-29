#!/usr/bin/env python3
"""Create-only complete-page derivatives for the fixed connection-curve study.

No curve recovery or PDF authoring. --self-test uses only synthetic temp files.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import logging
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import unittest
import warnings
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf')
SOURCE_SHA256 = 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4'
PAGES = (73, 74, 75, 76, 77, 117)
PDFTOPPM = Path('/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm')
FONT_CONFIG = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/nist-camera-method-audit/fonts.conf')
DPI = 200


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    path = Path(path)
    return {'path': str(path), 'resolved_path': str(path.resolve(strict=True)),
            'bytes': path.stat().st_size, 'sha256': digest(path.read_bytes())}


def check_source(path, expected):
    result = pin(path)
    if result['sha256'] != expected:
        raise ValueError('source SHA-256 mismatch')
    return result


def check_membership(pages):
    if tuple(pages) != PAGES:
        raise ValueError('exact ordered physical-page membership required')


def fresh_output(parent, name):
    # Refuse existing directories/files/symlinks, traversal, nested paths.
    if not name or name in ('.', '..') or Path(name).name != name:
        raise ValueError('output must be one new child directory name')
    parent = Path(parent).resolve(strict=True)
    result = parent / name
    if result.exists() or result.is_symlink():
        raise FileExistsError(result)
    result.mkdir()
    return result


def write_new(path, data):
    with Path(path).open('xb') as stream:
        stream.write(data)


def json_new(path, value):
    write_new(path, (json.dumps(value, indent=2, sort_keys=True) + '\n').encode())


def command_capture(argv, env, out, stem):
    result = subprocess.run(argv, env=env, capture_output=True, check=False)
    stdout = out / (stem + '.stdout')
    stderr = out / (stem + '.stderr')
    write_new(stdout, result.stdout)
    write_new(stderr, result.stderr)
    return {'argv': list(map(str, argv)), 'exit_code': result.returncode,
            'stdout': pin(stdout), 'stderr': pin(stderr)}


def same_pins(before, after):
    if before != after:
        raise ValueError('one or more inputs changed during processing')


def render(name):
    import PIL
    from PIL import Image
    import pypdf
    from pypdf import PdfReader

    check_membership(PAGES)
    check_source(SOURCE, SOURCE_SHA256)
    protocol = (HERE / 'PROTOCOL.md').read_text()
    if SOURCE_SHA256 not in protocol:
        raise ValueError('protocol does not contain the declared source hash')
    inputs = [SOURCE, Path(__file__).resolve(), HERE / 'PROTOCOL.md', FONT_CONFIG,
              Path(sys.executable), PDFTOPPM, Path(pypdf.__file__), Path(PIL.__file__)]
    before = [pin(path) for path in inputs]
    out = fresh_output(HERE, name)
    receipt = {'status': 'started', 'source': before[0], 'physical_pages': list(PAGES),
               'dpi': DPI, 'crop': False, 'requested_color': 'RGB',
               'printed_page_rule': 'physical page minus 51; must also be visually checked',
               'input_pins_before': before, 'commands': [], 'pages': [],
               'runtime': {'python': sys.version, 'python_executable': sys.executable,
                           'platform': platform.platform(), 'pypdf': pypdf.__version__,
                           'Pillow': PIL.__version__},
               'dependency_limit': 'Executable/module entry-point hashes and package versions, not a complete shared-library/font/package-content closure.'}
    parser_capture = io.StringIO()
    logger = logging.getLogger('pypdf')
    handler = logging.StreamHandler(parser_capture)
    logger.addHandler(handler)
    warning_records = []
    failure = None
    try:
        # Preserve the old config; only redirect its cache away from main.
        config = ET.fromstring(FONT_CONFIG.read_bytes())
        caches = config.findall('cachedir')
        if len(caches) != 1:
            raise ValueError('font config must have exactly one cache directory')
        caches[0].text = str(out / 'font-cache')
        config_bytes = ET.tostring(config, encoding='utf-8', xml_declaration=True)
        config_path = out / 'fonts.conf'
        write_new(config_path, config_bytes)
        receipt['font_config_transform'] = {'input': pin(FONT_CONFIG), 'output': pin(config_path),
                                            'change': 'cachedir only; XML serialization differs'}
        env = os.environ.copy()
        env['FONTCONFIG_FILE'] = str(config_path)
        receipt['environment_override'] = {'FONTCONFIG_FILE': str(config_path)}
        receipt['commands'].append(command_capture([str(PDFTOPPM), '-v'], env, out, 'poppler-version'))
        with warnings.catch_warnings(record=True) as captured, contextlib.redirect_stderr(parser_capture):
            warnings.simplefilter('always')
            reader = PdfReader(SOURCE)
            receipt['pdf_encrypted'] = reader.is_encrypted
            if reader.is_encrypted:
                receipt['empty_password_decrypt_result'] = int(reader.decrypt(''))
            receipt['pdf_page_count'] = len(reader.pages)
            if len(reader.pages) != 173:
                raise ValueError('source page count differs from expected 173')
            for physical in PAGES:
                page = reader.pages[physical - 1]
                prefix = out / f'page-{physical:03d}'
                cmd = [str(PDFTOPPM), '-f', str(physical), '-l', str(physical),
                       '-singlefile', '-r', str(DPI), '-png', str(SOURCE), str(prefix)]
                command = command_capture(cmd, env, out, f'page-{physical:03d}-render')
                receipt['commands'].append(command)
                if command['exit_code'] != 0:
                    raise RuntimeError(f'pdftoppm exited {command["exit_code"]} on page {physical}')
                png = prefix.with_suffix('.png')
                text_path = prefix.with_suffix('.txt')
                write_new(text_path, (page.extract_text() or '').encode('utf-8'))
                box = list(map(float, page.mediabox))
                rotation = int(page.get('/Rotate', 0)) % 360
                width, height = box[2] - box[0], box[3] - box[1]
                if rotation in (90, 270):
                    width, height = height, width
                expected = [math.ceil(width * DPI / 72), math.ceil(height * DPI / 72)]
                with Image.open(png) as image:
                    image.load()
                    if image.mode != 'RGB' or list(image.size) != expected:
                        raise ValueError(f'wrong mode/dimensions for page {physical}')
                    pixels = {'mode': image.mode, 'width': image.width, 'height': image.height,
                              'rgb_pixel_sha256': digest(image.tobytes())}
                receipt['pages'].append({'physical_page_1_based': physical,
                                         'printed_page_expected': physical - 51,
                                         'mediabox_points': box, 'cropbox_points': list(map(float, page.cropbox)),
                                         'rotation_degrees': rotation, 'image': pin(png),
                                         'pixels': pixels, 'text': pin(text_path)})
            warning_records = [{'category': w.category.__name__, 'message': str(w.message),
                                'filename': w.filename, 'lineno': w.lineno} for w in captured]
        receipt['input_pins_after'] = [pin(path) for path in inputs]
        same_pins(before, receipt['input_pins_after'])
        if tuple(row['physical_page_1_based'] for row in receipt['pages']) != PAGES:
            raise ValueError('rendered membership mismatch')
        receipt['status'] = 'complete_derivatives_only'
    except Exception as exc:
        failure = exc
        receipt['status'] = 'failed_preserved'
        receipt['failure'] = {'type': type(exc).__name__, 'message': str(exc)}
        receipt['input_pins_after'] = [pin(path) for path in inputs]
    finally:
        logger.removeHandler(handler)
        write_new(out / 'pypdf.stderr', parser_capture.getvalue().encode())
        json_new(out / 'pypdf.warnings.json', warning_records)
        receipt['products_before_receipt'] = [pin(p) for p in sorted(out.rglob('*')) if p.is_file()]
        receipt['render_stderr_nonempty'] = [c['stderr']['path'] for c in receipt['commands']
                                             if c['stderr']['bytes'] and '-v' not in c['argv']]
        receipt['parser_stderr_bytes'] = len(parser_capture.getvalue().encode())
        json_new(out / 'receipt.json', receipt)
    if failure:
        raise failure
    print(json.dumps({'status': receipt['status'], 'pages': len(receipt['pages']),
                      'receipt': pin(out / 'receipt.json'),
                      'nonempty_render_stderr': len(receipt['render_stderr_nonempty']),
                      'parser_stderr_bytes': receipt['parser_stderr_bytes']}))


class Guards(unittest.TestCase):
    def test_known_hash(self):
        self.assertEqual(digest(b'abc'), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')

    def test_source_pin_rejects_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'source'; p.write_bytes(b'abc')
            check_source(p, digest(b'abc'))
            with self.assertRaises(ValueError): check_source(p, '0' * 64)

    def test_exact_membership(self):
        check_membership(PAGES)
        for pages in (PAGES[:-1], PAGES[::-1], PAGES + (73,), (73, 74, 75, 76, 77, 118)):
            with self.assertRaises(ValueError): check_membership(pages)

    def test_create_only(self):
        with tempfile.TemporaryDirectory() as td:
            fresh_output(td, 'new')
            with self.assertRaises(FileExistsError): fresh_output(td, 'new')

    def test_reject_existing_file_and_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td); (p / 'file').write_bytes(b'x'); (p / 'link').symlink_to(p / 'missing')
            for name in ('file', 'link'):
                with self.assertRaises(FileExistsError): fresh_output(p, name)

    def test_reject_traversal(self):
        with tempfile.TemporaryDirectory() as td:
            for name in ('', '.', '..', '../escape', '/tmp/escape', 'a/b'):
                with self.assertRaises(ValueError): fresh_output(td, name)

    def test_exclusive_file_write(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'file'; write_new(p, b'first')
            with self.assertRaises(FileExistsError): write_new(p, b'second')
            self.assertEqual(p.read_bytes(), b'first')

    def test_changed_input_rejected(self):
        same_pins([{'sha256': 'a'}], [{'sha256': 'a'}])
        with self.assertRaises(ValueError): same_pins([{'sha256': 'a'}], [{'sha256': 'b'}])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='render01')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        render(args.out)

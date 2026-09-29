#!/usr/bin/env python3
"""Read-only, pinned complete-page viewer; loopback only, no writes or uploads."""
import argparse
import hashlib
import json
from http.server import ThreadingHTTPServer
from pathlib import Path
import struct
import types

HERE = Path(__file__).resolve().parent
R1 = HERE.parent / 'comparator-r1-replication'
HELPER_SHA = '1ea233c4fa8074298f9791a305fa46f0b1ac3151ce00ce48c8edd7e99de48142'
RECEIPT_SHA = '47d33d33b1695b00b21b72f9bda4a5c42d037ca1fb8a095c450aab9ba0eac1f5'
CANDIDATE_SHA = 'ec66ae85a45a0169b7e8cc61698cc522e75cda2f2905f4c283f45f88de1f55a7'
SOURCE_SHA = 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4'
PAGES = {
    73: (497348, '471745c7181f5edd02d84ad80ea3d396d26571c3441863b5909f8200877dbc4b'),
    74: (279563, '132859b7a2e3d5abb95f1411c7f111d6ec07c7c751ae2b1cd80954713a155856'),
    75: (309181, '60f4b265ff9449de096a091bbea9b0d8350209cee2a388533ee5c11efa802b20'),
    76: (943120, '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6'),
    77: (499256, 'cd0a15b5fa18a352c79d418d439f95c69b29f3713ff1106f0d325f269a9affc6'),
    117: (456303, '0f031fc21ba1639185ce134045ef6c6a4fcd8f814c4d0863b7e4e67e4b9f6e3d'),
}
CONTROL_SHA = 'f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pinned_bytes(path, digest):
    if path.is_symlink():
        raise ValueError('symlink_refused')
    data = path.read_bytes()
    if sha(data) != digest:
        raise ValueError('pin_mismatch')
    return data


def load_handler(path=R1 / 'serve_review.py', digest=HELPER_SHA):
    # Verify actual bytes BEFORE execution; no import cache or old-unit writes.
    data = pinned_bytes(path, digest)
    module = types.ModuleType('pinned_r1_readonly_handler')
    module.__file__ = str(path)
    exec(compile(data, str(path), 'exec'), module.__dict__)
    return module.handler_for


def check_png(data, size, width, height):
    if (len(data) != size or data[:16] != b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
            or len(data) < 33 or struct.unpack('>IIBBBBB', data[16:29])
            != (width, height, 8, 2, 0, 0, 0)):
        raise ValueError('png_header_or_size_mismatch')


def routes():
    receipt = json.loads(pinned_bytes(HERE / 'render01/receipt.json', RECEIPT_SHA))
    pinned_bytes(HERE / 'registration-root.md', CANDIDATE_SHA)
    pinned_bytes(Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf'), SOURCE_SHA)
    if (receipt['physical_pages'] != list(PAGES) or receipt['crop'] is not False
            or receipt['dpi'] != 200 or len(receipt['pages']) != len(PAGES)):
        raise ValueError('receipt_scope_mismatch')
    result = {}
    for number, record in zip(PAGES, receipt['pages']):
        size, digest = PAGES[number]
        path = HERE / f'render01/page-{number:03d}.png'
        if (record['physical_page_1_based'] != number
                or record['printed_page_expected'] != number - 51
                or record['image']['path'] != str(path)
                or record['image']['sha256'] != digest
                or record['image']['bytes'] != size
                or {k: record['pixels'][k] for k in ('width', 'height', 'mode')}
                != {'width': 1700, 'height': 2200, 'mode': 'RGB'}):
            raise ValueError('receipt_page_mismatch')
        check_png(pinned_bytes(path, digest), size, 1700, 2200)
        result[f'/pages/{number:03d}.png'] = (path, digest, 'image/png')
    path = R1 / 'localization-control/fixture.png'
    check_png(pinned_bytes(path, CONTROL_SHA), 11216, 1280, 720)
    result['/control.png'] = (path, CONTROL_SHA, 'image/png')
    for url, filename, mime in (
        ('/', 'review.html', 'text/html; charset=utf-8'),
        ('/coordinate.mjs', 'coordinate.mjs', 'text/javascript; charset=utf-8'),
    ):
        path = HERE / filename
        if path.is_symlink():
            raise ValueError('ui_symlink_refused')
        result[url] = (path, sha(path.read_bytes()), mime)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=0)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('port must be between 0 and 65535')
    handler_for = load_handler()
    assets = routes()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(assets))
    print(json.dumps({'url': f'http://127.0.0.1:{server.server_port}/',
                      'allowed_assets': len(assets), 'writes': False,
                      'ui_sha256': {url: assets[url][1] for url in ('/', '/coordinate.mjs')}}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()

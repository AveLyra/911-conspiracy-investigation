#!/usr/bin/env python3
"""Loopback-only, fixed-asset review server. No browsing, uploads or writes."""
import argparse
import hashlib
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
IMAGE_DIR = HERE.parent / 'comparator-roof-onset' / 'run02' / 'comparator'
FRAMES = {
    239: ('0001', '9f8d2878a69952da6d4a1e31f3a58415c9271c19e95160b28674692f5fb0439f'),
    434: ('0196', 'cbd2078df347521154157ae7c3b637585d3196cd3b1d1398ccc19be00cacacc5'),
    441: ('0203', '13c3d28ee22e129de4de3030cb2d9543079518b766f01487bf43694cdbf0f95f'),
    442: ('0204', '62f63c6b6f912cc4d5f859175dbd7b8da987dc6a440bd0f17366b803c02bea68'),
    443: ('0205', 'd64ec51cf17c6df8254446b642cef0542612e509245539b010c1bc8d473f80b3'),
    444: ('0206', '4679ce4d4e6634ac5721e36abc328ff11e75fa8eb57e468f6d390cf8c2200491'),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def routes():
    result = {}
    for url, filename, mime in (
        ('/', 'review.html', 'text/html; charset=utf-8'),
        ('/coordinate.js', 'coordinate.js', 'text/javascript; charset=utf-8'),
    ):
        path = HERE / filename
        result[url] = (path, sha(path.read_bytes()), mime)
    result['/control.png'] = (HERE / 'localization-control' / 'fixture.png',
        'f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48', 'image/png')
    for index, (ordinal, digest) in FRAMES.items():
        result[f'/frames/{index}.png'] = (IMAGE_DIR / f'frame-{ordinal}.png', digest, 'image/png')
    for path, digest, _ in result.values():
        if path.is_symlink() or sha(path.read_bytes()) != digest:
            raise ValueError('asset_identity_mismatch')
    return result


def route_key(target):
    try:
        parsed = urlsplit(target)
    except ValueError:
        return None
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        return None
    return target if target == parsed.path else None


def handler_for(assets):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'LocalReview/1'
        sys_version = ''

        def log_message(self, *_):
            pass  # Do not log arbitrary requested paths or headers.

        def end_headers(self):
            # Refusals receive the same restrictive policy as successful assets.
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Cross-Origin-Resource-Policy', 'same-origin')
            self.send_header('Content-Security-Policy',
                "default-src 'none'; img-src 'self'; script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; connect-src 'none'; "
                "frame-ancestors 'none'; form-action 'none'; base-uri 'none'")
            super().end_headers()

        def do_GET(self):
            self.respond(False)

        def do_HEAD(self):
            self.respond(True)

        def respond(self, head_only):
            authority = f'127.0.0.1:{self.server.server_port}'
            if self.headers.get('Host') != authority:
                self.send_error(403, 'Local host required')
                return
            origin = self.headers.get('Origin')
            if origin is not None and origin != f'http://{authority}':
                self.send_error(403, 'Cross-origin request refused')
                return
            key = route_key(self.path)
            if key not in assets:
                self.send_error(404, 'Not an allowed review asset')
                return
            path, digest, mime = assets[key]
            try:
                data = path.read_bytes()
                if path.is_symlink() or sha(data) != digest:
                    raise ValueError('asset_changed')
            except (OSError, ValueError):
                self.send_error(409, 'Review asset unavailable or changed')
                return
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            if not head_only:
                self.wfile.write(data)
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=0)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('port must be between 0 and 65535')
    assets = routes()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(assets))
    print(json.dumps({'url': f'http://127.0.0.1:{server.server_port}/',
                      'allowed_assets': len(assets), 'writes': False}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()

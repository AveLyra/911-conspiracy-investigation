#!/usr/bin/env python3
"""Seven-route read-only loopback diagnostic; no historical image routes."""
import argparse
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import types
import build_diagnostic as build


def load_handler():
    path = build.R1 / 'serve_review.py'
    data = build.read(path, build.HANDLER_SHA)
    module = types.ModuleType('pinned_r1_diagnostic_handler')
    module.__file__ = str(path)
    exec(compile(data, str(path), 'exec'), module.__dict__)
    return module.handler_for


def route_map(manifest, packet, control=None):
    control = control or build.R1 / 'localization-control/fixture.png'
    build.require(set(manifest['routes']) == build.ROUTES, 'exact seven routes required')
    result = {}
    for url, record in manifest['routes'].items():
        if url in build.CODE:
            build.require(record['kind'] == 'packet' and record['path'] == build.CODE[url],
                          'invalid packet route')
            path = packet / record['path']
            mime = 'text/html; charset=utf-8' if url == '/' else 'text/javascript; charset=utf-8'
        else:
            build.require(record['kind'] == 'source' and record['path'] == str(control),
                          'only exact synthetic source permitted')
            path = control; mime = 'image/png'
        build.require(record['mime'] == mime, 'route MIME mismatch')
        build.read(path, {k: record[k] for k in ('bytes', 'sha256')})
        result[url] = (path, record['sha256'], mime)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', required=True)
    parser.add_argument('--port', type=int, default=0)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535 or not build.re.fullmatch(r'packet[0-9]{2,}', args.packet):
        parser.error('explicit packetNN and port0–65535 required')
    packet = build.HERE / args.packet
    manifest = build.check_packet(packet)
    routes = route_map(manifest, packet)
    server = ThreadingHTTPServer(('127.0.0.1', args.port), load_handler()(routes))
    print(json.dumps({'url': f'http://127.0.0.1:{server.server_port}/',
                      'routes': sorted(routes), 'synthetic_only': True,
                      'writes': False, 'historical_measurement': False}), flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__ == '__main__':
    main()

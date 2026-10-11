#!/usr/bin/env python3
"""Pinned12-route loopback viewer. No directory browsing, writes or uploads."""
import argparse
import contextlib
import hashlib
from http.server import ThreadingHTTPServer
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock, patch

HERE = Path(__file__).resolve().parent
R1 = HERE.parent.parent / 'comparator-r1-replication'
BUILD_SHA = '3deb0c8ed6c1a2cd367ceaf096dac1ac4250a790f73c331128dd8141fd168b6c'
HANDLER_SHA = '1ea233c4fa8074298f9791a305fa46f0b1ac3151ce00ce48c8edd7e99de48142'
HANDLER_TEST_SHA = '2ab32ba83583958b49ebbdb36b8a5327d47b02da2a7b995a4551588a402aa6a8'
EXPECTED_ROUTES = {'/', '/review.mjs', '/response.mjs', '/coordinate-core.mjs', '/assets.mjs',
                   '/control.png', '/frames/274.png', '/frames/300.png', '/frames/342.png',
                   '/frames/365.png', '/frames/388.png', '/frames/411.png'}
CODE_FILES = {'/': 'review.html', '/review.mjs': 'review.mjs', '/response.mjs': 'response.mjs',
              '/coordinate-core.mjs': 'coordinate-core.mjs', '/assets.mjs': 'assets.mjs'}


def load_pinned(path, expected, name):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError('pinned module missing or symlinked')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('pinned module changed before execution')
    module = types.ModuleType(name)
    module.__file__ = str(path)
    # No import-cache writes into preserved units.
    exec(compile(data, str(path), 'exec'), module.__dict__)
    return module


def load_handler():
    return load_pinned(R1 / 'serve_review.py', HANDLER_SHA, 'pinned_r1_localization_handler').handler_for


def route_map(manifest, packet):
    declared = manifest['routes']
    if set(declared) != EXPECTED_ROUTES:
        raise ValueError('exact12-route scope required')
    result = {}
    for url, record in declared.items():
        if url in CODE_FILES:
            if record['kind'] != 'packet' or record['path'] != CODE_FILES[url]:
                raise ValueError('unexpected packet file route')
            path = packet / record['path']
        else:
            if record['kind'] != 'source' or not Path(record['path']).is_absolute():
                raise ValueError('expected original pinned source path')
            path = Path(record['path'])
        result[url] = (path, record['sha256'], record['mime'])
    return result


def routes(packet_name):
    builder = load_pinned(HERE / 'build_packet.py', BUILD_SHA, 'pinned_localization_builder')
    packet = HERE / packet_name
    manifest = builder.check_packet(packet)
    return route_map(manifest, packet), manifest


class Controls(unittest.TestCase):
    def test_wrong_module_pin_prevents_execution(self):
        with tempfile.TemporaryDirectory(prefix='localization-server-synthetic-') as temp:
            path = Path(temp) / 'fixture.py'
            path.write_text('raise AssertionError("must not execute")\n')
            with self.assertRaises(ValueError): load_pinned(path, '0' * 64, 'rejected')

    def test_module_symlink_and_missing_refused(self):
        with tempfile.TemporaryDirectory(prefix='localization-server-synthetic-') as temp:
            path = Path(temp) / 'fixture.py'; path.write_text('VALUE=1\n')
            link = Path(temp) / 'link.py'; link.symlink_to(path)
            expected = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(load_pinned(path, expected, 'synthetic').VALUE, 1)
            with self.assertRaises(ValueError): load_pinned(link, expected, 'rejected')
            with self.assertRaises(ValueError): load_pinned(Path(temp) / 'missing', expected, 'rejected')

    def fixture(self):
        values = {}
        for route in EXPECTED_ROUTES:
            code = route in CODE_FILES
            values[route] = {'kind': 'packet' if code else 'source',
                             'path': CODE_FILES[route] if code else '/synthetic/not-historical.png',
                             'sha256': 'a' * 64, 'mime': 'text/plain'}
        return {'routes': values}

    def test_twelve_routes_manifest_not_served(self):
        result = route_map(self.fixture(), Path('/synthetic/packet01'))
        self.assertEqual(set(result), EXPECTED_ROUTES)
        self.assertEqual(len(result), 12)
        self.assertNotIn('/manifest.json', result)
        self.assertEqual(result['/'][0], Path('/synthetic/packet01/review.html'))

    def test_route_missing_extra_and_traversal_rejected(self):
        for alteration in ('missing', 'extra', 'traversal', 'source-relative'):
            manifest = self.fixture()
            if alteration == 'missing': del manifest['routes']['/control.png']
            elif alteration == 'extra': manifest['routes']['/manifest.json'] = {}
            elif alteration == 'traversal': manifest['routes']['/']['path'] = '../review.html'
            else: manifest['routes']['/control.png']['path'] = '../source.png'
            with self.assertRaises(ValueError): route_map(manifest, Path('/synthetic/packet01'))

    def test_main_loopback_and_no_autostart_on_import(self):
        server = MagicMock(); server.server_port = 12345
        server.serve_forever.side_effect = KeyboardInterrupt
        with patch.object(sys, 'argv', ['serve_review.py', '--packet', 'packet01', '--port', '0']), \
             patch(__name__ + '.routes', return_value=({}, {'protocol_sha256': 'synthetic'})), \
             patch(__name__ + '.load_handler', return_value=lambda assets: object()), \
             patch(__name__ + '.ThreadingHTTPServer', return_value=server) as factory, \
             contextlib.redirect_stdout(io.StringIO()):
            main()
        self.assertEqual(factory.call_args.args[0], ('127.0.0.1', 0))
        server.server_close.assert_called_once()

    def test_invalid_ports_stop_before_input_loading(self):
        for port in ('-1', '65536'):
            with patch.object(sys, 'argv', ['serve_review.py', '--packet', 'packet01', '--port', port]), \
                 patch(__name__ + '.routes') as loader, contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit): main()
                loader.assert_not_called()


def self_test():
    # Reuse the unchanged20 synthetic handler controls, never its historical routes().
    sys.dont_write_bytecode = True
    load_pinned(R1 / 'serve_review.py', HANDLER_SHA, 'checked_handler_identity')
    shared = load_pinned(R1 / 'test_server.py', HANDLER_TEST_SHA, 'shared_r1_http_tests')
    suite = unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(Controls),
        unittest.defaultTestLoader.loadTestsFromModule(shared),
    ])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--packet')
    parser.add_argument('--port', type=int, default=0)
    args = parser.parse_args()
    if args.self_test:
        if args.packet is not None:
            parser.error('self-test cannot serve a packet')
        raise SystemExit(not self_test())
    if args.packet is None or not 0 <= args.port <= 65535:
        parser.error('explicit packet and port0–65535 required')
    assets, manifest = routes(args.packet)
    handler_for = load_handler()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(assets))
    print(json.dumps({'url': f'http://127.0.0.1:{server.server_port}/', 'packet': args.packet,
                      'allowed_routes': sorted(assets), 'writes': False,
                      'protocol_sha256': manifest['protocol_sha256'],
                      'human_review_implied': False}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()

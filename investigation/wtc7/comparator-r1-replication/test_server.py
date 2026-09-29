"""Synthetic HTTP boundary checks; never load source images or UI files."""
import contextlib
import hashlib
import http.client
import importlib.util
import io
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import MagicMock, patch


SPEC = importlib.util.spec_from_file_location(
    'review_server_under_test', Path(__file__).with_name('serve_review.py'))
SERVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SERVER)


class ServerControls(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='r1-http-control-')
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.assets = {}
        routes = [('/', 'text/html; charset=utf-8'),
                  ('/coordinate.js', 'text/javascript; charset=utf-8'),
                  ('/control.png', 'image/png')]
        routes += [(f'/frames/{i}.png', 'image/png')
                   for i in (239, 434, 441, 442, 443, 444)]
        for ordinal, (route, mime) in enumerate(routes):
            path = self.root / f'dummy-{ordinal}.bin'
            data = f'SYNTHETIC HTTP FIXTURE {ordinal}'.encode('ascii')
            path.write_bytes(data)
            self.assets[route] = (path, hashlib.sha256(data).hexdigest(), mime)
        self.httpd = SERVER.ThreadingHTTPServer(
            ('127.0.0.1', 0), SERVER.handler_for(self.assets))
        self.authority = f'127.0.0.1:{self.httpd.server_port}'
        self.thread = threading.Thread(
            target=self.httpd.serve_forever,
            kwargs={'poll_interval': 0.01}, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        self.assertFalse(self.thread.is_alive())
        self.directory.cleanup()

    def request(self, target='/', method='GET', host=None, origin=None):
        connection = http.client.HTTPConnection(
            '127.0.0.1', self.httpd.server_port, timeout=2)
        try:
            connection.putrequest(method, target, skip_host=True,
                                  skip_accept_encoding=True)
            connection.putheader('Host', self.authority if host is None else host)
            if origin is not None:
                connection.putheader('Origin', origin)
            connection.endheaders()
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            connection.close()

    def assert_security_headers(self, headers):
        self.assertEqual(headers.get('Cache-Control'), 'no-store')
        self.assertEqual(headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(headers.get('Referrer-Policy'), 'no-referrer')
        self.assertEqual(headers.get('Cross-Origin-Resource-Policy'), 'same-origin')
        policy = headers.get('Content-Security-Policy', '')
        for directive in ("default-src 'none'", "img-src 'self'",
                          "script-src 'self'", "connect-src 'none'",
                          "frame-ancestors 'none'", "form-action 'none'",
                          "base-uri 'none'"):
            self.assertIn(directive, policy)
        self.assertNotIn('Access-Control-Allow-Origin', headers)

    def test_all_nine_fixed_assets(self):
        for route, (path, _, mime) in self.assets.items():
            with self.subTest(route=route):
                status, headers, body = self.request(route)
                self.assertEqual(status, 200)
                self.assertEqual(body, path.read_bytes())
                self.assertEqual(headers['Content-Type'], mime)
                self.assertEqual(int(headers['Content-Length']), len(body))

    def test_head_has_same_length_and_no_body(self):
        for route, (path, _, _) in self.assets.items():
            with self.subTest(route=route):
                status, headers, body = self.request(route, method='HEAD')
                self.assertEqual(status, 200)
                self.assertEqual(body, b'')
                self.assertEqual(int(headers['Content-Length']), path.stat().st_size)

    def test_unknown_assets_and_directories(self):
        for route in ('/missing', '/frames', '/frames/', '/frames/240.png',
                      '/frames/239.png/', '/coordinate.js/extra'):
            with self.subTest(route=route):
                self.assertEqual(self.request(route)[0], 404)

    def test_traversal_not_resolved(self):
        for route in ('/../private.txt', '/frames/../coordinate.js',
                      '/%2e%2e/private.txt', '/frames/%2e%2e/coordinate.js',
                      '/..%2fprivate.txt', '/frames%2f239.png'):
            with self.subTest(route=route):
                self.assertEqual(self.request(route)[0], 404)

    def test_query_fragment_and_absolute_target_refused(self):
        for route in ('/?x=1', '/?', '/#part', '/#',
                      '/frames/239.png?x=1',
                      f'http://{self.authority}/', '//other.invalid/'):
            with self.subTest(route=route):
                self.assertEqual(self.request(route)[0], 404)

    def test_wrong_host_refused(self):
        for host in ('other.invalid', f'localhost:{self.httpd.server_port}',
                     '127.0.0.1', '127.0.0.1:1',
                     f'127.0.0.1:{self.httpd.server_port}.other.invalid'):
            with self.subTest(host=host):
                self.assertEqual(self.request(host=host)[0], 403)

    def test_cross_origin_refused(self):
        for origin in ('https://other.invalid', 'null',
                       f'https://{self.authority}', 'http://127.0.0.1:1'):
            with self.subTest(origin=origin):
                self.assertEqual(self.request(origin=origin)[0], 403)

    def test_exact_same_origin_permitted(self):
        self.assertEqual(self.request(origin=f'http://{self.authority}')[0], 200)

    def test_mutating_and_options_methods_not_implemented(self):
        before = {p: p.read_bytes() for p, _, _ in self.assets.values()}
        for method in ('POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'):
            with self.subTest(method=method):
                self.assertEqual(self.request(method=method)[0], 501)
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_changed_asset_refused(self):
        self.assets['/control.png'][0].write_bytes(b'SYNTHETIC CHANGED BY TEST')
        status, _, body = self.request('/control.png')
        self.assertEqual(status, 409)
        self.assertNotIn(b'SYNTHETIC CHANGED BY TEST', body)

    def test_missing_asset_refused(self):
        self.assets['/control.png'][0].unlink()
        self.assertEqual(self.request('/control.png')[0], 409)

    def test_symlink_even_with_same_bytes_refused(self):
        path = self.assets['/control.png'][0]
        duplicate = self.root / 'duplicate.bin'
        duplicate.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(duplicate)
        self.assertEqual(self.request('/control.png')[0], 409)

    def test_success_security_headers(self):
        for method in ('GET', 'HEAD'):
            with self.subTest(method=method):
                self.assert_security_headers(self.request(method=method)[1])

    def test_error_security_headers(self):
        responses = [self.request('/missing'),
                     self.request(host='other.invalid'),
                     self.request(method='POST')]
        self.assets['/control.png'][0].write_bytes(b'SYNTHETIC CHANGED BY TEST')
        responses.append(self.request('/control.png'))
        for status, headers, _ in responses:
            with self.subTest(status=status):
                self.assert_security_headers(headers)

    def test_head_error_has_no_body(self):
        status, _, body = self.request('/missing', method='HEAD')
        self.assertEqual(status, 404)
        self.assertEqual(body, b'')

    def test_malformed_absolute_target_refused_cleanly(self):
        self.assertEqual(self.request('http://[/')[0], 404)

    def test_existing_nonwhitelist_file_not_exposed(self):
        marker = b'SYNTHETIC NOT WHITELISTED'
        (self.root / 'private.txt').write_bytes(marker)
        for route in ('/private.txt', '/./private.txt', '/frames/'):
            with self.subTest(route=route):
                status, _, body = self.request(route)
                self.assertEqual(status, 404)
                self.assertNotIn(marker, body)
                self.assertNotIn(b'dummy-0.bin', body)

    def test_changed_asset_head_refused(self):
        self.assets['/control.png'][0].write_bytes(b'SYNTHETIC CHANGED BY TEST')
        status, _, body = self.request('/control.png', method='HEAD')
        self.assertEqual(status, 409)
        self.assertEqual(body, b'')


class EntrypointControls(unittest.TestCase):
    def test_main_binds_only_ipv4_loopback(self):
        fake = MagicMock()
        fake.server_port = 12345
        fake.serve_forever.side_effect = KeyboardInterrupt
        with patch.object(SERVER, 'routes', return_value={}), \
             patch.object(SERVER, 'ThreadingHTTPServer', return_value=fake) as factory, \
             patch('sys.argv', ['serve_review.py', '--port', '0']), \
             contextlib.redirect_stdout(io.StringIO()):
            SERVER.main()
        self.assertEqual(factory.call_args.args[0], ('127.0.0.1', 0))
        fake.server_close.assert_called_once()

    def test_invalid_ports_rejected_before_route_loading(self):
        for port in ('-1', '65536'):
            with self.subTest(port=port), \
                 patch.object(SERVER, 'routes') as routes, \
                 patch('sys.argv', ['serve_review.py', '--port', port]), \
                 contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    SERVER.main()
                self.assertEqual(caught.exception.code, 2)
                routes.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)

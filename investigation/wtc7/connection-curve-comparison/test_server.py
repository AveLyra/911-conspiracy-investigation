"""Read-only asset preflight plus synthetic loopback HTTP/security controls."""
import contextlib
import hashlib
import http.client
import io
import json
from pathlib import Path
import re
import struct
import tempfile
import threading
import types
import unittest
from unittest.mock import MagicMock, patch

HERE = Path(__file__).resolve().parent
SERVER = types.ModuleType('connection_viewer_under_test')
SERVER.__file__ = str(HERE / 'serve_review.py')
exec(compile((HERE / 'serve_review.py').read_bytes(), SERVER.__file__, 'exec'), SERVER.__dict__)


class AssetControls(unittest.TestCase):
    def test_fixed_asset_membership_pins_dimensions_and_javascript_metadata(self):
        routes = SERVER.routes()  # Read only; no decode, display or source modification.
        self.assertEqual(len(routes), 9)
        source = (HERE / 'coordinate.mjs').read_text()
        assets = json.loads(re.search(r'export const ASSETS = (\{.*?\n\});', source, re.S)[1])
        self.assertEqual(set(assets), {'control', '73', '74', '75', '76', '77', '117'})
        for record in assets.values():
            path, digest, mime = routes[record['url']]
            data = path.read_bytes()
            self.assertEqual(digest, record['hash'])
            self.assertEqual(len(data), record['bytes'])
            self.assertEqual(struct.unpack('>II', data[16:24]), (record['width'], record['height']))
            self.assertEqual(mime, 'image/png')

    def test_helper_pin_is_checked_before_execution(self):
        with tempfile.TemporaryDirectory(prefix='curve-helper-test-') as folder:
            path = Path(folder) / 'helper.py'
            path.write_bytes(b'raise RuntimeError("executed_before_pin")')
            with self.assertRaisesRegex(ValueError, 'pin_mismatch'):
                SERVER.load_handler(path, '0' * 64)
            with self.assertRaisesRegex(RuntimeError, 'executed_before_pin'):
                SERVER.load_handler(path, SERVER.sha(path.read_bytes()))
        self.assertEqual(SERVER.load_handler().__name__, 'handler_for')

    def test_png_header_size_and_color_guards(self):
        data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + struct.pack('>IIBBBBB', 2, 3, 8, 2, 0, 0, 0) + b'fake'
        SERVER.check_png(data, len(data), 2, 3)
        for size, width, height, raw in [(len(data)+1,2,3,data),(len(data),3,2,data),(len(data),2,3,b'X'+data[1:]),(len(data),2,3,data[:25]+b'\x00'+data[26:])]:
            with self.assertRaises(ValueError): SERVER.check_png(raw, size, width, height)

    def test_external_module_no_inline_script_or_remote_assets(self):
        html = (HERE / 'review.html').read_text()
        self.assertEqual(re.findall(r'<script\b[^>]*>.*?</script>',html,re.S), ['<script type="module" src="/coordinate.mjs"></script>'])
        self.assertNotRegex(html, r'(?:src|href)=["\']https?://')


class HTTPControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='curve-http-test-')
        self.root = Path(self.tmp.name)
        self.assets = {}
        for i, route in enumerate(['/', '/coordinate.mjs', '/control.png', *[f'/pages/{n:03d}.png' for n in SERVER.PAGES]]):
            path = self.root / f'asset-{i}'
            path.write_bytes(f'SYNTHETIC {i}'.encode())
            self.assets[route] = (path, SERVER.sha(path.read_bytes()), 'application/octet-stream')
        self.httpd = SERVER.ThreadingHTTPServer(('127.0.0.1',0),SERVER.load_handler()(self.assets))
        self.thread = threading.Thread(target=self.httpd.serve_forever,kwargs={'poll_interval':.01},daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown(); self.httpd.server_close(); self.thread.join(timeout=2)
        self.assertFalse(self.thread.is_alive()); self.tmp.cleanup()

    def request(self, target='/', method='GET', host=None, origin=None):
        c = http.client.HTTPConnection('127.0.0.1',self.httpd.server_port,timeout=2)
        try:
            c.putrequest(method,target,skip_host=True,skip_accept_encoding=True)
            c.putheader('Host',host if host is not None else f'127.0.0.1:{self.httpd.server_port}')
            if origin is not None: c.putheader('Origin',origin)
            c.endheaders(); r=c.getresponse()
            return r.status,dict(r.getheaders()),r.read()
        finally: c.close()

    def test_all_nine_routes_get_head_and_security_policy(self):
        for route,(path,_,_) in self.assets.items():
            for method in ('GET','HEAD'):
                status,headers,body=self.request(route,method)
                self.assertEqual(status,200)
                self.assertEqual(body,path.read_bytes() if method=='GET' else b'')
                self.assertEqual(int(headers['Content-Length']),path.stat().st_size)
                self.assertEqual(headers['Cache-Control'],'no-store')
                self.assertEqual(headers['X-Content-Type-Options'],'nosniff')
                self.assertEqual(headers['Referrer-Policy'],'no-referrer')
                self.assertIn("script-src 'self';",headers['Content-Security-Policy'])
                self.assertIn("connect-src 'none'",headers['Content-Security-Policy'])
                self.assertNotIn('Access-Control-Allow-Origin',headers)

    def test_exact_routes_no_query_traversal_directories_or_absolute_url(self):
        for route in ['/pages','/pages/','/pages/078.png','/private.txt','/../private.txt','/%2e%2e/private.txt','/pages/../coordinate.mjs','/?x=1','/?','/#','http://invalid/','http://[/','/pages%2f073.png']:
            self.assertEqual(self.request(route)[0],404,route)

    def test_host_and_origin_boundaries(self):
        for host in ['invalid', '127.0.0.1', f'localhost:{self.httpd.server_port}']:
            self.assertEqual(self.request(host=host)[0],403)
        for origin in ['null','https://invalid',f'https://127.0.0.1:{self.httpd.server_port}']:
            self.assertEqual(self.request(origin=origin)[0],403)
        self.assertEqual(self.request(origin=f'http://127.0.0.1:{self.httpd.server_port}')[0],200)

    def test_mutating_methods_refused_and_assets_unchanged(self):
        before={p:p.read_bytes() for p,_,_ in self.assets.values()}
        for method in ['POST','PUT','PATCH','DELETE','OPTIONS']:
            self.assertEqual(self.request(method=method)[0],501)
        self.assertEqual(before,{p:p.read_bytes() for p in before})

    def test_changed_missing_symlink_assets_refused(self):
        path=self.assets['/control.png'][0]; original=path.read_bytes()
        path.write_bytes(b'changed'); self.assertEqual(self.request('/control.png')[0],409)
        path.unlink(); self.assertEqual(self.request('/control.png')[0],409)
        target=self.root/'same'; target.write_bytes(original); path.symlink_to(target)
        self.assertEqual(self.request('/control.png')[0],409)

    def test_error_headers_and_head_body(self):
        for target,method in [('/missing','GET'),('/missing','HEAD'),('/','POST')]:
            status,headers,body=self.request(target,method)
            self.assertIn(status,(404,501)); self.assertEqual(headers['Cache-Control'],'no-store')
            self.assertIn("default-src 'none'",headers['Content-Security-Policy'])
            if method=='HEAD': self.assertEqual(body,b'')


class EntrypointControls(unittest.TestCase):
    def test_loopback_binding_and_close(self):
        fake=MagicMock(); fake.server_port=12345; fake.serve_forever.side_effect=KeyboardInterrupt
        assets={'/':(Path('fake'),'0'*64,'text/html'),'/coordinate.mjs':(Path('fake'),'1'*64,'text/javascript')}
        with patch.object(SERVER,'routes',return_value=assets), patch.object(SERVER,'ThreadingHTTPServer',return_value=fake) as factory, patch('sys.argv',['serve_review.py','--port','0']), contextlib.redirect_stdout(io.StringIO()): SERVER.main()
        self.assertEqual(factory.call_args.args[0],('127.0.0.1',0)); fake.server_close.assert_called_once()

    def test_invalid_port_stops_before_asset_reads(self):
        for port in ['-1','65536']:
            with patch.object(SERVER,'routes') as routes, patch('sys.argv',['serve_review.py','--port',port]), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught: SERVER.main()
                self.assertEqual(caught.exception.code,2); routes.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)

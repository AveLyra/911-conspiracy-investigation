import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
import build_diagnostic as b
import serve_diagnostic as s


class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='fit-diagnostic-synthetic-', dir='/private/tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.local = self.root / 'local'; self.here = self.local / 'diagnostic'
        self.r1 = self.root / 'r1'
        for path in [self.local / 'packet02', self.here, self.r1 / 'localization-control']:
            path.mkdir(parents=True, exist_ok=True)
        self.originals = {k: (b'<html><body>synthetic</body></html>' if k == 'review.html'
                             else ('// synthetic '+k).encode()) for k in b.ORIGINALS}
        for name, data in self.originals.items(): (self.local / 'packet02' / name).write_bytes(data)
        self.control = b'synthetic fixture bytes; not a historical image'
        (self.r1 / 'localization-control/fixture.png').write_bytes(self.control)
        (self.r1 / 'serve_review.py').write_bytes(b'# synthetic handler pin only\n')
        manifest = {'products': {k:b.identity(v) for k,v in self.originals.items()},
                    'assets': {'control': {'synthetic':True,'width':1280,'height':720,
                        'url':'/control.png','mode':'RGB',**b.identity(self.control)}}}
        raw = b.json_bytes(manifest); (self.local/'packet02/manifest.json').write_bytes(raw)
        (self.here/'PROTOCOL.md').write_bytes(b'synthetic protocol')
        for name in ['diagnostics.mjs','build_diagnostic.py','serve_diagnostic.py',
                     'test_diagnostic.py','test_diagnostics.mjs']:
            (self.here/name).write_bytes(('synthetic '+name).encode())
        self.kw = dict(local=self.local,here=self.here,r1=self.r1,
            originals={k:b.identity(v)['sha256'] for k,v in self.originals.items()},
            original_sha=b.identity(raw)['sha256'],
            protocol_sha=b.identity(b'synthetic protocol')['sha256'],
            handler_sha=b.identity(b'# synthetic handler pin only\n')['sha256'],
            control_sha=b.identity(self.control)['sha256'])

    def prepare(self): return b.expected_packet(**self.kw)

    def test_exact_derivative_and_repeated_builds(self):
        m1=b.build('packet01',self.here,self.prepare);m2=b.build('packet02',self.here,self.prepare)
        self.assertEqual(m1,m2)
        self.assertEqual(b.check_packet(self.here/'packet01',self.prepare),m1)
        for name in m1['products']:
            self.assertEqual((self.here/'packet01'/name).read_bytes(),(self.here/'packet02'/name).read_bytes())
        html=(self.here/'packet01/review.html').read_bytes()
        self.assertEqual(html.replace(b.TAG,b''),self.originals['review.html'])
        for name in set(self.originals)-{'review.html'}:
            self.assertEqual((self.here/'packet01'/name).read_bytes(),self.originals[name])
        self.assertEqual(set(m1['routes']),b.ROUTES);self.assertEqual(len(b.ROUTES),7)
        self.assertFalse(m1['historical_measurement'])

    def test_wrong_pin_refuses_before_output(self):
        self.kw['protocol_sha']='0'*64
        with self.assertRaises(ValueError): b.build('packet01',self.here,self.prepare)
        self.assertFalse((self.here/'packet01').exists())

    def test_changed_manifest_product_rejected(self):
        self.kw['originals']['assets.mjs']='0'*64
        with self.assertRaises(ValueError): self.prepare()

    def test_existing_and_unsafe_outputs_rejected(self):
        b.build('packet01',self.here,self.prepare)
        for name in ['packet01','../packet03','/packet03','packet1','packet03/other','']:
            with self.assertRaises(ValueError): b.build(name,self.here,self.prepare)

    def test_symlink_input_and_output_refused(self):
        target=self.here/'target';target.write_bytes(b'x')
        link=self.here/'link';link.symlink_to(target)
        with self.assertRaises(ValueError): b.read(link)
        (self.here/'packet09').symlink_to(self.here/'missing')
        with self.assertRaises(ValueError): b.build('packet09',self.here,self.prepare)

    def test_tampered_and_extra_products_refused(self):
        b.build('packet01',self.here,self.prepare)
        p=self.here/'packet01/review.mjs';p.write_bytes(b'changed')
        with self.assertRaises(ValueError): b.check_packet(self.here/'packet01',self.prepare)
        b.build('packet02',self.here,self.prepare)
        (self.here/'packet02/extra').write_bytes(b'extra')
        with self.assertRaises(ValueError): b.check_packet(self.here/'packet02',self.prepare)

    def test_midbuild_input_change_preserves_failed_output(self):
        calls=0
        def changing():
            nonlocal calls
            calls+=1
            if calls==2:(self.here/'diagnostics.mjs').write_bytes(b'changed')
            return self.prepare()
        with self.assertRaises(ValueError):b.build('packet01',self.here,changing)
        self.assertTrue((self.here/'packet01/manifest.json').is_file())

    def test_html_injection_requires_exact_single_boundary(self):
        for html in [b'no body',b'</body></body>',b'diagnostics.mjs</body>']:
            with self.assertRaises(ValueError):b.inject(html)

    def test_route_scope_and_wrong_source_refused(self):
        m=b.build('packet01',self.here,self.prepare);packet=self.here/'packet01'
        control=self.r1/'localization-control/fixture.png'
        self.assertEqual(set(s.route_map(m,packet,control)),b.ROUTES)
        for change in ['extra','missing','traversal','historical']:
            bad=copy.deepcopy(m)
            if change=='extra':bad['routes']['/frames/274.png']={}
            if change=='missing':del bad['routes']['/control.png']
            if change=='traversal':bad['routes']['/']['path']='../review.html'
            if change=='historical':bad['routes']['/control.png']['path']='/historical.png'
            with self.assertRaises(ValueError):s.route_map(bad,packet,control)

    def test_unchanged_handler_refusals_without_listening_server(self):
        # Load only the actual hash-checked handler factory. Its routes() is never called.
        factory=s.load_handler()
        p=self.here/'fixture';p.write_bytes(b'synthetic')
        handler=factory({'/control.png':(p,b.identity(b'synthetic')['sha256'],'image/png')})
        def request(path,host='127.0.0.1:12345',origin=None,head=False):
            obj=handler.__new__(handler)
            obj.server=types.SimpleNamespace(server_port=12345)
            obj.headers={'Host':host}
            if origin is not None:obj.headers['Origin']=origin
            obj.path=path;obj.wfile=io.BytesIO();obj.result=None
            obj.send_error=lambda code,*args:setattr(obj,'result',code)
            obj.send_response=lambda code:setattr(obj,'result',code)
            obj.send_header=lambda *args:None;obj.end_headers=lambda:None
            obj.respond(head)
            return obj.result,obj.wfile.getvalue()
        self.assertEqual(request('/control.png'),(200,b'synthetic'))
        self.assertEqual(request('/control.png',head=True),(200,b''))
        for path in ['/frames/274.png','/manifest.json','/','/../control.png','/control.png?x']:
            self.assertEqual(request(path)[0],404)
        self.assertEqual(request('/control.png',host='other')[0],403)
        self.assertEqual(request('/control.png',origin='http://other')[0],403)
        p.write_bytes(b'changed');self.assertEqual(request('/control.png')[0],409)
        self.assertFalse(hasattr(handler,'do_POST'))


if __name__=='__main__':unittest.main(verbosity=2)

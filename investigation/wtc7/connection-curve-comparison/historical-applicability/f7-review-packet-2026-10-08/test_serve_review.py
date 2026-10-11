"""Synthetic allowlist/HTTP checks; no historical images or server are opened."""
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import json
import unittest
import render_packet as render
import serve_review as server
from test_render_packet import encoded,fixture_packet


class SyntheticRoutes(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(prefix="f7-viewer-http-");self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.here=self.root/"viewer";self.base=self.root/"base"
        self.here.mkdir();self.base.mkdir();self.data=fixture_packet()
        for name,asset in self.data["assets"].items():
            path=self.base/asset["path"];path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(("TEST ONLY source "+name).encode())
        self.control=self.root/"control.png";self.control.write_bytes(b"TEST ONLY control")
        self.control_sha=render.sha(self.control.read_bytes())
        raw=encoded(self.data);self.digest=render.sha(raw)
        for name in ("packet01.json","packet02.json"):(self.here/name).write_bytes(raw)
        self.module=render.presentation_bytes(self.data,self.digest)
        for name in ("viewer-data01.mjs","viewer-data02.mjs"):(self.here/name).write_bytes(self.module)
        (self.here/"review.html").write_bytes(b"<!doctype html><p>TEST ONLY</p>")
        (self.here/"review.mjs").write_bytes(b"export const syntheticOnly=true;")
        self.factory=server.handler()  # Reuses only pinned old handler code, not its routes.

    def routes(self):
        return server.routes_for(self.here,self.base,self.control,self.digest,self.control_sha)

    def test_exact_seventeen_routes_and_identity_bound_data(self):
        assets=self.routes()
        expected={"/","/review.mjs","/viewer-data.mjs","/page.png","/control.png"}|{f"/source/Im{i}.jpg" for i in range(12)}
        self.assertEqual(set(assets),expected)
        raw=assets["/viewer-data.mjs"][0].read_bytes()
        self.assertIn(render.PACKET_ID.encode(),raw)
        self.assertIn(self.digest.encode(),raw)
        self.assertIn(b'"version":2',raw)
        self.assertNotIn(b'"path":',raw)

    def test_changed_packet_source_control_or_presentation_refused(self):
        paths=[self.here/"packet01.json",self.here/"packet02.json",self.control,
               self.base/"native-strips01/Im0.jpg",self.here/"viewer-data01.mjs",
               self.here/"viewer-data02.mjs"]
        for path in paths:
            with self.subTest(name=path.name):
                before=path.read_bytes();path.write_bytes(before+b" changed")
                with self.assertRaises(ValueError):self.routes()
                path.write_bytes(before)

    def test_leaf_symlinks_refused(self):
        for path in [self.here/"review.html",self.here/"review.mjs",self.here/"viewer-data01.mjs",
                     self.here/"packet01.json",self.base/"native-strips01/Im0.jpg",self.control]:
            with self.subTest(name=path.name):
                target=path.with_name(path.name+".synthetic-original");path.rename(target);path.symlink_to(target)
                with self.assertRaisesRegex(ValueError,"symlink"):self.routes()
                path.unlink();target.rename(path)


class SyntheticHTTP(SyntheticRoutes):
    def setUp(self):
        super().setUp();self.assets=self.routes()
        self.httpd=ThreadingHTTPServer(("127.0.0.1",0),self.factory(self.assets))
        self.thread=Thread(target=self.httpd.serve_forever,kwargs={"poll_interval":.01},daemon=True);self.thread.start()
        self.addCleanup(self.close)
        self.authority=f"127.0.0.1:{self.httpd.server_port}"

    def close(self):
        self.httpd.shutdown();self.httpd.server_close();self.thread.join(timeout=2)
        self.assertFalse(self.thread.is_alive())

    def request(self,path,method="GET",headers=None,body=None):
        connection=HTTPConnection("127.0.0.1",self.httpd.server_port,timeout=3)
        try:
            connection.request(method,path,headers=headers or {},body=body)
            response=connection.getresponse();return response.status,dict(response.getheaders()),response.read()
        finally:connection.close()

    def policy(self,headers):
        self.assertEqual(headers["Cache-Control"],"no-store")
        self.assertEqual(headers["X-Content-Type-Options"],"nosniff")
        self.assertEqual(headers["Referrer-Policy"],"no-referrer")
        self.assertEqual(headers["Cross-Origin-Resource-Policy"],"same-origin")
        for clause in ("default-src 'none'","connect-src 'none'","form-action 'none'","base-uri 'none'","frame-ancestors 'none'"):
            self.assertIn(clause,headers["Content-Security-Policy"])

    def test_each_route_get_head_and_headers(self):
        for url,(path,_,mime) in self.assets.items():
            for method in ("GET","HEAD"):
                with self.subTest(url=url,method=method):
                    status,headers,body=self.request(url,method)
                    self.assertEqual(status,200);self.policy(headers)
                    self.assertEqual(headers["Content-Type"],mime)
                    self.assertEqual(int(headers["Content-Length"]),len(path.read_bytes()))
                    self.assertEqual(body,path.read_bytes() if method=="GET" else b"")

    def test_host_origin_and_unlisted_paths_refused(self):
        for headers in ({"Host":"example.test"},{"Host":"localhost:"+str(self.httpd.server_port)},{"Host":"127.0.0.1:1"},{"Origin":"null"},{"Origin":"https://"+self.authority}):
            self.assertEqual(self.request("/",headers=headers)[0],403)
        self.assertEqual(self.request("/",headers={"Origin":"http://"+self.authority})[0],200)
        for path in ("/?","/#","/../review.html","/%2e%2e/review.html","/source/../review.mjs",
                     "/packet01.json","/packet02.json","/serve_review.py","/viewer-data01.mjs","/review.html","/unknown",
                     "http://"+self.authority+"/"):
            with self.subTest(path=path):self.assertEqual(self.request(path)[0],404)

    def test_writes_refused_without_file_changes(self):
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        for method in ("POST","PUT","PATCH","DELETE","OPTIONS"):
            status,headers,_=self.request("/",method,body=b"TEST ONLY")
            self.assertEqual(status,501);self.policy(headers)
        after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before,after)

    def test_every_asset_hash_checked_for_each_request(self):
        for url,(path,_,_) in self.assets.items():
            with self.subTest(url=url):
                before=path.read_bytes();path.write_bytes(before+b"MUTATED SYNTHETIC")
                for method in ("GET","HEAD"):
                    status,headers,body=self.request(url,method)
                    self.assertEqual(status,409);self.policy(headers);self.assertNotIn(b"MUTATED SYNTHETIC",body)
                path.write_bytes(before)

    def test_deleted_or_symlink_asset_refused(self):
        path=self.here/"review.mjs";before=path.read_bytes();path.unlink()
        self.assertEqual(self.request("/review.mjs")[0],409)
        target=self.here/"synthetic-target";target.write_bytes(before);path.symlink_to(target)
        self.assertEqual(self.request("/review.mjs")[0],409)

    def test_parent_symlink_shared_handler_limit(self):
        original=self.base/"native-strips01";target=self.root/"relocated-synthetic"
        original.rename(target);original.symlink_to(target,target_is_directory=True)
        self.assertEqual(self.request("/source/Im0.jpg")[0],200)
        (target/"Im0.jpg").write_bytes(b"changed synthetic")
        self.assertEqual(self.request("/source/Im0.jpg")[0],409)


if __name__=="__main__":
    unittest.main()


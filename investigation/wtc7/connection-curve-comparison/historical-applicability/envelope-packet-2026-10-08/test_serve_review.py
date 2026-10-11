"""Independent server checks with temporary bytes, never changed packet assets.

All HTTP data and mutations use temporary synthetic fixtures. The one real
route check reads the allowlist only; no test records a human response.
"""
import copy
import hashlib
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from unittest.mock import patch

import serve_review as server


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


class TemporaryPacket(unittest.TestCase):
    def setUp(self):
        helper = (server.R1 / "serve_review.py").read_bytes()
        self.assertEqual(digest(helper), server.HELPER_SHA)
        directory = TemporaryDirectory(prefix="envelope-server-test-")
        self.addCleanup(directory.cleanup)
        self.temp = Path(directory.name)
        self.base = self.temp / "curve"
        self.here = self.base / "historical-applicability" / "envelope-packet"
        self.r1 = self.temp / "comparator"
        self.here.mkdir(parents=True)
        self.r1.mkdir()
        (self.r1 / "serve_review.py").write_bytes(helper)
        control = self.r1 / "localization-control" / "fixture.png"
        control.parent.mkdir()
        control.write_bytes(b"TEST ONLY synthetic control bytes\x00")
        page = self.base / "render" / "page.png"
        page.parent.mkdir()
        page.write_bytes(b"TEST ONLY synthetic page bytes\x01")
        strip = self.base / "native" / "Im0.jpg"
        strip.parent.mkdir()
        strip.write_bytes(b"TEST ONLY synthetic strip bytes\x02")
        self.data = {
            "status": "test-only-unaccepted", "slots": [], "summary": {"test_only": True},
            "assumptions": ["synthetic fixture"], "domain_kind": "test-only",
            "assets": {
                "page": {"path": "render/page.png", "url": "/page.png", "sha256": digest(page.read_bytes())},
                "Im0": {"path": "native/Im0.jpg", "url": "/source/Im0.jpg", "sha256": digest(strip.read_bytes())},
            },
        }
        raw = encoded(self.data)
        for name in ("packet01.json", "packet02.json"):
            (self.here / name).write_bytes(raw)
        presentation = copy.deepcopy(self.data)
        for asset in presentation["assets"].values():
            del asset["path"]
        presentation["packet_sha256"] = digest(raw)
        script = b"export const PACKET = " + encoded(presentation) + b";\n"
        for name in ("viewer-data01.mjs", "viewer-data02.mjs"):
            (self.here / name).write_bytes(script)
        (self.here / "review.html").write_bytes(b"<!doctype html><p>TEST ONLY</p>\n")
        (self.here / "review.mjs").write_bytes(b"export const testOnly = true;\n")
        patcher = patch.multiple(server, HERE=self.here, BASE=self.base, R1=self.r1,
                                 PACKET_SHA=digest(raw), CONTROL_SHA=digest(control.read_bytes()))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.httpd = None

    def start_server(self):
        self.assets = server.routes()
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.handler()(self.assets))
        self.thread = Thread(target=self.httpd.serve_forever,
                             kwargs={"poll_interval": 0.01}, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)
        self.authority = f"127.0.0.1:{self.httpd.server_port}"
        self.assertEqual(self.httpd.server_address[0], "127.0.0.1")

    def stop_server(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        self.assertFalse(self.thread.is_alive())

    def request(self, target, method="GET", headers=None, body=None):
        connection = HTTPConnection("127.0.0.1", self.httpd.server_port, timeout=3)
        try:
            connection.request(method, target, headers={} if headers is None else headers, body=body)
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            connection.close()

    def replace_with_symlink(self, path):
        # Only paths inside this test's freshly generated temporary directory.
        self.assertTrue(path.is_relative_to(self.temp))
        target = path.with_name(path.name + ".test-only-original")
        path.rename(target)
        path.symlink_to(target)

    def assert_policy(self, headers):
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(headers["Referrer-Policy"], "no-referrer")
        self.assertEqual(headers["Cross-Origin-Resource-Policy"], "same-origin")
        for clause in ("default-src 'none'", "connect-src 'none'", "frame-ancestors 'none'",
                       "form-action 'none'", "base-uri 'none'"):
            self.assertIn(clause, headers["Content-Security-Policy"])


class RouteConstructionTests(TemporaryPacket):
    def test_fixed_routes_and_payload_without_filesystem_paths(self):
        assets = server.routes()
        self.assertEqual(set(assets), {"/", "/review.mjs", "/viewer-data.mjs",
                                      "/page.png", "/source/Im0.jpg", "/control.png"})
        self.assertNotIn(b'"path":', assets["/viewer-data.mjs"][0].read_bytes())
        self.assertEqual(assets["/page.png"][2], "image/png")
        self.assertEqual(assets["/source/Im0.jpg"][2], "image/jpeg")
        for path, expected, _ in assets.values():
            self.assertEqual(digest(path.read_bytes()), expected)

    def test_packet_and_repeat_hash_mismatch_rejected(self):
        for filename in ("packet01.json", "packet02.json"):
            with self.subTest(filename=filename):
                path = self.here / filename
                raw = path.read_bytes()
                path.write_bytes(raw + b" ")
                with self.assertRaisesRegex(ValueError, "asset identity mismatch"):
                    server.routes()
                path.write_bytes(raw)

    def test_image_and_control_hash_mismatch_rejected(self):
        for path in (self.base / "render/page.png", self.base / "native/Im0.jpg",
                     self.r1 / "localization-control/fixture.png"):
            with self.subTest(path=path.name):
                raw = path.read_bytes()
                path.write_bytes(raw + b"changed")
                with self.assertRaisesRegex(ValueError, "asset identity mismatch"):
                    server.routes()
                path.write_bytes(raw)

    def test_duplicate_presentation_mismatch_rejected(self):
        (self.here / "viewer-data02.mjs").write_bytes(b"different TEST ONLY script")
        with self.assertRaisesRegex(ValueError, "presentation repeat mismatch"):
            server.routes()

    def test_matching_presentations_must_match_packet(self):
        for name in ("viewer-data01.mjs", "viewer-data02.mjs"):
            (self.here / name).write_bytes(b"export const PACKET = {};\n")
        with self.assertRaisesRegex(ValueError, "presentation does not match packet"):
            server.routes()

    def test_leaf_symlinks_rejected_at_route_build(self):
        for path in (self.here / "packet01.json", self.here / "packet02.json",
                     self.base / "render/page.png", self.base / "native/Im0.jpg",
                     self.r1 / "localization-control/fixture.png", self.here / "review.html",
                     self.here / "review.mjs", self.here / "viewer-data01.mjs"):
            with self.subTest(path=path.name):
                self.replace_with_symlink(path)
                with self.assertRaisesRegex(ValueError, "symlink refused"):
                    server.routes()
                target = path.resolve()
                path.unlink()
                target.rename(path)

    def test_helper_hash_and_leaf_symlink_rejected_before_execution(self):
        path = self.r1 / "serve_review.py"
        raw = path.read_bytes()
        path.write_bytes(raw + b"\nraise RuntimeError('MUST NOT EXECUTE')\n")
        with self.assertRaisesRegex(ValueError, "asset identity mismatch"):
            server.handler()
        path.write_bytes(raw)
        self.replace_with_symlink(path)
        with self.assertRaisesRegex(ValueError, "symlink refused"):
            server.handler()


class RequestTests(TemporaryPacket):
    def setUp(self):
        super().setUp()
        self.start_server()

    def test_get_and_head_exact_bytes_mime_length_and_restrictive_headers(self):
        for url, (path, _, mime) in self.assets.items():
            for method in ("GET", "HEAD"):
                with self.subTest(url=url, method=method):
                    status, headers, body = self.request(url, method)
                    self.assertEqual(status, 200)
                    self.assertEqual(headers["Content-Type"], mime)
                    self.assertEqual(int(headers["Content-Length"]), len(path.read_bytes()))
                    self.assertEqual(body, path.read_bytes() if method == "GET" else b"")
                    self.assert_policy(headers)

    def test_same_origin_request_allowed(self):
        self.assertEqual(self.request("/", headers={"Origin": "http://" + self.authority})[0], 200)

    def test_foreign_host_or_origin_refused(self):
        variants = [{"Host": "example.test"}, {"Host": "localhost:" + str(self.httpd.server_port)},
                    {"Host": "127.0.0.1:1"}, {"Host": "127.0.0.1"},
                    {"Origin": "http://example.test"}, {"Origin": "null"},
                    {"Origin": "https://" + self.authority},
                    {"Origin": "http://" + self.authority + "/"}]
        for headers in variants:
            for method in ("GET", "HEAD"):
                with self.subTest(headers=headers, method=method):
                    status, response_headers, body = self.request("/", method, headers)
                    self.assertEqual(status, 403)
                    self.assert_policy(response_headers)
                    self.assertNotIn(b"<p>TEST ONLY</p>", body)
                    if method == "HEAD":
                        self.assertEqual(body, b"")

    def test_query_fragment_traversal_unknown_and_unlisted_files_refused(self):
        (self.here / "unlisted-secret.txt").write_bytes(b"TEST ONLY DO NOT SERVE")
        targets = ("/?query=1", "/?", "/#fragment", "/#", "/../review.html",
                   "/%2e%2e/review.html", "/source/../review.mjs", "/review.mjs%00",
                   "/source/", "/review.html", "/packet01.json", "/packet02.json",
                   "/serve_review.py", "/viewer-data01.mjs", "/unlisted-secret.txt",
                   "/.git/HEAD", "/unknown", "/source/Im1.jpg",
                   str(self.here / "unlisted-secret.txt"))
        for target in targets:
            for method in ("GET", "HEAD"):
                with self.subTest(target=target, method=method):
                    status, headers, body = self.request(target, method)
                    self.assertEqual(status, 404)
                    self.assert_policy(headers)
                    self.assertNotIn(b"TEST ONLY DO NOT SERVE", body)
                    if method == "HEAD":
                        self.assertEqual(body, b"")

    def test_absolute_request_target_refused_even_with_correct_host(self):
        status, _, _ = self.request("http://" + self.authority + "/", headers={"Host": self.authority})
        self.assertEqual(status, 404)

    def test_unsupported_methods_refused_without_writes(self):
        before = {p.relative_to(self.temp): p.read_bytes() for p in self.temp.rglob("*") if p.is_file()}
        for method in ("POST", "PUT", "PATCH", "DELETE", "OPTIONS"):
            status, headers, body = self.request("/", method, body=b"TEST ONLY NOT A HUMAN RESPONSE")
            self.assertEqual(status, 501)  # BaseHTTPRequestHandler's explicit unsupported-method response.
            self.assert_policy(headers)
            self.assertNotIn(b"<p>TEST ONLY</p>", body)
        after = {p.relative_to(self.temp): p.read_bytes() for p in self.temp.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_changed_asset_refused_on_each_get_and_head(self):
        for url, (path, _, _) in self.assets.items():
            with self.subTest(url=url):
                raw = path.read_bytes()
                self.assertEqual(self.request(url)[0], 200)
                path.write_bytes(raw + b"TEST ONLY MUTATION")
                for method in ("GET", "HEAD"):
                    status, headers, body = self.request(url, method)
                    self.assertEqual(status, 409)
                    self.assert_policy(headers)
                    self.assertNotIn(b"TEST ONLY MUTATION", body)
                path.write_bytes(raw)
                self.assertEqual(self.request(url)[0], 200)

    def test_deleted_or_direct_symlink_asset_refused_after_start(self):
        for kind in ("deleted", "symlink"):
            path = self.assets["/review.mjs"][0]
            raw = path.read_bytes()
            if kind == "deleted":
                path.unlink()
            else:
                self.replace_with_symlink(path)
            for method in ("GET", "HEAD"):
                self.assertEqual(self.request("/review.mjs", method)[0], 409)
            if kind == "symlink":
                path.unlink()
            path.write_bytes(raw)

    def test_parent_symlink_is_not_rejected_but_cannot_bypass_hash(self):
        # Characterize the preserved helper's limit honestly: only the leaf
        # is tested for symlinks. Parent redirects still cannot change bytes.
        original = self.base / "native"
        target = self.temp / "test-only-relocated-native"
        original.rename(target)
        original.symlink_to(target, target_is_directory=True)
        self.assertEqual(self.request("/source/Im0.jpg")[0], 200)
        (target / "Im0.jpg").write_bytes(b"TEST ONLY REDIRECTED DIFFERENT BYTES")
        self.assertEqual(self.request("/source/Im0.jpg")[0], 409)


class RealAllowlistReadOnlyTest(unittest.TestCase):
    def test_real_allowlist_has_only_seventeen_declared_assets(self):
        expected = {"/", "/review.mjs", "/viewer-data.mjs", "/page.png", "/control.png"}
        expected.update(f"/source/Im{i}.jpg" for i in range(12))
        self.assertEqual(set(server.routes()), expected)


if __name__ == "__main__":
    unittest.main()

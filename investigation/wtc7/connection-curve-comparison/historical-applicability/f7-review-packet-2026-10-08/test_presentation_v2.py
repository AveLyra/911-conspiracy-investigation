"""Finite synthetic repair-binding tests; no historical packet/source execution."""
import copy
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
import render_packet_v2 as render
import serve_review_v2 as server

fixtures = render.load_pinned(render.HERE / "test_render_packet.py",
    "1e78437875333f90f6fe0b4653c00b247e93b15c173f55cddfad777c05ab4127", "preserved_synthetic_fixtures")


class SyntheticRepair(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory(prefix="f7-repaired-viewer-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.here = self.root / "viewer"; self.here.mkdir()
        self.base = self.root / "base"; self.base.mkdir()
        self.candidate = fixtures.fixture_packet()
        self.candidate["inputs"] = {"synthetic-old": {"sha256": "1" * 64, "bytes": 1}}
        self.candidate["inputs_after"] = copy.deepcopy(self.candidate["inputs"])
        self.repair = copy.deepcopy(self.candidate)
        self.repair["inputs"]["synthetic-added"] = {"sha256": "2" * 64, "bytes": 2}
        self.repair["inputs_after"] = copy.deepcopy(self.repair["inputs"])
        self.candidate_sha = render.old.sha(fixtures.encoded(self.candidate))
        self.repair_sha = self.write_repair(self.repair)
        for name in ("packet01.json", "packet02.json"):
            (self.here / name).write_bytes(fixtures.encoded(self.candidate))
        self.expected = self.build()
        for name in ("viewer-data-v2-01.mjs", "viewer-data-v2-02.mjs"):
            (self.here / name).write_bytes(self.expected)
        # Preserve deliberately different old presentation bytes, never routed.
        self.old_presentation = render.old.presentation_bytes(self.candidate, self.candidate_sha)
        for name in ("viewer-data01.mjs", "viewer-data02.mjs"):
            (self.here / name).write_bytes(self.old_presentation)
        for name, asset in self.repair["assets"].items():
            path = self.base / asset["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(("TEST ONLY source " + name).encode())
        for name in ("review.html", "review.mjs"):
            (self.here / name).write_bytes(render.old.pinned(render.HERE / name, render.FIXED[name]))
        self.control = self.root / "control.png"
        self.control.write_bytes(b"TEST ONLY control")
        self.control_sha = render.old.sha(self.control.read_bytes())

    def write_repair(self, data):
        raw = fixtures.encoded(data)
        for name in ("packet-v2-01.json", "packet-v2-02.json"):
            (self.here / name).write_bytes(raw)
        return render.old.sha(raw)

    def build(self):
        return render.build_for(self.here, self.repair_sha, self.candidate_sha)

    def routes(self):
        return server.routes_for(self.here, self.base, self.control, self.repair_sha,
                                 self.candidate_sha, self.control_sha)

    def test_projection_changes_full_hash_only_and_inputs_untouched(self):
        before = {p.name: p.read_bytes() for p in self.here.glob("*.json")}
        self.assertEqual(self.build(), self.expected)
        new = json.loads(self.expected[22:-2]); old = json.loads(self.old_presentation[22:-2])
        self.assertEqual(new.pop("packet_sha256"), self.repair_sha)
        self.assertEqual(old.pop("packet_sha256"), self.candidate_sha)
        self.assertEqual(new, old)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.here.glob("*.json")})

    def test_candidate_cannot_fill_repaired_filename_or_digest(self):
        for name in ("packet-v2-01.json", "packet-v2-02.json"):
            path = self.here / name; saved = path.read_bytes()
            path.write_bytes(fixtures.encoded(self.candidate))
            with self.assertRaises(ValueError): self.build()
            path.write_bytes(saved)
        with self.assertRaisesRegex(ValueError, "candidate identity"):
            render.build_for(self.here, self.candidate_sha, self.candidate_sha)
        with self.assertRaises(ValueError):
            render.build_for(self.here, self.candidate_sha, self.repair_sha)

    def test_only_explicit_new_packet_filenames(self):
        (self.here / "packet-v2-01.json").unlink()
        with self.assertRaises(FileNotFoundError): self.build()
        self.assertTrue((self.here / "packet01.json").exists())

    def test_no_scientific_change_or_acceptance_contamination(self):
        for key, value in (("version", 1), ("human_accepted", True), ("summary", {"changed": True})):
            bad = copy.deepcopy(self.repair); bad[key] = value
            self.repair_sha = self.write_repair(bad)
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "scientific payload"):
                self.build()

    def test_pin_extension_preserves_old_map_and_after(self):
        variants = [copy.deepcopy(self.repair) for _ in range(3)]
        variants[0]["inputs_after"] = {}
        variants[1]["inputs"]["synthetic-old"]["bytes"] = 99
        variants[1]["inputs_after"] = copy.deepcopy(variants[1]["inputs"])
        variants[2]["inputs"] = {}; variants[2]["inputs_after"] = {}
        for bad in variants:
            self.repair_sha = self.write_repair(bad)
            with self.assertRaisesRegex(ValueError, "extend pins"): self.build()

    def test_duplicate_nonfinite_and_nonfrozen_input_refused(self):
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}'):
            for name in ("packet-v2-01.json", "packet-v2-02.json"):
                (self.here / name).write_bytes(raw)
            with self.assertRaises(ValueError): render.load_pair(self.here, render.old.sha(raw))
        with self.assertRaisesRegex(ValueError, "not frozen"): render.load_pair(self.here, "PENDING")

    def test_helper_pin_precedes_execution_and_refuses_symlink(self):
        path = self.root / "helper.py"; path.write_bytes(b'raise RuntimeError("must not run")')
        with self.assertRaisesRegex(ValueError, "helper identity"):
            render.load_pinned(path, "0" * 64, "synthetic_bad_helper")
        link = self.root / "link.py"; link.symlink_to(path)
        with self.assertRaisesRegex(ValueError, "symlink"):
            render.load_pinned(link, render.old.sha(path.read_bytes()), "synthetic_link")

    def test_exclusive_output_retains_prior(self):
        path = self.root / "exclusive.mjs"
        render.old.save_exclusive(path, self.expected)
        with self.assertRaises(FileExistsError): render.old.save_exclusive(path, b"wrong")
        self.assertEqual(path.read_bytes(), self.expected)

    def test_exact_routes_bind_repair_and_unchanged_ui(self):
        routes = self.routes()
        self.assertEqual(set(routes), {"/", "/review.mjs", "/viewer-data.mjs", "/page.png", "/control.png"}
                         | {f"/source/Im{i}.jpg" for i in range(12)})
        self.assertEqual(routes["/viewer-data.mjs"][0].name, "viewer-data-v2-01.mjs")
        self.assertEqual(routes["/viewer-data.mjs"][0].read_bytes(), self.expected)
        self.assertEqual(routes["/"][1], render.FIXED["review.html"])
        self.assertEqual(routes["/review.mjs"][1], render.FIXED["review.mjs"])
        for name in ("viewer-data01.mjs", "viewer-data02.mjs"):
            self.assertEqual((self.here / name).read_bytes(), self.old_presentation)

    def test_candidate_presentation_and_source_mutation_refused(self):
        for name in ("viewer-data-v2-01.mjs", "viewer-data-v2-02.mjs"):
            path = self.here / name; path.write_bytes(self.old_presentation)
            with self.assertRaises(ValueError): self.routes()
            path.write_bytes(self.expected)
        path = self.base / "native-strips01/Im11.jpg"
        path.write_bytes(path.read_bytes() + b"changed")
        with self.assertRaises(ValueError): self.routes()

    def test_copied_notes_include_repaired_full_identity(self):
        code = ("import * as review from " + json.dumps((render.HERE / "review.mjs").as_uri()) + ";"
                "import {readFileSync} from 'node:fs';"
                "const p=JSON.parse(readFileSync(0,'utf8'));review.validatePacket(p);"
                "process.stdout.write(review.formatResponses(p.slots,{},p));")
        result = subprocess.run(["node", "--input-type=module", "-e", code],
                                input=self.expected[22:-2], capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        text = result.stdout.decode()
        self.assertIn(self.repair_sha, text); self.assertNotIn(self.candidate_sha, text)
        self.assertEqual(text.splitlines()[:3], ["Conditional packet ID\t" + render.PACKET_ID,
                         "Conditional packet version\t2", "Conditional packet SHA256\t" + self.repair_sha])
        self.assertEqual(text.count("\tuninspected\t"), 84)

    def test_reused_handler_all_routes_integrity_and_readonly_policy(self):
        assets = self.routes()
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.handler()(assets))
        thread = Thread(target=httpd.serve_forever, kwargs={"poll_interval": .01}, daemon=True)
        thread.start()
        def request(url, method="GET", headers=None):
            connection = HTTPConnection("127.0.0.1", httpd.server_port, timeout=3)
            try:
                connection.request(method, url, headers=headers or {})
                response = connection.getresponse()
                return response.status, dict(response.getheaders()), response.read()
            finally: connection.close()
        try:
            for url, (path, _, mime) in assets.items():
                saved = path.read_bytes()
                for method in ("GET", "HEAD"):
                    status, headers, body = request(url, method)
                    self.assertEqual(status, 200); self.assertEqual(headers["Content-Type"], mime)
                    self.assertEqual(headers["Cache-Control"], "no-store")
                    self.assertIn("connect-src 'none'", headers["Content-Security-Policy"])
                    self.assertEqual(body, saved if method == "GET" else b"")
                path.write_bytes(saved + b"SYNTHETIC MUTATION")
                self.assertEqual(request(url)[0], 409)
                path.write_bytes(saved)
            for url in ("/packet-v2-01.json", "/packet01.json", "/viewer-data-v2-01.mjs", "/viewer-data01.mjs", "/../review.html", "/?x=1"):
                self.assertEqual(request(url)[0], 404)
            for method in ("POST", "PUT", "PATCH", "DELETE", "OPTIONS"):
                self.assertEqual(request("/", method)[0], 501)
            self.assertEqual(request("/", headers={"Host": "example.test"})[0], 403)
            self.assertEqual(request("/", headers={"Origin": "null"})[0], 403)
        finally:
            httpd.shutdown(); httpd.server_close(); thread.join(timeout=2)
            self.assertFalse(thread.is_alive())


if __name__ == "__main__":
    unittest.main()

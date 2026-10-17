import json
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.request
from audit_access import ReportLinks, SecureRedirects, pointer, request


class AccessControls(unittest.TestCase):
    def test_pointer_fields(self):
        raw = b"version https://git-lfs.github.com/spec/v1\noid sha256:" + b"a" * 64 + b"\nsize 123\n"
        parsed = pointer(raw)
        self.assertEqual(parsed["pdf_bytes_as_recorded"], 123)
        self.assertEqual(parsed["literal_pointer"].encode(), raw)

    def test_malformed_pointer_rejected(self):
        for raw in [b"PDF", b"version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 5\n"]:
            with self.assertRaises(ValueError):
                pointer(raw)

    def test_https_redirect_retains_head(self):
        redirected = SecureRedirects().redirect_request(urllib.request.Request("https://example.test/a", method="HEAD"), None, 301, "Moved", {}, "https://example.test/b")
        self.assertEqual(redirected.get_method(), "HEAD")

    def test_http_redirect_rejected(self):
        with self.assertRaises(ValueError):
            SecureRedirects().redirect_request(urllib.request.Request("https://example.test/a", method="HEAD"), None, 301, "Moved", {}, "http://example.test/b")

    def test_head_does_not_read_body(self):
        class Response:
            status = 200
            url = "https://example.test/report.pdf"
            headers = {"Content-Length": "123", "Content-Type": "application/pdf"}
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, *args): raise AssertionError("HEAD body must not be read")
        class Opener:
            def open(self, req, timeout):
                assert req.get_method() == "HEAD"
                return Response()
        with patch("urllib.request.build_opener", return_value=Opener()):
            got = request("https://example.test/report.pdf", "HEAD")
        self.assertNotIn("failure", got)
        self.assertFalse(got["pdf_body_acquired"])

    def test_only_selected_links(self):
        parser = ReportLinks()
        parser.feed('<a href="/private-contact">Contact</a><a href="/r">Download <b>Final Report</b></a>')
        self.assertEqual(parser.links, [{"label": "Download Final Report", "href": "/r"}])

    def test_saved_pin_and_header_relationship(self):
        saved = json.loads((Path(__file__).parent / "observations.json").read_text())
        pins = [row["pointer"] for row in saved["preserved_pdf_pins"]]
        self.assertNotEqual(pins[0]["pdf_sha256_as_recorded"], pins[1]["pdf_sha256_as_recorded"])
        self.assertEqual(pins[0]["pdf_bytes_as_recorded"] - pins[1]["pdf_bytes_as_recorded"], 2299)
        for pin, response in zip(pins, saved["public_requests"][1:]):
            self.assertEqual(response["method"], "HEAD")
            self.assertEqual(response["status"], 200)
            self.assertFalse(response["pdf_body_acquired"])
            self.assertEqual(int(response["headers"]["Content-Length"]), pin["pdf_bytes_as_recorded"])


if __name__ == "__main__":
    unittest.main()

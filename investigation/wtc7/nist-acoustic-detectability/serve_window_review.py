#!/usr/bin/env python3
"""Loopback-only preview that serves the review page and its three pinned stills."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse

HERE = Path(__file__).resolve().parent
INVESTIGATION = HERE.parent
ASSETS = {
    "/": (HERE / "window-state-review.html", "text/html; charset=utf-8"),
    "/window-state-review.html": (HERE / "window-state-review.html", "text/html; charset=utf-8"),
    "/images/141.jpg": (INVESTIGATION / "fire-coverage-batch3/assets/run01/images/A-a80015cf23e0.jpg", "image/jpeg"),
    "/images/142.jpg": (INVESTIGATION / "fire-coverage-batch3/assets/run01/images/A-7c7cc22dc34c.jpg", "image/jpeg"),
    "/images/143.jpg": (INVESTIGATION / "fire-coverage-batch3/assets/run01/images/A-60c26b7f3416.jpg", "image/jpeg"),
    "/fire-coverage-batch3/assets/run01/images/A-a80015cf23e0.jpg": (INVESTIGATION / "fire-coverage-batch3/assets/run01/images/A-a80015cf23e0.jpg", "image/jpeg"),
    "/fire-coverage-batch3/assets/run01/images/A-7c7cc22dc34c.jpg": (INVESTIGATION / "fire-coverage-batch3/assets/run01/images/A-7c7cc22dc34c.jpg", "image/jpeg"),
    "/fire-coverage-batch3/assets/run01/images/A-60c26b7f3416.jpg": (INVESTIGATION / "fire-coverage-batch3/assets/run01/images/A-60c26b7f3416.jpg", "image/jpeg"),
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        target = ASSETS.get(self.path.split("?", 1)[0])
        if target is None:
            self.send_error(404)
            return
        path, content_type = target
        try:
            content = path.read_bytes()
        except OSError:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, fmt, *args):
        print("window-review", self.address_string(), fmt % args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=49763)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Serving only this review page and its three stills at http://127.0.0.1:{args.port}/")
    server.serve_forever()


if __name__ == "__main__":
    main()

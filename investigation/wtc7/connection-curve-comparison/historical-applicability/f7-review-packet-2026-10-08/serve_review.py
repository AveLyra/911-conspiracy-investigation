"""Versioned read-only loopback wrapper; no imported path globals are patched."""
import argparse
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import types
import render_packet as presentation

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
R1 = BASE.parent / "comparator-r1-replication"
OLD = HERE.parent / "envelope-packet-2026-10-08"
OLD_SERVER_SHA = "6c1913c83a38ff6f1cd5ae1a2c8037f0fa7312a12501ed3d947bf364fd33c541"
CONTROL_SHA = "f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48"


def handler():
    path = OLD / "serve_review.py"
    raw = presentation.pinned(path, OLD_SERVER_SHA)
    module = types.ModuleType("f7_v2_preserved_server")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    # The old module verifies and imports its unchanged R1 handler. Its routes()
    # and historical packet globals are never used or modified.
    return module.handler()


def routes_for(here, base, control_path, packet_sha, control_sha):
    """Explicit fixture arguments for tests; production CLI has no hash override."""
    data, packet_raw = presentation.load_pair(here, packet_sha)
    expected = presentation.presentation_bytes(data, packet_sha)
    assets = {}
    for asset in data["assets"].values():
        path = base / asset["path"]
        raw = presentation.pinned(path, asset["sha256"])
        if len(raw) != asset["bytes"]:
            raise ValueError("source byte count mismatch")
        mime = "image/png" if asset["url"] == "/page.png" else "image/jpeg"
        assets[asset["url"]] = (path, asset["sha256"], mime)
    presentation.pinned(control_path, control_sha)
    assets["/control.png"] = (control_path, control_sha, "image/png")
    script = presentation.pinned(here/"viewer-data01.mjs", presentation.sha(expected))
    if script != presentation.pinned(here/"viewer-data02.mjs", presentation.sha(expected)):
        raise ValueError("presentation repeat mismatch")
    for url, filename, mime in (
        ("/", "review.html", "text/html; charset=utf-8"),
        ("/review.mjs", "review.mjs", "text/javascript; charset=utf-8"),
        ("/viewer-data.mjs", "viewer-data01.mjs", "text/javascript; charset=utf-8"),
    ):
        path = here/filename
        if path.is_symlink():
            raise ValueError("UI symlink refused")
        assets[url] = (path, presentation.sha(path.read_bytes()), mime)
    if presentation.load_pair(here, packet_sha)[1] != packet_raw:
        raise ValueError("packet changed during route preparation")
    return assets


def routes():
    before = presentation.control_pins()
    if presentation.build() != (HERE/"viewer-data01.mjs").read_bytes():
        raise ValueError("presentation does not match frozen packet")
    result = routes_for(HERE, BASE, R1/"localization-control/fixture.png",
                        presentation.PACKET_SHA, CONTROL_SHA)
    if before != presentation.control_pins():
        raise ValueError("controls changed during route preparation")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("invalid port")
    assets = routes()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler()(assets))
    print(json.dumps({"url": f"http://127.0.0.1:{server.server_port}/",
                      "packet_id": presentation.PACKET_ID, "version": 2,
                      "packet_sha256": presentation.PACKET_SHA,
                      "assets": len(assets), "writes": False,
                      "pins": {url: digest for url, (_, digest, _) in assets.items()}}, sort_keys=True), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


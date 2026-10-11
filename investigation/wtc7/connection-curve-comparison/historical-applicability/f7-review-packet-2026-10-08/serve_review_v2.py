"""Explicit repaired-packet routes with the unchanged pinned read-only handler."""
import argparse
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import render_packet_v2 as presentation

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
R1 = BASE.parent / "comparator-r1-replication"
CONTROL_SHA = "f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48"


def handler():
    # The preserved server imports its original renderer; pin both before load.
    presentation.old.pinned(HERE / "render_packet.py", presentation.PRIOR_RENDER_SHA)
    module = presentation.load_pinned(HERE / "serve_review.py", presentation.PRIOR_SERVER_SHA,
                                      "preserved_f7_server")
    result = module.handler()
    presentation.old.pinned(HERE / "render_packet.py", presentation.PRIOR_RENDER_SHA)
    presentation.old.pinned(HERE / "serve_review.py", presentation.PRIOR_SERVER_SHA)
    return result


def routes_for(here, base, control_path, packet_sha, candidate_sha, control_sha):
    """Fixture parameters only; real routes bind fixed new filenames and hashes."""
    old = presentation.old
    expected = presentation.build_for(here, packet_sha, candidate_sha)
    data, original = presentation.load_pair(here, packet_sha)
    routes = {}
    for asset in data["assets"].values():
        path = base / asset["path"]
        raw = old.pinned(path, asset["sha256"])
        if len(raw) != asset["bytes"]:
            raise ValueError("source byte count mismatch")
        mime = "image/png" if asset["url"] == "/page.png" else "image/jpeg"
        routes[asset["url"]] = (path, asset["sha256"], mime)
    old.pinned(control_path, control_sha)
    routes["/control.png"] = (control_path, control_sha, "image/png")
    for name in ("viewer-data-v2-01.mjs", "viewer-data-v2-02.mjs"):
        if old.pinned(here / name, old.sha(expected)) != expected:
            raise ValueError("repaired presentation mismatch")
    for url, name, mime in (
        ("/", "review.html", "text/html; charset=utf-8"),
        ("/review.mjs", "review.mjs", "text/javascript; charset=utf-8"),
        ("/viewer-data.mjs", "viewer-data-v2-01.mjs", "text/javascript; charset=utf-8"),
    ):
        path = here / name
        if path.is_symlink():
            raise ValueError("UI symlink refused")
        routes[url] = (path, old.sha(path.read_bytes()), mime)
    if original != presentation.load_pair(here, packet_sha)[1] or expected != presentation.build_for(here, packet_sha, candidate_sha):
        raise ValueError("packet changed during route preparation")
    return routes


def routes():
    before = presentation.control_pins()
    result = routes_for(HERE, BASE, R1 / "localization-control/fixture.png",
                        presentation.PACKET_SHA, presentation.CANDIDATE_SHA, CONTROL_SHA)
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
                      "packet_sha256": presentation.PACKET_SHA, "assets": len(assets),
                      "writes": False, "pins": {url: digest for url, (_, digest, _) in assets.items()}},
                     sort_keys=True), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

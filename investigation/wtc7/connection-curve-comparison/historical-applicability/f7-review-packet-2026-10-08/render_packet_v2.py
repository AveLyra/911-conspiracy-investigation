"""Dependency-repaired presentation; retain candidate code and outputs unchanged."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import types

HERE = Path(__file__).resolve().parent
PACKET_SHA = "d2c75d2a399d495d88f270181259c71893c8025c68e542c150a57c60a91b6c83"
CANDIDATE_SHA = "ceadeebf040913d5654c20bce5d55dca5ae2b7e4d6612821818f67af6024fb1c"
PRIOR_RENDER_SHA = "c69722bcfb6eaf6b8fffd9d57a5ea2b182ecfb5fb11c1acbfb8a5c0ce3fbb52d"
PRIOR_SERVER_SHA = "d6de6105bd4cc6ba18a4113dfc2a69d7768e19b57e23729d671668834dd7ed4b"
FIXED = {
    "render_packet.py": PRIOR_RENDER_SHA,
    "serve_review.py": PRIOR_SERVER_SHA,
    "review.html": "819d6277e8e4d9922eb6749beb4055c48406bb80dad83e1572c468b525460942",
    "review.mjs": "ced0242f49ddb2843793c2f7a8d80fb51dbf44d5b97e8df16ad3d085eaf2cb13",
    "DEPENDENCY-REPAIR.md": "0f60d4b0592840fcdce8f40cebb5e94b9fab8d76c73fb1683c9a9260a0af4770",
}
NEW_FILES = ("render_packet_v2.py", "serve_review_v2.py", "test_presentation_v2.py")


def load_pinned(path, digest, name):
    """Execute only the checked bytes; never alter imported path constants."""
    if path.is_symlink():
        raise ValueError("helper symlink refused")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError("helper identity mismatch")
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


old = load_pinned(HERE / "render_packet.py", PRIOR_RENDER_SHA, "preserved_f7_presentation")
PACKET_ID = old.PACKET_ID


def load_pair(here, digest):
    if not isinstance(digest, str) or not re.fullmatch("[0-9a-f]{64}", digest):
        raise ValueError("repaired packet SHA not frozen")
    raw = old.pinned(here / "packet-v2-01.json", digest)
    if raw != old.pinned(here / "packet-v2-02.json", digest):
        raise ValueError("repaired packet repeat mismatch")
    return json.loads(raw, object_pairs_hook=old.unique, parse_constant=old.reject_constant), raw


def build_for(here, packet_sha, candidate_sha):
    """Explicit synthetic fixture arguments; CLI has no identity override."""
    if packet_sha == candidate_sha:
        raise ValueError("repair cannot reuse candidate identity")
    data, _ = load_pair(here, packet_sha)
    candidate, _ = old.load_pair(here, candidate_sha)
    payload = lambda item: {key: value for key, value in item.items()
                            if key not in ("inputs", "inputs_after")}
    if payload(data) != payload(candidate):
        raise ValueError("dependency repair changed scientific payload")
    if (data.get("inputs") != data.get("inputs_after")
            or not isinstance(data.get("inputs"), dict)
            or not isinstance(candidate.get("inputs"), dict)
            or not all(data["inputs"].get(k) == v for k, v in candidate["inputs"].items())
            or len(data["inputs"]) <= len(candidate["inputs"])):
        raise ValueError("dependency repair did not preserve and extend pins")
    return old.presentation_bytes(data, packet_sha)


def control_pins():
    result = old.control_pins()
    for name, digest in FIXED.items():
        raw = old.pinned(HERE / name, digest)
        result[name] = {"bytes": len(raw), "sha256": digest}
    for name in NEW_FILES:
        path = HERE / name
        if path.is_symlink():
            raise ValueError("new code symlink refused")
        raw = path.read_bytes()
        result[name] = {"bytes": len(raw), "sha256": old.sha(raw)}
    return result


def build():
    before = control_pins()
    raw = build_for(HERE, PACKET_SHA, CANDIDATE_SHA)
    if before != control_pins() or raw != build_for(HERE, PACKET_SHA, CANDIDATE_SHA):
        raise ValueError("presentation inputs changed")
    return raw


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", choices=("01", "02"))
    args = parser.parse_args()
    before = control_pins()
    raw = build()
    output = HERE / ("viewer-data-v2-" + args.run + ".mjs")
    old.save_exclusive(output, raw)
    if before != control_pins() or build() != raw:
        raise ValueError("changed after save; preserve output")
    print(json.dumps({"file": output.name, "bytes": len(raw), "sha256": old.sha(raw),
                      "packet_id": PACKET_ID, "version": 2, "packet_sha256": PACKET_SHA,
                      "controls_before": before, "controls_after": control_pins()}, sort_keys=True))

"""Thin version-2 presentation serializer; no selection or source mutation."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "envelope-packet-2026-10-08"
PACKET_SHA = "ceadeebf040913d5654c20bce5d55dca5ae2b7e4d6612821818f67af6024fb1c"  # Root-frozen packet bytes, not a self-hash.
PACKET_ID = "conditional-envelope-f7-v2-2026-10-08"
PROTOCOL_SHA = "c3081a9ca870d0b67ddee5cec2d7dc4d346db137711baf1dbdc39af3bc362651"
LINEAGE = {
    "render_packet.py": "514425a36d5b2327ced15c97f7603e1eba208c4d2e57983789076a0f43e6b68a",
    "serve_review.py": "6c1913c83a38ff6f1cd5ae1a2c8037f0fa7312a12501ed3d947bf364fd33c541",
    "review.mjs": "509142c1cd0ddecfd864aa904de31b16773076305026c60de793621920ba7082",
    "review.html": "7bee34510477e5b911f84ba3dd2380a447d46b86e2ab58389edca34053c6b2c6",
}
LOCAL_FILES = ("render_packet.py", "serve_review.py", "review.html", "review.mjs",
               "test_render_packet.py", "test_serve_review.py", "test_review.mjs")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pinned(path, digest):
    if path.is_symlink():
        raise ValueError("symlink refused")
    raw = path.read_bytes()
    if sha(raw) != digest:
        raise ValueError("asset identity mismatch")
    return raw


def unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key")
        value[key] = item
    return value


def reject_constant(value):
    raise ValueError("nonfinite JSON: " + value)


def load_pair(directory, expected_sha):
    if not isinstance(expected_sha, str) or not re.fullmatch("[0-9a-f]{64}", expected_sha):
        raise ValueError("historical packet SHA not frozen")
    first = pinned(directory / "packet01.json", expected_sha)
    if first != pinned(directory / "packet02.json", expected_sha):
        raise ValueError("packet repeat mismatch")
    data = json.loads(first, object_pairs_hook=unique, parse_constant=reject_constant)
    return data, first


def validate_identity(data, digest):
    if type(data.get("version")) is not int or data["version"] != 2 or data.get("packet_id") != PACKET_ID:
        raise ValueError("wrong packet version or ID")
    if not re.fullmatch("[0-9a-f]{64}", digest):
        raise ValueError("invalid packet hash")
    if (data.get("status") != "conditional_mapping_packet_pending_human"
            or data.get("human_accepted") is not False
            or data.get("actual_D", "missing") is not None
            or data.get("model_discrepancies", "missing") is not None):
        raise ValueError("unexpected acceptance or measurement")
    expected = [f"CE-{panel}{bolt}Q{q}" for panel in ("F", "E")
                for bolt in range(3, 10) for q in (1, 2, 3)]
    if [s.get("id") for s in data["slots"]] != expected:
        raise ValueError("wrong ordered 42-slot roster")
    for slot in data["slots"]:
        if slot.get("human_accepted") is not False:
            raise ValueError("slot acceptance contamination")
        if [entry.get("id") for entry in slot["entries"]] != [slot["id"]+"-spring", slot["id"]+"-shell"]:
            raise ValueError("wrong 84-entry roster")
        for entry in slot["entries"]:
            if entry.get("human_status") != "uninspected" or entry.get("human_response", "missing") is not None:
                raise ValueError("human response contamination")
    names = {"page"} | {f"Im{i}" for i in range(12)}
    if set(data["assets"]) != names:
        raise ValueError("complete source asset roster required")
    for name, asset in data["assets"].items():
        url = "/page.png" if name == "page" else f"/source/{name}.jpg"
        path = "render01/page-076.png" if name == "page" else f"native-strips01/{name}.jpg"
        if asset.get("url") != url or asset.get("path") != path:
            raise ValueError("unexpected source route or path")
        if (not isinstance(asset.get("sha256"), str)
                or not re.fullmatch("[0-9a-f]{64}", asset["sha256"])
                or any(type(asset.get(k)) is not int or asset[k] <= 0 for k in ("bytes", "width", "height"))):
            raise ValueError("invalid source metadata")


def presentation_bytes(data, digest):
    """Pure synthetic-testable projection; never rewrites the input packet."""
    validate_identity(data, digest)
    projected = copy.deepcopy({key: data[key] for key in (
        "status", "version", "packet_id", "human_accepted",
        "slots", "summary", "assets", "assumptions", "domain_kind")})
    for asset in projected["assets"].values():
        del asset["path"]
    projected["packet_sha256"] = digest
    return ("export const PACKET = " + json.dumps(
        projected, sort_keys=True, separators=(",", ":"), allow_nan=False) + ";\n").encode()


def control_pins():
    pinned(HERE / "PROTOCOL.md", PROTOCOL_SHA)
    result = {"PROTOCOL.md": {"bytes": (HERE/"PROTOCOL.md").stat().st_size, "sha256": PROTOCOL_SHA}}
    for name, expected in LINEAGE.items():
        raw = pinned(OLD/name, expected)
        result["../envelope-packet-2026-10-08/"+name] = {"bytes": len(raw), "sha256": expected}
    for name in LOCAL_FILES:
        path = HERE/name
        if path.is_symlink():
            raise ValueError("local code symlink refused")
        raw = path.read_bytes()
        result[name] = {"bytes": len(raw), "sha256": sha(raw)}
    return result


def build():
    if not re.fullmatch("[0-9a-f]{64}", PACKET_SHA):
        raise ValueError("historical packet SHA not frozen")
    before = control_pins()
    data, original = load_pair(HERE, PACKET_SHA)
    result = presentation_bytes(data, PACKET_SHA)
    if before != control_pins() or load_pair(HERE, PACKET_SHA)[1] != original:
        raise ValueError("inputs changed during presentation")
    return result


def save_exclusive(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", choices=("01", "02"))
    args = parser.parse_args()
    before = control_pins()
    raw = build()
    output = HERE / ("viewer-data"+args.run+".mjs")
    save_exclusive(output, raw)
    if before != control_pins() or build() != raw:
        raise ValueError("changed after save; preserve output")
    print(json.dumps({"file": output.name, "bytes": len(raw), "sha256": sha(raw),
                      "packet_id": PACKET_ID, "version": 2, "packet_sha256": PACKET_SHA,
                      "controls_before": before, "controls_after": control_pins()}, sort_keys=True))

#!/usr/bin/env python3
"""Batch 3 adapter for hash-pinned batch 2 validation and descriptive comparison.

The only edit to reused source is its hard-coded 13-row validation count.
Membership, paths, source pins and filesystem guards belong to this adapter.
No observation file is read merely by importing this module.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import types

from PIL import Image

HERE = Path(__file__).absolute().parent
BASE = HERE.parent / "fire-coverage-batch2" / "summarize.py"
BASE_SHA256 = "f24bb98a1b988a8eef20ae2095d5ec7fa6819e3520f0516cbca126c733641464"
PROTOCOL_SHA256 = "ecdd7be9123231e05217c456ebc5ffbaa71c7828802d1212e0ed26a784e559c6"
PROVENANCE_KEY_SHA256 = "50144e50b2907bdd0dd4a62f398bedf3c8f40dc3008888580486496ddebd094f"
PAIR_KEY_SHA256 = "5b01f713bd100c8eda211800b29e93704b023dd6f12aaaa7c7f1210fe79da8e1"
NOTE_PINS = {"TILED-IMAGE-ADDENDUM.md": "bede56a07730055dd16e20d6be22e3e1f32667504ee9028346cbb3e4bbebd724",
             "PAIR-KEY-NOTE.md": "dad716c5bee95ade5269556f2260cfe6659c810f1bbfa11703ad9fbba6717979"}
KEY_PATH = "anonymous-key.json"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, value, *, existing=True):
    """Reject traversal/symlinks before following any user or manifest path."""
    root = Path(root).absolute()
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    if ".." in path.parts or "." in Path(value).parts:
        raise ValueError("noncanonical path")
    path = path.absolute()
    if path == root or root not in path.parents:
        raise ValueError("path outside declared root")
    for component in [path, *path.parents]:
        if component.is_symlink():
            raise ValueError("symlink forbidden")
    if existing and not path.is_file():
        raise ValueError("input must be a regular file")
    if not existing and not path.parent.is_dir():
        raise ValueError("output parent must already exist")
    return path


def legacy(sample, protocol_hash=PROTOCOL_SHA256, key_hash=PROVENANCE_KEY_SHA256):
    safe_path(HERE.parent, BASE)
    raw = BASE.read_bytes()
    if digest(raw) != BASE_SHA256:
        raise ValueError("batch 2 source pin mismatch")
    text = raw.decode("utf-8")
    old = 'len(data["assets"]) == 13'
    new = 'len(data["assets"]) == len(SAMPLE)'
    if text.count(old) != 1:
        raise ValueError("expected single batch 2 count adaptation")
    module = types.ModuleType("batch2_reused")
    module.__file__ = str(BASE)
    exec(compile(text.replace(old, new), str(BASE), "exec"), module.__dict__)
    module.SAMPLE = tuple(sample)
    module.PROTOCOL_SHA256 = protocol_hash
    module.PROVENANCE_KEY_SHA256 = key_hash
    return module


def read_json(path):
    raw = Path(path).read_bytes()
    return legacy(()).decode_json(raw), digest(raw)


def validate_key(key, scope="full"):
    m = legacy(())
    m.require(isinstance(key, dict) and isinstance(key.get("assets"), list), "key assets missing")
    m.require(bool(key["assets"]), "key membership empty")
    pins = {}
    for item in key["assets"]:
        m.require(isinstance(item, dict), "key asset must be an object")
        aid = item.get("asset_id")
        m.require(isinstance(aid, str) and re.fullmatch(r"[AC]-[0-9a-f]{12}", aid), "invalid asset ID")
        m.require(aid not in pins, "duplicate key asset ID")
        view = item.get("extracted_view")
        m.require(isinstance(view, dict), "key extracted_view missing")
        m.require(view.get("format") == "JPEG", "only native JPEG accepted; tiled reconstruction failed")
        expected = f"assets/run01/images/{aid}.jpg"
        m.dimensions(item.get("native_pdf_dimensions"), "native PDF image")
        m.require(view.get("dimensions") == item["native_pdf_dimensions"], "native dimension mismatch")
        m.require(view.get("path") == expected, "unexpected source path")
        m.require(isinstance(view.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", view["sha256"]), "invalid image hash")
        m.dimensions(view.get("dimensions"), "key image")
        m.require(type(view.get("bytes")) is int and view["bytes"] > 0, "invalid source byte size")
        pins[aid] = {"asset_id": aid, **view}
    if scope == "pair":
        m.require(len(pins) == 2 and key.get("sample_asset_ids") == list(pins), "invalid pair membership")
    else:
        pair = key.get("pair_asset_ids")
        m.require(isinstance(pair, list) and len(pair) == 2 and len(set(pair)) == 2 and set(pair) <= set(pins), "invalid pair membership")
        m.require(list(pins)[:2] == pair, "pair must be first two key assets")
        m.require(key.get("selected_asset_ids") == list(pins), "selected membership/order mismatch")
    return pins


def verify_sources(root, key_hash, protocol_hash, scope):
    m = legacy(())
    m.require(scope in ("pair", "full"), "invalid comparison scope")
    snapshot = {}

    def capture(relative, expected=None):
        path = safe_path(root, relative)
        raw = path.read_bytes()
        actual = digest(raw)
        if expected is not None:
            m.require(actual == expected, "input pin mismatch")
        snapshot[str(path)] = actual
        return raw

    capture("PROTOCOL.md", protocol_hash)
    for path, sha in NOTE_PINS.items():
        capture(path, sha)
    m.require(isinstance(key_hash, str) and re.fullmatch(r"[0-9a-f]{64}", key_hash), "anonymous key must be frozen")
    key = m.decode_json(capture("anonymous-pair-key.json" if scope == "pair" else KEY_PATH, key_hash))
    pins = validate_key(key, scope)
    for item in key["assets"]:
        pin = pins[item["asset_id"]]
        raw = capture(pin["path"], pin["sha256"])
        m.require(len(raw) == pin["bytes"], "image byte size mismatch")
        with Image.open(io.BytesIO(raw)) as image:
            m.require(image.format == pin["format"], "image header format mismatch")
            m.require(list(image.size) == pin["dimensions"], "image header dimension mismatch")
    sample = list(pins)
    snapshot[str(BASE)] = BASE_SHA256
    snapshot[str(Path(__file__).absolute())] = digest(Path(__file__).read_bytes())
    return sample, pins, snapshot


def verify_snapshot(snapshot, root):
    for path, expected in snapshot.items():
        allowed = HERE.parent if Path(path) == BASE else (HERE if Path(path) == Path(__file__).absolute() else root)
        checked = safe_path(allowed, path)
        if digest(checked.read_bytes()) != expected:
            raise ValueError("input changed during comparison")


def build_report(label_paths, *, root=HERE, scope="full", key_hash=None, protocol_hash=PROTOCOL_SHA256):
    root = Path(root).absolute()
    if key_hash is None:
        key_hash = PAIR_KEY_SHA256 if scope == "pair" else PROVENANCE_KEY_SHA256
    sample, pins, snapshot = verify_sources(root, key_hash, protocol_hash, scope)
    m = legacy(sample, protocol_hash, key_hash)
    m.require(len(label_paths) >= 2, "at least two observation records required")
    records, reviewers, labels = [], set(), []
    for label_path in label_paths:
        path = safe_path(root, label_path)
        data, sha = read_json(path)
        m.validate_labels(data, pins)
        m.require(data["reviewer"] not in reviewers, "duplicate reviewer identity")
        reviewers.add(data["reviewer"])
        snapshot[str(path)] = sha
        records.append(data)
        labels.append({"path": str(path.relative_to(root)), "sha256": sha, "reviewer": data["reviewer"]})
    report = {
        "schema_version": 2, "batch": 3, "scope": scope,
        "sample_asset_ids": sample,
        "source_hashes": {"protocol_sha256": protocol_hash, "provenance_key_sha256": key_hash,
                          "batch2_code_sha256": BASE_SHA256, "code_sha256": snapshot[str(Path(__file__).absolute())],
                          "labels": labels, "images": [pins[x] for x in sample]},
        "input_snapshot": snapshot,
        "reuse": {"source": "../fire-coverage-batch2/summarize.py", "single_source_replacement":
                  ['len(data["assets"]) == 13', 'len(data["assets"]) == len(SAMPLE)']},
        "limitations": ["Qualitative image descriptions, not fire extent, temperature, cause or event counts.",
                        "Raw disagreements and null/unresolved observations are retained without consensus.",
                        "Matching axes or JSON do not establish accuracy, spatial agreement or independent events.",
                        "Reason strings are checked for presence, not substantive observational adequacy.",
                        "Input integrity is not historical authentication or qualified human review."],
        "raw_records": records, "comparisons": m.compare_records(records),
    }
    verify_snapshot(snapshot, root)
    return report


def write_report(report, out, *, root=HERE):
    out = safe_path(root, out, existing=False)
    if report.get("input_snapshot"):
        verify_snapshot(report["input_snapshot"], root)
    with out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels", nargs="+", required=True)
    parser.add_argument("--scope", choices=("pair", "full"), default="full")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        out = safe_path(HERE, args.out, existing=False)
        if out.exists():
            raise ValueError("output already exists")
        report = build_report(args.labels, scope=args.scope)
        write_report(report, out)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print("Saved validated descriptive comparisons to a fresh JSON file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

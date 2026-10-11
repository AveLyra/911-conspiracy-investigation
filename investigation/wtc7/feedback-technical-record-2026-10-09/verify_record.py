"""Check this bounded requirements record; does not certify semantic completeness."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(record, source=None):
    require(record["schema"] == "sherlock-feedback-technical-record/v1", "schema")
    pin = record["source"]
    require(type(pin["lines"]) is int and pin["lines"] > 0, "source line count")
    require(type(pin["bytes"]) is int and pin["bytes"] > 0, "source byte count")
    require(re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]) is not None, "source hash")
    require(set(record["digest_topics"]) == {f"{i:02d}" for i in range(1, 28)}, "digest topic index")
    require(all(isinstance(x, str) and x.strip() for x in record["digest_topics"].values()), "digest topic titles")
    source_lines = None
    if source is not None:
        require(digest(source) == pin["sha256"], "source snapshot mismatch")
        require(len(source) == pin["bytes"], "source size mismatch")
        source_lines = source.splitlines(keepends=True)
        require(len(source_lines) == pin["lines"], "source line mismatch")
    next_line = 1
    ids = set()
    mapped = set()
    counts = {"requirement": 0, "context": 0, "blank": 0}
    keys = {"id", "start", "end", "kind", "sfb", "digest_items", "title",
            "technical_record", "acceptance", "qualification", "omission", "source_sha256"}
    for unit in record["units"]:
        require(set(unit) == keys, f"unit fields: {unit.get('id', '?')}")
        require(type(unit["start"]) is int and type(unit["end"]) is int, "integer spans")
        require(unit["start"] == next_line, f"gap, overlap or reorder at {next_line}")
        require(unit["start"] <= unit["end"] <= pin["lines"], "span bounds")
        require(unit["id"] == f"TR-L{unit['start']:04d}", "source-based ID")
        require(unit["id"] not in ids, "duplicate ID")
        ids.add(unit["id"])
        kind = unit["kind"]
        require(kind in counts, "unit kind")
        counts[kind] += 1
        for field in ("title", "technical_record", "qualification", "omission"):
            require(isinstance(unit[field], str), f"text field {field}")
        require(bool(unit["title"].strip()), "empty title")
        for field in ("sfb", "digest_items", "acceptance"):
            require(isinstance(unit[field], list) and all(isinstance(x, str) and x.strip() for x in unit[field]), f"list field {field}")
        require(set(unit["sfb"]) <= {f"SFB-{i:03d}" for i in range(1, 6)}, "SFB mapping")
        require(set(unit["digest_items"]) <= {f"{i:02d}" for i in range(1, 28)}, "digest mapping")
        mapped.update(unit["digest_items"])
        if kind == "requirement":
            require(bool(unit["sfb"]) and bool(unit["digest_items"]), "missing requirement mapping")
            require(bool(unit["technical_record"].strip()), "empty requirement")
            require(bool(unit["acceptance"]), "missing acceptance case")
            require(bool(unit["qualification"].strip()), "missing qualification")
        else:
            require(bool(unit["omission"].strip()), "unexplained context exclusion")
        require(re.fullmatch(r"[0-9a-f]{64}", unit["source_sha256"]) is not None, "unit hash")
        if source_lines is not None:
            actual = digest(b"".join(source_lines[unit["start"] - 1:unit["end"]]))
            require(actual == unit["source_sha256"], f"source span mismatch {unit['id']}")
        next_line = unit["end"] + 1
    require(next_line == pin["lines"] + 1, "incomplete source coverage")
    require(mapped == {f"{i:02d}" for i in range(1, 28)}, "unmapped digest topic")
    return {"source_lines_accounted_for": pin["lines"], "units": len(ids),
            "kinds": counts, "digest_topics_mapped": len(mapped),
            "source_bytes_verified": source is not None,
            "semantic_completeness_certified_by_checker": False}


def render(record):
    out = ["# Sherlock feedback technical requirements", "",
           "This is the source-ordered technical transcription and coverage map for the frozen feedback snapshot. The JSON record is the editable source for this generated view. See README.md for scope, status, review limits and source privacy.", "",
           f"Source SHA-256: `{record['source']['sha256']}`. Source lines: {record['source']['lines']}.", ""]
    out += ["## Earlier digest crosswalk", "",
            "Topic membership is navigation, not proof that the earlier digest or recipient log retained every refinement.", "",
            "| Digest item | Topic | Detailed units |", "| --- | --- | --- |"]
    for item, title in sorted(record["digest_topics"].items()):
        units = ", ".join(u["id"] for u in record["units"] if item in u["digest_items"])
        out.append(f"| {item} | {title} | {units} |")
    out += [""]
    for u in record["units"]:
        out += [f"## {u['id']} {u['title']}", "",
                f"Source lines {u['start']}–{u['end']}; {u['kind']}. SFB mapping: {', '.join(u['sfb']) or 'none'}. Earlier digest topics: {', '.join(u['digest_items']) or 'none'}.", ""]
        if u["technical_record"]:
            out += [u["technical_record"], ""]
        if u["acceptance"]:
            out += ["Acceptance checks", ""] + [f"- {a}" for a in u["acceptance"]] + [""]
        if u["qualification"]:
            out += [f"Qualification: {u['qualification']}", ""]
        if u["omission"]:
            out += [f"Publication transformation: {u['omission']}", ""]
    return "\n".join(out)


def verify_manifest(root):
    manifest = read_json(root / "manifest.json")
    files = manifest["files"]
    require(isinstance(files, dict) and files, "manifest files")
    for name, pin in files.items():
        require(name == Path(name).name and name != "manifest.json", "manifest path")
        path = root / name
        require(not path.is_symlink() and path.is_file(), f"regular file {name}")
        data = path.read_bytes()
        require(digest(data) == pin["sha256"] and len(data) == pin["bytes"], f"file mismatch {name}")
    actual = {p.name for p in root.iterdir() if p.name != "manifest.json"}
    require(actual == set(files), "unlisted or missing packet entry")
    return len(files)


def verify_review(record, review, record_bytes):
    require(review["schema"] == "sherlock-feedback-review/v1", "review schema")
    require(review["source_sha256"] == record["source"]["sha256"], "review source pin")
    require(review["reviewed_final_record_sha256"] == digest(record_bytes), "review record binding")
    ids = []
    for part in review["partitions"]:
        start, end = part["source_lines"]
        expected = [u["id"] for u in record["units"] if start <= u["start"] and u["end"] <= end]
        require(part["reviewed_ids"] == expected and bool(expected), "review partition coverage")
        ids.extend(part["reviewed_ids"])
        for finding in part["findings"]:
            require(bool(finding["resolution"].strip()), "unresolved review finding")
    require(ids == [u["id"] for u in record["units"]], "incomplete or duplicate review coverage")
    return len(ids)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", type=Path, help="Optional authorized local original; never uploaded")
    ap.add_argument("--render", action="store_true", help="Regenerate REQUIREMENTS.md from record.json")
    ap.add_argument("--manifest", action="store_true", help="Verify the complete release manifest")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    record_path = root / "record.json"
    record = read_json(record_path)
    result = validate(record, args.source.read_bytes() if args.source else None)
    result["reviewed_units_verified"] = verify_review(record, read_json(root / "review.json"), record_path.read_bytes())
    rendered = render(record)
    if args.render:
        (root / "REQUIREMENTS.md").write_text(rendered, encoding="utf-8")
    else:
        require((root / "REQUIREMENTS.md").read_text(encoding="utf-8") == rendered, "stale rendered requirements")
    if args.manifest:
        result["manifest_files_verified"] = verify_manifest(root)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

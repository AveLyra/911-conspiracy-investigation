"""Reproduce the bounded filename census and notice-byte identity; no network."""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

def checked(path, digest):
    body = path.read_bytes()
    if hashlib.sha256(body).hexdigest() != digest:
        raise ValueError("Input hash mismatch: " + path.name)
    return body

def main():
    if len(sys.argv) != 4:
        raise SystemExit("Usage: verify.py NOTICE CATALOG PARSER")
    pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    notice_path, catalog_path, parser_path = map(Path, sys.argv[1:])
    notice = checked(notice_path, pins["notice"]["sha256"])
    catalog = checked(catalog_path, pins["catalog"]["sha256"])
    checked(parser_path, pins["parser"]["sha256"])
    assert len(notice) == pins["notice"]["bytes"]
    assert len(catalog) == pins["catalog"]["bytes"]
    lines = notice.decode("utf-8").splitlines()
    assert lines[0] == "Notice for Release 32"
    assert "NYPD photographs" in lines[2]
    spec = importlib.util.spec_from_file_location("release32_passive_parser", parser_path)
    parser = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parser)
    rows = parser.read_bencode(catalog)[b"info"][b"files"]
    paths = ["/".join(part.decode("utf-8") for part in row[b"path"]) for row in rows]
    assert len(paths) == pins["catalog"]["entries"]
    counts = dict(collections.Counter(Path(p).suffix.lower() for p in paths))
    assert counts == pins["catalog"]["suffix_counts"]
    image_suffixes = set(pins["catalog"]["image_suffixes"])
    other = [p for p in paths if Path(p).suffix.lower() not in image_suffixes]
    assert len(other) == pins["catalog"]["nonimage_candidates"]
    rx = re.compile(pins["catalog"]["relevant_nonimage_path_regex"], re.I)
    assert sum(bool(rx.search(p)) for p in other) == pins["catalog"]["relevant_nonimage_path_regex_count"]
    docs = [p for p in other if Path(p).suffix.lower() in (".txt", ".pdf")]
    assert len(docs) == pins["catalog"]["document_like_candidates"]
    for item in pins["document_like_candidates"]:
        i = item["catalog_index"]
        assert paths[i] == item["path"]
        assert rows[i][b"length"] == item["declared_bytes"]
    assert rows[pins["notice"]["catalog_index"]][b"length"] == len(notice)
    print(json.dumps({"verified_notice_bytes": len(notice), "catalog_entries": len(paths),
        "nonimage_filename_candidates": len(other), "text_pdf_candidates": len(docs),
        "filter_matches": 0, "all_bodies_reviewed": False,
        "agency_authentication_or_physical_identity_established": False}, indent=2))
if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify preserved representations and notes, not historical transfer claims."""
import argparse
import hashlib
import json
from pathlib import Path

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", type=Path, help="Native study directory containing sources/")
    parser.add_argument("--native-root", type=Path, help="Root containing protected earlier studies")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    pins = json.loads((here / "SOURCE-PINS.json").read_text())
    source = pins["source"]
    assert source["native_source_acquired"] is False
    assert source["native_sha256"] is None
    assert source["direct_access_status"] == 403
    assert len(source["claims"]) == 6
    assert len({r["id"] for r in source["claims"]}) == 6
    assert source["indexed_capture"]["sha256"] != source["native_sha256"]
    print("Publication-scope checks passed: indexed-source lead; native bytes unacquired.")
    if args.study:
        path = args.study / source["indexed_capture"]["path"]
        assert path.stat().st_size == source["indexed_capture"]["bytes"]
        assert sha(path) == source["indexed_capture"]["sha256"]
        text = path.read_text()
        for claim in source["claims"]:
            assert claim["needle"] in text, claim["id"]
        for name in ("sec-oct6-ex991", "sec-oct6-index"):
            meta = json.loads((args.study / "sources" / (name + ".fetch.json")).read_text())
            body = args.study / "sources" / (name + ".response")
            assert meta["status"] == 403
            assert len(body.read_bytes()) == meta["bytes"]
            assert sha(body) == meta["sha256"]
        print("Saved indexed representation: length/hash match; six claim locators match.")
        print("Two 403 response entities match receipts; neither is treated as the exhibit.")
    else:
        print("Native-source checks NOT RUN: pass --study to supply the retained captures.")
    if args.native_root:
        for item in pins["protected_predecessors"]:
            path = args.native_root / item["relative_to_native_root"]
            assert path.stat().st_size == item["bytes"]
            assert sha(path) == item["sha256"], str(path)
        print("Five protected predecessor files unchanged.")
    else:
        print("Predecessor preservation checks NOT RUN: pass --native-root to supply originals.")
    print("No employment, asset delivery, data survival or call attribution is validated by these checks.")

if __name__ == "__main__":
    main()

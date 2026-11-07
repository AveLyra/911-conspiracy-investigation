#!/usr/bin/env python3
"""Check preserved source entities; do not authenticate handwriting or history."""
import argparse
import hashlib
import json
import zlib
from pathlib import Path

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--image-dir", type=Path)
    parser.add_argument("--mfr", type=Path)
    parser.add_argument("--native-root", type=Path)
    args = parser.parse_args()
    pins = json.loads((Path(__file__).resolve().parent / "SOURCE-PINS.json").read_text())
    assert set(pins["sources"]) == {"soc-notes-315.pdf", "soc-handwritten-313.pdf"}
    assert [pins["sources"][n]["physical_pages"] for n in sorted(pins["sources"])] == [11, 2]
    assert len(pins["observations"]) == len({r["id"] for r in pins["observations"]}) == 12
    assert pins["all_five_track_completion_claimed"] is False
    print("Two source entities, twelve qualified observations, no full-goal completion claim.")
    if args.source_dir:
        import pypdf
        for name, row in pins["sources"].items():
            p = args.source_dir / name
            data = p.read_bytes()
            assert data.startswith(b"%PDF-")
            assert len(data) == row["bytes"]
            assert sha(p) == row["sha256"]
            assert f"{zlib.crc32(data):08x}" == row["crc32"]
            assert len(pypdf.PdfReader(p).pages) == row["physical_pages"]
        print(f"Two PDF size/SHA-256/CRC/page checks passed with pypdf {pypdf.__version__}.")
    else:
        print("PDF checks NOT RUN; supply --source-dir containing retained originals.")
    if args.image_dir:
        count = 0
        for row in pins["sources"].values():
            for image in row["images"]:
                p = args.image_dir / image["file"]
                assert p.stat().st_size == image["bytes"]
                assert sha(p) == image["sha256"]
                count += 1
        assert count == 13
        print("Thirteen retained page-image hashes and lengths match.")
    else:
        print("Image checks NOT RUN; supply --image-dir with retained renders.")
    if args.mfr:
        assert args.mfr.stat().st_size == pins["official_mfr"]["bytes"]
        assert sha(args.mfr) == pins["official_mfr"]["sha256"]
        print("Previously acquired official memorandum hash matches.")
    else:
        print("Official-MFR check NOT RUN; supply --mfr.")
    if args.native_root:
        for row in pins["protected_predecessors"]:
            p = args.native_root / row["path"]
            assert p.stat().st_size == row["bytes"]
            assert sha(p) == row["sha256"]
        print("Five protected predecessor files unchanged.")
    else:
        print("Predecessor checks NOT RUN; supply --native-root.")
    print("Manual handwriting, author/event joins, clock labels, source release and historical claims remain separately qualified.")

if __name__ == "__main__":
    main()

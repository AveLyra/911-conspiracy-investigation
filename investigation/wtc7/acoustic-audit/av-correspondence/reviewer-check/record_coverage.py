#!/usr/bin/env python3
"""Record exactly which root-produced images this reviewer inspected."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RUN = BASE / "run01"
OUT = Path(__file__).resolve().parent / "initial-visual-coverage.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        raise FileExistsError("Refusing existing coverage record")
    receipt = json.loads((RUN / "receipt.json").read_text())
    products = receipt["products"]
    overview = [f"compilation-overview/sheet-{i:04d}.png" for i in range(0, 301, 30)]
    overview.append("comparator-overview/sheet-0000.png")
    native_ids = {
        "compilation": [30, 31, 236, 237, 273, 274, 290, 291, 292,
                        306, 307, 308, 309, 310, 311, 312, 315],
        "comparator": [1, 2, 3, 4, 5, 6, 7, 12],
    }
    coverage = []
    for path in overview:
        coverage.append({"path": path, "view": "overview, all populated cells",
                         "sha256": digest(RUN / path)})
    for label, identifiers in native_ids.items():
        rows = json.loads((RUN / f"{label}-selected.json").read_text())
        for identifier in identifiers:
            path = f"{label}/frame-{identifier:04d}.png"
            row = next(r for r in rows if r["png"] == path)
            coverage.append({"path": path, "view": "whole native raster, 1280x720",
                             "source_index": row["source_index"],
                             "source_seconds_exact": row["source_seconds_exact"],
                             "sha256": digest(RUN / path)})
    if not all(row["sha256"] == products[row["path"]]["sha256"] for row in coverage):
        raise ValueError("Viewed-image hash differs from root receipt")
    result = {"status": "hash_match", "images": coverage,
              "overview_files": 12, "overview_historical_frames": 334,
              "native_full_raster_frames": 25,
              "root_receipt_sha256": digest(RUN / "receipt.json"),
              "root_script_sha256": digest(BASE / "extract_frames.py"),
              "protocol_sha256": digest(BASE / "PROTOCOL.md"),
              "recorder_sha256": digest(Path(__file__)),
              "limits": "Records already performed visual inspection and fresh byte checks. Does not itself verify image interpretation, independent source authenticity, calibrated motion, audio content, or complete native-raster review of the 334-frame selection."}
    with OUT.open("x") as file:
        json.dump(result, file, indent=2, sort_keys=True)
        file.write("\n")
    print(json.dumps({"status": result["status"], "viewed_images_hashed": len(coverage)}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Record only the second-stage images actually inspected by this reviewer."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RUN = BASE / "refine01"
OUT = Path(__file__).resolve().parent / "refinement-visual-coverage.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        raise FileExistsError("Refusing existing refinement coverage")
    products = json.loads((RUN / "receipt.json").read_text())["products"]
    images = []
    for label, indexes, sheets in (
        ("compilation", [23, 24, 31, 39, 61, 75, 90], [0, 30, 60]),
        ("comparator", [1, 30], [0]),
    ):
        rows = json.loads((RUN / f"{label}-selected.json").read_text())
        for i in sheets:
            path = f"{label}-overview/sheet-{i:04d}.png"
            images.append({"path": path, "view": "overview, all populated cells", "sha256": digest(RUN / path)})
        for i in indexes:
            path = f"{label}/frame-{i:04d}.png"
            row = next(r for r in rows if r["png"] == path)
            images.append({"path": path, "view": "whole native raster, 1280x720",
                           "source_index": row["source_index"],
                           "source_seconds_exact": row["source_seconds_exact"],
                           "sha256": digest(RUN / path)})
    if not all(r["sha256"] == products[r["path"]]["sha256"] for r in images):
        raise ValueError("Viewed-image hash differs from root receipt")
    result = {"status": "hash_match", "images": images,
              "overview_files": 4, "overview_frame_views": 120,
              "native_full_raster_views": 9,
              "root_receipt_sha256": digest(RUN / "receipt.json"),
              "root_refinement_script_sha256": digest(BASE / "refine_frames.py"),
              "refinement_declaration_sha256": digest(BASE / "REFINEMENT.md"),
              "recorder_sha256": digest(Path(__file__)),
              "limits": "Frame coverage overlaps initial sampling; counts are not independent observations. Inspection does not authenticate original chronology, audio, or a causal mechanism. No second-run or audio-crosswalk review."}
    with OUT.open("x") as file:
        json.dump(result, file, indent=2, sort_keys=True)
        file.write("\n")
    print(json.dumps({"status": result["status"], "viewed_images_hashed": len(images)}))


if __name__ == "__main__":
    main()

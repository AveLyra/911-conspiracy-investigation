"""Verify recorded archive copies and analytic bookkeeping, not historical truth.

python verify.py --source-dir /path/to/preserved/sources
Requires Pillow. Source images are read only; no network or source modification.
"""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-dir", required=True, type=Path)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    index = json.loads((here / "IMAGE-SOURCES.json").read_text())
    rows = index["files"]
    assert len(rows) == len({r["id"] for r in rows}) == 56
    assert sum(r["bytes"] for r in rows) == 40908936
    assert len({r["sha256"] for r in rows}) == 55
    scans = [r for r in rows if r["name"].startswith("WTC")]
    assert {r["name"] for r in scans} == {f"WTC{n:03}.jpg" for n in range(1, 51)}
    assert sum(r["bytes"] for r in scans) == 37796640
    checked = []
    for row in rows:
        path = args.source_dir / row["relative_source_path"]
        raw = path.read_bytes()
        assert len(raw) == row["bytes"], row["name"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"], row["name"]
        with Image.open(path) as im:
            assert im.format == "JPEG", row["name"]
            im.verify()
        checked.append({"id": row["id"], "name": row["name"], "matches_captured_hash_and_size": True})
    inspection = json.loads((here / "SCAN-INSPECTION.json").read_text())
    assert len(inspection["images"]) == 50
    for scan in inspection["images"]:
        capture = next(r for r in scans if r["name"] == scan["name"])
        assert scan["sha256"] == capture["sha256"]
        assert scan["dimensions"] == [3456, 2502]
        assert scan["exif"] in ({}, {"ExifIFD": {}})
        assert scan["ocr_returncode"] == 0
    controls = json.loads((here / "OCR-CONTROLS.json").read_text())["controls"]
    assert len(controls) == 4 and not any(r["ocr_detected_control"] for r in controls)
    duplicate = json.loads((here / "DUPLICATE-CHECK.json").read_text())
    assert duplicate["distinct_ids_same_sha256"]
    assert not duplicate["all_18_pairs_byte_compared"]
    join = json.loads((here / "PHOTO-JOINS.json").read_text())
    assert not join["W14A_W14B_candidate_photos_joined"]
    assert not join["G3005_or_Column79_joined"]
    result = {
        "scope": "Captured-byte identity, JPEG readability and report bookkeeping. Manual source-image readings are separate; not historical origin, camera clock, custody or physical-test validation.",
        "archive_images_verified": len(checked),
        "files": checked,
        "scan_ocr_processes_completed": 50,
        "visually_read_control_labels_detected_by_ocr": 0,
        "ocr_control_labels_tested": 4,
        "all_required_original_records_obtained": False,
        "goal_complete": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Separate fixture-schedule/pixel check; does not import root extraction code."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform

from PIL import Image

BASE = Path(__file__).resolve().parent.parent
RUN = BASE / "run01"
OUT = Path(__file__).resolve().parent / "synthetic-check.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        raise FileExistsError("Refusing existing reviewer result")
    checks = {}
    coverage = {}
    for offset in (0, 5):
        prefix = f"synthetic-{offset}"
        meta_path = RUN / f"{prefix}-stream.json"
        pts_path = RUN / f"{prefix}-all-frame-pts.json"
        rows_path = RUN / f"{prefix}-selected-selected.json"
        stream = json.loads(meta_path.read_text())["streams"][0]
        frames = json.loads(pts_path.read_text())["frames"]
        rows = json.loads(rows_path.read_text())
        tick = Fraction(stream["time_base"])
        checks[prefix + ":36_source_frames"] = len(frames) == 36
        # The fixture generator requests 12 fps. Container timestamps are checked
        # against that separately constructed rational schedule, permitting only
        # half of one container tick for representational rounding.
        errors = [abs(f["pts"] * tick - (offset + Fraction(i, 12)))
                  for i, f in enumerate(frames)]
        checks[prefix + ":full_timestamp_schedule"] = all(e <= tick / 2 for e in errors)
        expected_indexes = list(range(0, 24, 3)) + list(range(24, 36))
        checks[prefix + ":selected_indexes"] = [r["source_index"] for r in rows] == expected_indexes
        for row in rows:
            i = row["source_index"]
            path = RUN / row["png"]
            checks[f"{prefix}:frame{i}:hash"] = digest(path) == row["sha256"]
            with Image.open(path) as image:
                image.load()
                actual = list(image.getdata())
                background = (i * 7 % 256, i * 11 % 256, i * 13 % 256)
                patch = (255 - i, i, 90)
                expected = [patch if 5 <= x < 30 and 4 <= y < 20 else background
                            for y in range(48) for x in range(64)]
                checks[f"{prefix}:frame{i}:all_rgb_pixels"] = (
                    image.mode == "RGB" and image.size == (64, 48) and actual == expected)
        coverage[prefix] = {
            "input_hashes": {p.name: digest(p) for p in (meta_path, pts_path, rows_path)},
            "container_tick": str(tick),
            "max_schedule_error_seconds_exact": str(max(errors)),
            "source_frames_checked": len(frames),
            "native_pngs_checked": len(rows),
        }
    result = {
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "coverage": coverage,
        "python": platform.python_version(),
        "pillow": Image.__version__,
        "script_sha256": digest(Path(__file__)),
        "root_script_sha256": digest(BASE / "extract_frames.py"),
        "protocol_sha256": digest(BASE / "PROTOCOL.md"),
        "limits": "Independent schedule and decoded-pixel checks of root-generated fixtures only; no new video decode, cross-decoder validation, historical-source authentication, or causal/event measurement.",
    }
    with OUT.open("x") as file:
        json.dump(result, file, indent=2, sort_keys=True)
        file.write("\n")
    print(json.dumps({"status": result["status"], "checks": len(checks),
                      "source_timestamps": 72, "native_fixture_images": 40}))


if __name__ == "__main__":
    main()

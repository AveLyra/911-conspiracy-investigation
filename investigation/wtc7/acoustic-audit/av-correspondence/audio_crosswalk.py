#!/usr/bin/env python3
"""Declared digital-audio windows at visual edit coordinates; not sound attribution."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.io import wavfile

HERE = Path(__file__).resolve().parent
INPUTS = {
    "edited": (HERE.parent / "run01/edited-stereo.wav", 430, 1102500,
               "b8557ab9a0f2ac6dc9d3d59d0334de96431340ad34f2e5642c47a5a51a3a09dd"),
    "msnbc": (HERE.parent / "run01/msnbc-stereo.wav", 578, 1675800,
              "b9758e82432a354fc584b22529b03c84aefc7b192d8579d5b8f95de3b715b292"),
}
EDITS = [("edit435", "edited", Fraction(435)),
         ("edit441", "edited", Fraction(13256, 30)),
         ("edit580", "msnbc", Fraction(17423, 30))]


def pin(path):
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}


def index_at(time, start, rate):
    coordinate = (Fraction(time) - start) * rate
    if coordinate.denominator != 1:
        raise ValueError("Nonintegral declared sample boundary; do not silently round")
    return coordinate.numerator


def measure(samples, first, last):
    if not 0 <= first < last <= len(samples):
        raise ValueError("Window outside retained audio")
    values = samples[first:last].astype(np.float64)
    if values.ndim != 2 or values.shape[1] != 2 or not np.all(np.isfinite(values)):
        raise ValueError("Expected finite stereo array")
    rms = np.sqrt(np.mean(values * values, axis=0))
    peak = np.max(np.abs(values), axis=0)
    db = lambda v: [float(20 * np.log10(x)) if x > 0 else None for x in v]
    return {"first_sample": first, "end_sample_exclusive": last, "frames": last - first,
            "rms": rms.tolist(), "peak": peak.tolist(), "rms_dbfs": db(rms), "peak_dbfs": db(peak)}


def synthetic_checks():
    s = np.array([[0.25, -0.5]] * 8 + [[0.5, -0.25]] * 8, dtype=np.float32)
    pre, post = measure(s, 0, 8), measure(s, 8, 16)
    checks = {"known_pre_rms_peak": pre["rms"] == pre["peak"] == [0.25, 0.5],
              "known_post_rms_peak": post["rms"] == post["peak"] == [0.5, 0.25],
              "half_open_count": pre["frames"] == post["frames"] == 8,
              "exact_edit_index": index_at(Fraction(13256, 30), 430, 44100) == 523320}
    for name, action in [
        ("nonintegral_boundary_rejected", lambda: index_at(Fraction(1, 7), 0, 44101)),
        ("out_of_range_rejected", lambda: measure(s, -1, 8)),
        ("empty_window_rejected", lambda: measure(s, 8, 8)),
    ]:
        try:
            action()
        except ValueError:
            checks[name] = True
        else:
            checks[name] = False
    if not all(checks.values()):
        raise ValueError("Synthetic test failure")
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", choices=["audio01", "audio02"])
    args = parser.parse_args()
    out = HERE / args.run
    if out.exists():
        raise FileExistsError("Refusing existing audio result")
    checks = synthetic_checks()
    records, sources, arrays = [], {}, {}
    for label, (path, start, count, sha) in INPUTS.items():
        sources[label] = pin(path)
        if sources[label]["sha256"] != sha:
            raise ValueError("Retained WAV pin mismatch")
        rate, samples = wavfile.read(path)
        if rate != 44100 or samples.dtype != np.float32 or samples.shape != (count, 2):
            raise ValueError("Retained WAV contract mismatch")
        arrays[label] = samples
    for name, label, at in EDITS:
        start = INPUTS[label][1]
        sample = index_at(at, start, 44100)
        boundaries = [("before_0.1s", at - Fraction(1, 10), at),
                      ("after_0.1s", at, at + Fraction(1, 10))]
        boundaries += [(f"bin_{i:02d}", at - Fraction(1, 5) + Fraction(i, 50),
                         at - Fraction(1, 5) + Fraction(i + 1, 50)) for i in range(20)]
        windows = {}
        for window, begin, end in boundaries:
            windows[window] = {"source_begin_exact": str(begin), "source_end_exact": str(end),
                               **measure(arrays[label], index_at(begin, start, 44100), index_at(end, start, 44100))}
        records.append({"id": name, "wav": label, "visual_first_new_frame_pts_seconds": str(at),
                        "wav_start_seconds": start, "boundary_sample": sample, "windows": windows})
    for label, (path, _, _, _) in INPUTS.items():
        if pin(path) != sources[label]:
            raise ValueError("Input WAV changed")
    result = {"scope": "Uploaded-track coordinate crosswalk; no original A/V synchronization or source attribution",
              "sample_rate": 44100, "channel_order": ["L", "R"], "sources": sources,
              "code": pin(Path(__file__)), "protocol": pin(HERE / "PROTOCOL.md"),
              "refinement": pin(HERE / "REFINEMENT.md"), "synthetic_checks": checks,
              "runtime": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
              "edits": records}
    out.mkdir()
    (out / "measurements.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"run": args.run, "status": "complete", "edits": 3, "windows": 66, "checks": len(checks)}))


if __name__ == "__main__":
    main()

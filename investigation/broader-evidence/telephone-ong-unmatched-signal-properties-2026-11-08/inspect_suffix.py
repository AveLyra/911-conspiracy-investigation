"""Passive, in-memory analysis of one pinned court-resource suffix.

python inspect_suffix.py /path/to/court-flights.zip --helper /path/to/reproduce_resources.py
Requires NumPy and local FFmpeg/ffprobe. Never writes or plays source audio.
"""
import argparse
import hashlib
import importlib.util
import json
import platform
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
ARCHIVE_SHA = "3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801"
MEMBER_SHA = "8c844a2370852e55597a4aa73ef8b8ff0e6c03e3fec982a9cd98aeb937e5a3ec"
HELPER_SHA = "2af3d0339c5ca876255948a014205f8caa6ff019c1303e79a0ba774a22f36ade"
MP3_SHA = "b1340270d0e8f4b159bb4b057ea57ec227cd021fb12dc5fd37a46b7e3e9b78b5"
PCM_SHA = "3f63b0884240c467a8f3e2570314a1c2b6e814d79feb3327aff62ccab7cfc229"
VIEW_SHA = "3b9b7033b8ac59b93f8a2d3bba378cf5e7e3cc581b0bf417281759d9b8063990"
START, STOP, RATE = 1928909, 1980709, 8000
MAX_BYTES, MAX_RAW_MATCHES = 64 * 1024 * 1024, 10000


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def metrics(values):
    a = np.asarray(values, dtype=np.float64)
    require(a.ndim == 1 and a.size > 0 and np.isfinite(a).all(), "Invalid metric input")
    zeros = a == 0
    boundaries = np.diff(np.r_[False, zeros, False].astype(np.int8))
    lengths = np.flatnonzero(boundaries == -1) - np.flatnonzero(boundaries == 1)
    return {
        "samples": int(a.size), "numeric_zero_samples": int(zeros.sum()),
        "nonzero_samples": int((~zeros).sum()), "numeric_zero_fraction": float(zeros.mean()),
        "longest_numeric_zero_run_samples": int(lengths.max()) if lengths.size else 0,
        "mean": float(a.mean()), "rms": float(np.sqrt(np.mean(a * a))),
        "abs_peak": float(np.abs(a).max()), "minimum": float(a.min()), "maximum": float(a.max()),
    }


def exact_repeats(haystack, needle):
    require(needle and len(needle) % 4 == 0, "Need nonempty whole-sample target")
    raw_count, count, starts, pos = 0, 0, [], 0
    while True:
        hit = haystack.find(needle, pos)
        if hit == -1:
            complete = True
            break
        if raw_count == MAX_RAW_MATCHES:
            complete = False
            break
        raw_count += 1
        if hit % 4 == 0:
            count += 1
            if len(starts) < 10:
                starts.append(hit // 4)
        pos = hit + 1
    return {"complete": complete, "raw_byte_matches_examined": raw_count,
            "sample_aligned_matches": count, "first_up_to_10_start_samples": starts,
            "max_raw_matches": MAX_RAW_MATCHES}


def controls():
    z = metrics(np.zeros(32, dtype="<f4"))
    require(z["numeric_zero_samples"] == 32 and z["longest_numeric_zero_run_samples"] == 32
            and z["rms"] == 0, "Zero control")
    c = metrics(np.full(32, 0.5, dtype="<f4"))
    require(c["mean"] == 0.5 and c["rms"] == 0.5 and c["nonzero_samples"] == 32, "Constant control")
    pattern = np.array([1, 2], dtype="<f4").tobytes()
    repeat = exact_repeats(np.array([1, 2, 1, 2], dtype="<f4").tobytes(), pattern)
    require(repeat["complete"] and repeat["first_up_to_10_start_samples"] == [0, 2], "Repeat control")
    misaligned = exact_repeats(b"x" + pattern, pattern)
    require(misaligned["raw_byte_matches_examined"] == 1 and misaligned["sample_aligned_matches"] == 0,
            "Byte/sample alignment control")
    rng = np.random.Generator(np.random.PCG64(20261108))
    random_check = exact_repeats(rng.standard_normal(4096).astype("<f4").tobytes(),
                                 rng.standard_normal(128).astype("<f4").tobytes())
    require(random_check["complete"] and random_check["sample_aligned_matches"] == 0, "Random control")
    plus, minus = np.array([0.0], dtype="<f4"), np.array([-0.0], dtype="<f4")
    require(metrics(np.r_[plus, minus])["numeric_zero_samples"] == 2
            and plus.tobytes() != minus.tobytes(), "Signed zero control")
    try:
        metrics(np.array([float("nan")]))
    except ValueError:
        nonfinite = True
    else:
        nonfinite = False
    require(nonfinite, "Nonfinite rejection control")
    return {"all_passed": True, "zero": z, "constant": c, "known_repeat": repeat,
            "misaligned_repeat": misaligned, "seeded_random_nonrepeat": random_check,
            "signed_zero_numeric_equal_bytes_different": True, "nonfinite_rejected": nonfinite}


def invoke(executable, args, data=None):
    r = subprocess.run([executable, *args], input=data, capture_output=True, timeout=60)
    require(r.returncode == 0, f"{Path(executable).name} failed, stderr SHA256 {sha(r.stderr)}")
    require(len(r.stdout) <= MAX_BYTES, "Decoded output exceeds bound")
    return r


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", nargs="?")
    parser.add_argument("--helper")
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--controls-only", action="store_true")
    args = parser.parse_args()
    checked_controls = controls()
    if args.controls_only:
        print(json.dumps(checked_controls, indent=2, allow_nan=False))
        return
    require(args.archive and args.helper, "Archive and pinned helper are required")
    helper_path = Path(args.helper)
    require(sha(helper_path.read_bytes()) == HELPER_SHA, "Helper hash mismatch")
    spec = importlib.util.spec_from_file_location("pinned_court_helper", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    archive = Path(args.archive)
    require(archive.stat().st_size <= MAX_BYTES and sha(archive.read_bytes()) == ARCHIVE_SHA,
            "Archive size/hash mismatch")
    with zipfile.ZipFile(archive) as z:
        require(z.namelist().count("Ong.swf") == 1 and z.getinfo("Ong.swf").file_size <= MAX_BYTES,
                "Ambiguous/oversized member")
        raw = z.read("Ong.swf")
    require(sha(raw) == MEMBER_SHA, "Member hash mismatch")
    unpacked = helper.unpack(raw)
    tag_start = 8 + (5 + 4 * (unpacked[8] >> 3) + 7) // 8 + 4
    selected = [(offset, body) for code, offset, body, path in
                helper.walk(unpacked, tag_start, len(unpacked))
                if code == 14 and path == "root" and len(body) >= 9
                and struct.unpack_from("<H", body)[0] == 1]
    require(len(selected) == 1 and selected[0][0] == 26, "Unexpected event tag")
    offset, body = selected[0]
    require(body[2] >> 4 == 2, "Expected MP3 event")
    mp3 = body[9:]
    require(len(mp3) == 492856 and sha(mp3) == MP3_SHA, "Event MP3 mismatch")
    fields = {"declared_sample_count": struct.unpack_from("<I", body, 3)[0],
              "seek_samples": struct.unpack_from("<h", body, 7)[0], "rate_code": (body[2] >> 2) & 3}
    require(fields == {"declared_sample_count": 2726784, "seek_samples": 1669, "rate_code": 1},
            "Source fields differ from baseline")
    versions = {}
    for name, exe in (("ffmpeg", args.ffmpeg), ("ffprobe", args.ffprobe)):
        v = invoke(exe, ["-version"]).stdout
        versions[name] = {"version_line": v.decode().splitlines()[0], "version_output_sha256": sha(v)}
    commands = {
        "probe": ["-v", "error", "-select_streams", "a:0", "-show_entries",
                  "stream=codec_name,sample_rate,channels", "-of", "json", "pipe:0"],
        "native": ["-v", "warning", "-i", "pipe:0", "-map", "0:a:0", "-c:a", "pcm_s16le",
                   "-f", "s16le", "pipe:1"],
        "view": ["-v", "warning", "-i", "pipe:0", "-map", "0:a:0", "-ac", "1", "-ar", "8000",
                 "-c:a", "pcm_f32le", "-f", "f32le", "pipe:1"],
    }
    probe_run = invoke(args.ffprobe, commands["probe"], mp3)
    streams = json.loads(probe_run.stdout)["streams"]
    require(len(streams) == 1 and streams[0] == {"codec_name": "mp3", "sample_rate": "11025", "channels": 1},
            "Probe differs from baseline")
    native_run = invoke(args.ffmpeg, commands["native"], mp3)
    require(len(native_run.stdout) == 5459328 and sha(native_run.stdout) == PCM_SHA,
            "Native PCM mismatch: stop old-region measurement")
    view_run = invoke(args.ffmpeg, commands["view"], mp3)
    view = view_run.stdout
    require(len(view) == STOP * 4 and sha(view) == VIEW_SHA, "Analysis view mismatch: stop measurement")
    a = np.frombuffer(view, dtype="<f4")
    require(np.isfinite(a).all(), "Nonfinite source analysis value")
    suffix, context = a[START:STOP], a[START - (STOP - START):START]
    suffix_metrics, context_metrics = metrics(suffix), metrics(context)
    preceding_bytes = view[:START * 4]
    full_repeats = exact_repeats(preceding_bytes, view[START * 4:STOP * 4])
    blocks = []
    for start in range(START, STOP, RATE):
        stop = min(start + RATE, STOP)
        blocks.append({"event_analysis_sample_range": [start, stop], "is_full_8000_sample_block": stop-start == RATE,
                       "metrics": metrics(a[start:stop]),
                       "exact_earlier_repetition": exact_repeats(preceding_bytes, view[start*4:stop*4])})
    require(full_repeats["complete"] and all(b["exact_earlier_repetition"]["complete"] for b in blocks),
            "Exact search cap reached; source measurement is incomplete")
    result = {
        "source_url": "https://coop.vaed.uscourts.gov/moussaoui/flights.zip",
        "archive_sha256": ARCHIVE_SHA, "member": "Ong.swf", "member_sha256": MEMBER_SHA,
        "helper_sha256": HELPER_SHA, "script_sha256": sha(Path(__file__).read_bytes()),
        "software": {"Python": platform.python_version(), "NumPy": np.__version__, **versions},
        "source_tag_uncompressed_offset": offset, "source_fields_preserved": fields,
        "event_mp3_bytes": len(mp3), "event_mp3_sha256": MP3_SHA,
        "probe": streams[0], "native_pcm_bytes": len(native_run.stdout), "native_pcm_sha256": PCM_SHA,
        "native_samples": len(native_run.stdout)//2,
        "analysis_view_samples": a.size, "analysis_rate": RATE, "analysis_f32_sha256": VIEW_SHA,
        "commands": commands,
        "stderr_sha256": {"probe": sha(probe_run.stderr), "native": sha(native_run.stderr), "view": sha(view_run.stderr)},
        "source_seek_or_player_metadata_applied": False,
        "prior_locator": {"event_overlap": [27, START], "stream_overlap": [0, 1928882], "fit_rerun": False},
        "suffix_range": [START, STOP], "suffix_nominal_analysis_seconds": (STOP-START)/RATE,
        "suffix_metrics": suffix_metrics,
        "context_range": [START-(STOP-START), START], "context_metrics": context_metrics,
        "suffix_context_rms_ratio": suffix_metrics["rms"]/context_metrics["rms"] if context_metrics["rms"] else None,
        "earlier_search_range": [0, START], "whole_suffix_exact_earlier_repetition": full_repeats,
        "suffix_blocks": blocks, "controls": checked_controls,
        "scope": "Same-FFmpeg-family, reused-parser numeric properties of one derived event suffix; no listening, words, caller, playback, original custody, historical clocks or causal adjudication",
    }
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

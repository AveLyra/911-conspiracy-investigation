#!/usr/bin/env python3
"""PTS-checked whole-frame screening, adapted from the preserved Peskin helper."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
import subprocess

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
REFERENCE = REPO / "research/sherlock-wtc7-investigation/fire-originals/peskin/sample_every_second.py"
spec = importlib.util.spec_from_file_location("preserved_frame_helper", REFERENCE)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
identity, save = helper.identity, helper.save
FFMPEG, FFPROBE = "/opt/homebrew/bin/ffmpeg", "/opt/homebrew/bin/ffprobe"
MEDIA = REPO / "research/wtc7-video-comparison/media"
SOURCES = {
    "compilation": (MEDIA / "compilations/WTC Building 7 Collapse - 27 Angles [cmp7rV2aZhM].f136.mp4",
                    "1ea6063dac3847ee01969987bcee66991056d85ad61839ec301fb888a4456d87", 124393041),
    "comparator": (MEDIA / "comparators/explosive/Capital One Tower Implosion [rW_xXcS4y3A].f136.mp4",
                   "8560cd686a18c8fcc16fe802691e0f17f117c713b4cd1862017af24d391ce5a2", 4901052),
}
PLANS = {"compilation": [(434, 443, None), (580, 582, 4), (599, 610, 4)], "comparator": [(12, 15, 4)]}


class Runner:
    def __init__(self, out):
        self.out, self.commands = out, []

    def run(self, command, label, input_bytes=None):
        result = subprocess.run(command, input=input_bytes, capture_output=True, timeout=60)
        (self.out / f"{label}.stderr.local.txt").write_bytes(result.stderr)
        self.commands.append({"argv": command, "label": label, "exit": result.returncode, "stderr_bytes": len(result.stderr)})
        if result.returncode:
            raise RuntimeError(f"{label} failed; retain local diagnostics")
        return result


def probe(runner, source, label):
    meta = json.loads(runner.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=index,codec_type,codec_name,pix_fmt,width,height,time_base,start_pts,start_time,duration,sample_aspect_ratio,display_aspect_ratio,r_frame_rate,avg_frame_rate,color_range,color_space,color_transfer,color_primaries:stream_side_data=side_data_type,rotation",
         "-of", "json", str(source)], label + "-stream").stdout)
    frames = json.loads(runner.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_frames", "-show_entries",
         "frame=pts,best_effort_timestamp,width,height,pix_fmt", "-of", "json", str(source)], label + "-frames").stdout)
    save(runner.out / f"{label}-stream.json", meta)
    save(runner.out / f"{label}-all-frame-pts.json", frames)
    video = meta["streams"][0]
    if len(meta["streams"]) != 1 or video["codec_type"] != "video":
        raise ValueError("Expected one selected video stream")
    prior = None
    for frame in frames["frames"]:
        if "pts" not in frame or (prior is not None and frame["pts"] <= prior):
            raise ValueError("Absent/non-increasing source PTS")
        prior = frame["pts"]
        if any(frame[key] != video[key] for key in ("width", "height", "pix_fmt")):
            raise ValueError("Source decoded geometry/format changes")
    return video, frames["frames"]


def choose(frames, tick, plan):
    selected = []
    for start, end, rate in plan:
        subset, bins = [], set()
        for index, frame in enumerate(frames):
            time = frame["pts"] * tick
            if start <= time < end:
                slot = int(time * rate) if rate else None
                if rate is None or slot not in bins:
                    subset.append({"source_index": index, "source_pts": frame["pts"], "source_time_base": str(tick),
                                   "source_seconds_exact": str(time), "source_seconds": float(time),
                                   "interval": [start, end], "quarter_bin": slot})
                    bins.add(slot)
        if not subset or (rate and bins != set(range(start * rate, end * rate))):
            raise ValueError("Missing declared sample coverage")
        selected.extend(subset)
    if len({r["source_index"] for r in selected}) != len(selected):
        raise ValueError("Overlapping extraction intervals")
    return sorted(selected, key=lambda r: r["source_index"])


def extract(runner, source, label, video, frames, plan, known_pixels=None):
    rows = choose(frames, Fraction(video["time_base"]), plan)
    native = runner.out / label
    native.mkdir()
    expr = "+".join(f"eq(n,{row['source_index']})" for row in rows)
    command = [FFMPEG, "-nostdin", "-hide_banner", "-loglevel", "info", "-n", "-copyts", "-noautorotate",
               "-i", str(source), "-map", "0:v:0", "-an", "-vf", f"select='{expr}',format=rgb24,showinfo",
               "-frames:v", str(len(rows)), "-noautoscale", "-pix_fmt", "rgb24", "-fps_mode", "passthrough",
               "-enc_time_base:v", "demux", str(native / "frame-%04d.png")]
    result = runner.run(command, label + "-decode")
    log = result.stderr.decode(errors="replace")
    if re.search(r"corrupt|invalid data|error|warning|conceal", log, re.I):
        raise ValueError("Decode diagnostic requires review")
    clocks = re.findall(r"config in time_base: (\d+/\d+)", log)
    if len(set(clocks)) != 1 or Fraction(clocks[0]) != Fraction(video["time_base"]):
        raise ValueError("Filter/source clock mismatch")
    shown = re.findall(r"\[Parsed_showinfo_[^\]]+\]\s+n:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:([^ ]+).*?\bs:(\d+)x(\d+)\b", log)
    paths = sorted(native.glob("*.png"))
    if len(paths) != len(rows) or len(shown) != len(rows):
        raise ValueError("Selected/output/showinfo count mismatch")
    for i, (row, path, display) in enumerate(zip(rows, paths, shown)):
        n, pts, seconds, width, height = display
        if int(n) != i or int(pts) != row["source_pts"]:
            raise ValueError("Per-frame PTS/index mismatch")
        if (int(width), int(height)) != (video["width"], video["height"]):
            raise ValueError("Rendered dimensions changed")
        with Image.open(path) as im:
            im.load()
            if im.size != (video["width"], video["height"]) or im.mode != "RGB":
                raise ValueError("PNG contract mismatch")
            if known_pixels is not None and not np.array_equal(np.asarray(im), known_pixels[row["source_index"]]):
                raise ValueError("Synthetic RGB pixels differ")
        row.update({"png": str(path.relative_to(runner.out)), **identity(path)})
    save(runner.out / f"{label}-selected.json", rows)
    return rows


def sheets(out, label, rows):
    directory = out / (label + "-overview")
    directory.mkdir()
    for start in range(0, len(rows), 30):
        group = rows[start:start + 30]
        sheet = Image.new("RGB", (1600, 208 * ((len(group) + 4) // 5)), "white")
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(group):
            x, y = i % 5 * 320, i // 5 * 208
            with Image.open(out / row["png"]) as im:
                im.thumbnail((320, 180))
                sheet.paste(im, (x, y))
            draw.text((x + 3, y + 182), f"#{row['source_index']}  t={row['source_seconds']:.6f}s", fill="black")
        sheet.save(directory / f"sheet-{start:04d}.png")


def synthetic(runner):
    pixels = np.zeros((36, 48, 64, 3), dtype=np.uint8)
    for n in range(36):
        pixels[n, :, :, :] = [n * 7 % 256, n * 11 % 256, n * 13 % 256]
        pixels[n, 4:20, 5:30, :] = [255 - n, n, 90]
    checks = {}
    for offset in (0, 5):
        name = f"synthetic-{offset}"
        source = runner.out / (name + ".mkv")
        runner.run([FFMPEG, "-nostdin", "-v", "error", "-n", "-f", "rawvideo", "-pixel_format", "rgb24",
                    "-video_size", "64x48", "-framerate", "12", "-i", "pipe:0", "-vf", f"setpts=PTS+{offset}/TB",
                    "-c:v", "ffv1", "-pix_fmt", "bgr0", str(source)], name + "-generate", pixels.tobytes())
        video, frames = probe(runner, source, name)
        rows = extract(runner, source, name + "-selected", video, frames,
                       [(offset, offset + 2, 4), (offset + 2, offset + 3, None)], pixels)
        checks[name + "_20_expected_frames_and_pixels"] = len(rows) == 20
        checks[name + "_original_start_retained"] = rows[0]["source_seconds_exact"] == str(offset)
        try:
            choose(frames, Fraction(video["time_base"]), [(offset + 3, offset + 4, 4)])
        except ValueError:
            checks[name + "_missing_bins_rejected"] = True
        else:
            checks[name + "_missing_bins_rejected"] = False
    if not all(checks.values()):
        raise ValueError("Synthetic acceptance failed")
    save(runner.out / "synthetic-checks.json", checks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", choices=["run01", "run02"])
    args = parser.parse_args()
    out = HERE / args.run
    if out.exists():
        raise FileExistsError("Refusing existing output")
    for source, pin, size in SOURCES.values():
        if identity(source) != {"sha256": pin, "bytes": size}:
            raise ValueError("Source pin mismatch")
    out.mkdir()
    runner = Runner(out)
    receipt = {"protocol": identity(HERE / "PROTOCOL.md"), "script": identity(Path(__file__)), "reference_helper": identity(REFERENCE),
               "python": platform.python_version(), "pillow": Image.__version__, "numpy": np.__version__, "sources_before": {},
               "binary_pins": {p: identity(Path(p)) for p in (FFMPEG, FFPROBE)}, "status": "started"}
    save(out / "start.json", receipt)
    try:
        synthetic(runner)
        for label, (source, pin, size) in SOURCES.items():
            receipt["sources_before"][label] = identity(source)
            video, frames = probe(runner, source, label)
            if video["width"] != 1280 or video["height"] != 720 or video["sample_aspect_ratio"] != "1:1":
                raise ValueError("Historical source geometry differs from planned contract")
            rows = extract(runner, source, label, video, frames, PLANS[label])
            if len(rows) != (322 if label == "compilation" else 12):
                raise ValueError("Historical frame count differs from protocol")
            sheets(out, label, rows)
        receipt["sources_after"] = {key: identity(source) for key, (source, _, _) in SOURCES.items()}
        if receipt["sources_before"] != receipt["sources_after"]:
            raise ValueError("Source changed")
        receipt["status"] = "complete"
    except Exception as exc:
        receipt["status"] = "failed"
        receipt["failure_type"] = type(exc).__name__
        receipt["failure_category"] = str(exc) if isinstance(exc, ValueError) else "Inspect local diagnostic"
        raise
    finally:
        receipt["commands"] = runner.commands
        receipt["products"] = {str(p.relative_to(out)): identity(p) for p in sorted(out.rglob("*"))
                               if p.is_file() and ".local." not in p.name and p.name not in ("start.json", "receipt.json")}
        save(out / "receipt.json", receipt)
    print(json.dumps({"run": args.run, "status": "complete", "historical_frames": 334}))


if __name__ == "__main__":
    main()

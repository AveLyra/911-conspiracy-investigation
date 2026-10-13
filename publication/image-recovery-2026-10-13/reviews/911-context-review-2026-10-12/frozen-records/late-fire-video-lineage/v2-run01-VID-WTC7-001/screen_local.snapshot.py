#!/usr/bin/env python3
"""Local full-decode screening derivatives; never historical clock/causal evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import re
import subprocess
import sys
import traceback
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageDraw

FFMPEG = Path("/opt/homebrew/bin/ffmpeg")
FFPROBE = Path("/opt/homebrew/bin/ffprobe")
PROTOCOL_SHA256 = "f81d1e7e1d8ae914cd62e182cd6f2db642bd60e19737d204f18d3b97d1e70486"
REVISION = "v2-single-terminal-empty-token"
GRAMMAR_DECLARATION = Path(__file__).with_name("GRAMMAR-FOLLOWUP.md")
GRAMMAR_DECLARATION_SHA256 = "8c1f26316c6ace3f68fb06881b9eed465827672bb7d7168aa250275ae8efa723"
STREAM_FIELDS = "index,codec_type,codec_name,pix_fmt,width,height,avg_frame_rate,r_frame_rate,time_base,start_pts,start_time,duration,nb_frames,field_order,sample_aspect_ratio,display_aspect_ratio,color_range,color_space,color_transfer,color_primaries,chroma_location"
SHOW_FRAME = re.compile(r"\[Parsed_showinfo_[^\]]+\].*?\bn:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:(\S+).*?\bs:(\d+)x(\d+)\b")
SHOW_BASE = re.compile(r"config in time_base:\s*(\d+/\d+)")


class CheckError(Exception):
    """Only fixed category strings, never incidental source metadata."""


def require(condition, category):
    if not condition:
        raise CheckError(category)


def identity(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return {"bytes": Path(path).stat().st_size, "sha256": digest.hexdigest()}


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def copy_exclusive(source, destination):
    with Path(source).open("rb") as src, Path(destination).open("xb") as dst:
        for block in iter(lambda: src.read(1024 * 1024), b""):
            dst.write(block)


def read_selection(path):
    value = json.loads(Path(path).read_text())
    require(isinstance(value, dict) and isinstance(value.get("sources"), list), "selection_schema")
    require(1 <= len(value["sources"]) <= 8, "selection_source_count")
    ids, paths, hashes = set(), set(), set()
    for row in value["sources"]:
        require(isinstance(row, dict), "selection_source_schema")
        require(isinstance(row.get("id"), str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", row["id"]), "selection_id")
        require(isinstance(row.get("path"), str) and Path(row["path"]).is_absolute(), "selection_path")
        require(isinstance(row.get("sha256"), str) and re.fullmatch(r"[a-f0-9]{64}", row["sha256"]), "selection_sha256")
        require(type(row.get("bytes")) is int and row["bytes"] > 0, "selection_bytes")
        require(type(row.get("step_seconds")) is int and row["step_seconds"] in (2, 15), "selection_step")
        resolved = str(Path(row["path"]).resolve())
        require(row["id"] not in ids and resolved not in paths and row["sha256"] not in hashes, "selection_duplicate")
        ids.add(row["id"])
        paths.add(resolved)
        hashes.add(row["sha256"])
    return value


def parse_positive_fraction(value):
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError, TypeError):
        raise CheckError("time_base_invalid") from None
    require(result > 0, "time_base_invalid")
    return result


def frame_plan(lines, tick, step, dimensions):
    """Exact rational planning from all decoded source frame PTS; no float bins."""
    samples, counts = [], {}
    terminal_delimiter_records = 0
    previous = None
    total = 0
    first_pts = last_pts = None
    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split("|")
        if parts[-1] == "":
            require(len(parts) == 4 and all(parts[:-1]), "frame_inventory_terminal_delimiter_shape")
            parts = parts[:-1]
            terminal_delimiter_records += 1
        require(all("=" in item for item in parts), "frame_inventory_malformed")
        pairs = [item.split("=", 1) for item in parts]
        require(len({key for key, value in pairs}) == len(pairs), "frame_inventory_duplicate_field")
        fields = dict(pairs)
        require(set(fields) == {"pts", "width", "height"}, "frame_inventory_fields")
        require(all(re.fullmatch(r"-?\d+", fields[key]) for key in fields), "frame_inventory_integer")
        pts, width, height = int(fields["pts"]), int(fields["width"]), int(fields["height"])
        require((width, height) == dimensions, "source_geometry_change")
        require(previous is None or pts > previous, "source_pts_duplicate_or_out_of_order")
        exact = pts * tick
        bin_number = math.floor(exact / step)
        counts[bin_number] = counts.get(bin_number, 0) + 1
        if counts[bin_number] == 1:
            samples.append({"sample_index": len(samples), "source_frame_index": total,
                            "source_pts": pts, "source_time_base": str(tick),
                            "source_seconds_exact": str(exact), "bin": bin_number,
                            "bin_start_seconds": bin_number * step,
                            "bin_end_seconds_exclusive": (bin_number + 1) * step})
        if first_pts is None:
            first_pts = pts
        last_pts = previous = pts
        total += 1
    require(total > 0, "source_no_frames")
    first_bin, last_bin = samples[0]["bin"], samples[-1]["bin"]
    require(last_bin - first_bin <= 1000000, "source_bin_span_unbounded")
    return samples, {"recognized_terminal_delimiter_records": terminal_delimiter_records,
                     "decoded_frame_count": total, "first_source_pts": first_pts,
                     "last_source_pts": last_pts, "observed_bin_range": [first_bin, last_bin],
                     "occupied_bin_count": len(samples),
                     "frame_count_per_occupied_bin": [{"bin": k, "frames": v} for k, v in counts.items()],
                     "empty_bins_within_observed_range": [k for k in range(first_bin, last_bin + 1) if k not in counts],
                     "range_note": "No inference about bins before first or after last decoded frame; empty internal bins are not filled."}


def validate_display_time(text, exact):
    try:
        number = Decimal(text)
        require(number.is_finite(), "display_timestamp_invalid")
        tolerance = Fraction(Decimal(1).scaleb(number.as_tuple().exponent)) / 2
        require(abs(Fraction(number) - exact) <= tolerance, "display_timestamp_mismatch")
    except (InvalidOperation, ValueError, OverflowError):
        raise CheckError("display_timestamp_invalid") from None


def reconcile_showinfo(log, rows, tick, dimensions):
    bases = SHOW_BASE.findall(log)
    require(bool(bases) and all(parse_positive_fraction(base) == tick for base in bases), "filter_time_base_mismatch")
    matches = SHOW_FRAME.findall(log)
    require(len(matches) == len(rows), "selected_frame_count_mismatch")
    for index, (match, row) in enumerate(zip(matches, rows)):
        number, pts, shown, width, height = match
        require(int(number) == index and int(pts) == row["source_pts"], "selected_frame_pts_or_order_mismatch")
        require((int(width), int(height)) == dimensions, "selected_frame_geometry_mismatch")
        validate_display_time(shown, row["source_pts"] * tick)


def classify_decode_diagnostics(log):
    """Permit one reviewed software-fallback notice; retain every raw log line."""
    fallback_count = 0
    for line in log.splitlines():
        if not re.search(r"\[(?:warning|error|fatal|panic)\]", line):
            continue
        if re.fullmatch(r"(?:\[swscaler @ 0x[0-9a-f]+\]\s*)+\[warning\] No accelerated colorspace conversion found from yuv420p to rgb24\.", line):
            fallback_count += 1
        else:
            raise CheckError("decode_diagnostic_review")
    return {"reviewed_software_colorspace_fallback_notices": fallback_count,
            "unreviewed_warning_or_error_count": 0}


def command_run(argv, destination, label, receipt):
    with (destination / f"{label}.stdout").open("xb") as stdout, (destination / f"{label}.stderr").open("xb") as stderr:
        result = subprocess.run(argv, stdout=stdout, stderr=stderr, check=False)
    receipt["commands"].append({"argv": argv, "returncode": result.returncode,
                                "stdout": f"{label}.stdout", "stderr": f"{label}.stderr"})
    require(result.returncode == 0, f"{label}_nonzero_exit")
    return destination / f"{label}.stdout", destination / f"{label}.stderr"


def validate_png(path, dimensions):
    with Image.open(path) as frame:
        frame.load()
        require(frame.format == "PNG" and frame.mode == "RGB" and frame.size == dimensions, "native_png_contract")


def make_overviews(destination, source_id, rows):
    sheets = []
    for start in range(0, len(rows), 12):
        sheet = Image.new("RGB", (960, 1120), "white")
        draw = ImageDraw.Draw(sheet)
        subset = rows[start:start + 12]
        for index, row in enumerate(subset):
            x, y = (index % 3) * 320, (index // 3) * 280
            with Image.open(destination / row["png"]) as frame:
                frame.thumbnail((320, 240), resample=Image.Resampling.LANCZOS)
                sheet.paste(frame, (x, y))
            draw.text((x + 3, y + 243), f"{source_id} / sample {row['sample_index']:04d}", fill="black")
            draw.text((x + 3, y + 256), f"bin {row['bin']} / PTS {row['source_pts']}", fill="black")
            draw.text((x + 3, y + 268), f"source seconds {row['source_seconds_exact']}", fill="black")
        path = destination / "overview" / f"sheet-{start // 12:04d}.png"
        with path.open("xb") as stream:
            sheet.save(stream, format="PNG")
        sheets.append({"path": str(path.relative_to(destination)),
                       "sample_indices": [row["sample_index"] for row in subset], **identity(path)})
    return sheets


def screen_source(source, destination):
    destination.mkdir(exist_ok=False)
    (destination / "native").mkdir()
    (destination / "overview").mkdir()
    record = {"source_id": source["id"], "source": source, "commands": [], "status": "started"}
    save(destination / "start.json", record)
    phase = "source_hash"
    try:
        expected = {key: source[key] for key in ("bytes", "sha256")}
        record["source_before"] = identity(source["path"])
        require(record["source_before"] == expected, "source_pin_mismatch")
        phase = "probe"
        argv = [str(FFPROBE), "-v", "warning", "-show_entries",
                f"stream={STREAM_FIELDS}:format=duration,start_time,size:stream_tags=:stream_disposition=:format_tags=:stream_side_data=",
                "-of", "json", source["path"]]
        stdout, stderr = command_run(argv, destination, "probe", record)
        require(not stderr.read_bytes().strip(), "probe_diagnostic_review")
        probe = json.loads(stdout.read_text())
        videos = [stream for stream in probe.get("streams", []) if stream.get("codec_type") == "video"]
        require(len(videos) == 1, "video_stream_count")
        video = videos[0]
        dimensions = video["width"], video["height"]
        require(all(type(value) is int and value > 0 for value in dimensions) and math.prod(dimensions) <= 10000000, "source_dimensions")
        tick = parse_positive_fraction(video["time_base"])
        record["allowlisted_probe"] = probe
        phase = "frame_inventory"
        argv = [str(FFPROBE), "-v", "warning", "-select_streams", "v:0", "-show_frames",
                "-show_entries", "frame=pts,width,height:frame_tags=:frame_side_data=",
                "-of", "compact=p=0:nk=0", source["path"]]
        stdout, stderr = command_run(argv, destination, "frame-inventory", record)
        require(not stderr.read_bytes().strip(), "frame_inventory_diagnostic_review")
        with stdout.open() as lines:
            rows, coverage = frame_plan(lines, tick, source["step_seconds"], dimensions)
        record["coverage"] = coverage
        save(destination / "planned-frames.json", rows)
        phase = "decode"
        expression = "+".join(f"eq(n,{row['source_frame_index']})" for row in rows)
        argv = [str(FFMPEG), "-nostdin", "-hide_banner", "-nostats", "-loglevel", "level+info", "-n",
                "-copyts", "-noautorotate", "-i", source["path"], "-map", "0:v:0", "-an", "-sn", "-dn",
                "-map_metadata", "-1", "-map_chapters", "-1", "-vf", f"select='{expression}',showinfo",
                "-noautoscale", "-pix_fmt", "rgb24", "-fps_mode", "passthrough", "-enc_time_base:v", "demux",
                str(destination / "native" / "frame-%06d.png")]
        stdout, stderr = command_run(argv, destination, "decode", record)
        log = stderr.read_text(errors="replace")
        record["diagnostic_summary"] = classify_decode_diagnostics(log)
        reconcile_showinfo(log, rows, tick, dimensions)
        phase = "native_reconciliation"
        paths = sorted((destination / "native").iterdir())
        require(len(paths) == len(rows), "native_png_count")
        for index, (row, path) in enumerate(zip(rows, paths), 1):
            require(path.name == f"frame-{index:06d}.png", "native_png_sequence")
            validate_png(path, dimensions)
            row.update({"png": str(path.relative_to(destination)), "width": dimensions[0], "height": dimensions[1], **identity(path)})
        save(destination / "frames.json", rows)
        phase = "overviews"
        record["overview_sheets"] = make_overviews(destination, source["id"], rows)
        phase = "source_hash_after"
        record["source_after"] = identity(source["path"])
        require(record["source_after"] == expected, "source_changed")
        record["status"] = "completed"
        record["sample_count"] = len(rows)
        record["products"] = {str(path.relative_to(destination)): identity(path) for path in sorted(destination.rglob("*")) if path.is_file()}
        save(destination / "receipt.json", record)
        return {"source_id": source["id"], "status": "completed", "samples": len(rows), "overview_sheets": len(record["overview_sheets"]), "receipt": identity(destination / "receipt.json")}
    except BaseException as error:
        record.update({"status": "failed", "phase": phase, "category": str(error) if isinstance(error, CheckError) else "unexpected_exception", "exception_type": type(error).__name__})
        try:
            record["source_after"] = identity(source["path"])
            record["source_after_matches_pin"] = record["source_after"] == {key: source[key] for key in ("bytes", "sha256")}
        except Exception:
            record["source_after_status"] = "unavailable"
        with (destination / "failure-traceback-local.txt").open("x") as stream:
            traceback.print_exc(file=stream)
        save(destination / "failure.json", record)
        raise


def run(selection_path, protocol_path, destination, source_ids=None):
    require(destination.is_absolute(), "run_path_absolute_required")
    destination.mkdir(exist_ok=False)  # Never reuse, erase, or repair a run.
    record = {"status": "started", "phase": "preflight", "sources": [], "commands": [],
              "revision": REVISION,
              "python_version": platform.python_version(), "pillow_version": Image.__version__,
              "method": "Two complete decoder passes from file start; exact rational source-PTS bins; first decoded source frame per occupied bin.",
              "derivatives": "Native stored-raster RGB PNG; RGB conversion is uncalibrated. Overviews are 3 columns by 4 rows, max 320x240 LANCZOS thumbnails, without SAR correction.",
              "limits": "No historical clock, original custody, original cadence, continuous-event duration, calibrated color/area or causal claim. ffprobe and ffmpeg share decoder libraries. Coarse samples can miss short events. Raw diagnostics remain local-only."}
    save(destination / "start.json", record)
    sources = []
    try:
        selection = read_selection(selection_path)
        sources = selection["sources"]
        record["selection_identity"] = identity(selection_path)
        record["protocol_identity"] = identity(protocol_path)
        record["grammar_declaration_identity"] = identity(GRAMMAR_DECLARATION)
        require(record["grammar_declaration_identity"]["sha256"] == GRAMMAR_DECLARATION_SHA256, "grammar_declaration_pin_mismatch")
        require(record["protocol_identity"]["sha256"] == PROTOCOL_SHA256, "protocol_pin_mismatch")
        require(selection.get("protocol_sha256", PROTOCOL_SHA256) == PROTOCOL_SHA256, "selection_protocol_pin_mismatch")
        record["selection_source_count"] = len(sources)
        if source_ids is not None:
            require(len(set(source_ids)) == len(source_ids) and set(source_ids).issubset({source["id"] for source in sources}), "source_subset_invalid")
            sources = [source for source in sources if source["id"] in source_ids]
        record["requested_source_ids"] = [source["id"] for source in sources]
        script = Path(__file__).resolve()
        record["script_identity"] = identity(script)
        for source, name in ((selection_path, "selection.snapshot.json"), (protocol_path, "protocol.snapshot.md"), (script, "screen_local.snapshot.py"), (GRAMMAR_DECLARATION, "grammar-followup.snapshot.md")):
            copy_exclusive(source, destination / name)
        record["tools"] = {}
        for tool in (FFMPEG, FFPROBE):
            stdout, stderr = command_run([str(tool), "-version"], destination, tool.name + "-version", record)
            record["tools"][tool.name] = {"path": str(tool), **identity(tool), "version": stdout.read_text().splitlines()[0]}
        record["source_pins_before"] = {}
        for source in sources:
            actual = identity(source["path"])
            record["source_pins_before"][source["id"]] = actual
            require(actual == {key: source[key] for key in ("bytes", "sha256")}, "source_pin_mismatch")
        save(destination / "preflight.json", record)
        record["phase"] = "sources"
        for source in sources:
            record["sources"].append(screen_source(source, destination / source["id"]))
            print(json.dumps(record["sources"][-1]), flush=True)
        record["phase"] = "final_pins"
        require(identity(selection_path) == record["selection_identity"] and identity(protocol_path) == record["protocol_identity"] and identity(script) == record["script_identity"] and identity(GRAMMAR_DECLARATION) == record["grammar_declaration_identity"], "control_changed")
        record["source_pins_after"] = {source["id"]: identity(source["path"]) for source in sources}
        require(record["source_pins_after"] == record["source_pins_before"], "source_changed")
        record["status"] = "completed"
        record.pop("phase")
        record["products"] = {str(path.relative_to(destination)): identity(path) for path in sorted(destination.rglob("*")) if path.is_file()}
        save(destination / "receipt.json", record)
        return record
    except BaseException as error:
        record.update({"status": "failed", "category": str(error) if isinstance(error, CheckError) else "unexpected_exception", "exception_type": type(error).__name__})
        record["source_pins_after_failure"] = {}
        for source in sources:
            try:
                record["source_pins_after_failure"][source["id"]] = identity(source["path"])
            except Exception:
                record["source_pins_after_failure"][source["id"]] = {"status": "unavailable"}
        with (destination / "failure-traceback-local.txt").open("x") as stream:
            traceback.print_exc(file=stream)
        save(destination / "failure.json", record)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--source-id", action="append", help="Optional declared source ID; repeat for a subset. Selection snapshot remains unchanged.")
    args = parser.parse_args()
    try:
        record = run(args.selection, args.protocol, args.run, args.source_id)
        print(json.dumps({"status": "completed", "sources": len(record["sources"])}))
    except BaseException as error:
        category = str(error) if isinstance(error, CheckError) else "destination_exists" if isinstance(error, FileExistsError) else "unexpected_exception"
        print(json.dumps({"status": "failed", "category": category, "exception_type": type(error).__name__}))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

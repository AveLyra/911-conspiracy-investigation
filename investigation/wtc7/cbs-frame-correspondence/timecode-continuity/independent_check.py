"""Separately authored arithmetic audit; no producer imports or media access.

The author also implemented upstream DIF extraction/storage: those are common
dependencies, not independent historical evidence. This checker operates only
on the pinned JSON candidate inventory after explicit execution authorization.
Issue-code ordering is immaterial; all numeric values, positions and counts are
compared. Drop-frame ordinals sum completed minute lengths instead of using the
producer's nominal-count-minus-skipped-labels formula.
"""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import re


UNIT = Path(__file__).resolve().parent
EXPECTED_RESULT_SHA = "175808f97cb938071d699e9830593d173bcac851e221e97a9a55535b0cc2d34e"
LANES = ("nd", "df", "selected")
NOMINAL_PERIOD = Fraction(1001, 30000)
REQUIRED = {
    "PLAN.md", "references.md", "timecode.py", "test_timecode.py",
    "sources/ffmpeg-n7.1-timecode.c", "sources/ffmpeg-n7.1-timecode.h",
    "sources/ffmpeg-n7.1-dv.c",
    "../dv-metadata/sources/ffmpeg-n7.1-libavformat-dvenc.c",
    "../dv-metadata/sources/ffmpeg-n7.1-libavcodec-dv_profile.c",
    "../dv-metadata/v2/freeze.json", "../dv-metadata/independent-audit.json",
    "../dv-metadata/v2/inventory-summary.json", "../sibling-lineage/results.json",
    "../sibling-lineage/inputs.json",
} | {f"../dv-metadata/v2/results/clip{n}-result.json" for n in range(1, 9)}


def ensure(condition, message):
    if not condition:
        raise ValueError(message)


def ranges(parts):
    return [name + "_range" for name, value, ceiling in
            zip(("h", "m", "s", "f"), parts, (23, 59, 59, 29))
            if type(value) is not int or not 0 <= value <= ceiling]


def ordinal(parts, drop):
    """Count labels in complete minutes, then valid labels in this minute."""
    problems = ranges(parts)
    if problems:
        return None, problems
    hour, minute, second, frame = parts
    whole_minutes = hour * 60 + minute
    shortened = drop and whole_minutes % 10 != 0
    if shortened and second == 0 and frame < 2:
        return None, ["omitted_drop_frame_label"]
    completed = sum(1798 if drop and index % 10 else 1800
                    for index in range(whole_minutes))
    in_minute = second * 30 + frame - (2 if shortened else 0)
    return completed + in_minute, []


def decode(raw_hex):
    ensure(isinstance(raw_hex, str) and re.fullmatch(r"13[0-9a-f]{8}", raw_hex),
           "not a fixed five-byte timecode candidate")
    payload = bytes.fromhex(raw_hex)[1:]
    values, invalid = {}, []
    # Decode bytes directly, without a packed-word conversion or library helper.
    for name, byte, mask in zip(("f", "s", "m", "h"), payload,
                                (0x3f, 0x7f, 0x7f, 0x3f)):
        tens, units = divmod(byte & mask, 16)
        values[name] = tens * 10 + units if tens <= 9 and units <= 9 else None
        if values[name] is None:
            invalid.append(name + "_invalid_bcd")
    parts = [values[name] for name in ("h", "m", "s", "f")]
    problems = invalid + ranges(parts)
    nd, nd_problems = ordinal(parts, False)
    df, df_problems = ordinal(parts, True)
    if invalid:
        nd_problems = invalid + nd_problems
        df_problems = invalid + df_problems
    drop = bool(payload[0] & 0x40)
    flags = sum((byte & mask) * 256 ** (3 - index)
                for index, (byte, mask) in enumerate(zip(payload,
                                                        (0xc0, 0x80, 0x80, 0xc0))))
    return {"raw_hex": raw_hex, "components_h_m_s_f": parts,
            "component_issues": problems, "drop_bit": drop,
            "positional_flag_hex": f"{flags:08x}", "nd": nd, "df": df,
            "selected": df if drop else nd, "nd_issues": nd_problems,
            "df_issues": df_problems,
            "selected_issues": df_problems if drop else nd_problems}


def parse_header(text):
    if not isinstance(text, str) or not re.fullmatch(
            r"[0-9]{2};[0-9]{2};[0-9]{2};[0-9]{2}", text):
        return {"text": text, "components_h_m_s_f": None,
                "issues": ["unsupported_native_label_syntax"]}
    parts = list(map(int, text.split(";")))
    return {"text": text, "components_h_m_s_f": parts, "issues": ranges(parts)}


def reconstruct(document, expected_frames):
    count = document["result"]["frames"]
    ensure(type(count) is int and 1 <= count <= 2500 and count == expected_frames,
           "fixed frame count mismatch")
    ordered = [None] * count
    for candidate in document["result"]["target_variants"]:
        raw = candidate["raw_hex"]
        ensure(isinstance(raw, str), "nontext raw candidate")
        if not raw.startswith("13"):
            continue
        ensure(re.fullmatch(r"13[0-9a-f]{8}", raw), "candidate encoding")
        ensure(candidate["area"] == "subcode", "timecode outside admitted area")
        index = candidate["first_frame"]
        ensure(type(index) is int and 0 <= index < count, "candidate frame index")
        ensure(type(candidate["last_frame"]) is int and candidate["last_frame"] == index,
               "candidate spans multiple frames")
        ensure(type(candidate["frames_present"]) is int and candidate["frames_present"] == 1,
               "candidate frame population")
        ensure(type(candidate["occurrences"]) is int and candidate["occurrences"] == 40,
               "candidate repetition population")
        ensure(ordered[index] is None, "conflicting candidate at frame")
        ordered[index] = raw
    ensure(all(raw is not None for raw in ordered), "missing candidate frame")
    ensure(len(set(ordered)) == count, "raw-value uniqueness differs from fixed inventory")
    return ordered


def transitions(rows):
    edges = []
    for index, (left, right) in enumerate(zip(rows, rows[1:])):
        mode_changed = left["drop_bit"] != right["drop_bit"]
        selected_difference = (None if left["selected"] is None or right["selected"] is None
                               else right["selected"] - left["selected"])
        edge = {"left_frame": index, "right_frame": index + 1,
                "drop_bit_changed": mode_changed,
                "selected_raw_difference": selected_difference,
                "flag_xor_hex": f"{int(left['positional_flag_hex'], 16) ^ int(right['positional_flag_hex'], 16):08x}"}
        for lane in LANES:
            first, last = left[lane], right[lane]
            delta = None if first is None or last is None else last - first
            if lane == "selected" and mode_changed:
                delta = None
            drop = lane == "df" or (lane == "selected" and left["drop_bit"])
            day = sum(1798 if drop and minute % 10 else 1800 for minute in range(1440))
            edge[lane + "_delta"] = delta
            edge[lane + "_possible_daily_rollover"] = delta == 1 - day
        edges.append(edge)
    return edges


def compute_clip(document, header):
    video = header["video_header"]
    ensure(all(type(video[key]) is int and video[key] > 0
               for key in ("scale", "rate", "length")), "invalid video count/rate")
    ensure(document["clip"] == header["clip"], "clip/header identity mismatch")
    raw_values = reconstruct(document, video["length"])
    rows = [{"frame": index, **decode(raw)} for index, raw in enumerate(raw_values)]
    edges = transitions(rows)
    lane_results = {}
    for lane in LANES:
        lane_results[lane] = {
            "invalid_frames": [r["frame"] for r in rows if r[lane] is None],
            "one_step_edges": sum(e[lane + "_delta"] == 1 for e in edges),
            "non_one_step_right_frames": [e["right_frame"] for e in edges
                                           if e[lane + "_delta"] not in (None, 1)],
            "unavailable_right_frames": [e["right_frame"] for e in edges
                                          if e[lane + "_delta"] is None],
            "possible_daily_rollover_right_frames": [e["right_frame"] for e in edges
                                                       if e[lane + "_possible_daily_rollover"]],
            "first_ordinal": rows[0][lane], "last_ordinal": rows[-1][lane],
        }
    labels = {}
    for key in ("tc_O", "tc_A"):
        entries = header["fields"][key]
        ensure(len(entries) == 1, "missing or multiple header labels")
        label = parse_header(entries[0]["prefix_utf8"])
        label["matches_first_components"] = (not label["issues"]
                                             and not rows[0]["component_issues"]
                                             and label["components_h_m_s_f"] == rows[0]["components_h_m_s_f"])
        for lane, drop in (("nd", False), ("df", True)):
            if label["components_h_m_s_f"] is None:
                number, problems = None, label["issues"]
            else:
                number, problems = ordinal(label["components_h_m_s_f"], drop)
            label[lane + "_ordinal"] = number
            label[lane + "_issues"] = problems
            label[lane + "_start_difference"] = (None if number is None or rows[0][lane] is None
                                                   else rows[0][lane] - number)
        labels[key] = label
    count = len(rows)
    period = Fraction(video["scale"], video["rate"])
    summary = {
        "clip": document["clip"], "frames": count, "edges": len(edges),
        "first": rows[0], "last": rows[-1],
        "component_invalid_frames": [r["frame"] for r in rows if r["component_issues"]],
        "drop_bit_counts": dict(Counter(str(r["drop_bit"]) for r in rows)),
        "positional_flag_counts": dict(Counter(r["positional_flag_hex"] for r in rows)),
        "flag_change_right_frames": [e["right_frame"] for e in edges if int(e["flag_xor_hex"], 16)],
        "lanes": lane_results, "header_comparisons": labels,
        "avi_frame_period": str(period), "nominal_dv_frame_period": str(NOMINAL_PERIOD),
        "period_difference_avi_minus_nominal": str(period - NOMINAL_PERIOD),
        "first_to_last_avi_span": str((count - 1) * period),
        "first_to_last_nominal_dv_span": str((count - 1) * NOMINAL_PERIOD),
        "container_duration_avi": str(count * period),
    }
    return {"summary": summary, "frames": rows, "transitions": edges}


def compare_clips(clips):
    pairs = []
    for left, right in itertools.combinations(clips, 2):
        pair = {"left_clip": left["summary"]["clip"],
                "right_clip": right["summary"]["clip"], "lanes": {}}
        for lane in LANES:
            a = [r[lane] for r in left["frames"]]
            b = [r[lane] for r in right["frames"]]
            available = None not in a and None not in b
            if lane == "selected":
                available = available and len({r["drop_bit"] for c in (left, right)
                                                for r in c["frames"]}) == 1
            pair["lanes"][lane] = None if not available else {
                "start_difference": b[0] - a[0],
                "all_left_ordinals_before_right": max(a) < min(b),
                "boundary_counter_distance": b[0] - a[-1],
                "unrepresented_counter_positions": b[0] - a[-1] - 1,
            }
        pairs.append(pair)
    return pairs


def compare(actual, expected, path="result"):
    """Compare all fields; diagnostic issue-code order is not substantive."""
    if isinstance(expected, dict):
        ensure(isinstance(actual, dict) and actual.keys() == expected.keys(), path + " keys differ")
        for key in expected:
            compare(actual[key], expected[key], path + "." + key)
    elif isinstance(expected, list):
        ensure(isinstance(actual, list), path + " is not a list")
        if path.endswith("issues"):
            ensure(sorted(actual) == sorted(expected), path + " issue codes differ")
        else:
            ensure(len(actual) == len(expected), path + " length differs")
            for index, (got, want) in enumerate(zip(actual, expected)):
                compare(got, want, f"{path}[{index}]")
    else:
        ensure(type(actual) is type(expected) and actual == expected,
               f"{path}: {actual!r} != {expected!r}")


def pin(path):
    with path.open("rb") as stream:
        value = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"bytes": path.stat().st_size, "sha256": value}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorized-result-audit", action="store_true", required=True)
    parser.parse_args()
    destination = UNIT / "independent-audit01.json"
    ensure(not destination.exists() and not destination.is_symlink(), "audit output already exists")
    result_path = UNIT / "result01.json"
    result_pin = pin(result_path)
    ensure(result_pin["sha256"] == EXPECTED_RESULT_SHA and result_pin["bytes"] <= 8 * 1024 * 1024,
           "result pin/cap mismatch")
    freeze_path = UNIT / "freeze.json"
    freeze_pin = pin(freeze_path)
    freeze = json.loads(freeze_path.read_text())
    ensure(set(freeze["files"]) == REQUIRED, "unexpected frozen population")
    for name, expected in freeze["files"].items():
        ensure(pin(UNIT / name) == expected, "input pin mismatch: " + name)
    checker_files = {name: pin(UNIT / name)
                     for name in ("independent_check.py", "test_independent_check.py")}
    result = json.loads(result_path.read_text())
    ensure(result["schema"] == "dv-timecode-continuity-v1"
           and result["before_after_pins_match"] is True
           and result["freeze_pin"] == freeze_pin, "result identity/freeze flags")
    headers = json.loads((UNIT / "../sibling-lineage/results.json").read_text())["items"]
    manifest = json.loads((UNIT / "../sibling-lineage/inputs.json").read_text())
    ensure([h["clip"] for h in headers] == list(range(1, 9))
           and [i["clip"] for i in manifest["items"]] == list(range(1, 9)), "fixed clip identities")
    computed = []
    for index, header in enumerate(headers, 1):
        document = json.loads((UNIT / f"../dv-metadata/v2/results/clip{index}-result.json").read_text())
        ensure(document["clip"] == index, "raw inventory clip identity")
        ensure(header["video_header"]["length"] == int(manifest["items"][index - 1]["saved_video"]["nb_frames"]),
               "header/manifest count mismatch")
        computed.append(compute_clip(document, header))
    pairs = compare_clips(computed)
    compare(result["clips"], computed, "clips")
    compare(result["conditional_pairs"], pairs, "conditional_pairs")
    totals = {"frames": sum(len(c["frames"]) for c in computed),
              "transitions": sum(len(c["transitions"]) for c in computed),
              "pairs": len(pairs), "header_comparisons": 16}
    ensure(totals == {"frames": 5567, "transitions": 5559, "pairs": 28,
                      "header_comparisons": 16}, "fixed population totals")
    for name, expected in freeze["files"].items():
        ensure(pin(UNIT / name) == expected, "input changed during audit: " + name)
    ensure(pin(freeze_path) == freeze_pin and pin(result_path) == result_pin, "freeze/result changed")
    for name, expected in checker_files.items():
        ensure(pin(UNIT / name) == expected, "checker changed during audit")
    audit = {"schema": "independent-timecode-arithmetic-audit-v1", "status": "pass",
             "result_pin": result_pin, "freeze_pin": freeze_pin, "checker_pins": checker_files,
             "source_pins": freeze["files"], "before_after_pins_match": True,
             "totals": totals, "per_clip": [c["summary"] for c in computed],
             "all_pair_calculations": pairs,
             "limits": ["No original media read or decoding; pinned candidate inventories are shared inputs.",
                        "Author also implemented upstream DIF extraction/storage; this is separate arithmetic, not independent historical evidence.",
                        "Possible daily wraps are not unwrapped; forced ND/DF lanes are sensitivity cases; mode changes remain unavailable.",
                        "No clock authenticity, event-day chronology, fire severity or causal inference."]}
    serialized = json.dumps(audit, indent=2) + "\n"
    ensure(len(serialized.encode()) <= 256 * 1024, "audit output exceeds bounded size")
    with destination.open("x", encoding="utf-8") as stream:
        stream.write(serialized)
    ensure(json.loads(destination.read_text()) == audit, "audit readback mismatch")
    print(json.dumps({"output": str(destination), "pin": pin(destination), **totals}))


if __name__ == "__main__":
    main()

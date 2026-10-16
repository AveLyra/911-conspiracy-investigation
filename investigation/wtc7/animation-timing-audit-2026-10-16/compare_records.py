"""Reproducible comparisons of declared source transcriptions and static SWF output.

Does not infer solver time, select a correct label, or perform video measurements.
"""
import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sub(a, b):
    return str(Decimal(a) - Decimal(b))


def compare(timing, swf):
    out = {"method": "Decimal arithmetic on explicitly attributed printed values; matching root tag positions only within date pairs", "timing_residuals": []}
    for row in timing["table_3_1"]:
        if row["observed"] is None or row.get("reference_not_independent_prediction"):
            continue
        out["timing_residuals"].append({"event": row["event"],
            "qualifier": row.get("observed_qualifier", "Reported video-derived time; no independent timing here"),
            "model_minus_observed_with_debris": [sub(v, row["observed"]) for v in row["with_debris"]],
            "model_minus_observed_without_debris": [sub(v, row["observed"]) for v in row["without_debris"]]})
    out["faq_12_9_check"] = {"observed_interval_using_vibration_proxy": sub("6.9", "-6.0"), "modeled_interval_with_debris": sub("6.3", "-6.6"), "limitation": "Agreement is conditional on proxy identification, reference alignment and rounded source values; no measurement error or independent fit calculated"}
    out["floor_failure_table_minus_prose"] = sub(timing["table_3_1"][0]["with_debris"][0], timing["floor_failure_with_debris_prose_p42"])
    out["clock_offsets_absolute_minus_relative"] = {
        key: [sub(b, a) for a, b in value] for key, value in timing.items()
        if key.endswith("_pairs")}
    out["figure_12_68_panel_endpoint_minus_caption_endpoint"] = [
        {"relative": sub(panel[0], caption[0]), "absolute": sub(panel[1], caption[1])}
        for panel, caption in zip([timing["figure_12_68_panel_pairs"][0], timing["figure_12_68_panel_pairs"][-1]], timing["figure_12_68_caption_endpoint_pairs"])]
    out["swf_date_pairs"] = []
    for i in [0, 2]:
        first, second = swf["files"][i:i+2]
        a, b = first["tags"], second["tags"]
        same_order = [x["code"] for x in a] == [x["code"] for x in b]
        if not same_order:
            raise ValueError("root tag order differs; positional comparison ineligible")
        out["swf_date_pairs"].append({"files": [first["name"], second["name"]], "root_tag_order_matches": same_order, "root_tags": len(a), "same_payloads": sum(x["payload_sha256"] == y["payload_sha256"] for x, y in zip(a, b)), "different_payloads": [{"root_position_zero_based": n, "code": x["code"], "name": x["name"], "lengths": [x["length"], y["length"]]} for n, (x, y) in enumerate(zip(a, b)) if x["payload_sha256"] != y["payload_sha256"]]})
    out["swf_header_summary"] = [{"name": f["name"], "sha256": f["sha256"], "canvas_pixels": [(f["rect_twips"][1] - f["rect_twips"][0]) / 20, (f["rect_twips"][3] - f["rect_twips"][2]) / 20], "frame_rate": f["frame_rate"], "root_frames": f["declared_root_frames"], "recursive_video_frames": f["recursive_counts"].get("VideoFrame", 0), "recursive_video_declarations": f["recursive_counts"].get("DefineVideoStream", 0)} for f in swf["files"]]
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timing", default="timing-observations.json")
    parser.add_argument("--swf", default="swf-structure-run01.json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = compare(json.loads(Path(args.timing).read_text()), json.loads(Path(args.swf).read_text()))
    result["input_sha256"] = {"timing": digest(args.timing), "swf": digest(args.swf)}
    with open(args.output, "x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"output": args.output, "sha256": digest(args.output)}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prospective tiled-image gate; no raster is written if geometry fails."""
import io
import json
from pathlib import Path
import sys

from PIL import Image

import compare

HERE = Path(__file__).absolute().parent
KEY_SHA256 = "ac3fd35f7dbc0bee7d970c677e0609520455b789d0a77ffc3d3fb2840ecd86da"
TOLERANCE_POINTS = 1e-4


def geometry(tiles):
    failures = []
    if len(tiles) != 17:
        failures.append("expected exactly 17 preserved tiles")
    ordered = sorted(tiles, key=lambda x: -(x["invocations"][0]["ctm"][5] + x["invocations"][0]["ctm"][3]))
    first = ordered[0]
    a0, _, _, d0, e0, _ = first["invocations"][0]["ctm"]
    scale = d0 / first["native_pdf_dimensions"][1]
    previous_bottom = None
    rows = []
    offset = 0
    for tile in ordered:
        invocations = tile["invocations"]
        a, b, c, d, e, f = invocations[0]["ctm"]
        width, height = tile["native_pdf_dimensions"]
        residual = abs(d - height * scale)
        join = None if previous_bottom is None else abs(previous_bottom - (f + d))
        local = []
        if len(invocations) != 1 or invocations[0]["physical_page"] != 252:
            local.append("invocation/page mismatch")
        if b != 0 or c != 0 or a <= 0 or d <= 0:
            local.append("rotation/reflection/nonpositive scale")
        if abs(a-a0) > TOLERANCE_POINTS or abs(e-e0) > TOLERANCE_POINTS:
            local.append("horizontal placement/scale mismatch")
        if width != 975 or tile["extracted_view"].get("mode") != "RGB" or tile.get("bits_per_component") != 8 or tile.get("colorspace") != "/DeviceRGB":
            local.append("width/color mismatch")
        if tile.get("masks") or invocations[0].get("clipping_operator_seen_in_current_stream_state"):
            local.append("mask/clipping")
        if residual > TOLERANCE_POINTS:
            local.append("common vertical scale mismatch")
        if join is not None and join > TOLERANCE_POINTS:
            local.append("noncontiguous vertical placement")
        failures.extend(f"{tile['asset_id']}: {x}" for x in local)
        rows.append({"asset_id": tile["asset_id"], "object_reference": tile["object_reference"],
                     "ctm": invocations[0]["ctm"], "dimensions": [width,height],
                     "row_range": [offset,offset+height], "height_residual_points": residual,
                     "preceding_join_residual_points": join, "failures": local})
        offset += height
        previous_bottom = f
    if offset != 661:
        failures.append("combined source rows must equal 661")
    return ordered, {"accepted": not failures, "tolerance_points": TOLERANCE_POINTS,
                     "reference_vertical_points_per_pixel": scale,
                     "dimensions": [975,offset], "tiles": rows, "failures": failures}


def main():
    key_path = compare.safe_path(HERE, "assets/run01/provenance-key.json")
    raw = key_path.read_bytes()
    if compare.digest(raw) != KEY_SHA256:
        raise ValueError("source key pin mismatch")
    key = compare.legacy(()).decode_json(raw)
    tiles = [x for x in key["assets"] if x["native_pdf_dimensions"][0] == 975 and any(i["physical_page"] == 252 for i in x["invocations"])]
    ordered, receipt = geometry(tiles)
    snapshot = {str(key_path): KEY_SHA256}
    for tile in ordered:
        for field in ("extracted_view", "raw_encoded_stream"):
            pin = tile[field]
            p = compare.safe_path(HERE, pin["path"])
            content = p.read_bytes()
            if len(content) != pin["bytes"] or compare.digest(content) != pin["sha256"]:
                raise ValueError("tile source integrity failed")
            snapshot[str(p)] = pin["sha256"]
    addendum = compare.safe_path(HERE,"TILED-IMAGE-ADDENDUM.md")
    snapshot[str(addendum)] = compare.digest(addendum.read_bytes())
    snapshot[str(Path(__file__).absolute())] = compare.digest(Path(__file__).read_bytes())
    receipt.update({"source_key_sha256": KEY_SHA256, "addendum_sha256": snapshot[str(addendum)],
                    "code_sha256": snapshot[str(Path(__file__).absolute())], "input_snapshot": snapshot,
                    "pixel_decoding_performed": False, "png_written": False,
                    "scope": "Geometric source-representation gate; no visual observation or historical inference."})
    out_dir = HERE / "assets/assembled01"
    compare.safe_path(HERE, out_dir, existing=False)
    out_dir.mkdir(exist_ok=False)
    if receipt["accepted"]:
        decoded = []
        for tile in ordered:
            with Image.open(io.BytesIO(compare.safe_path(HERE,tile["extracted_view"]["path"]).read_bytes())) as image:
                if image.mode != "RGB" or list(image.size) != tile["native_pdf_dimensions"]:
                    raise ValueError("decoded color/dimensions mismatch")
                decoded.append(image.tobytes())
        pixels = b"".join(decoded)
        joined = Image.frombytes("RGB", (975,661), pixels)
        png_path = out_dir / "C-tiled-source.png"
        with png_path.open("xb") as f:
            joined.save(f,format="PNG")
        with Image.open(png_path) as check:
            if check.tobytes() != pixels:
                raise ValueError("PNG pixel readback mismatch")
        receipt.update({"pixel_decoding_performed": True, "png_written": True,
                        "png_sha256": compare.digest(png_path.read_bytes()), "decoded_pixels_sha256": compare.digest(pixels)})
    for path, expected in snapshot.items():
        if compare.digest(compare.safe_path(HERE,path).read_bytes()) != expected:
            raise ValueError("source changed during tiled-image gate")
    with (out_dir / "receipt.json").open("x") as f:
        json.dump(receipt,f,indent=2,sort_keys=True)
        f.write("\n")
    print(json.dumps({"accepted": receipt["accepted"], "png_written": receipt["png_written"],
                      "tile_count": len(ordered), "failures": receipt["failures"]}))
    return 0 if receipt["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

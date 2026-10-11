"""Independent F7 context/source check; no producer or display imports.

The display CLI is run as a black box and decoded here against native pixels.
Both implementations use Pillow; this is not independent JPEG-codec validation.
No cells are attributed to curves and no human acceptance is supplied.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
BOX = [218, 0, 332, 88]
CONTEXT_SHA = "ff9f1f0e47b443994c6ba5325a1f2347c2522f48f2a79012b3c6d285bcb6874f"
EXPECTED = {
    "PROTOCOL.md": "aae8d37e8f0cda59f4c226e05c386f0dd73ace7b6954c7cd7ea81142f252ab19",
    "READERS.md": "d62c0390fbb19bc507cb49a8da3d04802f1ad39e39784eb88ae27cc909424417",
    "read_context.py": "826e1bc24904d631b0b613ceea73b6ddc14b228438e77db751f291a60c717599",
    "../PROTOCOL.md": "2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd",
    "../force56-remainder/READERS.md": "e2508d4ca55ea9e6f06fef260a7ab17613ecbe533be47376c5c63264c436da2f",
    "../read_context.py": "da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18",
    "../approach34/read_context.py": "384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3",
    "../../native-strips01/Im2.jpg": "9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9",
    "../../render01/page-076.png": "0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path):
    raw = Path(path).read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def records_match(records, box, source):
    x0, y0, x1, y1 = box
    width = x1 - x0
    require(type(records) is list and len(records) == width * (y1-y0), "record count")
    for index, record in enumerate(records):
        x, y = x0 + index % width, y0 + index // width
        require(type(record) is dict and set(record) == {"x", "y", "rgb"}, "record fields")
        require(type(record["x"]) is int and type(record["y"]) is int and
                (record["x"], record["y"]) == (x, y), "exact row-major coordinates")
        rgb = record["rgb"]
        require(type(rgb) is list and len(rgb) == 3 and
                all(type(n) is int and 0 <= n <= 255 for n in rgb), "RGB integers")
        require(tuple(rgb) == source.getpixel((x, y)), "native RGB mismatch")


def decode_columns(lines, columns, rows):
    """Independent strict parser; reconstruct omitted cells as exact white."""
    require(len(lines) == len(columns), "display column count")
    result = {(x, y): (255, 255, 255) for x in columns for y in rows}
    for expected_x, line in zip(columns, lines):
        match = re.fullmatch(r"(\d+): ?(.*)", line)
        require(match is not None and int(match[1]) == expected_x, "display column order")
        previous = -1
        for token in match[2].split():
            part = re.fullmatch(r"(\d+)(?:-(\d+))?=(g\d+|\d+,\d+,\d+)", token)
            require(part is not None, "display token grammar")
            first, last = int(part[1]), int(part[2] or part[1])
            value = part[3]
            rgb = (int(value[1:]),)*3 if value.startswith("g") else tuple(map(int, value.split(",")))
            require(first <= last and first > previous and first in rows and last in rows,
                    "display row range, order or overlap")
            require(all(0 <= n <= 255 for n in rgb) and rgb != (255, 255, 255), "display RGB/white rule")
            for y in range(first, last+1):
                result[expected_x, y] = rgb
            previous = last
    return result


def controls():
    results = {}
    im = Image.new("RGB", (2, 2), (255, 255, 255))
    im.putpixel((0, 0), (255, 254, 255))
    good = [{"x": x, "y": y, "rgb": list(im.getpixel((x, y)))} for y in range(2) for x in range(2)]
    records_match(good, [0, 0, 2, 2], im)
    results["valid_records"] = True
    mutations = {"missing_record": good[:-1], "reordered_records": [good[1], good[0], *good[2:]],
                 "duplicate_coordinate": [good[0], good[0], *good[2:]]}
    bad = copy.deepcopy(good)
    bad[0]["rgb"] = [255, 255, 255]
    mutations["near_white_changed"] = bad
    bad = copy.deepcopy(good)
    bad[0]["x"] = False
    mutations["boolean_coordinate"] = bad
    for label, records in mutations.items():
        try:
            records_match(records, [0, 0, 2, 2], im)
        except ValueError:
            results[label+"_rejected"] = True
        else:
            raise AssertionError(label)
    parsed = decode_columns(["0: 0-1=254,255,255 3=g0", "1: "], range(2), range(4))
    require(parsed[0, 0] == (254, 255, 255) and parsed[0, 1] == (254, 255, 255) and
            parsed[0, 2] == (255, 255, 255) and parsed[0, 3] == (0, 0, 0) and
            parsed[1, 3] == (255, 255, 255), "display fixture")
    results["display_near_white_gap_run_grayscale_empty"] = True
    for label, lines in {
        "overlap": ["0: 0-1=g0 1=g1"], "out_of_range": ["0: 4=g0"],
        "reversed": ["0: 2-1=g0"], "wrong_column": ["1: 0=g0"],
        "bad_rgb": ["0: 0=g256"], "explicit_white": ["0: 0=g255"],
        "missing_column": [], "invalid_token": ["0: garbage"],
    }.items():
        try:
            decode_columns(lines, range(1), range(4))
        except ValueError:
            results["display_"+label+"_rejected"] = True
        else:
            raise AssertionError(label)
    return results


def verify():
    checks = controls()
    names = list(EXPECTED) + ["context01.json", "context02.json", "context_check.py"]
    before = {name: pin(HERE/name) for name in names}
    for name, sha in EXPECTED.items():
        require(before[name]["sha256"] == sha, "frozen input "+name)
    first = (HERE/"context01.json").read_bytes()
    require(first == (HERE/"context02.json").read_bytes(), "context repeat bytes")
    require(hashlib.sha256(first).hexdigest() == CONTEXT_SHA, "frozen context hash")
    expected_inputs = {name: before[name] for name in EXPECTED}
    with Image.open(HERE/"../../native-strips01/Im2.jpg") as source:
        require(source.mode == "RGB" and source.size == (741, 88), "source representation")
        for name in ("context01.json", "context02.json"):
            data = json.loads((HERE/name).read_text())
            require(data["inputs"] == expected_inputs, "complete exact nine-pin closure")
            require(data["target_boxes"] == {"F7": [220, 0, 330, 88]} and
                    data["context_boxes"] == {"F7": BOX}, "declared geometry")
            require(data["sources"] == {"F7": "Im2.jpg"} and data["source_size"] == [741, 88], "source identity")
            require(data["classification"] is None and data["human_accepted"] is False, "no selection or human acceptance")
            require(set(data["cells"]) == {"F7"}, "context key")
            records_match(data["cells"]["F7"], BOX, source)
        command = [sys.executable, "-B", str(HERE/"read_context.py"), "show", "--first", "218", "--last", "331"]
        shown = subprocess.run(command, cwd=HERE, capture_output=True, check=True)
        require(not shown.stderr, "display stderr")
        lines = shown.stdout.decode("utf-8").splitlines()
        require(lines[0] == "F7-Im2-early context [218, 0, 332, 88]; rows 0..87; omitted EXACT WHITE only; gN=N,N,N; inclusive equal-RGB runs; no thresholds.", "display header")
        decoded = decode_columns(lines[1:], range(218, 332), range(88))
        require(all(rgb == source.getpixel(xy) for xy, rgb in decoded.items()), "display/source equality")
        nonwhite = sum(rgb != (255, 255, 255) for rgb in decoded.values())
    require(before == {name: pin(HERE/name) for name in names}, "all pins unchanged after check")
    return {
        "status": "independent_context_source_fidelity_pass",
        "checker_pin": before["context_check.py"], "pins_before": before, "pins_after": before,
        "runtime": {"executable": sys.executable, "python": platform.python_version(), "pillow": pillow_version},
        "replay_command": [sys.executable, "-B", str(HERE/"context_check.py")],
        "exclusive_save_command": [sys.executable, "-B", str(HERE/"context_check.py"), "--save"],
        "display_command": command, "display_sha256": hashlib.sha256(shown.stdout).hexdigest(),
        "display_bytes": len(shown.stdout), "controls": checks,
        "context_copies": 2, "source_records_checked": 20064, "distinct_cells": 10032,
        "display_columns_checked": 114, "display_cells_checked": 10032,
        "nonwhite_display_cells": nonwhite, "exact_white_omitted_cells": 10032-nonwhite,
        "required_producer_pins": 9, "human_accepted": False, "curve_selection": None,
        "limits": ["No producer/display module imported; display CLI tested as black box.",
                   "Pillow decoding shared with producer; not independent JPEG-codec validation.",
                   "Source/RGB/display fidelity only, not perceptual ownership, H assumptions, physical support or human acceptance."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    require(not (args.controls and args.save), "choose controls or save")
    result = controls() if args.controls else verify()
    raw = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.save:
        with (HERE/"context-check.json").open("x") as output:
            output.write(raw)
        print(json.dumps({"output": pin(HERE/"context-check.json"), "status": result["status"]}, sort_keys=True))
    else:
        print(raw, end="")

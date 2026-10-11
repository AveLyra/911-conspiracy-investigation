"""Finite synthetic challenges; no historical measurements or manual annotations.

DECLARATION BEFORE EXECUTION: 12 straight scenes (three slopes, two phases,
two colors), four constructed scenes, two unchanged codecs, and columns64..95.
The fixed maximal-nonwhite diagnostic is NOT the frozen manual-envelope method.
No outcome causes a threshold, halo, scene, query or annotation adjustment.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

import PIL
from PIL import Image, features

HERE = Path(__file__).resolve().parent
C = HERE.parent.parent
PINNED = {
    "historical-applicability/envelope-packet-2026-10-08/PROTOCOL.md":
        "ffa2fc84231d2b19dedfc6be7272460f05a980cdf6c5c6d8f15c36a66e8baaa9",
    "raster_uncertainty.py":
        "878872fcde4316e2655e156221de970a41f5186351a9525159c7eb7520e8760f",
    "manual-envelope-trial/PROTOCOL.md":
        "11e1d727b2de69c50ed6c343f59b101a4ec3f3b8c2ad724bff5557da1b0318ad",
    "manual-envelope-trial/report.md":
        "d3f56c561acb6d5a3854724294e02f4c12ab595a405cf03a7ab3f38f6ed20186",
    "manual-envelope-trial/reader-a.json":
        "a828d3d11cdadfcc8438e67fe0d5d0bbb14d808bbea42010cdef50de9cae1203",
    "manual-envelope-trial/reader-b.json":
        "07153e7140a2c7f37f39cd041270920b12bf1407faa0d0041a96276a12bb130e",
    "manual-envelope-trial/score-a01.json":
        "6a7a86d5a4d8c3e4e5ce7dcee1e46a3e190eb3ecb44650a4653079ff528a2049",
    "manual-envelope-trial/score-b01.json":
        "49f6e4400e44d0dd87a253ebfa1123de85f41973a95006ce5d6a907daef9b761",
}
WIDTH, HEIGHT = 160, 96
OFFSETS = tuple(F(v, 8) for v in (1, 3, 5, 7))
SLOPES = ("0", "1/2", "2")
PHASES = ("0", "1/2")
COLORS = (("black", (0, 0, 0)), ("pale254", (254, 254, 254)))
CODECS = ("png", "jpg50s2")
COLUMNS = tuple(range(64, 96))
FEATURES = ("line", "quartic_excursion", "subpixel_gap", "fractional_cap", "blank")


def packed(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    data = Path(path).read_bytes()
    return {"sha256": digest(data), "bytes": len(data)}


def input_pins():
    result = {}
    for relative, expected in PINNED.items():
        result[relative] = pin(C / relative)
        if result[relative]["sha256"] != expected:
            raise ValueError(f"changed_frozen_input:{relative}")
    for name in ("raster_challenge.py", "test_raster_challenge.py"):
        result[str((HERE / name).relative_to(C))] = pin(HERE / name)
    return result


def load_renderer():
    # Verify before executing the unchanged helper, including during tests.
    path = C / "raster_uncertainty.py"
    if pin(path)["sha256"] != PINNED["raster_uncertainty.py"]:
        raise ValueError("changed_renderer_before_import")
    spec = importlib.util.spec_from_file_location("envelope_frozen_raster_helper", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@dataclass(frozen=True)
class Scene:
    name: str
    color: tuple[int, int, int]
    slope: str = "0"
    phase: str = "0"
    feature: str = "line"

    def __post_init__(self):
        if (not isinstance(self.name, str) or not self.name
                or type(self.color) is not tuple or len(self.color) != 3
                or any(type(v) is not int or not 0 <= v <= 255 for v in self.color)
                or self.color == (255, 255, 255)
                or self.slope not in SLOPES or self.phase not in PHASES
                or self.feature not in FEATURES):
            raise ValueError("invalid_fixed_scene")
        if self.feature != "line" and (self.slope != "0" or self.phase != "0"):
            raise ValueError("constructed_features_require_horizontal_baseline")


def scenes():
    output = []
    for color_name, color in COLORS:
        for slope in SLOPES:
            for phase in PHASES:
                output.append(Scene(f"{color_name}-m{slope}-p{phase}", color, slope, phase))
    output.extend(Scene(name, (0, 0, 0), feature=name) for name in FEATURES[1:])
    return tuple(output)


def support_intervals(scene):
    """Generating support; endpoint conventions do not alter open-column tests."""
    if scene.feature == "blank":
        return ()
    if scene.feature == "fractional_cap":
        return ((F(16), F(161, 2)),)
    if scene.feature == "subpixel_gap":
        return ((F(16), F(1287, 16)), (F(1289, 16), F(144)))
    return ((F(16), F(144)),)


def supported(scene, u):
    return any(a <= u < b for a, b in support_intervals(scene))


def center(scene, u):
    y = F(48) + F(scene.slope) * (u - 80) + F(scene.phase)
    if scene.feature == "quartic_excursion" and F(643, 8) <= u <= F(645, 8):
        # C1 compact quartic bump on80+3/8..80+5/8; zero derivative at ends.
        # Peak4 at80+1/2; zero at every x sample of the fixed4x4 renderer.
        y += 4 * (1 - 64 * (u - F(161, 2)) ** 2) ** 2
    return y


def render(scene, helper):
    """Vertical width1; exact rational4x4 point sampling, unchanged mixing."""
    pixels = bytearray(WIDTH * HEIGHT * 3)
    for x in range(WIDTH):
        centers = Counter(center(scene, F(x) + dx) for dx in OFFSETS
                          if supported(scene, F(x) + dx))
        for y in range(HEIGHT):
            count = sum(n for c, n in centers.items() for dy in OFFSETS
                        if c - F(1, 2) <= F(y) + dy < c + F(1, 2))
            index = 3 * (y * WIDTH + x)
            pixels[index:index + 3] = bytes(helper.mixed_channel(v, count) for v in scene.color)
    return Image.frombytes("RGB", (WIDTH, HEIGHT), bytes(pixels))


def truth(scene, x):
    if type(x) is not int or not 0 <= x < WIDTH:
        raise ValueError("invalid_column")
    pieces = [(max(F(x), a), min(F(x + 1), b)) for a, b in support_intervals(scene)
              if max(F(x), a) < min(F(x + 1), b)]
    length = sum((b - a for a, b in pieces), F(0))
    values = [center(scene, u) for a, b in pieces for u in (a, b)]
    if scene.feature == "quartic_excursion" and x == 80:
        values.append(F(52))  # Exact derivative-zero point, not sampled truth.
    return {"support_intervals": [[str(a), str(b)] for a, b in pieces],
            "support_length": str(length), "full_column_support": length == 1,
            "ordinate_infimum_supremum": [str(min(values)), str(max(values))] if values else None}


def diagnostic(image, x):
    if image.mode != "RGB" or image.size != (WIDTH, HEIGHT) or type(x) is not int or not 0 <= x < WIDTH:
        raise ValueError("invalid_diagnostic_input")
    # Fixed maximal decoded nonwhite geometry; no curve classifier or reader.
    rows = [y for y in range(HEIGHT) if image.getpixel((x, y)) != (255, 255, 255)]
    runs = []
    for y in rows:
        if runs and runs[-1][1] == y:
            runs[-1][1] = y + 1
        else:
            runs.append([y, y + 1])
    return {"nonwhite_rows": rows, "runs": runs,
            "envelope": runs[0] if len(runs) == 1 else None,
            "status": "single_run" if len(runs) == 1 else "missing" if not runs else "disconnected"}


def column_result(scene, image, x):
    observed, expected = diagnostic(image, x), truth(scene, x)
    envelope = observed["envelope"]
    if envelope is None:
        outcome = "unavailable_" + observed["status"]
    elif not expected["full_column_support"]:
        outcome = "unsupported_full_column_proposal"
    else:
        lo, hi = map(F, expected["ordinate_infimum_supremum"])
        outcome = "contained" if envelope[0] <= lo <= hi <= envelope[1] else "enclosure_failure"
    return {"column": x, "observed": observed, "truth": expected, "outcome": outcome,
            "three_column_single_run_diagnostic": 0 < x < WIDTH - 1 and all(
                diagnostic(image, z)["envelope"] is not None for z in (x - 1, x, x + 1))}


def raster_record(scene, codec, base_image, helper):
    encoded, decoded, warnings = helper.encode_decode(base_image, codec)
    columns = [column_result(scene, decoded, x) for x in COLUMNS]
    return {"scene": asdict(scene), "codec": codec,
            "base_rgb_sha256": digest(base_image.tobytes()),
            "encoded_sha256": digest(encoded), "encoded_bytes": len(encoded),
            "encoded_base64": base64.b64encode(encoded).decode("ascii"),
            "decoded_rgb_sha256": digest(decoded.tobytes()), "warnings": warnings,
            "columns": columns, "outcome_counts": dict(sorted(Counter(r["outcome"] for r in columns).items()))}


def compare_pair(records, left, right, codec, kind):
    a, b = (next(r for r in records if r["scene"]["name"] == name and r["codec"] == codec)
            for name in (left, right))
    ca, cb = (next(c for c in r["columns"] if c["column"] == 80) for r in (a, b))
    return {"kind": kind, "left": left, "right": right, "codec": codec,
            "base_rgb_equal": a["base_rgb_sha256"] == b["base_rgb_sha256"],
            "encoded_equal": a["encoded_base64"] == b["encoded_base64"],
            "decoded_equal": a["decoded_rgb_sha256"] == b["decoded_rgb_sha256"],
            "query_column": 80, "left_query": ca, "right_query": cb}


def build():
    before = input_pins()
    helper = load_renderer()
    declared = scenes()
    records = []
    for scene in declared:
        base = render(scene, helper)
        for codec in CODECS:
            records.append(raster_record(scene, codec, base, helper))
    pairs = [compare_pair(records, left, right, codec, kind)
             for left, right, kind in (
                 ("black-m0-p0", "quartic_excursion", "constructed_subpixel_curvature_alias"),
                 ("black-m0-p0", "subpixel_gap", "constructed_subpixel_support_alias"),
                 ("pale254-m0-p0", "blank", "constructed_pale_quantization_alias"))
             for codec in CODECS]
    prior = {name: json.loads((C / f"manual-envelope-trial/score-{name}01.json").read_text())["result"]["counts"]
             for name in ("a", "b")}
    after = input_pins()
    if before != after:
        raise ValueError("inputs_changed_during_challenge")
    return {"version": 1, "status": "synthetic_challenge_only_no_historical_admission",
            "declaration": {"scenes": [asdict(s) for s in declared], "codecs": CODECS, "columns": COLUMNS,
                "raster_size": [WIDTH, HEIGHT], "subpixel_offsets": [str(v) for v in OFFSETS],
                "vertical_stroke_width": "1", "original_support": "[16,144) unless explicitly varied",
                "quartic_bump": "y=48+4*(1-64*(x-161/2)^2)^2 on[643/8,645/8], else48",
                "narrow_gap": "[1287/16,1289/16) absent; width1/8 is half the1/4 horizontal sample spacing",
                "fractional_cap": "trace support ends at161/2",
                "diagnostic": "All decoded nonwhite rows; envelope only for one contiguous run; zero halo. This is NOT manual annotation.",
                "truth": "Exact generating support and full-column ordinate infimum/supremum, not pixel centers.",
                "no_tuning": True},
            "inputs": before, "inputs_after": after,
            "runtime": {"python": platform.python_version(), "pillow": PIL.__version__,
                        "jpeg": features.version_codec("jpg"), "executable": pin(Path(sys.executable)),
                        "imaging_binary": pin(Path(Image.core.__file__))},
            "prior_manual_trial_counts_not_rerun": prior,
            "records": records, "constructed_pairs": pairs,
            "totals": {"scenes": len(declared), "raster_cases": len(records),
                       "column_records": sum(len(r["columns"]) for r in records),
                       "outcomes": dict(sorted(Counter(c["outcome"] for r in records for c in r["columns"]).items()))},
            "limits": [
                "High-curvature and subpixel-gap pairs are deliberately constructed identifiability counterexamples, not representative historical behavior.",
                "The maximal-nonwhite diagnostic is not either frozen manual reader or the historical eligibility rule. Its failures do not falsify historical Hink0.",
                "An equal raster can have different generating extrema or support under this specified finite renderer. No annotation was chosen after seeing truth.",
                "Pale color254, vertical width1, fixed4x4 point sampling and two codec settings are artificial controls, not estimates of the historical renderer.",
                "Compression can alter visible rows; missing/disconnected diagnostic output does not prove universal human unreadability.",
                "Passing ordinary controls does not prove enclosure for every curve. Prior manual-trial passes remain unchanged.",
                "No historical image, ordinate, discrepancy, human sample, source edit or causal finding enters this calculation."]}


def save(output):
    output = Path(output)
    if output.parent.resolve() != HERE or output.name not in ("raster-challenge01.json", "raster-challenge02.json"):
        raise ValueError("output_not_one_of_two_declared_local_files")
    if output.exists():
        raise FileExistsError(output)
    result = build()
    with output.open("xb") as stream:
        stream.write(packed(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    if bool(args.output) == bool(args.check):
        parser.error("choose --output NEW_DECLARED_FILE or --check EXISTING_FILE")
    if args.output:
        result = save(args.output)
        output_pin = pin(args.output)
    else:
        result = build()
        if packed(result) != args.check.read_bytes():
            raise ValueError("saved_result_replay_mismatch")
        output_pin = pin(args.check)
    print(json.dumps({"totals": result["totals"], "result": output_pin,
                      "equal_constructed_pairs": sum(p["encoded_equal"] for p in result["constructed_pairs"])}))


if __name__ == "__main__":
    main()

"""Independent raw-JSON/CTM check; stdout only, no producer imports or pixels.

The saved protocol, old classification contract and output field schema were
inspected. This is a separate implementation, not a blind annotation reading.
It verifies conditional arithmetic, not the truth of Hidentity/Hsupport/Hink0.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
RECON = "historical-applicability/footprint-reconciliation-2026-10-08.json"
RECON_SHA = "ed4a1ded5e53b7d102c9462f5f939883640359da5c0472220a92fbba1b7a354e"
REPRESENTATION = "pypdf-representation01.json"
REP_SHA = "1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5"
MASKS = {"F": ((850, 225, 1280, 315), (1040, 310, 1160, 470)),
         "E": ((470, 1055, 900, 1148), (575, 1138, 695, 1302))}
STATUSES = {"identified_local_fragment", "fringe_only", "identity_conflict",
            "no_attributable_cells", "boundary_truncated"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(file):
    return json.loads(file.read_text(), parse_float=Fraction)


def pin(file):
    content = file.read_bytes()
    return {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}


def row_set(values, height):
    require(isinstance(values, list), "row set must be a list")
    require(all(type(n) is int and 0 <= n < height for n in values),
            "row set requires native integer cells")
    require(values == sorted(set(values)), "row set is duplicated or unordered")
    return set(values)


def inspect_record(raw, route, box, height):
    """Normalize only inspected schemas; classify from literal raw membership."""
    old = "column" in raw
    x = raw["column" if old else "x"]
    require(type(x) is int and box[0] <= x < box[2], "column outside target")
    if old:
        require(raw["route"] == route, "route mismatch")
    core_key, fringe_key = ("core_rows", "fringe_rows") if old else ("core", "fringe")
    core = row_set(raw[core_key], height)
    fringe = row_set(raw[fringe_key], height)
    require(not core & fringe, "core/fringe overlap")
    outer = core | fringe
    require(all(box[1] <= y < box[3] for y in outer), "selected cell outside target")
    require(raw["status"] in STATUSES, "unknown status")
    flags = raw["boundary_flags"]
    require(isinstance(flags, list) and all(isinstance(v, str) for v in flags),
            "malformed boundary flags")
    expected_flags = set()
    if outer:
        for hit, label in ((x == box[0], "target_left"),
                           (x == box[2] - 1, "target_right"),
                           (box[1] in outer, "strip_top" if old else "target_top"),
                           (box[3] - 1 in outer, "strip_bottom" if old else "target_bottom")):
            if hit:
                expected_flags.add(label)
    require(set(flags) == expected_flags and len(flags) == len(expected_flags),
            "boundary flags inconsistent with selected cells")
    fragment = raw.get("fragment_id")
    explicit = isinstance(fragment, str) and bool(fragment.strip())
    members = None
    if "fragment_membership" in raw:
        require(isinstance(raw["fragment_membership"], dict), "bad membership map")
        members = [(name, part["core_rows"], part["fringe_rows"])
                   for name, part in raw["fragment_membership"].items()]
    if "fragments" in raw:
        require(members is None and isinstance(raw["fragments"], list),
                "mixed or malformed fragment schemas")
        members = [(part["fragment_id"], part["core"], part["fringe"])
                   for part in raw["fragments"]]
    if members is not None:
        names, member_core, member_fringe = [], set(), set()
        for name, c_values, f_values in members:
            require(isinstance(name, str) and bool(name.strip()), "bad fragment identifier")
            c_set, f_set = row_set(c_values, height), row_set(f_values, height)
            require(not c_set & f_set, "member core/fringe overlap")
            names.append(name)
            member_core |= c_set
            member_fringe |= f_set
        require(len(names) == len(set(names)), "duplicate fragment identifiers")
        require(member_core == core and member_fringe == fringe, "fragment union mismatch")
    reasons = []
    predicates = [(raw["status"] != "identified_local_fragment", "nonidentified_status"),
                  (not core, "empty_core"), (not outer, "empty_outer"),
                  (bool(outer) and len(outer) != max(outer) - min(outer) + 1,
                   "disconnected_outer"),
                  (bool(flags), "boundary"), (not explicit, "missing_identifier")]
    reasons.extend(label for applies, label in predicates if applies)
    if members is not None:
        if len(members) > 1:
            reasons.append("multiple_fragment_members")
        elif len(members) == 1:
            name, c_values, f_values = members[0]
            if not explicit or name != fragment or c_values != raw[core_key] or f_values != raw[fringe_key]:
                reasons.append("inconsistent_single_fragment_identity")
        elif outer or explicit:
            reasons.append("inconsistent_single_fragment_identity")
    rectangle = [x, min(outer), x + 1, max(outer) + 1] if not reasons else None
    # Geometry is preserved even when an additional conservative rule withholds
    # the conditional window. No union or interpolation is made here.
    for field in ("band_refs", "unassigned_band_refs"):
        if field in raw:
            require(isinstance(raw[field], list), "bad unassigned-band reference")
    if raw.get("band_refs") or raw.get("unassigned_band_refs"):
        reasons.append("unassigned_band_reference")
    if x in (box[0], box[2] - 1) or outer & {box[1], box[3] - 1}:
        if "boundary" not in reasons:
            reasons.append("boundary")
    return {"column": x, "route": route, "fragment_id": fragment,
            "native_rectangle": rectangle, "reasons": reasons}


def corners_to_page(rectangle, invocation):
    """Forward map all four corners directly; do not use Strip or its inverse."""
    width, height = invocation["native_dimensions"]
    a, b, c, d, e, f = map(Fraction, invocation["ctm"])
    require(width > 0 and height > 0 and a > 0 and d > 0 and b == c == 0,
            "unsupported CTM or image dimensions")
    points = [(e + a * Fraction(x, width), f + d * (1 - Fraction(y, height)))
              for x, y in itertools.product((rectangle[0], rectangle[2]),
                                            (rectangle[1], rectangle[3]))]
    pdf = [min(x for x, _ in points), min(y for _, y in points),
           max(x for x, _ in points), max(y for _, y in points)]
    rendered = [(x * Fraction(25, 9), (792 - y) * Fraction(25, 9)) for x, y in points]
    render = [min(x for x, _ in rendered), min(y for _, y in rendered),
              max(x for x, _ in rendered), max(y for _, y in rendered)]
    return pdf, render


def axis_intervals(panel, reader):
    # Literal saved candidate axes, independently transcribed from the two notes.
    if panel == "F":
        centers = {"L": 449, "R": 1294, "T": 224, "B": 829}
    else:
        centers = {"L": 473 if reader == "root" else 474,
                   "R": 1297, "T": 1048, "B": 1669}
    offsets = (-3, 4) if reader == "root" else (-6, 6)
    return {name: [Fraction(center + off) for off in offsets]
            for name, center in centers.items()}


def closed_overlap(first, second):
    return not (first[2] < second[0] or second[2] < first[0]
                or first[3] < second[1] or second[3] < first[1])


def axis_extrema(rectangle, axes, ordinate_max):
    require(all(len(v) == 2 and v[0] <= v[1] for v in axes.values()), "reversed axis interval")
    require(axes["R"][0] > axes["L"][1] and axes["B"][0] > axes["T"][1],
            "nonpositive axis denominator")
    require(rectangle[0] <= rectangle[2] and rectangle[1] <= rectangle[3],
            "reversed graphical rectangle")
    x_values, y_values = [], []
    # Independently enumerate the uncertain point and endpoint vertices.
    for left in axes["L"]:
        for right in axes["R"]:
            for x in (rectangle[0], rectangle[2]):
                x_values.append(Fraction(8, 5) * (x - left) / (right - left))
    for top in axes["T"]:
        for bottom in axes["B"]:
            for y in (rectangle[1], rectangle[3]):
                y_values.append(Fraction(ordinate_max) * (bottom - y) / (bottom - top))
    return [min(x_values), max(x_values)], [min(y_values), max(y_values)]


def expected_rows(source, region, panel, invocation):
    if "observations" in source:
        raw_routes = {route: [r for r in source["observations"] if r["route"] == route]
                      for route in ("solid", "dash")}
        require(sum(map(len, raw_routes.values())) == len(source["observations"]), "unknown route")
    else:
        require(set(source["routes"]) == {"solid", "dash"}, "missing/extra routes")
        raw_routes = source["routes"]
    result = []
    for route in ("solid", "dash"):
        rows = [inspect_record(raw, route, region["target_box"], invocation["native_dimensions"][1])
                for raw in raw_routes[route]]
        require([r["column"] for r in rows] == list(range(region["target_box"][0], region["target_box"][2])),
                "route coverage missing, duplicated, or reordered")
        for row in rows:
            row["pdf_rectangle"] = row["render_rectangle"] = None
            if row["native_rectangle"] is not None:
                pdf, render = corners_to_page(row["native_rectangle"], invocation)
                row["pdf_rectangle"], row["render_rectangle"] = pdf, render
                if any(closed_overlap(render, mask) for mask in MASKS[panel]):
                    row["reasons"].append("composed_page_exclusion")
                for reader in ("root", "independent"):
                    axis = axis_intervals(panel, reader)
                    interior = (axis["L"][1], axis["T"][1], axis["R"][0], axis["B"][0])
                    if not (render[0] > interior[0] and render[1] > interior[1]
                            and render[2] < interior[2] and render[3] < interior[3]):
                        row["reasons"].append("not_inside_all_" + reader + "_plot_bounds")
        # Freeze eligibility before testing neighbors: this is a one-column
        # guard, not a recursively shrinking connected component.
        base_good = {r["column"]: not r["reasons"] for r in rows}
        identifiers = {r["column"]: r["fragment_id"] for r in rows}
        for row in rows:
            x = row["column"]
            if any(not base_good.get(n, False) or identifiers.get(n) != row["fragment_id"]
                   for n in (x - 1, x + 1)):
                row["reasons"].append("fragment_end_or_interruption")
            row["conditional_window"] = not row["reasons"]
            row["curve_support_established"] = False
            row["physical_windows"] = None
            if row["conditional_window"]:
                row["physical_windows"] = []
                for reader in ("root", "independent"):
                    x_values, y_values = axis_extrema(row["render_rectangle"],
                                                    axis_intervals(panel, reader),
                                                    1000000 if panel == "F" else 800000)
                    row["physical_windows"].append({"axis_id": panel + "-" + reader,
                        "displacement_m": x_values, "ordinate": y_values,
                        "ordinate_unit": "N" if panel == "F" else "N-m"})
            result.append(row)
    return result


def serialized(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, list):
        return [serialized(v) for v in value]
    if isinstance(value, dict):
        return {k: serialized(v) for k, v in value.items()}
    return value


def manual_checks():
    checks = []
    def check(name, condition):
        require(condition, "manual check failed: " + name)
        checks.append(name)
    invocation = {"native_dimensions": [10, 5], "ctm": [20, 0, 0, 10, 3, 4]}
    pdf, render = corners_to_page([2, 1, 3, 3], invocation)
    check("manual_full_cell_pdf_y_inversion", pdf == [7, 8, 9, 12])
    check("manual_render_full_cell", render == [Fraction(175, 9), Fraction(6500, 3), 25, Fraction(19600, 9)])
    alternate = dict(invocation, ctm=[20, 0, 0, 5, 3, 4])
    alt_pdf, _ = corners_to_page([2, 1, 3, 3], alternate)
    check("manual_distinct_vertical_pitch", alt_pdf == [7, 6, 9, 8])
    axes = {"L": [Fraction(0), Fraction(1)], "R": [Fraction(9), Fraction(10)],
            "T": [Fraction(0), Fraction(1)], "B": [Fraction(9), Fraction(10)]}
    x, y = axis_extrema([Fraction(2), Fraction(2), Fraction(4), Fraction(4)], axes, 100)
    check("manual_uncertain_x_extrema", x == [Fraction(8, 45), Fraction(32, 45)])
    check("manual_uncertain_y_extrema", y == [Fraction(500, 9), Fraction(800, 9)])
    for name, replacement in (("zero_denominator_rejected", [1, 10]),
                              ("negative_denominator_rejected", [0, 10])):
        bad = dict(axes, R=list(map(Fraction, replacement)))
        try:
            axis_extrema([2, 2, 4, 4], bad, 100)
        except ValueError:
            check(name, True)
        else:
            check(name, False)
    check("mask_touch_withheld", closed_overlap([1, 2, 3, 4], [3, 4, 8, 9]))
    check("mask_disjoint_retained", not closed_overlap([1, 2, 3, 4], [4, 4, 8, 9]))
    check("root_full_selected_axis_cell", axis_intervals("F", "root")["L"] == [446, 453])
    check("independent_continuous_allowance", axis_intervals("E", "independent")["L"] == [468, 480])
    for values in ([1, 1], [True], [-1], [2, 1]):
        try:
            row_set(values, 5)
        except ValueError:
            pass
        else:
            raise ValueError("malformed row set admitted")
    check("four_malformed_row_sets_rejected", True)
    return checks


def verify(run_file):
    expected_pins = {RECON: RECON_SHA, REPRESENTATION: REP_SHA}
    for name, expected in expected_pins.items():
        require(pin(BASE / name)["sha256"] == expected, "frozen input changed: " + name)
    run_pin = pin(run_file)
    actual = load(run_file)
    reconciliation = load(BASE / RECON)
    invocations = load(BASE / REPRESENTATION)["image_invocations"]
    require(len(invocations) == 12 and len({p["name"] for p in invocations}) == 12,
            "expected all twelve CTMs")
    strips = {p["name"]: p for p in invocations}
    require(actual["inputs"] == actual["inputs_after"], "producer input pins changed")
    before = {name: pin(BASE / name) for name in actual["inputs"]}
    require(before == actual["inputs"], "producer input pins differ from current files")
    require(all(before.get(name) == expected for name, expected in reconciliation["verified_input_pins"].items()),
            "producer omitted or changed reconciliation pins")
    self_before = pin(Path(__file__))
    expected_axes = {panel + "-" + reader: axis_intervals(panel, reader)
                     for panel in ("F", "E") for reader in ("root", "independent")}
    require(actual["axis_boxes"] == serialized(expected_axes), "axis-box mismatch")
    require(actual["assumptions"] == ["Hidentity", "Hsupport", "Hink0"], "assumptions changed")
    require(actual["human_accepted"] is False and actual["shared_axis_parameters"] is True,
            "acceptance/correlation flags changed")
    require(all(actual[k] is None for k in ("common_support", "quantile_targets", "model_discrepancies")),
            "unauthorized downstream result")
    reading_index = {r["reader_path"]: r for r in actual["readings"]}
    require(len(reading_index) == len(actual["readings"]) == 34, "duplicate/missing readings")
    counts = Counter()
    reasons = Counter()
    pair_counts = {}
    records_checked = []
    for pair in reconciliation["pairs"]:
        pair_counts[pair["pair"]] = Counter()
        for region in pair["completed_footprints"]:
            counts["regions"] += 1
            for reader in region["readers"]:
                name = reader["path"]
                source = load(BASE / name)
                wanted = expected_rows(source, region, pair["pair"][0], strips[region["source"]])
                found = reading_index[name]
                require(found["pair"] == pair["pair"] and found["source"] == region["source"],
                        "reading provenance mismatch: " + name)
                require(len(found["rows"]) == len(wanted) == reader["route_records"],
                        "record count mismatch: " + name)
                for observed, expected in zip(found["rows"], wanted):
                    location = name + ":" + expected["route"] + ":" + str(expected["column"])
                    expected = serialized(expected)
                    for field, value in expected.items():
                        require(observed.get(field) == value, "mismatch " + location + ":" + field)
                    counts["records"] += 1
                    pair_counts[pair["pair"]]["records"] += 1
                    reasons.update(expected["reasons"])
                    if expected["native_rectangle"] is not None:
                        counts["converted_rectangles"] += 1
                    if expected["conditional_window"]:
                        counts["conditional_windows"] += 1
                        counts["physical_axis_hulls"] += len(expected["physical_windows"])
                        pair_counts[pair["pair"]]["conditional_windows"] += 1
                expected_summary = {"records": len(wanted),
                    "conditional_windows": sum(r["conditional_window"] for r in wanted),
                    "reasons_nonexclusive": dict(Counter(k for r in wanted for k in r["reasons"]))}
                require(found["summary"] == expected_summary, "reading summary mismatch: " + name)
                records_checked.append(name)
    require(counts["regions"] == 17 and counts["records"] == actual["records"] == 10840,
            "scope differs from all 10840 records/17 regions")
    require(len(pair_counts) == 14 and set(records_checked) == set(reading_index), "pair/reading scope mismatch")
    require({name: pin(BASE / name) for name in before} == before, "input changed during independent check")
    require(pin(run_file) == run_pin and pin(Path(__file__)) == self_before, "run/checker changed during check")
    return {"status": "pass_conditional_arithmetic_only", "coverage": dict(counts),
            "pairs": pair_counts, "readings": len(records_checked),
            "reason_counts_nonexclusive": dict(reasons), "inputs_pinned": len(before),
            "run": str(run_file), "run_pin": run_pin, "checker_pin": self_before,
            "independence": "Raw annotations and raw decimal CTMs; no producer, screen or registration imports. Output schema was inspected; not blind.",
            "limits": "No source pixels, support unions, confidence coverage, hypothesis verification or human curve acceptance."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="?", type=Path, default=HERE / "run01.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    checks = []
    try:
        checks = manual_checks()
        receipt = {"status": "self_checks_pass"} if args.self_test else verify(args.run.resolve())
        receipt["manual_checks"] = checks
        print(json.dumps(receipt, indent=2, sort_keys=True))
    except (AssertionError, KeyError, TypeError, ValueError, OSError) as error:
        print(json.dumps({"status": "fail", "error_type": type(error).__name__,
                          "error": str(error), "completed_manual_checks": checks}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

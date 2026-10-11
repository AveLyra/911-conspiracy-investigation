#!/usr/bin/env python3
"""Classify A/B/C diffs and sample temperature ratios. Research only."""

from __future__ import annotations

import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
THERMAL = ROOT / "exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539/ANSYS Thermal Data.zip"

TEMP_RE = re.compile(r"TEMP\s*,\s*([-+0-9.Ee]+)", re.I)


def case_of(name: str) -> str:
    if name.startswith("CaseA_Temps/"):
        return "A"
    if name.startswith("CaseB_Temps/"):
        return "B"
    if name.startswith("CaseC_Temps/"):
        return "C"
    return "?"


def klass(base: str) -> str:
    if re.match(r"WTC7-\d+\.int$", base):
        return "hour_driver"
    if re.match(r"WTC7-Fl\d{2}-\d+\.int$", base):
        return "floor_hour_driver"
    if "SLNo" in base:
        return "slno"
    if "SLAB" in base:
        return "slab"
    if "Core" in base:
        return "core"
    if re.search(r"-\dC\d+", base):
        return "member"
    return "other"


def sample_temps(data: bytes, limit: int = 30) -> list[float]:
    vals = []
    for raw in data.splitlines():
        match = TEMP_RE.search(raw.decode("latin-1", errors="replace"))
        if not match:
            continue
        vals.append(float(match.group(1)))
        if len(vals) >= limit:
            break
    return vals


def mean(vals: list[float]) -> float | None:
    return sum(vals) / len(vals) if vals else None


def main() -> None:
    out: dict = {}
    with zipfile.ZipFile(THERMAL) as archive:
        paths = defaultdict(dict)
        for info in archive.infolist():
            if info.is_dir():
                continue
            paths[Path(info.filename).name][case_of(info.filename)] = info.filename

        ac_classes = Counter()
        ac_examples = defaultdict(list)
        for base, mapping in paths.items():
            if "A" not in mapping or "C" not in mapping:
                continue
            a = archive.read(mapping["A"])
            c = archive.read(mapping["C"])
            if a == c:
                continue
            key = klass(base)
            ac_classes[key] += 1
            if len(ac_examples[key]) < 8:
                ac_examples[key].append({"base": base, "a": len(a), "c": len(c)})
        out["ac_diff_classes"] = dict(ac_classes)
        out["ac_examples"] = {k: v for k, v in ac_examples.items()}

        slabs = [
            "CaseA_Temps/WTC7-Fl07-SLAB-1.int",
            "CaseB_Temps/INTFILES+10%14SEP07/WTC7-Fl07-SLAB-1.int",
            "CaseC_Temps/WTC7-Fl07-SLAB-1.int",
        ]
        out["slab_heads"] = {}
        for name in slabs:
            data = archive.read(name)
            lines = data.decode("latin-1", errors="replace").splitlines()[:12]
            out["slab_heads"][name] = {
                "size": len(data),
                "lines": [line[:160] for line in lines],
            }

        drivers = {}
        for hour in (1, 6, 12):
            base = f"WTC7-{hour}.int"
            row = {}
            for case in "ABC":
                text = archive.read(paths[base][case]).decode("latin-1", errors="replace")
                row[case] = {
                    "sha": __import__("hashlib").sha256(text.encode("latin-1")).hexdigest()[:16],
                    "text": text,
                }
            drivers[base] = row
        out["hour_drivers"] = {
            base: {case: payload["text"] for case, payload in row.items()}
            for base, row in drivers.items()
        }

        sample_bases = []
        for prefix in ("WTC7-Fl07", "WTC7-Fl08", "WTC7-Fl11", "WTC7-Fl13", "WTC7-Fl14"):
            for suffix in ("-SLAB-1.int", "-Core1-1.int", "-1C101-1.int", "-2.int"):
                sample_bases.append(prefix + suffix)
        sample_bases.extend(
            [
                "WTC7-Fl08-1C137-2.int",
                "WTC7-Fl10-SLAB-12.int",
                "WTC7-Fl12-Core2-8.int",
                "WTC7-Fl09-Core3-5.int",
            ]
        )

        ratios = []
        for base in sample_bases:
            mapping = paths.get(base)
            if not mapping or "A" not in mapping:
                continue
            row = {"base": base, "klass": klass(base)}
            means = {}
            for case in "ABC":
                name = mapping.get(case)
                if not name:
                    continue
                vals = sample_temps(archive.read(name))
                row[f"{case}_n"] = len(vals)
                row[f"{case}_mean"] = mean(vals)
                means[case] = mean(vals)
            if means.get("A") and means.get("B"):
                row["B_over_A"] = means["B"] / means["A"]
            if means.get("A") and means.get("C"):
                row["C_over_A"] = means["C"] / means["A"]
            if means.get("C") and means.get("B"):
                row["B_over_C"] = means["B"] / means["C"]
            ratios.append(row)
        out["ratios"] = ratios

        # Broader member-file ratio histogram for even floors
        hist = Counter()
        counted = 0
        for base, mapping in paths.items():
            if klass(base) != "member":
                continue
            if "A" not in mapping or "B" not in mapping:
                continue
            a_vals = sample_temps(archive.read(mapping["A"]), 12)
            b_vals = sample_temps(archive.read(mapping["B"]), 12)
            if not a_vals or not b_vals or mean(a_vals) in (None, 0):
                continue
            ratio = mean(b_vals) / mean(a_vals)
            if ratio < 0.95:
                bucket = "lt_0.95"
            elif ratio < 1.02:
                bucket = "0.95-1.02"
            elif ratio < 1.08:
                bucket = "1.02-1.08"
            elif ratio < 1.12:
                bucket = "1.08-1.12"
            else:
                bucket = "gt_1.12"
            hist[bucket] += 1
            counted += 1
            if counted >= 400:
                break
        out["member_BA_ratio_hist"] = {"n": counted, "buckets": dict(hist)}

    dest = HERE / "phase3-followup.json"
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(dest)
    print("ac_classes", out["ac_diff_classes"])
    print("slab0", out["slab_heads"][slabs[0]]["lines"][:6])
    print("WTC7-1 A")
    print(out["hour_drivers"]["WTC7-1.int"]["A"])
    print("WTC7-1 B")
    print(out["hour_drivers"]["WTC7-1.int"]["B"])
    print("WTC7-1 C")
    print(out["hour_drivers"]["WTC7-1.int"]["C"])
    print("hist", out["member_BA_ratio_hist"])
    for row in ratios:
        print(row)


if __name__ == "__main__":
    main()

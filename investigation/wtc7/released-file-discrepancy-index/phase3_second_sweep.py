#!/usr/bin/env python3
"""Second sweep: remaining unread classes after DISC-001-028.

Read-only of exhibits/raw. Writes only under this folder and /tmp.
Does not execute LS-DYNA or ANSYS. Does not print letter bodies with
personal addresses.
"""

from __future__ import annotations

import email
import hashlib
import json
import re
import zipfile
from collections import Counter, defaultdict
from email import policy
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
JUNE = ROOT / "exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539"
THERMAL = JUNE / "ANSYS Thermal Data.zip"
EML = ROOT / "exhibits/raw/Interim Response #1 - DOC-NIST-2024-000233 2025-06-05T12_20_28-07_00.eml"
TMP = Path("/tmp/disc-second-sweep")
SMALL = 2048
BF_RE = re.compile(r"^BF,\s*(\d+)\s*,\s*TEMP\s*,\s*([-+0-9.Ee]+)", re.I)
INPUT_RE = re.compile(r"/INPUT|#include|\*INCLUDE", re.I)
FLAG_RE = re.compile(
    r"\b(delete|delet|decouple|remove|restart|instantaneous|3\.5\s*hr|4\.0\s*hr|4\.1\s*hr|no-conn)\b",
    re.I,
)
COMMENT_START = re.compile(r"^\s*(!|\$\*|\$)")
PNG_TEXT_CHUNKS = {b"tEXt", b"iTXt", b"zTXt"}
INTEREST = re.compile(
    r"LS-DYNA|ANSYS|8,91|8910|25644|25,644|4\.1|3\.5|connection|additional files|input file",
    re.I,
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def case_of(name: str) -> str:
    if name.startswith("CaseA_Temps/"):
        return "A"
    if name.startswith("CaseB_Temps/"):
        return "B"
    if name.startswith("CaseC_Temps/"):
        return "C"
    return "?"


def png_text_keys(data: bytes) -> list[str]:
    keys = []
    pos = 8
    end = len(data)
    while pos + 12 <= end:
        length = int.from_bytes(data[pos : pos + 4], "big")
        ctype = data[pos + 4 : pos + 8]
        start = pos + 8
        stop = start + length
        if stop + 4 > end:
            break
        if ctype in PNG_TEXT_CHUNKS:
            payload = data[start:stop]
            key = payload.split(b"\x00", 1)[0].decode("latin-1", errors="replace")[:80]
            keys.append(f"{ctype.decode()}:{key}")
        pos = stop + 4
        if ctype == b"IEND":
            break
    return keys


def sample_temps(data: bytes, limit: int = 40) -> dict:
    temps = []
    for raw in data.splitlines():
        match = BF_RE.match(raw.decode("latin-1", errors="replace"))
        if not match:
            continue
        temps.append(float(match.group(2)))
        if len(temps) >= limit:
            break
    if not temps:
        return {"n": 0}
    return {
        "n": len(temps),
        "min": min(temps),
        "max": max(temps),
        "mean": sum(temps) / len(temps),
    }


def scan_body_flags(data: bytes, source: str, skip_first: int = 0) -> list[dict]:
    hits = []
    text = data.decode("latin-1", errors="replace")
    for index, line in enumerate(text.splitlines(), 1):
        if index <= skip_first:
            continue
        if not line or line.startswith("BF,") or line.startswith("BFE,"):
            continue
        if not (INPUT_RE.search(line) or FLAG_RE.search(line) or COMMENT_START.match(line)):
            continue
        hits.append({"source": source, "line": index, "text": line[:180]})
        if len(hits) >= 20:
            break
    return hits


def extract_june_letter() -> dict:
    TMP.mkdir(parents=True, exist_ok=True)
    message = email.message_from_bytes(EML.read_bytes(), policy=policy.default)
    found = []
    for part in message.walk():
        filename = part.get_filename() or ""
        if not filename.lower().endswith(".pdf"):
            continue
        payload = part.get_payload(decode=True) or b""
        dest = TMP / Path(filename).name
        dest.write_bytes(payload)
        found.append(
            {
                "filename": filename,
                "size": len(payload),
                "sha256": sha256(payload),
                "path": str(dest),
            }
        )
    out = {"attachments": found, "mentions": []}
    if not found:
        out["blocker"] = "no_pdf_attachment"
        return out
    reader = PdfReader(found[0]["path"])
    out["pages"] = len(reader.pages)
    mentions = []
    for index, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        for line in text.splitlines():
            compact = " ".join(line.split())
            if INTEREST.search(compact):
                mentions.append({"page": index, "text": compact[:240]})
    out["mentions"] = mentions
    return out


def main() -> None:
    report: dict = {
        "scope": "Second sweep after DISC-001-028: A/B/C identity, large-body flags, PNG text, SRC-029 letter.",
        "scanner": str(HERE.relative_to(ROOT) / "phase3_second_sweep.py"),
    }

    hash_pairs = {"AB_same": 0, "AB_diff": 0, "AC_same": 0, "AC_diff": 0, "shared_ABC": 0}
    size_pairs = {"AB_size_diff": 0, "AC_size_diff": 0}
    ab_diff_examples = []
    ac_diff_examples = []
    by_case: dict[str, dict[str, tuple[int, str]]] = {"A": {}, "B": {}, "C": {}}
    png_text = Counter()
    png_with_text = 0
    nul_compare = {}
    large_body_hits = []
    large_scanned = 0
    large_skipped_header_only_no_hit = 0
    temp_pairs = []

    sample_names = [
        "WTC7-Fl07-SLAB-1.int",
        "WTC7-Fl08-SLAB-1.int",
        "WTC7-Fl11-SLAB-6.int",
        "WTC7-Fl13-Core1-4.int",
        "WTC7-Fl08-1C101-1.int",
        "WTC7-Fl12-2C140-8.int",
        "WTC7-Fl07-SLNo-1.int",
    ]

    with zipfile.ZipFile(THERMAL) as archive:
        files = [info for info in archive.infolist() if not info.is_dir()]
        report["member_count"] = len(files)
        paths = defaultdict(dict)
        for info in files:
            base = Path(info.filename).name
            case = case_of(info.filename)
            paths[base][case] = info.filename

        shared = [base for base, mapping in paths.items() if {"A", "B", "C"} <= set(mapping)]
        report["shared_basename_count"] = len(shared)

        for info in files:
            case = case_of(info.filename)
            base = Path(info.filename).name
            digest = hashlib.sha256(archive.read(info.filename)).hexdigest()
            by_case[case][base] = (info.file_size, digest)
            if info.filename.endswith(".png"):
                keys = png_text_keys(archive.read(info.filename))
                if keys:
                    png_with_text += 1
                    png_text.update(keys)

        for base in shared:
            a_size, a_hash = by_case["A"][base]
            b_size, b_hash = by_case["B"][base]
            c_size, c_hash = by_case["C"][base]
            hash_pairs["shared_ABC"] += 1
            if a_hash == b_hash:
                hash_pairs["AB_same"] += 1
            else:
                hash_pairs["AB_diff"] += 1
                if len(ab_diff_examples) < 25:
                    ab_diff_examples.append({"base": base, "a_size": a_size, "b_size": b_size})
            if a_hash == c_hash:
                hash_pairs["AC_same"] += 1
            else:
                hash_pairs["AC_diff"] += 1
                if len(ac_diff_examples) < 25:
                    ac_diff_examples.append({"base": base, "a_size": a_size, "c_size": c_size})
            if a_size != b_size:
                size_pairs["AB_size_diff"] += 1
            if a_size != c_size:
                size_pairs["AC_size_diff"] += 1

        ac_diff_classes = Counter()
        for base, mapping in paths.items():
            if "A" in mapping and "C" in mapping:
                if by_case["A"][base][1] != by_case["C"][base][1]:
                    if re.match(r"WTC7-\d+\.int$", base):
                        ac_diff_classes["hour_driver"] += 1
                    elif re.match(r"WTC7-Fl\d{2}-\d+\.int$", base):
                        ac_diff_classes["floor_hour_driver"] += 1
                    else:
                        ac_diff_classes["other"] += 1

        ab_diff_classes = Counter()
        for base, mapping in paths.items():
            if "A" in mapping and "B" in mapping:
                if by_case["A"][base][1] != by_case["B"][base][1]:
                    if re.match(r"WTC7-\d+\.int$", base):
                        ab_diff_classes["hour_driver"] += 1
                    elif re.match(r"WTC7-Fl\d{2}-\d+\.int$", base):
                        ab_diff_classes["floor_hour_driver"] += 1
                    elif "SLAB" in base:
                        ab_diff_classes["slab"] += 1
                    elif "Core" in base:
                        ab_diff_classes["core"] += 1
                    elif re.search(r"1C|2C", base):
                        ab_diff_classes["member"] += 1
                    else:
                        ab_diff_classes["other"] += 1

        report["hash_pairs"] = hash_pairs
        report["size_pairs"] = size_pairs
        report["ab_diff_classes"] = dict(ab_diff_classes)
        report["ac_diff_classes"] = dict(ac_diff_classes)
        report["ab_diff_examples"] = ab_diff_examples
        report["ac_diff_examples"] = ac_diff_examples

        for base in sample_names:
            row = {"base": base}
            for case in "ABC":
                name = paths.get(base, {}).get(case)
                if not name:
                    row[case] = None
                    continue
                data = archive.read(name)
                row[case] = {"size": len(data), **sample_temps(data)}
            if row.get("A") and row.get("B") and row["A"].get("mean") and row["B"].get("mean"):
                row["B_over_A"] = row["B"]["mean"] / row["A"]["mean"]
            if row.get("A") and row.get("C") and row["A"].get("mean") and row["C"].get("mean"):
                row["C_over_A"] = row["C"]["mean"] / row["A"]["mean"]
            temp_pairs.append(row)
        report["temp_pairs"] = temp_pairs

        nul_name = "CaseB_Temps/INTFILES+10%14SEP07/WTC7-Fl08-1C137-2.int"
        twins = {
            "A": "CaseA_Temps/WTC7-Fl08-1C137-2.int",
            "C": "CaseC_Temps/WTC7-Fl08-1C137-2.int",
        }
        nul = archive.read(nul_name)
        nul_compare["B_size"] = len(nul)
        nul_compare["B_nul_count"] = nul.count(b"\x00")
        nul_compare["B_head"] = nul[:60].decode("latin-1", errors="replace")
        for case, name in twins.items():
            data = archive.read(name)
            nul_compare[case] = {
                "size": len(data),
                "sha256": sha256(data),
                "head": data[:80].decode("latin-1", errors="replace"),
                "same_as_B": data == nul,
            }
        report["nul_compare"] = nul_compare

        for info in files:
            if not info.filename.endswith(".int"):
                continue
            if info.file_size <= SMALL:
                continue
            data = archive.read(info.filename)
            hits = scan_body_flags(data, info.filename, skip_first=0)
            large_scanned += 1
            nonempty = [h for h in hits if not h["text"].lstrip().startswith("/input")]
            # keep /input only if it appears after the usual driver header zone
            late_inputs = [h for h in hits if h["line"] > 40 and "/input" in h["text"].lower()]
            interesting = nonempty + late_inputs
            if interesting:
                large_body_hits.extend(interesting[:8])
            else:
                large_skipped_header_only_no_hit += 1

        report["large_int_scanned"] = large_scanned
        report["large_body_non_bf_hits"] = large_body_hits[:80]
        report["large_body_hit_count"] = len(large_body_hits)
        report["large_no_extra_flag"] = large_skipped_header_only_no_hit
        report["png_with_text"] = png_with_text
        report["png_text_keys"] = dict(png_text)

        hour_drivers = {}
        for case in "ABC":
            name = paths["WTC7-1.int"][case]
            text = archive.read(name).decode("latin-1", errors="replace")
            hour_drivers[case] = {
                "size": len(text),
                "sha256": sha256(text.encode("latin-1")),
                "fl07_live": bool(re.search(r"(?m)^(?!!).*/input,WTC7-Fl07", text)),
                "fl07_commented": bool(re.search(r"(?m)^!.*/input,WTC7-Fl07", text)),
                "lines": len(text.splitlines()),
            }
        report["hour_driver_wtc7_1"] = hour_drivers

    report["june_letter"] = extract_june_letter()
    report["scanner_sha256"] = sha256((HERE / "phase3_second_sweep.py").read_bytes())

    dest = HERE / "phase3-second-sweep.json"
    dest.write_text(json.dumps(report, indent=2) + "\n")
    print(dest)
    print("members", report["member_count"], "shared", report["shared_basename_count"])
    print("hashes", report["hash_pairs"])
    print("ab_classes", report["ab_diff_classes"])
    print("ac_classes", report["ac_diff_classes"])
    print("temps")
    for row in temp_pairs:
        print(" ", row["base"], {k: row[k] for k in row if k != "base"})
    print("large_scanned", large_scanned, "extra_hits", len(large_body_hits))
    print("png_text", png_with_text, dict(png_text))
    print("nul", {k: v for k, v in nul_compare.items() if k != "B_head"})
    letter = report["june_letter"]
    print("letter_pages", letter.get("pages"), "mentions", len(letter.get("mentions", [])))
    for item in letter.get("mentions", []):
        print(" L", item["page"], item["text"])


if __name__ == "__main__":
    main()

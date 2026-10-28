"""Read-only checks of pinned public PDFs; not call authentication or replication.

Run with Python containing PyMuPDF:
    python verify_records.py T01.pdf T02.pdf > VERIFICATION.json
The PDF arguments may point to freshly downloaded entities. They are never edited.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

import fitz

EXPECTED = [
    ("T01", "9671b7afe9a45928dcbe053e567b7f830876bc31e32a1d221b39fa59493d5bbb", 121),
    ("T02", "8e32a96701a04a3d9f4e979158bb5ecd753111d1d9f50f7b7a44f003d3ca2e1b", 4),
]


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Supply the two preserved PDF paths, T01 then T02")
    results = []

    def check(name, condition, detail):
        results.append({"check": name, "passed": bool(condition), "detail": detail})

    docs = {}
    for argument, (sid, digest, pages) in zip(sys.argv[1:], EXPECTED):
        data = Path(argument).read_bytes()
        check(sid + " pinned bytes", hashlib.sha256(data).hexdigest() == digest,
              {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        docs[sid] = fitz.open(stream=data, filetype="pdf")
        check(sid + " page count", len(docs[sid]) == pages, len(docs[sid]))

    def page(sid, number):
        return re.sub(r"\s+", " ", docs[sid][number - 1].get_text())

    p94 = page("T01", 94)
    p95 = page("T01", 95)
    n265 = p94.split("265 The records available", 1)[1].split("266 A witness", 1)[0]
    check("Four printed connected-call starts",
          re.findall(r"9:\d{2}:\d{2}", n265) == ["9:15:34", "9:20:15", "9:25:48", "9:30:56"],
          "T01 p94 note265; starts do not prove caller or leg identity")
    check("Printed duration and arithmetic",
          "9:25:48 for two minutes, 34 seconds" in n265 and 2 * 60 + 34 == 154,
          {"printed_seconds": 154, "previous_other_source_seconds": 159, "difference": 5})
    check("Express attribution limit",
          "do not allow for a determination" in n265 and "all family members" in n265,
          "Limitation and stated family-canvass rationale present; no unique network join checked")
    n266 = p94.split("266 A witness", 1)[1]
    n267 = p95.split("267 FBI", 1)[1].split("268 The", 1)[0]
    check("Witness citation September14", "September 14, 2001" in n266,
          "T01 p94 note266; also visually checked")
    check("Witness citation September4", "Sept 4, 2001" in n267,
          "T01 p95 note267; also visually checked; same witness/report not established")
    check("Named DOJ log and reported time",
          "Watch Officer Log, 0001-2400 HRS" in p95 and "entry at 9:33" in p95,
          "T01 p95 note268; actual log not acquired")
    check("Staff report EDT convention",
          "Eastern Daylight Time unless otherwise" in page("T01", 2),
          "T01 p2; does not calibrate unacquired source clocks")
    p3 = page("T02", 3)
    check("MFR recollection limitation", "had trouble recalling any specific times" in p3,
          "T02 p3; sequence limitation also explicit")
    check("MFR elapsed anchors labeled approximate",
          "11 minutes, 27 seconds" in p3 and "thirty-nine seconds" in p3
          and "7:32" in p3 and "7:40" in p3 and "Central Time" in p3,
          "T02 p3; staff-derived tape anchors, not independently calibrated here")
    check("MFR sequencing limitation",
          "hard for him to sequence the order" in page("T02", 4),
          "T02 p4")
    for argument, (sid, digest, _) in zip(sys.argv[1:], EXPECTED):
        check(sid + " bytes unchanged after reading",
              hashlib.sha256(Path(argument).read_bytes()).hexdigest() == digest,
              "No PDF write operation performed")
    result = {
        "checks": results,
        "passed": sum(r["passed"] for r in results),
        "total": len(results),
        "scope": "Pinned-byte, page and selected-content checks; images read separately",
        "historical_authentication": False,
        "native_carrier_replication": False,
        "search_cap_met": False,
        "search_operations": 17,
        "search_cap": 16,
    }
    print(json.dumps(result, indent=2))
    if result["passed"] != result["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

"""Verify archived notice/request bodies and the bounded content/date checks.

Requires PyMuPDF and Tesseract. Supply the folder with the six held response files.
"""
import argparse
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import subprocess

import fitz


def check(condition, description):
    if not condition:
        raise SystemExit(f"Failed: {description}")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("sources", type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
for pin in ledger["sources"]:
    data = (args.sources / pin["file"]).read_bytes()
    check(len(data) == pin["bytes"], f"{pin['file']} length")
    check(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{pin['file']} hash")

metadata = json.loads((args.sources / "record.body").read_bytes())
check(metadata["publication_date"] == "2009-08-14", "notice date")
check(metadata["document_number"] == "E9-19535" and metadata["start_page"] == 41124, "notice identifier")
check(metadata["corrections"] == [], "scoped metadata corrections field")
availability = json.loads((args.sources / "archive-availability.body").read_bytes())
check(availability["archived_snapshots"]["closest"]["timestamp"] == "20090902014628", "advertised capture")
with fitz.open(args.sources / "notice.body", filetype="pdf") as notice:
    text = " ".join(notice[0].get_text().split())
    check("c.o.b., August 24, 2009." in text, "printed deadline")
    check("within ten (10) working days" in text, "relative deadline")
    check("FOIArequests09_15_42_63_88.pdf" in text, "packet filename")

pub = date.fromisoformat(metadata["publication_date"])
for start, expected in [(0, "2009-08-27"), (1, "2009-08-28")]:
    days = [pub + timedelta(days=i) for i in range(start, 20)]
    weekday_ten = [day for day in days if day.weekday() < 5][9]
    check(weekday_ten.isoformat() == expected, "weekday-only interval")

with fitz.open(args.sources / "packet-replay.body", filetype="pdf") as packet:
    check(len(packet) == 16, "16 archived packet pages")
    for page, anchor in {
        1: "November 20, 2008",
        4: "All Photos, Videos, still or moving images",
        11: "February 27, 2009",
        12: "February 26, 2009",
        13: "February 26, 2009",
        14: "April 21, 2009",
        15: "Native source files for all images in Chapter 5",
    }.items():
        check(anchor in " ".join(packet[page - 1].get_text().split()), f"packet p. {page}")
    for page, anchor in {
        5: "request all of the photographs and videos collected",
        6: "their native format whenever possible, with all metadata included",
    }.items():
        pix = packet[page - 1].get_pixmap(matrix=fitz.Matrix(2, 2), colorspace=fitz.csGRAY, alpha=False)
        ocr = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "6"],
                             input=pix.tobytes("png"), capture_output=True, check=True)
        check(anchor in " ".join(ocr.stdout.decode().split()), f"packet p. {page} OCR")
print("Six source hashes and lengths, notice dates and identifiers, two weekday counts, 16-page packet and nine packet anchors passed")

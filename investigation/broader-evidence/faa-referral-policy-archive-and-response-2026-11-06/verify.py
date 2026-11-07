#!/usr/bin/env python3
"""Verify pinned downloads and selected fields. Usage: python verify.py SOURCE_DIR."""

import hashlib
import json
from pathlib import Path
import re
import sys

import fitz


def require(test, detail):
    if not test:
        raise ValueError(detail)


ANCHORS = {
    "audit": {9: {19: "mid-2015 and 2017", 30: "OIG External"},
              10: {41: "2150.3B"}, 11: {40: "2150.3B", 45: "2150.2B"},
              13: {16: "June 6, 2017", 19: "May 26, 2017"},
              19: {32: "all three recommendations resolved but open"},
              20: {33: "promptness of referrals could not be quantified", 40: "mid-2015"},
              29: {7: "January 2019", 12: "July 2019", 23: "one-time training"}},
    "alternate": {11: {83: "2150.3B", 88: "2150.2B"}},
    "historical": {1: {2: "2150.3A"}, 35: {53: "OFFICE OF INSPECTOR GENERAL"},
                   36: {16: "enforcing compliance with aviation safety"}},
    "released": {13: {63: "I08E00012SINV – ALERTS", 64: "08IHA593001 - TIGR", 65: "2/04/2009", 74: "FINAL"}},
    "index": {2: {14: "closed during calendar year 2012."},
              4: {10: "TIGR Case", 16: "Date", 17: "Closed", 51: "CLOSED 07/16/2011"},
              8: {48: "I10Z0000110100", 54: "042R005C001", 55: "CLOSED"}},
}


def word(page, token, left, right, top, bottom):
    matches = [v for v in page.get_text("words")
               if v[4] == token and left <= v[0] < right and top <= v[1] < bottom]
    require(len(matches) == 1, f"expected one {token} in the selected column and row")
    return matches[0]


def table_checks(key, doc):
    if key == "index":
        new = word(doc[7], "I10Z0000110100", 45, 100, 135, 150)
        old = word(doc[7], "042R005C001", 365, 420, 135, 150)
        require(abs(new[1] - old[1]) < 0.1, "case fields are on different rows")
        word(doc[3], "07/16/2011", 470, 510, 98, 110)
    if key == "audit":
        page = doc[12]
        reported = [word(page, value, 280, 308, top, top + 14)[4]
                    for value, top in [("26", 250), ("351", 277), ("5", 306)]]
        combined = word(page, "204", 400, 437, 277, 291)[4]
        require(sum(map(int, reported)) == 382 and combined == "204", "FAA table values differ")
        bars = [path["rect"] for path in page.get_drawings()
                if 273 <= path["rect"].y0 <= 304 and path["rect"].width > 10]
        require(len(bars) >= 4 and all(bar.x1 < 308 for bar in bars),
                "FAA row separators no longer leave the ALERTS cell spanning the three rows")


def status_check(data):
    html = data.decode()
    blocks = re.split(r'<div class="recommendation closed">', html)[1:]
    found = [(re.search(r"No\. (\d+) to OST", block)[1],
              re.search(r"\d{2}\.\d{2}\.\d{4}", block)[0]) for block in blocks]
    require(found == [("1", "12.04.2020"), ("2", "11.29.2022"), ("3", "09.07.2021")],
            "recommendation/date pairs differ")


def main():
    source_dir = Path(sys.argv[1])
    pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    for source in pins["sources"]:
        key = source["id"]
        data = (source_dir / source["file"]).read_bytes()
        require(len(data) == source["bytes"], f"{key} size differs")
        require(hashlib.sha256(data).hexdigest() == source["sha256"], f"{key} hash differs")
        if key == "status":
            status_check(data)
        if source["pdf_pages"] is not None:
            with fitz.open(stream=data, filetype="pdf") as doc:
                require(len(doc) == source["pdf_pages"], f"{key} page count differs")
                for page, anchors in ANCHORS[key].items():
                    lines = doc[page - 1].get_text().splitlines()
                    for line, snippet in anchors.items():
                        require(snippet in lines[line - 1], f"{key} p. {page} l. {line} differs")
                table_checks(key, doc)
        print(f"Verified {key}")
    print("Verified exact source hashes, selected PDF anchors, row geometry and closure-date joins")


if __name__ == "__main__":
    main()

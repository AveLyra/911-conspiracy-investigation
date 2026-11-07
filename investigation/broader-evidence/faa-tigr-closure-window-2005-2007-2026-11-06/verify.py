#!/usr/bin/env python3
"""Check the pinned release PDFs and the readable 2007 enclosure.

Usage: python verify.py SOURCE_DIRECTORY
Requires PyMuPDF and Tesseract, with the English model available.
"""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import fitz


TARGET = re.compile(
    r"042\s*R\s*0\s*1\s*2\s*2\s*0\s*0\s*1|NORAD|9\s*[-/.–]\s*11|"
    r"September\s+11|Commission|FAA\s+.{0,70}statement",
    re.IGNORECASE,
)
ANCHORS = {
    "period.pdf": {1: {27: "October 2005 – July 2007"},
                   2: {7: "2007", 12: "since October 1, 2005", 15: "(b)(2), (6) and (7)(C)"},
                   4: {1: "CASE_NO", 5: "TITLE"},
                   7: {29: "Lower Manhattan Recovery Project, FY 2007"}},
    "early.pdf": {2: {11: "since January 1, 2003", 12: "dates that each case was opened and closed"},
                  4: {1: "CASE_NO", 37: "1/1/03 - 11/9/05", 38: "OPENED", 39: "CLOSED"}},
    "transition.pdf": {2: {13: "October 1, 2008", 16: "blank areas", 30: "producing 6 pages"},
                       4: {1: "10/1/08 - 3/12/10", 3: "Case Number"}},
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_list(document):
    for number in range(4, 11):
        page = document[number - 1]
        gray = page.get_pixmap(colorspace=fitz.csGRAY, alpha=False)
        samples = gray.samples
        dark_pixels = sum(samples[y * gray.width + 110] < 75 for y in range(80, 540))
        require(dark_pixels >= 300, f"expected dark band in case-number column on page {number}")
        raster = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
        result = subprocess.run(
            ["tesseract", "stdin", "stdout", "--psm", "6"],
            input=raster.tobytes("png"), capture_output=True, check=True,
        )
        ocr = result.stdout.decode()
        require(len(ocr.split()) >= 50, f"insufficient OCR on page {number}")
        for text in (ocr, page.get_text()):
            require(not TARGET.search(" ".join(text.split())), f"target match on page {number}")
        if number == 7:
            require("Lower Manhattan Recovery Project" in " ".join(ocr.split()),
                    "known visible title did not survive OCR")
        print(f"Page {number}: {dark_pixels} dark pixels in 460-pixel column sample, zero target matches")


def main():
    source_directory = Path(sys.argv[1])
    pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    for pin in pins["sources"]:
        name = pin["file"]
        data = (source_directory / name).read_bytes()
        require(len(data) == pin["bytes"], f"size differs for {name}")
        require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"hash differs for {name}")
        with fitz.open(stream=data, filetype="pdf") as doc:
            require(len(doc) == pin["pages"], f"page count differs for {name}")
            for number, snippets in ANCHORS[name].items():
                lines = doc[number - 1].get_text().splitlines()
                for line, expected in snippets.items():
                    require(expected in lines[line - 1], f"{name} p. {number} l. {line} differs")
            if name == "period.pdf":
                check_list(doc)
        print(f"Verified {name}")


if __name__ == "__main__":
    main()

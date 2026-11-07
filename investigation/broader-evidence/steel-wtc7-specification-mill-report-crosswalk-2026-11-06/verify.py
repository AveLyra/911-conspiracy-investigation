#!/usr/bin/env python3
"""Run catalog mode with openpyxl and PDF modes with PyMuPDF.

Usage: python verify.py SOURCE_KEY SOURCE_FILE
SOURCE_KEY is a key listed in SOURCE-PINS.json.
The PDF modes check text anchors. Visual comparisons remain a manual step.
"""

import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile


def require(condition, description):
    if not condition:
        raise ValueError(description)


def verify_bytes(data, pin):
    require(len(data) == pin["bytes"], "source length differs")
    require(hashlib.sha256(data).hexdigest() == pin["sha256"], "source SHA-256 differs")


def verify_catalog(data, pin):
    from openpyxl import load_workbook

    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        require(archive.testzip() is None, "ZIP CRC validation failed")
        members = {}
        for name, member_pin in pin["members"].items():
            matches = [p for p in archive.namelist() if PurePosixPath(p).name == name]
            require(len(matches) == 1, f"expected exactly one {name}")
            members[name] = archive.read(matches[0])
            verify_bytes(members[name], member_pin)
        require(not any(re.fullmatch(r"WTCI-000187-P(?:_\d+)?\.PDF", PurePosixPath(p).name, re.I)
                        for p in archive.namelist()), "a candidate scan is a ZIP member")

    book = load_workbook(io.BytesIO(members["tblDocumentMain.xlsx"]), read_only=True, data_only=True)
    assigned = []
    shared_doc_id = []
    for number, row in enumerate(book["tblDocumentMain"].values, 1):
        fields = tuple(row[column] for column in (0, 2, 5, 6, 7, 14, 15, 16))
        if fields[1:3] == ("000187", "P"):
            assigned.append((number, fields))
        if fields[-1] == "W01437":
            shared_doc_id.append((number, fields))
    book.close()
    first = (1035, (1201, "000187", "P", "5/15/2003", "PANYNJ",
                    "W01437, Syska & Hennessy, Mechanical and Electrical Systems (3 books), WTC 7",
                    "12/6/2002", "W01437"))
    second = (1768, (1959, "000229", "P", "6/18/2003", "PANYNJ",
                     "W01437, WTC 7 Tenant Alteration Application, Beam Envelope",
                     "12/6/2002", "W01437"))
    require(assigned == [first], "catalog assigned-ID rows differ")
    require(shared_doc_id == [first, second], "catalog W01437 rows differ")

    found = []
    for number, line in enumerate(members["DirectoryPrint_ScannedPaperDocuments.txt"].splitlines(), 1):
        if re.match(rb"\s+WTCI-000187-P(?:_\d+)?\.PDF\s", line):
            found.append((number, line.decode("ascii").split()))
    sizes = (9553, 2657, 9888, 9648, 965, 8325, 14563, 9762)
    times = ("04:05:02", "04:05:26", "04:07:06", "04:08:44", "04:08:54", "04:10:00", "04:11:38", "04:13:20")
    expected = []
    for index, (size, time) in enumerate(zip(sizes, times), 1):
        suffix = f"_{index:03d}" if index > 1 else ""
        expected.append((4703 + index, [f"WTCI-000187-P{suffix}.PDF", str(size), "KB", "1/22/2010", time, "PM"]))
    require(found == expected, "directory entries differ")
    print("Verified ZIP, two member hashes, one assigned-ID row, two shared DocID rows and eight directory entries")


PDF_ANCHORS = {
    "nist-specifications": (168, {95: {36: "WTC 7 Project Specifications.", 37: "1984. (WTCI-187-P)."},
                                  156: {32: "Mill test reports were to be furnished"},
                                  157: {4: "separate contract for testing and inspection"},
                                  160: {22: "1984. (WTC1-187-P)."}}),
    "nist-construction": (282, {44: {4: "retaining them for 7 years."},
                               64: {13: "after retaining them for about 7 years."},
                               159: {21: "discarded by the general contractor"},
                               164: {30: "separate contract for testing and inspection"},
                               165: {7: "no inspection requirements during construction"}}),
    "filed-materials": (235, {173: {1: "JA-3004", 14: "I have reviewed and analyzed numerous materials",
                                  33: "Section 10B", 47: "11-12"},
                             174: {1: "JA-3005", 16: "1964", 66: "Testwe", 70: "Mill Test"},
                             175: {1: "JA-3006", 16: "Manual of Steel Construction", 19: "1980"}}),
}


def verify_pdf(data, key):
    import fitz

    expected_pages, anchors = PDF_ANCHORS[key]
    with fitz.open(stream=data, filetype="pdf") as document:
        require(len(document) == expected_pages, "physical page count differs")
        for page, checks in anchors.items():
            lines = document[page - 1].get_text().splitlines()
            for number, expected in checks.items():
                require(expected in lines[number - 1], f"anchor differs on page {page}, line {number}")
    print(f"Verified {key} hash, {expected_pages} pages and text anchors")


def main():
    key, source = sys.argv[1:]
    ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    pin = next(record for record in ledger["sources"] if record["key"] == key)
    data = Path(source).read_bytes()
    verify_bytes(data, pin)
    if key == "catalog":
        verify_catalog(data, pin)
    else:
        verify_pdf(data, key)


if __name__ == "__main__":
    main()

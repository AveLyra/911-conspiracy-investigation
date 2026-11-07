#!/usr/bin/env python3
"""Verify the selected public archive members. Usage: python verify.py SOURCE_DIR."""

from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
import zlib

import fitz


ANCHORS = {
    "gte-box13-788.pdf": {
        1: {11: "M-SFA-00006033", 12: "M-SFA-00006046", 13: "14", 15: "1A-1A30336"},
        14: {6: "M-SFA-00006046"}, 15: {29: "M-SFA-00006022"}, 16: {2: "M-SFA-00006023"},
        17: {11: "M-SFA-00006022", 12: "M-SFA-00006023", 13: "2"},
        18: {1: "M-SFA-00006023", 12: "SOURCE ACCN", 13: "6586"},
        19: {11: "M-SFA-00006024", 12: "M-SFA-00006032", 13: "9"},
        20: {84: "Page 2"}, 33: {40: "SOURCE ACCN", 45: "6586", 47: "Page 15"},
        34: {12: "09:35:32-0500", 21: "08:33:53 -0600", 39: "UAL_flt93.xls",
             49: "base64", 52: 'filename="UAL_flt93.xls"', 57: "1A-1A65562", 58: "M-NKA-00001342"},
        35: {48: "1A-1A65562", 49: "M-NKA-00001341"}, 41: {2: "1A-1A65562", 3: "M-NKA-00001348"},
    },
    "team1-request14-withdrawal.pdf": {1: {9: "Pages: 235", 12: "DCI Req. #14", 13: "09-26-2003"}},
    "team1-request24-withdrawal.pdf": {1: {9: "Pages: 237", 12: "DCI Req. #24", 13: "12-22-2003"}},
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def carrier_checks(document):
    require(document.embfile_count() == 0, "unexpected embedded file")
    require(not any(annotation.type[1] == "FileAttachment"
                    for page in document for annotation in page.annots() or ()),
            "unexpected page file attachment")
    for first, second in [(15, 17), (16, 18)]:
        first_xref = document[first - 1].get_images()[0][0]
        second_xref = document[second - 1].get_images()[0][0]
        first_image = document.extract_image(first_xref)["image"]
        second_image = document.extract_image(second_xref)["image"]
        require(first_image != second_image, "scan pair unexpectedly byte-identical")
    relay = datetime.fromisoformat("2001-11-06T09:35:32-05:00")
    date = datetime.fromisoformat("2001-11-06T08:33:53-06:00")
    require((relay - date).total_seconds() == 99, "printed date-field arithmetic differs")


def main():
    source_dir = Path(sys.argv[1])
    pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    for pin in pins["members"]:
        name = pin["file"]
        data = (source_dir / name).read_bytes()
        require(len(data) == pin["bytes"], f"{name} size differs")
        require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{name} hash differs")
        require(f"{zlib.crc32(data):08x}" == pin["crc32"], f"{name} ZIP CRC differs")
        with fitz.open(stream=data, filetype="pdf") as document:
            require(len(document) == pin["pages"], f"{name} page count differs")
            for number, checks in ANCHORS[name].items():
                lines = document[number - 1].get_text().splitlines()
                for line, expected in checks.items():
                    require(expected in lines[line - 1], f"{name} p. {number} l. {line} differs")
            if name == "gte-box13-788.pdf":
                carrier_checks(document)
        print(f"Verified {name}")
    print("Verified page anchors, repeated-label image differences, empty attachment inventories and 99 seconds")


if __name__ == "__main__":
    main()

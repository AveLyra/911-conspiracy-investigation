#!/usr/bin/env python3
"""Usage: python verify.py SOURCE_DIR BOX19_PDF COURT_ZIP PARSER_DIR.

Requires PyMuPDF and the previously published static parser pair in PARSER_DIR.
"""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import zlib

import fitz


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_bytes(path, pin):
    data = path.read_bytes()
    require(len(data) == pin["bytes"], f"length differs for {path.name}")
    require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"hash differs for {path.name}")
    return data


def check_pdf(path, pin, anchors, attachment_inventory=False):
    data = check_bytes(path, pin)
    require(f"{zlib.crc32(data):08x}" == pin["crc32"], f"CRC differs for {path.name}")
    with fitz.open(stream=data, filetype="pdf") as doc:
        require(len(doc) == pin["pages"], f"page count differs for {path.name}")
        for page, checks in anchors.items():
            lines = doc[page - 1].get_text().splitlines()
            for number, snippet in checks.items():
                require(snippet in lines[number - 1], f"{path.name} p. {page} l. {number} differs")
        if attachment_inventory:
            require(doc.embfile_count() == 0, "unexpected embedded file")
            require(not any(a.type[1] == "FileAttachment" for p in doc for a in p.annots() or ()),
                    "unexpected page file attachment")


def check_court(court, parser_dir, pins):
    for entry in pins["parsers"]:
        check_bytes(parser_dir / entry["file"], entry)
    sys.path.insert(0, str(parser_dir.resolve()))
    from structural_context import Bits, check_controls, extract, place_prefix, tags

    check_bytes(court, pins["court_zip"])
    with zipfile.ZipFile(court) as archive:
        raw = archive.read("UA93.swf")
    parsed = extract(raw)
    require(parsed["input_sha256"] == pins["court_swf"]["sha256"], "SWF hash differs")
    require(len(parsed["text_definitions"]) == 420, "SWF definition count differs")
    selected = {
        975: (863074, "Beamer", 866497),
        976: (863120, "Todd", 866514),
        977: (863161, "09:42:44", 866914),
        978: (863208, "0 SECONDS", 866937),
        981: (863457, "09:43:48", 871408),
        983: (863567, "09:43:48", 875736),
        984: (863614, "3,925 SECONDS", 875759),
        986: (863748, "GTE OPERATORLINE LEFT OPEN", 875805),
    }
    definitions = {entry["id"]: entry for entry in parsed["text_definitions"]}
    for cid, (offset, text, _) in selected.items():
        require((definitions[cid]["offset"], definitions[cid]["text"]) == (offset, text),
                f"definition differs for ID {cid}")
    check_controls()
    data = raw if raw[:3] == b"FWS" else b"FWS" + raw[3:8] + zlib.decompress(raw[8:])
    bits = Bits(data, 8)
    bits.rect()
    placements = {offset: place_prefix(body)["character_id"]
                  for code, offset, body, container in tags(data, bits.align() + 4, len(data))
                  if code == 26 and container == "root/sprite-991"}
    for cid, (_, _, offset) in selected.items():
        require(placements.get(offset) == cid, f"placement differs for ID {cid}")
    require(divmod(3925, 60) == (65, 25), "duration conversion differs")


def main():
    source, box19, court, parser = map(Path, sys.argv[1:])
    pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    check_pdf(source / "gte-interview-00595.pdf", pins["members"]["gte-interview-00595.pdf"],
              {1: {8: "May 11, 2004", 31: "took over the headset"},
               3: {5: "15 minutes", 15: "The FBI has the notes"}})
    check_pdf(source / "gte-interview-416.pdf", pins["members"]["gte-interview-416.pdf"],
              {1: {7: "May 11,2004", 26: "took over the headset"},
               3: {4: "15 minutes", 12: "The FBI has the notes"}})
    check_pdf(box19, pins["box19"],
              {24: {10: "M-INT-OQ162543", 11: "28.P350-302-116622", 14: "NCTA_007",
                    29: "Appendix A-3", 31: "updated spreadsheet", 39: "unique number"},
               25: {7: "Duration Connect", 9: "Duration Operator", 10: "3925 seconds",
                    11: "kept the call open", 12: "Scp Duration"},
               33: {5: "302-96202", 35: "three 3 page spreadsheet"}}, attachment_inventory=True)
    check_court(court, parser, pins)
    print("Verified three PDFs, selected source fields, eight exhibit placements and 65:25 conversion")


if __name__ == "__main__":
    main()

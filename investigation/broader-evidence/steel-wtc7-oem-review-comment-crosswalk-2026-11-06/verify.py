"""Verify the held source files and six OEM catalog joins."""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import re
from xml.etree import ElementTree
from zipfile import ZipFile

import fitz


def require(condition, label):
    if not condition:
        raise SystemExit(f"Check failed: {label}")


def digest(data):
    return hashlib.sha256(data).hexdigest()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("sources", nargs=5, type=Path, help="Paths in SOURCE-PINS.json order")
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
for pin, path in zip(ledger["sources"], args.sources, strict=True):
    data = path.read_bytes()
    require(path.name == pin["file"], pin["file"])
    require(len(data) == pin["bytes"] and digest(data) == pin["sha256"], path.name)
    if "pages" in pin:
        with fitz.open(stream=data, filetype="pdf") as pdf:
            require(len(pdf) == pin["pages"], f"{path.name} page count")

with ZipFile(args.sources[1]) as archive:
    members = {}
    for name, sha256 in ledger["catalog_members"].items():
        paths = [entry for entry in archive.namelist() if PurePosixPath(entry).name == name]
        require(len(paths) == 1, name)
        members[name] = archive.read(paths[0])
        require(digest(members[name]) == sha256, name)

ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
with ZipFile(BytesIO(members["tblDocumentMain.xlsx"])) as workbook:
    strings = [
        "".join(entry.itertext())
        for entry in ElementTree.fromstring(workbook.read("xl/sharedStrings.xml")).findall("s:si", ns)
    ]
    sheet = ElementTree.fromstring(workbook.read("xl/worksheets/sheet1.xml"))
    rows = {int(row.get("r")): row for row in sheet.findall(".//s:row", ns)}

directory = members["DirectoryPrint_ScannedPaperDocuments.txt"].splitlines()
for join in ledger["joins"]:
    fields = {}
    for cell in rows[join["row"]]:
        value = cell.find("s:v", ns)
        if value is not None:
            column = re.sub(r"\d", "", cell.get("r"))
            fields[column] = strings[int(value.text)] if cell.get("t") == "s" else value.text
    filename = f"WTCI-{fields['C']}-{fields['F']}.PDF"
    require(filename == join["filename"], filename)
    require(join["title_anchor"] in fields["O"], f"{filename} title")
    require(fields["P"] == join["catalog_date"], f"{filename} catalog date")
    require(fields.get("Q", "") == join["document_id"], f"{filename} document ID")
    require(directory[join["directory_line"] - 1].split()[0].decode() == filename, f"{filename} directory")

with fitz.open(args.sources[2]) as nist:
    area = " ".join(nist[58].get_text().split())
    require("100 ft" in area and "168 ft" in area, "NCSTAR 1-1J p. 59 area values")
with fitz.open(args.sources[3]) as nist:
    require("each item was initialed" in nist[237].get_text(), "NCSTAR 1-1 p. 238 checklist")

print("5 source hashes and lengths, 4 PDF page counts, 2 ZIP member hashes, 6 catalog joins and 2 NIST text comparisons passed")

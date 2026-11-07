"""Check public-source bytes, City page fields and six catalog/directory joins.

Requires PyMuPDF. Supply the held source directory and the original 12-090 ZIP.
"""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import fitz


def check(condition, description):
    if not condition:
        raise SystemExit(f"Failed: {description}")


def verify_bytes(data, pin):
    check(len(data) == pin["bytes"], "byte length")
    check(hashlib.sha256(data).hexdigest() == pin["sha256"], "SHA-256")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("sources", type=Path)
parser.add_argument("catalog", type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
for pin in ledger["sources"]:
    data = (args.sources / pin["file"]).read_bytes()
    verify_bytes(data, pin)
    if pin["pages"] is not None:
        with fitz.open(stream=data, filetype="pdf") as doc:
            check(len(doc) == pin["pages"], f"{pin['file']} page count")

plan = (args.sources / "plan-complete.pdf").read_bytes()
check(plan.rstrip().endswith(b"%%EOF"), "complete PDF marker")
receipt = ledger["plan_acquisition"]
prefix = (args.sources / "plan-verified-size.body").read_bytes()
verify_bytes(prefix, {"bytes": receipt["partial_bytes"], "sha256": receipt["partial_sha256"]})
check(plan.startswith(prefix), "original interrupted prefix")
offset = 0
for index, part in enumerate(receipt["ranges"]):
    data = (args.sources / part["file"]).read_bytes()
    verify_bytes(data, part)
    headers = (args.sources / f"plan-part{index}.headers").read_text().lower()
    check("206 partial content" in headers, "range status")
    check(f"bytes {offset}-{part['last']}/{len(plan)}" in headers, "Content-Range")
    check(receipt["weak_etag"].lower() in headers and receipt["last_modified"].lower() in headers,
          "shared response validators")
    check(plan[offset:part["last"] + 1] == data and part["first"] == offset, "range alignment")
    offset += len(data)
check(offset == len(plan), "complete range coverage")

anchors = {
    "plan-complete.pdf": {
        5: ["Date Prepared - January, 1988"],
        122: ["APRIL 18,1988", "has been evaluated and you are hereby notified that it has been approved"],
        224: ["Floors 35 through the roof", "November 18, 1988"],
        227: ["April 5, 1988", "Floors 14-24", "April 1, 1988"],
        229: ["NYC-WTC_000168946", "Testwell Craig", "Structural, Firestopping, Concrete",
              "Fireproofing and Bolting", "Prior to the issuance of a Final Certificate of Occupancy"],
        230: ["floors 1-13", "December 31, 1987"],
        237: ["Floors 25-34", "April 11, 1988"],
        239: ["NYC-WTC_000168956", "Testwell Craig", "Fireproofing and Bolting"],
    },
    "govinfo.body": {
        88: ["Floors 9, 10, and 11", "unable to locate a final inspection report",
             "Floor 23 in 1993", "September 24, 1998", "August 12, 1997"],
    },
}
count = 0
for name, pages in anchors.items():
    with fitz.open(args.sources / name, filetype="pdf") as doc:
        for page, values in pages.items():
            text = " ".join(doc[page - 1].get_text().split())
            for value in values:
                check(value in text, f"{name} p. {page}: {value}")
                count += 1

archive = args.catalog.read_bytes()
verify_bytes(archive, ledger["catalog"])
with ZipFile(BytesIO(archive)) as z:
    def member(name):
        paths = [p for p in z.namelist() if PurePosixPath(p).name == name]
        check(len(paths) == 1, f"unique {name}")
        return z.read(paths[0])

    book = member("tblDocumentMain.xlsx")
    directory = member("DirectoryPrint_ScannedPaperDocuments.txt").splitlines()
ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
with ZipFile(BytesIO(book)) as workbook:
    strings = ["".join(s.itertext()) for s in ET.fromstring(workbook.read("xl/sharedStrings.xml")).findall("s:si", ns)]
    rows = {int(r.get("r")): r for r in ET.fromstring(workbook.read("xl/worksheets/sheet1.xml")).findall(".//s:row", ns)}

expected = [
    (4133, "000303", "I", "Firestopping Inspection Engineers Report", "1/22/2007", 7830),
    (4047, "000018", "SOM", "Field Inspection Reports for Firestopping", "9/27/1989", 417),
    (4056, "000027", "SOM", "Fax on Firestopping", "2/9/1993", 426),
    (4070, "000041", "SOM", "Specification for Firestopping", "2/5/1993", 440),
    (430, "000045", "FEMA", "Fire Stopping - WTC 7", "", 758),
    (3898, "000212", "I", "Fire Stopping - WTC 7", "", 7725),
]
for number, ident, category, title, day, line in expected:
    values = {}
    for cell in rows[number]:
        value = cell.find("s:v", ns)
        if value is not None:
            column = re.sub(r"\d", "", cell.get("r"))
            values[column] = strings[int(value.text)] if cell.get("t") == "s" else value.text
    check((values["C"], values["F"], values.get("P", "")) == (ident, category, day),
          f"workbook row {number} fields")
    check(title in values["O"], f"workbook row {number} title")
    check(directory[line - 1].split()[0] == f"WTCI-{ident}-{category}.PDF".encode(), f"directory line {line}")
print(f"5 source hashes, complete 4-range City PDF and prior prefix, {count} page anchors and 6 catalog joins passed")

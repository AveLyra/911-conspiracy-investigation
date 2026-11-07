"""Verify the captured HTML/JSON bytes and selected record fields.

Requires Beautiful Soup. Supply the directory with the held response files.
"""
import argparse
import hashlib
import json
from pathlib import Path

from bs4 import BeautifulSoup


def check(condition, description):
    if not condition:
        raise SystemExit(f"Failed: {description}")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
for pin in ledger["captured"]:
    data = (args.source / pin["file"]).read_bytes()
    check(len(data) == pin["bytes"], f"{pin['file']} byte length")
    check(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{pin['file']} SHA-256")
    if pin["http_status"] == 403:
        check(not data.startswith(b"%PDF"), f"{pin['file']} is not a PDF body")

case = BeautifulSoup((args.source / "foia.body").read_bytes(), "html.parser")
check("3:2009cv00986" in case.get_text(" ", strip=True), "Texas case identifier")
docket = {}
for row in case.find_all("tr"):
    cells = [cell.get_text(" ", strip=True) for cell in row.find_all("td", recursive=False)]
    if len(cells) == 3 and cells[1].isdigit():
        docket[int(cells[1])] = (cells[0], cells[2])
expected = {
    1: ("2009-05-28", "COMPLAINT"), 4: ("2009-08-13", "ANSWER"),
    6: ("2009-08-14", "STATUS REPORT ORDER"), 7: ("2009-09-04", "Joint STATUS REPORT"),
    17: ("2010-11-04", "MOTION for Protective Order"), 18: ("2010-11-04", "Appendix in Support"),
    19: ("2010-11-30", "RESPONSE"), 21: ("2010-12-14", "REPLY"),
    25: ("2011-01-26", "ORDER granting 17"), 26: ("2011-04-28", "Joint STATUS REPORT"),
    27: ("2011-05-16", "Second STATUS REPORT"), 28: ("2011-05-16", "Joint Status Report due"),
    29: ("2011-06-01", "Joint STATUS REPORT"), 30: ("2011-06-06", "Joint STIPULATION OF DISMISSAL"),
    31: ("2011-06-07", "dismissed with prejudice"),
}
for number, (day, text) in expected.items():
    check(docket[number][0] == day and text in docket[number][1], f"ECF {number}")
check("Entered: 06/08/2011" in docket[31][1], "ECF 31 entry date")
check("Entered: 05/29/2009" in docket[1][1], "ECF 1 entry date")

mirror = json.loads((args.source / "r32.body").read_bytes())
names = [item["name"] for item in mirror["files"]]
check(mirror["metadata"]["date"] == "2010-10-08", "mirror release date")
check(len(names) == 35 and sum(name.endswith(".rar") for name in names) == 28, "mirror item counts")
check(sum(name.endswith("42A0375 - G33D9.rar") for name in names) == 1, "G33D9 package")
print(f"{len(ledger['captured'])} source hashes and lengths, {len(expected)} docket rows, both entry dates and mirror counts passed")

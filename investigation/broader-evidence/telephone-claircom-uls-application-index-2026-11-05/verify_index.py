"""Emit a minimal two-application projection from the pinned FCC public export."""
import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZipFile

EXPECTED_HASH = "7db9fa8234315ec52fcc6d49e7becfc080587495e56879005bd28c4964bbfc0f"
TARGETS = {"0000421562": "741133", "0000420815": "740283"}
SCHEMA = {
    "HD.dat": {4: "Call Sign", 6: "Radio Service Code"},
    "AD.dat": {4: "Application Purpose", 5: "Application Status", 10: "Receipt Date",
               16: "Requesting A Waiver", 17: "How Many Waivers Requested",
               18: "Any Attachments", 21: "Date Entered"},
    "AT.dat": {4: "Attachment Code", 5: "Attachment Description", 6: "Attachment Date",
               7: "Attachment File Name", 8: "Action Performed"},
}
archive_path = Path(sys.argv[1])
data = archive_path.read_bytes()
assert hashlib.sha256(data).hexdigest() == EXPECTED_HASH
projection = {}
with ZipFile(archive_path) as archive:
    for member, schema in SCHEMA.items():
        rows = []
        with archive.open(member) as source:
            for line_number, line in enumerate(source, 1):
                fields = line.rstrip(b"\r\n").decode("latin-1").split("|")
                file_number = fields[2]
                if file_number not in TARGETS:
                    continue
                assert fields[1] == TARGETS[file_number]
                rows.append({"line": line_number, "ULS File Number": file_number,
                             "Unique System Identifier": fields[1],
                             **{label: fields[position] for position, label in schema.items()}})
        projection[member] = rows
assert [len(rows) for rows in projection.values()] == [2, 2, 13]
for file_number, expected_count in (("0000421562", 7), ("0000420815", 6)):
    rows = [row for row in projection["AT.dat"] if row["ULS File Number"] == file_number]
    assert len(rows) == expected_count
    assert all(row["Attachment File Name"] == "" for row in rows)
assert {row["How Many Waivers Requested"] for row in projection["AD.dat"]} == {"4", "1"}
assert {row["Receipt Date"] for row in projection["AD.dat"]} == {"04/09/2001"}

print(json.dumps({
    "source": {"url": "https://data.fcc.gov/download/pub/uls/complete/a_paging.zip",
               "access_date_eastern": "2026-11-05", "sha256": EXPECTED_HASH, "bytes": len(data),
               "snapshot_listing": "2026-10-31 12:48:25",
               "directory_url": "https://data.fcc.gov/download/pub/uls/complete/",
               "directory_sha256": "dc50c35a38d3291a5f795edfa1b1f3a51c4c7256be799ca9a0765a45d34e2d91",
               "member_locators": "One-based physical lines in the named pipe-delimited ZIP member."},
    "schema": {"url": "https://wireless.fcc.gov/wtbfiles/pa_ddef51.pdf",
               "locator": "AD printed p. 2, AT printed p. 62 and HD header definition",
               "access": "FCC indexed document text"},
    "projected_rows": projection
}, indent=2))

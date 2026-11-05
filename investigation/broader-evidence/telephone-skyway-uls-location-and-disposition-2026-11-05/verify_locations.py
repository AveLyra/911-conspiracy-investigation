"""Compare the two pinned FCC snapshots without printing coordinates or addresses."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from zipfile import ZipFile

APP_HASH = "7db9fa8234315ec52fcc6d49e7becfc080587495e56879005bd28c4964bbfc0f"
LICENSE_HASH = "e0e2510c0a399695e5f7e6ab37fa662e2d774d14b5eb35e1a18ad8547185448e"
APPS = {"2145523": "0001403659", "2258481": "0001604737", "2298556": "0001644195",
        "2411195": "0001741749", "2517515": "0001785972", "2665105": "0001931747"}
LICENSE_ID = "2565569"


def read_member(archive, name):
    with archive.open(name) as source:
        for number, line in enumerate(source, 1):
            fields = line.rstrip(b"\r\n").decode("latin-1").split("|")
            if len(fields) > 4:
                yield number, fields


def locations(archive, ids):
    return [(number, row[1], int(row[8]), row[5], tuple(row[19:27]))
            for number, row in read_member(archive, "LO.dat") if row[1] in ids]


def locator(location):
    line, system_id, number, action, _ = location
    return {"line": line, "system_id": system_id, "location_number": number, "action": action}


app_path, license_path = map(Path, sys.argv[1:])
for path, digest in ((app_path, APP_HASH), (license_path, LICENSE_HASH)):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
with ZipFile(app_path) as app, ZipFile(license_path) as license_db:
    headers = [{"line": n, "system_id": r[1], "file_number": r[2], "last_action_date": r[43]}
               for n, r in read_member(app, "HD.dat") if r[4] == "WPYZ281"]
    assert {row["system_id"]: row["file_number"] for row in headers} == APPS
    details = [{"line": n, "system_id": r[1], "file_number": r[2], "purpose": r[4],
                "status": r[5], "receipt_date": r[10], "date_entered": r[21]}
               for n, r in read_member(app, "AD.dat") if r[1] in APPS]
    assert len(details) == len({row["system_id"] for row in details}) == 6
    assert all(row["file_number"] == APPS[row["system_id"]] for row in details)
    assert any(row["file_number"] == "0001931747" and row["receipt_date"] == "11/10/2004"
               and row["status"] == "D" for row in details)
    history = [{"line": n, "date": r[4], "code": r[5]} for n, r in read_member(app, "HS.dat")
               if r[1] == "2665105" and r[2] == "0001931747"]
    assert any(row["date"] == "03/03/2006" and row["code"] == "APDIS" for row in history)
    assert any(row["date"] == "03/04/2006" and row["code"] == "LETDIS" for row in history)
    selected_attachments = [{"line": n, "file_number": r[2], "description": r[5], "date": r[6],
                             "filename": r[7], "action": r[8]}
                            for n, r in read_member(app, "AT.dat")
                            if r[2] in {"0001604737", "0001931747"}]
    assert len(selected_attachments) == 3
    assert any(row["description"] == "Additional 21 site amendment" for row in selected_attachments)
    license_header = [{"line": n, "system_id": r[1], "status": r[5], "expiration_date": r[8]}
                      for n, r in read_member(license_db, "HD.dat") if r[4] == "WPYZ281"]
    assert len(license_header) == 1 and license_header[0]["system_id"] == LICENSE_ID
    assert license_header[0]["expiration_date"] == "11/30/2004"
    app_locations = locations(app, APPS)
    license_locations = locations(license_db, {LICENSE_ID})

assert len(app_locations) == 137 and len(license_locations) == 135
assert all(all(loc[-1]) for loc in app_locations + license_locations)
app_numbers = Counter(loc[2] for loc in app_locations)
license_numbers = {loc[2] for loc in license_locations}
assert len(app_numbers) == len(license_numbers) == 135
assert set(app_numbers) - license_numbers == {136} and license_numbers - set(app_numbers) == {128}
app_coords = {loc[-1] for loc in app_locations}
license_coords = {loc[-1] for loc in license_locations}
assert len(app_coords) == 136 and len(license_coords) == 135 and license_coords < app_coords
app_only = [loc for loc in app_locations if loc[-1] not in license_coords]
assert [loc[:4] for loc in app_only] == [(8254, "2258481", 20, "A")]
different_numbers = [{"application": locator(a), "license": locator(b)}
                     for a in app_locations for b in license_locations if a[-1] == b[-1] and a[2] != b[2]]
assert [(pair["application"]["location_number"], pair["license"]["location_number"])
        for pair in different_numbers] == [(n, n - 1) for n in range(129, 137)]
location_rows_by_file = Counter(APPS[loc[1]] for loc in app_locations)
output = {
    "access_date_eastern": "2026-11-05",
    "sources": [
        {"url": "https://data.fcc.gov/download/pub/uls/complete/a_paging.zip",
         "sha256": APP_HASH, "bytes": app_path.stat().st_size, "listing": "2026-10-31 12:48:25"},
        {"url": "https://data.fcc.gov/download/pub/uls/complete/l_paging.zip",
         "sha256": LICENSE_HASH, "bytes": license_path.stat().st_size, "listing": "2026-11-01 10:20:31"},
    ],
    "format": {"url": "https://wireless.fcc.gov/wtbfiles/pa_ddef51.pdf",
               "scope": "HD, AD, AT, HS and LO fields. Exact LO coordinates compared using positions 20–27."},
    "history_codes": "https://wireless.fcc.gov/uls/releases/d992205c.pdf",
    "headers": headers, "details": details, "extension_history": history,
    "selected_attachments": selected_attachments, "license_header": license_header,
    "location_check": {"application_rows": len(app_locations), "license_rows": len(license_locations),
                       "application_rows_by_file": dict(location_rows_by_file),
                       "repeated_application_numbers": sorted(n for n, count in app_numbers.items() if count > 1),
                       "application_only_numbers": sorted(set(app_numbers) - license_numbers),
                       "license_only_numbers": sorted(license_numbers - set(app_numbers)),
                       "unique_application_coordinate_tuples": len(app_coords),
                       "unique_license_coordinate_tuples": len(license_coords),
                       "shared_coordinate_tuples": len(app_coords & license_coords),
                       "application_only_coordinates": [locator(loc) for loc in app_only],
                       "same_coordinates_different_number": different_numbers},
}
print(json.dumps(output, indent=2))

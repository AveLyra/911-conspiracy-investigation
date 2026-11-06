"""Screen candidate Mode 3 4000 near ACY in four pinned WTC-branch members."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import struct
import sys
import zlib

from rs3_reference import MARK, MODES, distance_nm, project, unpack_site_footer

ACY = (39 + 27.45 / 60, -(74 + 34.63 / 60))
TARGET = 0o4000
WINDOWS = {"early": (14 * 3600 + 23 * 60, 14 * 3600 + 38 * 60),
           "late": (15 * 3600 + 23 * 60, 15 * 3600 + 38 * 60)}
DAY = int(datetime(2001, 9, 11, tzinfo=timezone.utc).timestamp())


def utc(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).strftime("%H:%M:%S")


def inspect(data, pin):
    assert len(data) == pin["bytes"]
    assert sha256(data).hexdigest() == pin["sha256"]
    assert f"{zlib.crc32(data):08x}" == pin["crc32"]
    assert data[10:27] == b"RADES Sensor Data"
    offset = 100
    while data[offset:offset+4] == MARK:
        a, b = data[offset+8:offset+10]
        offset += 16 + 2 * (a + b)
    footer = offset
    assert data[footer:footer+8] == b"\xaa" * 8
    sites = unpack_site_footer(data, footer)
    offset = 100
    raw_count = 0
    seconds = set()
    by_site = Counter()
    nearby_all_codes = Counter()
    code_4000 = Counter()
    near = []
    while offset < footer:
        assert data[offset:offset+4] == MARK
        a, b = data[offset+8:offset+10]
        kind, _, _, timestamp = struct.unpack_from("<HBBI", data, offset+6)
        sec = timestamp - DAY
        assert 0 <= sec < 86400
        seconds.add(sec)
        raw_count += 1
        win = next((key for key, (start, end) in WINDOWS.items() if start <= sec < end), None)
        if win and (a, kind) in MODES and b == 2:
            site = sites[data[offset+4]]
            alias = site["alias"]
            by_site[win, alias] += 1
            words = struct.unpack_from("<7H", data, offset+18)
            code = (words[3] >> 1) & 0xfff
            radius = (words[0] & ~1) / 32
            angle = (words[1] & ~1) * 360 / 8192
            # Triangle inequality skips geometrically impossible points only.
            if code == TARGET:
                code_4000[win, alias] += 1
            if abs(distance_nm(site["latlon"], ACY) - radius) <= 25:
                coord = project(site["latlon"], radius, angle)
                distance = distance_nm(ACY, coord)
                if distance <= 25:
                    nearby_all_codes[win, alias] += 1
                    if code == TARGET:
                        near.append(dict(window=win, site=alias, encoded=utc(timestamp),
                                         offset=offset, kind=kind, distance_nm=round(distance, 5),
                                         point=[round(c, 7) for c in coord], range_nm=radius,
                                         bearing=angle, mode_word=f"{words[3]:04x}"))
        offset += 16 + 2 * (a + b)
    assert offset == footer
    return dict(raw_count=raw_count, whole_seconds=len(seconds),
                missing_whole_seconds=max(seconds)-min(seconds)+1-len(seconds),
                start=utc(min(seconds)+DAY), last=utc(max(seconds)+DAY),
                window_families_by_site={":".join(k):n for k,n in sorted(by_site.items())},
                window_near_all_codes_by_site={":".join(k):n for k,n in sorted(nearby_all_codes.items())},
                window_code4000_all_distances_by_site={":".join(k):n for k,n in sorted(code_4000.items())},
                sites=sites, nearby_code4000=sorted(near,key=lambda row:(row["encoded"],row["offset"])))


def main():
    pinfile, *files = map(Path, sys.argv[1:])
    members = json.loads(pinfile.read_text())
    assert len(files) == len(members) == 4
    assert {p.name for p in files} == set(members)
    test_site = (39.0, -74.0)
    assert abs(distance_nm(test_site, project(test_site, 10, 30)) - 10) < 1e-8
    result = {p.name: inspect(p.read_bytes(), members[p.name]) for p in files}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

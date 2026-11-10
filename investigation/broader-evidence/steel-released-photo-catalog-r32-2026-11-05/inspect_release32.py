"""Read a catalog fetched over HTTPS. No torrent client or network calls."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


def read_bencode(data):
    def read_at(start):
        marker = data[start]
        if marker == ord("i"):
            end = data.index(b"e", start + 1)
            return int(data[start + 1:end]), end + 1
        if marker in (ord("l"), ord("d")):
            values = []
            offset = start + 1
            while data[offset] != ord("e"):
                value, offset = read_at(offset)
                values.append(value)
            if marker == ord("d"):
                return dict(zip(values[::2], values[1::2], strict=True)), offset + 1
            return values, offset + 1
        colon = data.index(b":", start)
        length = int(data[start:colon])
        end = colon + 1 + length
        return data[colon + 1:end], end

    value, end = read_at(0)
    if end != len(data):
        raise ValueError("Trailing bytes in bencoded manifest")
    return value


def summarize(metadata_path, torrent_path):
    metadata = json.loads(metadata_path.read_text())
    torrent = torrent_path.read_bytes()
    torrent_entry = next(
        f for f in metadata["files"]
        if f["name"].endswith("FOIA_-_Release_32.torrent")
    )
    if hashlib.sha1(torrent).hexdigest() != torrent_entry["sha1"]:
        raise ValueError("Torrent bytes differ from the archive metadata SHA-1")
    rows = read_bencode(torrent)[b"info"][b"files"]
    paths = [
        ([part.decode("utf-8", errors="replace") for part in row[b"path"]], row[b"length"])
        for row in rows
    ]
    disc = [item for item in paths if any("42A0375" in part for part in item[0])]
    selected = [item for item in disc if any("WTCI-102-I" in part for part in item[0])]
    groups = Counter()
    anchors = []
    dated_folders = Counter()
    for path, size in selected:
        pos = next(i for i, part in enumerate(path) if "WTCI-102-I" in part)
        groups[path[pos + 1] if pos + 1 < len(path) - 1 else "(root)"] += 1
        for part in path[pos + 1:-1]:
            if re.search(r"(?i)claremont|january|2002-01|01-30|1-30|1_30|01-21|1-21|1_21", part):
                dated_folders[part] += 1
        if path[-1].lower() == "p2080056.jpg" or re.search(
            r"(?i)W[- ]?14[AB]|C12[AB]|2002[-_.]01[-_.](21|30)|"
            r"01[-_.](21|30)[-_.](02|2002)|[.]xls[xm]?$",
            "/".join(path[pos + 1:]),
        ):
            anchors.append({"path": "/".join(path), "bytes": size})
    return {
        "metadata_item": metadata["metadata"]["identifier"],
        "manifest_sha1": torrent_entry["sha1"],
        "manifest_sha256": hashlib.sha256(torrent).hexdigest(),
        "all_file_paths": len(paths),
        "disc_paths": len(disc),
        "selected_paths": len(selected),
        "selected_first_subfolders": dict(sorted(groups.items())),
        "selected_date_or_yard_folders": dict(sorted(dated_folders.items())),
        "anchor_matches": anchors,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.metadata, args.manifest), indent=2))

"""Read-only, bounded SWF structure audit; never executes ActionScript."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

LIMIT = 16 * 1024 * 1024
NAMES = {0: "End", 1: "ShowFrame", 12: "DoAction", 39: "DefineSprite",
         59: "DoInitAction", 60: "DefineVideoStream", 61: "VideoFrame",
         69: "FileAttributes", 77: "Metadata", 82: "DoABC"}
INPUTS = [
    ("CU_animation_20080829100216.swf", "e067773201621de8dcc0851eeada92a61a02ec8490302af99fe676274c145f44"),
    ("whole_building_animation_20080829100049.swf", "9acbef93ef59f0103071b8ce580cee3beb8cdb6139a2ac16f15d864013c84f44"),
    ("CU_animation_20080907013011.swf", "c3a00150f07f449d5a642879f2c294a186b3314cb2672134d708ecff85db8508"),
    ("whole_building_animation_20080907013006.swf", "1926c25114092d4c61a170ed8d1a2a04aa223f758421f75b35fdf6185e793074"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def u30(data, pos):
    value = 0
    for shift in range(0, 35, 7):
        if pos >= len(data):
            raise ValueError("truncated variable integer")
        byte = data[pos]
        pos += 1
        value |= (byte & 127) << shift
        if byte < 128:
            return value, pos
    raise ValueError("overlong variable integer")


def abc_strings(data):
    """Read only ABC version and initial numeric/string constant pools."""
    if len(data) < 4:
        raise ValueError("short ABC header")
    minor, major = struct.unpack_from("<HH", data)
    pos = 4
    for _ in range(2):
        count, pos = u30(data, pos)
        if count > LIMIT:
            raise ValueError("oversize constant count")
        for _ in range(max(0, count - 1)):
            _, pos = u30(data, pos)
    count, pos = u30(data, pos)
    pos += max(0, count - 1) * 8
    if pos > len(data):
        raise ValueError("truncated double constants")
    count, pos = u30(data, pos)
    values = []
    if count > LIMIT:
        raise ValueError("oversize string count")
    for _ in range(max(0, count - 1)):
        length, pos = u30(data, pos)
        if pos + length > len(data):
            raise ValueError("truncated string")
        values.append(data[pos:pos + length])
        pos += length
    return {"minor": minor, "major": major, "string_count": len(values),
            "media_strings": [s.decode("utf-8", "replace") for s in values
                              if re.search(rb"\.(?:flv|swf)(?:$|\?)", s, re.I)],
            "control_names_present": sorted({s.decode("ascii") for s in values
                if s in {b"play", b"seek", b"autoPlay", b"duration", b"source",
                         b"totalTime", b"frameRate", b"playheadTime", b"playbackSpeed"}}),
            "string_pool_sha256": sha(b"".join(struct.pack("<I", len(v)) + v for v in values))}


def rect(data):
    if not data:
        raise ValueError("empty RECT")
    width = data[0] >> 3
    bitpos = 5
    values = []
    for _ in range(4):
        value = 0
        for _ in range(width):
            if bitpos >= len(data) * 8:
                raise ValueError("truncated RECT")
            value = (value << 1) | ((data[bitpos // 8] >> (7 - bitpos % 8)) & 1)
            bitpos += 1
        if width and value & (1 << (width - 1)):
            value -= 1 << width
        values.append(value)
    return values, (bitpos + 7) // 8


def tags(data, start, stop, ancestry=(), depth=0):
    if depth > 32:
        raise ValueError("excess nesting")
    rows, pos, ended = [], start, False
    while pos < stop:
        offset = pos
        if pos + 2 > stop:
            raise ValueError("truncated tag header")
        value = struct.unpack_from("<H", data, pos)[0]
        pos += 2
        code, length = value >> 6, value & 63
        if length == 63:
            if pos + 4 > stop:
                raise ValueError("truncated long tag length")
            length = struct.unpack_from("<I", data, pos)[0]
            pos += 4
        if pos + length > stop:
            raise ValueError("tag exceeds container")
        payload = data[pos:pos + length]
        row = {"code": code, "name": NAMES.get(code, "tag_%d" % code),
               "offset_uncompressed": offset, "payload_offset_uncompressed": pos,
               "length": length, "payload_sha256": sha(payload),
               "ancestry_sprite_ids": list(ancestry)}
        if code == 39:
            if length < 4:
                raise ValueError("short sprite")
            sprite_id, frame_count = struct.unpack_from("<HH", payload)
            row["sprite_id"] = sprite_id
            row["declared_frames"] = frame_count
            row["children"], row["trailing_bytes"] = tags(
                data, pos + 4, pos + length, ancestry + (sprite_id,), depth + 1)
        elif code == 60:
            if length != 10:
                raise ValueError("unexpected DefineVideoStream length")
            sid, frames, width, height, flags, codec = struct.unpack("<HHHHBB", payload)
            row["video_declaration"] = {"id": sid, "frames": frames,
                "width": width, "height": height, "flags": flags, "codec": codec}
        elif code == 82:
            if length < 5:
                raise ValueError("short DoABC")
            nul = payload.find(b"\0", 4)
            if nul < 0:
                raise ValueError("unterminated ABC name")
            row["abc"] = abc_strings(payload[nul + 1:])
        rows.append(row)
        pos += length
        if code == 0:
            if length != 0:
                raise ValueError("nonempty End")
            ended = True
            break
    if not ended:
        raise ValueError("container lacks End")
    return rows, stop - pos


def flatten(rows):
    for row in rows:
        yield row
        yield from flatten(row.get("children", []))


def parse(raw):
    if len(raw) < 8:
        raise ValueError("short SWF")
    signature = raw[:3]
    if signature == b"CWS":
        inflater = zlib.decompressobj()
        body = inflater.decompress(raw[8:], LIMIT + 1)
        if len(body) > LIMIT or not inflater.eof or inflater.unused_data:
            raise ValueError("oversize/incomplete/trailed compressed SWF")
    elif signature == b"FWS":
        body = raw[8:]
        if len(body) > LIMIT:
            raise ValueError("oversize SWF")
    else:
        raise ValueError("unsupported signature")
    data = raw[:8] + body
    bounds, rect_bytes = rect(body)
    pos = 8 + rect_bytes
    if pos + 4 > len(data):
        raise ValueError("short timeline header")
    rate, frames = struct.unpack_from("<HH", data, pos)
    rows, trailing = tags(data, pos + 4, len(data))
    all_rows = list(flatten(rows))
    def counts(items):
        return dict(sorted(collections.Counter(r["name"] for r in items).items()))
    return {"bytes": len(raw), "sha256": sha(raw), "signature": signature.decode(),
            "version": raw[3], "declared_uncompressed_bytes": struct.unpack_from("<I", raw, 4)[0],
            "actual_uncompressed_bytes": len(data),
            "declared_length_matches": struct.unpack_from("<I", raw, 4)[0] == len(data),
            "rect_twips": bounds, "frame_rate_8_8_raw": rate, "frame_rate": rate / 256,
            "declared_root_frames": frames, "root_counts": counts(rows),
            "recursive_counts": counts(all_rows), "trailing_root_bytes": trailing,
            "printable_media_references": sorted({s.decode("ascii", "replace") for s in
                re.findall(rb"[ -~]{4,}", body) if re.search(rb"\.(?:flv|swf)(?:$|\?)", s, re.I)}),
            "tags": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--media-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    # The caller must supply a root verified by the repository media resolver.
    output = {"method": "bounded static parse; no ActionScript execution or video decoding",
              "offset_convention": "byte offsets after CWS inflation; source hash is original compressed bytes",
              "files": []}
    for name, expected in INPUTS:
        raw = (Path(args.media_root) / name).read_bytes()
        if sha(raw) != expected:
            raise ValueError("unexpected source bytes: " + name)
        output["files"].append({"name": name, **parse(raw)})
    with open(args.output, "x", encoding="utf-8") as stream:
        json.dump(output, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"files": 4, "output": args.output}))


if __name__ == "__main__":
    main()

"""Passive portable control/export/selected-action reproduction. No SWF code executes."""
import argparse
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import zipfile
SAFE_API = {b"Sound", b"attachSound", b"start", b"stop", b"setVolume", b"onSoundComplete"}

HELPER_SHA256 = '2af3d0339c5ca876255948a014205f8caa6ff019c1303e79a0ba774a22f36ade'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

class Reader:
    def __init__(self, raw):
        self.raw = raw
        self.pos = 0

    def take(self, size):
        if self.pos + size > len(self.raw):
            raise ValueError("Control record truncated")
        out = self.raw[self.pos:self.pos + size]
        self.pos += size
        return out

    def uint(self, size):
        return int.from_bytes(self.take(size), "little")

    def cstring_hash(self):
        end = self.raw.find(b"\0", self.pos)
        if end < 0:
            raise ValueError("Unterminated symbol/class name")
        raw = self.raw[self.pos:end]
        self.pos = end + 1
        return {"string_bytes": len(raw), "string_sha256": sha(raw)}

    def end(self):
        if self.pos != len(self.raw):
            raise ValueError("Unparsed control bytes")

def sound_info(reader):
    flags = reader.uint(1)
    if flags & 0xC0:
        raise ValueError("Nonzero reserved SOUNDINFO bits")
    out = {"flags_hex": f"{flags:02x}", "sync_stop": bool(flags & 32),
           "sync_no_multiple": bool(flags & 16), "has_envelope": bool(flags & 8),
           "has_loops": bool(flags & 4), "has_out_point": bool(flags & 2),
           "has_in_point": bool(flags & 1)}
    if flags & 1:
        out["in_point"] = reader.uint(4)
    if flags & 2:
        out["out_point"] = reader.uint(4)
    if flags & 4:
        out["loop_count"] = reader.uint(2)
    if flags & 8:
        count = reader.uint(1)
        out["envelope_points"] = [
            {"pos44": reader.uint(4), "left_level": reader.uint(2), "right_level": reader.uint(2)}
            for _ in range(count)]
    return out

def fixtures():
    raw = b"\x1f" + struct.pack("<IIH", 100, 200, 3) + b"\x01" + struct.pack("<IHH", 50, 1000, 2000)
    r = Reader(raw)
    v = sound_info(r)
    r.end()
    assert v["in_point"] == 100 and v["out_point"] == 200 and v["loop_count"] == 3
    assert v["sync_no_multiple"] and not v["sync_stop"]
    assert v["envelope_points"] == [{"pos44": 50, "left_level": 1000, "right_level": 2000}]
    r = Reader(b"\x20")
    assert sound_info(r)["sync_stop"]
    r.end()
    rejected = 0
    for bad in (b"", b"\x01\0", b"\x80", b"\x08\x01\0", b"\x04\x01"):
        try:
            sound_info(Reader(bad))
        except ValueError:
            rejected += 1
    assert rejected == 5
    return {"all_optional_fields_and_envelope_known_values": True, "stop_only": True,
            "malformed_cases_rejected": rejected}

def cstring(reader):
    end = reader.raw.find(b"\0", reader.pos)
    if end < 0:
        raise ValueError("Unterminated action string")
    out = reader.raw[reader.pos:end]
    reader.pos = end + 1
    return out

def describe(raw, export_name):
    result = {"string_bytes": len(raw), "string_sha256": sha(raw), "matches_export": raw == export_name}
    if raw in SAFE_API:
        result["api_name"] = raw.decode("ascii")
    return result

def records(data, export_name):
    pos, pool, rows = 0, None, []
    while pos < len(data):
        offset = pos
        code = data[pos]
        pos += 1
        length = 0
        if code & 0x80:
            if pos + 2 > len(data):
                raise ValueError("Short action header")
            length = struct.unpack_from("<H", data, pos)[0]
            pos += 2
        if pos + length > len(data):
            raise ValueError("Action exceeds selected block")
        body = data[pos:pos + length]
        row = {"action_offset_within_tag_body": offset, "code": code,
               "body_bytes": length, "body_sha256": sha(body)}
        if code == 0x88:
            r = Reader(body)
            count = r.uint(2)
            pool = [cstring(r) for _ in range(count)]
            r.end()
            row["constants"] = [describe(x, export_name) for x in pool]
        if code == 0x96:
            r = Reader(body)
            values = []
            while r.pos < len(body):
                kind = r.uint(1)
                value = {"type": kind}
                if kind == 0:
                    value.update(describe(cstring(r), export_name))
                elif kind == 1:
                    value["float"] = struct.unpack("<f", r.take(4))[0]
                elif kind in (2, 3):
                    value["literal"] = "null" if kind == 2 else "undefined"
                elif kind == 4:
                    value["register"] = r.uint(1)
                elif kind == 5:
                    value["boolean_raw"] = r.uint(1)
                elif kind == 6:
                    value["double_raw_hex"] = r.take(8).hex()
                elif kind == 7:
                    value["unsigned_integer"] = r.uint(4)
                elif kind in (8, 9):
                    index = r.uint(1 if kind == 8 else 2)
                    value["constant_index"] = index
                    if pool is not None:
                        if index >= len(pool):
                            raise ValueError("Constant index exceeds local pool")
                        value.update(describe(pool[index], export_name))
                    else:
                        value["constant_resolution"] = "No local constant pool in this block"
                else:
                    raise ValueError("Unknown Push value kind")
                values.append(value)
            row["push_values"] = values
        if code in (0x9B, 0x8E):
            row["scope_limit"] = "Nested function body not expanded or interpreted"
        rows.append(row)
        pos += length
        if code == 0:
            if pos != len(data):
                raise ValueError("Bytes after actionEnd")
            return rows
    raise ValueError("Missing actionEnd")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("archive")
    ap.add_argument("--helper", required=True)
    args = ap.parse_args()
    helper = Path(args.helper)
    assert sha(helper.read_bytes()) == HELPER_SHA256
    spec = importlib.util.spec_from_file_location("bounded_resource_helpers", helper)
    swf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(swf)
    assert sha(Path(args.archive).read_bytes()) == swf.EXPECTED
    fixtures()
    output = {"controls": [], "actions": [], "start": []}
    with zipfile.ZipFile(args.archive) as z:
        for member in ("Lyles.swf", "Ong.swf"):
            raw = z.read(member)
            data = swf.unpack(raw)
            rect_end = 8 + (5 + 4 * (data[8] >> 3) + 7) // 8
            tags = list(swf.walk(data, rect_end + 4, len(data)))
            frames = collections.defaultdict(lambda: 1)
            control, exports, symbol = [], [], None
            for code, offset, body, path in tags:
                frame = frames[path]
                if code == 1:
                    frames[path] += 1
                if code not in (15, 17, 56, 89):
                    continue
                r = Reader(body)
                row = {"tag_code": code, "uncompressed_tag_offset": offset,
                       "body_bytes": len(body), "body_sha256": sha(body), "container": path,
                       "local_frame_ordinal": frame}
                if code == 15:
                    row.update(sound_id=r.uint(2), sound_info=sound_info(r))
                elif code == 89:
                    row.update(class_name=r.cstring_hash(), sound_info=sound_info(r))
                elif code == 17:
                    row["button_id"] = r.uint(2)
                    row["transitions"] = []
                    for i in range(4):
                        sid = r.uint(2)
                        value = {"transition_index": i, "sound_id": sid}
                        if sid:
                            value["sound_info"] = sound_info(r)
                        row["transitions"].append(value)
                else:
                    values = []
                    for _ in range(r.uint(2)):
                        cid = r.uint(2)
                        name = cstring(r)
                        values.append({"character_id": cid, "symbol_name": {"string_bytes": len(name), "string_sha256": sha(name)}})
                        if cid == 1:
                            assert symbol is None
                            symbol = name
                    row["exports"] = values
                r.end()
                (exports if code == 56 else control).append(row)
            output["controls"].append({"member": member, "member_sha256": sha(raw),
                "member_bytes": len(raw), "frame_rate_header": struct.unpack_from("<H", data, rect_end)[0] / 256,
                "declared_root_frames": struct.unpack_from("<H", data, rect_end + 2)[0],
                "walked_root_show_frames": frames["root"] - 1, "controls": control, "exports": exports,
                "control_tag_counts": {str(c): sum(t[0] == c for t in tags) for c in (15, 17, 56, 89)}})
            assert symbol is not None
            blocks = [(o, b, p) for c, o, b, p in tags if c == 12 and symbol + b"\0" in b]
            assert len(blocks) <= 2
            selected = []
            variable = None
            for o, b, p in blocks:
                assert len(b) <= 65536
                selected.append({"uncompressed_tag_offset": o, "body_bytes": len(b),
                                 "body_sha256": sha(b), "container": p, "actions": records(b, symbol)})
                assert b[0] == 0x88
                r = Reader(b[3:3 + int.from_bytes(b[1:3], "little")])
                constants = [cstring(r) for _ in range(r.uint(2))]
                r.end()
                variable = constants[0]
            output["actions"].append({"member": member, "member_sha256": sha(raw),
                "symbol_name": describe(symbol, symbol), "DoAction_count": sum(t[0] == 12 for t in tags),
                "matching_blocks": selected})
            assert variable is not None
            starts = [(o, b, p) for c, o, b, p in tags if c == 12 and variable + b"\0" in b and b"start\0" in b]
            candidates = [{"uncompressed_tag_offset": o, "body_bytes": len(b), "body_sha256": sha(b), "container": p} for o, b, p in starts]
            extra = []
            if len(starts) == 1 and len(starts[0][1]) <= 65536:
                o, b, p = starts[0]
                extra = [{"uncompressed_tag_offset": o, "body_bytes": len(b), "body_sha256": sha(b), "container": p, "actions": records(b, symbol)}]
            output["start"].append({"member": member, "member_sha256": sha(raw),
                "variable_name_sha256": sha(variable), "candidate_locators": candidates, "selected_blocks": extra})
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()

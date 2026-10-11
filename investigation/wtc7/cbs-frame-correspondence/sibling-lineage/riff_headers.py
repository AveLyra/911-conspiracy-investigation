"""Versioned header walk from lineage-142; no subprocesses or essence decoding."""
import hashlib
import re
import struct
from fractions import Fraction


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(stream, size, *, max_payload=4*1024*1024, max_records=10000, max_depth=12):
    rows, used = [], 0
    if any(type(v) is not int or v < 0 for v in (size, max_payload, max_records, max_depth)):
        raise ValueError("invalid nonnegative bound")

    def read(offset, n):
        stream.seek(offset)
        data = stream.read(n)
        if len(data) != n:
            raise ValueError("short read")
        return data

    def walk(start, end, parents, depth):
        nonlocal used
        if depth > max_depth:
            raise ValueError("depth limit")
        offset = start
        while offset < end:
            if len(rows) >= max_records:
                raise ValueError("record limit")
            if end - offset < 8:
                raise ValueError("truncated header")
            kind, count = struct.unpack("<4sI", read(offset, 8))
            payload, stop = offset + 8, offset + 8 + count
            padded = stop + count % 2
            if padded > end:
                raise ValueError("chunk outside parent")
            row = {"offset": offset, "kind": kind.decode("ascii", "backslashreplace"),
                   "kind_hex": kind.hex(), "bytes": count, "parents": parents}
            rows.append(row)
            if kind in (b"RIFF", b"LIST"):
                if count < 4:
                    raise ValueError("container lacks type")
                sub = read(payload, 4)
                row["container_type"] = sub.decode("ascii", "backslashreplace")
                if kind == b"RIFF" and sub not in (b"AVI ", b"AVIX"):
                    raise ValueError("unsupported RIFF type")
                if sub == b"movi":
                    row["skip_reason"] = "movie payload"
                else:
                    walk(payload + 4, stop, parents + [row["container_type"]], depth + 1)
            elif kind in (b"JUNK", b"idx1", b"indx") or kind.startswith(b"ix"):
                row["skip_reason"] = "padding or index"
            elif re.fullmatch(rb"[0-9A-Fa-f]{2}(?:db|dc|wb|pc)", kind):
                row["skip_reason"] = "essence or palette outside movie list"
            else:
                if used + count > max_payload:
                    raise ValueError("payload limit")
                data = read(payload, count)
                used += count
                row["payload_hex"] = data.hex()
                row["payload_sha256"] = digest(data)
            offset = padded

    if read(0, 4) != b"RIFF":
        raise ValueError("not RIFF")
    walk(0, size, [], 0)
    return {"records": rows, "metadata_payload_bytes_read": used,
            "limits": {"payload": max_payload, "records": max_records, "depth": max_depth}}


def fields(rows):
    result = {key: [] for key in ("tc_O", "tc_A", "rn_O", "rn_A", "cmnt")}
    for row in rows:
        key = row["kind"]
        if key not in result or "payload_hex" not in row:
            continue
        expected = "Cdat" if key == "cmnt" else "Tdat"
        if not row["parents"] or row["parents"][-1] != expected:
            continue
        data = bytes.fromhex(row["payload_hex"])
        prefix, sep, tail = data.partition(b"\0")
        try:
            text = prefix.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        result[key].append({"header_offset": row["offset"], "payload_offset": row["offset"] + 8,
                            "bytes": len(data), "payload_sha256": digest(data),
                            "prefix_utf8": text, "prefix_hex": prefix.hex(),
                            "NUL_present": bool(sep), "tail_hex": tail.hex()})
    return result


def video_headers(rows):
    result = []
    for row in rows:
        if row["kind"] != "strh" or row["parents"][-2:] != ["hdrl", "strl"]:
            continue
        data = bytes.fromhex(row["payload_hex"])
        if data[:4] != b"vids":
            continue
        if len(data) < 56:
            raise ValueError("short video stream header")
        initial, scale, rate, start, length = struct.unpack_from("<IIIII", data, 16)
        if scale == 0 or rate == 0:
            raise ValueError("zero video timebase")
        result.append({"header_offset": row["offset"], "initial_frames": initial,
                       "scale": scale, "rate": rate, "start": start, "length": length,
                       "time_base": str(Fraction(scale, rate)),
                       "duration_seconds_rational": str(Fraction(length * scale, rate))})
    return result


def timecode(text, drop=False):
    if not isinstance(text, str):
        return None
    match = re.fullmatch(r"([0-9]{2})([:;])([0-9]{2})\2([0-9]{2})\2([0-9]{2})", text)
    if not match:
        return None
    h, m, s, f = (int(match.group(k)) for k in (1, 3, 4, 5))
    if h > 23 or m > 59 or s > 59 or f > 29:
        return None
    if drop and m % 10 and s == 0 and f < 2:
        return None
    total = (h * 3600 + m * 60 + s) * 30 + f
    if drop:
        minutes = h * 60 + m
        total -= 2 * (minutes - minutes // 10)
    return total


def unique_text(values):
    # Even equal duplicate occurrences are not silently collapsed.
    if len(values) != 1 or not values[0]["prefix_utf8"]:
        return None
    return values[0]["prefix_utf8"]


def compare(items, drop, lane="O"):
    if lane not in ("O", "A"):
        raise ValueError("unknown original/alternate lane")
    groups, unavailable = {}, []
    for item in items:
        fs = item["fields"]
        tape = unique_text(fs["rn_" + lane])
        tc = unique_text(fs["tc_" + lane])
        n = timecode(tc, drop)
        if tape is None or tc is None or n is None:
            unavailable.append({"clip": item["clip"], "reason": "missing/duplicate tape or timecode in this lane, or unconvertible label"})
            continue
        groups.setdefault(tape, []).append((n, item))
    output = []
    for tape, members in sorted(groups.items()):
        members.sort(key=lambda x: (x[0], x[1]["clip"]))
        edges = []
        for (na, a), (nb, b) in zip(members, members[1:]):
            count = a["video_header"]["length"]
            unit = Fraction(1001, 30000) if drop else Fraction(1, 30)
            edges.append({"from": a["clip"], "to": b["clip"], "equal_start": na == nb,
                          "start_delta_frames": nb - na,
                          "start_delta_seconds": str((nb-na) * unit),
                          "conditional_gap_frames": nb - na - count,
                          "conditional_gap_seconds": str((nb-na-count) * unit)})
        output.append({"tape": tape, "sorted_clips": [x[1]["clip"] for x in members],
                       "start_frame_labels": [x[0] for x in members], "adjacent": edges})
    return {"lane": lane, "interpretation": "DF30000/1001" if drop else "ND30",
            "groups": output, "unavailable": unavailable,
            "meaning": "conditional common-source one-to-one mapping; not authenticated event chronology"}

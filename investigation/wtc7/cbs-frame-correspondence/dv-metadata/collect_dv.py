"""Fixed-input DV metadata collection; stdout only, no codecs or subprocesses."""
import argparse
import base64
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import platform
import re
import struct
import zlib

from dif_metadata import extract_frame, iterate_packs

UNIT = Path(__file__).resolve().parent
INPUT = UNIT.parent / "sibling-lineage/inputs.json"
INPUT_SHA = "56b787a9af0738ba422b71ed98413c2712a4691a99242ff493967c19d90b4f06"
TARGET_TYPES = {0x13, 0x52, 0x53, 0x62, 0x63}
REQUIRED = {"PLAN.md", "references.md", "dif_metadata.py", "test_dif_metadata.py",
            "collect_dv.py", "test_collect_dv.py", "../sibling-lineage/inputs.json",
            "sources/ffmpeg-n7.1-libavcodec-dv.h",
            "sources/ffmpeg-n7.1-libavcodec-dv_profile.c",
            "sources/ffmpeg-n7.1-libavcodec-dvenc.c",
            "sources/ffmpeg-n7.1-libavformat-dvenc.c"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pin(path):
    with path.open("rb") as stream:
        value = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"bytes": path.stat().st_size, "sha256": value}


def verify_freeze(freeze):
    require(set(freeze["files"]) == REQUIRED, "incomplete/unexpected frozen dependency set")
    for name, expected in freeze["files"].items():
        require(pin(UNIT/name) == expected, "changed frozen dependency: "+name)


def movie_chunks(stream, size, max_chunks=10000, max_depth=12):
    """Walk bounded RIFF headers, not payload signatures; return stream0 frames."""
    chunks = []
    count = 0

    def read_at(offset, amount):
        require(0 <= offset <= size and 0 <= amount <= size-offset, "read outside file")
        stream.seek(offset)
        value = stream.read(amount)
        require(len(value) == amount, "short RIFF read")
        return value

    def walk(start, stop, parents, depth):
        nonlocal count
        require(depth <= max_depth, "RIFF depth limit")
        offset = start
        while offset < stop:
            require(count < max_chunks, "RIFF chunk limit")
            require(stop-offset >= 8, "truncated RIFF header")
            kind, length = struct.unpack("<4sI", read_at(offset, 8))
            end = offset+8+length
            padded = end+(length % 2)
            require(padded <= stop, "RIFF payload outside parent")
            count += 1
            if kind in (b"RIFF", b"LIST"):
                require(length >= 4, "RIFF container lacks type")
                form = read_at(offset+8, 4)
                if kind == b"RIFF":
                    require(not parents and form in (b"AVI ", b"AVIX"), "unexpected RIFF type/location")
                if form == b"movi":
                    require(len(parents)==1 and parents[0] in (b"AVI ",b"AVIX"), "unexpected movi hierarchy")
                elif b"movi" in parents:
                    require(form == b"rec " and parents[-1] == b"movi", "unsupported movie list nesting")
                walk(offset+12, end, parents+[form], depth+1)
            elif re.fullmatch(rb"[0-9A-Fa-f]{2}(?:db|dc)", kind):
                require(b"movi" in parents, "video outside movi")
                require(kind[:2] == b"00", "unexpected video stream")
                require(length == 120000, "unsupported video chunk size")
                require(len(chunks) < 2500, "frame limit")
                chunks.append([offset+8, length])
            offset = padded

    require(size >= 12 and read_at(0, 4) == b"RIFF", "not RIFF")
    walk(0, size, [], 0)
    return chunks, count


def compress_metadata(data):
    encoded = zlib.compress(data, 9)
    require(len(encoded) <= 1024*1024, "compressed metadata limit")
    require(zlib.decompress(encoded) == data, "metadata compression round-trip failure")
    return {"encoding": "zlib-base64", "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "compressed_bytes": len(encoded),
            "compressed_sha256": hashlib.sha256(encoded).hexdigest(),
            "data": base64.b64encode(encoded).decode("ascii")}


def collect(path, expected_frames):
    counts = defaultdict(Counter)
    targets = {}
    retained = bytearray()
    with path.open("rb") as stream:
        chunks, header_count = movie_chunks(stream, path.stat().st_size)
        require(len(chunks) == expected_frames, "actual/declared frame count mismatch")

        def read_at(offset, amount):
            stream.seek(offset)
            return stream.read(amount)

        for frame, (offset, size) in enumerate(chunks):
            try:
                packed, detail = extract_frame(read_at, offset, size)
            except ValueError as exc:
                raise ValueError(f"frame {frame}: {exc}") from exc
            require(len(packed) == 9570, "unexpected retained frame length")
            retained.extend(packed)
            per_frame = Counter()
            for row in iterate_packs(packed):
                # No date/time decoding or majority-value selection here.
                area = row["area"]
                raw = row["raw"]
                counts[area][f"{raw[0]:02x}"] += 1
                if raw[0] in TARGET_TYPES:
                    per_frame[(area, raw.hex())] += 1
            for (area, raw), n in sorted(per_frame.items()):
                key = area+":"+raw
                if key not in targets:
                    require(len(targets)<25000, "raw timing variant limit")
                    targets[key] = {"area": area, "raw_hex": raw, "occurrences": 0,
                                    "frames_present": 0, "first_frame": frame,
                                    "last_frame": frame}
                record = targets[key]
                record["occurrences"] += n
                record["frames_present"] += 1
                record["last_frame"] = frame
    require(sum(sum(c.values()) for c in counts.values()) == expected_frames*660,
            "pack-slot population mismatch")
    return {"frames": len(chunks), "frame_chunks": chunks, "riff_headers": header_count,
            "retained_bytes_per_frame": 9570, "pack_slots_per_frame": 660,
            "pack_type_counts": {a: dict(sorted(c.items())) for a,c in sorted(counts.items())},
            "target_variants": list(targets.values()),
            "metadata": compress_metadata(bytes(retained))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clip", type=int, required=True, choices=range(1,9))
    args = parser.parse_args()
    freeze_path = UNIT / "freeze.json"
    freeze_pin = pin(freeze_path)
    freeze = json.loads(freeze_path.read_text())
    verify_freeze(freeze)
    require(pin(INPUT)["sha256"] == INPUT_SHA, "changed prior input manifest")
    manifest = json.loads(INPUT.read_text())
    require([r["clip"] for r in manifest["items"]] == list(range(1,9)), "changed population")
    item = manifest["items"][args.clip-1]
    source = (INPUT.parent/manifest["source_root"]).resolve()
    require(source == UNIT.parent.parent/"cbs-vince-source-screen", "unexpected source root")
    dependencies = {}
    for name in [item["acquisition_record"], item["container_record"], item["path"]]:
        dependencies[name] = pin(source/name)
    rec = next(r for r in manifest["acquisition_records"] if r["path"]==item["acquisition_record"])
    require(dependencies[item["acquisition_record"]]["sha256"] == rec["sha256"], "changed acquisition record")
    require(dependencies[item["container_record"]]["sha256"] == item["container_record_sha256"], "changed saved probe")
    require(dependencies[item["path"]] == {k:item[k] for k in ("bytes","sha256")}, "changed source bytes")
    saved = json.loads((source/item["container_record"]).read_text())
    video = [s for s in saved["streams"] if s["codec_type"]=="video"]
    require(len(video)==1 and video[0]["index"]==0 and video[0]["codec_name"]=="dvvideo"
            and video[0]["codec_tag_string"]=="dvsd" and video[0]["width"]==720
            and video[0]["height"]==480, "unsupported saved stream profile")
    frames = int(item["saved_video"]["nb_frames"])
    require(frames==int(video[0]["nb_frames"]) and frames<=2500, "unexpected frame population")
    result = collect(source/item["path"], frames)
    for name, expected in dependencies.items():
        require(pin(source/name)==expected, "dependency changed during scan")
    verify_freeze(freeze)
    require(pin(freeze_path)==freeze_pin, "freeze changed during scan")
    output = json.dumps({"schema":"dv-metadata-inventory-v1", "clip":args.clip,
                      "python":platform.python_version(), "source":item,
                      "dependencies":dependencies, "freeze":freeze_pin,
                      "before_after_pins_match":True, "result":result}, separators=(",",":"))
    require(len(output.encode("utf-8")) <= 8*1024*1024, "serialized output limit")
    print(output)


if __name__ == "__main__":
    main()

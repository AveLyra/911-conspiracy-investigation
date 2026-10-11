"""Read-only, separately implemented audit of fixed DV metadata artifacts.

No producer imports, media codecs, clock decoding, subprocesses or file writes.
Shares the declared FFmpeg-based layout, input inventory, Python runtime and
stdlib SHA256/zlib with the producer; this is not a second historical source.
Use --self-test for synthetic, in-memory controls only. Default audits all eight.
"""
import argparse
from collections import Counter, defaultdict
from io import BytesIO
import hashlib
import json
from pathlib import Path
import stat
import struct
import zlib

BASE = Path(__file__).resolve().parent
TARGET = {0x13, 0x52, 0x53, 0x62, 0x63}
V1_NAMES = {"PLAN.md", "references.md", "collect_dv.py", "dif_metadata.py",
            "test_collect_dv.py", "test_dif_metadata.py", "../sibling-lineage/inputs.json",
            "sources/ffmpeg-n7.1-libavcodec-dv.h", "sources/ffmpeg-n7.1-libavcodec-dv_profile.c",
            "sources/ffmpeg-n7.1-libavcodec-dvenc.c", "sources/ffmpeg-n7.1-libavformat-dvenc.c"}
V2_NAMES = {"PLAN.md", "run.py", "storage.py", "test_run.py", "test_storage.py", "../freeze.json"} | {"../" + p for p in V1_NAMES}
WATCH = {}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    digest = hashlib.sha256()
    length = 0
    with path.open("rb") as stream:
        while data := stream.read(262144):
            digest.update(data)
            length += len(data)
    need(length == path.stat().st_size, "file size changed during hash")
    return {"bytes": length, "sha256": digest.hexdigest()}


def watch(path, expected=None):
    path = path.resolve()
    actual = pin(path)
    if expected is not None:
        need(actual == expected, f"pin mismatch: {path}")
    if path in WATCH:
        need(WATCH[path] == actual, f"changed between reads: {path}")
    WATCH[path] = actual
    return actual


def exact_int(value, expected, label):
    need(type(value) is int and value == expected, label)


def read_at(stream, offset, size):
    stream.seek(offset)
    value = stream.read(size)
    need(len(value) == size, "short direct read")
    return value


def riff_frames(stream, size):
    """Iterative container traversal; no producer traversal or payload search."""
    need(size >= 12 and read_at(stream, 0, 4) == b"RIFF", "missing RIFF")
    pending = [(0, size, ())]
    frames = []
    count = 0
    while pending:
        cursor, stop, ancestors = pending.pop()
        need(len(ancestors) <= 12, "RIFF depth cap")
        while cursor < stop:
            need(stop-cursor >= 8 and count < 10000, "RIFF header/count boundary")
            header = read_at(stream, cursor, 8)
            kind = header[:4]
            length = int.from_bytes(header[4:], "little")
            end = cursor + 8 + length
            following = end + (length & 1)
            need(following <= stop, "RIFF payload extent")
            count += 1
            if kind in (b"RIFF", b"LIST"):
                need(length >= 4, "short container form")
                form = read_at(stream, cursor+8, 4)
                if kind == b"RIFF":
                    need(not ancestors and form in (b"AVI ", b"AVIX"), "RIFF hierarchy")
                if form == b"movi":
                    need(len(ancestors) == 1 and ancestors[0] in (b"AVI ", b"AVIX"), "movi hierarchy")
                elif b"movi" in ancestors:
                    need(form == b"rec " and ancestors[-1] == b"movi", "movie nested list")
                if following < stop:
                    pending.append((following, stop, ancestors))
                pending.append((cursor+12, end, ancestors+(form,)))
                break
            if all(x in b"0123456789abcdefABCDEF" for x in kind[:2]) and kind[2:] in (b"dc", b"db"):
                need(b"movi" in ancestors and kind[:2] == b"00", "unexpected video location/stream")
                need(length == 120000 and len(frames) < 2500, "video size/frame cap")
                frames.append([cursor+8, length])
            cursor = following
    return frames, count


def inflate(encoded, expected):
    need(0 < len(encoded) <= 1048576, "compressed chunk cap")
    decoder = zlib.decompressobj()
    raw = decoder.decompress(encoded, expected+1)
    need(len(raw) == expected and decoder.eof, "zlib length/EOF")
    need(not decoder.unused_data and not decoder.unconsumed_tail, "zlib trailing data")
    return raw


def load_chunks(directory, metadata, frames):
    need(metadata["schema"] == "dv-metadata-chunk-storage-v1", "storage schema")
    for key, value in (("frames", frames), ("bytes_per_frame", 9570), ("chunk_frames", 100), ("raw_bytes", frames*9570)):
        exact_int(metadata[key], value, key)
    entries = metadata["chunks"]
    need(len(entries) == (frames+99)//100 <= 25, "chunk coverage count")
    need(not directory.is_symlink() and directory.is_dir(), "unsafe chunk directory")
    need(set(p.name for p in directory.iterdir()) == {f"chunk{i:03d}.zlib" for i in range(len(entries))}, "artifact population")
    decoded = []
    total = 0
    for index, entry in enumerate(entries):
        first, stop = index*100, min((index+1)*100, frames)
        need(entry["path"] == f"chunk{index:03d}.zlib", "chunk name/order")
        for key, value in (("first_frame", first), ("stop_frame", stop), ("frames", stop-first), ("raw_bytes", (stop-first)*9570)):
            exact_int(entry[key], value, "chunk "+key)
        path = directory / entry["path"]
        info = path.lstat()
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "unsafe chunk file")
        need(type(entry["encoded_bytes"]) is int and 0 < entry["encoded_bytes"] <= 1048576, "encoded count")
        watch(path, {"bytes": entry["encoded_bytes"], "sha256": entry["encoded_sha256"]})
        encoded = path.read_bytes()
        need(len(encoded) == entry["encoded_bytes"] and sha(encoded) == entry["encoded_sha256"], "artifact read mismatch")
        raw = inflate(encoded, entry["raw_bytes"])
        need(sha(raw) == entry["raw_sha256"], "chunk raw hash")
        decoded.append(raw)
        total += len(encoded)
    raw = b"".join(decoded)
    need(total == metadata["encoded_bytes"] and total <= 25*1048576, "whole encoded count")
    need(len(raw) == frames*9570 <= 23925000 and sha(raw) == metadata["raw_sha256"], "whole raw length/hash")
    need(metadata["readback"] == {"chunks_verified":len(entries), "frames":frames, "raw_bytes":len(raw), "raw_sha256":sha(raw), "compared_to_original_input":True}, "producer readback descriptor")
    return raw


def direct_frame(stream, start):
    """Read individual retained blocks in file order, and count raw pack slots."""
    pieces = []
    slots = []
    # A sequence is six control blocks followed by nine audio/video groups.
    types = [(0,0,80,None), (1,0,80,"subcode"), (1,1,80,"subcode")]
    types += [(2,n,80,"vaux") for n in range(3)]
    for group in range(9):
        types.append((3,group,8,"aaux"))
        types.extend((4,group*15+n,3,None) for n in range(15))
    need(len(types) == 150, "audit layout length")
    for sequence in range(10):
        for block, (section, number, take, area) in enumerate(types):
            data = read_at(stream, start+sequence*12000+block*80, take)
            need((data[0] & 0xE0) == section*32, "section ID")
            need((data[1] & 0xF0) == sequence*16 and not data[1] & 8, "sequence/channel ID")
            need(data[2] == number, "block ID")
            if section == 0:
                need(not data[3] & 128, "DSF")
            pieces.append(data)
            if area == "subcode":
                offsets = [6+8*n for n in range(6)]
            elif area == "vaux":
                offsets = [3+5*n for n in range(15)]
            elif area == "aaux":
                offsets = [3]
            else:
                offsets = []
            slots.extend((area, data[p:p+5]) for p in offsets)
    need(Counter(a for a,p in slots) == {"subcode":120,"vaux":450,"aaux":90}, "frame slot population")
    raw = b"".join(pieces)
    need(len(raw) == 9570 and all(len(p)==5 for a,p in slots), "frame retained/slot bytes")
    return raw, slots


def controls():
    for directory, names in ((BASE, V1_NAMES), (BASE/"v2", V2_NAMES)):
        watch(directory/"freeze.json")
        frozen = json.loads((directory/"freeze.json").read_text())
        need(set(frozen["files"]) == names, "freeze dependency population")
        for relative, expected in frozen["files"].items():
            watch(directory/relative, expected)


def audit():
    controls()
    watch(Path(__file__))
    input_path = BASE.parent/"sibling-lineage/inputs.json"
    need(watch(input_path)["sha256"] == "56b787a9af0738ba422b71ed98413c2712a4691a99242ff493967c19d90b4f06", "fixed input pin")
    inputs = json.loads(input_path.read_text())
    need([i["clip"] for i in inputs["items"]] == list(range(1,9)), "input clip population")
    source_root = (input_path.parent/inputs["source_root"]).resolve()
    need(source_root == BASE.parent.parent/"cbs-vince-source-screen", "source root")
    acquisition_pins = {r["path"]:r["sha256"] for r in inputs["acquisition_records"]}
    output = []
    for item in inputs["items"]:
        number = item["clip"]
        path = BASE/"v2/results"/f"clip{number}-result.json"
        result_pin = watch(path)
        need(result_pin["bytes"] <= 8*1048576, "result JSON cap")
        document = json.loads(path.read_text())
        need(document["schema"] == "dv-metadata-chunked-inventory-v2" and document["clip"] == number, "result identity")
        need(document["source"] == item and document["before_after_pins_match"] is True and document["artifact_readback_verified"] is True, "source/result identity")
        need(document["freeze"] == WATCH[(BASE/"freeze.json").resolve()] and document["v2_freeze"] == WATCH[(BASE/"v2/freeze.json").resolve()], "result freeze identity")
        required = {item["path"], item["acquisition_record"], item["container_record"]}
        need(set(document["dependencies"]) == required, "result source dependency set")
        for relative, expected in document["dependencies"].items():
            watch(source_root/relative, expected)
        need(document["dependencies"][item["path"]] == {k:item[k] for k in ("bytes","sha256")}, "source expected pin")
        need(document["dependencies"][item["acquisition_record"]]["sha256"] == acquisition_pins[item["acquisition_record"]], "acquisition pin join")
        need(document["dependencies"][item["container_record"]]["sha256"] == item["container_record_sha256"], "container pin join")
        container = json.loads((source_root/item["container_record"]).read_text())
        videos = [s for s in container["streams"] if s["codec_type"] == "video"]
        need(len(videos)==1, "saved video stream count")
        video = videos[0]
        need([video[k] for k in ("index","codec_name","codec_tag_string","width","height")] == [0,"dvvideo","dvsd",720,480], "saved video profile")
        frames = int(item["saved_video"]["nb_frames"])
        need(frames == int(video["nb_frames"]) and 1<=frames<=2500, "saved frame count")
        result = document["result"]
        for key, expected in (("frames",frames),("retained_bytes_per_frame",9570),("pack_slots_per_frame",660)):
            exact_int(result[key],expected,"result "+key)
        retained = load_chunks(path.parent/f"clip{number}",result["metadata"],frames)
        counts = {area:Counter() for area in ("subcode","vaux","aaux")}
        occurrences = Counter()
        seen = defaultdict(list)
        target_frames = Counter()
        frame_patterns = Counter()
        differing_frames = 0
        with (source_root/item["path"]).open("rb") as stream:
            locations, headers = riff_frames(stream,item["bytes"])
            need(locations == result["frame_chunks"] and len(locations)==frames, "direct RIFF frame coverage")
            exact_int(result["riff_headers"],headers,"RIFF header count")
            for frame, (start, length) in enumerate(locations):
                raw, slots = direct_frame(stream,start)
                need(raw == retained[frame*9570:(frame+1)*9570], f"retained byte mismatch clip {number} frame {frame}")
                present = set()
                frame_counts = {area:Counter() for area in ("subcode","vaux","aaux")}
                for area, pack in slots:
                    counts[area][f"{pack[0]:02x}"] += 1
                    frame_counts[area][f"{pack[0]:02x}"] += 1
                    if pack[0] in TARGET:
                        key = (area, pack.hex())
                        occurrences[key] += 1
                        present.add(key)
                pattern = tuple((area,tuple(sorted(c.items()))) for area,c in sorted(frame_counts.items()))
                frame_patterns[pattern] += 1
                for key in present:
                    seen[key].append(frame)
                for kind in TARGET:
                    if any(int(raw_hex[:2],16)==kind for area,raw_hex in present):
                        target_frames[f"{kind:02x}"] += 1
                if len({raw_hex for area,raw_hex in present if raw_hex.startswith("13")}) > 1:
                    differing_frames += 1
        need({a:dict(c) for a,c in counts.items()} == result["pack_type_counts"], "all pack-type counts")
        actual_variants = {(area,raw):{"area":area,"raw_hex":raw,"occurrences":count,"frames_present":len(seen[(area,raw)]),"first_frame":seen[(area,raw)][0],"last_frame":seen[(area,raw)][-1]} for (area,raw),count in occurrences.items()}
        reported_variants = {(r["area"],r["raw_hex"]):r for r in result["target_variants"]}
        need(len(reported_variants)==len(result["target_variants"])<=25000 and actual_variants==reported_variants, "all target variants/counts/frame bounds")
        output.append({"clip":number,"frames":frames,"riff_headers":headers,"chunks":len(result["metadata"]["chunks"]),"retained_bytes":len(retained),"slots":frames*660,"pack_type_counts":{a:dict(sorted(c.items())) for a,c in counts.items()},"per_frame_pack_type_patterns":[{"frames":n,"counts":{a:dict(c) for a,c in pattern}} for pattern,n in sorted(frame_patterns.items())],"target_type_occurrences":{f"{t:02x}":sum(c.get(f"{t:02x}",0) for c in counts.values()) for t in sorted(TARGET)},"frames_with_target_type":{f"{t:02x}":target_frames[f"{t:02x}"] for t in sorted(TARGET)},"frames_with_multiple_distinct_raw_13":differing_frames,"target_variant_count":len(actual_variants),"result_pin":result_pin,"source_pin":document["dependencies"][item["path"]],"retained_sha256":sha(retained),"all_checks_pass":True})
    need(sum(r["frames"] for r in output)==5567,"whole frame population")
    for path, expected in WATCH.items():
        need(pin(path)==expected,f"audit post-pin mismatch: {path}")
    return {"schema":"independent-dv-byte-audit-v1","audit_code_pin":WATCH[Path(__file__).resolve()],"scope":"all eight admitted copies; raw metadata only; no clock/date interpretation","independence":"No producer/parser/storage imports; common declared FFmpeg layout, inputs, Python runtime and stdlib SHA256/zlib; not independent historical evidence.","frames":sum(r["frames"] for r in output),"retained_bytes":sum(r["retained_bytes"] for r in output),"slots":sum(r["slots"] for r in output),"watched_file_count":len(WATCH),"before_after_pins_match":True,"clips":output,"all_checks_pass":True}


def self_test():
    def chunk(kind,payload):
        return kind+struct.pack("<I",len(payload))+payload+(b"\0" if len(payload)&1 else b"")
    frame = bytearray(120000)
    for seq in range(10):
        sections = [(0,0)]+[(1,n) for n in range(2)]+[(2,n) for n in range(3)]
        for group in range(9):
            sections += [(3,group)]+[(4,group*15+n) for n in range(15)]
        for block,(section,number) in enumerate(sections):
            offset=seq*12000+block*80
            frame[offset:offset+3]=bytes((section*32,seq*16,number))
    synthetic=chunk(b"RIFF",b"AVI "+chunk(b"LIST",b"movi"+chunk(b"00dc",frame)))
    locations,headers=riff_frames(BytesIO(synthetic),len(synthetic))
    need(locations==[[32,120000]] and headers==3,"synthetic RIFF")
    raw,slots=direct_frame(BytesIO(synthetic),32)
    need(len(raw)==9570 and len(slots)==660,"synthetic direct bytes")
    need(inflate(zlib.compress(raw),9570)==raw,"synthetic inflate")
    refusals=0
    for broken in (synthetic[:-1],synthetic[:11]):
        try:riff_frames(BytesIO(broken),len(broken))
        except ValueError:refusals+=1
    for broken in (zlib.compress(raw)[:-1],zlib.compress(raw)+b"trailing",zlib.compress(raw)+zlib.compress(raw)):
        try:inflate(broken,9570)
        except ValueError:refusals+=1
    changed=bytearray(synthetic); changed[32+119920+2]^=1
    try:direct_frame(BytesIO(changed),32)
    except ValueError:refusals+=1
    need(refusals==6,"synthetic refusal population")
    return {"synthetic_positive_checks":3,"synthetic_refusals":refusals,"passed":True}


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    print(json.dumps(self_test() if args.self_test else audit(),sort_keys=True))

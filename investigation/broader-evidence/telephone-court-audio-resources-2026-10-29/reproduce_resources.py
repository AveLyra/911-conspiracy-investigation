"""Portable passive court-resource check; optional local-only audio decoding.

Usage: python3 reproduce_resources.py /path/to/court-flights.zip --decode
Prints numeric/hash results; never executes SWF code, plays audio or saves audio.
"""
import argparse
import collections
import hashlib
import json
import shutil
import struct
import subprocess
import zipfile
import zlib

EXPECTED = "3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801"
MEMBERS = ("AA11.swf", "AA77.swf", "UA175.swf", "UA93.swf",
           "Lyles.swf", "Ong.swf", "Atta.swf", "Jarrah.swf")
MAX_BYTES = 64 * 1024 * 1024
SELECTED = (14, 15, 17, 18, 19, 45, 89, 57, 71, 60, 61, 87)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unpack(raw):
    if len(raw) < 12 or raw[:3] not in (b"FWS", b"CWS"):
        raise ValueError("Unsupported or short SWF")
    declared = struct.unpack_from("<I", raw, 4)[0]
    if not 12 <= declared <= MAX_BYTES:
        raise ValueError("Declared length outside scope")
    if raw[:3] == b"CWS":
        dec = zlib.decompressobj()
        body = dec.decompress(raw[8:], declared - 8 + 1)
        if not dec.eof or dec.unused_data or dec.unconsumed_tail:
            raise ValueError("Incomplete, trailing or excessive compressed data")
        data = b"FWS" + raw[3:8] + body
    else:
        data = raw
    if len(data) != declared:
        raise ValueError("Declared/actual length mismatch")
    return data


def walk(data, start, stop, path="root", depth=0):
    if depth > 64 or not 0 <= start <= stop <= len(data):
        raise ValueError("Container bounds/depth")
    pos = start
    while pos < stop:
        offset = pos
        if pos + 2 > stop:
            raise ValueError("Short tag header")
        header = struct.unpack_from("<H", data, pos)[0]
        pos += 2
        code, size = header >> 6, header & 63
        if size == 63:
            if pos + 4 > stop:
                raise ValueError("Short extended header")
            size = struct.unpack_from("<I", data, pos)[0]
            pos += 4
        if pos + size > stop:
            raise ValueError("Tag exceeds container")
        body = data[pos:pos + size]
        yield code, offset, body, path
        if code == 39:
            if size < 6:
                raise ValueError("Short sprite")
            sprite = struct.unpack_from("<H", body)[0]
            yield from walk(data, pos + 4, pos + size,
                            path + "/sprite-" + str(sprite), depth + 1)
        pos += size
        if code == 0:
            if size or pos != stop:
                raise ValueError("Nonterminal or nonempty End tag")
            return
    raise ValueError("Missing End tag")


def decode(mp3, ffprobe, ffmpeg):
    def run(args):
        return subprocess.run(args, input=mp3, capture_output=True, check=True, timeout=90)
    probe = run([ffprobe, "-v", "error", "-select_streams", "a:0", "-show_entries",
                 "stream=codec_name,sample_rate,channels", "-of", "json", "pipe:0"])
    stream = json.loads(probe.stdout)["streams"][0]
    frames = run([ffprobe, "-v", "error", "-select_streams", "a:0", "-show_frames",
                  "-show_entries", "frame=nb_samples", "-of", "json", "pipe:0"])
    frame_list = json.loads(frames.stdout)["frames"]
    pcm = run([ffmpeg, "-v", "error", "-i", "pipe:0", "-map", "0:a:0",
               "-c:a", "pcm_s16le", "-f", "s16le", "pipe:1"]).stdout
    assert len(pcm) <= MAX_BYTES and len(pcm) % (2 * int(stream["channels"])) == 0
    samples = len(pcm) // (2 * int(stream["channels"]))
    assert samples == sum(int(x["nb_samples"]) for x in frame_list)
    return {"probe": stream, "decoded_pcm_sha256": sha(pcm), "decoded_pcm_bytes": len(pcm),
            "decoded_sample_count_per_channel": samples, "probed_frame_count": len(frame_list),
            "probed_frame_sample_sum": samples}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive")
    parser.add_argument("--decode", action="store_true")
    args = parser.parse_args()
    with open(args.archive, "rb") as f:
        assert sha(f.read()) == EXPECTED
    ffprobe, ffmpeg = shutil.which("ffprobe"), shutil.which("ffmpeg")
    if args.decode and not (ffprobe and ffmpeg):
        raise RuntimeError("Local ffprobe and ffmpeg required for --decode")
    result = {"archive_sha256": EXPECTED, "members": [], "decodes": []}
    with zipfile.ZipFile(args.archive) as z:
        for name in MEMBERS:
            assert z.getinfo(name).file_size <= MAX_BYTES
            raw = z.read(name)
            data = unpack(raw)
            # RECT begins with five-bit Nbits, then four signed Nbits fields.
            start = 8 + (5 + 4 * (data[8] >> 3) + 7) // 8 + 4
            tags = list(walk(data, start, len(data)))
            counts = collections.Counter(t[0] for t in tags)
            events = []
            streams = []
            for code, offset, body, path in tags:
                if code == 14:
                    assert len(body) >= 7
                    row = {"uncompressed_tag_offset": offset, "body_bytes": len(body),
                           "body_sha256": sha(body), "container": path,
                           "sound_id": struct.unpack_from("<H", body)[0],
                           "format_code": body[2] >> 4, "rate_code": (body[2] >> 2) & 3,
                           "sample_count": struct.unpack_from("<I", body, 3)[0],
                           "sound_data_bytes": len(body) - 7, "sound_data_sha256": sha(body[7:])}
                    events.append(row)
                    if args.decode and name in ("Lyles.swf", "Ong.swf") and row["sound_id"] == 1 and path == "root":
                        assert row["format_code"] == 2 and len(body) >= 9
                        mp3 = body[9:]
                        checked = decode(mp3, ffprobe, ffmpeg)
                        checked.update(member=name, mp3_sha256=sha(mp3), mp3_bytes=len(mp3),
                                       signed_seek_samples=struct.unpack_from("<h", body, 7)[0],
                                       swf_declared_sample_count=row["sample_count"])
                        result["decodes"].append(checked)
                if code in (18, 45) and path == "root":
                    streams.append({"uncompressed_tag_offset": offset, "header_hex": body.hex()})
            result["members"].append({"member": name, "member_sha256": sha(raw),
                                       "tag_counts": dict(counts), "events": events,
                                       "root_stream_headers": streams})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

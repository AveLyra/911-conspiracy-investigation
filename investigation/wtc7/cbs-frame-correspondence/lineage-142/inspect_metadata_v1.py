"""Read-only, fixed-input metadata inventory; no decoded image/audio output."""
import hashlib
import io
import json
from pathlib import Path
import platform
import struct
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
INPUTS = {
    "avi": (BASE / "cbs-vince-source-screen/stage4/raw/clip7-attempt1.avi",
            140334936, "a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b"),
    "jpeg": (BASE / "fire-coverage-batch3/assets/run01/images/A-7c7cc22dc34c.jpg",
             151488, "68c9d384ac3b1099361f255f80a74d387073d67500089099765f4f0cf030215a"),
    "pdf": (Path("/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf"),
            52766002, "30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f"),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    with path.open("rb") as stream:
        sha = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha}


def safe(value):
    if isinstance(value, bytes):
        result = {"bytes": len(value), "sha256": digest(value)}
        try:
            result["utf8"] = value.decode("utf-8")
        except UnicodeDecodeError:
            result["hex"] = value.hex()
        return result
    if isinstance(value, dict):
        return {str(k): safe(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [safe(v) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def riff_inventory(stream, size):
    """Enumerate RIFF headers, skip essence/index, retain bounded metadata."""
    rows = []
    used = 0

    def walk(start, end, parents, depth):
        nonlocal used
        if depth > 12:
            raise ValueError("RIFF depth limit")
        offset = start
        while offset < end:
            if len(rows) >= 10000 or end - offset < 8:
                raise ValueError("RIFF record limit or truncated header")
            stream.seek(offset)
            header = stream.read(8)
            if len(header) != 8:
                raise ValueError("RIFF short read")
            kind, count = struct.unpack("<4sI", header)
            payload = offset + 8
            stop = payload + count
            padded = stop + (count % 2)
            if padded > end:
                raise ValueError("RIFF chunk beyond parent")
            row = {"offset": offset, "kind_hex": kind.hex(),
                   "kind": kind.decode("ascii", "backslashreplace"),
                   "bytes": count, "parents": parents}
            rows.append(row)
            if kind in (b"RIFF", b"LIST"):
                if count < 4:
                    raise ValueError("RIFF container lacks type")
                stream.seek(payload)
                subtype = stream.read(4)
                name = subtype.decode("ascii", "backslashreplace")
                row["container_type"] = name
                if subtype == b"movi":
                    row["payload_inspected"] = False
                else:
                    walk(payload + 4, stop, parents + [name], depth + 1)
            elif kind not in (b"JUNK", b"idx1") and not kind.startswith(b"ix"):
                used += count
                if used > 4 * 1024 * 1024:
                    raise ValueError("RIFF metadata payload limit")
                stream.seek(payload)
                data = stream.read(count)
                if len(data) != count:
                    raise ValueError("RIFF metadata short read")
                row["payload"] = safe(data)
            else:
                row["payload_inspected"] = False
            offset = padded

    stream.seek(0)
    if stream.read(4) != b"RIFF":
        raise ValueError("not RIFF")
    walk(0, size, [], 0)
    return {"records": rows, "metadata_payload_bytes_read": used,
            "scope": "header tree excluding movi, JUNK and index payloads; no DV pack parsing"}


class HeaderChecks(unittest.TestCase):
    def parse(self, data):
        return riff_inventory(io.BytesIO(data), len(data))

    def test_info_and_odd_padding(self):
        data = b"RIFF" + struct.pack("<I", 26) + b"AVI LIST" + struct.pack("<I", 14)
        data += b"INFOINAM" + struct.pack("<I", 1) + b"x\0"
        out = self.parse(data)
        self.assertEqual(out["records"][-1]["payload"]["utf8"], "x")
        self.assertEqual(out["metadata_payload_bytes_read"], 1)

    def test_movie_payload_is_not_parsed(self):
        data = b"RIFF" + struct.pack("<I", 20) + b"AVI LIST" + struct.pack("<I", 8)
        data += b"movibad!"
        out = self.parse(data)
        self.assertFalse(out["records"][-1]["payload_inspected"])
        self.assertEqual(out["metadata_payload_bytes_read"], 0)

    def test_truncated_chunk(self):
        with self.assertRaises(ValueError):
            self.parse(b"RIFF" + struct.pack("<I", 100) + b"AVI ")

    def test_container_missing_type(self):
        with self.assertRaises(ValueError):
            self.parse(b"RIFF" + struct.pack("<I", 2) + b"AB")

    def test_nonriff(self):
        with self.assertRaises(ValueError):
            self.parse(b"NOTRIFF!")


def command(argv):
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=30, check=False)
    result = {"argv": argv, "returncode": proc.returncode,
              "stdout": proc.stdout, "stderr": proc.stderr}
    if proc.returncode:
        raise RuntimeError(json.dumps(result))
    return result


def main():
    from PIL import Image, __version__ as pillow_version
    import pypdf
    from pypdf.generic import IndirectObject

    before = {key: pin(spec[0]) for key, spec in INPUTS.items()}
    for key, (_, size, sha) in INPUTS.items():
        if (before[key]["bytes"], before[key]["sha256"]) != (size, sha):
            raise ValueError(f"pinned input mismatch: {key}")
    result = {"schema": "figure142-held-metadata-v1", "inputs_before": before,
              "collector": pin(Path(__file__)), "plan": pin(HERE / "PLAN.md"),
              "runtime": {"python": platform.python_version(), "pillow": pillow_version,
                          "pypdf": pypdf.__version__}}
    ffprobe = "/opt/homebrew/bin/ffprobe"
    result["ffprobe_version"] = command([ffprobe, "-version"])
    result["container_probe"] = command([ffprobe, "-v", "error", "-show_format",
                                         "-show_streams", "-show_chapters", "-of", "json",
                                         str(INPUTS["avi"][0])])
    with INPUTS["avi"][0].open("rb") as stream:
        result["riff"] = riff_inventory(stream, INPUTS["avi"][1])
    with Image.open(INPUTS["jpeg"][0]) as image:
        result["jpeg"] = {"size": list(image.size), "format": image.format,
                          "info": safe(image.info), "exif": safe(dict(image.getexif())),
                          "application_and_comment_segments": safe(image.applist),
                          "scope": "Pillow header metadata; no image.load or pixel decoding; no post-SOS scan"}
    reader = pypdf.PdfReader(INPUTS["pdf"][0])
    obj = IndirectObject(2850, 0, reader).get_object()
    page = reader.pages[271]
    resource = page["/Resources"]["/XObject"].raw_get("/Im0")
    if (resource.idnum, resource.generation) != (2850, 0):
        raise ValueError("page image resource identity differs")
    data = obj.get_data()
    if digest(data) != INPUTS["jpeg"][2]:
        raise ValueError("PDF image stream differs from held JPEG")
    root = reader.trailer["/Root"]
    xmp = root.get("/Metadata")
    result["pdf"] = {"pages": len(reader.pages), "document_info": safe(dict(reader.metadata or {})),
                     "root_keys": sorted(root.keys()), "image_dictionary": safe(dict(obj)),
                     "page_image_reference": [resource.idnum, resource.generation],
                     "image_encoded_bytes": len(data), "image_encoded_sha256": digest(data),
                     "catalog_xmp": safe(xmp.get_object().get_data()) if xmp else None,
                     "scope": "document info/catalog XMP, page272 Im0 and object2850/0; not full-object forensic scan"}
    after = {key: pin(spec[0]) for key, spec in INPUTS.items()}
    if before != after:
        raise ValueError("inputs changed during inspection")
    result["inputs_after"] = after
    result["source_bytes_unchanged"] = True
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit("usage: inspect_metadata.py [--test]")

"""Inspect pinned candidate JPEGs without changing them or executing metadata.

python3 inspect_candidate_jpegs.py SOURCE_DIRECTORY SOURCE_PINS_JSON

Adobe resource 1036 is decoded using its documented 28-byte header. The
three-by-three thumbnail comparison is a limited scene-consistency test,
not authentication, an editing detector, or a building-origin determination.
No source image or embedded thumbnail is written by this program.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct

import numpy as np
from PIL import Image, IptcImagePlugin, __version__ as pillow_version


def need(condition, message):
    if not condition:
        raise ValueError(message)


def jpeg_segments(data):
    need(data[:2] == b"\xff\xd8", "Not a JPEG SOI")
    pos = 2
    result = []
    while pos < len(data):
        need(data[pos] == 255, "Invalid pre-scan JPEG marker boundary")
        marker_start = pos
        while pos < len(data) and data[pos] == 255:
            pos += 1
        need(pos < len(data), "Truncated JPEG marker")
        marker = data[pos]
        pos += 1
        if marker == 0xD9:
            break
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            continue
        need(pos + 2 <= len(data), "Truncated JPEG segment length")
        length = struct.unpack_from(">H", data, pos)[0]
        need(length >= 2 and pos + length <= len(data), "JPEG segment exceeds entity")
        payload_start = pos + 2
        payload = data[payload_start:pos + length]
        result.append(dict(marker=marker, marker_offset=marker_start,
                           payload_offset=payload_start, payload=payload))
        pos += length
        if marker == 0xDA:
            break  # The entropy-coded scan is decoded separately by Pillow.
    return result


def photoshop_resources(segment):
    data = segment["payload"]
    prefix = b"Photoshop 3.0\0"
    need(data.startswith(prefix), "APP13 has an unhandled signature")
    pos = len(prefix)
    result = []
    while pos < len(data):
        need(pos + 7 <= len(data), "Truncated resource header")
        need(data[pos:pos + 4] == b"8BIM", "Unhandled Photoshop resource signature")
        resource_id = struct.unpack_from(">H", data, pos + 4)[0]
        pos += 6
        name_size = data[pos]
        padded_name_size = (name_size + 2) // 2 * 2
        pos += padded_name_size
        need(pos + 4 <= len(data), "Truncated resource size")
        size = struct.unpack_from(">I", data, pos)[0]
        pos += 4
        need(pos + size <= len(data), "Resource exceeds APP13 bounds")
        body = data[pos:pos + size]
        result.append(dict(resource_id=resource_id, payload_size=size,
                           file_offset=segment["payload_offset"] + pos,
                           sha256=hashlib.sha256(body).hexdigest(), payload=body))
        pos += size + size % 2
    need(pos == len(data), "Resource padding extends beyond APP13")
    return result


def inspect(root, pins):
    records = []
    full_images = []
    thumbs = []
    for row in pins:
        path = root / row["filename"]
        data = path.read_bytes()
        need(len(data) == row["bytes"] and
             hashlib.sha256(data).hexdigest() == row["sha256"],
             "Source entity differs; preserve separately")
        segments = jpeg_segments(data)
        app13 = [s for s in segments if s["marker"] == 0xED]
        need(len(app13) == 1, "Expected one bounded Photoshop resource block")
        resources = photoshop_resources(app13[0])
        selected = [r for r in resources if r["resource_id"] == 1036]
        need(len(selected) == 1, "Expected one resource 1036")
        thumb = selected[0]
        need(len(thumb["payload"]) >= 28, "Thumbnail header truncated")
        fmt, width, height, row_bytes, total, compressed, bits, planes = (
            struct.unpack_from(">6I2H", thumb["payload"]))
        need((fmt, bits, planes) == (1, 24, 1), "Unhandled thumbnail encoding")
        need(total == row_bytes * height * planes, "Thumbnail uncompressed-size fields disagree")
        payload = thumb["payload"][28:]
        need(len(payload) == compressed, "Thumbnail compressed-size fields disagree")
        thumbnail = Image.open(io.BytesIO(payload))
        thumbnail.load()
        need(thumbnail.size == (width, height), "Thumbnail dimensions disagree")
        full = Image.open(io.BytesIO(data))
        full.load()
        need(full.format == "JPEG" and list(full.size) == row["dimensions"],
             "Full image format or dimensions differ")
        # Cross-check Pillow's independent APP13 parsing against our offsets.
        need(full.info["photoshop"][1036] == thumb["payload"],
             "Independent resource decoders disagree")
        full_images.append(full.convert("RGB"))
        thumbs.append(thumbnail.convert("RGB"))
        record = dict(
            filename=row["filename"], bytes=len(data), sha256=row["sha256"],
            dimensions=list(full.size), decoded_complete_raster=True,
            exif_entries_returned=len(full.getexif()),
            iptc_field_count_returned=len(IptcImagePlugin.getiptcinfo(full) or {}),
            application_segments=[dict(
                marker="APP" + str(s["marker"] - 0xE0),
                marker_offset=s["marker_offset"], payload_offset=s["payload_offset"],
                payload_size=len(s["payload"]),
                sha256=hashlib.sha256(s["payload"]).hexdigest())
                for s in segments if 0xE0 <= s["marker"] <= 0xEF],
            resource_descriptors=[{k: v for k, v in r.items() if k != "payload"}
                                  for r in resources],
            thumbnail=dict(resource_id=1036, resource_payload_file_offset=thumb["file_offset"],
                           jpeg_file_offset=thumb["file_offset"] + 28,
                           header=dict(format=fmt, width=width, height=height,
                                       row_bytes=row_bytes, total_bytes=total,
                                       compressed_bytes=compressed,
                                       bits_per_pixel=bits, planes=planes),
                           jpeg_sha256=hashlib.sha256(payload).hexdigest()),
            independent_resource_parser_agrees=True)
        records.append(record)
    matrix = []
    for thumbnail in thumbs:
        arr = np.asarray(thumbnail, dtype=np.float64)
        matrix.append([float(np.sqrt(np.mean((arr - np.asarray(
            full.resize(thumbnail.size, Image.Resampling.LANCZOS),
            dtype=np.float64)) ** 2))) for full in full_images])
    nearest = [int(np.argmin(r)) for r in matrix]
    need(nearest == list(range(len(pins))),
         "Thumbnail is closer to another candidate image; preserve and inspect")
    return dict(pillow_version=pillow_version, numpy_version=np.__version__,
                files=records, rmse_matrix_thumbnail_rows_full_image_columns=matrix,
                row_and_column_filenames=[r["filename"] for r in pins],
                closest_full_image_indices=nearest,
                each_thumbnail_closest_to_own_full_image=True,
                comparison_method="RGB values 0–255; full image resized with Pillow LANCZOS; no ICC transform, registration or threshold tuning",
                scope="Entity integrity, bounded metadata/thumbnail parsing, complete current raster decode and coarse three-scene consistency only; no camera/custody/building-origin or alteration authentication")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", type=Path)
    parser.add_argument("pins", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.sources, json.loads(args.pins.read_text())), indent=2))

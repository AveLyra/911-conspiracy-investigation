"""Compare the two pinned presentation copies, page by page."""
import argparse
import hashlib
import json
from pathlib import Path

import fitz
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("wpi_2005", type=Path)
parser.add_argument("mirror_2006", type=Path)
args = parser.parse_args()

pins = (
    (args.wpi_2005, "ff0723ddd1ba6fb341f23d80ea9a2f5bec45768019023cd35cf841301336ebb7"),
    (args.mirror_2006, "11dd136a5b4c9f205ae3289f792dcd2c5642d47a6fc3e20a95cf73366bc49e1b"),
)
documents = []
for path, expected in pins:
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"Unexpected SHA-256 for {path}")
    documents.append(fitz.open(stream=data, filetype="pdf"))

old, new = documents
if len(old) != len(new):
    raise ValueError("Page counts differ")

text_changes = []
geometry_changes = []
render_changes = []
for number, (first, second) in enumerate(zip(old, new, strict=True), 1):
    if first.get_text() != second.get_text():
        text_changes.append(number)
    if (first.rect, first.rotation) != (second.rect, second.rotation):
        geometry_changes.append(number)
    first_raster = first.get_pixmap(colorspace=fitz.csRGB, alpha=False)
    second_raster = second.get_pixmap(colorspace=fitz.csRGB, alpha=False)
    if (first_raster.width, first_raster.height) != (second_raster.width, second_raster.height):
        raise ValueError(f"Raster dimensions differ on page {number}")
    width, height = first_raster.width, first_raster.height
    rgb_first = np.frombuffer(first_raster.samples, dtype=np.uint8).reshape(height, width, 3)
    rgb_second = np.frombuffer(second_raster.samples, dtype=np.uint8).reshape(height, width, 3)
    differences = np.abs(rgb_first.astype(np.int16) - rgb_second).max(axis=2)
    first_images = first.get_image_info(hashes=True)
    second_images = second.get_image_info(hashes=True)
    image_changes = []
    for index, (before, after) in enumerate(zip(first_images, second_images, strict=True), 1):
        if before["digest"] != after["digest"]:
            image_changes.append({
                "image_occurrence": index,
                "before": [before["width"], before["height"], before["digest"].hex()],
                "after": [after["width"], after["height"], after["digest"].hex()],
            })
    if differences.any() or image_changes:
        render_changes.append({
            "page": number,
            "changed_pixels": int(np.count_nonzero(differences)),
            "total_pixels": int(differences.size),
            "pixels_differing_by_more_than_16": int(np.count_nonzero(differences > 16)),
            "images": image_changes,
        })

print(json.dumps({
    "pymupdf": fitz.__version__,
    "numpy": np.__version__,
    "pages": len(old),
    "title_slides": [doc[0].get_text().splitlines()[8] for doc in documents],
    "metadata": [doc.metadata for doc in documents],
    "text_changes": text_changes,
    "geometry_changes": geometry_changes,
    "render_changes": render_changes,
}, indent=2))

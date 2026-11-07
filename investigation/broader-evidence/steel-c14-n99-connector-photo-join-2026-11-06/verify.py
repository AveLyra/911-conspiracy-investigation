"""Compare three archive photographs with two fixed report-image regions.

Requires PyMuPDF, Pillow, NumPy and SciPy. Source images remain separate.
"""
import argparse
import hashlib
import json
from pathlib import Path

import fitz
import numpy as np
from PIL import Image
from scipy.signal import fftconvolve


def check(condition, label):
    if not condition:
        raise SystemExit(f"Failed: {label}")


def box_sums(pixels, height, width):
    summed = np.pad(pixels.cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    return summed[height:, width:] - summed[:-height, width:] - summed[height:, :-width] + summed[:-height, :-width]


def compare(target, source):
    height, width = target.shape
    target = target - target.mean()
    target_norm = np.linalg.norm(target)
    best = (-1.0,)
    for turns in range(4):
        rotated = source.rotate(90 * turns, expand=True)
        for scaled_width in range(width, 281, 2):
            scaled_height = round(scaled_width * rotated.height / rotated.width)
            if scaled_height < height:
                continue
            resized = rotated.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
            pixels = np.asarray(resized, dtype=np.float64)
            sums = box_sums(pixels, height, width)
            squares = box_sums(pixels**2, height, width)
            deviation = np.sqrt(np.maximum(squares - sums**2 / target.size, 1))
            score = fftconvolve(pixels, target[::-1, ::-1], mode="valid") / (target_norm * deviation)
            y, x = np.unravel_index(np.argmax(score), score.shape)
            candidate = (float(score[y, x]), 90 * turns, scaled_width, scaled_height, int(x), int(y))
            if candidate[0] > best[0]:
                best = candidate
    return best


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("report", type=Path)
parser.add_argument("photo", nargs=3, type=Path)
args = parser.parse_args()
ledger = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
for path, pin in zip([args.report, *args.photo], ledger["sources"], strict=True):
    data = path.read_bytes()
    check(len(data) == pin["bytes"], f"{pin['label']} bytes")
    check(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{pin['label']} SHA-256")

scores = {}
with fitz.open(args.report, filetype="pdf") as pdf:
    for locator in ledger["report_regions"]:
        page = pdf[locator["page"] - 1]
        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(0.45, 0.45),
            clip=fitz.Rect(*locator["bounds_points"]),
            colorspace=fitz.csGRAY,
            alpha=False,
        )
        target = np.asarray(Image.frombytes("L", (pixmap.width, pixmap.height), pixmap.samples), dtype=np.float64)
        for path, pin in zip(args.photo, ledger["sources"][1:], strict=True):
            with Image.open(path) as image:
                check(list(image.size) == pin["dimensions"], f"{pin['label']} pixel dimensions")
                result = compare(target, image.convert("L"))
                label = f"{locator['label']} / {pin['label']}"
                scores[label] = result[0]
                print(f"{label}: {result[0]:.4f}  rotation={result[1]}  scaled={result[2:4]}  offset={result[4:6]}")

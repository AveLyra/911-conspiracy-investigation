"""Inspect acquired archive JPEGs; preserve source bytes; OCR is a search aid.

Run after acquisition: python inspect_scans.py --source-dir ... --output-dir ...
Requires installed Pillow and tesseract. No network or historical authentication.
"""
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
from pathlib import Path

import PIL
from PIL import ExifTags, Image, ImageDraw, ImageOps


def inspect(path):
    raw = path.read_bytes()
    with Image.open(path) as im:
        exif = im.getexif()
        exif_data = {ExifTags.TAGS.get(k, str(k)): str(v) for k, v in exif.items()}
        try:
            nested = exif.get_ifd(ExifTags.IFD.Exif)
            exif_data["ExifIFD"] = {
                ExifTags.TAGS.get(k, str(k)): str(v) for k, v in nested.items()
            }
        except (KeyError, ValueError, TypeError):
            pass
        result = {
            "name": path.name,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "dimensions": list(im.size),
            "format": im.format,
            "exif": exif_data,
        }
    run = subprocess.run(
        ["tesseract", str(path), "stdout", "--psm", "11", "-l", "eng"],
        capture_output=True, text=True, timeout=60,
    )
    result.update(
        ocr_returncode=run.returncode, ocr_text=run.stdout, ocr_stderr=run.stderr,
        ocr_scope="One unrotated sparse-text pass, PSM11/eng. Not a reliable absence test.",
    )
    assert hashlib.sha256(path.read_bytes()).hexdigest() == result["sha256"]
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-dir", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()
    paths = sorted(args.source_dir.glob("WTC*.jpg"))
    assert {p.name for p in paths} == {f"WTC{n:03}.jpg" for n in range(1, 51)}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(inspect, paths))
    version = subprocess.run(["tesseract", "--version"], capture_output=True, text=True).stdout
    result = {
        "scope": "All 50 acquired WTC001-WTC050 archive scan entities, not all collected-steel images or all historical photos. Source files unchanged. No origin adjudication.",
        "pillow_version": PIL.__version__, "tesseract_version": version,
        "images": rows,
    }
    with (args.output_dir / "SCAN-INSPECTION.json").open("x") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    sheets = []
    for start in range(0, len(paths), 10):
        selected = paths[start:start + 10]
        sheet = Image.new("RGB", (1800, 5 * 350 + 50), "white")
        draw = ImageDraw.Draw(sheet)
        draw.text((12, 10), "DERIVED review contact sheet; not a source photograph", fill="black")
        for i, path in enumerate(selected):
            x, y = (i % 2) * 900, 50 + (i // 2) * 350
            with Image.open(path) as im:
                thumb = ImageOps.contain(im.convert("RGB"), (880, 315))
            sheet.paste(thumb, (x + 10, y + 25))
            draw.text((x + 12, y + 5), path.name, fill="black")
        target = args.output_dir / f"contact-{start + 1:03}-{start + len(selected):03}.jpg"
        sheet.save(target, quality=94)
        sheets.append({"name": target.name, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    with (args.output_dir / "CONTACT-SHEETS.json").open("x") as f:
        json.dump(sheets, f, indent=2)
        f.write("\n")
    print(json.dumps({"images": len(rows), "ocr_successes": sum(r["ocr_returncode"] == 0 for r in rows), "derived_contact_sheets": len(sheets)}))


if __name__ == "__main__":
    main()

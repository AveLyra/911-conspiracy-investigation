#!/usr/bin/env python3
"""Check acquired bytes, metadata and a bounded static catalog screen.
Does not authenticate camera originals, visual matches or historical custody.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
from PIL import Image
import pypdf

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--photo", type=Path, required=True)
ap.add_argument("--research-root", type=Path, help="Optional native research root for PDF and predecessor checks")
ap.add_argument("--render-root", type=Path, help="Resolve through media_path.py before supplying the verified render directory")
ap.add_argument("--manifest", type=Path, help="Previously pinned static bencoded catalog; no peer connections")
ap.add_argument("--catalog-reader", type=Path, help="Pinned existing inspect_release32.py")
args = ap.parse_args()
pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
def require(ok, label):
    if not ok:
        raise AssertionError(label)
def check_file(path, item, label):
    data = path.read_bytes()
    require(len(data) == item["bytes"], label + " length")
    require(hashlib.sha256(data).hexdigest() == item["sha256"], label + " SHA-256")
    return data

photo = check_file(args.photo, pins["photo"], "photo")
im = Image.open(args.photo)
im.load()
require(im.format == pins["photo"]["format"] == "JPEG", "JPEG format")
require(list(im.size) == pins["photo"]["size"] == [1280,960], "decoded pixel dimensions")
require(im.mode == pins["photo"]["mode"], "decoded mode")
exif = im.getexif()
keep = {271:"Make",272:"Model",306:"DateTime",36867:"DateTimeOriginal",
        36868:"DateTimeDigitized",274:"Orientation",40962:"PixelXDimension",40963:"PixelYDimension"}
actual = {keep[k]:str(v) for k,v in exif.items() if k in keep}
try:
    actual.update({keep[k]:str(v) for k,v in exif.get_ifd(34665).items() if k in keep})
except (KeyError,ValueError,TypeError):
    pass
require(actual == pins["photo"]["limited_exif"], "reproduce limited EXIF reading")
zero = b"0000:00:00 00:00:00"
offsets = [m.start() for m in re.finditer(re.escape(zero), photo)]
require(offsets == pins["photo"]["raw_zero_date_ASCII_offsets"], "independent raw zero-date byte locations")
require(pins["photo"]["bytes"] == pins["photo"]["declared_catalog_bytes"], "declared-vs-acquired length")
checks = {"photo_bytes_and_decode":"PASS", "limited_EXIF":actual,
          "raw_zero_date_ASCII_offsets":offsets}
if args.research_root:
    pages = {}
    for item in pins["reference_pdfs"]:
        path = args.research_root / item["relative_to_research_root"]
        check_file(path, item, "reference PDF")
        reader = pypdf.PdfReader(path)
        require(len(reader.pages) >= item["physical_page_read"], "selected reference page exists")
        pages[item["title"]] = {"total_pages":len(reader.pages), "selected_page":item["physical_page_read"]}
    for item in pins["protected_predecessors"]:
        check_file(args.research_root / item["relative_to_research_root"], item, "predecessor")
    checks["reference_PDFs"] = pages
    checks["protected_predecessors_unchanged"] = len(pins["protected_predecessors"])
else:
    checks["reference_PDFs_and_predecessors"] = "NOT TESTED: no native root supplied"
if args.render_root:
    for item in pins["reference_pdfs"]:
        check_file(args.render_root / item["render_file"],
            {"bytes":item["render_bytes"],"sha256":item["render_sha256"]}, "render")
    checks["selected_renders_preserved"] = len(pins["reference_pdfs"])
else:
    checks["selected_renders_preserved"] = "NOT TESTED: no verified render root supplied"
if args.manifest:
    require(args.catalog_reader is not None, "supply pinned catalog reader with manifest")
    data = check_file(args.manifest, pins["catalog"], "static catalog")
    check_file(args.catalog_reader, pins["existing_catalog_reader"], "catalog reader")
    spec = importlib.util.spec_from_file_location("pinned_static_catalog_reader", args.catalog_reader)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rows = mod.read_bencode(data)[b"info"][b"files"]
    require(len(rows) == pins["catalog"]["all_paths"], "catalog row count")
    extensions = set(pins["catalog"]["native_extensions"])
    native = []
    named = []
    for i,row in enumerate(rows):
        parts = [p.decode("utf-8", errors="replace") for p in row[b"path"]]
        path = "/".join(parts)
        item = {"catalog_index":i,"path":path,"declared_bytes":row[b"length"]}
        if Path(parts[-1]).suffix.lower() in extensions:
            native.append(item)
        if re.search(pins["catalog"]["filename_pattern"], parts[-1]):
            named.append(item)
    require(len(native) == pins["catalog"]["native_extension_matches"], "native-extension result")
    require(named == pins["catalog"]["filename_matches"], "exact filename-match result")
    hit = next(r for r in named if r["catalog_index"] == pins["photo"]["catalog_index"])
    require(hit["path"] == pins["photo"]["catalog_path"] and hit["declared_bytes"] == len(photo), "catalog-to-acquired-file locator")
    checks["static_catalog_screen"] = {"paths":len(rows),"native_extension_hits":len(native),"filename_hits":len(named)}
else:
    checks["static_catalog_screen"] = "NOT TESTED: manifest not supplied"
print(json.dumps({"status":"PASS","Pillow":Image.__version__,"pypdf":pypdf.__version__,
    "checks":checks,"limits":"Checks acquired representations only. Does not independently judge visual identity, authenticate building/floor/camera/date/custody, equate two copies with independent evidence, show metadata alteration, or complete any missing-original criterion."}, indent=2))

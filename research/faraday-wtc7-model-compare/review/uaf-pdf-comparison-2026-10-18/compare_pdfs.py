"""Read-only, fixed-protocol PDF comparison; all generated paths are create-only."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import fitz

SOURCES = [
    {"id": "march2020", "url": "https://files.wtc7report.org/file/public-download/A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March2020.pdf", "bytes": 45196602, "sha256": "f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa"},
    {"id": "march-2020", "url": "https://files.wtc7report.org/file/public-download/A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March-2020.pdf", "bytes": 45194303, "sha256": "41dd3390627fac24c2bd696160c48f15e05d3213cc05325c4e4e89608df96d27"},
]

def digest(b):
    return hashlib.sha256(b).hexdigest()

def filehash(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def write_json(p, value):
    with open(p, "x", encoding="utf-8") as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write("\n")

def write_text(p, value):
    with open(p, "x", encoding="utf-8") as f:
        f.write(value)

def utc():
    return datetime.now(timezone.utc).isoformat()

class HttpsRedirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 5
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not newurl.startswith("https://"):
            raise ValueError("Non-HTTPS redirect rejected")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def acquire_one(source, media):
    target = media / (source["id"] + ".pdf")
    receipt = {"source": source, "requested_at_utc": utc(), "output": str(target)}
    start = time.monotonic()
    try:
        opener = urllib.request.build_opener(HttpsRedirects())
        request = urllib.request.Request(source["url"], headers={"User-Agent": "Public-source-PDF-comparison/1.0", "Accept-Encoding": "identity"})
        with opener.open(request, timeout=30) as response, open(target, "xb") as f:
            receipt.update(status=response.status, final_url=response.url, headers={k: v for k, v in response.headers.items() if k.lower() in {"content-type", "content-length", "last-modified", "etag", "date", "content-encoding"}})
            count = 0
            while True:
                if time.monotonic() - start > 240:
                    raise TimeoutError("240-second acquisition limit")
                b = response.read(128 * 1024)
                if not b:
                    break
                count += len(b)
                if count > 64 * 1024 * 1024:
                    raise ValueError("64MiB limit")
                f.write(b)
        receipt["complete"] = True
    except Exception as e:
        receipt.update(complete=False, error=f"{type(e).__name__}: {e}")
    receipt["ended_at_utc"] = utc()
    if target.exists():
        receipt.update(acquired_bytes=target.stat().st_size, acquired_sha256=filehash(target))
    receipt["admitted_historical_source"] = receipt.get("complete", False) and receipt.get("acquired_bytes") == source["bytes"] and receipt.get("acquired_sha256") == source["sha256"]
    write_json(media / (source["id"] + "-acquisition.json"), receipt)
    return receipt

def page_record(page, dpi=150):
    text = page.get_text("text", sort=False)
    raw = text.encode("utf-8")
    normalized = " ".join(unicodedata.normalize("NFC", text).split()).encode("utf-8")
    pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB, alpha=False)
    result = {
        "page": page.number + 1,
        "geometry": {"rect": list(page.rect), "mediabox": list(page.mediabox), "cropbox": list(page.cropbox), "rotation": page.rotation},
        "raw_text": {"sha256": digest(raw), "bytes": len(raw), "empty": not bool(raw)},
        "normalized_text": {"sha256": digest(normalized), "bytes": len(normalized)},
        "raster": {"sha256": digest(pix.samples), "width": pix.width, "height": pix.height, "channels": pix.n, "dpi": dpi, "alpha": pix.alpha},
        "links": page.get_links(),
        "annotation_xrefs": list(page.annot_xrefs()),
        "widgets": [{"name": w.field_name, "type": w.field_type, "value": w.field_value} for w in (page.widgets() or [])],
    }
    return result, text, pix

def object_inventory(doc):
    inventory = []
    for xref in range(1, doc.xref_length()):
        obj = doc.xref_object(xref, compressed=False)
        record = {"xref": xref, "object_text_sha256": digest(obj.encode()), "object_text_bytes": len(obj.encode()), "is_stream": doc.xref_is_stream(xref)}
        if record["is_stream"]:
            raw, decoded = doc.xref_stream_raw(xref), doc.xref_stream(xref)
            record.update(raw_stream_sha256=digest(raw), raw_stream_bytes=len(raw), decoded_stream_sha256=digest(decoded), decoded_stream_bytes=len(decoded))
        inventory.append(record)
    return inventory

def doc_record(doc, path):
    return {
        "bytes": path.stat().st_size,
        "sha256": filehash(path),
        "header_hex": path.open("rb").read(16).hex(),
        "metadata": doc.metadata,
        "catalog_version": doc.xref_get_key(doc.pdf_catalog(), "Version"),
        "trailer": doc.pdf_trailer(),
        "xref_length": doc.xref_length(),
        "page_count": doc.page_count,
        "repaired": doc.is_repaired,
        "encrypted": doc.is_encrypted,
        "needs_password": doc.needs_pass,
        "embedded_files": doc.embfile_names(),
        "bookmarks": doc.get_toc(simple=False),
        "xml_metadata_sha256": digest(doc.get_xml_metadata().encode()),
        "xml_metadata_bytes": len(doc.get_xml_metadata().encode()),
    }

def compare(media, results, rasters=None):
    paths = [media / (s["id"] + ".pdf") for s in SOURCES]
    for source, path in zip(SOURCES, paths):
        if path.stat().st_size != source["bytes"] or filehash(path) != source["sha256"]:
            raise ValueError("Historical source admission failed; preserve bytes, stop comparison")
    results.mkdir(parents=True, exist_ok=False)
    if rasters is None:
        rasters = media
    else:
        rasters.mkdir(parents=True, exist_ok=False)
    before = [filehash(p) for p in paths]
    runtime = {"python": sys.version, "executable": sys.executable, "executable_sha256": filehash(sys.executable), "fitz_version": fitz.version, "fitz_module": fitz.__file__, "fitz_module_sha256": filehash(fitz.__file__), "native_modules": {str(p): filehash(p) for p in Path(fitz.__file__).parent.glob("*.so")}}
    write_json(results / "runtime.json", runtime)
    docs = [fitz.open(p) for p in paths]
    doc_records = [doc_record(d, p) for d, p in zip(docs, paths)]
    write_json(results / "documents.json", {s["id"]: r for s, r in zip(SOURCES, doc_records)})
    inventories = [object_inventory(d) for d in docs]
    write_json(results / "object-inventories.json", {s["id"]: r for s, r in zip(SOURCES, inventories)})
    object_diffs = []
    for i in range(max(map(len, inventories))):
        a = inventories[0][i] if i < len(inventories[0]) else None
        b = inventories[1][i] if i < len(inventories[1]) else None
        if a != b:
            xref = i + 1
            texts = [d.xref_object(xref, compressed=False) if xref < d.xref_length() else "<ABSENT>" for d in docs]
            object_diffs.append({"xref": xref, "march2020": a, "march-2020": b, "object_texts": texts, "object_text_diff": list(difflib.unified_diff(texts[0].splitlines(), texts[1].splitlines(), fromfile="march2020", tofile="march-2020", lineterm=""))})
    write_json(results / "object-differences.json", object_diffs)
    page_results, page_differences = [], []
    for i in range(max(d.page_count for d in docs)):
        rows, texts = [], []
        for source, doc in zip(SOURCES, docs):
            if i >= doc.page_count:
                rows.append({"page": i + 1, "error": "ABSENT"})
                texts.append("")
                continue
            try:
                row, text, pix = page_record(doc[i])
                rows.append(row)
                texts.append(text)
                # Preserve representative control page; changed pages saved below.
                if i == 0:
                    target = rasters / (source["id"] + "-page-001-150dpi.png")
                    with open(target, "xb") as f:
                        f.write(pix.tobytes("png"))
            except Exception as e:
                rows.append({"page": i + 1, "error": f"{type(e).__name__}: {e}"})
                texts.append("")
        pair = {"page": i + 1, "sources": dict(zip([s["id"] for s in SOURCES], rows))}
        pair["equal_channels"] = {k: not any("error" in r for r in rows) and rows[0][k] == rows[1][k] for k in ["geometry", "raw_text", "normalized_text", "raster", "links", "annotation_xrefs", "widgets"]}
        page_results.append(pair)
        if not all(pair["equal_channels"].values()):
            page_differences.append({"page": i + 1, "equal_channels": pair["equal_channels"], "text_diff": list(difflib.unified_diff(texts[0].splitlines(), texts[1].splitlines(), fromfile="march2020", tofile="march-2020", lineterm=""))})
            for source, doc in zip(SOURCES, docs):
                if i < doc.page_count and i != 0:
                    target = rasters / f"{source['id']}-page-{i+1:03d}-150dpi.png"
                    with open(target, "xb") as f:
                        f.write(doc[i].get_pixmap(dpi=150, colorspace=fitz.csRGB, alpha=False).tobytes("png"))
        if (i + 1) % 10 == 0:
            print(f"Compared {i+1} page pairs", flush=True)
    write_json(results / "pages.json", page_results)
    write_json(results / "page-differences.json", page_differences)
    # Aligned byte scan and equal prefix/suffix are not a shifted global edit alignment.
    byte_a, byte_b = [p.read_bytes() for p in paths]
    common = min(len(byte_a), len(byte_b))
    first = next((i for i in range(common) if byte_a[i] != byte_b[i]), common)
    suffix = 0
    while suffix < common - first and byte_a[-1-suffix] == byte_b[-1-suffix]:
        suffix += 1
    after = [filehash(p) for p in paths]
    if before != after:
        raise ValueError("Sources changed during comparison")
    summary = {"started_with_historical_hashes": before, "post_comparison_hashes": after, "page_counts": [d.page_count for d in docs], "differing_pages": [p["page"] for p in page_differences], "channel_difference_pages": {k: [p["page"] for p in page_results if not p["equal_channels"][k]] for k in page_results[0]["equal_channels"]}, "object_difference_xrefs": [r["xref"] for r in object_diffs], "byte_length_difference": len(byte_a)-len(byte_b), "identical_prefix_bytes": first, "identical_suffix_bytes": suffix, "completed_at_utc": utc(), "mupdf_warnings": fitz.TOOLS.mupdf_warnings(), "source_files_unchanged": before == after}
    write_json(results / "summary.json", summary)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["acquire", "compare"])
    parser.add_argument("--media", type=Path, required=True)
    parser.add_argument("--results", type=Path)
    parser.add_argument("--rasters", type=Path)
    args = parser.parse_args()
    if args.mode == "acquire":
        args.media.mkdir(parents=True, exist_ok=False)
        with ThreadPoolExecutor(max_workers=2) as pool:
            receipts = list(pool.map(lambda s: acquire_one(s, args.media), SOURCES))
        print(json.dumps(receipts, indent=2))
        if not all(r["admitted_historical_source"] for r in receipts):
            raise SystemExit(2)
    else:
        compare(args.media, args.results, args.rasters)

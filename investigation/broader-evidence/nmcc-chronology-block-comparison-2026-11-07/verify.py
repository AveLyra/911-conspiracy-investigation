#!/usr/bin/env python3
"""Verify preservation and the selected visible-label comparison, not historical events."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import re
import pypdf

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--source-pdf", type=Path, required=True)
ap.add_argument("--predecessor-root", type=Path)
ap.add_argument("--media-root", type=Path, help="Resolve through media_path.py before supplying the verified render directory")
args = ap.parse_args()
pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
def require(ok, message):
    if not ok:
        raise AssertionError(message)
def check_file(path, item, label):
    data = path.read_bytes()
    require(len(data) == item["bytes"], label + ": byte length")
    require(hashlib.sha256(data).hexdigest() == item["sha256"], label + ": SHA-256")
    return data

data = check_file(args.source_pdf, pins["source"], "source PDF")
require(data.startswith(b"%PDF-"), "PDF signature")
reader = pypdf.PdfReader(args.source_pdf)
require(len(reader.pages) == pins["source"]["physical_pages"], "physical page count")
require(pins["source"]["url"] == "https://www.archives.gov/files/declassification/iscap/pdf/2012-156-doc-14-part-2.pdf", "recorded source URL")
actual = {}
for page in [19,20,21,22]:
    text = reader.pages[page-1].extract_text() or ""
    actual[page] = re.findall(r"(?m)^\s*(\d{6}L)\s*$", text)
for saved in pins["fresh_extraction"]:
    require(actual[saved["physical_page"]] == saved["labels"], "reproduce saved page extraction")
a = actual[19] + actual[20]
b = actual[21] + actual[22]
rows = pins["manual_row_ledger"]
require(len(rows) == 16, "manual ledger size")
require(a == [r["manual_label_A"] for r in rows], "extraction vs independent visual ledger A")
require(b == [r["manual_label_B"] for r in rows], "extraction vs independent visual ledger B")
require([r["row"] for r in rows] == list(range(1,17)), "row order/coverage")
require([(r["physical_page_A"], r["physical_page_B"]) for r in rows] == [(19,21)]*10 + [(20,22)]*6, "physical-page mapping")
require(a == b, "ordered label equality in this comparison")
require(len(a) == 16 and len(set(a)) == 15, "row and distinct-label counts")
require({k:v for k,v in Counter(a).items() if v > 1} == {"111421L":2}, "preserve duplicate label")
require(rows[6]["subject_review_paraphrase"] != rows[7]["subject_review_paraphrase"], "duplicate labels retained as two separate subject rows")
require(pins["counts"]["ordered_sequences_equal"] and pins["counts"]["left_row_labels_per_block"] == [16,16], "published count consistency")
require([x["row"] for x in pins["visible_contrasts"]] == [2,7], "declared visual-contrast locators")
require(pins["full_images_read"] == [19,20,21,22], "declared image-reading scope")
checks = {"source_PDF_hash_and_page_count":"PASS", "selected_pages":4,
    "left_labels_per_block":[len(a),len(b)], "distinct_labels_per_block":[len(set(a)),len(set(b))],
    "ordered_labels_equal":a == b, "preserved_duplicate":{"111421L":2}}
if args.predecessor_root:
    for item in pins["protected_predecessors"]:
        check_file(args.predecessor_root / item["relative_to_research_root"], item, "predecessor")
    checks["protected_predecessor_files_unchanged"] = len(pins["protected_predecessors"])
else:
    checks["protected_predecessor_files_unchanged"] = "NOT TESTED: no root supplied"
if args.media_root:
    for item in pins["inspected_images"]:
        check_file(args.media_root / item["file"], item, "render")
    checks["inspected_render_entities_preserved"] = len(pins["inspected_images"])
else:
    checks["inspected_render_entities_preserved"] = "NOT TESTED: no verified root supplied"
print(json.dumps({"status":"PASS", "pypdf":pypdf.__version__, "checks":checks,
    "limits":"Reproduces selected label extraction and declared ledger consistency only. Does not independently read coverage, authenticate footer/native dates, recover hidden text, validate events or clocks, show directive implementation, prove missing-record disposition or complete the five-track goal."}, indent=2))

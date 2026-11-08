#!/usr/bin/env python3
"""Check source identity and cited anchors; not adjudication or lab validation."""
import argparse, hashlib, json, re
from pathlib import Path
from pypdf import PdfReader
ap=argparse.ArgumentParser()
ap.add_argument("--pdf", required=True, type=Path)
ap.add_argument("--predecessor", type=Path)
args=ap.parse_args()
pins=json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
s=pins["sources"][0]
b=args.pdf.read_bytes()
assert len(b)==s["bytes"]
assert hashlib.sha256(b).hexdigest()==s["sha256"]
r=PdfReader(args.pdf)
assert len(r.pages)==s["pdf_pages"]==206
p201=(r.pages[200].extract_text() or "").splitlines()
p202=(r.pages[201].extract_text() or "").splitlines()
joined=lambda lines: re.sub(r"\s+"," "," ".join(lines)).strip()
assert "MICHAEL NESTOR" in " ".join(p201[38:40])
x=joined(p202[46:52])
assert "also charged in this indictment" in x
y=joined(p202[52:56])
assert "plead guilty to both schemes" in y
assert "$100 per day" in y
assert "pending against the company" in y
assert "more than $104,000" in joined(p202[39:46])
assert "July 13, 2006" in (r.pages[81].extract_text() or "")
assert pins["sources"][1]["pdf_sha256"] is None
if args.predecessor:
 assert hashlib.sha256(args.predecessor.read_bytes()).hexdigest()==pins["predecessor"]["native_report_sha256"]
print(json.dumps({"source_identity":"matched","page_count":206,"cited_anchors":"matched","predecessor_unchanged":"checked" if args.predecessor else "not checked","court_outcome":"not verified","sample_or_NIST_join":"not verified"}))

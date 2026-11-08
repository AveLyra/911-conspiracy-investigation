#!/usr/bin/env python3
"""Verify a released-log copy and selected anchors, not FOIA outcomes."""
from pathlib import Path
import argparse,hashlib,json
from pypdf import PdfReader
ap=argparse.ArgumentParser()
ap.add_argument("--pdf",required=True,type=Path)
args=ap.parse_args()
pins=json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
s=pins["source"];b=args.pdf.read_bytes()
assert len(b)==s["bytes"]==17597187
assert hashlib.sha256(b).hexdigest()==s["sha256"]
r=PdfReader(args.pdf)
assert len(r.pages)==s["pdf_pages"]==354
t=lambda n:(r.pages[n-1].extract_text() or "")
assert "2008-480" in t(2)
assert "2007000252" in t(15)
assert "2007004527" in t(206)
assert "2007006096" in t(273)
assert "2007006970" in t(313)
assert "Flight 77" in t(313) and "Pentagon" in t(313)
assert "September 11, 2001 tapes" in t(273)
assert "9/11" in t(147)
assert "Closed" in t(206)
print(json.dumps({"source_hash":"matched","pages":354,"selected_text_anchors":"matched","manual_row_readings":"not tested by code","final_FOIA_responses":"not acquired","FAA_case_disposition":"not acquired","operational_media":"not acquired"}))

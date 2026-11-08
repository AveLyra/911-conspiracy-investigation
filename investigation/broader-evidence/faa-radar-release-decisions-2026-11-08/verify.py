#!/usr/bin/env python3
"""Check held source entities and text anchors; not legal/data outcomes."""
from pathlib import Path
import argparse,hashlib,json
from pypdf import PdfReader
ap=argparse.ArgumentParser()
ap.add_argument("--source-dir",required=True,type=Path)
args=ap.parse_args()
pins=json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
readers={}
for s in pins["sources"]:
 b=(args.source_dir/s["file"]).read_bytes()
 assert len(b)==s["bytes"]
 assert hashlib.sha256(b).hexdigest()==s["sha256"]
 r=PdfReader(args.source_dir/s["file"])
 assert len(r.pages)==s["pdf_pages"]
 readers[s["file"]]=r
def text(name,n):
 return readers[name].pages[n-1].extract_text() or ""
den="FAA-RadarDataDenials_2009-2010.pdf"
pol="FAA-ERIT-releases_2005-2010U.pdf"
memo="FAA-SensitiveRadar_2005.pdf"
assert "records destruction date" in text(den,2)
assert "five instances" in text(den,2)
assert "processed radar" in text(den,2)
assert "2009-006494" in text(den,7) and "CD-ROM" in text(den,7)
assert "2009-006996" in text(den,10) and "CD-ROM" in text(den,10)
assert "2010-004656" in text(pol,2)
assert "August 26, 2011" in text(pol,58)
assert "August 6, 2011" in text(pol,58)
assert "2011-8771" in text(memo,2)
print(json.dumps({"sources":3,"source_hashes":"matched","pdf_pages":[len(r.pages) for r in readers.values()],"selected_text_anchors":"matched","manual_page_readings":"not tested by code","retention_query_or_case_outcome":"not acquired","radar_payload_or_clock_validation":"not performed"}))

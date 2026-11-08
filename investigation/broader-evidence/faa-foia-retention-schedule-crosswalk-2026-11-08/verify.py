#!/usr/bin/env python3
"""Reproduce source anchors and hypothetical anniversaries, not disposal findings."""
from pathlib import Path
from datetime import date
import argparse,hashlib,json,re
from pypdf import PdfReader
ap=argparse.ArgumentParser()
ap.add_argument("--source-dir",required=True,type=Path)
args=ap.parse_args()
pins=json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
readers={}
for s in pins["sources"]:
 b=(args.source_dir/s["file"]).read_bytes()
 assert len(b)==s["bytes"] and hashlib.sha256(b).hexdigest()==s["sha256"]
 r=PdfReader(args.source_dir/s["file"])
 assert len(r.pages)==s["pdf_pages"]
 readers[s["file"]]=r
def flat(f,n):
 return re.sub(r"\s+","",readers[f].pages[n-1].extract_text() or "")
# These are text-anchor tests; table association was visually read separately.
assert "Destroy6yearsafterdateofreply." in flat("faa1350-chapter4.pdf",9)
assert "Destroy6yearsafterdateoflastentry." in flat("faa1350-chapter4.pdf",9)
assert "Destroy6yearsafterdateoflastentry." in flat("grs-transmittal7-1995.pdf",94)
assert "Destroy6yearsafterdateofreply." in flat("grs-index.pdf",80)
assert "Destroy5yearsafterdateoflastentry." in flat("grs-index.pdf",81)
assert "completeFOIAfile" in flat("held-faa8020-16a.pdf",47)
assert "outsidelabelofeachmedium" in flat("held-faa8020-16a.pdf",48)
results=[]
for x in pins["conditional_calendar"]["branches"]:
 anchor=date.fromisoformat(x["assumed_trigger_date"])
 assert not (anchor.month==2 and anchor.day==29), "Leap-day rule not specified for this bounded scenario."
 anniversary=anchor.replace(year=anchor.year+x["years"])
 ref=date.fromisoformat(x["reference_date"])
 assert anniversary.isoformat()==x["calendar_anniversary"]
 assert (anniversary<=ref)==x["anniversary_reached_at_reference"]
 results.append({"id":x["id"],"hypothetical_anniversary":anniversary.isoformat(),"reached_at_reference":anniversary<=ref})
print(json.dumps({"source_entities":len(readers),"source_hashes_and_anchors":"matched","conditional_scenarios":results,"actual_case_class_reply_hold_or_disposal":"not established","operative_version_or_legal_compliance":"not adjudicated","scientific_clock_validation":"not performed"}))

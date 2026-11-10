#!/usr/bin/env python3
"""Reproduce safe field accounting for an explicitly qualified released transcript.
Requires pypdf6.10.0. Read-only source/visible-OCR/raster inputs. No network,
hidden text extraction, speech output, OCR correction or clock/audio decoding.
Image-based agency/notation joins remain manual observations, not machine authentication.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,sys
import pypdf

def clock(label):
    if not re.fullmatch(r"\d{4}(?::\d{2})?",label):
        raise ValueError("Not a declared clock label")
    h=int(label[:2]);m=int(label[2:4]);s=int(label[5:]) if len(label)>4 else 0
    if h>23 or m>59 or s>59:raise ValueError("Invalid clock label")
    return 3600*h+60*m+s

def account(rows,markers):
    times=Counter(x["printed_time"] for x in rows)
    return {
        "timed_rows":len(rows),
        "unique_second_labels":len(times),
        "timed_rows_by_physical_page":dict(Counter(str(x["physical_page"]) for x in rows)),
        "manual_image_agency_counts":dict(Counter(x["manual_image_agency_code"] for x in rows)),
        "repeated_second_labels":{t:{"rows":n,"manual_agency_codes":[x["manual_image_agency_code"] for x in rows if x["printed_time"]==t]} for t,n in times.items() if n>1},
        "minute_markers":len(markers),
        "first_last_timed_row_labels":[rows[0]["printed_time"],rows[-1]["printed_time"]],
        "nominal_header_span_seconds":clock("1316")-clock("1255"),
        "nominal_first_to_last_timed_row_seconds":clock(rows[-1]["printed_time"])-clock(rows[0]["printed_time"]),
        "nominal_header_start_to_first_row_seconds":clock(rows[0]["printed_time"])-clock("1255"),
        "nominal_last_row_to_header_end_seconds":clock("1316")-clock(rows[-1]["printed_time"]),
        "limits":"Label arithmetic and visible-row accounting only. Not measured audio duration, silence, erased material, independent clocks, call counts, speakers or accurate speech."
    }

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf",type=Path,required=True)
    ap.add_argument("--prior-media",type=Path,required=True)
    ap.add_argument("--new-media",type=Path,required=True)
    a=ap.parse_args();root=Path(__file__).resolve().parent
    pins=json.loads((root/"SOURCE-PINS.json").read_text())
    ledger=json.loads((root/"FIELD-LEDGER.json").read_text())
    checks=[]
    def check(name,passed):checks.append({"check":name,"passed":bool(passed)})
    raw=a.pdf.read_bytes();source=pins["source"]
    check("Pinned released PDF bytes/hash/page count",len(raw)==source["bytes"] and hashlib.sha256(raw).hexdigest()==source["sha256"] and len(pypdf.PdfReader(a.pdf).pages)==237)
    texts={};parsed=[];minute_rows=[]
    for p in pins["selected_page_pins"]:
        page=p["physical_page"];media=a.new_media if p["newly_rendered_and_read"] else a.prior_media
        data=(media/"visible-ocr"/("AEA1130-p"+str(page)+".txt")).read_bytes()
        image=(media/"renders"/("AEA1130-p"+str(page)+".png")).read_bytes()
        lines=data.decode().splitlines();texts[page]=lines
        check("Physical"+str(page)+" unchanged OCR/raster hashes and line count",hashlib.sha256(data).hexdigest()==p["visible_ocr_sha256"] and hashlib.sha256(image).hexdigest()==p["raster_sha256"] and len(lines)==p["ocr_lines"])
        actual=[]
        for i,line in enumerate(lines,1):
            if m:=re.match(r"^\s*(\d{4}:\d{2})(?:\s|$)",line):
                actual.append({"physical_page":page,"time_ocr_line":i,"printed_time":m[1]})
            elif m:=re.fullmatch(r"\s*(\d{4})\s*",line):
                minute_rows.append({"physical_page":page,"ocr_line":i,"minute":m[1]})
        expected=[{k:x[k] for k in ["physical_page","time_ocr_line","printed_time"]} for x in ledger["rows"] if x["physical_page"]==page]
        check("Physical"+str(page)+" exact ordered timestamp/line ledger, repeated rows retained",actual==expected)
        parsed+=actual
    check("Two new images plus three reused/reread, whole package not asserted read",pins["new_images_read"]==[188,189] and pins["reused_images_reread"]==[186,187,190] and pins["cumulative_unread"]==219)
    check("All minute marker rows and locators reproduced",minute_rows==ledger["minute_markers"])
    expected_minutes=[f"{m//60:02d}{m%60:02d}" for m in range(12*60+55,13*60+16+1)]
    check("Twenty-two separate cardinal-minute labels1255through1316", [x["minute"] for x in minute_rows]==expected_minutes)
    check("Forty-eight rows with nondecreasing valid second labels, not deduplicated",len(parsed)==48 and all(clock(y["printed_time"])>=clock(x["printed_time"]) for x,y in zip(parsed,parsed[1:])))
    check("One marked parenthetical structure at preserved physical188/OCR58",texts[188][57].lstrip().startswith("*(") and texts[188][57].rstrip().endswith(")"))
    check("Separate unintelligible notation anchors physical188/OCR50,60",all("unintelligible" in texts[188][i-1].lower() for i in [50,60]))
    check("Uncertainty footer and end label locators retained", "*" in texts[190][33] and "interpretation" in texts[190][34] and "End of Transcript" in texts[190][36])
    stats=account(ledger["rows"],minute_rows)
    check("Manual-row aggregate matches page totals; attribution remains image-based",stats["timed_rows_by_physical_page"]=={"186":1,"187":15,"188":14,"189":13,"190":5})
    check("Three repeated second labels remain two separately labelled rows each",stats["unique_second_labels"]==45 and sorted(stats["repeated_second_labels"])==["1301:07","1303:39","1303:40"] and all(x["rows"]==2 for x in stats["repeated_second_labels"].values()))
    check("Nominal1260second label span partitions341+573+346 only as arithmetic",stats["nominal_header_span_seconds"]==1260 and stats["nominal_header_start_to_first_row_seconds"]==341 and stats["nominal_first_to_last_timed_row_seconds"]==573 and stats["nominal_last_row_to_header_end_seconds"]==346)
    # Controls concern field-ledger integrity, not the historical underlying event.
    altered=bytearray(raw);altered[len(altered)//2]^=1
    check("One-byte mutated source fails identity",hashlib.sha256(altered).hexdigest()!=source["sha256"])
    check("Dropped final row changes frozen row accounting",account(ledger["rows"][:-1],minute_rows)!=stats)
    check("Deduplicating equal timestamps changes frozen row accounting",len(set(x["printed_time"] for x in ledger["rows"]))!=stats["timed_rows"])
    result={"runtime":{"python":sys.version.split()[0],"pypdf":pypdf.__version__},"checks":checks,"passed":sum(x["passed"] for x in checks),"failed":sum(not x["passed"] for x in checks),"accounting":stats,"prior_OCR_anchor_failures":"Earlier32pass/4fail result is preserved unchanged and not rerun or repaired by these different timestamp-ledger checks. No glyph normalization.","manual_limits":"Agency/notation row joins and printed-page readings remain explicit manual image observations, not machine-authenticated voices, event accuracy, original clocks, delivered copy, native lineage or compliance."}
    print(json.dumps(result,indent=2));return int(result["failed"]>0)
if __name__=="__main__":sys.exit(main())

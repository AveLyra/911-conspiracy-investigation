#!/usr/bin/env python3
"""Reproduce a fixed released-source/form crosswalk without clock fitting.
Requires pypdf6.10.0, preserved source PDF and pinned rasters/visible OCR.
Handwriting, candidate role/event joins, blank-grid readings and pagination
remain manual observations. No text-layer/redaction recovery or roster output.
"""
from pathlib import Path
import argparse,json,hashlib,re,sys
import pypdf

def minutes(s):
    if not re.fullmatch(r"\d{4}",s) or int(s[:2])>23 or int(s[2:])>59:
        raise ValueError("Invalid nominal clock label")
    return int(s[:2])*60+int(s[2:])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf",type=Path,required=True)
    ap.add_argument("--media-root",type=Path,required=True)
    a=ap.parse_args();root=Path(__file__).resolve().parent
    p=json.loads((root/"SOURCE-PINS.json").read_text())
    cross=json.loads((root/"FORM-CROSSWALK.json").read_text())
    checks=[];texts={}
    def check(label,ok):checks.append({"check":label,"passed":bool(ok)})
    data=a.pdf.read_bytes();s=p["source"]
    check("Exact held PDF SHA256/bytes/page count",hashlib.sha256(data).hexdigest()==s["sha256"] and len(data)==s["bytes"] and len(pypdf.PdfReader(a.pdf).pages)==237)
    for x in p["selected_page_pins"]:
        page=x["physical_page"];b=(a.media_root/"renders"/("AEA1130-p"+str(page)+".png")).read_bytes()
        ok=hashlib.sha256(b).hexdigest()==x["raster_sha256"]
        if x["OCR_performed"]:
            b=(a.media_root/"visible-ocr"/("AEA1130-p"+str(page)+".txt")).read_bytes();lines=b.decode().splitlines();texts[page]=lines
            ok=ok and hashlib.sha256(b).hexdigest()==x["visible_ocr_sha256"] and len(lines)==x["ocr_lines"]
        check("Physical"+str(page)+" unchanged raster and performed-OCR pins",ok)
    anchors=[
      (16,3,7,["CERTIFIED INDEX","September 19, 2001","originals are on file in this office"]),
      (21,1,2,["Section 4","FAA Form 7230-4","Daily Record of Facility Operation"]),
      (22,4,55,["Daily Record of Facility Operation","FAA Form 7230-4"]),
      (23,6,61,["Daily Record of Facility Operation","FAA Form 7230-4"]),
      (24,1,2,["Section 5","Personnel Logs"]),
      (32,5,22,["SIGN IN / SIGN OUT CORRECTION FORM","ZNY Form 7210-5"]),
      (22,35,39,["1238","1250","1304","INFORMED OF ANOTHER POSSIBLE HIJACK UAL175","ADVISED SECOND AIRCRAFT CRASHED INTO WORLD TRADE CENTER"]),
      (22,14,31,["COMPUTER PROBLEMS","QCF RADAR OTS 1400-1600Z","LHY VOR OTS"])
    ]
    for page,lo,hi,parts in anchors:
        text=" ".join(texts[page][lo-1:hi])
        check("Physical"+str(page)+" selected safe anchors"+str(lo)+"-"+str(hi),all(t in text for t in parts))
    pairrow=next(x for x in cross["rows"] if x["id"]=="OF05");diffs=[]
    for x in pairrow["candidate_pairs"]:
        actual=texts[x["daily_page"]][x["daily_ocr_line"]-1]
        check("Daily candidate label atphysical"+str(x["daily_page"])+"/OCR"+str(x["daily_ocr_line"]),bool(re.match(r"^\s*"+re.escape(x["daily_label"])+r"\b",actual)))
        diffs.append(minutes(x["daily_label"])-minutes(x["cert_label"]))
    check("Three nominal manual-candidate label differences equal240minutes",diffs==[240,240,240])
    check("Declared sixteen-image cap and six OCR inputs honored",len(p["actual_images_read"])==16 and len(p["selected_page_pins"])==16 and len(texts)==6 and p["cap_exhausted"])
    check("Only34knownpacketimages in these studies,203notexamined",len(p["cumulative_known_packet_images_across_these_studies"])==34 and p["pages_not_examined_in_these_studies"]==203)
    manual=next(x for x in cross["rows"] if x["id"]=="OF04")["observation"]
    check("Both different manualTimeOfflabels preserved without selection",manual["personnel_log_labels"]==["0632","1432"] and manual["OSIC_CIC_certification_labels"]==["0632","0810"])
    mutated=bytearray(data);mutated[len(mutated)//2]^=1
    check("One-byte changed source fails identity",hashlib.sha256(mutated).hexdigest()!=s["sha256"])
    result={"runtime":{"python":sys.version.split()[0],"pypdf":pypdf.__version__},"checks":checks,"passed":sum(x["passed"] for x in checks),"failed":sum(not x["passed"] for x in checks),"nominal_candidate_label_differences_minutes":diffs,"scope":"Fixed entity/derivative identity, selected typed anchors and conditional arithmetic. No actual clock-offset fit, conversion, audio/radar test or individual roster output.","manual_and_historical_limits":"Source handwriting/role joins, form meanings, pagination, blank-grid observation and footer/representation warning remain manually qualified. No controlling time/account, actual duty boundaries, native version/edit/signing/delivery, requirement compliance, preservation, clock basis or intent established."}
    print(json.dumps(result,indent=2));return int(result["failed"]>0)
if __name__=="__main__":sys.exit(main())

#!/usr/bin/env python3
"""Verify three released source entities and selected safe receipt/review fields.
Requires pypdf6.10.0 and the separately pinned visible-raster OCR/images.
No network, hidden text extraction, redaction/identifier recovery or native-email
authentication. Airbill fields and annex numbered-item grouping remain manual.
"""
from pathlib import Path
import argparse,hashlib,json,re,sys
import pypdf

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--media-root",type=Path,required=True)
    a=ap.parse_args();root=Path(__file__).resolve().parent
    pins=json.loads((root/"SOURCE-PINS.json").read_text())
    ledger=json.loads((root/"RECEIPT-LEDGER.json").read_text())
    checks=[];texts={};entities={}
    def check(name,ok):checks.append({"check":name,"passed":bool(ok)})
    for src in pins["sources"]:
        path=a.media_root/"sources"/(src["id"]+".pdf");b=path.read_bytes();entities[src["id"]]=b
        check(src["id"]+" exact PDF bytes/hash/page count",len(b)==src["bytes"] and hashlib.sha256(b).hexdigest()==src["sha256"] and len(pypdf.PdfReader(path).pages)==src["physical_pages"])
    for x in pins["selected_page_pins"]:
        ident=x["source"]+"-p"+str(x["physical_page"])
        png=(a.media_root/"renders"/(ident+".png")).read_bytes()
        ok=hashlib.sha256(png).hexdigest()==x["raster_sha256"]
        if x["OCR_performed"]:
            b=(a.media_root/"visible-ocr"/(ident+".txt")).read_bytes();lines=b.decode().splitlines();texts[(x["source"],x["physical_page"])]=lines
            ok=ok and hashlib.sha256(b).hexdigest()==x["visible_ocr_sha256"] and len(lines)==x["ocr_lines"]
        check(ident+" raster and performed-OCR hashes/line count",ok)
    anchors=[
    ("AEA1128",1,1,1,["11/15/2001 7:46 AM"]),
    ("AEA1128",1,12,19,["We have received the accident package","UAL175","ZNY-ARTCC-148"]),
    ("AEA1129",1,1,1,["2/1/2002 8:39 AM"]),
    ("AEA1129",1,14,17,["We received the corrections","However, please have the facility make the changes","attached"]),
    ("AEA1129",1,25,32,["12/18/2001 8:57 AM","January 4, 2002"]),
    ("AEA1129",1,41,50,["11/15/2001 7:46 AM","We have received the accident package","ZNY-ARTCC-148"]),
    ("AEA1129",1,54,55,["UAL175 Change 2.doc"]),
    ("AEA1129",2,5,34,["SECTION 6: POSITION LOG","3600.1","7230","Military Operations Specialist","Departure Director","Traffic Management Coordinator"]),
    ("AEA1129",4,22,23,["Employee did not sign on Personnel Log","not required to sign on automated sign-in/sign-out log"]),
    ("AEA1129",4,28,29,["FAA Form 7230-4"]),
    ("AEA1129",4,34,34,["Sign-on log does not exist for this position"]),
    ("AEA1129",4,39,44,["TMU log; log not available"])]
    for src,page,lo,hi,needles in anchors:
        body=" ".join(texts[(src,page)][lo-1:hi])
        check(src+" physical"+str(page)+" selected safe anchors "+str(lo)+"-"+str(hi),all(s in body for s in needles))
    annex=[line for p in [2,3,4] for line in texts[("AEA1129",p)]]
    response_counts={phrase:sum(len(re.findall(re.escape(phrase),line,re.I)) for line in annex) for phrase in ["Correction made","No Correction required","Legend is correct"]}
    check("Three response phrase counts reproduced without treating them as implementation",response_counts=={"Correction made":23,"No Correction required":1,"Legend is correct":1})
    unavailable=sum("Position log information not available" in line for line in texts[("AEA1129",2)])
    check("Three Section6 unavailable-response phrases, not independent missing events",unavailable==3)
    tmumissing=sum("TMU log; log not available" in line for line in texts[("AEA1129",4)])
    check("Two Section11 TMU-unavailability responses remain distinct from no-log assertion",tmumissing==2)
    check("Forwarded receipt date/case match standalone receipt's selected fields",texts[("AEA1128",1)][0].strip()==texts[("AEA1129",1)][40].strip() and "ZNY-ARTCC-148" in texts[("AEA1128",1)][16] and "ZNY-ARTCC-148" in texts[("AEA1129",1)][47])
    manual=next(x for x in ledger["rows"] if x["id"]=="SR08")["observation"]
    groups=manual["annex_manual_numbered_counts"]
    check("Manual annex group-accounting only:5+24+6=35",groups["position_log"]==5 and sum(groups["transcripts"].values())==24 and groups["personnel_statements"]==6 and manual["total_manual_numbered_entries"]==35)
    check("All six released-source pages actually image-read; airbill OCR intentionally absent",pins["all_six_images_read"] and len(pins["selected_page_pins"])==6 and sum(x["OCR_performed"] for x in pins["selected_page_pins"])==5)
    sample=bytearray(entities["AEA1129"]);sample[len(sample)//2]^=1
    check("One-byte changed receipt source fails identity",hashlib.sha256(sample).hexdigest()!=next(x["sha256"] for x in pins["sources"] if x["id"]=="AEA1129"))
    check("Three distinct source entities do not imply three independent receipts",len(set(hashlib.sha256(b).hexdigest() for b in entities.values()))==3)
    output={"runtime":{"python":sys.version.split()[0],"pypdf":pypdf.__version__},"checks":checks,"passed":sum(x["passed"] for x in checks),"failed":sum(not x["passed"] for x in checks),"safe_response_phrase_counts":response_counts,"manual_numbered_item_counts":groups,"limits":"Source/derivative identity and selected safe fields only; manual role joins, airbill date/service options, second attachment label and annex number grouping remain image observations. No native headers/attachments, actual pickup/delivery, exact contents/version, final acceptance, deadline compliance, missing-log cause, lawful disposition or intent established. Repeated forwarded receipt is not independent corroboration."}
    print(json.dumps(output,indent=2));return int(output["failed"]>0)
if __name__=="__main__":sys.exit(main())

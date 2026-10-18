"""Scoped source inventory and complete-page review derivatives; create-only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile
import fitz
from geometry_check import conditional_geometry

ROOT=Path(__file__).parent
MEDIA=Path(sys.argv[1])
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1048576),b""):h.update(chunk)
    return h.hexdigest()
def save(path,obj):
    with path.open("x") as f:json.dump(obj,f,indent=2);f.write("\n")
def inventory(repo,pathspec):
    cmd=["git","ls-tree","-r","--name-only","HEAD","--",*pathspec]
    paths=subprocess.check_output(cmd,cwd=repo,text=True).splitlines()
    suffixes={".cae",".inp",".odb",".sdb",".s2k",".sdbk",".s$k",".cdb"}
    candidates=[p for p in paths if Path(p).suffix.lower() in suffixes]
    return {"repo":str(repo),"head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=repo,text=True).strip(),"command":cmd,"indexed_paths":len(paths),"path_listing_sha256":hashlib.sha256(("\n".join(paths)+"\n").encode()).hexdigest(),"native_suffixes":sorted(suffixes),"candidate_paths":candidates,"limits":"Tracked paths at this commit only; untracked inputs, archives and other disks not exhaustively searched. Names are not content authentication."}

save(ROOT/"native-availability.json",{"inventories":[inventory(Path("/Users/admin/docs/911-worktrees/public-inclusive-lead-review-2026-10-15"),[]),inventory(Path("/Users/admin/docs/911"),["research"])],"no_new_archive_route":"Previously rejected aggregate UAF dataset routes were not reopened"})
wrapper=Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/model-access-audit/sources/uaf-direct-download.zip")
if sha(wrapper)!="9f5ed822b4f5b28efef1051d731eb64d27547ef44903c897fe946c806267f25d":
    raise ValueError("The held wrapper changed; do not assume its old contents")
with zipfile.ZipFile(wrapper) as z:
    members=[{"name":i.filename,"bytes":i.file_size,"compressed_bytes":i.compress_size,"crc32":f"{i.CRC:08x}"} for i in z.infolist()]
    hashes={i.filename:hashlib.sha256(z.read(i)).hexdigest() for i in z.infolist()}
    if len(members)!=1 or members[0]["name"]!="readme.txt" or hashes["readme.txt"]!="96a368fccb099aee2ee95a1a0c6fb83cdf02560077a6b9eebc864041293c0e4f":
        raise ValueError("Unexpected wrapper member; stop classification")
save(ROOT/"wrapper-check.json",{"bytes":wrapper.stat().st_size,"sha256":sha(wrapper),"members":members,"decompressed_member_hashes":hashes,"full_readme_not_republished":True,"native_model_payload":False})
save(ROOT/"conditional-geometry.json",conditional_geometry())

sources={
 "uaf-final":{"path":Path("/Volumes/dev_src_case_sensitive/911-PROJECT/active-media/working-tree/research/911-conspiracy-investigation-public/investigation/wtc7/uaf-pdf-comparison-2026-10-18/sources/march2020.pdf"),"expected":"f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa","pages":[63,65,66,67,68,69,71,88,89,90,91,92,93,94]},
 "nist-ncstar-1-9":{"path":Path("/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf"),"expected":"30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f","pages":[392,393,394,395,396,397,398,548,549]},
 "frankel-9114-public-copy":{"path":MEDIA/"frankel-9114-public-copy.pdf","expected":"c02608a6b90c11b7d06a8d6d515fe3d264cebe0f92babd5183c9a0527030caf6","pages":[]},
 "frankel-1091-public-copy":{"path":MEDIA/"frankel-1091-public-copy.pdf","expected":"640cad6a983a269c77f52ae72224365ed2b4d1c6c90fb7959c2d0865c3a4c343","pages":[]}
}
records={}
for label,s in sources.items():
    before=sha(s["path"])
    if before!=s["expected"]:raise ValueError("Input changed: "+label)
    d=fitz.open(s["path"])
    rows=[]
    for number in s["pages"]:
        page=d[number-1];text=page.get_text();pix=page.get_pixmap(dpi=110,colorspace=fitz.csRGB,alpha=False)
        target=MEDIA/f"{label}-physical-{number:03d}-review.png"
        with target.open("xb") as f:f.write(pix.tobytes("png"))
        rows.append({"physical_page":number,"text_sha256":hashlib.sha256(text.encode()).hexdigest(),"raster_path":str(target),"raster_sha256":sha(target),"raster_dpi":110})
    after=sha(s["path"])
    if after!=before:raise ValueError("Input changed during read")
    records[label]={"path":str(s["path"]),"bytes":s["path"].stat().st_size,"sha256_before":before,"sha256_after":after,"pages":len(d),"repaired":d.is_repaired,"review_renders":rows}
save(ROOT/"source-review-records.json",records)
print(json.dumps({"sources_unchanged":True,"sources":list(records),"review_page_renders":sum(len(r["review_renders"]) for r in records.values()),"conditional_geometry":conditional_geometry()},indent=2))

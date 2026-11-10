"""Check exact acquired AWA940bytes and selected visible fields, not history.
No network or modifications; no audio/clock/native authentication. Requires
pypdf. Usage: python3 verify_original.py --source /path/to/source.pdf
"""
import argparse, hashlib, json, re
from pathlib import Path
import pypdf

PIN = "97baabe1e23b268da2c9e02d6510b7c19bd65234e22f3e1cb8b1bdeb210fe530"

def verify(path):
    body = path.read_bytes()
    if len(body) != 31742 or hashlib.sha256(body).hexdigest() != PIN:
        raise ValueError("Different entity: preserve separately, not silent repinning")
    pdf = pypdf.PdfReader(path)
    if len(pdf.pages) != 2:
        raise ValueError("Different page count")
    text = [p.extract_text() or "" for p in pdf.pages]
    checks = {"Full_subject": "Full Transcript" in text[0], "UAL175_subject": "UAL175" in text[0],
              "OMIC_position": "Operations Manager In Charge (OMIC)" in text[0],
              "case_file": "ZNY-ARTCC-148" in text[0], "printed_date": "February 4, 2002" in text[0],
              "declared_start": "1230 UTC" in text[0], "declared_end": "1344 UTC" in text[0],
              "work_file": "UAL175_MEMO.doc" in text[1], "footer_date": "09/25/2001" in text[1],
              "placeholder_both_pages": all("Pagination" in t and "Masthead" in t for t in text),
              "CC_NOM_legend": "CC-NOM" in text[0], "Huntress_legend": "Huntress" in text[0]}
    if not all(checks.values()):
        raise ValueError("A selected field did not reproduce; inspect source without normalizing")
    stamps = [re.findall(r"\b(?:[01]\d|2[0-3])[0-5]\d:[0-5]\d\b", t) for t in text]
    if stamps != [[], []]:
        raise ValueError("Source time-code extraction changed; preserve and inspect")
    info = pdf.metadata or {}
    return {"sha256": PIN, "bytes": len(body), "pages": 2, "pypdf": pypdf.__version__,
            "selected_visible_checks": checks, "timecoded_dialogue_matches": stamps,
            "embedded_attachment_names_count": len(list(pdf.attachments.keys())),
            "filtered_metadata": {k: info.get(k) for k in ["/Creator", "/Producer", "/CreationDate", "/ModDate"]},
            "limits": "Selected source/byte checks only; both images read separately; no native/clock/complete recording/enclosure identity or causal authentication"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    print(json.dumps(verify(ap.parse_args().source), indent=2))

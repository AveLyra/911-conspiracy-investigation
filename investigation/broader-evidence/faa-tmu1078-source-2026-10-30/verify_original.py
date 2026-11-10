"""Check the exact locally supplied released PDF and selected visible fields.
No network, modification, hidden-text reconstruction, speech export, audio or
clock inference. Requires pypdf. Usage: python3 verify_original.py --source FILE
"""
import argparse, hashlib, json, re
from pathlib import Path
import pypdf

EXPECTED = "a10386e4e39d455c7438328eca88bb28a76b7aea5c33282b4537779924851432"

def verify(path):
    body = path.read_bytes()
    if len(body) != 27138 or hashlib.sha256(body).hexdigest() != EXPECTED:
        raise ValueError("Different source bytes: preserve separately; do not silently replace the pin")
    pdf = pypdf.PdfReader(path)
    if len(pdf.pages) != 2:
        raise ValueError("Unexpected source page count")
    pages = [p.extract_text() or "" for p in pdf.pages]
    anchors = {"Full_subject": "Full Transcript" in pages[0], "subject_AAL11": "AAL11" in pages[0],
               "printed_memo_date": "January 17, 2002" in pages[0],
               "declared_start": "1255" in pages[0], "declared_end": "1316" in pages[0],
               "line_1078": '"1078"' in pages[0], "work_file": "UAL175_R42_memo.doc" in pages[1],
               "footer_date_token": "09/27/2001" in pages[1],
               "visible_placeholder": "Pagination" in pages[0] and "Masthead" in pages[0]}
    if not all(anchors.values()):
        raise ValueError("Selected field not reproduced; inspect image without normalizing a value")
    stamps = [re.findall(r"\b(?:[01]\d|2[0-3])[0-5]\d:[0-5]\d\b", t) for t in pages]
    if stamps != [["1300:41"], []]:
        raise ValueError("Time-stamp extraction differs; preserve and inspect")
    info = pdf.metadata or {}
    return {"source_sha256": EXPECTED, "bytes": len(body), "pages": 2, "pypdf": pypdf.__version__,
            "selected_field_checks": anchors, "visible_transcription_time_stamps": stamps,
            "enumerated_embedded_attachments": len(list(pdf.attachments.keys())),
            "filtered_PDF_metadata": {k: info.get(k) for k in ["/Creator", "/Producer", "/CreationDate", "/ModDate"]},
            "limits": "Selected visible-field/byte checks; not native authorship, complete underlying transcript/audio, exact enclosure/channel, receiver, media clock or historical cause"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    print(json.dumps(verify(ap.parse_args().source), indent=2))

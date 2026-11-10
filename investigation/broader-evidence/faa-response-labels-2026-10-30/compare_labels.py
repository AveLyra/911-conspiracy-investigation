"""Reproduce printed-label arithmetic and optionally identify the source PDF.
No network, source modification, audio decoding or clock authentication.
Usage: python3 compare_labels.py [--source /path/to/source.pdf]
Source identity/page/structural checks require pypdf; arithmetic uses stdlib only.
"""
import argparse, hashlib, json
from pathlib import Path

def minutes(value):
    if len(value) != 4 or not value.isdigit():
        raise ValueError("Expected the preserved same-day HHMM label")
    h, m = int(value[:2]), int(value[2:])
    if h > 23 or m > 59:
        raise ValueError("Invalid same-day HHMM label; preserve and investigate")
    return 60 * h + m

def compare(root, source=None):
    ledger_path = root / "OBSERVED-LABELS.json"
    ledger = json.loads(ledger_path.read_text())
    rows = []
    for row in ledger["rows"]:
        rec_ends = [minutes(x["end"]) for x in row["rerecording_labels"]]
        trans_end = minutes(row["transcript_label"]["end"])
        rows.append({"id": row["id"], "rerecording_ranges": [[x["start"], x["end"]] for x in row["rerecording_labels"]],
                     "transcript_range": [row["transcript_label"]["start"], row["transcript_label"]["end"]],
                     "transcript_end_minus_last_listed_rerecording_end_minutes": trans_end - max(rec_ends)})
    result = {"observed_labels_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
              "conditional_pairing": ledger["pairing_limit"], "arithmetic": rows,
              "limits": "Listed same-day HHMM end-label subtraction only; not actual media duration/gap, unique channel mapping, native clock, receipt, completeness or historical cause"}
    if source is not None:
        import pypdf
        body = source.read_bytes()
        if len(body) != 4592330 or hashlib.sha256(body).hexdigest() != ledger["source_sha256"]:
            raise ValueError("Different source bytes: preserve the differing entity; do not silently replace the pin")
        pdf = pypdf.PdfReader(source)
        if len(pdf.pages) != 26:
            raise ValueError("Unexpected page count")
        result["source_check"] = {"sha256": ledger["source_sha256"], "bytes": len(body), "pages": len(pdf.pages),
                                  "pypdf": pypdf.__version__, "extractable_text_characters": [len(x.extract_text() or "") for x in pdf.pages],
                                  "enumerated_embedded_attachment_count": len(list(pdf.attachments.keys()))}
    return result

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path)
    args = ap.parse_args()
    print(json.dumps(compare(Path(__file__).parent, args.source), indent=2))

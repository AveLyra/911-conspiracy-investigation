"""Reproduce representations separately; never repair or replace source values."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import fitz
import pdfplumber
from pypdf import PdfReader
from pypdf.generic import ContentStream

def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: verify.py CARRIER_PDF MFR_PDF")
    pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    carrier, mfr = map(Path, sys.argv[1:])
    for p, name in [(carrier, "carrier"), (mfr, "mfr")]:
        b = p.read_bytes()
        assert len(b) == pins[name]["bytes"]
        assert hashlib.sha256(b).hexdigest() == pins[name]["sha256"]
    obs = pins["observations"]
    cp = fitz.open(carrier)[12]
    words = [w[4] for w in cp.get_text("words")
        if 260 <= w[0] <= 310 and 82 <= w[1] <= 205 and re.fullmatch("[0-9]+", w[4])]
    assert words == obs["extractions"]["pymupdf_numeric_words"]["sequence"]
    chunks = []
    def visit(text, cm, tm, font, size):
        x = tm[4]*cm[0] + tm[5]*cm[2] + cm[4]
        y = 842-(tm[4]*cm[1] + tm[5]*cm[3] + cm[5])
        if 260 <= x <= 310 and 70 <= y <= 215 and re.fullmatch(r"\s*[0-9]{1,3}\s*", text):
            chunks.append(text)
    reader = PdfReader(carrier)
    reader.pages[12].extract_text(visitor_text=visit)
    assert chunks == obs["extractions"]["pypdf_numeric_chunks"]["sequence"]
    with pdfplumber.open(carrier) as pdf:
        pp = pdf.pages[12].extract_words(x_tolerance=3, y_tolerance=3, keep_blank_chars=False)
        pp = [w["text"] for w in pp if 260 <= w["x0"] <= 310 and 82 <= w["top"] <= 205
            and re.fullmatch("[0-9]+", w["text"])]
    assert pp == obs["extractions"]["pdfplumber_numeric_words"]["sequence"]
    ops = ContentStream(reader.pages[12].get_contents(), reader)
    modes = [list(args) for args, op in ops.operations if op == b"Tr"]
    assert modes == obs["pdf_internals"]["root_Tr_operand_lists"]
    trace = []
    for span in cp.get_texttrace():
        chars = [c for c in span.get("chars", []) if 260 <= c[2][0] <= 310 and 70 <= c[2][1] <= 215]
        text = "".join(chr(c[0]) for c in chars)
        if text.strip() in ("99", "75", "22"):
            trace.append((text, span.get("type"), span.get("font"), span.get("seqno")))
    expected = [(s["unicode_text_in_selected_character_origins"], s["type"], s["font"], s["seqno"])
        for s in obs["pdf_internals"]["selected_numeric_trace"]]
    assert trace == expected
    mp = fitz.open(mfr)[2]
    region = [w[4] for w in mp.get_text("words") if 460 <= w[0] <= 535 and 280 <= w[1] <= 440]
    numeric = [int(t) for t in region if re.fullmatch("[0-9]+", t)]
    manual = obs["manual_carrier"]["literals_in_visual_row_order"]
    manual_positive = [int(t) for t in manual if int(t) > 0]
    memo = obs["manual_mfr"]["rows"]
    memo_numeric = [r["reported_seconds"] for r in memo if r["reported_seconds"] is not None]
    assert Counter(manual_positive) == Counter(memo_numeric) == Counter(numeric)
    assert manual.count("0") == 2
    assert sum(r["length_label"] == "No Conn" for r in memo) == 2
    print(json.dumps({"carrier_manual_entries": len(manual),
        "pymupdf_numeric_word_sequence": words, "pypdf_selected_numeric_chunks": chunks,
        "pdfplumber_numeric_word_sequence": pp,
        "selected_trace_spans": len(trace), "root_Tr_instructions": len(modes),
        "conditional_positive_multiset_match": True,
        "manual_carrier_zeros": 2, "mfr_No_Conn_labels": 2,
        "zeros_mapped_to_No_Conn": False,
        "manual_glyphs_or_historical_calls_validated": False}, indent=2))
if __name__ == "__main__":
    main()

"""Check a locally supplied original PDF; no network or source modification.

Usage: python3 verify_original.py --source /path/to/AEA2579-retention-email.pdf
Requires pypdf. Full extracted text and personal/contact fields are never printed.
This checks source identity/page count and selected anchors, not native email
identity, receipt, compliance, legal applicability, motive or historical cause.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path
import pypdf

EXPECTED = "ace9aa35cb266decd2344d48c06bd0d2625cfc5ce2bded8dd2bafdca67898329"
PATTERNS = {
    "printed_header": r"09/14/2001\s+01\s*:\s*00\s+PM",
    "retention_direction": r"Retain and secure until further notice ALL Administrative/Operational data and\s+records",
    "UTC_range_as_printed": r"110000 UTC to 120400 UTC",
    "local_September10_example": r"September 10, 2001\s+2000 - 2400 local",
    "facility_scope": r"Centers, Terminals, AFSS's, FSDPS's, and FCT's",
    "uncertainty_instruction": r"If a question arises whether or not you should retain the data, RETAIN IT\.",
}

def check_source(path):
    body = Path(path).read_bytes()
    digest = hashlib.sha256(body).hexdigest()
    if len(body) != 24441 or digest != EXPECTED:
        raise ValueError("Different source bytes: preserve the differing entity and investigate; do not silently replace the source pin")
    reader = pypdf.PdfReader(path)
    if len(reader.pages) != 1:
        raise ValueError("Unexpected page count")
    text = reader.pages[0].extract_text() or ""
    # Patterns tolerate layout whitespace solely to locate printed statements;
    # no value is corrected, selected or exported as a replacement source.
    anchors = {key: bool(re.search(pattern, text)) for key, pattern in PATTERNS.items()}
    if not all(anchors.values()):
        raise ValueError("At least one pinned textual anchor was not found")
    return {"sha256": digest, "bytes": len(body), "pages": len(reader.pages),
            "python": sys.version.split()[0], "pypdf": pypdf.__version__,
            "selected_anchor_checks": anchors,
            "limits": "Byte/page/text checks only; visual reading recorded separately; no native-email authentication, delivery, compliance, historical clock or causal finding"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    print(json.dumps(check_source(args.source), indent=2))

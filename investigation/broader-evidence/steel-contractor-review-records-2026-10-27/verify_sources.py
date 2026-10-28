"""Read-only pinned-source/range checks; not independent validation of steel analysis.

python verify_sources.py S03-DOM.json S03-Project3.txt ncstar1-3.pdf
Requires PyMuPDF. Sources remain unchanged; JSON goes to stdout.
"""
from pathlib import Path
import hashlib
import json
import re
import sys
import fitz


def main():
    if len(sys.argv) != 4:
        raise SystemExit("Supply the preserved DOM capture, Project3 extract and held NIST PDF")
    root = Path(__file__).parent
    pins = json.loads((root / "SOURCES.json").read_text())
    minute_pin = next(x for x in pins if x["id"] == "S03")
    nist_pin = next(x for x in pins if x["id"] == "ST-NIST3")
    dom_path, part_path, pdf_path = map(Path, sys.argv[1:])
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    rows = []

    def check(name, value, scope):
        rows.append(dict(check=name, passed=bool(value), scope=scope))

    check("Minute DOM capture pinned", digest(dom_path) == minute_pin["capture_sha256"],
          "Visible DOM representation; not native HTTP or 2004 file bytes")
    check("Selected extract pinned", digest(part_path) == minute_pin["selected_extract_sha256"],
          "Local derivative text only")
    check("Held official PDF pinned", digest(pdf_path) == nist_pin["sha256"],
          "Previously acquired PDF; no new native PDF download claimed")
    full = json.loads(dom_path.read_text())
    text = full["text"]
    start = text.index("Project 3: Mechanical")
    end = text.index("Project 5:", start)
    part = part_path.read_text()
    check("Exact bounded Project3 range", part == text[start:end],
          "Correct next actual heading; later meeting sections excluded")
    check("Non-verbatim qualifier retained", "not intended to be a verbatim transcript" in text,
          "Current official page's express scope")
    check("Committee question and review context",
          "draft report from them since October" in part and "project-level review" in part,
          "Question premise is not an independently authenticated receipt date")
    check("Dissatisfaction and integration account",
          "not as happy with the report" in part and "as opposed to releasing the contractor report separately" in part,
          "Does not by itself identify substantive disagreement or motive")
    check("Appendix promise retained", "issue their report as an appendix" in part,
          "Actual appendix and its relation to draft not acquired")
    doc = fitz.open(pdf_path)
    for page in [41, 150, 179]:
        t = re.sub(r"\s+", " ", doc[page - 1].get_text())
        present = ("outside contractor" in t and
                   ("agreed with" in t or "in agreement with" in t))
        check("Final agreement passage physical " + str(page), present,
              "Three passages in one report; images read separately; no contractor/draft identity join")
    check("Minute capture unchanged after reading", digest(dom_path) == minute_pin["capture_sha256"],
          "No source write operation")
    check("NIST PDF unchanged after reading", digest(pdf_path) == nist_pin["sha256"],
          "No source write operation")
    result = dict(checks=rows, passed=sum(x["passed"] for x in rows), total=len(rows),
                  native_new_PDFs_acquired=0, independent_steel_test=False,
                  historical_authentication=False, search_operations=12, search_cap=12,
                  substantive_steel_chain_complete=False)
    print(json.dumps(result, indent=2))
    if result["passed"] != result["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

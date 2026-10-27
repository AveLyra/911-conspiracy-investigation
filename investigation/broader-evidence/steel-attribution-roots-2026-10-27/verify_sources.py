"""Verify frozen public entities and extract the selected source pages.

Python 3 + pypdf. No network, OCR, source edits, or historical authentication.
FEMA's tabular pages require the separately documented image review.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import pypdf

SOURCES = {
    "interim": {
        "sha256": "ef665958a86004e03a18b48f20445542b36c93f89c23eb0dd1bf2ac000fd4bac",
        "bytes": 12743791, "pages": 182,
        "selected": [1, 3, 118, 119, 121, 156, 159, 163],
        "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1000-5v3.pdf",
    },
    "fema": {
        "sha256": "e054a70f9410b1fe0b141f0ec2401244183f67da4d0a703df5ffb18483d6f6fc",
        "bytes": 2333446, "pages": 27, "selected": [14, 15, 16],
        "url": "https://www.fema.gov/pdf/library/fema403_apd.pdf",
    },
    "final": {
        "sha256": "d234d025912dab100a0dd479f826b2adff0fc23acd5acb42efc93a4a8bcd9bc3",
        "bytes": 12034476, "pages": 114, "selected": [3, 33, 92, 96],
        "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf",
    },
    "log": {
        "sha256": "4efe8054bead356ff3bd5d619e7b0080768df4b0e7ec122a102036dd6eeab90b",
        "bytes": 1480662, "pages": 7, "selected": [2, 6],
        "url": "https://documents.theblackvault.com/documents/foia/2014-000573AckLtr-FinalResponse.pdf",
    },
}


def compact(text):
    # Search aid only. Exact unmodified extraction is retained alongside results.
    return re.sub(r"\s+", "", text).lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for key in SOURCES:
        ap.add_argument("--" + key, type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    results, extracts, checks = {}, {}, []

    def check(name, passed):
        checks.append({"check": name, "passed": bool(passed)})

    for key, spec in SOURCES.items():
        path = getattr(args, key)
        raw = path.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        check(key + ": frozen SHA-256", sha == spec["sha256"])
        check(key + ": frozen byte count", len(raw) == spec["bytes"])
        # Do not inspect a substituted entity under the frozen source label.
        if sha != spec["sha256"] or len(raw) != spec["bytes"]:
            raise SystemExit("Frozen input mismatch for " + key)
        reader = pypdf.PdfReader(path)
        check(key + ": page count", len(reader.pages) == spec["pages"])
        extracts[key] = [
            {"physical_page": n, "text": reader.pages[n - 1].extract_text() or ""}
            for n in spec["selected"]
        ]
        results[key] = {k: v for k, v in spec.items() if k != "selected"}
        results[key]["selected_physical_pages"] = spec["selected"]

    def page(key, n):
        return next(x["text"] for x in extracts[key] if x["physical_page"] == n)

    check("interim: cover reads June 2004", "june2004" in compact(page("interim", 1)))
    check("final: title page reads September 2005", "september2005" in compact(page("final", 3)))
    for key, n in [("interim", 163), ("final", 96)]:
        t = compact(page(key, n))
        if key == "interim":
            check(key + ": extracted heading says unidentified", "unidentified" in t)
        else:
            # Frozen OCR layer misreads the heading; do not repair the source text.
            # The printed heading was verified independently in the source image.
            check(key + ": frozen raw OCR heading signature", "tablea-7.ustofjjnidentifiedwideflangesections." in t)
        check(key + ": selected table includes W-14A or A", "w-14aora" in t)
        check(key + ": selected table includes W-14B", "w-14b" in t)
    check("interim: intake-photo method present", "overallimages" in compact(page("interim", 119)))
    check("log: exact target case identifier", "doc-nist-2013-001311" in compact(page("log", 6)))

    # Exclude public requesters' contact/name fields from the published extracts.
    # The full acquired released-log entity remains preserved in source storage.
    extracts.pop("log")
    (args.out / "SOURCE-PAGES.json").write_text(json.dumps(extracts, indent=2) + "\n")
    output = {
        "method": "Byte identity, page counts and bounded text-location checks only; visual observations recorded separately. Not historical custody authentication or a physical test.",
        "pypdf_version": pypdf.__version__,
        "source_entities": results,
        "checks": checks,
        "passed": sum(x["passed"] for x in checks), "total": len(checks),
        "visual_checks_included_in_count": False,
    }
    (args.out / "VERIFICATION.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"passed": output["passed"], "total": output["total"]}))
    if output["passed"] != output["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

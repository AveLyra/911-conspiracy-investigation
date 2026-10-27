"""Check selected report entities and preserved, conflicting shipping anchors.

python3 verify_shipping.py --inventory NCSTAR1-3B.pdf --materials NCSTAR1-3.pdf \
    --interim SP1000-5v3.pdf

Source identity and text anchors only; does not authenticate a shipment date.
"""
import argparse
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader, __version__ as pypdf_version


def run(inputs, root):
    sources = json.loads((root / "CONTEXT-SOURCES.json").read_text())
    observations = json.loads((root / "SHIPPING-OBSERVATIONS.json").read_text())
    keys = {"ST-NIST3B": "final", "ST-NIST3": "materials", "June2004SP": "interim"}
    results = []
    for row in observations:
        key = keys[row["source_id"]]
        source = sources[key]
        body = inputs[key].read_bytes()
        if hashlib.sha256(body).hexdigest() != source["sha256"]:
            raise ValueError("Source entity differs; preserve separately")
        reader = PdfReader(inputs[key])
        if len(reader.pages) != source["pages"]:
            raise ValueError("PDF page count differs")
        text = "".join((reader.pages[row["physical_page"] - 1].extract_text() or "").split())
        offset = text.find(row["compact_text_anchor"])
        if offset != row["compact_anchor_offset"]:
            raise ValueError("Selected extraction anchor differs")
        results.append(dict(source_id=row["source_id"], sha256=source["sha256"],
                            physical_page=row["physical_page"],
                            printed_page=row["printed_page"],
                            preserved_month=row["preserved_month"],
                            compact_anchor_offset=offset, source_check_passed=True))
    if len({r["preserved_month"] for r in results}) != 2:
        raise ValueError("Conflicting reported month values were not retained")
    return dict(pypdf_version=pypdf_version, source_checks=results,
                conflicting_months_retained=True, actual_transport_date_verified=False,
                candidate_specific_receipt_acquired=False,
                scope="Three pinned published accounts and selected text anchors; not a transport or custody reconstruction")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ["inventory", "materials", "interim"]:
        parser.add_argument("--" + argument, type=Path, required=True)
    args = parser.parse_args()
    inputs = dict(final=args.inventory, materials=args.materials, interim=args.interim)
    print(json.dumps(run(inputs, Path(__file__).resolve().parent), indent=2))

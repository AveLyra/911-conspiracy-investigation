"""Compare six source-associated printed labels; never infer historical clock calibration.

Requires PyMuPDF. Supply unchanged book, December and May PDF paths and a new
output directory. Reads the accompanying SOURCES, ANCHOR-INPUTS and PRODUCT-ROWS.
The book labels are explicitly human image transcriptions, not raw recorder data.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import fitz


def time_seconds(value, faa=False):
    pattern = r"(\d{2})(\d{2}):(\d{2})" if faa else r"(\d{1,2}):(\d{2}):(\d{2})"
    match = re.fullmatch(pattern, value)
    if not match:
        return None
    h, m, s = map(int, match.groups())
    if not (0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60):
        return None
    return h * 3600 + m * 60 + s


def main():
    parser = argparse.ArgumentParser()
    for name in ["book", "december", "may", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).parent
    pins = {r["id"]: r for r in json.loads((root / "SOURCES.json").read_text())}
    sources = {"C01": args.book, "FAA-S04": args.december, "FAA-S05": args.may}
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    checks = []
    texts = {}
    for sid, path in sources.items():
        actual = digest(path)
        assert actual == pins[sid]["sha256"], (sid, "wrong entity")
        with fitz.open(path) as doc:
            texts[sid] = [p.get_text(sort=True) for p in doc]
        checks.append(dict(source=sid, sha256=actual, pages=len(texts[sid])))

    def find(sid, pages, needle):
        candidates = []
        for number in pages:
            lines = texts[sid][number - 1].splitlines()
            for i, line in enumerate(lines):
                match = re.match(r"^\s*(\d{4}:\d{2})\s+(.+)", line)
                if not match:
                    continue
                end = i + 1
                while end < len(lines) and lines[end].strip() and not re.match(
                        r"^\s*(?:\d{4}:\d{2}\s+|\d{4}\s*$)", lines[end]):
                    end += 1
                if needle in " ".join(" ".join(lines[i:end]).lower().split()):
                    candidates.append(dict(time=match.group(1), physical_page=number,
                                           derived_start_line=i + 1, derived_end_line=end))
        assert len(candidates) == 1, (sid, needle, len(candidates))
        return candidates[0]

    needles = ["with you level", "indy center roger", "climb and maintain",
               "three five oh american", "ten degrees to the right", "ten right american"]
    anchors = json.loads((root / "ANCHOR-INPUTS.json").read_text())
    assert [x["id"] for x in anchors] == ["A1", "A2", "A3", "A4", "A5", "A6"]
    comparisons = []
    for row, needle in zip(anchors, needles):
        dec = find("FAA-S04", [2], needle)
        may = find("FAA-S05", [2, 4], needle)
        assert dec["time"] == row["prior_december_time"]
        assert may["time"] == row["prior_may_time"]
        book = time_seconds(row["book_time_as_visible"])
        valid = book is not None
        comparisons.append(dict(id=row["id"], event=row["event"],
                                book_label=row["book_time_as_visible"],
                                valid_hh_mm_ss=valid, december=dec, may=may,
                                conditional_book_plus_4h_minus_december_seconds=
                                book + 4 * 3600 - time_seconds(dec["time"], True) if valid else None,
                                conditional_book_plus_4h_minus_may_seconds=
                                book + 4 * 3600 - time_seconds(may["time"], True) if valid else None))

    # Strict negative controls prevent silently carrying or repairing displayed errors.
    assert time_seconds("8:43:81") is None
    assert time_seconds("8:50-47") is None
    assert time_seconds("8:59:59") == 8 * 3600 + 59 * 60 + 59
    import csv
    with (root / "PRODUCT-ROWS.csv").open(newline="") as handle:
        products = list(csv.DictReader(handle))
    unique = {(r["reader_page"], r["section"], r["product"]) for r in products}
    assert len(unique) == len(products)
    counts = collections.Counter(r["status_as_printed"] for r in products)
    sections = collections.Counter(r["section"] for r in products)
    unchanged = {sid: digest(path) == pins[sid]["sha256"] for sid, path in sources.items()}
    assert all(unchanged.values())
    result = dict(source_checks=checks, comparisons=comparisons,
                  valid_selected_labels=sum(r["valid_hh_mm_ss"] for r in comparisons),
                  invalid_selected_labels=sum(not r["valid_hh_mm_ss"] for r in comparisons),
                  product_rows=len(products), product_status_counts=dict(counts),
                  product_section_counts=dict(sections), controls_passed=3,
                  source_hashes_unchanged=unchanged,
                  assumptions=["Same candidate events by frozen words and sequence, not native IDs",
                               "Four-hour addition is conditional label arithmetic, not clock calibration",
                               "One typed row is not a count of files, CD objects or independent evidence",
                               "Human image transcription; original images retained; OCR not controlling"],
                  historical_clock_calibrated=False, independent_recorder_measurement=False)
    args.output.mkdir(parents=True, exist_ok=False)
    with (args.output / "RESULT.json").open("x") as handle:
        json.dump(result, handle, indent=2)
    print(json.dumps({k: result[k] for k in ["valid_selected_labels", "invalid_selected_labels",
                                           "product_rows", "product_status_counts", "controls_passed"]}, indent=2))


if __name__ == "__main__":
    main()

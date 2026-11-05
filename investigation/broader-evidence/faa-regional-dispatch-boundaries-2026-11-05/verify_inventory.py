"""Verify the selected HOST inventory joins using the preserved PDF bodies."""
import json
import re
import sys
from pathlib import Path

import pymupdf


def page_text(path, page_number):
    body = path.read_bytes()
    assert body.startswith(b"%PDF-"), path
    with pymupdf.open(stream=body, filetype="pdf") as pdf:
        return pdf[page_number - 1].get_text(sort=True)


def time_label(value):
    # PyMuPDF reads some zero glyphs as letter O and separates one digit.
    # This affects extraction only. Printed disputed times are kept in the report.
    return re.sub(r"\s+", "", value).replace("O", "0")


def compare(source_dir):
    copies = page_text(source_dir / "7604127.body", 16)
    original = page_text(source_dir / "7604167.body", 1)
    labels = r"([0-9O ]{4,5}Z)"
    grouped = re.findall(
        rf"NY(\d{{4}})\s*-\s*(\d{{4}})\s+\S+\s+{labels}\s*-\s*(?:\(9/12\))?{labels}",
        copies,
    )
    individual = dict(
        (int(key), (time_label(start), time_label(end)))
        for key, start, end in re.findall(rf"NY(\d{{4}})\s+\S+\s+{labels}\s*-\s*{labels}", original)
    )
    assert len(grouped) == 4
    expected = []
    checked = []
    for first, last, start, end in grouped:
        first, last = int(first), int(last)
        start, end = time_label(start), time_label(end)
        expected.extend(range(first, last + 1))
        assert individual[first][0] == start and individual[last][1] == end
        checked.append({"first": f"NY{first}", "last": f"NY{last}", "start": start, "end": end})
    assert expected == list(range(1471, 1497))
    assert set(expected) == set(individual)
    return {"groups": checked, "matched_tape_ids": len(individual), "matched_group_endpoints": 8}


if __name__ == "__main__":
    print(json.dumps(compare(Path(sys.argv[1])), indent=2))

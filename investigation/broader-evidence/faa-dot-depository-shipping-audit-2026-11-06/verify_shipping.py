"""Check the pinned GPO shipping lists for the DOT management-report route."""

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
from zipfile import ZipFile

import fitz

CLASS = re.compile(r"\bTD[\s_]*1\.1\s*/\s*[34](?=\W|$)", re.I)
ITEM = re.compile(r"(?<!\d)0?982\s*[-–]\s*C\s*[-–]\s*22(?!\d)", re.I)
TITLE = re.compile(
    r"actions\s+taken\s+on\s+(?:the\s+)?office\s+of\s+inspector|"
    r"management\s+decisions\s+and\s+final\s+actions|"
    r"secretary.?s\s+semi[\s-]*annual\s+report",
    re.I,
)
RELATED = re.compile(r"inspector\s+general", re.I)
FISCAL_CUTOFF = {"electronic": 23, "microfiche": 270, "paper": 416, "separates": 32}


def coverage(sequences):
    return {
        category: {
            "missing_numbers": sorted(set(range(1, cutoff + 1)) - counts.keys()),
            "above_cutoff": sorted(counts.keys() - set(range(1, cutoff + 1))),
            "repeated_numbers": sorted(n for n, count in counts.items() if count > 1),
        }
        for category, cutoff in FISCAL_CUTOFF.items()
        for counts in [sequences[category]]
    }


def flatten(text):
    text = re.sub(r"(?<=\w)-[ \t]*\n(?=\w)", "", text)
    return " ".join(text.split())


def digest(file):
    with file.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def scan_csv(file, fiscal_year):
    formats = Counter()
    sequences = {category: Counter() for category in FISCAL_CUTOFF}
    rows = td_rows = 0
    alternate_headers = []
    hits = []
    related = []
    transport_sample = None
    microfiche_sample = None
    with ZipFile(file) as archive:
        assert archive.testzip() is None
        for name in sorted(archive.namelist()):
            if not name.lower().endswith(".csv"):
                continue
            category = name.split("/")[1]
            formats[category] += 1
            number = re.fullmatch(r"\d{2}(\d{4})\D+", Path(name).stem, re.I)
            if fiscal_year == 2007:
                assert number, name
                sequences[category][int(number[1])] += 1
            raw = archive.read(name)
            try:
                text = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = raw.decode("cp1252")
            reader = csv.reader(io.StringIO(text))
            first = next(reader)
            assert len(first) == 5, name
            # Some archived files vary the field names. A genuine first
            # data row is retained even when the member lacks a header.
            if first != ["CLASSNO", "TITLE", "ITEMNO", "LISTNO", "LISTDATE"]:
                alternate_headers.append({"member": name, "first_row": first})
            if not first[-1].isdigit():
                assert first[0] in {"CLASSNO", "N1", "_"}, (name, first)
                start_line = 2
                data = reader
            else:
                start_line = 1
                data = csv.reader(io.StringIO(text))
            for line, record in enumerate(data, start_line):
                assert len(record) == 5, (name, line)
                rows += 1
                doc_class, title, item, list_number, list_date = record
                hit = {"member": name, "row": line, "fields": record}
                if re.match(r"TD[\s_]", doc_class):
                    td_rows += 1
                    if transport_sample is None:
                        transport_sample = hit
                if category == "microfiche" and microfiche_sample is None:
                    microfiche_sample = hit
                if CLASS.search(doc_class) or TITLE.search(title) or ITEM.search(item):
                    hits.append(hit)
                if RELATED.search(title) and re.match(r"TD[\s_]", doc_class):
                    related.append(hit)
    assert rows > 0 and td_rows > 0 and transport_sample and microfiche_sample
    result = {
        "sha256": digest(file), "members_by_format": dict(formats),
        "data_rows": rows, "transportation_rows": td_rows,
        "target_matches": hits, "transportation_inspector_general_title_matches": related,
        "transportation_control": transport_sample, "microfiche_control": microfiche_sample,
        "alternate_first_rows": alternate_headers,
    }
    if fiscal_year == 2007:
        result["coverage_against_published_cutoffs"] = coverage(sequences)
    return result


def scan_pdf(file):
    formats = Counter()
    sequences = {category: Counter() for category in FISCAL_CUTOFF}
    hits = []
    empty_text_files = []
    supplemental = {}
    with ZipFile(file) as archive:
        assert archive.testzip() is None
        for name in sorted(archive.namelist()):
            if not name.lower().endswith(".pdf"):
                continue
            category = name.split("/")[1]
            formats[category] += 1
            number = re.match(r"2007-(\d{4})-", Path(name).name, re.I)
            assert number, name
            index = int(number[1])
            sequences[category][index] += 1
            with fitz.open(stream=archive.read(name), filetype="pdf") as document:
                text = flatten("\n".join(page.get_text() for page in document))
                pages = len(document)
            if not text:
                empty_text_files.append(name)
            match = CLASS.search(text) or TITLE.search(text) or ITEM.search(text)
            if match:
                hits.append({"member": name, "match": match.group()})
            if category == "paper" and index in {18, 72, 218}:
                supplemental[name] = {"pages": pages, "characters": len(text), "target_match": bool(match)}
    return {
        "sha256": digest(file), "members_by_format": dict(formats),
        "target_matches_in_extractable_text": hits, "empty_text_files": empty_text_files,
        "coverage_against_published_cutoffs": coverage(sequences),
        "paper_18_72_218": supplemental,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_directory", type=Path)
    parser.add_argument("fy2007_pdf_archive", type=Path)
    args = parser.parse_args()
    result = {
        "csv": {
            year: scan_csv(args.csv_directory / f"shipping-{year}.zip", year)
            for year in range(2006, 2010)
        },
        "pdf_2007": scan_pdf(args.fy2007_pdf_archive),
        "pymupdf": fitz.VersionBind,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Read-only adaptation of ../drawing-locator/check_metadata.py; no acquisition."""
import hashlib
import json
import math
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
EXPECTED = ["mes:key", "title", "source", "agency", "box_name", "folder_name",
            "page_count", "pdf_size", "production_volume", "production_end", "mes:date"]
QUERIES = {
    "generator": 'ALL extension:pdf source:"WTC 7" generator test',
    "signoff": 'ALL extension:pdf source:"WTC 7" "sign off"',
    "punch": 'ALL extension:pdf source:"WTC 7" punch',
    "date": 'ALL extension:pdf source:"WTC 7" "7/17/99"',
    "control": 'ALL extension:pdf source:"WTC 7" box_name:"7DCAS" folder_name:"SKP-3 & SKP-4 AND REVISED S-TS-7 FOR YOUR USE"',
}


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read(path):
    raw = path.read_bytes()
    return json.loads(raw, object_pairs_hook=unique), {
        "file": path.name, "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest()}


def scalar(prop):
    assert len(prop["data"]) == 1, (prop["id"], "multivalue")
    value = prop["data"][0]["value"]
    kinds = [k for k in ("str", "num") if k in value]
    assert len(kinds) == 1, (prop["id"], "scalar kind")
    answer = value[kinds[0]]
    assert type(answer) is str if kinds[0] == "str" else type(answer) in (int, float)
    return answer


def properties(result):
    props = {}
    for prop in result["properties"]:
        assert prop["id"] not in props, (prop["id"], "duplicate property")
        props[prop["id"]] = scalar(prop)
    assert set(props) == set(EXPECTED), set(props)
    key = props["mes:key"]
    assert re.fullmatch(r"NYC-WTC_\d{9}", key)
    assert props["title"] == key + ".pdf" and props["source"] == "WTC 7"
    assert re.fullmatch(r"[1-9]\d*", props["page_count"])
    size = props["pdf_size"]
    assert type(size) in (int, float) and math.isfinite(size) and size > 0 and size == int(size)
    return props


def calculate():
    catalog, catalog_pin = read(HERE.parent / "folder-document-locator/folders.json")
    assert catalog["columns"] == ["source_index", "box", "folder", "documents", "pages", "first_bates"]
    assert len(catalog["rows"]) == catalog["rows_total"]
    pattern = re.compile(r"generator|sign[ -]*off|punch", re.I)
    hits, excluded = [], []
    for index, row in enumerate(catalog["rows"], 1):
        assert len(row) == 6 and type(row[0]) is int and 0 <= row[0] < len(catalog["sources"])
        assert all(type(row[j]) is str for j in (1, 2, 5))
        assert all(type(row[j]) is int and row[j] > 0 for j in (3, 4))
        if pattern.search(row[2]):
            item = {"row_ordinal_one_based": index, "source": catalog["sources"][row[0]], "row": row}
            (hits if item["source"] == "WTC 7" else excluded).append(item)
    memo = Path("/Users/admin/docs/911/research/WTC7_archive_leads_2026-09-16.md")
    memo_raw = memo.read_bytes()
    memo_hits = [{"line": i, "text": line} for i, line in enumerate(memo_raw.decode().splitlines(), 1)
                 if pattern.search(line)]
    queries, docs, pins = [], {}, [catalog_pin]
    for label, query in QUERIES.items():
        request, rp = read(HERE / f"{label}-request.json")
        response, sp = read(HERE / f"{label}-response.json")
        pins.extend((rp, sp))
        assert request == {"user": {"query": {"unparsed": query}}, "count": 50,
                           "content_sample_length": 0,
                           "properties": [{"name": n, "formats": ["VALUE"]} for n in EXPECTED]}
        echo = dict(response["search_request"])
        assert echo.pop("user_context", {}) == {} and echo == request
        rs = response["resultset"]
        estimated = response["estimated_count"]
        assert type(estimated) is int and estimated >= 0
        assert type(rs["next_avail"]) is bool and type(rs["prev_avail"]) is bool
        if "results" not in rs:
            assert estimated == 0 and not rs["next_avail"], "unexpected absent results"
        results = rs.get("results", [])
        assert type(results) is list and len(results) <= 50
        assert estimated >= len(results), "Estimate below returned count requires explicit review"
        ids = []
        for result in results:
            props = properties(result)
            key = props["mes:key"]
            assert key not in ids, (label, "duplicate ID", key)
            ids.append(key)
            if key in docs:
                assert docs[key]["properties"] == props, (key, "cross-query conflict")
                docs[key]["queries"].append(label)
            else:
                docs[key] = {"properties": props, "queries": [label]}
        causes = [s["termination_cause"] for s in rs["per_service_dataset"]]
        queries.append({"label": label, "query": query, "returned": len(ids), "estimated_count": estimated,
                        "ids": ids, "next_avail": rs["next_avail"], "prev_avail": rs["prev_avail"],
                        "results_key_present": "results" in rs, "termination_causes": causes,
                        "incomplete": (rs["prev_avail"] or rs["next_avail"] or estimated > len(ids)
                                       or not causes or any(c != "NO_MORE_RESULTS" for c in causes)),
                        "sum_document_pages": sum(int(docs[k]["properties"]["page_count"]) for k in ids)})
    assert "NYC-WTC_000167873" in queries[-1]["ids"], "Known-record control absent"
    local = {}
    for file in sorted(HERE.parent.rglob("NYC-WTC_*.pdf")):
        if file.stem in docs:
            local.setdefault(file.stem, []).append(str(file.relative_to(HERE.parent)))
    return {"catalog_pin": catalog_pin, "catalog_rows": len(catalog["rows"]),
            "catalog_hits": hits, "catalog_offsource_exclusions": excluded,
            "memo": {"file": memo.name, "sha256": hashlib.sha256(memo_raw).hexdigest(), "matches": memo_hits},
            "queries": queries, "unique_documents": docs, "unique_count": len(docs),
            "query_occurrences": sum(q["returned"] for q in queries),
            "unique_page_sum": sum(int(d["properties"]["page_count"]) for d in docs.values()),
            "held_pdf_name_matches": local, "pins": pins}


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2, sort_keys=True, allow_nan=False))

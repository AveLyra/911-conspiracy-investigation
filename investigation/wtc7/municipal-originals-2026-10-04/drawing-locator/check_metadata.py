"""Read-only, strict metadata checks; stdout is a derived locator, not content."""
import hashlib
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = ["mes:key", "title", "source", "agency", "box_name", "folder_name",
            "page_count", "pdf_size", "production_volume", "production_end", "mes:date"]


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
    scalar_keys = [key for key in ("str", "num") if key in value]
    assert len(scalar_keys) == 1, prop["id"]
    return value[scalar_keys[0]]


catalog, catalog_pin = read(HERE.parent / "folder-document-locator/folders.json")
assert catalog["columns"] == ["source_index", "box", "folder", "documents", "pages", "first_bates"]
assert len(catalog["rows"]) == catalog["rows_total"]
pattern = re.compile(r"SKP[ -]*[34]|S[ -]*TS[ -]*7", re.I)
catalog_hits = []
for index, row in enumerate(catalog["rows"], 1):
    assert len(row) == 6
    assert type(row[0]) is int and 0 <= row[0] < len(catalog["sources"])
    assert all(type(row[j]) is str for j in (1, 2, 5))
    assert all(type(row[j]) is int and row[j] > 0 for j in (3, 4))
    if pattern.search(row[2]):
        catalog_hits.append({"row_ordinal_one_based": index,
                             "source": catalog["sources"][row[0]], "row": row})

queries, documents, pins = [], {}, [catalog_pin]
for label in ("skp3", "skp4", "sts7", "control"):
    request, request_pin = read(HERE / f"{label}-request.json")
    response, response_pin = read(HERE / f"{label}-response.json")
    pins.extend((request_pin, response_pin))
    echo = dict(response["search_request"])
    assert echo.pop("user_context", {}) == {}
    assert echo == request, label
    assert request["count"] == 50 and request["content_sample_length"] == 0
    assert [p["name"] for p in request["properties"]] == EXPECTED
    resultset = response["resultset"]
    ids, pages = [], 0
    for result in resultset["results"]:
        props = {}
        for prop in result["properties"]:
            assert prop["id"] not in props, (label, prop["id"])
            props[prop["id"]] = scalar(prop)
        assert set(props) == set(EXPECTED), (label, set(props))
        key = props["mes:key"]
        assert re.fullmatch(r"NYC-WTC_\d{9}", key)
        assert props["title"] == key + ".pdf"
        assert props["source"] == "WTC 7"
        assert re.fullmatch(r"[1-9]\d*", props["page_count"])
        size = props["pdf_size"]
        assert type(size) in (int, float) and math.isfinite(size)
        assert size > 0 and size == int(size), (key, "nonintegral byte count")
        assert key not in ids, (label, "duplicate result", key)
        ids.append(key)
        pages += int(props["page_count"])
        if key in documents:
            assert documents[key]["properties"] == props, (key, "cross-query disagreement")
            documents[key]["queries"].append(label)
        else:
            documents[key] = {"properties": props, "queries": [label]}
    services = [s["termination_cause"] for s in resultset["per_service_dataset"]]
    queries.append({"label": label, "query": request["user"]["query"]["unparsed"],
                    "returned": len(ids), "estimated_count": response["estimated_count"],
                    "ids": ids, "sum_document_pages": pages,
                    "next_avail": resultset["next_avail"], "prev_avail": resultset["prev_avail"],
                    "termination_causes": services})

assert queries[-1]["ids"] == ["NYC-WTC_000167873"], "Known-cover control mismatch"
print(json.dumps({"catalog_pin": catalog_pin, "catalog_hits": catalog_hits,
                  "queries": queries, "unique_documents": documents,
                  "unique_count": len(documents),
                  "query_occurrences": sum(q["returned"] for q in queries),
                  "unique_page_sum": sum(int(d["properties"]["page_count"]) for d in documents.values()),
                  "pins": pins}, indent=2, sort_keys=True))

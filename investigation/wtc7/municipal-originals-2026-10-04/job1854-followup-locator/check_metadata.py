"""Bounded read-only adapter of the previous archive metadata contract."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "prior_metadata_contract", HERE.parent / "test-acceptance-locator/check_metadata.py")
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
LABELS = ("penn", "penn_phrase", "apt", "transient", "date_slash", "date_words",
          "load_shedding", "fuel_pump", "break_glass", "control")


def analyze(label, query, request, response):
    expected = {"user": {"query": {"unparsed": query}}, "count": 50,
                "content_sample_length": 0,
                "properties": [{"name": n, "formats": ["VALUE"]} for n in prior.EXPECTED]}
    assert request == expected, (label, "request contract")
    echo = dict(response["search_request"])
    assert echo.pop("user_context", {}) == {} and echo == request, (label, "request echo")
    rs = response["resultset"]
    estimate = response["estimated_count"]
    assert type(estimate) is int and estimate >= 0
    assert type(rs["next_avail"]) is bool and type(rs["prev_avail"]) is bool
    if "results" not in rs:
        assert estimate == 0 and not rs["next_avail"], (label, "unexpected absent results")
    results = rs.get("results", [])
    assert type(results) is list and len(results) <= 50
    assert estimate >= len(results), (label, "estimate below returned count")
    docs = {}
    for result in results:
        props = prior.properties(result)
        key = props["mes:key"]
        assert key not in docs, (label, "duplicate ID", key)
        docs[key] = props
    services = rs.get("per_service_dataset", [])
    assert type(services) is list
    causes = [service.get("termination_cause") for service in services]
    assert all(cause is None or type(cause) is str for cause in causes)
    row = {"label": label, "query": query, "returned": len(docs),
           "estimated_count": estimate, "ids": list(docs),
           "next_avail": rs["next_avail"], "prev_avail": rs["prev_avail"],
           "results_key_present": "results" in rs, "termination_causes": causes,
           "incomplete": (rs["prev_avail"] or rs["next_avail"] or estimate > len(docs)
                          or not causes or any(c != "NO_MORE_RESULTS" for c in causes)),
           "sum_document_pages": sum(int(p["page_count"]) for p in docs.values())}
    return row, docs


def merge(docs, found, label):
    for key, props in found.items():
        if key in docs:
            assert docs[key]["properties"] == props, (key, "cross-query conflict")
            docs[key]["queries"].append(label)
        else:
            docs[key] = {"properties": props, "queries": [label]}


def calculate():
    queries, query_pin = prior.read(HERE / "queries.json")
    assert tuple(queries) == LABELS, "Fixed query labels/order changed"
    rows, docs, pins = [], {}, [query_pin]
    for label, query in queries.items():
        request, request_pin = prior.read(HERE / f"{label}-request.json")
        response, response_pin = prior.read(HERE / f"{label}-response.json")
        pins.extend((request_pin, response_pin))
        row, found = analyze(label, query, request, response)
        rows.append(row)
        merge(docs, found, label)
    assert "NYC-WTC_000167873" in rows[-1]["ids"], "Known-record control absent"
    return {"queries": rows, "unique_documents": docs, "unique_count": len(docs),
            "query_occurrences": sum(q["returned"] for q in rows),
            "unique_page_sum": sum(int(d["properties"]["page_count"]) for d in docs.values()),
            "pins": pins}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions are required; do not use optimized Python")
    print(json.dumps(calculate(), indent=2, sort_keys=True, allow_nan=False))


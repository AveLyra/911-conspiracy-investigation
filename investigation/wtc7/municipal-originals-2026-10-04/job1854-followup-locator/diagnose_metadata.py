"""Diagnostic inventory after the unchanged strict contract failed.
Missing folder_name stays absent. This output cannot certify full-protocol acceptance.
"""
import json
import math
import re
import check_metadata as m


def diagnose_record(result):
    try:
        props = m.prior.properties(result)
        return {"properties": props, "strict_valid": True, "missing": [], "strict_error": None}
    except AssertionError as failure:
        props = {}
        for prop in result["properties"]:
            assert prop["id"] not in props, "duplicate properties cannot be normalized"
            props[prop["id"]] = m.prior.scalar(prop)
        missing = sorted(set(m.prior.EXPECTED) - set(props))
        extra = sorted(set(props) - set(m.prior.EXPECTED))
        assert missing == ["folder_name"] and not extra, "Unrecognized schema exception"
        key = props["mes:key"]
        assert re.fullmatch(r"NYC-WTC_\d{9}", key)
        assert props["title"] == key + ".pdf" and props["source"] == "WTC 7"
        assert re.fullmatch(r"[1-9]\d*", props["page_count"])
        size = props["pdf_size"]
        assert type(size) in (int, float) and math.isfinite(size) and size > 0 and size == int(size)
        return {"properties": props, "strict_valid": False, "missing": missing,
                "strict_error": {"type": type(failure).__name__,
                                 "argument_property_names": sorted(props)}}


def diagnose_query(label, query, request, response):
    expected = {"user": {"query": {"unparsed": query}}, "count": 50,
                "content_sample_length": 0,
                "properties": [{"name": n, "formats": ["VALUE"]} for n in m.prior.EXPECTED]}
    assert request == expected
    echo = dict(response["search_request"])
    assert echo.pop("user_context", {}) == {} and echo == request
    rs, estimate = response["resultset"], response["estimated_count"]
    assert type(estimate) is int and estimate >= 0
    assert type(rs["next_avail"]) is bool and type(rs["prev_avail"]) is bool
    if "results" not in rs:
        assert estimate == 0 and not rs["next_avail"]
    results = rs.get("results", [])
    assert type(results) is list and len(results) <= 50 and estimate >= len(results)
    services = rs.get("per_service_dataset", [])
    assert type(services) is list
    causes = [service.get("termination_cause") for service in services]
    assert all(c is None or type(c) is str for c in causes)
    docs, quarantined = {}, []
    for ordinal, result in enumerate(results, 1):
        item = diagnose_record(result)
        key = item["properties"]["mes:key"]
        assert key not in docs, (label, "duplicate ID", key)
        docs[key] = item
        if not item["strict_valid"]:
            quarantined.append({"label": label, "ordinal_one_based": ordinal,
                                "id": key, "diagnostic": item, "raw_result": result})
    row = {"label": label, "query": query, "returned": len(results),
           "estimated_count": estimate, "ids": list(docs), "next_avail": rs["next_avail"],
           "prev_avail": rs["prev_avail"], "results_key_present": "results" in rs,
           "termination_causes": causes,
           "incomplete": (rs["prev_avail"] or rs["next_avail"] or estimate > len(results)
                          or not causes or any(c != "NO_MORE_RESULTS" for c in causes)),
           "sum_document_pages": sum(int(d["properties"]["page_count"]) for d in docs.values()),
           "strict_valid_occurrences": len(results)-len(quarantined),
           "quarantined_occurrences": len(quarantined)}
    return row, docs, quarantined


def calculate():
    queries, query_pin = m.prior.read(m.HERE / "queries.json")
    assert tuple(queries) == m.LABELS
    rows, docs, quarantine, pins = [], {}, [], [query_pin]
    for label, query in queries.items():
        request, rp = m.prior.read(m.HERE / f"{label}-request.json")
        response, sp = m.prior.read(m.HERE / f"{label}-response.json")
        pins.extend((rp, sp))
        row, found, invalid = diagnose_query(label, query, request, response)
        rows.append(row)
        quarantine.extend(invalid)
        for key, record in found.items():
            if key in docs:
                assert docs[key]["diagnostic"] == record, (key, "cross-query conflict")
                docs[key]["queries"].append(label)
            else:
                docs[key] = {"diagnostic": record, "queries": [label]}
    assert "NYC-WTC_000167873" in rows[-1]["ids"]
    invalid_ids = sorted(k for k, d in docs.items() if not d["diagnostic"]["strict_valid"])
    return {"status": "diagnostic_only_full_contract_failed" if invalid_ids else "diagnostic_only",
            "queries": rows, "documents": docs, "unique_count": len(docs),
            "query_occurrences": sum(q["returned"] for q in rows),
            "strict_valid_occurrences": sum(q["strict_valid_occurrences"] for q in rows),
            "quarantined_occurrences": len(quarantine), "quarantined_unique_ids": invalid_ids,
            "strict_valid_unique_count": len(docs)-len(invalid_ids),
            "unique_page_sum": sum(int(d["diagnostic"]["properties"]["page_count"]) for d in docs.values()),
            "quarantine": quarantine, "pins": pins}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions required")
    print(json.dumps(calculate(), indent=2, sort_keys=True, allow_nan=False))


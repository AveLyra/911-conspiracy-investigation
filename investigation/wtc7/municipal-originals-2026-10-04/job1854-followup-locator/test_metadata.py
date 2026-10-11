"""Synthetic protocol tests; no network and no historical result consumption."""
import copy
import json
import unittest
import check_metadata as m

class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.query = 'ALL extension:pdf source:"WTC 7" Penn'
        self.request = {"user": {"query": {"unparsed": self.query}}, "count": 50,
                        "content_sample_length": 0,
                        "properties": [{"name": n, "formats": ["VALUE"]} for n in m.prior.EXPECTED]}
        props = {"mes:key": "NYC-WTC_000167873", "title": "NYC-WTC_000167873.pdf",
                 "source": "WTC 7", "agency": "None", "box_name": "7DCAS",
                 "folder_name": "test", "page_count": "1", "pdf_size": 100,
                 "production_volume": "v", "production_end": "end", "mes:date": "date"}
        self.doc = {"properties": [{"id": key, "data": [{"value":
                    {"num" if type(value) is int else "str": value}}]}
                   for key, value in props.items()]}
        self.response = {"search_request": copy.deepcopy(self.request), "estimated_count": 1,
                         "resultset": {"next_avail": False, "prev_avail": False,
                                       "results": [copy.deepcopy(self.doc)],
                                       "per_service_dataset": [{"termination_cause": "NO_MORE_RESULTS"}]}}

    def run_case(self):
        return m.analyze("synthetic", self.query, self.request, self.response)

    def test_complete(self):
        row, docs = self.run_case()
        self.assertFalse(row["incomplete"])
        self.assertEqual(row["sum_document_pages"], 1)
        self.assertEqual(docs["NYC-WTC_000167873"]["agency"], "None")

    def test_empty_absent_key(self):
        self.response["estimated_count"] = 0
        del self.response["resultset"]["results"]
        row, _ = self.run_case()
        self.assertFalse(row["results_key_present"])
        self.assertFalse(row["incomplete"])

    def test_empty_present_key(self):
        self.response["estimated_count"] = 0
        self.response["resultset"]["results"] = []
        self.assertEqual(self.run_case()[0]["returned"], 0)

    def test_nonempty_absent_results(self):
        del self.response["resultset"]["results"]
        with self.assertRaises(AssertionError): self.run_case()

    def test_next(self):
        self.response["resultset"]["next_avail"] = True
        self.assertTrue(self.run_case()[0]["incomplete"])

    def test_previous(self):
        self.response["resultset"]["prev_avail"] = True
        self.assertTrue(self.run_case()[0]["incomplete"])

    def test_estimated_more(self):
        self.response["estimated_count"] = 2
        self.assertTrue(self.run_case()[0]["incomplete"])

    def test_estimated_less(self):
        self.response["estimated_count"] = 0
        with self.assertRaises(AssertionError): self.run_case()

    def test_missing_service_evidence(self):
        del self.response["resultset"]["per_service_dataset"]
        self.assertTrue(self.run_case()[0]["incomplete"])

    def test_missing_cause(self):
        self.response["resultset"]["per_service_dataset"] = [{}]
        self.assertTrue(self.run_case()[0]["incomplete"])

    def test_count_limit(self):
        self.response["resultset"]["per_service_dataset"][0]["termination_cause"] = "COUNT_LIMIT"
        self.assertTrue(self.run_case()[0]["incomplete"])

    def test_duplicate_id(self):
        self.response["estimated_count"] = 2
        self.response["resultset"]["results"].append(copy.deepcopy(self.doc))
        with self.assertRaises(AssertionError): self.run_case()

    def test_duplicate_property(self):
        self.response["resultset"]["results"][0]["properties"].append(copy.deepcopy(self.doc["properties"][0]))
        with self.assertRaises(AssertionError): self.run_case()

    def test_echo_mismatch(self):
        self.response["search_request"]["count"] = 49
        with self.assertRaises(AssertionError): self.run_case()

    def test_query_mismatch(self):
        self.query = "different"
        with self.assertRaises(AssertionError): self.run_case()

    def test_duplicate_json_key(self):
        with self.assertRaises(ValueError):
            json.loads('{"x":1,"x":2}', object_pairs_hook=m.prior.unique)

    def test_cross_query_conflict(self):
        _, found = self.run_case()
        merged = {}
        m.merge(merged, found, "one")
        changed = copy.deepcopy(found)
        changed["NYC-WTC_000167873"]["folder_name"] = "different"
        with self.assertRaises(AssertionError): m.merge(merged, changed, "two")

    def test_query_memberships(self):
        _, found = self.run_case()
        merged = {}
        m.merge(merged, found, "one")
        m.merge(merged, found, "two")
        self.assertEqual(merged["NYC-WTC_000167873"]["queries"], ["one", "two"])

    def test_bad_scalar(self):
        self.response["resultset"]["results"][0]["properties"][0]["data"].append({"value": {"str": "extra"}})
        with self.assertRaises(AssertionError): self.run_case()

    def test_wrong_source(self):
        self.response["resultset"]["results"][0]["properties"][2]["data"][0]["value"]["str"] = "WTC 1"
        with self.assertRaises(AssertionError): self.run_case()

if __name__ == "__main__":
    unittest.main()


"""Synthetic tests for the narrow diagnostic exception; strict code is unchanged."""
import copy
import unittest
import diagnose_metadata as d
from test_metadata import MetadataTests

class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        fixture = MetadataTests()
        fixture.setUp()
        self.doc = fixture.doc
        self.request, self.response, self.query = fixture.request, fixture.response, fixture.query

    def test_valid_row(self):
        self.assertTrue(d.diagnose_record(self.doc)["strict_valid"])

    def test_missing_folder_stays_missing(self):
        self.doc["properties"] = [p for p in self.doc["properties"] if p["id"] != "folder_name"]
        item = d.diagnose_record(self.doc)
        self.assertFalse(item["strict_valid"])
        self.assertEqual(item["missing"], ["folder_name"])
        self.assertNotIn("folder_name", item["properties"])
        self.assertEqual(len(item["properties"]), 10)

    def test_missing_id_stops(self):
        self.doc["properties"] = [p for p in self.doc["properties"] if p["id"] != "mes:key"]
        with self.assertRaises(AssertionError): d.diagnose_record(self.doc)

    def test_duplicate_stops(self):
        self.doc["properties"].append(copy.deepcopy(self.doc["properties"][0]))
        with self.assertRaises(AssertionError): d.diagnose_record(self.doc)

    def test_invalid_missing_folder_record_stops(self):
        self.doc["properties"] = [p for p in self.doc["properties"] if p["id"] != "folder_name"]
        self.doc["properties"][0]["data"][0]["value"]["str"] = "bad key"
        with self.assertRaises(AssertionError): d.diagnose_record(self.doc)

    def test_literal_none_not_absence(self):
        self.doc["properties"][5]["data"][0]["value"]["str"] = "None"
        self.assertTrue(d.diagnose_record(self.doc)["strict_valid"])
        self.assertEqual(d.diagnose_record(self.doc)["properties"]["folder_name"], "None")

    def test_query_counts_include_quarantine(self):
        self.response["resultset"]["results"][0]["properties"] = [
            p for p in self.doc["properties"] if p["id"] != "folder_name"]
        row, _, q = d.diagnose_query("test", self.query, self.request, self.response)
        self.assertEqual((row["returned"], row["strict_valid_occurrences"], row["quarantined_occurrences"]), (1, 0, 1))
        self.assertEqual(q[0]["ordinal_one_based"], 1)
        self.assertEqual(q[0]["raw_result"], self.response["resultset"]["results"][0])

    def test_more_results_remains_partial(self):
        self.response["estimated_count"] = 100
        row, _, _ = d.diagnose_query("test", self.query, self.request, self.response)
        self.assertTrue(row["incomplete"])

if __name__ == "__main__":
    unittest.main()


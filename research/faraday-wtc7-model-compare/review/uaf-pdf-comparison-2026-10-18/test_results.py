"""Acceptance checks for actual saved results; no scientific-cause validation."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).parent
def load(name, directory="results"):
    return json.loads((ROOT / directory / name).read_text())

class Results(unittest.TestCase):
    def test_full_coverage_and_no_errors(self):
        pages = load("pages.json")
        self.assertEqual([p["page"] for p in pages], list(range(1, 126)))
        self.assertTrue(all("error" not in r for p in pages for r in p["sources"].values()))

    def test_full_repeat(self):
        for name in ["documents.json", "object-inventories.json", "object-differences.json", "pages.json", "page-differences.json", "runtime.json"]:
            self.assertEqual(load(name), load(name, "repeat-results"), name)
        a, b = load("summary.json"), load("summary.json", "repeat-results")
        a.pop("completed_at_utc")
        b.pop("completed_at_utc")
        self.assertEqual(a, b)

    def test_independent_text_agreement(self):
        self.assertEqual(load("summary.json")["channel_difference_pages"]["raw_text"], load("independent-pypdf-text-check.json")["differing_pages"])

    def test_sources_unchanged(self):
        summary = load("summary.json")
        self.assertTrue(summary["source_files_unchanged"])
        self.assertEqual(summary["started_with_historical_hashes"], summary["post_comparison_hashes"])

if __name__ == "__main__":
    unittest.main(verbosity=2)

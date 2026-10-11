"""Finite structural negative controls; no product acceptance or semantic proof."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import verify_record as v


class RecordChecks(unittest.TestCase):
    def setUp(self):
        self.record = v.read_json(Path(__file__).with_name("record.json"))

    def fails(self, mutate):
        record = copy.deepcopy(self.record)
        mutate(record)
        with self.assertRaises(ValueError):
            v.validate(record)

    def test_real_structure(self):
        self.assertEqual(v.validate(self.record)["digest_topics_mapped"], 27)

    def test_missing_unit(self):
        self.fails(lambda r: r["units"].pop(2))

    def test_missing_tail(self):
        self.fails(lambda r: r["units"].pop())

    def test_overlap(self):
        self.fails(lambda r: r["units"][1].update(start=r["units"][0]["end"]))

    def test_reorder(self):
        self.fails(lambda r: r["units"].reverse())

    def test_unknown_field(self):
        self.fails(lambda r: r["units"][0].update(silent_extra=True))

    def test_empty_acceptance(self):
        self.fails(lambda r: next(u for u in r["units"] if u["kind"] == "requirement").update(acceptance=[]))

    def test_empty_requirement(self):
        self.fails(lambda r: next(u for u in r["units"] if u["kind"] == "requirement").update(technical_record=""))

    def test_boolean_line(self):
        self.fails(lambda r: r["units"][0].update(start=True))

    def test_no_mapping(self):
        self.fails(lambda r: [u.update(digest_items=[]) for u in r["units"]])

    def test_missing_topic(self):
        self.fails(lambda r: r["digest_topics"].pop("27"))

    def test_missing_single_requirement_mapping(self):
        self.fails(lambda r: next(u for u in r["units"] if u["kind"] == "requirement").update(digest_items=[]))

    def test_missing_single_sfb_mapping(self):
        self.fails(lambda r: next(u for u in r["units"] if u["kind"] == "requirement").update(sfb=[]))

    def test_render_retains_each_field(self):
        rendered = v.render(self.record)
        for u in self.record["units"]:
            self.assertIn(u["id"], rendered)
            for field in ("title", "technical_record", "qualification", "omission"):
                if u[field]:
                    self.assertIn(u[field], rendered)
            for acceptance in u["acceptance"]:
                self.assertIn(acceptance, rendered)

    def test_duplicate_json_key(self):
        with self.assertRaises(ValueError):
            json.loads('{"a":1,"a":2}', object_pairs_hook=v.unique_object)

    def test_changed_source(self):
        with self.assertRaises(ValueError):
            v.validate(self.record, b"different source\n")

    def test_line_hash_checks(self):
        r = copy.deepcopy(self.record)
        source = b"x\n" * r["source"]["lines"]
        r["source"]["bytes"] = len(source)
        r["source"]["sha256"] = hashlib.sha256(source).hexdigest()
        with self.assertRaises(ValueError):
            v.validate(r, source)

    def test_source_positive_and_tampered_span(self):
        r = copy.deepcopy(self.record)
        source = b"x\n" * r["source"]["lines"]
        r["source"]["bytes"] = len(source)
        r["source"]["sha256"] = hashlib.sha256(source).hexdigest()
        for u in r["units"]:
            u["source_sha256"] = hashlib.sha256(b"x\n" * (u["end"] - u["start"] + 1)).hexdigest()
        self.assertTrue(v.validate(r, source)["source_bytes_verified"])
        r["units"][0]["source_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            v.validate(r, source)

    def test_manifest_scope_and_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = b"synthetic\n"
            (root / "fixture.txt").write_bytes(data)
            manifest = {"files": {"fixture.txt": {"sha256": v.digest(data), "bytes": len(data)}}}
            (root / "manifest.json").write_text(json.dumps(manifest))
            self.assertEqual(v.verify_manifest(root), 1)
            (root / "extra.txt").write_text("unlisted")
            with self.assertRaises(ValueError):
                v.verify_manifest(root)
            (root / "extra.txt").unlink()
            (root / "fixture.txt").write_text("changed")
            with self.assertRaises(ValueError):
                v.verify_manifest(root)

    def test_review_coverage_and_binding(self):
        root = Path(__file__).resolve().parent
        review = v.read_json(root / "review.json")
        raw = (root / "record.json").read_bytes()
        self.assertEqual(v.verify_review(self.record, review, raw), len(self.record["units"]))
        bad = copy.deepcopy(review)
        bad["partitions"][0]["reviewed_ids"].pop()
        with self.assertRaises(ValueError):
            v.verify_review(self.record, bad, raw)
        bad = copy.deepcopy(review)
        bad["partitions"].append(bad["partitions"][0])
        with self.assertRaises(ValueError):
            v.verify_review(self.record, bad, raw)
        with self.assertRaises(ValueError):
            v.verify_review(self.record, review, raw + b"\n")


if __name__ == "__main__":
    unittest.main()

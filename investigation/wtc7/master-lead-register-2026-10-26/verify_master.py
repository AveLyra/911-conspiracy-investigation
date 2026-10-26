#!/usr/bin/env python3
"""Verify this integration's preservation contracts; not historical conclusions."""
import argparse
import difflib
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import unquote

from build_master import BASE, BASELINE_COMMIT, OLD, RF, BI, BP, ROOT, HERE, raw, relocate_baseline, put, js


def sha(data):
    return hashlib.sha256(data).hexdigest()


def current(path):
    p = ROOT / path
    if p.exists():
        return p.read_bytes()
    return subprocess.check_output(["git", "show", "HEAD:" + path], cwd=ROOT)


def read_json(path):
    return json.loads((HERE / path).read_text())


class MasterIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = read_json("register.json")
        cls.old = json.loads(raw(OLD + "/register.json"))
        cls.scope = read_json("SCOPE.json")
        cls.master = (HERE / "MASTER-LIST.md").read_text()

    def test_01_complete_stable_id_crosswalk(self):
        entries = self.reg["entries"]
        self.assertEqual([x["id"] for x in entries], [f"M{i:03}" for i in range(1, 153)])
        self.assertEqual([x["original_id"] for x in entries[134:]],
                         [f"RF{i:03}" for i in range(1, 9)] + [f"BP{i:02}" for i in range(1, 11)])
        self.assertEqual(self.reg["entries"][:134], self.old["entries"])
        self.assertEqual(self.reg["inherited_register_metadata"], {k: v for k, v in self.old.items() if k != "entries"})
        self.assertEqual((self.reg["entry_count"], self.reg["new_entry_count"]), (152, 18))
        self.assertIsNone(self.reg["independent_anomaly_count"])

    def test_02_prior_eighty_source_files_unchanged(self):
        self.assertEqual(len(self.scope["protected_files"]), 80)
        for path, pin in self.scope["protected_files"].items():
            with self.subTest(path=path):
                data = current(path)
                self.assertEqual(sha(data), pin["sha256"])
                self.assertEqual(len(data), pin["bytes"])
                self.assertEqual(data, raw(path))

    def test_03_original_records_and_excerpts_exact(self):
        rf = json.loads(raw(RF + "/findings.json"))["findings"]
        bp = json.loads(raw(BI + "/integrated-findings.json"))["findings"]
        rf_report = raw(RF + "/REPORT.md").decode().splitlines(keepends=True)
        bp_report = raw(BP + "/RECORD.md").decode().splitlines(keepends=True)
        excerpts = (HERE / "SOURCE-EXCERPTS.md").read_text()
        for entry, original in zip(self.reg["entries"][134:], rf + bp, strict=True):
            self.assertEqual(entry["original_record"], original)
            loc = entry["locators"][0]
            self.assertEqual(sha(raw(loc["repository_path"])), loc["source_sha256"])
            self.assertEqual(sha(loc["excerpt"].encode()), loc["excerpt_sha256"])
            byte_start, byte_stop = loc["excerpt_bytes_zero_based_half_open"]
            self.assertEqual(raw(loc["repository_path"])[byte_start:byte_stop], loc["excerpt"].encode())
            start, stop = loc["text_lines_1based"]
            if entry["original_id"].startswith("RF"):
                self.assertEqual(loc["excerpt"], "".join(rf_report[start:stop]))
            else:
                self.assertEqual(loc["excerpt"], original["verbatim_published_body"])
                excerpt_start, excerpt_stop = loc["excerpt_text_lines_1based"]
                source_prefix = raw(loc["repository_path"])[:byte_start].decode()
                self.assertEqual(excerpt_start, source_prefix.count("\n") + 1)
                self.assertEqual(excerpt_stop, excerpt_start + len(loc["excerpt"].splitlines()) - 1)
            self.assertIn(loc["excerpt"], excerpts)
            self.assertIn(loc["excerpt"], self.master)

    def test_04_primary_source_pins_not_reinvented(self):
        op = json.loads(raw(RF + "/source-pins.json"))
        bank = json.loads(raw(BI + "/sources/published/SOURCES.json"))
        self.assertEqual(self.reg["new_primary_source_catalogs"], {"operational": op, "bank_phone": bank})
        allowed = {p["url"]: p["sha256"] for p in op["sources"]}
        for key in ("new_retrievals", "preceding_sources_reused"):
            for item in bank[key]:
                if "sha256" in item:
                    allowed[item["url"]] = item["sha256"]
        for entry in self.reg["entries"][134:]:
            self.assertTrue(entry["source_urls"])
            self.assertTrue(entry["primary_source_pins"])
            for pin in entry["primary_source_pins"]:
                self.assertEqual(pin["sha256"], allowed[pin["url"]])
            for url in entry["source_urls"]:
                self.assertIn(url, json.dumps(op) + json.dumps(bank) + entry["locators"][0]["excerpt"])
        for name, pin in self.scope["redundant_public_dependencies"].items():
            self.assertEqual((HERE / name).read_bytes(), raw(pin["source"]))
            self.assertEqual(sha((HERE / name).read_bytes()), pin["sha256"])

    def test_05_all_open_bundles_and_targets_exact(self):
        targets = json.loads(raw(BI + "/targets-v2.json"))
        self.assertEqual(read_json("OPEN-TARGETS.json"), targets)
        self.assertEqual(self.reg["current_open_targets"], targets)
        self.assertEqual([x["id"] for x in targets["targets"]], [f"BR{i:02}" for i in range(1, 6)])
        self.assertEqual([x["id"] for x in targets["bank_phone_original_targets"]], [f"BPR{i:02}" for i in range(1, 11)])
        self.assertIn("$100,000", self.master)
        self.assertIn("apartment-payment 1A-file lead is distinct", self.master)

    def test_06_inherited_master_body_preserved_except_links(self):
        baseline = raw(OLD + "/MASTER-LIST.md").decode()
        expected = relocate_baseline(baseline[baseline.index("## Register\n"):])
        body = self.master.split("\n\n## Broader operational-record and bank/telephone additions\n", 1)[0]
        self.assertTrue(body.endswith(expected))
        self.assertEqual(re.findall(r"^### (M\d{3}) —", self.master, re.M), [f"M{i:03}" for i in range(1, 153)])
        all_ids = {e["id"] for e in self.reg["entries"]}
        for e in self.reg["entries"]:
            self.assertTrue(set(e["related"]) <= all_ids)

    def test_07_local_links_and_anchors(self):
        files = list(HERE.glob("*.md")) + [ROOT / "investigation/MASTER-LIST.md"]
        count = 0
        for path in files:
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if target.startswith(("http:", "https:")):
                    continue
                name, _, anchor = target.partition("#")
                dest = (path.parent / unquote(name)).resolve() if name else path
                if dest.name == "VERIFICATION.json" and not dest.exists():
                    continue
                self.assertTrue(dest.is_file(), (path.name, target))
                if anchor:
                    self.assertIn(f'id="{anchor}"', dest.read_text(), (path.name, target))
                count += 1
        self.assertGreater(count, 250)

    def test_08_conflicting_and_confirming_values_retained(self):
        bank = "\n".join(x["locators"][0]["excerpt"] for x in self.reg["entries"][142:])
        for value in ("1,558", "4,000", "8,000", "9,900", "April 19", "April 20", "22", "27", "CBR", "cell phone", "1A", "42"):
            self.assertIn(value, bank)
        bp08 = self.reg["entries"][149]
        self.assertEqual(bp08["original_id"], "BP08")
        for value in ("eight", "42", "June 23"):
            self.assertIn(value, bp08["locators"][0]["excerpt"])
        for value in ("coincidence", "limited", "January2000", "02/01/2000", "page5", "page6", "text/plain"):
            self.assertIn(value, self.master)

    def test_09_text_payload_and_disclosure_boundaries(self):
        allowed = {"README.md", "MASTER-LIST.md", "SOURCE-EXCERPTS.md", "CROSSWALK.md", "CHECKLIST.md",
                   "register.json", "OPEN-TARGETS.json", "SCOPE.json", "build_master.py", "verify_master.py",
                   "TEXT-CHANGES.diff", "VERIFICATION.json", "MANIFEST.json", "CALL-ROWS.json", "NEXT-RECORDS.md", "recount_calls.py"}
        pattern = re.compile(r"/(?:Users|Volumes|private)/|BEGIN [A-Z ]*PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}")
        for path in HERE.iterdir():
            self.assertIn(path.name, allowed)
            self.assertFalse(path.is_symlink())
            self.assertTrue(path.is_file())
            self.assertLess(path.stat().st_size, 16 * 1024 * 1024)
            if path.suffix != ".py":
                self.assertIsNone(pattern.search(path.read_text()), path.name)

    def test_10_manifest_when_present(self):
        p = HERE / "MANIFEST.json"
        if not p.exists():
            return
        manifest = json.loads(p.read_text())
        expected = {x.name for x in HERE.iterdir() if x.is_file() and x.name not in ("MANIFEST.json", "VERIFICATION.json")}
        self.assertEqual(set(manifest["files"]), expected)
        for name, pin in manifest["files"].items():
            data = (HERE / name).read_bytes()
            self.assertEqual(sha(data), pin["sha256"])
            self.assertEqual(len(data), pin["bytes"])
        pointer = (ROOT / "investigation/MASTER-LIST.md").read_bytes()
        self.assertEqual(sha(pointer), manifest["navigation_pointer"]["sha256"])


def record_changes():
    old = raw(OLD + "/MASTER-LIST.md").decode().splitlines(keepends=True)
    new = (HERE / "MASTER-LIST.md").read_text().splitlines(keepends=True)
    chunks = list(difflib.unified_diff(old, new, fromfile=OLD + "/MASTER-LIST.md", tofile=str(HERE.relative_to(ROOT) / "MASTER-LIST.md")))
    for path in sorted(HERE.glob("*.md")) + [ROOT / "investigation/MASTER-LIST.md"]:
        if path.name == "MASTER-LIST.md" and path.parent == HERE:
            continue
        chunks.extend(difflib.unified_diff([], path.read_text().splitlines(keepends=True), fromfile="/dev/null", tofile=str(path.relative_to(ROOT))))
    put("TEXT-CHANGES.diff", "".join(chunks))
    js("MANIFEST.json", {
        "date": "2026-10-26",
        "self_and_verification_excluded": True,
        "files": {p.name: {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())}
                  for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in ("MANIFEST.json", "VERIFICATION.json")},
        "navigation_pointer": {"path": "investigation/MASTER-LIST.md", "sha256": sha((ROOT / "investigation/MASTER-LIST.md").read_bytes())},
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()
    if args.record:
        record_changes()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MasterIntegrationTests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    if args.record:
        js("VERIFICATION.json", {
            "date": "2026-10-26", "command": "python3 -B verify_master.py --record",
            "tests_run": result.testsRun, "failures": 0, "errors": 0,
            "entries": 152, "new_crosswalk_entries": 18, "protected_prior_files": 80,
            "scope": "Stable-ID/object/excerpt/source-pin/open-target/link/file preservation and integrity, not historical claim validation or reauthentication of unavailable originals.",
            "pdf_layout": "Not applicable; no PDF created or altered.",
            "remote_publication": "Not asserted by this precommit receipt; exact resulting commit and remote files require separate verification.",
        })
    print(json.dumps({"tests": result.testsRun, "status": "passed", "historical_adjudication": False}))


if __name__ == "__main__":
    main()

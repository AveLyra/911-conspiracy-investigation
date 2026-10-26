#!/usr/bin/env python3
"""Check source-note transfer, original entry preservation and public scope."""
import argparse
import difflib
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import unquote

from build_cia_master import BASE, OLD, STUDY, HERE, ROOT, PUBLIC_NOTES, blob, relocate, write, js

NOTES = ROOT / STUDY


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text())


class CiaMasterChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg=load(HERE/"register.json")
        cls.old=json.loads(blob(OLD+"/register.json"))
        cls.scope=load(HERE/"SCOPE.json")
        cls.findings=load(NOTES/"findings.json")["findings"]
        cls.sources=load(NOTES/"SOURCES.json")

    def test_01_ids_and_unchanged_prior_records(self):
        self.assertEqual([e["id"] for e in self.reg["entries"]],[f"M{i:03}" for i in range(1,161)])
        self.assertEqual(self.reg["entries"][:152],self.old["entries"])
        self.assertEqual(self.reg["prior_master_metadata"],{k:v for k,v in self.old.items() if k!="entries"})
        self.assertEqual((self.reg["entry_count"],self.reg["new_entry_count"]),(160,8))
        self.assertIsNone(self.reg["independent_anomaly_count"])

    def test_02_all_prior_package_blobs_preserved(self):
        self.assertEqual(len(self.scope["protected_files"]),96)
        for path,pin in self.scope["protected_files"].items():
            p=ROOT/path
            data=p.read_bytes() if p.is_file() else subprocess.check_output(["git","show","HEAD:"+path],cwd=ROOT)
            self.assertEqual(sha(data),pin["sha256"],path)
            self.assertEqual(data,blob(path),path)

    def test_03_exact_verified_native_notes(self):
        self.assertEqual(set(self.scope["public_native_note_copies"]),set(PUBLIC_NOTES))
        for name,pin in self.scope["public_native_note_copies"].items():
            data=(NOTES/name).read_bytes()
            self.assertEqual(sha(data),pin["sha256"],name)
            self.assertEqual(len(data),pin["bytes"],name)
        receipt=load(NOTES/"SOURCE-VERIFICATION.json")
        self.assertEqual((receipt["tests_run"],receipt["failures"],receipt["errors"]),(9,0,0))
        self.assertEqual((receipt["cia_complete_text_pages_checked"],receipt["mfr_complete_pages_checked"],receipt["complete_page_visual_reads"]),(14,4,11))

    def test_04_original_finding_objects_and_primary_pins(self):
        additions=self.reg["entries"][152:]
        self.assertEqual([e["original_id"] for e in additions],[f"CL{i:03}" for i in range(1,9)])
        for e,f in zip(additions,self.findings,strict=True):
            self.assertEqual(e["original_record"],f)
            self.assertEqual(e["id"],f["master_id"])
            for loc in e["locators"]:
                source=self.sources["sources"][loc["source_id"]]
                self.assertEqual(loc["source_sha256"],source["sha256"])
                self.assertEqual(loc["source_url"],source["url"])
                self.assertEqual(loc["review_report_sha256"],sha((NOTES/"REPORT.md").read_bytes()))
        self.assertEqual(self.reg["new_source_catalog"],self.sources)

    def test_05_all_questions_and_previous_targets_retained(self):
        new=load(NOTES/"OPEN-QUESTIONS.json")
        self.assertEqual(self.reg["new_open_questions"],new)
        self.assertEqual([t["id"] for t in new["targets"]],[f"CIAQ{i:03}" for i in range(1,9)])
        for f,t in zip(self.findings,new["targets"],strict=True):
            self.assertEqual(t["existing_record_target_and_test"],f["next_test"])
        self.assertEqual(self.reg["prior_open_targets"],self.old["current_open_targets"])
        self.assertEqual(len(self.reg["prior_open_targets"]["targets"]),5)
        self.assertEqual(len(self.reg["prior_open_targets"]["bank_phone_original_targets"]),10)

    def test_06_readable_master_and_inherited_body(self):
        master=(HERE/"MASTER-LIST.md").read_text()
        previous=blob(OLD+"/MASTER-LIST.md").decode()
        body=relocate(previous[previous.index("## Register\n"):])
        self.assertIn(body,master)
        self.assertEqual(re.findall(r"^### (M\d{3}) —",master,re.M),[f"M{i:03}" for i in range(1,161)])
        all_ids={e["id"] for e in self.reg["entries"]}
        for e in self.reg["entries"]:self.assertTrue(set(e["related"])<=all_ids)
        for f in self.findings:
            self.assertIn(f["observation"],master)
            self.assertIn(f["limit"],master)
            self.assertIn(f["next_test"],master)
            for q in f["conflicting_or_qualifying_records"]:self.assertIn(q,master)

    def test_07_source_excerpts_and_visual_scope(self):
        excerpts=(NOTES/"SOURCE-EXCERPTS.md").read_text()
        pins=load(NOTES/"EXCERPT-PINS.json")["excerpts"]
        self.assertEqual(len(pins),42)
        for p in pins:
            self.assertIn(f'id="{p["excerpt_id"]}"',excerpts)
            self.assertRegex(p["text_sha256"],r"^[0-9a-f]{64}$")
        visual=load(NOTES/"VISUAL-REVIEW.json")["pages"]
        self.assertEqual(len(visual),11)
        self.assertTrue(all(p["independent_visual_read_this_pass"] for p in visual))

    def test_08_access_and_adverse_or_conflicting_accounts(self):
        access=self.sources["current_access"]
        self.assertEqual(len(access),4)
        self.assertTrue(all(x["complete_response"] for x in access))
        self.assertEqual(access[0]["status"],200)
        self.assertFalse(access[0]["starts_pdf"])
        self.assertIn("system-maintenance",access[0]["final_url"])
        report=(NOTES/"REPORT.md").read_text()
        for phrase in ("five days later","eight days later","a week later","late 2002","January 2004","February 2004","appropriate format","speculation","none of the evaluated FBI employees committed misconduct","retain this particular draft"):
            self.assertTrue(phrase in report,phrase)
        self.assertNotIn("III.A.9.b",report)
        self.assertIn("Not a real-name or CIR-role authentication.",self.sources["sources"]["NARA-MFR"]["provenance_limit"])

    def test_09_relative_links_and_anchors(self):
        count=0
        for path in list(HERE.glob("*.md"))+list(NOTES.glob("*.md")):
            for target in re.findall(r"\]\(([^)]+)\)",path.read_text()):
                if target.startswith(("https:","http:")):continue
                name,_,anchor=target.partition("#")
                dest=(path.parent/unquote(name)).resolve() if name else path
                if dest.name=="VERIFICATION.json" and not dest.exists():continue
                self.assertTrue(dest.is_file(),(path.name,target))
                if anchor:self.assertIn(f'id="{anchor}"',dest.read_text(),(path.name,target))
                count+=1
        self.assertGreater(count,100)

    def test_10_text_only_reviewed_payload(self):
        pattern=re.compile(r"/(?:Users|Volumes|private)/|BEGIN [A-Z ]*PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}")
        allowed_notes=set(PUBLIC_NOTES)|{"TEXT-CHANGES.diff","MANIFEST.json"}
        allowed_master={"README.md","MASTER-LIST.md","CHECKLIST.md","SCOPE.json","register.json","build_cia_master.py","verify_cia_master.py","TEXT-CHANGES.diff","VERIFICATION.json","MANIFEST.json"}
        for folder,allowed in [(HERE,allowed_master),(NOTES,allowed_notes)]:
            for p in folder.iterdir():
                self.assertTrue(p.is_file())
                self.assertFalse(p.is_symlink())
                self.assertIn(p.name,allowed)
                self.assertLess(p.stat().st_size,16*1024*1024)
                if p.suffix!=".py":self.assertIsNone(pattern.search(p.read_text()),p.name)

    def test_11_manifests_when_present(self):
        for folder,excluded in [(HERE,{"MANIFEST.json","VERIFICATION.json"}),(NOTES,{"MANIFEST.json"})]:
            m=folder/"MANIFEST.json"
            if not m.exists():continue
            manifest=load(m)
            expected={p.name for p in folder.iterdir() if p.is_file() and p.name not in excluded}
            self.assertEqual(set(manifest["files"]),expected)
            for name,pin in manifest["files"].items():
                data=(folder/name).read_bytes()
                self.assertEqual(sha(data),pin["sha256"])
                self.assertEqual(len(data),pin["bytes"])


def record():
    previous=blob(OLD+"/MASTER-LIST.md").decode().splitlines(keepends=True)
    master=(HERE/"MASTER-LIST.md").read_text().splitlines(keepends=True)
    changes=list(difflib.unified_diff(previous,master,fromfile=OLD+"/MASTER-LIST.md",tofile=str((HERE/"MASTER-LIST.md").relative_to(ROOT))))
    for p in sorted(HERE.glob("*.md")):
        if p.name=="MASTER-LIST.md":continue
        changes.extend(difflib.unified_diff([],p.read_text().splitlines(keepends=True),fromfile="/dev/null",tofile=str(p.relative_to(ROOT))))
    write(HERE/"TEXT-CHANGES.diff","".join(changes))
    changes=[]
    for p in sorted(NOTES.glob("*.md")):
        changes.extend(difflib.unified_diff([],p.read_text().splitlines(keepends=True),fromfile="/dev/null",tofile=str(p.relative_to(ROOT))))
    write(NOTES/"TEXT-CHANGES.diff","".join(changes))
    for folder,excluded in [(HERE,{"MANIFEST.json","VERIFICATION.json"}),(NOTES,{"MANIFEST.json"})]:
        js(folder/"MANIFEST.json",{"date":"2026-10-26","self_and_master_verification_excluded":sorted(excluded),
            "files":{p.name:{"bytes":p.stat().st_size,"sha256":sha(p.read_bytes())} for p in sorted(folder.iterdir()) if p.is_file() and p.name not in excluded}})


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--record",action="store_true")
    args=parser.parse_args()
    if args.record:record()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CiaMasterChecks))
    if not result.wasSuccessful():raise SystemExit(1)
    if args.record:
        js(HERE/"VERIFICATION.json",{"date":"2026-10-26","command":"python3 -B verify_cia_master.py --record","tests_run":result.testsRun,"failures":0,"errors":0,"entries":160,"new_entries":8,"prior_entries_unchanged":152,"protected_prior_package_files":96,"separate_source_check_groups_passed":9,"scope":"Exact reviewed-note transfer, stable IDs, old source/record preservation, conflict/adverse/target retention, links and disclosure scope. Not native historical-message authentication or intent adjudication.","pdf_layout":"No new PDF generated.","remote_publication":"Not asserted by this precommit receipt; exact resulting commit and remote blobs checked separately."})
    print(json.dumps({"checks":result.testsRun,"status":"passed","entries":160}))


if __name__=="__main__":main()

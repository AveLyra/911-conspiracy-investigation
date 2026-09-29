"""Synthetic adapter controls; no historical observation records are read."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
import compare

# Retain batch 2's disclosed-rule controls and every per-asset schema control.
# Provenance metadata tests are replaced below because membership/path changed.
original = compare.legacy(())
raw_sample = ("A-873f87e7149b", "A-e1b0c06ad11d", "A-9e7b4935c8aa", "A-0b722775db93",
              "A-fa6f410444bb", "A-ffe3726a0312", "A-0e60b82a1a4c", "A-6902e91e39ee",
              "A-671f312eade8", "A-69d899e75343", "A-8bc36f05fe38", "A-7b61385d1373", "A-f1e2fa01e344")
original.SAMPLE=raw_sample
test_path=compare.BASE.with_name("test_summarize.py")
if compare.digest(test_path.read_bytes()) != "e2b971fe187d60ca81c1475dd63afa13d3b137cbbdcfa2680cd557bc6d5995a5":
    raise ValueError("batch 2 tests pin mismatch")
sys.modules["summarize"]=original
spec=importlib.util.spec_from_file_location("batch2_controls",test_path)
old_tests=importlib.util.module_from_spec(spec)
spec.loader.exec_module(old_tests)
RuleControls=old_tests.RuleControls


class SchemaControls(old_tests.SchemaControls):
    def test_provenance_pins_membership_and_structure(self):
        # Adapter-specific provenance tests below replace this old 28-asset fixture.
        self.assertEqual(len(original.SAMPLE),13)


class AdapterControls(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="fire3-controls-")
        self.root=Path(self.temp.name).resolve()
        (self.root/"assets/run01/images").mkdir(parents=True)
        self.protocol=b"Synthetic protocol, not historical evidence.\n"
        (self.root/"PROTOCOL.md").write_bytes(self.protocol)
        for name in compare.NOTE_PINS:
            (self.root/name).write_bytes((compare.HERE/name).read_bytes())
        self.assets=[]
        encoded=io.BytesIO()
        Image.new("RGB",(100,100),(0,0,0)).save(encoded,format="JPEG")
        data=encoded.getvalue()
        for i in range(25):
            aid=f"A-{i:012x}"
            path=f"assets/run01/images/{aid}.jpg"
            (self.root/path).write_bytes(data)
            self.assets.append({"asset_id":aid,"native_pdf_dimensions":[100,100],
                                "extracted_view":{"path":path,"sha256":compare.digest(data),"bytes":len(data),
                                                  "dimensions":[100,100],"format":"JPEG"}})
        self.key={"pair_asset_ids":[a["asset_id"] for a in self.assets[:2]],
                  "selected_asset_ids":[a["asset_id"] for a in self.assets],"assets":self.assets}
        self.pair={"sample_asset_ids":self.key["pair_asset_ids"],"assets":self.assets[:2]}
        self.key_hash=self.save_json("anonymous-key.json",self.key)
        self.pair_hash=self.save_json("anonymous-pair-key.json",self.pair)
        self.protocol_hash=compare.digest(self.protocol)

    def tearDown(self): self.temp.cleanup()

    def save_json(self,path,value):
        raw=(json.dumps(value,sort_keys=True)+"\n").encode()
        (self.root/path).write_bytes(raw)
        return compare.digest(raw)

    def record(self,name="synthetic-a",scope="full"):
        key=self.key if scope=="full" else self.pair
        pins=compare.validate_key(key,scope)
        module=compare.legacy(tuple(pins),self.protocol_hash,self.key_hash if scope=="full" else self.pair_hash)
        with patch.object(old_tests,"subject",module):
            return old_tests.record(name,pins)

    def build(self,scope="full"):
        return compare.build_report(["a.json","b.json"],root=self.root,scope=scope,
                                    key_hash=self.key_hash if scope=="full" else self.pair_hash,
                                    protocol_hash=self.protocol_hash)

    def labels(self,scope="full"):
        for p,n in (("a.json","synthetic-a"),("b.json","synthetic-b")):
            self.save_json(p,self.record(n,scope))

    def test_pair_and_full_counts_and_exact_repeats(self):
        for scope,n in (("pair",2),("full",25)):
            self.labels(scope)
            a,b=self.build(scope),self.build(scope)
            self.assertEqual(a,b)
            self.assertEqual(len(a["sample_asset_ids"]),n)
            self.assertEqual(len(a["comparisons"][0]["assets"]),n)
            self.assertEqual(len(a["raw_records"][0]["assets"]),n)
            compare.write_report(a,f"{scope}-one.json",root=self.root)
            compare.write_report(b,f"{scope}-two.json",root=self.root)
            self.assertEqual((self.root/f"{scope}-one.json").read_bytes(),(self.root/f"{scope}-two.json").read_bytes())

    def test_membership_duplicate_and_hash_dimension_mutations_rejected(self):
        mutations=[lambda d:d["assets"].pop(),lambda d:d["assets"].append(copy.deepcopy(d["assets"][0])),
                   lambda d:d["assets"][0].update(asset_id="unknown"),lambda d:d["assets"][0].update(image_sha256="0"*64),
                   lambda d:d["assets"][0].update(dimensions=[True,100])]
        for scope in ("pair","full"):
            for mutation in mutations:
                self.labels(scope); d=self.record(scope=scope); mutation(d); self.save_json("a.json",d)
                with self.assertRaises(ValueError): self.build(scope)

    def test_key_membership_paths_and_metadata(self):
        mutations=[lambda k:k["assets"].pop(),lambda k:k["assets"][1].update(asset_id=k["assets"][0]["asset_id"]),
                   lambda k:k["assets"][0]["extracted_view"].update(path="../escape.jpg"),
                   lambda k:k["assets"][0]["extracted_view"].update(format="PNG"),
                   lambda k:k["assets"][0]["extracted_view"].update(sha256="bad"),
                   lambda k:k["assets"][0]["extracted_view"].update(bytes=True),
                   lambda k:k["assets"][0].update(native_pdf_dimensions=[10,10]),
                   lambda k:k["pair_asset_ids"].reverse(),lambda k:k["selected_asset_ids"].reverse()]
        for mutate in mutations:
            key=copy.deepcopy(self.key); mutate(key)
            with self.assertRaises(ValueError): compare.validate_key(key)

    def test_source_pins_and_no_pixel_decoding(self):
        self.labels()
        with patch.object(Image.Image,"load",side_effect=AssertionError("pixel decode forbidden")),patch.object(Image.Image,"save",side_effect=AssertionError("save forbidden")):
            self.build()
        with self.assertRaises(ValueError):
            compare.build_report(["a.json","b.json"],root=self.root,key_hash="0"*64,protocol_hash=self.protocol_hash)
        p=self.root/self.assets[0]["extracted_view"]["path"]
        p.write_bytes(p.read_bytes()+b"altered")
        with self.assertRaises(ValueError): self.build()

    def test_wrong_header_rejected(self):
        self.labels()
        with patch.object(compare.Image,"open") as fake:
            fake.return_value.__enter__.return_value.format="JPEG"
            fake.return_value.__enter__.return_value.size=(1,1)
            with self.assertRaises(ValueError): self.build()

    def test_duplicate_json_keys_reviewers_and_nonfinite_rejected(self):
        self.labels()
        (self.root/"a.json").write_text('{"x":1,"x":2}')
        with self.assertRaises(ValueError): self.build()
        self.labels(); self.save_json("b.json",self.record())
        with self.assertRaises(ValueError): self.build()
        self.labels(); d=self.record(); d["assets"][0]["target_rect"][0]=float("nan"); self.save_json("a.json",d)
        with self.assertRaises(ValueError): self.build()

    def test_path_containment_and_symlinks(self):
        self.labels()
        for path in ("../outside.json","/etc/hosts"):
            with self.assertRaises(ValueError): compare.safe_path(self.root,path)
        (self.root/"link.json").symlink_to(self.root/"a.json")
        with self.assertRaises(ValueError): compare.build_report(["link.json","b.json"],root=self.root,key_hash=self.key_hash,protocol_hash=self.protocol_hash)
        (self.root/"linked-parent").symlink_to(self.root/"assets")
        with self.assertRaises(ValueError): compare.safe_path(self.root,"linked-parent/output.json",existing=False)
        image=self.root/self.assets[0]["extracted_view"]["path"]
        image.unlink(); image.symlink_to(self.root/self.assets[1]["extracted_view"]["path"])
        with self.assertRaises(ValueError): self.build()

    def test_existing_output_and_input_change_rejected(self):
        self.labels(); report=self.build()
        compare.write_report(report,"out.json",root=self.root)
        with self.assertRaises(FileExistsError): compare.write_report(report,"out.json",root=self.root)
        (self.root/"dangling.json").symlink_to(self.root/"absent.json")
        with self.assertRaises(ValueError): compare.write_report(report,"dangling.json",root=self.root)
        self.save_json("a.json",self.record("changed"))
        with self.assertRaises(ValueError): compare.write_report(report,"never.json",root=self.root)
        self.assertFalse((self.root/"never.json").exists())

    def test_nulls_disagreements_and_independent_oracle(self):
        self.labels(); d=self.record("synthetic-b")
        d["assets"][0].update(target_evaluability="unresolved_target",target_rect=None)
        d["assets"][1]["luminous_features"]=[old_tests.feature("ambiguous_glow")]
        d["assets"].reverse(); self.save_json("b.json",d)
        report=self.build()
        expected={(self.assets[0]["asset_id"],"target_evaluability"),(self.assets[1]["asset_id"],"ambiguous_glow_identified")}
        actual={(x["asset_id"],name) for x in report["comparisons"][0]["assets"] for name,value in x["axes"].items() if value["comparison"]=="different"}
        self.assertEqual(actual,expected)
        self.assertIsNone(report["comparisons"][0]["assets"][0]["regions_without_forced_matching"]["target_rect"]["right"])
        self.assertEqual(report["raw_records"][1],d)


if __name__=="__main__": unittest.main(verbosity=2)

"""Finite presentation tests; all generated packets/assets are synthetic."""
import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import render_packet as render


def encoded(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def fixture_packet():
    slots = []
    for panel in ("F", "E"):
        for bolt in range(3, 10):
            for q in (1, 2, 3):
                slot_id = f"CE-{panel}{bolt}Q{q}"
                slots.append({"id": slot_id, "pair": f"{panel}{bolt}", "human_accepted": False,
                              "selection_status": "unavailable_empty_primary_domain",
                              "entries": [{"id": slot_id+"-"+model, "model": model,
                                           "human_status": "uninspected", "human_response": None}
                                          for model in ("spring", "shell")]})
    assets = {}
    for name in ["page"]+[f"Im{i}" for i in range(12)]:
        raw = ("TEST ONLY source "+name).encode()
        assets[name] = {"path": "render01/page-076.png" if name == "page" else f"native-strips01/{name}.jpg",
                        "url": "/page.png" if name == "page" else f"/source/{name}.jpg",
                        "sha256": render.sha(raw), "bytes": len(raw),
                        "width": 1700 if name == "page" else 741,
                        "height": 2200 if name == "page" else 88}
    return {"version": 2, "packet_id": render.PACKET_ID,
            "status": "conditional_mapping_packet_pending_human", "human_accepted": False,
            "actual_D": None, "model_discrepancies": None,
            "domain_kind": "C_H_primary_primary_not_actual_D",
            "assumptions": ["Hidentity", "Hsupport", "Hink0"],
            "slots": slots, "assets": assets, "summary": {"synthetic_fixture_only": True}}


class PresentationTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture_packet()
        self.digest = render.sha(encoded(self.data))

    def test_deterministic_identity_and_nonmutating_projection(self):
        saved = copy.deepcopy(self.data)
        first = render.presentation_bytes(self.data, self.digest)
        self.assertEqual(first, render.presentation_bytes(self.data, self.digest))
        self.assertEqual(self.data, saved)
        projected = json.loads(first.removeprefix(b"export const PACKET = ").removesuffix(b";\n"))
        self.assertEqual(projected["version"], 2)
        self.assertEqual(projected["packet_id"], render.PACKET_ID)
        self.assertEqual(projected["packet_sha256"], self.digest)
        self.assertTrue(all("path" not in a for a in projected["assets"].values()))
        self.assertEqual(len(projected["slots"]), 42)
        self.assertEqual(sum(len(s["entries"]) for s in projected["slots"]), 84)
        self.assertTrue(all(e["human_status"] == "uninspected" for s in projected["slots"] for e in s["entries"]))

    def test_version_id_and_full_hash_required(self):
        for key, value in [("version", 1), ("version", True), ("version", 2.0), ("packet_id", "old")]:
            bad = copy.deepcopy(self.data); bad[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                render.presentation_bytes(bad, self.digest)
        for digest in ("short", "A"*64, "0"*63, ""):
            with self.subTest(digest=digest), self.assertRaises(ValueError):
                render.presentation_bytes(self.data, digest)

    def test_old_acceptance_is_not_carried(self):
        variants = []
        for key,value in [("human_accepted",True),("actual_D",[]),("model_discrepancies",{})]:
            bad=copy.deepcopy(self.data);bad[key]=value;variants.append(bad)
        bad=copy.deepcopy(self.data);bad["slots"][0]["human_accepted"]=True;variants.append(bad)
        for key,value in [("human_status","agree with mapping"),("human_response",{}),("human_status",None)]:
            bad=copy.deepcopy(self.data);bad["slots"][0]["entries"][0][key]=value;variants.append(bad)
        for bad in variants:
            with self.assertRaises(ValueError):render.presentation_bytes(bad,self.digest)

    def test_exact_slot_and_entry_order(self):
        for kind in ("missing","reordered","duplicate","entry"):
            bad=copy.deepcopy(self.data)
            if kind=="missing":bad["slots"].pop()
            if kind=="reordered":bad["slots"].reverse()
            if kind=="duplicate":bad["slots"][1]=bad["slots"][0]
            if kind=="entry":bad["slots"][0]["entries"].reverse()
            with self.subTest(kind=kind),self.assertRaises(ValueError):
                render.presentation_bytes(bad,self.digest)

    def test_complete_fixed_source_routes_and_paths(self):
        for key,value in [("url","/review.mjs"),("path","../secret"),("path","/tmp/secret"),("width",True),("height",0),("bytes",-1),("sha256","short")]:
            bad=copy.deepcopy(self.data);bad["assets"]["Im0"][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                render.presentation_bytes(bad,self.digest)
        bad=copy.deepcopy(self.data);del bad["assets"]["Im11"]
        with self.assertRaises(ValueError):render.presentation_bytes(bad,self.digest)

    def test_nonfinite_serialization_rejected(self):
        bad=copy.deepcopy(self.data);bad["summary"]["bad"]=float("nan")
        with self.assertRaises(ValueError):render.presentation_bytes(bad,self.digest)

    def test_pair_requires_frozen_hash_and_equal_bytes(self):
        with TemporaryDirectory(prefix="f7-viewer-pair-") as tmp:
            here=Path(tmp);raw=encoded(self.data)
            for name in ("packet01.json","packet02.json"):(here/name).write_bytes(raw)
            self.assertEqual(render.load_pair(here,self.digest)[0],self.data)
            with self.assertRaisesRegex(ValueError,"not frozen"):render.load_pair(here,"PENDING")
            (here/"packet02.json").write_bytes(raw+b" ")
            with self.assertRaisesRegex(ValueError,"identity mismatch"):render.load_pair(here,self.digest)

    def test_duplicate_keys_and_nonfinite_input_rejected(self):
        with TemporaryDirectory(prefix="f7-viewer-json-") as tmp:
            here=Path(tmp)
            for raw in (b'{"x":1,"x":2}',b'{"x":NaN}'):
                for name in ("packet01.json","packet02.json"):(here/name).write_bytes(raw)
                with self.assertRaises(ValueError):render.load_pair(here,render.sha(raw))

    def test_exclusive_output_preserves_first_bytes(self):
        with TemporaryDirectory(prefix="f7-viewer-exclusive-") as tmp:
            path=Path(tmp)/"synthetic.mjs"
            render.save_exclusive(path,b"TEST ONLY")
            with self.assertRaises(FileExistsError):render.save_exclusive(path,b"second")
            self.assertEqual(path.read_bytes(),b"TEST ONLY")

    def test_source_symlink_refused(self):
        with TemporaryDirectory(prefix="f7-viewer-symlink-") as tmp:
            here=Path(tmp);target=here/"target";target.write_bytes(b"TEST")
            link=here/"link";link.symlink_to(target)
            with self.assertRaisesRegex(ValueError,"symlink"):render.pinned(link,render.sha(b"TEST"))


if __name__=="__main__":
    unittest.main()


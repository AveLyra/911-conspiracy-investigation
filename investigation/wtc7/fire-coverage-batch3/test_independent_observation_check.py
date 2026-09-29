"""Synthetic controls for the independent standard-library observer checker."""
import copy
import json
import struct
import unittest
import independent_observation_check as checker


def fixture(n=2):
    members={f"A-{i:012x}":{"sha256":"a"*64,"dimensions":[10,10]} for i in range(n)}
    records=[]
    for reviewer in ("synthetic-a","synthetic-b"):
        records.append({"reviewer":reviewer,"independence":"Synthetic only","protocol_sha256":checker.PINS["PROTOCOL.md"],"provenance_key_sha256":"b"*64,
                        "assets":[{"asset_id":aid,"image_sha256":"a"*64,"dimensions":[10,10],"complete_native_image_inspected":True,
                                   "target_rect":[0,0,10,10],"target_evaluability":"partial_detail","target_reason":"Synthetic framing limit.",
                                   "luminous_features":[],"smoke":{"status":"not_identified","regions":[],"reason":"Synthetic nondetection."},
                                   "nondetection_regions":[],"visibility_limits":["Synthetic only"],"overlay_regions":[]} for aid in members]})
    return members,records


class IndependentControls(unittest.TestCase):
    def test_exact_counts_membership_and_duplicates(self):
        for n in (2,25):
            members,records=fixture(n)
            self.assertEqual(len(checker.validate(records[0],members,"b"*64)),n)
            for kind in ("missing","duplicate","unknown"):
                r=copy.deepcopy(records[0])
                if kind=="missing":r["assets"].pop()
                elif kind=="duplicate":r["assets"][1]=copy.deepcopy(r["assets"][0])
                else:r["assets"][0]["asset_id"]="unknown"
                with self.assertRaises(ValueError):checker.validate(r,members,"b"*64)

    def test_pin_schema_numeric_reason_and_consistency_failures(self):
        mutations=[lambda a:a.update(image_sha256="0"*64),lambda a:a.update(dimensions=[True,10]),lambda a:a.update(complete_native_image_inspected=1),
                   lambda a:a.update(target_rect=[False,0,10,10]),lambda a:a.update(target_rect=[0,0,11,10]),lambda a:a.update(target_rect=[0,0,float("inf"),10]),
                   lambda a:a.update(target_rect=None),lambda a:a.update(target_evaluability="unresolved_target"),lambda a:a.update(target_reason=" "),
                   lambda a:a.update(visibility_limits=[]),lambda a:a.update(invented_score=1),lambda a:a["smoke"].update(status="visible"),
                   lambda a:a["smoke"].update(regions=[[0,0,1,1]])]
        for mutate in mutations:
            members,records=fixture(); mutate(records[0]["assets"][0])
            with self.assertRaises(ValueError):checker.validate(records[0],members,"b"*64)

    def test_all_axes_coexist_nulls_and_rectangles_preserved(self):
        members,records=fixture(); a=records[1]["assets"][0]
        a.update(target_rect=None,target_evaluability="unresolved_target")
        a["luminous_features"]=[{"rect":[1,1,2,2],"appearance":appearance,"target_relation":"uncertain","reason":"Synthetic feature.","alternatives":["Reflection."]} for appearance in ("flame_like","ambiguous_glow")]
        a["smoke"]={"status":"visible","regions":[[0,0,10,10]],"reason":"Synthetic veil."}
        a["nondetection_regions"]=[{"rect":[2,2,3,3],"reason":"Bounded synthetic opportunity."}]
        rows=[checker.validate(r,members,"b"*64) for r in records]
        result=checker.recompute(*rows,members)
        self.assertEqual(sum(not x["same"] for x in result[0]["axes"].values()),5)
        self.assertIsNone(result[0]["all_observation_fields"]["target_rect"]["right"])
        self.assertEqual(result[0]["all_observation_fields"]["luminous_features"]["right"],a["luminous_features"])
        self.assertTrue(all(x["same"] for x in result[1]["axes"].values()))

    def test_pair_carry_forward_rejects_changed_reason_or_rectangle(self):
        members,records=fixture(); pair=checker.validate(records[0],members,"b"*64)
        self.assertTrue(all(checker.carry_forward(pair,copy.deepcopy(pair)).values()))
        for field,value in (("target_reason","Changed"),("target_rect",[0,0,9,10])):
            full=copy.deepcopy(pair);full[next(iter(full))][field]=value
            with self.assertRaises(ValueError):checker.carry_forward(pair,full)

    def test_json_duplicate_keys_and_nonfinite(self):
        for raw in ('{"x":1,"x":2}','{"a":{"x":1,"x":2}}','{"a":NaN}','{"a":1e999}'):
            with self.assertRaises(ValueError):checker.parse(raw)

    def test_jpeg_header_dimensions_without_pixel_decoder(self):
        header=b"\xff\xd8\xff\xc0"+struct.pack(">HBHHB",8,8,37,975,3)+b"\xff\xd9"
        self.assertEqual(checker.jpeg_dimensions(header),[975,37])
        for raw in (b"not JPEG",header[:7],b"\xff\xd8\xff\xda\x00\x02"):
            with self.assertRaises(ValueError):checker.jpeg_dimensions(raw)

    def test_producer_contract_and_mutated_comparison(self):
        members,records=fixture();rows=[checker.validate(r,members,"b"*64) for r in records]
        recomputed=checker.recompute(*rows,members)
        report={"scope":"pair","batch":3,"schema_version":2,"sample_asset_ids":list(members),"raw_records":records,
                "source_hashes":{"protocol_sha256":checker.PINS["PROTOCOL.md"],"provenance_key_sha256":"b"*64},
                "comparisons":[{"left_reviewer":"synthetic-a","right_reviewer":"synthetic-b","assets":checker.producer_shape(recomputed,*rows)}]}
        self.assertTrue(checker.verify_producer(report,records,recomputed,members,"pair","b"*64))
        report["comparisons"][0]["assets"][0]["axes"]["flame_like_identified"]["right"]=True
        with self.assertRaises(ValueError):checker.verify_producer(report,records,recomputed,members,"pair","b"*64)


if __name__=="__main__":unittest.main(verbosity=2)

"""Dense selection/control-gate tests; synthetic metadata only."""
import copy
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest

DRIVER=None
PARENT=None


def fixture():
    return [{'source_index':i,'png':f'{i}.png','source_pts':i*1001,
        'source_time_base':'1/30000','source_seconds_exact':str(Fraction(i*1001,30000))} for i in range(300,540)]


class DenseControls(unittest.TestCase):
    def test_equal_content_preserves_distinct_presented_indices(self):
        rows=fixture()
        for row in rows:
            row.update(sha256='a'*64,bytes=1234)
        selected=DRIVER.dense_rows(PARENT,rows)
        self.assertEqual(len(selected),240)
        self.assertEqual([r['source_index'] for r in selected],list(range(300,540)))
        self.assertEqual(len({(r['sha256'],r['bytes']) for r in selected}),1)
        self.assertEqual(selected,rows)

    def test_exact_selection_and_endpoints(self):
        rows=DRIVER.dense_rows(PARENT,fixture())
        self.assertEqual(len(rows),240)
        self.assertEqual(Fraction(rows[0]['source_seconds_exact']),Fraction(1001,100))
        self.assertEqual(Fraction(rows[-1]['source_seconds_exact']),Fraction(539539,30000))
        self.assertEqual([r['source_index'] for r in rows],list(range(300,540)))

    def test_missing_duplicate_extra_reordering(self):
        rows=fixture()
        for bad in (rows[:-1],rows+[rows[0]],rows[::-1],rows[:-1]+[rows[0]]):
            with self.assertRaises(ValueError):DRIVER.dense_rows(PARENT,bad)

    def test_malformed_pts_and_types(self):
        for key,value in [('source_pts',300300.0),('source_pts',True),('source_pts',300301),('source_time_base','1/29970'),('source_seconds_exact','10'),('source_index',True)]:
            rows=fixture();rows[0][key]=value
            with self.assertRaises(ValueError):DRIVER.dense_rows(PARENT,rows)
        rows=fixture();rows[0]['png']='../escape.png'
        with self.assertRaises(ValueError):DRIVER.dense_rows(PARENT,rows)

    def test_references_membership_and_pts(self):
        rows=[{'source_index':i,'png':f'{i}.png','source_pts':i*512,'source_time_base':'1/15360','source_seconds_exact':str(Fraction(i,30))} for i in [12900,12960,13020]]
        self.assertEqual(len(DRIVER.reference_rows(PARENT,rows)),3)
        with self.assertRaises(ValueError):DRIVER.reference_rows(PARENT,rows[:-1])
        rows[0]['source_seconds_exact']='429'
        with self.assertRaises(ValueError):DRIVER.reference_rows(PARENT,rows)

    def test_cartesian_coverage(self):
        rows=[{'reference_index':r,'source_index':i} for r in [12900,12960,13020] for i in range(300,540)]
        DRIVER.verify_pairs(rows)
        for bad in (rows[:-1],rows[:-1]+[rows[0]],rows+[rows[0]]):
            with self.assertRaises(ValueError):DRIVER.verify_pairs(bad)

    def test_bands_ties_and_endpoints(self):
        self.assertEqual(DRIVER.bands([304,300,301,301,303]),[[300,301],[303,304]])
        rows=[{'reference_index':r,'source_index':i,'transforms':[{'static_score':.8,'dynamic':{'score':None}}]} for r in [12900,12960,13020] for i in (300,301,303)]
        rank=DRIVER.rankings(PARENT,rows)['12900']
        self.assertEqual(rank['static']['exact_best_ties'],[300,301,303])
        self.assertEqual(rank['static']['near_best_bands']['0.005'],[[300,301],[303,303]])
        self.assertTrue(rank['static']['endpoint_leader'])
        self.assertFalse(rank['dynamic']['endpoint_leader'])

    def test_hash_and_output_refusal(self):
        with tempfile.TemporaryDirectory(prefix='dense-pins-') as d:
            p=Path(d)/'data';p.write_bytes(b'synthetic')
            self.assertEqual(DRIVER.checked({'path':str(p),**DRIVER.pin(p)}),p)
            with self.assertRaises(ValueError):DRIVER.checked({'path':str(p),'sha256':'0'*64})
            with self.assertRaises(ValueError):DRIVER.checked({'path':str(p)})
            with self.assertRaises(FileNotFoundError):DRIVER.checked({'path':str(p)+'missing','sha256':'0'*64})
            out=Path(d)/'fresh';out.mkdir()
            with self.assertRaises(FileExistsError):out.mkdir(exist_ok=False)
            PARENT.save(out/'x.json',{})
            with self.assertRaises(FileExistsError):PARENT.save(out/'x.json',{})
        for mode,name in [('screen','screen03'),('screen','../screen01'),('controls','screen01'),('bad','controls01')]:
            with self.assertRaises(ValueError):DRIVER.run_name(mode,name)

    def test_gate_state_products_and_required_counts(self):
        with tempfile.TemporaryDirectory(prefix='dense-gate-') as d:
            p=Path(d);state={'synthetic':'frozen'}
            q={'pass':True,'dense_tests':8,'parent_tests':9,'inherited':{'controls':11,'pass':True}}
            PARENT.save(p/'controls.json',q)
            rec={'mode':'controls','status':'complete','before':state,'after':state,'products':{'controls.json':DRIVER.pin(p/'controls.json')}}
            PARENT.save(p/'receipt.json',rec);DRIVER.gate(PARENT,p,state)
            with self.assertRaises(ValueError):DRIVER.gate(PARENT,p,{'changed':True})
            q['parent_tests']=8;(p/'controls.json').write_text(json.dumps(q))
            with self.assertRaises(ValueError):DRIVER.gate(PARENT,p,state)
            rec['products']['controls.json']=DRIVER.pin(p/'controls.json');(p/'receipt.json').write_text(json.dumps(rec))
            with self.assertRaises(ValueError):DRIVER.gate(PARENT,p,state)

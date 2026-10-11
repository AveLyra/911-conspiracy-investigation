"""Synthetic contract tests, not fixtures extracted from historical annotations."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import compare as c


def fixture(region='F5-Im3'):
    pair,source=region.split('-');box=c.TARGETS[region];cb=c.CONTEXTS[region]
    d={'region_id':region,'pair':pair,'source':source+'.jpg','reader':'primary',
       'target_box':box.copy(),'context_box':cb.copy(),
       'coverage':{'full_context_inspected':True,'raw_context_cells':(cb[2]-cb[0])*(cb[3]-cb[1]),
       'raw_blocks':[{'columns':[cb[0],cb[2]-1],'receipt':'synthetic'}],'uncompleted_context':[]},
       'human_accepted':False,'physical_support':None,'routes':{},'unassigned_bands':[]}
    for route in ('solid','dash'):
        d['routes'][route]=[{'x':x,'core':[],'fringe':[],'fragment_id':None,
          'fragment_membership':[],'status':'no_attributable_cells','reason':'Synthetic empty',
          'boundary_flags':[],'unassigned_band_refs':[]} for x in range(box[0],box[2])]
    return d


def select(r,core,fringe):
    r.update(core=core,fringe=fringe,fragment_id='fixture',
      fragment_membership=[{'fragment_id':'fixture','core':core,'fringe':fringe}],
      status='identified_local_fragment')


class Contracts(unittest.TestCase):
    def setUp(self):self.h,self.v,self.a=c.helpers();self.d=fixture()
    def check(self,d):return c.validate(d,d['region_id'],'primary',self.h,self.a)
    def test_both_empty_geometries(self):self.check(self.d);self.check(fixture('F6-Im1'))
    def test_original_preserved(self):
        old=copy.deepcopy(self.d);self.check(self.d);self.assertEqual(old,self.d)
    def test_exact_peer_alias_only_for_peer(self):
        self.d['reader']='force56_peer';old=copy.deepcopy(self.d)
        c.validate(self.d,'F5-Im3','peer',self.h,self.a)
        self.assertEqual(old,self.d)
        with self.assertRaises(ValueError):self.check(self.d)
    def test_unknown_peer_alias_rejected(self):
        self.d['reader']='some_peer'
        with self.assertRaises(ValueError):c.validate(self.d,'F5-Im3','peer',self.h,self.a)
    def test_source_mismatch(self):
        self.d['source']='Im10.jpg'
        with self.assertRaises(ValueError):self.check(self.d)
    def test_row87_boundary(self):
        r=self.d['routes']['solid'][1];select(r,[87],[])
        r.update(status='boundary_truncated',boundary_flags=['target_bottom']);self.check(self.d)
    def test_row88_rejected(self):
        select(self.d['routes']['solid'][1],[88],[])
        with self.assertRaises(ValueError):self.check(self.d)
    def test_f6_target_y_bound(self):
        d=fixture('F6-Im1');select(d['routes']['solid'][1],[54],[])
        with self.assertRaises(ValueError):self.check(d)
    def test_missing_column(self):
        self.d['routes']['solid'].pop()
        with self.assertRaises(ValueError):self.check(self.d)
    def test_membership_loss(self):
        r=self.d['routes']['solid'][1];select(r,[60],[]);r['fragment_membership']=[]
        with self.assertRaises(ValueError):self.check(self.d)
    def test_duplicate_ink(self):
        for route in ('solid','dash'):select(self.d['routes'][route][1],[60],[])
        with self.assertRaises(ValueError):self.check(self.d)
    def test_partial_raw_read(self):
        self.d['coverage']['raw_blocks'][0]['columns'][0]+=1
        with self.assertRaises(ValueError):self.check(self.d)
    def test_uninspected(self):
        self.d['coverage']['full_context_inspected']=False
        with self.assertRaises(ValueError):self.check(self.d)
    def test_orphan(self):
        self.d['routes']['solid'][1]['unassigned_band_refs']=['missing']
        with self.assertRaises(ValueError):self.check(self.d)
    def test_multiple_bands_reciprocal(self):
        for route,y in [('solid',60),('dash',70)]:
            b=copy.deepcopy(self.d['routes'][route][1]);select(b,[y],[])
            b.update(band_id=route,candidate_routes=[route]);self.d['unassigned_bands'].append(b)
            self.d['routes'][route][1].update(status='identity_conflict',unassigned_band_refs=[route])
        old=copy.deepcopy(self.d);bands=self.check(self.d)
        self.assertEqual(len(bands[311]),2);self.assertEqual(old,self.d)
        self.d['routes']['dash'][1]['unassigned_band_refs']=['solid']
        with self.assertRaises(ValueError):self.check(self.d)
    def test_missing_reciprocal(self):
        b=copy.deepcopy(self.d['routes']['solid'][1]);select(b,[60],[])
        b.update(band_id='test',candidate_routes=['solid']);self.d['unassigned_bands']=[b]
        with self.assertRaises(ValueError):self.check(self.d)
    def test_set_arithmetic(self):
        self.assertEqual(self.h.operations({1,2},{2,3}),{'intersection':[2],'union':[1,2,3],
          'primary_only':[1],'peer_only':[3],'symmetric_difference':[1,3]})
    def test_recursive_pins_and_conflict(self):
        with tempfile.TemporaryDirectory(prefix='force56-deps-') as tmp:
            base=Path(tmp);leaf=base/'leaf.txt';leaf.write_text('synthetic')
            mid=base/'mid.json';mid.write_text(json.dumps({'inputs':{'leaf.txt':c.pin(leaf)}}))
            top=base/'top.json';top.write_text(json.dumps({'inputs':{'mid.json':c.pin(mid)}}))
            deps={};c.collect(top,c.pin(top),deps);self.assertEqual(len(deps),3)
            leaf.write_text('changed')
            with self.assertRaises(ValueError):c.collect(top,c.pin(top),{})
            with self.assertRaises(ValueError):c.collect(leaf,c.pin(leaf),deps)


if __name__=='__main__':unittest.main()

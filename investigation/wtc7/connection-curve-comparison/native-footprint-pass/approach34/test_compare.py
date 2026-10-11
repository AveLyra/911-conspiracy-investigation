"""Synthetic contract checks only: no historical annotations as fixtures."""
import copy
import unittest
import compare as c


def fixture():
    d={'region_id':'E3-Im10','pair':'E3','source':'Im10.jpg','reader':'primary',
       'target_box':[195,35,365,92],'context_box':[193,33,367,92],
       'coverage':{'full_context_inspected':True,'raw_context_cells':10266,
         'raw_blocks':[{'columns':[193,366],'receipt':'synthetic'}]},'human_accepted':False,
       'physical_support':None,'routes':{},'unassigned_bands':[]}
    for route in ('solid','dash'):
        d['routes'][route]=[{'x':x,'core':[],'fringe':[],'fragment_id':None,
         'fragment_membership':[],'status':'no_attributable_cells','reason':'Synthetic empty',
         'boundary_flags':[],'unassigned_band_refs':[]} for x in range(195,365)]
    return d


def select(r,core,fringe):
    r.update(core=core,fringe=fringe,fragment_id='fixture',
      fragment_membership=[{'fragment_id':'fixture','core':core,'fringe':fringe}],
      status='identified_local_fragment')


class Contracts(unittest.TestCase):
    def setUp(self):
        self.h,self.v=c.helpers();self.d=fixture()
    def check(self,d):return c.validate(d,'E3-Im10','primary',self.h,self.v)
    def test_empty_coverage(self):self.check(self.d)
    def test_adapter_preserves_original(self):
        old=copy.deepcopy(self.d);c.adapted(self.d);self.assertEqual(old,self.d)
    def test_row91_valid_boundary(self):
        r=self.d['routes']['solid'][1];select(r,[91],[])
        r.update(status='boundary_truncated',boundary_flags=['target_bottom']);self.check(self.d)
    def test_row92_rejected(self):
        select(self.d['routes']['solid'][1],[92],[])
        with self.assertRaises(ValueError):self.check(self.d)
    def test_partial_coverage_rejected(self):
        self.d['routes']['solid'].pop()
        with self.assertRaises(ValueError):self.check(self.d)
    def test_membership_loss_rejected(self):
        r=self.d['routes']['solid'][1];select(r,[60],[]);r['fragment_membership']=[]
        with self.assertRaises(ValueError):self.check(self.d)
    def test_duplicate_model_ink_rejected(self):
        for route in ('solid','dash'):select(self.d['routes'][route][1],[60],[])
        with self.assertRaises(ValueError):self.check(self.d)
    def test_orphan_ref_rejected(self):
        self.d['routes']['solid'][1]['unassigned_band_refs']=['missing']
        with self.assertRaises(ValueError):self.check(self.d)
    def test_route_specific_conflict(self):
        b=copy.deepcopy(self.d['routes']['solid'][1]);select(b,[60],[])
        b.update(status='identity_conflict',band_id='fixture',candidate_routes=['solid'])
        self.d['unassigned_bands']=[b]
        r=self.d['routes']['solid'][1];r.update(status='identity_conflict',unassigned_band_refs=['fixture'])
        self.check(self.d)
        self.d['routes']['dash'][1].update(status='identity_conflict',unassigned_band_refs=['fixture'])
        with self.assertRaises(ValueError):self.check(self.d)
    def test_missing_reciprocal_rejected(self):
        b=copy.deepcopy(self.d['routes']['solid'][1]);select(b,[60],[])
        b.update(status='identity_conflict',band_id='fixture',candidate_routes=['solid'])
        self.d['unassigned_bands']=[b]
        with self.assertRaises(ValueError):self.check(self.d)
    def test_uninspected_rejected(self):
        self.d['coverage']['full_context_inspected']=False
        with self.assertRaises(ValueError):self.check(self.d)
    def test_unassigned_local_ink_status_adapter(self):
        b=copy.deepcopy(self.d['routes']['solid'][1]);select(b,[60],[])
        b.update(band_id='fixture',candidate_routes=['solid'])
        self.d['unassigned_bands']=[b]
        self.d['routes']['solid'][1].update(status='identity_conflict',unassigned_band_refs=['fixture'])
        original=copy.deepcopy(self.d);self.check(self.d)
        self.assertEqual(self.d,original)
        b['status']='fringe_only'
        with self.assertRaises(ValueError):self.check(self.d)
    def test_multiple_route_specific_bands_retained(self):
        for route,y in [('solid',60),('dash',70)]:
            b=copy.deepcopy(self.d['routes'][route][1]);select(b,[y],[])
            b.update(band_id=route,candidate_routes=[route])
            self.d['unassigned_bands'].append(b)
            self.d['routes'][route][1].update(status='identity_conflict',unassigned_band_refs=[route])
        bands=self.check(self.d);self.assertEqual(len(bands[196]),2)
        self.d['routes']['dash'][1]['unassigned_band_refs']=['solid']
        with self.assertRaises(ValueError):self.check(self.d)
    def test_incomplete_actual_read_blocks_rejected(self):
        self.d['coverage']['raw_blocks'][0]['columns']=[194,366]
        with self.assertRaises(ValueError):self.check(self.d)
    def test_set_operations(self):
        self.assertEqual(self.h.operations({1,2},{2,3}),
          {'intersection':[2],'union':[1,2,3],'primary_only':[1],
           'peer_only':[3],'symmetric_difference':[1,3]})


if __name__=='__main__':unittest.main()

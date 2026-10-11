import copy
import unittest
from compare_force45 import validate, rows, operations, comparison, visible_geometry, members, TARGETS, CONTEXTS


def fixture(region='F4-Im4',role='primary'):
    x0,_,x1,_ = TARGETS[region]
    def r(x):
        return {'x':x,'core':[],'fringe':[],'fragment_id':None,'status':'no_attributable_cells',
                'boundary_flags':[],'band_refs':[],'note':'Synthetic empty observation.'}
    return {'pair':region.split('-')[0],'region_id':region,'source_image':region.split('-')[1]+'.jpg',
            'reader':role,'target_box':list(TARGETS[region]),'context_box':list(CONTEXTS[region]),
            'human_accepted':False,'physical_support':None,
            'routes':{k:[r(x) for x in range(x0,x1)] for k in ('solid','dash')},'unassigned_bands':[]}


def selected(x,core,fringe=None,identity='s'):
    return {'x':x,'core':core,'fringe':fringe or [],'fragment_id':identity,
            'status':'identified_local_fragment' if core else 'fringe_only','boundary_flags':[],'band_refs':[],
            'note':'Synthetic selected ink.'}


class Tests(unittest.TestCase):
    def test_all_region_contracts(self):
        for rid in TARGETS: self.assertEqual(validate(fixture(rid),rid,'primary'),{})
    def test_same_pair_regions_not_interchangeable(self):
        with self.assertRaises(ValueError): validate(fixture('F5-Im2'),'F5-Im4')
    def test_wrong_source(self):
        d=fixture('F5-Im2');d['source_image']='Im4.jpg'
        with self.assertRaises(ValueError): validate(d)
    def test_wrong_pair(self):
        d=fixture();d['pair']='F5'
        with self.assertRaises(ValueError): validate(d)
    def test_wrong_role(self):
        with self.assertRaises(ValueError): validate(fixture(),role='peer')
    def test_boolean_box(self):
        d=fixture();d['target_box'][1]=False
        with self.assertRaises(ValueError): validate(d)
    def test_boolean_row(self):
        with self.assertRaises(ValueError): rows({'core':[True],'fringe':[]})
    def test_boolean_column(self):
        d=fixture();d['routes']['solid'][0]['x']=True
        with self.assertRaises(ValueError): validate(d)
    def test_missing_column(self):
        d=fixture();d['routes']['solid'].pop()
        with self.assertRaises(ValueError): validate(d)
    def test_class_overlap(self):
        with self.assertRaises(ValueError): rows({'core':[3],'fringe':[3]})
    def test_unsorted(self):
        with self.assertRaises(ValueError): rows({'core':[5,3],'fringe':[]})
    def test_outside_target_y(self):
        d=fixture('F5-Im2');d['routes']['solid'][2]=selected(227,[49])
        with self.assertRaises(ValueError): validate(d)
    def test_missing_boundary(self):
        d=fixture();d['routes']['solid'][0]=selected(330,[5])
        with self.assertRaises(ValueError): validate(d)
    def test_fringe_only_bottom_truncated(self):
        d=fixture();r=selected(332,[],[87]);r.update(status='boundary_truncated',boundary_flags=['target_bottom'])
        d['routes']['solid'][2]=r; validate(d)
    def test_false_truncation(self):
        d=fixture();d['routes']['solid'][2]=selected(332,[5]);d['routes']['solid'][2]['status']='boundary_truncated'
        with self.assertRaises(ValueError): validate(d)
    def test_multi_fragment_union(self):
        r=selected(332,[4,9],[3,10],None)
        r['fragments']=[{'fragment_id':'a','core':[4],'fringe':[3]}, {'fragment_id':'b','core':[9],'fringe':[10]}]
        d=fixture();d['routes']['solid'][2]=r;validate(d)
    def test_bad_fragment_union(self):
        r=selected(332,[4,9],[3,10],None);r['fragments']=[{'fragment_id':'a','core':[4],'fringe':[3]}]
        with self.assertRaises(ValueError): members(r)
    def test_duplicate_fragment_cells(self):
        r=selected(332,[4],[],None)
        r['fragments']=[{'fragment_id':'a','core':[4],'fringe':[]},{'fragment_id':'b','core':[],'fringe':[4]}]
        with self.assertRaises(ValueError): members(r)
    def test_fictitious_merged_fragment_id(self):
        r=selected(332,[4,9],[], 'merged')
        r['fragments']=[{'fragment_id':'a','core':[4],'fringe':[]},{'fragment_id':'b','core':[9],'fringe':[]}]
        with self.assertRaises(ValueError): members(r)
    def test_same_column_band_reference(self):
        d=fixture();b=selected(332,[6],identity='u');b['status']='identity_conflict';b['band_id']='band332'
        d['unassigned_bands']=[b];r=d['routes']['solid'][2];r.pop('band_refs');r['unassigned_band_refs']=[{'x':332,'band_id':'band332'}]
        self.assertIn(332,validate(d))
    def test_wrong_column_reference(self):
        d=fixture();b=selected(332,[6],identity='u');b['status']='identity_conflict';d['unassigned_bands']=[b]
        d['routes']['solid'][3]['band_refs']=['u']
        with self.assertRaises(ValueError): validate(d)
    def test_unassigned_model_duplicate(self):
        d=fixture();b=selected(332,[6],identity='u');b['status']='identity_conflict';d['unassigned_bands']=[b]
        d['routes']['solid'][2]=selected(332,[6])
        with self.assertRaises(ValueError): validate(d)
    def test_duplicate_model_ink(self):
        d=fixture()
        for route in d['routes']: d['routes'][route][2]=selected(332,[6])
        with self.assertRaises(ValueError): validate(d)
    def test_empty_is_not_missing(self):
        d=fixture();b=copy.deepcopy(d['routes']['solid'][2]);d['unassigned_bands']=[b]
        bs=validate(d);self.assertIn(332,bs);self.assertNotIn(333,bs)
    def test_reference_to_empty_band_rejected(self):
        d=fixture();b=copy.deepcopy(d['routes']['solid'][2]);b['band_id']='empty'
        d['unassigned_bands']=[b];d['routes']['solid'][2]['band_refs']=['empty']
        with self.assertRaises(ValueError): validate(d)
    def test_all_five_operations(self):
        self.assertEqual(operations({1,3},{3,5}),{'intersection':[3],'union':[1,3,5],
            'primary_only':[1],'peer_only':[5],'symmetric_difference':[1,5]})
    def test_holes_preserved(self): self.assertEqual(operations({1,3},{3})['primary_only'],[1])
    def test_class_swap_outer_same(self):
        result=comparison({'core':[2],'fringe':[3]}, {'core':[3],'fringe':[2]})
        self.assertEqual(result['outer']['symmetric_difference'],[])
        self.assertEqual(result['core']['symmetric_difference'],[2,3])
    def test_named_role_order(self):
        a,b=fixture(),fixture(role='peer');a['routes']['solid'][2]=selected(332,[4]);b['routes']['solid'][2]=selected(332,[5])
        bands={'primary':validate(a),'peer':validate(b)}
        x=visible_geometry({'primary':a,'peer':b},bands,330,425)
        self.assertEqual(x,visible_geometry({'peer':b,'primary':a},bands,330,425))
        self.assertEqual(x[2]['sets']['core']['primary_only'],[4])
        self.assertEqual(x[2]['sets']['core']['peer_only'],[5])
    def test_no_human_promotion(self):
        d=fixture();d['human_accepted']=True
        with self.assertRaises(ValueError): validate(d)
    def test_missing_reason(self):
        d=fixture();d['routes']['solid'][0]['note']=' '
        with self.assertRaises(ValueError): validate(d)


if __name__=='__main__': unittest.main()

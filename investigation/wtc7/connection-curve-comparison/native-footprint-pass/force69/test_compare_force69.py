"""Synthetic-only controls for the fixed next-batch adapter and references."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import compare_force69 as C


def fixture(region='F6-Im2', role='primary'):
    box = C.TARGETS[region]
    def row(x):
        return {'x':x,'core':[],'fringe':[],'fragment_id':None,
                'status':'no_attributable_cells','boundary_flags':[],
                'band_refs':[],'note':'Synthetic empty selection, not absent physical support.'}
    return {'region_id':region,'pair':region.split('-')[0],
            'source_image':region.split('-')[1]+'.jpg','reader':role,
            'target_box':list(box),'context_box':list(C.CONTEXTS[region]),
            'routes':{route:[row(x) for x in range(box[0],box[2])] for route in ('solid','dash')},
            'unassigned_bands':[],'human_accepted':False,'physical_support':None}


def conflict_fixture():
    data = fixture()
    data['unassigned_bands'] = [{'x':210,'core':[20],'fringe':[19,21],
        'fragment_id':'u','band_id':'band210','candidate_routes':['dash'],
        'status':'identity_conflict','boundary_flags':[],'note':'Synthetic unresolved dash neighborhood.'}]
    data['routes']['dash'][5].update(status='identity_conflict',band_refs=[{'x':210,'band_id':'band210'}])
    return data


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = C.helper()

    def validate(self,data,region='F6-Im2',role='primary'):
        return C.validate(data,region,role,self.h)

    def test_all_six_regions_and_named_roles(self):
        for region in C.TARGETS:
            for role in C.ROLES:
                self.validate(fixture(region,role),region,role)

    def test_empty_not_missing(self):
        data=fixture(); self.assertEqual(self.validate(data),{})
        band=copy.deepcopy(data['routes']['solid'][0]); band['candidate_routes']=[]
        data['unassigned_bands']=[band]
        self.assertEqual(self.validate(data)[205]['core'],[])

    def test_candidate_specific_not_both_routes(self):
        data=conflict_fixture(); self.validate(data)
        self.assertEqual(data['routes']['solid'][5]['status'],'no_attributable_cells')

    def test_both_candidates_when_explicit(self):
        data=conflict_fixture()
        data['unassigned_bands'][0]['candidate_routes'].append('solid')
        data['routes']['solid'][5].update(status='identity_conflict',band_refs=['band210'])
        self.validate(data)

    def test_unassigned_material_without_model_candidate(self):
        data=conflict_fixture()
        data['unassigned_bands'][0]['candidate_routes']=[]
        data['routes']['dash'][5].update(status='no_attributable_cells',band_refs=[])
        self.validate(data)

    def test_forbidden_route_reference(self):
        data=conflict_fixture()
        data['routes']['solid'][5].update(status='identity_conflict',band_refs=['band210'])
        with self.assertRaises(ValueError):self.validate(data)

    def test_candidate_needs_reference(self):
        data=conflict_fixture()
        data['routes']['dash'][5].update(status='no_attributable_cells',band_refs=[])
        with self.assertRaises(ValueError):self.validate(data)

    def test_duplicate_reference(self):
        data=conflict_fixture();data['routes']['dash'][5]['band_refs']*=2
        with self.assertRaises(ValueError):self.validate(data)

    def test_wrong_reference_schema(self):
        data=conflict_fixture();data['routes']['dash'][5]['band_refs'][0]['extra']=1
        with self.assertRaises(ValueError):self.validate(data)

    def test_empty_band_reference(self):
        data=conflict_fixture();data['unassigned_bands'][0].update(core=[],fringe=[],fragment_id=None)
        with self.assertRaises(ValueError):self.validate(data)

    def test_empty_band_cannot_have_candidates(self):
        data=fixture(); band=copy.deepcopy(data['routes']['solid'][0])
        band['candidate_routes']=['solid'];data['unassigned_bands']=[band]
        with self.assertRaises(ValueError):self.validate(data)

    def test_invalid_or_duplicate_candidates(self):
        for candidates in (['other'],['dash','dash'],'dash',[True]):
            data=conflict_fixture();data['unassigned_bands'][0]['candidate_routes']=candidates
            with self.subTest(candidates=candidates),self.assertRaises(ValueError):self.validate(data)

    def test_missing_candidate_field_is_not_explicit_empty(self):
        data=conflict_fixture()
        data['unassigned_bands'][0].pop('candidate_routes')
        data['routes']['dash'][5].update(status='no_attributable_cells',band_refs=[])
        with self.assertRaises(ValueError):self.validate(data)
        data['unassigned_bands'][0].update(core=[],fringe=[],fragment_id=None,status='no_attributable_cells')
        with self.assertRaises(ValueError):self.validate(data)

    def test_empty_band_identity_conflict_rejected(self):
        data=fixture();band=copy.deepcopy(data['routes']['solid'][0])
        band.update(status='identity_conflict',candidate_routes=[])
        data['unassigned_bands']=[band]
        with self.assertRaises(ValueError):self.validate(data)

    def test_empty_conflict_needs_material_reference(self):
        data=fixture();data['routes']['solid'][5]['status']='identity_conflict'
        with self.assertRaises(ValueError):self.validate(data)

    def test_unknown_route_is_not_empty_no_conflict(self):
        data=conflict_fixture();data['routes']['dash'][5]['status']='no_attributable_cells'
        with self.assertRaises(ValueError):self.validate(data)

    def test_same_pair_different_strip_not_interchangeable(self):
        data=fixture('F7-Im1')
        with self.assertRaises(ValueError):self.validate(data,'F7-Im2')

    def test_wrong_role(self):
        with self.assertRaises(ValueError):self.validate(fixture(),role='peer')

    def test_multiple_fragments_and_aggregate_band(self):
        data=conflict_fixture();data['unassigned_bands'][0].update(fragment_id=None,fragments=[
            {'fragment_id':'a','core':[20],'fringe':[19]},
            {'fragment_id':'b','core':[],'fringe':[21]}])
        self.validate(data)
        data['unassigned_bands'][0]['fragments'][1]['fringe']=[22]
        with self.assertRaises(ValueError):self.validate(data)

    def test_geometry_and_membership_faults(self):
        changes=[('bool_x',lambda d:d['routes']['solid'][0].update(x=True)),
                 ('out_of_box',lambda d:d['routes']['solid'][0].update(core=[88],fragment_id='a')),
                 ('missing_column',lambda d:d['routes']['solid'].pop()),
                 ('empty_reason',lambda d:d['routes']['solid'][0].update(note=' ')),
                 ('false_boundary',lambda d:d['routes']['solid'][0].update(boundary_flags=['target_left'])),
                 ('human_acceptance',lambda d:d.update(human_accepted=True)),
                 ('wrong_source',lambda d:d.update(source_image='Im1.jpg'))]
        for label,mutate in changes:
            data=fixture();mutate(data)
            with self.subTest(label=label),self.assertRaises(ValueError):self.validate(data)

    def test_set_operations_and_direction(self):
        expected={'intersection':[4],'union':[2,4,7],'primary_only':[2],
                  'peer_only':[7],'symmetric_difference':[2,7]}
        self.assertEqual(self.h.operations({2,4},{4,7}),expected)
        self.assertEqual(self.h.operations({4,7},{2,4})['primary_only'],[7])

    def test_class_swap_keeps_outer_but_not_class(self):
        result=self.h.comparison({'core':[2],'fringe':[4]},{'core':[4],'fringe':[2]})
        self.assertEqual(result['outer']['symmetric_difference'],[])
        self.assertEqual(result['core']['symmetric_difference'],[2,4])

    def test_all_ink_includes_unassigned_once(self):
        primary=conflict_fixture();peer=copy.deepcopy(primary);peer['reader']='peer'
        data={'peer':peer,'primary':primary}
        bands={role:self.validate(value,role=role) for role,value in data.items()}
        result=self.h.visible_geometry(data,bands,205,365)
        self.assertEqual(result[5]['sets']['outer']['union'],[19,20,21])
        self.assertEqual(result[5]['sets']['outer']['symmetric_difference'],[])


class IntegrationTests(unittest.TestCase):
    """Invented context and inert source bytes; no historical measurement."""
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory(prefix='force69-synthetic-')
        self.root=Path(self.directory.name)/'native-footprint-pass'/'force69'
        self.root.mkdir(parents=True)
        self.region='F9-Im0'
        x0,y0,x1,y1=C.CONTEXTS[self.region]
        context={'target_boxes':{self.region:C.TARGETS[self.region]},
                 'context_boxes':{self.region:C.CONTEXTS[self.region]},
                 'sources':{self.region:'Im0.jpg'},'pairs':{self.region:'F9'},
                 'cells':{self.region:[{'x':x,'y':y,'rgb':[255,255,255]}
                                      for y in range(y0,y1) for x in range(x0,x1)]}}
        raw=(json.dumps(context,sort_keys=True)+'\n').encode()
        for name in ('context01.json','context02.json'):(self.root/name).write_bytes(raw)
        for name in ('PROTOCOL.md','primary_helper.py','peer_export.py','test_compare_force69.py',
                     '../../native-strips01/Im0.jpg'):
            path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(b'SYNTHETIC INERT FIXTURE, NOT A HISTORICAL SOURCE\n')
        self.readings={};self.pins={}
        for role in C.ROLES:
            data=fixture(self.region,role)
            data['sentinel_metadata']={'reader':role,'not_to_drop':[1,None,'extra']}
            names=['PROTOCOL.md','context01.json','context02.json','../../native-strips01/Im0.jpg']
            if role=='primary':names.append('primary_helper.py')
            else:data['expander_pin']=C.pin(self.root/'peer_export.py')
            data['inputs']={name:C.pin(self.root/name) for name in names}
            script=self.root/f'reader-{self.region}-{role}.py';script.write_bytes(b'# Inert synthetic literal script\n')
            data['script_pin']=C.pin(script)
            self.readings[role]=data
            data_raw=(json.dumps(data,sort_keys=True)+'\n').encode()
            for suffix in ('','-repeat'):(self.root/f'reader-{self.region}-{role}{suffix}.json').write_bytes(data_raw)
            self.pins[role]=C.pin_bytes(data_raw)['sha256']

    def tearDown(self):
        self.directory.cleanup()

    def run_fixture(self):
        with patch.object(C,'HERE',self.root):
            return C.run(self.region,{'peer':self.pins['peer'],'primary':self.pins['primary']})

    def test_complete_original_and_metadata_preservation(self):
        a=self.run_fixture();b=self.run_fixture()
        self.assertEqual(a,b)
        self.assertEqual(a['literal_readings'],self.readings)
        self.assertEqual(a['summary']['routes']['entries'],210)
        self.assertEqual(a['summary']['visible_ink']['entries'],105)
        self.assertEqual(a['summary']['routes']['outer_different'],0)
        for row in a['route_comparisons']:
            for role in C.ROLES:
                self.assertEqual(row[role+'_original'],self.readings[role]['routes'][row['route']][row['x']-220])

    def test_reader_repeat_mismatch(self):
        (self.root/f'reader-{self.region}-peer-repeat.json').write_bytes(b'{}\n')
        with self.assertRaises(ValueError):self.run_fixture()

    def test_dependency_mismatch(self):
        (self.root/'PROTOCOL.md').write_bytes(b'CHANGED SYNTHETIC FIXTURE\n')
        with self.assertRaises(ValueError):self.run_fixture()

    def test_frozen_input_hash_mismatch(self):
        self.pins['primary']='0'*64
        with self.assertRaises(ValueError):self.run_fixture()

    def test_peer_expander_mismatch(self):
        (self.root/'peer_export.py').write_bytes(b'CHANGED SYNTHETIC HELPER\n')
        with self.assertRaises(ValueError):self.run_fixture()


if __name__ == '__main__':
    unittest.main(verbosity=2)

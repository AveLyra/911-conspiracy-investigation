import copy
import unittest
from compare_e89 import validate, operations, rows, visible_geometry


def fixture():
    def record(x):return {'x':x,'core':[],'fringe':[],'status':'identity_conflict','fragment_id':None,'boundary_flags':[],'band_refs':[]}
    return {'pair':'E8','target_box':[535,54,690,86],
            'routes':{k:[record(x) for x in range(535,690)] for k in ['solid','dash']},'unassigned_bands':[]}


class Checks(unittest.TestCase):
    def test_valid_empty_attribution(self):self.assertEqual(validate(fixture()),{})
    def test_missing_column(self):
        d=fixture();d['routes']['solid'].pop()
        with self.assertRaises(ValueError):validate(d)
    def test_hole_preserved(self):self.assertEqual(operations({40,42},{42})['root_only'],[40])
    def test_boolean_rejected(self):
        with self.assertRaises(ValueError):rows({'core':[True],'fringe':[]})
    def test_class_overlap(self):
        with self.assertRaises(ValueError):rows({'core':[40],'fringe':[40]})
    def test_unsorted(self):
        with self.assertRaises(ValueError):rows({'core':[42,40],'fringe':[]})
    def test_wrong_boundary(self):
        d=fixture();d['routes']['solid'][0]['boundary_flags']=['target_left']
        with self.assertRaises(ValueError):validate(d)
    def test_missing_reference(self):
        d=fixture();d['routes']['solid'][2]['band_refs']=['missing']
        with self.assertRaises(ValueError):validate(d)
    def test_valid_unassigned(self):
        d=fixture();d['unassigned_bands']=[{'x':537,'core':[74],'fringe':[73,75],'fragment_id':'u','boundary_flags':[]}]
        d['routes']['solid'][2]['band_refs']=['u'];self.assertIn(537,validate(d))
    def test_duplicate_assignment(self):
        d=fixture();d['unassigned_bands']=[{'x':537,'core':[74],'fringe':[],'fragment_id':'u','boundary_flags':[]}]
        d['routes']['dash'][2].update(core=[74],status='identified_local_fragment',fragment_id='d')
        with self.assertRaises(ValueError):validate(d)
    def test_wrong_column_reference(self):
        d=fixture();d['unassigned_bands']=[{'x':537,'core':[74],'fringe':[],'band_id':'u','boundary_flags':[]}]
        r=d['routes']['solid'][3];r.pop('band_refs');r['unassigned_band_refs']=[{'x':537,'band_id':'u'}]
        with self.assertRaises(ValueError):validate(d)
    def test_empty_is_not_missing_band(self):
        d=fixture();d['unassigned_bands']=[{'x':537,'core':[],'fringe':[],'fragment_id':None,'boundary_flags':[]}]
        self.assertIn(537,validate(d));self.assertNotIn(538,validate(d))
    def test_class_swap_not_agreement(self):
        self.assertEqual(operations({40,42},{40,42})['symmetric_difference'],[])
        self.assertEqual(operations({40},{42})['symmetric_difference'],[40,42])


    def test_fringe_only_bottom_truncation(self):
        d=fixture();d['routes']['dash'][2].update(fringe=[85],status='boundary_truncated',fragment_id='d',boundary_flags=['target_bottom'])
        validate(d)
    def test_empty_truncation_rejected(self):
        d=fixture();d['routes']['dash'][2].update(status='boundary_truncated',fragment_id='d')
        with self.assertRaises(ValueError):validate(d)
    def test_target_rows(self):
        d=fixture();d['routes']['dash'][2].update(core=[53],status='identified_local_fragment',fragment_id='d')
        with self.assertRaises(ValueError):validate(d)
    def test_duplicate_models(self):
        d=fixture()
        for rs in d['routes'].values():rs[2].update(core=[74],status='identified_local_fragment',fragment_id='d')
        with self.assertRaises(ValueError):validate(d)
    def test_e5_geometry(self):
        d=fixture();d['pair']='E9';d['target_box']=[530,30,690,56]
        for rs in d['routes'].values():
            template=copy.deepcopy(rs[0]);rs[:]=[dict(template,x=x) for x in range(530,690)]
        validate(d)
    def test_all_five_operations(self):
        self.assertEqual(operations({1,3},{3,5}),{'intersection':[3],'union':[1,3,5],'root_only':[1],'peer_only':[5],'symmetric_difference':[1,5]})
    def test_bad_status(self):
        d=fixture();d['routes']['dash'][2]['status']='accepted'
        with self.assertRaises(ValueError):validate(d)

    def test_visible_role_order(self):
        a=fixture();b=fixture()
        a['routes']['solid'][2].update(core=[74],status='identified_local_fragment',fragment_id='s')
        b['routes']['solid'][2].update(core=[75],status='identified_local_fragment',fragment_id='s')
        forward={'root':a,'independent':b};reverse={'independent':b,'root':a}
        bands={'root':validate(a),'independent':validate(b)}
        x=visible_geometry(forward,bands,535,690)
        self.assertEqual(x,visible_geometry(reverse,bands,535,690))
        self.assertEqual(x[2]['sets']['core']['root_only'],[74])
        self.assertEqual(x[2]['sets']['core']['peer_only'],[75])

if __name__=='__main__':unittest.main()



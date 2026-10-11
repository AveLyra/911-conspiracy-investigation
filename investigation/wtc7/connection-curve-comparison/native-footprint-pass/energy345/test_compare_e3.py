import copy
import unittest
from compare_e3 import validate, operations, rows


def fixture():
    def record(x):return {'x':x,'core':[],'fringe':[],'status':'identity_conflict','fragment_id':None,'boundary_flags':[],'band_refs':[]}
    return {'pair':'E3','target_box':[365,30,690,60],
            'routes':{k:[record(x) for x in range(365,690)] for k in ['solid','dash']},'unassigned_bands':[]}


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
        d=fixture();d['unassigned_bands']=[{'x':367,'core':[43],'fringe':[42,44],'fragment_id':'u','boundary_flags':[]}]
        d['routes']['solid'][2]['band_refs']=['u'];self.assertIn(367,validate(d))
    def test_duplicate_assignment(self):
        d=fixture();d['unassigned_bands']=[{'x':367,'core':[43],'fringe':[],'fragment_id':'u','boundary_flags':[]}]
        d['routes']['dash'][2].update(core=[43],status='identified_local_fragment',fragment_id='d')
        with self.assertRaises(ValueError):validate(d)
    def test_wrong_column_reference(self):
        d=fixture();d['unassigned_bands']=[{'x':367,'core':[43],'fringe':[],'band_id':'u','boundary_flags':[]}]
        r=d['routes']['solid'][3];r.pop('band_refs');r['unassigned_band_refs']=[{'x':367,'band_id':'u'}]
        with self.assertRaises(ValueError):validate(d)
    def test_empty_is_not_missing_band(self):
        d=fixture();d['unassigned_bands']=[{'x':367,'core':[],'fringe':[],'fragment_id':None,'boundary_flags':[]}]
        self.assertIn(367,validate(d));self.assertNotIn(368,validate(d))
    def test_class_swap_not_agreement(self):
        self.assertEqual(operations({40,42},{40,42})['symmetric_difference'],[])
        self.assertEqual(operations({40},{42})['symmetric_difference'],[40,42])


if __name__=='__main__':unittest.main()

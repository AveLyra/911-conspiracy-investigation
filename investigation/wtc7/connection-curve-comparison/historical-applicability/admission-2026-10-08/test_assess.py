"""Synthetic geometry tests; not validation of historical H assumptions."""
import copy
from fractions import Fraction as F
from pathlib import Path
import tempfile
import unittest

import assess as a


def cell(name,route,left,right,source='synthetic',y=10,body='one',role='primary'):
    return {'id':name,'pair':'F3','role':role,'route':route,'render_x':[left,right],
            'source':source,'native_rectangle':[0,y,1,y+2], 'body':[role,source,body]}


def length(result,status='paired_local_candidate'):
    return result['render_lengths'][status]


class GeometryTests(unittest.TestCase):
    def test_empty_is_not_actual_support(self):
        result=a.partition([])
        self.assertEqual(result['segments'],[])
        self.assertEqual(result['paired_runs'],[])
        self.assertEqual(length(result),0)
        self.assertNotIn('actual_D',result)

    def test_overlap_exact_fraction(self):
        result=a.partition([cell('s','solid',F(1,3),2),cell('d','dash',1,F(5,2),y=20)])
        self.assertEqual([s['status'] for s in result['segments']],['solid_only','paired_local_candidate','dash_only'])
        self.assertEqual(length(result),1)
        self.assertEqual(result['paired_runs'][0]['render_x'],[F(1),F(2)])

    def test_touch_is_not_interval(self):
        result=a.partition([cell('s','solid',0,1),cell('d','dash',1,2,y=20)])
        self.assertEqual(length(result),0)
        self.assertEqual(result['any_paired_render_length'],0)

    def test_dash_gaps_preserved(self):
        result=a.partition([cell('s','solid',0,5),cell('d1','dash',1,2,y=20),cell('d2','dash',3,4,y=20)])
        self.assertEqual(length(result),2)
        self.assertEqual([r['render_x'] for r in result['paired_runs']],[[F(1),F(2)],[F(3),F(4)]])

    def test_no_candidate_gap_recorded(self):
        result=a.partition([cell('s','solid',0,1),cell('d','dash',3,4,y=20)])
        self.assertEqual(length(result,'gap'),2)

    def test_shared_ink_mixed_roles(self):
        result=a.partition([cell('s','solid',0,1,role='primary'),cell('d','dash',0,1,role='peer')])
        self.assertEqual(length(result),0)
        self.assertEqual(length(result,'shared_ink_ownership_conflict'),1)
        self.assertEqual(result['segments'][0]['shared_ink_conflicts'],[['s','d']])

    def test_different_strips_overlap_without_shared_pixels(self):
        result=a.partition([cell('s','solid',0,1,source='one'),cell('d','dash',0,1,source='two')])
        self.assertEqual(length(result),1)
        self.assertEqual(result['segments'][0]['shared_ink_conflicts'],[])

    def test_duplicate_coverage_withheld_not_multivalued_finding(self):
        result=a.partition([cell('s1','solid',0,2),cell('s2','solid',1,3),cell('d','dash',0,3,y=20)])
        self.assertEqual(length(result),2)
        self.assertEqual(length(result,'overlapping_candidate_coverage'),1)
        self.assertEqual(result['segments'][1]['overlapping_routes'],['solid'])
        self.assertEqual(result['own_candidate_render_lengths']['solid'],3)
        self.assertEqual(len(result['paired_runs']),2)

    def test_overlapping_one_style_still_flagged(self):
        result=a.partition([cell('s1','solid',0,2),cell('s2','solid',1,3)])
        self.assertEqual(result['segments'][1]['status'],'solid_only')
        self.assertEqual(result['segments'][1]['overlapping_routes'],['solid'])

    def test_fragment_changes_not_joined(self):
        result=a.partition([cell('s','solid',0,3),cell('d1','dash',0,1,y=20,body='first'),
                            cell('d2','dash',1,3,y=20,body='second')])
        self.assertEqual(length(result),3)
        self.assertEqual(len(result['paired_runs']),2)

    def test_same_body_bookkeeping_merge_retains_edges(self):
        result=a.partition([cell('s','solid',0,3),cell('d1','dash',0,1,y=20),cell('d2','dash',1,3,y=20)])
        self.assertEqual(len(result['segments']),2)
        self.assertEqual(result['paired_runs'][0]['segment_indices'],[0,1])

    def test_input_order_does_not_select_reader(self):
        values=[cell('s','solid',0,3),cell('d1','dash',0,1,y=20),cell('d2','dash',2,3,y=20)]
        self.assertEqual(a.partition(values),a.partition(values[::-1]))

    def test_invalid_cells_rejected(self):
        original=cell('s','solid',0,1)
        for change in ({'render_x':[False,1]},{'render_x':[0,1.0]},{'render_x':['nan',1]},
                       {'render_x':[1,1]},{'render_x':[2,1]},{'route':'unknown'},
                       {'id':''},{'native_rectangle':[0,1,0,2]},{'body':['','','']}):
            with self.subTest(change=change),self.assertRaises((ValueError,TypeError)):
                a.partition([dict(original,**change)])
        with self.assertRaises(ValueError):a.partition([original,original])

    def test_all_four_role_combinations(self):
        values=[cell('sp','solid',0,2,role='primary'),cell('dp','dash',1,3,y=20,role='primary'),
                cell('sq','solid',4,6,role='peer'),cell('dq','dash',5,7,y=20,role='peer')]
        results=a.pairings('F3',values,{'F-root':{'L':[0,0],'R':[10,10]}})
        self.assertEqual([(r['solid_reader'],r['dash_reader']) for r in results],
            [('primary','primary'),('primary','peer'),('peer','primary'),('peer','peer')])
        self.assertEqual([length(r) for r in results],[1,0,0,1])
        self.assertTrue(all(r['actual_D'] is None and r['human_accepted'] is False for r in results))

    def test_shared_axis_bounds(self):
        self.assertEqual(a.length_bounds(10,{'L':[0,2],'R':[98,100]}),[F(4,25),F(1,6)])
        self.assertEqual(a.length_bounds(0,{'L':[0,2],'R':[98,100]}),[0,0])
        for axis in ({'L':[2,0],'R':[98,100]},{'L':[0,10],'R':[10,20]},{'L':[0,0],'R':[1.0,2]}):
            with self.assertRaises(ValueError):a.length_bounds(1,axis)
        with self.assertRaises(ValueError):a.length_bounds(-1,{'L':[0,0],'R':[1,1]})

    def test_marginal_hulls_cannot_create_intersection(self):
        # Under one unknown translation t in [-10,10], both intervals shift
        # together. Their separate marginal hulls overlap but true geometry does not.
        marginal_s=(-10,11); marginal_d=(-8,13)
        self.assertLess(max(marginal_s[0],marginal_d[0]),min(marginal_s[1],marginal_d[1]))
        result=a.partition([cell('s','solid',0,1),cell('d','dash',2,3,y=20)])
        self.assertEqual(length(result),0)

    def test_native_boundary_touch_not_shared_ink(self):
        self.assertFalse(a.shared_ink(cell('s','solid',0,1,y=10),cell('d','dash',0,1,y=12)))

    def test_partition_does_not_mutate(self):
        values=[cell('s','solid',0,1),cell('d','dash',0,1,y=20)]
        before=copy.deepcopy(values)
        a.partition(values)
        self.assertEqual(values,before)

    def test_pin_mismatch_and_conflict(self):
        with tempfile.TemporaryDirectory(prefix='admission-pin-test-') as directory:
            path=Path(directory)/'input'
            a.save(path,b'first')
            pins={}
            a.include(pins,path)
            with self.assertRaises(ValueError):a.include(pins,path,'0'*64)
            with self.assertRaises(ValueError):a.include(pins,path,{'sha256':a.pin(path)['sha256'],'bytes':True})
            key=next(iter(pins));pins[key]={'sha256':'0'*64,'bytes':5}
            with self.assertRaises(ValueError):a.include(pins,path)

    def test_exclusive_save_and_exact_json(self):
        with tempfile.TemporaryDirectory(prefix='admission-output-test-') as directory:
            path=Path(directory)/'output.json'
            raw=a.encode({'fraction':F(2,3),'actual_D':None})
            a.save(path,raw)
            with self.assertRaises(FileExistsError):a.save(path,b'changed')
            self.assertEqual(path.read_bytes(),raw)
            self.assertIn(b'"2/3"',raw)


if __name__=='__main__':unittest.main()

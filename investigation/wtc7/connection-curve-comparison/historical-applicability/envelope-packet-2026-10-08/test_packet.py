import copy
from fractions import Fraction as F
from pathlib import Path
import tempfile
import unittest
import packet as p


def segment(a,b,state='paired_local_candidate'):
    return {'render_x':[a,b],'status':state}


class Selection(unittest.TestCase):
    def test_full_domain(self):
        self.assertEqual([p.quantile([[0,F(8,5)]],q)['page_x'] for q in (F(1,4),F(1,2),F(3,4))],[F(2,5),F(4,5),F(6,5)])

    def test_gap_tie_unchanged(self):
        d=[[0,F(1,5)],[F(4,5),1]]
        got=[p.quantile(d,q) for q in (F(1,4),F(1,2),F(3,4))]
        self.assertEqual([r['page_x'] for r in got],[F(1,10),F(1,5),F(9,10)])
        self.assertTrue(got[1]['cumulative_tie'])

    def test_empty_not_zero_curve(self):
        self.assertIsNone(p.quantile([],F(1,2))['page_x'])

    def test_invalid_domains(self):
        for d in ([[0,0]],[[1,0]],[[False,1]],[[0,1.0]],[[0,2],[1,3]],[[2,3],[0,1]]):
            with self.subTest(d=d),self.assertRaises(ValueError):p.quantile(d,F(1,2))
        for q in (0,1,False,0.5):
            with self.subTest(q=q),self.assertRaises(ValueError):p.quantile([[0,1]],q)

    def test_merge_is_length_only(self):
        s=[segment(0,1),segment(1,2),segment(2,3,'gap'),segment(3,4)]
        self.assertEqual(p.intervals(s),[[0,2],[3,4]])
        self.assertEqual(p.point_state({'segments':s},F(1))['status'],'boundary_unresolved')
        self.assertEqual(p.point_state({'segments':s},F(5,2))['status'],'gap')

    def test_overlap_refused(self):
        with self.assertRaises(ValueError):p.intervals([segment(0,2),segment(1,3)])

    def test_same_point_missing_alternative(self):
        self.assertEqual(p.point_state({'segments':[segment(0,1)]},F(2))['status'],'outside_candidate_extent')
        self.assertEqual(p.point_state({'segments':[segment(0,1)]},None)['status'],'no_primary_target')

    def test_displacement_shared_positive_affine(self):
        self.assertEqual(p.displacement(F(5),{'L':[0,1],'R':[9,10]}),[F(32,45),F(8,9)])
        for shift in (F(-3),F(1,7)):
            target=p.quantile([[shift,shift+2],[shift+4,shift+6]],F(1,4))['page_x']
            self.assertEqual(target,shift+1)
        with self.assertRaises(ValueError):p.displacement(F(1),{'L':[0,2],'R':[1,3]})

    def test_native_mapping_roundtrip_and_orientation(self):
        inv={'ctm':[36,0,0,36,0,756],'native_dimensions':[100,100]}
        c={'id':'s','reader_path':'r','role':'primary','route':'solid','source':'Im0','fragment_id':'a',
           'native_rectangle':[10,20,11,23],'render_rectangle':[10,20,11,23]}
        result=p.map_cell(c,F(21,2),inv)
        self.assertEqual(result['native_x'],F(21,2));self.assertFalse(result['boundary_touch'])
        self.assertTrue(p.map_cell(c,F(11),inv)['boundary_touch'])
        with self.assertRaises(ValueError):p.map_cell(c,F(12),inv)
        with self.assertRaises(ValueError):p.map_cell(dict(c,render_rectangle=[10,21,11,23]),F(21,2),inv)

    def test_duplicate_per_model_and_pair(self):
        def slot(n,change=False):
            entries=[]
            for model in ('spring','shell'):
                rect=[1,2,2,3] if model=='spring' or not change else [2,2,3,3]
                entries.append({'id':f'{n}-{model}','model':model,
                    'mappings':{role:[{'source':'Im0','native_rectangle':rect,'cell_id':str(n)}] for role in p.ROLES},
                    'duplicate_entries':{role:[] for role in p.ROLES}})
            return {'id':str(n),'pair':'F3','entries':entries,'duplicate_paired_slots':[]}
        slots=[slot(1),slot(2),slot(3,True)];p.duplicate_flags(slots)
        self.assertEqual(slots[0]['duplicate_paired_slots'],['2'])
        self.assertEqual(slots[2]['duplicate_paired_slots'],[])
        self.assertEqual(slots[0]['entries'][0]['duplicate_entries']['primary'],['2-spring','3-spring'])

    def test_exclusive_save_and_fraction(self):
        with tempfile.TemporaryDirectory(prefix='conditional-packet-') as directory:
            path=Path(directory)/'packet.json';raw=p.encode({'q':F(1,3),'human':None})
            p.save(path,raw)
            with self.assertRaises(FileExistsError):p.save(path,b'wrong')
            self.assertEqual(path.read_bytes(),raw)


if __name__=='__main__':unittest.main()

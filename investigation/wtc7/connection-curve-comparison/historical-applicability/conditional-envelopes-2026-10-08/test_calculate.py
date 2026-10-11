"""Synthetic arithmetic/schema tests, not historical enclosure validation."""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest

import calculate as c


def entry(x=13,**changes):
    value = {'x':x,'core':[30,31],'fringe':[29,32],
             'fragment_id':'one','boundary_flags':[],
             'status':'identified_local_fragment'}
    value.update(changes)
    return value


def strip(height=36):
    return c.geometry.Strip('synthetic',100,100,(36,0,0,height,180,540))


def routes():
    return {r:[entry(x) for x in range(10,17)] for r in ('solid','dash')}


class Controls(unittest.TestCase):
    def test_normalization_does_not_mutate(self):
        value = entry(fragments=[{'fragment_id':'one','core':[30,31],'fringe':[29,32]}])
        original = copy.deepcopy(value)
        normalized,refs = c.normalize(value,'solid',100)
        self.assertEqual(original,value)
        self.assertEqual(refs,[])
        self.assertEqual(normalized['fragment_membership'],{'one':{'core_rows':[30,31],'fringe_rows':[29,32]}})

    def test_old_schema(self):
        value = {'column':13,'core_rows':[30,31],'fringe_rows':[29,32],
                 'fragment_id':'one','status':'identified_local_fragment','boundary_flags':[]}
        self.assertEqual(c.normalize(value,'solid',100)[0]['column'],13)

    def test_malformed_rows(self):
        for change in ({'x':True},{'core':[True]},{'core':[100]},{'core':[31,30]},
                       {'core':[30,30]},{'fringe':[30]},{'boundary_flags':None}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                c.normalize(entry(**change),'solid',100)

    def test_membership_error_not_missing(self):
        for fragments in ([{'fragment_id':'one','core':[30],'fringe':[29,32]}],
                          [{'fragment_id':'one','core':[30,31],'fringe':[29,32]}]*2):
            with self.assertRaises(ValueError):
                c.normalize(entry(fragments=fragments),'solid',100)

    def test_cell_edges_y_inversion_and_nonuniform_scale(self):
        pdf,render = c.render_rect(strip(),[10,20,11,23])
        self.assertEqual(pdf,(F(918,5),F(14193,25),F(4599,25),F(2844,5)))
        self.assertEqual(render,(F(510),F(620),F(511),F(623)))
        other,_ = c.render_rect(strip(18),[10,20,11,23])
        self.assertEqual(other[3]-other[1],(pdf[3]-pdf[1])/2)

    def test_masks_include_touch_not_nearby(self):
        self.assertTrue(c.touches((849,240,850,241),c.EXCLUSIONS['F'][0]))
        self.assertFalse(c.touches((848,240,849,241),c.EXCLUSIONS['F'][0]))

    def test_axis_allowance_conventions(self):
        self.assertEqual(c.axis('F','root')['L'],(F(446),F(453)))
        self.assertEqual(c.axis('E','independent')['L'],(F(468),F(480)))

    def test_fractional_extrema(self):
        self.assertEqual(c.fractions_between((F(25),F(30)),(F(0),F(2)),(F(98),F(100)),F(8,5)),
                         (F(92,245),F(24,49)))
        for left,right in [((F(0),F(10)),(F(10),F(20))),((F(20),F(30)),(F(10),F(15)))]:
            with self.assertRaises(ValueError): c.fractions_between((F(3),F(4)),left,right,F(1))
        with self.assertRaises(ValueError): c.fractions_between((F(4),F(3)),(F(0),F(1)),(F(10),F(11)),F(1))

    def test_endpoint_withholding_not_iterated(self):
        result = c.process(routes(),strip(),[10,10,17,90],'F')
        for route in ('solid','dash'):
            self.assertEqual([r['column'] for r in result if r['route']==route and r['conditional_window']],[12,13,14])
        self.assertTrue(all(not r['curve_support_established'] for r in result))

    def test_unknown_band_and_gap_not_bridged(self):
        for change in ({'band_refs':['unknown']},{'fragment_id':'other'},
                       {'status':'identity_conflict'},{'core':[],'fringe':[]}):
            value = routes()
            value['solid'][3].update(change)
            rows = c.process(value,strip(),[10,10,17,90],'F')
            self.assertFalse(any(r['conditional_window'] for r in rows if r['route']=='solid'))
            self.assertEqual(sum(r['conditional_window'] for r in rows if r['route']=='dash'),3)

    def test_incomplete_coverage_is_error(self):
        value = routes(); value['solid'].pop()
        with self.assertRaises(ValueError): c.process(value,strip(),[10,10,17,90],'F')

    def test_preservation_and_serialization(self):
        with tempfile.TemporaryDirectory(prefix='conditional-window-test-') as folder:
            path = Path(folder)/'out.json'
            data = c.encoded({'x':F(1,3),'missing':None})
            c.save(path,data)
            with self.assertRaises(FileExistsError): c.save(path,b'changed')
            self.assertEqual(path.read_bytes(),data)
            self.assertEqual(json.loads(data),{'x':'1/3','missing':None})
        with self.assertRaises(TypeError): c.encoded({'bad':object()})


if __name__=='__main__': unittest.main()

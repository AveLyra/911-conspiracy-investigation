"""Synthetic implementation tests; no historical coefficient used as truth."""
import copy
import unittest
import numpy as np
from calculate import fit, validate_table, centered_differences, western, windows


class CalculationTests(unittest.TestCase):
    def test_linear_velocity(self):
        t=np.arange(7,dtype=float)/5
        result=fit(t,4-9.8*t,1)
        self.assertAlmostEqual(result['downward_acceleration'],9.8,places=10)
        self.assertLess(max(abs(x) for x in result['residuals']),1e-10)

    def test_quadratic_position(self):
        t=np.arange(7,dtype=float)/5
        result=fit(t,50+2*t-4.9*t*t,2)
        self.assertAlmostEqual(result['downward_acceleration'],9.8,places=10)

    def test_constant_and_linear_positions(self):
        for y in [np.ones(7)*30,30+np.arange(7)*2]:
            self.assertAlmostEqual(fit(np.arange(7),y,2)['downward_acceleration'],0,places=10)

    def test_translation(self):
        t=np.arange(7)/5; y=20-3*t-4*t*t
        for degree in [1,2]:
            a=fit(t,y,degree)['downward_acceleration']; b=fit(t+100,y+1000,degree)['downward_acceleration']
            self.assertAlmostEqual(a,b,places=8)

    def test_rounding_witness(self):
        t=np.arange(7)/5; y=20-3*t-4*t*t
        for degree in [1,2]:
            base=fit(t,y,degree); weights=np.array(base['acceleration_input_weights'])
            for sign in [-1,1]:
                changed=fit(t,y+sign*.005*np.sign(weights),degree)
                self.assertAlmostEqual(changed['downward_acceleration']-base['downward_acceleration'],
                                       sign*base['display_rounding_half_width'],places=9)

    def test_bad_fit_input(self):
        for t,y,d in [([0,0,1],[1,2,3],1),([0,1],[2,3],2),([0,1,2],[2,float('nan'),4],1),([0,1,2],[2,3],1)]:
            with self.assertRaises(ValueError): fit(t,y,d)

    def test_schema_failures(self):
        columns=['time_s','ref_y','nw_y','nw_relative_y','center_y','center_relative_y','center_adjusted_y','sw_y','sw_relative_y','sw_adjusted_y']
        rows=[{'page':50,'row':i+1,**{c:'1.00' for c in columns},'time_s':f'{8+i/30:.2f}'} for i in range(25)]
        good={'columns':columns,'rows':rows}; self.assertEqual(len(validate_table(good,50)),25)
        for alteration in ['missing','nan','duplicate','null','row']:
            bad=copy.deepcopy(good)
            if alteration=='missing': del bad['rows'][0]['nw_y']
            elif alteration=='nan': bad['rows'][0]['nw_y']='NaN'
            elif alteration=='duplicate': bad['rows'][1]['time_s']=bad['rows'][0]['time_s']
            elif alteration=='null': bad['rows'][0]['nw_y']=None
            else: bad['rows'][0]['row']=2
            with self.assertRaises((ValueError,KeyError)): validate_table(bad,50)

    def test_derivative_boundary(self):
        rows=[]
        for i in range(3):
            r={'row':i+1,'time_s':str(i/5)}
            for track in ['ne','ec','wc','nw']:
                r[track+'_y']=str(10-i*.2); r[track+'_v']=None if i!=1 else '-0.970'
            rows.append(r)
        result=centered_differences(rows)
        self.assertEqual(len(result['rows']),4)
        self.assertTrue(all(r['rounding_compatible'] for r in result['rows']))
        rows[1]['ne_v']='-0.969'
        self.assertFalse(centered_differences(rows)['rows'][0]['rounding_compatible'])

    def test_western_exact(self):
        rows=[]
        for i in range(2):
            r={'row':i+1,'time_s':['8.20','8.23'][i],'ref_y':'10.00'}
            for track,value in [('nw',30),('center',26),('sw',22)]:
                r[track+'_y']=str(float(value-i)); r[track+'_relative_y']=str(float(value-i-10))
                if track!='nw': r[track+'_adjusted_y']=str(float(20-i))
            rows.append(r)
        result=western(rows)
        self.assertTrue(all(x['rounding_compatible'] for x in result['subtractions']))
        self.assertTrue(all(x['compatible_common_offset'] for x in result['offsets'].values()))
        self.assertTrue(all(v=='0' for r in result['displacements_from_8_20'] for v in r['pair_differences_fraction'].values()))

    def test_window_membership(self):
        rows=[{'time_s':str(i/5),'ne_v':'0.00','ec_v':'0.00','wc_v':'0.00','nw_v':'0.00'} for i in range(70)]
        self.assertEqual(len(windows(rows,'ne')),10)
        self.assertEqual(len(windows(rows,'nw')),13)
        self.assertEqual(windows(rows,'ne')[0],('grid','7.8','8.8'))


if __name__=='__main__': unittest.main()

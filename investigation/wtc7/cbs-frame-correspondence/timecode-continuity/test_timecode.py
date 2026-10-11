"""Synthetic controls only; no historical result reads."""
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import unittest
from unittest.mock import patch
import timecode as t


def pack(h=0,m=0,s=0,f=0,drop=False,flags=(0,0,0,0)):
    data=[(v//10)*16+v%10 for v in (f,s,m,h)]
    data[0]|=64 if drop else 0
    return bytes([0x13]+[a|b for a,b in zip(data,flags)]).hex()


def document(raws):
    return {'clip':1,'result':{'frames':len(raws),'target_variants':[
        {'area':'subcode','raw_hex':v,'occurrences':40,'frames_present':1,'first_frame':i,'last_frame':i}
        for i,v in enumerate(raws)]}}


def header(n,label='00;00;00;00'):
    return {'fields':{'tc_O':[{'prefix_utf8':label}],'tc_A':[{'prefix_utf8':label}]},
            'video_header':{'scale':1001,'rate':30000,'length':n,'start':0,'time_base':'1001/30000'}}


class TimecodeTests(unittest.TestCase):
    def test_endianness_and_flag_positions(self):
        row=t.decode(pack(12,34,56,27,True,(128,128,128,192)))
        self.assertEqual(row['components_h_m_s_f'],[12,34,56,27])
        self.assertEqual(row['positional_flag_hex'],'c08080c0')
        self.assertTrue(row['drop_bit'])
        self.assertFalse(row['component_issues'])

    def test_each_invalid_bcd_unit_retained_not_zero(self):
        for offset in range(1,5):
            data=bytearray.fromhex(pack());data[offset]=0x0a
            row=t.decode(data.hex())
            self.assertIsNone(row['components_h_m_s_f'][4-offset])
            self.assertIsNone(row['selected'])

    def test_each_out_of_range_component(self):
        for parts in [(24,0,0,0),(0,60,0,0),(0,0,60,0),(0,0,0,30)]:
            row=t.decode(pack(*parts))
            self.assertTrue(row['component_issues'])
            self.assertIsNone(row['selected'])

    def test_all_ones_and_bad_candidate_syntax(self):
        row=t.decode('13ffffffff')
        self.assertEqual(row['components_h_m_s_f'],[None]*4)
        self.assertIsNone(row['selected'])
        for raw in ('', '13000000','1400000000','13GG000000','13 00000000',None):
            with self.subTest(raw=raw),self.assertRaises(ValueError):t.decode(raw)

    def test_drop_minute_and_tenth_minute_boundaries(self):
        cases=[((0,0,59,29),(0,1,0,2)),((0,9,59,29),(0,10,0,0)),((0,59,59,29),(1,0,0,0))]
        for a,b in cases:
            rows=[t.decode(pack(*a,True)),t.decode(pack(*b,True))]
            self.assertEqual(t.transitions(rows)[0]['selected_delta'],1)
        self.assertEqual(t.transitions([t.decode(pack(*p,True)) for p in cases[0]])[0]['nd_delta'],3)

    def test_drop_omitted_labels_and_non_drop_alternative(self):
        for h in (0,1,23):
            for m in (1,9,11,59):
                for f in (0,1):
                    row=t.decode(pack(h,m,0,f,True))
                    self.assertEqual(row['df_issues'],['omitted_drop_frame_label'])
                    self.assertIsNone(row['selected'])
                    self.assertIsNotNone(row['nd'])
        self.assertIsNotNone(t.decode(pack(0,10,0,0,True))['df'])

    def test_exhaustive_independently_enumerated_ten_minute_cycle(self):
        ordinal=0
        for minute in range(10):
            for second in range(60):
                for frame in range(30):
                    if minute!=0 and second==0 and frame<2:continue
                    row=t.decode(pack(0,minute,second,frame,True))
                    self.assertEqual(row['selected'],ordinal)
                    ordinal+=1
        self.assertEqual(ordinal,17982)
        self.assertEqual(t.decode(pack(0,10,0,0,True))['selected'],ordinal)

    def test_non_drop_second_minute_hour_boundaries(self):
        for a,b in [((0,0,0,29),(0,0,1,0)),((0,0,59,29),(0,1,0,0)),((0,59,59,29),(1,0,0,0))]:
            self.assertEqual(t.transitions([t.decode(pack(*a)),t.decode(pack(*b))])[0]['selected_delta'],1)

    def test_day_rollover_only_candidate(self):
        for drop,modulus in [(False,2592000),(True,2589408)]:
            edge=t.transitions([t.decode(pack(23,59,59,29,drop)),t.decode(pack(0,0,0,0,drop))])[0]
            self.assertEqual(edge['selected_delta'],1-modulus)
            self.assertTrue(edge['selected_possible_daily_rollover'])
            self.assertNotEqual(edge['selected_delta'],1)

    def test_repeat_skip_backward_and_invalid_endpoint(self):
        rows=[t.decode(pack(f=f)) for f in (0,1,1,4,2)]
        self.assertEqual([e['selected_delta'] for e in t.transitions(rows)],[1,0,3,-2])
        rows.append(t.decode('13ffffffff'))
        self.assertIsNone(t.transitions(rows)[-1]['selected_delta'])

    def test_mode_change_does_not_pass_on_accidental_one(self):
        edge=t.transitions([t.decode(pack(f=0)),t.decode(pack(f=1,drop=True))])[0]
        self.assertEqual(edge['selected_raw_difference'],1)
        self.assertIsNone(edge['selected_delta'])
        self.assertTrue(edge['drop_bit_changed'])

    def test_extra_flag_only_change_retained(self):
        edge=t.transitions([t.decode(pack(f=0)),t.decode(pack(f=1,flags=(128,128,128,192)))])[0]
        self.assertEqual(edge['selected_delta'],1)
        self.assertEqual(edge['flag_xor_hex'],'808080c0')

    def test_reconstruct_reordered_rows_without_reordering_frames(self):
        d=document([pack(f=0),pack(f=1)]);d['result']['target_variants'].reverse()
        self.assertEqual(t.reconstruct(d,2),[pack(f=0),pack(f=1)])

    def test_missing_duplicate_conflicting_population_refused(self):
        base=document([pack(f=0),pack(f=1)])
        variants=[]
        a=deepcopy(base);a['result']['target_variants'].pop();variants.append(a)
        a=deepcopy(base);a['result']['target_variants'][1]['first_frame']=0;variants.append(a)
        for key,value in [('area','vaux'),('occurrences',39),('frames_present',2),('last_frame',0),('first_frame',True)]:
            a=deepcopy(base);a['result']['target_variants'][1][key]=value;variants.append(a)
        for d in variants:
            with self.assertRaises(ValueError):t.reconstruct(d,2)

    def test_audited_raw_uniqueness_guard_not_general_counter_rule(self):
        with self.assertRaisesRegex(ValueError,'uniqueness'):
            t.reconstruct(document([pack(f=0),pack(f=0)]),2)
        # A repeated numeric counter with changed ancillary flags is distinct raw
        # input and must remain a zero-step finding, not be filtered out.
        raws=[pack(f=0),pack(f=0,flags=(128,0,0,0))]
        self.assertEqual(t.reconstruct(document(raws),2),raws)
        self.assertEqual(t.transitions([t.decode(x) for x in raws])[0]['selected_delta'],0)

    def test_strict_ascii_header_and_range_validation(self):
        self.assertFalse(t.parse_header('23;59;59;29')['issues'])
        for bad in ('00:00:00:00','00;00;00;00 ','０0;00;00;00','00;00;00;30',None):
            self.assertTrue(t.parse_header(bad)['issues'])

    def test_full_synthetic_clip_labels_periods_and_all_edges(self):
        d=document([pack(f=0),pack(f=1),pack(f=3)])
        h=header(3);h['video_header'].update(scale=333673,rate=10000000,time_base='333673/10000000')
        result=t.analyze_clip(d,h);s=result['summary']
        self.assertEqual(s['lanes']['selected']['non_one_step_right_frames'],[2])
        self.assertEqual(s['lanes']['selected']['one_step_edges'],1)
        self.assertTrue(s['header_comparisons']['tc_O']['matches_first_components'])
        self.assertEqual(Fraction(s['first_to_last_avi_span']),2*Fraction(333673,10000000))
        self.assertEqual(Fraction(s['container_duration_avi']),3*Fraction(333673,10000000))
        self.assertNotEqual(s['avi_frame_period'],s['nominal_dv_frame_period'])

    def test_invalid_semantics_preserved_in_full_result(self):
        result=t.analyze_clip(document([pack(), '13ffffffff']),header(2))
        self.assertEqual(len(result['frames']),2)
        self.assertEqual(result['summary']['lanes']['selected']['invalid_frames'],[1])
        self.assertEqual(result['summary']['lanes']['selected']['unavailable_right_frames'],[1])

    def test_bad_rates_and_count_refused(self):
        for key,value in [('rate',0),('scale',True),('length',2),('start',False),('time_base','1/0')]:
            h=header(1);h['video_header'][key]=value
            with self.assertRaises((ValueError,ZeroDivisionError)):t.analyze_clip(document([pack()]),h)

    def test_pair_boundary_distance_not_gap_or_duration(self):
        a=t.analyze_clip(document([pack(f=0),pack(f=1)]),header(2))
        b=t.analyze_clip(document([pack(f=4),pack(f=5)]),header(2,'00;00;00;04'))
        b['summary']['clip']=2
        lane=t.compare_clips([a,b])[0]['lanes']['selected']
        self.assertEqual(lane,{'start_difference':4,'all_left_ordinals_before_right':True,'boundary_counter_distance':3,'unrepresented_counter_positions':2})

    def test_frozen_population_and_collision_refusal(self):
        with patch.object(Path,'read_text',return_value='{"files":{}}'),patch.object(t,'pin') as p:
            with self.assertRaises(ValueError):t.controls()
            p.assert_not_called()
        with patch.object(Path,'exists',return_value=True),patch.object(t,'controls') as c:
            with self.assertRaises(ValueError):t.main()
            c.assert_not_called()


if __name__=='__main__':unittest.main()

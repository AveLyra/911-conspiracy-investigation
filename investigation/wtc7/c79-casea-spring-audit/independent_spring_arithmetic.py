"""Independent exact supplied-table diagnostics; never execute input sources."""
import argparse
import copy
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import tempfile
import time
import unittest

HERE = Path(__file__).resolve().parent
PINS = {
    'ARITHMETIC-PROTOCOL.md': 'f43d0df31f06b9d735e01d32c4450ba9dd2dd980efbbc46d61462b41db4fdf56',
    'PROTOCOL.md': 'b616114713bdfb20765bc033adc12d38cf888ae95704a41c17f705c3e791ea41',
    'spring-manual-review.md': '7631a2b81bcc0f8c638581fdb083edcd2817e474bfe2df973b52e9a35dbd3aee',
    'casea-root01.json': '27e8905727fa8462724db70f6ce11f411391170a4a6636936491027eaba988a2',
}

class SemanticError(ValueError):
    pass

def require(ok, code):
    if not ok:
        raise SemanticError(code)

def rational(value):
    require(type(value) in (int, float), 'numeric_type')
    require(math.isfinite(value), 'nonfinite')
    return Q(*value.as_integer_ratio()) if type(value) is float else Q(value)

def integer(value):
    v = value if isinstance(value, Q) else rational(value)
    require(v.denominator == 1, 'noninteger_identifier')
    return v.numerator

def encoded(v):
    if v is None:
        return None
    return {'numerator': str(v.numerator), 'denominator': str(v.denominator), 'approximation': float(v)}

def nonempty_slots(values, count):
    require(len(values) == 8, 'card_arity')
    require(all(v is None or rational(v) == 0 for v in values[count:]), 'unsupported_extra_field')
    for v in values:
        if v is not None:
            rational(v)
    return values[:count]

def default(value, fallback, zero_defaults=False):
    if value is None:
        return Q(fallback)
    q = rational(value)
    return Q(fallback) if zero_defaults and q == 0 else q

def sign_counts(values):
    return {name: sum((v < 0, v == 0, v > 0)[i] for v in values)
            for i, name in enumerate(('negative', 'zero', 'positive'))}

def direction(values):
    differences = [b-a for a,b in zip(values, values[1:])]
    c = sign_counts(differences)
    return {
        'steps': len(differences), 'step_sign_counts': c,
        'strictly_increasing': bool(differences) and c['positive'] == len(differences),
        'strictly_decreasing': bool(differences) and c['negative'] == len(differences),
        'nondecreasing': not c['negative'], 'nonincreasing': not c['positive'],
        'constant': not c['negative'] and not c['positive'],
        'mixed_nonzero_step_signs': bool(c['negative'] and c['positive']),
        'has_equal_adjacent_values': bool(c['zero']),
    }

def point_summary(points):
    require(len(points) >= 2, 'fewer_than_two_points')
    xs, ys = zip(*points)
    secants = []
    for i, ((a,b),(c,d)) in enumerate(zip(points, points[1:])):
        dx,dy = c-a,d-b
        secants.append({'from_point':i, 'to_point':i+1, 'dx':encoded(dx),
                        'dy':encoded(dy), 'slope':encoded(dy/dx) if dx else None,
                        'status':'defined' if dx else 'undefined_zero_abscissa_step'})
    slopes = [Q(int(r['slope']['numerator']),int(r['slope']['denominator']))
              for r in secants if r['slope'] is not None]
    return {
        'point_count':len(points), 'x_min':encoded(min(xs)), 'x_max':encoded(max(xs)),
        'y_min':encoded(min(ys)), 'y_max':encoded(max(ys)),
        'x_order':direction(xs), 'y_order':direction(ys),
        'x_sign_counts':sign_counts(xs), 'y_sign_counts':sign_counts(ys),
        'origin_point_indices':[i for i,(x,y) in enumerate(points) if x == y == 0],
        'quadrant_counts':{f'x{sx}_y{sy}':sum((x>0)-(x<0)==sx and (y>0)-(y<0)==sy
                                           for x,y in points)
                           for sx in (-1,0,1) for sy in (-1,0,1)},
        'secants':secants, 'defined_slope_sign_counts':sign_counts(slopes),
        'undefined_slope_count':len(secants)-len(slopes),
        'first_point':[encoded(q) for q in points[0]],
        'last_point':[encoded(q) for q in points[-1]],
        'first_adjacent_slope':secants[0]['slope'],
        'last_adjacent_slope':secants[-1]['slope'],
    }

def curve_diagnostic(curve):
    fields=nonempty_slots(curve['values'],7)
    lcid=integer(fields[0]); require(lcid == curve['curve_id'], 'curve_header_id')
    sidr=integer(default(fields[1],0)); datatype=integer(default(fields[6],0))
    require(sidr in (0,1,2) and datatype in (0,1), 'unsupported_curve_header')
    sfa=default(fields[2],1,True); sfo=default(fields[3],1,True)
    offa=default(fields[4],0); offo=default(fields[5],0)
    original=[]; transformed=[]; rows=[]
    for i,p in enumerate(curve['points']):
        require(len(p['values']) == 2, 'point_arity')
        a,o=map(rational,p['values'])
        x,y=sfa*(a+offa),sfo*(o+offo)
        original.append((a,o)); transformed.append((x,y))
        rows.append({'point_index':i,'source_line':p['line'],
                     'supplied':[encoded(a),encoded(o)], 'transformed':[encoded(x),encoded(y)]})
    return {'curve_id':lcid,'source_record':copy.deepcopy(curve),
            'effective_header':{'SIDR':sidr,'DATTYP':datatype,'SFA':encoded(sfa),
                                'SFO':encoded(sfo),'OFFA':encoded(offa),'OFFO':encoded(offo)},
            'generated_zero_points_branch':bool(offa>0 and datatype==0),
            'points':rows, 'supplied':point_summary(original),
            'transformed':point_summary(transformed)}, transformed

def index_unique(records, id_function, error):
    out={}
    for r in records:
        key=id_function(r)
        require(key not in out,error)
        out[key]=r
    return out

def card(cards, keyword, eid, expected_rows, used):
    key=keyword+':'+str(eid)
    if key not in cards:
        return None
    c=cards[key]
    require(c['keyword']==keyword and len(c['cards'])==expected_rows, 'card_keyword_or_rows')
    for row,n in zip(c['cards'],used):
        nonempty_slots(row['values'],n)
    require(integer(c['cards'][0]['values'][0])+integer(c['offset'])==eid,'effective_card_id')
    return c

def calculate(inventory, expected_count):
    targets=inventory['target_elements']
    require(len(targets)==expected_count,'selection_coverage')
    target_index=index_unique(targets, lambda e:integer(e['values'][0]),'duplicate_selected_element')
    curves=index_unique(inventory['curve_inventory'],lambda c:integer(c['curve_id']),'duplicate_curve_reference')
    cards=inventory['selected_cards']; diagnoses={}; transformed={}; chains=[]; unresolved=[]
    for eid,element in target_index.items():
        require(len(element['values'])==8,'element_arity')
        ev=element['values']; pid=integer(ev[1])
        require(element['source']==121,'unsupported_element_namespace')
        integer(ev[2]); integer(ev[3]); require(integer(default(ev[4],0))==0,'orientation_dependency_changed')
        s=default(ev[5],1); pf=integer(default(ev[6],0)); offset=default(ev[7],0)
        require(pf in (0,1),'print_flag_variant')
        part=card(cards,'*PART',pid,1,[8]); require(part is not None,'missing_part')
        pv=part['cards'][0]['values']; shift=integer(part['offset'])
        sectionid=integer(pv[1])+shift; mid=integer(pv[2])+shift
        section=card(cards,'*SECTION_DISCRETE',sectionid,2,[6,2])
        mat=card(cards,'*MAT_SPRING_NONLINEAR_ELASTIC',mid,1,[3])
        require(section is not None and mat is not None,'missing_section_or_material')
        sv=section['cards'][0]['values']; lim=section['cards'][1]['values']
        dro=integer(default(sv[1],0)); require(dro in (0,1),'unsupported_DRO')
        mv=mat['cards'][0]['values']; lcd=integer(mv[1]); lcr=integer(default(mv[2],0))
        refs={'LCD':lcd};
        if lcr != 0:
            refs['LCR']=lcr
        missing=[]
        for role,ref in refs.items():
            if ref not in curves:
                missing.append({'role':role,'curve_id':ref})
                continue
            if ref not in diagnoses:
                diagnoses[ref],transformed[ref]=curve_diagnostic(curves[ref])
        chain={
            'eid':eid,'effective_pid':pid,'source_element':copy.deepcopy(element),
            'part':copy.deepcopy(part),'section':copy.deepcopy(section),'material':copy.deepcopy(mat),
            'effective_section_id':sectionid,'effective_material_id':mid,
            'LCD':lcd,'LCR_supplied':mv[2],'LCR_numeric':lcr,
            'LCR_state':'nonzero_reference_followed' if lcr else 'zero_or_blank_no_nonzero_reference',
            'S_supplied':ev[5],'S_effective':encoded(s),'OFFSET_supplied':ev[7],
            'OFFSET_numeric':encoded(offset),'PF_supplied':ev[6],'PF_numeric':pf,
            'DRO_numeric':dro,'section_optional_supplied':dict(zip(('KD','V0','CL','FD','CDL','TDL'),sv[2:6]+lim[:2])),
            'missing_curve_dependencies':missing,
            'status':'source_dependency_unresolved' if missing else 'table_arithmetic_available',
        }
        if lcd in transformed:
            scaled=[(x,s*y) for x,y in transformed[lcd]]
            chain['element_scaled_supplied_points']=[[encoded(x),encoded(y)] for x,y in scaled]
            chain['element_scaled_diagnostic']=point_summary(scaled)
        if missing:
            unresolved.append({'eid':eid,'dependencies':missing})
        chains.append(chain)
    groups={}
    for chain in chains:
        s=chain['S_effective']; key=(chain['LCD'],s['numerator'],s['denominator'])
        groups.setdefault(key,[]).append({'eid':chain['eid'],'source':chain['source_element']['source'],
                                         'line':chain['source_element']['line']})
    for p,n in inventory['selected_part_counts'].items():
        require(integer(n)>=sum(c['effective_pid']==integer(int(p)) for c in chains),'part_population_coverage')
    return {
        'status':'SOURCE_DEPENDENCY_UNRESOLVED' if unresolved else 'SUPPLIED_TABLE_ARITHMETIC_COMPLETE',
        'selected_element_count':len(chains),'selected_part_counts':copy.deepcopy(inventory['selected_part_counts']),
        'selected_source_cards':copy.deepcopy(cards),'chains':chains,
        'curves':[diagnoses[k] for k in sorted(diagnoses)],
        'curve_scale_groups':[{'LCD':k[0],'S':{'numerator':k[1],'denominator':k[2]},'elements':v}
                              for k,v in sorted(groups.items())],
        'unresolved_dependencies':unresolved,
        'curve_inventory_ids':list(curves),
        'limits':[
            'Independent arithmetic on frozen root extraction, not independent raw-source verification.',
            'Exact fractions preserve parsed binary64 values, not original decimal lexemes.',
            'FD0 has no established immediate-failure or disabled-failure truth table in the reviewed pages.',
            'LCR0 is retained without asserting a solver scale or automatic inactive state.',
            'Origin/quadrants condition remains literally attributed to LCR, not reassigned to LCD.',
            'No solver-exact interpolation, extrapolation, unloading, energy, capacity, force history or cause.',
            'Curve records lack a keyword-variant field; base-registry classification is inherited from source producer.',
        ],
    }

def digest(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def check_pins(base,pins):
    actual={name:digest(base/name) for name in pins}
    require(actual==pins,'source_pin_mismatch')
    return actual

def save(path,value):
    with path.open('x') as f:
        json.dump(value,f,sort_keys=True,indent=2,allow_nan=False)
        f.write('\n')

def fixture(points=None):
    if points is None:
        points=[[-1.,-2.],[0.,0.],[1.,3.]]
    curve={'curve_id':7,'source':121,'keyword_line':30,'header_line':31,
           'values':[7.,0.,1.,1.,0.,0.,0.,None],
           'points':[{'line':32+i,'values':v} for i,v in enumerate(points)]}
    cards={}
    for keyword,values in [('*PART',[[20.,20.,20.,0.,0.,0.,0.,0.]]),
                           ('*SECTION_DISCRETE',[[20.,0.,0.,0.,0.,0.,None,None],[0.,0.,None,None,None,None,None,None]]),
                           ('*MAT_SPRING_NONLINEAR_ELASTIC',[[20.,7.,0.,None,None,None,None,None]])]:
        cards[keyword+':20']={'keyword':keyword,'source':121,'keyword_line':10,
                             'offset':0,'cards':[{'line':11+i,'values':v} for i,v in enumerate(values)]}
    return {'selected_cards':cards,'curve_inventory':[curve],'selected_part_counts':{'20':3},
            'target_elements':[{'source':121,'line':1,'values':[1.,20.,10.,11.,0.,1.,0.,0.]}]}

class Controls(unittest.TestCase):
    def test_fraction_binary_not_decimal(self):
        self.assertNotEqual(rational(0.1),Q(1,10))
        self.assertEqual(rational(0.1),Q(3602879701896397,36028797018963968))
    def test_nonfinite_and_bool(self):
        for x in [float('nan'),float('inf'),True,'2']:
            with self.assertRaises(SemanticError): rational(x)
    def test_offset_before_scale(self):
        c=fixture()['curve_inventory'][0]; c['values'][2:6]=[2.,3.,4.,5.]
        d,xy=curve_diagnostic(c); self.assertEqual(xy[0],(Q(6),Q(9)))
        self.assertTrue(d['generated_zero_points_branch'])
    def test_curve_zero_and_blank_defaults(self):
        for z in [0.,None]:
            c=fixture()['curve_inventory'][0]; c['values'][2:4]=[z,z]
            self.assertEqual(curve_diagnostic(c)[1][0],(Q(-1),Q(-2)))
    def test_element_zero_not_blank(self):
        a=fixture(); a['target_elements'][0]['values'][5]=0.
        self.assertEqual(calculate(a,1)['chains'][0]['element_scaled_diagnostic']['y_max'],encoded(Q(0)))
        a['target_elements'][0]['values'][5]=None
        self.assertEqual(calculate(a,1)['chains'][0]['element_scaled_diagnostic']['y_max'],encoded(Q(3)))
    def test_negative_force_scale(self):
        a=fixture(); a['target_elements'][0]['values'][5]=-2.
        s=calculate(a,1)['chains'][0]['element_scaled_diagnostic']
        self.assertEqual(s['y_min'],encoded(Q(-6))); self.assertEqual(s['defined_slope_sign_counts']['negative'],2)
    def test_duplicate_x(self):
        s=point_summary([(Q(0),Q(0)),(Q(0),Q(1)),(Q(1),Q(1))])
        self.assertIsNone(s['secants'][0]['slope']); self.assertEqual(s['undefined_slope_count'],1)
    def test_order_retained(self):
        p=[[2.,0.],[1.,2.],[1.,2.],[3.,-2.]]
        d,xy=curve_diagnostic(fixture(p)['curve_inventory'][0])
        self.assertEqual([x for x,y in xy],[Q(2),Q(1),Q(1),Q(3)])
        self.assertTrue(d['transformed']['x_order']['mixed_nonzero_step_signs'])
    def test_decreasing_and_all_slope_signs(self):
        s=point_summary([(Q(3),Q(0)),(Q(2),Q(1)),(Q(1),Q(1)),(Q(0),Q(0))])
        self.assertTrue(s['x_order']['strictly_decreasing'])
        self.assertEqual(s['defined_slope_sign_counts'],{'negative':1,'zero':1,'positive':1})
    def test_origin_coverage(self):
        d,_=curve_diagnostic(fixture()['curve_inventory'][0])
        self.assertEqual(d['supplied']['origin_point_indices'],[1])
        self.assertEqual(d['supplied']['x_sign_counts'],{'negative':1,'zero':1,'positive':1})
    def test_generated_point_branch(self):
        c=fixture()['curve_inventory'][0]; c['values'][4]=1.; c['values'][6]=1.
        self.assertFalse(curve_diagnostic(c)[0]['generated_zero_points_branch'])
        c['values'][6]=0.; c['values'][4]=-1.
        self.assertFalse(curve_diagnostic(c)[0]['generated_zero_points_branch'])
    def test_missing_curve_preserved(self):
        a=fixture(); a['curve_inventory']=[]; r=calculate(a,1)
        self.assertEqual(r['status'],'SOURCE_DEPENDENCY_UNRESOLVED')
        self.assertEqual(r['unresolved_dependencies'][0]['dependencies'],[{'role':'LCD','curve_id':7}])
        self.assertNotIn('element_scaled_diagnostic',r['chains'][0])
    def test_duplicate_curve(self):
        a=fixture(); a['curve_inventory']*=2
        with self.assertRaises(SemanticError): calculate(a,1)
    def test_duplicate_element(self):
        a=fixture(); a['target_elements']*=2
        with self.assertRaises(SemanticError): calculate(a,2)
    def test_coverage(self):
        with self.assertRaises(SemanticError): calculate(fixture(),17)
    def test_missing_card(self):
        a=fixture(); a['selected_cards'].pop('*PART:20')
        with self.assertRaises(SemanticError): calculate(a,1)
    def test_namespace_mismatch(self):
        a=fixture(); a['selected_cards']['*PART:20']['offset']=1000
        with self.assertRaises(SemanticError): calculate(a,1)
    def test_forward_reference(self):
        a=fixture(); unused=copy.deepcopy(a['curve_inventory'][0]); unused['curve_id']=8; unused['values'][0]=8.
        a['curve_inventory'].insert(0,unused)
        self.assertEqual(calculate(a,1)['curves'][0]['curve_id'],7)
    def test_fractional_identifier(self):
        with self.assertRaises(SemanticError): integer(2.1)
    def test_unsupported_fields(self):
        a=fixture(); a['selected_cards']['*MAT_SPRING_NONLINEAR_ELASTIC:20']['cards'][0]['values'][3]=9.
        with self.assertRaises(SemanticError): calculate(a,1)
    def test_orientation_changed(self):
        a=fixture(); a['target_elements'][0]['values'][4]=2.
        with self.assertRaises(SemanticError): calculate(a,1)
    def test_nonzero_lcr_missing(self):
        a=fixture(); a['selected_cards']['*MAT_SPRING_NONLINEAR_ELASTIC:20']['cards'][0]['values'][2]=8.
        r=calculate(a,1); self.assertEqual(r['unresolved_dependencies'][0]['dependencies'],[{'role':'LCR','curve_id':8}])
        self.assertIn('element_scaled_diagnostic',r['chains'][0])
    def test_zero_fields_not_interpreted(self):
        c=calculate(fixture(),1)['chains'][0]
        self.assertEqual(c['section_optional_supplied']['FD'],0.)
        self.assertEqual(c['LCR_state'],'zero_or_blank_no_nonzero_reference')
    def test_create_only(self):
        with tempfile.TemporaryDirectory(prefix='spring-arithmetic-control-') as d:
            p=Path(d)/'test.json'; save(p,{'test':1})
            with self.assertRaises(FileExistsError): save(p,{'test':2})
            self.assertEqual(json.loads(p.read_text()),{'test':1})
    def test_pin_refusal(self):
        with tempfile.TemporaryDirectory(prefix='spring-pin-control-') as d:
            p=Path(d)/'test.json'; save(p,{'test':1})
            with self.assertRaises(SemanticError): check_pins(Path(d),{'test.json':'0'*64})

def run_controls():
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    result=unittest.TextTestRunner(stream=sys.stderr,verbosity=1).run(suite)
    require(result.wasSuccessful(),'controls_failed')
    return {'count':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    parser.add_argument('--controls-only',action='store_true'); args=parser.parse_args()
    output=HERE/args.output
    require(output.parent==HERE and output.name.startswith('independent-spring-arithmetic'),'output_scope')
    require(not output.exists(),'output_exists')
    start=time.monotonic(); own=digest(Path(__file__)); controls=run_controls()
    if args.controls_only:
        save(output,{'status':'CONTROLS_PASS','controls':controls,'code_sha256':own,'command':sys.argv})
        print('CONTROLS_PASS',controls['count']); return
    before=check_pins(HERE,PINS)
    root=json.loads((HERE/'casea-root01.json').read_text())
    require(root['status']=='PASS','source_result_not_pass')
    try:
        result=calculate(root['result']['springs_numeric_inventory'],17)
        status=result['status']
    except SemanticError as exc:
        result={'error_code':str(exc)}; status='SEMANTIC_JOIN_FAILED'
    after=check_pins(HERE,PINS); require(digest(Path(__file__))==own,'code_changed')
    save(output,{'status':status,'result':result,'controls':controls,'pins_before':before,
                 'pins_after':after,'code_sha256':own,'command':sys.argv,
                 'elapsed_seconds':time.monotonic()-start,
                 'maxrss_bytes_darwin':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    print(status)
    if status=='SEMANTIC_JOIN_FAILED': sys.exit(2)

if __name__=='__main__':
    main()

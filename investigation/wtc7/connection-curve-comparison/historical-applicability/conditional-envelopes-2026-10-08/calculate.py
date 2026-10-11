"""Conditional windows from frozen ink rectangles, not established support."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
RECON = 'historical-applicability/footprint-reconciliation-2026-10-08.json'
RECON_SHA = 'ed4a1ded5e53b7d102c9462f5f939883640359da5c0472220a92fbba1b7a354e'
REP_SHA = '1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5'
EXCLUSIONS = {'F': [(850,225,1280,315),(1040,310,1160,470)],
              'E': [(470,1055,900,1148),(575,1138,695,1302)]}
CENTERS = {'root': {'F': (449,1294,224,829),'E': (473,1297,1048,1669)},
           'independent': {'F': (449,1294,224,829),'E': (474,1297,1048,1669)}}


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def module(name, path, expected=None):
    if expected and pin(path)['sha256'] != expected:
        raise ValueError('Changed method: '+str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


geometry = module('conditional_saved_geometry', BASE/'registration_controls.py',
                  '98873f48740f69499f509e1e1db5c425586d25811e83ae9c88c862db7e54bc54')
screen = module('conditional_saved_screen', HERE.parent/'screen.py')


def rows_ok(rows, height):
    if (not isinstance(rows,list) or any(type(x) is not int or not 0<=x<height for x in rows)
            or rows != sorted(set(rows))):
        raise ValueError('Malformed native row set')


def normalize(raw, route, height):
    old = 'column' in raw
    x = raw['column'] if old else raw['x']
    if type(x) is not int or x<0:
        raise ValueError('Malformed column')
    core = raw['core_rows'] if old else raw['core']
    fringe = raw['fringe_rows'] if old else raw['fringe']
    for rows in (core,fringe): rows_ok(rows,height)
    if set(core)&set(fringe): raise ValueError('Overlapping core/fringe')
    if not isinstance(raw['boundary_flags'],list): raise ValueError('Malformed boundary flags')
    e = {'column':x,'route':route,'core_rows':core,'fringe_rows':fringe,
         'status':raw['status'],'fragment_id':raw.get('fragment_id'),
         'boundary_flags':raw['boundary_flags']}
    members = raw.get('fragment_membership') if old else None
    if 'fragments' in raw:
        if members is not None: raise ValueError('Conflicting membership schemas')
        members = {}
        for item in raw['fragments']:
            key = item['fragment_id']
            if not isinstance(key,str) or not key.strip() or key in members:
                raise ValueError('Invalid or duplicate fragment')
            members[key] = {'core_rows':item['core'],'fringe_rows':item['fringe']}
    if members is not None:
        if not isinstance(members,dict): raise ValueError('Malformed membership')
        for key,item in members.items():
            if not isinstance(key,str) or not key.strip(): raise ValueError('Malformed member ID')
            for field in ('core_rows','fringe_rows'): rows_ok(item[field],height)
            if set(item['core_rows'])&set(item['fringe_rows']):
                raise ValueError('Overlapping fragment classes')
        for key,expected in [('core_rows',core),('fringe_rows',fringe)]:
            actual = set().union(*(set(m[key]) for m in members.values()))
            if actual!=set(expected): raise ValueError('Membership union differs from record')
        e['fragment_membership'] = members
    return e, raw.get('band_refs',[])+raw.get('unassigned_band_refs',[])


def render_rect(strip,rect):
    x0,y1 = strip.image_to_pdf(rect[0],rect[1])
    x1,y0 = strip.image_to_pdf(rect[2],rect[3])
    return (x0,y0,x1,y1),(x0/F(9,25),(F(792)-y1)/F(9,25),
                            x1/F(9,25),(F(792)-y0)/F(9,25))


def touches(a,b):
    return a[0]<=b[2] and b[0]<=a[2] and a[1]<=b[3] and b[1]<=a[3]


def axis(panel,reader):
    lo,hi = (-3,4) if reader=='root' else (-6,6)
    return {k:(F(v+lo),F(v+hi)) for k,v in zip('LRTB',CENTERS[reader][panel])}


def fractions_between(position,left,right,span):
    for value in (position,left,right):
        if len(value)!=2 or value[0]>value[1]: raise ValueError('Reversed interval')
    if right[0]<=left[1]: raise ValueError('Axis denominator not strictly positive')
    values = [span*(p-l)/(r-l) for p,l,r in itertools.product(position,left,right)]
    return min(values),max(values)


def map_axis(rect,panel,registration):
    a = axis(panel,registration)
    x = fractions_between((rect[0],rect[2]),a['L'],a['R'],F(8,5))
    y = fractions_between((-rect[3],-rect[1]),(-a['B'][1],-a['B'][0]),
                          (-a['T'][1],-a['T'][0]),F(1000000 if panel=='F' else 800000))
    return {'axis_id':panel+'-'+registration,'displacement_m':x,
            'ordinate':y,'ordinate_unit':'N' if panel=='F' else 'N-m'}


def base_row(raw,route,strip,box,panel):
    entry,refs = normalize(raw,route,strip.height)
    if not box[0]<=entry['column']<box[2]: raise ValueError('Column outside declared target')
    outer = entry['core_rows']+entry['fringe_rows']
    if any(not box[1]<=y<box[3] for y in outer): raise ValueError('Selected cell outside target')
    r = screen.classify(entry)
    reasons = list(r['reasons'])
    if refs: reasons.append('unassigned_band_reference')
    if entry['column'] in (box[0],box[2]-1) or any(y in (box[1],box[3]-1) for y in outer):
        if 'boundary' not in reasons: reasons.append('boundary')
    rect = r['native_cell_rectangle']
    pdf = render = None
    if rect is not None:
        pdf,render = render_rect(strip,rect)
        if any(touches(render,b) for b in EXCLUSIONS[panel]): reasons.append('composed_page_exclusion')
        for reg in ('root','independent'):
            a = axis(panel,reg)
            if not (a['L'][1]<render[0] and render[2]<a['R'][0]
                    and a['T'][1]<render[1] and render[3]<a['B'][0]):
                reasons.append('not_inside_all_'+reg+'_plot_bounds')
    return {'column':entry['column'],'route':route,'fragment_id':entry['fragment_id'],
            'reasons':reasons,'native_rectangle':rect,'pdf_rectangle':pdf,'render_rectangle':render}


def process(raw_routes,strip,box,panel):
    rows = []
    for route in ('solid','dash'):
        values = [base_row(r,route,strip,box,panel) for r in raw_routes[route]]
        if [r['column'] for r in values]!=list(range(box[0],box[2])):
            raise ValueError('Incomplete or unordered route coverage')
        for i,r in enumerate(values):
            reasons = r['reasons'].copy()
            neighbors = values[max(0,i-1):i]+values[i+1:i+2]
            if len(neighbors)!=2 or any(n['reasons'] or n['fragment_id']!=r['fragment_id'] for n in neighbors):
                reasons.append('fragment_end_or_interruption')
            result = dict(r,reasons=reasons,conditional_window=not reasons,
                          physical_windows=None,curve_support_established=False)
            if not reasons:
                result['physical_windows'] = [map_axis(r['render_rectangle'],panel,a) for a in ('root','independent')]
            rows.append(result)
    return rows


def rational_json(value):
    if isinstance(value,F): return str(value)
    raise TypeError('Unexpected output type')


def encoded(value):
    return (json.dumps(value,default=rational_json,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def save(path,raw):
    with path.open('xb') as stream: stream.write(raw)


def run(target):
    if target.exists(): raise FileExistsError('Existing result preserved')
    if pin(BASE/RECON)['sha256']!=RECON_SHA: raise ValueError('Changed reconciliation')
    if pin(BASE/'pypdf-representation01.json')['sha256']!=REP_SHA: raise ValueError('Changed representation')
    rec = json.loads((BASE/RECON).read_text())
    before = dict(rec['verified_input_pins'])
    for name,expected in before.items():
        if pin(BASE/name)!=expected: raise ValueError('Changed reconciled input: '+name)
    extras = [RECON,'pypdf-representation01.json','registration_controls.py','registration-root.md',
              'registration-independent.md','registration-comparison.md','historical-applicability/screen.py']
    extras += [str((HERE/n).relative_to(BASE)) for n in ('PROTOCOL.md','calculate.py','test_calculate.py')]
    for name in extras: before[name] = pin(BASE/name)
    rep = json.loads((BASE/'pypdf-representation01.json').read_text(),parse_float=F)
    strips = {r['name']:geometry.Strip(r['name'],*r['native_dimensions'],r['ctm']) for r in rep['image_invocations']}
    readings = []
    for pair in rec['pairs']:
        for region in pair['completed_footprints']:
            strip = strips[region['source']]
            for reader in region['readers']:
                path = reader['path']; d = json.loads((BASE/path).read_text())
                routes = d.get('routes')
                if routes is None:
                    routes = {r:[e for e in d['observations'] if e['route']==r] for r in ('solid','dash')}
                rows = process(routes,strip,region['target_box'],pair['pair'][0])
                if len(rows)!=reader['route_records']: raise ValueError('Unexpected record count')
                readings.append({'pair':pair['pair'],'source':region['source'],'reader_path':path,'rows':rows,
                                 'summary':{'records':len(rows),'conditional_windows':sum(r['conditional_window'] for r in rows),
                                            'reasons_nonexclusive':dict(Counter(k for r in rows for k in r['reasons']))}})
    after = {name:pin(BASE/name) for name in before}
    if before!=after: raise ValueError('Inputs changed during calculation')
    total = sum(r['summary']['records'] for r in readings)
    if total!=10840 or len(readings)!=34: raise ValueError('Reconciliation scope mismatch')
    output = {'status':'conditional_preparation_not_accepted_measurement','inputs':before,'inputs_after':after,
              'axis_boxes':{p+'-'+a:axis(p,a) for p in 'FE' for a in CENTERS},
              'assumptions':['Hidentity','Hsupport','Hink0'],'readings':readings,'records':total,
              'human_accepted':False,'common_support':None,'quantile_targets':None,'model_discrepancies':None,
              'outside_target_inventory':RECON,'shared_axis_parameters':True,
              'limits':'Conditional marginal windows only; not independent errors, centerlines, curve support or calibrated confidence bounds.'}
    raw = encoded(output); save(target,raw)
    return {'records':total,'readings':len(readings),'conditional_windows':sum(r['summary']['conditional_windows'] for r in readings),
            'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run',choices=('run01','run02'))
    args = parser.parse_args()
    print(json.dumps(run(HERE/(args.run+'.json')),sort_keys=True))

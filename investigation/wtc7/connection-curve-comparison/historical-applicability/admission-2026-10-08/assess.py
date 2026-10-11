"""Conditional common-page coverage; no actual support or model discrepancy."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD = 'historical-applicability/force56-extension-2026-10-08/'
NEW = 'native-footprint-pass/force6-im3/'
CALC = 'historical-applicability/conditional-envelopes-2026-10-08/calculate.py'
ADAPTER = 'historical-applicability/approach34-extension-2026-10-08/extend.py'
PAIR_IDS = tuple(p+str(n) for p in 'FE' for n in range(3,10))
ROLES = ('primary', 'peer')
STATES = ('gap', 'solid_only', 'dash_only', 'overlapping_candidate_coverage',
          'shared_ink_ownership_conflict', 'paired_local_candidate')
FIXED = {
    OLD+'run-v2-01.json': '3b9e96e03a0daa37a0c30e8b9e4eb540b0b350a1b3ae832eeb3acc161815dd07',
    OLD+'run-v2-02.json': '3b9e96e03a0daa37a0c30e8b9e4eb540b0b350a1b3ae832eeb3acc161815dd07',
    OLD+'independent-check.json': '89b2948f2233fe0ae1883245fbe5166a84de586d707b510ae195578b8216081b',
    NEW+'independent-check.json': '22491e6a1e4459941dff884dab4b8d54e389c3731847c5fd1ae8849ca4d8b591',
    NEW+'reader-primary.json': 'd53723cc3d1b86bdbaf5cbed2dec5690e18ddf67efad2dae323bc7905690a3e9',
    NEW+'reader-peer.json': 'ab84ccc41a395414982489c8ef4e9d874908a4e79c6b08a84a6d3c651ba32f42',
    NEW+'compare.py': '63dae6eb1e69ac974f4a065650440ac13f5fbb5f4cbfdd41b7bddad8f2076ce7',
    CALC: '9d3f00efca8cb858b80a2b34c11f8253d2de59c66b46257df9dfc715d73ee89a',
    ADAPTER: '18f5862d014c5e9848cd6332da3929437c7ff93031e3ca255730d1f9e0dfc3f0',
    'pypdf-representation01.json': '1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(value):
    require(type(value) in (int, str, F), 'Exact rational required, not float/bool')
    return F(value)


def encode(value):
    def default(item):
        if type(item) is F:
            return str(item)
        raise TypeError('Unexpected JSON type')
    return (json.dumps(value, default=default, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def pin(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def load(path):
    return json.loads(Path(path).read_text())


def include(pins, path, expected=None):
    path = Path(path).resolve()
    key = os.path.relpath(path, BASE)
    observed = pin(path)
    if type(expected) is str:
        require(observed['sha256'] == expected, 'Changed frozen input '+key)
    elif expected is not None:
        require(type(expected) is dict and set(expected) == {'sha256','bytes'} and
                type(expected['bytes']) is int and expected['bytes'] >= 0 and
                observed == expected, 'Changed/invalid input pin '+key)
    require(key not in pins or pins[key] == observed, 'Conflicting pin '+key)
    pins[key] = observed
    return key


def inherit(pins, owner, data, root):
    require(data['inputs'] == data['inputs_after'], 'Before/after receipt differs '+str(owner))
    for name, expected in data['inputs'].items():
        include(pins, root/name, expected)


def import_fixed(name):
    require(pin(BASE/name)['sha256'] == FIXED[name], 'Changed import '+name)
    spec = importlib.util.spec_from_file_location('admission_'+Path(name).stem, BASE/name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def shared_ink(first, second):
    if first['source'] != second['source']:
        return False
    a, b = first['native_rectangle'], second['native_rectangle']
    return max(a[0],b[0]) < min(a[2],b[2]) and max(a[1],b[1]) < min(a[3],b[3])


def validate_cells(cells):
    ids = []
    for cell in cells:
        require(cell['route'] in ('solid','dash'), 'Unknown route')
        require(type(cell['id']) is str and cell['id'] and cell['id'] not in ids, 'Duplicate/empty cell ID')
        ids.append(cell['id'])
        a,b = map(rational, cell['render_x'])
        require(a < b, 'Reversed/zero source interval')
        rect = cell['native_rectangle']
        require(type(rect) is list and len(rect)==4 and all(type(x) is int for x in rect), 'Native cell rectangle')
        require(rect[0] < rect[2] and rect[1] < rect[3], 'Native rectangle area')
        require(type(cell['source']) is str and cell['source'], 'Source identity')
        require(type(cell['body']) is list and len(cell['body'])==3 and
                all(type(x) is str and x for x in cell['body']), 'Reader-local body identity')


def partition(cells):
    """Sweep exact source edges; preserve every active reference and gap."""
    validate_cells(cells)
    indexed = {cell['id']:cell for cell in cells}
    events = defaultdict(lambda: {'start':set(), 'end':set()})
    for cell in cells:
        a,b = map(rational,cell['render_x'])
        events[a]['start'].add(cell['id'])
        events[b]['end'].add(cell['id'])
    edges = sorted(events)
    active, segments = set(), []
    for left,right in zip(edges,edges[1:]):
        active.difference_update(events[left]['end'])
        active.update(events[left]['start'])
        by_route = {route:sorted(key for key in active if indexed[key]['route']==route)
                    for route in ('solid','dash')}
        solid,dash = by_route['solid'],by_route['dash']
        conflicts = [[s,d] for s in solid for d in dash if shared_ink(indexed[s],indexed[d])]
        if not solid and not dash:
            status = 'gap'
        elif not dash:
            status = 'solid_only'
        elif not solid:
            status = 'dash_only'
        elif len(solid)>1 or len(dash)>1:
            status = 'overlapping_candidate_coverage'
        elif conflicts:
            status = 'shared_ink_ownership_conflict'
        else:
            status = 'paired_local_candidate'
        segments.append({'render_x':[left,right], 'solid_refs':solid,'dash_refs':dash,
                         'shared_ink_conflicts':conflicts, 'status':status,
                         'overlapping_routes':[r for r in ('solid','dash') if len(by_route[r])>1]})
    runs = []
    for index, segment in enumerate(segments):
        if segment['status'] != 'paired_local_candidate':
            continue
        signature = [indexed[segment[r+'_refs'][0]]['body'] for r in ('solid','dash')]
        left,right = segment['render_x']
        if runs and runs[-1]['render_x'][1] == left and runs[-1]['body_pair']==signature:
            runs[-1]['render_x'][1] = right
            runs[-1]['segment_indices'].append(index)
        else:
            runs.append({'render_x':[left,right], 'body_pair':signature,'segment_indices':[index]})
    lengths = {status:sum((s['render_x'][1]-s['render_x'][0] for s in segments if s['status']==status),F(0)) for status in STATES}
    own = {route:sum((s['render_x'][1]-s['render_x'][0] for s in segments if s[route+'_refs']),F(0)) for route in ('solid','dash')}
    common = sum((s['render_x'][1]-s['render_x'][0] for s in segments if s['solid_refs'] and s['dash_refs']),F(0))
    return {'segments':segments, 'paired_runs':runs, 'render_lengths':lengths,
            'own_candidate_render_lengths':own, 'any_paired_render_length':common,
            'paired_segment_count':sum(s['status']=='paired_local_candidate' for s in segments)}


def length_bounds(length, axis):
    length = rational(length)
    require(length >= 0, 'Negative length')
    left,right = ([rational(x) for x in axis[k]] for k in ('L','R'))
    require(len(left)==len(right)==2 and left[0]<=left[1] and right[0]<=right[1]
            and right[0]>left[1], 'Invalid shared axis')
    return [F(8,5)*length/(right[1]-left[0]), F(8,5)*length/(right[0]-left[1])]


def make_cells(readings, roles, regions):
    result = []
    for reading in readings:
        path = reading['reader_path']
        require(path in roles and path in regions, 'Unrostered reading')
        region = regions[path]
        require(reading['pair']==region['pair'] and reading['source']==region['source'], 'Reading identity mismatch')
        for row in reading['rows']:
            require(type(row['conditional_window']) is bool and row['curve_support_established'] is False, 'Conditional status required')
            if not row['conditional_window']:
                continue
            require(row['reasons']==[] and row['fragment_id'], 'Eligible row with reason or no body')
            rect = row['render_rectangle']
            require(len(rect)==4 and all(rational(rect[i])<rational(rect[i+2]) for i in (0,1)), 'Render rectangle')
            result.append({'id':path+':'+row['route']+':'+str(row['column']),
                'pair':reading['pair'],'role':roles[path], 'reader_path':path,
                'source':reading['source'], 'target_box':region['target_box'],
                'route':row['route'], 'column':row['column'], 'fragment_id':row['fragment_id'],
                'native_rectangle':row['native_rectangle'], 'render_rectangle':rect,
                'render_x':[rational(rect[0]),rational(rect[2])],
                'body':[path,reading['source'],row['fragment_id']]})
    validate_cells(result)
    return result


def pairings(pair, cells, axes):
    found = []
    for solid_role in ROLES:
        for dash_role in ROLES:
            chosen = [cell for cell in cells if cell['pair']==pair and
                      cell['role']==(solid_role if cell['route']=='solid' else dash_role)]
            result = partition(chosen)
            length = result['render_lengths']['paired_local_candidate']
            result.update(solid_reader=solid_role,dash_reader=dash_role,
                conditional_candidate_length_m={axis_id:length_bounds(length,axis)
                    for axis_id,axis in axes.items() if axis_id.startswith(pair[0]+'-')},
                actual_D=None, candidate_set='C_H', human_accepted=False)
            found.append(result)
    return found


def build():
    before = {}
    for name,sha in FIXED.items():
        include(before,BASE/name,sha)
    old = load(BASE/(OLD+'run-v2-01.json'))
    require((BASE/(OLD+'run-v2-01.json')).read_bytes()==(BASE/(OLD+'run-v2-02.json')).read_bytes(),'Old repeat differs')
    inherit(before,OLD,old,BASE)
    old_receipt = load(BASE/(OLD+'independent-check.json'))
    require(old_receipt['input_pins_unchanged_after_check'] is True and
            old_receipt['required_total_pin_count']==len(old['inputs']), 'Prior independent coverage')
    require(hashlib.sha256(json.dumps(old['inputs'],sort_keys=True,allow_nan=False).encode()).hexdigest()
            ==old_receipt['required_input_map_sha256'], 'Prior independent dependency-map checksum')
    for name,expected in old_receipt['fixed_reference_pins'].items():
        include(before,BASE/name,expected)
    include(before,BASE/(OLD+'independent_check.py'),old_receipt['checker_pin'])
    for name,expected in old_receipt['run_pins'].items():
        include(before,BASE/OLD/name,expected)
    inherit(before,NEW+'independent-check.json',load(BASE/(NEW+'independent-check.json')),BASE/NEW)
    for name in ('NUMERICAL-PROTOCOL.md','HUMAN-SAMPLE-SELECTION.md','HUMAN-REVIEW-GATE.md',NEW+'report.md',NEW+'reader-primary-notes.md',NEW+'reader-peer-notes.md'):
        include(before,BASE/name)
    for name in ('PROTOCOL.md','assess.py','test_assess.py'):
        include(before,HERE/name)
    calc,adapter,validator = (import_fixed(name) for name in (CALC,ADAPTER,NEW+'compare.py'))
    for name,sha in validator.HELPERS.items():
        key = os.path.relpath((BASE/NEW/name).resolve(),BASE)
        require(key in before and before[key]['sha256']==sha,'Unpinned validator helper')
    require(len(old['readings'])==42 and old['records']==13240,'Old inventory scope')
    preserved_old_readings = encode(old['readings'])
    require(tuple(item['pair'] for item in old['inventory']['pairs'])==PAIR_IDS,'Pair scope/order')
    roles,regions = {},{}
    for pair in old['inventory']['pairs']:
        for region in pair['completed_footprints']:
            require(len(region['readers'])==2,'Exactly two readers')
            for role,reader in zip(ROLES,region['readers']):
                path = reader['path']
                require(path not in roles,'Duplicate reader path')
                roles[path]=role
                regions[path]={'pair':pair['pair'],'source':region['source'],'target_box':region['target_box']}
    require(set(roles)=={r['reader_path'] for r in old['readings']},'Reading roster coverage')
    rep = json.loads((BASE/'pypdf-representation01.json').read_text(),parse_float=F)
    invocation = next(r for r in rep['image_invocations'] if r['name']=='Im3')
    strip = calc.geometry.Strip('Im3',*invocation['native_dimensions'],invocation['ctm'])
    added,originals = [],{}
    for role in ROLES:
        path=NEW+f'reader-{role}.json'
        data=load(BASE/path)
        original_bytes=encode(data)
        validator.validate(data,role)
        adapted={route:[adapter.row_adapter(row,height=88) for row in data['routes'][route]] for route in ('solid','dash')}
        rows=calc.process(adapted,strip,[145,0,440,88],'F')
        require(encode(data)==original_bytes,'Original mutated')
        added.append({'pair':'F6','source':'Im3','reader_path':path,'rows':rows,
            'summary':{'records':len(rows),'conditional_windows':sum(row['conditional_window'] for row in rows),
                'reasons_nonexclusive':dict(Counter(k for row in rows for k in row['reasons']))}})
        originals[path]=data
        roles[path]=role
        regions[path]={'pair':'F6','source':'Im3','target_box':[145,0,440,88]}
    require(sum(len(r['rows']) for r in added)==1180,'New scope')
    readings=old['readings']+added
    cells=make_cells(readings,roles,regions)
    pairs=[{'pair':pair,'scenarios':pairings(pair,cells,old['axis_boxes'])} for pair in PAIR_IDS]
    require(encode(old['readings'])==preserved_old_readings,'Old reading object mutated')
    after={name:pin(BASE/name) for name in before}
    require(after==before,'Input changed during assessment')
    return {'status':'conditional_candidate_geometry_not_admitted_support','version':1,
        'inputs':before,'inputs_after':after,'prior_conditional_result':OLD+'run-v2-01.json',
        'old_reading_objects_unchanged':True,'old_reading_count':42,'old_record_count':13240,
        'old_reading_objects_sha256':hashlib.sha256(preserved_old_readings).hexdigest(),
        'new_readings':added,'new_source_originals':originals,'roles':roles,'regions':regions,
        'all_record_count':sum(len(r['rows']) for r in readings),'candidate_cells':cells,'pairs':pairs,
        'axis_boxes':old['axis_boxes'],'shared_axis_parameters':True,
        'assumptions':['Hidentity','Hsupport','Hink0'],
        'actual_D':None,'quantile_targets':None,'model_discrepancies':None,'human_accepted':False,
        'limits':['All old readings/exclusions remain in the pinned prior result, not overwritten.',
            'Four reader combinations are sensitivity scenarios, not independent evidence.',
            'C_H is not D. No marginal physical hulls were intersected.',
            'Overlapping coverage is withheld, not called physical multivaluedness.',
            'No polyline, gap/seam join, pre-raster guarantee, physical endpoint or cause finding.']}


def save(path,raw):
    with Path(path).open('xb') as output:
        output.write(raw)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run',choices=('01','02'))
    args=parser.parse_args()
    result=build()
    target=HERE/('run'+args.run+'.json')
    raw=encode(result)
    save(target,raw)
    print(json.dumps({'file':target.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
        'pairs':len(result['pairs']),'records':result['all_record_count'],
        'candidate_cells':len(result['candidate_cells']),'input_pins':len(result['inputs'])},sort_keys=True))

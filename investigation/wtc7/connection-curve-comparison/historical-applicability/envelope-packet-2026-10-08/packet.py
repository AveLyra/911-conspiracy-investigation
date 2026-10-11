"""Conditional 42-slot mapping packet; no ordinate discrepancies or acceptance."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import itertools
import json
import os
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
ADMISSION = BASE/'historical-applicability/admission-2026-10-08'
RUN_SHA = '4aeca445bc71d4495dd578df6a4de96e3bf2d54004b6afb0b1efcf7bb631930e'
RECEIPT_SHA = '9d05f112c632af128ae2d37f18a0fcab0ebabb78cc76f0d5bc453493feb88afd'
REP_SHA = '1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5'
PAGE_SHA = '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6'
PDF = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf')
PDF_SHA = 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4'
PAIRS = tuple(p+str(n) for p in 'FE' for n in range(3,10))
ROLES = ('primary','peer')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def q(value):
    require(type(value) in (str,int,F), 'exact rational required')
    return F(value)


def encode(value):
    def default(item):
        if type(item) is F:return str(item)
        raise TypeError('nonserializable value')
    return (json.dumps(value,default=default,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def load(path):
    return json.loads(Path(path).read_text(),parse_float=F)


def pin(path):
    raw=Path(path).read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def include(pins,path,expected=None):
    path=Path(path).resolve()
    key=os.path.relpath(path,BASE)
    observed=pin(path)
    if type(expected) is str:require(observed['sha256']==expected,'changed fixed input '+key)
    elif expected is not None:require(observed==expected,'changed input '+key)
    require(key not in pins or pins[key]==observed,'conflicting pin '+key)
    pins[key]=observed
    return key


def intervals(segments):
    """Length bookkeeping only; original excluded endpoints are not filled."""
    selected=[]
    previous=None
    for segment in segments:
        left,right=map(q,segment['render_x'])
        require(left<right and (previous is None or left>=previous),'unordered/overlapping elementary intervals')
        previous=right
        if segment['status']!='paired_local_candidate':continue
        if selected and selected[-1][1]==left:selected[-1][1]=right
        else:selected.append([left,right])
    return selected


def quantile(domain,fraction):
    fraction=q(fraction)
    require(0<fraction<1,'interior quantile required')
    parsed=[]
    for raw in domain:
        require(len(raw)==2,'two interval endpoints required')
        left,right=map(q,raw)
        require(left<right and (not parsed or left>=parsed[-1][1]),'invalid domain')
        parsed.append((left,right))
    length=sum((b-a for a,b in parsed),F(0))
    if not parsed:return {'page_x':None,'total_length':F(0),'component':None,'cumulative_tie':False}
    target=fraction*length
    cumulative=F(0)
    for i,(left,right) in enumerate(parsed):
        following=cumulative+right-left
        if following>=target:
            return {'page_x':left+target-cumulative,'total_length':length,'component':i,
                    'cumulative_tie':following==target}
        cumulative=following
    raise ValueError('unreachable quantile')


def point_state(scenario,x):
    if x is None:return {'status':'no_primary_target','segment_indices':[]}
    x=q(x)
    interiors=[];touching=[]
    for i,s in enumerate(scenario['segments']):
        left,right=map(q,s['render_x'])
        if left<x<right:interiors.append(i)
        if x in (left,right):touching.append(i)
    require(len(interiors)<=1,'overlapping scenario segments')
    if touching:return {'status':'boundary_unresolved','segment_indices':touching}
    if interiors:return {'status':scenario['segments'][interiors[0]]['status'],'segment_indices':interiors}
    return {'status':'outside_candidate_extent','segment_indices':[]}


def map_cell(cell,x,invocation):
    a,b,c,d,e,f=map(q,invocation['ctm']);w,h=invocation['native_dimensions']
    require(a>0 and d>0 and b==c==0,'only declared positive-axis CTMs')
    require(type(w) is int and type(h) is int and min(w,h)>0,'native dimensions')
    nr=cell['native_rectangle']
    require(len(nr)==4 and all(type(z) is int for z in nr),'native rectangle types')
    u0,v0,u1,v1=nr
    require(0<=u0<u1<=w and 0<=v0<v1<=h,'native rectangle bounds')
    render=[(e+a*F(u0,w))/F(9,25),(792-f-d+d*F(v0,h))/F(9,25),
            (e+a*F(u1,w))/F(9,25),(792-f-d+d*F(v1,h))/F(9,25)]
    require(render==list(map(q,cell['render_rectangle'])),'candidate CTM mismatch')
    require(render[0]<=x<=render[2],'target outside candidate cell')
    native_x=w*(F(9,25)*x-e)/a
    require(F(u0)<=native_x<=F(u1),'inverse native x outside footprint')
    return {'cell_id':cell['id'],'reader_path':cell['reader_path'],'role':cell['role'],
            'route':cell['route'],'source':cell['source'],'fragment_id':cell['fragment_id'],
            'native_rectangle':nr,'render_rectangle':render,'native_x':native_x,
            'boundary_touch':native_x in (u0,u1),'asset_url':'/source/'+cell['source']+'.jpg'}


def displacement(x,box):
    if x is None:return None
    left,right=([q(z) for z in box[k]] for k in ('L','R'))
    require(left[0]<=left[1]<right[0]<=right[1],'invalid x axis')
    values=[F(8,5)*(x-l)/(r-l) for l,r in itertools.product(left,right)]
    return [min(values),max(values)]


def duplicate_flags(slots):
    entries=defaultdict(list);pairs=defaultdict(list)
    for slot in slots:
        primary=[]
        for entry in slot['entries']:
            for role in ROLES:
                maps=entry['mappings'][role]
                footprint=tuple(sorted((m['source'],tuple(m['native_rectangle'])) for m in maps))
                if footprint:entries[(slot['pair'],entry['model'],role,footprint)].append(entry)
                if role=='primary':primary.append(footprint)
        if all(primary):pairs[(slot['pair'],tuple(primary))].append(slot)
    for key,group in entries.items():
        role=key[2]
        for entry in group:entry['duplicate_entries'][role]=[other['id'] for other in group if other is not entry]
    for group in pairs.values():
        for slot in group:slot['duplicate_paired_slots']=[other['id'] for other in group if other is not slot]


def make_slots(admission,invocations):
    require(tuple(p['pair'] for p in admission['pairs'])==PAIRS,'fourteen pair roster/order')
    slots=[];inventory=[]
    for pair in admission['pairs']:
        name=pair['pair'];scenarios={}
        for scenario in pair['scenarios']:
            key=(scenario['solid_reader'],scenario['dash_reader'])
            require(key not in scenarios,'duplicate reader scenario')
            scenarios[key]=scenario
        require(set(scenarios)==set(itertools.product(ROLES,repeat=2)),'all four scenarios required')
        primary=scenarios[('primary','primary')]
        domain=intervals(primary['segments'])
        inventory.append({'pair':name,'primary_length_bookkeeping':domain,
            'own_candidate_render_lengths':primary['own_candidate_render_lengths'],
            'all_scenarios_preserved_in':'admission-2026-10-08/run01.json'})
        cells=[c for c in admission['candidate_cells'] if c['pair']==name]
        for index,fraction in enumerate((F(1,4),F(1,2),F(3,4)),1):
            selected=quantile(domain,fraction);x=selected['page_x']
            states={s+'-'+d:point_state(scenarios[(s,d)],x) for s,d in itertools.product(ROLES,repeat=2)}
            status='unavailable_empty_primary_domain' if x is None else states['primary-primary']['status']
            require(x is None or status in ('paired_local_candidate','boundary_unresolved'),'invalid primary selection')
            slot={'id':f'CE-{name}Q{index}','pair':name,'quantile':fraction,
                  **selected,'selection_status':status,'scenario_states':states,
                  'displacement_m':{key:displacement(x,box) for key,box in admission['axis_boxes'].items() if key.startswith(name[0]+'-')},
                  'duplicate_paired_slots':[],'entries':[], 'human_accepted':False}
            for model,route in (('spring','solid'),('shell','dash')):
                mappings={role:[] for role in ROLES}
                if x is not None:
                    for c in cells:
                        left,right=map(q,c['render_x'])
                        if c['route']==route and left<=x<=right:
                            mappings[c['role']].append(map_cell(c,x,invocations[c['source']]))
                slot['entries'].append({'id':slot['id']+'-'+model,'model':model,'style':route,
                    'mappings':mappings,'duplicate_entries':{role:[] for role in ROLES},
                    'human_response':None,'human_status':'uninspected',
                    'reason':'No primary paired coverage; do not invent a coordinate.' if x is None else
                             'Boundary locator only; point support unresolved.' if status=='boundary_unresolved' else
                             'Conditional local mapping proposed; not accepted curve support.'})
            slots.append(slot)
    duplicate_flags(slots)
    require(len(slots)==42 and sum(len(s['entries']) for s in slots)==84,'complete slot roster')
    return slots,inventory


def build():
    pins={}
    include(pins,ADMISSION/'run01.json',RUN_SHA);include(pins,ADMISSION/'run02.json',RUN_SHA)
    include(pins,ADMISSION/'independent-check.json',RECEIPT_SHA)
    receipt=load(ADMISSION/'independent-check.json')
    require(receipt['inputs']==receipt['inputs_after'],'prior receipt drift')
    for name,expected in receipt['inputs'].items():include(pins,BASE/name,expected)
    admission=load(ADMISSION/'run01.json')
    require(admission['human_accepted'] is False and admission['actual_D'] is None,'unexpected prior acceptance')
    require(admission['model_discrepancies'] is None,'discrepancy before selection')
    include(pins,BASE/'pypdf-representation01.json',REP_SHA)
    include(pins,PDF,PDF_SHA)
    rep=load(BASE/'pypdf-representation01.json')
    require(rep['source_sha256']==PDF_SHA,'source PDF identity')
    invocations={i['name']:i for i in rep['image_invocations']}
    require(set(invocations)=={f'Im{i}' for i in range(12)},'full strip roster')
    assets={}
    for name,inv in invocations.items():
        path=BASE/'native-strips01'/(name+'.jpg')
        key=include(pins,path,inv['encoded_jpeg_sha256'])
        require(pins[key]['bytes']==inv['encoded_jpeg_bytes'],'encoded source size')
        with Image.open(path) as im:
            require(list(im.size)==inv['native_dimensions'] and im.mode=='RGB','source image format')
        assets[name]={'path':key,**pins[key],'width':inv['native_dimensions'][0],
                      'height':inv['native_dimensions'][1],'ctm':inv['ctm'],'url':'/source/'+name+'.jpg'}
    page=BASE/'render01/page-076.png';key=include(pins,page,PAGE_SHA)
    with Image.open(page) as im:require(im.size==(1700,2200) and im.mode=='RGB','full page format')
    assets['page']={'path':key,**pins[key],'width':1700,'height':2200,'url':'/page.png'}
    for name in ('PROTOCOL.md','packet.py','test_packet.py'):
        include(pins,HERE/name)
    slots,inventory=make_slots(admission,invocations)
    after={name:pin(BASE/name) for name in pins}
    require(after==pins,'inputs changed during build')
    return {'status':'conditional_mapping_packet_pending_human','version':1,
        'domain_kind':'C_H_primary_primary_not_actual_D','slots':slots,'inventory':inventory,
        'assets':assets,'inputs':pins,'inputs_after':after,
        'source_pdf':{'path':os.path.relpath(PDF,BASE),'sha256':PDF_SHA,'physical_page':76,'printed_page':25},
        'parent_result':'historical-applicability/admission-2026-10-08/run01.json',
        'assumptions':['Hidentity','Hsupport','Hink0'],'actual_D':None,'model_discrepancies':None,
        'original_actual_D_sampling_fulfilled':False,'human_accepted':False,
        'summary':dict(Counter(s['selection_status'] for s in slots)),
        'limits':['A conditional mapping packet, not accepted support or a discrepancy result.',
            'Merging adjacent intervals is length bookkeeping, not closure of excluded endpoints.',
            'Uninspected entries remain uninspected; confirmed axes/legends need no repeat.',
            'Reader alternatives refer to the same page x, not their own quantiles.']}


def save(path,raw):
    with Path(path).open('xb') as stream:stream.write(raw)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('run',choices=('01','02'))
    args=parser.parse_args();result=build();raw=encode(result);path=HERE/('packet'+args.run+'.json')
    save(path,raw)
    print(json.dumps({'file':path.name,'pin':pin(path),'slots':len(result['slots']),
                     'summary':result['summary'],'input_pins':len(result['inputs'])},sort_keys=True))

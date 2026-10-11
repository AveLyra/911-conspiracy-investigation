"""Literal primary F5-Im2 ink reading; expansion never selects from RGB."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'PROTOCOL.md': '4df4510ba5664888124512ab052cfe535fce23dba482e5021cc69d4d0c47f285',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../../native-strips01/Im2.jpg': '9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'read_context.py': 'cfce638b10df652fd8a8273603e9dee12c71952f567d4c1f534d6cd12e2b05ab',
    'context01.json': '161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
    'context02.json': '161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
}
SOLID = [
    [225,225,[73,74],[72,75],'s01'],
    [228,228,[72],[71,73],'s02'],
    [229,229,[71,72],[70,73],'s02'],
    [230,230,[71],[70,72],'s02'],
    [231,232,[70,71],[69,72],'s02'],
    [233,233,[69,70],[68,71],'s02'],
    [234,234,[69],[68,70],'s02'],
    [235,235,[68,69],[67,70],'s02'],
    [236,236,[68],[67,69],'s02'],
    [237,237,[67,68],[66,69],'s02'],
    [238,238,[67],[66,68],'s02'],
    [239,239,[66,67],[65,68],'s02'],
    [240,241,[65,66],[64,67],'s02'],
    [248,248,[65],[64,66],'s03'],
    [249,249,[64,65],[63,66],'s03'],
    [250,251,[64,65],[66],'s03'],
    [252,252,[64,65],[63,66],'s03'],
    [253,255,[64],[63,65],'s03'],
    [256,259,[63,64],[62,65],'s03'],
    [260,262,[63],[62,64],'s03'],
    [263,266,[62,63],[61,64],'s03'],
    [267,268,[62],[61,63],'s03'],
    [269,271,[62,63],[61,64],'s03'],
    [272,272,[63,64],[62,65],'s03'],
    [273,274,[63,64],[62,65],'s03'],
    [275,278,[64,65],[63,66],'s03'],
    [279,281,[65,66],[64,67],'s03'],
    [282,283,[66,67],[65,68],'s03'],
    [284,284,[67,68],[66,69],'s03'],
    [285,285,[67,68],[66],'s03'],
    [293,293,[69,70],[71],'s04'],
    [294,296,[70,71],[69,72],'s04'],
    [297,297,[71,72],[70,73],'s04'],
    [298,298,[71,72],[70,73],'s04'],
    [299,299,[72,73],[71,74],'s04'],
    [300,300,[72,73,74],[71,75],'s04'],
    [301,301,[73,74,75],[72,76],'s04'],
    [302,302,[74,75],[73,76],'s04'],
    [303,303,[75,76],[74,77],'s04'],
    [304,304,[76,77],[75,78],'s04'],
    [305,305,[77,78],[76,79],'s04'],
    [306,306,[78],[77,79],'s04'],
    [307,307,[78,79],[77,80],'s04'],
    [308,308,[79,80],[78,81],'s04'],
    [309,309,[80,81],[79,82],'s04'],
    [310,310,[81,82],[80,83],'s04'],
    [311,311,[81,82,83],[80,84],'s04'],
    [312,312,[82,83,84],[81,85],'s04'],
    [313,313,[83,84],[82,85],'s04'],
    [314,314,[84,85],[83,86],'s04'],
    [315,315,[85,86],[84,87],'s04'],
    [316,316,[86,87],[85],'s04'],
    [317,317,[87],[86],'s04'],
    [318,318,[],[87],'s04'],
]
DASH = [
    [258,258,[],[87],'d01'],
    [259,259,[87],[86],'d01'],
    [260,260,[],[87],'d01'],
    [262,262,[],[85,86],'d02'],
    [263,263,[85,86],[84,87],'d02'],
    [264,264,[85],[84,86],'d02'],
    [265,265,[84,85],[83,86],'d02'],
    [266,266,[83,84],[82,85],'d02'],
    [267,267,[82,83,84],[81,85],'d02'],
    [268,268,[82,83],[81,84],'d02'],
    [269,269,[],[82],'d02'],
    [271,271,[],[78,79],'d03'],
    [272,272,[79],[78,80],'d03'],
    [273,274,[78,79],[77,80],'d03'],
    [275,275,[77,78],[76,79],'d03'],
    [276,277,[77],[76,78],'d03'],
    [278,278,[],[76,77],'d03'],
    [280,280,[],[75],'d04'],
    [281,281,[74,75],[73,76],'d04'],
    [282,282,[73,74,75],[72,76],'d04'],
    [283,283,[72,73],[71,74,75],'d04'],
    [284,284,[71,72],[70,73],'d04'],
    [285,285,[70,71],[72],'d04'],
    [293,293,[65,66],[64,67],'d05'],
    [294,294,[65,66],[64,67],'d05'],
    [295,295,[65],[64,66],'d05'],
    [296,296,[],[65],'d05'],
    [298,298,[],[61,62],'d06'],
    [299,299,[60,61,62],[59,63],'d06'],
    [300,300,[60,61],[59,62],'d06'],
    [301,301,[59,60],[58,61],'d06'],
    [302,302,[59],[58,60],'d06'],
    [303,303,[58,59],[57,60],'d06'],
    [304,304,[],[58,59],'d06'],
    [306,306,[],[57],'d07'],
    [307,307,[],[56,57,58],'d07'],
    [308,308,[56,57],[55,58],'d07'],
    [309,309,[56,57],[55,58],'d07'],
    [310,311,[55,56],[54,57],'d07'],
    [312,312,[55,56],[54,57],'d07'],
    [313,313,[],[55,56],'d07'],
    [316,316,[],[54,55],'d08'],
    [317,317,[55,56],[54,57],'d08'],
    [318,318,[56,57,58],[55,59],'d08'],
    [319,319,[57,58,59],[56,60,61],'d08'],
    [320,320,[59,60],[58,61],'d08'],
    [321,321,[],[60],'d08'],
    [323,323,[61,62],[60,63],'d09'],
    [324,324,[60,61,62],[59,63],'d09'],
    [325,325,[59,60],[58,61],'d09'],
    [326,326,[58,59],[57,60],'d09'],
    [327,328,[58,59],[57,60],'d09'],
    [329,329,[],[58,59],'d09'],
    [330,330,[],[62,63],'d10'],
    [331,331,[62,63],[61,64],'d10'],
    [332,332,[63,64,65],[62,66],'d10'],
    [333,333,[64,65,66],[63,67],'d10'],
    [334,334,[65,66,67],[64,68],'d10'],
    [335,335,[66,67],[65,68],'d10'],
    [336,336,[],[67,68],'d10'],
    [339,339,[],[68,69],'d11'],
    [340,340,[68,69],[67,70],'d11'],
    [341,341,[67,68],[66,69],'d11'],
    [342,343,[67,68],[66,69],'d11'],
    [344,344,[67,68,69],[66,70],'d11'],
    [345,345,[],[68,69],'d11'],
    [346,346,[72,73,74],[71,75],'d12'],
    [347,347,[73,74,75,76],[72,77],'d12'],
    [348,348,[76,77],[75,78],'d12'],
    [349,349,[77,78],[76,79],'d12'],
]
UNASSIGNED = [
    [226,227,[],[72,73,74,75],'u-red'],
    [242,242,[],[64,65,66,67],'u-green'],
    [243,245,[],[63,64,65,66,67],'u-green'],
    [246,246,[],[63,64,65,66],'u-green'],
    [247,247,[],[64,65,66],'u-green'],
    [250,251,[],[63],'u-green-fringe'],
    [285,285,[],[69],'u-cross'],
    [286,286,[],[67,68,69,70,71],'u-cross'],
    [287,290,[],[67,68,69,70],'u-cross'],
    [291,292,[],[66,67,68,69,70],'u-cross'],
    [314,314,[],[55],'u314'],
    [337,337,[],[67],'u337'],
    [338,338,[],[69],'u338'],
]


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def pieces(runs,x):
    return [{'fragment_id':r[4],'core':r[2],'fringe':r[3]}
            for r in runs if r[0] <= x <= r[1]]


def record(x,fragments,refs,band=False):
    core = sorted(y for p in fragments for y in p['core'])
    fringe = sorted(y for p in fragments for y in p['fringe'])
    if len(core) != len(set(core)) or len(fringe) != len(set(fringe)) or set(core)&set(fringe):
        raise ValueError('Duplicate literal membership')
    selected = core+fringe
    flags = []
    if selected:
        if x == 225: flags.append('target_left')
        if x == 349: flags.append('target_right')
        if 50 in selected: flags.append('target_top')
        if 87 in selected: flags.append('target_bottom')
    if band:
        status = 'identity_conflict' if selected else 'no_attributable_cells'
        note = 'Unresolved blue/red or blue/green overlap, same-color crossing, or pale interbody material retained once. Same-color crossing cells are not copied into both models. Empty does not prove absent ink.'
    else:
        status = ('boundary_truncated' if flags else 'identified_local_fragment' if core else 'fringe_only') if selected else ('identity_conflict' if refs else 'no_attributable_cells')
        note = 'Manual continuous/broken blue-style attribution from complete page/strip and raw RGB. Separate IDs across unresolved crossings avoid inferring connectivity. Core/fringe is subjective, not calibrated containment; empty is not zero support.'
    return {'x':x,'core':core,'fringe':fringe,
            'fragment_id':fragments[0]['fragment_id'] if len(fragments) == 1 else None,
            'fragments':fragments,'status':status,'boundary_flags':flags,'band_refs':refs,'note':note}


def build():
    before = {k:pin(HERE/k) for k in EXPECTED}
    if any(before[k]['sha256'] != v for k,v in EXPECTED.items()): raise ValueError('Changed dependency')
    routes = {'solid':[],'dash':[]}
    bands = []
    for x in range(225,350):
        unassigned = pieces(UNASSIGNED,x)
        bands.append(record(x,unassigned,[],True))
        solid_refs = [p['fragment_id'] for p in unassigned if p['fragment_id'] in ('u-red','u-green','u-green-fringe','u-cross')]
        dash_refs = [p['fragment_id'] for p in unassigned if p['fragment_id'] in ('u-cross','u314','u337','u338')]
        routes['solid'].append(record(x,pieces(SOLID,x),solid_refs))
        routes['dash'].append(record(x,pieces(DASH,x),dash_refs))
    pixels = {(r['x'],r['y']):r['rgb'] for r in json.loads((HERE/'context01.json').read_text())['cells']['F5-Im2']}
    for group in [*routes.values(),bands]:
        if [r['x'] for r in group] != list(range(225,350)): raise ValueError('Coverage')
        for r in group:
            for key in ('core','fringe'):
                if r[key] != sorted(set(r[key])): raise ValueError('Row order')
                for y in r[key]:
                    if type(y) is not int or not 50 <= y < 88: raise ValueError('Bounds')
                    if pixels[r['x'],y] == [255,255,255]: raise ValueError(('Selected exact white',r['x'],y))
    for s,d,u in zip(routes['solid'],routes['dash'],bands):
        sets = [set(r['core']+r['fringe']) for r in (s,d,u)]
        if any(sets[i]&sets[j] for i,j in [(0,1),(0,2),(1,2)]): raise ValueError('Duplicate attribution')
    if before != {k:pin(HERE/k) for k in EXPECTED}: raise ValueError('Changed dependency')
    return {
        'pair':'F5','region_id':'F5-Im2','source_image':'Im2.jpg','reader':'primary',
        'reader_agent':'force5_primary','status':'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box':[225,50,350,88],'context_box':[223,48,352,88],
        'inputs':before,'script_pin':pin(Path(__file__)),
        'literal_instructions':{'solid':SOLID,'dash':DASH,'unassigned':UNASSIGNED},
        'coverage':{'native_strip_viewed':True,'complete_composed_page_viewed':True,
            'view_receipt':'view_image calls preceding raw receipt 7b655f: unchanged full Im4, Im2 and page076',
            'page_display_limit':'1700x2200 page displayed1376x1780; no coordinates taken from resized page',
            'context_blocks_inclusive':[[223,247],[248,272],[273,297],[298,322],[323,351]],
            'raw_read_receipts':['8dfc3d','f2ff7a','c0a85c','09c7ae','61a1f5'],
            'context_rows_inclusive':[48,87],'context_cells':5160,
            'all_target_columns_read':True,'model_route_records':250,'unassigned_band_records':125},
        'identity_basis':'Confirmed blue five-bolt legend, solid Spring and broken Shell. Full-strip continuous crest/decline style and broken local dash bodies distinguish routes where visible. Blue/red, blue/green and same-blue close/crossing regions are explicitly unresolved; no identification from vertical order alone.',
        'independence':'Prior-informed primary AI reader prospectively designated before new pixels; no force45 peer or root-F4 annotation content read before freezing both F5 regions. Older E9-root implementation was inspected solely for representation design.',
        'limits':'Native ink only; no RGB threshold selection, interpolation, original-curve bound, physical ordinate, support, seam join, historical inference or human acceptance. Region-local IDs do not connect to Im4 IDs.',
        'human_accepted':False,'physical_support':None,'routes':routes,'unassigned_bands':bands}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output',required=True); args = p.parse_args()
    if args.output not in ['reader-F5-Im2-primary.json','reader-F5-Im2-primary-repeat.json']: raise ValueError('Output name')
    out = HERE/args.output
    result = build()
    with out.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    print(json.dumps({'output':str(out),'pin':pin(out),'route_records':250,'band_records':125}))

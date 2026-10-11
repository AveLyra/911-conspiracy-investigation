"""Literal prior-informed primary F4/Im4 reading; no RGB-driven selection."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'PROTOCOL.md':'4df4510ba5664888124512ab052cfe535fce23dba482e5021cc69d4d0c47f285',
    '../PROTOCOL.md':'2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json':'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../../native-strips01/Im4.jpg':'53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd',
    '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'read_context.py':'cfce638b10df652fd8a8273603e9dee12c71952f567d4c1f534d6cd12e2b05ab',
    'context01.json':'161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
    'context02.json':'161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
}
# Manual inclusive x ranges, explicit row sets and local fragment identity.
SOLID = [
    [331,331,[],[0,1,2],'s01'], [332,332,[],[0,1,2,3],'s01'],
    [333,333,[0,1],[2,3],'s01'], [334,334,[0,1,2],[3,4],'s01'],
    [335,335,[1,2,3],[0,4,5],'s01'], [336,336,[2,3,4,5],[1,6,7],'s01'],
    [337,337,[3,4,5,6],[2,7,8],'s01'], [338,338,[5,6,7,8],[4,9,10],'s01'],
    [339,339,[6,7,8,9],[5,10,11],'s01'], [340,340,[8,9,10,11],[7,12,13],'s01'],
    [341,341,[9,10,11,12],[8,13,14],'s01'], [342,342,[11,12,13],[10,14,15],'s01'],
    [343,343,[12,13,14,15],[11,16,17],'s01'], [344,344,[14,15,16],[13,17,18],'s01'],
    [345,345,[15,16,17,18],[14,19,20],'s01'], [346,346,[17,18,19,20],[16,21,22],'s01'],
    [347,347,[18,19,20,21],[17,22,23],'s01'], [348,348,[20,21,22],[19,23,24],'s01'],
    [349,349,[21,22,23,24],[20,25,26],'s01'], [350,350,[23,24,25],[22,26,27],'s01'],
    [351,351,[24,25,26,27],[23,28,29],'s01'], [352,352,[26,27,28],[25,29,30],'s01'],
    [353,353,[27,28,29,30],[26,31,32],'s01'], [354,354,[29,30,31],[28,32,33],'s01'],
    [355,355,[30,31,32,33],[29,34,35],'s01'], [356,356,[32,33,34,35],[31,36,37],'s01'],
    [357,357,[33,34,35,36],[32,37,38],'s01'], [358,358,[35,36,37],[34,38,39],'s01'],
    [359,359,[37,38,39],[36,40,41],'s01'], [360,360,[38,39,40,41],[37,42,43],'s01'],
    [361,361,[40,41,42],[39,43,44],'s01'], [362,362,[41,42,43,44],[40,45,46],'s01'],
    [363,363,[43,44,45,46],[42,47,48],'s01'], [364,364,[44,45,46,47],[43,48,49],'s01'],
    [365,365,[46,47,48,49],[45,50,51],'s01'], [366,366,[48,49,50],[47,51,52],'s01'],
    [367,367,[49,50,51,52],[48,53,54],'s01'], [368,368,[51,52,53],[50,54,55],'s01'],
    [369,369,[52,53,54,55],[51,56,57],'s01'], [370,370,[54,55,56],[53,57,58],'s01'],
    [371,371,[55,56,57],[54,58,59],'s01'], [372,372,[56,57,58],[55,59,60],'s01'],
    [373,373,[57,58,59,60],[56,61],'s01'], [374,374,[58,59,60,61],[57,62,63],'s01'],
    [375,375,[60,61,62],[59,63,64],'s01'], [376,376,[61,62,63],[60,64,65],'s01'],
    [377,377,[62,63,64],[61,65,66],'s01'], [378,378,[63,64,65],[62,66,67],'s01'],
    [379,379,[64,65,66],[63,67,68],'s01'], [380,380,[65,66,67,68],[64,69,70],'s01'],
    [381,381,[66,67,68,69],[65,70,71],'s01'], [382,382,[68,69,70],[67,71,72],'s01'],
    [383,383,[69,70,71],[68,72,73],'s01'], [384,384,[70,71,72,73],[69,74,75],'s01'],
    [385,385,[71,72,73,74],[70,75,76],'s01'], [386,386,[72,73,74,75],[71,76,77],'s01'],
    [387,387,[73,74,75,76],[72,77,78],'s01'], [388,388,[74,75,76,77],[73,78,79],'s01'],
    [389,389,[76,77,78],[75,79,80],'s01'], [390,390,[77,78,79],[76,80,81],'s01'],
    [391,391,[78,79,80,81],[77,82,83],'s01'], [392,392,[80,81,82],[79,83,84],'s01'],
    [393,393,[81,82,83],[80,84,85],'s01'], [394,394,[82,83,84],[81,85,86],'s01'],
    [395,395,[83,84,85],[82,86,87],'s01'], [396,396,[84,85,86],[83,87],'s01'],
    [397,397,[85,86,87],[84],'s01'], [398,398,[86,87],[85],'s01'],
    [399,399,[87],[86],'s01'], [400,400,[],[87],'s01'],
]
DASH = [
    [355,355,[],[3,4,5],'d01'], [356,356,[2,3,4],[1,5,6],'d01'],
    [357,357,[3,4,5],[2,6,7],'d01'], [358,358,[4,5],[3,6,7],'d01'],
    [359,359,[5,6],[4,7,8],'d01'], [360,360,[5,6,7],[4,8,9],'d01'],
    [361,361,[6,7],[5,8,9],'d01'],
    [362,362,[],[10,11,12,13],'d02'], [363,363,[10,11,12,13,14,15],[9,16,17],'d02'],
    [364,364,[14,15,16],[12,13,17,18],'d02'], [365,365,[19,20,21,22],[18,23,24],'d02'],
    [366,366,[21,22,23,24],[20,25,26],'d02'], [367,367,[24,25],[22,23,26],'d02'],
    [368,368,[],[24,25,26],'d02'],
    [370,370,[28,29,30,31],[27,32,33],'d03'],
    [371,371,[28,29,30,31,32,33,34],[27,35,36],'d03'], [372,372,[32,33,34],[30,31,35,36],'d03'],
    [373,373,[37,38,39,40,41],[36,42,43],'d04'], [374,374,[39,40,41,42],[38,43,44],'d04'],
    [375,375,[41,42,43],[40,44,45],'d04'], [376,376,[42,43],[41,44],'d04'],
    [377,377,[],[42,43],'d04'],
    [379,379,[],[42,43,44],'d05'], [380,380,[42,43,44,45,46],[41,47,48],'d05'],
    [381,381,[44,45,46,47],[43,48],'d05'], [382,382,[47],[46,48,49],'d05'],
    [383,383,[51,52],[50,53,54],'d06'], [384,384,[51,52],[50,53,54],'d06'],
    [385,385,[51,52],[50,53],'d06'], [386,387,[50,51,52],[49,53,54],'d06'],
    [388,388,[51,52],[50,53,54],'d06'], [389,389,[],[51,52,53],'d06'],
    [390,390,[56,57,58,59],[55,60,61],'d07'], [391,391,[57,58,59,60,61],[56,62,63],'d07'],
    [392,392,[60,61,62],[59],'d07'],
    [395,395,[61],[60,62,63],'d08'], [396,396,[60,61,62,63],[59,64,65],'d08'],
    [397,397,[61,62,63,64,65],[60,66,67],'d08'], [398,398,[63,64,65,66],[62,67,68],'d08'],
    [399,399,[],[65,66,67],'d08'], [399,399,[69,70,71],[68,72],'d09'],
    [400,400,[70,71,72],[69,73,74],'d09'], [401,402,[71,72,73],[70,74],'d09'],
    [403,403,[71,72],[70,73,74],'d09'], [404,404,[71],[70,72,73],'d09'],
    [405,405,[],[71,72],'d09'],
    [406,406,[74,75,76,77],[73,78,79],'d10'], [407,407,[75,76,77,78,79],[74,80],'d10'],
    [408,408,[78,79,80],[77,81,82],'d10'], [409,409,[],[79,80],'d10'],
    [409,409,[],[82,83],'d11'], [410,412,[82,83],[81,84],'d11'],
    [413,413,[82,83],[81,84,85],'d11'], [414,414,[82,83,84,85],[81,86],'d11'],
    [415,415,[84,85],[83,86],'d11'], [416,416,[],[84,85],'d11'],
]
UNASSIGNED = [
    [362,362,[],[6,7],'u362'], [369,369,[],[28,29,30,31],'u369'],
    [378,378,[],[42,43,44],'u378'], [389,389,[],[55,56,57],'u389'],
    [393,393,[],[60,61],'u393'], [405,405,[],[74,75],'u405'],
]


def pin(path):
    b = path.read_bytes()
    return {'sha256':hashlib.sha256(b).hexdigest(), 'bytes':len(b)}


def expand(runs, x):
    fs = [{'fragment_id':r[4], 'core':r[2], 'fringe':r[3]}
          for r in runs if r[0] <= x <= r[1]]
    seen = set()
    for f in fs:
        if f['core'] != sorted(set(f['core'])) or f['fringe'] != sorted(set(f['fringe'])):
            raise ValueError('Class order')
        if set(f['core']) & set(f['fringe']): raise ValueError('Class overlap')
        selected = set(f['core'] + f['fringe'])
        if selected & seen: raise ValueError('Duplicate fragment cell')
        seen |= selected
    c = sorted({y for f in fs for y in f['core']})
    f = sorted({y for a in fs for y in a['fringe']})
    return c, f, fs


def record(x, runs, band=False, refs=None):
    c, f, fs = expand(runs, x)
    selected = c+f
    flags = []
    if selected:
        if x == 330: flags.append('target_left')
        if x == 424: flags.append('target_right')
        if 0 in selected: flags.append('target_top')
        if 87 in selected: flags.append('target_bottom')
    status = ('identity_conflict' if band else 'boundary_truncated' if flags else
              'identified_local_fragment' if c else 'fringe_only') if selected else 'no_attributable_cells'
    return {'x':x, 'core':c, 'fringe':f, 'fragments':fs,
            'fragment_id':fs[0]['fragment_id'] if len(fs)==1 else None,
            'status':status, 'boundary_flags':flags, 'band_refs':refs or [],
            'note':'Manual local ink attribution only. Fringe and interbody material may be compression artifacts; nonselection is not exclusion of original curve. No bridging or seam join.'}


def controls():
    runs = [[0,0,[2],[1],'a'],[0,1,[5],[6],'b']]
    c,f,fs = expand(runs,0)
    assert c == [2,5] and f == [1,6] and len(fs) == 2
    assert expand(runs,2) == ([],[],[])
    try: expand([[0,0,[2],[1],'a'],[0,0,[],[2],'b']],0)
    except ValueError: pass
    else: raise AssertionError('Duplicate accepted')
    r = record(330,[[330,330,[],[0],'edge']])
    assert r['boundary_flags'] == ['target_left','target_top'] and r['status']=='boundary_truncated'
    assert record(331,[])['status']=='no_attributable_cells'
    print('PASS: five literal expansion controls; no historical data used')


def build():
    before = {k:pin(HERE/k) for k in EXPECTED}
    if any(before[k]['sha256'] != v for k,v in EXPECTED.items()): raise ValueError('Changed dependency')
    routes = {'solid':[], 'dash':[]}
    bands = []
    for x in range(330,425):
        b = record(x,UNASSIGNED,True)
        bands.append(b)
        refs = [a['fragment_id'] for a in b['fragments']]
        for route,runs in [('solid',SOLID),('dash',DASH)]:
            routes[route].append(record(x,runs,refs=refs if route=='dash' else []))
    pixels = {(r['x'],r['y']):r['rgb'] for r in json.loads((HERE/'context01.json').read_text())['cells']['F4-Im4']}
    for x, s, d, b in zip(range(330,425),routes['solid'],routes['dash'],bands):
        seen = set()
        for r in [s,d,b]:
            for y in r['core']+r['fringe']:
                if type(y) is not int or not 0 <= y < 88: raise ValueError(('Bounds',x,y))
                if pixels[x,y] == [255,255,255]: raise ValueError(('Selected exact white',x,y))
                if y in seen: raise ValueError(('Duplicate attribution',x,y))
                seen.add(y)
    if before != {k:pin(HERE/k) for k in EXPECTED}: raise ValueError('Changed dependency')
    return {'pair':'F4', 'region_id':'F4-Im4', 'source_image':'Im4.jpg', 'reader':'primary',
            'reader_actor':'root', 'status':'frozen_manual_native_annotation_not_accepted_measurement',
            'target_box':[330,0,425,88], 'context_box':[328,0,427,88],
            'inputs':before, 'script_pin':pin(Path(__file__)),
            'literal_instructions':{'solid':SOLID,'dash':DASH,'unassigned':UNASSIGNED},
            'coverage':{'native_strip_viewed':True,'complete_composed_page_viewed':True,
                'view_receipt':'Root view_image calls after context save 1d819a: full unchanged Im4 and page-076',
                'page_display_limit':'1700x2200 page displayed1376x1780; native coordinates from raw RGB only',
                'context_blocks_inclusive':[[328,347],[348,367],[368,387],[388,407],[408,426]],
                'raw_read_receipts':['06b4a5','92eb49','2a6dd0','6b7f3d','efa00d'],
                'context_rows_inclusive':[0,87],'context_cells':8712,
                'all_target_columns_read':True,'model_route_records':190,'unassigned_band_records':95},
            'identity_basis':'Gold four-bolt local continuous and broken styles in complete strip and confirmed composed-page legend. No height-only identity. Dash bodies are separate local IDs, not inferred gap support.',
            'independence':'Prior-informed primary AI reader. No peer annotation content or substantive interpretation read before this freeze.',
            'limits':'Native ink only; faint edges are assessed not calibrated. No original-curve containment, physical ordinate, common support, seam join, model discrepancy or causal finding.',
            'human_accepted':False,'physical_support':None,'routes':routes,'unassigned_bands':bands}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--controls',action='store_true')
    p.add_argument('--output')
    args = p.parse_args()
    if args.controls: controls()
    else:
        if args.output not in ['reader-F4-Im4-primary.json','reader-F4-Im4-primary-repeat.json']:
            raise ValueError('Output name')
        result = build()
        out = HERE/args.output
        with out.open('x') as f:
            json.dump(result,f,indent=2,sort_keys=True,allow_nan=False)
            f.write('\n')
        print(json.dumps({'output':args.output,'pin':pin(out),'route_records':190,'band_records':95}))

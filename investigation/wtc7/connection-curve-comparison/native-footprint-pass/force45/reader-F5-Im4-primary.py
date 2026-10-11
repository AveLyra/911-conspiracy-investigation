"""Literal primary F5-Im4 ink reading; expansion never selects from RGB."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'PROTOCOL.md': '4df4510ba5664888124512ab052cfe535fce23dba482e5021cc69d4d0c47f285',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../../native-strips01/Im4.jpg': '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'read_context.py': 'cfce638b10df652fd8a8273603e9dee12c71952f567d4c1f534d6cd12e2b05ab',
    'context01.json': '161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
    'context02.json': '161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
}
SOLID = [
    [377,377,[],[0],'s01'],
    [378,378,[0],[1,2],'s01'],
    [379,379,[0,1,2],[3],'s01'],
    [380,380,[2,3,4],[1,5],'s01'],
    [381,381,[3,4,5,6],[2,7],'s01'],
    [382,382,[5,6,7],[4,8,9],'s01'],
    [383,383,[7,8,9],[6,10],'s01'],
    [384,384,[9,10],[8,11],'s01'],
    [385,385,[10,11,12],[9,13],'s01'],
    [386,386,[12,13,14],[11,15],'s01'],
    [387,387,[14,15,16],[13,17],'s01'],
    [388,388,[15,16,17],[14,18,19],'s01'],
    [389,389,[17,18,19],[16,20,21],'s01'],
    [390,390,[19,20,21],[18,22],'s01'],
    [391,391,[21,22],[20,23],'s01'],
    [392,392,[22,23,24],[21,25],'s01'],
    [393,393,[24,25],[23,26],'s01'],
    [394,394,[25,26,27],[24,28],'s01'],
    [395,395,[27,28],[26,29],'s01'],
    [396,396,[28,29],[27,30],'s01'],
    [397,397,[29,30,31],[28,32],'s01'],
    [398,398,[31,32],[30,33],'s01'],
    [399,399,[32,33,34],[31,35],'s01'],
    [400,400,[33,34,35],[32,36],'s01'],
    [401,401,[35,36],[34,37],'s01'],
    [402,402,[36,37],[35,38],'s01'],
    [403,403,[37,38,39],[36,40],'s01'],
    [404,404,[38,39,40,41],[37,42],'s01'],
    [405,405,[40,41,42],[39,43],'s01'],
    [406,406,[41,42,43],[40,44],'s01'],
    [407,407,[43,44],[42,45,46],'s01'],
    [408,408,[44,45,46],[43,47],'s01'],
    [409,409,[46,47],[45,48,49],'s01'],
    [410,410,[47,48],[46,49],'s01'],
    [411,411,[48,49,50],[47,51],'s01'],
    [412,412,[50,51,52],[49,53],'s01'],
    [413,413,[51,52,53],[54],'s01'],
    [414,414,[53,54],[52,55,56],'s01'],
    [415,415,[54,55,56],[53,57],'s01'],
    [416,416,[56,57],[55,58],'s01'],
    [417,417,[57,58],[56,59],'s01'],
    [418,418,[58,59],[57,60],'s01'],
    [419,419,[59,60,61],[58,62],'s01'],
    [420,420,[60,61,62],[59,63],'s01'],
    [421,421,[61,62],[60,63],'s01'],
    [422,422,[62,63,64],[61,65],'s01'],
    [423,423,[63,64,65],[62,66],'s01'],
    [424,424,[65,66],[64,67],'s01'],
    [425,425,[65,66,67],[64,68],'s01'],
    [426,426,[66,67,68],[65,69],'s01'],
    [427,427,[68,69],[67,70],'s01'],
    [428,428,[69,70],[68,71],'s01'],
    [429,429,[70,71],[69,72],'s01'],
    [430,430,[71,72],[70,73],'s01'],
    [431,431,[72,73],[71,74],'s01'],
    [432,432,[73,74],[72,75],'s01'],
    [433,433,[73,74,75],[72,76],'s01'],
    [434,434,[74,75,76,77],[73,78],'s01'],
    [435,435,[76,77,78],[75,79],'s01'],
    [436,436,[77,78],[76,79],'s01'],
    [437,437,[78,79,80],[77,81],'s01'],
    [438,438,[79,80,81],[78,82],'s01'],
    [439,439,[81],[80,82],'s01'],
    [440,440,[81,82,83],[80,84],'s01'],
    [441,441,[82,83,84],[81,85],'s01'],
    [442,442,[84,85],[83,86],'s01'],
    [443,443,[85,86],[84,87],'s01'],
    [444,444,[86,87],[85],'s01'],
    [445,445,[87],[86],'s01'],
    [446,446,[],[87],'s01'],
]
DASH = [
    [415,415,[],[0],'d01'],
    [416,416,[0,1],[2],'d01'],
    [417,417,[1,2,3],[0,4],'d01'],
    [418,418,[],[3,4],'d01'],
    [420,420,[],[8,9],'d02'],
    [421,422,[8,9],[7,10],'d02'],
    [423,423,[8,9],[7,10],'d02'],
    [424,424,[9,10],[8,11],'d02'],
    [425,425,[],[9,10,11],'d02'],
    [426,426,[14,15],[13,16],'d03'],
    [427,427,[15,16,17],[14,18],'d03'],
    [428,428,[17,18],[16,19],'d03'],
    [429,429,[18,19],[17,20],'d03'],
    [430,430,[],[19,20],'d03'],
    [432,432,[],[21,22],'d04'],
    [433,433,[21,22,23],[20,24,25],'d04'],
    [434,434,[23,24,25,26],[22,27],'d04'],
    [435,435,[25,26,27],[24,28],'d04'],
    [436,436,[],[26,27],'d04'],
    [436,436,[],[30,31],'d05'],
    [437,437,[30,31,32],[29,33],'d05'],
    [438,438,[32,33],[31,34],'d05'],
    [439,439,[33,34],[32,35],'d05'],
    [440,440,[34],[33,35],'d05'],
    [441,441,[],[34,35],'d05'],
    [443,443,[38,39,40],[37,41],'d06'],
    [444,444,[39,40,41],[38,42,43],'d06'],
    [445,445,[],[41,42,43],'d06'],
    [456,456,[65,66],[64,67],'d07'],
    [457,457,[66,67],[65,68],'d07'],
    [458,458,[67,68],[66,69],'d07'],
    [459,459,[68,69],[67,70],'d07'],
    [460,460,[69,70],[68,71],'d07'],
    [461,461,[],[70],'d07'],
    [461,461,[],[73,74,75,76],'d08'],
    [462,462,[74,75,76,77,78],[73,79,80],'d08'],
    [463,463,[76,77,78,79],[75,80],'d08'],
    [464,464,[],[79],'d08'],
    [464,464,[],[82,83,84],'d09'],
    [465,465,[83,84],[82,85],'d09'],
    [466,466,[84,85],[83,86],'d09'],
    [467,467,[85,86],[84,87],'d09'],
    [468,468,[86,87],[85],'d09'],
    [469,469,[87],[86],'d09'],
]
UNASSIGNED = [
    [419,419,[],[4],'u419'],
    [431,431,[],[21],'u431'],
    [442,442,[],[34,35,38],'u442'],
    [446,446,[],[47,48,49],'u446'],
    [447,447,[],[47,48,49,50],'u447'],
    [448,448,[],[48,49,50,51],'u448'],
    [449,449,[],[49,50,51,52,53],'u449'],
    [450,450,[],[50,51,52,53,54],'u450'],
    [451,451,[],[51,52,53,54,55],'u451'],
    [452,452,[],[54,55,56,57,58],'u452'],
    [453,453,[],[55,56,57,58,59,60,61],'u453'],
    [454,454,[],[57,58,59,60,61,62],'u454'],
    [455,455,[],[58,59,60,61,62],'u455'],
]


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def pieces(runs, x):
    return [{'fragment_id': r[4], 'core': r[2], 'fringe': r[3]}
            for r in runs if r[0] <= x <= r[1]]


def record(x, fragments, refs, band=False):
    core = sorted(y for p in fragments for y in p['core'])
    fringe = sorted(y for p in fragments for y in p['fringe'])
    if len(core) != len(set(core)) or len(fringe) != len(set(fringe)) or set(core) & set(fringe):
        raise ValueError('Duplicate literal membership')
    selected = core + fringe
    flags = []
    if selected:
        if x == 375: flags.append('target_left')
        if x == 474: flags.append('target_right')
        if 0 in selected: flags.append('target_top')
        if 87 in selected: flags.append('target_bottom')
    if band:
        status = 'identity_conflict' if selected else 'no_attributable_cells'
        note = 'Pale between-body material or blue/red mixed-color overlap retained once without a model identity. Empty is not proof of absent ink.'
    else:
        status = ('boundary_truncated' if flags else 'identified_local_fragment' if core else 'fringe_only') if selected else ('identity_conflict' if refs else 'no_attributable_cells')
        note = 'Manual local blue continuous/broken-style reading from complete source and raw RGB. Separate pieces retain local IDs. Core/fringe is subjective, not calibrated containment; empty means no attributed cells, not zero support.'
    return {'x': x, 'core': core, 'fringe': fringe,
            'fragment_id': fragments[0]['fragment_id'] if len(fragments) == 1 else None,
            'fragments': fragments, 'status': status, 'boundary_flags': flags,
            'band_refs': refs, 'note': note}


def build():
    before = {k: pin(HERE/k) for k in EXPECTED}
    if any(before[k]['sha256'] != v for k, v in EXPECTED.items()):
        raise ValueError('Changed dependency')
    routes = {'solid': [], 'dash': []}
    bands = []
    for x in range(375,475):
        unassigned = pieces(UNASSIGNED,x)
        bands.append(record(x,unassigned,[],True))
        routes['solid'].append(record(x,pieces(SOLID,x),[]))
        routes['dash'].append(record(x,pieces(DASH,x),[p['fragment_id'] for p in unassigned]))
    pixels = {(r['x'],r['y']): r['rgb'] for r in json.loads((HERE/'context01.json').read_text())['cells']['F5-Im4']}
    for group in [*routes.values(),bands]:
        if [r['x'] for r in group] != list(range(375,475)): raise ValueError('Coverage')
        for r in group:
            for key in ('core','fringe'):
                if r[key] != sorted(set(r[key])): raise ValueError('Row order')
                for y in r[key]:
                    if type(y) is not int or not 0 <= y < 88: raise ValueError('Bounds')
                    if pixels[r['x'],y] == [255,255,255]: raise ValueError(('Selected exact white',r['x'],y))
    for s,d,u in zip(routes['solid'],routes['dash'],bands):
        sets = [set(r['core']+r['fringe']) for r in (s,d,u)]
        if any(sets[i]&sets[j] for i,j in [(0,1),(0,2),(1,2)]): raise ValueError('Duplicate attribution')
    if before != {k: pin(HERE/k) for k in EXPECTED}: raise ValueError('Changed dependency')
    return {
        'pair':'F5','region_id':'F5-Im4','source_image':'Im4.jpg','reader':'primary',
        'reader_agent':'force5_primary','status':'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box':[375,0,475,88],'context_box':[373,0,477,88],
        'inputs':before,'script_pin':pin(Path(__file__)),
        'literal_instructions':{'solid':SOLID,'dash':DASH,'unassigned':UNASSIGNED},
        'coverage':{'native_strip_viewed':True,'complete_composed_page_viewed':True,
            'view_receipt':'view_image calls preceding raw receipt 7b655f: unchanged full Im4, Im2 and page076',
            'page_display_limit':'1700x2200 page displayed1376x1780; no coordinates taken from resized page',
            'context_blocks_inclusive':[[373,392],[393,412],[413,432],[433,452],[453,476]],
            'raw_read_receipts':['7b655f','ec3e20','0e8456','a42681','774ff3'],
            'context_rows_inclusive':[0,87],'context_cells':9152,
            'all_target_columns_read':True,'model_route_records':200,'unassigned_band_records':100},
        'identity_basis':'Confirmed blue five-bolt legend, solid Spring and broken Shell. Full-strip style identifies local continuous descending branch and distinct broken bodies. Mixed red/blue crossing is left unresolved rather than assigning by vertical order.',
        'independence':'Prior-informed primary AI reader prospectively designated before new pixels; no force45 peer or root-F4 annotations read before freezing both F5 regions. Older E9-root implementation was inspected solely for representation design.',
        'limits':'Native ink only; no RGB threshold selection, interpolation, original-curve bound, physical ordinate, support, seam join, historical inference or human acceptance. Region-local IDs do not connect to Im2 IDs.',
        'human_accepted':False,'physical_support':None,'routes':routes,'unassigned_bands':bands}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output',required=True); args = p.parse_args()
    if args.output not in ['reader-F5-Im4-primary.json','reader-F5-Im4-primary-repeat.json']: raise ValueError('Output name')
    out = HERE/args.output
    result = build()
    with out.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    print(json.dumps({'output':str(out),'pin':pin(out),'route_records':200,'band_records':100}))

"""Literal primary E8 ink reading, with no RGB-based cell selection."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'PROTOCOL.md':'98edc562841efdbc3ffb7f25c813b507cf553142a972f5558680e7218f7e6e25',
    '../PROTOCOL.md':'2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json':'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../../native-strips01/Im7.jpg':'3509c0fb002d47d1cc9d1ae624377534c8b31bd9fea7fdadd380a7b5f4d4a09d',
    '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'read_context.py':'377d4f41b990502ca87fc7d1b4b9b069eede0aa71f281c68cb5ae879d7196a2c',
    'context01.json':'0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
    'context02.json':'0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
}
# Inclusive x endpoints and explicitly read row sets; expansion is mechanical.
SOLID = [
    [540,542,[76,77],[75,78],'s01'],
    [543,548,[76],[75,77,78],'s01'],
    [549,551,[75,76],[74,77],'s01'],
    [552,557,[75],[74,76],'s01'],
    [558,563,[74,75],[73,76],'s01'],
    [564,575,[74],[73,75,76],'s01'],
    [576,593,[73,74],[72,75],'s01'],
    [594,617,[73],[72,74,75],'s01'],
    [618,637,[73,74],[72,75],'s01'],
    [638,689,[73],[72,74,75],'s01'],
]
DASH = [
    [540,541,[72],[71,73],'d01'],
    [542,542,[71,72],[70,73],'d01'],
    [543,543,[71],[70,72],'d01'],
    [544,545,[70,71],[69,72],'d01'],
    [546,546,[70],[69,71],'d01'],
    [547,547,[],[69,70,71],'d01'],
    [549,550,[68,69],[67,70],'d02'],
    [551,551,[68],[67,69],'d02'],
    [552,553,[67,68],[66,69],'d02'],
    [554,555,[67],[66,68],'d02'],
    [556,556,[],[66,67,68],'d02'],
    [558,558,[],[65,66,67],'d03'],
    [559,559,[66],[65,67],'d03'],
    [560,561,[65],[64,66],'d03'],
    [562,564,[64,65],[63,66],'d03'],
    [565,565,[],[64,65,66],'d03'],
    [568,570,[63,64],[62,65],'d04'],
    [571,574,[63],[62,64],'d04'],
    [575,575,[],[62,63,64],'d04'],
    [577,583,[62],[61,63,64],'d05'],
    [595,595,[],[61,62,63],'d07'],
    [587,593,[62],[61,63,64],'d06'],
    [596,602,[62],[61,63,64],'d07'],
    [605,611,[62],[61,63,64],'d08'],
    [615,621,[62],[61,63,64],'d09'],
    [624,630,[62],[61,63,64],'d10'],
    [633,639,[62],[61,63,64],'d11'],
    [642,648,[62],[61,63,64],'d12'],
    [652,658,[62],[61,63,64],'d13'],
    [661,667,[62],[61,63,64],'d14'],
    [670,676,[62],[61,63,64],'d15'],
    [680,685,[62],[61,63,64],'d16'],
    [686,686,[],[61,62,63],'d16'],
    [688,689,[62],[61,63,64],'d17'],
]
UNASSIGNED = [
    [535,535,[74,75,77],[73,76,78],'u-close01'],
    [536,536,[74,77],[73,75,76,78],'u-close01'],
    [537,539,[76,77],[73,74,75,78],'u-close01'],
    [548,548,[],[69,70,71],'u548'],
    [557,557,[],[66,67],'u557'],
    [566,567,[],[64,65],'u566'],
    [576,576,[],[62,63],'u576'],
    [584,586,[],[62,63],'u584'],
    [594,594,[],[62,63],'u594'],
    [603,604,[],[62,63],'u603'],
    [612,614,[],[62,63],'u612'],
    [622,623,[],[62,63],'u622'],
    [631,632,[],[62,63],'u631'],
    [640,641,[],[62,63],'u640'],
    [649,651,[],[62,63],'u649'],
    [659,660,[],[62,63],'u659'],
    [668,669,[],[62,63],'u668'],
    [677,679,[],[62,63],'u677'],
    [687,687,[],[62,63],'u687'],
]


def pin(path):
    b=path.read_bytes()
    return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}


def select_literal(runs,x):
    matches=[r for r in runs if r[0]<=x<=r[1]]
    if len(matches)>1:raise ValueError('Overlapping literal runs')
    return matches[0][2:] if matches else [[],[],None]


def entry(x,c,f,identity,status,note,refs=None):
    selected=c+f
    flags=[]
    if selected:
        if x==535:flags.append('target_left')
        if x==689:flags.append('target_right')
        if 54 in selected:flags.append('target_top')
        if 85 in selected:flags.append('target_bottom')
    return {'x':x,'core':c,'fringe':f,'fragment_id':identity,'status':status,
            'boundary_flags':flags,'band_refs':refs or [],'note':note}


def build():
    before={k:pin(HERE/k) for k in EXPECTED}
    if any(before[k]['sha256']!=v for k,v in EXPECTED.items()):raise ValueError('Changed input')
    routes={'solid':[],'dash':[]};bands=[]
    for x in range(535,690):
        c,f,bid=select_literal(UNASSIGNED,x)
        bands.append(entry(x,c,f,bid,'identity_conflict' if bid else 'no_attributable_cells',
            'Close traces or pale interbody material recorded once. Tentative fringe may include raster artifacts; neither nonselection nor an empty band proves absence.'))
        for route,runs in [('solid',SOLID),('dash',DASH)]:
            c,f,fid=select_literal(runs,x)
            status=('boundary_truncated' if x==689 else 'identified_local_fragment' if c else 'fringe_only') if fid else 'identity_conflict'
            routes[route].append(entry(x,c,f,fid,status,
                'Manual visible-ink/style reading. Separate local dash bodies are not bridged. Left close-trace zone and unassigned pale material do not establish hidden model identity or zero support.',
                [bid] if not fid and bid else []))
    pixels={(r['x'],r['y']):r['rgb'] for r in json.loads((HERE/'context01.json').read_text())['cells']['E8']}
    for group in [*routes.values(),bands]:
        if [r['x'] for r in group]!=list(range(535,690)):raise ValueError('Coverage')
        for r in group:
            if set(r['core'])&set(r['fringe']):raise ValueError('Class overlap')
            for key in ('core','fringe'):
                if r[key]!=sorted(set(r[key])):raise ValueError('Row order')
                for y in r[key]:
                    if not 54<=y<86 or pixels[r['x'],y]==[255,255,255]:raise ValueError(('Invalid selected cell',r['x'],y))
    for s,d,u in zip(routes['solid'],routes['dash'],bands):
        sets=[set(r['core']+r['fringe']) for r in (s,d,u)]
        if any(sets[i]&sets[j] for i,j in [(0,1),(0,2),(1,2)]):raise ValueError('Duplicate attribution')
    if before!={k:pin(HERE/k) for k in EXPECTED}:raise ValueError('Changed input')
    return {'pair':'E8','reader':'root','status':'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box':[535,54,690,86],'context_box':[533,52,692,88],
        'inputs':before,'script_pin':pin(Path(__file__)),
        'literal_instructions':{'solid':SOLID,'dash':DASH,'unassigned':UNASSIGNED},
        'coverage':{'native_strip_viewed':True,'complete_composed_page_viewed':True,
            'view_receipt':'view_image calls after f5c510; unchanged native Im7 and page-076',
            'page_display_limit':'Page1700x2200 displayed1376x1780; coordinates from raw RGB, not resized page.',
            'context_blocks_inclusive':[[533,572],[573,612],[613,652],[653,691]],
            'raw_read_receipts':['651f20','9660fd','d52443','96eb21'],
            'context_rows_inclusive':[52,87],'context_cells':5724,'all_target_columns_read':True,
            'model_route_records':310,'unassigned_band_records':155},
        'identity_basis':'Cyan/eight bolts, confirmed solid Spring and dashed Shell legend. Full strip and repeated breaks support route identity where assigned; no vertical-order-only assignment. Close left zone retained unassigned.',
        'independence':'Prior-informed primary AI reader. Peer E8 freeze hashes received, but no peer annotation content or substantive reading inspected before this freeze.',
        'limits':'Native selected ink only; no threshold, fitted periodicity, interpolation, automatic seam join, calibrated containment, physical ordinate/support, causal or historical model inference.',
        'human_accepted':False,'physical_support':None,'routes':routes,'unassigned_bands':bands}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    if args.output not in ['reader-E8-root.json','reader-E8-root-repeat.json']:raise ValueError('Output name')
    result=build();out=HERE/args.output
    with out.open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'output':str(out),'pin':pin(out),'route_records':310,'band_records':155}))

"""Literal primary E9 ink reading; RGB used only for transcription checks."""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
EXPECTED={
    'PROTOCOL.md':'98edc562841efdbc3ffb7f25c813b507cf553142a972f5558680e7218f7e6e25',
    '../PROTOCOL.md':'2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json':'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../../native-strips01/Im7.jpg':'3509c0fb002d47d1cc9d1ae624377534c8b31bd9fea7fdadd380a7b5f4d4a09d',
    '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'read_context.py':'377d4f41b990502ca87fc7d1b4b9b069eede0aa71f281c68cb5ae879d7196a2c',
    'context01.json':'0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
    'context02.json':'0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
}
SOLID=[
    [530,530,[49],[48,50],'s01'],
    [531,533,[48,49],[47,50],'s01'],
    [534,536,[48],[47,49],'s01'],
    [537,538,[47,48],[46,49],'s01'],
    [539,541,[47],[46,48],'s01'],
    [542,543,[46,47],[45,48],'s01'],
    [544,547,[46],[45,47],'s01'],
    [548,549,[45,46],[44,47],'s01'],
    [550,553,[45],[44,46],'s01'],
    [554,557,[44,45],[43,46],'s01'],
    [558,563,[44],[43,45],'s01'],
    [564,567,[43,44],[42,45],'s01'],
    [568,575,[43],[42,44],'s01'],
    [576,579,[42,43],[41,44],'s01'],
    [580,589,[42],[41,43],'s01'],
    [590,607,[41,42],[40,43],'s01'],
    [608,689,[41],[40,42],'s01'],
]
DASH=[
    [530,532,[52],[51,53,54],'d01'],
    [535,535,[51],[50,52],'d02'],
    [536,538,[50,51],[52],'d02'],
    [539,541,[50],[49,51],'d02'],
    [544,544,[],[49,50],'d03'],
    [545,546,[49],[48,50],'d03'],
    [547,549,[48,49],[50],'d03'],
    [550,550,[48],[47,49],'d03'],
    [554,554,[48],[47,49],'d04'],
    [555,557,[47,48],[49],'d04'],
    [558,560,[47],[46,48],'d04'],
    [563,569,[47],[46,48],'d05'],
    [572,572,[],[46,47,48],'d06'],
    [573,578,[47],[46,48],'d06'],
    [579,579,[],[47,48],'d06'],
    [581,581,[],[46,47,48],'d07'],
    [582,588,[47],[46,48],'d07'],
    [591,597,[47],[46,48],'d08'],
    [600,606,[47],[46,48],'d09'],
    [609,609,[],[46,47,48],'d10'],
    [610,615,[47],[46,48],'d10'],
    [616,616,[],[46,47,48],'d10'],
    [619,625,[47],[46,48],'d11'],
    [628,634,[47],[46,48],'d12'],
    [637,643,[47],[46,48],'d13'],
    [647,653,[47],[46,48],'d14'],
    [656,662,[47],[46,48],'d15'],
    [665,671,[47],[46,48],'d16'],
    [674,674,[],[46,47,48],'d17'],
    [675,680,[47],[46,48],'d17'],
    [681,681,[],[46,47,48],'d17'],
    [684,689,[47],[46,48],'d18'],
]
UNASSIGNED=[
    [533,534,[],[52,53],'u533'],
    [542,543,[],[50,51],'u542'],
    [551,553,[],[48,49],'u551'],
    [561,562,[],[47,48],'u561'],
    [570,571,[],[47,48],'u570'],
    [580,580,[],[47,48],'u580'],
    [589,590,[],[47,48],'u589'],
    [598,599,[],[47,48],'u598'],
    [607,608,[],[47,48],'u607'],
    [617,618,[],[47,48],'u617'],
    [626,627,[],[47,48],'u626'],
    [635,636,[],[47,48],'u635'],
    [644,646,[],[47,48],'u644'],
    [654,655,[],[47,48],'u654'],
    [663,664,[],[47,48],'u663'],
    [672,673,[],[47,48],'u672'],
    [682,683,[],[47,48],'u682'],
]


def pin(path):
    b=path.read_bytes();return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}


def select_literal(runs,x):
    matches=[r for r in runs if r[0]<=x<=r[1]]
    if len(matches)>1:raise ValueError('Overlapping literal runs')
    return matches[0][2:] if matches else [[],[],None]


def entry(x,c,f,identity,status,note,refs=None):
    selected=c+f;flags=[]
    if selected:
        if x==530:flags.append('target_left')
        if x==689:flags.append('target_right')
        if 30 in selected:flags.append('target_top')
        if 55 in selected:flags.append('target_bottom')
    return {'x':x,'core':c,'fringe':f,'fragment_id':identity,'status':status,
            'boundary_flags':flags,'band_refs':refs or [],'note':note}


def build():
    before={k:pin(HERE/k) for k in EXPECTED}
    if any(before[k]['sha256']!=v for k,v in EXPECTED.items()):raise ValueError('Changed input')
    routes={'solid':[],'dash':[]};bands=[]
    for x in range(530,690):
        c,f,bid=select_literal(UNASSIGNED,x)
        bands.append(entry(x,c,f,bid,'identity_conflict' if bid else 'no_attributable_cells',
            'Pale interbody material retained without model identity; may include raster artifacts. Empty or unselected does not prove original-curve absence.'))
        for route,runs in [('solid',SOLID),('dash',DASH)]:
            c,f,fid=select_literal(runs,x)
            status=('boundary_truncated' if x in (530,689) else 'identified_local_fragment' if c else 'fringe_only') if fid else 'identity_conflict'
            routes[route].append(entry(x,c,f,fid,status,
                'Full-strip continuous/broken style, not vertical order alone, informs manual assignment. Each dash body stays separate. Core/fringe distinctions are subjective and not calibrated containment bounds.',
                [bid] if not fid and bid else []))
    pixels={(r['x'],r['y']):r['rgb'] for r in json.loads((HERE/'context01.json').read_text())['cells']['E9']}
    for group in [*routes.values(),bands]:
        if [r['x'] for r in group]!=list(range(530,690)):raise ValueError('Coverage')
        for r in group:
            if set(r['core'])&set(r['fringe']):raise ValueError('Class overlap')
            for key in ('core','fringe'):
                if r[key]!=sorted(set(r[key])):raise ValueError('Row order')
                for y in r[key]:
                    if not 30<=y<56 or pixels[r['x'],y]==[255,255,255]:raise ValueError(('Invalid selected cell',r['x'],y))
    for s,d,u in zip(routes['solid'],routes['dash'],bands):
        sets=[set(r['core']+r['fringe']) for r in (s,d,u)]
        if any(sets[i]&sets[j] for i,j in [(0,1),(0,2),(1,2)]):raise ValueError('Duplicate attribution')
    if before!={k:pin(HERE/k) for k in EXPECTED}:raise ValueError('Changed input')
    return {'pair':'E9','reader':'root','status':'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box':[530,30,690,56],'context_box':[528,28,692,58],
        'inputs':before,'script_pin':pin(Path(__file__)),
        'literal_instructions':{'solid':SOLID,'dash':DASH,'unassigned':UNASSIGNED},
        'coverage':{'native_strip_viewed':True,'complete_composed_page_viewed':True,
            'view_receipt':'view_image calls after f5c510; unchanged native Im7 and page-076',
            'page_display_limit':'Page1700x2200 displayed1376x1780; coordinates from raw RGB, not resized page.',
            'context_blocks_inclusive':[[528,568],[569,609],[610,650],[651,691]],
            'raw_read_receipts':['b48a1c','c01b8d','f12cee','3f1e4f'],
            'context_rows_inclusive':[28,57],'context_cells':4920,'all_target_columns_read':True,
            'model_route_records':320,'unassigned_band_records':160},
        'identity_basis':'Purple/nine bolts; confirmed legend solid Spring, dashed Shell. The full strip supports a continuous upper trace and locally broken lower trace; model identity is not inferred solely from height.',
        'independence':'Prior-informed primary AI reading. No current peer E9 annotation content or substantive reading inspected before freeze; peer E8 discussion is disclosed and concerns another pair.',
        'limits':'Native selected ink only; no color threshold, fitted periodicity, interpolation, seam join, calibrated containment, physical ordinate/support, causal or historical model inference.',
        'human_accepted':False,'physical_support':None,'routes':routes,'unassigned_bands':bands}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    if args.output not in ['reader-E9-root.json','reader-E9-root-repeat.json']:raise ValueError('Output name')
    result=build();out=HERE/args.output
    with out.open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'output':str(out),'pin':pin(out),'route_records':320,'band_records':160}))

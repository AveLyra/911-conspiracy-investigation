"""Literal root E3 reading; expansion never inspects RGB or selects pixels."""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
EXPECTED={
    'PROTOCOL.md':'be57860a830ab716498ba5d25733021c1c975da1b0427f50f64071af4eaf5f16',
    'IDENTITY-CLARIFICATION.md':'c9d79b6d92a5cbc2f4747e027bce81ee5b1cbec0528b018b368f22fd2b01098b',
    '../PROTOCOL.md':'2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json':'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../../native-strips01/Im10.jpg':'fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3',
    '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'context01.json':'59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
    'context02.json':'59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
}
# Inclusive manual runs, not a pixel-value predicate or fitted periodic rule.
DASH_RUNS=[
    [489,494],[498,503],[508,513],[517,522],[526,531],[535,541],
    [545,550],[554,559],[563,569],[573,578],[582,587],[591,596],
    [600,606],[610,615],[619,624],[628,633],[638,643],[647,652],
    [656,661],[665,671],[675,680],[684,689],
]
# In these interbody columns row43 is exactly white; no candidate selected.
EMPTY_INTERBODY=[496,533,543,552,589,599,626,672,682]
EARLY_FRINGE={365:[45,46],366:[45],367:[],368:[45,46],369:[45,46],
              370:[45,46],371:[45,46],372:[45],373:[45],374:[45]}


def pin(path):
    b=path.read_bytes()
    return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}


def flags(x,rows):
    if not rows:return []
    return (['target_left'] if x==365 else [])+(['target_right'] if x==689 else [])+(['target_top'] if 30 in rows else [])+(['target_bottom'] if 59 in rows else [])


def entry(x,core,fringe,status,fragment,note,refs=None):
    return {'x':x,'core':core,'fringe':fringe,'status':status,'fragment_id':fragment,
            'boundary_flags':flags(x,core+fringe),'note':note,'band_refs':refs or []}


def build():
    before={k:pin(HERE/k) for k in EXPECTED}
    if any(before[k]['sha256']!=v for k,v in EXPECTED.items()):raise ValueError('Changed input')
    routes={'solid':[],'dash':[]}; bands=[]
    for x in range(365,690):
        matches=[i for i,(first,last) in enumerate(DASH_RUNS,1) if first<=x<=last]
        if len(matches)>1:raise ValueError('Overlapping literal runs')
        if x<=374:
            core,fringe,local=[43,44],EARLY_FRINGE[x],'u-merged01'
        elif x<=485:
            core,fringe,local=[43],[42,44],'u-merged01'
        elif matches or x in EMPTY_INTERBODY:
            core,fringe,local=[],[],None
        else:
            core,fringe,local=[],[43],f'u-pale-{x}'
        bands.append(entry(x,core,fringe,'identity_conflict' if core or fringe else 'no_attributable_cells',local,
            'Visible merged ink or tentative interbody material; model contribution unresolved. An empty unassigned set does not establish absence of hidden solid ink. Farther pale pixels not selected are not certified outside the original curve.'))
        refs=[local] if local else []
        routes['solid'].append(entry(x,[],[],'identity_conflict',None,
            'No independently separable solid assignment in this target. Hidden overlap, ended solid trace, and unresolved local mixture remain alternatives; no endpoint or zero-support finding.',refs))
        if matches:
            routes['dash'].append(entry(x,[43],[42,44],
                'boundary_truncated' if x==689 else 'identified_local_fragment',f'd{matches[0]:02d}',
                'Local repeated dash body supported by full strip style. Row43 is confident ink; adjacent rows42/44 tentative edges. Does not exclude unresolved solid overprinting; no bridge to another body.'))
        else:
            routes['dash'].append(entry(x,[],[],'identity_conflict' if refs else 'no_attributable_cells',None,
                'No unique dash-body cells assigned at this column; merged material or uncertain body edge stays unassigned. Empty attribution is not a verified dash gap or zero.',refs))
    if before!={k:pin(HERE/k) for k in EXPECTED}:raise ValueError('Input changed')
    return {
        'pair':'E3','reader':'root','status':'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box':[365,30,690,60],'context_box':[363,28,692,62],
        'inputs':before,'script_pin':pin(Path(__file__)),
        'literal_instructions':{'dash_runs_inclusive':DASH_RUNS,'empty_interbody':EMPTY_INTERBODY,
            'early_fringe':EARLY_FRINGE,'early_core':[43,44],
            'merged_later':{'columns_inclusive':[375,485],'core':[43],'fringe':[42,44]},
            'other_nonempty_interbody':{'core':[],'fringe':[43]},
            'dash_core':[43],'dash_fringe':[42,44]},
        'coverage':{'native_strip_viewed':True,'complete_composed_page_viewed':True,
            'page_display_limit':'1700x2200 displayed at1376x1780; source-native coordinates came from raw RGB.',
            'view_receipt':'functions image call immediately before 01deb4',
            'context_blocks_inclusive':[[363,409],[410,479],[480,549],[550,619],[620,691]],
            'raw_read_receipts':['01deb4','e374a0','10aba6','39d340'],
            'context_rows_inclusive':[28,61],'context_cells':11186,
            'all_target_columns_read':True,'model_route_records':650,'unassigned_band_records':325,
            'uncompleted':'E4/E5 annotation and remaining approach outside this locator; not completed by this artifact.'},
        'identity_basis':'Confirmed source legend: black three bolts, solid Spring/dashed Shell. This target starts near contact. Root cannot uniquely partition the initial shared ink. Later recurring separated dark bodies support a local dashed assignment; this does not identify a solid termination or rule out hidden overlap.',
        'independence':'Prior-informed primary AI reading; no current peer E3 annotation inspected before freeze. Same source, not blinded, not human/expert acceptance.',
        'limits':'Native visible-ink assignment only. No threshold, interpolation, pre-raster containment bound, physical ordinate, admitted support, model discrepancy or historical cause inference.',
        'human_accepted':False,'physical_support':None,'routes':routes,'unassigned_bands':bands,
    }


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='reader-E3-root.json');args=p.parse_args()
    result=build();target=HERE/args.output
    with target.open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'output':str(target),'pin':pin(target),'route_records':650,'band_records':325}))

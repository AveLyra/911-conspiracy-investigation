"""Literal independent manual E3 reading; no pixel-dependent selection."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

PINS = {
    'PROTOCOL.md': 'be57860a830ab716498ba5d25733021c1c975da1b0427f50f64071af4eaf5f16',
    'IDENTITY-CLARIFICATION.md': 'c9d79b6d92a5cbc2f4747e027bce81ee5b1cbec0528b018b368f22fd2b01098b',
    'context01.json': '59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
    'context02.json': '59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
    'read_context.py': '67e6788059653ba5d1e3eb18302e46bbc4299149646a8fed1516416dd7d1fe22',
    '../../native-strips01/Im10.jpg': 'fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}

# Inclusive literal column runs selected after full source and raw context review.
# These expand only human-readable manual decisions, not image values.
BAND = [
    (365,365,[44],[43,45,46]), (366,367,[43,44],[]),
    (368,373,[43,44,45],[46]), (374,374,[43,44],[45]),
    (375,375,[43],[44]), (376,376,[43],[42,44]),
    (377,383,[43,44],[42,45]), (384,385,[43],[42,44]),
    (386,393,[43],[42,44]), (394,480,[43],[42,44]),
]
DASH_BODIES = [
    (481,485),(489,494),(498,504),(507,513),(517,522),
    (526,532),(535,541),(545,550),(554,559),(563,569),
    (572,578),(582,587),(591,597),(600,606),(609,615),
    (619,624),(628,634),(637,643),(647,652),(656,662),
    (665,671),(674,680),(684,689),
]
# Faint adjacent endpoint material retained as fringe, not an interpolated gap.
ENDPOINTS = [
    (486,1),(488,2),(495,2),(497,3),(505,3),(506,4),
    (514,4),(516,5),(523,5),(525,6),(534,7),(542,7),
    (544,8),(551,8),(553,9),(560,9),(562,10),(570,10),
    (571,11),(579,11),(581,12),(588,12),(590,13),(598,13),
    (607,14),(608,15),(616,15),(618,16),(625,16),(627,17),
    (635,17),(636,18),(644,18),(646,19),(653,19),(655,20),
    (663,20),(664,21),(673,22),(681,22),(683,23),
]

def flags(x):
    return ['target_left'] if x == 365 else ['target_right'] if x == 689 else []

def record(x, core, fringe, status, note, fragment=None, refs=None):
    return dict(x=x, core=core, fringe=fringe, status=status, note=note,
                fragment_id=fragment, boundary_flags=flags(x) if core or fringe else [],
                unassigned_band_refs=refs or [])

def build():
    bands=[]
    for a,b,core,fringe in BAND:
        for x in range(a,b+1):
            bands.append(dict(band_id='E3-independent-shared-band', x=x,
                core=list(core),fringe=list(fringe),boundary_flags=flags(x),
                competing_identities=['spring ink','shell ink','overprinted spring and shell ink'],
                note='Visible black band; local superposed contributions cannot be partitioned reliably. Core denotes visible ink only.'))
    solid=[]; dash=[]
    for x in range(365,690):
        refs=[{'band_id':'E3-independent-shared-band','x':x}] if x <=480 else []
        solid.append(record(x,[],[],'identity_conflict',
            'No separately resolved spring footprint: unresolved contributions in shared band.' if refs else
            'Dashed ink is visible locally; absent separately visible continuous ink does not establish termination or absence of a hidden spring curve.',refs=refs))
        dash.append(record(x,[],[],'identity_conflict' if refs else 'no_attributable_cells',
            'Shell contribution not partitionable from shared black band.' if refs else
            'No shell cells attributed in this inspected column; pale compression material is not certified to exclude underlying curve.',refs=refs))
    for i,(a,b) in enumerate(DASH_BODIES,1):
        for x in range(a,b+1):
            dash[x-365]=record(x,[43],[42,44],'boundary_truncated' if x==689 else 'identified_local_fragment',
                'Locally distinguishable black dash body, matched to dashed shell legend; this does not recover any hidden spring contribution.',f'E3-independent-dash-{i:02d}')
    for x,i in ENDPOINTS:
        dash[x-365]=record(x,[],[43],'fringe_only',
            'Pale material adjacent to this visually distinguished dash endpoint; attribution uncertain, no gap bridge.',f'E3-independent-dash-{i:02d}')
    for route in (solid,dash):
        assert [r['x'] for r in route] == list(range(365,690))
        for r in route:
            assert not set(r['core']) & set(r['fringe'])
            assert all(30 <= y <60 for y in r['core']+r['fringe'])
            assert not r['unassigned_band_refs'] or not(r['core'] or r['fringe'])
    assert len(bands)==116 and len({b['x'] for b in bands})==116
    return dict(reader='curve_recovery_feasibility; independent prior-informed AI reader',pair='E3',
        pins=PINS,annotation_script_sha256=sha(Path(__file__)),
        frozen_utc=datetime.now(timezone.utc).isoformat(),
        coverage=dict(target_box=[365,30,690,60],context_box=[363,28,692,62],
            context_cells_read=11186,model_route_records=650,full_native_Im10_viewed=True,
            full_composed_page_viewed=True,page_display_resize='1700x2200 to 1376x1780; context only, not pixel coordinate evidence',
            raw_blocks=[{'first':363,'last':412,'receipt':'bb685e'},
                        {'first':413,'last':512,'receipt':'0c29e5'},
                        {'first':513,'last':612,'receipt':'028503'},
                        {'first':613,'last':691,'receipt':'c83c33'}],
            raw_rows_inclusive=[28,61],all_blocks_untruncated=True),
        method='Viewed unchanged native strip and composed page; manually read every raw sparse RGB context column. Exact white alone omitted by frozen display. Literal ranges here transcribe judgments; no source pixel decoding/classification, threshold, line fit, interpolation or selected margin.',
        independence='Prior shared region/method knowledge; not blind or historically independent. Did not read current root or peer E3 annotations before freezing.',
        limits=['Core/fringe is an uncalibrated reading, not pre-raster containment.',
                'Shared-band identity withheld even where relative darkness suggests overprinting; no duplicate model assignment.',
                'Pale material outside selected sets remains unassigned, not proven outside mathematical curve.',
                'Separate local dash IDs do not imply mathematical gap endpoints or global model identity continuity.',
                'No physical ordinates, supported domain, metrics, human acceptance or causal inference. E4/E5 not inspected.'],
        routes={'solid':solid,'dash':dash},unassigned_bands=bands)

if __name__=='__main__':
    for p,h in PINS.items():
        assert sha(HERE/p)==h, p
    result=build()
    target=HERE/'reader-E3-independent.json'
    with target.open('x') as f:
        json.dump(result,f,indent=2); f.write('\n')
    print(json.dumps({'path':str(target),'sha256':sha(target),'script_sha256':sha(Path(__file__)),
                      'frozen_utc':result['frozen_utc'],'records':650,'context_cells':11186}))

"""E4 literal manual annotation; pixel checks validate but never choose cells."""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PINS={
 'PROTOCOL.md':'be57860a830ab716498ba5d25733021c1c975da1b0427f50f64071af4eaf5f16',
 'IDENTITY-CLARIFICATION.md':'c9d79b6d92a5cbc2f4747e027bce81ee5b1cbec0528b018b368f22fd2b01098b',
 '../PROTOCOL.md':'2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
 '../REGIONS.json':'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
 'context01.json':'59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
 'context02.json':'59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
 'read_context.py':'67e6788059653ba5d1e3eb18302e46bbc4299149646a8fed1516416dd7d1fe22',
 '../../native-strips01/Im9.jpg':'3154e28ea82ca2f39c465a7bdfe367677216543df296cf918cbbd259248f8129',
 '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}
# Literal inclusive ranges transcribed after all four RGB blocks were read.
BODIES=[(481,485),(489,494),(498,503),(508,513),(517,522),
 (526,531),(536,541),(545,550),(554,559),(563,568),(573,578),
 (582,587),(591,596),(600,605),(610,615),(619,624),(628,633),
 (638,643),(647,652),(656,661),(666,671),(675,680),(684,689)]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def flags(x,rows):
    return (["target_left"] if x==440 and rows else [])+(["target_right"] if x==689 and rows else [])+(["target_top"] if 72 in rows else [])+(["target_bottom"] if 91 in rows else [])

def row(x,core,fringe,status,note,fid=None,refs=None):
    return dict(x=x,core=list(core),fringe=list(fringe),status=status,note=note,
                fragment_id=fid,boundary_flags=flags(x,core+fringe),unassigned_band_refs=refs or [])

def build():
    bands=[]; routes={'solid':[],'dash':[]}
    for x in range(440,690):
        refs=[]
        if x<=480:
            bands.append(dict(band_id='E4-independent-shared-gold',x=x,
                core=[86,87],fringe=[85,88],boundary_flags=flags(x,[85,86,87,88]),
                competing_identities=['spring contribution','shell contribution','overprinted contributions'],
                note='One visible gold band; periodic modulation does not permit partition of coincident contributions. Core denotes ink, not model identity.'))
            refs=[{'band_id':'E4-independent-shared-gold','x':x}]
        routes['solid'].append(row(x,[],[],'identity_conflict',
            'No separately identified continuous spring footprint. A hidden/ended/overprinted contribution remains unresolved; no Im10 seam join.',refs=refs))
        routes['dash'].append(row(x,[],[],'identity_conflict' if refs else 'no_attributable_cells',
            'Shared gold contributions not individually resolved.' if refs else
            'Pale yellow/compression material inspected but not assigned to a dash; empty attribution is not a mathematical gap or absence.',refs=refs))
    for i,(a,b) in enumerate(BODIES,1):
        for x in range(a,b+1):
            routes['dash'][x-440]=row(x,[86],[85,87,88],
                'boundary_truncated' if x==689 else 'identified_local_fragment',
                'Visible repeated gold dash body; dashed style matches shell legend locally, without identifying any hidden spring ink.',
                f'E4-independent-dash-{i:02d}')
    return dict(reader='curve_recovery_feasibility; prior-informed independent AI source reader',pair='E4',pins=PINS,
        annotation_script_sha256=sha(Path(__file__)),
        freeze_status='Deterministic separately frozen reading; actual execution time reported with output hash, no live timestamp inserted.',
        coverage=dict(target_box=[440,72,690,92],context_box=[438,70,692,92],
            context_cells_read=5588,model_route_records=500,full_Im9_viewed=True,full_page_viewed=True,
            page_display='1700x2200 reduced to 1376x1780; context only',
            raw_blocks=[{'first':438,'last':500,'receipt':'01a459'},
                        {'first':501,'last':564,'receipt':'e1fe6b'},
                        {'first':565,'last':628,'receipt':'6b48f6'},
                        {'first':629,'last':691,'receipt':'5f05c3'}],
            rows_inclusive=[70,91],all_blocks_untruncated=True),
        method='Full unchanged native strip and page viewed, then every raw RGB context cell read in four finite blocks. Exact white alone omitted. Literal hand-authored runs expand mechanically; no classifier, fixed color cutoff, interpolation, fitted line or automatic margin. Pixel lookup below checks mistakes only; never changes selection.',
        independence='Source-informed, shared prior locator/method knowledge, not blind or independent historical evidence. No current root E4 or other reader E4 annotation read before freeze.',
        limits=['Visible ink membership is not calibrated pre-raster containment or mathematical support.',
            'Faint color between selected dash bodies remains unassigned; no claim of genuine empty gaps.',
            'No selected row91 cells: inspected bottom-edge pale material was not attributed; this does not validate seam continuity or an endpoint.',
            'Shared band not duplicated into two model observations. No physical ordinate or discrepancy, human acceptance or cause inference.',
            'Complete fixed E4 region reading only, not whole curve or all-pair completion.'],
        routes=routes,unassigned_bands=bands)

def verify(a):
    ctx=json.loads((HERE/'context01.json').read_text())['cells']['E4']
    cells={(c['x'],c['y']):c['rgb'] for c in ctx}
    assert len(cells)==len(ctx)==5588
    selected=[]
    for rs in a['routes'].values():
        assert [r['x'] for r in rs]==list(range(440,690))
        for r in rs:
            assert not r['unassigned_band_refs'] or not(r['core'] or r['fringe'])
            selected.append(r)
    selected+=a['unassigned_bands']
    white=[]
    for r in selected:
        assert r['core']==sorted(set(r['core'])) and r['fringe']==sorted(set(r['fringe']))
        assert not set(r['core']) & set(r['fringe'])
        assert all(72<=y<92 for y in r['core']+r['fringe'])
        assert r['boundary_flags']==flags(r['x'],r['core']+r['fringe'])
        white += [(r['x'],y) for y in r['core']+r['fringe'] if cells[r['x'],y]==[255,255,255]]
    assert not white, white
    bands={(b['band_id'],b['x']) for b in a['unassigned_bands']}
    for rs in a['routes'].values():
        for r in rs:
            assert all((q['band_id'],q['x']) in bands and q['x']==r['x'] for q in r['unassigned_band_refs'])
    a['verification']={'records':500,'context_cells':5588,'selected_exact_white':white,
        'bounds_membership_disjointness_and_references':'passed; no selections redrawn',
        'pre_freeze_failures':[]}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,choices=['reader-E4-independent.json','reader-E4-independent-repeat.json']);args=p.parse_args()
    for name,h in PINS.items(): assert sha(HERE/name)==h,name
    a=build();verify(a)
    target=HERE/args.output
    with target.open('x') as f: json.dump(a,f,indent=2);f.write('\n')
    print(json.dumps({'path':str(target),'sha256':sha(target),'script_sha256':sha(Path(__file__)), 'records':500,'context_cells':5588,'checks':'passed'}))

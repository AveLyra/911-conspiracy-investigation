"""Expand literal, manually inspected E6 selections; never read source pixels."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Inclusive manual column runs, core rows, fringe rows. These encode observations,
# not a color predicate, fitted line, repeated dash-period generator or margin.
SOLID = [(515,519,[70,71],[69,72]), (520,527,[70],[69,71]),
         (528,689,[69,70],[68,71])]
DASH_BODIES = [(515,518),(523,527),(532,537),(541,546),(551,555),
               (560,565),(569,574),(578,583),(588,592),(597,602),
               (606,611),(615,621),(624,630),(634,639),(643,648),
               (653,658),(662,667),(671,676),(680,685),(689,689)]
# Pale adjoining material is retained without allocating it to an assumed dash.
PALE = [519,522,528,531,538,540,547,550,556,559,566,568,575,577,
        584,587,593,596,603,605,612,614,622,633,640,642,649,652,
        661,668,670,677,686]
EMPTY = [520,521,529,530,539,548,549,557,558,567,576,585,586,
         594,595,604,613,623,631,632,641,650,651,659,660,669,
         678,679,687,688]

def pin(p):
    b=p.read_bytes(); return hashlib.sha256(b).hexdigest()

def entry(x,c,f,status,fragment,note):
    flags=[]
    if c or f:
        if x==515: flags.append('target_left')
        if x==689: flags.append('target_right')
        if 57 in c+f: flags.append('target_top')
        if 84 in c+f: flags.append('target_bottom')
    return {'x':x,'core':c,'fringe':f,'status':'boundary_truncated' if flags else status,
            'note':note,'fragment_id':fragment,'boundary_flags':flags}

def main():
    rows={'solid':{},'dash':{}}
    for first,last,c,f in SOLID:
        for x in range(first,last+1):
            rows['solid'][x]=entry(x,c,f,'identified_local_fragment','ind-E6-solid-01',
                'Continuous red band in full strip; manually read darker row(s) and tentative adjacent pale edge. Local style supports provisional solid identity; no calibrated bound.')
    for i,(first,last) in enumerate(DASH_BODIES,1):
        for x in range(first,last+1):
            assert x not in rows['dash']
            rows['dash'][x]=entry(x,[73,74],[72,75],'identified_local_fragment',f'ind-E6-dash-{i:02}',
                'Locally darker red short body in the broken band, separated in image context from adjacent bodies; pale neighboring rows tentative. No gap bridge.')
    for x in PALE:
        assert x not in rows['dash']
        rows['dash'][x]=entry(x,[],[73,74],'identity_conflict',None,
            'Pale red material near the broken band; attribution to a dash body versus compression/neighbor spread remains unresolved. Not assigned a fictitious continuous shell path.')
    for x in EMPTY:
        assert x not in rows['dash']
        rows['dash'][x]=entry(x,[],[],'no_attributable_cells',None,
            'Complete raw context column inspected; no cells confidently or tentatively attributed here. Not proof of a true gap, absent curve or zero.')
    for route,table in rows.items():
        assert sorted(table)==list(range(515,690)), (route,sorted(set(range(515,690))-set(table)))
        for e in table.values():
            assert e['core']==sorted(set(e['core'])) and e['fringe']==sorted(set(e['fringe']))
            assert not set(e['core'])&set(e['fringe'])
            assert all(type(y) is int and 57<=y<85 for y in e['core']+e['fringe'])
    pins={'source_sha256':pin(HERE.parent/'native-strips01/Im8.jpg'),
          'protocol_sha256':pin(HERE/'PROTOCOL.md'),'roster_sha256':pin(HERE/'REGIONS.json'),
          'raw_context_sha256':pin(HERE/'context01.json'),'literal_script_sha256':pin(Path(__file__))}
    assert pins['source_sha256']=='0c49df5f6117d3f0e9b206d7c3352edf57849e4ac00ef9764b857b1445947d83'
    assert pins['protocol_sha256']=='2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd'
    assert pins['roster_sha256']=='ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131'
    assert pins['raw_context_sha256']=='b611904d9f065dcd23860e7bca998b26a07b6c0196b20dd5af9d3b1e854cadfb'
    out={'reader':'curve_recovery_feasibility, independent E6 reader','pair':'E6','pins':pins,
         'coverage':{'full_native_Im8_viewed':True,'full_page076_viewed':True,
                     'page_display_resized':[1376,1780],'raw_context_box':[513,55,692,87],
                     'target_box':[515,57,690,85],'actual_raw_blocks':[[513,552],[553,602],[603,652],[653,691]],
                     'raw_receipts':['ead07f','24def2','adeed8','8615b9'],
                     'context_cells_read':5728,'target_records':350,'uninspected_records':0},
         'method':'Full unchanged native strip and composed legend viewed; every raw context column read without truncation using exact-white omission only. Literal manual runs mechanically expanded; no RGB classifier, threshold, interpolation, fitted centerline or added margin. Repeated row membership reflects inspected near-horizontal bands, not inferred latent geometry.',
         'independence':'Prior source/renderer/context-verification knowledge shared; not blind or historical independence. No root or peer new annotations read before freeze.',
         'limits':['Core/fringe are subjective native ink assignments, not calibrated containment bounds.','Unallocated pale dash material remains identity_conflict with no fragment ID; unknown is not empty support.','Separate dash bodies are reader-local, not a continuous reconstructed path.','No physical ordinates, support union, human acceptance or causal conclusion.'],
         'routes':{r:[table[x] for x in range(515,690)] for r,table in rows.items()}}
    with (HERE/'reader-E6-independent.json').open('x') as f:
        json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({'records':350,'json_sha256':pin(HERE/'reader-E6-independent.json'),'script_sha256':pin(Path(__file__))}))

if __name__=='__main__': main()

"""Deterministic post-exchange three-cell erratum; preserve original evidence."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIGINAL = '245b5ffe99b0481ab86e57c3bb7d1fccd7d1539a6ce004de967ec118d2e6c243'
CONTEXT = '59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48'
CHANGES = [(372,46),(373,46),(381,45)]

def digest(b):
    return hashlib.sha256(b).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True,choices=[
        'reader-E3-independent-corrected.json',
        'reader-E3-independent-corrected-repeat.json'])
    args=p.parse_args()
    original_bytes=(HERE/'reader-E3-independent.json').read_bytes()
    context_bytes=(HERE/'context01.json').read_bytes()
    assert digest(original_bytes)==ORIGINAL
    assert digest(context_bytes)==CONTEXT
    original=json.loads(original_bytes)
    raw=json.loads(context_bytes)['cells']['E3']
    cells={(r['x'],r['y']):r['rgb'] for r in raw}
    assert len(cells)==len(raw)==11186
    selected_white=[]
    for route,rows in original['routes'].items():
        for r in rows:
            for kind in ('core','fringe'):
                for y in r[kind]:
                    if cells[r['x'],y]==[255,255,255]:
                        selected_white.append((route,r['x'],y,kind))
    for r in original['unassigned_bands']:
        for kind in ('core','fringe'):
            for y in r[kind]:
                if cells[r['x'],y]==[255,255,255]:
                    selected_white.append(('unassigned',r['x'],y,kind))
    assert sorted(selected_white)==sorted(('unassigned',x,y,'fringe') for x,y in CHANGES)
    corrected=copy.deepcopy(original)
    for x,y in CHANGES:
        rows=[r for r in corrected['unassigned_bands'] if r['x']==x]
        assert len(rows)==1
        r=rows[0]
        assert r['band_id']=='E3-independent-shared-band'
        assert r['fringe'].count(y)==1 and y not in r['core']
        r['fringe'].remove(y)
    # Verify the complete annotation object by reversing precisely the removals.
    restored=copy.deepcopy(corrected)
    for x,y in CHANGES:
        r=next(r for r in restored['unassigned_bands'] if r['x']==x)
        r['fringe']=sorted(r['fringe']+[y])
    assert restored==original
    assert corrected['routes']==original['routes']
    original_freeze=corrected.pop('frozen_utc')
    corrected['source_history']={'original_frozen_utc':original_freeze,
        'retained_metadata_status':'All other original metadata and coverage retained verbatim as source history, not a new reading or freeze.'}
    corrected['correction']={
        'status':'post-exchange erratum; deterministic corrected derivative, not second blind reading',
        'parent_file':'reader-E3-independent.json','parent_sha256':ORIGINAL,
        'context_file':'context01.json','context_sha256':CONTEXT,
        'correction_script_sha256':digest(Path(__file__).read_bytes()),
        'changes':[{'band_id':'E3-independent-shared-band','x':x,'y':y,
                    'operation':'remove fringe membership','rgb':[255,255,255]} for x,y in CHANGES],
        'reason':'Overbroad literal manual run transcription included three exact-white cells; no new source attribution.',
        'corrected_freeze_utc':None,
        'freeze_note':'Deterministic artifact; actual execution and file hash are reported separately. Original timestamp is history only.',
        'verification':{'removed_cells':3,'all_routes_unchanged':True,
                        'all_other_original_fields_unchanged_except_relocated_freeze':True,
                        'new_source_decisions':0}}
    output=HERE/args.output
    data=(json.dumps(corrected,indent=2)+'\n').encode()
    with output.open('xb') as f: f.write(data)
    print(json.dumps({'file':str(output),'sha256':digest(data),'removed_cells':3,
                      'routes_unchanged':True,'reverse_change_verification':True}))

if __name__=='__main__': main()

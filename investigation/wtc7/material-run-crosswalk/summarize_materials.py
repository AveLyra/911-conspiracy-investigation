#!/usr/bin/env python3
"""Deterministic report arithmetic on retained typed outputs, no new source read."""
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
def read(name,pin):
    data=(HERE/name).read_bytes()
    assert hashlib.sha256(data).hexdigest()==pin, 'input_pin'
    return json.loads(data)

def compute():
    a=read('run01.json','b69c12ec0668c9bdf5f5ea59dbf483d2a959de7bd477c172efe69c2f03e33594')
    b=read('run02.json','7663fa0b97ea7f3177aca68de215115db77b499da97530250d382d0214b129b3')
    assert {k:v for k,v in a.items() if k!='elapsed_seconds'}=={k:v for k,v in b.items() if k!='elapsed_seconds'}, 'repeat_difference'
    parts={p['pid']:p for p in a['all_part_references']}
    used={p['pid']:p for p in a['used_parts']}
    missing=set(a['missing_used_parts'])
    shell=Counter(p['pid'] for p in a['damage_matches'] if p['kind']=='shell')
    discrete=Counter(p['pid'] for p in a['damage_matches'] if p['kind']=='discrete')
    selected={p['part']['pid']:p for p in a['selected_parts']}
    rows=[]
    for pid in sorted(missing):
        p=parts[pid]; q=parts[pid+1000]
        rows.append(dict(pid=pid,mid=p['mid'],sid=p['sid'],part_line=p['card_line'],
            section_line=selected[pid]['section']['keyword_line'],
            shell_count=used[pid]['elements']['shell'],damage_set2_shell_count=shell[pid],
            counterpart_pid=q['pid'],counterpart_mid=q['mid'],counterpart_part_line=q['card_line'],
            counterpart_used=q['pid'] in used,
            original_part_cards_equal=p['values']==q['values'],title_hash_equal=p['title_sha256']==q['title_sha256'],
            unequal_original_card_fields=[i+1 for i,(u,v) in enumerate(zip(p['values'],q['values'])) if u!=v]))
    return dict(repeated_results_equal_excluding_elapsed=True,missing_part_rows=rows,
        missing_shells=sum(p['shell_count'] for p in rows),
        damage_shell_missing_material=sum(p['damage_set2_shell_count'] for p in rows),
        damage_shell_all=sum(shell.values()),damage_shell_by_part=dict(shell),
        damage_discrete_by_part=dict(discrete),
        damage_discrete_missing_material=sum(v for p,v in discrete.items() if p in missing),
        same_raw_part_cards=sum(p['original_part_cards_equal'] for p in rows),
        unequal_raw_part_cards=sum(not p['original_part_cards_equal'] for p in rows),
        same_part_title_hash=sum(p['title_hash_equal'] for p in rows),
        material_counterpart_count=len(a['transformed_same_original_id_candidates']),
        six_explicit_beams=[{k:p[k] for k in ('source','line','kind','eid','pid','values','selection')}
                            for p in a['damage_matches'] if p['kind']=='beam'],
        total_uncompressed_bytes=sum(v['uncompressed_bytes'] for v in a['receipts'].values()),
        total_lines=sum(v['lines'] for v in a['receipts'].values()))

if __name__=='__main__':
    result=compute(); out=HERE/'crosswalk-summary01.json'
    with out.open('x') as f: json.dump(result,f,sort_keys=True,indent=2); f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,(list,dict))},sort_keys=True))
    print('sha256',hashlib.sha256(out.read_bytes()).hexdigest())

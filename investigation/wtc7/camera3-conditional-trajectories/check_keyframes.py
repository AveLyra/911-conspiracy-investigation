#!/usr/bin/env python3
"""Post-result numeric keyframe membership follow-up; no arbitrary XML exports."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
SOURCE=Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/nested/Camera3-test_Camera3-test.trk')
MASS='org.opensourcephysics.cabrillo.tracker.PointMass'


def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}


def main():
    out=HERE/'keyframes01.json'
    if out.exists(): raise ValueError('output_exists')
    inputs={'source':SOURCE,'points':HERE/'extraction01/points.json',
            'declaration':HERE/'KEYFRAME-ADDENDUM.md','producer':Path(__file__)}
    before={k:pin(v) for k,v in inputs.items()}
    assert before['source']['sha256']=='955d1c2d00d7c287f4f235063eb603a0080cf0941595a5419aa7c94726c1a41c'
    assert before['points']['sha256']=='f85e6f0ddbb55e3ef142a62e774237c69a59b9bbcbc31a92f93a37b9a9099df3'
    raw=SOURCE.read_bytes()
    if len(raw)>10_000_000 or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('rejected_xml_envelope')
    try: root=ET.fromstring(raw)
    except ET.ParseError: raise ValueError('invalid_xml') from None
    objects=[o for o in root.findall("./property[@name='tracks']/property/object") if o.get('class')==MASS]
    assert len(objects)==2
    points=json.loads(inputs['points'].read_text())
    rows=[]
    for ordinal,obj in enumerate(objects,1):
        fields=obj.findall("./property[@name='keyFrames']")
        if len(fields)>1: raise ValueError('duplicate_keyframe_array')
        keys=[]
        if fields:
            arr=fields[0]
            if arr.get('type')!='array': raise ValueError('unexpected_array_type')
            children=list(arr)
            if len(children)==1 and children[0].get('type')=='string':
                literal=(children[0].text or '').strip()
                if not re.fullmatch(r'\{\s*\d{1,3}(?:\s*,\s*\d{1,3})*\s*\}',literal):
                    raise ValueError('unexpected_braced_integer_list')
                children=[]
                for pos,item in enumerate(literal.strip('{}').split(',')):
                    entry=ET.Element('property',name=f'[{pos}]',type='int')
                    entry.text=item.strip()
                    children.append(entry)
            for pos,entry in enumerate(children):
                if entry.get('name')!=f'[{pos}]' or entry.get('type')!='int':
                    raise ValueError('unexpected_integer_array_shape')
                literal=(entry.text or '').strip()
                if not re.fullmatch(r'\d{1,3}',literal): raise ValueError('non_integer_key')
                value=int(literal)
                if not 0<=value<=441: raise ValueError('out_of_range_key')
                keys.append(value)
        if len(keys)!=len(set(keys)): raise ValueError('duplicate_keyframe')
        marked=[p['frame'] for p in points['tracks'][ordinal-1]['points']]
        rows.append({'track':f'track{ordinal:02d}','saved_keyframes_present':bool(fields),
                     'keyframes':keys,'count':len(keys),
                     'saved_marks_not_in_keyframes':sorted(set(marked)-set(keys)),
                     'keyframes_not_in_saved_marks':sorted(set(keys)-set(marked)),
                     'loader_missing_empty_fallback_applies_if_this_code_path_runs':not bool(keys)})
    after={k:pin(v) for k,v in inputs.items()}
    assert before==after
    result={'status':'pass_saved_keyframe_membership_only','inputs_before':before,'inputs_after':after,'tracks':rows}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'key_counts':[r['count'] for r in rows],
                      'saved_nonkey_counts':[len(r['saved_marks_not_in_keyframes']) for r in rows]}))


if __name__=='__main__': main()

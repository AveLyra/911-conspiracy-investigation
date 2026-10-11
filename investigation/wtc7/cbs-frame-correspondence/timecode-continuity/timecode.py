"""Strict, fixed-population counter analysis; no media decoding or clock authentication."""
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import re

UNIT = Path(__file__).resolve().parent
REQUIRED = {
    'PLAN.md', 'references.md', 'timecode.py', 'test_timecode.py',
    'sources/ffmpeg-n7.1-timecode.c', 'sources/ffmpeg-n7.1-timecode.h',
    'sources/ffmpeg-n7.1-dv.c',
    '../dv-metadata/sources/ffmpeg-n7.1-libavformat-dvenc.c',
    '../dv-metadata/sources/ffmpeg-n7.1-libavcodec-dv_profile.c',
    '../dv-metadata/v2/freeze.json', '../dv-metadata/independent-audit.json',
    '../dv-metadata/v2/inventory-summary.json',
    '../sibling-lineage/results.json', '../sibling-lineage/inputs.json',
} | {f'../dv-metadata/v2/results/clip{n}-result.json' for n in range(1,9)}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}


def controls():
    frozen = json.loads((UNIT/'freeze.json').read_text())
    require(set(frozen['files'])==REQUIRED,'incomplete frozen dependency set')
    for name, expected in frozen['files'].items():
        require(pin(UNIT/name)==expected,'changed frozen dependency: '+name)
    return pin(UNIT/'freeze.json')


def component_issues(parts):
    return [name+'_range' for name,value,limit in zip(('h','m','s','f'),parts,(24,60,60,30))
            if type(value) is not int or not 0<=value<limit]


def ordinal(parts, drop):
    require(isinstance(parts,(list,tuple)) and len(parts)==4 and type(drop) is bool,
            'invalid ordinal arguments')
    issues = component_issues(parts)
    if issues:
        return None, issues
    h,m,s,f = parts
    if drop and m%10!=0 and s==0 and f<2:
        return None,['omitted_drop_frame_label']
    nominal = (h*3600+m*60+s)*30+f
    minutes = h*60+m
    return nominal-(2*(minutes-minutes//10) if drop else 0),[]


def decode(raw_hex):
    require(isinstance(raw_hex,str) and re.fullmatch(r'13[0-9a-f]{8}',raw_hex) is not None,
            'not a five-byte raw timecode candidate')
    payload = bytes.fromhex(raw_hex)[1:]
    values = []
    issues = []
    for name,value,mask in zip(('f','s','m','h'),payload,(0x3f,0x7f,0x7f,0x3f)):
        bcd = value & mask
        low,high = bcd&15,bcd>>4
        if low>9 or high>9:
            values.append(None)
            issues.append(name+'_invalid_bcd')
        else:
            values.append(low+10*high)
    parts = list(reversed(values))
    issues += component_issues(parts)
    nd,nd_errors = ordinal(parts,False)
    df,df_errors = ordinal(parts,True)
    drop = bool(payload[0]&0x40)
    return {'raw_hex':raw_hex,'components_h_m_s_f':parts,'component_issues':issues,
            'drop_bit':drop,'positional_flag_hex':bytes((payload[0]&0xc0,payload[1]&0x80,payload[2]&0x80,payload[3]&0xc0)).hex(),
            'nd':nd,'df':df,'selected':df if drop else nd,
            'nd_issues':nd_errors,'df_issues':df_errors,
            'selected_issues':df_errors if drop else nd_errors}


def parse_header(text):
    if not isinstance(text,str) or re.fullmatch(r'[0-9]{2};[0-9]{2};[0-9]{2};[0-9]{2}',text) is None:
        return {'text':text,'components_h_m_s_f':None,'issues':['unsupported_native_label_syntax']}
    parts = [int(x) for x in text.split(';')]
    return {'text':text,'components_h_m_s_f':parts,'issues':component_issues(parts)}


def reconstruct(document, expected_frames):
    result = document['result']
    require(type(result['frames']) is int and result['frames']==expected_frames,'frame population')
    require(type(expected_frames) is int and 1<=expected_frames<=2500,'unsupported population')
    variants = result['target_variants']
    require(len(variants)==expected_frames,'candidate population changed')
    ordered = [None]*expected_frames
    for v in variants:
        f = v['first_frame']
        require(type(f) is int and 0<=f<expected_frames,'candidate index')
        require(v['area']=='subcode' and type(v['last_frame']) is int and v['last_frame']==f
                and type(v['frames_present']) is int and v['frames_present']==1
                and type(v['occurrences']) is int and v['occurrences']==40,'candidate support changed')
        require(ordered[f] is None,'overlapping candidate frame')
        ordered[f] = v['raw_hex']
    require(all(v is not None for v in ordered),'missing candidate frame')
    require(len(set(ordered))==expected_frames,'audited raw-value uniqueness changed')
    return ordered


def transitions(rows):
    edges=[]
    for i,(a,b) in enumerate(zip(rows,rows[1:])):
        changed = a['drop_bit']!=b['drop_bit']
        edge={'left_frame':i,'right_frame':i+1,'drop_bit_changed':changed,
              'selected_raw_difference':None if a['selected'] is None or b['selected'] is None else b['selected']-a['selected'],
              'flag_xor_hex':f"{int(a['positional_flag_hex'],16)^int(b['positional_flag_hex'],16):08x}"}
        for lane in ('nd','df','selected'):
            delta = None if a[lane] is None or b[lane] is None or (lane=='selected' and changed) else b[lane]-a[lane]
            edge[lane+'_delta']=delta
            modulus=2589408 if lane=='df' or (lane=='selected' and a['drop_bit']) else 2592000
            edge[lane+'_possible_daily_rollover']=delta==1-modulus
        edges.append(edge)
    return edges


def analyze_clip(document, header):
    count=document['result']['frames']
    rows=[{'frame':i,**decode(raw)} for i,raw in enumerate(reconstruct(document,count))]
    edges=transitions(rows)
    lanes={}
    for lane in ('nd','df','selected'):
        lanes[lane]={'invalid_frames':[r['frame'] for r in rows if r[lane] is None],
                     'one_step_edges':sum(e[lane+'_delta']==1 for e in edges),
                     'non_one_step_right_frames':[e['right_frame'] for e in edges if e[lane+'_delta'] is not None and e[lane+'_delta']!=1],
                     'unavailable_right_frames':[e['right_frame'] for e in edges if e[lane+'_delta'] is None],
                     'possible_daily_rollover_right_frames':[e['right_frame'] for e in edges if e[lane+'_possible_daily_rollover']],
                     'first_ordinal':rows[0][lane],'last_ordinal':rows[-1][lane]}
    labels={}
    for key in ('tc_O','tc_A'):
        entries=header['fields'][key]
        require(len(entries)==1,'header label occurrence changed')
        label=parse_header(entries[0]['prefix_utf8'])
        label['matches_first_components']=not label['issues'] and not rows[0]['component_issues'] and label['components_h_m_s_f']==rows[0]['components_h_m_s_f']
        for lane,drop in (('nd',False),('df',True)):
            value,errors=ordinal(label['components_h_m_s_f'],drop) if label['components_h_m_s_f'] is not None else (None,['syntax'])
            label[lane+'_ordinal']=value
            label[lane+'_issues']=errors
            label[lane+'_start_difference']=None if value is None or rows[0][lane] is None else rows[0][lane]-value
        labels[key]=label
    video=header['video_header']
    require(all(type(video[k]) is int and video[k]>0 for k in ('scale','rate','length')),'invalid header counts/rate')
    require(video['length']==count and type(video['start']) is int and video['start']==0,'header frame/start mismatch')
    period=Fraction(video['scale'],video['rate']); nominal=Fraction(1001,30000)
    require(period==Fraction(video['time_base']),'header rational inconsistency')
    summary={'clip':document['clip'],'frames':count,'edges':len(edges),'first':rows[0], 'last':rows[-1],
             'component_invalid_frames':[r['frame'] for r in rows if r['component_issues']],
             'drop_bit_counts':dict(Counter(str(r['drop_bit']) for r in rows)),
             'positional_flag_counts':dict(Counter(r['positional_flag_hex'] for r in rows)),
             'flag_change_right_frames':[e['right_frame'] for e in edges if e['flag_xor_hex']!='00000000'],
             'lanes':lanes,'header_comparisons':labels,
             'avi_frame_period':str(period),'nominal_dv_frame_period':str(nominal),
             'period_difference_avi_minus_nominal':str(period-nominal),
             'first_to_last_avi_span':str((count-1)*period),
             'first_to_last_nominal_dv_span':str((count-1)*nominal),
             'container_duration_avi':str(count*period)}
    return {'summary':summary,'frames':rows,'transitions':edges}


def compare_clips(clips):
    pairs=[]
    for i,a in enumerate(clips):
        for b in clips[i+1:]:
            pair={'left_clip':a['summary']['clip'],'right_clip':b['summary']['clip'],'lanes':{}}
            for lane in ('nd','df','selected'):
                left=[r[lane] for r in a['frames']]; right=[r[lane] for r in b['frames']]
                available=all(x is not None for x in left+right)
                if lane=='selected':
                    available=available and len({r['drop_bit'] for r in a['frames']+b['frames']})==1
                pair['lanes'][lane]=None if not available else {
                    'start_difference':right[0]-left[0],
                    'all_left_ordinals_before_right':max(left)<min(right),
                    'boundary_counter_distance':right[0]-left[-1],
                    'unrepresented_counter_positions':right[0]-left[-1]-1}
            pairs.append(pair)
    return pairs


def main():
    destination=UNIT/'result01.json'
    require(not destination.exists() and not destination.is_symlink(),'result already exists')
    before=controls()
    read=lambda name:json.loads((UNIT/name).read_text())
    header=read('../sibling-lineage/results.json')
    inputs=read('../sibling-lineage/inputs.json')
    audit=read('../dv-metadata/independent-audit.json')
    require(header['all_pins_unchanged_after'] is True and audit['all_checks_pass'] is True,'prior result gates')
    require([x['clip'] for x in header['items']]==[x['clip'] for x in inputs['items']]==[x['clip'] for x in audit['clips']]==list(range(1,9)),'clip identity population')
    results=[]
    for n,h,item,a in zip(range(1,9),header['items'],inputs['items'],audit['clips'],strict=True):
        path=f'../dv-metadata/v2/results/clip{n}-result.json'
        require(pin(UNIT/path)==a['result_pin'],'audit result pin mismatch')
        document=read(path)
        require(document['source']==h['source']==item and document['clip']==n,'source identity join')
        require(document['before_after_pins_match'] is True and document['artifact_readback_verified'] is True,'raw result gates')
        require(document['result']['frames']==int(item['saved_video']['nb_frames']),'input count join')
        results.append(analyze_clip(document,h))
    require(sum(x['summary']['frames'] for x in results)==5567,'total frames')
    require(sum(x['summary']['edges'] for x in results)==5559,'total transitions')
    pairs=compare_clips(results)
    require(len(pairs)==28,'pair population')
    require(controls()==before,'freeze changed during calculation')
    output={'schema':'dv-timecode-continuity-v1','python':platform.python_version(),'freeze_pin':before,
            'scope':'Component/range/DF arithmetic, not full DV conformance or camera chronology',
            'before_after_pins_match':True,'clips':results,'conditional_pairs':pairs}
    text=json.dumps(output,sort_keys=True,separators=(',',':'))+'\n'
    require(len(text.encode())<=8*1024*1024,'output cap')
    with destination.open('x',encoding='utf-8') as stream:stream.write(text)
    require(json.loads(destination.read_text())==output,'result readback mismatch')
    print(json.dumps({'result':str(destination),'pin':pin(destination),'frames':5567,'transitions':5559,'pairs':28}))


if __name__=='__main__':main()

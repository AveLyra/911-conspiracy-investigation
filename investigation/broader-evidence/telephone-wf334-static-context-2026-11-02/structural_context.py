"""Passive structural references for selected court text; no ActionScript execution.

Uses the earlier static font/tag reader. Frame ordinals are local authored
ShowFrame positions, not runtime path, clock time or actual joint visibility.
Only explicit-character PlaceObject2 edges are graphed. Button records,
move-only updates, clipping and actions are not simulated.
"""
from collections import Counter,defaultdict
import hashlib,struct
from static_swf_text import Bits,tags,extract

TEXT_IDS={331,930,1786,1787,433}
SPRITE_IDS={778,985,1788,2011}

def place_prefix(body):
    if len(body)<3:raise ValueError('truncated PlaceObject2')
    flags=body[0];depth=struct.unpack_from('<H',body,1)[0];pos=3
    cid=None
    if flags&2:
        cid=struct.unpack_from('<H',body,pos)[0];pos+=2
    if flags&4:
        bits=Bits(body,pos);bits.matrix();pos=bits.align()
    if flags&8:
        bits=Bits(body,pos);add=bits.take(1);mult=bits.take(1);n=bits.take(4)
        for _ in range(4*(add+mult)):bits.take(n,True)
        pos=bits.align()
    ratio=None
    if flags&16:
        ratio=struct.unpack_from('<H',body,pos)[0];pos+=2
    name=None
    if flags&32:
        end=body.index(0,pos);name=body[pos:end].decode('utf-8');pos=end+1
    return dict(flags=flags,depth=depth,character_id=cid,move=bool(flags&1),ratio=ratio,instance_name=name,prefix_bytes=pos)

def check_controls():
    # Fixed byte vectors test fields and ID-absent updates, not historical facts.
    vectors=[(b'\x02\x07\x00\x17\x00',dict(flags=2,depth=7,character_id=23,move=False,ratio=None,instance_name=None,prefix_bytes=5)),
      (b'\x01\x07\x00',dict(flags=1,depth=7,character_id=None,move=True,ratio=None,instance_name=None,prefix_bytes=3)),
      (b'\x03\x02\x00\xa2\x03',dict(flags=3,depth=2,character_id=930,move=True,ratio=None,instance_name=None,prefix_bytes=5)),
      (b'\x22\x07\x00\x17\x00Name\x00',dict(flags=34,depth=7,character_id=23,move=False,ratio=None,instance_name='Name',prefix_bytes=10)),
      (b'\x16\x01\x00\x17\x00\x00\xff\xff',dict(flags=22,depth=1,character_id=23,move=False,ratio=65535,instance_name=None,prefix_bytes=8)),
      (b'\x2a\x01\x00\x17\x00\x00X\x00',dict(flags=42,depth=1,character_id=23,move=False,ratio=None,instance_name='X',prefix_bytes=8))]
    for raw,want in vectors:assert place_prefix(raw)==want
    failed=False
    try:place_prefix(b'\x02\x01')
    except (ValueError,struct.error,IndexError):failed=True
    assert failed
    return dict(valid_vectors=len(vectors),truncation_controls=1,scope='Byte/optional-field parsing only; not runtime, independent historical decoder or source authentication.')

def analyze(raw):
    assert raw[:3]==b'FWS'
    assert len(raw)==struct.unpack_from('<I',raw,4)[0]
    bits=Bits(raw,8);bits.rect();start=bits.align()+4
    alltags=list(tags(raw,start,len(raw)))
    counts=Counter();frames=defaultdict(lambda:1);sprites={};edges=[];labels=[];actions=Counter()
    for code,off,body,path in alltags:
        frame=frames[path];counts[code]+=1
        if code==39:
            sid,n=struct.unpack_from('<HH',body)
            assert sid not in sprites
            sprites[sid]=dict(id=sid,definition_offset=off,declared_frames=n)
        if code==12:actions[path]+=1
        if code==26:
            x=place_prefix(body)
            if x['character_id'] is not None:
                edges.append(dict(x,container=path,placement_offset=off,frame_ordinal=frame,body_length=len(body),body_sha256=hashlib.sha256(body).hexdigest(),encoded_prefix_hex=body[:x['prefix_bytes']].hex()))
        if code==43:
            end=body.index(0);label=body[:end].decode('utf-8')
            if label=='Reuben' and path in ('root/sprite-985','root/sprite-2011'):
                labels.append(dict(container=path,tag_offset=off,frame_ordinal=frame,label=label,body_sha256=hashlib.sha256(body).hexdigest()))
        if code==1:frames[path]+=1
    assert not any(counts[x] for x in [4,70]),'Unsupported placement tag present'
    for sid,x in sprites.items():
        assert frames['root/sprite-'+str(sid)]-1==x['declared_frames'],sid
    root_frames=frames['root']-1
    # FrameCount follows FrameSize and FrameRate in the main SWF header.
    assert struct.unpack_from('<H',raw,start-2)[0]==root_frames
    d=extract(raw);texts=[x for x in d['text_definitions'] if x['id'] in TEXT_IDS]
    selected=[e for e in edges if e['character_id'] in TEXT_IDS|SPRITE_IDS]
    relcontainers=['root','root/sprite-778','root/sprite-985','root/sprite-1788','root/sprite-2011']
    return dict(input_sha256=hashlib.sha256(raw).hexdigest(),input_bytes=len(raw),swf_version=raw[3],root_declared_frames=root_frames,full_structure_counts=dict(sprites=len(sprites),PlaceObject2=counts[26],explicit_character_placements=len(edges),ShowFrame=counts[1],DoAction=counts[12],DefineButton2=counts[34]),all_sprite_frame_counts_match=True,selected_sprite_definitions=[sprites[x] for x in sorted(SPRITE_IDS)],selected_text_definitions=texts,selected_placements=selected,selected_Reuben_labels=labels,unexecuted_actions_by_selected_container={x:actions[x] for x in relcontainers},scope='Static explicit-reference subset, local authored frame positions and names. No move-only state simulation, button links, transforms/visibility/clipping, ActionScript evaluation, visited path, caller/flight/manifest/message/carrier/canvass authentication.')

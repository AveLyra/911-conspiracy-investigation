"""Passive static control/stream comparison of two held court SWFs.

python3 compare_sound_controls.py /path/to/court-flights.zip [--helper PATH]
No SWF execution, audio playback/decoding, media writes or network calls.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import zipfile

ARCHIVE_SHA = '3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801'
HELPER_SHA = '2af3d0339c5ca876255948a014205f8caa6ff019c1303e79a0ba774a22f36ade'
MEMBERS = {'Lyles.swf':'28f2a83db87177a2538ebd36ddfc03b63e7b696b7d16603a793921ff27ce4ec7',
           'Ong.swf':'8c844a2370852e55597a4aa73ef8b8ff0e6c03e3fec982a9cd98aeb937e5a3ec'}
TRANSITIONS = ('OverUpToIdle','IdleToOverUp','OverUpToOverDown','OverDownToOverUp')
MAX_BYTES=64*1024*1024

def sha(b): return hashlib.sha256(b).hexdigest()

def read(b,p,fmt):
    n=struct.calcsize(fmt)
    if p+n>len(b):raise ValueError('Truncated sound/control field')
    return struct.unpack_from(fmt,b,p),p+n

def soundinfo(b,p):
    (flags,),p=read(b,p,'<B')
    if flags&0xc0:raise ValueError('Nonzero SoundInfo reserved bits')
    r={'flags':flags,'sync_stop':bool(flags&32),'sync_no_multiple':bool(flags&16)}
    for flag,key,fmt in [(1,'in_point','<I'),(2,'out_point','<I'),(4,'loop_count','<H')]:
        if flags&flag:
            (r[key],),p=read(b,p,fmt)
    if flags&8:
        (n,),p=read(b,p,'<B');r['envelopes']=[]
        for _ in range(n):
            v,p=read(b,p,'<IHH');r['envelopes'].append({'pos44':v[0],'left_level':v[1],'right_level':v[2]})
    return r,p

def buttonsound(b):
    (button,),p=read(b,0,'<H');rows=[]
    for label in TRANSITIONS:
        (sound,),p=read(b,p,'<H');row={'transition':label,'sound_id':sound}
        if sound:row['sound_info'],p=soundinfo(b,p)
        rows.append(row)
    if p!=len(b):raise ValueError('Unconsumed DefineButtonSound bytes')
    return button,rows

def controls():
    z,p=soundinfo(b'\0',0);assert p==1 and z=={'flags':0,'sync_stop':False,'sync_no_multiple':False}
    b=b'\x3f'+struct.pack('<IIHB',123,456,7,2)+struct.pack('<IHHIHH',10,100,200,20,300,400)
    a,p=soundinfo(b,0);assert p==len(b) and a['in_point']==123 and a['out_point']==456 and a['loop_count']==7
    assert a['envelopes']==[{'pos44':10,'left_level':100,'right_level':200},{'pos44':20,'left_level':300,'right_level':400}]
    assert a['sync_stop'] and a['sync_no_multiple']
    rejected=0
    for end in range(len(b)):
        try:soundinfo(b[:end],0)
        except ValueError:rejected+=1
    assert rejected==len(b)
    try:soundinfo(b'\xc0',0)
    except ValueError:pass
    else:raise AssertionError('Reserved bits not rejected')
    button,rows=buttonsound(struct.pack('<HHH',7,0,11)+b'\0'+struct.pack('<HH',0,0))
    assert button==7 and [x['sound_id'] for x in rows]==[0,11,0,0] and rows[1]['sound_info']['flags']==0
    try:buttonsound(struct.pack('<HH',7,11))
    except ValueError:pass
    else:raise AssertionError('Truncated button not rejected')
    return {'zero_flags':'pass','all_conditional_fields_and_two_envelopes':'pass','all_truncated_full_field_prefixes_rejected':rejected,'reserved_bits_rejected':True,'button_zero_and_nonzero_slots':'pass','truncated_button_rejected':True,'scope':'Parser controls only; not historical validation'}

def analyze(raw,name,helper):
    assert sha(raw)==MEMBERS[name];data=helper.unpack(raw)
    rectend=8+(5+4*(data[8]>>3)+7)//8
    rate_raw,declared_frames=struct.unpack_from('<HH',data,rectend);start=rectend+4
    tags=list(helper.walk(data,start,len(data)));roots=[t for t in tags if t[3]=='root']
    definitions={};button_ids=set();event_controls=[];button_controls=[];stream_heads=[];blocks=[];frame=1;chunks=[]
    for code,offset,body,path in tags:
        if code in (7,34):
            if len(body)<2:raise ValueError('Short button definition')
            button_ids.add(struct.unpack_from('<H',body)[0])
        if code==14:
            if len(body)<7:raise ValueError('Short sound definition')
            sid=struct.unpack_from('<H',body)[0]
            if sid in definitions:raise ValueError('Duplicate character sound ID')
            r={'sound_id':sid,'offset':offset,'container':path,'body_sha256':sha(body),'format_code':body[2]>>4,'rate_code':(body[2]>>2)&3,'declared_sample_count':struct.unpack_from('<I',body,3)[0]}
            if r['format_code']==2:
                if len(body)<9:raise ValueError('Short event MP3 fields')
                r.update(seek_samples=struct.unpack_from('<h',body,7)[0],mp3_bytes=len(body)-9,mp3_sha256=sha(body[9:]))
            definitions[sid]=(r,body[9:] if r['format_code']==2 else None)
        if code==17:
            bid,rows=buttonsound(body);button_controls.append({'offset':offset,'container':path,'body_sha256':sha(body),'button_id':bid,'transitions':rows})
        if code==15:
            (sid,),p=read(body,0,'<H');si,p=soundinfo(body,p)
            if p!=len(body):raise ValueError('Trailing StartSound data')
            event_controls.append({'offset':offset,'container':path,'sound_id':sid,'sound_info':si})
    for code,offset,body,path in roots:
        if code in (18,45):
            if len(body)<4:raise ValueError('Short stream header')
            compression=body[1]>>4
            r={'offset':offset,'frame':frame,'code':code,'header_hex':body.hex(),'compression':compression,'rate_code':(body[1]>>2)&3,'average_sample_count':struct.unpack_from('<H',body,2)[0]}
            need=6 if compression==2 else 4
            if len(body)!=need:raise ValueError('Unexpected stream header length')
            if compression==2:r['latency_seek']=struct.unpack_from('<h',body,4)[0]
            stream_heads.append(r)
        if code==19:
            if len(stream_heads)!=1 or stream_heads[0]['compression']!=2:raise ValueError('Unsupported or ambiguous root stream')
            (samples,seek),_=read(body,0,'<Hh');payload=body[4:]
            blocks.append({'offset':offset,'frame':frame,'body_bytes':len(body),'sample_count':samples,'seek_samples':seek,'mp3_bytes':len(payload),'mp3_sha256':sha(payload)})
            chunks.append(payload)
        if code==1:frame+=1
    if not blocks:raise ValueError('No root MP3 blocks in scoped member')
    if len({b['frame'] for b in blocks})!=len(blocks):raise ValueError('Multiple root stream blocks at one frame')
    joined=b''.join(chunks);resource,payload=definitions[1]
    if payload is None:raise ValueError('Scoped resource1 is not MP3')
    mismatch=next((i for i,(a,b) in enumerate(zip(joined,payload)) if a!=b),None)
    if mismatch is None and len(joined)!=len(payload):mismatch=min(len(joined),len(payload))
    for row in button_controls:
        row['button_definition_exists']=row['button_id'] in button_ids
        for t in row['transitions']:
            t['sound_definition_exists']=t['sound_id']==0 or t['sound_id'] in definitions
    return {'member':name,'member_sha256':sha(raw),'member_bytes':len(raw),'swf_version':raw[3],'uncompressed_bytes':len(data),'frame_rate_fixed8_raw':rate_raw,'frame_rate_nominal':rate_raw/256,'declared_root_frames':declared_frames,'observed_root_showframes':frame-1,'header_and_observed_root_frame_counts_equal':declared_frames==frame-1,'sound_definitions':[v[0] for k,v in sorted(definitions.items())],'start_sound_controls':event_controls,'start_sound2_tag_count':sum(t[0]==89 for t in tags),'button_sound_controls':button_controls,'root_stream_heads':stream_heads,'root_stream_block_count':len(blocks),'root_stream_first_frame':blocks[0]['frame'],'root_stream_last_frame':blocks[-1]['frame'],'root_stream_sample_count_sum':sum(b['sample_count'] for b in blocks),'root_stream_seek_min':min(b['seek_samples'] for b in blocks),'root_stream_seek_max':max(b['seek_samples'] for b in blocks),'root_stream_payload_bytes':len(joined),'root_stream_payload_sha256':sha(joined),'stream_payload_equals_define_sound_1_mp3':joined==payload,'first_payload_difference_offset':mismatch,'stream_first_seek_equals_header_latency':blocks[0]['seek_samples']==stream_heads[0]['latency_seek'],'stream_first_seek_equals_event_seek':blocks[0]['seek_samples']==resource['seek_samples'],'blocks':blocks,'scope':'Static file structure only; root frames not call times; no actions executed or runtime/speaker/custody/carrier authentication'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive');p.add_argument('--helper',type=Path,default=Path(__file__).resolve().parent.parent/'telephone-court-audio-resources-2026-10-29/reproduce_resources.py');args=p.parse_args()
    helperbytes=args.helper.read_bytes()
    if sha(helperbytes)!=HELPER_SHA:raise ValueError('Pinned existing helper differs')
    spec=importlib.util.spec_from_file_location('pinned_passive_helper',args.helper);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    tests=controls();archive=Path(args.archive)
    if sha(archive.read_bytes())!=ARCHIVE_SHA:raise ValueError('Archive differs')
    result={'archive_url':'https://coop.vaed.uscourts.gov/moussaoui/flights.zip','archive_sha256':ARCHIVE_SHA,'helper_sha256':HELPER_SHA,'script_sha256':sha(Path(__file__).read_bytes()),'parser_controls':tests,'results':[]}
    with zipfile.ZipFile(archive) as z:
        for name in MEMBERS:
            if z.getinfo(name).file_size>MAX_BYTES:raise ValueError('Member exceeds bound')
            result['results'].append(analyze(z.read(name),name,helper))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

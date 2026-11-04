"""Read native QuickTime mapping fields, without media decoding or source writes.

File offsets/sample indexes are zero-based. Native chunk/description/reference IDs
are one-based. Time intersections are exact half-open interval arithmetic only;
they are not a decoder/presentation simulation.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import argparse,csv,hashlib,json,struct,sys
from native_tables import inspect,require,InvalidTable,controls as base_controls


def full(data):
    require(len(data)>=4,'truncated full atom prefix')
    require(data[0]==0,'unsupported nonzero atom version')
    return dict(version=data[0],flags=int.from_bytes(data[1:4],'big'))


def time_header(data,offset):
    out=full(data);require(len(data)>=20,'truncated time header')
    scale,duration=struct.unpack_from('>II',data,12)
    require(scale>0,'zero timescale')
    out.update(time_scale=scale,duration=duration,time_scale_byte_offset=offset+12,
               duration_byte_offset=offset+16,duration_seconds_exact=str(Fraction(duration,scale)))
    return out


def counted(data,width):
    out=full(data);require(len(data)>=8,'truncated count')
    count=struct.unpack_from('>I',data,4)[0]
    require(len(data)==8+count*width,'counted table length mismatch')
    out['entry_count']=count
    return out


def edits(data,offset):
    out=counted(data,12);rows=[]
    for i in range(out['entry_count']):
        duration,media_time,rate=struct.unpack_from('>Iii',data,8+i*12)
        rows.append(dict(index=i,byte_offset=offset+8+i*12,track_duration=duration,
                         media_time=media_time,media_rate_raw=rate,
                         media_rate_exact=str(Fraction(rate,65536)),empty_edit=media_time==-1,
                         positive_rate=rate>0))
    out['entries']=rows;return out


def chunks(data,offset):
    out=counted(data,12);rows=[]
    previous=0
    for i in range(out['entry_count']):
        first,samples,desc=struct.unpack_from('>III',data,8+i*12)
        require(first>previous and samples>0 and desc>0,'invalid sample-to-chunk run')
        rows.append(dict(index=i,byte_offset=offset+8+i*12,first_chunk=first,
                         samples_per_chunk=samples,sample_description_id=desc))
        previous=first
    require(not rows or rows[0]['first_chunk']==1,'first chunk must be one')
    out['entries']=rows;return out


def offsets(data,offset):
    out=counted(data,4)
    out['entries']=[dict(chunk=i+1,byte_offset=offset+8+i*4,
                        file_offset=struct.unpack_from('>I',data,8+i*4)[0])
                    for i in range(out['entry_count'])]
    return out


def descriptions(data,offset):
    out=full(data);require(len(data)>=8,'truncated descriptions')
    n=struct.unpack_from('>I',data,4)[0];cursor=8;rows=[]
    for i in range(n):
        require(cursor+16<=len(data),'truncated description entry')
        size,kind=struct.unpack_from('>I4s',data,cursor)
        require(size>=16 and cursor+size<=len(data),'description size out of bounds')
        reference=struct.unpack_from('>H',data,cursor+14)[0]
        rows.append(dict(id=i+1,byte_offset=offset+cursor,size=size,
                         format=kind.decode('latin1'),data_reference_index=reference,
                         data_reference_index_byte_offset=offset+cursor+14))
        cursor+=size
    require(cursor==len(data),'description entries do not fill atom')
    out.update(entry_count=n,entries=rows);return out


def references(data,offset):
    out=full(data);require(len(data)>=8,'truncated references')
    n=struct.unpack_from('>I',data,4)[0];cursor=8;rows=[]
    for i in range(n):
        require(cursor+12<=len(data),'truncated reference entry')
        size,kind=struct.unpack_from('>I4s',data,cursor)
        require(size>=12 and cursor+size<=len(data),'reference size out of bounds')
        version=data[cursor+8];flags=int.from_bytes(data[cursor+9:cursor+12],'big')
        rows.append(dict(id=i+1,byte_offset=offset+cursor,size=size,
                         type=kind.decode('latin1'),version=version,flags=flags,
                         self_reference_flag=bool(flags&1),flags_byte_offset=offset+cursor+9,
                         opaque_reference_data_bytes=size-12))
        cursor+=size
    require(cursor==len(data),'reference entries do not fill atom')
    out.update(entry_count=n,entries=rows);return out


def map_samples(runs,chunk_offsets,sizes,mdat,file_size):
    rows=[];index=0;attempted=0;chunk_rows=[]
    require(not runs or runs[-1]['first_chunk']<=len(chunk_offsets),'run begins past last chunk')
    for n,run in enumerate(runs):
        stop=runs[n+1]['first_chunk'] if n+1<len(runs) else len(chunk_offsets)+1
        for chunk in range(run['first_chunk'],stop):
            pos=chunk_offsets[chunk-1]['file_offset'];first_index=index
            attempted+=run['samples_per_chunk']
            for j in range(run['samples_per_chunk']):
                if index>=len(sizes):break
                size=sizes[index];end=pos+size
                rows.append(dict(sample_index=index,chunk=chunk,file_offset=pos,size=size,
                                 end_exclusive=end,sample_description_id=run['sample_description_id'],
                                 inside_file=0<=pos<=end<=file_size,
                                 inside_mdat=any(lo<=pos<=end<=hi for lo,hi in mdat)))
                index+=1;pos=end
            chunk_rows.append(dict(chunk=chunk,first_sample_index=first_index,
                                   mapped_samples=index-first_index,declared_samples=run['samples_per_chunk'],
                                   file_offset=chunk_offsets[chunk-1]['file_offset'],end_exclusive=pos))
    ordered=sorted(rows,key=lambda x:(x['file_offset'],x['end_exclusive']))
    overlaps=[];furthest=None
    for row in ordered:
        if furthest is not None and row['file_offset']<furthest['end_exclusive']:
            overlaps.append([furthest['sample_index'],row['sample_index']])
        if furthest is None or row['end_exclusive']>furthest['end_exclusive']:furthest=row
    summary=dict(size_table_count=len(sizes),chunk_mapping_declared_samples=attempted,
                 mapped_samples=len(rows),unmapped_size_indexes=list(range(index,len(sizes))),
                 excess_declared_samples=max(0,attempted-len(sizes)),
                 outside_file_indexes=[x['sample_index'] for x in rows if not x['inside_file']],
                 outside_mdat_indexes=[x['sample_index'] for x in rows if not x['inside_mdat']],
                 overlapping_sample_index_pairs=overlaps,
                 ordered_file_offsets=all(a['file_offset']<=b['file_offset'] for a,b in zip(rows,rows[1:])),
                 first_samples=rows[:5],last_samples=rows[-5:],first_chunks=chunk_rows[:3],last_chunks=chunk_rows[-3:])
    return summary,rows


def intersections(edit_rows,movie_scale,media_scale,time_runs):
    intervals=[];start=0
    for row in time_runs:
        for j in range(row['sample_count']):
            intervals.append((start,start+row['sample_delta']));start+=row['sample_delta']
    result=[]
    for edit in edit_rows:
        r=dict(edit)
        if edit['empty_edit'] or not edit['positive_rate']:
            r['arithmetic_performed']=False;result.append(r);continue
        lo=Fraction(edit['media_time'])
        hi=lo+Fraction(edit['track_duration']*media_scale,movie_scale)*Fraction(edit['media_rate_raw'],65536)
        full_count=0;partial=[];outside=[]
        for i,(a,b) in enumerate(intervals):
            if lo<=a and b<=hi:full_count+=1
            elif a<hi and b>lo:partial.append(i)
            else:outside.append(i)
        r.update(arithmetic_performed=True,media_interval_start_exact=str(lo),
                 media_interval_end_exact=str(hi),track_seconds_exact=str(Fraction(edit['track_duration'],movie_scale)),
                 nominal_sample_intervals_fully_inside=full_count,
                 nominal_sample_intervals_partial_indexes=partial,
                 nominal_sample_intervals_outside_indexes=outside,
                 interpretation='Exact half-open interval geometry, not actual decoder selection or proof of historical editing')
        result.append(r)
    return result


def controls():
    result=base_controls()
    def good(name,fn,test):
        require(test(fn()),name+' wrong result');result.append(dict(name=name,passed=True,expected='specified readout or reported mismatch'))
    def bad(name,fn):
        try:fn()
        except InvalidTable as e:result.append(dict(name=name,passed=True,expected='reject malformed input',error=str(e)))
        else:raise AssertionError(name+' accepted')
    good('header scale/duration offsets',lambda:time_header(b'\0'*12+struct.pack('>II',600,1200),100),lambda r:r['time_scale_byte_offset']==112 and r['duration_seconds_exact']=='2')
    bad('zero timescale rejected',lambda:time_header(b'\0'*20,0))
    bad('nonzero edit version not guessed',lambda:edits(b'\1\0\0\0'+struct.pack('>I',0),0))
    good('signed empty edit and fractional rate retained',lambda:edits(b'\0'*4+struct.pack('>IIii',1,600,-1,32768),40),lambda r:r['entries'][0]['empty_edit'] and r['entries'][0]['media_rate_exact']=='1/2')
    bad('truncated edit entries rejected',lambda:edits(b'\0'*4+struct.pack('>II',1,600),0))
    bad('nonmonotone first chunk rejected',lambda:chunks(b'\0'*4+struct.pack('>IIIIIII',2,1,2,1,1,3,1),0))
    good('chunk offsets are absolute values',lambda:offsets(b'\0'*4+struct.pack('>III',2,100,200),20),lambda r:r['entries'][1]['file_offset']==200 and r['entries'][1]['byte_offset']==32)
    bad('overclaimed offset count rejected',lambda:offsets(b'\0'*4+struct.pack('>II',2,100),0))
    runs=[dict(first_chunk=1,samples_per_chunk=2,sample_description_id=1)]
    offs=[dict(file_offset=100),dict(file_offset=200)]
    good('variable sizes map within each chunk',lambda:map_samples(runs,offs,[10,20,30,40],[(90,300)],300),lambda r:[x['file_offset'] for x in r[1]]==[100,110,200,230])
    good('missing size entries reported, not normalized',lambda:map_samples(runs,offs,[10,20,30],[(90,300)],300),lambda r:r[0]['excess_declared_samples']==1)
    good('unmapped sizes reported, not discarded',lambda:map_samples(runs,offs,[10,20,30,40,50],[(90,300)],300),lambda r:r[0]['unmapped_size_indexes']==[4])
    good('out-of-media address reported',lambda:map_samples(runs,offs,[10,20,30,40],[(90,150)],300),lambda r:r[0]['outside_mdat_indexes']==[2,3])
    good('overlapping addresses reported',lambda:map_samples(runs,[dict(file_offset=100),dict(file_offset=110)],[10,20,30,40],[(90,300)],300),lambda r:len(r[0]['overlapping_sample_index_pairs'])>0)
    good('edit interval boundary arithmetic',lambda:intersections([dict(empty_edit=False,positive_rate=True,media_time=1,track_duration=2,media_rate_raw=65536)],1,2,[dict(sample_count=3,sample_delta=2)]),lambda r:r[0]['nominal_sample_intervals_fully_inside']==1 and r[0]['nominal_sample_intervals_partial_indexes']==[0,2])
    body=b'\0'*4+struct.pack('>I',1)+struct.pack('>I4s',16,b'cvid')+b'\0'*6+struct.pack('>H',1)
    good('description reference index locator',lambda:descriptions(body,100),lambda r:r['entries'][0]['data_reference_index']==1 and r['entries'][0]['data_reference_index_byte_offset']==122)
    body=b'\0'*4+struct.pack('>I',1)+struct.pack('>I4sI',12,b'alis',1)
    good('self-reference flag, no opaque path exposed',lambda:references(body,100),lambda r:r['entries'][0]['self_reference_flag'] and r['entries'][0]['opaque_reference_data_bytes']==0)
    bad('reference size bounds rejected',lambda:references(b'\0'*4+struct.pack('>II4sI',1,50,b'alis',1),0))
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);p.add_argument('mapping_csv',type=Path)
    a=p.parse_args();tests=controls();before=a.source.stat();started=datetime.now(timezone.utc).isoformat()
    digest=hashlib.sha256()
    with a.source.open('rb') as f:
        while block:=f.read(8*1024*1024):digest.update(block)
        base=inspect(f,before.st_size)
        def read_atom(atom):
            length=atom['size']-atom['header_bytes'];require(length<8*1024*1024,'metadata payload cap')
            f.seek(atom['payload_offset']);data=f.read(length);require(len(data)==length,'short metadata read');return data
        def find(kind,track=None):
            rows=[x for x in base['atoms'] if x['type']==kind and (track is None or '/trak['+str(track)+']/' in x['path'])]
            require(len(rows)==1,'missing/ambiguous '+kind);return rows[0]
        atom=find('mvhd');movie=dict(atom=atom,fields=time_header(read_atom(atom),atom['payload_offset']))
        tracks=[]
        for track in (1,2):
            entry=dict(track=track)
            for kind,parse in [('mdhd',time_header),('elst',edits)]:
                atom=find(kind,track);entry[kind]=dict(atom=atom,fields=parse(read_atom(atom),atom['payload_offset']))
            tracks.append(entry)
        native={}
        for kind,parse in [('stsc',chunks),('stco',offsets),('stsd',descriptions),('dref',references)]:
            atom=find(kind,1);native[kind]=dict(atom=atom,fields=parse(read_atom(atom),atom['payload_offset']))
        atom=find('stsz',1);data=read_atom(atom);n=struct.unpack_from('>I',data,8)[0]
        require(struct.unpack_from('>I',data,4)[0]==0,'mapping expects checked variable-size first track')
        sizes=list(struct.unpack_from('>'+str(n)+'I',data,12))
    mdat=[(x['payload_offset'],x['end_exclusive']) for x in base['atoms'] if x['type']=='mdat']
    mapping,rows=map_samples(native['stsc']['fields']['entries'],native['stco']['fields']['entries'],sizes,mdat,before.st_size)
    descs={x['id']:x for x in native['stsd']['fields']['entries']}
    refs={x['id']:x for x in native['dref']['fields']['entries']}
    joins=[]
    for ident in sorted({x['sample_description_id'] for x in native['stsc']['fields']['entries']}):
        desc=descs.get(ident);ref=refs.get(desc['data_reference_index']) if desc else None
        joins.append(dict(sample_description_id=ident,description=desc,reference=ref,
                          resolved_to_self_reference=bool(ref and ref['self_reference_flag'])))
    timing=[x for x in base['tables'] if x['atom']['type']=='stts' and '/trak[1]/' in x['atom']['path']][0]['fields']
    nominal=intersections(tracks[0]['elst']['fields']['entries'],movie['fields']['time_scale'],tracks[0]['mdhd']['fields']['time_scale'],timing['entries'])
    after=a.source.stat();require((before.st_size,before.st_mtime_ns,before.st_ino)==(after.st_size,after.st_mtime_ns,after.st_ino),'source changed')
    columns=['sample_index','chunk','file_offset','size','end_exclusive','sample_description_id','inside_file','inside_mdat']
    with a.mapping_csv.open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
    result=dict(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),source_bytes=before.st_size,source_sha256=digest.hexdigest(),source_stat_unchanged=True,source_mode='rb',movie_header=movie,track_headers_and_edits=tracks,first_track_native_tables=native,sample_mapping=mapping,data_reference_joins=joins,nominal_edit_intersections=nominal,prior_native_time_table=timing,mdat_payload_extents=mdat,source_decoded=False,actual_decoder_selection_tested=False,audio_packet_mapping=False,all_media_payloads_examined_for_validity=False,controls=tests,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),base_parser_sha256=hashlib.sha256((Path(__file__).parent/'native_tables.py').read_bytes()).hexdigest(),mapping_csv_sha256=hashlib.sha256(a.mapping_csv.read_bytes()).hexdigest(),mapping_csv_bytes=a.mapping_csv.stat().st_size,python=sys.version)
    with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:result[k] for k in ['source_sha256','source_stat_unchanged','movie_header','track_headers_and_edits','sample_mapping','data_reference_joins','nominal_edit_intersections','mapping_csv_bytes']},indent=2))
    print('Controls passed:',len(tests))

if __name__=='__main__':main()

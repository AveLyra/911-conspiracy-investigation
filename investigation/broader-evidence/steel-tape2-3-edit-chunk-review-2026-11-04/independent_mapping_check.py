"""Independent integer reads and closed-form check; no parser import or decoding."""
from pathlib import Path
from fractions import Fraction
from datetime import datetime,timezone
import argparse,csv,hashlib,json
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('results',type=Path);p.add_argument('mapping',type=Path);p.add_argument('output',type=Path)
a=p.parse_args();before=a.source.stat()
with a.source.open('rb') as f:
 def integer(offset,signed=False):
  f.seek(offset);b=f.read(4);assert len(b)==4;return int.from_bytes(b,'big',signed=signed)
 ns=integer(815639049);sizes=[integer(815639053+4*i) for i in range(ns)]
 nr=integer(815620717);runs=[tuple(integer(815620721+12*i+4*j) for j in range(3)) for i in range(nr)]
 nc=integer(815685493);starts=[integer(815685497+4*i) for i in range(nc)]
 movie_scale=integer(815620060);movie_duration=integer(815620064)
 media_scale=integer(815620380);media_duration=integer(815620384)
 edit_duration=integer(815620340);media_time=integer(815620344,True);rate_raw=integer(815620348,True)
 f.seek(815620609);data_reference=int.from_bytes(f.read(2),'big')
 f.seek(815620568);reference_flags=int.from_bytes(f.read(3),'big')
weighted=sum((runs[i+1][0] if i+1<len(runs) else nc+1)-row[0] for i,row in enumerate(runs))
# Independently expand runs via a chunk-number lookup rather than mapper run loops.
per_chunk={}
for i,(first,n,desc) in enumerate(runs):
 stop=runs[i+1][0] if i+1<len(runs) else nc+1
 for chunk in range(first,stop):per_chunk[chunk]=(n,desc)
count=sum(x[0] for x in per_chunk.values())
expected=[];sample=0
for chunk in range(1,nc+1):
 n,desc=per_chunk[chunk];offset=starts[chunk-1]
 for j in range(n):
  expected.append((sample,chunk,offset,sizes[sample],offset+sizes[sample],desc))
  offset+=sizes[sample];sample+=1
with a.mapping.open(newline='') as f:
 rows=list(csv.DictReader(f))
assert len(rows)==len(expected)==ns==count==11607 and nc==1550 and nr==1526
for actual,want in zip(rows,expected):
 assert tuple(int(actual[k]) for k in ['sample_index','chunk','file_offset','size','end_exclusive','sample_description_id'])==want
 assert 48<=want[2]<want[4]<=815620032
assert all(x[4]<=y[2] for x,y in zip(expected,expected[1:]))
end=Fraction(media_time)+Fraction(edit_duration*media_scale,movie_scale)*Fraction(rate_raw,65536)
# This source's previously checked timing run is constant200 units/sample.
fully_inside=int(end//200)
partial=int(end%200!=0)
outside=ns-fully_inside-partial
assert fully_inside==11605 and partial==1 and outside==1
assert media_duration==ns*200==2321400 and movie_duration==edit_duration==464704
assert movie_scale==600 and media_scale==2997 and media_time==0 and rate_raw==65536
assert data_reference==1 and reference_flags==1
r=json.loads(a.results.read_text());assert r['source_sha256']=='4beeea4b0e66c5fcaf68f5336ea4b76518f89c6d1cfbba6833915e359f8a4bcb'
assert r['mapping_csv_sha256']==hashlib.sha256(a.mapping.read_bytes()).hexdigest()
after=a.source.stat();assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns)
out={'utc':datetime.now(timezone.utc).isoformat(),'method':'Separate int.from_bytes reads, chunk-number lookup, full CSV row equality and closed-form interval arithmetic; no import of either parser','raw_runs':nr,'chunks':nc,'sample_count':ns,'all_mapping_rows_match':True,'all_video_ranges_in_file_mdat':True,'video_ranges_do_not_overlap':True,'first_row':expected[0],'last_row':expected[-1],'movie_scale':movie_scale,'movie_duration':movie_duration,'media_scale':media_scale,'media_duration':media_duration,'edit_duration':edit_duration,'edit_media_time':media_time,'edit_rate_raw':rate_raw,'nominal_end_media_units_exact':str(end),'nominal_fully_inside':fully_inside,'nominal_partial':partial,'nominal_outside':outside,'self_reference_index':data_reference,'self_reference_flags':reference_flags,'source_stat_unchanged':True,'decoder_selection_tested':False}
with a.output.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))

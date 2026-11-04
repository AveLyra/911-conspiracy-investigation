"""Check complete native-reader logs against their summaries and prior size map."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import argparse,csv,hashlib,json
p=argparse.ArgumentParser();p.add_argument('run_directory',type=Path);p.add_argument('native_map_csv',type=Path);p.add_argument('new_output',type=Path);a=p.parse_args()
names=['positive-nil','positive-argb','negative-nil','source-nil','source-argb']
results={};checks=[]
def check(name,value):
 checks.append(dict(name=name,passed=bool(value)))
 if not value:raise AssertionError(name)
for name in names:
 path=a.run_directory/(name+'-RAW-LOCAL.json');raw=path.read_bytes();x=json.loads(raw);rows=x.get('sample_rows',[])
 if 'buffer_count' in x:
  check(name+' buffer total',len(rows)==x['buffer_count'])
  check(name+' sample sum',sum(row[1] for row in rows)==x['sample_count_sum'])
  check(name+' zero sample total',sum(row[1]==0 for row in rows)==x['zero_sample_buffer_count'])
  check(name+' image total',sum(bool(row[7]) for row in rows)==x['image_buffer_count'])
  check(name+' buffer format totals',dict(Counter(row[6] for row in rows))==x['observed_buffer_formats'])
  check(name+' sequential buffer index',all(row[0]==i for i,row in enumerate(rows)))
 results[name]={'raw_file':path.name,'raw_bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),'metadata':{k:v for k,v in x.items() if k!='sample_rows'},'first_rows':rows[:3],'last_rows':rows[-5:],'zero_sample_rows':[row for row in rows if row[1]==0]}
check('positive storage control three samples',results['positive-nil']['metadata']['counts_complete'] and results['positive-nil']['metadata']['sample_count_sum']==3)
check('positive decode control three images',results['positive-argb']['metadata']['counts_complete'] and results['positive-argb']['metadata']['image_buffer_count']==3)
check('negative control rejected',results['negative-nil']['metadata']['counts_complete'] is False and results['negative-nil']['metadata'].get('caught_error') is not None)
with a.native_map_csv.open(newline='') as f:native=list(csv.DictReader(f))
source=json.loads((a.run_directory/'source-nil-RAW-LOCAL.json').read_text());media=[row for row in source['sample_rows'] if row[1]>0]
check('source storage reading complete',source['counts_complete'] is True)
check('one sample in each returned media buffer',all(row[1]==1 for row in media))
check('returned positive rows fit native map',len(media)<=len(native))
check('ordered numeric size correspondence',all(row[5]==int(native[i]['size']) for i,row in enumerate(media)))
check('ordered nominal PTS correspondence',all(row[2]==[i*200,2997,1,0] for i,row in enumerate(media)))
check('returned full nominal durations retained',all(row[4]==[200,2997,1,0] for row in media))
check('negative source decode not promoted to complete',results['source-argb']['metadata']['counts_complete'] is False and results['source-argb']['metadata']['reader_status']=='failed')
end=Fraction(464704*2997,600);last=media[-1];packet_end=Fraction(last[2][0])+Fraction(last[4][0]);difference=packet_end-end
out={'checked_runs':results,'checks':checks,'all_checks_passed':all(c['passed'] for c in checks),'native_map_reference':{'bytes':a.native_map_csv.stat().st_size,'sha256':hashlib.sha256(a.native_map_csv.read_bytes()).hexdigest(),'rows':len(native)},'source_numeric_correspondence':{'positive_sample_rows':len(media),'native_declared_size_rows':len(native),'compared_native_indexes':[0,len(media)-1],'remaining_native_indexes':list(range(len(media),len(native))),'all_returned_sizes_match_ordered_prefix':True,'all_PTS_match_nominal_ordered_prefix':True,'payload_byte_identity_tested':False,'source_packet_payloads_hashed':False,'all_returned_nominal_durations':200,'last_positive_row':last,'native_edit_endpoint_media_units_exact':str(end),'last_returned_nominal_end_media_units_exact':str(packet_end),'overhang_media_units_exact':str(difference),'overhang_seconds_exact':str(difference/2997),'scope':'Ordered numeric correspondence, not compressed-payload identity, actual presentation or historical-cause adjudication'},'independent_source_storage_count_complete':True,'independent_source_decoded_count_complete':False,'source_decode_error':results['source-argb']['metadata']['reader_error'],'prior_counts_and_failed_extraction_unchanged':True}
with a.new_output.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'checks_passed':len(checks),'source_numeric_correspondence':out['source_numeric_correspondence'],'independent_source_decoded_count_complete':False},indent=2))

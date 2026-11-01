from pathlib import Path
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--source-map');a=p.parse_args();r=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest();m=json.loads((r/'MANIFEST.json').read_text())
for f in m['files']:
 b=(r/f['name']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['name']
checked=[]
if a.source_map:
 sm=json.loads(Path(a.source_map).read_text())
 for f in json.loads((r/'SOURCE-PINS.json').read_text())['inputs']:
  b=Path(sm[f['id']]).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['id'];checked.append(f['id'])
o=json.loads((r/'OBSERVATIONS.json').read_text());rows=o['production_email']['rows']
hours=sum(x['printed_hours'] for x in rows);assert hours==o['production_email']['stated_total_hours']==30
assert o['production_email']['postscript']['hours']==6 and o['production_email']['relationship_of_postscript_to_total'].startswith('not explicit')
c=o['certification'];assert c['fax_cover_stated_pages_including_cover']==4 and c['acquired_PDF_pages']==8
joined=o['cross_record_comparison'];assert joined['production_report_tapes']==2 and sum(joined['landline_explicit_counts'])==3 and joined['landline_OS_count'] is None
new=[x for x in json.loads((r/'SOURCE-PINS.json').read_text())['inputs'] if x['id'] in ['A90-74','A90-98','A90-99']]
assert sum(x['physical_pages'] for x in new)==15
print(json.dumps({'status':'passed','manifest_files':len(m['files']),'source_inputs_checked':checked,'new_source_pages':15,'printed_category_hour_sum':hours,'stated_total_hours':30,'postscript_hours_kept_separate':6,'verified_combined_hours':None,'fax_cover_count':4,'released_PDF_count':8,'reported_production_tapes':2,'other_memo_explicit_count_sum':3,'other_memo_OS_count':None,'same_batch_join':False,'scope':'Declared byte identity and arithmetic of manually read printed fields only; not actual collection/production, native audio, clocks, receipt, applicability/compliance, historical cause or substantive goal acceptance.'}))

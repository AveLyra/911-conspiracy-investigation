#!/usr/bin/env python3
"""Post-freeze exhaustive comparison; saved products and synthetic bytes only."""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re
import resource
import sys
import tempfile
import time

BASE=Path(__file__).resolve().parent
PINS={
 'independent_scan.py':'8c5aee84f2b4b96d4149cd8469902531a31f8d47c59cb2f4f7037657eddfe3ff',
 'independent-controls01.json':'3c1797ca32ae37c40361d08ffc3a6c9e9c8e673fa38c2fdf94f8faa0e385ae0a',
 'independent-scan01.json':'76a43ff38376979140608c5d368a93ae40bd7c9d55b33a3ec1e87069a6ce5bc7',
 'search_definitions.py':'3bdbefb2c324671293991070aa5991033a163f6ff13359ab1f276b115c72968a',
 'root-01.json':'b85f806373294697eb1dc15b2673c5d8d34f81890658c0a76937fec9a55f9b06',
 'root-02.json':'e5eea54090c3215534e6c5f4ae776680b673769353fa12240ba2699368f91a49',
 'verify_saved_coverage.py':'aa229f6e83cba5b2a214844ad744264beb9f936590299431a8cdc579187ca2ec',
 'coverage-check01.json':'a71466540ea58ba15e0309ccb2ca7e1cdf1179fc34b153d8c15cf6b50ccd9d5a',
 'PROTOCOL.md':'dfc4ecbf348066574c6d38b5b087272120f006d35bfb72a1920ff79c14189865',
 'SCAN-CONVENTIONS.md':'06d9f8921be5dd2994dcca74c56ca5104b3aa88be85048a34c1b476ea82c85be',
 '../CHARTER.md':'54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
 '../c79-casea-spring-audit/casea-root01.json':'27e8905727fa8462724db70f6ce11f411391170a4a6636936491027eaba988a2',
 '../c79-casea-spring-audit/independent-definition-presence01.json':'7377187b71fe0fc10a5483ed80424499555270708d02a61d2d2a991c14a939c7',
 '../thermal-transfer-crosswalk/run01.json':'4754a59f0628a3ed91e913ce9aa5215254a4e476dcd17d9ee32e964eda2f8117',
}
ENCODINGS={'ascii':'ascii','utf-16le':'utf-16-le','utf-16be':'utf-16-be'}
BODY_KEYS={'all_nul','bytes','eof','initial_utf8_bom','lines','literal_hits','nonascii_bytes','nul_bytes','sha256'}
class Failure(Exception):pass
def need(ok,code):
 if not ok:raise Failure(code)
def sha(path):
 with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def schema(obj,keys):need(type(obj) is dict and set(obj)==set(keys),'SCHEMA')
def check_pins():
 out={name:sha(BASE/name) for name in PINS};need(out==PINS,'INPUT_PIN')
 out['consumer']=sha(Path(__file__));return out
def diff(a,b):
 out={'equal':True,'leaves':0,'containers':0,'mismatch_count':0,'mismatches':[]}
 def bad(path,x,y):
  out['equal']=False;out['mismatch_count']+=1
  if len(out['mismatches'])<50:out['mismatches'].append({'path':path,'left_sha256':digest(x),'right_sha256':digest(y)})
 def walk(x,y,path):
  if type(x) is dict and type(y) is dict:
   out['containers']+=1
   if set(x)!=set(y):bad(path+'/keys',sorted(x),sorted(y))
   for key in sorted(set(x)&set(y)):walk(x[key],y[key],path+'/'+str(key))
  elif type(x) is list and type(y) is list:
   out['containers']+=1
   if len(x)!=len(y):bad(path+'/length',len(x),len(y))
   for i,(xx,yy) in enumerate(zip(x,y)):walk(xx,yy,path+'/'+str(i))
  else:
   out['leaves']+=1
   numeric=type(x) in (int,float) and type(y) in (int,float)
   same=math.isfinite(x) and math.isfinite(y) and x==y if numeric else type(x) is type(y) and x==y
   if not same:bad(path,x,y)
 walk(a,b,'');out['left_sha256']=digest(a);out['right_sha256']=digest(b);return out

def common_body(scan):
 hits=[{'family':h['family'],'encoding':ENCODINGS[h['encoding']],
  'line':h['line'],'byte_column0':h['byte_column'],'byte_offset0':h['byte_offset'],
  'line_leading':h['line_leading'],'suffix_present':h['has_suffix']} for h in scan['hits']]
 return {'all_nul':scan['all_nul'],'bytes':scan['bytes_read'],'eof':scan['eof'],
  'initial_utf8_bom':scan['initial_utf8_bom'],'lines':scan['physical_lines'],
  'literal_hits':hits,'nonascii_bytes':scan['non_ascii_bytes'],
  'nul_bytes':scan['nul_bytes'],'sha256':scan['sha256']}
def own_records(own):
 bodies=own['bodies'];excluded=own['excluded']
 apdl=[r for r in bodies if r['kind']=='APDL'];sep=[r for r in bodies if r['kind']=='September']
 zipped=sorted([r for r in bodies if r['kind']=='ZIP']+excluded,key=lambda r:r['zip_ordinal'])
 need([r['zip_ordinal'] for r in zipped]==list(range(own['zip']['entry_count'])),'ZIP_ORDINAL_COVERAGE')
 need(len({r['alias'] for r in bodies+excluded})==len(bodies)+len(excluded),'OWN_ALIAS_UNIQUENESS')
 mapped=[];aliases=[]
 for ordinal,r in enumerate(apdl,1):
  need(r['alias']=='APDL'+str(ordinal) and r['name_sha256']==r['filename_sha256'],'APDL_ALIAS_SCOPE')
  mapped.append({'alias':f'APDL{ordinal:02d}','kind':'apdl','manifest_line':r['manifest_row'],
   'name_sha256':r['filename_sha256'],'body':common_body(r['scan'])})
  aliases.append(r['alias'])
 for r in zipped:
  ordinal=r['zip_ordinal']+1
  row={'alias':f'ZIP{ordinal:05d}','ordinal':ordinal,'name_sha256':r['name_sha256'],
   'declared_bytes':r['expected_bytes'],'declared_crc32':r['expected_crc32']}
  if 'scan' in r:
   row.update(kind='zip_body',manifest_line=r['manifest_row'],body=common_body(r['scan']),crc_eof_pass=r['crc_verified'])
   need(r['sha256_verified'] and r['scan']['sha256']==r['expected_sha256'] and
    r['scan']['crc32_actual']==r['expected_crc32'],'OWN_ZIP_VERIFICATION')
  else:
   need(r['reason'] in ('directory','PNG'),'EXCLUSION_REASON')
   need(r['bytes_read']==0 and r['crc_verified'] is False and r['sha256_verified'] is False,'EXCLUSION_FLAGS')
   row['kind']='directory_excluded' if r['reason']=='directory' else 'png_body_excluded'
   if r['reason']=='PNG':row['manifest_line']=r['manifest_row']
  mapped.append(row);aliases.append(r['alias'])
 for r in sep:
  need(r['alias']=='SRC'+str(r['source']),'SEPTEMBER_ALIAS')
  need(r['compressed_sha256']==r['compressed_after_sha256'] and r['gzip_crc_checked_by_reader'],'OWN_GZIP_VERIFICATION')
  need((r['scan']['bytes_read'],r['scan']['physical_lines'],r['scan']['sha256'])==
   (r['expected_bytes'],r['expected_lines'],r['expected_sha256']),'OWN_GZIP_EOF')
  mapped.append({'alias':r['alias'],'kind':'gzip_body','name_sha256':r['name_sha256'],
   'compressed_bytes':r['compressed_bytes'],'compressed_sha256':r['compressed_sha256'],
   'body':common_body(r['scan'])});aliases.append(r['alias'])
 need(len(mapped)==len(bodies)+len(excluded),'ALL_RECORD_COVERAGE')
 return mapped,aliases

def pinned_module(name):
 need(sha(BASE/name)==PINS[name],'MODULE_PIN')
 spec=importlib.util.spec_from_file_location('synthetic_'+name.replace('.','_'),BASE/name)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def controls():
 # Imports are post-freeze, for synthetic byte fixtures ONLY. No producer main,
 # manifest loader, historical function, raw stream or extraction is called.
 own=pinned_module('independent_scan.py');root=pinned_module('search_definitions.py')
 need(sha(BASE/'independent-controls01.json')==PINS['independent-controls01.json'],'FIXTURE_PIN')
 fixture_receipt=json.loads((BASE/'independent-controls01.json').read_text())
 rows=[]
 for f in fixture_receipt['controls']['fixtures']:
  raw=bytes.fromhex(f['input_hex']);fresh=own.body_scan(raw)
  need(fresh==f['result'],'OWN_SYNTHETIC_REPLAY')
  a=common_body(fresh);b=root.scan(io.BytesIO(raw),root.MEMBER_CAP);schema(b,BODY_KEYS)
  comparison=diff(a,b);need(comparison['equal'],'SYNTHETIC_CROSS_READER_MISMATCH')
  rows.append({'name':f['name'],'input_hex':f['input_hex'],'own_common':a,'root_common':b,'comparison':comparison})
 base={'records':[{'alias':'ZIP00002','kind':'zip_body','ordinal':2,'manifest_line':9,
  'name_sha256':'a'*64,'declared_bytes':3,'declared_crc32':19,'crc_eof_pass':True,
  'body':copy.deepcopy(rows[3]['root_common'])},
  {'alias':'ZIP00003','kind':'png_body_excluded','ordinal':3,'manifest_line':10,
   'name_sha256':'b'*64,'declared_bytes':2,'declared_crc32':20}]}
 variants=[]
 def mutate(name,fn):
  x=copy.deepcopy(base);fn(x);variants.append({'name':name,'mutated':x,'comparison':diff(base,x)})
 for key,value in [('alias','ZIP00004'),('kind','directory_excluded'),('ordinal',3),
  ('manifest_line',10),('name_sha256','c'*64),('declared_bytes',4),('declared_crc32',21),('crc_eof_pass',False)]:
  mutate('changed_'+key,lambda x,k=key,v=value:x['records'][0].__setitem__(k,v))
 for key,value in [('bytes',1),('lines',9),('sha256','d'*64),('nul_bytes',1),
  ('nonascii_bytes',1),('all_nul',True),('initial_utf8_bom',True),('eof',False)]:
  mutate('changed_body_'+key,lambda x,k=key,v=value:x['records'][0]['body'].__setitem__(k,v))
 for key,value in [('line',99),('byte_column0',100),('byte_offset0',100),
  ('encoding','utf-16-be'),('family','DEFINE_FUNCTION'),('line_leading',True),('suffix_present',True)]:
  mutate('changed_hit_'+key,lambda x,k=key,v=value:x['records'][0]['body']['literal_hits'][0].__setitem__(k,v))
 mutate('omitted_hit',lambda x:x['records'][0]['body']['literal_hits'].pop())
 mutate('reordered_hits',lambda x:x['records'][0]['body']['literal_hits'].reverse())
 mutate('missing_excluded',lambda x:x['records'].pop())
 mutate('duplicate_record',lambda x:x['records'].append(copy.deepcopy(x['records'][0])))
 mutate('reordered_records',lambda x:x['records'].reverse())
 mutate('false_became_zero',lambda x:x['records'][0]['body'].__setitem__('all_nul',0))
 need(all(not v['comparison']['equal'] for v in variants),'NEGATIVE_CONTROL_MISSED')
 with tempfile.TemporaryDirectory(prefix='curve-compare-control-') as folder:
  path=Path(folder)/'fixture';path.touch();before=sha(path)
  try:path.open('x')
  except FileExistsError:refused=True
  else:refused=False
  need(refused and sha(path)==before,'OUTPUT_REFUSAL_CONTROL')
 return {'passed':True,'cross_reader_fixture_count':len(rows),'cross_reader_fixtures':rows,
  'negative_count':len(variants),'negative_base':base,'negative_variants':variants,
  'create_only_refused':refused}

def calculate():
 read=lambda n:json.loads((BASE/n).read_text())
 own=read('independent-scan01.json');first=read('root-01.json');repeat=read('root-02.json');coverage=read('coverage-check01.json')
 need(all(x['status']=='PASS' for x in (own,first,repeat,coverage)),'RESULT_STATUS')
 need(own['code_sha256']==PINS['independent_scan.py'] and
  first['code_sha256']==repeat['code_sha256']==PINS['search_definitions.py'],'RECORDED_CODE_PIN')
 need(own['pins_before']==own['pins_after'],'OWN_INPUT_CHANGED')
 a,aliases=own_records(own);b=first['result']['records']
 schema(first['result'],{'archive_counts','body_count','june_read_bytes','limits','literal_hit_count','pins_after','pins_before','records'})
 need(len(a)==len(b),'RECORD_POPULATION')
 comparisons=[]
 for index,(x,y,alias) in enumerate(zip(a,b,aliases)):
  comparison=diff(x,y)
  comparisons.append({'index':index,'own_alias':alias,'root_alias':y['alias'],
   'kind':y['kind'],'comparison':comparison})
 z=own['zip'];expected_counts={'entries':z['entry_count'],'directories':z['directories'],
  'files':z['regular_entries'],'png_excluded':z['png_excluded'],
  'bodies_read':sum(x['kind']=='zip_body' for x in a)}
 summary={'archive_counts':diff(expected_counts,first['result']['archive_counts']),
  'june_read_bytes':diff(own['june_total_scanned_bytes'],first['result']['june_read_bytes']),
  'body_count':diff(len(own['bodies']),first['result']['body_count']),
  'literal_hit_count':diff(sum(len(r['scan']['hits']) for r in own['bodies']),first['result']['literal_hit_count'])}
 expected_root_pins={'ANSYS Thermal Data.zip':z['container_sha256'],
  'PROTOCOL.md':own['pins_before']['protocol'],'SCAN-CONVENTIONS.md':own['pins_before']['scan_conventions'],
  'casea-root01.json':own['pins_before']['prior_spring_source'],
  'independent-definition-presence01.json':own['pins_before']['prior_family_inventory'],
  'production-2025-06-05-file-manifest-sha256.csv':own['pins_before']['june_manifest']}
 summary['shared_pins_before']=diff(expected_root_pins,first['result']['pins_before'])
 summary['shared_pins_after']=diff(expected_root_pins,first['result']['pins_after'])
 # Reconstruct every aggregate in the independent result from its body rows.
 family_counts={e:{f:0 for f in ('DEFINE_CURVE','DEFINE_TABLE','DEFINE_FUNCTION')} for e in ENCODINGS}
 lead_counts=copy.deepcopy(family_counts)
 for r in own['bodies']:
  found=Counter((h['encoding'],h['family']) for h in r['scan']['hits'])
  leading=Counter((h['encoding'],h['family']) for h in r['scan']['hits'] if h['line_leading'])
  for e in ENCODINGS:
   for f in family_counts[e]:
    need(r['scan']['marker_counts'][e][f]==found[e,f] and r['scan']['line_leading_counts'][e][f]==leading[e,f],'OWN_BODY_HIT_COUNTS')
    family_counts[e][f]+=found[e,f];lead_counts[e][f]+=leading[e,f]
 summary['own_family_totals']=diff(family_counts,own['result']['marker_counts'])
 summary['own_leading_totals']=diff(lead_counts,own['result']['line_leading_counts'])
 own_totals={'all_nul_bodies':sum(r['scan']['all_nul'] for r in own['bodies']),
  'apdl_count':sum(r['kind']=='APDL' for r in own['bodies']),
  'bodies_with_hits':[r['alias'] for r in own['bodies'] if r['scan']['hits']],
  'body_count':len(own['bodies']),'bytes_scanned':sum(r['scan']['bytes_read'] for r in own['bodies']),
  'excluded_count':len(own['excluded']),'marker_counts':family_counts,'line_leading_counts':lead_counts,
  'non_ascii_bodies':sum(r['scan']['non_ascii_bytes']>0 for r in own['bodies']),
  'nul_bodies':sum(r['scan']['nul_bytes']>0 for r in own['bodies']),
  'physical_lines':sum(r['scan']['physical_lines'] for r in own['bodies']),
  'september_count':sum(r['kind']=='September' for r in own['bodies']),
  'zip_body_count':sum(r['kind']=='ZIP' for r in own['bodies'])}
 schema(own['result'],set(own_totals)|{'scope'})
 summary['all_own_numeric_aggregates']=diff(own_totals,{k:own['result'][k] for k in own_totals})
 expected_coverage={'complete_root_result_repeat':True,'june_bodies_reconciled':25365,
  'june_fields_per_body':6,'september_bodies_reconciled':3,
  'all_bodies_eof':all(r['scan']['eof'] is True for r in own['bodies']),
  'literal_hits':sum(len(r['scan']['hits']) for r in own['bodies']),
  'all_nul_bodies':[{'alias':x['alias'],'bytes':x['body']['bytes']} for x in a if 'body' in x and x['body']['all_nul']],
  'read_bytes':sum(r['scan']['bytes_read'] for r in own['bodies']),
  'physical_lines':sum(r['scan']['physical_lines'] for r in own['bodies'])}
 schema(coverage['result'],set(expected_coverage)|{'limits'})
 summary['saved_coverage_checks']=diff(expected_coverage,{k:coverage['result'][k] for k in expected_coverage})
 need(coverage['code_sha256']==PINS['verify_saved_coverage.py'],'COVERAGE_CODE_PIN')
 need(all(PINS[k]==v for k,v in coverage['pins'].items()),'COVERAGE_INPUT_PINS')
 full_repeat=diff(first['result'],repeat['result'])
 meta_keys={'code_sha256','command','controls','elapsed_seconds','maxrss_bytes_darwin','python','result','status'}
 schema(first,meta_keys);schema(repeat,meta_keys)
 repeat_meta={k:diff(first[k],repeat[k]) for k in sorted(meta_keys-{'result','command','elapsed_seconds','maxrss_bytes_darwin'})}
 need(first['command'][-2:]==['--output','root-01.json'] and repeat['command'][-2:]==['--output','root-02.json'],'ROOT_COMMAND_OUTPUT')
 repeat_meta['command_prefix']=diff(first['command'][:-1],repeat['command'][:-1])
 passed=all(r['comparison']['equal'] for r in comparisons) and all(v['equal'] for v in summary.values()) and full_repeat['equal'] and all(v['equal'] for v in repeat_meta.values())
 return {'passed':passed,'per_record':comparisons,'summary_comparisons':summary,
  'full_root_result_repeat':full_repeat,'root_repeat_metadata':repeat_meta,
  'root_runtime_metadata':[{k:r[k] for k in ('command','python','elapsed_seconds','maxrss_bytes_darwin')} for r in (first,repeat)],
  'counts':{'all_records':len(a),'scanned_bodies':len(own['bodies']),'excluded':len(own['excluded']),
   'record_leaves_compared':sum(r['comparison']['leaves'] for r in comparisons),
   'record_mismatches':sum(r['comparison']['mismatch_count'] for r in comparisons),
   'bytes_scanned':expected_coverage['read_bytes'],'physical_lines':expected_coverage['physical_lines']},
  'limits':[
   'Original independent source/code froze before root inspection. Adapter is post-freeze; producer imports here are used only on preserved synthetic fixture bytes.',
   'ZIP ordinals are translated zero-based independent to one-based root; APDL and ZIP alias padding is normalized explicitly, with both aliases retained per record.',
   'Independent-only fields include computed CRC numbers, LF/max-line counts, UTF16 BOM flags, ZIP compression metadata, manifest/name-hash extras and explicit expected September EOF pins. These do not acquire nonexistent root counterparts.',
   'Root independently verifies ZIP CRC via complete ZipFile reads but retains only expected CRC and success, not a separate computed CRC number. Excluded PNG/directory bodies were not scanned.',
   'Root did not enforce original September uncompressed byte/line/hash pins during source scan; the separately pinned saved coverage check and this independent source reconciliation establish agreement afterward.',
   'Root rejects duplicate ZIP names; independent preserves and opens each ordinal. Pinned archive contains none. Independent APDL cap is remaining June budget; root uses4MiB, above all three pinned sizes.',
   'Resource limits are checkpoints, not OS hard limits. Root used Python3.14, independent source used3.12; recorded equality is for these actual runs.',
   'Negative literal matching is not general-language evaluation, complete constitutive provenance, historical execution, support-capacity or collapse-cause evidence.']}

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args()
 need(re.fullmatch(r'independent-comparison(?:-root)?[0-9]+\.json',args.out) is not None,'OUTPUT_SCOPE')
 target=BASE/args.out
 with target.open('x') as destination:
  began=time.monotonic();receipt={'status':'FAIL','command':sys.argv}
  try:
   receipt['controls']=controls();receipt['pins_before']=check_pins()
   receipt['result']=calculate();receipt['pins_after']=check_pins()
   need(receipt['pins_before']==receipt['pins_after'],'INPUT_CHANGED')
   receipt['status']='PASS' if receipt['result']['passed'] else 'FAIL'
  except Exception as exc:
   receipt['failure']={'class':type(exc).__name__}
   if isinstance(exc,Failure):receipt['failure']['code']=str(exc)
  receipt.update(elapsed_seconds=time.monotonic()-began,
   peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
   runtime={'python':sys.version,'executable':sys.executable},code_sha256=sha(Path(__file__)))
  json.dump(receipt,destination,sort_keys=True,indent=2,allow_nan=False);destination.write('\n')
 print(json.dumps({'status':receipt['status'],'file':target.name,'sha256':sha(target),
  'counts':receipt.get('result',{}).get('counts'),'failure':receipt.get('failure')}))
 return 0 if receipt['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

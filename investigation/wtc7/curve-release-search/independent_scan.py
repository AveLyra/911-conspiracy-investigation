#!/usr/bin/env python3
"""Independent, bounded literal-family scan. Numeric/hash metadata only.

No imported investigation reader; standard-library implementation. Reuses the
author's general pin/create-only/EOF discipline, not root scanner code. Does not
execute inputs, decode arbitrary source text, extract member paths, or parse laws.
"""
import argparse
from collections import Counter,defaultdict
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path,PurePosixPath
import re
import resource
import struct
import sys
import tempfile
import time
import warnings
import zipfile
import zlib

BASE=Path(__file__).resolve().parent
JUNE=Path('/Users/admin/docs/911/exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539')
SEPTEMBER=Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
MANIFEST=Path('/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv')
AUDIT=Path('/Users/admin/docs/911/intake/audits/2026-09-11-supplement-integrity.json')
PINS={
 BASE/'PROTOCOL.md':'dfc4ecbf348066574c6d38b5b087272120f006d35bfb72a1920ff79c14189865',
 BASE/'SCAN-CONVENTIONS.md':'06d9f8921be5dd2994dcca74c56ca5104b3aa88be85048a34c1b476ea82c85be',
 BASE.parent/'CHARTER.md':'54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
 BASE.parent/'c79-casea-spring-audit/casea-root01.json':'27e8905727fa8462724db70f6ce11f411391170a4a6636936491027eaba988a2',
 BASE.parent/'c79-casea-spring-audit/independent-definition-presence01.json':'7377187b71fe0fc10a5483ed80424499555270708d02a61d2d2a991c14a939c7',
 MANIFEST:'30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf',
 AUDIT:'bef3e413bf02060782568e58bfab77bdb0e64b5ed59ba04dc0d6882c6d4f79f2',
}
PIN_ALIASES=('protocol','scan_conventions','charter','prior_spring_source',
 'prior_family_inventory','june_manifest','september_integrity_audit')
ZIP_SHA='2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181'
SEPT_PINS={
 116:(5331,'982a0e4728ec54f84c44bf364ec34cae5f731e66da4bfad40a4b85ca4bd751da',17314,1921,'876066eb62e4c849c6bb9fb1598cc0be8b700843483a6ddd3cf6aa9847ad2455'),
 117:(103872,'aa39ae4c977c51048fd267d890d98b66bd49dccaa965715b1cce1397a54c5273',325983,45156,'a823cf4792694cb73ef77a5a29d6e52c1566bfb86b971687eb61fe3f1629be25'),
 118:(2702040,'51b1624338dce5da4dc5a91c13d1356338997af0d3fef9cd627b29ee3bbb9447',34808082,870204,'fa721837357cf7b7fd43e49d2a9d171973663e12399c503163ef56c3464b060d'),
}
FAMILIES=('DEFINE_CURVE','DEFINE_TABLE','DEFINE_FUNCTION')
ENCODINGS=('ascii','utf-16le','utf-16be')
LIMITS={'zip_entries':30000,'member_bytes':4*1024**2,'june_bytes':512*1024**2,
 'september_stream_bytes':512*1024**2,'line_bytes':16384,'body_hits':10000,
 'seconds':300,'peak_bytes':768*1024**2}
ALNUM=set(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
NONASCII=re.compile(br'[\x80-\xff]')
class Failure(Exception):pass
def need(ok,code):
 if not ok:raise Failure(code)
def bhash(data):return hashlib.sha256(data).hexdigest()
def nhash(value):return bhash(value.encode('utf-8'))
def fhash(path):
 with path.open('rb') as handle:return hashlib.file_digest(handle,'sha256').hexdigest()
def peak():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
def guard(start):
 need(time.monotonic()-start<=LIMITS['seconds'],'TIME_CAP')
 need(peak()<=LIMITS['peak_bytes'],'RSS_CAP')
def pin_equal(value,expected):need(value==expected,'PIN_MISMATCH')
def pins():
 out={alias:fhash(path) for alias,path in zip(PIN_ALIASES,PINS)}
 need(len(PIN_ALIASES)==len(PINS) and
  all(out[alias]==value for alias,value in zip(PIN_ALIASES,PINS.values())),'DEPENDENCY_PIN')
 out['independent_scanner']=fhash(Path(__file__))
 return out
def bounded_read(handle,cap,start):
 parts=[];size=0
 while True:
  chunk=handle.read(min(1024**2,cap-size+1))
  if not chunk:break
  size+=len(chunk);need(size<=cap,'BYTE_CAP');parts.append(chunk);guard(start)
 return b''.join(parts)

def leading(prefix,encoding,line_start):
 if line_start==0 and prefix.startswith(b'\xef\xbb\xbf'):prefix=prefix[3:]
 if encoding=='ascii':return all(v in (9,13,32) for v in prefix)
 if len(prefix)%2:return False
 allowed={s.encode(encoding) for s in (' ','\t','\r')}
 return all(prefix[i:i+2] in allowed for i in range(0,len(prefix),2))
def suffix(upper,end,encoding):
 if encoding=='ascii':return end<len(upper) and upper[end] in ALNUM
 following=upper[end:end+2]
 if len(following)!=2:return False
 return following[0] in ALNUM and following[1]==0 if encoding=='utf-16le' else following[0]==0 and following[1] in ALNUM

def body_scan(data):
 parts=data.split(b'\n');lf=len(parts)-1
 lines=lf+int(bool(parts[-1]))
 longest=max([len(p)+1 for p in parts[:-1]]+[len(parts[-1])])
 need(longest<=LIMITS['line_bytes'],'LINE_CAP')
 del parts
 upper=data.upper();locations=[]
 for encoding in ENCODINGS:
  for family in FAMILIES:
   needle=('*'+family).encode(encoding);position=0
   while True:
    position=upper.find(needle,position)
    if position<0:break
    locations.append((position,encoding,family,len(needle)))
    need(len(locations)<=LIMITS['body_hits'],'HIT_CAP');position+=1
 locations.sort()
 counts={e:{f:0 for f in FAMILIES} for e in ENCODINGS}
 lead_counts={e:{f:0 for f in FAMILIES} for e in ENCODINGS}
 hits=[]
 for offset,encoding,family,length in locations:
  start=data.rfind(b'\n',0,offset)+1
  is_leading=leading(data[start:offset],encoding,start)
  hits.append({'family':family,'encoding':encoding,'byte_offset':offset,
   'line':data.count(b'\n',0,offset)+1,'byte_column':offset-start,
   'line_leading':is_leading,'has_suffix':suffix(upper,offset+length,encoding)})
  counts[encoding][family]+=1;lead_counts[encoding][family]+=int(is_leading)
 return {'bytes_read':len(data),'sha256':bhash(data),'crc32_actual':zlib.crc32(data)&0xffffffff,
  'eof':True,'physical_lines':lines,'lf_bytes':lf,'max_line_bytes':longest,
  'nul_bytes':data.count(b'\0'),'non_ascii_bytes':len(NONASCII.findall(data)),
  'all_nul':bool(data) and data.count(b'\0')==len(data),
  'initial_utf8_bom':data.startswith(b'\xef\xbb\xbf'),
  'initial_utf16le_bom':data.startswith(b'\xff\xfe'),
  'initial_utf16be_bom':data.startswith(b'\xfe\xff'),
  'marker_counts':counts,'line_leading_counts':lead_counts,'hits':hits,
  'scope':'literal_byte_search_only'}

def safe_local(root,relative):
 p=PurePosixPath(relative)
 need(not p.is_absolute() and '..' not in p.parts,'SOURCE_PATH_SCOPE')
 result=(root/relative).resolve();need(result.is_relative_to(root.resolve()),'SOURCE_ROOT_SCOPE')
 need(result.is_file(),'SOURCE_NOT_FILE');return result
def duplicate_names(infos):
 groups=defaultdict(list)
 for index,info in enumerate(infos):groups[info.orig_filename].append(index)
 return [{'name_sha256':nhash(n),'ordinals':ids} for n,ids in sorted(groups.items()) if len(ids)>1]
def zip_body(archive,info,start):
 need(info.file_size<=LIMITS['member_bytes'],'ZIP_MEMBER_CAP')
 need(not info.flag_bits&1,'ENCRYPTED_ZIP_MEMBER')
 with archive.open(info,'r') as handle:data=bounded_read(handle,LIMITS['member_bytes'],start)
 need(len(data)==info.file_size,'ZIP_SIZE');need(zlib.crc32(data)&0xffffffff==info.CRC,'ZIP_CRC')
 return data

def scan_inputs(receipt,start):
 with MANIFEST.open(newline='') as handle:
  reader=csv.DictReader(handle)
  need(reader.fieldnames==['relative_path','filename','extension','size_bytes','modified_time_utc','sha256'],'MANIFEST_SCHEMA')
  manifest=[{**r,'manifest_row':i+2} for i,r in enumerate(reader)]
 by_name={}
 for row in manifest:
  need(row['relative_path'] not in by_name,'DUPLICATE_MANIFEST_PATH')
  by_name[row['relative_path']]=row
 apdl=[r for r in manifest if PurePosixPath(r['relative_path']).suffix.lower()=='.apdl']
 archives=[r for r in manifest if r['sha256']==ZIP_SHA]
 need(len(apdl)==3 and len(archives)==1,'MANIFEST_SOURCE_SELECTION')
 archive_row=archives[0];archive_path=safe_local(JUNE,archive_row['relative_path'])
 need(archive_path.stat().st_size==int(archive_row['size_bytes']) and fhash(archive_path)==ZIP_SHA,'ZIP_CONTAINER_PIN')
 june_bytes=0;records=receipt['bodies'];excluded=receipt['excluded']
 file_checks=[]
 for ordinal,row in enumerate(apdl,1):
  alias='APDL'+str(ordinal);receipt['current_alias']=alias
  path=safe_local(JUNE,row['relative_path']);need(path.stat().st_size==int(row['size_bytes']),'APDL_SIZE')
  with path.open('rb') as handle:data=bounded_read(handle,LIMITS['june_bytes']-june_bytes,start)
  scan=body_scan(data);pin_equal(scan['sha256'],row['sha256']);need(scan['bytes_read']==int(row['size_bytes']),'APDL_BYTES')
  june_bytes+=len(data);need(june_bytes<=LIMITS['june_bytes'],'JUNE_CAP')
  records.append({'alias':alias,'kind':'APDL','manifest_row':row['manifest_row'],
   'name_sha256':nhash(row['relative_path']),'filename_sha256':nhash(row['filename']),
   'expected_bytes':int(row['size_bytes']),'expected_sha256':row['sha256'],'scan':scan})
  file_checks.append((path,row['sha256'],int(row['size_bytes'])));del data
 with zipfile.ZipFile(archive_path) as archive:
  infos=archive.infolist();need(len(infos)<=LIMITS['zip_entries'],'ZIP_ENTRY_CAP')
  receipt['zip']={'entry_count':len(infos),'duplicate_names':duplicate_names(infos),
   'manifest_row':archive_row['manifest_row'],'container_bytes':archive_path.stat().st_size,
   'container_sha256':ZIP_SHA,'container_name_sha256':nhash(archive_row['relative_path']),
   'name_hash_encoding':'UTF8_of_ZipInfo_orig_filename','ordinal_base':0}
  for ordinal,info in enumerate(infos):
   alias='ZIP'+str(ordinal);receipt['current_alias']=alias;guard(start)
   name=info.orig_filename;need(name==info.filename,'ZIP_NORMALIZED_NAME')
   directory=info.is_dir();png=not directory and PurePosixPath(name).suffix.lower()=='.png'
   relative=str(PurePosixPath(archive_row['relative_path']).with_suffix('')/name)
   row=by_name.get(relative)
   if not directory:need(row is not None,'ZIP_MANIFEST_MEMBER_MISSING')
   common={'alias':alias,'kind':'ZIP','zip_ordinal':ordinal,'name_sha256':nhash(name),
    'manifest_row':None if row is None else row['manifest_row'],
    'manifest_name_sha256':None if row is None else nhash(row['relative_path']),
    'filename_sha256':None if row is None else nhash(row['filename']),
    'expected_bytes':info.file_size,'compressed_bytes':info.compress_size,
    'expected_crc32':info.CRC,'compression_type':info.compress_type,'flags':info.flag_bits,
    'expected_sha256':None if row is None else row['sha256']}
   if row is not None:need(info.file_size==int(row['size_bytes']),'ZIP_MANIFEST_SIZE')
   if directory or png:
    excluded.append({**common,'reason':'directory' if directory else 'PNG',
     'bytes_read':0,'crc_verified':False,'sha256_verified':False});continue
   data=zip_body(archive,info,start);june_bytes+=len(data);need(june_bytes<=LIMITS['june_bytes'],'JUNE_CAP')
   scan=body_scan(data);pin_equal(scan['sha256'],row['sha256'])
   records.append({**common,'crc_verified':True,'sha256_verified':True,'scan':scan});del data
  receipt['zip']['regular_entries']=sum(not i.is_dir() for i in infos)
  receipt['zip']['directories']=sum(i.is_dir() for i in infos)
  receipt['zip']['png_excluded']=sum(not i.is_dir() and PurePosixPath(i.filename).suffix.lower()=='.png' for i in infos)
  need((len(infos),receipt['zip']['directories'],receipt['zip']['png_excluded'])==(25639,5,272),'ZIP_CENSUS')
 receipt['june_total_scanned_bytes']=june_bytes
 need(sum(r['kind']=='ZIP' for r in records)==25362,'ZIP_BODY_CENSUS')
 need(fhash(archive_path)==ZIP_SHA and archive_path.stat().st_size==int(archive_row['size_bytes']),'ZIP_CHANGED')
 receipt['zip']['container_after_sha256']=fhash(archive_path)
 for path,digest,size in file_checks:need(fhash(path)==digest and path.stat().st_size==size,'APDL_CHANGED')
 audit=json.loads(AUDIT.read_text())
 for source,(compressed_size,compressed_hash,usize,ulines,uhash) in SEPT_PINS.items():
  matches=[r for r in audit['members'] if r['extracted_sha256']==compressed_hash]
  need(len(matches)==1,'SEPTEMBER_AUDIT_SELECTION');row=matches[0]
  name=row['name'];path=safe_local(SEPTEMBER,name);alias='SRC'+str(source);receipt['current_alias']=alias
  need(path.stat().st_size==compressed_size and fhash(path)==compressed_hash,'SEPTEMBER_COMPRESSED_PIN')
  with gzip.open(path,'rb') as handle:data=bounded_read(handle,LIMITS['september_stream_bytes'],start)
  scan=body_scan(data)
  need((scan['bytes_read'],scan['physical_lines'],scan['sha256'])==(usize,ulines,uhash),'SEPTEMBER_EOF_PIN')
  need(fhash(path)==compressed_hash and path.stat().st_size==compressed_size,'SEPTEMBER_CHANGED')
  records.append({'alias':alias,'kind':'September','source':source,'name_sha256':nhash(name),
   'compressed_bytes':compressed_size,'compressed_sha256':compressed_hash,
   'compressed_after_sha256':fhash(path),'gzip_crc_checked_by_reader':True,
   'expected_bytes':usize,'expected_sha256':uhash,'expected_lines':ulines,'scan':scan});del data
 receipt.pop('current_alias',None);guard(start)
 totals={e:{f:0 for f in FAMILIES} for e in ENCODINGS}
 leading_totals={e:{f:0 for f in FAMILIES} for e in ENCODINGS}
 for row in records:
  for encoding in ENCODINGS:
   for family in FAMILIES:
    totals[encoding][family]+=row['scan']['marker_counts'][encoding][family]
    leading_totals[encoding][family]+=row['scan']['line_leading_counts'][encoding][family]
 return {'body_count':len(records),'apdl_count':3,'zip_body_count':25362,'september_count':3,
  'excluded_count':len(excluded),'bytes_scanned':sum(r['scan']['bytes_read'] for r in records),
  'physical_lines':sum(r['scan']['physical_lines'] for r in records),
  'nul_bodies':sum(r['scan']['nul_bytes']>0 for r in records),
  'all_nul_bodies':sum(r['scan']['all_nul'] for r in records),
  'non_ascii_bodies':sum(r['scan']['non_ascii_bytes']>0 for r in records),
  'marker_counts':totals,'line_leading_counts':leading_totals,
  'bodies_with_hits':[r['alias'] for r in records if r['scan']['hits']],
  'scope':'Literal explicit-definition families only in named released input bytes/encodings; no dynamic/encoded/binary/other-record/runtime absence or historical law finding.'}

def controls():
 fixtures=[
  ('mixed',b' \t*DeFiNe_CuRvE\n',1,1),
  ('bom',b'\xef\xbb\xbf \r*DEFINE_TABLE',1,1),
  ('variant',b'*DEFINE_FUNCTION_X\n',1,1),
  ('embedded',b'! *DEFINE_CURVE\n"*DEFINE_TABLE"; *DEFINE_FUNCTION\n',3,0),
  ('repeated',b'*DEFINE_CURVE *DEFINE_CURVE\n',2,1),
  ('le',' \t*define_curve_X'.encode('utf-16le'),2,1),
  ('be','\r*define_table'.encode('utf-16be'),1,1),
  ('nul',b'\0'*328,0,0),('mixed_nul',b'\0*DEFINE_CURVE\xff',1,0),
  ('no_final_lf',b'*DEFINE_FUNCTION',1,1),('empty',b'',0,0),
  ('unrelated',b'DEFINE_CURVE *DEFINE_CURV *DEFINE_TABEL\n',0,0),
  ('odd_utf16_prefix',b'x'+'*DEFINE_CURVE'.encode('utf-16le'),1,0),
  ('utf16_bom',b'\xff\xfe'+'*DEFINE_CURVE'.encode('utf-16le'),1,0),
  ('utf16_lf_raw','a\n*DEFINE_CURVE'.encode('utf-16le'),2,1),
  ('utf16be_lf','a\n*DEFINE_CURVE'.encode('utf-16be'),1,1),
  ('utf8_text',b'\xc3\xa9 "*DEFINE_FUNCTION"',1,0),
 ]
 results=[]
 for name,data,hit_count,leading_count in fixtures:
  result=body_scan(data)
  need(len(result['hits'])==hit_count and sum(r['line_leading'] for r in result['hits'])==leading_count,'SYNTHETIC_MARKER')
  results.append({'name':name,'input_hex':data.hex(),'result':result,
   'expected_hits':hit_count,'expected_leading':leading_count})
 need(results[2]['result']['hits'][0]['has_suffix'],'VARIANT_CONTROL')
 need([(h['encoding'],h['byte_offset'],h['line'],h['byte_column'],h['line_leading'])
  for h in results[14]['result']['hits']]==[('utf-16be',3,2,0,True),
   ('utf-16le',4,2,1,False)],'OVERLAPPING_ENCODING_CONTROL')
 need(results[7]['result']['all_nul'] and results[8]['result']['non_ascii_bytes']==1,'BYTE_CLASS_CONTROL')
 need(body_scan(b'a\nb')['physical_lines']==2 and body_scan(b'a\n')['physical_lines']==1,'LF_CONTROL')
 need(body_scan(b'abc\n \t*DEFINE_TABLE')['hits'][0]['byte_offset']==6,'OFFSET_CONTROL')
 rejected={}
 for code,call in [('line_cap',lambda:body_scan(b'x'*(LIMITS['line_bytes']+1))),
  ('byte_cap',lambda:bounded_read(io.BytesIO(b'123'),2,time.monotonic())),
  ('hit_cap',lambda:body_scan(b'*DEFINE_CURVE\n'*(LIMITS['body_hits']+1))),
  ('pin',lambda:pin_equal('a','b'))]:
  try:call()
  except Failure:rejected[code]=True
  else:rejected[code]=False
 need(all(rejected.values()),'REJECTION_CONTROL')
 with tempfile.TemporaryDirectory(prefix='curve-scan-control-') as folder:
  target=Path(folder)/'fixture';target.touch();before=fhash(target)
  try:target.open('x')
  except FileExistsError:refused=True
  else:refused=False
  need(refused and fhash(target)==before,'CREATE_ONLY_CONTROL')
 container=io.BytesIO()
 with warnings.catch_warnings():
  warnings.simplefilter('ignore',UserWarning)
  with zipfile.ZipFile(container,'w',compression=zipfile.ZIP_STORED) as z:
   z.writestr('same',b'one');z.writestr('same',b'two')
 raw=container.getvalue()
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  infos=z.infolist();need(duplicate_names(infos)==[{'name_sha256':nhash('same'),'ordinals':[0,1]}],'DUPLICATE_NAME_CONTROL')
  contents=[zip_body(z,i,time.monotonic()) for i in infos]
  need(contents==[b'one',b'two'],'ZIP_ORDINAL_CONTROL')
 corrupted=bytearray(raw);name_len,extra_len=struct.unpack_from('<HH',corrupted,26)
 corrupted[30+name_len+extra_len]^=1
 try:
  with zipfile.ZipFile(io.BytesIO(corrupted)) as z:zip_body(z,z.infolist()[0],time.monotonic())
 except zipfile.BadZipFile:crc_rejected=True
 else:crc_rejected=False
 need(crc_rejected,'CRC_CORRUPTION_CONTROL')
 return {'passed':True,'fixture_count':len(results),'fixtures':results,
  'other_checks':['variant','NUL_and_nonASCII','LF_count','absolute_offset',
   'line_cap','byte_cap','hit_cap','pin_refusal','output_refusal','duplicate_name',
   'ordinal_specific_open','corrupt_CRC','overlapping_encoding_locators'],'other_count':13,
  'rejections':rejected,'create_only_refused':refused,
  'zip_input_hex':raw.hex(),'zip_corrupt_input_hex':corrupted.hex(),
  'zip_member_payload_hex':[x.hex() for x in contents],'crc_corruption_rejected':crc_rejected}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--out',required=True)
 parser.add_argument('--controls-only',action='store_true');args=parser.parse_args()
 need(re.fullmatch(r'independent-[a-z0-9-]+\.json',args.out) is not None,'OUTPUT_SCOPE')
 target=BASE/args.out
 with target.open('x') as destination:
  started=time.monotonic();receipt={'status':'FAIL','command':sys.argv,'bodies':[],'excluded':[]}
  try:
   receipt['controls']=controls()
   if args.controls_only:receipt['status']='CONTROLS_PASS'
   else:
    receipt['pins_before']=pins();receipt['result']=scan_inputs(receipt,started)
    receipt['pins_after']=pins();need(receipt['pins_before']==receipt['pins_after'],'CHANGED_INPUTS')
    receipt['status']='PASS'
  except Exception as exc:
   receipt['failure']={'class':type(exc).__name__}
   if isinstance(exc,Failure):receipt['failure']['code']=str(exc)
  receipt.update(code_sha256=fhash(Path(__file__)),elapsed_seconds=time.monotonic()-started,
   peak_bytes=peak(),limits=LIMITS,runtime={'python':sys.version,'executable':sys.executable})
  json.dump(receipt,destination,sort_keys=True,indent=2,allow_nan=False);destination.write('\n')
 print(json.dumps({'status':receipt['status'],'file':target.name,'sha256':fhash(target),
  'counts':receipt.get('result'),'failure':receipt.get('failure')}))
 return 0 if receipt['status'] in ('PASS','CONTROLS_PASS') else 1
if __name__=='__main__':raise SystemExit(main())

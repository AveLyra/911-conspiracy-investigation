#!/usr/bin/env python3
"""Verify publication integrity and integration; not historical truth or clock calibration."""
from pathlib import Path
import json,hashlib,subprocess,re,sys
H=Path(__file__).resolve().parent;R=H.parents[2]
S=R/'investigation/broader-evidence/outstanding-records-verification-2026-10-26'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(ref,p):return subprocess.check_output(['git','show',ref+':'+p],cwd=R)
groups=[]
def ok(name,condition):
 if not condition:raise AssertionError(name)
 groups.append(name)
reg=json.loads((H/'register.json').read_text());scope=json.loads((H/'SCOPE.json').read_text());prev=json.loads(blob(scope['prior_master_commit'],scope['prior_master_path']+'/register.json'))
ok('175 unique contiguous master IDs',len(reg['entries'])==175 and [e['id'] for e in reg['entries']]==[f'M{n:03}' for n in range(1,176)])
ok('all160prior objects exactly preserved',reg['entries'][:160]==prev['entries'])
ok('all prior metadata preserved',reg['prior_master_metadata']=={k:v for k,v in prev.items() if k!='entries'})
ok('BR/BPR open target ledger unchanged',reg['prior_open_targets']==prev['prior_open_targets'])
f=json.loads((S/'findings.json').read_text())['findings'];incoming=json.loads((S/'INCOMING-FAA-FINDINGS.json').read_text())['findings']
ok('3CIA+12FAA stable incoming-ID coverage',[x['id'] for x in f]==['CC001','CC002','CC003']+[f'FA{n:03}' for n in range(1,13)] and {x['id'] for x in f if x['id'].startswith('FA')}=={x['id'] for x in incoming})
ok('15new master rows bind exact reviewed findings',all(e['original_record']==x for e,x in zip(reg['entries'][160:],f)))
# All claims must have conflicts/limits, next tests and no automatic truth selection.
ok('all15 preserve qualifications and unrun discriminating tests',all(x['conflicting_or_qualifying_records'] and x['next_test'] and x['claim_type'] for x in f))
pin=json.loads((S/'EXCERPT-PINS.json').read_text());ex=(S/'SOURCE-EXCERPTS.md').read_bytes();lines=ex.decode().splitlines();sources=json.loads((S/'SOURCES.json').read_text())['sources']
ok('excerpt file hash',sha(ex)==pin['file_sha256'])
for key,p in pin['pins'].items():
 assert lines[p['line_start']-1]=='## '+key,key
 assert sha('\n'.join(lines[p['line_start']+3:p['line_end']-1]).rstrip('\n').encode())==p['excerpt_sha256'],key
 assert p['source_sha256']==sources[p['source_id']]['sha256'],key
ok('126 exact excerpt hashes/line/source joins',len(pin['pins'])==126)
ok('all finding-to-pin links exact',all(l==pin['pins'][i] for x in f for i,l in zip(x['source_refs'],x['locators'])))
report=(S/'REPORT.md').read_bytes()
ok('all master review hashes bind this report',all(l['review_report_sha256']==sha(report) for e in reg['entries'][160:] for l in e['locators']))
a=json.loads((S/'AUDIO-CONTROL-CHECK.json').read_text());c=a['checks']
ok('failed audio control not historical evidence',c[0]['all_pcm_bytes_zero'] and c[0]['sample_frames']==240000 and c[0]['most_repeated_text']=='You' and a['evidentiary_transcription_accepted'] is False and a['wall_clock_map'] is None)
ok('ASR segment/repeat/overrun counts preserved',[x['segments'] for x in c]==[1,47,96] and [x['most_repeated_count'] for x in c]==[1,46,92] and [x['segments_past_clip'] for x in c]==[0,1,1])
ar=json.loads((S/'ARITHMETIC-CHECK.json').read_text())
ok('stated anchor/page arithmetic only',[ar['notification_stated_anchor_difference_minutes'],ar['arrival_nominal_difference_minutes'],ar['conditional_exchange_forward_shift_minutes'],ar['responsive_page_allocation_sum'],ar['packet_count_arithmetic']]==[51,38,[44,53],4845,429])
ok('official DOT acquisition distinct from failed CIA PDF',sources['DOT-OFFICIAL']['sha256']=='8dde0e97d6e6adac23afea241cfff77c9a0fb4095087959f54874fc6640dc616' and json.loads((S/'SOURCES.json').read_text())['official_cia_attempt']['is_pdf'] is False)
# The previously published papers and sources are protected against this working candidate as well as HEAD.
for path,p in scope['protected_files'].items():
 q=R/path;b=q.read_bytes() if q.is_file() else blob('HEAD',path)
 assert sha(b)==p['sha256'],path
ok('110 earlier source/master files unchanged',len(scope['protected_files'])==110)
prior=blob(scope['prior_master_commit'],scope['prior_master_path']+'/MASTER-LIST.md').decode();body=prior[prior.index('## Register\n'):]
# Difference contract: only relative citation destinations relocate within the preserved prior body.
def stripdest(s):return re.sub(r'\]\(([^)]+)\)','](DEST)',s).strip()
new=(H/'MASTER-LIST.md').read_text();kept=new[new.index('## Register\n'):new.index('\n\n## CIA continuation, FAA/NORAD/Mineta and local-method review')]
ok('prior master body unchanged except citation destinations',stripdest(kept)==stripdest(body))
ok('all19native-note initial copy hashes',all(sha((S/n).read_bytes())==v['sha256'] for n,v in scope['public_note_copy_pins'].items()) and len(scope['public_note_copy_pins'])==19)
# Publication files should be small reviewed notes, not media or private paths/credentials.
for directory in [H,S]:
 for p in directory.iterdir():
  if not p.is_file():continue
  b=p.read_bytes();assert p.suffix in ['.md','.json','.py','.diff'],str(p)
  private_path_pattern=b'/' + b'Users/|' + b'/' + b'Volumes/'
  assert not re.search(private_path_pattern,b),str(p)
  assert not re.search(rb'BEGIN (?:OPENSSH|RSA) PRIVATE KEY|ghp_[A-Za-z0-9]{20,}',b),str(p)
ok('reviewed payload paths/types/private-marker check',True)
# Optional generated manifests exclude their own hash to avoid self-reference.
for directory in [H,S]:
 m=directory/'MANIFEST.json'
 if m.exists():
  data=json.loads(m.read_text())
  for n,p in data['files'].items():assert sha((directory/n).read_bytes())==p['sha256'],str(directory/n)
  ok('file manifest '+directory.name,True)
r={'status':'PASS','check_group_count':len(groups),'checks':groups,'limits':'Integrity, coverage, explicit limits and preservation only. Source file hashing and16page visual review are separately receipted; no native-message authentication, calibrated clock truth or motive result.'}
print(json.dumps(r,ensure_ascii=False,indent=2))

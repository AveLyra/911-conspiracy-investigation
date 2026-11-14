#!/usr/bin/env python3
"""Verify captured source bytes, stated source markers and candidate format."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,subprocess
b=Path('/Users/admin/docs/911-worktrees/broader-evidence-review-2026-10-26/research/broader-evidence-review-2026-10-26/telephone-felt-audio-candidate-2026-11-14')
pins=json.loads((b/'SOURCE-PINS.json').read_text())
class P(HTMLParser):
 def __init__(self):super().__init__();self.t=[]
 def handle_data(self,s):self.t.append(s)
texts={}
for k,v in pins['sources'].items():
 p=b/(k+'.html'); data=p.read_bytes();assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256'];q=P();q.feed(data.decode('utf-8',errors='replace'));texts[k]=re.sub(r'\s+',' ',' '.join(q.t)).lower()
for k,s in [('NPS','70 seconds'),('HOUSTON','5 or 6 minutes long'),('KALLAS','audio recording released under foia'),('WPXI','obtained a recording of the phone call')]: assert s in texts[k],(k,s)
p=Path('/Volumes/dev_src_case_sensitive/911-PROJECT/active-media/working-tree/research/broader-evidence-review-2026-10-26/telephone-felt-audio-candidate-2026-11-14/source.mp3');data=p.read_bytes(); assert len(data)==1657984 and hashlib.sha256(data).hexdigest()==pins['public_candidate_audio']['sha256']
r=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,sample_rate,channels','-of','json',str(p)]));assert r['format']['duration']=='138.135510' and r['streams'][0]['codec_name']=='mp3'
print('PASS: source hashes, four textual anchors, MP3 hash and container duration; call span/audio provenance untested.')

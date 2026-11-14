#!/usr/bin/env python3
"""Verify downloaded public NARA audio bytes and ffprobe format-duration observations.
Usage: python3 VERIFY.py PATH_TO_7598789.mp3 PATH_TO_7598772.mp3
Requires ffprobe on PATH; does not test speech content or clock alignment.
"""
import hashlib,json,subprocess,sys
from pathlib import Path
cases=[(235730444,"e887c08dd70a295f91089dddb1f0b2756edfeae1a269ea48631f0bf37972d2d5",7366.508469),(234660471,"2b79a5671051a51363827564c56e45dbd764ac800dff69e68ab53e049aca11a1",7333.071750)]
if len(sys.argv)!=3: raise SystemExit(__doc__)
for path,(size,sha,duration) in zip(map(Path,sys.argv[1:]),cases):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 actual_size=path.stat().st_size
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)]))
 actual=float(probe['format']['duration'])
 assert actual_size==size and h.hexdigest()==sha, 'Source bytes differ'
 assert abs(actual-duration)<0.01, 'Duration differs by at least 0.01s'
 print(json.dumps({'bytes':actual_size,'sha256':h.hexdigest(),'ffprobe_seconds':actual,'nominal_label_seconds':7200,'excess_seconds':round(actual-7200,6)}))

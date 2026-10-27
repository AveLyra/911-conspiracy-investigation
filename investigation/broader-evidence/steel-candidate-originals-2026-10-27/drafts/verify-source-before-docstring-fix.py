"""Verify this pinned public movie entity and repeat the video-frame count.

python3 verify_source.py /path/to/WTC\ Tape\ 3.mov
Requires ffprobe on PATH. Does not download media or execute embedded code.
Matching bytes/decoded count is not a recording-date or custody validation.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root=Path(__file__).resolve().parent
expected=json.loads((root/'SOURCE.json').read_text())
source=Path(sys.argv[1]);h=hashlib.sha256();total=0
with source.open('rb') as f:
    for b in iter(lambda:f.read(1024*1024),b''):
        h.update(b);total+=len(b)
if h.hexdigest()!=expected['sha256'] or total!=expected['bytes']:
    raise ValueError('Different source entity: preserve separately; this study does not adjudicate variants')
command=['ffprobe','-v','warning','-count_frames','-select_streams','v:0',
         '-show_entries','stream=nb_read_frames,nb_frames,duration,r_frame_rate,avg_frame_rate',
         '-of','json',str(source)]
a=subprocess.run(command,capture_output=True,text=True,check=True)
count=json.loads(a.stdout)['streams'][0]
print(json.dumps(dict(sha256=h.hexdigest(),bytes=total,video=count,
      decoded_equals_stored=count['nb_read_frames']==count['nb_frames'],
      decoder_stderr=a.stderr,
      scope='Current-file integrity and video decode count only; not analog-tape completeness, specimen identity, origin, cause, camera dates or audio synchronization.'),indent=2))

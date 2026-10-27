"""Acquire two public NIST candidate-control photographs, no session material.

Run with NEW_OUTPUT_DIRECTORY and C13A-PUBLIC-IDS.json. Raw images stay local.
This is acquisition, not origin authentication. Refuses existing destinations.
"""
import hashlib
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

out = Path(sys.argv[1])
pins = json.loads(Path(sys.argv[2]).read_text())
out.mkdir(parents=True, exist_ok=False)
receipts = []
for pin in pins:
    url = 'https://drive.google.com/uc?' + urllib.parse.urlencode(
        dict(export='download', id=pin['id']))
    with urllib.request.urlopen(url, timeout=60) as response:
        body = response.read()
        row = dict(pin, source_url=url, final_url=response.url,
                   access_utc=datetime.now(timezone.utc).isoformat(),
                   status=response.status, content_type=response.headers.get('Content-Type'),
                   response_headers=dict(response.headers.items()),
                   bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
    filename = pin['filename'] if body.startswith(b'\xff\xd8') and len(body)==pin['provider_bytes'] else 'variant-' + pin['id'] + '.bin'
    with (out / filename).open('xb') as handle:
        handle.write(body)
    row['saved_filename'] = filename
    receipts.append(row)
    with (out / ('receipt-' + pin['id'] + '.json')).open('x') as handle:
        json.dump(row, handle, indent=2)
    if filename != pin['filename']:
        raise ValueError('Unexpected entity retained as variant; original not replaced')
with (out / 'ACQUISITION-RESULT.json').open('x') as handle:
    json.dump(receipts, handle, indent=2)
print(json.dumps([{k:r[k] for k in ['id','saved_filename','bytes','sha256','status','content_type']} for r in receipts],indent=2))

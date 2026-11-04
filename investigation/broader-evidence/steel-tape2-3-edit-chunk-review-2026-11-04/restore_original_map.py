"""Restore the exact measured CRLF CSV from its reversible text envelope."""
from pathlib import Path
import argparse,base64,hashlib
p=argparse.ArgumentParser();p.add_argument('encoded',type=Path);p.add_argument('new_output',type=Path)
a=p.parse_args()
raw=base64.b64decode(a.encoded.read_bytes(),validate=False)
expected='e1ea5219eb07adfeacff55945eacb2347a6492c4bfb08fffa0bb948c43dc2c2b'
assert len(raw)==557839 and hashlib.sha256(raw).hexdigest()==expected
with a.new_output.open('xb') as f:f.write(raw)
print('Restored557839bytes; original SHA-256 verified:'+expected)

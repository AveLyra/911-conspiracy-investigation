#!/usr/bin/env python3
import hashlib,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]
bad=[];count=0
for line in (root/'SHA256SUMS.txt').read_text().splitlines():
 expected,name=line.split('  ',1);p=root/name;h=hashlib.sha256()
 if not p.is_file():bad.append((name,'MISSING'));continue
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 if h.hexdigest()!=expected:bad.append((name,'HASH MISMATCH'))
 count+=1
print(f'Verified {count} files; failures: {len(bad)}')
for x in bad:print(*x)
sys.exit(bool(bad))

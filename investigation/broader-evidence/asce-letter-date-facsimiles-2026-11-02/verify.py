"""Verify supplied source entities against preserved fingerprints; no network or date adjudication."""
import argparse,hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--images',type=Path,required=True);parser.add_argument('--prior-text',type=Path,required=True);args=parser.parse_args()
rows=json.loads((p/'SOURCES.json').read_text())['sources'];results=[]
for row in rows:
 path=args.prior_text if row['id']=='B161' else args.images/f"ASCE-page{row['printed_page']}.png"
 data=path.read_bytes();assert len(data)==row['bytes'],row['id'];assert hashlib.sha256(data).hexdigest()==row['sha256'],row['id']
 if row['id']=='B161':
  lines=data.decode().splitlines()
  for line,value in zip(row['one_based_export_lines'],row['values_in_order']):assert lines[line-1].strip()==value
 else:assert data.startswith(b'\x89PNG\r\n\x1a\n')
 results.append({'id':row['id'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'match':True})
print(json.dumps({'sources_match':results,'scope':'Fingerprints and prior text line locators only; visible dates were manually read. This does not authenticate the native letter, signatures, date, cause or historical claims.'},indent=2))

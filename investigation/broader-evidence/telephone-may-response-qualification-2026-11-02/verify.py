"""Check declared source/preservation/status fields, not historical call validity."""
from pathlib import Path
import argparse,hashlib,json

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--native-inputs',type=Path);a=p.parse_args();r=Path(__file__).resolve().parent
 mf=json.loads((r/'BUNDLE-HASHES.json').read_text())
 for x in mf['files']:
  b=(r/x['name']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['name']
 obs=json.loads((r/'OBSERVATIONS.json').read_text())['observations'];assert [x['id'] for x in obs]==[f'RS{i:02}' for i in range(1,5)]
 for x in obs:
  assert x['distinction'] and x['missing_discriminator']
  for q in x['pins']:
   n=q['physical_page'];assert n in(70,71) and q['production_footer']=={70:'000000745',71:'000000746'}[n]
   assert q['url'].endswith('#page='+str(n))
 assert obs[1]['literal_values']['response_timezone']=='not printed'
 assert obs[1]['literal_values']['response_time']=='6:13 a.m.'
 assert 'at this time' in obs[2]['literal_values']['disposition'] and 'by Las Vegas' in obs[2]['literal_values']['disposition']
 assert obs[3]['literal_values']['typed_reference']=='265D-NY-280350 Serial 79'
 todo=(r/'OPEN-TODOS.md').read_text()
 for t,n in [('FAA',4),('TEL',4),('REC',3),('MAT',3),('STL',4)]:
  for i in range(1,n+1):assert '**'+t+f'{i:02}'+':**' in todo
 count=0
 if a.native_inputs:
  v=json.loads(a.native_inputs.read_text())
  for x in v['files']:
   b=Path(x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['role'];count+=1
  before=Path(v['preceding']).read_bytes();assert before==Path(v['preserved']).read_bytes()
  assert Path(v['combined']).read_bytes()==before+b'\n\n'+(r/'README.md').read_bytes()
 print(json.dumps({'status':'passed','body_files':len(mf['files']),'native_identity_files':count,'reused_response_faces':2,'new_source_acquisitions':0,'original_requirements_retained':18,'scope':'Bytes/manuallocators/qualifiedstatus/oldsourcepreservation/TODOretention only; no independentpixeltranscription, nativecaseversion, historicalmeeting/caller/carrier/clock/custody authentication or whole-goal acceptance.'},indent=2))
if __name__=='__main__':main()

from pathlib import Path
import json,hashlib,argparse,re
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4194304),b''):h.update(b)
 return h.hexdigest()
ap=argparse.ArgumentParser()
ap.add_argument('--source-map',type=Path)
args=ap.parse_args()
base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
checks=[]
for x in manifest['files']:
 f=base/x['name']
 assert f.is_file() and f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],x['name']
 checks.append(x['name'])
source_checks=[];metric_checks=[]
sources=json.loads((base/'SOURCES.json').read_text())
byid={x['id']:x for x in sources['sources']}
if args.source_map:
 mapping=json.loads(args.source_map.read_text())
 for id,path in mapping.items():
  x=byid[id];f=Path(path)
  assert f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],id
  source_checks.append(id)
  if id in ('RUN119','RUN84'):
   rows=json.loads(f.read_text())['transcription'];e=x['metrics']
   pattern=re.compile(sources['machine_locator_pattern'])
   values={'segment_count':len(rows),'literal_music_playing_segments':sum(r['text'].strip().casefold()=='(music playing)' for r in rows),'segments_over_500_characters':sum(len(r['text'])>500 for r in rows),'maximum_segment_characters':max(len(r['text']) for r in rows),'zero_length_model_segments':sum(r['offsets']['from']==r['offsets']['to'] for r in rows),'aircraft_pattern_matches':[i for i,r in enumerate(rows) if pattern.search(r['text'])]}
   for k,v in values.items():
    if k=='aircraft_pattern_matches':assert not v and not e[k],id
    else:assert v==e[k],(id,k)
   metric_checks.append(id)
print(json.dumps({'status':'passed','manifest_files_checked':checks,'source_files_checked':source_checks,'machine_metric_inputs_checked':metric_checks,'scope':'Byte/declared-metric checks only. Not historical truth, speech accuracy, inference exit success, signature authenticity or whole-goal acceptance.'},indent=2))

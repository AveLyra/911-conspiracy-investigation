"""Reproduce selected printed-value comparisons, not historical clock calibration.

Usage: python compare_sources.py --sources NEW_PDF_DIRECTORY --f04 AWA658.pdf --output NEW_OUTPUT
Inputs must match the pinned entities. Event matching is a declared manual
candidate association by words/position/context, not a native event ID.
PyMuPDF extracts sorted text; original images govern visual readings.
"""
from pathlib import Path
import argparse,hashlib,json,re
import fitz

ap=argparse.ArgumentParser()
ap.add_argument('--sources',type=Path,required=True)
ap.add_argument('--f04',type=Path,required=True)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
pins={
 'S01':('S01-7596630-ZID93.pdf','8f20feb7c28f2e0e9e56bfbea4edb7fd1515e30f15e4cf5842b2b3f4bc92b9d8'),
 'S02':('S02-7596481-ZID166.pdf','713a5438f6d9b49d1fa4235c5993c7fc41257e62934942bd6735544b55bf2329'),
 'S03':('S03-7596478-ZID158.pdf','4e93a60dcb3d77020c48ddd2e57c74d748d5e214f99bf6c947e46143a7e7a5d1'),
 'S04':('S04-7595834-ZID161.pdf','6c304d1a27a2ae34951e2883182a3f1fc2ec682258061e9de6512fc79aa19d99'),
 'S05':('S05-7595835-ZID162.pdf','1a6252be9720f383377310b07e876e1e95173b198ce9b5a1a5cb21e6e581f2e0'),
 'S06':('S06-7596426-ZID105.pdf','162d54edeb6ebe6394ea71e3bd1dd8f61d3ecbb1b1195d7e02c6ae3b1e9bda1e'),
 'F04':(None,'27580b551698194522fb21d7896964b676d5921b63c7fd05e64b9ae8559c507d')}
text={};counts={};verified=[]
for key,(name,digest)in pins.items():
 path=args.f04 if key=='F04'else args.sources/name
 body=path.read_bytes()
 assert hashlib.sha256(body).hexdigest()==digest,(key,'source hash mismatch')
 with fitz.open(path)as doc:
  text[key]=[p.get_text(sort=True)for p in doc];counts[key]=len(doc)
 verified.append({'source':key,'bytes':len(body),'sha256':digest,'pages':counts[key]})

def rows(source,page):
 lines=text[source][page-1].splitlines();out=[]
 for i,line in enumerate(lines):
  m=re.match(r'^\s*(\d{4}:\d{2})\s+(.+)',line)
  if not m:continue
  end=i+1
  while end<len(lines)and lines[end].strip()and not re.match(r'^\s*(?:\d{4}:\d{2}\s+|\d{4}\s*$)',lines[end]):end+=1
  out.append({'source':source,'page':page,'start_line':i+1,'end_line':end,
              'time':m.group(1),'verbatim_text_layer':'\n'.join(lines[i:end])})
 return out

def find(source,pages,needle):
 candidates=[r for p in pages for r in rows(source,p)
             if needle in ' '.join(r['verbatim_text_layer'].lower().split())]
 assert len(candidates)==1,(source,pages,needle,len(candidates))
 return candidates[0]

def seconds(value):return int(value[:2])*3600+int(value[2:4])*60+int(value[5:])
def delta(a,b):return seconds(a['time'])-seconds(b['time'])

anchors=[('A1','Check-in','with you level'),('A2','Squawk instruction','indy center roger'),
 ('A3','Climb instruction','climb and maintain'),('A4','Climb readback','three five oh american'),
 ('A5','Right-vector instruction','ten degrees to the right'),('A6','Ten-right readback','ten right american')]
comparisons=[]
for aid,label,needle in anchors:
 readings={k:find(s,p,needle)for k,s,p in [
  ('compiled_associate','F04',[38]),('draft_radar','F04',[71,72]),
  ('december_radar','S04',[2]),('may_associate','S05',[2,4]) ]}
 comparisons.append({'id':aid,'candidate_event':label,'readings':readings,
  'compiled_associate_minus_december_seconds':delta(readings['compiled_associate'],readings['december_radar']),
  'draft_radar_minus_december_seconds':delta(readings['draft_radar'],readings['december_radar']),
  'december_minus_may_seconds':delta(readings['december_radar'],readings['may_associate'])})

# Reuse the six predeclared command/check-in joins; add the second of two
# identical short Indy calls within the 1256 sequence. No exhaustive census.
shared_rows=[{'id':r['id'],'r':r['readings']['december_radar'],
 'ra':r['readings']['may_associate'],
 'r_minus_ra_seconds':r['december_minus_may_seconds']}for r in comparisons]
def second_short_indy(source,page):
 candidates=[r for r in rows(source,page)if 'american seventy seven indy' in
             ' '.join(r['verbatim_text_layer'].lower().split())]
 assert len(candidates)==2,(source,page,len(candidates))
 return candidates[1]
a=second_short_indy('S04',3);b=second_short_indy('S05',4)
shared_rows.append({'id':'J7','selection':'Second short Indy call in page-local 1256 cluster; manual words/sequence association',
 'r':a,'ra':b,'r_minus_ra_seconds':delta(a,b)})

relay=[]
for key,oldp,newp,needle in [
 ('R1',45,9,'we have an unconfirmed report'),
 ('R2',45,9,"we've had an unconfirmed report"),
 ('R3',45,10,'confirmed th'),
 ('R4',46,11,'they confirmed it'),
 ('R5',47,12,'boston')]:
 if key=='R5':
  # The one-word answer and the following readback both include Boston.
  def answer(s,p):
   x=[r for r in rows(s,p)if re.search(r'\bAAL\s+boston\s*$',r['verbatim_text_layer'])]
   assert len(x)==1,(s,p,len(x));return x[0]
  a=answer('F04',oldp);b=answer('S05',newp)
 else:a=find('F04',[oldp],needle);b=find('S05',[newp],needle)
 relay.append({'id':key,'old':a,'may':b,'may_minus_old_seconds':delta(b,a)})

excerpts=[]
for s,p,lo,hi in [('S02',1,6,24),('S04',1,19,20),('S04',1,29,30),
 ('S05',1,9,10),('S05',1,18,19),('S05',1,32,33),('S06',1,13,17),('S06',1,23,25)]:
 lines=text[s][p-1].splitlines();assert hi<=len(lines)
 excerpts.append({'source':s,'page':p,'lines':[lo,hi],
                  'verbatim_text_layer':'\n'.join(lines[lo-1:hi])})

summary={'source_checks':verified,'new_PDFs':6,'new_PDF_pages':sum(v for k,v in counts.items()if k!='F04'),
 'extractor':'PyMuPDF '+str(fitz.VersionBind)+' get_text(sort=True); page-local splitlines locators',
 'first_six_compiled_minus_december':[r['compiled_associate_minus_december_seconds']for r in comparisons],
 'first_six_draft_minus_december':[r['draft_radar_minus_december_seconds']for r in comparisons],
 'first_six_december_minus_may':[r['december_minus_may_seconds']for r in comparisons],
 'shared_selected_pair_count':len(shared_rows),
 'shared_selected_delta_counts':{str(d):sum(x['r_minus_ra_seconds']==d for x in shared_rows)for d in sorted({x['r_minus_ra_seconds']for x in shared_rows})},
 'compiled_first_report_to_relay_seconds':seconds(relay[2]['old']['time'])-seconds(relay[0]['old']['time']),
 'may_first_report_to_relay_seconds':seconds(relay[2]['may']['time'])-seconds(relay[0]['may']['time']),
 'interpretation_limits':['Candidate matches by words and surrounding sequence, not original event IDs.',
  'Printed-source arithmetic only; no accepted historical clock or cause.',
  'Both agreement and disagreement retained; no exhaustive event/word census claimed.',
  'Source images were separately inspected; source hashes do not authenticate historical assertions.']}
args.output.mkdir(exist_ok=False,parents=True)
for name,value in [('COMPARISONS.json',{'six_anchors':comparisons,'shared_candidates':shared_rows,'relay_candidates':relay}),
 ('EXCERPTS.json',excerpts),('REPRODUCIBILITY.json',summary)]:
 with(args.output/name).open('x')as f:json.dump(value,f,indent=2)
print(json.dumps({k:v for k,v in summary.items()if k not in ['source_checks','interpretation_limits']},indent=2))

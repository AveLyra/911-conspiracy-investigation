"""Literal E8 source reading; no pixel-selection algorithm."""
import argparse
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
PINS={
 'PROTOCOL.md':'98edc562841efdbc3ffb7f25c813b507cf553142a972f5558680e7218f7e6e25',
 '../PROTOCOL.md':'2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
 '../REGIONS.json':'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
 'read_context.py':'377d4f41b990502ca87fc7d1b4b9b069eede0aa71f281c68cb5ae879d7196a2c',
 'context01.json':'0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
 'context02.json':'0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
 '../../native-strips01/Im7.jpg':'3509c0fb002d47d1cc9d1ae624377534c8b31bd9fea7fdadd380a7b5f4d4a09d',
 '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}
# Inclusive manual ranges: first/last column, explicit core and fringe rows.
SOLID=[(535,538,[77],[76,78]),(539,541,[76,77],[75,78]),
 (542,547,[76],[75,77]),(548,551,[75,76],[74,77]),
 (552,559,[75],[74,76]),(560,563,[74,75],[73,76]),
 (564,575,[74],[73,75]),(576,588,[73,74],[72,75]),
 (589,595,[73,74],[72,75]),(596,618,[73],[72,74,75]),
 (619,634,[73,74],[72,75]),(635,689,[73],[72,74,75])]
# A separate ID for each visible dash. Early bodies bend across row levels.
DASH=[
 [(535,535,[74,75],[73,76]),(536,537,[74],[73,75])],
 [(540,541,[72],[71,73]),(542,543,[71],[70,72]),(544,546,[70,71],[69,72])],
 [(549,550,[68,69],[67,70]),(551,552,[68],[67,69]),(553,555,[67],[66,68])],
 [(559,559,[66],[65,67]),(560,562,[65],[64,66]),(563,564,[64,65],[63,66])],
 [(568,571,[63,64],[62,65]),(572,574,[63],[62,64])],
 [(577,583,[62],[61,63])],[(587,592,[62],[61,63])],
 [(596,601,[62],[61,63])],[(605,611,[62],[61,63])],
 [(614,620,[62],[61,63])],[(624,629,[62],[61,63])],
 [(633,639,[62],[61,63])],[(642,648,[62],[61,63])],
 [(652,657,[62],[61,63])],[(661,667,[62],[61,63])],
 [(670,676,[62],[61,63])],[(679,685,[62],[61,63])],
 [(688,689,[62],[61,63])]]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def flags(x,ys):
 return (['target_left'] if x==535 and ys else [])+(['target_right'] if x==689 and ys else [])+(['target_top'] if 54 in ys else [])+(['target_bottom'] if 85 in ys else [])
def rec(x,c,f,fid):
 fs=flags(x,c+f)
 return dict(x=x,core=list(c),fringe=list(f),fragment_id=fid,boundary_flags=fs,
  status='boundary_truncated' if fs else 'identified_local_fragment' if c else 'no_attributable_cells',
  note='Locally identifiable cyan stroke: continuous lower piece is solid/spring, discrete upper pieces dashed/shell by full-strip style and page legend, not height alone.' if c else 'Inspected pale interbody material not assigned; empty selection does not establish true gap or absence.',
  unassigned_band_refs=[])
def build():
 routes={k:[rec(x,[],[],None) for x in range(535,690)] for k in ('solid','dash')}
 for a,b,c,f in SOLID:
  for x in range(a,b+1):routes['solid'][x-535]=rec(x,c,f,'E8-independent-solid')
 for i,pieces in enumerate(DASH,1):
  for a,b,c,f in pieces:
   for x in range(a,b+1):routes['dash'][x-535]=rec(x,c,f,f'E8-independent-dash-{i:02d}')
 # At x535 tentative edges meet at row76. Preserve that contact once, not
 # as two attributed model cells. This is a literal manual identity decision.
 routes['solid'][0]['fringe']=[78]
 routes['dash'][0]['fringe']=[73]
 for k in routes:routes[k][0]['unassigned_band_refs']=[{'x':535,'band_id':'E8-independent-contact'}]
 bands=[dict(x=535,band_id='E8-independent-contact',core=[],fringe=[76],boundary_flags=['target_left'],
  competing_identities=['solid edge','dash edge','overprinted/compression edge'],
  note='Tentative contact cell between separately visible strokes; no unique model attribution.')]
 return dict(pair='E8',reader='curve_recovery_feasibility, independent prior-informed AI reader',pins=PINS,
  annotation_script_sha256=sha(Path(__file__)),target_box=[535,54,690,86],context_box=[533,52,692,88],
  coverage=dict(context_cells=5724,model_route_records=310,full_native_strip_viewed=True,full_composed_page_viewed=True,
   page_display='1700x2200 reduced to1376x1780; context only, coordinates from RGB',
   blocks=[{'first':533,'last':572,'receipt':'9b3428'},{'first':573,'last':612,'receipt':'78ca9b'},
    {'first':613,'last':652,'receipt':'2889b4'},{'first':653,'last':691,'receipt':'bd82ef'}],rows_inclusive=[52,87],all_blocks_untruncated=True),
  method='All raw context cells read after unchanged full strip/page viewing. Only exact white omitted by display. Literal manual runs mechanically expanded, no RGB classifier, threshold, interpolation, guessed centerline or selected margin. RGB used only for pre-freeze transcription diagnosis.',
  independence='Prior source/locator/method knowledge shared; not blind, human reviewed or independent historical evidence. No current other E8 annotation read before freeze.',
  limits=['Uncalibrated visible-ink core/fringe, not original mathematical curve containment.',
   'Pale unselected material remains unresolved, not excluded curve support. Discrete IDs do not establish physical dash endpoints.',
   'One tentative contact cell kept separate; no band duplication or automatic seam joins.',
   'No physical ordinates, discrepancy metric, supported domain, human acceptance or causal claim.'],
  freeze_status='Deterministic separate reading; actual execution time reported externally with hash.',routes=routes,unassigned_bands=bands,human_accepted=False)
def verify(a):
 cells={(r['x'],r['y']):r['rgb'] for r in json.loads((HERE/'context01.json').read_text())['cells']['E8']}
 assert len(cells)==5724
 white=[]
 for records in list(a['routes'].values())+[a['unassigned_bands']]:
  for r in records:
   c,f=r['core'],r['fringe'];assert c==sorted(set(c)) and f==sorted(set(f)) and not set(c)&set(f)
   assert all(54<=y<86 for y in c+f);assert r['boundary_flags']==flags(r['x'],c+f)
   white += [(r['x'],y) for y in c+f if cells[r['x'],y]==[255,255,255]]
 assert not white,white
 for rs in a['routes'].values():assert [r['x'] for r in rs]==list(range(535,690))
 for s,d in zip(a['routes']['solid'],a['routes']['dash']):
  assert not set(s['core']+s['fringe'])&set(d['core']+d['fringe'])
  for b in a['unassigned_bands']:
   if b['x']==s['x']:assert not set(b['core']+b['fringe'])&set(s['core']+s['fringe']+d['core']+d['fringe'])
 for rs in a['routes'].values():
  for r in rs:
   for ref in r['unassigned_band_refs']:assert any(b['x']==ref['x']==r['x'] and b['band_id']==ref['band_id'] for b in a['unassigned_bands'])
 a['verification']={'selected_exact_white':white,'coverage_bounds_classes_references_duplicate_assignment':'passed','pre_freeze_failures':[],'automatic_selection_repairs':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True,choices=['reader-E8-independent.json','reader-E8-independent-repeat.json']);args=p.parse_args()
 for name,h in PINS.items():assert sha(HERE/name)==h,name
 a=build();verify(a);target=HERE/args.output
 with target.open('x') as f:json.dump(a,f,indent=2);f.write('\n')
 print(json.dumps({'sha256':sha(target),'script_sha256':sha(Path(__file__)),'records':310,'context_cells':5724}))

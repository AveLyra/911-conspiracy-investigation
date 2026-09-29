# R1 numerical-input source and preserved-control recheck

2026-09-27 UTC. Research only. Separate checker: `/root/curve_source`.
**Assigned source/synthetic-integrity prerequisite: PASS.** The actual read-only
check returned exit 0 on Python 3.14.0. All 32 pinned inputs remained unchanged
through the check. This is not approval of numerical results or a causal claim.

## Scope and result

Read the execution declaration, frozen protocol, prior source check, human
intake, and localization protocol/observer/verification records. Main controls
and charter had been read in this ongoing session; all four current hashes
match their prior pins. Applicable evidence-falsification and source-of-truth
controls were retained. This checker is prior-informed and has earlier source
and methodological roles; it is not a blind or historically independent source.

The full executed command below records all exact input paths, SHA-256 pins
and checked sizes. Its assertions establish:

- Both 242-row selected maps are byte-identical and enumerate source indices
  239–480 exactly once. Both held whole-source PTS inventories and the
  upstream inventory are byte-identical, each with 1,350 integer, strictly
  increasing PTS rows matching `best_effort_timestamp`.
- For the six fixed indices **239, 434, 441–444**, both maps join the zero-based
  whole-source inventory exactly. The twelve selected PTS/time-base/exact-time
  joins pass using rational arithmetic and time base 1/30000.
- All **twelve** corresponding PNGs match their own size/hash pins, selected
  map entries and receipt product entries. Paired run02/run03 PNG bytes are
  equal. Each signature/IHDR declares 1280×720, 8-bit RGB, noninterlaced.
  No PNG decompression, pixel verification, CRC/chunk inventory or display
  occurred.
- Both receipts report complete/242 historical frames; the actual held
  4,901,052-byte video matches both source-before/source-after records.
  Product membership was checked for six PNGs and two metadata products
  **per run**, not every receipt product or every one of 242 PNGs.
- The execution declaration, original protocol, human-intake record and all
  five pinned localization-control inputs match their declared hashes.
  The synthetic fixture's size/hash/IHDR and truth's builder/fixture/protocol
  identities match; its pixel geometry was **not freshly verified**.
- Parsing the preserved observer table against literal saved truth gives A:
  y=181 in [175,188], width13; B: y=457 in [451,464], width13; C: y=594 in
  [588,602], width14. All three contain the target y and meet high−low≤24.

All 32 input byte strings were reread and found unchanged at the end. There
were no failed assertions, command errors or mismatches in this recheck.
A metadata-only schema inspection preceded this command; no new script,
image derivative or arithmetic result artifact was created.

## Gate meaning and exclusions

The preserved synthetic pass is an arithmetic recheck of the previously
frozen one-image/one-AI-reader control, not another localization experiment.
The prior geometry verification remains attributable to
[localization-verification.md](localization-verification.md), not to a fresh
pixel check here. The A “top-left” wording ambiguity remains a control-design
limitation; the frozen observer expressly selected the left roof/wall junction.

The human record's **y-only inclusive ±1 native-pixel** interpretation remains
separately attributed, non-statistical, and distinct from the frozen AI
ranges. This recheck pinned that record; it did **not** repeat all 36
human-envelope/AI-band membership checks. The human mapping gate's documented
disposition is separate from the source and preserved-synthetic checks here.
No AI bands were replaced, narrowed or reinterpreted.

Integrity is not authenticity. The preserved video is a project-attributed
platform access copy, not an authenticated native camera original. Matching
maps/receipts or repeat bytes can preserve common upstream or extraction
errors. The earlier decoder/colorspace notices and network-route limitation
recorded in [source-check.md](source-check.md) are not erased. Encoded PTS
coordinates are not authenticated exposure times. Header checks do not prove
a single-frame/no-APNG contract or pixel-to-video correspondence.

No old numerical claim, root/oracle motion output, new displacement,
historical motion result, stationary-reference assumption, physical onset,
device timing, gravity or WTC7 cause was assessed. There was no image
decode/display, new source acquisition, source change, or legal promotion.
Numerical adapter controls, independent arithmetic and outcome comparison
remain other workers' separate execution gates. This note does not authorize
the separate pending observation-readiness matrix saves.

## Actual executed command

Working directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Only Python standard-library read operations, assertions and stdout were used.

```sh
python3 -B - <<'PY'
from pathlib import Path
from fractions import Fraction
import hashlib, json, struct, re, platform
M=Path('/Users/admin/docs/911')
B=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation')
D=B/'comparator-r1-replication'
R=B/'comparator-roof-onset'
pins={}
def add(path, sha, size=None):
    pins[path]=(sha,size)
for rel,sha in {
 'AGENTS.md':'01e3fbd03120a2085520818cea0a843a8c6748b4c7bb8ef0e68547c634a963cc',
 'WORKFLOW.md':'17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a',
 'START-HERE.md':'30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72',
 'research/sherlock-wtc7-investigation/CHARTER.md':'54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd'
}.items(): add(M/rel,sha)
for rel,sha,size in [
 ('EXECUTION-2026-09-27.md','16533732f0d4a9e02b295d46398e5c5fbe8b04f9250dd2eb8130c3373fd86f1f',None),
 ('PROTOCOL.md','2bbc5777dd39dde42a2945d1d049a1a46f8c4b61678308e328e803f0ffa2331a',None),
 ('human-observations-2026-09-26.md','c7714d0abad6d9806a9f3f4a80abacdf9f6404b6ad11cc59b26b2429e45c842d',None),
 ('build_localization_control.py','051fe73a9986861a60a85d1eb46cd6e6e99ed4d75beb770abbbcd5b4b2c3be1a',2258),
 ('localization-control.md','12acb3639864d22e7fdc3a6653229a71f26e38a16680b384283298407dcfc15b',2152),
 ('localization-control/fixture.png','f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48',11216),
 ('localization-control/truth.json','d9fcad8bf01b01ab3e2b2675ac2ee145cbe0e1f4456f930184ab95b98d028bb2',621),
 ('localization-observer.md','3bce051c29a2da12bb8364ac8f3a4622817d32ae39400e358d5f58f67a8455a7',2704)
]: add(D/rel,sha,size)
video=M/'research/wtc7-video-comparison/media/comparators/explosive/Capital One Tower Implosion [rW_xXcS4y3A].f136.mp4'
add(video,'8560cd686a18c8fcc16fe802691e0f17f117c713b4cd1862017af24d391ce5a2',4901052)
mapsha='14c72246559d79812c1eef4b42d977c64d1f28bc97d0f034a945cddb8db5561a'
ptssha='d8496f26d271eda8955e0fc46b3ff98754c2b5bc06793e8729adf0840a387c3b'
frames=[
 (239,'frame-0001.png',239239,'239239/30000',881140,'9f8d2878a69952da6d4a1e31f3a58415c9271c19e95160b28674692f5fb0439f'),
 (434,'frame-0196.png',434434,'217217/15000',922606,'cbd2078df347521154157ae7c3b637585d3196cd3b1d1398ccc19be00cacacc5'),
 (441,'frame-0203.png',441441,'147147/10000',927384,'13c3d28ee22e129de4de3030cb2d9543079518b766f01487bf43694cdbf0f95f'),
 (442,'frame-0204.png',442442,'221221/15000',928276,'62f63c6b6f912cc4d5f859175dbd7b8da987dc6a440bd0f17366b803c02bea68'),
 (443,'frame-0205.png',443443,'443443/30000',927885,'d64ec51cf17c6df8254446b642cef0542612e509245539b010c1bc8d473f80b3'),
 (444,'frame-0206.png',444444,'37037/2500',927123,'4679ce4d4e6634ac5721e36abc328ff11e75fa8eb57e468f6d390cf8c2200491')
]
for run,sha in [('run02','e17b37b98c136ba81c79c70ccd03f4b709b127507fd5c6111c5b217b2a14856c'),('run03','e7f2303079ad3810ccab88d403eb548a71b05db9bdb5f4e595e043bfdfcd4f28')]:
 add(R/run/'receipt.json',sha,70641)
 add(R/run/'comparator-selected.json',mapsha,98723)
 add(R/run/'comparator-all-frame-pts.json',ptssha,193227)
 for i,name,pts,seconds,size,sha in frames: add(R/run/'comparator'/name,sha,size)
upstream=M/'research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/run01/comparator-all-frame-pts.json'
add(upstream,ptssha,193227)
data={}
for p,(sha,size) in pins.items():
 raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==sha, ('pin',str(p))
 assert size is None or len(raw)==size, ('size',str(p))
 data[p]=raw
def ident(p): return {'bytes':len(data[p]),'sha256':hashlib.sha256(data[p]).hexdigest()}
def header(raw):
 assert raw[:8]==b'\x89PNG\r\n\x1a\n'
 assert struct.unpack('>I',raw[8:12])[0]==13 and raw[12:16]==b'IHDR'
 return struct.unpack('>IIBBBBB',raw[16:29])
maps=[json.loads(data[R/r/'comparator-selected.json']) for r in ('run02','run03')]
assert data[R/'run02/comparator-selected.json']==data[R/'run03/comparator-selected.json']
inventories=[json.loads(data[p])['frames'] for p in [R/'run02/comparator-all-frame-pts.json',R/'run03/comparator-all-frame-pts.json',upstream]]
assert data[R/'run02/comparator-all-frame-pts.json']==data[R/'run03/comparator-all-frame-pts.json']==data[upstream]
for rows in maps:
 assert len(rows)==242 and [r['source_index'] for r in rows]==list(range(239,481))
for inv in inventories:
 assert len(inv)==1350
 assert all(type(r['pts']) is int and r['pts']==r['best_effort_timestamp'] for r in inv)
 assert all(a['pts']<b['pts'] for a,b in zip(inv,inv[1:]))
for run,rows,inv in zip(('run02','run03'),maps,inventories):
 receipt=json.loads(data[R/run/'receipt.json'])
 assert receipt['status']=='complete' and receipt['historical_frames']==242
 assert receipt['source_path']==str(video)
 assert receipt['source_before']==receipt['source_after']==ident(video)
 for name in ('comparator-selected.json','comparator-all-frame-pts.json'):
  assert receipt['products'][name]==ident(R/run/name)
 for i,name,pts,seconds,size,sha in frames:
  row=next(r for r in rows if r['source_index']==i)
  assert row['png']=='comparator/'+name
  assert row['source_pts']==pts==inv[i]['pts']
  assert row['source_time_base']=='1/30000'
  assert Fraction(row['source_seconds_exact'])==Fraction(seconds)==pts*Fraction(row['source_time_base'])
  assert row['source_seconds']==float(Fraction(seconds))
  p=R/run/'comparator'/name
  assert {'bytes':row['bytes'],'sha256':row['sha256']}==ident(p)
  assert receipt['products'][row['png']]==ident(p)
  assert header(data[p])==(1280,720,8,2,0,0,0)
for i,name,pts,seconds,size,sha in frames:
 assert data[R/'run02/comparator'/name]==data[R/'run03/comparator'/name]
truth=json.loads(data[D/'localization-control/truth.json'])
assert truth['synthetic_only'] is True and truth['not_a_historical_localization_calibration'] is True
assert truth['dimensions']==[1280,720]
assert truth['fixture']==ident(D/'localization-control/fixture.png')
assert truth['builder']==ident(D/'build_localization_control.py')
assert truth['protocol']==ident(D/'localization-control.md')
assert header(data[D/'localization-control/fixture.png'])==(1280,720,8,2,0,0,0)
matches=re.findall(r'^\| ([ABC]) \| localizable \| \[(\d+), (\d+)\] \|',data[D/'localization-observer.md'].decode(),re.M)
assert len(matches)==3 and {s for s,lo,hi in matches}=={'A','B','C'}
synthetic=[]
for s,lo,hi in matches:
 lo,hi=int(lo),int(hi)
 x,y=truth['points'][s]
 assert lo<=y<=hi and hi-lo<=24
 synthetic.append({'shape':s,'literal_truth':[x,y],'envelope':[lo,hi],'width_high_minus_low':hi-lo,'pass':True})
for p,raw in data.items(): assert p.read_bytes()==raw, ('changed_during_check',str(p))
print(json.dumps({'status':'PASS_SCOPED_SOURCE_AND_PRESERVED_SYNTHETIC_GATE','python':platform.python_version(),'pinned_files':len(data),'unchanged_files':len(data),'selected_rows_per_map':242,'whole_source_rows_per_inventory':1350,'inventories':3,'historical_pngs_byte_header_checked':12,'selected_clock_joins':12,'receipt_membership_per_run':'six PNG plus two metadata products','synthetic_header_only':True,'synthetic_saved_envelopes':synthetic,'displacement_calculations':0,'image_decodes_or_displays':0},sort_keys=True))
for p in pins: print(str(p), json.dumps(ident(p),sort_keys=True))
PY
```

Exit: **0**. Exact first result line:

```json
{"displacement_calculations": 0, "historical_pngs_byte_header_checked": 12, "image_decodes_or_displays": 0, "inventories": 3, "pinned_files": 32, "python": "3.14.0", "receipt_membership_per_run": "six PNG plus two metadata products", "selected_clock_joins": 12, "selected_rows_per_map": 242, "status": "PASS_SCOPED_SOURCE_AND_PRESERVED_SYNTHETIC_GATE", "synthetic_header_only": true, "synthetic_saved_envelopes": [{"envelope": [175, 188], "literal_truth": [521, 181], "pass": true, "shape": "A", "width_high_minus_low": 13}, {"envelope": [451, 464], "literal_truth": [283, 457], "pass": true, "shape": "B", "width_high_minus_low": 13}, {"envelope": [588, 602], "literal_truth": [1041, 594], "pass": true, "shape": "C", "width_high_minus_low": 14}], "unchanged_files": 32, "whole_source_rows_per_inventory": 1350}
```

The command also printed the 32 checked paths with actual byte sizes and
SHA-256 values; the explicit pins and paths are preserved in the command above.


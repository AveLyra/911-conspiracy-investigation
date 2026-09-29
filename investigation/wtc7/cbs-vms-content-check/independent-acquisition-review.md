# Independent candidate-lineage and pre-admission review

September 20, 2026 UTC / September 19 local. Initial stage by
`/root/ap_catalog_source`, full-reasoning review. **Actual acquisition receipt,
new source bytes, diagnostics and historical samples have not been inspected
by this reviewer.** Root will supply those for an append-only follow-up.

## Result and authority

The protocol selects the exact previously observed candidate and correctly
calls it an **Other-category** item. Its acquisition and claim boundaries are
appropriately narrow. The remaining method details below should be explicit
in the post-probe, pre-viewing plan; this is not approval of unrun diagnostics
or permission to expand retrieval.

Read the current main AGENTS.md, WORKFLOW.md, START-HERE.md, full investigation
CHARTER and this unit's complete PROTOCOL. Applied repo-orchestrator,
evidence-falsification-auditor and source-of-truth-guardian, including their
applicable references. Intake confirms branch research/sherlock-wtc7-investigation
at e8d83d7, with pre-existing/concurrent research changes. Only this working
research note is a write target; no canonical/source/frozen/engine/legal state
is changed. The skills require separating preserved metadata, prospective
checks and historical inferences; they do not impose another approval gate
on already authorized bounded research.

## Rechecked source chain

Reparsed all ten prior JSON files for other-list, cd-list, cdvideo-list,
analysis-list and cbsvms-metadata (request and response for each), and reread
the NIST category markup at lines 684–724. Every descendant request URL exactly
equals its parent listing's returned URL, with the expected ID and title.

| Stage | Exact identifier |
|---|---|
| Other Photos and Videos, official anchor line 712 / caption 721 | `1RGlFysE_IIBXDb_hGtk_XmAKEKYq0L5r` |
| PhotosAndVideoFromCDorDVD | `1G7Ko0Nf1TZNJFb_WjA7PEjUTHpd5eCN_` |
| Video | `1GAo8-t_O6CyfBPqwCOfCyAERyZkY1Nth` |
| WTCI-134-I WTC7 Analysis Videos | `1S41RVzRrbTj3ChYhPz9pMb5Tc-IEjTyB` |
| CBS-VMS-Wtc7.wmv | `1Iiw99TkBywBLRXvHAekU1Y0DKV85sFBo` |

The official anchor uses googledrive.nist.gov; the recorded listing request
uses drive.google.com with the same folder ID. This is grounded ID continuity,
not an observed redirect. The distinct **Original Video from Tapes** anchor
at line 700 is `12vUikS9WpbovdIWwLAIqI7rSKDE4WMRQ`; it is not this path.

Candidate listing and exact metadata agree on eight fields: id, title,
mime_type=`video/x-ms-wmv`, size=`8717690`, url, display_url,
file_or_folder=`file`, and modified_time=`2019-11-26T03:57:36.800Z`.
Exact item URL:
`https://drive.google.com/file/d/1Iiw99TkBywBLRXvHAekU1Y0DKV85sFBo/view?usp=drivesdk`.
The date is catalog metadata, not a historical capture clock.

Do not claim complete metadata equality: listing created_time/shared become
null in exact metadata, and listing capability fields are absent there.
Requested md5Checksum is not returned; parent_ids is null. Parent-scoped
request/response context supports traversal, not independently populated
parent fields. Five response envelopes say isError=false; that is a captured
tool status, not independent provider attestation. Neither the NIST category,
filename, MIME nor size authenticates a camera master, CBS authorship or a
relationship to Dub5/Release 25. Missing pagination and untouched branches
preclude an exhaustive-public-search claim.

## Concrete diagnostic/selection risks to resolve before admission

1. **Bind retrieval to the selected bytes.** In the receipt, connect refreshed
   metadata and the connector-returned materialized file to this exact ID;
   compare received size with 8,717,690 and pin the acquired hash. If identity
   or size changes, preserve the discrepancy for assessment rather than
   silently updating expectations. An authenticated access reference concerns
   access, not historical authenticity; do not persist credentials.
2. **Specify the sampled stream and time convention.** Before viewing, name
   the selected video stream, decoded-frame index convention, integer PTS and
   rational time base, and whether the two-second grid begins at the first
   presentation timestamp or another declared origin. Define missing,
   duplicate or nonmonotone timestamp handling, ties and endpoint deduplication.
   Set the exact increased step and resulting unique-frame count so endpoints
   cannot silently push the initial set beyond 80. Do not use nominal fps as
   a substitute for observed timestamps.
3. **Check complete output, not repeated hashes alone.** Reconcile both full
   decode inventories' counts/order/timestamps against the probe inventory,
   retaining unexpected differences and boundary gaps. Record stream mapping,
   decoder/runtime versions, decoded pixel format and all process statuses.
   The same decoder can repeat the same error; two equal inventories establish
   repeatability only. The protocol's warning/error stop must apply to probe,
   full decode and sample extraction, without importing the older DV helper's
   clean-log verdict as WMV validation.
4. **Keep representation limits visible.** Pin native dimensions, sample aspect
   ratio and interlace flags and the output PNG/pixel hashes. No aspect
   resampling means raw pixel geometry may differ from intended display
   geometry; no deinterlacing preserves possible combing. Color conversion and
   compression can affect orange/flame-like appearance. These limitations do
   not forbid qualitative screening, but do forbid treating apparent shape,
   brightness or color as calibrated physical measurements.
5. **Keep the synthetic control's claim narrow.** It should test the actual
   selection/extraction path, expected indices and pixel correspondence,
   including the applicable endpoint/time-grid rules. Passing verifies those
   operations on known inputs; it cannot certify the historical WMV's decoder
   correctness, completeness or source lineage. Any untested timestamp case
   must remain a stated limitation rather than an implicit pass.
6. **Preserve independent observation scope.** Freeze each standalone sample
   description before exchanging conclusions or showing comparison anchors.
   Record any exposure deviation. A two-second/capped grid can miss a short
   target scene or edit, so report mismatch only for viewed samples. A scene
   match is not a continuous-source or clock match; denser follow-up needs its
   own declared coverage. Human/specialist acceptance remains unperformed.

These are specific plan/receipt checks, not requests for broader searches,
additional media, software changes or quantitative historical measurements.

## Claim assessment and strongest objection

- **A, retained-record observation:** this precise catalog candidate is
  identified through the Other branch, with matching eight-field metadata.
- **Pending:** acquisition identity, usable decode and sample correspondence;
  this reviewer has not inspected their new evidence yet.
- **Unsupported here:** whole-file target absence, camera origin, unedited
  continuity, historical clock, fire duration/temperature or cause.

The strongest alternative is another scene or an edited/re-encoded analytical
replay despite the CBS/WTC7 title. A positive sparse match could also be a
short inserted excerpt with no missing pre-onset context. Exact source bytes,
clean diagnostic records and scene inspection can test narrower propositions;
none alone supplies the historical tape/clip crosswalk.

## Verification record and pins

Ran repository intake (exit 0); complete control/skill reads; the local inline
Python JSON audit (exit 0, three exact descendant joins, official entry-ID
check, eight-field comparison and normalization differences); and SHA-256
checks (exit 0). No network, decode or image display was used. Source pins for
all ten JSON inputs agree with the prior audit's table and executable recipe
in [independent-provenance](../late-fire-original-tape-catalog/independent-provenance.md),
SHA-256 `b78f2d66c1ff36d042657a75c38c9dbb8359dd4c7b61d834912cdf51362af0b6`.
That earlier wider audit is not silently rerun or expanded here.

| Input | SHA-256 |
|---|---|
| This unit's PROTOCOL.md | `9e14734660f2f3223f00dd0bbbe10d61bc2d8a82d2cb7afce0af32f9c4a4db35` |
| Preserved NIST repository HTML | `af73969464f1d1a32fb96b169af129a21fd6781cdc18766c26d203bb0dfc5dfa` |
| analysis-list.response.json | `2c6a1dd87bf581a970979cd7f88b563c9fa7f8e26b6e5753d9b61be702b37145` |
| cbsvms-metadata.response.json | `accb9bb106221753202894d54a7aeb62d5778fb4828c07f53665e708d075c514` |

Follow-up remains explicitly pending: inspect the actual refreshed metadata,
receipt and diagnostics supplied by root, preserving this initial review.

## Follow-up: acquired bytes and initial diagnostics independently reconciled

September 20, 2026 UTC / September 19 local. This supplement preserves the
initial 8,749 bytes (SHA-256
`87eda3888d0a2c7c580d8ea5c0491dd1d88c989e9fd38ba0e1e43e3c4b1ef877`).
No video decoding, playback or historical image display was performed by this
reviewer. The development-verification skill was read/applied to the bounded
code review; it did not authorize implementation or substitute successful
execution for substantive acceptance.

### Acquisition evidence and credential caveat

The fresh normalized metadata is identical to the prior exact metadata.
Its request uses the selected ID. The raw fetch request uses the observed
item URL, download_raw_file=true and include_base64=false. The saved redacted
response agrees on ID, filename, MIME and 8,717,690 bytes, and retains the
connector's opaque materialized-file reference. The temporary download URL
is redacted in both nested response locations; no base64 body was saved.

Independently read/hash-checked the local regular, non-symlink WMV:
**8,717,690 bytes**, SHA-256
`bae07b52bc85c735c72b227b55a327da3a49c6bf6a0798ccc9d85602dae185ad`.
That matches both source-before/source-after identities in the diagnostic
receipt. This verifies current local bytes and consistency of the captured
acquisition chain, not a provider-supplied checksum or camera authentication.

Root reports HTTP 200 retrieval using the connector-returned temporary URL
through standard input with no-clobber. Those transport details and retrieval
time were not independently reconstructed from the presently inspected
metadata/fetch/diagnostic records. Root also reports that an initial tool-result
echo exposed the signed temporary URL in tool output. **Do not claim zero
tool-log exposure.** This review uses the saved redacted response and neither
repeats that URL nor certifies a repository-wide secret scan. Redaction of the
saved response does not erase the earlier tool-output exposure.

### Code and process review

Read inspect_candidate.py fully and all 377 lines of the imported
sample_sequence.py; parsed both with ast.parse without importing/executing
them. The new script uses the prior capture/identity/save utilities but never
calls its DV/FFV1 log grammar or sampling admission function. It records current
code hashes rather than importing a prior scientific acceptance flag. New
output directories/files are exclusive; source identity is checked before/after.

The script's main() does not turn a refused/needs-review receipt into a nonzero
Python exit. Therefore the wrapper's exit alone cannot be an acceptance test.
Its saved per-process statuses and final receipt are the relevant evidence;
no code was changed. The receipt correctly says
`diagnostics_require_review`, `all_processes_zero_stderr_empty=false`,
`repeat_stdout_identical=true`, scientific_or_human_acceptance=false.

Checked all six exact argument records, six statuses, six stdout and six
stderr files plus receipt: 25 diagnostic files. FFmpeg and ffprobe identify
version 7.1.1. All six subprocess return codes are 0 with no launch error.
Version/container/probe stderr are empty. Each RGB decode has **13 lines /
1,508 bytes** of stderr, all exactly the following vocabulary apart from
memory addresses:

`No accelerated colorspace conversion found from yuv420p to rgb24.`

The logs are not byte-identical because the addresses differ. No other
nonempty diagnostic text occurs in these two files. The wording concerns
availability of accelerated conversion; it is not by itself proof of pixel
accuracy, input corruption or historical editing. Equal decode outputs do not
clear the protocol's warning gate.

### All-frame reconciliation, not just receipt repetition

Independently parsed **4,531 probe frame rows and all 9,062 checksum rows**
across the two decodes, without calling the producer's inventory validator.

| Check | Result |
|---|---|
| Container/selection | ASF; audio stream 0 is WMAV2; selected v:0 is actual video stream **1**, WMV1, 320×240, yuv420p |
| Frame metadata | Every frame is stream 1, 320×240, yuv420p; interlaced_frame=0, top_field_first=0, repeat_pict=0 |
| Aspect ratio | Absent from both video-stream and all frame metadata; checksum header SAR=0/1. **Not a verified 1:1 SAR** |
| PTS | All integer, strictly increasing; time base 1/1000; all decimal pts_time values exactly agree; every pkt_dts and best_effort_timestamp equals PTS |
| Endpoints | PTS 33 to 302602 = 0.033 to 302.602 seconds; endpoint span 302.569 seconds, not an event/fire duration |
| Cadence | 3,321 gaps of 67 ticks; 1,207 of 66; one 267 and one 133 |
| Exceptional gaps | Indices 4301→4302: 287053→287320; 4302→4303: 287320→287453. No interpolation or historical explanation supplied |
| Frame durations | Probe duration absent for indices 0–40, then 66 ticks for 4,490 rows; checksum rows use 67 for those first 41, then 66 for 4,490. Do not silently present imputed early durations as source fields |
| Checksum mapping | Both inventories have 4,531 rows; each output DTS=PTS=corresponding probe PTS, output stream 0, raw RGB24 size 230,400 bytes; all rows have valid MD5 format |
| Repeats | Every corresponding checksum row matches; the entire 362,696-byte output files match; 4,531 distinct RGB MD5 values within each pass |

The stream records otherwise agree; the frame-probe record additionally has
nb_read_frames=4531, absent in the container-only probe. Container/stream
duration 303.102 seconds is not identical to the last decoded-frame timestamp
or endpoint span. These different quantities must not be silently equated or
converted into a claim that every original-camera instant survives.

### Disposition and next bounded check

The acquired identity and the above inventory consistency checks are supported.
**Image admission is not cleared by this supplement.** Root's newly saved
DIAGNOSTIC-REVIEW-PLAN.md was read: it proposes examining the exact installed
version's conversion fallback and a native-yuv420p repeated checksum pair.
That is a specific response to the retained warning; its proposed source read
and diagnostic outputs were not inspected or executed by this reviewer.
Native/YUV repeat hashes should be compared within that representation, with
counts/PTS reconciled to this probe; they need not equal RGB hashes.

No synthetic selection-control result, sample plan/product or historical
scene was reviewed here. Missing SAR, timestamp gaps, inferred durations and
conversion uncertainty remain explicit. Even subsequent computational access
clearance would not authenticate camera origin, original continuity, scene
identity or a clock.

### Actual checks, failure retained, and output pins

The first local audit exited 1 at a too-strict equality assertion comparing
the two stream dictionaries: show_frames adds nb_read_frames. After inspecting
that exact single-field difference, the final audit checked all shared fields
and separately checked nb_read_frames against the independently counted rows;
it exited 0. No acceptance criterion was relaxed for a data mismatch.
Syntax parsing, raw-byte hashing, all-row comparisons and receipt/status
reconciliation were read-only. No duplicate diagnostic run was started.

| Artifact | SHA-256 |
|---|---|
| inspect_candidate.py | `42357f7fff4d1ef993d1a87c66ee2734fedcf91b9581c282ca73490c25432969` |
| Imported sample_sequence.py | `c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d` |
| sources/metadata.request.json | `ae2bb61df7917f4f03722e10f2d1fe30d411c744241f77157b7148e838dc35b3` |
| sources/metadata.response.json | `accb9bb106221753202894d54a7aeb62d5778fb4828c07f53665e708d075c514` |
| sources/fetch.request.json | `2775ecc698e6b82151dc37593fe2a604360c121ce6c91cb2e9f2c4268611c393` |
| sources/fetch.response.redacted.json | `64e62ab63f544c68ebbf2c541eb1dd2d0d2f0c4620f8907235d3754494b08c41` |
| diagnostics/receipt.json | `bd4e427931c6d42be6f2f63494330ee0ebab1ac1c693057558cd4fcd5c533838` |
| diagnostics/probe.stdout | `100459eda24cd9cc2cfc401b1c8260d881ce52af4f52c888c8761eb440d945f4` |
| diagnostics/container.stdout | `db1406a09617a8c892bb343866bb8fcb35a2f383ead41f3690999a6101b773a8` |
| diagnostics/decode01.stdout and decode02.stdout | `7b1e98aaa8b2dc796f7aa5d0d734c5c3ca35e86f10d0c48ae2832c9d2da56c76` |
| diagnostics/decode01.stderr | `bb5610db330e2926ad9c9693d0086162daa948eca066cb0c5ee198c624848bfa` |
| diagnostics/decode02.stderr | `c20289975aed9bf8c1a486405aaf6bf6e98f534707c79f47bbbdf939e5ffbfa6` |

The final independent audit command, run from the worktree root:

```sh
python3 - <<'PY'
from pathlib import Path
from collections import Counter
from fractions import Fraction
import ast,json,re,hashlib
b=Path('research/sherlock-wtc7-investigation/cbs-vms-content-check'); d=b/'diagnostics'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=b/'sources/CBS-VMS-Wtc7.wmv'
identity={'bytes':source.stat().st_size,'sha256':sha(source)}
receipt=json.loads((d/'receipt.json').read_bytes())
assert source.is_file() and not source.is_symlink()
assert identity==receipt['source_before']==receipt['source_after']
assert identity['bytes']==8717690
print('SOURCE',identity)
script=b/'inspect_candidate.py'; parent=b/'../late-fire-sequence/sample_sequence.py'
ast.parse(script.read_text()); ast.parse(parent.read_text())
assert sha(script)==receipt['code_sha256'] and sha(parent)==receipt['parent_code_sha256']
print('CODE_PINS_MATCH',receipt['code_sha256'],receipt['parent_code_sha256'])
for step in receipt['steps']:
 name=step['name']; status=json.loads((d/(name+'.status.json')).read_bytes()); cmd=json.loads((d/(name+'.command.json')).read_bytes()); out=(d/(name+'.stdout')).read_bytes(); err=(d/(name+'.stderr')).read_bytes()
 assert step['returncode']==status['returncode'] and step['launch_error']==status['launch_error']
 assert len(out)==step['stdout_bytes'] and len(err)==step['stderr_bytes']
 print('PROCESS',name,status,len(out),len(err),'stdout_sha256',hashlib.sha256(out).hexdigest())
 if name.startswith('decode'):
  lines=err.decode().splitlines()
  pattern=r'\[swscaler @ 0x[0-9a-f]+\] \[swscaler @ 0x[0-9a-f]+\] No accelerated colorspace conversion found from yuv420p to rgb24\.'
  print('DIAGNOSTICS',name,len(lines),'exact_vocabulary_matches',sum(re.fullmatch(pattern,line) is not None for line in lines))
  assert all(re.fullmatch(pattern,line) for line in lines)
container=json.loads((d/'container.stdout').read_bytes()); probe=json.loads((d/'probe.stdout').read_bytes()); frames=probe['frames']; streams=probe['streams']
assert len(streams)==1 and streams[0]['index']==1 and streams[0]['codec_type']=='video'
v=streams[0]; tb=Fraction(v['time_base']); pts=[f['pts'] for f in frames]
assert all(type(p) is int for p in pts) and all(p<q for p,q in zip(pts,pts[1:]))
assert all(f['stream_index']==1 and f['media_type']=='video' for f in frames)
assert all((f['width'],f['height'],f['pix_fmt'])==(320,240,'yuv420p') for f in frames)
assert all(Fraction(f['pts_time'])==f['pts']*tb for f in frames)
print('STREAM',v)
print('FRAME_COUNT',len(frames),'FIRST_LAST_PTS',pts[0],pts[-1],'EXACT_SECONDS',str(pts[0]*tb),str(pts[-1]*tb),'SPAN',str((pts[-1]-pts[0])*tb))
print('PTS_DELTAS',dict(Counter(q-p for p,q in zip(pts,pts[1:]))))
print('FRAME_FIELDS',{k:dict(Counter(str(f.get(k,'ABSENT')) for f in frames)) for k in ['interlaced_frame','top_field_first','sample_aspect_ratio','duration','duration_time','repeat_pict']})
print('PROBE_TIME_FIELDS',{k:sum(f.get(k)!=f['pts'] for f in frames) for k in ['pkt_dts','best_effort_timestamp']})
print('CONTAINER_STREAMS',[(s['index'],s['codec_type'],s['codec_name']) for s in container['streams']])
cv=next(s for s in container['streams'] if s['index']==1)
print('STREAM_SCHEMA_DIFFERENCE',{k:[cv.get(k,'ABSENT'),v.get(k,'ABSENT')] for k in cv.keys()|v.keys() if cv.get(k,'ABSENT')!=v.get(k,'ABSENT')})
assert all(cv[k]==v[k] for k in cv) and set(v)-set(cv)=={'nb_read_frames'} and int(v['nb_read_frames'])==len(frames)
print('EXCEPTIONAL_GAPS',[(i,pts[i-1],p,p-pts[i-1]) for i,p in enumerate(pts) if i and p-pts[i-1] not in (66,67)])
parsed=[]
for name in ['decode01','decode02']:
 text=(d/(name+'.stdout')).read_text(); lines=text.splitlines(); hdr=[l for l in lines if l.startswith('#')]; entries=[l for l in lines if l and not l.startswith('#')]; rows=[]
 assert '#tb 0: 1/1000' in hdr and '#dimensions 0: 320x240' in hdr and '#codec_id 0: rawvideo' in hdr
 for line in entries:
  f=[x.strip() for x in line.split(',')]; assert len(f)==6 and re.fullmatch('[0-9a-f]{32}',f[5]); rows.append(tuple(map(int,f[:5]))+(f[5],))
 assert len(rows)==len(frames)
 for i,row in enumerate(rows):
  stream,dts,p,duration,size,h=row
  assert stream==0 and dts==p==pts[i] and size==320*240*3 and duration>0
 print('CHECKSUM',name,len(rows),'duration_counts',dict(Counter(r[3] for r in rows)),'unique_rgb_md5',len({r[5] for r in rows}),'same_as_probe_duration',sum(r[3]==frames[i].get('duration') for i,r in enumerate(rows)))
 parsed.append(rows)
assert parsed[0]==parsed[1] and (d/'decode01.stdout').read_bytes()==(d/'decode02.stdout').read_bytes()
assert receipt['repeat_stdout_identical'] is True and receipt['all_processes_zero_stderr_empty'] is False and receipt['status']=='diagnostics_require_review' and receipt['scientific_or_human_acceptance'] is False
prior=Path('research/sherlock-wtc7-investigation/late-fire-original-tape-catalog/sources')
meta=json.loads((b/'sources/metadata.response.json').read_bytes())['structuredContent']; old=json.loads((prior/'cbsvms-metadata.response.json').read_bytes())['structuredContent']
assert meta==old
fetch=json.loads((b/'sources/fetch.response.redacted.json').read_bytes())['structuredContent']; request=json.loads((b/'sources/fetch.request.json').read_bytes())
assert request['url']==meta['url']==fetch['url'] and request['download_raw_file'] is True and request['include_base64'] is False
assert fetch['id']==meta['id'] and fetch['file_size_bytes']==identity['bytes'] and fetch['b64_string'] is None
assert fetch['file_uri']['download_url']=='[temporary bearer URL redacted]'
print('METADATA_UNCHANGED_AND_FETCH_ID_SIZE_AGREE')
for p in [script,d/'receipt.json',b/'sources/metadata.request.json',b/'sources/metadata.response.json',b/'sources/fetch.request.json',b/'sources/fetch.response.redacted.json']:
 print('PIN',str(p.relative_to(b)),p.stat().st_size,sha(p))
print('AUDIT_COMPLETE: diagnostic warnings retained; no admission clearance')
PY
```

## Second follow-up: warning disposition and sample-product audit

September 20, 2026 UTC / September 19 local. The preceding 23,243 bytes remain
preserved, SHA-256
`a0a15b491cdef7866178e370fee9290c97f70c652f32722591fce1318d38e5f4`.
This stage read the newly pinned FRAME-PLAN, diagnostic-review plan, complete
sampler, relevant acquired C function, native diagnostic files and existing
sample products. It did not retrieve anything, re-decode video, render or
display images, or interpret historical imagery.

### Narrow warning disposition

Checked the acquired n7.1.1 yuv2rgb.c bytes against the FRAME-PLAN pin and read
the function around lines 561–638. In this source, an available accelerated
function returns before the warning. Otherwise the warning is logged and,
for the observed non-YUV422P input/RGB24 output combination, the switch returns
`yuv2rgb_c_24_rgb`. This supports classifying **this exact message** as a
missing-acceleration/software-fallback notice rather than a corrupt-frame
diagnostic. The version-tag source is not proof of the installed binary's
exact build, and no calibrated-color or universal decoder-correctness claim
follows.

Independently parsed both additional native-yuv420p inventories: **9,062 rows**
total, 4,531 each. Both statuses are 0/no launch error and both warning-level
stderr files are empty. Their commands differ from the original full RGB
command only in requested pixel format. Every row has the corresponding probe
PTS/DTS, the matching RGB-inventory duration and expected native frame size
115,200 bytes. Both native outputs match byte-for-byte and contain 4,531
distinct native MD5s. Native and RGB hashes were compared **within** format,
not incorrectly equated across formats.

The original receipt and both warned stderr hashes were rechecked unchanged.
Those runs remain warned. The specific subsequent assessment satisfies the
protocol's requirement for a warning assessment; it is not retroactive
conversion of those logs into empty/clean logs.

### Declared indices and actual products

Recomputed the target grid from first PTS 33 with integer arithmetic:
two seconds gives 153 distinct endpoint-inclusive samples; four seconds gives
77, the first positive two-second multiple below the 80-image cap. All 77
printed indices agree with the calculation. Missing/duplicate/decreasing PTS
are absent in this source. Endpoints, earliest-at-or-after selection,
deduplication and locator times all match the declared plan.

Audited **154 historical PNG instances** (77 in each run), numerically only:
every file has its recorded hash, RGB mode, native 320×240 dimensions, recorded
RGB SHA-256/MD5, and MD5 equality with the selected frame's full-stream RGB
checksum. Source index/order/filename/PTS and plan pins agree. Both runs'
frames.json and locators.json are identical; all image-file and pixel hashes
repeat. The full reference's 4,531 distinct RGB hashes strengthen the mapping
for these particular samples; they are not independent historical evidence.

Also checked all four existing synthetic PNGs: indices 0/60/120/124, 96×64,
solid red/green/blue/blue pixels, hashes, zero diagnostic lines and status 0.
This inspects the saved control products, not a new fixture extraction.
Constant-color spans cannot identify every frame uniquely, as the plan admits.

Isolated the sampler's actual diagnostic predicate using its parsed AST and a
minimal raising assertion stub, without importing its extraction module.
All six pure checks passed: unknown diagnostic, nonzero status and unapproved
fallback reject; approved exact fallback and empty successful stderr accept;
approved fallback plus an extra unknown diagnostic rejects. This independently
checks the three declared negatives plus three additional predicate cases,
not every possible malformed-log case.

### Consequential code review and limits

No consequential frame-selection or product-mapping defect was found for
these pinned runs. The script pins the source, computes deterministic indices,
requires exact-warning-only diagnostics, checks each PNG against its selected
full-stream checksum, and preserves exclusive output directories.

It is **not a standalone all-gates validator**: sample() does not itself require
a successful prior synthetic-control receipt, native diagnostic clearance or
the external warning-source review. Those are procedural prerequisites checked
in this record. Future use cannot infer them merely from its
descriptive_derivatives_only receipt. Likewise its saved probe/checksum inputs
must remain pinned/reconciled to the selected source; source hashing alone does
not authenticate arbitrary replacement reference files.

For this recorded source and products, the computational checks support
restricted descriptive screening under the exact warning disposition.
They do not supply a scene finding or human/scientific acceptance. Unknown
SAR, colorimetry, encoded timestamp gaps, sparse coverage and original-camera
continuity/timing limits remain unchanged.

### Verification scope and pins

First attempted the independent numeric audit with system Python; it exited 1
at import because Pillow was unavailable, before checking any rows/products.
Using the documented bundled runtime, the complete audit exited 0. It used
stdlib parsing/hashes and Pillow only to decode PNG bytes for numeric checks;
no image was displayed. No existing diagnostic script/control/extraction was
rerun, and no root source/code file was edited.

| Artifact | SHA-256 |
|---|---|
| FRAME-PLAN.md | `7985786b00611b5f478636c2bbebb978bd627efe8964d2fed26171a7cd897bc8` |
| DIAGNOSTIC-REVIEW-PLAN.md | `6daac9090bf4dd2ba1d109a086bc9d9e2225593f587ee87c1a1a048c797c93c0` |
| sample_candidate.py | `fa9c97bc0d82202a78c9010eda09cddb1292d236df2617f42f48368a48c02824` |
| sources/ffmpeg-n7.1.1-yuv2rgb.c | `f0a61e340defcbb193f51d9f8c7faed727cc89987d2786551f6a966458f8f29b` |
| Both native-diagnostics/decode*.stdout | `61857dd2e2742e128ce1b5fde30214c81d9e170843d80483100f3b191cdc5b62` |
| control01/receipt.json | `eabed1c7097e2c7668f273b27d13ba8dbdb233e6d4e0583be65c0e604f73f3be` |
| run01/receipt.json and run02/receipt.json | `b50a16a2bdeae7351fa0bcbd17fb9999f9e208ef087857a7ac0a4285ea08ba72` |
| run01/frames.json and run02/frames.json | `0137dd6f05624c68f783dbc463d11ceddaae15957a9db96095c2578930a83324` |
| run01/locators.json and run02/locators.json | `8776c554547e3d8e42a6950b78ac9cf9837f9a6722fe7c9ee05e3b59b3704c27` |

Reproducible independent numeric audit (worktree root):

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 - <<'PY'
from pathlib import Path
from collections import Counter
import ast,bisect,hashlib,json,re,types
from PIL import Image
b=Path('research/sherlock-wtc7-investigation/cbs-vms-content-check'); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest(); read=lambda p:json.loads(p.read_bytes())
probe=read(b/'diagnostics/probe.stdout'); pts=[f['pts'] for f in probe['frames']]
assert len(pts)==4531 and all(type(x) is int for x in pts) and all(a<c for a,c in zip(pts,pts[1:]))
def sums(p):
 lines=p.read_text().splitlines(); rows=[]
 for line in lines:
  if not line or line.startswith('#'): continue
  f=[x.strip() for x in line.split(',')]; assert len(f)==6 and re.fullmatch('[0-9a-f]{32}',f[5]); rows.append(tuple(map(int,f[:5]))+(f[5],))
 assert len(rows)==4531
 return rows
rgb=sums(b/'diagnostics/decode01.stdout'); native=[]
oldcmd=read(b/'diagnostics/decode01.command.json')
for name in ['decode01','decode02']:
 d=b/'native-diagnostics'; status=read(d/(name+'.status.json')); err=(d/(name+'.stderr')).read_bytes(); command=read(d/(name+'.command.json'))
 assert status=={'launch_error':None,'returncode':0} and err==b''
 expected=oldcmd.copy(); expected[expected.index('-pix_fmt')+1]='yuv420p'; assert command==expected
 rows=sums(d/(name+'.stdout'))
 assert all(r[0]==0 and r[1]==r[2]==pts[i] and r[3]==rgb[i][3] and r[4]==115200 for i,r in enumerate(rows))
 native.append(rows); print('NATIVE',name,len(rows),status,'stderr',len(err),'unique_hashes',len({r[5] for r in rows}),'sha',sha(d/(name+'.stdout')))
assert native[0]==native[1] and (b/'native-diagnostics/decode01.stdout').read_bytes()==(b/'native-diagnostics/decode02.stdout').read_bytes()
plan=b/'FRAME-PLAN.md'; plan_hash=sha(plan); assert plan_hash=='7985786b00611b5f478636c2bbebb978bd627efe8964d2fed26171a7cd897bc8'
indices=sorted({0,len(pts)-1}|{bisect.bisect_left(pts,t) for t in range(pts[0],pts[-1]+1,4000)})
printed=plan.read_text().split('Exact indices:\n\n',1)[1].split('\n\n',1)[0]
assert indices==[int(x) for x in printed.replace('\n','').strip('.').split(',')]
counts={step:len({0,len(pts)-1}|{bisect.bisect_left(pts,t) for t in range(pts[0],pts[-1]+1,step)}) for step in [2000,4000]}
assert counts=={2000:153,4000:77}; print('PLAN',counts,'all77indices_match',True)
script=b/'sample_candidate.py'; tree=ast.parse(script.read_text()); script_hash=sha(script)
def require(ok,why):
 if not ok: raise ValueError(why)
nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='WARNING' for t in n.targets) or isinstance(n,ast.FunctionDef) and n.name=='check_diagnostics']
ns={'re':re,'m':types.SimpleNamespace(prior=types.SimpleNamespace(require=require))}; exec(compile(ast.Module(body=nodes,type_ignores=[]),str(script),'exec'),ns)
warning=b'[swscaler @ 0x1] [swscaler @ 0x2] No accelerated colorspace conversion found from yuv420p to rgb24.\n'
cases=[(b'unknown\n',0,True,False),(b'',7,True,False),(warning,0,False,False),(warning,0,True,True),(b'',0,False,True),(warning+b'other warning\n',0,True,False)]
for raw,status,allow,expected in cases:
 try: ns['check_diagnostics'](raw,{'returncode':status},allow); result=True
 except ValueError: result=False
 assert result==expected
print('PURE_DIAGNOSTIC_CONTROLS',len(cases),'passed')
for run in ['control01','run01','run02']:
 d=b/run; rows=read(d/'frames.json'); receipt=read(d/'receipt.json'); status=read(d/'decode.status.json'); command=read(d/'decode.command.json'); err=(d/'decode.stderr').read_bytes()
 assert receipt['script_sha256']==script_hash and receipt['scientific_or_human_acceptance'] is False and receipt['status']=='descriptive_derivatives_only'
 assert status=={'launch_error':None,'returncode':0} and (d/'decode.stdout').read_bytes()==b''
 ns['check_diagnostics'](err,status,run!='control01'); assert receipt['diagnostic_lines']==len(err.splitlines())
 expected_indices=[0,60,120,124] if run=='control01' else indices
 assert [r['source_index'] for r in rows]==expected_indices and [r['order'] for r in rows]==list(range(1,len(rows)+1))
 source=Path(command[command.index('-i')+1]); assert sha(source)==receipt['source_sha256']
 expected_filter="select='"+'+'.join(f'eq(n,{i})' for i in expected_indices)+"'"; assert command[command.index('-vf')+1]==expected_filter
 assert len(list((d/'native').glob('*.png')))==len(rows)
 for order,r in enumerate(rows,1):
  p=d/r['path']; assert r['path']==f'native/frame-{order:06d}.png' and sha(p)==r['png_sha256']
  with Image.open(p) as im: im.load(); assert im.mode=='RGB'; pixels=im.tobytes(); size=im.size
  assert hashlib.sha256(pixels).hexdigest()==r['rgb_sha256'] and hashlib.md5(pixels).hexdigest()==r['rgb_md5']
  if run=='control01':
   color=[(255,0,0),(0,255,0),(0,0,255),(0,0,255)][order-1]; assert size==(96,64) and pixels==bytes(color)*(96*64)
  else: assert size==(320,240) and r['rgb_md5']==rgb[r['source_index']][5]
 if run!='control01':
  loc=read(d/'locators.json'); assert loc==[{'order':r['order'],'source_index':r['source_index'],'pts':pts[r['source_index']],'time_base':'1/1000'} for r in rows]
  assert read(d/'plan-pin.json')=={'sha256':plan_hash}
 print('SAMPLES',run,len(rows),'pixel_and_file_hashes_match','diagnostic_lines',len(err.splitlines()))
assert read(b/'run01/frames.json')==read(b/'run02/frames.json') and read(b/'run01/locators.json')==read(b/'run02/locators.json')
print('REPEATED77_METADATA_PIXEL_PNG_MATCH')
for p in [plan,b/'DIAGNOSTIC-REVIEW-PLAN.md',script,b/'sources/ffmpeg-n7.1.1-yuv2rgb.c',b/'control01/receipt.json',b/'run01/receipt.json',b/'run02/receipt.json',b/'run01/frames.json',b/'run02/frames.json',b/'run01/locators.json',b/'run02/locators.json']:
 print('PIN',str(p.relative_to(b)),p.stat().st_size,sha(p))
print('NUMERICAL_AUDIT_PASS: no image display or video redecode')
PY
```

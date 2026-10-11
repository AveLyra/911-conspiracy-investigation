# Stage 2: nonvisual source/selection/product audit

2026-10-03. Research-only independent artifact review of Clips 3 and 4.
**Passed: no mismatch or blocking defect found in the declared nonvisual
source/selection/product checks.** No visual reading, scene judgment,
historical AVI decode, source retrieval or scientific/human acceptance is
performed by this audit.

## Result and limits

Both selected first-attempt files match the exact refreshed and original
catalogue ID/title/MIME/size records, the acquisition receipts and input
paths. Each source was freshly sized and hashed. Recorded transfers exited
0, HTTP 200, with empty matching-hash stderr; retained raw-directory contents
contain precisely those two received copies and their diagnostics. There is
no failed attempt in this stage. This auditor did not independently witness
the network transfer. The recorded response remains access_not_verified;
normalized checksum omission is not provider-checksum absence, and the
received-byte hashes are not original-camera authentication.

| Source | Received bytes / SHA-256 | Full inventory | Exact time base | Selected indices |
|---|---|---:|---|---|
| Clip 3, attempt 1 | 23621148 / `ced46b4c4318ef53c38eaf9485b76efa4d4d2c155b7194871a8479f0841a993d` | 189 frames, PTS 0–188 | `333673/10000000` | 0,24,47,71,94,118,141,165,188 |
| Clip 4, attempt 1 | 25734188 / `a4eb4934882428b15a156d2a7bfe1755e3dc00b37667f08a59c365645b3e07e8` | 206 frames, PTS 0–205 | `166837/5000000` | 0,26,52,77,103,129,154,180,205 |

The independent linear integer/rational oracle reproduces all 18 target
choices without calling the adapter's selection function. All 395 complete
preparation frame records are consistent with the selected native stream.
Both extraction inventories equal their corresponding preparation inventory,
giving 790 further record-instance comparisons: 1,185 record instances across
three passes, **not** 1,185 independent recorded frames. Exact encoded clocks
are retained, not replaced with nominal frame rate or authenticated event time.

All frame records and selected showinfo joins agree on 720 × 480, yuv411p,
SAR 8:9, interlaced=1 and top-field-first=0 (showinfo i:B). Every one of 36
PNG instances is RGB at native raster size and matches its complete PNG and
decoded RGB-byte hashes. All 18 corresponding material pairs match across
run01/run02, including exact PTS and native metadata. These are repeated
extractions of two received copies using the same toolchain, not independent
camera validation or independent-decoder reproduction.

All six current preparation input/runtime pins and 28 preparation product
size/hash pins match. Source before/after identities, declarations and
protocol snapshots agree in preparation and both extractions, and the source
files match a final rehash. The checker verifies 12 source command arrays
and five version command arrays, 17 zero/no-launch-error statuses, 13 empty
probe/version stderr files, and four empty decode stdout files. All four
decode receipts are clean with zero rejected entries and nine showinfo/color
pairs each. Full corresponding repeat logs match after only the documented
address/output-directory normalization.

The fresh control receipts report 14 parent-helper and 25 adapter tests,
zero errors/failures, with matching helper/test/adapter/synthetic-source pins.
Those 39 tests were **not rerun by this auditor**. The present artifact check
was freshly executed, rather than treating their green receipts as proof of
source identity, target correctness or historical validity.

This passes only the stage-two nonvisual artifact gate. It does not identify
scenes, exclude unsampled scenes, classify glazing/fire, establish event timing
or cause, or satisfy an actual-human review gate. Clips 5–8 remain outside
this review; stage-one artifacts are reused only as a pinned checker and
earlier source metadata. The strongest limitation is that exact, repeatable
derivatives can still come from edited, mislabeled or historically
unauthenticated source copies. A scene association requires the separately
frozen visual records and, if warranted, a later source-transform test.

## Scope and method

The reviewer read the current main AGENTS, WORKFLOW, START-HERE and CHARTER,
the unchanged unit protocol, adapter and tests, inherited extraction helper
and tests, preceding code review and complete stage-one artifact checker.
Current implementation/test hashes match their previously reviewed pins.
This is a new agent review, not a claim of a new camera, licensed expert or
independent toolchain. This reviewer did not author those implementation
files; it reuses the separately written stage-one artifact checker rather
than importing the extraction/selection implementation to validate itself.

The checker below pins that earlier checker in its preserved document and
changes only the stage/pair/metadata joins. Its linear integer/rational target
oracle, process/command checks, native metadata and PNG/RGB/PTS comparisons
are unchanged. Supplemental checks cover the exact refreshed source records,
fetch receipt fields and the newly run synthetic-control result pins. The
original eight-item metadata and stage-one record remain read-only.

The complete run01 decode logs for both clips have been read directly. The
checker compares each entire repeat log after normalizing only run directory
and runtime hexadecimal addresses. It does not loosen diagnostic acceptance
to accommodate new output. This checks the particular saved logs; it is not
a new general-purpose diagnostic parser or independent decoder validation.

## Actual verification and artifact pins

`cat` read both metadata records, acquisition/input records, the preparation
and both outer extraction receipts, both fresh control result files and
complete run01 decode logs. The read-only checker parsed all six complete
inventories, source receipts, command/status files and frame manifests,
rehashed all received copies, and opened only the extracted PNGs for byte
checks. `shasum -a 256` independently returned the pins below. An initial
instruction-path search returned no descendant AGENTS files and therefore
skipped its chained protocol read; a separate complete protocol read followed.
No source or method was altered by that unsuccessful search.

The exact checker command shown below ran from `/Users/admin/docs/911` using
the bundled Python interpreter. Tool chunk `f867fa`, process exit 0: PASS;
2 fresh metadata joins, 2 transfer attempts, 6 current preparation pins,
28 preparation product pins, 17 process statuses, 13 empty probe/version
stderr files, 395 preparation plus 790 repeated inventory records,
18 targets, 12 source command arrays, 36 PNG/RGB pairs, 4 decode logs,
and 18 matching repeated PNG pairs. No failed checker run or repaired media
artifact preceded that pass. Only this review document was authored.

| Artifact | SHA-256 |
|---|---|
| `metadata-refresh.json` | `e0c52f41ddd9ce8b6b2837af3b5cd7527f81aaabf46955de6dec34b0e6c424a4` |
| `acquisition.json` | `ba3a70d91e5b842b9da0b97fa5beacde409484f898e06fdb9e577600b5bb3afc` |
| `input.json` | `63e1268cf22ccae65aabdccf8036127b80e3e649abaaab9fd42ee77ede7e45ef` |
| `preparation01/preparation-receipt.json` | `6f2b5cbd10020702e253174fecbba9f1e5c16b169f6e493e0fe33bd324f4e73f` |
| `preparation01/sampling-manifest.json` | `5689b7a6ec0c0969d36d8140db041dc7d47874ddb808f28b62845cb4e0203cb6` |
| `preparation01/selection-targets.json` | `5ab837d58c8821f7f16117ec4ea2392f65411462273d3e2b868e1ddaf2e522b7` |
| `run01/run-receipt.json` | `1a0b36974c687fbda958e359cbb36361a295915f71471630bdac08601c77750e` |
| `run02/run-receipt.json` | `1a0b36974c687fbda958e359cbb36361a295915f71471630bdac08601c77750e` |
| `controls-parent01/test-results.json` | `5241f8566563764c068d0060b33eb8a07d70f64dff236c6d9503e43d40ba1744` |
| `controls-adapter01/test-results.json` | `f8bab2e2fa7dd00f2b0d1e2b1ff7635d51f311f96d8db4bb82036ca103dc9682` |

The evidence-audit and repository-authority skills kept repeatability distinct
from historical/scientific acceptance; development-verification guided the
exact command, control-pin and product checks. No browser validation applies.

## Runnable read-only check

This opens extracted PNGs with Pillow only to inspect dimensions/mode and
hash decoded RGB bytes. It does not display images or decode the AVIs. It
hashes the received source files and reads saved inventories/diagnostics.
No file is created and no subprocess or network call is made by this code.

Run from any directory:

```sh
awk '/^```python$/{inside=1;next} /^```$/{if(inside){exit}} inside{print}' /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-vince-source-screen/stage2/artifact-review.md | /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B
```

<!-- ARTIFACT_CHECK_START -->
```python
from pathlib import Path
import hashlib

unit = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-vince-source-screen')
prior = unit / 'stage1/artifact-review.md'
raw = prior.read_bytes()
if hashlib.sha256(raw).hexdigest() != 'aa08679c94180502caf8c4c89660bae804cee745767a314be61a9870c5d5ae7c':
    raise RuntimeError('Prior checker identity changed; adaptation refused')
code = raw.decode().split('```python\n', 1)[1].split('\n```', 1)[0]
def replace_once(old, new):
    global code
    if code.count(old) != 1:
        raise RuntimeError('Expected exactly one adaptation site: ' + old)
    code = code.replace(old, new, 1)

replace_once("S, P = U/'stage1', U/'stage1/preparation01'", "S, P = U/'stage2', U/'stage2/preparation01'")
replace_once("need(acq['metadata_refresh_sha256']==sha(U/'metadata-refresh.json'),'metadata pin')",
             "need(acq['metadata_refresh_sha256']==sha(S/'metadata-refresh.json'),'metadata pin')")
replace_once("inp['stage']==1", "inp['stage']==2")
replace_once("targets['stage']==1", "targets['stage']==2")
replace_once("[v['clip_number'] for v in inp['sources']]==[1,2]", "[v['clip_number'] for v in inp['sources']]==[3,4]")
replace_once("[v['clip_number'] for v in acq['items']]==[1,2]", "[v['clip_number'] for v in acq['items']]==[3,4]")
replace_once("meta['items'][:2]", "meta['items'][2:4]")
replace_once("[v['id'] for v in manifest['sources']]==['vince-clip1','vince-clip2']", "[v['id'] for v in manifest['sources']]==['vince-clip3','vince-clip4']")
replace_once("[v['id'] for v in targets['sources']]==['vince-clip1','vince-clip2']", "[v['id'] for v in targets['sources']]==['vince-clip3','vince-clip4']")
extra = """
need(sha(U/'metadata-refresh.json')=='476d65df2849a72ef85ce29daffd1f1961bd8819c5dc7c616bbba34ce316ee82','original all-eight metadata pin')
need(sha(U.parent/'nist-acoustic-detectability/cbs-folder-metadata-2026-09-28.json')=='44168a69f5b823f70e82f45cf06f8ff610c9388e39876ed0d8a60043d7554e1a','fixed catalogue pin')
fresh=read(S/'metadata-refresh.json')
need(fresh['stage']==2 and [v['clip'] for v in fresh['items']]==['3','4'],'fresh metadata pair')
need(acq['schema']=='cbs-vince-acquisition-v1','acquisition schema')
need(acq['retrieval']['download_raw_file'] is True and acq['retrieval']['include_base64'] is False,'raw fetch policy')
need('--max-time 55' in acq['retrieval']['options'],'recorded transfer timeout')
need(len(acq['items'])==len(inp['sources'])==2,'complete two-clip stage')
for f,o,a in zip(fresh['items'],meta['items'][2:4],acq['items']):
    md=f['response']['structuredContent']; earlier=o['metadata']; fetched=a['fetch_safe_result']
    need(f['response']['isError'] is False,'metadata response failure')
    need(f['request']==o['request'],'exact metadata request')
    for key in ('id','title','mime_type','size','url','modified_time'):
        need(md[key]==earlier[key],'fresh/original metadata join '+key)
    need(md['source_visibility_status']=='access_not_verified','visibility limitation preserved')
    need(a['request_url']==md['url'],'raw request URL join')
    need(fetched['isError'] is False and fetched['inline_bytes_present'] is False,'fetch outcome')
    need(fetched['id']==md['id'] and fetched['title']==fetched['file_name']==md['title'],'fetch identity join')
    need(fetched['mime_type']==md['mime_type'] and fetched['file_size_bytes']==int(md['size']),'fetch type/size join')
    need(fetched['reference_type']=='object' and fetched['reference_keys']==['download_url','file_id','mime_type','file_name'],'returned top-level reference receipt')
    need(a['selected_attempt']==1 and len(a['attempts'])==1,'declared first-attempt success')
    attempt=a['attempts'][0]
    need(attempt['attempt']==1 and attempt['http_code']==200 and attempt['content_type']=='video/avi','transfer result')
    need(0 < attempt['transfer_seconds'] <= 55,'recorded transfer duration')
    counts['fresh_metadata_joins']+=1
need(sorted(p.name for p in (S/'raw').iterdir())==['clip3-attempt1.avi','clip3-attempt1.stderr','clip4-attempt1.avi','clip4-attempt1.stderr'],'complete retained transfer files')
parent=read(S/'controls-parent01/test-results.json'); adapter_test=read(S/'controls-adapter01/test-results.json')
for result,total in ((parent,14),(adapter_test,25)):
    need(result['tests_run']==total and result['successful'] is True and result['errors']==result['failures']==0,'fresh control result')
    need(result['helper_sha256']==helper,'control helper pin')
    counts['reported_control_tests']+=total
need(parent['tests_sha256']==sha(U.parent/'late-fire-sequence/test_sample_sequence.py')=='cd997911f50d89d57c65906a1ac4eef3cda09ac4667a1f07307f9945068fcc43','parent test pin')
need(parent['synthetic_source_sha256']==sha(U.parent/'late-fire-catalog-join/control01/synthetic.avi')=='03faf8b842dbec9ea7358b91f3cb0097a40a1b0719696b698025a4b79599b8c6','synthetic source pin')
need(adapter_test['tests_sha256']==sha(U/'test_prepare_samples.py')=='484d1f391b3d4e0bf0116fa35e6f2f20bd264c0098b255a1b59dff0d27e74c55','adapter test pin')
need(adapter_test['adapter_sha256']==adapter and adapter_test['synthetic_only'] is True and adapter_test['scientific_or_human_acceptance'] is False,'adapter control boundaries')
"""
replace_once('selected={}\n', extra + '\nselected={}\n')
exec(compile(code, str(prior) + ':stage2-pair-adaptation', 'exec'), {})
```
<!-- ARTIFACT_CHECK_END -->

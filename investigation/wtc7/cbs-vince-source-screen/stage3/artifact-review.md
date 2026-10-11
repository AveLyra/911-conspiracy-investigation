# Stage 3: nonvisual source/selection/product audit

2026-10-04 UTC (October 3 locally). Research only; Clips 5 and 6.
**Selected-source, target and product checks passed. The requested 55-second
transfer-time limit was not met for Clip 6 attempt 1.** That operational
deviation remains separate from selected-source and derivative integrity;
it is not silently reclassified as compliant. This is not an unqualified
protocol-compliance pass.

## Artifact result

All three received attempt files and their stderr identities match the saved
acquisition record. The exact original and refreshed catalogue ID/title/MIME/
size joins match the selected inputs. Clip 5 attempt 1 and Clip 6 attempt 2
are complete copies with recorded exit 0, empty stderr and matching sizes;
their recorded transfer durations are below 55 seconds. Clip 6 attempt 1 is
21,929,315 bytes short and absent from the sampling inputs. Both safe fetch
receipts are reconciled; no temporary bearer URL is required or logged.

| Selected source | Bytes / SHA-256 | Complete inventory | Exact time base | Selected indices |
|---|---|---:|---|---|
| Clip 5, attempt 1 | 65881740 / `8a7c04527e7807ec141c9da2af65d7a654493c462ecdff238764d3760196727f` | 529 frames, PTS 0–528 | `333673/10000000` | 0,66,132,198,264,330,396,462,528 |
| Clip 6, attempt 2 | 24615508 / `c68e8b3b3c82bc980addbfc00c767ba486e8e54826e48427f0d57f5fdac9d074` | 197 frames, PTS 0–196 | `333673/10000000` | 0,25,49,74,98,123,147,172,196 |

The independent linear integer/rational oracle reproduces all 18
first-at-or-after choices without calling the adapter. All 726 preparation
frame records pass native stream/PTS checks. Both extraction inventories
equal their complete preparation counterparts: 1,452 additional comparisons,
or 2,178 record instances across three passes—not 2,178 independent frames.
All records and selected showinfo joins retain 720 × 480, yuv411p, SAR 8:9,
interlaced=1 and top-field-first=0 (showinfo i:B). Encoded times are not
authenticated event clocks.

Every one of 36 PNG instances has matching complete-file and decoded RGB-byte
hashes, RGB mode, native dimensions and exact PTS joins. All 18 corresponding
run01/run02 material pairs match. Six current preparation input/runtime pins
and all 28 preparation product size/hash pins match. Before/after source
identities, protocol/manifest snapshots and a final source rehash agree.
The checker verifies 12 source command arrays, five version command arrays,
17 zero/no-launch-error process statuses, 13 empty probe/version stderr
files and four empty decode stdout files. All four decode receipts are
clean, with no rejected entries and nine showinfo/color pairs each. Complete
repeat logs match after replacing only runtime hexadecimal addresses and
run-specific output directories; no extra log normalization was needed.

The new control result files report 14 parent-helper and 25 adapter tests
with zero errors/failures. Current implementation/test/synthetic-source pins
match those receipts. These 39 tests were not rerun by this auditor; the
artifact checker itself was freshly run. Neither synthetic-test success nor
same-toolchain repeatability establishes historical source authenticity.

The strongest remaining objection is provenance: perfectly repeatable frames
can derive from edited or mislabeled access copies. Metadata still reports
access_not_verified and omits provider checksums in its normalized fields;
omission does not prove provider absence. This audit does not identify a
scene, exclude unsampled content, classify fire or glass, assess cause, or
complete human review. Clips 7–8 are outside the audited stage and remain
required by the fixed protocol.

## Retained exception and scope

The saved timeout diagnostic states 71,150 milliseconds and 2,686,193 of
24,615,508 bytes received. The acquisition receipt reports exit 28, HTTP 200
and 71.150559 seconds despite the requested `--max-time 55`. The partial is
preserved, not admitted. Its SHA-256 is
`1272dffa33cf4f05833b63431804344c15c9205db3b6f10eea77daed7714c761`;
the 100-byte diagnostic's hash is
`26a3097da56da02780c9b6df8e2665058708ac2df3c8b62153e724a5a16cc2a5`.
Cause of the timeout overrun is unresolved. The record describes one allowed
retry only after the terminal failure; this auditor did not witness the live
transfer or retry. HTTP 200 is not treated as proof of successful acquisition.

This review directly reuses the preserved, hash-pinned stage-one checker,
not a chain through stage two. Adaptations identify stage 3, pair 5–6 and the
fresh metadata format. Its independent linear target oracle, native metadata,
diagnostic, exact-command, source-integrity and PNG/RGB/PTS checks are retained.
Supplemental checks retain all three transfer attempts, explicitly detect the
overrun and reconcile both safe fetch receipts plus the fresh control pins.
There is no broader warning allowlist or new permission to exceed a timeout.

Main controls/charter, protocol, implementation and tests were read in the
preceding bounded review. A fresh stage-three hash check confirmed unchanged
protocol/adapter/helper/test and original-checker identities. Both complete
run01 and run02 decode logs have been read, along with the timeout stderr.
The source metadata, acquisition/input records, preparation and both outer
extraction receipts and fresh control results were read completely. No visual
records, historical frames, scenes or audiovisual interpretations were read.

Only this working research note is authored. The same agent reviewed stage
two, but did not author the media executor or adapter. Shared toolchain and
reuse of the prior independent checker limit computational independence.
No source/camera authentication, actual-human acceptance, historical cause,
research promotion, external disclosure, commit or push is authorized here.

## Actual verification and pins

The exact command below ran from `/Users/admin/docs/911` using bundled Python,
tool chunk `075221`, process exit 0. It returned `artifact_result: PASS` and
`transfer_time_cap_result: NOT_MET_RETAINED_DEVIATION`. Counts: 2 refreshed
metadata joins, 3 attempt files, 1 excluded partial, 1 retained time overrun,
6 current preparation pins, 28 preparation product pins, 17 process statuses,
13 empty probe/version stderr files, 726 plus 1,452 inventory records,
18 targets, 12 source command arrays, 36 PNG/RGB records, 4 decode logs and
18 repeated material pairs. No failed artifact-check run or repaired source
preceded this result. `shasum -a 256` returned the following current pins;
the checker independently rehashes all relevant products and sources.

| Artifact | SHA-256 |
|---|---|
| `metadata-refresh.json` | `c342a82bd53a2725a9ae53f5a038c62b946aee8321b4543fe29c186c4a8446a3` |
| `acquisition.json` | `4cd769c801dbb58c1bf56166c8c5d7f797485813b251366c04557cbe13f3a2f7` |
| `input.json` | `e0cfbdfc35a3fa4a66be9e73c1eb84cd53622fb9b8b06cb59b730a1851be45f0` |
| `preparation01/preparation-receipt.json` | `a4b2efbe36a33496e3847acbecf6d56b240160656872d1e7387f28e3cacfbb81` |
| `preparation01/sampling-manifest.json` | `5aa620112fd6d505950f882fb836ae96032e05355430427598b47af7ee289c15` |
| `preparation01/selection-targets.json` | `d2bbb409fc90d86e65b186dfaa06443f9c95bf72680adda61f8bb56b4409ea26` |
| `run01/run-receipt.json` | `aa16c20f053702560c93715dc4fc7090532673d5bb6aea7eaf78578594207219` |
| `run02/run-receipt.json` | `aa16c20f053702560c93715dc4fc7090532673d5bb6aea7eaf78578594207219` |
| `controls-parent01/test-results.json` | `5241f8566563764c068d0060b33eb8a07d70f64dff236c6d9503e43d40ba1744` |
| `controls-adapter01/test-results.json` | `f8bab2e2fa7dd00f2b0d1e2b1ff7635d51f311f96d8db4bb82036ca103dc9682` |

The evidence-audit and repository-authority skills preserve the failure and
prevent a numerical product pass from becoming a scientific acceptance claim.
Development verification guided exact-command/control/product checks; no
browser validation applies.

## Runnable read-only check

The checker hashes AVIs without decoding them, parses the saved inventories
and logs, and opens extracted PNGs only for native geometry/mode and RGB-byte
hashes. It invokes no subprocess, makes no network request, displays no image
and writes no file. Artifact consistency and transfer-cap compliance are
reported separately.

```sh
awk '/^```python$/{inside=1;next} /^```$/{if(inside){exit}} inside{print}' /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-vince-source-screen/stage3/artifact-review.md | /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B
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

replace_once("S, P = U/'stage1', U/'stage1/preparation01'", "S, P = U/'stage3', U/'stage3/preparation01'")
replace_once("need(acq['metadata_refresh_sha256']==sha(U/'metadata-refresh.json'),'metadata pin')",
             "need(acq['metadata_refresh_sha256']==sha(S/'metadata-refresh.json'),'metadata pin')")
replace_once("inp['stage']==1", "inp['stage']==3")
replace_once("targets['stage']==1", "targets['stage']==3")
replace_once("[v['clip_number'] for v in inp['sources']]==[1,2]", "[v['clip_number'] for v in inp['sources']]==[5,6]")
replace_once("[v['clip_number'] for v in acq['items']]==[1,2]", "[v['clip_number'] for v in acq['items']]==[5,6]")
replace_once("meta['items'][:2]", "meta['items'][4:6]")
replace_once("[v['id'] for v in manifest['sources']]==['vince-clip1','vince-clip2']", "[v['id'] for v in manifest['sources']]==['vince-clip5','vince-clip6']")
replace_once("[v['id'] for v in targets['sources']]==['vince-clip1','vince-clip2']", "[v['id'] for v in targets['sources']]==['vince-clip5','vince-clip6']")
replace_once("'result':'PASS'", "'artifact_result':'PASS','transfer_time_cap_result':'NOT_MET_RETAINED_DEVIATION'")
extra = """
need(sha(U/'metadata-refresh.json')=='476d65df2849a72ef85ce29daffd1f1961bd8819c5dc7c616bbba34ce316ee82','original all-eight metadata pin')
need(sha(U.parent/'nist-acoustic-detectability/cbs-folder-metadata-2026-09-28.json')=='44168a69f5b823f70e82f45cf06f8ff610c9388e39876ed0d8a60043d7554e1a','fixed catalogue pin')
fresh=read(S/'metadata-refresh.json')
need(fresh['stage']==3 and [v['clip'] for v in fresh['items']]==['5','6'],'fresh metadata pair')
need(acq['schema']=='cbs-vince-acquisition-v1','acquisition schema')
need(acq['retrieval']['download_raw_file'] is True and acq['retrieval']['include_base64'] is False,'raw fetch policy')
need('--max-time 55' in acq['retrieval']['options'],'requested transfer timeout')
need(len(acq['items'])==len(inp['sources'])==2,'complete two-clip stage')
need([a['selected_attempt'] for a in acq['items']]==[1,2],'selected attempts')
need([[t['attempt'] for t in a['attempts']] for a in acq['items']]==[[1],[1,2]],'retained ordered attempt set')
overruns=[]
for f,o,a in zip(fresh['items'],meta['items'][4:6],acq['items']):
    md=f['response']['structuredContent']; earlier=o['metadata']
    need(f['response']['isError'] is False,'metadata response failure')
    need(f['request']==o['request'],'exact metadata request')
    for key in ('id','title','mime_type','size','url','modified_time'):
        need(md[key]==earlier[key],'fresh/original metadata join '+key)
    need(md['source_visibility_status']=='access_not_verified','visibility limitation preserved')
    need(a['request_url']==md['url'],'raw request URL join')
    for fetched in (a['first_fetch_safe_result'],a['fetch_safe_result']):
        need(fetched['isError'] is False and fetched['inline_bytes_present'] is False,'fetch outcome')
        need(fetched['id']==md['id'] and fetched['title']==fetched['file_name']==md['title'],'fetch identity join')
        need(fetched['mime_type']==md['mime_type'] and fetched['file_size_bytes']==int(md['size']),'fetch type/size join')
        need(fetched['reference_type']=='object' and fetched['reference_keys']==['download_url','file_id','mime_type','file_name'],'returned top-level reference receipt')
    for attempt in a['attempts']:
        need(attempt['http_code']==200 and attempt['content_type']=='video/avi','recorded response type')
        need(attempt['requested_max_time_seconds']==55 and attempt['transfer_seconds']>0,'requested time bound')
        overrun=attempt['transfer_seconds']>55
        need(attempt['reported_duration_exceeded_requested_limit'] is overrun,'honest duration-overrun flag')
        if overrun: overruns.append((a['clip_number'],attempt['attempt'],attempt['transfer_seconds']))
        if attempt['attempt']==a['selected_attempt']:
            need(not overrun,'selected complete transfer time cap')
    counts['fresh_metadata_joins']+=1
need(overruns==[(6,1,71.150559)],'known operational deviation retained, not within cap')
counts['retained_transfer_time_overruns']=len(overruns)
need((S/'raw/clip6-attempt1.stderr').read_bytes()==b'curl: (28) Operation timed out after 71150 milliseconds with 2686193 out of 24615508 bytes received\\n','specific timeout evidence')
need(sorted(p.name for p in (S/'raw').iterdir())==['clip5-attempt1.avi','clip5-attempt1.stderr','clip6-attempt1.avi','clip6-attempt1.stderr','clip6-attempt2.avi','clip6-attempt2.stderr'],'complete retained transfer files')
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
exec(compile(code, str(prior) + ':stage3-pair-adaptation', 'exec'), {})
```
<!-- ARTIFACT_CHECK_END -->

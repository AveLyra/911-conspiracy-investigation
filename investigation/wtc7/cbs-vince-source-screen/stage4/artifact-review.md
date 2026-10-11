# Stage 4: nonvisual source/selection/product audit

2026-10-04 UTC. Research only; exact Clips 7 and 8. **Material source,
selection and product checks passed. Complete repeat log text is unequal.**
After the earlier address/path normalization, each clip's log differs only
in its final processing-fps field. Both differing lines are retained and
explicitly checked; they are not normalized away or called equal.

## Results

Both first-attempt files have the recorded complete catalogue sizes, matching
received-byte hashes, exit 0 and empty stderr. Refreshed IDs/titles/MIME/sizes
join the original all-eight metadata, safe fetch receipts and sampling inputs.
All retained raw-directory files are accounted for; there are no partials in
this stage. Requested timeout is 55 seconds; the recorded durations of
6.159989 and 9.343747 seconds are below it and their overrun flags agree.
This is a check of preserved receipts, not an independently witnessed network
transfer or a guarantee that the timeout will constrain another attempt.
The stage-three overrun remains preserved in its own record.

| Source | Bytes / SHA-256 | Complete inventory | Exact time base | Selected indices |
|---|---|---:|---|---|
| Clip 7, attempt 1 | 140334936 / `a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b` | 1,128 frames, PTS 0–1127 | `333673/10000000` | 0,141,282,423,564,705,846,987,1127 |
| Clip 8, attempt 1 | 260031856 / `0fc34e26ea949705126bbcf38247db62b0b98842ab79643200957d93c23950a3` | 2,091 frames, PTS 0–2090 | `333673/10000000` | 0,262,523,784,1045,1307,1568,1829,2090 |

Independent linear integer/rational arithmetic reproduces all 18 declared
first-at-or-after target choices, without calling the adapter's selection
function. All 3,219 preparation frame records retain strict increasing PTS
and consistent native stream metadata. Two complete extraction inventories
equal the preparation inventories, adding 6,438 comparisons: 9,657 record
instances across three passes, not independently recorded frames.

Every selected frame retains the inventory/showinfo join for 720 × 480,
yuv411p, SAR 8:9, interlaced=1 and top-field-first=0 (showinfo i:B). All 36
PNG instances have RGB mode, native raster, matching complete-file and
decoded RGB-byte hashes and exact PTS joins. All 18 run01/run02 material
pairs match. These repeated same-toolchain derivatives do not authenticate
the original camera recording or event clock.

Six current preparation input/runtime pins, 28 preparation product size/hash
pins, source before/after identities, declaration snapshots and final source
rehashes agree. Twelve source command arrays and five version command arrays
match their declared forms. Seventeen saved process statuses are zero with
no launch error; 13 probe/version stderr files and four decode stdout files
are empty. Four decode receipts are clean with zero rejected entries and
nine showinfo/color pairs each. Their original strict diagnostic grammar was
not changed.

All four complete decode logs have 34 lines. After only address/path
normalization, line 34 differs as follows; every other line matches:

| Source | run01 final processing fps | run02 final processing fps |
|---|---:|---:|
| Clip 7 | 0.0 | 8.7 |
| Clip 8 | 4.1 | 5.7 |

The full differing lines are returned by the checker, which also verifies
these exact observed differences. Any other difference is refused as
unresolved. These are final execution-rate statistics, not the separately
preserved source frame rate or encoded PTS. No historical-frame disagreement
was found in the material comparisons. Whole-log equality remains false;
the checker does not issue an undifferentiated all-fields PASS.

Fresh control receipts report 14 parent-helper and 25 adapter tests with zero
errors/failures, with current code/test/synthetic-source pins. This reviewer
did not rerun those 39 tests; it freshly ran the artifact checker. Passing
synthetic controls alone was not used to establish historical-file integrity.

Strongest limitation: precisely repeatable derivatives can still originate
from edited or mislabeled access copies. The metadata reports
access_not_verified, and normalized checksum omission does not demonstrate
provider-checksum absence. This audit cannot identify scenes, exclude an
unsampled scene, infer glazing/fire/temperature/motion/cause, or satisfy a
human gate. It addresses only these two selected sources and their products,
not completion of the full investigation.

## Scope and independence

The reviewer reread the unchanged protocol and stage-three timing exception,
verified current protocol/adapter/helper/test pins, and then read stage-four
metadata, acquisition/input, preparation and both outer extraction receipts,
fresh control results and all four complete decode logs. No root/reader
observations or reference/candidate images were read. This agent audited the
preceding stages but did not author the source sampler/adapter; it is not a
licensed expert, human reviewer, independent camera or independent toolchain.

The runnable check directly reuses the original hash-pinned stage-one
artifact checker. It does not call stage-two/three checker code or import the
sampler/adapter. Adaptations identify stage 4, the 7–8 pair and refreshed
metadata fields. Supplemental checks reconcile every recorded attempt, fetch
identity and fresh-control pin. Requested and reported durations are compared
as data, not presumed compliant from the command setting.

The exact rational target oracle and all source/native-metadata/command/
status/strict-diagnostic/product/PNG/RGB/PTS/repeat checks are retained. The
old additional whole-log equality assertion is represented as an explicit
comparison result with every differing line retained, rather than aborting
before checking the second source or pretending the comparison passed.
No extraction acceptance grammar or scientific threshold changes. This is
not permission to ignore unknown diagnostics or accept corrupted inputs.

## Actual verification and pins

Read-only complete-log comparison: chunk `66d1be`, exit 0, identified exactly
the two final-summary differences above. The first complete artifact checker
run: chunk `5caf8a`, exit 0, returned material checks PASS, zero reported
transfer-cap overruns and two explicitly unequal log comparisons. It checked
2 refreshed metadata joins, 2 attempts, 6 current preparation pins,
28 preparation products, 17 statuses, 13 empty probe/version stderr files,
3,219 plus 6,438 inventory records, 18 targets, 12 source command arrays,
36 PNG/RGB pairs, 4 logs and 18 repeated material pairs. The exact-difference
guard was then added before the final rerun; no media, input or decoder
acceptance rule was edited. No failed check preceded the first result.
The guarded rerun completed exit 0, chunk `e4986f`, with the same material
PASS and the same two explicitly unequal, exact-difference-checked logs.

The command below uses the bundled Python interpreter from
`/Users/admin/docs/911`; it is stdout-only. `shasum -a 256` independently
returned the following current pins; the checker rehashes sources/products.

| Artifact | SHA-256 |
|---|---|
| `metadata-refresh.json` | `b5a5d6bc0bf12a8079f96f5ecc0548d4c260beb0fcf06bde5be870508cb4a27e` |
| `acquisition.json` | `7ad550f1e6394c0e5e86984b2a63090a5f250c70735e838592fe8282ba2fb6a7` |
| `input.json` | `ca06dd79aeae760997e3d2f1a61fe8b92ee54c644f8b40493f1cfaa0843ed86b` |
| `preparation01/preparation-receipt.json` | `564dfaf153652b079338c693fd0b918b5102c9d4d2f95b4ed51da61b4ce85904` |
| `preparation01/sampling-manifest.json` | `8cfc8ac6ce67b0c1ca15c874b3663a638585798bb3aba8461bfe2b5c4fbc4fd6` |
| `preparation01/selection-targets.json` | `9d676f014c4b866129eeb77df2a6be519326dd8dbe08a54ac8026864514f4e72` |
| `run01/run-receipt.json` | `5ff2f949d47f0e0e0eeb98b3778fd8844878f9a131c66bd00eb0ca904b0da31e` |
| `run02/run-receipt.json` | `5ff2f949d47f0e0e0eeb98b3778fd8844878f9a131c66bd00eb0ca904b0da31e` |
| `controls-parent01/test-results.json` | `5241f8566563764c068d0060b33eb8a07d70f64dff236c6d9503e43d40ba1744` |
| `controls-adapter01/test-results.json` | `f8bab2e2fa7dd00f2b0d1e2b1ff7635d51f311f96d8db4bb82036ca103dc9682` |

Evidence-audit, repository-authority and development-verification skills
guided provenance separation, retained discrepancies and reproducible checks.
Only this note was authored. No browser/UI test applies.

## Runnable read-only check

The code hashes AVI bytes without decoding them, reads saved inventories and
logs, and opens existing PNGs only for native dimensions/mode and RGB-byte
hashing. It does not display images, retrieve content, run subprocesses or
write files. No result is a scene identification or human acceptance.

```sh
awk '/^```python$/{inside=1;next} /^```$/{if(inside){exit}} inside{print}' /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-vince-source-screen/stage4/artifact-review.md | /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B
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

replace_once("S, P = U/'stage1', U/'stage1/preparation01'", "S, P = U/'stage4', U/'stage4/preparation01'")
replace_once("need(acq['metadata_refresh_sha256']==sha(U/'metadata-refresh.json'),'metadata pin')",
             "need(acq['metadata_refresh_sha256']==sha(S/'metadata-refresh.json'),'metadata pin')")
replace_once("inp['stage']==1", "inp['stage']==4")
replace_once("targets['stage']==1", "targets['stage']==4")
replace_once("[v['clip_number'] for v in inp['sources']]==[1,2]", "[v['clip_number'] for v in inp['sources']]==[7,8]")
replace_once("[v['clip_number'] for v in acq['items']]==[1,2]", "[v['clip_number'] for v in acq['items']]==[7,8]")
replace_once("meta['items'][:2]", "meta['items'][6:8]")
replace_once("[v['id'] for v in manifest['sources']]==['vince-clip1','vince-clip2']", "[v['id'] for v in manifest['sources']]==['vince-clip7','vince-clip8']")
replace_once("[v['id'] for v in targets['sources']]==['vince-clip1','vince-clip2']", "[v['id'] for v in targets['sources']]==['vince-clip7','vince-clip8']")
replace_once("'result':'PASS'", "'material_artifact_checks':'PASS','reported_transfer_cap_overruns':overruns,'normalized_log_comparisons':log_comparisons,'scientific_or_human_acceptance':False")
extra = """
need(sha(U/'metadata-refresh.json')=='476d65df2849a72ef85ce29daffd1f1961bd8819c5dc7c616bbba34ce316ee82','original all-eight metadata pin')
need(sha(U.parent/'nist-acoustic-detectability/cbs-folder-metadata-2026-09-28.json')=='44168a69f5b823f70e82f45cf06f8ff610c9388e39876ed0d8a60043d7554e1a','fixed catalogue pin')
fresh=read(S/'metadata-refresh.json')
need(fresh['stage']==4 and [v['clip'] for v in fresh['items']]==['7','8'],'fresh metadata pair')
need(acq['schema']=='cbs-vince-acquisition-v1','acquisition schema')
need(acq['retrieval']['download_raw_file'] is True and acq['retrieval']['include_base64'] is False,'raw fetch policy')
need('--max-time 55' in acq['retrieval']['options'],'requested transfer timeout')
need(len(acq['items'])==len(inp['sources'])==2,'complete two-clip stage')
overruns=[]; raw_paths=[]; log_comparisons=[]
for f,o,a in zip(fresh['items'],meta['items'][6:8],acq['items']):
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
    need(1<=len(a['attempts'])<=2,'nonempty bounded attempts')
    need([t['attempt'] for t in a['attempts']]==list(range(1,len(a['attempts'])+1)),'ordered attempts')
    need(a['selected_attempt'] in [t['attempt'] for t in a['attempts']],'selected attempt exists')
    for attempt in a['attempts']:
        need(attempt['http_code']==200 and attempt['content_type']=='video/avi','recorded response type')
        need(attempt['requested_max_time_seconds']==55 and attempt['transfer_seconds']>0,'requested time bound')
        overrun=attempt['transfer_seconds']>55
        need(attempt['reported_duration_exceeded_requested_limit'] is overrun,'honest duration-overrun flag')
        if overrun: overruns.append({'clip':a['clip_number'],'attempt':attempt['attempt'],'reported_seconds':attempt['transfer_seconds']})
        for key in ('path','stderr'):
            p=S/attempt[key]
            need(p.parent==S/'raw' and p.is_file() and not p.is_symlink(),'regular raw artifact')
            raw_paths.append(p.name)
    counts['fresh_metadata_joins']+=1
need(len(raw_paths)==len(set(raw_paths)),'unique attempt paths')
need(sorted(p.name for p in (S/'raw').iterdir())==sorted(raw_paths),'complete retained transfer files')
counts['retained_transfer_time_overruns']=len(overruns)
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
replace_once("    need(normalized_logs[0]==normalized_logs[1],'normalized complete decode logs')", """
    left,right=[text.splitlines() for text in normalized_logs]
    differences=[]
    for k in range(max(len(left),len(right))):
        a=left[k] if k<len(left) else None; b=right[k] if k<len(right) else None
        if a!=b: differences.append({'line':k+1,'run01':a,'run02':b})
    observed_fps={'vince-clip7':('0.0','8.7'),'vince-clip8':('4.1','5.7')}[sid]
    exact_lines=['[info] frame=    9 fps='+value+' q=-0.0 Lsize=N/A time=00:00:00.00 bitrate=N/A speed=   0x    ' for value in observed_fps]
    need(len(left)==len(right)==34 and differences==[{'line':34,'run01':exact_lines[0],'run02':exact_lines[1]}],
         'Unresolved complete-log difference beyond the preserved final processing-fps values')
    log_comparisons.append({'source':sid,'normalized_text_equal':normalized_logs[0]==normalized_logs[1],
                            'line_counts':[len(left),len(right)],'differences':differences})
""")
exec(compile(code, str(prior) + ':stage4-pair-adaptation', 'exec'), {})
```
<!-- ARTIFACT_CHECK_END -->

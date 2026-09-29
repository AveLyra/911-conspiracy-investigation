# Stage 1: nonvisual source/selection/product audit

2026-09-28. Bounded independent artifact reconciliation. **Passed; no artifact
mismatch or blocking defect found within this stage's declared checks.** No
historical images displayed or audiovisual interpretation. Only this review
note is authored. The reader previously
authored the inherited extraction helper; selection, byte, pixel and receipt
checks below do not import its code or the new adapter.

## Result, coverage and retained failure

Metadata-refresh title/ID/MIME/size joins for Clips 1 and 2 match their exact
acquisition entries and selected input paths. All three transfer-attempt files
were freshly sized and hashed. Clip 1 attempt 1 and Clip 2 attempt 2 are the
two selected complete received copies. Clip 2 attempt 1 is preserved at
99,294,428 bytes, SHA-256
`2b43fee8db077c918b0a5b5e138bf1e795fda0a80d5318aceba00e6016167d38`,
with recorded exit 28, a 102-byte matching-hash timeout diagnostic, and
`preserved_partial_timeout_not_admitted` disposition. It is 1,390,132 bytes
short of the catalogue size and is absent from the sampling inputs. The
review does not independently witness the network transfer or authenticate
the provider beyond the retained normalized metadata/acquisition record.

| Source | Selected bytes / SHA-256 | Full inventory | Exact time base | Selected indices |
|---|---|---:|---|---|
| Clip 1, attempt 1 | 52084896 / `5e5be4b275d8277e72a6243c1130226c257a1a6918bd9d8e29d1de4306a94982` | 418 frames, PTS 0–417 | `41709/1250000` | 0,53,105,157,209,261,313,365,417 |
| Clip 2, attempt 2 | 100684560 / `78b141b40008609bdec1a94b042732bb85477ec50633d805d6887eb77dbb3a42` | 809 frames, PTS 0–808 | `333673/10000000` | 0,101,202,303,404,505,606,707,808 |

Independent linear integer/rational selection reproduces all 18 declared
first-at-or-after targets; no adapter selection function is called. Full
preparation inventories contain 1,227 frame records. Each corresponding
run01/run02 probe inventory is exactly equal as parsed JSON, adding 2,454
record checks: **3,681 inventory-record instances across three passes**, not
3,681 independently recorded frames. The two source clocks are preserved,
not substituted with a nominal frame rate or an authenticated event clock.

All inventory frames and selected showinfo records agree on 720 × 480,
`yuv411p`, SAR `8:9`, interlaced=1, top-field-first=0 (showinfo `i:B`).
The 36 PNG instances are RGB at native raster dimensions; every complete
PNG hash and decoded RGB-byte hash matches its frame manifest. All **18
run01/run02 material PNG pairs** match. These are two executions on the same
two received recordings, not independent camera or historical validation.
No metric shape or interlaced-field interpretation is inferred.

Six current preparation input/runtime pins and all 28 preparation product
size/hash pins match. All protocol/manifest snapshots and source identities
before/after preparation and both extractions match, with a fresh final source
rehash. All 12 source command arrays plus five version-command arrays match
their declared forms. Seventeen process status records show exit 0 and no
launch error; all 13 probe/version stderr files are empty. All four decode
stdout files are empty. The four decode diagnostic records are clean with
zero rejected entries and nine selected showinfo/color pairs each.

The complete run01 decode logs for both clips were read directly. Independent
severity/prefix/PTS/native-metadata checks pass for all four logs. Full run02
logs equal the respective run01 log after replacing only runtime hexadecimal
addresses and the run-specific output directory. This is not a new general
diagnostic-parser certification; it checks these particular preserved logs.
No claim is made that all path-bearing receipts or raw logs are byte-identical.

Clips 3–8 are outside this stage's artifact review and remain unreviewed here.
This passes the nonvisual integrity/selection/product gate only. It cannot
identify scenes, guarantee an unsampled scene is absent, establish original
camera custody or event time, or satisfy an actual-human acceptance gate.
Prior helper authorship and shared libraries/toolchain limit code independence;
the selection traversal and artifact checks themselves are separately written.

## Actual execution and pins

Read metadata-refresh, acquisition, input and both outer run receipts fully;
used bounded JSON selectors for preparation status/targets; then parsed all
six complete inventories, all source receipts, statuses, command arrays and
frame manifests in the checker. `cat` read both complete run01 decode logs;
`rg --files -uu` enumerated stage paths; `wc -c` and `shasum -a 256` supplied
sizes/pins. No observer/candidate/reference judgments were read. The live root
process was never polled, interrupted or restarted by this reader; completed
run02 receipts were present when audited.

Actual final command (working directory `/Users/admin/docs/911`):

```sh
awk '/^```python$/{inside=1;next} /^```$/{if(inside){exit}} inside{print}' /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-vince-source-screen/stage1/artifact-review.md | python3 -B
```

Initial core check: chunk `2a13f4`, exit 0. Explicit command-array and target
metadata/count-reference guards were then added without changing inputs or
thresholds; final check: chunk `e91b78`, exit 0. Both passed. No failed checker
run or hidden repaired source result. The only historical failure in scope is
the retained acquisition timeout above. No new primitive tests were needed.

| Artifact | SHA-256 |
|---|---|
| `../metadata-refresh.json` | `476d65df2849a72ef85ce29daffd1f1961bd8819c5dc7c616bbba34ce316ee82` |
| `acquisition.json` | `65c65ab1ee8993d98609ff0f863609b05bd6f1b5293e24264fa1b0b1ca2363a7` |
| `input.json` | `0a92c9eaff72bdd66529da1b70b7fdc9138db84213e15e767fdd782e8a27aa1b` |
| `preparation01/preparation-receipt.json` | `f4698130c52f066076befa445f4878d968924644e66c6393c587cf1808eaf5d2` |
| `preparation01/sampling-manifest.json` | `8f5d2642e79180ffca66a3e02a3acd191174f4779ba3da63bc2a16c474197602` |
| `preparation01/selection-targets.json` | `d861d4687d6447a603384a0215aad754575e1a927317a4a4fcbd57ef95656499` |
| `run01/run-receipt.json` | `b92d39c03cf3aeb29494e86c82c3a15cad49a1424d361b87815f7e119b92f609` |
| `run02/run-receipt.json` | `b92d39c03cf3aeb29494e86c82c3a15cad49a1424d361b87815f7e119b92f609` |

The fixed protocol, adapter and helper pins are explicit in the runnable check;
the preceding independent-code-review records their separately scoped review.

## Runnable check

From this stage directory, run the following as `python3 -B` via stdin. It
reads only the declared metadata, stage artifacts and necessary pinned
controls/runtime identities; hashes received media bytes but does not decode
the AVIs, call a subprocess, retrieve content or display images. Pillow opens
the already extracted PNGs solely for dimensions/mode and RGB-byte hashing.

<!-- ARTIFACT_CHECK_START -->
```python
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib, json, re
from PIL import Image

U = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-vince-source-screen')
S, P = U/'stage1', U/'stage1/preparation01'
def need(ok, why):
    if not ok: raise RuntimeError(why)
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def ident(p): return {'bytes':p.stat().st_size,'sha256':sha(p)}
def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'duplicate JSON key'); d[k]=v
    return d
def read(p): return json.loads(p.read_bytes(),object_pairs_hook=unique)
counts=Counter(); summary=[]
protocol='5dbaca2b2329db7bc85f67fc0995adf5fd15b8fe3fd0c4b0e50f445179dd35bc'
helper='c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d'
adapter='5992d2a95be2dd8587a13980a7c05b363bd9760d24dc9768c345a3733049bb87'
need(sha(U/'PROTOCOL.md')==protocol,'protocol version')
need(sha(U/'prepare_samples.py')==adapter,'adapter version')
need(sha(U.parent/'late-fire-sequence/sample_sequence.py')==helper,'helper version')
meta,acq,inp=read(U/'metadata-refresh.json'),read(S/'acquisition.json'),read(S/'input.json')
need(acq['metadata_refresh_sha256']==sha(U/'metadata-refresh.json'),'metadata pin')
need(acq['protocol_sha256']==protocol,'acquisition protocol')
need([v['clip'] for v in meta['items']]==list(range(1,9)),'metadata order')
need(len({v['metadata']['id'] for v in meta['items']})==8,'metadata unique IDs')
need(inp['schema']=='cbs-vince-input-v1' and inp['stage']==1,'input schema/stage')
need([v['clip_number'] for v in inp['sources']]==[1,2],'input stage pair')
need([v['clip_number'] for v in acq['items']]==[1,2],'acquisition pair')
selected={}
for a,i,m in zip(acq['items'],inp['sources'],meta['items'][:2]):
    md=m['metadata']; n=a['clip_number']
    need(a['provider_id']==m['request']['fileId']==md['id'],'provider join')
    need(a['title']==md['title']==f'Vince Demetri Clip {n}.avi','title join')
    need(a['mime_type']==md['mime_type']=='video/avi','MIME join')
    need(a['catalogue_and_fetch_bytes']==int(md['size']),'catalogue size')
    need(a['max_filesize']==int(md['size'])+1048576,'transfer cap')
    need(len(a['attempts'])<=2,'attempt cap')
    for attempt in a['attempts']:
        p=S/attempt['path']; actual=ident(p)
        need(actual=={k:attempt[k] for k in ('bytes','sha256')},'attempt byte identity')
        err=S/attempt['stderr']; need(err.stat().st_size==attempt['stderr_bytes'],'transfer stderr size')
        if 'stderr_sha256' in attempt: need(sha(err)==attempt['stderr_sha256'],'transfer stderr hash')
        counts['transfer_attempts']+=1
        if attempt['attempt']==a['selected_attempt']:
            need(attempt['exit_code']==0 and attempt['disposition']=='complete_received_copy','selected transfer')
            need(actual['bytes']==int(md['size']) and not err.read_bytes(),'complete size/diagnostic')
            need(i=={'id':f'vince-clip{n}','clip_number':n,'path':str(p),**actual},'input source join')
            selected[i['id']]=actual
        else:
            need(attempt['exit_code']==28 and attempt['disposition']=='preserved_partial_timeout_not_admitted','partial disposition')
            need(actual['bytes']<int(md['size']),'partial length')
            need(str(p) not in [v['path'] for v in inp['sources']],'partial used')
            need('Operation timed out' in err.read_text(),'partial failure evidence')
            counts['excluded_partials']+=1
pr=read(P/'preparation-receipt.json')
need(pr['status']=='prepared_not_executed' and not pr['reasons'],'preparation state')
need(pr['scientific_or_human_acceptance'] is False,'preparation acceptance')
need(pr['pins_unchanged'] and pr['pins_before']==pr['pins_after'],'preparation pins')
for path,digest in pr['pins_before'].items():
    need(sha(Path(path))==digest,'current input/runtime pin'); counts['current_preparation_pins']+=1
for rel,pin in pr['products'].items():
    need(ident(P/rel)==pin,'preparation product pin'); counts['preparation_product_pins']+=1
need((P/'manifest.input.json').read_bytes()==(S/'input.json').read_bytes(),'input snapshot')
need(sha(P/'protocol.input.md')==protocol,'protocol snapshot')
manifest,targets=read(P/'sampling-manifest.json'),read(P/'selection-targets.json')
need(manifest['schema']=='late-fire-sequence-v1','sampling schema')
need(targets['schema']=='cbs-vince-nine-target-v1' and targets['stage']==1,'target schema/stage')
need([v['id'] for v in manifest['sources']]==['vince-clip1','vince-clip2'],'sampling IDs')
need([v['id'] for v in targets['sources']]==['vince-clip1','vince-clip2'],'target IDs')
for base in (P,S/'run01',S/'run02'):
    for statuspath in sorted(base.rglob('*.status.json')):
        status=read(statuspath)
        need(status=={'returncode':0,'launch_error':None},'process failure')
        counts['zero_process_statuses']+=1
    for p in base.rglob('*.stderr'):
        if p.name!='decode.stderr':
            need(p.read_bytes()==b'','probe/version stderr'); counts['empty_probe_version_stderr']+=1
    for name in ('ffprobe',) if base==P else ('ffprobe','ffmpeg'):
        need(read(base/f'{name}-version.command.json')==[f'/opt/homebrew/bin/{name}','-version'],'version command')
        need((base/f'{name}-version.stdout').read_bytes().startswith(f'{name} version 7.1.1 '.encode()),'version stdout')
for i,sel,tar in zip(inp['sources'],manifest['sources'],targets['sources']):
    sid=i['id']; source=Path(i['path']); d=P/sid
    doc=read(d/'frames.stdout'); container=read(d/'container.stdout')
    need(len(doc['streams'])==1,'one selected video'); st=doc['streams'][0]; frames=doc['frames']; tb=Fraction(st['time_base'])
    need(container['format']['format_name']=='avi','container AVI')
    video=next(v for v in container['streams'] if v['codec_type']=='video')
    for k in ('index','codec_name','pix_fmt','width','height','time_base','sample_aspect_ratio'):
        need(video[k]==st[k],'container/inventory metadata')
    need(st['codec_type']=='video' and st['codec_name']=='dvvideo' and st['pix_fmt']=='yuv411p','video lane')
    need((st['width'],st['height'],st['sample_aspect_ratio'])==(720,480,'8:9') and tb>0,'native metadata')
    pts=[]
    for f in frames:
        need(type(f['pts']) is int and (not pts or f['pts']>pts[-1]),'PTS ordering'); pts.append(f['pts'])
        need(f['media_type']=='video' and f['stream_index']==st['index'],'frame stream')
        need((f['width'],f['height'],f['pix_fmt'],f['sample_aspect_ratio'])==(720,480,'yuv411p','8:9'),'frame metadata')
        need((f['interlaced_frame'],f['top_field_first'])==(1,0),'frame interlace')
        counts['preparation_inventory_frames']+=1
    for origin in (video,st):
        for k in ('nb_frames','nb_read_frames'):
            if k in origin and origin[k]!='N/A': need(int(origin[k])==len(frames),'declared frame count')
    expected=[]
    for j,row in enumerate(tar['targets']):
        numerator=8*pts[0]+j*(pts[-1]-pts[0]); idx=next(k for k,p in enumerate(pts) if 8*p>=numerator)
        exact={'j':j,'fraction':str(Fraction(j,8)),'target_pts_exact':str(Fraction(numerator,8)),
               'target_seconds_exact':str(Fraction(numerator,8)*tb),'selected_index':idx,
               'selected_pts':pts[idx],'selected_seconds_exact':str(pts[idx]*tb)}
        need(row==exact,'independent first-at-or-after target'); expected.append(idx); counts['targets']+=1
    need(len(tar['targets'])==9 and tar['indices']==sorted(set(expected)),'nine targets/dedup')
    need(sel=={k:i[k] for k in ('id','path','sha256','bytes')}|{'count':len(frames),'indices':sorted(set(expected))},'sampling manifest')
    need(tar['count']==len(frames) and tar['first_pts']==pts[0] and tar['last_pts']==pts[-1],'target bounds')
    need(Fraction(tar['time_base'])==tb and read(d/'targets.json')==tar,'target copies/clock')
    for key in ('width','height','sample_aspect_ratio','pix_fmt','codec_name'):
        need(tar[key]==st[key],'target native metadata')
    reported=[{'origin':name,'field':key,'count':int(origin[key])} for name,origin in [('container',video),('frames',st)]
              for key in ('nb_frames','nb_read_frames') if key in origin and origin[key]!='N/A']
    need(tar['reported_frame_counts']==reported,'target reported-count references')
    probe=['/opt/homebrew/bin/ffprobe','-v','warning','-select_streams','v:0','-show_frames','-show_streams','-show_format','-of','json',str(source)]
    need(read(d/'frames.command.json')==probe,'preparation frame command')
    need(read(d/'container.command.json')==['/opt/homebrew/bin/ffprobe','-v','warning','-show_streams','-show_format','-of','json',str(source)],'container command')
    before=read(d/'receipt.json')
    need(before['source']==i and before['source_identity']=={'before':selected[sid],'after':selected[sid]},'probe source receipt')
    need(before['status']=='metadata_selection_only_not_extracted' and not before['reasons'],'probe acceptance')
    need(before['scientific_or_human_acceptance'] is False,'probe scientific acceptance')
    need(before['pins']==pr['pins_before'],'probe input pins')
    for name in ('container','frames'): need(before['probe_diagnostics'][name]=={'status':'clean','bytes':0,'nonempty_lines':0,'rejected':[]},'probe diagnostic receipt')
    pair=[]; normalized_logs=[]
    for run in ('run01','run02'):
        base=S/run; r=base/sid; rr=read(base/'run-receipt.json'); receipt=read(r/'receipt.json')
        need(rr['status']=='descriptive_candidates_only' and not rr['reasons'],'run state')
        need(rr['sources']==[{'id':v['id'],'admission':'descriptive_candidate_pending_independent_and_human_review'} for v in inp['sources']],'complete run source summary')
        need(rr['pins']['code_sha256']==helper and rr['pins']['plan_sha256']==protocol and rr['pins']['manifest_sha256']==sha(P/'sampling-manifest.json'),'run pins')
        need((base/'manifest.input.json').read_bytes()==(P/'sampling-manifest.json').read_bytes() and sha(base/'plan.input')==protocol,'run declarations')
        need(receipt['source']==sel and receipt['pins']==rr['pins'],'source run pins')
        need(receipt['source_identity']=={'before':selected[sid],'after':selected[sid],'status':'matched_before_and_after'},'run source identity')
        need(not receipt['reasons'] and receipt['structure']=='inventory_and_products_checked' and receipt['scientific_or_human_acceptance'] is False,'source state')
        need(receipt['admission']=='descriptive_candidate_pending_independent_and_human_review','bounded admission')
        need(read(r/'probe.stdout')==doc,'complete repeat frame inventory'); counts['extraction_inventory_frames']+=len(frames)
        need(read(r/'probe.command.json')==probe,'extraction probe command')
        expr='+'.join(f'eq(n,{n})' for n in expected)
        command=['/opt/homebrew/bin/ffmpeg','-nostdin','-hide_banner','-nostats','-loglevel','level+info',
                 '-n','-copyts','-noautorotate','-guess_layout_max','0','-i',str(source),'-map','0:v:0','-an','-sn','-dn',
                 '-map_metadata','-1','-map_chapters','-1','-vf',f"select='{expr}',showinfo",'-noautoscale','-pix_fmt','rgb24',
                 '-fps_mode','passthrough','-enc_time_base:v','demux',str(r/'native/frame-%06d.png')]
        need(read(r/'decode.command.json')==command,'exact native extraction command')
        counts['source_command_arrays']+=2
        need(receipt['probe_diagnostics']=={'status':'clean','bytes':0,'nonempty_lines':0,'rejected':[]},'run probe diagnostics')
        rows=read(r/'frames.json'); need(len(rows)==len(expected)==9,'frame manifest count')
        need(sorted(p.name for p in (r/'native').iterdir())==[f'frame-{k:06d}.png' for k in range(1,10)],'complete native files')
        for ordinal,(idx,row) in enumerate(zip(expected,rows),1):
            p=r/'native'/f'frame-{ordinal:06d}.png'; f=frames[idx]
            with Image.open(p) as im:
                im.load(); need(im.mode=='RGB' and im.size==(720,480),'native PNG mode/geometry'); rgb=hashlib.sha256(im.tobytes()).hexdigest()
            wanted={'source_index':idx,'pts':pts[idx],'time_base':str(tb),'pts_seconds_exact':str(pts[idx]*tb),
                    'file':f'native/frame-{ordinal:06d}.png','width':720,'height':480,'rgb_sha256':rgb,'png_sha256':sha(p),
                    'sample_aspect_ratio':f['sample_aspect_ratio'],'interlaced_frame':f['interlaced_frame'],'top_field_first':f['top_field_first']}
            need(row==wanted,'PNG/pixel/PTS manifest row'); counts['png_and_rgb_pairs']+=1
        raw=(r/'decode.stderr').read_text(); need(not re.search(r'\[(?:warning|error|fatal|panic)\]',raw),'decode severity')
        need((r/'decode.stdout').read_bytes()==b'','decode stdout')
        logpts=[(int(a),int(b)) for a,b in re.findall(r'\bn:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:',raw)]
        need(logpts==list(enumerate(pts[idx] for idx in expected)),'independent showinfo PTS join')
        need(re.findall(r'config in time_base: (\d+/\d+)',raw)==[str(tb)],'showinfo time base')
        need(len(re.findall(r'fmt:yuv411p cl:topleft sar:8/9 s:720x480 i:B ',raw))==9,'showinfo native metadata')
        need(re.findall(r'^\[info\] frame=\s*(\d+)',raw,re.M)==['9'],'showinfo final count')
        dd=receipt['decode_diagnostics']; need(dd['status']=='clean' and dd['rejected']==[],'decode receipt')
        need(dd['accepted_line_kinds']['show_frame']==dd['accepted_line_kinds']['show_color']==9,'showinfo/color cardinality')
        for line in raw.splitlines():
            need(line.startswith('[info] ') or re.match(r'^\[(?:Parsed_showinfo_1|out#0/image2) @ 0x[0-9a-f]+\] \[info\] ',line),'unrecognized diagnostic prefix')
        normalized_logs.append(re.sub(r'@ 0x[0-9a-f]+', '@ ADDR',raw).replace(str(S/run), 'RUN'))
        pair.append(rows); counts['decode_logs']+=1
    need(pair[0]==pair[1],'repeat material products'); counts['repeat_png_pairs']+=len(pair[0])
    need(normalized_logs[0]==normalized_logs[1],'normalized complete decode logs')
    need(ident(source)==selected[sid],'current source identity')
    counts['source_command_arrays']+=2
    summary.append({'id':sid,'frames':len(frames),'time_base':str(tb),'first_pts':pts[0],'last_pts':pts[-1],'indices':expected,'source':selected[sid]})
need(counts['zero_process_statuses']==17 and counts['empty_probe_version_stderr']==13 and counts['source_command_arrays']==12,'complete command/status coverage')
print(json.dumps({'result':'PASS','counts':dict(counts),'sources':summary,'historical_video_decodes':0,'image_displays':0,'files_written':0},indent=2))
```
<!-- ARTIFACT_CHECK_END -->

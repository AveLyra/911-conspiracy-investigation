# Independent numerical and source review

2026-09-19. Research-only review by Codex agent /root/ap_catalog_source. No
image was displayed, no audio heard, no new media retrieved or decoded, and
no producer function was imported. Pillow read saved PNGs only to check their
dimensions, mode and RGB hashes. This is another AI agent's numerical audit
of shared artifacts, not a human review or independent historical source.

## Result

**All 2,106 retained inventory rows and 128 PNG instances reconcile.** Each
source's run01/run02 pair has identical probe and frames.json bytes and
matching independently recomputed PNG/RGB hashes. All eight retained
probe/decode statuses are zero, all four probe stderr streams are empty, and
all four decode logs contain only the inspected informational output. No
numerical, source-identity or diagnostic discrepancy was found in this scope.

| Source | Inventories per pass | Samples per pass | Exact time base | Geometry / source metadata |
|---|---:|---:|---|---|
| Dub5 14 | 578 | 26 | 333651/10000000 | 720×480; SAR 8:9; interlaced_frame/top_field_first 1/0 |
| Dub5 15 | 475 | 38 | 6673/200000 | 720×480; SAR 8:9; interlaced_frame/top_field_first 1/0 |

The totals count repeated computations: 1,053 inventory rows and 64 selected
image products per pass. They are not 128 independent historical observations.
Every retained inventory PTS is a non-boolean integer equal to its own
zero-based index; all rise strictly within each file. Selected rational times
agree exactly with PTS × the file's time base. Printed six-decimal probe and
showinfo times agree within half a microsecond of those fractions. Each file
keeps its own zero and time base; this audit creates no inter-file event clock.

## Source and metadata reconciliation

Both local source sizes and SHA-256 values were independently recomputed:

| Source | Bytes | SHA-256 |
|---|---:|---|
| sources/cbs-net-dub5-14.avi | 73,206,324 | 055319a4017ce2f097dd8e9eb3ab5cbacd33bde06463d13eb4f6e32a30f655aa |
| ../late-fire-catalog-join/sources/cbs-net-dub5-15.avi | 60,183,924 | 8a4e3e02105d65140c2a3dc0bc95af0d907866de85353d5c9f498636aea79781 |

The refreshed Dub5 14 normalized response agrees with the preceding unit's
response on all six compared fields: id, title, size, mime_type, url and
modified_time. The ID remains 1cero39dWDYw60oQ4LUaw_Uk939KdBAKP; the modification
field remains 2019-11-23T04:06:43.477Z. The new created_time is null, while the
older capture populated it; acquisition.md's exact requested field list omits
creation time. This is not evidence that the provider erased a historical
creation date. Requested checksum/parent fields still supply no usable
provider checksum or parent in the normalized response.

The old Dub5 15 metadata title/size and its currently held source match the
declared reuse. Neither source was independently reacquired. The current
byte hashes match the manifest and all four receipts' recorded before/after
identities, but this reviewer did not witness those historical before/after
checks or the acquisition transport. Local agreement is not a provider-hash
comparison, original-camera authentication, or proof that file numbers imply
temporal adjacency. The earlier Organized-category source route remains the
one asserted; no Original Video from Tapes label is borrowed.

## Complete computation and diagnostic coverage

The independent script below built the intended selections from the written
rules, not the producer's selection function: Dub5 14 uses 0,30,…,570 plus
572–577; Dub5 15 uses 0,15,…,465 plus 1–5 and 474. It traversed all rows and
all 128 PNG instances, checked exact selected indices, integer timestamps,
rational times, dimensions, SAR/interlace fields, RGB mode, file hashes and
pixel hashes. No images were viewed or interpreted.

It also compared every retained probe/decode command array to the intended
source, selection and native video-only settings, reconciled every selected
showinfo index/PTS/time/format/SAR/dimension/interlace field, checked final
counts, and checked the receipt's line-kind accounting against actual logs.
Non-showinfo lines from all four logs were printed and read; they contain
ordinary input/output, stream, encoder and final-summary information.
All 320 decode-log lines were traversed: 128 frame records, 128 color records,
8 configuration records and 56 other informational lines.

| Run/source | Probe stderr bytes | Decode log lines | Selected showinfo rows | Probe/decode return codes |
|---|---:|---:|---:|---|
| run01 / 14 | 0 | 68 | 26 | 0 / 0 |
| run02 / 14 | 0 | 68 | 26 | 0 / 0 |
| run01 / 15 | 0 | 92 | 38 | 0 / 0 |
| run02 / 15 | 0 | 92 | 38 | 0 / 0 |

Decode stdout is empty in all four runs. No warning/error/fatal/panic severity,
invalid UTF-8, unexpected control character or nonempty untagged line was
found. The receipts have clean diagnostics, empty refusal reasons, matched
source identities and checked inventories/products. Their admission remains
descriptive_candidate_pending_independent_and_human_review and their
scientific_or_human_acceptance remains false. Both top-level receipts say
descriptive_candidates_only; manifest/plan snapshots match the declared files.

Version-output first lines identify FFmpeg/ffprobe 7.1.1 in both runs, and all
four version-status records report returncode 0 without a launch error.
The root-control01 test-results record says 14 grouped tests, zero failures and
errors, with the pinned helper/test identities. This reviewer read that
record and the full helper-review/root-preflight notes but did not rerun the
synthetic suite, re-audit its test code, or independently claim its results.

## Limits and strongest objection

These checks establish consistency and repeatability of the saved computation.
The same source and FFmpeg build can repeat a deterministic decoding error
without emitting a warning; neither repeated pixels nor synthetic FFV1 tests
are independent DV-decoder validation. RGB conversion, uncorrected interlacing
and non-square pixel geometry remain interpretive limits. Software cleanliness
does not establish source history, continuous recording, inter-file adjacency,
exact report-frame identity, fire duration/amount/temperature or collapse
mechanism. Human/specialist review and scientific acceptance remain separate.

No new visual finding is made about either source. Root/observer visual notes
were not read for this numerical lane. The most useful possible disconfirming
evidence would be a source-version mismatch, nonmatching boundary geometry or
an independently demonstrated edit; the present checks cannot rule those out.

## Verification record and pins

Read main AGENTS.md, WORKFLOW.md, START-HERE.md, the full charter, this unit's
PROTOCOL, FRAME-PLAN, selection.json, acquisition.md, root-preflight.md and
helper-review.md. Applied the evidence-falsification/source-of-truth skills
already read in this continuing lane and the development-verification skill.
Inspected structured source metadata, inventories, manifests, commands, status,
receipts and diagnostic streams. Only this review note was added.

One initial audit invocation exited 1 because it guessed snapshot filenames
selection.json / FRAME-PLAN.md inside run01. A filename listing established
manifest.input.json / plan.input. The corrected full traversal exited 0.
After adding explicit command-array and log-accounting checks, the complete
script below again exited 0. This was an audit-path error, not a failed source
or a waived acceptance check. No source/producer output changed.

| Record | SHA-256 |
|---|---|
| PROTOCOL.md | 878822418fae5d60096bbc509e101025cdd23463f062ce6fb7e0eb25c9098ef9 |
| FRAME-PLAN.md | 4c2870ab8775dd4a8b33fdbd59d32fafc2940fb14d7cee6cc19df829ad476297 |
| selection.json | 21d9595609115deb0ea35a9cd81d8d01c38d92c06716eeb9dc1aa0285acc1867 |
| sample_sequence.py | c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d |
| acquisition.md | 8cc621cfe5377c321daae570227e4462439e48be3310ba4f2b287f384c2eb9ca |
| root-preflight.md | 9c86d00e9d754862751eec6c8e8df7f6996f439cf44f88b4aaf4711966f60419 |
| helper-review.md | 443cb54c3584a92e367ec1d0e0014c0dc84937551eb8db2c2d059e06a13de8ed |
| sources/dub5-14.metadata.connector.json | 7fd57203fa44cbbc9c22b7e809ef66ace6357fe26fe13b379f7409af1139b705 |
| root-control01/test-results.json | 5241f8566563764c068d0060b33eb8a07d70f64dff236c6d9503e43d40ba1744 |
| Both run-receipt.json files | 6d13511054ec8b704639e570973959b8df58feab8007276086b9d9f47d878c28 |
| Both Dub5 14 frames.json | 0b8c323f83403166f517dbab46479ccf571c8467c7d0faed40943b7842433901 |
| Both Dub5 14 probe.stdout | 54b19bebf7c58072b4fb93e51019c6a75be842938abcac7b6176e2252d6d546e |
| Both Dub5 15 frames.json | 7159c3f98c7b2121e04eeb4abc13884811771b2f9f01eb4f37049f321938323a |
| Both Dub5 15 probe.stdout | 9278d5d193d2a5910f15d34ff7e1b1db92109be8e7dca957424ca786f32f453e |

All per-PNG file/pixel hashes remain in the pinned frame tables and were
recomputed, not merely copied from the paired tables. Hashes pin current
bytes; they do not authenticate historical assertions. No whole-log equality
is claimed: run paths and process addresses can differ.

## Reproducible independent traversal

Run the exact read-only command below from this unit directory:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B - <<'PY'
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
from PIL import Image
import json,re
b=Path.cwd(); old=b.parent/'late-fire-catalog-join'
def j(p): return json.loads(p.read_text())
def h(p):
    z=sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):z.update(chunk)
    return z.hexdigest()
def need(x,msg):
    if not x:raise RuntimeError(msg)
manifest=j(b/'selection.json'); sources=manifest['sources']
expected={14:list(range(0,571,30))+list(range(572,578)),15:sorted(set(range(0,466,15))|set(range(6))|{474})}
tbmap={14:F(333651,10000000),15:F(6673,200000)}
pins={'code_sha256':h(b/'sample_sequence.py'),'manifest_sha256':h(b/'selection.json'),'plan_sha256':h(b/'FRAME-PLAN.md'),'parent_code_sha256':h(old/'sample_frames.py')}
newmeta=j(b/'sources/dub5-14.metadata.connector.json')['structuredContent']
prior=j(old/'sources/cbs-net-dub5-14.metadata.connector.json')['structuredContent']
fields=['id','title','size','mime_type','url','modified_time']
need({k:newmeta[k] for k in fields}=={k:prior[k] for k in fields},'refreshed metadata')
print('metadata_six_fields_equal', {k:newmeta[k] for k in fields})
print('created_time old/new',prior['created_time'],newmeta['created_time'])
inventory_total=png_total=0; allpins=[]
for src in sources:
    num=int(src['id'].split('-')[-1]); inp=Path(src['path'])
    need(src['indices']==expected[num] and all(type(v) is int for v in src['indices']),'selection')
    actual={'bytes':inp.stat().st_size,'sha256':h(inp)}
    need(actual=={k:src[k] for k in actual},'source identity')
    catalog=j(old/f'sources/cbs-net-dub5-{num}.metadata.connector.json')['structuredContent']
    need(int(catalog['size'])==actual['bytes'] and catalog['title']==f'CBS-Net Dub5 {num}.avi','catalog size/title')
    print('source',num,actual)
    repeat={}
    for run in ['run01','run02']:
        d=b/run/src['id']; probe=j(d/'probe.stdout'); rows=probe['frames']; st=probe['streams'][0]; fr=j(d/'frames.json'); rec=j(d/'receipt.json')
        tb=F(st['time_base']); need(tb==tbmap[num] and len(rows)==src['count']==int(st['nb_frames'])==int(st['nb_read_frames']),'inventory count/timebase')
        need((st['width'],st['height'],st['sample_aspect_ratio'],st['pix_fmt'])==(720,480,'8:9','yuv411p'),'stream geometry')
        for i,r in enumerate(rows):
            need(type(r['pts']) is int and r['pts']==i,'integer/increasing PTS')
            need((r['width'],r['height'],r['sample_aspect_ratio'],r['interlaced_frame'],r['top_field_first'])==(720,480,'8:9',1,0),'row geometry')
            for k in ['pts_time','pkt_dts_time','best_effort_timestamp_time']:
                need(abs(F(r[k])-i*tb)<=F(1,2000000),'rounded time')
            need(r['pkt_dts']==r['best_effort_timestamp']==r['pts'] and r['duration']==1,'row timestamp agreement')
        need([r['source_index'] for r in fr]==expected[num],'manifest indices')
        need(len(list((d/'native').glob('*.png')))==len(fr),'PNG count')
        for r,i in zip(fr,expected[num]):
            need(type(r['source_index']) is int and type(r['pts']) is int and r['pts']==rows[i]['pts'],'selected integer locators')
            need(F(r['time_base'])==tb and F(r['pts_seconds_exact'])==r['pts']*tb,'exact rational time')
            for k in ['width','height','sample_aspect_ratio','interlaced_frame','top_field_first']:need(r[k]==rows[i][k],k)
            p=d/r['file']; need(h(p)==r['png_sha256'],'PNG hash')
            with Image.open(p) as im:
                need(im.format=='PNG' and im.mode=='RGB' and im.size==(720,480),'PNG geometry/mode')
                need(sha256(im.tobytes()).hexdigest()==r['rgb_sha256'],'RGB hash')
        for stage in ['probe','decode']:
            need(j(d/f'{stage}.status.json')=={'launch_error':None,'returncode':0},'process status')
            cmd=j(d/f'{stage}.command.json'); need(str(inp) in cmd,'command source')
            if stage=='probe':
                need(cmd==['/opt/homebrew/bin/ffprobe','-v','warning','-select_streams','v:0','-show_frames','-show_streams','-show_format','-of','json',str(inp)],'probe command')
            else:
                vf="select='"+"+".join('eq(n,%d)'%i for i in expected[num])+"',showinfo"
                want=['/opt/homebrew/bin/ffmpeg','-nostdin','-hide_banner','-nostats','-loglevel','level+info','-n','-copyts','-noautorotate','-guess_layout_max','0','-i',str(inp),'-map','0:v:0','-an','-sn','-dn','-map_metadata','-1','-map_chapters','-1','-vf',vf,'-noautoscale','-pix_fmt','rgb24','-fps_mode','passthrough','-enc_time_base:v','demux',str(d/'native/frame-%06d.png')]
                need(cmd==want,'decode command')
        need((d/'probe.stderr').read_bytes()==b'' and (d/'decode.stdout').read_bytes()==b'','unexpected diagnostic stream')
        logs=(d/'decode.stderr').read_text(encoding='utf-8'); lines=logs.splitlines()
        need(not re.search(r'\[(?:warning|error|fatal|panic)\]',logs,re.I),'explicit diagnostic')
        need(all('[info]' in z for z in lines if z.strip()),'untagged diagnostic')
        need(all(ord(c)>=32 or c in '\n\r\t' for c in logs),'control character')
        configs=re.findall(r'config in time_base: (\S+), frame_rate:',logs)
        need(len(configs)==1 and F(configs[0])==tb,'showinfo timebase')
        shows=re.findall(r'\[info\] n:\s*(\d+) pts:\s*(-?\d+) pts_time:(\S+)\s+duration:\s*\d+ duration_time:\S+ fmt:(\S+) cl:\S+ sar:(\S+) s:(\d+)x(\d+) i:(\S+)',logs)
        need(len(shows)==len(fr),'showinfo count')
        for n,(show,r) in enumerate(zip(shows,fr)):
            a,pts,t,fmt,sar,w,hh,inter=show
            need((int(a),int(pts),fmt,sar,int(w),int(hh),inter)==(n,r['pts'],'yuv411p','8/9',720,480,'B'),'showinfo fields')
            need(abs(F(t)-F(r['pts_seconds_exact']))<=F(1,2000000),'showinfo time')
        final=re.findall(r'\[info\] frame=\s*(\d+) .*Lsize=',logs);need(final==[str(len(fr))],'final output count')
        need(len(re.findall('color_range:unknown color_space:unknown color_primaries:unknown color_trc:unknown',logs))==len(fr),'color line count')
        for k,v in pins.items():need(rec['pins'][k]==v,'receipt pin')
        need(rec['source']==src and rec['source_identity']['before']==actual and rec['source_identity']['after']==actual,'receipt source')
        need(rec['source_identity']['status']=='matched_before_and_after' and rec['structure']=='inventory_and_products_checked','receipt structure')
        need(rec['probe_diagnostics']=={'bytes':0,'nonempty_lines':0,'rejected':[],'status':'clean'},'probe receipt')
        need(rec['decode_diagnostics']['status']=='clean' and rec['decode_diagnostics']['rejected']==[],'decode receipt')
        kinds={'duration':1,'final_summary':1,'input':1,'input_audio':1,'input_video':1,'mapping':1,'metadata':2,'metadata_entry':2,'output':1,'output_summary':1,'output_video':1,'show_color':len(fr),'show_config_in':1,'show_config_out':1,'show_frame':len(fr),'video_mapping':1}
        need(rec['decode_diagnostics']['accepted_line_kinds']==kinds and sum(kinds.values())==len(lines),'line accounting')
        need(rec['scientific_or_human_acceptance'] is False and not rec['reasons'] and rec['admission']=='descriptive_candidate_pending_independent_and_human_review','admission ceiling')
        rr=j(b/run/'run-receipt.json')
        need(rr['status']=='descriptive_candidates_only' and not rr['reasons'],'run receipt')
        for k,v in pins.items():need(rr['pins'][k]==v,'run pin')
        need((b/run/'manifest.input.json').read_bytes()==(b/'selection.json').read_bytes(),'manifest snapshot')
        need((b/run/'plan.input').read_bytes()==(b/'FRAME-PLAN.md').read_bytes(),'plan snapshot')
        repeat[run]={x:h(d/x) for x in ['frames.json','probe.stdout']}
        repeat[run]['pngs']=[(r['png_sha256'],r['rgb_sha256']) for r in fr]
        inventory_total+=len(rows);png_total+=len(fr)
        nonframes=[re.sub(r'(?<=@ )0x[0-9a-f]+','0xADDR',z) for z in lines if 'Parsed_showinfo_' not in z]
        print('run',run,num,'inventory',len(rows),'PNGs',len(fr),'probe_stderr',0,'decode_lines',len(lines),'showinfo',len(shows),'statuses',0,0)
        print('non_showinfo_lines',json.dumps(nonframes))
        print('product_pins',run,num,repeat[run]['frames.json'],repeat[run]['probe.stdout'])
    need(repeat['run01']==repeat['run02'],'repeat products')
need((inventory_total,png_total)==(2106,128),'total coverage')
print('PASS inventory_rows',inventory_total,'PNG_instances',png_total,'source_product_pairs',2)
print('pins',pins)
PY
```

Final audit output included `PASS inventory_rows 2106 PNG_instances 128 source_product_pairs 2`; exit 0. Separate `shasum -a 256`, version-header and version-status reads supplied the additional pins/status observations above.


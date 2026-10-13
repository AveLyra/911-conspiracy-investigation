"""Read-only image recovery audit. Writes bounded review records/previews only.

Never deletes, links, replaces or restores investigation files. Frozen decoder
commands are adapted only at input/output locations to send PNGs through RAM.
"""
import collections
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version

BASE = Path('${SOURCE_WORKSPACE}')
OUT = BASE/'outputs/911-context-review-2026-10-12'
PRIOR = BASE/'outputs/911-image-relevance-2026-10-12'
VAULT = BASE/'outputs/911-image-recovery'
REPO = Path('${SOURCE_CASE_REPOSITORY}')
REV = '354af3e8b34e9ff3ffbb5f29e643538e090e63d1'
PREFIX = 'research/sherlock-wtc7-investigation/'
LFS = [REPO/'.git/lfs/objects', REPO/'.git/modules/911-conspiracy-investigation-public/lfs/objects']
MIN_FREE = 10_000_000_000

def sha(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def save(path, value):
    with open(path,'x') as f: json.dump(value,f,indent=2)

def csvsave(path, rows, fields=None):
    with open(path,'x',newline='') as f:
        w=csv.DictWriter(f,fields or list(rows[0]))
        w.writeheader(); w.writerows(rows)

def guard():
    s=os.statvfs(BASE)
    if s.f_bavail*s.f_frsize < MIN_FREE: raise RuntimeError('10 GB free reserve reached; originals untouched')

def prepare():
    guard()
    OUT.mkdir()
    for name in ['frozen-records','previews','receipts']: (OUT/name).mkdir()
    scope=list(csv.DictReader(open(PRIOR/'priority-context-keep.csv')))
    assert len(scope)==913 and len({r['sha256'] for r in scope})==913
    core={r['sha256'] for r in csv.DictReader(open(PRIOR/'priority-core-keep.csv'))}
    assert not core & {r['sha256'] for r in scope}
    manifest=json.load(open(VAULT/'recovery-manifest.json'))
    assert manifest['source_commit']==REV
    files={r['source_path']:r for r in manifest['restored']}
    frozen={}
    def blob(rel, parse=True):
        if rel not in frozen:
            data=subprocess.check_output(['git','-C',str(REPO),'show',REV+':'+PREFIX+rel])
            dest=OUT/'frozen-records'/rel
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data)
            frozen[rel]={'git_reference':str(REPO)+'@'+REV+':'+PREFIX+rel,'path':str(dest),
                         'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
        data=Path(frozen[rel]['path']).read_bytes()
        return json.loads(data) if parse else data
    groups=collections.defaultdict(list)
    for r in scope:
        rel=r['representative_source_path'][len(PREFIX):]
        groups[str(Path(rel).parent.parent)].append(r)
    specs=[]; flat=[]; pages=[]; next_id=1
    for number,(run,members) in enumerate(sorted(groups.items()),1):
        members.sort(key=lambda r:r['representative_source_path'])
        historical_status='descriptive_source_screen_only'
        if run.startswith('cbs-vince-source-screen'):
            clip=int(re.search(r'vince-clip(\d+)$',run)[1]); stage=(clip+1)//2
            src=next(x for x in blob(f'cbs-vince-source-screen/stage{stage}/preparation01/sampling-manifest.json')['sources'] if x['id']==f'vince-clip{clip}')
            argv=blob(run+'/decode.command.json'); frames=blob(run+'/frames.json')
            blob(f'cbs-vince-source-screen/stage{stage}/sample_frames.py',False) if False else None
        elif run.startswith('cbs-vms-content-check'):
            receipt=blob(run+'/receipt.json'); argv=blob(run+'/decode.command.json'); frames=blob(run+'/frames.json')
            locs={x['order']:x for x in blob(run+'/locators.json')}
            for f in frames: f.update({'pts':locs[f['order']]['pts'],'time_base':locs[f['order']]['time_base']})
            src={'id':'CBS-VMS','path':argv[argv.index('-i')+1],'sha256':receipt['source_sha256'],'bytes':8717690}
            blob('cbs-vms-content-check/sample_candidate.py',False); blob(run+'/plan-pin.json')
            historical_status=receipt['status']
        elif run.startswith('late-fire-catalog-join'):
            receipt=blob(run+'/receipt.json'); argv=blob(run+'/decode.command.json'); frames=blob(run+'/frames.json')
            src={'id':'CBS-Net-Dub6-44','path':receipt['source'],'sha256':receipt['source_sha256'],'bytes':receipt['source_bytes']}
            blob('late-fire-catalog-join/sample_frames.py',False)
            historical_status='DV_decode_errors_manual_review_required_not_admitted'
        else:
            failed=run.endswith('/VID-WTC7-001') or run.endswith('/VID-WTC7-006')
            receipt=blob(run+('/failure.json' if failed else '/receipt.json'))
            src=receipt['source']
            commands=[c['argv'] for c in receipt['commands'] if '-i' in c['argv'] and Path(c['argv'][0]).name=='ffmpeg']
            assert len(commands)==1
            argv=commands[0]
            frames=blob(run+('/planned-frames.json' if failed else '/frames.json'))
            historical_status=('historical_decode_refusal_preserved_'+receipt['category']) if failed else receipt['status']
            snap=str(Path(run).parent/'screen_local.snapshot.py')
            blob(snap,False)
            if failed: blob(run+'/start.json')
        candidates=[Path(src['path'])]+[root/src['sha256'][:2]/src['sha256'][2:4]/src['sha256'] for root in LFS]
        candidates=list(dict.fromkeys(str(p) for p in candidates if p.is_file() and p.stat().st_size==src['bytes']))
        assert candidates, (run,'preserved source video not found')
        source=Path(candidates[-1]) # use stable content-addressed copy if present
        current_sha=sha(source)
        assert current_sha==src['sha256'],(run,'source video hash differs')
        groupid=f'G{number:02d}'
        by_name={}
        for i,f in enumerate(frames,1):
            name=Path(f.get('file') or f.get('png') or f.get('path') or f'native/frame-{i:06d}.png').name
            by_name[name]=f
        actual=[]
        for r in members:
            guard()
            file=Path(r['representative_path']); s=file.stat()
            assert s.st_size==int(r['bytes']) and sha(file)==r['sha256']
            f=by_name[file.name]
            expected=f.get('png_sha256') or f.get('sha256')
            if expected: assert expected==r['sha256'],(run,file.name,'frozen PNG differs')
            with Image.open(file) as im:
                im.load(); assert im.size==(int(r['width']),int(r['height']))
                rgb=hashlib.sha256(im.convert('RGB').tobytes()).hexdigest()
            if f.get('rgb_sha256'): assert rgb==f['rgb_sha256']
            srcindex=f.get('source_index',f.get('source_frame_index'))
            assert srcindex is not None
            row={**r,'review_id':f'I{next_id:04d}','group_id':groupid,'run':run,
                 'filename':file.name,'source_index':srcindex,'source_pts':f.get('pts',f.get('source_pts','')),
                 'time_base':f.get('time_base',f.get('source_time_base','')),
                 'encoded_seconds':f.get('pts_seconds_exact',f.get('source_seconds_exact','')),
                 'video_sha256':src['sha256'],'preserved_video_path':str(source),
                 'rgb_sha256_current':rgb,'frozen_original_png_sha256':expected or '',
                 'historical_status':historical_status,'initial_stat':{'dev':s.st_dev,'ino':s.st_ino,'nlink':s.st_nlink,'size':s.st_size,'mtime_ns':s.st_mtime_ns,'blocks':s.st_blocks},
                 'frozen_frame_record':f}
            actual.append(row); flat.append(row);next_id+=1
        # Frozen full frame roster may include other unique objects; emission order
        # is verified against every saved row, and context membership stays exact.
        specs.append({'group_id':groupid,'run':run,'source_pin':src,'preserved_video_path':str(source),
                      'existing_video_paths':candidates,'source_current_sha256':current_sha,
                      'source_stat':{'size':source.stat().st_size,'mtime_ns':source.stat().st_mtime_ns,'inode':source.stat().st_ino},
                      'original_argv':argv,'historical_status':historical_status,'frames':frames,'scope':actual})
        # Every object appears in one labeled page. Thumbnails preserve the full
        # image including borders; no crop, retouching or frame selection.
        for start in range(0,len(actual),16):
            chunk=actual[start:start+16]; pageid=f'P{len(pages)+1:03d}'
            canvas=Image.new('RGB',(1560,1390),'#14191f'); draw=ImageDraw.Draw(canvas)
            font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',14)
            titlefont=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',20)
            draw.text((14,8),f'{pageid} {groupid} {run}',fill='white',font=titlefont)
            draw.text((14,38),'Full uncropped frames; <=384 x 288 previews; AI retention review only',fill='#c7ccd5',font=font)
            for cell,r in enumerate(chunk):
                x=8+(cell%4)*390; y=70+(cell//4)*330
                with Image.open(r['representative_path']) as im:
                    im=im.convert('RGB');im.thumbnail((384,288),Image.Resampling.LANCZOS)
                    canvas.paste(im,(x+(384-im.width)//2,y+(288-im.height)//2))
                draw.text((x,y+292),f'{r["review_id"]} {r["filename"]}',fill='white',font=font)
                draw.text((x,y+310),f'n={r["source_index"]} pts={r["source_pts"]}',fill='#c7ccd5',font=font)
                r['preview_page']=pageid;r['preview_cell']=cell+1
            dest=OUT/'previews'/(pageid+'.jpg');canvas.save(dest,quality=84,optimize=True)
            pages.append({'page_id':pageid,'group_id':groupid,'path':str(dest),'sha256':sha(dest),
                          'review_ids':[r['review_id'] for r in chunk],'object_sha256s':[r['sha256'] for r in chunk]})
        print(groupid,run,len(actual),'source verified',flush=True)
    csvsave(OUT/'frozen-records.csv',list(frozen.values()))
    save(OUT/'scope.json',flat);save(OUT/'groups.json',specs);save(OUT/'pages.json',pages)
    (OUT/'original-context-scope.csv').write_bytes((PRIOR/'priority-context-keep.csv').read_bytes())
    save(OUT/'audit-scope.json',{'status':'prepared_no_deletion','scope_count':len(flat),'groups':len(specs),'pages':len(pages),
         'recovery_manifest_sha256':sha(VAULT/'recovery-manifest.json'),'scope_csv_sha256':sha(PRIOR/'priority-context-keep.csv'),
         'core_csv_sha256':sha(PRIOR/'priority-core-keep.csv'),'source_commit':REV,
         'acceptance':['Every one of 913 unique objects visually reviewed using labeled uncropped previews; uncertain cases inspected individually',
                       'Current preserved video bytes SHA-256 verified before and after decoding',
                       'Every candidate PNG reproduced from frozen selected source positions and compared byte-for-byte with its current hash',
                       'Recovery qualifications and historical processing refusals retained',
                       'Specific all-link/object deletion proposal produced; zero files deleted'],
         'dependencies':'Preserved video bytes, frozen source positions/options, currently installed FFmpeg and loaded libraries',
         'exclusions':['Deletion','Public/private upload','Changes to study authority','Core images','Source videos','Unrelated projects/caches'],
         'free_bytes_at_preparation':os.statvfs(BASE).f_bavail*os.statvfs(BASE).f_frsize,'pillow':pillow_version})
    print('PREPARED',len(flat),'objects',len(pages),'pages',flush=True)

def exact_read(s,n):
    pieces=[]
    while n:
        b=s.read(n)
        if not b: raise RuntimeError('truncated PNG stream')
        pieces.append(b);n-=len(b)
    return b''.join(pieces)

def png_read(s):
    signature=s.read(8)
    if not signature: return None
    if signature!=b'\x89PNG\r\n\x1a\n':raise RuntimeError('non-PNG stream')
    parts=[signature];total=8
    while True:
        length=exact_read(s,4);n=int.from_bytes(length,'big')
        if n>16_000_000 or total>24_000_000:raise RuntimeError('bounded PNG limit')
        kind=exact_read(s,4);payload=exact_read(s,n+4);total+=n+12
        parts.extend([length,kind,payload])
        if kind==b'IEND':return b''.join(parts)

def verify():
    guard()
    groups=json.load(open(OUT/'groups.json'));scope=json.load(open(OUT/'scope.json'))
    ffmpeg=Path(groups[0]['original_argv'][0])
    version=subprocess.check_output([str(ffmpeg),'-version']).decode()
    deps=subprocess.check_output(['/usr/bin/otool','-L',str(ffmpeg)]).decode()
    save(OUT/'decoder.json',{'path':str(ffmpeg),'resolved_path':str(ffmpeg.resolve()),'sha256':sha(ffmpeg),
         'version':version,'otool_direct_dependencies':deps,'python':sys.version,'pillow':pillow_version,
         'runtime_restoration_tested':False,'note':'Current byte recovery is tested. Future decoding after toolchain changes may differ; dependency hashes recorded separately.'})
    allresults=[];summary=[]
    for g in groups:
        guard();start=time.monotonic();gid=g['group_id'];src=Path(g['preserved_video_path']);pin=g['source_pin']
        before=sha(src);assert before==pin['sha256'] and src.stat().st_size==pin['bytes']
        argv=g['original_argv'][:-1];argv[argv.index('-i')+1]=str(src)
        argv+=['-c:v','png','-f','image2pipe','pipe:1']
        stderrpath=OUT/'receipts'/(gid+'.stderr.txt')
        rows=[];error=None;status=None;extra=False
        scoped={r['filename']:r for r in g['scope']}
        def terminate():
            if process.poll() is None: process.kill()
        with open(stderrpath,'xb') as err:
            process=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=err)
            timer=threading.Timer(600,terminate);timer.start()
            try:
                for ordinal,f in enumerate(g['frames'],1):
                    guard()
                    data=png_read(process.stdout)
                    if data is None:raise RuntimeError('too few source frames')
                    name=Path(f.get('file') or f.get('png') or f.get('path') or f'native/frame-{ordinal:06d}.png').name
                    h=hashlib.sha256(data).hexdigest()
                    frozen=f.get('png_sha256') or f.get('sha256')
                    with Image.open(io.BytesIO(data)) as im:
                        im.load();rgb=hashlib.sha256(im.convert('RGB').tobytes()).hexdigest();size=im.size;mode=im.mode
                    r=scoped.get(name)
                    row={'ordinal':ordinal,'filename':name,'source_index':f.get('source_index',f.get('source_frame_index')),
                         'generated_png_sha256':h,'generated_bytes':len(data),'generated_rgb_sha256':rgb,
                         'width':size[0],'height':size[1],'mode':mode,'frozen_png_sha256':frozen or '',
                         'frozen_png_match':h==frozen if frozen else None,'frozen_rgb_match':rgb==f['rgb_sha256'] if f.get('rgb_sha256') else None,
                         'context_scope_member':bool(r)}
                    if r:
                        row.update({'review_id':r['review_id'],'current_png_sha256':r['sha256'],
                                    'current_png_match':h==r['sha256'],'current_rgb_match':rgb==r['rgb_sha256_current'],
                                    'current_size_match':len(data)==int(r['bytes']),
                                    'current_dimensions_match':size==(int(r['width']),int(r['height']))})
                    rows.append(row)
                extra=png_read(process.stdout) is not None
                status=process.wait(timeout=30)
            except Exception as exc:
                error=str(exc)
            finally:
                timer.cancel();process.stdout.close()
                if process.poll() is None:process.kill();process.wait(timeout=30)
                if status is None:status=process.returncode
        after=sha(src)
        passed=not error and not extra and status==0 and before==after==pin['sha256'] and len(rows)==len(g['frames'])
        results=[]
        for row in rows:
            if not row['context_scope_member']:continue
            r=next(r for r in g['scope'] if r['review_id']==row['review_id'])
            okay=passed and row['current_png_match'] and row['current_rgb_match'] and row['current_size_match'] and row['current_dimensions_match']
            if row['frozen_png_match'] is False or row['frozen_rgb_match'] is False:okay=False
            results.append({**row,'group_id':gid,'run':g['run'],'preserved_video_path':str(src),
                            'video_sha256':pin['sha256'],'group_execution_passed':passed,'byte_recovery_verified':bool(okay),
                            'has_original_hash_verified_path':r['has_original_hash_verified_path'],'historical_status':g['historical_status']})
        allresults.extend(results)
        receipt={'group_id':gid,'run':g['run'],'source_pin':pin,'preserved_video_path':str(src),
                 'source_sha256_before':before,'source_sha256_after':after,'original_argv':g['original_argv'],'verification_argv':argv,
                 'decoder_sha256':sha(ffmpeg),'returncode':status,'error':error,'extra_png':extra,
                 'stderr_path':str(stderrpath),'stderr_sha256':sha(stderrpath),'stderr_bytes':stderrpath.stat().st_size,
                 'elapsed_seconds':time.monotonic()-start,'group_execution_passed':passed,
                 'historical_status_unchanged':g['historical_status'],'frames':rows,
                 'scope':'PNG byte/pixel reproducibility only; no source authentication, event clock or scientific/human admission'}
        save(OUT/'receipts'/(gid+'.json'),receipt)
        summary.append({k:receipt[k] for k in ['group_id','run','elapsed_seconds','returncode','error','group_execution_passed','stderr_bytes']})
        n=sum(r['byte_recovery_verified'] for r in results)
        print(gid,'verified',n,'/',len(g['scope']),'seconds',round(receipt['elapsed_seconds'],2),flush=True)
    expected={r['review_id'] for r in scope};covered={r['review_id'] for r in allresults}
    missing=sorted(expected-covered)
    save(OUT/'recovery-results.json',allresults)
    csvsave(OUT/'recovery-results.csv',allresults, sorted(set().union(*(r.keys() for r in allresults))))
    save(OUT/'recovery-summary.json',{'scope':len(scope),'covered':len(covered),'missing':missing,
          'byte_recovery_verified':sum(r['byte_recovery_verified'] for r in allresults),'groups':summary,
          'source_manifest_sha256_after':sha(VAULT/'recovery-manifest.json'),
          'no_image_writes':True,'no_deletions':True})
    print('COMPLETE',sum(r['byte_recovery_verified'] for r in allresults),'/',len(scope),'byte recovered; missing',missing,flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['prepare']:prepare()
    elif sys.argv[1:]==['verify']:verify()
    else:raise SystemExit('Use prepare or verify; this script has no delete mode.')

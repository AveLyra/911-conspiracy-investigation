# Independent extraction and method verification

September 20, 2026 UTC. Working research only under [PROTOCOL.md](PROTOCOL.md)
and the full investigation charter. Main AGENTS/WORKFLOW/START-HERE, full
charter, current STATUS opening/current-next-task, the complete new protocol,
pinned A/V helper and its complete Peskin dependency were read. A combined
controls/status return truncated; bounded follow-up reads supplied the missing
control/current-task context. Source-preservation, evidence-audit and
development-verification skills govern this check.

**PASS within numerical/input/derivative scope for final run02/run03.**
The exact selected clock set, preserved source/runtime pins, all recorded
products, paired historical images, known synthetic pixels and a fresh
source-to-PNG RGB checksum comparison reconcile. Original warning histories
remain; this is not a warning-free claim, visual acceptance, historical
authentication or physical validation.

No historical image was displayed by this reviewer. One independently invoked
historical decode produced only frame hashes in memory/stdout, not new images.
The only project file written by this reviewer is this note; generated harmless
control/diagnostic outputs are retained in the temporary directory below.
No source, producer code, frozen observation or canonical/legal record changed.

## Review chronology and implementation boundary

The initial driver, SHA-256
`0b53e73c8cba8789b59aa87f284e7eb56405ce32effac32f4165e8c1088bd48d`,
was reviewed after it was written. Root reports run01 had already completed
before receiving this reviewer's defect message; no timeout or visual admission
had occurred in that initial run. Do not label this code review pre-execution
or relabel run01 as a failed historical decode.

The actual defect was a failure path: inherited Runner.run could raise
TimeoutExpired before recording its command or captured stdout/stderr.
The driver also lacked final code/dependency/binary identity comparisons.
Root preserved the original exact bytes as
`run01/extract_window-initial.py.snapshot`, repaired only the local driver
and produced final paired runs. The extra initial snapshot was added after
run01's original receipt, not silently represented as an original product.

Reviewed final driver SHA-256:
`e316e1fd6e76cdd770e7ec7637491ea7b552d3a9c475a5c38d5d37552538c726`.
The timeout/nonzero failure path now preserves captured output and command
information; successful runs compare script, both dependencies plus protocol,
FFmpeg/ffprobe and Python executable identities before/after.

Pinned dependencies independently read/rehashed:

| Input | SHA-256 |
|---|---|
| PROTOCOL.md | 1d1d1993a6d9a27f66037d5abef449ffe685e7238c20a81a9b85f97ae240883c |
| Main acoustic-audit/av-correspondence/extract_frames.py | 2fc45bb67ba656c3670fea188f2b71261a9ca315718aaf92e16010ef4bcceb6a |
| Main fire-originals/peskin/sample_every_second.py | a913be680052ceb61ddf1ed89ef675c9d21972f8869a62e9e038be2f8048d40b |
| Initial driver snapshot | 0b53e73c8cba8789b59aa87f284e7eb56405ce32effac32f4165e8c1088bd48d |

The initial/final `boundary_plan` and `selection_controls` function ASTs
were separately compared and are identical. The standalone ten selector
controls passed on both versions. The initial version additionally matched an
independent exact-index oracle for 500 deterministic irregular-PTS cases:
296 admissible selections and 204 expected refusals. This tests finite declared
cases, not all possible clocks or generic decoder correctness.

## Exact coverage and source identity

Source:
`/Users/admin/docs/911/research/wtc7-video-comparison/media/comparators/explosive/Capital One Tower Implosion [rW_xXcS4y3A].f136.mp4`,
4901052 bytes, SHA-256
`8560cd686a18c8fcc16fe802691e0f17f117c713b4cd1862017af24d391ce5a2`.

The whole-copy source index is the zero-based position in the 1350-row PTS
inventory; output PNG ordinal is a separate namespace. Both fresh full
inventories exactly equal the held run01 A/V inventory, whose SHA-256 is
`d8496f26d271eda8955e0fc46b3ff98754c2b5bc06793e8729adf0840a387c3b`.

| Selection | Whole-source indices | Count | Encoded clock |
|---|---|---:|---|
| Half-open requested interval | 240–479 | 240 | 8 ≤ PTS/30000 < 16 |
| Immediate preceding row | 239 | 1 | 239239/30000 s |
| Immediate following row | 480 | 1 | 480480/30000 = 16.016 s |
| Complete retained set | 239–480 | 242 | Actual stored PTS, not assumed fps |

For example, output `comparator/frame-0001.png` is source index239, and
`frame-0242.png` is index480. Row `source_seconds_exact` joins exactly to
`source_pts × source_time_base`; `best_effort_timestamp` agrees with PTS.
Both fresh historical probe stderr files per run are empty. The stored raster
is 1280×720, RGB output from yuv420p, source time base1/30000 and SAR1:1.

Inter-frame float sentinels only adapt the old helper's JSON plan interval;
their exact constructions are `159159/20000` and `961961/60000`. The driver
checks that the resulting floats stay strictly between the appropriate exact
frame times and that selected indices equal the exact target index list.
These row `interval` values are extraction sentinels, not onset times, physical
uncertainty limits or a replacement for the requested [8,16) window.

## Final paired products and known-pixel checks

| Final run | Receipt SHA-256 | Recorded products | Historical PNGs | Synthetic PNGs independently pixel-checked |
|---|---|---:|---:|---:|
| run02 | e17b37b98c136ba81c79c70ccd03f4b709b127507fd5c6111c5b217b2a14856c | 364 | 242 | 92 |
| run03 | e7f2303079ad3810ccab88d403eb548a71b05db9bdb5f4e595e043bfdfcd4f28 | 364 | 242 | 92 |

Both receipts are `complete`, with 13 subprocess commands each, all exit0.
Every recorded product's current byte count/SHA-256 matches (728 total), and
actual membership equals the receipt's listed product set after excluding
start.json/receipt.json. Script snapshots equal the final script. Start versus
final receipt pins, before/after identities and current source/dependency/
binary/Python executable identities all agree. Current Pillow12.0.0 and
NumPy2.3.4 versions agree with the receipts; Python is3.13.7.

All242 historical PNG byte pairs and complete selected maps match exactly.
Six paired metadata/control files also match byte-for-byte: full historical
inventory, stream description, selected map, sentinels, selector controls and
old synthetic check results. Log bytes contain process/runtime details and
are not required to be identical. Every historical PNG has the declared
single-frame RGB1280×720 header contract.

This reviewer reconstructed the independent expected pixel arrays for both
synthetic offsets (0 and5), the original20-image selections and new26-image
boundary selections: **92 images/run, 184 exact known-pixel matches total**.
The boundary selections are exactly synthetic source indices5–30. These
fixtures exercise known RGB fields and clocks, not H.264 historical identity,
camera chronology or object-motion annotation.

The dedicated repaired-runner check independently executed:

- A harmless subprocess with a0.3-second timeout: TimeoutExpired raised;
  exact12-byte stdout and12-byte stderr and the attempted command/timeout
  fields remained available.
- A harmless exit3 subprocess: RuntimeError raised; exact9-byte stdout and
  stderr plus command/exit status remained.
- A preexisting run directory containing a28-byte sentinel: main refused
  before extraction and the sentinel/membership stayed unchanged.

Those are **10 selector checks plus three distinct failure/non-overwrite
checks** on the final driver. They are not process-tree kill tests or a
demonstration that every filesystem/process failure is covered. No historical
process timed out in this review.

## Fresh source-RGB correspondence

With explicit root authorization, this reviewer independently invoked the
pinned FFmpeg binary from source start, used the compact selection
`between(n,239,480)` rather than the producer's enumerated expression, converted
to RGB24, and emitted SHA-256 framehash rows instead of PNG images. No input
seek, scale, rotation, interpolation or new image file was used.

All242 hash rows have the correct source PTS/timebase and2764800 packed RGB
bytes. Each matches the SHA-256 of the decompressed RGB bytes of its pinned
run02 PNG exactly; run03's identical PNG bytes extend that correspondence to
the paired set. Source and FFmpeg binary hashes were unchanged after the check.
The invocation returned exit0, preserving all stdout/stderr locally.

This is an independently executed selection/output/checksum route using the
**same FFmpeg decoder and color-conversion family**, not a second independent
decoder implementation. It does not prove original exposure cadence, historical
speed, exact colorimetry, feature identity or a physical onset.

## Diagnostic categories, retained fallback and residual gate

Both final runs retain exactly13 notices:
`No accelerated colorspace conversion found from yuv420p to rgb24.`
The fresh independent framehash invocation also retains13. The inherited
keyword-only rejection filter does not catch this wording. A helper receipt's
`complete` status therefore means execution completed, not automatic diagnostic
or scientific admission.

The complete saved stderr lines from each final run were classified without
printing arbitrary metadata. Counts per run are:

| Category | Count |
|---|---:|
| I/O headers | 15 |
| Metadata lines/headings | 59 |
| Stream descriptions | 20 |
| Colorspace-fallback notices requiring explicit assessment | 13 |
| showinfo lines | 681 |
| Progress lines | 7 |
| Output summaries | 5 |
| Empty stderr files (separate file count) | 8 |

The681 showinfo lines comprise334 frame rows,334 color rows,10 filter-clock
configuration lines,2 frame-side-data lines and1 blank showinfo line.
A preliminary classifier left12 metadata lines unclassified per run; inspection
of field names identified `compatible_brands` and `Metadata` formatting.
The corrected classifier explicitly handles these and rejects unknown lines.
No unclassified diagnostic category or keyword-indicated corruption/error
remained; this does **not** erase the fallback notices.

Root's [execution record](execution.md) attributes its fallback interpretation
to official FFmpeg7.1 source and discloses that software-documentation lookup
as a deviation from the protocol's original no-new-network wording. This
reviewer made no network request or independent upstream-source retrieval.
The runtime records identify FFmpeg7.1.1/libswscale8.3.100 through root's
assessment; matching source-family documentation is not exact loaded-library
build proof. The source lookup and descriptive-use admission remain attributed
to root, while current pixels/counts/categories were checked here.

No blanket fallback whitelist or general warning-free claim is warranted.
Fresh unrecognized diagnostics in another run require assessment. Current
agreement supports the recorded RGB derivative under the declared descriptive
shape/motion use, not calibrated brightness, thermal measurements or native
camera authenticity. Root's initial index239 display and later feature choices
are outside this reviewer's visual coverage.

## Local evidence and actual commands

Commands below ran from:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/`,
with `PYTHONDONTWRITEBYTECODE=1` and
`/Users/admin/.pyenv/versions/3.13.7/bin/python3`.
All reported checks returned exit0; the deliberately failing child processes
were caught/verified as specified, not counted as successful subprocesses.

Generated diagnostic/control files are retained at
`/private/tmp/roof-onset-review.6jJtK5/`, created by
`mktemp -d /private/tmp/roof-onset-review.XXXXXX`. These are temporary local
evidence, not source files or guaranteed durable project storage.

| Local check product | SHA-256 |
|---|---|
| framehash-check.json | 50d44381b75c449cd14b74a3f8280694b5473f8c79ef947c6f075e7540498f63 |
| paired-product-check.json | 653084952ae101cf4ae53e54a65a62b250552188a90df690fde85dd075cab79a |
| framehash.stdout.local.txt (27325 bytes) | a744a770c5c02c89a81c8d8cbd75d97d9bd893e0b1d185b007f6b2e42cd34281 |
| framehash.stderr.local.txt (3524 bytes) | 5a34d22496e54f294a48843147a8f1f63be9821b119b3c9e0c8b7c69a58ae549 |

The recipes preserve the actual paths/commands used. Re-executing create-only
checks requires a new explicitly named temporary directory; do not overwrite
the retained evidence to obtain a repeat.

### Pure exact-selector/inventory check (initial driver)

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
from fractions import Fraction
import hashlib, json, random, types
p=Path("research/sherlock-wtc7-investigation/comparator-roof-onset/extract_window.py")
b=p.read_bytes()
m=types.ModuleType("bounded_driver_review"); m.__file__=str(p.resolve())
exec(compile(b,str(p),"exec"),m.__dict__)
checks=m.selection_controls()
assert len(checks)==10 and all(checks.values())
rng=random.Random(20260920)
positive=negative=0
for case in range(500):
    pts=[rng.randint(-100,100)]
    for j in range(rng.randint(4,40)): pts.append(pts[-1]+rng.randint(1,9))
    tick=Fraction(1,rng.choice([1,3,11,30000]))
    start=Fraction(rng.randint(pts[0]-10,pts[-1]+10))*tick
    end=start+Fraction(rng.randint(1,30))*tick
    inside=[i for i,t in enumerate(pts) if start<=t*tick<end]
    admissible=bool(inside) and inside[0]>0 and inside[-1]<len(pts)-1
    try:
        _,actual,_=m.boundary_plan([{"pts":v} for v in pts],tick,start,end)
    except ValueError:
        assert not admissible,case
        negative+=1
    else:
        assert admissible and actual==list(range(inside[0]-1,inside[-1]+2)),case
        positive+=1
inventory=Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/run01/comparator-all-frame-pts.json")
ib=inventory.read_bytes()
assert hashlib.sha256(ib).hexdigest()=="d8496f26d271eda8955e0fc46b3ff98754c2b5bc06793e8729adf0840a387c3b"
doc=json.loads(ib)
assert isinstance(doc,dict) and set(doc)=={"frames"}
frames=doc["frames"]
assert len(frames)==1350
plan,indices,sentinels=m.boundary_plan(frames,Fraction(1,30000),8,16)
inside=[i for i,f in enumerate(frames) if Fraction(8)<=Fraction(f["pts"],30000)<Fraction(16)]
assert inside==list(range(240,480)) and indices==list(range(239,481))
assert frames[239]["pts"]<240000<=frames[240]["pts"]
assert frames[479]["pts"]<480000<=frames[480]["pts"]
print(json.dumps({"status":"PASS pure read-only selection checks; no subprocess/decode called",
                  "driver_sha256":hashlib.sha256(b).hexdigest(),"builtin_controls":len(checks),
                  "independent_exact_oracle_cases":500,"positive":positive,"rejected":negative,
                  "held_inventory_count":len(frames),"interior_count":len(inside),
                  "bounded_output_count":len(indices),"first":{"index":239,**frames[239]},
                  "last":{"index":480,**frames[480]},"sentinels":sentinels},indent=2))

PY
```

### Repaired timeout, nonzero exit and existing-run refusal

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
import hashlib, json, subprocess, sys, types
p=Path("research/sherlock-wtc7-investigation/comparator-roof-onset/extract_window.py")
b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=="e316e1fd6e76cdd770e7ec7637491ea7b552d3a9c475a5c38d5d37552538c726"
m=types.ModuleType("repaired_driver_review"); m.__file__=str(p.resolve())
exec(compile(b,str(p),"exec"),m.__dict__)
out=Path("/private/tmp/roof-onset-review.6jJtK5")
assert out.is_dir() and not list(out.iterdir())
r=m.PreservingRunner(out)
timeout_cmd=[sys.executable,"-B","-c","import sys,time; print('timeout-out',flush=True); print('timeout-err',file=sys.stderr,flush=True); time.sleep(2)"]
try:
    r.run(timeout_cmd,"short-timeout",timeout=0.3)
except subprocess.TimeoutExpired:
    pass
else:
    raise AssertionError("timeout did not raise")
assert (out/"short-timeout.stdout.local.bin").read_bytes()==b"timeout-out\n"
assert (out/"short-timeout.stderr.local.txt").read_bytes()==b"timeout-err\n"
assert r.commands[0]=={"argv":timeout_cmd,"label":"short-timeout","exit":None,"status":"timeout",
                        "timeout_seconds":0.3,"stderr_bytes":12,"stdout_bytes":12}
exit_cmd=[sys.executable,"-B","-c","import sys; print('exit-out',flush=True); print('exit-err',file=sys.stderr,flush=True); sys.exit(3)"]
try:
    r.run(exit_cmd,"exit-three",timeout=1)
except RuntimeError:
    pass
else:
    raise AssertionError("nonzero exit did not raise")
assert (out/"exit-three.stdout.local.bin").read_bytes()==b"exit-out\n"
assert (out/"exit-three.stderr.local.txt").read_bytes()==b"exit-err\n"
assert r.commands[1]["exit"]==3 and r.commands[1]["argv"]==exit_cmd
checks=m.selection_controls()
assert len(checks)==10 and all(checks.values())
existing=out/"run02"; existing.mkdir()
(exists_marker:=existing/"preserved-fixture.bin").write_bytes(b"existing-output-must-survive")
prior=exists_marker.read_bytes()
old_here,old_argv=m.HERE,sys.argv
m.HERE=out; sys.argv=[str(p),"run02"]
try:
    try: m.main()
    except FileExistsError: pass
    else: raise AssertionError("existing output was accepted")
finally:
    m.HERE=old_here; sys.argv=old_argv
assert exists_marker.read_bytes()==prior and list(existing.iterdir())==[exists_marker]
assert hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(b).hexdigest()
print(json.dumps({"status":"PASS ten selector controls, real short-timeout/nonzero-output preservation, existing-run refusal",
                  "driver_sha256":hashlib.sha256(b).hexdigest(),"test_directory":str(out),
                  "commands":r.commands,"products":{str(f.relative_to(out)):{"bytes":f.stat().st_size,"sha256":hashlib.sha256(f.read_bytes()).hexdigest()}
                             for f in sorted(out.rglob("*")) if f.is_file()}},indent=2))

PY
```

### Independent source-framehash comparison

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
from io import BytesIO
from fractions import Fraction
import hashlib, json, re, subprocess
from PIL import Image
unit=Path("research/sherlock-wtc7-investigation/comparator-roof-onset")
scratch=Path("/private/tmp/roof-onset-review.6jJtK5")
def identity(p):
    b=p.read_bytes()
    return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
receipt=json.loads((unit/"run02/receipt.json").read_bytes())
source=Path(receipt["source_path"])
before=identity(source); binary=Path("/opt/homebrew/bin/ffmpeg"); tool_before=identity(binary)
assert before==receipt["source_before"] and tool_before==receipt["binaries"][str(binary)]
command=[str(binary),"-nostdin","-hide_banner","-loglevel","info","-n","-copyts","-noautorotate",
         "-i",str(source),"-map","0:v:0","-an","-vf","select='between(n,239,480)',format=rgb24",
         "-frames:v","242","-noautoscale","-pix_fmt","rgb24","-fps_mode","passthrough",
         "-enc_time_base:v","demux","-c:v","rawvideo","-f","framehash","-hash","sha256","-"]
try:
    result=subprocess.run(command,capture_output=True,timeout=60)
except subprocess.TimeoutExpired as e:
    for name,data in [("framehash.stderr.local.txt",e.stderr or b""),("framehash.stdout.local.txt",e.stdout or b"")]:
        with (scratch/name).open("xb") as f: f.write(data)
    raise
for name,data in [("framehash.stderr.local.txt",result.stderr),("framehash.stdout.local.txt",result.stdout)]:
    with (scratch/name).open("xb") as f: f.write(data)
assert result.returncode==0
lines=result.stdout.decode("ascii").splitlines()
assert "#hash: SHA256" in lines and "#tb 0: 1/30000" in lines and "#dimensions 0: 1280x720" in lines
checksums=[]
for line in lines:
    if not line or line.startswith("#"): continue
    stream,dts,pts,duration,size,digest=[a.strip() for a in line.split(",")]
    assert int(stream)==0 and int(size)==1280*720*3
    checksums.append((int(pts),int(size),digest))
rows=json.loads((unit/"run02/comparator-selected.json").read_bytes())
assert len(checksums)==len(rows)==242
for row,(pts,size,pin) in zip(rows,checksums):
    assert row["source_pts"]==pts and Fraction(row["source_seconds_exact"])==Fraction(pts,30000)
    b=(unit/"run02"/row["png"]).read_bytes()
    assert hashlib.sha256(b).hexdigest()==row["sha256"]
    with Image.open(BytesIO(b)) as im:
        assert im.mode=="RGB" and im.size==(1280,720) and im.n_frames==1
        pixels=im.tobytes()
    assert len(pixels)==size and hashlib.sha256(pixels).hexdigest()==pin
log=result.stderr.decode(errors="replace")
fallback="No accelerated colorspace conversion found from yuv420p to rgb24."
assert not re.search(r"corrupt|invalid data|error|warning|conceal",log,re.I)
assert identity(source)==before and identity(binary)==tool_before
record={"status":"PASS exact source-framehash / saved PNG RGB correspondence","count":242,"source":before,
        "ffmpeg":tool_before,"argv":command,"exit":result.returncode,
        "stdout":identity(scratch/"framehash.stdout.local.txt"),
        "stderr":identity(scratch/"framehash.stderr.local.txt"),
        "fallback_notice_count":log.count(fallback),"first_pts":checksums[0][0],"last_pts":checksums[-1][0],
        "limits":"Same FFmpeg decoder/color-conversion family; independent selection/checksum/output route, not historical authenticity or colorimetric calibration."}
with (scratch/"framehash-check.json").open("x") as f: json.dump(record,f,indent=2); f.write("\n")
print(json.dumps({k:v for k,v in record.items() if k!="argv"},indent=2))

PY
```

### Final products, controls, maps and complete diagnostic classification

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
from io import BytesIO
from fractions import Fraction
from collections import Counter
import hashlib,json,re,sys
import numpy as np
from PIL import Image
base=Path("research/sherlock-wtc7-investigation/comparator-roof-onset")
scratch=Path("/private/tmp/roof-onset-review.6jJtK5")
seen={}
def read(p):
    b=p.read_bytes(); seen[str(p.resolve())]=hashlib.sha256(b).hexdigest(); return b
def ident(p):
    b=read(p); return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def jload(p): return json.loads(read(p))
held=jload(Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/run01/comparator-all-frame-pts.json"))
results=[]; run_rows=[]
for run in ["run02","run03"]:
    d=base/run; receipt=jload(d/"receipt.json"); start=jload(d/"start.json")
    assert receipt["status"]=="complete" and receipt["historical_frames"]==242
    for field in ["source_before","script","dependencies","python_executable","binaries","python","pillow","numpy"]:
        assert start[field]==receipt[field],field
    for a,b in [("source_before","source_after"),("script","script_after"),("dependencies","dependencies_after"),
                ("binaries","binaries_after"),("python_executable","python_executable_after")]:
        assert receipt[a]==receipt[b],(a,b)
    assert ident(Path(receipt["source_path"]))==receipt["source_before"]
    assert ident(base/"extract_window.py")==ident(d/"extract_window.py.snapshot")==receipt["script"]
    for field in ["dependencies","binaries"]:
        for path,pin in receipt[field].items(): assert ident(Path(path))==pin
    assert ident(Path(sys.executable))==receipt["python_executable"]
    assert receipt["numpy"]==np.__version__ and receipt["pillow"]==Image.__version__
    products=receipt["products"]
    actual={str(p.relative_to(d)) for p in d.rglob("*") if p.is_file() and p.name not in ("start.json","receipt.json")}
    assert set(products)==actual and len(products)==364
    for path,pin in products.items(): assert ident(d/path)==pin,path
    assert all(c["exit"]==0 for c in receipt["commands"])
    assert len(receipt["commands"])==13
    for c in receipt["commands"]:
        assert len(read(d/(c["label"]+".stderr.local.txt")))==c["stderr_bytes"]
    assert all(jload(d/"selection-controls.json").values()) and len(jload(d/"selection-controls.json"))==10
    assert all(jload(d/"synthetic-checks.json").values()) and len(jload(d/"synthetic-checks.json"))==6
    stream=jload(d/"comparator-stream.json")["streams"][0]
    inventory=jload(d/"comparator-all-frame-pts.json")
    assert inventory==held
    assert len(inventory["frames"])==1350 and stream["time_base"]=="1/30000"
    assert read(d/"comparator-stream.stderr.local.txt")==read(d/"comparator-frames.stderr.local.txt")==b""
    rows=jload(d/"comparator-selected.json")
    assert [r["source_index"] for r in rows]==list(range(239,481))
    for r in rows:
        f=inventory["frames"][r["source_index"]]
        assert r["source_pts"]==f["pts"]==f["best_effort_timestamp"]
        assert Fraction(r["source_time_base"])==Fraction(1,30000)
        assert Fraction(r["source_seconds_exact"])==Fraction(f["pts"],30000)
        b=read(d/r["png"])
        assert {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}=={"bytes":r["bytes"],"sha256":r["sha256"]}
        with Image.open(BytesIO(b)) as im:
            assert im.mode=="RGB" and im.size==(1280,720) and im.n_frames==1
    run_rows.append(rows)
    synthetic_count=0
    for offset in [0,5]:
        for selection,count in [("selected",20),("boundary",26)]:
            label=f"synthetic-{offset}-{selection}"
            records=jload(d/(label+"-selected.json"))
            assert len(records)==count
            expected_indices=list(range(5,31)) if selection=="boundary" else list(range(0,24,3))+list(range(24,36))
            assert [r["source_index"] for r in records]==expected_indices
            for r in records:
                n=r["source_index"]; expected=np.zeros((48,64,3),dtype=np.uint8)
                expected[:,:,:]=[n*7%256,n*11%256,n*13%256]
                expected[4:20,5:30,:]=[255-n,n,90]
                with Image.open(BytesIO(read(d/r["png"]))) as im:
                    assert im.mode=="RGB" and im.n_frames==1
                    assert np.array_equal(np.asarray(im),expected)
                synthetic_count+=1
    categories=Counter(); shown=Counter()
    for p in sorted(d.glob("*.stderr.local.txt")):
        text=read(p).decode(errors="replace")
        assert not re.search(r"corrupt|invalid data|error|warning|conceal",text,re.I)
        lines=text.splitlines()
        if not lines: categories["empty_stderr_files"]+=1
        for line in lines:
            if not line.strip(): kind="blank"
            elif "No accelerated colorspace conversion found from yuv420p to rgb24." in line: kind="software_colorspace_fallback"
            elif line.startswith("[Parsed_showinfo_"):
                kind="showinfo"
                body=line.split("]",1)[1].strip()
                if body.startswith("n:"): subtype="frame"
                elif body.startswith("color_range:"): subtype="color"
                elif body.startswith(("config in","config out")): subtype="filter_configuration"
                elif body.startswith(("side data","UUID=","User Data=")): subtype="frame_side_data"
                elif not body: subtype="blank"
                else: raise AssertionError(("unclassified_showinfo",hashlib.sha256(body.encode()).hexdigest()))
                shown[subtype]+=1
            elif line.startswith(("Input #","Output #","Stream mapping:","Press [q]")): kind="io_header"
            elif line.strip()=="Metadata:" or re.match(r"^\s+[A-Za-z_][A-Za-z0-9_ -]*\s+:",line) or line.strip().startswith("compatible_brands:"): kind="metadata"
            elif line.startswith(("  Duration:","  Stream #")): kind="stream_description"
            elif re.match(r"^\[out#\d+/image2 @ ",line): kind="output_summary"
            elif line.startswith("frame="): kind="progress"
            else: raise AssertionError(("unclassified_line",hashlib.sha256(line.encode()).hexdigest()))
            categories[kind]+=1
    assert categories["software_colorspace_fallback"]==13
    results.append({"run":run,"receipt":ident(d/"receipt.json"),"products":len(products),"historical_pngs":242,
                    "known_pixel_pngs_checked":synthetic_count,"diagnostic_categories":dict(categories),"showinfo_subcategories":dict(shown)})
assert run_rows[0]==run_rows[1]
for r in run_rows[0]:
    assert read(base/"run02"/r["png"])==read(base/"run03"/r["png"])
for rel in ["comparator-all-frame-pts.json","comparator-stream.json","comparator-selected.json","selection-sentinels.json","selection-controls.json","synthetic-checks.json"]:
    assert read(base/"run02"/rel)==read(base/"run03"/rel),rel
for path,pin in seen.items(): assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==pin,("changed",path)
report={"status":"PASS final run products/pins/maps/pixels and complete diagnostic classification; fallback retained",
        "runs":results,"historical_pair_matches":242,"all_inventory_rows_match_held":1350,
        "implementation_sha256":hashlib.sha256((base/"extract_window.py").read_bytes()).hexdigest()}
with (scratch/"paired-product-check.json").open("x") as f: json.dump(report,f,indent=2); f.write("\n")
print(json.dumps(report,indent=2))

PY
```

## Acceptance boundary

No material selector/product mismatch remains within these checks. The repaired
failure path is exercised, and source/script/dependency/runtime identities are
preserved. The current fallback warning assessment is explicit rather than
silently granted by an old successful run.

Visible feature identity, camera/reference stability, censoring, annotation
uncertainty and independently frozen onset observations remain separate gates.
No original speed, detonation, support-removal event, acceleration/free fall,
whole-building motion or causal ranking is established by this note.


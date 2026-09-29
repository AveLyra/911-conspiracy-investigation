# Window-attribution input and locator review

Working research only. Independent, bounded input review for the fixed
15-image [window-attribution plan](WINDOW-ATTRIBUTION-PLAN.md); no historical
image viewing, pixel decompression, video decoding, transforms or network use.

**Result: PASS within byte/metadata and saved-record-join scope.** All 15 selected
PNG SHA-256 pins and all four manifest pins match. Their actual stored locators
join as described below. No input mismatch was found. This does not validate a
scene association, authenticate the source or its clock, reproduce the decoder,
or constitute scientific/human acceptance. Existing RGB rendering metadata
qualifies, but does not itself prevent, the restricted qualitative comparison.

Reviewed plan SHA-256:
`a509bdda7efc2fdc18fe25d2f758d822f637f964e96f369f5a39318cf77463e8`.
The governing main-repository AGENTS.md, WORKFLOW.md and START-HERE.md, the full
investigation charter and the full plan were read. Source-of-truth and
evidence-falsification safeguards preserve the boundary between current checks,
inherited extraction evidence and untested interpretation.

## Exact path bases and index namespaces

All relative paths in this note resolve below:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/`.

- **C:** `cbs-vms-content-check/run01/native/`.
- **P:** `late-fire-video-lineage/run01-PESKIN-COMPLETE/PESKIN-COMPLETE/native/`.
- **D:** `peskin-figure-correspondence/dense12/`.

C filename suffixes are one-based sample orders, not video indices.
P filename suffixes are one-based output orders; manifest `sample_index` is
zero-based and `source_frame_index` is separately recorded.
D filename suffixes are zero-based indices within the accepted
`[2518,2526)` second interval, not whole-source indices. Its saved probe
contains padding: filter to that interval before applying its local index.
The D whole-source indices below were independently joined by unique source PTS
against the existing full Peskin inventory, not inferred from nominal fps.

All listed PTS values have time base **1/1000 second** and describe encoded
source positions, not a recovered historical clock. C is source
`CBS-VMS-Wtc7.wmv`; P and D are source ID `PESKIN-COMPLETE`.

| Base/file | Output/sample or local index | Whole-source zero-based index | Source PTS | Stored raster | PNG bytes |
|---|---:|---:|---:|---|---:|
| C/frame-000001.png | order 1 | 0 | 33 | 320×240 | 145494 |
| C/frame-000005.png | order 5 | 240 | 16049 | 320×240 | 163160 |
| C/frame-000006.png | order 6 | 300 | 20053 | 320×240 | 150739 |
| C/frame-000016.png | order 16 | 900 | 60093 | 320×240 | 102137 |
| C/frame-000031.png | order 31 | 1799 | 120086 | 320×240 | 148238 |
| C/frame-000032.png | order 32 | 1859 | 124090 | 320×240 | 155078 |
| P/frame-000167.png | sample 166; order 167 | 74625 | 2490002 | 1620×1080 | 2177933 |
| P/frame-000168.png | sample 167; order 168 | 75075 | 2505016 | 1620×1080 | 2139753 |
| P/frame-000169.png | sample 168; order 169 | 75525 | 2520031 | 1620×1080 | 717016 |
| P/frame-000170.png | sample 169; order 170 | 75974 | 2535013 | 1620×1080 | 1756844 |
| P/frame-000171.png | sample 170; order 171 | 76424 | 2550028 | 1620×1080 | 1119320 |
| P/frame-000172.png | sample 171; order 172 | 76873 | 2565010 | 1620×1080 | 1759439 |
| P/frame-000173.png | sample 172; order 173 | 77323 | 2580025 | 1620×1080 | 1389064 |
| D/native-0093.png | local 93 | 75558 (PTS join) | 2521133 | 1620×1080 | 527145 |
| D/native-0185.png | local 185 | 75650 (PTS join) | 2524203 | 1620×1080 | 525179 |

Every PNG's current IHDR declares 8-bit RGB (color type 2), with compression,
filter-method and interlace fields zero. This is a binary-header check, not a
fresh decoded-pixel or visual check.

## Fresh encoded-byte pins

| Base/file | SHA-256 |
|---|---|
| C/frame-000001.png | 93ed3e5a9abc719f7703b641b00ba231a0a141c301b40154ef6a23ebd6c8e1c3 |
| C/frame-000005.png | 4df25dbbc05ae580e4449abdeb3776fc7215b2e65b74afd1fae602a516536221 |
| C/frame-000006.png | 9ba251b51cddc4dddf04f3897ef3d2a124a31bb3b7e7bd6e39642d26437eda9a |
| C/frame-000016.png | 707b36c1161c5e6d0213633f6e7d59948ac144213cc20fe93fd38ba32dd0c58c |
| C/frame-000031.png | f6df67a0befa4ec43d028b8b75e0b3663598de8856011942a829589436a0c52d |
| C/frame-000032.png | 0c2a91095140d9a4df5caf4a2d8e9312eae5819c4eac81a8e40098f9bc0741fc |
| P/frame-000167.png | 08dd5901909e80cf346b826c8528d2e59561964740a1eb5b4adbd814fe49cde1 |
| P/frame-000168.png | 1b13503ad20503b2132770ccb0ad20a3eca0a8ad62e1cba201473c23f62a4e49 |
| P/frame-000169.png | 66afdff8df53e5726b2844d8587c5f53ba3debfc1a8c31113626771477cfa02b |
| P/frame-000170.png | bf2071a61a6094f4902e5de7cea59ac500792b878f94db28d24f94d0421b0483 |
| P/frame-000171.png | fd8b59bebb3f95549e409d048e9fb7fe89e5660b71f719f7e4e78f8527c09eb5 |
| P/frame-000172.png | bea4d02fbf98d47ebbc0b406a60de89d2471e0bfbb4253ff7fb1eb9bed5527b2 |
| P/frame-000173.png | b105517de5f7a83222774ea58bf0094dff3bd9c161c9739c611339968e071f6a |
| D/native-0093.png | 3bb0cdc2b0cd5b9e85f94c1c7bf8674232edfd192cd7276ebfcfa00b9a686f3c |
| D/native-0185.png | 7d7af8f0ba19221420bbaf5dfa9f57812b8931c19c5cc1f235debcdab400297a |

| Manifest | Fresh SHA-256 |
|---|---|
| cbs-vms-content-check/run01/locators.json | 8776c554547e3d8e42a6950b78ac9cf9837f9a6722fe7c9ee05e3b59b3704c27 |
| cbs-vms-content-check/run01/frames.json | 0137dd6f05624c68f783dbc463d11ceddaae15957a9db96095c2578930a83324 |
| late-fire-video-lineage/run01-PESKIN-COMPLETE/PESKIN-COMPLETE/frames.json | eb6df31eb7c8ff14598de6dd9dc37c84d0becf753905f8cf7447853918bf96cd |
| peskin-figure-correspondence/dense12/frames.json | 5735831aeeeaa7be1e634f698a4f9771b22e64408e4d9eb4f3c5a282a77c28c4 |

## Pixel identity: recorded and joined, not freshly decoded

The following SHA-256 values are saved decoded RGB identities, read from
the pinned manifests. They were **not recomputed from pixels in this pass**.
For C, the manifest RGB MD5, expected 230400 RGB bytes and PTS also match the
corresponding row of the saved full-stream `diagnostics/decode01.stdout`.
For D, its receipt's exact native-image PNG pin joins to the local frame row,
filtered probe PTS and full-source inventory. P's manifest has no separate RGB
pixel hash; its encoded PNG pin and prior extraction evidence are its available
identity bridge. Do not invent an independent pixel hash for P.

| Base/file | Recorded decoded RGB SHA-256 |
|---|---|
| C/frame-000001.png | 38806eeb46ec66e5cda5f58a7ea3da87674e298f13f3277705e81f50ff1727ae |
| C/frame-000005.png | 190da5d35c5e3f644cd8272f216dd3c01052248fbc44ac51bb89f99c62f9b9bd |
| C/frame-000006.png | 857db3c3d7eefb67c4fb5c39488fb0846522612447f557fcb34f9d88dc521c0a |
| C/frame-000016.png | db5a1d5143564295d9a4797c28bbd324a01964d3281145067a7914388d0f92f7 |
| C/frame-000031.png | a8ce9c4c46b1d96d7d258f512666bba401d08ff18e420a0c2de67a7e2542e7e5 |
| C/frame-000032.png | 446d77c58bc877b211ff338935ba451afeb354b51c886564f99c169c876c2ae2 |
| D/native-0093.png | 71ad2756d78120bb00ccedd02ddf59f55f20b463ddbb7d5486e5ebf17e183175 |
| D/native-0185.png | c4054bd1fd419775c60fb9faabdc4db9272cb935994fb6e3e0b8842ad581b352 |

## Source and prior-admission bridge

**CBS.** The saved source identity is
`cbs-vms-content-check/sources/CBS-VMS-Wtc7.wmv`, 8717690 bytes,
SHA-256 `bae07b52bc85c735c72b227b55a327da3a49c6bf6a0798ccc9d85602dae185ad`.
Saved container/probe records identify video stream 1 (v:0), WMV1, 320×240,
time base 1/1000; the saved full inventory has 4531 rows. The run01 receipt
joins to the diagnostic receipt's unchanged before/after source identity.
Its status remains `descriptive_derivatives_only`,
`scientific_or_human_acceptance: false`, and 13 diagnostic lines.

The [existing CBS validation](validation.md) records both 77-image extraction
passes, prior complete decoded-pixel checks, the retained RGB conversion notices,
upstream source review and two clean native-YUV repeats. Those are inherited
checks, not rerun here. This review does not turn warned RGB runs into clean
runs or extend their admission to photometry. Unknown source SAR, colorimetry,
compression, chronology, gaps and sparse coverage remain.

**Peskin.** Both coarse and dense receipts record the same unchanged source:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-originals/peskin/sources/peskin-commons-resumed.webm`,
696711067 bytes, SHA-256
`0f438006c27e3059e7a5a480d4a7ee5382c5a136945c2a0120e583e3456f324d`.
This is the joined access copy `PESKIN-COMPLETE`, not an authenticated
camera original. Its recorded video stream is VP9 stream 0, 1620×1080,
SAR 8:9, display aspect 4:3, time base 1/1000.

The coarse receipt is completed and its selected records join to
`planned-frames.json` and the 88924-row full-source inventory. Its diagnostic
summary retains 13 reviewed software colorspace-fallback notices and zero
unreviewed warning/error entries; it is not an empty-diagnostic run. The accepted
dense12 receipt is completed and its 239 recorded PTS values equal the
interval-filtered probe list, first/last 2518029/2525971. The
[existing dense validation](../peskin-figure-correspondence/validation.md)
records same-code repro12, native-pixel and anchor checks. These are inherited;
this pass did not rerun the decoder, reproduction, controls, dense score search
or figure-correspondence analysis. Failed dense01 remains excluded.

Neither source video was freshly hashed in this input review. Their identities
above are verified **joins of saved receipts**, not new acquisition or source
authenticity findings.

| Receipt/support file | Fresh SHA-256 |
|---|---|
| cbs-vms-content-check/run01/receipt.json | b50a16a2bdeae7351fa0bcbd17fb9999f9e208ef087857a7ac0a4285ea08ba72 |
| cbs-vms-content-check/diagnostics/decode01.stdout | 7b1e98aaa8b2dc796f7aa5d0d734c5c3ca35e86f10d0c48ae2832c9d2da56c76 |
| late-fire-video-lineage/run01-PESKIN-COMPLETE/PESKIN-COMPLETE/receipt.json | bab83bc8c87a7d487555672801e18cb50abd6b2ba4acb97631d39b073ff47164 |
| late-fire-video-lineage/run01-PESKIN-COMPLETE/PESKIN-COMPLETE/frame-inventory.stdout | 59f7ac4f20357d631fac5af8eaa210f18c261749f342a452aaed72c870551cd8 |
| late-fire-video-lineage/run01-PESKIN-COMPLETE/PESKIN-COMPLETE/planned-frames.json | 64af33b868be56c51bebd74b2b0e0150b1d9bf8b4b0385b7fcd9f851d7548e75 |
| peskin-figure-correspondence/dense12/receipt.json | 9d149ffecb76137c9581017671eabf6b930bbdbd4da99e8a52c4c032186536ef |
| peskin-figure-correspondence/dense12/frame-probe.json | ec17328346428ba12e37cea321eef20edcc49114a50131a09b5f10ccae52b55a |

## Rendering metadata and narrow method qualification

A separate current binary PNG-chunk pass checked file pins, chunk CRCs and
selected rendering/animation chunks without decompressing IDAT:

| Set | pHYs raw (x, y, unit) | gAMA | cHRM |
|---|---|---|---|
| C, all six | (0, 1, 0) | absent | absent |
| P, all seven | (8, 9, 0) | 0.50994 | (0.3127, 0.329, 0.64, 0.33, 0.3, 0.6, 0.15, 0.06) |
| D, both | absent | absent | absent |

No selected file contains the checked acTL/fcTL animation-control, tRNS, iCCP or
sRGB chunks. This is not a comprehensive decoder-conformance audit or a claim
that every possible metadata type was absent. In particular, do not call these
15 images “metadata-free.” The C zero x-density value does not establish a
meaningful physical/display pixel aspect. The P pHYs values are retained as
recorded; no correction or resampling was applied.

The intended reader/viewer's treatment of aspect, gamma and chromaticity has
not been tested. Preserve the existing complete PNG bytes and metadata.
For this pass, positive association must rest on distinctive adjacency,
occlusion, foreground/background and window-band relationships robust to
rendering interpretation, with contradictory relationships checked. Exclude
color/brightness similarity, measured intensity, metric aspect ratios or angles
as decisive matching evidence. If a proposed relationship depends on uncertain
rendering, call it unresolved rather than importing Stage C's metadata-free
luminance-display rule or adding a transform. This qualification does not relax
the plan's requirement for at least two distinctive spatial relationships or
its fixed 15-image cap.

Root reported an earlier preflight that wrongly reused the Stage C
empty-render-metadata assertion, stopping on the first P image after C's six.
Root reported no images displayed in that attempt. That is a **root-reported
failed applicability assertion**, not a failure executed or independently
replayed by this reviewer. Its failure should be retained in the execution
record; it is not grounds to strip metadata or alter an already admitted input.

## Commands, actual results and limits

Both commands below ran from the absolute investigation base given above,
using `PYTHONDONTWRITEBYTECODE=1` and
`/Users/admin/.pyenv/versions/3.13.7/bin/python3`; each returned exit 0.

1. The first returned
   `PASS: bytes, headers, recorded locator/pixel-hash joins only; no image decode`,
   with 15 selected PNGs, four pinned manifests and the tables' locator results.
   It rehashed every file it read before returning, checking unchanged bytes.
2. The second returned
   `PASS: pinned bytes, chunk CRCs, nonanimated PNG structure; no IDAT decompression`,
   with the metadata table above. This phrase describes absent checked animation
   controls, not an independent decoded-frame validation.

A preliminary schema lookup, `jq '.[0]' peskin-figure-correspondence/dense12/frame-probe.json`,
returned exit 5 because that file is an object, not an array. Inspection of its
keys and `.frames` corrected the lookup; no substantive PTS mismatch was
waived. This is distinct from root's reported rendering-metadata assertion.

These are inline read-only checks, not a newly installed validation framework
or a negative-fixture-tested generic PNG verifier. The recipes make the actual
checks inspectable; they do not replace prior extraction controls. No source
file, manifest, image, frozen observation, code or canonical/legal record was
edited. The sole authorized new artifact is this note.

### Exact byte/locator command

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
from fractions import Fraction
import hashlib, json, re, struct
base = Path.cwd()
seen = {}
def blob(rel):
    p = base / rel
    b = p.read_bytes()
    seen[rel] = hashlib.sha256(b).hexdigest()
    return b
def jload(rel):
    return json.loads(blob(rel))
def check_pin(rel, pin):
    b = blob(rel)
    assert hashlib.sha256(b).hexdigest() == pin, ("pin", rel)
    return b
plan_path = "cbs-vms-content-check/WINDOW-ATTRIBUTION-PLAN.md"
plan = blob(plan_path).decode()
chosen = re.findall(r"^\| ([^|\n]+\.png) \| ([0-9a-f]{64}) \|$", plan, re.M)
assert len(chosen) == len(dict(chosen)) == 15
pins = {
"cbs-vms-content-check/run01/locators.json":"8776c554547e3d8e42a6950b78ac9cf9837f9a6722fe7c9ee05e3b59b3704c27",
"cbs-vms-content-check/run01/frames.json":"0137dd6f05624c68f783dbc463d11ceddaae15957a9db96095c2578930a83324",
"late-fire-video-lineage/run01-PESKIN-COMPLETE/PESKIN-COMPLETE/frames.json":"eb6df31eb7c8ff14598de6dd9dc37c84d0becf753905f8cf7447853918bf96cd",
"peskin-figure-correspondence/dense12/frames.json":"5735831aeeeaa7be1e634f698a4f9771b22e64408e4d9eb4f3c5a282a77c28c4"}
man = {p:json.loads(check_pin(p,h)) for p,h in pins.items()}
cdir = "cbs-vms-content-check/run01/"
pdir = "late-fire-video-lineage/run01-PESKIN-COMPLETE/PESKIN-COMPLETE/"
ddir = "peskin-figure-correspondence/dense12/"
cf, cl, pf, df = (man[cdir+"frames.json"], man[cdir+"locators.json"],
                   man[pdir+"frames.json"], man[ddir+"frames.json"])
cr, pr, dr = (jload(x+"receipt.json") for x in (cdir,pdir,ddir))
cdiag = jload("cbs-vms-content-check/diagnostics/receipt.json")
cprobe = jload("cbs-vms-content-check/diagnostics/probe.stdout")
ccontainer = jload("cbs-vms-content-check/diagnostics/container.stdout")
cstream, = [s for s in ccontainer["streams"] if s["codec_type"]=="video"]
assert cstream["index"] == 1 and cstream["time_base"] == "1/1000"
assert cr["status"] == "descriptive_derivatives_only"
assert cr["source_sha256"] == cdiag["source_before"]["sha256"] == cdiag["source_after"]["sha256"]
assert cr["source_sha256"] == "bae07b52bc85c735c72b227b55a327da3a49c6bf6a0798ccc9d85602dae185ad"
assert pr["status"] == dr["status"] == "completed"
assert pr["source_id"] == pr["source"]["id"] == "PESKIN-COMPLETE"
assert pr["source_before"] == pr["source_after"] == dr["source_before"] == dr["source_after"]
assert pr["source"]["sha256"] == dr["source_before"]["sha256"] == "0f438006c27e3059e7a5a480d4a7ee5382c5a136945c2a0120e583e3456f324d"
for r, prefix, field in [(pr,pdir,"products"), (dr,ddir,"outputs")]:
    for name in ["frames.json"]:
        b = blob(prefix+name)
        assert r[field][name] == {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
cmd5 = []
cb = blob("cbs-vms-content-check/diagnostics/decode01.stdout").decode()
assert "#tb 0: 1/1000" in cb and "#dimensions 0: 320x240" in cb
for line in cb.splitlines():
    if line and not line.startswith("#"):
        a = [x.strip() for x in line.split(",")]
        assert len(a)==6
        cmd5.append((int(a[2]),int(a[4]),a[5]))
assert len(cmd5)==len(cprobe["frames"])==4531
inventory_path = pdir+"frame-inventory.stdout"
ib = blob(inventory_path)
assert pr["products"]["frame-inventory.stdout"] == {"bytes":len(ib),"sha256":hashlib.sha256(ib).hexdigest()}
inventory=[]
for line in ib.decode().splitlines():
    fields=dict(x.split("=",1) for x in line.split("|") if "=" in x)
    inventory.append((int(fields["pts"]),int(fields["width"]),int(fields["height"])))
assert len(inventory)==88924
bypts={}
for i,row in enumerate(inventory):
    bypts.setdefault(row[0],[]).append(i)
pp = jload(pdir+"planned-frames.json")
ppb = blob(pdir+"planned-frames.json")
assert pr["products"]["planned-frames.json"] == {"bytes":len(ppb),"sha256":hashlib.sha256(ppb).hexdigest()}
db=blob(ddir+"frame-probe.json")
assert dr["outputs"]["frame-probe.json"] == {"bytes":len(db),"sha256":hashlib.sha256(db).hexdigest()}
dprobe=json.loads(db)["frames"]
filtered=[r for r in dprobe if dr["interval"][0]*1000 <= r["pts"] < dr["interval"][1]*1000]
assert [r["source_pts"] for r in df] == [r["pts"] for r in filtered]
rows=[]
for path,pin in chosen:
    b=check_pin(path,pin)
    assert b[:8]==b"\x89PNG\r\n\x1a\n" and b[12:16]==b"IHDR"
    w,h,depth,ctype,comp,fil,inter=struct.unpack(">IIBBBBB",b[16:29])
    assert depth==8 and ctype==2 and comp==fil==inter==0
    row={"path":path,"png_bytes":len(b),"png_sha256":pin,"IHDR":[w,h,depth,ctype]}
    if path.startswith(cdir):
        local=path[len(cdir):]
        f,=[x for x in cf if x["path"]==local]
        loc,=[x for x in cl if x["order"]==f["order"]]
        assert f["png_sha256"]==pin and f["source_index"]==loc["source_index"]
        i=loc["source_index"]; pts=loc["pts"]
        assert cprobe["frames"][i]["pts"]==pts
        assert (w,h)==(cprobe["frames"][i]["width"],cprobe["frames"][i]["height"])==(320,240)
        assert cmd5[i]==(pts,w*h*3,f["rgb_md5"])
        assert loc["time_base"]=="1/1000"
        row.update(source="CBS-VMS-Wtc7.wmv",output_order=f["order"],source_index=i,
                   pts=pts,timebase=loc["time_base"],pixel_sha256_recorded=f["rgb_sha256"],
                   pixel_md5_recorded=f["rgb_md5"])
    elif path.startswith(pdir):
        local=path[len(pdir):]
        f,=[x for x in pf if x["png"]==local]
        assert (f["sha256"],f["bytes"],f["width"],f["height"])==(pin,len(b),w,h)
        assert pr["products"][local]=={"bytes":len(b),"sha256":pin}
        p,=[x for x in pp if x["sample_index"]==f["sample_index"]]
        for key,value in p.items(): assert f[key]==value,(path,key)
        i=f["source_frame_index"]; pts=f["source_pts"]
        assert inventory[i]==(pts,w,h)
        assert Fraction(pts)*Fraction(f["source_time_base"])==Fraction(f["source_seconds_exact"])
        row.update(source="PESKIN-COMPLETE",sample_index=f["sample_index"],output_order=f["sample_index"]+1,
                   source_index=i,pts=pts,timebase=f["source_time_base"],
                   pixel_identity="No separate RGB-pixel hash in this manifest; pinned encoded PNG and inherited extraction checks.")
    else:
        assert path.startswith(ddir)
        local=path[len(ddir):]
        n,=[x for x in dr["native_images"] if x["path"]==local]
        assert (n["sha256"],n["bytes"])==(pin,len(b))
        assert dr["outputs"][local]=={"bytes":len(b),"sha256":pin}
        f,=[x for x in df if x["frame_index"]==n["frame_index"]]
        pts=f["source_pts"]; i,=bypts[pts]
        assert inventory[i]==(pts,w,h) and (w,h)==(1620,1080)
        assert filtered[f["frame_index"]]["pts"]==pts
        row.update(source="PESKIN-COMPLETE",dense_local_index=f["frame_index"],
                   source_index_via_full_inventory=i,pts=pts,timebase=f["source_time_base"],
                   pixel_sha256_recorded=f["decoded_rgb_sha256"])
    row["encoded_seconds_exact"]=str(Fraction(row["pts"])*Fraction(row["timebase"]))
    rows.append(row)
for rel,pin in seen.items():
    assert hashlib.sha256((base/rel).read_bytes()).hexdigest()==pin,("changed",rel)
print(json.dumps({"status":"PASS: bytes, headers, recorded locator/pixel-hash joins only; no image decode",
 "selected_pngs":len(rows),"plan_sha256":seen[plan_path],"manifest_pins":pins,
 "receipt_pins":{p:seen[p] for p in [cdir+"receipt.json",pdir+"receipt.json",ddir+"receipt.json"]},
 "support_pins":{p:seen[p] for p in ["cbs-vms-content-check/diagnostics/decode01.stdout",inventory_path,ddir+"frame-probe.json"]},
 "rows":rows},indent=2))
PY
```

### Exact metadata command

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
import hashlib, re, struct, zlib, json
plan = Path("cbs-vms-content-check/WINDOW-ATTRIBUTION-PLAN.md")
pairs=re.findall(r"^\| ([^|\n]+\.png) \| ([0-9a-f]{64}) \|$",plan.read_text(),re.M)
assert len(pairs)==15
rows=[]
for rel,pin in pairs:
    b=Path(rel).read_bytes()
    assert hashlib.sha256(b).hexdigest()==pin
    assert b[:8]==b"\x89PNG\r\n\x1a\n"
    pos=8; meta={}; names=[]
    while pos<len(b):
        n=struct.unpack(">I",b[pos:pos+4])[0]
        kind=b[pos+4:pos+8]; data=b[pos+8:pos+8+n]
        crc=struct.unpack(">I",b[pos+8+n:pos+12+n])[0]
        assert zlib.crc32(kind+data)&0xffffffff==crc
        names.append(kind.decode("ascii"))
        if kind==b"pHYs": meta["pHYs_raw"]=list(struct.unpack(">IIB",data))
        elif kind==b"gAMA": meta["gamma"]=struct.unpack(">I",data)[0]/100000
        elif kind==b"cHRM": meta["chromaticity"]=[v/100000 for v in struct.unpack(">8I",data)]
        elif kind==b"acTL": meta["animation"]=list(struct.unpack(">II",data))
        pos+=n+12
        if kind==b"IEND": break
    assert pos==len(b) and "acTL" not in names and "fcTL" not in names
    assert not ({"tRNS","iCCP","sRGB"} & set(names))
    rows.append({"path":rel,"metadata":meta})
print(json.dumps({"status":"PASS: pinned bytes, chunk CRCs, nonanimated PNG structure; no IDAT decompression","rows":rows},indent=2))

PY
```

## Remaining acceptance boundary

This pass clears only the pinned-input/locator prerequisite within its stated
scope. It does not provide an independent visual observation or common-source
finding. Building, face, historical time, exposure identity, common camera and
causal implications remain unresolved except where a separate visual/source
record specifically establishes a narrower proposition. Even a subsequent
strong scene association cannot count repeated material as independent fire
witnesses or erase the source-family dependence.


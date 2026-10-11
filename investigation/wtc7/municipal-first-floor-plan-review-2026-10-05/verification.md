# First-floor plan integrity and view-accounting verification

## Initial independent freeze

October 5, 2026. Identity/lineage check only, under the complete [PROTOCOL.md](PROTOCOL.md). Protocol SHA-256 `362a30b7a945c674f60cc90e165930b87f0da3b617373787671b2f060b4ee324`. This initial record was prepared before reading any new root or peer visual findings or the new synthesis.

Only this verification note was written. All sources, rasters, earlier observations and controls remained read-only. The source PDF was not parsed or viewed; images were not decoded or displayed. No rendering, OCR, extraction, decompression, crop, transform, network, model query, corpus census, main/legal edit, Git operation or historical interpretation occurred.

The source-preservation, evidence-audit and PDF-scope controls keep this an integrity check, not a new primary reading. Matching hashes establish identity relative to recorded bytes, not historical authenticity. The raster signatures/dimensions are header observations, not proof of delivered display resolution.

## Fixed-input result

Base P is:

`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/oil-route-packet`

All three full-file byte counts and SHA-256 values match the fixed protocol table and the exact pins in both existing lineage receipts. The PDF begins `%PDF-`; its eight-page count is an existing admission/receipt statement, **not freshly reparsed** here. Both PNG signatures equal `89504e470d0a1a0a`, first chunk type is IHDR with length 13, and the raw IHDR width/height fields match the table. No pixel decoding, PNG CRC/decompression or PDF object check was performed.

| Input relative to P | Bytes | Header dimensions | SHA-256 | Existing pin lines |
| --- | ---: | --- | --- | --- |
| `NYC-WTC_000166828.pdf` | 533928 | PDF magic only | `3812f9cf9399f044943bf718dcdc5cdad42dd0416a9cea7be10714168edca2e9` | `source-log.md:33`; `derivative-check.md:32` |
| `166828-4.png` | 214105 | 1797 x 2400 | `9e26270b70e21e0abd83c9785f049cadc4955c8dbc9d153fd1cf71d60479a78d` | `source-log.md:60`; `derivative-check.md:89` |
| `166828-large-4.png` | 1757977 | 3593 x 4800 | `4332f6cdec6bf169373a34d561bda80e1e87eecd53fa9e160a9a426772fe56da` | `source-log.md:75`; `derivative-check.md:136` |

## Earlier records unchanged

All four records below match the exact sizes/hashes previously frozen in the municipal model-crosswalk checker inventory, whose hash is `65bb6d2956d9b0a820bbb4cf6b489a7a40ad665c48787836b4b26754b3f3e039`. The old root/peer observation hashes also occur in the existing source log; their contents were not read in this check.

| Earlier file relative to P | Bytes | SHA-256 | Additional old pin reference |
| --- | ---: | --- | --- |
| `source-log.md` | 11526 | `c760ef2addddd182294da1e6e2b497d9249e8710d8ec9b24f62c0c67ee35ec2d` | prior frozen inventory only in this check |
| `derivative-check.md` | 11085 | `80b47ec12e9144d419c0f73fac3840dd92630014695ee2cd1c8c363274e5b0b1` | `source-log.md:164` |
| `root-observations.md` | 12910 | `877240e853e5bda774495a3f67a25e9ee6623e3b07ba8cbd84fb96cec464707e` | `source-log.md:85` |
| `review.md` | 23045 | `7ede5179ceb467159e91d4b0d5d48485942e93ae540287ddbca5bab973948d8f` | `source-log.md:114` |

The existing derivative receipt describes its prior all-page `-f 1 -l 8 -png -scale-to 2400` execution using this source and prefix `166828`, terminal `0fcc57` exit 0. It separately records the page-four repeat `-f 4 -l 4 -png -scale-to 4800`, terminal `76a097` exit 0 and full-byte equality with the root raster. The page-four source/render lineage is thus present in the unchanged receipt, and current bytes match its pins. **Those historical commands were read, not rerun or newly certified.** Adjacent other-page receipt text was not treated as new checks or new input coverage.

## Actual commands and results

Complete protocol read: `9047cd`, exit 0. `shasum -a 256` on current main AGENTS/WORKFLOW/START-HERE/CHARTER, protocol and earlier inventory, followed by the nonexistence check for this new output, ended 0 (`51f4af`). Current controls match the previously read pins:

- AGENTS: `934437bfc0ddbe522cc73461819593706d12c0644cb306d263d9f1fe3914a857`.
- WORKFLOW: `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a`.
- START-HERE: `b291da2b9ab3f1a8e9e69ff5a5d930c689ff2d45a6b2ce06a521e76295fbd560`.
- Complete main CHARTER: `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.

The stdout-only byte/header/reference check used the bundled Python interpreter:

`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`

Receipt `0dead1`, exit 0; 2026-10-05T04:33:42.040975+00:00 to 2026-10-05T04:33:42.048471+00:00; elapsed 0.007502 seconds. Three fixed inputs and four old records passed; no missing file, mismatch or failed assertion was reported. The old lineage-command sections were read with bounded `sed -n` ranges (`fdb98e` and `a85c65`, exit 0), without executing them. No failed check occurred in this initial unit check.

The exact byte/header check was executed as a quoted PY here-document with this body:

```python
from pathlib import Path
import hashlib,struct,re,json,time,datetime
B=Path("/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation")
P=B/"municipal-originals-2026-10-04/oil-route-packet"
U=B/"municipal-first-floor-plan-review-2026-10-05"
t=time.perf_counter(); start=datetime.datetime.now(datetime.timezone.utc).isoformat()
expected=[("NYC-WTC_000166828.pdf",533928,None,"3812f9cf9399f044943bf718dcdc5cdad42dd0416a9cea7be10714168edca2e9"),("166828-4.png",214105,[1797,2400],"9e26270b70e21e0abd83c9785f049cadc4955c8dbc9d153fd1cf71d60479a78d"),("166828-large-4.png",1757977,[3593,4800],"4332f6cdec6bf169373a34d561bda80e1e87eecd53fa9e160a9a426772fe56da")]
protocol=(U/"PROTOCOL.md").read_bytes(); assert hashlib.sha256(protocol).hexdigest()=="362a30b7a945c674f60cc90e165930b87f0da3b617373787671b2f060b4ee324"
prior=(B/"municipal-model-crosswalk-2026-10-05/inventory-check.md").read_bytes(); assert hashlib.sha256(prior).hexdigest()=="65bb6d2956d9b0a820bbb4cf6b489a7a40ad665c48787836b4b26754b3f3e039"
old={p:(int(n),h) for p,n,h in re.findall(r'^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|',prior.decode(),re.M)}
receipt_names=["source-log.md","derivative-check.md"]
receipts={name:(P/name).read_text() for name in receipt_names}
inputs=[]; failures=[]
for name,n,dimensions,pin in expected:
 data=(P/name).read_bytes(); actual=hashlib.sha256(data).hexdigest()
 if dimensions is None: header=data[:5].decode("ascii"); actual_dims=None; header_ok=data[:5]==b"%PDF-"
 else:
  header=data[:8].hex(); actual_dims=list(struct.unpack(">II",data[16:24])); header_ok=data[:8]==b"\x89PNG\r\n\x1a\n" and data[12:16]==b"IHDR" and struct.unpack(">I",data[8:12])[0]==13
 matches={rn:[i+1 for i,line in enumerate(text.splitlines()) if pin in line] for rn,text in receipts.items()}
 checks={"size":len(data)==n,"sha256":actual==pin,"header":header_ok,"dimensions":actual_dims==dimensions,"protocol_pin":pin in protocol.decode(),"prior_derivative_pin":bool(matches["derivative-check.md"])}
 if not all(checks.values()): failures.append(name)
 inputs.append({"name":name,"bytes":len(data),"sha256":actual,"header":header,"dimensions":actual_dims,"checks":checks,"receipt_pin_lines":matches})
old_inputs=[]
for name in ["source-log.md","derivative-check.md","root-observations.md","review.md"]:
 path=P/name; data=path.read_bytes(); actual=hashlib.sha256(data).hexdigest(); relative=str(path.relative_to(B)); n,pin=old[relative]
 refs={rn:[i+1 for i,line in enumerate(text.splitlines()) if actual in line] for rn,text in receipts.items() if rn!=name}
 match=(len(data),actual)==(n,pin)
 if not match: failures.append(name)
 old_inputs.append({"name":name,"bytes":len(data),"sha256":actual,"matches_prior_frozen_inventory":match,"existing_receipt_pin_lines":refs})
print(json.dumps({"start_utc":start,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"elapsed_seconds":time.perf_counter()-t,"inputs":inputs,"old_inputs":old_inputs,"protocol_sha256":hashlib.sha256(protocol).hexdigest(),"prior_inventory_sha256":hashlib.sha256(prior).hexdigest(),"failures":failures},indent=2))
raise SystemExit(bool(failures))
```

## Protocol-before-view and later accounting boundary

The coordinator supplied the frozen protocol pin before assigning this check; its full text states that it was saved before any new image view. The unchanged pin has been independently verified. **The claimed save-before-view order is not established by a filesystem mtime or by this hash check alone.** The actual protocol save/hash and subsequent image/save receipts will be compared in a later accounting appendix when supplied.

At this initial freeze, new reader view accounting is deliberately **pending**: no new root/peer observations have been opened, no view has been independently witnessed by this checker, and no claim of completed reader coverage, zero delays, native one-to-one display, allowed-repeat compliance or readability success is made. Later accounting must distinguish directly observed checker results from coordinator/reader-reported tool receipts.

The fixed budget is one complete 2400-raster view per reader and, only after a saved material-unreadability reason, at most one complete 4800 repeat. An original-detail request/forwarding is not proof of native display; actual metadata and resize notices control the reported display limitation. New observations must remain separate from the old records. Any later appendix must preserve this initial freeze and identify its original hash.

## Post-freeze appendix: reported view accounting

This appendix was added only after both readers' final freezes were reported. The initial 9,727-byte verification record remains a preserved prefix, SHA-256 `f46abd26b0936b9a4063d0ebf1349bcad642bbfe8f1513da6fc94284851eef09`. No new visual findings were displayed or interpreted by this checker. Reader records were handled only as bytes, with the supplied section headings used as prefix boundaries.

### Reported sequence, not an independent tool-history audit

The coordinator reports this sequence:

1. Protocol saved with `apply_patch`, then its hash `362a30…e324` recorded before any new unit image view; method preflight receipt `4d70cf` and clearance followed.
2. Root's initial full-page view used `view_image({path: P/166828-4.png, detail: "original"})`, then `image(result.image_url, "original")`. Root reported requested, returned and forwarded detail as original and no explicit resize notice. Root saved the initial note **and repeat reason** before its second call, reporting initial hash `98941cfe…329e`.
3. Root's single larger view used the complete `P/166828-large-4.png` with the same explicit detail request/forwarding. The tool reported a resize from 3593 x 4800 to 2751 x 3676. Root appended a separate final section and froze its final record.
4. Peer reports the same two whole-page raster choices and explicit original request/forwarding. Its initial note and repeat reason were saved and pinned before its repeat: reported receipt `a1c02f → 663338`, exit 0, initial hash `eb3c85ca…71f5`. First view had no explicit resize notice; repeat reported the same 3593 x 4800 to 2751 x 3676 resize. Peer reported final protocol/raster/whitespace check `c90382 → dff1cc`, exit 0, then its final freeze.
5. Root reports reading both frozen records afterward and no further views. Each reader reports exactly two views, zero other pages/views, and no rendering, extraction or OCR in this unit.

These are coordinator/reader-reported tool facts, **not independently observed tool chronology**. No durable tool-history export or independent timing evidence was inspected here; file mtimes were not used as a chronology substitute. The root protocol-before-view declaration and the reported initial-save-before-repeat order are consistent with the protocol and the recoverable records, but byte recoverability alone does not prove when they were saved. The material need for a repeat is attributed to each reader's saved reason, not substantively adjudicated by this checker.

| Reader | View | Saved raster | Actual reported display metadata |
| --- | ---: | --- | --- |
| Root | 1 | 1797 x 2400, `166828-4.png` | Original request/return/forwarding; no explicit resize notice |
| Root | 2 | 3593 x 4800, `166828-large-4.png` | Explicit resize to 2751 x 3676 despite original request/forwarding |
| Peer | 1 | 1797 x 2400, `166828-4.png` | Original request/forwarding; no explicit resize notice |
| Peer | 2 | 3593 x 4800, `166828-large-4.png` | Explicit resize to 2751 x 3676 despite original request/forwarding |

The reported budget is therefore four total views of **one physical page**, two per reader, using two existing rasters. No notice on the first views is not proof of native one-to-one display. Both larger displays were explicitly reduced; no restored source detail, successful legibility, independent historical corroboration or engineering acceptance follows.

### Independently checked record identities

| New reader file | Final bytes | Final SHA-256 | Recoverable initial bytes | Initial SHA-256 |
| --- | ---: | --- | ---: | --- |
| `root-observations.md` | 5970 | `c2363a7f453882268a28662f96bbf7a7f5a411497d19a55ca2d7dba63a6ab2e1` | 2864 | `98941cfe204731c3ed7f56eddccc1b7ef2499327e1de135b57bfc9078a58329e` |
| `review.md` | 9318 | `add6b6446f05a7adda6379956a435d57c19dc5ed1956e83975ea371f485f959c` | 4131 | `eb3c85cab1e1bd3659aa99f3f7883f99b4e96a542da25b8ea1799f9d44cd71f5` |

Root initial content ends before `## Single larger view and final reading`; peer initial content ends before `## Single permitted repeat and closed reading`. Each appended heading is preceded by **one additional separator LF beyond the original initial-file bytes**. In each case the exact original prefix hash is recovered by excluding only that added LF; no content, internal whitespace or original end-of-file newline is normalized.

**Retained failed boundary check:** `42c5e3`, exit 1, first hashed all 2,865 bytes before the root heading, including the added separator LF. That raw prefix hash was `6b6f316185218132926a0140c2b60c96372dbd8f289681f58b91c07cc4ba9b2d`, not the reported initial hash. The final root-note hash already matched. Explicit boundary correction `41fb31`, exit 0, excluded only that single added LF and recovered the exact 2,864-byte initial hash. The original failed attempt remains a failed check, not a pass or an altered source.

For the peer, the 4,132-byte raw pre-heading prefix likewise includes its separator LF and hashes to `bd7ce3ff2185f56e5aa26acefa2e2c8f37751471e1f708b996357be259b3548c`; the first 4,131 bytes exactly match the reported initial freeze. This distinction was recorded directly rather than silently trimming the note.

### Final bounded checks

Receipt `de051e`, exit 0, 2026-10-05T04:39:48.738005+00:00 to 2026-10-05T04:39:48.755150+00:00, elapsed 0.017156 seconds:

- Both reported final note hashes and both recoverable initial hashes match.
- The sole source PDF and both page-four PNG full-file sizes/hashes match the initial table; PDF magic and PNG signature/IHDR dimensions remain correct.
- All four earlier source/derivative/observation records remain unchanged.
- Protocol remains `362a30b7a945c674f60cc90e165930b87f0da3b617373787671b2f060b4ee324`.
- Initial verification remained exactly 9,727 bytes with its frozen hash immediately before this append.
- No unresolved identity/header/prefix mismatch remains. The reported viewing sequence is not promoted to independently audited chronology.

**Retained post-append guard failure:** `0e53ff`, exit 1, first confirmed the unchanged initial-prefix hash, then incorrectly required an additional LF before the appendix heading. Inspection `5efc2c`, exit 0, established that the preserved initial record already ends with two LFs: the appendix starts exactly at byte offset 9,727, with no extra separator byte. The source record was unchanged; the guard was corrected to require the heading at that exact offset. Final-newline and trailing-whitespace inspection found no formatting defect. The corrected closing guard result is reported separately; this failed guard is not relabelled a pass.

The actual stdout-only command used the same bundled Python interpreter with this quoted PY here-document body; it does not output note contents or image pixels:

```python
from pathlib import Path
import hashlib,struct,json,time,datetime
B=Path("/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation")
U=B/"municipal-first-floor-plan-review-2026-10-05"; P=B/"municipal-originals-2026-10-04/oil-route-packet"
t=time.perf_counter(); start=datetime.datetime.now(datetime.timezone.utc).isoformat()
readers=[("root-observations.md","## Single larger view and final reading","c2363a7f453882268a28662f96bbf7a7f5a411497d19a55ca2d7dba63a6ab2e1","98941cfe204731c3ed7f56eddccc1b7ef2499327e1de135b57bfc9078a58329e"),("review.md","## Single permitted repeat and closed reading","add6b6446f05a7adda6379956a435d57c19dc5ed1956e83975ea371f485f959c","eb3c85cab1e1bd3659aa99f3f7883f99b4e96a542da25b8ea1799f9d44cd71f5")]
results=[]; failures=[]
for name,heading,final_pin,initial_pin in readers:
 data=(U/name).read_bytes(); marker=heading.encode(); count=data.count(marker)
 if count!=1: failures.append(name+":heading_count"); continue
 raw=data.split(marker,1)[0]; candidate=raw[:-1] if raw.endswith(b"\n\n") else raw
 raw_pin=hashlib.sha256(raw).hexdigest(); candidate_pin=hashlib.sha256(candidate).hexdigest()
 original=raw if raw_pin==initial_pin else candidate
 result={"name":name,"final_bytes":len(data),"final_sha256":hashlib.sha256(data).hexdigest(),"final_match":hashlib.sha256(data).hexdigest()==final_pin,"raw_prefix_bytes":len(raw),"raw_prefix_sha256":raw_pin,"raw_prefix_match":raw_pin==initial_pin,"recoverable_initial_bytes":len(original),"excluded_separator_LF_bytes":len(raw)-len(original),"recoverable_initial_sha256":hashlib.sha256(original).hexdigest(),"initial_match":hashlib.sha256(original).hexdigest()==initial_pin}
 results.append(result)
 if not result["final_match"] or not result["initial_match"]: failures.append(name)
expected=json.loads("[{\"name\":\"NYC-WTC_000166828.pdf\",\"bytes\":533928,\"sha256\":\"3812f9cf9399f044943bf718dcdc5cdad42dd0416a9cea7be10714168edca2e9\",\"dimensions\":null},{\"name\":\"166828-4.png\",\"bytes\":214105,\"sha256\":\"9e26270b70e21e0abd83c9785f049cadc4955c8dbc9d153fd1cf71d60479a78d\",\"dimensions\":[1797,2400]},{\"name\":\"166828-large-4.png\",\"bytes\":1757977,\"sha256\":\"4332f6cdec6bf169373a34d561bda80e1e87eecd53fa9e160a9a426772fe56da\",\"dimensions\":[3593,4800]},{\"name\":\"source-log.md\",\"bytes\":11526,\"sha256\":\"c760ef2addddd182294da1e6e2b497d9249e8710d8ec9b24f62c0c67ee35ec2d\",\"dimensions\":null},{\"name\":\"derivative-check.md\",\"bytes\":11085,\"sha256\":\"80b47ec12e9144d419c0f73fac3840dd92630014695ee2cd1c8c363274e5b0b1\",\"dimensions\":null},{\"name\":\"root-observations.md\",\"bytes\":12910,\"sha256\":\"877240e853e5bda774495a3f67a25e9ee6623e3b07ba8cbd84fb96cec464707e\",\"dimensions\":null},{\"name\":\"review.md\",\"bytes\":23045,\"sha256\":\"7ede5179ceb467159e91d4b0d5d48485942e93ae540287ddbca5bab973948d8f\",\"dimensions\":null}]")
source_results=[]
for e in expected:
 data=(P/e["name"]).read_bytes(); actual=hashlib.sha256(data).hexdigest(); header_ok=True
 if e["name"].endswith(".png"): header_ok=data[:8]==b"\x89PNG\r\n\x1a\n" and data[12:16]==b"IHDR" and list(struct.unpack(">II",data[16:24]))==e["dimensions"]
 elif e["name"].endswith(".pdf"): header_ok=data[:5]==b"%PDF-"
 match=len(data)==e["bytes"] and actual==e["sha256"] and header_ok
 source_results.append({"name":e["name"],"bytes":len(data),"sha256":actual,"header_check":header_ok,"match":match})
 if not match: failures.append(e["name"])
protocol_pin=hashlib.sha256((U/"PROTOCOL.md").read_bytes()).hexdigest(); initial_verification=(U/"verification.md").read_bytes(); verification_pin=hashlib.sha256(initial_verification).hexdigest()
if protocol_pin!="362a30b7a945c674f60cc90e165930b87f0da3b617373787671b2f060b4ee324": failures.append("protocol")
if verification_pin!="f46abd26b0936b9a4063d0ebf1349bcad642bbfe8f1513da6fc94284851eef09": failures.append("initial_verification")
print(json.dumps({"start_utc":start,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"elapsed_seconds":time.perf_counter()-t,"readers":results,"source_and_old_records":source_results,"protocol_sha256":protocol_pin,"initial_verification_bytes":len(initial_verification),"initial_verification_sha256":verification_pin,"failures":failures},indent=2))
raise SystemExit(bool(failures))
```

This closes the bounded preservation/accounting check, not the substantive visual review. This check made no source/member reading, new model join, registration, authenticity, physical or causal finding.

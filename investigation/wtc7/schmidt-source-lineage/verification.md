# Independent representation verification

2026-09-24. Technical verification only. The verifier read this unit's
`PROTOCOL.md`, `LOCAL-REPRESENTATION-FOLLOWUP.md`, `extract_selected.py`, and
`representations/receipt.json`. It used pdfminer.six, not the producer's
pypdf parser, to recover the three fixed report image objects. It did not
import or call the producer for those independent checks. The producer was
called separately only for the declared existing-output refusal test.

**Result:** both exported JPEG codestreams match the independently parsed
PDF objects byte-for-byte. The exported PNG matches all decoded source RGB
samples, not merely its dimensions or a producer-supplied hash. All five
full-page PNGs have the expected dimensions and the current hashes below.
The fixed source and selected derivative hashes remained unchanged.

## Sources, runtime, and scope

Source: `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf`.
Size: **52,766,002 bytes**. SHA-256:
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
The report is encrypted; comparison uses decrypted terminal JPEG bytes or
decoded Flate samples, not pre-decipher ciphertext.

Runtime: bundled Python **3.12.14**, pdfminer.six **20251230**. The executable
used for both commands below was:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
The producer receipt records pypdf 6.10.0; the independent parser does not use
it. Pillow reads the JPEG headers and PNG pixels. This is separate parser
implementation, not independent historical evidence or professional review.

Input pins checked before and after:

| File | Bytes | SHA-256 |
|---|---:|---|
| extract_selected.py | 2,834 | `4b7cbd535b587ae95ed1ea1224be162dc8234cfa2c6be47426fafafa733935ce` |
| PROTOCOL.md | 3,492 | `0c5a522ae46c220c1aa6f793a477008a39ee93dcb79aa4c53ec754f91530b260` |
| LOCAL-REPRESENTATION-FOLLOWUP.md | 1,928 | `e920a5e5bfe850263c62d4609b79429e68797d6a064c527873a80967f689258c` |
| representations/receipt.json | 1,414 | `2b0394f21741058515bd306ac24e12d515f5ec893c15f69e411f847c97ee3c91` |

## Independent image-object results

| Physical page / object / resource | Export | Native dimensions | Bytes | Export SHA-256 |
|---|---|---|---:|---|
| 167 / 711 / Im0 | figure530.jpg | 378×504 | 35,519 | `f770fb0f992a72d69371407c12391ddf3b143fbe08549db8a6d51f6de8ab367f` |
| 168 / 714 / Im0 | figure531-decoded.png | 1024×768 | 225,296 | `bad30feeb23f3274ec39444d420b26e8f639bb68428b522fbbf66145715d6afb` |
| 168 / 715 / Im1 | figure532.jpg | 540×301 | 41,061 | `0f2f23f8ba82b06580db46d22f5fc1307b275de09c79a7b6eeb5b3764279b494` |

For objects 711 and 715, pdfminer's decrypted terminal DCT codestream bytes
exactly equal the exported JPEG bytes. Header format and native dimensions
also match. The JPEGs were not re-encoded by this verification.

Object 714 declares **FlateDecode, DeviceRGB, 8 bits per component**. It is
not indexed color, so there is no palette/color lookup table to validate.
There is no object-level `Decode`, `SMask`, `Mask`, or `DecodeParms` override.
The independently inflated **2,359,296 bytes** (`1024 × 768 × 3`) equal every
RGB sample decoded from the exported PNG in row-major order. Sample SHA-256:
`c678c1d03d6b02fc01fd47bc8fb2a6513436ff5ee5623790696e5f86ad0ae499`.
This establishes the particular PNG's sample equality to that source object,
not the scientific meaning, origin, or correctness of its displayed data.

For traceability, independent pre-decipher raw-stream hashes differ from
the post-decipher representations:

- 711: `17a38afe03b87180edd4e5dab59c5e166886f07ace97dd1deca6bdef4a2087a0`.
- 714: `d0449f175a113f515d938a7c4bdc06649e20f5c799264fa6bd8c55bd311ff90c`.
- 715: `f7c992156b2ae664225bafb0ae7f2cebec7cafd2f23a80f04ca0f29117880206`.

The parsed unclipped placement boxes (PDF points) are respectively
`[72.0,245.6399994,427.6799927,720.0]`,
`[111.4199982,428.9400024,500.5200043,720.0]`, and
`[103.1399994,118.5599976,508.9199982,345.0]`.
These are representation geometry, not historical measurements. No clipped
visibility or figure-content interpretation is asserted from those boxes.

## Full-page derivative checks

All physical pages 164–168 have zero source rotation, and their full media
boxes imply **935×1210 pixels at 110 dpi**. Each held PNG fully decodes as RGB
at that size. Current PNG byte hashes and decoded-pixel hashes are:

| Physical page | PNG bytes | PNG SHA-256 | RGB sample SHA-256 |
|---|---:|---|---|
| 164 | 263,332 | `b711133a5ef0547c5473f5b195eed30fa0cf52fa625cb83da24103bad4e909af` | `4419cd012a619b1b8dcd4eb0588aad927b42e0f11f2271890839a6f61b8aec09` |
| 165 | 152,979 | `73a9b5782fde915bfb49f189aa37d8433174b42db67e1ccfa9078b78a7d6e96c` | `a74211eec7b0c2080e4eb9cad8c940ef812f710a207aa657477bd9c910fe67aa` |
| 166 | 402,849 | `51f09945928166755d0b829030763161a702b2f549c69a8e226bd462bafdb39d` | `e58613ee55645a4ad93619ce02661dd67814e6aa5ae7f3942c50759492b68dc4` |
| 167 | 614,461 | `9df8b4f972312da74ead62afc9b71d2271b6db3287f23f482b670a893dac05da` | `e564aed3eab7f59b8adc6773e17cade605e92e1f9fdea51cfef7a10915dad197` |
| 168 | 381,127 | `c63d3209e5cf0a0e6a798be94b41d19a107acc4e5c7b0ced82b68379547c7f1a` | `8caf2a98d31940a9e4e653b2164407e53619a6f5fd28038ffab55ad8de37e5ff` |

This is **not an independent full-page rerender**. Dimensions and hashes do
not alone prove source-to-render visual fidelity. Root and the source reviewer
own full-page visual inspection; this verifier made no exposure-match,
glass-state, clock, or color-code interpretation. The producer's render
command and any original render diagnostics must remain separately recorded.

## Actual independent command

The following code was executed through the absolute bundled Python command
`python3 -B - <<'PY' ... PY`, exit 0. It printed the source/output pins and
the results above. No Python warning was recorded and no terminal diagnostic
was emitted. No verifier script or extra data file was written.

```python
from pathlib import Path
import hashlib,io,json,math,platform,subprocess,warnings
import pdfminer
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTImage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter,PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import literal_name
from PIL import Image
root=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/schmidt-source-lineage')
source=Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf')
def digest(raw):return hashlib.sha256(raw).hexdigest()
def pin(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())}
files=[source,root/'extract_selected.py',root/'PROTOCOL.md',root/'LOCAL-REPRESENTATION-FOLLOWUP.md',root/'representations/receipt.json']+sorted((root/'representations').glob('figure*'))+[root/f'physical-{i}.png' for i in range(164,169)]
before=[pin(p) for p in files]
assert before[0]['sha256']=='30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f'
receipt=json.loads((root/'representations/receipt.json').read_text())
assert receipt['script_sha256']==digest((root/'extract_selected.py').read_bytes())
expected={(167,711):('figure530.jpg',[378,504]),(168,714):('figure531-decoded.png',[1024,768]),(168,715):('figure532.jpg',[540,301])}
def images(obj):
 if isinstance(obj,LTImage):yield obj
 for child in getattr(obj,'_objs',[]):yield from images(child)
checks=[];pages=[]
with source.open('rb') as f,warnings.catch_warnings(record=True) as warning_records:
 warnings.simplefilter('always')
 doc=PDFDocument(PDFParser(f),password='')
 manager=PDFResourceManager();device=PDFPageAggregator(manager);interpreter=PDFPageInterpreter(manager,device)
 for number,page in enumerate(PDFPage.create_pages(doc),1):
  if number<164:continue
  if number>168:break
  box=page.mediabox;dims=[math.ceil((box[2]-box[0])*110/72),math.ceil((box[3]-box[1])*110/72)]
  assert page.rotate==0
  pp=root/f'physical-{number}.png'
  with Image.open(pp) as im:
   im.load();assert list(im.size)==dims and im.mode=='RGB'
   pages.append({'physical_page':number,'expected_110dpi_size':dims,'png':pin(pp),'rgb_pixel_sha256':digest(im.tobytes())})
  if number not in (167,168):continue
  interpreter.process_page(page)
  for image in images(device.get_result()):
   key=(number,image.stream.objid);assert key in expected
   name,size=expected[key];s=image.stream;attrs=s.attrs
   assert [attrs['Width'],attrs['Height']]==size and attrs['BitsPerComponent']==8
   actual=pin(root/'representations'/name)
   original=next(x for x in receipt['outputs'] if x['object_id']==s.objid)
   assert actual['sha256']==original['sha256'] and actual['bytes']==original['bytes']
   ciphertext=s.get_rawdata();decoded=s.get_data()
   row={'page':number,'resource':image.name,'object_id':s.objid,'dimensions':size,'bbox_unclipped_points':list(image.bbox),'export':actual,'filter':literal_name(attrs['Filter']),'colorspace':literal_name(attrs['ColorSpace']),'predecipher_raw_sha256':digest(ciphertext),'pdfminer_get_data_bytes':len(decoded),'pdfminer_get_data_sha256':digest(decoded)}
   if s.objid in (711,715):
    assert decoded==(root/'representations'/name).read_bytes()
    with Image.open(io.BytesIO(decoded)) as im:assert im.format=='JPEG' and list(im.size)==size
    row['terminal_jpeg_byte_equal']=True
   else:
    assert literal_name(attrs['Filter'])=='FlateDecode' and literal_name(attrs['ColorSpace'])=='DeviceRGB'
    assert all(k not in attrs for k in ('Decode','SMask','Mask','DecodeParms'))
    assert len(decoded)==size[0]*size[1]*3
    with Image.open(root/'representations'/name) as im:
     im.load();assert im.mode=='RGB' and list(im.size)==size and im.tobytes()==decoded
    row.update({'full_rgb_samples_equal':True,'indexed_color_table':'not applicable: DeviceRGB, not Indexed','decode_mask_predictor_override':'none in source object'})
   checks.append(row)
assert len(checks)==3 and {(x['page'],x['object_id']) for x in checks}==set(expected)
assert len(pages)==5
assert [pin(p) for p in files]==before
print(json.dumps({'status':'independent_representation_checks_pass','parser':'pdfminer.six','version':pdfminer.__version__,'python':platform.python_version(),'source':before[0],'source_encrypted':bool(doc.encryption),'checks':checks,'full_pages':pages,'input_pins':before[1:],'all_selected_inputs_unchanged':True,'warnings':[str(w.message) for w in warning_records]},indent=2))
```

## Existing-output refusal check

Source inspection establishes that `extract_selected.py` constructs all three
exports in memory, then calls `representations.mkdir(exist_ok=False)` before
any output-file open. A read-only-safe rerun against the existing directory
confirmed refusal at that call. Thus it refuses **before writes**, not before
input reads or in-memory extraction.

Executed command:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/schmidt-source-lineage/extract_selected.py
```

Working directory was this unit. The subprocess returned **1**, empty stdout,
and the expected `FileExistsError` referencing `representations`. Its 751-byte
stderr had SHA-256
`17146a7863f527bda9d163088fdab510e07f3089bb8e2dc69d34f74bdfd05085`.
The surrounding check returned 0 after confirming unchanged hashes for the
source, producer script, all four existing representation files, and all five
full-page PNGs, and unchanged representation-directory member names. It did
not suppress or treat this expected producer failure as an extraction success.

Actual wrapper:

```python
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/schmidt-source-lineage')
source=Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf')
files=[source,root/'extract_selected.py']+sorted((root/'representations').iterdir())+[root/f'physical-{i}.png' for i in range(164,169)]
def snapshot():return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
before=snapshot();names=sorted(p.name for p in (root/'representations').iterdir())
command=[sys.executable,'-B',str(root/'extract_selected.py')]
r=subprocess.run(command,cwd=root,capture_output=True)
assert r.returncode==1 and r.stdout==b''
assert b'FileExistsError' in r.stderr and b'representations' in r.stderr
assert snapshot()==before and sorted(p.name for p in (root/'representations').iterdir())==names
print(json.dumps({'command':command,'cwd':str(root),'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'expected_refusal':'FileExistsError at existing representations directory','selected_input_and_output_hashes_unchanged':True,'representation_member_names_unchanged':True,'scope':'collision path only; extraction was recomputed in memory before mkdir failed; no new output file'}))
```

The refusal test covers this existing-directory collision only. It is not
an exhaustive test of partial-write failures, symlink attacks, concurrent
mutation, permissions, or all image formats. The producer was not altered.

## Evidentiary ceiling

This verifies report-derived representation identity and one no-clobber
behavior. Hash equality does not authenticate a camera original, photographer,
clock, source worksheet, exposure match, historical glass condition, thermal
input, or collapse mechanism. No denied route, archive acquisition, media
download, main/raw-source edit, historical measurement, or accepted-engine
operation occurred. Only this verification note was written by this agent.

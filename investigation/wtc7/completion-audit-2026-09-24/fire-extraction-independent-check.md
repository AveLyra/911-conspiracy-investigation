# Independent fire-image extraction check

2026-09-24. Research only. **PASS for the bounded technical extraction check**;
no visual/caption, clock, fire-state, historical-authentication or model-input
agreement finding is made by this reviewer.

Read [FIRE-FIRST-ACTION.md](FIRE-FIRST-ACTION.md), the complete
[wrapper](extract_fire_first_action.py) and the complete reused main
`fire-annotation/prepare_assets.py`, including its verification mode. The
original verification mode was **not invoked**: it expects a different
association file and writes amended provenance. I independently parsed the
already-held report using pdfplumber/pdfminer, never imported or ran the
producer, and wrote only this note. No source acquisition, image display,
crop, recompression, new render, source edit, package installation or engine
acceptance occurred. The PDF skill was read and bundled runtime located;
an initial guessed skill path was missing, followed by the actual catalogued
skill path. This was read-only source-byte processing authorized by the
parent's bounded task, not another scientific image reading.

## Inputs and actual check

Runtime: bundled Python3.12.14, pdfplumber0.11.9, pdfminer.six20251230.
The main NCSTAR1-9 PDF is52,766,002 bytes,797 physical pages, SHA256
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
The before/after source identities match the producer and protocol pins.

The wrapper and underlying extractor hashes match their receipt; the
prospective protocol matches the exact copied `assets/PROTOCOL.md`. Selected
pages and processing order are exactly274,275,276,277. Thirty recorded
products plus the provenance key were freshly rehashed and size-checked:
**31/31 match**. This is not31 independent observations. Four full-page PNGs
have the recorded935×1210 dimensions and pass Pillow file verification; I did
not view their pixels or rerender them. The four saved rendering commands
report exit0, empty stderr and no extraction warnings.

Independent parser results:

| Physical page | Invoked native image | PDF object | Native dimensions | Decrypted encoded JPEG bytes | Ciphertext bytes |
|---|---|---:|---|---:|---:|
|274|None|—|—|—|—|
|275|A-79c9dd7424ec|2859|695×476|149499|149520|
|276|A-0ca71594109e|2862|328×311|58899|58928|
|277|A-e128b967bc22|2865|624×416|40644|40672|

Each page's image count agrees with the producer's invocation records. Object
IDs join uniquely; native dimensions agree with pdfminer, the producer PDF
dictionary and JPEG headers. Independent page-placement bounding boxes match
the producer with maximum difference **0.0 PDF points** for all three images.
All four page MediaBoxes are[0,0,612,792]. These are extraction/placement
checks, not proof of clip visibility or a caption-to-image association.

For each image, pdfminer's `stream.get_data()` bytes exactly equal both the
saved `streams/*.bin` and `images/*.jpg` bytes. The source PDF is encrypted
and opens with no supplied password; pdfminer's `rawdata` is the encrypted
payload, not the JPEG bytes exposed after decryption. Its length agrees with
the PDF stream dictionary. Ciphertext and decrypted encoded bytes are distinct
for all three objects. Consequently the producer's `raw_encoded_stream` field
must be read as **parser-exposed decrypted encoded JPEG**, not on-disk
ciphertext. No original-camera authenticity, original camera resolution or
unmodified historical image is established by byte preservation.

The image assignments remain empty in the technical provenance key. Root's
selection of Figures5-145/146 requires its separate complete-page/native
visual association; this reviewer neither certified nor guessed that join.
Page277's adjacent image also remains a technical object here, not a newly
classified exposure. Technical verification does not supply a second
independent scene annotation or retire the paired-reading obligation.

## A failed reviewer assertion, resolved without changing products

The initial check stopped at an overly strict JPEG end-marker assertion:
it required the last two bytes to be `FFD9`. All three preserved decrypted
streams instead end in `FFD9 0A` (JPEG end marker followed by a newline).
A diagnostic parser pass confirmed the exact lengths, hashes and final
byte form, and Pillow recognizes the streams as JPEGs. The corrected check
requires that exact trailing form and preserves every byte. The subsequent
full verification passes. This was an error in this reviewer's initial
sanity condition, **not a source, extraction or recompression defect**; the
failure is retained here rather than called a first-pass success.

## Reproduction core

The actual checks were run as in-memory Python through the bundled executable
with `-B -`; no new script or binary output was written. The essential parser
and byte comparison is reproduced below; the executed version additionally
asserted the wrapper/protocol identities, counts, image headers and saved
render return codes described above.

```python
from pathlib import Path
import hashlib, json, pdfplumber

A = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/completion-audit-2026-09-24')
H = A / 'fire-first-action'
R = H / 'assets/run01'
S = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf')
def identity(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
receipt = json.loads((R / 'extraction-receipt.json').read_bytes())
key = json.loads((R / 'provenance-key.json').read_bytes())
before = identity(S)
for rec in receipt['files_verified'] + [receipt['provenance_key']]:
    assert identity(H / rec['path']) == {x: rec[x] for x in ('bytes','sha256')}
with pdfplumber.open(S) as pdf:
    assert len(pdf.pages) == key['source']['physical_pages'] == 797
    assert pdf.doc.encryption is not None
    for pn in (274,275,276,277):
        expected = [(a,v) for a in key['assets'] for v in a['invocations']
                    if v['physical_page'] == pn]
        images = pdf.pages[pn-1].images
        assert len(images) == len(expected)
        for im in images:
            st = im['stream']
            matches = [(a,v) for a,v in expected
                       if a['object_reference']['object_id'] == st.objid]
            assert len(matches) == 1
            a,v = matches[0]
            cipher = bytes(st.rawdata)  # Save before get_data clears rawdata.
            assert len(cipher) == st.attrs['Length']
            encoded = st.get_data()
            assert encoded[:2] == b'\xff\xd8'
            assert encoded[-3:] == b'\xff\xd9\n'
            assert encoded == (H / a['raw_encoded_stream']['path']).read_bytes()
            assert encoded == (H / a['extracted_view']['path']).read_bytes()
            assert cipher != encoded
            assert list(im['srcsize']) == a['native_pdf_dimensions']
            bounds = [im[x] for x in ('x0','y0','x1','y1')]
            assert max(abs(x-y) for x,y in zip(bounds,v['page_bbox_unclipped_points'])) <= 1e-8
assert identity(S) == before
```

## Pins and limits

| Artifact | SHA256 |
|---|---|
|wrapper|ff83894cf7025f05247f5941ca24fc97f49aeff1e43c1b16f5a4575c0d8d9ad7|
|reused extractor|d9dbd73bc7483e5e1d136085c257bc5db3c808db53e4d95b40feade9c71e5af1|
|first-action protocol|7cbdd9cbdf67c2c8570dfbc249045c1ddb6b91f07394a481e74da932f93243c8|
|extraction receipt|1a7e987c2527574ac93185f06628cf284f4b324f486e0ce54c9c5b437bed74fc|
|provenance key|ad1180b2d233758c05a14f661071285d16fe3efeb1a1b02d626985438a8ba288|
|wrapper receipt|32f55f1f68d29bcdfee7ed49abbf06ae7f9250cd806bfe2707935eeb3ee35e29|
|object2859 encoded JPEG|904c3ccb0b6a011c69586bdc3205f148d20ab82c56f21c21fa7701c5e2e6ab68|
|object2862 encoded JPEG|6e53ada788d77760b78e6cd3294dd9bcfa7e7097cf24c6d1c55e02de118a391b|
|object2865 encoded JPEG|b59e534dcaf06a99d2a67ccb0f562d9f0e03b8ecc16d081fecd16e0ddac4c713|
|object2859 ciphertext|3698918fd410730217df0147889c8f75d3c3dfde13780b451bca943fc0222975|
|object2862 ciphertext|94c27ff4478e31f95fc136a9c5c7a8748f539c892259be205bb68c8e5b44b4f9|
|object2865 ciphertext|69dabfe07bf334b539c9b8f9139f15066cd8c8a97832650e7ecb1339f38c8d7e|

Ciphertext hashes were computed in memory; no new ciphertext file was saved.
The source is unchanged. Parser independence is between pypdf producer and
pdfminer/pdfplumber check, not independent historical provenance or independent
camera evidence. No live process remains from this check. Root must separately
evaluate complete-page/native visual associations, source-derived clocks,
visibility and observations; this pass supplies no fire classification or
causal-ranking change.

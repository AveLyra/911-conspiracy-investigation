# Rendering and representation preparation

2026-09-24. Technical derivatives only; no historical ordinates, series
identities, numerical curve comparison, or physical interpretation extracted.
The source readers separately perform complete-page visual and substantive
review. This note is not an acceptance of their interpretation or of the
published models.

## Render admission and actual execution

The fixed source is the held main `authority/nist/wtc7/ncstar-1-9a.pdf`, SHA-256
`cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`.
Exactly physical pages 73, 74, 75, 76, 77, and 117 were rendered at 200 dpi,
RGB PNG, complete media box with no cropping. All six are 1700 by 2200 pixels.
The printed-page mapping is physical minus 51 (22–26 and 66). The rendering
agent subsequently viewed all six complete PNGs at the tool's default
display size (resized to 1376 by 1780), confirmed those visible footers, and
found no evident clipping, missing page region, or illegible body text. This
is render QA, not a numerical curve reading. Root and the independent source
reader perform their own substantive inspection. The source contains 173 pages.

Actual commands, both exit 0, from this directory:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B render.py --self-test
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B render.py --out render01
```

Eight synthetic controls passed in 0.003 seconds: known SHA-256, source-hash
rejection, exact ordered page membership, existing-directory refusal,
file/dangling-symlink refusal, traversal refusal, exclusive-file writing, and
before/after input-change rejection. These are software guards, not tests of
the report's scientific accuracy. They do not exercise every runtime failure.

`render.py` SHA-256:
`a5083f34465587ff8ee877b5bd1d7dd5a7ced28ec491ab3ec9bbc1a5aed011ba`.
`render01/receipt.json` SHA-256:
`47d33d33b1695b00b21b72f9bda4a5c42d037ca1fb8a095c450aab9ba0eac1f5`.
The receipt preserves all six exact Poppler argv arrays, exit codes, stdout
and stderr files, source/code/protocol/runtime/config hashes before and after,
page boxes, PNG byte and decoded-RGB-pixel hashes, text hashes, and the 33
products preceding the receipt. The source and all pinned inputs stayed
unchanged. Six render stderr files and the parser stderr file were empty;
the Python warning list was empty. Poppler's `-v` stderr is separately retained
as version information, not misclassified as a rendering warning.

Python 3.12.14, pypdf 6.10.0, Pillow 12.3.0; exact platform and executable are
in the receipt. Dependency pins cover executables and package entry-point
files plus versions, not every shared library, package file, font, or font
cache. No claim of a fully hermetic runtime is made.

The existing main `nist-camera-method-audit/fonts.conf` names a cache in main.
It was read and pinned but not edited or used directly for rendering. The
renderer created `render01/fonts.conf`, changing only the parsed `cachedir`
value to `render01/font-cache` (XML serialization also changes), and passed
that exact local file through `FONTCONFIG_FILE`. Its two font directories
were retained. This avoided intentionally directing generated cache files
into main. No old derivatives, sources, or accepted engine state were edited.

## Page 76 representation inventory

A separate read-only pypdf content-stream inventory found one page content
stream and twelve image `Do` invocations; all are `/Image`, `/DCTDecode`,
8 bits/component. `/Im0`–`/Im5` are 741 by 88 pixels, `/Im6`–`/Im11` are 745 by
92 pixels. No invoked form XObjects were found. Content-stream SHA-256:
`60c4e0d1c34e7c4abe6c1b3916dbfc740c0ad3dc226dd7b55ceb7fd6605cdcc6`.

Operator counts:

```json
{"BT":10,"Do":12,"ET":10,"Q":14,"TJ":10,"Tc":15,"Td":7,
 "Tf":14,"Tj":8,"Tm":11,"Tw":13,"W":2,"cm":12,"f":3,
 "g":2,"gs":1,"n":2,"q":14,"re":5,"rg":2}
```

The only directly set gray/RGB/CMYK/dash/width operators among `RG`, `rg`,
`G`, `g`, `K`, `k`, `d`, and `w` were `g [0]` twice and `rg [1,1,1]` twice.
There were no `m`, `l`, `c`, `S`, or `s` operations. Five rectangles, three
fills, and two clipping operations are present; this is not an assertion of
zero vector page content. It supplies no candidate native vector curve paths.
The raster content has not been decoded into ordinates or assigned to series.

All referenced image object generations are 0:

| Resource | Object | Resource | Object |
|---|---:|---|---:|
| Im0 | 1770 | Im6 | 1778 |
| Im1 | 1771 | Im7 | 1779 |
| Im2 | 1774 | Im8 | 1780 |
| Im3 | 1775 | Im9 | 1781 |
| Im4 | 1776 | Im10 | 1772 |
| Im5 | 1777 | Im11 | 1773 |

The initial inventory's object-ID fields were null because dictionary indexing
dereferenced the objects. A second read-only check used `raw_get` to recover
the references above. This was a metadata-access correction, not a change in
the source or selection. Initial output was preserved in the task tool record;
neither run changed disk state.

Reproduce the representation counts and corrected reference lookup with the
same bundled Python executable (stdout only):

```python
from collections import Counter
import hashlib, json
from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import ContentStream

p = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf')
expected = 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4'
assert hashlib.sha256(p.read_bytes()).hexdigest() == expected
r = PdfReader(p)
if r.is_encrypted:
    r.decrypt('')
page = r.pages[75]
stream = ContentStream(page.get_contents(), r)
counts = Counter(op.decode('latin1') for operands, op in stream.operations)
styles = Counter((op.decode('latin1'), str(operands))
    for operands, op in stream.operations
    if op in (b'RG', b'rg', b'G', b'g', b'K', b'k', b'd', b'w'))
x = page['/Resources']['/XObject']
objects = []
for operands, op in stream.operations:
    if op != b'Do':
        continue
    name = operands[0]
    ref = x.raw_get(name)
    obj = ref.get_object()
    assert str(obj['/Subtype']) == '/Image'
    objects.append({'name': str(name), 'id': ref.idnum, 'generation': ref.generation,
        'width': obj['/Width'], 'height': obj['/Height'],
        'bits': obj['/BitsPerComponent'], 'filter': str(obj['/Filter'])})
print(json.dumps({'content_sha256': hashlib.sha256(stream.get_data()).hexdigest(),
    'counts': dict(sorted(counts.items())),
    'styles': [{'operator': a, 'operands': b, 'count': n}
        for (a, b), n in sorted(styles.items())], 'images': objects}, indent=2))
assert hashlib.sha256(p.read_bytes()).hexdigest() == expected
```

This condensed replay is equivalent for this observed image-only XObject
membership; unlike the initial inventory it fails if a form XObject is found,
rather than recursively inspecting that form. Neither method is a graph
digitizer. The exact code block above was run from this saved Markdown using
the bundled Python executable, exit 0; it reproduced the counts, styles,
content hash, twelve images, and corrected object numbers. The prospective
numerical gate remains controlling.

## Independent parser confirmation — 2026-09-24, after initial record

The earlier rendering and representation records remain unchanged. A second
parser, pdfminer.six 20251230, was used by `representation-check.py`, which
does not import pypdf or the rendering implementation. Its create-only output
was saved and hash-frozen before the separate pypdf byte/placement baseline
was created. The second implementation shares the source PDF, known page
selection, and earlier resource membership; it is independent parser
verification, not independent historical evidence or blind evidence review.

Actual commands (bundled Python path as above), each exit 0:

```sh
python3 -B representation-check.py --self-test
python3 -B representation-check.py --out representation-check01.json
python3 -B pypdf-representation-reference.py --self-test
python3 -B pypdf-representation-reference.py --out pypdf-representation01.json --comparison-out representation-comparison01.json
```

Here `python3` abbreviates the same absolute bundled executable used in the
render commands, not the shell's default interpreter. Three synthetic
pdfminer-side controls passed (affine bounding boxes, membership rejection,
known hash). Two separate pypdf-side controls passed (noncommutative matrix
composition order and rotated bounding box). These do not validate graph
reading or physical models. No control failed in these executions.

| Saved file | SHA-256 |
|---|---|
| representation-check.py | `4ae37253ccba29d90f727ba8b36a819acb7b077a36b19565246721b003b52bd3` |
| representation-check01.json | `517d657d206e6ac5b955be53bde63d5fecd9bc7b6fa05c971d6e88d7f111834b` |
| pypdf-representation-reference.py | `dfaf773f3778ae1d4fc9d670ee4cf6b183c8b1241cb081fb522cc210a1abf918` |
| pypdf-representation01.json | `1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5` |
| representation-comparison01.json | `f62742154ade9f98e85857f1557ad625ed82dc7f25c7c76522872ba732fcfcf1` |

Both implementations found exactly the same twelve named image invocations.
All object numbers, dimensions, bits/component, terminal encoded JPEG byte
counts and SHA-256 values match; every current transformation matrix and
unclipped bounding box matches with maximum absolute residual **0.0 points**
(declared comparison tolerance 1e-9 points). Operator counts also match. The
source and all input pins stayed unchanged; both runs recorded empty stderr
and zero warnings. The independent receipt stores each JPEG hash and each
transform rather than only an aggregate pass.

The PDF is encrypted. For all twelve images, pdfminer's pre-decipher raw
stream bytes differ from its decrypted terminal JPEG codestream bytes.
Comparison with pypdf uses the latter. Neither representation is a native
solver array, and no JPEG pixels were decoded or assembled by these checks;
Pillow read headers only to verify dimensions and JPEG format.

The independent path inventory identifies three painted rectangles: one
black thin header line and two white rectangles. It also records two
unpainted rectangular path endings and the two nonzero clipping requests.
The pdfminer interpreter expands each PDF `re` into a rectangular `m/l/h`
path internally; those expanded records do not contradict the earlier
absence of literal native `m/l/c/S/s` operators. No stroked vector curve paths
were found.

**Composition limitation:** native PDF glyph text includes the two panels'
solid-line/spring-element and dashed-line/shell-element model labels, in
addition to header, footer, and captions. The label text is not solely in
the JPEG strips. Bare image extraction therefore does not preserve all of
the published labeling. The complete page rendering remains the source for
series-identification context. The native text device-order string and all
painted path records are retained; no inference was made about any covered
raster pixels or the reason for this page composition.

The image boxes are deliberately labeled **unclipped**. pdfminer's layout
interpreter does not apply clipping; the custom recorder preserves clipping
requests separately. Neither the cross-parser zero residual nor the text
extraction proves clipped visibility. The prospective numerical method must
use the fully composed source view and explicitly address any consequential
mask/overprint, not silently promote the unclipped boxes into visible support.

These checks involved only PDF representation geometry. They extracted no
force/displacement/energy ordinate, curve identity, numerical model metric,
or causal conclusion, and performed no image assembly, resampling, solver
execution, or source acquisition.

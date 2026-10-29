# Reproduce the scoped AWA-570 comparison

Download the four unmodified public PDFs from the exact source URLs in SOURCES.json and check their SHA-256 values before comparing them. They were acquired at different documented times and retained separately. The recorded environment is Python 3.12.14, pypdf 6.10.0, Pillow 12.3.0 and pdftoppm 26.05.0.

For each PDF, render all pages into its own new directory, preserving existing outputs:

```sh
mkdir renders-7596136
pdftoppm -r 120 -png awa-570-naid7596136.pdf renders-7596136/page
```

Repeat with each other source and its distinct output directory. With 65 pages, the observed names are page-01.png through page-65.png. Compare image mode/dimensions and decoded pixels, not PNG-file bytes:

```python
from pathlib import Path
from hashlib import sha256
from PIL import Image
from pypdf import PdfReader

def pixel_signature(path):
    with Image.open(path) as image:
        image.load()
        return image.mode, image.size, sha256(image.tobytes()).hexdigest()

def text_signatures(pdf):
    reader = PdfReader(pdf)
    return [sha256((page.extract_text() or '').encode('utf-8')).hexdigest()
            for page in reader.pages]

reference = text_signatures('awa-570-naid7596136.pdf')
for candidate in ['7597139', '7597905', '7598444']:
    text = text_signatures('awa-570-naid' + candidate + '.pdf')
    assert len(reference) == len(text) == 65
    for page in range(1, 66):
        ref_image = Path('renders-7596136') / f'page-{page:02d}.png'
        other_image = Path('renders-' + candidate) / f'page-{page:02d}.png'
        print(candidate, page, reference[page-1] == text[page-1],
              pixel_signature(ref_image) == pixel_signature(other_image))
```

This is a portable description of the operators used by the executed local acquisition/comparison program. The local program rendered all 260 pages, compared all pagewise signatures and retained raw receipts/renders unchanged; this documentation's standalone example was not separately rerun as an additional independent experiment. PAGE-COMPARISON.json records that actual run. Success verifies only these representations under the stated settings. It does not certify hidden features, full PDF semantic equality, earlier versions, historical truth, metadata clock accuracy, native authorship, interview-exhibit identity or custody.

Info-dictionary values were read with `PdfReader(...).metadata`. XMP values were passively parsed from the root `/Metadata` stream, retaining the literal selected CreateDate/ModifyDate/MetadataDate/CreatorTool/Producer/DocumentID/InstanceID fields and the decoded stream SHA-256. No JavaScript, form actions or embedded executable content was run. Render stderr retained the Fontconfig default-configuration warning despite successful outputs; this is a runtime warning, not a historical source finding. No full-page OCR was newly performed.

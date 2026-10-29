# Reproduce the limited source checks

The recorded run used Python 3.12.14 and pypdf 6.10.0. Supply the two unchanged PDFs identified by URLs and SHA-256 in SOURCES.json, plus the held extraction identified there. The run command is:

```sh
python verify_sources.py --interview DOT-interviews.pdf --interview-text held-pypdf.txt --book AWA-570.pdf
```

The held extraction can be regenerated from the public 4,380-page PDF with the original method below. Use the recorded pypdf version when checking the whole-derivative hash; another version may produce different text order/spacing. The two original PDF hashes remain independent of extraction version. The output file is exclusive-create, preserving an existing copy:

```python
from pathlib import Path
from pypdf import PdfReader
reader = PdfReader('DOT-interviews.pdf')
with Path('held-pypdf.txt').open('x', encoding='utf-8') as stream:
    for page in reader.pages:
        stream.write((page.extract_text() or '') + '\f')
```

This unit did not repeat extraction of all 4,380 pages: it verified the preserved whole-derivative hash and re-extracted all 14 selected interview pages for comparison. The full-extraction method above is the earlier acquisition script's method. The recorded SOURCE-CHECKS.json is the actual limited run, not a claim that this documentation's whole-file regeneration was independently rerun.

Manually inspect interview physical pages 3951–3964 and AWA-570 pages 1, 2, 4, 7, 27 and 33. Twenty images were read in this unit at 120 dpi. Visual confirmation is separate from the script's 28 source/extraction/anchor checks. The report cover demonstrates why: its image contains the title/date/source while its extracted text has only two Unicode characters. Script success does not establish completeness, native authenticity, accurate historical statements, disposal execution, motive, legal compliance or calibrated radar clocks.

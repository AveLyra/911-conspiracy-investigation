# Method, dependence and limits

Public-source acquisition and inspection on 2026-10-27. Earlier findings, original files and working registers remain unchanged. This directory is an additive research supplement, not a case filing or scientific replication.

1. Downloaded the official court item HTML and its linked 28,304,524-byte ZIP via HTTPS. Tested ZIP CRCs and preserved originals. Extracted only `AA77.swf`; never executed the bundled Windows/Mac launchers or ActionScript.
2. Parsed SWF header, tag boundaries, recursive sprites, DefineFont2 character tables and DefineText/DefineText2 glyph indices with `extract_swf_text.py`. The header length and every visited tag/text/font boundary are checked. All 548 text definitions and 14 fonts decoded without an out-of-range glyph. Public `SWF-SOURCE-PINS.json` retains 25 relevant definitions and exact offsets/glyph indices. This is static source-content examination, not a Flash display-list renderer, a trial playback audit or a validation of carrier data. Formatting line breaks are not fully reconstructed; trailing spaces and joined words are preserved as decoded.
3. Acquired the 73-page Flight Call Notes and 302s PDF from a public mirror. Extracted text with pypdf and visually inspected physical pages 47–51. Recorded form/production locators; no full substantive reading of all 73 pages claimed. The mirror is not authenticated against an acquired official FBI bundle. The prior official bundle 403 is retained in the earlier first-pass record; it was not repeated here.
4. Acquired the publicly accessible two-page May 20 briefing embed and its two referenced scan JPEGs. Read both images and checked text-layer values. These are mirror page entities, **not the original PDF, a native MFR, or proof of its archival chain**. A hash fixes the acquired bytes only. Historic sensitivity markings are visible on the public scan; no identity behind redactions was reconstructed.
5. Rehashed the held official Commission notes PDF; extracted and visually inspected PDF page 7, printed 455, note 57. Converted the four printed minutes/seconds to seconds without changing source values. `CALL-COMPARISON.json` retains all three descriptions. Source agreement may reflect shared derivation, not independent corroboration.
6. Acquired only three accessible preview pages each from the Request 14 response and Key 302s embeds. No paywall or login restriction was bypassed. The Request 14 preview supplies the 50-page enclosure and later Bates-version lead; the Key 302s preview does not contain the September 20 report. Search results displaying later text are pointers, not complete acquired records. Their full contents remain open.

One retrieved GWU `doc02.pdf` was initially saved under a telephone-oriented local filename. Inspection of its seven pages and the publisher index identified it as the **NTSB AA77 flight-path study**, not a telephone response. Its bytes and misleading initial label remain preserved locally; it is excluded from the telephone evidence. A filename is not document identity. The attempted alternate complete-response mirror failed DNS resolution. Neither event establishes a historical discrepancy.

PDF images: Poppler `pdftoppm -f 47 -l 51 -r 100 -png` for interview pages; PyMuPDF 1.27.2.2 at 1.5 scale for note 57. Python 3.13.7 and pypdf 6.10.0. Visual verification and text checks are separate. A Java runtime was unavailable, so no independent Java Flash exporter was run; no such check is claimed.

Reproduce static extraction with Python's standard library:

```sh
python3 extract_swf_text.py /absolute/path/to/AA77.swf /absolute/path/to/new-output.json
python3 verify.py
python3 verify.py --zip /absolute/path/to/flights.zip --notes /absolute/path/to/911Report_Notes.pdf --interviews /absolute/path/to/Team7-Box13-Flight-Call-Notes-and-302s.pdf
```

The optional source verification requires pypdf. These commands verify acquired versions, exact source pins and arithmetic; they cannot establish caller identity, actual duration, completeness, intent or historical cause. They do not download records or transmit data.

Publication contains original research notes, source URLs/hashes, masked court labels and reproducible code. Original downloads, full raw interview/OCR text, source HTML scripts, unmasked contact/card data, scan images and unrelated records remain local. No private case correspondence, litigation strategy or credentials are part of this payload.

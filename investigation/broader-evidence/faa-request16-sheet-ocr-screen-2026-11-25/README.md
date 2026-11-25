# FAA Request 16: bounded OCR screen for the notification sheet

2026-11-25 · B129 / PD01–PD04. The [preceding comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/1fe97cc9db870c4ef4731fac76bcc97e3a23b3aa/investigation/broader-evidence/faa-request16-notification-sheet-candidate-2026-11-25/README.md) found that the July 2003 Request 16 response refers to a “Notifications to Military” sheet, while a separately released sheet carries that title and a 09/20/01 date. Their identity and any transmission remain unverified.

## Test and result

The 22-page [AWA-1077 release, NARA 34913881](https://catalog.archives.gov/id/34913881), was rendered at 1.5× grayscale and independently OCRed page by page with Tesseract 5.5.2, default language and page segmentation mode 3, using PyMuPDF 1.27.2.2. The checked PDF SHA-256 is `ccbb8e3b92af9efcdd09b427375ea25659134a9b8bc027b45c3bf7d138e2259c`.

The case-insensitive whitespace-tolerant title pattern matched **only physical p. 11**, the previously visually checked response. A numeric `09/20/01`-style date pattern matched **no pages**; all 22 pages returned nonempty OCR output. [Reproduction script](verify_ocr.py) reports only page numbers and counts, not raw page text. It verifies the input hash and expected result. OCR quality, fonts, scans and date formatting can cause misses; the date search does not cover every possible date expression.

This test does **not** establish that the named sheet is absent, that the original production lacked it, or that it was not transmitted. It does not identify the sheet referenced in the 2003 response with either 2001-dated copy. It screened only AWA-1077; it did not examine every possible attachment or other collection. The earlier AWA-329 and fax-sheet observations and all conflicting source descriptions remain unchanged.

## Next records

Obtain the actual item-16 enclosure and packing or receipt records and compare its full content to the separately held 2001-dated sheet. Continue separately to seek the corrected May 2003 answer and receipt and the signed administrative and recommendation dispositions. Do not treat this test as a correction, a completed custody join or evidence of intent.

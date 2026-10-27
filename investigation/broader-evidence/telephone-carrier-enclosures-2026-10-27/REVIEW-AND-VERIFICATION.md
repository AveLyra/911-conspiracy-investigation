# Review and actual verification

Verified October 27, 2026, before publication.

`PYTHONDONTWRITEBYTECODE=1 python3 verify_fields.py --court-zip /path/to/court-flights.zip --captures /path/to/held/captures`

Exit 0: all 28 held JPEG hashes and byte sizes matched; 23 manually read portrait Bates/fax labels produced the documented gaps; three selected intervals matched the printed Duration values; five pinned court text definitions matched the hash-pinned ZIP/SWF. The source-field inputs are manual transcriptions, not independent native decoding. The conditional +2-hour comparison is not a measured clock correction. Prior court-decoder work is reused as a comparison control, not recounted as a new finding.

Two additional tests used separate synthetic copies: a changed printed Duration and a changed source-entity hash. Both exited 1 for the expected discriminating reason. CONTROL-RESULT.json records those actual outcomes. Original source images were not altered. The original source report and the preceding local draft remain preserved.

Adversarial review: no claim that adjacent event blocks establish the same physical call, that every zero means no conversation, that every zero is a routing phase, or that all source timelines are calibrated. No authenticated operator/office join or caller assignment was made. No claim that 23 matching page-count differences authenticate the missing contents or establish government removal. Primary carrier field definitions and complete release originals were not acquired. The source pages can be incomplete or misassembled without implying motive. Agreement with a derivative exhibit can reflect common ancestry rather than independent corroboration.

Privacy review: manually selected factual fields, public source URLs/metadata and original code/notes only. No images, full OCR, QA views, network IDs, phone/card/account identifiers, private case correspondence or strategy are in this candidate. Hashes and Bates/page identifiers identify the source entities; they do not prove provenance beyond the documented public image reproduction.

Publication is a separate acceptance step. The final local receipt must verify the exact account, author and committer, remote branch/main commit, and every remotely published file byte. A successful test run does not complete the broader five-track investigation.

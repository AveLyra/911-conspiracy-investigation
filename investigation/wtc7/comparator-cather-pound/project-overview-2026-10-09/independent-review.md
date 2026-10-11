# Independent access-disposition review

October 9, 2026. No material correction required within this bounded review.
The evidence/source-of-truth controls preserve the distinction between failed
access and evidence about historical preparation.

I read PROTOCOL.md completely, then all of report.md, execution.md and
access-result.json (`cat`, receipt d4ebdf). The protocol matches its prospective
SHA256 `10ba5204368c38bdd0beb0b1f92310fc6129e19facedff5afe3f426f6ab054b7`.

From this directory, the actual preservation command was:

```sh
shasum -a 256 PROTOCOL.md ../preparation/source/article.html ../preparation/report.md ../report.md ../../synthesis-packet/material-claim-index.json
```

Receipt e81a85, exit0: all three old source/report hashes match execution.md;
the frozen index remains
`e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8`, matching
the prior integration report. An auxiliary `rg` returned exit2 because a
guessed validation.md path does not exist; the report supplied the expected pin.

`jq -e` checked the saved JSON's null HTTP statuses, exit6, zero bytes/redirects,
false content-review flags and absent-body declaration: true, exit0 (a40360).
Independent bounded `find`/`stat` inspection, both before and after these files
landed (c2700b; 4b2363), found only response-headers.txt, zero bytes. Header
contents were not read.

The network details are root's labeled transcription, not a request I performed
or independently witnessed. This review verifies local consistency and
preservation, not the historical webpage. Reported DNS failure is not a received
HTTP denial/404. No content assessment occurred; completed preparation, residual
capacity and footprint remain unresolved. Neither page disappearance nor
concealment follows. No retry, new source, acquisition rerun or physical test
was performed. Only this review file was added.

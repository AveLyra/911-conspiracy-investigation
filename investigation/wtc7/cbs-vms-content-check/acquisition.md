# Acquisition receipt and transport limitations

September20,2026 UTC / September19 local. Public-source research, no upload.

The prior NIST-linked Other-category route is rechecked in
[independent review](independent-acquisition-review.md). Refreshed metadata
and exact raw-fetch request are in sources/. The response preserves the
connector's file identifier and reported8,717,690bytes, with its temporary
bearer URL redacted. The requested provider MD5 was not present in normalized
metadata; do not claim a remote checksum match.

The raw fetch used download_raw_file=true and include_base64=false, not a
native-document export. The returned top-level file_uri download reference
was used exactly, through standard input with terminal echo disabled, to:

```sh
curl --config - --fail --location --max-redirs 3 --proto '=https' --proto-redir '=https' --max-time 55 --max-filesize 10000000 --no-clobber --silent --show-error --output sources/CBS-VMS-Wtc7.wmv --write-out 'http=%{http_code} bytes=%{size_download}\n'
```

Session54507 completed exit0, HTTP200,8,717,690bytes. No download retry or
overwrite. The acquisition completed before the00:51:43UTC clock read in the
tool history; no independent server timestamp or saved response-header clock
was captured. Local materialization and subsequent unchanged before/after
identity are verified, not authenticated camera custody.

Local source: sources/CBS-VMS-Wtc7.wmv,8,717,690bytes, SHA256
`bae07b52bc85c735c72b227b55a327da3a49c6bf6a0798ccc9d85602dae185ad`.
It is a regular non-symlink file. The raw-filename capitalization is retained.
Catalog timestamps and encoded metadata are not recording dates.

## Credential-handling deviation

The initial raw connector result was mistakenly echoed in tool output before
redaction, exposing a temporary signed retrieval URL for this public video.
It was not copied into repository files or subsequent notes/commands; later
materialization used standard input, not a command-line credential. Do not
claim zero tool-log exposure or that saved-file redaction erased that output.
No case-private document, account password or confidential case payload was
sent. This is a failed logging safeguard, not evidence of source alteration.
The existing redact-before-display software feedback already covers it.

## Diagnostic source acquisition

Both browser attempts at the exact FFmpeg n7.1.1 raw/file-view source returned
cache errors. A subsequently declared direct HTTPS retrieval of
https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1.1/libswscale/yuv2rgb.c
completed exit0/HTTP200,46,246bytes. Preserved as
sources/ffmpeg-n7.1.1-yuv2rgb.c, SHA256
`f0a61e340defcbb193f51d9f8c7faed727cc89987d2786551f6a966458f8f29b`.
Its narrow warning/fallback meaning is documented in FRAME-PLAN.md. It is not
an independent video decoder or a build attestation for the installed binary.

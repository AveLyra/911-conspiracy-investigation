# Direct retrieval after web reader failure

2026-10-04. Prospective, separate route declaration; original
[PROTOCOL.md](PROTOCOL.md) remains unchanged at SHA256
`ba9f1aa7b2b785ec101e7f273dc064a7252fbdd4c4670526ec7df03ae075d82c`.
Its two web opens completed by13:29:10UTC with only tool-specific errors:
`turn742view0` and `turn742view1` said each exact URL was not accessible via
that tool. No HTTP status, actual server refusal, authentication challenge,
document metadata or contents were returned. No byte GET was run under that
protocol's accessible-PDF condition. Preserve this failed route as failed.

The charter calls for safe alternatives to capability gaps. A direct public
GET can distinguish inability of the reader from an actual server response;
it is not a retry of a demonstrated denial. This change is declared before
any direct request and is not retroactive compliance with the first route.

Root may make exactly one HTTPS GET to each of the two literal official URLs
listed in PROTOCOL.md, with no query changes, alternate hosts, credentials,
automatic retries or redirect following. Timeout40seconds, connect timeout10,
maximum10MiB per file. Save response bodies in a new private temporary directory;
record command/runtime, UTC window, status, effective URL, content type, byte
count and SHA256. Do not print response cookies, tokens or private data.

Only a200 PDF response with matching basic metadata/identity may be admitted
for local original preservation and the original declared full-document review
(at most20pages). A non-PDF body, redirect, access challenge/refusal or other
failure stops that target without alternate navigation. Preserve returned
bytes as a response, not a PDF or an authenticated record. Do not infer that
other target documents are available from a server response to one.

The original independent-review, sensitivity and scientific limits continue.
No extra searches, bulk groups, mirror download, outreach, fee or sensitive
transfer. A successful byte fetch must precede any claim of a held original;
parsing/rendering success does not authenticate historical content.

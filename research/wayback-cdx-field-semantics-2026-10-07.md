# Wayback CDX locator-field semantics: source-pinned boundary (2026-10-07)

**Record type:** original research note; source-document observation and
inference limit. This is an additive redundant copy of the Faraday worktree
note, not a replacement. It preserves the upstream documentation and earlier
live-query result as separate observations. It does not reconcile CDX fields,
replay responses, or WARC contents.

**Faraday original:**
`/Users/admin/docs/911-worktrees/faraday-wtc7-model-compare/review/wayback-cdx-field-semantics-2026-10-07.md`
**SHA-256 of Faraday original:**
`ab06d9679cbb55bcef5c83dcfd45a3a686749fe8223bdf5edbaf5b5869b4f289`

## Primary documents captured

1. Internet Archive `wayback` CDX Server README, at commit
   `7f6ee86b35790c3cb10ea1115a0eeb9c7a432e09`:
   <https://github.com/internetarchive/wayback/blob/7f6ee86b35790c3cb10ea1115a0eeb9c7a432e09/wayback-cdx-server/README.md>
   Raw bytes:
   <https://raw.githubusercontent.com/internetarchive/wayback/7f6ee86b35790c3cb10ea1115a0eeb9c7a432e09/wayback-cdx-server/README.md>
   Accessed 2026-10-07. SHA-256 of downloaded raw README:
   `e17a0e1f43c4dd887adbb1473a7be452bbc12f823b64ea3fda2105c8d27ee7dd`.

2. Internet Archive `CDX-Writer` README, at commit
   `ab0bbb2a2cdc97149abc8c015c32660f463bea33`:
   <https://github.com/internetarchive/CDX-Writer/blob/ab0bbb2a2cdc97149abc8c015c32660f463bea33/README.md>
   Raw bytes:
   <https://raw.githubusercontent.com/internetarchive/CDX-Writer/ab0bbb2a2cdc97149abc8c015c32660f463bea33/README.md>
   Accessed 2026-10-07. SHA-256 of downloaded raw README:
   `4e3f2f328ddf07e0eb02fbdef5c6fdc726aaef09edb39e29245b7bb6b68b9443`.

The commit identifiers make these source snapshots addressable independently
of later branch changes. They identify the downloaded documentation bytes;
they do not authenticate Wayback's runtime configuration or any archived
record.

## Source observations

- In the pinned CDX Server README, the list of fields described as publicly
  available is `urlkey`, `timestamp`, `original`, `mimetype`, `statuscode`,
  `digest`, and `length` (README lines 81–83).
- The same README separately says access controls may restrict fields, giving
  `filename` as an example; when restricted, results contain only public
  fields (lines 349–359). It also uses `offset=` to mean a request parameter
  that skips earlier result rows (lines 222–224). That is a parameter, not
  documentation that a response field named `offset` is available.
- In the pinned CDX-Writer README, the writer's format tokens include `V`
  (“compressed arc file offset”) and `g` (“file name”); the asterisk on `V`
  is footnoted “in alexa-made dat file” (lines 12–16, 35–45). This is a
  document about that writer's supported output formats, not a specification
  of the currently deployed Wayback CDX endpoint.

## Preserve the prior live-query observation separately

The 2026-10-06 Faraday query note records that a request asking the live
endpoint for
`timestamp,original,statuscode,digest,length,filename,offset` returned six
rows with `filename:null` and `offset:null`. The query response's SHA-256 is
recorded there as
`f603430497d07b1b473afa40935785a308d42a27e1c0485c8092b4055105b6cd`.

These are distinct observations: the live response's null values, the CDX
Server README's stated public-field list and access-control description, and
the CDX-Writer README's different field-token notation. The documents do not
show which implementation or configuration produced the particular live
response, whether those requested names were accepted as response fields, or
why their values were null. The two uses of the word “offset” must not be
treated as equivalent: one is documented as a request parameter; the other
appears as a writer-format token with a footnote.

## Inference ceiling and next discriminating check

The documentation makes field-availability/configuration a concrete
technical possibility to check; it does **not** establish that this caused
the live query's nulls. In particular, it does not show that the WARC records
are missing, inaccessible, or present, nor what their payloads contain. It
does not authenticate any NIST animation or support a conclusion about
substitution, deliberate removal, collapse cause, or intent.

**Next check, not performed:** run a separately preserved, minimal live CDX
query using only field names in the pinned server README's public-field list,
and separately preserve the prior null-field query. Do not treat a response
to that query as authentication of the WARC. Obtaining or inspecting a WARC
would remain a separate access and payload-integrity test.

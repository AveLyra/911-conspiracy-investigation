# Internet Archive CDX public-field documentation and locator observations

**Record type:** public-source documentation observation and bounded inference.
This supplements the earlier CDX-query and replay records; it does not
reconcile or replace any recorded value.

## Source and retrieval limits

Primary documentation inspected: Internet Archive's `wayback` repository,
`wayback-cdx-server/README.md`, under the mutable `master` branch:
<https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md>

Access date: 2026-10-06. The rendered GitHub page identifies itself as the
Wayback CDX Server API documentation. Its text describes the documentation as
beta and gives 2013 changelist entries. A source commit/revision was not pinned.
An attempt to retrieve the raw README for hashing failed with a DNS resolution
error for `raw.githubusercontent.com`; therefore no SHA-256 is claimed for the
documentation bytes. This limits source-version reproducibility.

## What the documentation says

The README's public-field list names `urlkey`, `timestamp`, `original`,
`mimetype`, `statuscode`, `digest`, and `length`; it does not list `filename` or
`offset` among those fields. Its access-control section says some fields,
including `filename`, may be restricted and that a request carrying an API-key
cookie can be granted access to restricted fields. It also describes the
`offset=` request parameter as pagination that skips earlier result rows.

These are statements in the upstream project's documentation, not a verified
description of the live service configuration on 2026-10-06. In particular,
the documentation does not establish why the specific CDX response below
returned null values. Its description of `offset=` as a request parameter also
does not establish that a same-named value requested in `fl=` would represent a
WARC byte offset.

## Related case-specific observations, kept separate

- The 2026-10-06 [CU-animation CDX response record](wayback-cdx-capture-locators-2026-10-06.md)
  reports `null` for requested `filename` and `offset` columns on all six rows.
  Its saved 1,002-byte response SHA-256 is
  `f603430497d07b1b473afa40935785a308d42a27e1c0485c8092b4055105b6cd`.
- The 2026-10-05 replay record reports `x-archive-src` WARC-name values in the
  replay headers for two 2016 URLs, while the CDX response's requested
  `filename`/`offset` values were null. The WARC files and records were not
  retrieved or examined in those checks.
- The local derivative inventory records a 2011 identity-replay body of
  13,113 bytes and SHA-256
  `27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a`; the
  later CDX query reports, for that timestamp, status `200`, digest
  `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX`, and length `4107`. These are preserved as
  different interface outputs. Their semantics and relationship remain
  unadjudicated.

## Claim ledger

| Claim | Type | Support | Limit / strongest alternative | What would change it |
| --- | --- | --- | --- | --- |
| The reviewed upstream README lists a public CDX field set that omits `filename` and `offset`, and describes filename access restrictions. | Documentation observation | Internet Archive `wayback` repository README, linked above; page inspected 2026-10-06 | Mutable `master`; beta/2013 documentation; no exact live deployment configuration. | A pinned documentation revision or contemporaneous service configuration showing a different field policy. |
| The documented access-control model is one possible reason a public response might not expose filename data. | Inference / untested alternative | README access-control section plus the separately recorded null values | It does not show this policy caused the particular nulls, nor that access was selectively restricted for these URLs. | A same-capture response under known configuration, or the underlying WARC record and its retrieval provenance. |

**Interpretation ceiling:** the documentation supplies a possible
access-policy explanation to keep in the alternatives ledger. It does not
resolve the observed metadata differences, establish the active policy for
these records, prove that the underlying records are available or unavailable,
or support an inference of deliberate concealment or video substitution.

**Next check, not performed:** preserve the exact deployed documentation/config
revision if obtainable from public sources and separately inspect the WARC
records identified in prior replay headers, if they can be publicly retrieved.
Do not treat the documentation's general policy description as proof of the
case-specific cause of the null fields.

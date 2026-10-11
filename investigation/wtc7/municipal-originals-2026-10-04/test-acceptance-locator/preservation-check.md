# Independent request and response preservation check

October 4, 2026 America/New_York / October 5 UTC. Five preserved response
bodies are byte-identical to their corresponding scratch files. All five
request objects exactly match the declared queries and metadata contract.
This is a transport-body copy-integrity/request-conformance check only;
no response JSON was parsed or candidate result inspected.

## Scope and controls

Read main AGENTS, WORKFLOW, START-HERE and the full investigation CHARTER;
read this unit's complete protocol and the referenced drawing/folder locator
protocols to trace the request contract. Read the source-of-truth and
evidence-falsification skills. The preservation skill limits the sole write
to this new research note; raw requests/responses, existing notes and other
files remain unchanged. No network request, PDF/image read, source-content
view, candidate-list exchange, STATUS/README edit, Git, main/legal or engine
action occurred. This bounded assignment does not perform the protocol's
separate substantive metadata, catalog or search-completeness analysis.

Protocol SHA-256:
`3938808129a75bf279e8ca8edb885282a7eb96bd4a58514556091e4254d09163`.
Main control hashes matched previously read versions (`7f75b3`, exit 0).
An initial combined instruction-output delivery was truncated; separate
complete WORKFLOW/START-HERE (`4846cc`) and CHARTER (`04a839`) reads resolved
that display limit before verification. The truncation was not a response
retrieval or preservation failure.

Paths used:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/test-acceptance-locator
R=/private/tmp/wtc7-test-locator.g4fXce
B=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/drawing-locator/control-request.json
```

## Response copies and raw request pins

Actual check `6b294d`, exit 0, completed at `2026-10-05T00:48:21Z`.
For each exact prefix `generator signoff punch date control`, executed:

```sh
cmp -s "$U/$query_id-response.json" "$R/$query_id-response.json"
shasum -a 256 "$U/$query_id-response.json" "$R/$query_id-response.json" "$U/$query_id-request.json"
wc -c "$U/$query_id-response.json" "$R/$query_id-response.json" "$U/$query_id-request.json"
```

All five `cmp` calls returned 0, and both copies have each listed hash and
byte count. Total response bytes in either set: 171881. Total request bytes:
5512. Bodies were handled only as opaque bytes by comparison/hash/size tools.

| Prefix | Response bytes, each copy | Response SHA-256, both copies |
|---|---:|---|
| generator | 66134 | `bf13d5608fc49e3da64b3291b2779ddfd64692e05ae7c7fa063a9d7e2afd3186` |
| signoff | 30480 | `42c16897153f26bb0a0844f6693cd5cac3818a9dbd6e8acb85563a2616a5e6eb` |
| punch | 65056 | `cd6bfc2d72090d0dcd33cf8b014d4be63ae4b05d71ace3de66700cfa45f6b73d` |
| date | 1760 | `ea21d260015169581e7b80212786e6be4aeb7abd6ea8c821a555998ba89a2e4f` |
| control | 8451 | `7386207c519d9144fc0a2b9e6092351a41ba38059f2008e8156d4ed0686f6a29` |

| Prefix | Request bytes | Request SHA-256 |
|---|---:|---|
| generator | 1092 | `e1544eaee6223d67fae024e8af3b46ecb0f3632ac974f773fe71ca14d7699974` |
| signoff | 1090 | `49edcbb99fa46b38e296f30604fe9e92712eee08bd1a54aa85144efe4c9fb672` |
| punch | 1083 | `e89ebba5493130dbd6de0e5907738fb9e20e333521e75be5461605d0f6a8d573` |
| date | 1089 | `96a71e417281f8b1bf7fdbc78d63ab4a9ead179b32885f2f927f3b4540875c94` |
| control | 1158 | `05a0df86737b4efeaf9949051c23385e22ed46c16a4ddbca567511e1a45277ef` |

## Exact request conformance

Read the five request files and preceding control request (`028f34`, exit 0).
The preceding control pin is the same `05a0df...277ef` value listed in full
above; a separate `cmp -s "$U/control-request.json" "$B"` returned 0.
No prior or current response was parsed to establish this contract.

Stdout-only `python3` request validation (`195be5`, exit 0) loaded only these
five requests, the prior request and current protocol. `json.loads` used an
`object_pairs_hook` rejecting duplicate keys at every nesting level. It
compared each complete object against exactly:

```text
{"user":{"query":{"unparsed":EXACT_QUERY}},
 "count":50,"content_sample_length":0,
 "properties":[{"name":NAME,"formats":["VALUE"]}, ...]}
```

The exact ordered eleven names are `mes:key`, `title`, `source`, `agency`,
`box_name`, `folder_name`, `page_count`, `pdf_size`, `production_volume`,
`production_end`, `mes:date`. Each property has only `name` and
`formats:["VALUE"]`; order agrees with the prior contract, names are unique,
and complete-object equality excludes extra request fields. Count and sample
length were explicitly checked as integer 50 and integer 0.

Each exact query below was also located as a literal in the protocol:

```text
generator: ALL extension:pdf source:"WTC 7" generator test
signoff: ALL extension:pdf source:"WTC 7" "sign off"
punch: ALL extension:pdf source:"WTC 7" punch
date: ALL extension:pdf source:"WTC 7" "7/17/99"
control: ALL extension:pdf source:"WTC 7" box_name:"7DCAS" folder_name:"SKP-3 & SKP-4 AND REVISED S-TS-7 FOR YOUR USE"
```

All six checks per request returned true: literal query, complete object,
integer count, integer sample length, exact ordered properties and unique
property names. Five requests checked; zero failures; zero response JSONs
parsed. Request validation and prior-control byte comparison each explicitly
returned 0. Exact request conformity means semantic JSON-object equality to
the declared contract, not a claim that protocol prose has JSON byte identity.

## Limits

No preservation mismatch or request-contract failure was observed. Hashes and
byte agreement establish present local integrity relative to scratch, not
historical authenticity, API correctness, completeness, chronology of copying,
proof these payloads were actually transmitted or verified HTTPS status/timing.
Transport process receipts were not independently replayed or authenticated.
Response validity, query echoes, service termination/pagination, candidate IDs,
counts, joins, content and relevance remain outside this check. No positive or
negative substantive finding follows from these byte counts or hashes.

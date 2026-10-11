# E3 approach — peer source-reading record

October 8, 2026. Reader: `/root/approach_source_peer`, a separate prior-informed
AI reader. This is a manual native-cell attribution record, not human review,
calibrated curve containment, physical support, or historical corroboration.

## Frozen scope and prior knowledge

The controlling approach protocol SHA-256 is
`cc94c588f9b132318c7ca55fcffe1ed7eafbb92fd131583ffcbc74a13e5e54b7`.
The READERS contract hash is
`6a019e587d1cdb47303047c5c03dbae4d9c347941a8227f27a7a8e0b8dfd0b5b`.
E3 target is `[195,35,365,92]`; context is `[193,33,367,92]`, in zero-based,
half-open native cell edges. All 170 target columns are recorded for each of
the solid and dash routes, including columns with no attributed cells.

Before the new protocol froze, this reader read the main AGENTS, WORKFLOW,
START-HERE and CHARTER; the comparison PROTOCOL, NUMERICAL-PROTOCOL and human
review gate; the parent native-footprint and energy345 protocols; and the
existing E3/E4 locator-level inventory. The unchanged complete Im10 strip and
complete composed page 76 were each viewed once for orientation, with original
detail requested. No coordinates were inferred from the page display.
That visual familiarity is prior knowledge, not a blind source reading. The
new target protocol was read and its hash checked before raw context reading.

The Im10 encoded JPEG hash was verified as
`fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3`,
dimensions 745 by 92. The complete page hash was verified as
`0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6`,
dimensions 1700 by 2200. Initial checks used `shasum -a 256` and
`sips -g pixelWidth -g pixelHeight`. Annotation builds verify the pinned source,
protocol, display runner, parent helper and saved context bytes before and
after expansion. The literal annotation script does not decode source pixels
or use an RGB classifier.

No new primary or other reader annotation was read before this peer script and
JSON froze. Root supplied the primary's existence/hash but its contents were
not opened. All previous files and sources were left untouched by this reader.

## Actual raw context coverage

Python used:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
The display runner hash is
`384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3`.

The reader reran `python3 -B read_context.py controls`; all 11 control values
were true (receipt `67ebc7`). In the same receipt, `shasum -a 256` independently
confirmed that both context saves have hash
`783cd6f756918cef8a70ea79d925d7b010554b535f8d8f654970605d1c8b9095`.
The parent's pre-save control and save receipts were supplied as background;
they are not substituted for this reader's actual inspection.

Every call below used `python3 -B read_context.py show --pair E3 --first FIRST
--last LAST`. Each printed every requested column, all rows 33 through 91,
omitting only exact `(255,255,255)`. `gN` represented exactly `(N,N,N)`;
equal-value row runs were lossless. All 15 outputs exited 0 and were
untruncated. All displayed values and the explicitly omitted exact-white
complements were read before the annotation script was written.

| Inclusive columns | Actual tool receipt |
|---|---|
| 193–202 | `3229fe` |
| 203–212 | `43b34d` |
| 213–222 | `06a54f` |
| 223–232 | `9c2e96` |
| 233–242 | `f515c5` |
| 243–252 | `328fad` |
| 253–262 | `c54483` |
| 263–272 | `4bf66c` |
| 273–282 | `63ea86` |
| 283–292 | `91ca20` |
| 293–307 | `9c573b` |
| 308–322 | `380f9a` |
| 323–337 | `2d6eb7` |
| 338–352 | `f98114` |
| 353–366 | `c6650d` |

This covers 174 columns by 59 rows = 10,266 source cells. The two cells of
context beyond the target on either horizontal side were inspected without
silently expanding the annotation target. There are no uninspected context
columns. This is a self-attestation of AI reading; a receipt cannot independently
witness perception or prove that attribution is correct.

## Manual attribution and limitations

Core and fringe choices are literal human-readable instructions in
`reader-E3-peer.py`. Expansion parses only those instructions. There was no
threshold, automatic color selection, smoothing, interpolation, centerline
fit, source editing, physical-unit conversion or transfer from the primary's
new annotations. The complete-page legend supplies the local style naming;
vertical ordering alone does not establish identity.

The early target includes other colored strokes and a crop-edge entry. This
reader retains some dark entry cells as solid-only uncertain candidates. A
second uncertainty neighborhood covers possible black/blue edge allocation.
In the broad black/blue contact neighborhood, the reader could not confidently
assign the selected dark footprint specifically to the black continuous route,
so that footprint is recorded once as unassigned, with the E3 solid route
referencing it. This is deliberately a limitation of this reader's attribution;
it does not establish that another reader cannot distinguish those cells.
It does not implicate the spatially separate E3 dash route.

The `candidate_routes` vocabulary contains only E3 solid and dash. A
solid-only candidate reference therefore does **not** rule out blue ink or
colored compression as an alternative owner. The export explicitly states
this representation limit. Unassigned membership IDs identify aggregate
visible candidate neighborhoods; they are not proof of a continuous physical
piece across columns, of a hidden E3 path, or of exclusive E3 membership.
In particular, interrupted early candidate entries under one band ID must not
be interpolated. Per-member ownership against non-E3 curves is not enforced
by this schema.

Fifteen separate local dash-body IDs preserve the visibly separated dash
candidates; no intervening pale/white interval is bridged. The first cropped
dash candidate and the rightmost target contact retain explicit boundary
flags. Pale material at some dash edges is fringe-only; it is not a proven
pre-raster curve boundary. Empty sets mean no attribution by this reader,
not true absence, an exact gap, zero energy or a physical endpoint.

Farther right, cells between distinct black core candidates are recorded once
in unassigned bands with reciprocal solid/dash references. No selected cell is
duplicated into both model routes or into a route and an unassigned band.
The last target columns do not resolve whether a hidden solid continues,
terminates, or is overprinted beyond the target.

## Freeze and verification

The initial `python3 -B reader-E3-peer.py --save` completed its two in-memory
expansions and validation but failed at the exclusive-create file operation
because this worktree lies outside the default writable roots (receipt
`8a23d6`, `PermissionError`). No output JSON was created by that attempt.
The same exact save was then approved through the tool's escalation mechanism
and succeeded (receipt `5d5a19`, exit 0). This was not an overwrite or a change
to the protocol or annotation literals.

Frozen script SHA-256:
`dde56416f60a972dda91a81e9893e76a18c5abcd1b3f092e19f35ec2302fefb8`.

Frozen JSON SHA-256:
`b93d4745e7b05496a64ebb14c10ae525bfec0b9892cdfeca77b21a7d30352828`,
250,938 bytes. These pins were sent to root before any counterpart reading.
The script exposes `build()` for later independent replay without overwriting
the saved original. Its `--save` path uses exclusive creation.

A separate read-only invocation imported this script, performed two further
`build()` expansions and compared their serialized bytes with the saved JSON
(receipt `e36fcd`, exit 0): all three were identical. The script's validation
checked complete route-column coverage; integer target bounds; sorted,
disjoint core/fringe classes; exact fragment-membership unions; target-edge
flags; nonempty bands; same-column reciprocal candidate references; and
absence of any duplicate selected source cell across routes and bands.
Those are producer checks, not an independent recovery or proof of identity.

| Export component | Records | Core cells | Fringe cells |
|---|---:|---:|---:|
| Solid route | 170 | 134 | 149 |
| Dash route | 170 | 98 | 161 |
| Unassigned bands | 51 | 39 | 64 |

The source/display controls and all attribution disputes remain distinct from
the later separate checker, geometric support decision and human review.
No selected review slots, historical discrepancy, physical support,
cause-ranking change, source promotion, disclosure, commit or push occurred.

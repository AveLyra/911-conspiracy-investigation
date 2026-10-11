# Separate synthetic-delivery review

October 9, 2026 local. No historical measurement or human acceptance.

## Result

The independent cell-boundary oracle agrees with all twelve recorded selected
cells. One intended Fit target misses: (500,180) selects (500,179). Fit targets
(500,179) and (500,180) have different requested centers but the same delivered
click, (330,472). All twelve cases have stable recorded geometry within 1e-9.
Thus changed delivered coordinates explain this run's miss without a demonstrated
mapping defect. This does not identify the rounding layer or prove the cause
of the earlier uninstrumented miss. Six fine-view successes are not a general
precision guarantee.

All twelve individual case objects exactly equal their aggregate counterparts,
including every key/value. All 36 case events exactly equal the corresponding
entries in the 42-event raw log. The remaining triplets, sequences 19–21 and
31–33, bridge the recorded zoom transitions and retain the prior locked cell.
Their target IDs remain null; button identity is not invented. All 42 events
are recorded completed/trusted and synthetic-control-only.

Four recorded keyboard steps advance right/down and reverse left/up exactly.
The twelve complete draft snapshots contain 72 uninspected historical rows and
no synthetic draft. Keyboard records retain zero draft counts and no pending
box; they do not contain independent full post-keyboard draft snapshots.

## Independence, execution and preservation

The checker was prior-informed and independently authored without importing
or executing the producer's mapping/controller/logger modules. Protocol and
methodology preceded observations. Some initial Fit observations occurred while
schema alignment was being finished; the checker froze before this reviewer
inspected actual case data, not before all browser observations. Schema alignment
preserved nullable fields and logged control-event gaps, without relaxing the
mapping criterion.

Actual commands, from this directory, under Node v22.16.0:

```sh
node --test test_delivery.mjs
node verify_delivery.mjs browser-cases.json
cmp verification-peer.json verification-root.json
```

Sixteen tests passed (`ed563a`); verifier passed (`be77de`); summaries are
byte-identical (`54016a`). Separate read-only Node assertions checked complete
case/log/keyboard reconciliation (`7d3586`) and zoom bridges (`ed563a`). No peer
check failed. The peer JSON was saved through apply_patch.

Archived pre-guard server bytes match packet01/02 pins; final server bytes match
packet03/04 (`37d537`). Root's initial API failure and deliberate server-stop
chronology remain root-reported, not independently witnessed. Final HTTP and
full protected-input closure belong to root's separate checks.

## Selected byte pins

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| browser-cases.json | 175434 | aac9dc29fa226b8d56b2ca1c1fcb931c8e41287f2687ca956ee688e9f14a8597 |
| verification-peer.json | 21434 | 7fb234f224f3b6173585ed6436c54bff1e0d22fff2a3c5b7852ac37b35097279 |
| keyboard-observations.json | 1549 | cda49426e046ffe39e86662d18527d0c0b3f79f2472dd3f4ac1ae769dae62531 |

Protocol, checker and original-manifest pins are in the peer summary. Complete
24-file ordered pin-array fingerprint from `7d3586`:
`468f6f008697bef5c86871bdb5cbfd231cb884c00ba8a90ddc90d5816cbb8bed`.

This is computational review of supplied records, not independent browser
observation, display calibration or human localization. Pre-request visualViewport
was unrecorded; visibility checks cannot exclude unrecorded overlays. No browser,
server, source edit, historical annotation or accepted-state change occurred.

# Independent remaining-fire-figure coverage check

2026-09-24. Research only. Read the frozen first-action plan, full coverage
join implementation and saved result after the initial media review had been
saved. Did not read root's new fire observations or synthesis, view source
images/PDF pages, run the producer, mutate its inputs, or acquire anything.

## Result

**Candidate membership and the 8/26 disposition count independently agree.**
The source-map's precise remaining-candidate table contains **34 unique figure
identifiers**. Eight have paired records in the declared 25-photo inventory;
26 have no matching extraction/paired record in this declared union. Figures
5-145 and 5-146 are both in the latter group. This is finite research-coverage
accounting, not global absence, report completeness, source unavailability or
historical fire absence.

There is one precision issue in the reviewed version: the source map gives
**Figures 5-145/146 jointly at pages 275–276**, whereas the join assigns an
individual page to each figure. That is not directly supplied by this grouped
map row. Other grouped entries retain page sets correctly. Preserve both
candidates' map locator as `[275,276]`, or label the individual assignment as
an inference until a separately recorded complete-page/native-image review
establishes it. This does not affect candidate membership, 8/26 dispositions
or the decision to inspect both pages plus context. Do not silently make the
later visual association look like an earlier map-only result.

| Independent check | Actual result |
|---|---|
| Parse only the source map's `Located but not visually inspected in this audit` table, not the producer's transcribed array | 34 identifiers, all unique; same ordered membership as the saved result |
| Join each candidate against the key's `assets[].figure_associations[]` and batch inventory's stated paired review statuses | Every extracted-ID and paired-ID list agrees for all 34 rows |
| Paired candidates | 5-59, 5-60, 5-61, 5-79, 5-111, 5-114, 5-116, 5-118 |
| Remaining candidates | 5-121, 122, 123, 124, 128, 129, 130, 132, 133, 134, 136, 138, 139, 140, 141, 142, 143, 144, 145, 146, 152, 153, 154, 155, 156, 159 |
| Selected 145/146 | Neither has an extracted or paired ID in the reviewed key/batch records; the extension target-page set excludes 275/276 |
| Saved input identities | All 12 recorded SHA-256 pins match current bytes when the one relative script path is resolved against this audit directory |
| Subsequent source-family coverage | Previously inspected Peskin/Didik, photometric/correspondence and late-fire/CBS scopes do not retire 145/146 or supply a scored observation for them |

The later-family account remains a **manual scope transcription**, not an
automated exhaustive image search. The full media review records the inspected
union and its actual limits. Peskin's scene links include 147–149/151, the
photometric/correspondence targets are 148/149, and the late-fire work targets
157/158. Didik includes 125/126/150 context, with 124 appearing in timing text;
caption or contextual mention is not a native-image annotation. Extra imagery
may exist outside this union. Even an earlier full-page reading would not
necessarily satisfy the paired-annotation requirement.

## Method and actual commands

The independent check used system Ruby 2.6 standard JSON/Digest/Pathname and
did not import or execute `join_fire_coverage.rb`. `cat`, `sed`, `rg`, `jq` and
`shasum -a 256` were read-only. The decisive membership extraction was:

```ruby
section = File.read(source_map_path)
  .split('## Located but not visually inspected in this audit', 2).fetch(1)
  .split('The two briefing PDFs', 2).fetch(0)
figures = section.lines.select { |line| line.start_with?('|') }.flat_map do |line|
  line.split('|')[1].scan(/(?<!\d)5-(\d+)((?:\/\d+)*)/).flat_map do |n, rest|
    [n.to_i] + rest.split('/').reject(&:empty?).map(&:to_i)
  end
end.sort
```

All figure assignments and IDs were independently joined using the parsed
key/inventory, and compared exactly with every saved row. Intersecting the
34-figure set with the paired inventory yields eight; subtraction yields 26.
The complete successful read-only invocation exited 0. Directly reading the
nine source-table rows confirmed the grouped page-range transcription and
exposed the 145/146 page-specificity issue. No numerical tolerances or visual
interpretations were used to force agreement.

Two failed reviewer attempts remain part of the method history:

1. Hash checking from main initially treated the producer's relative script
   path as relative to main. It failed with a missing-file error. Resolving
   that one path against this audit directory allowed all twelve pins to be
   checked. This is a receipt portability limitation, not an altered source.
2. The first figure parser lacked a digit-left-boundary guard and incorrectly
   read the tail of the page range `275-276` as figure 5-276. It returned 35
   candidates and failed comparison. The corrected literal figure grammar
   above excludes that page-range substring and returns exactly 34. The
   source-table reading, not the target count alone, justifies the correction.

## Bounded extractor-wrapper inspection

Read all of `extract_fire_first_action.py` and the relevant preserved
`prepare_assets.py` source sections (lines 1–185 and 260–340, plus function/
constant searches). This is not a complete parser review or fresh extraction
reproduction. The wrapper pins the legacy extractor before import, overrides
only HERE/SELECTED/PAGE_ORDER, copies the exact first-action protocol, and
records its overrides in a separate receipt. The legacy extraction source
checks the preserved report's hash before/after, uses fresh output directories,
starts figure associations empty, and preserves terminal JPEG codestreams
without Pillow resaving when its explicit conditions apply.

The wrapper's historical command field would name the reused implementation;
its separate wrapper receipt correctly explains the actual route. Actual run
success, source identity, image recompression status, render diagnostics,
figure associations and complete visual coverage must be checked in the new
run artifacts and observation record. This review supplies none of those
unperformed checks. In particular, preserved render warnings are not made
acceptable simply because the process returns zero. The old extractor's
historical verification mode must not be applied using an unrelated association
sidecar; the first-action plan correctly excludes that shortcut.

## Reviewed-version pins

| Artifact | SHA-256 |
|---|---|
| FIRE-FIRST-ACTION.md | `7cbdd9cbdf67c2c8570dfbc249045c1ddb6b91f07394a481e74da932f93243c8` |
| join_fire_coverage.rb | `173c28424f982ca93c82c9be257019cbf4e651ced88a769b27e6f25df4fb7290` |
| fire-coverage01.json | `926b86b5004f9566fbb470ab81242b3f5861c9f8d7c909a502346f67e00c075a` |
| extract_fire_first_action.py | `ff83894cf7025f05247f5941ca24fc97f49aeff1e43c1b16f5a4575c0d8d9ad7` |

The grouped-locator issue was sent to root before this note. Counts are not
withdrawn, but page-specific source attribution needs the qualification above.
No physical, thermal, mechanism, intent, legal or package-completion conclusion
follows from the checked coverage result.

## Follow-up — 2026-09-24: correction independently verified

The initial review above is preserved. Read `FIRE-JOIN-CORRECTION.md` and the
two-line script diff, then independently compared the two result objects and
current source pins without executing either producer or reading the new
`fire-first-look.md` observations.

All six checks passed in a read-only Ruby/JSON/Digest/Pathname calculation,
exit 0:

- `join_fire_coverage.v1.rb` exactly matches the original script hash recorded
  in `fire-coverage01.json`.
- `fire-coverage01.json` retains its original reviewed hash.
- All twelve revised input paths are absolute and all current bytes match
  their `fire-coverage02.json` pins.
- Every non-script input pin is unchanged.
- Candidate membership, counts, scope and manual-follow-up account are
  unchanged: 34 candidates, 8 paired and 26 remaining.
- The only row changes are the declared corrections for 145/146: both now
  retain `[275,276]` and `grouped-map locator; no unique page assigned`.
  All other fields and all other rows compare exactly.

The script diff contains only the absolute script-path change and grouped
145/146 locator change. `diff -u` exited 1 because it found those expected
differences; that is not a failed scientific check. The current correction
resolves both issues identified in this review while preserving the original
result and its limitations. Later visual associations remain a distinct
evidence layer, not verified by this follow-up.

| Follow-up artifact | SHA-256 |
|---|---|
| Preserved v1 script | `173c28424f982ca93c82c9be257019cbf4e651ced88a769b27e6f25df4fb7290` |
| Corrected script | `4e1026df562d09e28e7f95caf9bef6565065cd189dac77eb91e37ab6a84cb4db` |
| Preserved output01 | `926b86b5004f9566fbb470ab81242b3f5861c9f8d7c909a502346f67e00c075a` |
| Corrected output02 | `f68729fa4d96471481b53e71f88feb39489ec42e519a1cb60a03dff53138aba4` |
| Correction note | `155dc171adc0bb6ec2f269ca47332c7c38937813bdd2ff493f0c600cfb1b271b` |
| This review before appended follow-up | `802e6894faad8f707affcdd0a1d5b8b590d137f08abab48f4537b2d214b9e8e0` |

No images, new source contents, broader coverage or physical conclusions were
added to the independent verification scope.

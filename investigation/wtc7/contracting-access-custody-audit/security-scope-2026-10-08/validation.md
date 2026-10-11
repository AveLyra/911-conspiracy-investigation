# Security filing review validation

October 8, 2026. These are source-representation, coverage and document checks,
not historical authentication, a complete-filing audit or engineering tests.

## Actual checks performed

1. Repository intake ran with `python3 /Users/admin/.codex/skills/repo-orchestrator/scripts/repo_intake.py`
   in the investigation worktree (receipt `7282c3`). Branch/HEAD and extensive
   intentional WIP were inspected; no reset, checkout, commit or push occurred.
2. `shasum -a 256 SCOPE.md web-projection-*.json *.headers *.response`
   pinned the initial artifacts (receipt `4ff713`; projection06 was added and
   hashed subsequently). The complete current set is [source-manifest.json](source-manifest.json).
3. A read-only `python3 -B` JSON/hash/byte audit compared every manifest entry,
   including thirteen files, and checked all three HTTP403 HTML headers/bodies:
   all pins and lengths matched, all bodies were 4,819 bytes (`059fb3`).
4. Six `cat web-projection-0N.json` reads were JSON-parsed in the orchestration
   context and each `output` compared by exact string equality with the
   corresponding retained in-session tool result. All six matched. This checks
   preservation of reader returns, not equality to SEC original bytes.
5. Read-only `python3 -B` audits collected source-URL/line labels and checked
   the following complete passage ranges. Every required label was represented,
   and overlapping body-line strings agreed exactly (`059fb3`, `172d00`).

```text
SEC99: (221,298), (350,397), (486,500), (606,643), (696,729)
SEC00: (160,310), (329,376), (397,414), (457,463), (573,611)
SECQ:  (0,39), (266,298), (306,470)
```

The computed total is **13 ranges / 714 required line labels**. Receipt059fb3
mistakenly printed a hardcoded count of15 after running the correct predicates.
Receipt172d00 recomputed the count from the actual range dictionary and
confirmed13/714. This reporting-label error is retained; no predicate, source
text or disposition changed to obtain a pass.

6. The source interpretation was separately read before the root report;
   the date discrepancy was preserved; final review found no material
   correction. A separate local verifier checked all manifest artifacts,
   seven independently selected claim/date ranges (488 labels), and all five
   manifest review ranges (1,620 labels). These are different coverage sets,
   not conflicting counts. See [review.md](review.md).
7. `git diff --check -- research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md`
   passed after the deduplicated local feedback update (receipt `dc4136`).

## Final assembly check

Root's read-only `python3 -B` audit (`3157a3`) checked five local Markdown
files, eight local link occurrences, thirteen manifest artifacts, two review
snapshot pins and three updated navigation entries. All matched/resolved;
final newline, trailing-whitespace and conflict-marker checks passed.
Three external report links were not reopened during this local check.
The separate verifier independently resolved all eight local links (`9ed76c`)
and checked the two snapshot hashes (`f3414b`), with no material correction.

`git diff --check -- research/README.md research/sherlock-wtc7-investigation/STATUS.md research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md research/sherlock-wtc7-investigation/contracting-access-custody-audit/README.md`
passed (`69674b`). The corresponding diffstat includes extensive pre-existing
WIP and is not this unit's change count. The new unit is untracked until a
later authorized commit; no commit/push was performed.

## Reproduction boundary

The JSON manifest gives exact file paths, byte lengths, SHA256 hashes, source
URLs, periods, date qualifications and reading coverage. A local reproduction
can parse each JSON, recompute its hash/length and test the listed source-label
ranges. The raw origin response cannot be reproduced from a projection. A
future original acquisition must be recorded as a new artifact, compared with
this preserved representation and reviewed, not silently substituted.

No generic software suite, fresh scientific simulation, human annotation,
expert review, original-filing authentication, cause ranking, legal promotion
or Sherlock/Faraday acceptance was run or supplied by these checks.

## Remaining limits

The selected 1997 body remains unread. Direct acquisition of all three usable
filings failed. Saved reader windows are partial and were preserved after
initial inspection. A second reader shared those representations. WTC7 scope,
contract completion conditions and actual later access remain unidentified.
These are consequential limits, not ignored failures. The finite source pass
ends with them; the full charter remains active and incomplete.

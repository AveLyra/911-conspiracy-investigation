# Verification and acceptance record

September19,2026 local / September20 UTC completion. Research-only. Numerical
checks do not upgrade the descriptive observations to calibrated measurements,
human acceptance or causal findings.

## Commands actually run and results

Working directory for helper/test commands:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-sequence`.
Python below means the exact bundled executable
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
FFmpeg and ffprobe were `/opt/homebrew/bin/ffmpeg` and `/opt/homebrew/bin/ffprobe`,
both reporting7.1.1; complete version output and status remain in both runs.

1. `python3 -B test_sample_sequence.py --out <unit>/root-control01` using that
   bundled executable: exit0,14 grouped tests in0.824seconds. The exact expanded
   command, inspected scope and limits are in [root-preflight](root-preflight.md).
   Real synthetic decoding plus mocked negatives and saved diagnostic streams
   are distinct from independent validation of historical DV footage. The
   producer's13-test control01 and14-test control02 remain separate records.
2. `python3 -B sample_sequence.py --manifest <unit>/selection.json
   --manifest-sha256 21d9595609115deb0ea35a9cd81d8d01c38d92c06716eeb9dc1aa0285acc1867
   --plan <unit>/FRAME-PLAN.md
   --plan-sha256 4c2870ab8775dd4a8b33fdbd59d32fafc2940fb14d7cee6cc19df829ad476297
   --out <unit>/run01`, then the same with run02: each exit0,
   `descriptive_candidates_only`, two sources. Here `<unit>` is the absolute
   working directory above. Every expanded probe/decode command and numeric
   status is retained alongside its stdout/stderr. Both source receipts have
   empty refusal reasons and scientific_or_human_acceptance:false.
3. Another agent independently traversed all2,106 decoded inventory rows and
   all128 PNG instances across the two passes. Its [review](independent-review.md)
   retains the entire read-only checking command and output summary. Root read
   that command, extracted its sole shell-embedded Python block without
   changing it and executed it from this unit: exit0,
   `PASS inventory_rows 2106 PNG_instances 128 source_product_pairs 2`.
   This is a rerun of the independent method, not a third independently written
   method. Source hashes/sizes, six catalog identity fields, rational PTS,
   dimensions/SAR/interlace, all PNG/RGB hashes, command arrays and stages agree.
4. Probe stderr is empty in all four runs; decode stdout is empty; all eight
   probe/decode returncodes are0. Decode logs contain320 total informational
   lines:128 selected-frame records,128 color records,8 configuration lines
   and56 other reviewed lines. The helper and independent traversal reject
   severity/control/unknown-message failures. This does not exclude silent
   decoder defects or authenticate a camera original.
5. Both root and observer individually displayed all64 run01 PNGs at original
   detail. No128-image visual-coverage claim follows from repeat products.
   Observer separately ran its manifest-file hash checks:26/26 and38/38 OK.
   See [observer](observer-sequence.md) and [root](root-sequence-freeze.md) for
   actual descriptive coverage, timestamps and the asymmetric freeze deviation.
6. Root's initial final-artifact check parsed both Python files without writing
   bytecode and41 JSON files (root/source metadata, run01/run02 and the three
   test-results files). Deliberately malformed negative-test fixtures were not
   blanket-parsed as valid JSON. It checked10 then-existing Markdown files for
   trailing whitespace and11 local links for existence, and rehashed the pins
   below: exit0. Later review/validation notes receive a separate final check.
7. `git diff --check -- research/README.md
   research/sherlock-wtc7-investigation/STATUS.md
   research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md`, from the worktree:
   exit0, no whitespace errors. This checks tracked navigation changes, not an
   automatic admission of every existing untracked research artifact.
8. `python3 /Users/admin/docs/911/tools/validate_record.py --strict`, from main:
   exit0, `OK (headers + issue↔fact links + citation tags)`. No legal-record
   edits were made. This does not factually or legally validate this research.
9. Final read-only syntax/JSON/link/pin check: exit0, two Python files,
   41 JSON files,12 Markdown files and18 existing local links. Reconstructed
   the critical review's exact report hash by removing only the three
   disclosed navigation lines: PASS. Frozen observer/root/numerical-review
   hashes remained unchanged. Repeated tracked `git diff --check`: exit0.
   Final report SHA-256:
   `365f7cc66e48a948427a93704f9a709eb196ce1493415a3a1b48d9184063665f`;
   critical review SHA-256:
   `a9f314489fde97928d714c54810dc76314a66f04ab357eb37f23beba094b8f42`.

## Preserved limits, failed attempts and deviations

The initial producer test invocation lacked worktree write permission and did
not execute tests; the authorized runs are separately retained. The numerical
review first guessed the wrong snapshot filenames, exited1, listed actual
files and reran the entire corrected traversal; no source output was changed.
Root also encountered a nonexistent research-subdirectory README, located the
actual research/README.md and read it before editing. One report patch failed
its exact-context check and was reapplied with corrected context, without
waiving verification. Premature reads of the not-yet-created helper review did
not establish pre-run review; root's own earlier preflight did exist.

The observer summary arrived before root's full record was frozen. The report
explicitly discloses that protocol deviation and does not claim two fully
independent pre-exchange visual records. The producer's separate helper review
arrived after run01, although root's code/test review and written preflight
preceded it. Old protocols/frozen notes and previous errored Dub6 outputs were
not rewritten to hide these limits. No raw diagnostic from an excluded source
was silently promoted by the new helper.

The [critical consistency review](critical-review.md) identified four wording
issues: common inputs versus authenticated common origin, encoded PTS versus
camera/event clock, separately zeroed timestamps versus independent clocks,
and selected products versus decoded inventory. All were corrected and the
reviewer reread the report. The reviewer authored the helper; this was not an
independent code or fresh visual audit. Its reviewed report SHA-256 is
`60c0e41b445eb2a28dadafab66b4362f5c30e524268a0639fe11bada57703fa9`.
Only links to this verification record and that review were added afterward;
the final check reconstructs the reviewed text by removing those three new
lines and requires the same hash, rather than silently updating the review pin.

## Important pins

| Artifact | SHA-256 |
|---|---|
| PROTOCOL.md | 878822418fae5d60096bbc509e101025cdd23463f062ce6fb7e0eb25c9098ef9 |
| FRAME-PLAN.md | 4c2870ab8775dd4a8b33fdbd59d32fafc2940fb14d7cee6cc19df829ad476297 |
| selection.json | 21d9595609115deb0ea35a9cd81d8d01c38d92c06716eeb9dc1aa0285acc1867 |
| sample_sequence.py | c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d |
| test_sample_sequence.py | cd997911f50d89d57c65906a1ac4eef3cda09ac4667a1f07307f9945068fcc43 |
| observer-sequence.md | a193075371078b2c78c4afa90800e7fcaf054d8e518aaf5b7452903891a3e0bd |
| root-sequence-freeze.md | ffc850a24c5385c50f1d684bf1670f840cecbd307bc5d6977af4058acb39eeb0 |
| independent-review.md | 8bc2a41dc295016653bed0e56306c4dc31733ba141f8d79eea8a788d40752f68 |

Source/frame/product pins are in the numerical review and manifests. Hashes
protect current-byte identity, not truth, original custody or physical adequacy.
No source acquired in this unit has been uploaded, published, committed or
pushed; no accepted Sherlock/Faraday finding or main-repository legal promotion.

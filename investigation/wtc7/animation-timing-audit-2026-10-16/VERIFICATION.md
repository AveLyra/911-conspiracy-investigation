# Execution, limitations and adversarial review

Executed October 16, 2026. No actual engineering expert, law faculty, independent
agent or human measurement review is claimed. The source, numerical, opposing
interpretation and records-law perspectives below are self-review lenses.

## Performed checks

- Freshly hashed four previously held SWFs and required exact expected hashes
  before parsing. All four matched. Every declared inflated file length matched
  the actual length. Root/sprite boundaries were checked; no source was edited.
- Ran `audit_swf.py` twice, separately, against the verified media store.
  `cmp swf-structure-run01.json swf-structure-run02.json` returned 0. Both files:
  318,296 bytes, SHA-256
  `bbd16840d5d85f69a317ed56b8325915c28c8bfa80e9ceaa874cb807c5b9f2a0`.
- Ran `compare_records.py` with each respective SWF output. `cmp` returned 0.
  Both comparisons: 5,461 bytes, SHA-256
  `ad73d90a800fd9c90dd0a3a90bb0cebd2673443906befe4fc1058c8c14031a1d`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_audit_swf.py test_compare_records.py`
  passed all **16** tests. Ten parser controls cover plain/compressed headers,
  nested video tags, declarations, retained conflicting declared length and
  malformed/truncated input. Six comparison controls cover Decimal subtraction,
  signed residuals, proxy/reference treatment, conflicting clocks, positional
  tag eligibility and pair differences. These do not validate ActionScript,
  Flash playback, source authenticity, a solver or a cause of collapse.
- Read NCSTAR 1A physical 83–86 (printed 41–44), and NCSTAR 1-9 physical
  655–660 (printed 589–594) through PDF text extraction. Inspected complete
  page images for printed 591, 592, 593 and Table 3–1 on printed 43. First two
  images were previously retained renders; last two were newly rendered from
  the held PDFs at 100 dpi. Model display can resize images; small typography
  is not a subpixel measurement. The clock values and upper legends are legible.
  Earlier uncertainty about cramped lower ticks remains in its original report.
- Fresh source-PDF hashes matched the earlier report pins: NCSTAR 1A
  `03c801bc1338533b54c6a64a66f074165c9429a59df11e2f58a19f5da91aef09`;
  NCSTAR 1-9
  `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
  See `sources.json` for all acquisition kinds and render hashes.
- Captured selected official FAQ paragraphs on October 16 at 11:39:21 UTC.
  Acquired HTML: HTTP 200, 142,941 bytes, SHA-256
  `542c37e287e8567a912f668aaa57e4d8587328ce9fdf188612eb487e1e3999b5`.
  `nist-faq-capture-2026-10-16.json` preserves public paragraphs with whitespace
  normalized, source URL, acquisition time, length and original HTML hash.
  The entire HTML response is not retained in this packet. This is the current
  FAQ, not an authenticated reconstruction of its 2008/2011 text.
- Three fresh CDX probes at approximately 11:42:27 UTC returned valid HTTP-200
  JSON. All returned rows are saved in `archive-index-probes-2026-10-16.json`,
  with exact request URLs, lengths and response hashes. Responses were capped
  at 2 MiB and 1000 rows; these actual lists contain only 3–6 data rows each.
  Index observations are not promoted to original payload observations.
- Read the primary *Quick* opinion's search/Exemption 3/segregability reasoning,
  *Cole*'s request interpretation, search, withholding and segregability reasoning,
  *Shapiro*'s concrete-record explanation/remand analysis, and §7306's text.
  Sources and hosting/mirror distinctions are in the report/manifest. No docket
  status, present agency affidavit or current litigation record is asserted.
- All Python files passed AST parsing; all eight JSON files parsed. Markdown
  links passed filesystem-or-tracked-Git-blob checks. All four preserved old
  report hashes matched their unchanged HEAD blobs. A targeted disclosure scan
  found none of its credential/private-contact/case-metadata patterns; this was
  supplemented by substantive review, not treated as universal privacy proof.
- `ghave` identified the authenticated account as **AveLyra** and the exact
  destination as **AveLyra/911-conspiracy-investigation**, public, default branch
  `main`. SSH with the same identity used by `gitave` returned GitHub's
  successful **AveLyra** authentication greeting (exit 1 is its normal no-shell
  result). No default-account credentials were substituted.

## Failures retained, not treated as historical evidence

The first rendering attempt returned exit 1 because the new remote output
directory did not yet exist. After creating that uniquely named directory,
both selected-page renders returned exit 0; Poppler emitted a Fontconfig warning.
The rendered complete pages were inspected and readable. These are local tool
events, not evidence of a NIST file problem.

The first source-manifest attempt failed on an existing report omitted from
the sparse worktree. The script was updated to read that exact unchanged HEAD
Git blob rather than hydrate media or assume the record absent. The next run
successfully pinned 14 source/capture records and four old reports.

The official Adobe specification URL returned 404 through the web tool; the
identified mirror failed browser retrieval and returned HTTP 403 through a
bounded direct request. No specification PDF was acquired. Format interpretation
therefore remains inspectable code plus synthetic controls and the located
documentation, not complete independent specification conformance testing.

## Scope and strongest objections

1. **Caption errors versus physics.** Conflicting clocks are established in
   this report edition. They may be editorial rather than numerical. No native
   frame/run crosswalk was obtained, so the correct clock and cause are unknown.
2. **Validation is not necessarily false.** Both 12.9-second subtractions work.
   The start of the observed interval is a vibration proxy; this limits the
   claimed directness and independence, not necessarily the physical inference.
   NIST disclosed some use of visual inputs and later-stage model limitations.
3. **Player changes versus content changes.** Hashes, canvas and tag structure
   changed across held captures. Nothing here demonstrates a changed FLV, a
   manipulated duration or historical video substitution. Unknown tag contents,
   dynamic loads and full ActionScript behavior were not executed or validated.
4. **Archive commonality versus removal.** Equal reported CDX digests across
   asset names are a concrete index observation. They can fit common site/error
   handling. Original ARC/WARC bytes and replay-layer transformations remain
   untested; no archived video payload was recovered by the index requests.
5. **Legal materiality.** A scientific or editorial issue is not automatically
   a defect in search, exemption or segregability proof. *Quick* and *Cole*
   are adverse merits decisions. The public report identifies record-specific
   tests without asserting that a court has accepted them or narrowing any
   request, discovery position or claim.

The public files contain only public technical/court-source observations,
original bounded analysis/code and generic legal implications. No private
correspondence, unreleased production, personal contacts, credentials, litigation
strategy or pending filing language is included. Commit identity is deliberately
handled by the configured AveLyra helper, not embedded as an analyst credential.
Old reports and evidence are unchanged. Local generated cache files are not
staged or removed. New PNG renderings are retained in the verified operational
media store, not published by this text-only unit; public source-PDF page links
allow readers to inspect the original figures.

Publication is verified separately after commit/push; this file does not claim
a remote update before the server confirms it.

The existing executable commit/push hooks were inspected and contain only Git
LFS delegation. This unit adds Markdown, Python and JSON only, with no LFS
objects. A command-scoped `core.hooksPath=/dev/null` may therefore be used for
this text-only commit/push to avoid the previously observed shared-store LFS
hook hang. No hook file or repository configuration is changed, and no missing
LFS upload is represented as complete.

## Reproduction

Run in this directory. Resolve the four SWF input paths using the repository's
verified media resolver; pass the containing directory as `--media-root`.
Use new output names because the scripts deliberately refuse to overwrite.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_audit_swf.py test_compare_records.py
PYTHONDONTWRITEBYTECODE=1 python3 audit_swf.py --media-root VERIFIED_SWF_DIRECTORY --output swf-structure-newrun.json
PYTHONDONTWRITEBYTECODE=1 python3 compare_records.py --swf swf-structure-newrun.json --output comparisons-newrun.json
```

Online captures are dated acquisitions, not deterministic bytes. Optional
`capture_faq.py --output NEW_NAME.json` and `capture_cdx.py --output NEW_NAME.json`
perform bounded public read-only requests and record their actual outcomes.
The source manifest generator takes `--case-root`, verified `--media-tree` and
new `--output`; it reads only the explicit public sources listed in its code.
No source media, model or ActionScript is executed by these procedures.

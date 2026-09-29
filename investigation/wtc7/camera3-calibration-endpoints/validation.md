# Endpoint and repetition validation

Research-only work in the dedicated `research/sherlock-wtc7-investigation`
worktree, based on `e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`. The prior metric
unit made progress and remains frozen. This new unit conducts the actual
source-raster query check, not a repeated general admissibility review.

## Fixed identities and source decode

[PROTOCOL.md](PROTOCOL.md), SHA-256
`8c23c82af39edf6cc1ff6627e3c70e38728b599c830b41865ec457d3f7950981`,
fixed source and indices 138/141/168 before new image viewing.
[prepare.py](prepare.py), SHA-256
`fb1a69aca54d0b945adbc4e8e620ddcc2b6adc3d3101465bd71748461db977e3`,
ran with Python 3.13.7/Pillow 12.0.0 and the exact previously recorded
FFmpeg command/binary. All eight input pins were unchanged after execution.

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-calibration-endpoints/prepare.py --out run01
```

Observed exit 0. The full 152,755,200-byte grayscale stream and all 442
per-frame hashes matched the prior diagnostic. The source and nested alias
each match `48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`.
The fresh raw stream was held in memory, not retained as a second large
artifact. Diagnostic text was not disclosed/exported; only its size/hash
and three literal corruption-warning mentions were recorded. No new
warning localization is claimed. The old rejected clean-decode/matcher
status remains intact.

The run has eight files: initial pins, receipt, three native PNGs and three
unmarked context crops. Its [receipt](run01/receipt.json) SHA-256 is
`8ae034a788f93a8c8c80704c4fe4b675105065be2a28567e9c4c21cf47a83219`.
Inherited diagnostic PTS are 9200/9400/11200 at 1/1000 second, not the saved
analysis origin zero or independently verified camera times.

## Independent visual and pixel checks

Root and the separate observer each viewed all three complete native frames
and three complete unmarked context crops. Their initial notes were frozen
separately before comparison:

- Root: `4a87459c047d179854fae44e52d125056422f0058c50384fb309b24678a1835f`.
- Separate observer: `f27e4352733c61ce838f836cdc05cbdd6e3a6b7b1dff806ac0a3e2ff3268c6a3`.

These are not human annotations or clean holdout data. Root withheld an
exact row count; the separate observer gave a tentative 14–16-cycle
envelope. The report retains that difference instead of creating consensus.

The [independent product review](independent-products.md) rechecked eight
current input pins, all six PNG identities, three native grayscale hashes
against the earlier map, exact selected PTS joins and all 1,956,150 context-
crop pixels by independent NumPy repetition. This was not a second full
442-frame decode. A pre-decode synthetic mapping check covered all 72,450
source cells in the declared context crop; image roundtrips were checked.

There is one preserved **presentation deviation**: the protocol called the
context crop coordinate-labelled, but the PNGs have no on-image labels.
They are unmarked images with coordinate mapping recorded in the receipt.
This is not a wrong crop or pixel transform. Neither code nor frozen
protocol was silently rewritten to erase the mismatch. Later query overlays
are separately identified and do not retroactively label the first crops.

## Exploratory refinement

Root's frozen note declared the two small endpoint boxes before those
displays were generated. [refine.py](refine.py), SHA-256
`8bf67d74d89dc3ef89f3a23f622a1aba2104e9d1f7883a0d49cb6b7079734cd8`,
ran with observed exit 0. It produced six unmarked 12x nearest-neighbor
patches, six separate red-query overlays and a receipt: thirteen files.
The receipt SHA-256 is
`104c342609d05b3067c65463841429f368771ce416950ef0c0bac58c760d037d`.
Pillow 12.0.0 is recorded. Python 3.13.7 was the observed launcher runtime;
the refinement receipt itself does not record the Python version.

Both analysts viewed all twelve complete refinement displays, so each
viewed eighteen displays derived from only **three distinct source frames**
across this unit. The separate observer viewed them before reading root's
note. Root viewed them before receiving the separate observer's refinement
summary, but root's final refined interpretation was written after that
summary; no separately frozen blind refined root verdict is claimed.

The [refinement review](refinement-review.md) preserves actual visual coverage.
Independent product checks cover nineteen input/product pins, all 793,152
unmarked patch pixels, all 793,152 overlay pixels and the six 104-pixel red-arm
masks. Exact binary-rational query mapping verifies the declared display
convention, not the historical Tracker coordinate convention or physical
endpoint identity. Source pixels outside the arms are unchanged and the
query-centre pixel is not painted over.

## Repetition diagnostic and independent arithmetic

[PROFILE-DECLARATION.md](PROFILE-DECLARATION.md), SHA-256
`6eaea06dcc96e3d429f1ab845ffe02ffea21329c6845e156ea58c1339760de71`,
declared strip, windows, lags, detrending, null threshold and tie rule after
the two first-pass notes but before calculations. It is explicitly
exploratory. [profile_rows.py](profile_rows.py), SHA-256
`b28ace99e0c532937ddfcf247f6724ad9eea8d4533f035fd20b4b43bf4c65ca5`,
ran under Python 3.13.7/NumPy 2.3.4/Pillow 12.0.0 with observed exit 0.
Its yielded tool invocation completed through the original handle; it was
not restarted. Nine controls passed before the historical profiles.

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-calibration-endpoints/profile_rows.py profile01.json
```

[profile01.json](profile01.json), SHA-256
`6cf5b643c0705f6ca95f2ddf2fb8e61e2eee891afeba806762f15c2b877c645e`,
contains all 549 row sums/means and 198 historical lag correlations. All
eighteen method/window maxima are uniquely lag 13 on the declared integer
grid. The nine controls retain 99 synthetic correlations, including nulls;
the case and cell counts are different.

The frozen declaration's phrase “excluding both query neighborhoods” is
imprecise: the strip excludes both exact query locations but intersects
each enlarged endpoint patch in 80 native pixels. The report now says
“excluding both exact query locations.” No selection, declaration, code or
computed array was altered. The independent review preserves the precise
intersection boxes and original wording.

The independent [verify_profile.py](verify_profile.py), SHA-256
`ccce8646eb4ad26f6f08d3534ec5423d9c6a7e449edec6f578dcb9d9b206590b`,
uses integer pixel sums, exact Fraction means/closed-form OLS and 60-digit
Decimal normalization, without importing the producer. Absolute tolerance
`1e-12` was fixed before result values were inspected. It reproduces all
549 sums/means, 198 historical correlations, eighteen maxima lists and nine
controls/99 synthetic cells. Maximum correlation difference is approximately
`1.19e-15`; the smallest admitted historical overlap norm is approximately
60.9444 versus the declared `1e-10` cutoff. Thirteen input pins were checked
before and after. No lag or tolerance was tuned to obtain the result.

The reviewer executed it with observed exit 0 and preserved
[independent-profile01.json](independent-profile01.json), SHA-256
`663d223bbe97d1809e48756e60162c3df899d53c966d160bafa0ea4a2a160f1f`.
Root read the entire verifier and reran it successfully:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-calibration-endpoints/verify_profile.py --out independent-profile-root01.json
```

Root observed exit 0, status `pass`. The root receipt SHA-256 is
`2680a5c50878e37bcc0bf8d548e5f008dc277b307d684d600c1f86132e18b58b`.
A later root whole-JSON comparison, also observed exit 0, confirmed every
field equals the reviewer's receipt except the recorded command. This is a
rerun of the independent method, not a second independent method or source.

The report's dimensional scenario table was also checked with exact Fraction
arithmetic: one regular interval is `12.75*0.3048` metres; lengths for
14/15/16 intervals are 54.4068/58.293/62.1792 m. Relative factors 14/15 and
16/15 are scenario sensitivities, not measured error bars. The vertical
query span divided by 13 is approximately 14.960563; Euclidean tape length
is not silently substituted for a fixed-column vertical period.

## Review and investigation boundaries

The [independent profile review](independent-profile-review.md) and
[final source-interpretation review](final-source-review.md) record their
exact report/code hashes and scope. Numerical reproduction is not physical
floor/endpoint identification; the visual reviewers do not certify the
profile implementation merely because the result resembles their reading.
No new measured acceleration, source-clock correction, projection-error
bound, universal support-loss conclusion or cause ranking is assigned.

Root read both completed reviews and their addenda in full. The final report
SHA-256 is `00d7e2a884d5b063a1a1ad14817e7b6954a57c181e4ec018c9e852ef4b88da43`.
The numerical review confirms the one exact query-language correction and
passes that hash; its own SHA-256 is
`ffd63ee6d8c1d7efba7cd15a114b13f0c564f51d38d6db43f728a92bbb747665`.
The source-interpretation review passes the preceding report hash
`dc9210ef904ee99e98159b9c834f674789b6d95a8a2b7dba427bbb9394e16143`;
its own SHA-256 is
`3db1a582e76b848f7fd4af426390b9296740873bf55c509699aa0bcb3d6988fe`.
Only the numerical reviewer's requested point-versus-neighborhood wording
differs from that source-reviewed version. The source reviewer did not
repeat a complete review of the final one-phrase revision. All bounded
current-unit reviewers are terminal; no old authentication failure is
substituted for a completed review.

Scoped integration checked all ten unit Markdown files plus the three
updated navigation/feedback documents: **13 documents and 176 local-link
occurrences**. All resolve, with 104 occurrences requiring the original
read-only repository because this worktree is sparse; this is not a claim
that the checkout is self-contained. No unexpected trailing whitespace or
conflict markers were found. All four Python files parse as ASTs, and all
thirteen explicitly rechecked unit/declaration/code/result/review pins
match. The tracked navigation diff check passed; direct checks included
the untracked unit omitted by an ordinary tracked diff. No canonical-record
validator or additional scientific rerun is claimed by these checks.

Some initial filename/extension searches found no later PNG/raw artifact;
that motivated the declared new decode, not an inference of destroyed
evidence. Two attempted reads of reviewer files occurred before their
authors had saved them; completed files were subsequently read. No numerical
or decoding failure occurred in this unit. Original source/warning failures
remain preserved and were not rewritten as current clean certification.

No original project XML/private fields, new agency production, held packet,
correspondence or canonical spines were opened or changed. No outreach,
external acquisition/transfer, Faraday bridge, application/model execution,
case import, promotion, filing, commit or push. Source/evidence safeguards
kept approximate scale support, endpoint ambiguity and cause inference
distinct. The next task is a declared conditional trajectory reconstruction,
not another generic calibration gate. The full goal remains active.

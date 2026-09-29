# Independent released-input literal-family search

September 13, 2026. Research-only; no source execution, law interpretation,
historical-run validation or causal ranking. The base protocol and prospective
byte-locator conventions control this finite search.

## Frozen independent pass

The independently implemented `independent_scan.py` and its source result
froze before inspection of the new root scanner or results. Prior June
coverage inventories, source manifests, September integrity metadata and the
earlier missing LCD602/LCD803 finding were known. This is independence of
implementation and new source reading, not an independent historical witness
or a claim of unfamiliarity with the corpus.

The scanner imports no investigation parser. It uses Python standard-library
byte, ZIP, gzip, CSV and hash operations. Prior experience with this author's
pin/EOF/create-only safeguards informed its design; no earlier scanner is
imported. The main privacy/record controls and worktree charter were read.
Evidence-audit, source-of-truth and development-verification safeguards keep
lexical observations separate from source-role and causal inferences. The
orchestrator intake was read-only; unrelated status/path output was suppressed.
No new root code or result was used to design or tune this producer.

| Artifact | SHA-256 |
| --- | --- |
| PROTOCOL.md | `dfc4ecbf348066574c6d38b5b087272120f006d35bfb72a1920ff79c14189865` |
| SCAN-CONVENTIONS.md | `06d9f8921be5dd2994dcca74c56ca5104b3aa88be85048a34c1b476ea82c85be` |
| independent_scan.py | `8c5aee84f2b4b96d4149cd8469902531a31f8d47c59cb2f4f7037657eddfe3ff` |
| independent-controls01.json | `3c1797ca32ae37c40361d08ffc3a6c9e9c8e673fa38c2fdf94f8faa0e385ae0a` |
| independent-scan01.json | `76a43ff38376979140608c5d368a93ae40bd7c9d55b33a3ec1e87069a6ce5bc7` |

## Coverage and result

The full scan returned PASS: 25,368 bodies, 513,121,900 bytes and 8,648,698
LF-based physical lines. These comprise three manifest-selected June APDL
files, all 25,362 non-PNG regular thermal-ZIP bodies and September SRC116,
SRC117 and SRC118. All nine family/encoding marker totals are zero, as are
their separate line-leading totals. This includes literal opportunities in
comments, strings and non-leading positions; no semantic comment stripping
or command execution narrowed the marker search.

The June ZIP has 25,639 entries: five directories, 272 excluded PNG bodies
and 25,362 scanned bodies. All 25,634 nondirectory entry identities/size pins
reconcile to the preserved manifest through the explicit archive-stem prefix
mapping. Every scanned ZIP body reached EOF and passed CRC, size and manifest
SHA256 checks. Excluded entries retain ordinals/name hashes and metadata;
their pixels/body CRC/SHA were not checked individually. The full ZIP's
86,819,483-byte container hash was checked before and after. No ZIP entry
was extracted to an embedded path, and no duplicate names were found.

The three APDL files and non-PNG bodies total 477,970,521 bytes. APDL complete
bytes/hashes and source-after checks match their manifest pins. September
streams match compressed-before/after pins and independently measured EOF
byte/line/hash values: SRC116 17,314 bytes / 1,921 lines; SRC117 325,983 /
45,156; SRC118 34,808,082 / 870,204. The additional reference audit is pinned
at `bef3e413bf02060782568e58bfab77bdb0e64b5ed59ba04dc0d6882c6d4f79f2`.
It supplies prior integrity expectations, not this new marker-search result.

One ZIP body contains 328 NUL bytes and no other bytes; it has one physical
line. Its zero-based ordinal is 15,108, alias `ZIP15108`, name hash
`0f9d4ff085098823cfa162a1195ed3e96b7d26e6fcac3c890717aa6568dc8478`.
Earlier one-based `ZIP15109` names the same member, not another source.
No scanned body contains bytes above127. The all-NUL body remains in literal
byte coverage and is not treated as a functioning source program.

The 53,274,959-byte receipt retains every body/exclusion alias, original
zero-based ZIP ordinal, filename/name hashes, available manifest row,
expected/measured byte and hash fields, ZIP CRC/metadata, physical line and
maximum-line counts, NUL/non-ASCII flags, initial BOM flags and all marker
counts/hits. No arbitrary source text, comment, heading or embedded path is
exported. Pin receipts use fixed aliases. No law or numeric curve is parsed.

## Detection and controls

The full body bytes are uppercased for three literal stems in each of ASCII,
UTF16LE and UTF16BE, at every byte alignment. Encoding patterns may overlap;
they remain separate opportunities, not evidence of an actual file encoding.
Locators use one-based LF physical lines, zero-based byte columns and
absolute offsets. Line lengths include their LF. The narrower leading flag
follows the prospective encoded whitespace/BOM rule, not general Unicode
parsing. A suffix means only a following encoded ASCII letter/digit/underscore.

Seventeen synthetic fixtures plus thirteen additional checks pass before the
historical scan and at its start. They cover mixed case, whitespace/BOM,
variants, comments/quotes/repetitions, both UTF16 orders, shifted overlapping
encoding matches, odd prefixes, NUL/non-ASCII, empty/no-final-LF inputs,
unrelated strings, exact locators, line/byte/hit caps, source-pin and output
refusal, duplicate ZIP names, ordinal-specific member opening and corrupt
CRC rejection. Full safe fixture bytes and outcomes are in the controls
receipt and source receipt; corrupt ZIP fixture input is preserved as hex.

One **pre-source synthetic expectation failure** is retained in
`independent-controls-failed01.json`, SHA
`719e04b7bb427dcace85986f17b0dba1ec52ddfa5105bafbb1dab948b12ba24b`.
The original tests incorrectly expected one hit in two UTF16LE fixtures;
the scanner correctly found overlapping shifted UTF16BE patterns under the
already declared any-alignment convention. Only those expectations changed,
with a specific overlap-locator check added; the scanning algorithm did not.
The exact failed version is preserved in
`independent_scan_before_control_expectation_fix.py`, SHA
`d3d36bf19c3d7994fb8c977605341f62db5e2cde0b1e86e90c291d8cd29d8d78`.
No historical body was opened during that failed control attempt.

Actual commands, with bundled Python3.12.14 and `-B`, from the dedicated
investigation worktree:

```text
independent_scan.py --controls-only --out independent-controls01.json
independent_scan.py --out independent-scan01.json
```

The source scan measured 6.807774 seconds and peak RSS301,563,904 bytes,
exited0, and left no live handle. Source/protocol/code pins agree before and
after. Bounds remain 30,000 ZIP entries, 4MiB/member, 512MiB total June input,
512MiB per September stream, 16KiB/physical line, 10,000 hits/body, 300seconds
and 768MiB measured RSS. Outputs are create-only; failures have sanitized
receipts. No scan was truncated or supported by an incomplete EOF result.

## Inference boundary and pending comparison

This negative result closes the declared literal-family search in these
bytes and encodings. It does not exclude generated keyword strings,
nonliteral APDL export logic, compressed subpayloads, other encodings/binary
representations, external inputs, restarts or a different historical package.
It supplies no curves602/803 and no source-to-run authentication. A number602
or803 in another namespace is not a substitute constitutive definition.

The next useful discriminator is an actual typed definition with complete
source/version/include/run provenance, or a separately declared investigation
of a specific accessible generator lead. No replacement law, stiffness,
capacity or failure history follows from this zero marker count. Prior
SRC119–121 results are separate pinned coverage, not rerun or counted as
additional historical corroboration here.

At this initial freeze, the new root code/results have not been read. A later
exhaustive common-field adapter and its receipt must be named explicitly
before claiming agreement between the new readers. The original independent
producer and result must remain unchanged.

## Post-freeze exhaustive comparison and report review

This appendendum supersedes the initial pending status, not its historical
freeze record. The preceding review was saved at SHA256
`796ec6cca2c61026ec2148d7990fee2fc983ba4b90123a07c892a3e7b4506683`
before inspecting the newly released root code/results. The independent
source code, controls, failure artifacts and source result remain unchanged.

After that freeze, this reviewer read the complete root source scanner and
saved-coverage verifier. The separately written `independent_compare.py`
adapts the two frozen output schemas; it does not rerun historical source
processing. Its imports of the two pinned scanners call only their byte
scanners on preserved synthetic fixture bytes. The adapter was frozen after
adding explicit root-result key coverage and reconstructing all independent
numeric summary fields; no source reader or result changed during that work.

| Completed artifact | SHA256 |
| --- | --- |
| independent_compare.py | `ea10f1aa8193779ba1badc2a691cac150deb55390fa1ccb5b79f99fce768ec74` |
| independent-comparison01.json | `d45d1adb5eba7a03f6bf6d0278fd1d94bbfbc5138100176cb3ae0633bce4aa1a` |
| Compared root source code | `3bdbefb2c324671293991070aa5991033a163f6ff13359ab1f276b115c72968a` |
| Compared root-01.json | `b85f806373294697eb1dc15b2673c5d8d34f81890658c0a76937fec9a55f9b06` |
| Compared root-02.json | `e5eea54090c3215534e6c5f4ae776680b673769353fa12240ba2699368f91a49` |
| Compared coverage-check01.json | `a71466540ea58ba15e0309ccb2ca7e1cdf1179fc34b153d8c15cf6b50ccd9d5a` |

The adapter returned PASS, exit0, with no live handle. It compared all25,645
records:25,368 scanned bodies and277 exclusions, with407,801 record-level
leaves and zero mismatches. It explicitly translates independent zero-based
ZIP ordinals into root one-based ordinals and normalizes alias padding;
both source aliases remain in each comparison record. The full ordered
record population, every common kind/ordinal/manifest-line/name-hash field,
declared byte/CRC metadata, retained CRC-success flag, body byte/hash/line/
NUL/non-ASCII/BOM/EOF fields, and complete marker locator/encoding/suffix/
leading records are compared. Excluded bodies do not acquire unperformed
body scans merely by matching their declared metadata.

All ten aggregate/pin checks pass, including reconstructed independent
family/leading counts and all other numeric summaries. The complete root
result repeat separately compares407,824 leaves and76,387 containers with
zero mismatches, including its interpretation-limit strings and source pins.
Root status, code, controls, Python version and command prefix also agree;
the two required output names and their run-specific elapsed/RSS values are
retained rather than falsely required to be identical. The independent
comparison took1.909118seconds and measured peakRSS347,471,872bytes with
bundled Python3.12.14; all frozen consumer/input pins agree before and after.

Because historical hits are all zero, the comparison also evaluates all17
preserved positive/negative synthetic byte fixtures through both scanners
and compares every common output field. Twenty-nine comparator mutation
controls reject altered identity/metadata/body/hit fields, missing/duplicate/
reordered records, omitted/reordered hits, and a false-versus-zero type
substitution. A create-only output-refusal control also passes. Complete
fixture bytes, mapped outputs and mutation comparisons are retained. These
controls address a zero-result blind spot; they do not prove arbitrary
language parsing or untested encodings correct.

Important implementation asymmetries remain disclosed:

- The independent reader records duplicate ZIP-name ordinal groups and opens
  each `ZipInfo`; root rejects duplicates. The actual pinned archive has none.
- The initial limit summary's4MiB/member ceiling applies to ZIP members.
  Independent APDL reads instead use the remaining512MiB June budget; root
  applies4MiB to each APDL file. All three actual files are below both limits.
- Independent-only LF/max-line/UTF16-BOM fields, calculated CRC numbers,
  compression metadata and extra manifest/expected-pin fields do not have
  root counterparts. Root's complete ZIP reads enforce CRC but retain only
  the declared CRC and successful EOF check.
- Root's original source scan pins September compressed files and checks
  gzip EOF, but does not itself enforce the prior uncompressed byte/line/
  hash tuples. Its separate saved-coverage check subsequently reconciles
  them; the independent source reader enforces those tuples itself. Neither
  later comparison turns the initial root implementation into that stronger
  predeclared guard retrospectively.
- Time and RSS safeguards are checkpoints, not OS-hard limits. Root's actual
  source runs used Python3.14.0 and the independent reader used3.12.14. Actual
  agreement across these runs is implementation corroboration, not a second
  historical source of evidence.

For a fresh saved-result comparison from the unit directory, use bundled
Python with `-B independent_compare.py --out independent-comparison-root01.json`
or another unused filename accepted by its fixed pattern. Outputs are
create-only. Changing the output name does not select new source receipts:
the adapter still reads the pinned independent-scan01, root01/root02 and
coverage-check01. A new producer receipt would require a separately declared
input/pin update. No failed comparison or producer output may be overwritten.

Finally, this reviewer read the full working report at SHA256
`f24e67a745a8f32f1dadbff506cc032e1c58dd01a5caa9709f46c42e72ce8ada`
and validation at
`4166831089c48b53dff47684283c461c6b44f08dde8c970225cc3db92a5fd291`.
No substantive source-coverage or inference overstatement was found in those
versions. Their pending-comparison wording and artifact links require the
ordinary closeout update now supported by this receipt; this is not a claim
to have reviewed later report revisions or an unexecuted root replay.
The distinction between scoped literal absence, unresolved typed LCD602/803
dependencies, historical execution and collapse cause is maintained. The
strongest alternative remains applicable definitions supplied by another
authenticated package, generation process or restart state. No cause-ranking,
intent, invalid-law or universal-absence conclusion follows from this pass.

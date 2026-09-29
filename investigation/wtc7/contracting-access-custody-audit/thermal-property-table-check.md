# Printed SFRM-property table crosswalk

2026-09-28. Working research only. Separately authored AI transcription and
finite arithmetic check, not licensed engineering review, native-model
reproduction, or independent experimental validation. Main AGENTS, WORKFLOW,
START-HERE and CHARTER WP3 control. This note implements only the prospectively
declared 33-pair comparison in
[the scope note](thermal-property-source-crosswalk-2026-09-28.md).

## Frozen findings

The 11 temperature keys match exactly: 25, 50, 100, 200, 300, 400, 500, 600,
800, 1000, and 1200 degrees C. All **33 literal numeric property pairs differ**.
For conductivity only, ordinary nearest-0.1 decimal half-up rounding of the
11 NCSTAR 1-6A DC/F values matches **all 11** TN1771 displayed values; there
are **zero halfway cases**. The specific-heat and density differences are
retained below, not erased by a fitted conversion or closeness threshold.

The 25 degrees C conductivity pair is 0.0460 versus 0.0 W/(m K), and the
defined rounding gives 0.0. This provides a concrete display-precision
explanation compatible with the printed zero. It does not establish which
unrounded value or zero, if either, was present in an executed native input.
Likewise, the differences in specific heat and density establish differences
between the printed tables, not their cause, numerical importance, or an
experimental failure. No fit, interpolation, unit-conversion-factor search,
graph measurement, model execution, or causal inference was performed.

## Source and inspection coverage

Complete page images and the matching held text derivatives were inspected:

| Source selection | Printed locator | Compared column/section | Units |
|---|---|---|---|
| NCSTAR 1-6A physical 120 | p68, Table 6-4 | BLAZE-SHIELD DC/F, measured thermal conductivity | W/(m K) |
| NCSTAR 1-6A physical 121 | p69, Table 6-5 | BLAZE-SHIELD DC/F, calculated specific heat capacity | J/(kg K) |
| NCSTAR 1-6A physical 126 | p74, Table 6-8 | BLAZE-SHIELD DC/F, calculated density | kg/m3 |
| TN1771 physical/printed 41 | Appendix A, 3. SFRM, A. Density | SFRM density | kg/m3 |
| TN1771 physical/printed 42 | Appendix A, SFRM B and C | Specific heat and thermal conductivity | J/(kg K); W/(m K) |

Footers, material headings and units were visually verified; units require
no conversion for this comparison. The page-41 upper conductivity table is
above the `3. SFRM` heading and was **not** mistaken for SFRM conductivity.
The page-42 lower table is the selected SFRM conductivity table.

All five images were opened with `view_image`, requesting `detail: original`.
The tool may still resize display images; this is legible full-page reading,
not a source-pixel measurement. Matching text was used as a secondary check,
not as a substitute for the page layouts. The 1-6A text has collapsed spacing
and OCR defects (for example, the 800 degrees C specific-heat row appears as
`soo`); the printed images control the transcription.

No other source pages or root/other-reader synthesis were read for this
comparison. The reviewer read the scope note while it contained only the
prospective scope, held-source/selection record, scope correction, and
declared comparison. Prior reviews of other sections of these sources and
the later thermal paper are disclosed; this is not a blinded or unseen
holdout review. The scope itself identified the candidate rounding issue.
The page-126 concluding paragraph continues onto the next page; this task
does not claim to have reviewed the complete subsection or full methods.

## All conductivity pairs and rounding checks

Difference means **TN1771 minus NCSTAR 1-6A**, in W/(m K). Both published
values are literal transcriptions; the rounded column is a declared derived
check, not a recovered author operation.

| Temperature C | 1-6A Table 6-4 DC/F | TN1771 p42 | Signed difference | 1-6A nearest 0.1 | Matches TN display |
|---:|---:|---:|---:|---:|---|
| 25 | 0.0460 | 0.0 | -0.0460 | 0.0 | yes |
| 50 | 0.0687 | 0.1 | +0.0313 | 0.1 | yes |
| 100 | 0.0628 | 0.1 | +0.0372 | 0.1 | yes |
| 200 | 0.0810 | 0.1 | +0.0190 | 0.1 | yes |
| 300 | 0.1106 | 0.1 | -0.0106 | 0.1 | yes |
| 400 | 0.1286 | 0.1 | -0.0286 | 0.1 | yes |
| 500 | 0.1651 | 0.2 | +0.0349 | 0.2 | yes |
| 600 | 0.2142 | 0.2 | -0.0142 | 0.2 | yes |
| 800 | 0.3380 | 0.3 | -0.0380 | 0.3 | yes |
| 1000 | 0.5010 | 0.5 | -0.0010 | 0.5 | yes |
| 1200 | 0.5329 | 0.5 | -0.0329 | 0.5 | yes |

## All specific-heat pairs

Difference means TN1771 minus NCSTAR 1-6A, in J/(kg K). No additional rounding
test or adjustment was applied.

| Temperature C | 1-6A Table 6-5 DC/F | TN1771 p42 | Signed difference |
|---:|---:|---:|---:|
| 25 | 826.4 | 826.9 | +0.5 |
| 50 | 941.5 | 942.0 | +0.5 |
| 100 | 723.9 | 724.3 | +0.4 |
| 200 | 897.2 | 897.6 | +0.4 |
| 300 | 1020.2 | 1020.7 | +0.5 |
| 400 | 1070.6 | 1071.4 | +0.8 |
| 500 | 1097.6 | 1098.2 | +0.6 |
| 600 | 1189.7 | 1190.3 | +0.6 |
| 800 | 1258.6 | 1259.4 | +0.8 |
| 1000 | 1325.3 | 1326.0 | +0.7 |
| 1200 | 1391.7 | 1392.5 | +0.8 |

## All density pairs

Difference means TN1771 minus NCSTAR 1-6A, in kg/m3. No additional rounding
test or adjustment was applied.

| Temperature C | 1-6A Table 6-8 DC/F | TN1771 p41 | Signed difference |
|---:|---:|---:|---:|
| 25 | 236.8 | 237.0 | +0.2 |
| 50 | 236.1 | 236.3 | +0.2 |
| 100 | 230.1 | 230.3 | +0.2 |
| 200 | 224.6 | 224.8 | +0.2 |
| 300 | 222.1 | 222.3 | +0.2 |
| 400 | 220.3 | 220.5 | +0.2 |
| 500 | 219.0 | 219.2 | +0.2 |
| 600 | 218.2 | 218.4 | +0.2 |
| 800 | 361.1 | 361.4 | +0.3 |
| 1000 | 375.8 | 376.1 | +0.3 |
| 1200 | 432.1 | 432.4 | +0.3 |

## Actual commands, computation and results

Only the authorized note is written. No source, renderer, saved JSON, model
implementation or other note is modified. Full paths were used for image and
text reading; paths below are relative to this audit directory.

1. `view_image` successfully opened the five complete PNGs named in the hash
   table below. All were visually read, including table headings and footers.
2. `sed -n '1,220p'` was run separately on each matching `.txt` path below.
   All five calls returned complete selected-page text and terminal exit 0.
3. All source and TN1771 values were manually entered as decimal strings
   after image inspection. Temperature arrays were checked for exact equality
   and each property's source/target array was checked to contain 11 entries.
   A transient JavaScript tool calculation used scaled integer (`BigInt`)
   subtraction: four decimal places for conductivity and one for specific
   heat/density. This avoids binary floating-point display residue. For
   conductivity, with `K` the 1-6A value in units of 0.0001 W/(m K),
   `(K + 500n) / 1000n` using nonnegative BigInt division gives the rounded
   number of tenths. The halfway check was `K % 1000n === 500n`; no row met it.
   No executable code file or separate numerical-output artifact was created;
   this note records the result.
4. Actual tool result: `pairs_checked: 33`, `literal_numeric_matches: 0`,
   `nonzero_differences: 33`, `k_rounding_checks: 11`,
   `k_rounding_matches: 11`, `k_halfway_cases: 0`. All 33 signed differences
   were emitted to the task output before this note was written and are
   reproduced above. A result summary was then sent to root before reading
   any synthesis.
5. `shasum -a 256` was run in this audit directory on both preserved PDFs
   and all ten selected PNG/text derivatives in one call; terminal exit 0.
   All returned hashes are below. Both source PDF pins match the declared
   held sources. This checks bytes, not historical authenticity or a new
   reproduction of the existing renderer.
6. `test ! -e` on this note's absolute path returned terminal exit 0 before
   creation. The note was then created with `apply_patch`, preserving existing
   sources, derivatives, independent reviews, and protected state.
7. A complete `sed -n '1,280p'` readback of this note returned exit 0. Its 33
   numeric table rows were parsed and compared to the frozen transcription,
   signed differences and conductivity-rounding results: all matched. The
   targeted `git status --short` check showed this note as a new untracked
   file; it was not staged or committed.

## Fresh SHA-256 pins

| Artifact | SHA-256 |
|---|---|
| [NCSTAR 1-6A source](ncstar-1-6a-source01.pdf) | `75b910620ee9c9f202256acd898f01f28a0df23546132c2108a2a1735cb021b3` |
| [TN1771 source](nist-tn1771-source01.pdf) | `c94d92defa00689c906f54a7075e4887a1bdd86731688b34d98200ec29fc94e3` |
| `thermal-property-render01/6a-page-120.png` | `b09dc049db5ef6d173f1cf19154f991e9acc89de73797185f8878269e6a4ba16` |
| `thermal-property-render01/6a-page-121.png` | `3f6210b428bdf252a1bfd081ae5a9b79ca3d62da69412277399d70d3f37779fe` |
| `thermal-property-render01/6a-page-126.png` | `589d0a4c0a1c0aebe512cde7453c2335a29b23135c308af1da3c5f073eaadda1` |
| `tn1771-render01/tn1771-page-041.png` | `88f65db73b4c8e3430d6abed25a3e06705b086a3dbe599bddf9bf9b959c2be0b` |
| `tn1771-render01/tn1771-page-042.png` | `669ba723a9616755d627d3246b50bbf4eab707f414c084a102e7b542c48ae094` |
| `thermal-property-render01/6a-page-120.txt` | `0827ed0e0f47290d3adb8507043580294b9db4308a73b657db66d1b09821829d` |
| `thermal-property-render01/6a-page-121.txt` | `bed5595ef01eaef3fbc5b13bd743f367249e1af77a35e76309e7658051d06377` |
| `thermal-property-render01/6a-page-126.txt` | `1bda85dc90a7f8d27f4b84c08151f1bb759538eadf474f4203de30a271ae8b3d` |
| `tn1771-render01/tn1771-page-041.txt` | `82f93fef4a6ba4caf9f743ea5a2389e4a705a8f75692ae17fe570067b1cf04b0` |
| `tn1771-render01/tn1771-page-042.txt` | `dd217b3902f35db6cb897bdfe36f116789d3f238651734dde7dcd0272df10916` |

## Claim ledger and remaining boundary

| Claim | Type and strength | Support and limits | What could change it |
|---|---|---|---|
| The printed temperature keys agree and all 33 literal property pairs differ | Observed/transcribed plus derived subtraction; A for this bounded published-table proposition | Five complete page images, all pairs and differences preserved above; not an experiment | A source-pin error, image misreading, or arithmetic discrepancy on recheck |
| All 11 printed TN1771 conductivity values equal the declared one-decimal rounding of the DC/F values | Derived; A for this finite rounding result | Exact decimal arithmetic; the strongest limit is that identical displayed rounding need not identify native values or the authors' actual rounding operation | Any row failing the fixed rounding rule or a transcription correction |
| These tables establish identical executed native property inputs or independent experimental validation | Not established; D/underdetermined | No native input/run/output identity or independent experimental reproduction examined; 33 pairs are not 33 independent experiments | Source-pinned executed material tables, input-version/run mapping, and appropriate separate validation evidence |

The 1-6A labels and page-69 method description distinguish measured conductivity
from calculated specific heat; the latter is an indirect result with an
express limitation concerning chemical-reaction heat-capacity peaks. Page 74
labels the density table calculated and notes sample/application dependence
for conductivity and bulk density. A close or rounded printed-table match
does not remove those method, specimen or domain limits. The causes of the
specific-heat/density table differences remain unassigned in this arithmetic
check. No source-authority promotion, physical-validity finding, misconduct
attribution, or historical-cause ranking is made.

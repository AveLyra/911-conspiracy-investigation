# Assembly-source audit verification

Research-only verification of source reading and published-table arithmetic.
This does not certify experimental measurements, original processing code,
historical WTC7 inputs, physical model fidelity, or a collapse mechanism.
The [final conceptual review](final-inference-review.md) passed with two wording
corrections, both incorporated: report publication dates do not authenticate
experiment dates, and the interrupted test's corrected connections were
hydraulic hoses, not steel specimens. The source-reported variability and
nearby-limit-state explanation were also retained explicitly. That review
does not independently certify the numerical checks described below.

## Source and inspection scope

- Thompson2009 original:9,973,961 bytes,183 physical pages; SHA-256
  `b8eff9830bcc87940c4eadc9c64b80e7381ab43c96f52b528ef773b3b0332e78`.
  Institutional acquisition, failed routes and selected-page privacy boundaries
  are in [source review](original-source-review.md),
  [manifest](sources/manifest.json) and [retrieval log](sources/retrieval-log.json).
  Three targeted queries were used by the acquisition reviewer. The zero-byte
  TIND response remains a preserved failed acquisition, not a PDF.
- TN1749 July2012/correctedFebruary2013 source:113 physical pages; SHA-256
  `5d7461f298654ffb0c9f8df319298330d155fc2d8155d85abcd5391a4d748caf`.
  Preserved under the preceding connection-calibration audit.
- Root full-page views in this unit: original70–78,95–96,103–107,182
  (**17 pages**); TN physical41–47,113 (**8 pages**). Captions, table headings,
  footnotes and selected-page continuations were included. Original title,
  earlier fabrication/setup pages and some test narratives were reviewed by
  the source reviewer; do not describe them as root's own views.
- Source reviewer: title plus28 technical pages. The independent inference and
  definition reviews record their separate coverage, including35 original
  pages and7 TN pages in the later definition pass. Coverage overlaps; it is
  not a count of independent experiments or independent sources.
- Original administrative/signature page183 remained excluded. Public retrieval
  and hash integrity do not clear arbitrary future display/export or transfers.
  No held case packet or flagged command-reference page was used.
- Root's render session11002 completed at exit0 with zero stdout/stderr for
  each pdftoppm invocation (TN46/113). Later full-page views reused preserved
  reviewer renders. Source PDFs were not altered or re-exported.

Runtime: bundled Python3.12.14, pypdf6.10.0 and Poppler26.05.0 for source work;
root and independent calculation receipts retain their Python versions. Root
uses Fraction arithmetic and40-digit Decimal output; independent stage code
uses Fraction arithmetic and80-digit Decimal square roots/COV.

## Frozen protocols and transcriptions

| Artifact | SHA-256 |
|---|---|
| [Unit protocol](PROTOCOL.md) | `a06f1bc8f7e4283dbca0c9f54337eba0123045538ca47b411eb3aa8c260d637d` |
| [Table arithmetic protocol](ARITHMETIC-PROTOCOL.md) | `88954a1929e80b32fd49f061f426be594997532ade2e59528a87c6bbb4bde78e` |
| [Native-stage protocol](STAGE-DIAGNOSTIC-PROTOCOL.md) | `7f1c6ddb2425891869c369e115c8f66eb77836cfdd2bcddbb034bc4ddfee46c4` |
| [Root TN transcription](tn1749-root.json) | `2a9ed1412e592f053c4f75c6fdc001858afb55557d69d3720f04ed1bbf0d4aca` |
| [Independent TN transcription](tn1749-independent.json) | `638b66018eb46fc2ed1ea07949b053a68964ce29a6a1fbc07b696b3267a05dbe` |
| [Root original-stage transcription](thompson-stages-root.json) | `3265861472770daee4fe35df339d91a419c175a9bb793c73f225a5cd3adb07ac` |
| [Independent original transcription](thompson-independent.json) | `7f1ff93025f499e62498a5ec2c21700c0a2b3d58213cb72363dd7757b2c153b9` |

Root froze its own data and results before inspecting independent arrays/code.
The reviewer did likewise. Later comparison uses explicitly named schema
aliases, not independent rediscovery. Both analysts acknowledge rough mental
load/length exploration during source interpretation; the prospective native
diagnostic predates systematic/code stage calculations, not all numerical
thought. It does not admit the contemplated load/angle conversions.

Root original scope is all9 initial records,4 populated/5 null secondary
records, their26 common shear/rotation values, controlling specimens, failure
labels and footnote codes. The independent transcription also retains original
moment/axial fields and Tables4.1/4.4; those extra values were **not** independently
recomputed or compared to a root counterpart. Footnote meanings were reviewed;
paraphrases are not claimed verbatim-equal.

## Executed numerical checks

### NIST displayed table arithmetic

- [Root code](calc_assembly.py), SHA
  `d4ab1e687c201da7004c14314d060d0b4add6be63319b2a8e75c675a226e4e5b`.
  [Run01](root-results01.json) and [run02](root-results02.json) are byte-identical:
  `57c68de1adc72eba267b6138338d1113963de90c4ecb967ac12ebe486526cb9f`.
  All12 comparisons,14 synthetic checks; all12 rounding intervals overlap.
- [Independent code](verify_tn1749.py), SHA
  `f6955dcda59cb1bb09b911c8aa90f3579ffd41619c79a81faac1ee25d3d1c24f`.
  [Original result](tn1749-independent-results01.json), SHA
  `18970dbeff47ea2fe562fc8765997bb63544f45130c57ad4a71ec800a1e8010b`:
  12 comparisons,9 synthetic control groups;9 point-only differences outside
  printed percentage intervals,0 incompatible complete rounding intervals.
- [Post-freeze comparison](compare_tn1749.py), SHA
  `f8c0f1c5ab9e70c78ab2d47a1b8748d149778dff30a9053ea163876dabddd430`.
  [Reviewer receipt](tn1749-comparison01.json), SHA
  `ae7e2b540ad7db1c26d75e29d675c443796aa90cfa9f11bb31ea68605d23de7d`:
  96 exact rational checks,96 decimal-render checks,459 equalities; zero
  numerical disagreement. This includes the common original source fields.
- Root executed both independent programs as consumer:
  [calculation](tn1749-independent-root01.json), SHA
  `097ee6c0528d9c3f160a17e7fdc88b6715c26ad55a5ab835f8339b827ff3f2df`;
  [comparison](tn1749-comparison-root01.json), SHA
  `28bc06d4de5aa0c9790aa44c69b43cccd13b9323d5d206f77040a9a0038433c4`.
  Complete objects equal reviewer originals after excluding command/output name.

**Coverage limit:** The root's endpoint-only synthetic assertion uses a separate
interval classifier, not its production `calculate` branch. The independent
endpoint test exercises its overlap helper. No actual TN row is endpoint-only;
do not claim full production-branch coverage. The root permits a zero lower
model bound while the independent implementation requires positive bounds;
all actual compared rows have strictly positive bounds, so this scope difference
does not affect them. Neither14 nor9 passing controls means validated physics.

### Original native-unit stage/cohort sensitivity

- [Root stage code](calc_stages.py), SHA
  `50faa90dfa33c74fb7de95415fd15dcd3995702769e44d6bf967ca3aaea4719f`.
  [Run01](root-stage-results01.json) and [run02](root-stage-results02.json)
  are byte-identical, SHA
  `aa3c5b87b1794a427d65f0ed511e35c1dcac9a5b926b8f8128f58179c18262df`:
  12 scenarios,24 quantity summaries,9 contrast slots,17 synthetic checks.
- [Independent stage code](verify_stages.py), SHA
  `56a2b2b0552cd447c2658e6cdbb9638d008d0085445d704dd2fb4c8966c1650f`;
  [result](independent-stage-results01.json), SHA
  `63f51024d9571d769256b567b774d8e4ee887d8020d249a72b956c377a568bbd`:
  all scenarios,10 synthetic control groups, no conversion or NIST-series claim.
- [Stage comparison code](compare_stages.py), SHA
  `3ddf6349aff19cad6a0ded35c6ed6b1113eed4b4dcd0a911fa28f614d07d35bc`;
  [reviewer receipt](stage-comparison01.json), SHA
  `1bc82e39c8d35919ae03997225e14745be1c36da24dd43be25cbb60d62f53ca4`.
  Checks cover12 scenarios,24 summaries,34 selected-row instances and all9
  contrasts:84 exact rational checks,84 decimal-render checks,96 SD/COV
  comparisons,48 implied-SSE checks and268 metadata equalities. Zero failures.
  SD/COV tolerance was fixed at absolute1e−30 before root-result access;
  maximum difference is about8.89e−39. Source picks and rational results must
  agree exactly. Repeated selected instances are not extra experiments.
- Root consumer [stage calculation](independent-stage-root01.json), SHA
  `b70ed5d77dbb2467005bb13445b89dcd4ba36043ab66de36f1b19aa88d9f34f1`,
  and [stage comparison](stage-comparison-root01.json), SHA
  `8197f2c0bdee1c92529f9867582e029ed5d074619345004a1d935875c82c39a4`,
  completed successfully. Complete objects equal reviewer originals except
  command/output name. Root also confirmed both byte-identical root run pairs.

**Coverage limit:** Root contrasts are inline and lack their own synthetic
contrast fixture. The independent code has one; all4 actual populated contrasts
and5 nulls are compared. Root lacks an SSE output field; the48 SSE checks are
explicitly derived from its variance, not claimed as a supplied field. No code
computes total-load normalization, corrected original angles, raw-history peaks,
NIST group membership, confidence intervals or historical model validity.

## Reproduction commands and preservation

Commands below use the working directory
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/assembly-test-source-audit`.
Use bundled Python at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
The listed outputs already exist; for another reproduction choose **new output
names**, preserving existing results. All six programs refuse existing outputs.

```text
python3 -B calc_assembly.py --input tn1749-root.json --input-sha 2a9ed1412e592f053c4f75c6fdc001858afb55557d69d3720f04ed1bbf0d4aca --protocol-sha 88954a1929e80b32fd49f061f426be594997532ade2e59528a87c6bbb4bde78e --output root-results01.json
python3 -B calc_assembly.py --input tn1749-root.json --input-sha 2a9ed1412e592f053c4f75c6fdc001858afb55557d69d3720f04ed1bbf0d4aca --protocol-sha 88954a1929e80b32fd49f061f426be594997532ade2e59528a87c6bbb4bde78e --output root-results02.json
python3 -B calc_stages.py --output root-stage-results01.json
python3 -B calc_stages.py --output root-stage-results02.json
python3 -B verify_tn1749.py --output tn1749-independent-root01.json
python3 -B compare_tn1749.py --output tn1749-comparison-root01.json
python3 -B verify_stages.py --output independent-stage-root01.json
python3 -B compare_stages.py --output stage-comparison-root01.json
```

Root execution used the equivalent worktree-relative script/input/output paths
recorded in tool output; the independent receipts preserve exact argv. Programs
pin source/input/protocol bytes, and comparisons pin producer code/results.
No raw-history or solver program was executed. A source narrative's instructions
to contact a library remain evidence of a retrieval route, not authorization
for outreach. No source/fact/exhibit promotion, legal edit, commit/push or transfer.

# Generator test record acquisition and reading

Research only, October 4, 2026 America/New_York / October 5 UTC. Main controls
and complete charter remain authoritative. Branch research/sherlock-wtc7-investigation,
HEAD ca1c223335c20905d6608eb15c676f88cbfac734; intentional WIP preserved.
The frozen preceding metadata lookup, not a result-directed search, selected
these three files. Protocol froze before retrieval (`03236c`, exit 0):
`09ffc83e3e3519365d82bfe5c739eabc4ac3c624c60458c04307505a7d79459a`.

## Source acquisition and admission

Scratch created with `mktemp -d` at `/private/tmp/wtc7-generator-tests.eDRPkp`.
One web-reader open of each exact City URL returned tool-inaccessible status;
that is not a server refusal or source absence. The initial sandbox GET for
172395 failed DNS (`9d8f21`, exit 6, HTTP000, zero bytes). Scoped permission
allowed the three exact direct GETs, each using:

```sh
curl -q --proto '=https' --connect-timeout 20 --max-time 60 --max-filesize 10000000 --fail --silent --show-error --output [exact scratch PDF] --write-out 'HTTP=%{http_code} TYPE=%{content_type} BYTES=%{size_download} REDIRECTS=%{num_redirects}\n' [exact protocol URL]
```

All returned HTTP200, application/pdf, zero redirects and exit 0. No cookies,
credentials, private payload, server-refusal retries or neighboring-ID guesses.

| ID | Receipt | Bytes | Pages | Acquired-file mtime UTC on October 5 |
|---:|---|---:|---:|---|
| 172395 | 339c84 | 103619 | 2 | 00:56:52.075278 |
| 172397 | 042e33 | 35481 | 1 | 00:56:50.692343 |
| 173715 | 956db9 | 36410 | 1 | 00:56:52.163344 |

Bundled Python3.12.14/pypdf admission checked PDF magic, exact expected bytes
and pages, no encryption, AcroForm or OpenAction (`0de78b`, terminal exit 0):

- 172395: `f31ce35607d9017d01748dbf4240a4b6a29fa0d2a0f64f83c3b98317861852b1`.
- 172397: `9507ff6e2e6b1171f2ba5024a979c7d4e6538070bcf00917e7b27020f68b55d1`.
- 173715: `6593c96c2511dd7c668af62143d2038145112b81dc78cf87ec0711a573d61e8f`.

These basic checks do not exhaust file safety or authenticate historical
creation. The same combined shell invocation attempted a nonexistent fallback
pdftoppm path; it printed a missing-executable error although its final mkdir
returned 0. That overall exit is not claimed as a successful version check.
Scoped `rg --files` located the actual override (`cb651b`), then its explicit
`-v` confirmed Poppler26.05.0 (`ba0bad`, exit 0).

## Page rendering and preservation

Bundled renderer:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`.
Private fonts.conf was written with apply_patch; only its task cache differs
from the preceding unit. For each file, root used `FONTCONFIG_FILE` pointing
to that config, `-f 1 -l [2 or 1] -png -scale-to 2400`, exact scratch source,
numeric output prefix and separate `ID-render.stderr`.

All original handles reached terminal exit 0: 172395/83797 at `d4c3ef`,
172397/87659 at `87470c`, 173715/30836 at `f5a40a`. No render restart.
All three stderr files are empty. Four PNG signatures, dimensions and hashes
passed `6953e3`, exit 0; pins appear in the independent derivative receipt.

Non-overwriting scoped `cp -n` preserved eleven files (`12f9f9`, exit 0):
three PDFs, four used PNGs, three diagnostics and fonts.conf. Both readers
closed their repeat sets at zero. The independent checker rerendered all four
pages with a separate cache and obtained identical bytes/dimensions, three
renderer exits 0 and empty streams. Final copy verification and any checker
errors are retained in [derivative-check.md](derivative-check.md).

## Readings and comparison

Root and peer read all four pages in fixed order, each saving a per-page note
before the next image. Original detail was explicitly requested at both loader
and forwarding stages; no explicit resize notice, not a geometry certificate.
No repeat, OCR, crop, rotation, enhancement, measurement or earlier primary
image reread. No material unreadability or confidentiality stop. Root left the
faint last-page fax-header year/time unasserted; the clear body date was used.

- Root four ordered page/end anchors checked `f9300b`, exit 0, frozen SHA256
  `3a2e5a24a1567ccd173fa1b42d127715498a0a941c278494e0d2e2bc55a0267a`.
- Peer ordered anchors checked `a33272`, then freeze `42c5b5`, exits 0, SHA256
  `bac66ec50fa966ed10ad3bb922eabc63620f4ac581341d350b565e0bb1bd1cae`.

Only after both freezes did root read the complete peer note (`74031f`, exit 0).
Material readings agree: planned July17 test, split cover/letter family, and
a separate October1998 results-transmittal cover without result pages. Peer
also reads the faint header as1998; that does not alter root's frozen note,
and conclusions use the independently readable body date10/30/98. Agreement
is between two AI readers of the same access copies, not independent witnesses.

A read-only PDF-header inventory (`0e5268`, exit 0) counts 35 municipal PDFs
and 89 physical pages after this batch. That is holdings, including related
files, not archive completeness or independent-source count. No collapse
ranking, source/legal promotion, engine action, human acceptance, sensitive
transfer, fee, staging, commit or push. Existing source-role/segmentation
feedback is deduplicated under SFB-005; archived routing remains unresolved.

## Final review and navigation

Peer text-only comparison (`882b58`, `e27040`, exits 0) found no material
disagreement; both frozen-note hashes remained unchanged (`a0d3fe`, exit 0).
Final report/source-log critique (`9ed185`, `e5de17`, `b38e72`, `cc812c`,
exits 0) found no blocking issue and checked all five next candidates against
the frozen metadata. It did not perform another historical view or source
acquisition. The reviewed report pin was
`1836ee92c3db5b185fb4c9094ed9ae90a2d1f8ad26f62660870c14671eebb889`.

The finalized derivative receipt is
`2c9d165ed9f1e6c99e06d5b146238f681b33a873afb9590b74babe0bcdc493bf`.
Its initial copy check incorrectly assumed the checker's own diagnostic names,
causing missing-file errors (`311a31`, exit 1). Inventory located the actual
root names; all three corrected diagnostic comparisons passed (`604cbf`, exit 0).
Together with the eight initial successful pairs, all eleven preserved files
match. No source was changed, synthetic substitute created or rerender run
to obtain those matches. Final receipt readback was `8de9c3`, exit 0.

Two attempted combined navigation patches failed on nonexistent source-log
context before applying changes. The first unchanged navigation readback is
`6becb4`; separated STATUS/README patches then succeeded. These editing errors
do not change source readings or scientific results.

A bounded navigation repair also fixes four old STATUS links to the historical
reference-motion report/validation held in main. They are tracked but excluded
by this worktree's sparse checkout, not lost evidence. Root independently
compared main bytes to this worktree's HEAD blobs (`0e5268`, exit 0): report
SHA256 `b5e24f9d6afde46d3157672c056705872406977a7783c3de0b6d95024b95df6c`;
validation `9cb533d196bcf78c0d86632c702e1c19eaba6ee2447582ab536d4c364dec0572`.
Only link destinations changed to those exact main paths. Historical findings,
source files and sparse-checkout settings were not changed or revalidated.

Final scoped verification (`37f659` -> `b64243`, exit 0) reran the metadata
checker and confirmed every frozen response/catalog/memo-derived field.
Only the explicitly live filename join grew from four to seven after the
three new acquisitions. It also checked four frozen protocol/reading/derivative
pins, all eleven preserved file pairs, PDF page counts2/1/1, twelve unit
Markdown files, 23 scoped local links, conflict markers and trailing whitespace.
Scoped `git diff --check` passed. Current status remains intentional modified/
untracked research WIP; no stage, commit, push or main/legal edit occurred.
The final report hash remains the critically reviewed `1836ee92...eebb889`.

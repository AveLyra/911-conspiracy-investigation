# Independent Windsor source and rendering integrity review

2026-09-20 UTC. Reviewer: `next_discriminator`. Research-only integrity work
under the main controls and full charter. PDF, source-preservation,
evidence-falsification and development-verification safeguards apply. I read
PROTOCOL.md, the historical rendering/validation records, the launcher chain,
font configuration and central validation receipt. No scientific source
findings or root/observer substantive notes were read. No network, installation,
source repair, solver or source/canonical mutation occurred.

## Result and scope chronology

**Pass:** the source and all 13 historical page images match the central
comparator receipt. One fresh Poppler rendering of physical pages1–13 at
100dpi completed with exit0 and **zero stdout/stderr bytes**. Every fresh PNG
matches the corresponding held PNG byte-for-byte and in fully decoded RGB
pixels. All 23 pinned inputs remained unchanged across the run.

The original task selected pages10–13. Before any reproduction command,
root declared SCOPE-EXPANSION.md and explicitly authorized the same-source
13-page replay. I read that amendment before rendering. There was no earlier
four-page reproduction pass to preserve or supersede; only source/receipt
location and configuration preflight had occurred. This is one 13-page run,
not a four-page run retrospectively relabeled as complete coverage.

The documented font configuration names a cache inside main. To keep main
read-only, root explicitly approved a temp-local configuration with the same
font directories and DTD, changing only cachedir. Thus **runtime configuration
was not literally identical** to the historical one, although all 13 output
files reproduce exactly. The source-preservation safeguard caused this narrow
cache relocation; no broader environment repair was made.

## Inputs, source admission and preservation

Held source:

`/Users/admin/docs/911/research/sherlock-wtc7-investigation/comparator-expansion/windsor/sources/fletcher-santander-2007-draft.pdf`

Exactly **195,207 bytes**, SHA-256
`30de182736b632772a9d42b6178eea234ab60c54d7c8bd715bcccb72c637e007`.
It matches the source row in the central comparator validation-receipt.json,
including its 13-page count. A read-only MuPDF opening confirmed PDF format,
13 pages, no repair/encryption/open warnings. No source page text or image
was interpreted in that check; it does not authenticate the historical source.

All 13 original `windsor/rendered/fletcher-NN.png` identities were compared
with the corresponding central receipt rows. The source and page checks
passed before rendering. Original selected-page hashes include:

| Physical page | Preserved PNG SHA-256 |
|---|---|
|10|`799ba21f922266a219039caea7bd397aa155fd7e2ee57221d2113a3c3e071899`|
|11|`b60a548ce46dfe6a0d9174cffa63657227efda6dfaba63388bebd6bbfc5bbcd9`|
|12|`ce9152857ccc88454ec6c0303a686bc2f0eee21ff668d9a50e4046d8cd2b62e5`|
|13|`2176ad6468725584f58e779f8e67329b8d0110a2a6e8c01b0b0836232796cfbf`|

The complete 13-page original/fresh path and hash crosswalk is in the saved
temporary comparison receipt. No original image or PDF was replaced.

Control/provenance pins freshly checked before and after:

| Input | Bytes | SHA-256 |
|---|---:|---|
| Current PROTOCOL.md |4450|`d02efad11d2008aa65536547510d78110daae974693d4291d6c07c359573db05`|
| SCOPE-EXPANSION.md |1425|`063d4c02ca135382ebab6c71ce3b005f29ba946acd5f16f59d2d7b85bae6f147`|
| Central validation-receipt.json |12133|`022d706460953f551eee7ef8e4634dd56bf074a3b144c13a9550051c352fa0f9`|
| Historical fonts.conf |285|`a7cc869f858fdfbf20beb37ab29611fb6e1d27131f90cf07657c46f62d2868cb`|
| Temp-local fonts.conf |240|`710852d28347dcd565eb8c3cf2e907db09b94b502d5d53bae6b2375172981eb3`|

Historical configuration path is
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-coverage-extension/fonts.conf`.
The new file was authored with apply_patch and checked byte-for-byte against
the original after replacing only its cachedir string. Both retain
`/System/Library/Fonts`, `/Library/Fonts` and the same fontconfig DTD. The new
cachedir is `/private/tmp/windsor-integrity.wyiFjb/font-cache`. The main cache
was not configured as a write destination. Font-file and all loaded-library
binary identities were not comprehensively attested.

## Actual execution and runtime

Fresh dependency discovery reported bundle **26.905.11957**. The historical
command's override launcher is present and was read in full. It invokes the
native/poppler/bin wrapper, which prepends the bundle's library directory and
executes the actual native/poppler/poppler/bin/pdftoppm binary. All three were
pinned, not conflated with one executable:

| Runtime component | Bytes | SHA-256 |
|---|---:|---|
| dependencies/bin/override/pdftoppm |157|`de772e88ab9977ccde25def9b403bf42675d75f5dd82b19fbd7d8123ad183159`|
| dependencies/native/poppler/bin/pdftoppm |310|`d9d81b176e8fd38d07f2fbf4f84c17dc991c6bac3730ff3cad3239c4fcbed892`|
| dependencies/native/poppler/poppler/bin/pdftoppm |75280|`98ac4fedc4258b7125ad1048034c1448dccc58503614eb105f19d12cdb3a2d0d`|
| Explicit Python3.13.7 executable |33816|`7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e`|

All dependency paths above are relative to
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/`.
The Python path is `/Users/admin/.pyenv/versions/3.13.7/bin/python3`.
Pillow12.0.0 performed independent PNG parsing/full pixel decoding.

`mktemp -d /private/tmp/windsor-integrity.XXXXXX` created
`/private/tmp/windsor-integrity.wyiFjb`. An inline read-only/source verifier
and bounded subprocess launcher ran with
`PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B -`.
It first called the exact override launcher with `-v` (10-second limit):
exit0, empty stdout, and a 144-byte version/copyright stderr identifying
**Poppler26.05.0**. That expected version output is not a rendering warning.

The exact rendering command, run once with a 60-second limit, was:

```sh
FONTCONFIG_FILE=/private/tmp/windsor-integrity.wyiFjb/fonts.conf \
FONTCONFIG_PATH=/private/tmp/windsor-integrity.wyiFjb \
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm \
  -f 1 -l 13 -r 100 -png \
  /Users/admin/docs/911/research/sherlock-wtc7-investigation/comparator-expansion/windsor/sources/fletcher-santander-2007-draft.pdf \
  /private/tmp/windsor-integrity.wyiFjb/fletcher
```

Session **31536** reached terminal **exit0**. The render returned0 with empty
stdout and stderr, preserved as separate zero-byte logs. No retry, repair,
timeout or failure occurred in this task. Earlier comparator and unrelated
renderer failures are not erased or redescribed by this successful invocation.

## Comparison method and retained outputs

The inline verifier independently constructed page membership1–13 from the
amendment. It required exactly one matching original receipt row for every
page and exactly 13 fresh PNG names after rendering. It opened every original
and fresh PNG with Pillow, required PNG format and one image, called verify(),
then reopened and fully loaded each pair before comparing dimensions, mode
and pixel bytes. It separately compared complete file bytes and hashes.

All **13 pairs** are byte-identical and pixel-identical. Every image is RGB,
**827-by-1170 pixels**. The physical-page ordering is tied to explicit `-f 1
-l 13` and the numbered output mapping, not inferred from scientific content.
No printed-page labels or equation correctness were validated here.

The 23 before/after input pins cover the source, central receipt, protocol,
amendment, two font configurations, three Poppler chain components, Python
and all 13 original images. Every size/hash is unchanged. All generated
records use exclusive creation and remain in the fresh temp directory:

- `start.json`: 5,975 bytes, SHA-256
  `bb0e8192b1ca627a78366beca683c4b6164ea67cf6e6810409e09541ba9ce17b`.
- `command.json`: 948 bytes, SHA-256
  `8244c5bd4ea74b971b3ddd1adbec33cb424e9fdffbda7d534eb3bcecb5413252`.
- `comparison.json`: 19,879 bytes, SHA-256
  `2973c3f3e16673e5b30252ad086bb254dbe07313e6c23d6934341f1f12767d3f`.
- Version/render stdout and stderr, temp fonts.conf/cache, and13fresh PNGs
  remain preserved. No cleanup was performed. Temp storage is not a durable
  evidence-backup guarantee; decisive pins/results also remain in this note.

## Limits

This is a same-Poppler-version reproducibility check plus separate Pillow
decoding, with an explicitly relocated font cache. Stable bytes and absence
of emitted diagnostics do not establish independent visual glyph fidelity,
historical authenticity, or the correctness of the paper's claims. The source
opening check uses MuPDF only for parseability/page count, not a second pixel
rendering comparison. No scientific formulas, thermal quantities, source
interpretations or causal conclusions were assessed. Original sources,
derivatives, main records and other WIP remain untouched. The only new
worktree file authored by this task is this integrity review.

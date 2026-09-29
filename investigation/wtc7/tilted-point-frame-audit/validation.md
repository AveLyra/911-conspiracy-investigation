# Saved-point audit: execution and verification record

2026-09-24. Research working record; completed stages are recorded below in
execution order. The protocol and separate method review precede new historical
presentation. No physical trajectory, causal ranking or accepted finding is
created by these checks.

## Entry state and source checks

The preceding turn made bounded progress: a new source/code method review
established affirmative support for testing direct saved-image coordinates
against the current 720x480 raster. It did not run the proposed display tests
or inspect new point overlays. The separate bounded Luna confidence review
did not extend attribution coverage or perform a physical experiment.

Main AGENTS, WORKFLOW and START-HERE hashes remain respectively
`01e3fbd03120a2085520818cea0a843a8c6748b4c7bb8ef0e68547c634a963cc`,
`17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a`,
`30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72`.
Main's seven preexisting changed files are unrelated and remain protected.
The investigation branch remains at `e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`
with intentional uncommitted research work. No commit/push is authorized here.

Root reread the complete current main charter, protocol, method review,
source-semantics review, project-export review and `prepare_media.py`.
Initial combined output truncated part of the charter; its remaining sections
were read separately. No source read is inferred from a truncated range.

A root read-only Python JSON query verified the pinned project hash, both
selected arrays, unique x/y occurrences, equality of saved lexical float/value,
and every key-membership flag. It found PM05:43rows/8keys/35nonkeys;
PM08:40rows/40keys; union exactly `range(150,445,6)` (50frames), 83rows total.
Saved coordinate ranges are PM05 x392.875–397.14075165806935,
y151.375–236.28592483419305; PM08 x472.42691415313226–479.3436884707942,
y154.6795012032378–301.8097447795824. These are stored values, not new
measurements, physical bounds or observed feature positions.

`shasum -a 256` matched the old decoder helper
`b8d2010b99001dba79d10b887571ffdfa53b13d8b6800f26a1ed4442c11ba0d5`,
probe `778c35d099158ddc669316d88ee779cf89f5f5aa9c094cd5e1d5bed596bee1de`,
476-frame record `2988d1347bd55cba704530c6d3996dcab1cfa6d5b4beebe6d0ad912ccd4d3a15`,
and FFmpeg binary `7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569`.
The binary reports FFmpeg7.1.1. The selected installed bundled Python reports
3.12.14, Pillow12.3.0, NumPy2.3.5. No dependency was installed or upgraded.

## Pending gates

Synthetic controls, producer-code review, independent verification, repeated
historical decode/presentation, 50-panel/83-row separate visual records and
all-row comparison are not yet completed at this entry. Subsequent results
must state actual commands, failures and limits rather than silently treating
this checklist or method approval as passed tests.

## Completed preparation, before historical visual inspection

Root fully reviewed the producer and its13-test script. Root also read the
independent verifier's initial source/geometry functions and12 synthetic
controls; its later historical-manifest verifier is a separate pending check.
The old pinned helper's seven tests were rerun with bundled Python, all passed.

Producer controls01 passed13tests. Root repeated them as controls02:13passed,
receipt `d1b9a6eadf919a2dca785937e6a45e4bf05d88268a1eee91e03e38a11a8d9974`.
The producer then identified an inaccurate Y-plane caption on the synthetic
RGB fixture; historical L rendering was unaffected. A caption-only correction
was made, preserving both earlier runs. Final producer SHA256 is
`94eae0ca4eccb80eef453e76e3597f64955039f1ad9a15337de345ed1e1181a5`;
test script `a7c72cf051660c9af91e91e0a928015de430584de7c6b4271a168971d3114edc`.
Root read the changed lines and reran13tests twice, both passing:

- controls03 receipt `d46cc570d9ce8e47b6c431fc93964fd42c2427c8e48c93370eb70d1a9a099366`;
- controls04 receipt `bee0d7b73c05f6866c3bb78f194df9b82266cd4c4631c171b867b865dea1fa71`.

Commands use bundled Python3.12.14 with `-B`, then
`test_prepare.py --out controls02` (likewise03/04) from the worktree.
They exercised exact half-up, adjacent-to-tie and negative rounding, separate
original-domain/rounded-cell flags, every synthetic crop/mask/marker pixel,
missing/duplicate/incorrect rows/keys/frames/pins, no-clobber outputs and
success/warning/error/timeout diagnostics. They are software controls only.

Root separately derived the RGB coordinate pattern and every crop by direct
NumPy indexing, without importing either producer or verifier. All4,276,800
source/crop RGB channel samples across three complete panels matched; all five
plain/marked/mask pairs matched; all19PNG products and fixtures.json were
byte-identical between controls03/04. Root viewed the three complete final
synthetic panels at original1128x648 size: corrected caption, readable labels,
untouched source regions, missing slots and explicit padding were visible.

Before those final controls, root also generated/viewed one synthetic L-pattern
panel in `/private/tmp/wtc7-point-panel-root-6mxy3l3l/synthetic-panel.png`
(`fbabbeabf6fd1884aad83d8be22c797d04743235d9aeeada5822229668972c52`).
Its earlier producer hash was `0b177930a6b91ba4cb405db48b8301f48e4cd9b061ef9eb9be54f4bbd377f06d`;
it is supplementary layout review, not the final-version control receipt.
No historical image was viewed in any of these checks.

Root's separate rounding fixture reproduces `nextafter(0.5,-infinity)` as
`0.49999999999999994`: float-add-then-floor yields1, exact half-up yields0.
The final code already uses the declared exact convention. This is a generic
numerical pitfall, not a demonstrated historical error. A deduplicated
SFB-002/SFB-004 acceptance supplement is queued locally; nothing was sent.

After these controls and code review, root executed the frozen producer twice:
`prepare.py historical --out run01 --reviewed-producer-sha256
94eae0ca4eccb80eef453e76e3597f64955039f1ad9a15337de345ed1e1181a5`
(and a separate run02). Both succeeded:50frames/83rows/349PNGs each.
Run01 receipt `18dd861e333aaea0675c06c56477b2c5442ae8e805ed6c7ba5895cb85ccca8a1`;
run02 `64fbfa3f92d2f9e1c333b49b3b7ce58ee7c235bdb4299ded27d2409cfb12d398`.
Scoped worktree-write approval was used; no source bytes were changed.

Root independently rehashed and compared all357 substantive files in both
runs, checked manifest equality, exact50/83coverage, all476 frame records
against the held baseline, zero probe/decode warnings, and each receipt's
unchanged-input assertion. All passed. Path/argv-bearing input and completion
receipts differ as declared; they are not included in the byte-repeat claim.
This establishes output identity/repeatability, not yet the independent
historical-pixel check or visual interpretation. No historical viewing had
occurred at the time this section was saved.

## Independent historical representation check and root replay

Root completed review of the verifier and expanded controls. The
[verifier's report](verification.md) preserves its earlier12-test success,
the retained15-test failed02 font-bearing error, the narrowly reviewed
checker-only correction, and final15-test controls03 success. Root reran
the final15 tests as verify-controls04: exit0, all passed. No source/crop
pixel tolerance or historical acceptance criterion was weakened.

The final verifier SHA is
`3b2f45f97a9724a826469e88c5313dba7763d04ae14a1ea575c578827c3acf5e`;
tests `c9296ebc297cd71308da575e807b9611e73bd1b7c20a9db25b149c8c86da538f`.
Independent verification of producer synthetic controls03/04 passed, receipt
`07c529581c14f3ff891b6a525d3dfd1d9a3c9131d48c795d40e899c5481df57a`.

Historical verification01 exited0, `pass_representation_only`, SHA
`431ea2063f2a101d853bd32b651a11001b6429e46b51fa6bc103fb929fe5f9f2`.
Root repeated the same verifier in a fresh process with exclusive output
verification02.json: exit0, same pass, SHA
`bc254f11e590ff7a228a0d1e373a8ec1e2439f1c9725fc23c8d5fc9ea280eb4a`.
The replay command from the worktree was:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/tilted-point-frame-audit/verify.py --runs research/sherlock-wtc7-investigation/tilted-point-frame-audit/run01 research/sherlock-wtc7-investigation/tilted-point-frame-audit/run02 --reviewed-producer-sha256 94eae0ca4eccb80eef453e76e3597f64955039f1ad9a15337de345ed1e1181a5 --out research/sherlock-wtc7-investigation/tilted-point-frame-audit/verification02.json
```

Both check the exact83rows/50frames, all476clock/hash joins, all349PNGs,
full-canvas pixels including882labels per run, and357substantive repeat files.
The numerical coverage totals overlap and are not independent observations.
The verifier checks the full-stream digest receipt, not a third independent
full-stream decode; it independently checks actual selected native luma pixels.
Pillow/font/source inputs remain shared dependencies.

## Completed separate visual review and comparison

Only after both numerical checks passed did root and curve_source view the
historical panels. Both actually displayed all50complete1128x648panels with
`view_image(detail="original")` and original-detail forwarding, in ascending
steps of6from150through444. Both inspected all83present plain/marked pairs;
no panel failed or was skipped. Their frozen files contain actual viewed
paths and hashes. Source guidance and prior footage knowledge are disclosed;
this is neither blind nor human/specialist acceptance.

Root recorded judgments incrementally. The observer finished first and sent
only its completion/hash, not substantive findings. Root completed its83rows
and50-entry manifest, obtained SHA
`e31b2f9cbc880872aec69201c155f27c0aa3d3bed9bb5cea8d7748976c853a76`,
then notified the observer of the freeze before reading observer.md
(`9fe612f5df31b4a37557b57cde83d9f979499a5bf48744c06726ef4873b3b117`).
No exchanged finding preceded either completed record. Neither record is
recoded after comparison.

Root's separate read-only Python table parser verified83uniqueexactPM/frame
keys, every saved-key flag,50orderedpanelpaths and their actual hashes in
each observation file. It computed host/feature/relation agreement78/64/69,
complete-triple agreement63, and all20disagreeing rows. Complete agreements
are27/43PM05and36/40PM08. Reasons and category-definition differences remain
part of the interpretation; the counts are not accuracy metrics. The
separate computational comparison is retained in comparison.md.

Root read the entire9109-byte comparison.py and reran it with the bundled
Python `-B`; exit0, PASS. Script SHA
`d907e6d235e91f0e29d7c78362b8264e36bb4b591c92766fb7fe773960d6f4b1`.
The separate implementation checks the actual saved source keys, manifest and
receipt as well as both note tables; it agrees with root's simpler parser on
every count and disagreement. All frozen input pins and50PNG byte hashes and
header dimensions match. Its PNG-header check is not a visual/pixel review;
the earlier independent verifier supplies the separate pixel check.

A navigation read of an assumed investigation-level README returned
`No such file or directory`; no file was created to conceal it. `rg --files`
and a bounded read identified the existing research/README.md navigation.
Some combined source/navigation outputs were truncated; complete unit and
observation reads were obtained in adequately bounded calls. No claim of
new complete primary-paper inspection is based on those navigation snippets.

## Post-freeze source-method qualification

The method reviewer checked a bounded set of held paper pages and the held
lab instructions, saving method-followup.md. Root independently used bundled
pypdf to read the complete text on paper pages10,13,44,45 and lab page3,
checking both complete PDF hashes shown in report.md. The successful command
used `PdfReader(path).pages[page-1].extract_text()` and printed the selected
pages; no file or image was created. Earlier `pdftotext` attempts each exited127
because it was not on PATH. No install or successful Poppler extraction is
claimed. This source-text follow-up occurred after both observations froze and
did not change any category. It does not claim new figure/layout inspection.

The paper's roofline-point terminology limits a lower-foot-based criticism;
generic lab marking guidance does not establish this project's actual editing
history. Uninspected omitted metadata remains uninspected, not absent.

## Critical review, navigation and exit checks

The source-method reviewer read report.md completely and identified two
important qualifications: the imposed lower-foot test is stricter than the
paper's actual roofline-point language, and the inspected primary passages
should not remain queued as unexamined. Root incorporated both. The reviewer
then read the revised report completely, SHA
`6e2c940b11fcba0d9451730cbb3a7c8d69902b9e80b3ab6ab2da5a0346122528`,
and recorded both concerns resolved within that bounded review. The frozen
method-followup.md SHA is
`6561c386c6228416e6c308a69d21e0f9ce20856ef5468202380e7e7caceb29a1`.
This is not a new expert review of physical kinematics or the complete paper.

The existing STATUS.md and research/README.md now supersede their proposed
exact-point review with the completed result and a finite remaining technical
metadata/construction-record discriminator. One initial navigation patch was
rejected as an invalid hunk before application; the corrected patch succeeded.
No source record or frozen observation was changed to fix that editing error.
The context-distiller procedure preserved the branch/HEAD/WIP, actual checks,
unresolved gates and full-reasoning next-task recommendation in the existing
handoff rather than creating another competing status file.

Actual exit checks: scoped `git diff --check` exited0; a separate direct
read-only check passed terminal-newline/trailing-space and all local Markdown
link targets for all nine unit notes, and AST parsing for all five scripts.
Direct checks matter because new untracked files are not covered by Git's
ordinary diff check. These syntax/link checks are not rerun scientific tests.
Fresh main AGENTS/WORKFLOW/START-HERE/charter hashes match entry values; main's
seven preexisting changed paths are unchanged. The dedicated branch remains
`research/sherlock-wtc7-investigation` at
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`, with86porcelain status entries
including extensive intentional prior WIP. No repository-cleanliness claim,
staging, commit, push, source promotion or whole-goal completion is made.

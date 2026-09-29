# Bounded follow-up: what does the source define as EC/WC?

2026-09-24. Read-only source-method follow-up after the two observation records froze. This new note does not alter the protocol, method review, source data, or either observation record. It introduces no physical measurement, new figure, external retrieval, raw-project/private-metadata inspection, or claim of actual-human review.

## Finding

The inspected primary passages define **roofline points**, illustrated in Figure 4. They do not explicitly require continuously visible material corners, nor do they specify how EC/WC is marked after the visible step foot becomes indistinct. A direct material point, a selected roof-edge ordinate, and a constructed intersection are not distinguished by a documented post-indistinct-feature rule in these passages.

The protocol's lower-step-foot correspondence test is therefore **more specific than the paper's express roofline-point definition**. Failure to authenticate that particular foot is a limit on the stronger material-corner interpretation, not by itself a failed test of every legitimate roofline observable. Conversely, the possibility of using a geometric edge construction is not evidence that the authors actually used one, or that its uncertainty would be negligible.

## Direct primary text coverage and locators

Primary paper: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf`.

Fresh extraction covered complete page texts **10, 12–16, 41, 44–45, and 50**. These were read as `pypdf` text, **not newly rendered or visually inspected**. The prior `multipoint-table-reproduction/method-review.md` records earlier complete visual coverage of pages 10–16 and 37–50; that prior coverage is attributed, not claimed as a new inspection by this follow-up.

| Primary locator | Supported finding | Limit |
| --- | --- | --- |
| Paper p. 10, first paragraph; earlier-analysis discussion | The earlier center point approximates NIST's point, described as aligned with the east edge of the louvers on floors 46–47. | Approximate architectural alignment is not a post-obscuration marking recipe or proof of a specific material joint. This paragraph describes earlier work. |
| Paper p. 13, section 3 and §3.1, Figure 4 caption | The new study tracks four north-face roofline points; EC and WC are the blue and orange roofline labels. Screen wall and west penthouse are separate targets. | Caption and prose do not say EC/WC must remain recognizable lower step-foot material points. No fallback or construction rule is given here. |
| Paper pp. 15–16, §3.2 and Table 1 | The authors describe measured descent and their interpretation; the footnote states 0.2-second tracking intervals. Page 16 discusses a north-face fold near the louvers as an interpretation of the earlier small movement. | Interpretation of motion/folding is not documentation of how ambiguous image points were selected. |
| Paper pp. 44–45, EC/WC graph titles and captions | The plotted vertical position/velocity series refer back to the blue/orange points in Figure 4. | No direct-marking, edge/intersection, occlusion, or reassociation procedure is stated on these pages. |
| Paper p. 50, reproduction-material section | Links the general kit, calibration material/tutorial, Tracker, and the camera files. | A reproduction-material link does not itself identify the original saved project, editing history, or post-indistinct-feature definition. |

The second primary source is the already-held public kit document:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/Lab-Instructions.pdf`.

All five page texts were extracted; page 2 was read again in a separate bounded output after the first combined output truncated part of that page. No new PDF rendering or tutorial-video retrieval occurred.

- **Lab p. 2:** describes TRZ files as completed examples for comparison with student work, describes marks as position/time references, and discusses the tilted-camera footage and stationary-building check. This is affirmative reason not to assume a kit example is necessarily the publication's exact analysis file.
- **Lab p. 3:** prescribes creating a PointMass marker for the chosen point, manual shift-click marking, magnified adjustment, or alternatively automatic marking. It also discusses rotated coordinate axes and dimensional calibration. It does **not** provide EC/WC-specific identity criteria or a rule for continuing an indistinct step foot.
- **Lab pp. 4–5:** discuss regression selection, result interpretation and follow-up. These do not supply the missing target-specific continuation rule.

The lab's generic marking procedure cannot establish how these particular saved rows were generated. No wider claim that a definition is absent from every possible source is made.

## Existing project and software limits

The current `tilted-camera-source-join/project-export-review.md`, lines 79–84, expressly states that descriptive metadata, arbitrary strings, UI plots, fit descriptions, and some source names were omitted or hashed in the sanitized export. This follow-up did not open those omitted raw fields. Their absence from the reviewed derivative is **not evidence of absence in the original project**. There is no presently inspected, safe target-specific description to quote as resolving the question.

`tilted-camera-source-join/source-semantics-review.md`, lines 103–107, establishes a different point: saved coordinates and keys do not identify the marking procedure. Keys may be manual or automatic; PM05's 35 nonkeys precede all surviving keys and cannot be explained by interpolation between those surviving keys alone. Those source-code facts do not tell us whether an analyst chose a material point or a constructed image location.

## Frozen observation-definition caveat

The root record, lines 18–21, defines its host/candidate labels at the **neighborhood** level, not as precise subpixel authentication. The separate observer record, lines 38–51, likewise describes local appearance, but reserves `different_feature` for a marked edge segment beside a distinguishable step turn and explicitly allows a legitimate geometric roof-edge observable.

That difference can explain some middle-interval category disagreement without proving either reader mistaken or the historical coordinate wrong. The two records support a qualified visual statement under H0; they do not establish the original analyst's target definition. No rows were recoded or images newly viewed in this follow-up.

## Next discriminator, without repeating completed work

Do **not** queue another general review of the same paper or the same panels as though these relevant method passages were unexamined. This follow-up closes the narrower check of the specified held paper/lab passages. No additional authorized, uninspected passage in those two PDFs has been identified as likely to resolve the post-indistinct-feature rule.

The remaining target is a **specific source-linked construction/editing record** defining the selected image location after the step fades, if such a record can be inspected within the existing privacy/source boundary. Omitted project descriptions are a possible untested lead, not a finding that they contain the answer and not permission to expose them. A proposed narrowly allowlisted inspection would need its own scope/privacy decision; author contact is not authorized here.

If the historical rule cannot be recovered, any independent roofline measurement should name its own observable and uncertainty prospectively and be called a new analysis, not a recovered original marking procedure. That is separate from, and does not evade, calibration and actual-human consequential-measurement gates. The present audit does not reject a roof-edge observable merely because a material corner is not continuously recognizable.

## Actual commands and byte pins

Commands were run from `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`. The bundled Python executable was `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`. These are the two paper extraction invocations used, with the same path and page selections:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -c 'from pypdf import PdfReader; from pathlib import Path; import hashlib; p=Path("research/sherlock-wtc7-investigation/luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf"); print("SHA256",hashlib.sha256(p.read_bytes()).hexdigest()); r=PdfReader(p); [(print("PAGE",n),print(r.pages[n-1].extract_text())) for n in [12,13,14,15,16]]'
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -c 'from pypdf import PdfReader; r=PdfReader("research/sherlock-wtc7-investigation/luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf"); [(print("PAGE",n),print(r.pages[n-1].extract_text())) for n in [10,41,44,45,50]]'
```

The complete lab extraction and follow-up page-2 commands were:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -c 'from pypdf import PdfReader; from pathlib import Path; import hashlib; p=Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/Lab-Instructions.pdf"); print("SHA256",hashlib.sha256(p.read_bytes()).hexdigest()); r=PdfReader(p); print("PAGES",len(r.pages)); [(print("PAGE",i+1),print(p.extract_text())) for i,p in enumerate(r.pages)]'
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -c 'from pypdf import PdfReader; p="/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/Lab-Instructions.pdf"; print(PdfReader(p).pages[1].extract_text())'
```

These text commands exited 0 and wrote no files. A `command -v pdftotext` check found no executable on PATH. One attempted review lookup under main's `metric-motion-audit` returned path-not-found; it was not evidence of missing primary material, and the exact held lab PDF was then read directly. Earlier combined outputs with truncation were not treated as full-page coverage; the relied-on omitted page-2 text was retrieved separately. No extracted text artifact was created.

Fresh hashes:

| Artifact | SHA-256 |
| --- | --- |
| paper PDF | `cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394` |
| `Lab-Instructions.pdf` | `c3a9c7aa44f914dbcc7dd2e5604020db0466de8c27f9d71f70d485b80aeb5557` |
| `multipoint-table-reproduction/method-review.md` | `05898cc8985d31e8bed8c7ecc6246a6d2eb2c51e42593f478ec913510fa83072` |
| `camera2-paper-frame-join/settings-review.md` | `ec4956a7b0f3c41f36da691cd626bd95a7f546caa93fc29694682576a52d111d` |
| `tilted-camera-source-join/project-export-review.md` | `bf3cf0b544ac9317908b4425247a05ca1edd168c3c19294708728afb1e793173` |
| `tilted-camera-source-join/source-semantics-review.md` | `f2a62ac0826e64b60f59aede09c00ff703c1c1a48c549d4f7d42be41ff50b2e1` |
| `tilted-camera-source-join/project01.json` (hash-only this follow-up) | `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8` |
| `tilted-point-frame-audit/root-observations.md` | `e31b2f9cbc880872aec69201c155f27c0aa3d3bed9bb5cea8d7748976c853a76` |
| `tilted-point-frame-audit/observer.md` | `9fe612f5df31b4a37557b57cde83d9f979499a5bf48744c06726ef4873b3b117` |

The evidence-audit and source-of-truth skills required this separation of published observable, imposed audit target, generic software behavior, saved metadata, and historical marking intent. The PDF skill was applied as a text-only source check, with no claim of new layout/figure inspection. Main evidence and all frozen artifacts remain unchanged.

## Report review disposition

The initial report snapshot `1a89a306ac913738548a017d4fd72bee56f2bdc80daf4c187b032e8ed9e8f97e` was read completely. Two substantive corrections were requested: make the paper's broader roofline-point definition explicit beside the audit's stricter lower-foot test, and replace a proposed repeated primary-method search with the specifically unresolved construction/editing-record question.

The revised report snapshot `6e2c940b11fcba0d9451730cbb3a7c8d69902b9e80b3ab6ab2da5a0346122528` was then read completely. Its Result qualification and new primary-method section resolve the first concern; its narrowed next-discriminator paragraph resolves the duplicate-work concern. No further material overclaim was found within this bounded source-definition/interpretation review. The future metadata proposal remains a proposal under the controlling scope/privacy rules, not authorization conferred by this review. This review did not independently re-audit categorical counts or view historical images.

Fresh checks confirmed unchanged root/observer hashes as listed above and unchanged original `method-review.md` hash `cfe0b94704f419f18a8efb7992d03c38841242f3a369d21d877fba39f0e43fc6`. The follow-up note alone was added/extended. It is frozen after this disposition; later root edits, if any, are not covered by the reviewed snapshot hash.

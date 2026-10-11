# Independent Figure 5-142 metadata review

2026-10-04 07:16 UTC. Separate continuing metadata/method reviewer. **The positive byte findings are supported for these exact held files.** The report is appropriately bounded; no material scientific correction is required within the checks below. This is not an unqualified pass against the original plan's absolute no-decoding condition: ordinary ffprobe analysis may decode internally, and that deviation must remain visible.

The review was completed after both collector runs, not as pre-execution clearance. The reviewer did not run the historical collector, decode or display images/audio, use the network, or change source/collector/result files. Only this review was authored.

## Reviewed identities

| Artifact | SHA-256 |
| --- | --- |
| Original fixed plan | `f45a46ccd9bb3046c3f297cd63046a41a04ee4401487807ade50b1c50a17e024` |
| Initial collector, preserved | `0d1e50196b66123de304b122c3eb69b96d6661eab64d386a45c326f838918c3c` |
| Corrected collector | `65bc0e26954ff10b561e34830bb9e707efbc69153a789a1380da0fbd2b155c82` |
| Complete metadata result | `b2e51a671177c0b5ea0b2784eb1894eaacb38c24208d37a2c20207d5689781fc` |
| Preserved truncated first capture | `a67c16e3d09309cadb2f67ae5413010e5b8a68c9e0d938b11143cdbe89886d54` |
| Report reviewed | `4e7a00c264c51f3f26384a5e281e8ba362a29d17e712563304236eb27a60f3ad` |
| Execution record reviewed | `87ced04ed1910922a24d6d331251d119e3530f6e64cd8f5c41b8f423cf9a0f08` |

The three fixed inputs agree between plan, code and result: the 140334936-byte Clip 7 AVI (`a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b`), 151488-byte Figure 5-142 JPEG (`68c9d384ac3b1099361f255f80a74d387073d67500089099765f4f0cf030215a`), and 52766002-byte NCSTAR 1-9 PDF (`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`). The independent direct check rehashed all three before and after and found no change.

Current main AGENTS/WORKFLOW/START-HERE and charter pins match the controls already read for this continuing investigation; the charter remains `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`. The current STATUS entry was read, not treated as independent evidence. An initial overbroad STATUS display was truncated; the current section was then read separately. No claim to a full historical STATUS audit is made.

## Actual verification

The bundled executable was `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, with `-B` and assertions enabled. These are the reviewer's own executions, separate from the root runs recorded in [execution.md](execution.md):

- `python3 -B inspect_metadata.py --test`, from this directory: **six tests passed**, tool `645b66`, exit 0. They cover INFO/odd padding, skipped movie payload, skipped superindex, non-RIFF, an overlong/truncated chunk, and a container without its type. No temporary files or historical input were used by these tests.
- `/opt/homebrew/bin/ffprobe -h full 2>&1 | rg -n -C 2 'find_stream_info|read_intervals|show_streams'`: tool `c6cec0`, exit 0, without any media input. Installed help explicitly describes `-find_stream_info` as reading and decoding streams to fill missing information. The saved ordinary probe command did not disable that analysis.
- `python3 -B -`, stdout-only inline direct byte check from this directory: tool **`eff6d3`**, **exit 0**. It required the exact metadata-result hash, compared all three declared file sizes/hashes, sought each of the **24 recorded RIFF header offsets**, unpacked four-byte IDs and little-endian lengths, checked parent ranges, and compared all **866 retained payload bytes** to their saved length/hash/text-or-hex representation. Movie/index/JUNK payloads were not read by this header check. It also checked the selected PDF resource and raw JPEG bytes, then rehashed the three inputs. No collector helper or image decoder was called.
- Saved report/execution/pin read: `0867c2`, exit 0. The two directly linked report-context text files were checked at `009d48`, exit 0. They support the report's attributed approximately two-minute sequence, disclosed intensity/label adjustments, and unresolved lower-plume alternatives; they do not independently establish those historical observations.

The actual input tree contains no misplaced movie/audio leaf outside its skipped movie list. The positive payloads are independently confirmed at these zero-based offsets:

| Field | Header / payload byte offset | Prefix before first NUL |
| --- | --- | --- |
| `tc_O` | 140334512 / 140334520 | `00;03;12;26` |
| `tc_A` | 140334538 / 140334546 | `00;03;12;26` |
| `rn_O` | 140334564 / 140334572 | `Vince Demetri CBS` |
| `rn_A` | 140334612 / 140334620 | `Vince Demetri CBS` |
| `cmnt` | 140334672 / 140334680 | The saved flames/smoke/debris/corner description, including its original `buiding` spelling. |

The full field lengths are 18/18/40/40/256 bytes. Nonzero binary tails remain uninterpreted, not silently treated as string text or zero padding. Equal prefixes are duplicated fields in one access copy, not independent corroboration.

## PDF/JPEG join and semantic limits

The independent direct check confirmed physical page **272**, `/Im0` → **2850/0**, `/Subtype /Image`, `/Filter /DCTDecode`, and **706×457** dimensions. The object's raw encoded `_data` is exactly the held 151488-byte JPEG, including its SHA. This closes the possible gap between raw stream bytes and `get_data()` output; the collector's call to `get_data()` alone would not justify that general equivalence for arbitrary filters. Root separately checked raw `_data`, `get_data()` and the JPEG at `0d1022`; that is a separate execution, not mine.

The report correctly limits Adobe APP14 and document-level Word/PScript/Distiller metadata: they do not identify an exact tape exposure, editing recipe or deceptive alteration. Header-level EXIF absence is not an archive-wide absence finding. No broader PDF object/revision scan or post-scan JPEG inspection occurred.

Root's technical-reference lookup supplies the stated Adobe field-name mapping. This reviewer did **not** independently retrieve that specification or visually inspect its table. The report discloses that the source is an Adobe-authored 2020 specification obtained through a mirror, with a differently dated filename, extracted-text verification, incomplete screenshot verification, and no mirror-to-official byte comparison. Semantic interpretation therefore remains source-supported and separately attributed, not proved merely by the matching literal prefixes. Neither a tape-name field nor start-timecode text authenticates custody, clock truth, drop-frame/rate convention, continuous original recording, or the exact Figure 5-142 exposure.

## Concrete limitations and disposition

1. **Preserve the ffprobe deviation.** The original plan says no media decoding; ordinary stream analysis does not establish that guarantee. The actual runs requested metadata output, not frame/audio derivatives, and no historical view resulted. The positive field bytes are independently verified without relying on probing behavior, so this operational deviation does not invalidate them.
2. **Preserve the first capture and repair history.** The initial skip list omitted `indx`, emitting two superindex payloads and producing a truncated tool capture. That record is not a complete inventory. The corrected implementation skips `indx`; the complete result, source hashes and direct checks—not the partial capture—support the findings.
3. **Do not generalize the parser's scope.** The generic leaf branch could read a misplaced essence-named leaf as metadata. This is not present in the checked tree. The six controls do **not** exercise the 4-MiB payload, 10000-record or depth-12 refusal boundaries. The 30-second timeout applies only to external subprocesses, not all Python/PDF parsing. This is a bounded fixed-input check, not a universally validated forensic parser.
4. **Retain the attribution and inference boundaries.** The embedded comment is a stored description, not a second witness or new fire observation. The useful new lead is the tape-name/timecode pair; exact source-to-still identity, field handling and image processing remain unresolved. A strongest ordinary alternative is an adjusted/annotated publication still with incomplete retained export lineage; this remains a possibility, not a verified account. A matching source project, original capture/edit record or contrary applicable tag definition could change the assessment.
5. **Keep other reviews separate.** At the first report review, `documentary-review.md` was not yet present; its catalogue chain was not independently cleared by this reviewer. The failed read (`e69893`, exit 1) is a pending-file observation, not evidence of missing historical records. The final package should retain that separately assigned review and a resolving link. No scientific correction is required to the directly checked metadata/PDF/context claims.

The evidence-audit and source-of-truth skills informed this distinction between observed bytes, sourced semantics, inference and unknowns. No cause ranking, human acceptance, matrix state, main/legal record, disclosure status or engine activation changes through this review. The comprehensive investigation remains incomplete.

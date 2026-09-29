# Validation and actual coverage

2026-09-19. Research-only. The bounded source/description unit is complete;
physical calibration, human review and the full investigation are not.

## Executed controls and repeatability

Commands below used absolute script/output paths in this directory and Python
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
(3.12.14), with `-B`. Pillow was 12.3.0; the document reviewer also used pypdf
6.10.0 for page counts. No installation or source-project execution occurred.

| Actual command, shortened to unit-relative names | Result |
|---|---|
| `python3 -B prepare_context.py --test` | Five controls pass: half-open pixels, coordinate origin, bounds, type/mode and scale. Run before historical cropping and rerun by root at closeout. |
| `python3 -B prepare_context.py --out context01` and `--out context02` | Both exclusive runs exit 0. Six PNGs and a receipt per run. All seven corresponding files match byte-for-byte. |
| `python3 -B prepare_sources.py --test` | Five controls pass: exact identity and index/name/size/hash refusal. Run before historical member reading and rerun by root. |
| `python3 -B prepare_sources.py --out source-docs01` and `--out source-docs02` | Both exclusive runs exit 0. Unmodified PNG plus receipt per run; both corresponding files match. |
| `python3 -B alternate-tests.py` | 25 pass: 17 frozen-parser and eight adapter/oracle tests. Agent ran these before historical parsing; root reran all 25, including at closeout. |
| `python3 -B alternate-export.py --out alternate-export01.json` and `--out alternate-export02.json` | Both exclusive exports exit 0 and match byte-for-byte, 510,859 bytes each. |

Thus **35 synthetic tests** pass, and **10 material file pairs** reproduce.
These are not 35 historical/scientific validation tests or independent sources.
The root closeout check compared all ten pairs again, rather than comparing
receipt hashes alone.

The alternate exporter uses a pinned prior ElementTree parser and a separate
minidom traversal. Each export's direct-source check reconciles 1,133 locator
occurrences, 348 scalar lexical checks, two serialized key arrays, two
PointMass tracks, all 150 rows/300 coordinates and all 150 key flags. Root
also replayed that existing DOM oracle against the exact raw source and saved
export, obtaining the same counts. This replay used system Python 3.13.7;
it is not a third independently written verifier. Exact source and code pins
and command coverage are in [alternate review](alternate-review.md).

## Visual/source coverage and independence

The protocol predates this unit's observations. Root and the separate observer
each viewed all three declared whole native frames (0, 67, 135) and all three
declared unmarked 3× context crops. Both first-pass files were saved before
substantive exchange and before viewing the newly reviewed counted-window
image. Existing scene/source familiarity is disclosed in the report; neither
pass is an unused-data holdout or human forensic review. The observer separately
reconstructed all six crop products pixel-for-pixel without using the producer
helper. No endpoint was moved or remeasured.

After the source addendum, each reviewer viewed the complete counted-window
PNG, floor-sheet page 1 and lab-instruction pages 2–3. No other pages are
claimed as fresh visual coverage. Existing page derivatives, not new renders,
were used. The PDF source bytes, page counts and selected PNG/pixel identities
are retained in [document pins](document-pins.json). Root independently viewed
these four complete assets and read the document review.

Both source-copy runs checked the exact five declared outer member bodies;
the document reviewer independently read those same five bodies. Three floor
PDF copies are byte-identical; two counted images are byte-identical. The
PNG was copied unchanged to a safe chosen filename, not an archive-controlled
path. No alternate video was extracted, probed, decoded or viewed in this unit.
The outer filename screen covered 55 entries and only the six suffixes stated
in the report; it was not a nested-archive or public-record absence search.

Root's final in-memory checks passed **29 observer byte/pixel pins**, **18
document/control byte/pixel pins**, the ten repeat pairs, and unchanged frozen
first-pass/review hashes. That includes geometry/mode checks for the four
document images. Hash agreement establishes preservation, not historical truth.

## Pinned principal products

| Product | SHA-256 |
|---|---|
| PROTOCOL.md | `6be332d9537498582e7196c3adfa42ce29a7be6954824e4cea5d365665d74947` |
| SOURCE-ADDENDUM.md | `f7e279b0f1afb6c53ccf65eba286053f1d7b243a4fb333525cccac9ed61227da` |
| context01/receipt.json (identical context02) | `9d0447a64cdf23201f659bcfa6f636641a4a9bbd1999a46449e0cfce9acdbbcd` |
| source-docs01/receipt.json (identical source-docs02) | `6885fd5950e3db837899c04a97d556945bd0a351d61ac48229be0cd630e3e4b6` |
| alternate-export01.json (identical 02) | `e068c83b22a2bbeacf2b632bf68088a1ce32600455b9a5e258c946e5f6a80586` |
| root-observations.md | `b396c5a33122c7dbd63889e4efed45f49e150d360c7137acf68d39b50fab5c3d` |
| observer-note.md | `5baaf087aeda1eb9a9001f9217ce2ac0e2a5eae485140d6bbaf382783146573a` |
| document-review.md | `3a922f85a05c969bf766e6cb5088807a4248e477e557da4420880a1d97a4d672` |
| critical-review.md | `0b1ecdb71eee2013e36f19a34eb1c40be40e02db29c77fa73dd69ff04c915398` |
| report.md, corrected | `809578d80a789b96d70b555865a83c249e85c29967fbad02e72b8b1b858d8216` |

## Review changes, failed attempts and limits

The critical reviewer read the full declared text set but did not re-view
pixels or certify this later validation file. Root applied all three findings:
PointMass motion tracks versus total collection items; the narrower
counted-window-label heading; and accurate nearest-neighbor wording. No frozen
observation, source or numeric product was changed. That reviewer produced the
alternate export, so its text review is not independent implementation review.

No scientific control or historical export failed in this unit. Preserve the
smaller execution problems: initial nonexistent helper/source-location lookups,
a premature lookup of the still-pending document review, a reviewer-relative
lab-page path corrected to the explicit main source root, and an incorrectly
typed working directory on a later next-task read. These were locator failures,
not evidence that the sources do not exist. Oversized inspection outputs were
truncated and reissued separately; unread output was not credited as review.
Saving the critical review encountered an automatic approval timeout; a read-only
check found no created file, and one retry succeeded. Raw sources were unchanged.

The last unit-level test/pin checks above are distinct from repository record
validation (`python3 /Users/admin/docs/911/tools/validate_record.py --strict`),
which also exited 0 this turn. Header/link checks cannot validate the science.
No browser/UI behavior was changed, so browser checks do not apply. The
research worktree remains intentional uncommitted work at HEAD `e8d83d7`.
No cause ranking, accepted Sherlock/Faraday finding, canonical fact, legal
position, publication, transmission, commit or push was made.

# Method qualification: previous standalone output is not independent decoder validation

October30,2026. Additive qualification of our own wording. The earlier source records, numerical results, code and public commits remain preserved; nothing is silently corrected or replaced.

The comparison table in [commit39b64108](https://github.com/AveLyra/911-conspiracy-investigation/blob/39b64108cf112760b162bd176a6d4c80a86c55ca/investigation/broader-evidence/telephone-sound-controls-2026-10-30/README.md) uses the heading **“Prior independent decoder output count for that event resource.”** That adjective is too strong and could incorrectly suggest validation by independent decoder implementations. Read the field as **previous standalone FFmpeg decoder output count for that event resource**. The earlier [3b1c9b18 report](https://github.com/AveLyra/911-conspiracy-investigation/blob/3b1c9b18434e58faef2e7f22b4e457af387d856c/investigation/broader-evidence/telephone-court-audio-resources-2026-10-29/README.md) explicitly states that FFmpeg and ffprobe share a library family and do not provide independent decoder validation. That qualification remains controlling for what those earlier tests actually demonstrated; the original heading is retained as the record of our overstatement.

The prior counts remain **1,987,200** for Lyles' selected event resource and **2,729,664** for Ong's. The prior declared counts, SeekSamples, 2,880-sample Ong difference, newly parsed stream fields, distinct payload hashes and all conflicting observations remain unchanged. No value is selected as a corrected historical duration, and no discrepancy's cause is resolved.

The new October30 test did **not** decode audio. It statically compared stored MP3 bytes and parsed controls/fields. Its initial/portable outputs agreed exactly. A fresh reproduction using explicitly recorded **Python3.14.0** also matched the preserved full result. Earlier invocations did not separately record their interpreter versions; the later observed version must not be retroactively assigned to those invocations. The existing helper is reused, not an independent parser implementation. Positive/negative fixtures and byte reproducibility test parsing/preservation, not independent historical truth.

Scope distinctions to retain:

- Native field/definition values versus previous standalone decoder counts.
- Root stream prefixes/payloads versus event-resource prefixes/payloads.
- Reproducibility and parser controls versus independent decoder or source authentication.
- Stored file structure versus demonstrated runtime playback, audible contents, caller identity and a historical call clock.

No listening, new audio decoding, playback, source-to-caller join or underlying recording/edit/export/custody recovery was performed. Native carrier/operator/recipient, original recording and preparation records remain TODOs. All five tracks and eighteen substantive work-plan criteria remain unfinished.

This is a qualification of our wording, not a new independent recording, a misconduct finding or a claim the earlier report lacked the appropriate caveat. See SOURCE-PINS.json for the two preserved passages and their exact commit/file/line/hash locators. ADDITION.diff records the additive qualification text/pins against absent paths; MANIFEST.json records companion hashes. The original nine-file comparison bundle remains byte-identical to its published commit.

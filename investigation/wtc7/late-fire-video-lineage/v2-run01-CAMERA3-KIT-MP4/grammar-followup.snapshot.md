# Narrow inventory-grammar follow-up

2026-09-19. Declared after the preserved v1 failures and their independent
diagnosis, before a revised historical attempt. This changes only accepted
serialization grammar, not source selection, sampling, scientific criteria,
warning policy or native-image processing. The original protocol, selection,
helper/tests and failed runs remain unchanged.

Camera2's 8,042 frame records end in exactly one terminal `|`; the kit MP4's
first record does likewise, while its other 442 records already satisfy v1.
The original parser rejects the resulting empty token. Inventory diagnostics
are empty and integer timestamps/geometry are present. The diagnostic memo
retains exact hashes and the original refusal. This is not a missing-frame
repair or permission to drop arbitrary empty/unknown fields.

Authorize one separately named helper revision, `screen_local_v2.py`, copied
from the frozen implementation through an explicit reviewed patch. Only:

- Permit exactly one terminal empty token after exactly three nonempty tokens.
- Preserve the existing allowlisted unique-key, integer, fixed-geometry and
  strictly increasing-PTS checks after that syntactic recognition.
- Count recognized terminal delimiters in coverage; keep/hash raw inventories
  unchanged and continue to accept the original untrailed grammar.
- Identify the revision and this declaration in each new run; preserve helper
  and declaration snapshots/hashes. Leave decoder commands and diagnostic
  acceptance untouched.

Reject leading, interior, repeated or extra empty tokens, nonempty unknown
payload, duplicate/missing fields, malformed timestamps, geometry changes and
duplicate/decreasing PTS. Run the original sixteen controls against this
revision plus targeted positive/negative grammar tests before historical use.
Independently reproduce the preserved Camera2 candidate-plan hash from its
integer inventory; this is a planning check, not accepted images. Review the
full helper diff. A new downstream warning remains a new refusal.

Only the two exact failed source IDs (VID-WTC7-001, CAMERA3-KIT-MP4) may use
new `v2-run01-ID` and, if admitted, `v2-run02-ID` destinations. Success requires
the unchanged source, diagnostic, timestamp, geometry and repeatability checks.
No new selection, resampling or fit. Do not run the revision on 006 to evade
its unsupported Late-SEI diagnostic. That source remains an explicit unresolved
coverage gap requiring a separately justified decoder/bitstream investigation.

No accepted scientific finding, physical calibration, causal ranking or
historical authentication follows from a format-compatible parser.

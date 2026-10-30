# Reproduce the static sound-control and stream comparison

Use Python3 and the unchanged official [court ZIP](https://coop.vaed.uscourts.gov/moussaoui/flights.zip). Do not run the included launchers or SWFs. The script checks exact archive/member/helper fingerprints and performs read-only parsing; it makes no network request or media output.

The existing helper is [reproduce_resources.py from commit3b1c9b18](https://github.com/AveLyra/911-conspiracy-investigation/blob/3b1c9b18434e58faef2e7f22b4e457af387d856c/investigation/broader-evidence/telephone-court-audio-resources-2026-10-29/reproduce_resources.py). Its functions are reused without running its main entry point or --decode option. In a full repository checkout the default sibling path finds it; otherwise pass the exact reviewed helper:

```sh
python3 compare_sound_controls.py /path/to/court-flights.zip --helper /path/to/reproduce_resources.py > result.json
```

The full result must be **989,449 bytes**, SHA-256 **ea247c441880a3277267235daaa188e3f58b4b63a02c7a3bc1a9dd482947c9f3**, for these exact script/helper/input bytes. It contains the numeric block ledger, not audio. Compare the compact fields and per-member canonical-ledger hashes in RESULTS.json. Source offsets are uncompressed SWF tag-header offsets; frame indices are one-based root timeline positions. MP3 root block payload excludes the UI16 sample-count and SI16 seek fields; the event payload excludes its signed seek prefix. These exclusions follow distinct source structures, not an attempt to reconcile counts.

The code includes positive and truncated/reserved-bit parser controls. Passing them and matching hashes proves reproducibility only to this static scope. It does not validate historical source/custody, speaker identity, playback, complete conversation, carrier-field meanings or a call clock. No duration is selected and no media are normalized.

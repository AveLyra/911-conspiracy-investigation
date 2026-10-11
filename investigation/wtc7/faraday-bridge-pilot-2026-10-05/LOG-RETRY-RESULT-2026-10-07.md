# Log-path retry: native tests pass; custom matrix incomplete

The authorized log-file argument was added only to the separate
verify_bridge_retry_log.py. Earlier harnesses and failures remain preserved.
The safety guard and product tests/code are unchanged.

The native run collected and passed all nine cases, with zero failures or
skips (pytest 2.22 seconds; runner exit 0). This verifies the existing native
bridge test coverage, not full custom coverage, scientific validity, destination
resolution or Sherlock admission. Native fixtures still omit typed --synthetic.

The first custom matrix completed seven setup commands, then refused
evidence-refutes with exit 2: "directional evidence must record at least one
passed or failed control". This is an omitted fixture requirement, not an
export failure. The earlier enum repair did not address that requirement.
The refused command left its before/after workspace snapshot unchanged. No
unexpected guard denial occurred. Zero export cases ran; the second matrix,
final workspace audit/synthesis and ledger verification were not reached.
No missing control result was fabricated, and no further repair was performed.

Both full runs are retained under captured-log-retry-20261007 and their original
scratch roots. A separate read-only check confirmed all 13 product pins,
native counts, failed-command nonmutation and preserved regular-file hashes.
Faraday git status remains clean. Earlier original reports remain historical;
this result supersedes only their claim that no native tests have run.

Next proposed fixture repair requires defining and actually checking a relevant
synthetic control before recording its result, then inspecting the remaining
matrix contract for similar omissions before any retry. Merely labeling a
control passed to satisfy admission is not an acceptable fix. This work was
not performed under the log-path-only allowance. No case data, main-thread
goal state, human review gate, external channel, commit or push changed.

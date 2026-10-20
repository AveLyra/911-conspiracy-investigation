# Column 79 protocol verification tools

The frozen [four-case comparison protocol](../c79-factorial-protocol-2026-10-19/README.md) now has a standard-library checker that independently reruns its 22 recorded design checks. The checker reads the existing files without changing them. Synthetic controls exercise each named check, including missing comparison cases, changes to both factors, invented inputs, false execution claims, and treating an unknown historical result as false.

These are software and protocol-consistency tests. Passing them does not validate a finite-element model, authenticate a construction drawing, establish plate capacity, resolve a report discrepancy, or identify a historical collapse cause. The identified native UAF inputs, outputs and case mapping are still needed before executing the planned comparison.

## Reproduce the checks

From this directory, run:

```sh
python3 -B verify_protocol.py
python3 -B -m unittest -v test_verify_protocol
```

The first command reports 22 named checks, the three original file hashes, and whether the names match the earlier verification record. It exits with a nonzero code on failure. The second command runs synthetic positive and negative controls. Both commands are read-only; no network access, external libraries or solver is required. `-B` prevents new Python bytecode cache files.

The original protocol, README and verification record are pinned by SHA-256 to public commit `b57c0a52e9a9e26ad8f77046f773c1266eb52d8a`. Those byte-level checks are separate from the design checks: a changed source must not be silently accepted because its design still appears coherent. `--bundle` may point to another local copy for inspection, but this checker is intentionally for this preserved version rather than for approving later revisions.

## Scope and provenance

The protocol's existing source pins and page references remain unchanged. The checker compares those recorded values; it does not retrieve or reauthenticate the underlying UAF or NIST PDFs. Its targeted checks are not an exhaustive schema or a privacy clearance. The synthetic path strings in its negative controls are test fixtures, not actual user data.

`run-verification.json` records the actual runs, input and code hashes, control coverage, limitations and source/public copy checks. The source research copy and additive public mirror are kept separately. Earlier records are not overwritten, and no new model execution or third-party contact is performed by this package.

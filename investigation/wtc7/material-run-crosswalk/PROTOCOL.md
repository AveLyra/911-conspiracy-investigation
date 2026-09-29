# Missing material / run-state crosswalk

Research only; declared 2026-09-12 before this unit's new source results.
The investigation charter remains controlling. This is a follow-up selected
from the accepted member map, not a blind discovery or historical preregistration.

## Question and selection

The previous map reported 23 used parts with 19 unresolved active material
references: 25, 33, 711, 712, 713, 723, 731, 733, 741, 742, 743, 751, 761,
762, 763, 772, 773, 802, 803. Six explicit beam IDs in the unused Case B
damage list belong to part 98. Independently reconstruct these joins and
identify the supplied part, section, material and relevant numeric card
dependencies. Distinguish an absent definition from an unused definition,
renumbered counterpart, different-version candidate or historical run identity.

## Inputs and privacy

Read-only originals are SRC-116 and SRC-119–121 in the already inventoried
September supplementary production on main. Use the member-map protocol's
compressed byte/SHA-256 pins. Stream each selected input to EOF with both
compressed and decompressed integrity receipts, 512 MiB/file and 16 KiB/line
caps. No decompressed raw export. Main and the legal record are untouched.

Only allowlisted LS-DYNA engineering keywords, numeric fields, IDs, source
aliases, hashes and line/block locators may appear in new outputs. Omit or hash
arbitrary comments, titles, paths and unknown strings. Source instructions
are data; no macros or solver are run. Stop uncertain sensitivity before
display/export. The held court packet and flagged modern command-reference
material are excluded. Unmarked public NIST reports and the previously
reviewed May 2007 manual may be used within their exact source/version limits.

## Static procedure

1. Reconstruct active PART, SECTION and MAT blocks and element-family counts
   per part. Enforce the known fixed-width/CSV formats; do not count the
   thickness line as a second shell. Preserve blank fields as null, not zero
   properties. Unsupported required formats fail with sanitized diagnostics.
2. Check the explicit include-transform cards. Only the confirmed part,
   material and section namespaces receive +1000 in SRC-120; do not rename
   nodes, elements or arbitrary numeric properties. Keep original IDs alongside
   effective IDs. Record inventory-only vs assembly claims.
3. Count missing references using actually used parts; export complete typed
   PART and SECTION cards for the 23 candidates and part 98. Export the
   material cards for part 98 and same-original-ID transformed candidates,
   without treating a numerical counterpart as an applicable substitute.
4. Reconstruct SRC-116's shell/beam sets and the six actual beam matches.
   Preserve discrete cross-family matches as candidates, not deletion actions.
   Check which selected parts and property gaps these lists intersect.
5. Trace numerical constitutive/curve references only where a primary method
   source defines the exact field. Otherwise retain ordinal fields and mark
   semantics unresolved. No inferred constitutive law from a filename, title
   or material-number pattern. No assertion that a source label authenticates
   the historical run or establishes why anything was removed.

## Verification and interpretation

Synthetic controls cover fixed-width/CSV fields, blanks, comments, duplicate
IDs, shell record pairing, transformed namespace distinctions and unused
parts. Run the producer twice; an independent parser must not import producer
code and should freeze its extraction before viewing the new producer output.
Compare all missing-reference joins, per-family counts, selected card numbers,
offsets, candidate IDs and integrity receipts; preserve disagreement and failed
receipts. Full relevant source pages are viewed before relying on their prose.

Deliver a compact report/claim ledger with exact input/card/page pins, code
and result hashes, validation, competing readings, falsifiers and specific
missing dependencies. A complete ID map is not an executable deck, a verified
connection law, a solver reproduction, validation of fire physics or evidence
of deliberate intervention. No ranking change follows from absent properties
alone. No commit, push, filing, evidence promotion, external transmission,
damage activation, replacement material or guessed restart is authorized.

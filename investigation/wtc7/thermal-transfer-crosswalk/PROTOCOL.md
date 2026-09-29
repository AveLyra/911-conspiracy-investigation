# Thermal-file role and export crosswalk

2026-09-12. Exploratory WP3 / Q02 / Q06 / Q10 declaration before new command
or whole-body scan results. The prior repeated-assignment trace and older
June-production header audit are known. The charter remains controlling.

## Question and competing interpretations

Determine whether the released June files contain an identifiable routine
generating the LS-DYNA nodal temperature input, rather than only applying
thermal loads inside ANSYS. Do not assume that LS-DYNA temperatures were
exported from completed ANSYS structural results: current primary-source
discovery describes a separate LS-DYNA thermal-data set. Distinguish thermal
analysis, thermal-to-structural mapping, ANSYS temperature application,
structural-damage handoff, and LS-DYNA input generation.

Look for affirmative implementation evidence as well as missing links.
An exporter can write a keyword literally or construct it dynamically;
absence of a literal marker cannot prove absence of every possible exporter.
An input-loading command, filename extension, solver mention or source comment
does not by itself identify dataflow, execution, a complete routine or a
historical run. Record code vocabulary and unresolved calls without executing
or automatically following any source instruction.

## Sources and minimized output route

Read the three APDL entries selected from the pinned June production manifest
and all non-PNG, non-directory members of its known thermal ZIP, including
the previously NUL-flagged member. Read that member as bytes and report its
NUL/lexical coverage separately; do not silently decode it as ordinary text.
PNG member metadata is counted but image bytes are excluded. No new external
acquisition, solver, embedded call, macro evaluation or source-file execution.

Manifest SHA-256:
`30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf`.
Thermal ZIP SHA-256:
`2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181`.
APDL byte/SHA pins come from that manifest. The preflight metadata census
finds25,634 regular member entries,477,264,192 non-PNG bytes and a largest
member of1,591,990bytes. This is size metadata, not a content finding.

Continue the local engineering-only inspection boundary: outputs are source
ordinals, source/name hashes, archive member ordinals, byte/line/count/CRC
receipts, allowlisted command and marker names, command locators, and typed
numeric command fields where separately validated. No raw source bodies,
comments, arbitrary strings, author metadata, paths, credentials or personal
data enter tool logs or new files. Quoted/unrecognized arguments are omitted
or hashed, not displayed. Technical filenames may be linked internally by
hash, not copied wholesale. Labels A/B/C and filename-shape classes can be
emitted only through anchored known-pattern matching. If intended output
raises sensitivity uncertainty, stop that output before disclosure.

Main, raw sources, previous research derivatives and canonical/legal records
are read-only. New derivatives remain in this investigation worktree. The
held packet, correspondence and new legal analysis stay excluded.

## Lexical coverage and declared checks

This is a **lexical role audit**, not an APDL interpreter. Separate physical
lines, nonempty/comment-only lines, command starts, numeric data and unknown
tokens. Respect quoted `!` and `$` while separating comments and abbreviated
command sequences. Detect `*VWRITE`/`*MWRITE`/`*VREAD`/`*MREAD` format lines
as separate lexical material; do not mistake them for commands. Preserve
unrecognized or ambiguous constructs as explicit coverage limits.

Allowlist the relevant input/output, selection, thermal load, macro/control
and solver vocabulary in the scanner before historical processing. Match
full command tokens, not substrings such as BF within another word. Check
literal LS-DYNA thermal keyword and known output-basename markers separately
in code versus comments; retain their line locations, not source text.
Collect command counts per file/class and bounded locators for output/input
operations. Do not emit hundreds of thousands of BF/BFE rows or infer
temperature values from command counts. A body-load marker in a quoted format
string is not an executed command.

Read each source to EOF with byte/hash checks; archive reads validate CRC.
Caps:4MiB/member,16384bytes/line,512MiB total non-PNG+APDL input,
30000archive entries,768MiB observed process memory,10000 retained operational
locators per file. Never extract an archive member to an embedded path.
All outputs are create-only, including safe failure receipts. Preserve
source ordinal/line and error code without raw exception text.

Test synthetic comments/quotes/dollar separators, full-token matching,
format lines, NUL handling, unknowns, dynamic/quoted markers, caps, archive
CRC failure and repeated filenames before historical processing. A separate
reader should reconstruct the material counts and locators without importing
the root scanner or seeing its results before freezing its own output.
Different programmatic scans are not independent historical evidence.

## Completion of this bounded unit

Produce an evidence-backed role/source crosswalk: actual commands and their
documented semantics, public methodological dataflow, and exact unmatched
export/mapping dependency. Explicitly separate full-body lexical coverage
from semantic interpretation or execution. Do not equate a lexical miss with
nonexistence, deliberate withholding, erroneous temperatures or a cause.
If no exporter is identified after this finite source pass, preserve that
bounded result and proceed to other feasible charter work rather than
repeating the same generic search. No first/last temperature reduction,
solver, public transfer, legal promotion, commit/push or Faraday execution.

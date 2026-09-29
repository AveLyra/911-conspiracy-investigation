# APDL01 material-definition audit

2026-09-28. Prospective research-only WP3/Q02/Q10 unit. The previous goal turn
made progress by completing the published heat-storage method check. Main
AGENTS, WORKFLOW, START-HERE and the main CHARTER control; their current hashes
match the preceding audit. Intentional worktree WIP is preserved. No main/raw/
legal edits, model execution, include following, private drawings or transfer.

## Question and fixed source

Does the already located APDL01 candidate contain literal thermal storage
definitions, mechanical properties, or both? Existing command counts are known;
arguments and results have not been inspected for this unit. This is a
prior-informed finite source test, not blind preregistration. A mechanical-only
finding closes this candidate for the sought direct thermal definitions, not
the entire upstream-model search. Mixed/unresolved syntax must stay unresolved.

Use only APDL01, the first APDL row in the pinned June manifest, resolved by the
existing thermal-transfer route. Manifest SHA256
`30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf`;
candidate SHA256
`e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64`,
212,384 bytes; filename hash
`ff5c9a2bc8d8822fa9e3a1acaeb1becbab49aa2d5675c12f98b44261c1e00135`.
The existing derivative reports5,474 LF lines. No other APDL or archive body
is in scope. Source and manifest pins must be checked before and after, and
candidate path confinement/symlinks must be checked before opening it. No
source filename, free comment or unrelated argument enters outputs.

## Typed scope and interpretation

Collect source line/segment, segment hash and only explicitly recognized labels
and numeric fields for MP, MPDATA, MPTEMP, TB, TBTEMP, TBDATA and ET. Retain
blank fields as blank, distinct from explicit numeric zero. Preserve numeric
lexemes, including exponent notation, without evaluating expressions or
silently resolving defaults. Number syntax is ASCII signed decimal with optional
E/D exponent, at most64 characters; integer ID fields require literal unsigned
integers. Unsupported expressions/quoted fields remain hashed/unresolved.
Never turn a partial row into a fully decoded one.

MP/MPDATA labels: C, ENTH, DENS, KXX/KYY/KZZ, EX/EY/EZ, GXY/GYZ/GXZ,
PRXY/PRYZ/PRXZ, NUXY/NUYZ/NUXZ, ALPX/ALPY/ALPZ, CTEX/CTEY/CTEZ,
THSX/THSY/THSZ, REFT, EMIS, HF, QRATE, ALPD, BETD, DMPR, DMPS and MU.
TB labels/options: BISO, BKIN, MISO, MKIN, KINH, PLASTIC, ELASTIC, MELAS,
CONCR, CREEP, DENS, CTE, THERM, USER, STATE, COND, ENTH, SPHT, FLSPHT,
LINEAR and NONLINEAR. Recognition of a legacy name is lexical, not certification
that its command position is valid in a particular solver version. Unlisted
labels stay hashed, not displayed or assumed nonthermal.

ET admits numeric local/library IDs. Textual element names are unresolved in
this first pass: no unreviewed name-to-number substitution. Standard command
positions are used; MPDATA/MPTEMP UNBL coded-database variants are detected
and retained unresolved, not read with the ordinary field offsets. Empty or
overlong argument lists, extra nonblank fields, unmatched quotes and unexpected
formats are retained with explicit status. Extra trailing blank fields may be
ignored for schema matching but their count and segment hash are retained.

This is a lexical field audit, not a material-table interpreter. Do not combine
MPTEMP/MPDATA rows into active curves, infer Celsius/Kelvin, apply default IDs,
resolve selections/branches/macros or infer that any definition was executed.
MPDATA numeric locations and property values, MPTEMP numeric locations and
temperatures, TB numeric identifiers/counts/options, TBTEMP values, TBDATA
locations/values and ET numeric IDs/options stay tied to their original rows.

Quote-aware comment/command splitting and format-line handling may reuse the
existing pinned lexer, SHA256
`c6e69416a50a20a26ac15da70fdd3cc6fb56178c07b50a35c06b4b3fb6c3cd53`.
Importing it must not call historical(), selected_apdl() or main(), which read
a broader corpus. The independent parser must not import the producer/parser
or read its historical results before freezing its own. Counts for known control/
I/O commands and hashed unknown tokens flag unexamined behavior; no paths are
followed. Format records, unknown tokens and unresolved rows bound any negative
finding. A missing literal C/ENTH is not proof no other file or runtime supplied it.

## Documentation basis and version limit

Official Ansys2024 R2 HTML command references were opened on September28:
[MP](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_MP.html),
[MPDATA](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_MPDATA.html),
[MPTEMP](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_MPTEMP.html),
[ET](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_ET.html),
[TB](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_TB.html),
[TBTEMP](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_TBTEMP.html),
[TBDATA](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_TBDATA.html).
The2025 R1 [coded-database reference](https://ansyshelp.ansys.com/public/Views/Secured/corp/v251/en/pdf/ANSYS_Mechanical_APDL_Programmers_Reference.pdf)
was located via a search excerpt explicitly showing UNBL field offsets; only
that locator is used to exclude rather than decode the alternate form.
No complete manual PDF was acquired or read. Current official documentation
supports the field vocabulary, not the historical solver version or its actual
default/precedence behavior. Modern TB/PLASTIC options do not retroactively
prove validity of legacy TB syntax. Any element-role interpretation requires
a separate official element reference after the numeric code is known.

## Acceptance and preservation

Before native reading, pass synthetic checks for all seven schemas, blank/zero,
unknown/quoted labels, expressions, extra fields, D exponents, same-line
commands, comments, doubled/unclosed quotes, format records, UNBL exclusion,
privacy sentinels, caps, source-pin mismatch, path refusal and create-only
outputs. Caps:4MiB source,16,384 bytes/line,10,000 selected rows; no network
from the parser. Numeric values retain their raw unit ambiguity. Outputs and
failure receipts are create-only in this new unit directory; failures emit
only fixed codes, never exception messages or raw source context.

Root and a separate parser must freeze minimized results before comparison;
compare every selected locator, label, numeric/blank state and unresolved row,
plus source hashes and counts. Rerun producer for deterministic result equality.
An independent code/privacy review precedes historical execution. A mismatch
must be resolved or left as a consequential reproduction limit, not averaged.
Publish a research-only report with positive role evidence, unresolved syntax,
version limits and the next discriminating input. Keep unit tests, source reading,
historical execution and physical validation distinct. No collapse-cause ranking
follows directly from a script's vocabulary. Existing human/privacy/send and
archived Sherlock routing gates remain unchanged.

## Pre-native schema clarification

Before either native read, the two implementers fixed the exact ordinary
argument slots: MP=[label,id,5numbers]; MPDATA=[label,id,id,6numbers];
MPTEMP=[id,6numbers]; TB=[label,id,id,id,option,blank-only,blank-only];
TBTEMP=[number,id]; TBDATA=[id,6numbers]; ET=[id,id,7ids]. TB's final two slots
follow the current reference's unused/function positions; no historical EOSOPT
interpretation is invented. An option is an allowlisted table token or unsigned
integer. No-argument commands are unresolved except documented MPTEMP reset;
omitted trailing fields are represented as blanks with argument_count retained.
This is literal-field decoding, not solver-validity certification.

Segment ordinal counts all dollar-separated slots including empty ones. Hash
stripped segments re-encoded as latin1 bytes; hash stripped unresolved field
text as UTF8. This explicit representation avoids leaking text and avoids a
Unicode exception for direct synthetic function inputs. Historical bytes are
decoded as latin1 without claiming the source's original character encoding.
The independent source selector may locate the unique fixed source/name hash
provided it also verifies that it is the first of three APDL manifest rows.
No other native body is opened. These clarifications precede historical outputs.

Pre-native code review additionally requires quote-aware comma field splitting,
including doubled quotes. A quoted unknown value stays unresolved but must not
shift subsequent fields into incorrect roles. Invalid CLI arguments must produce
only a fixed failure code, not echo supplied text. These correct implementation
defects; they do not change the source, allowed output or scoring contract.

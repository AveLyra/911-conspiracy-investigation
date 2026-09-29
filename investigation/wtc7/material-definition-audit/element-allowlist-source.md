# Official 2024 R2 element-name allowlist: source and boundary

2026-09-28. Working research only. Main AGENTS, WORKFLOW, START-HERE and the
main investigation CHARTER control. Applied the evidence-falsification and
source-of-truth skills and their referenced checklists. This independent
public-source locator did not read native/APDL source, inspect unresolved field
values, compare field hashes, or infer any native value. The parent will freeze
its distinct field-reading scope before any native comparison.

## Finite source and construction

The official [2024 R2 numerical Element Library](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_elem/Hlp_E_LIBRARY.html)
is the primary enumeration source. Its full web-reader display, lines 0-182,
was inspected, including its Release 2024 R2 footer. The list contains 155
linked entries: 139 plain base-name labels and 16 MPC184 subtype labels.
Structural, thermal, coupled-field and other documented families are included;
this is not a thermal-only selection.

[element-allowlist.json](element-allowlist.json) contains the **139 distinct
base names**, ASCII lexicographically sorted, under the exact field `names`.
They were manually transcribed from the complete official library list, then
counted, deduplicated and sorted in memory. Every retained label matches
`^[A-Z]+[0-9]+$`. No label was supplied from a native field, guessed from a
digest, added after a native nonmatch, or inferred from a physics hypothesis.
The public-source list was first found and read independently before the
parent reported finding the same index. Agreement on that index is not a
second independent historical source.

For reproducible extraction from a separately preserved official HTML copy:
select only the element-list anchors following the availability introduction
and preceding chapter navigation; retain exact anchor text matching the above
base-name pattern, with surrounding whitespace stripped; record all excluded
anchor labels; deduplicate and sort. Do not regex-match arbitrary strings
across the whole page or count navigation links. Expect 155 list entries,
139 retained names and 16 subtype exclusions. This is a proposed extraction
method, not a claim that an HTML parser was run in this locator task.

The exclusions are retained explicitly in the JSON. They are:

```text
MPC184-Link/Beam       MPC184-Slider       MPC184-Revolute
MPC184-Universal       MPC184-Slot         MPC184-Point
MPC184-Translational   MPC184-Cylindrical  MPC184-Planar
MPC184-Weld            MPC184-Orient       MPC184-Spherical
MPC184-General         MPC184-Screw        MPC184-Spotweld
MPC184-Genb
```

The base `MPC184` remains included. Excluding these compound display labels is
a lexical base-name boundary, not an assertion that the associated element
behaviors do not exist. Ansys's [Element Input, section 3.1.1](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_elem/Hlp_E_CH2_1.html)
describes element names as a group label plus a unique number, with a maximum
length of eight characters, and identifies ET as the selection command. The
allowlist does not independently define every acceptable ET argument form.

## Current documentation is not the full historical vocabulary

The [2024 R2 element release notes](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/mapdl_releasenotes/rnelemchg.html)
identify SHELL294 as new at this release and describe no newly undocumented
elements at this release. They also direct readers to a GUI-inaccessible list
and to earlier release notes for prior undocumented elements. Therefore the
139-name set is not an exhaustive inventory of all element names ever used,
nor proof of compatibility with a particular earlier solver installation.

It should not be called a current-technology-only or non-legacy list: the
documented library itself includes older entries. Conversely, absence from
this version's documented library must not be classified as a non-element,
error, structural element or anything else by elimination. Preserve a nonmatch
as unresolved.

The official GUI-inaccessible locator is
`https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_elem/Hlp_E_CH3_3.html`.
The initial linked access and one direct retry both failed in the web reader
with `Cache miss`. No content of that page was recovered or relied on, and no
legacy companion names were added. GUI-inaccessible, undocumented, retired,
removed and unsupported are not interchangeable statuses; this task did not
establish which applies to an unlisted historical name.

The [2024 R2 Global Release Notes](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/global_releasenotes/global_releasenotes.html)
locate archived release notes through the 2024 R1 documentation and the
customer-site documentation route. Those onward destinations were not opened;
there was no authenticated/private access or attempt to exhaust prior releases.
The parent explicitly accepted a finite documented set with this historical
incompleteness if the companion could not be obtained within the bounded pass.

## Literal public searches and inspected routes

Four queries were issued, each restricted to `ansyshelp.ansys.com`:

1. `2024 R2 Ansys element reference numerical element library list`.
2. `"v242" "GUI-Inaccessible Elements" "archived"`.
3. `"v242" "Archived Elements"`.
4. `Ansys "GUI-Inaccessible Elements" "Archived"`.

Queries 2 and 3 returned empty results. Queries 1 and 4 also returned other
release versions and PDF snippets; none of those PDFs or other-version bodies
was opened or used to populate the list. No query contained native field
strings, hashes, private paths or case-specific source contents.

Successful primary HTML coverage:

- Numerical library: full 183 returned lines; authoritative enumeration above.
- [Summary of Element Types](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_elem/Hlp_E_CH3_2.html):
  returned display through line 484 of an 808-line page. This was partial
  classification-table coverage, not a complete independently enumerated
  cross-check and not the JSON's enumeration source.
- Element release notes: full 62-line display on the second read; release and
  undocumented-element caveats only.
- Element Input: full 237-line returned display; section 3.1.1 supports the
  base-name distinction. Other input topics were not used to infer any native
  model property.
- Global Release Notes: full 43-line display; archive locator only.

The GUI-inaccessible page failed twice as described above. No other failed
open, download, saved external source, or expanded historical search is claimed.

## Permitted inference and verification boundary

This is a prospective finite recognition vocabulary, not a model-validation
result. Membership does not establish that an element was executed, its active
KEYOPTs, degrees of freedom, historical defaults, material assignment, or the
causal significance of a record. Parameter substitutions, numeric forms and
other syntax require their own declared handling; this task did not examine
them in native data. A later nonmatch must remain unresolved under the frozen
scope, not trigger adaptive additions or hash guessing.

The in-memory transcription check found 139 entries, 139 unique names, all
matching the base-name pattern, and 16 excluded subtype labels. Its complete
input and result are in this task's tool history. It was not an independent
second transcription or a DOM extraction. The parent is separately checking
the list against the primary page before freezing its own native-reading step.
Only the two newly authorized allowlist files were written with apply_patch.
No existing records or native sources were changed; no model run, canonical
promotion, commit or push occurred.

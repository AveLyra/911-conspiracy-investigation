# G3005 native section verification protocol

October 21, 2026. This followup asks whether available native UAF files establish the section used for G3005 in Figure 3.14, and how that bears on UAF's criticism of NIST. G3005 is a floor beam beside girder A2001; they are not the same member.

Acceptance requires either an authenticated figure-to-case mapping and actual member geometry/section definition, or an explicit unresolved result after scoped file and archive checks. A filename, section name, screenshot label, or advertised download does not satisfy the native-assignment criterion.

## Read only checks

1. Verify the Intel operational store using the main repository's media resolver. Preserve both UAF final PDFs, the NIST report, the selected download wrapper and earlier findings unchanged.
2. Inventory the public Git tree and ignore-inclusive physical research holdings, without following symlinks or traversing Git internals. Record roots, counts, path-list hashes, candidate native suffixes, archives and errors. Do not describe this as a whole-disk search. Treat unavailable roots as exclusions, not empty inventories.
3. Inspect the directory and bounded README of the held UAF ZIP without extracting or executing its contents. Record every member, its hash and whether a native model is actually present. Do not acquire the aggregate archive or retry an already rejected route through another tool.
4. Check whether either UAF PDF embeds attached files. Recheck Figure 3.14's underlying image, rendered vector label and caption. Inspect complete pages containing Figures 3.11 and 3.14 and NIST Figures 8-22 and 8-27. Preserve competing representations rather than correcting their text or selecting the native section from them.
5. Check for likely native input syntax in small plaintext files within the public research checkout. Classify hits by their actual content and provenance; an audit script or quoted example is not a UAF deck. Proprietary binaries, differently named formats, other disks and inaccessible archives remain outside the absence claim.

## Native assignment test

The exact figure case is provisionally located by `Model-10_Nonlinear_10s_No_Support.odb`. To establish G3005's section, obtain that ODB and matching INP/CAE or an authenticated read-only export, all includes and their hashes, the instance/element-set-to-G3005 mapping, and active assignments. For beam elements inspect profile dimensions or generalized section properties and orientation. For shell/solid elements inspect node geometry, web/flange thicknesses and material/section assignments; a W-shape name alone is insufficient. Check suppressed/overlapping assignments and job provenance. An ODB model-data export may answer the section question without rerunning the solver, if it contains the necessary data and is linked to the figure.

## Effect on criticism

Separate the published NIST preliminary-model labels from NIST's actual native assignment and its later reduced/global models. Separate UAF's G3005 section claim, bracing claim, boundary-condition claim and side-plate claim. A possible error in one comparison must not silently validate or invalidate the others. Explain conditional effects using stated mechanics, not a fabricated rerun or numerical sensitivity result.

## Deliverables and release checks

Add a source research note, reproducible inventory/check code, observations and tests; create a separately named public mirror. All earlier records remain untouched. Before publication verify the exact public destination, AveLyra authentication and every new outgoing commit's author and committer. Stage only this package, push additively and verify the remote blobs. No private records, third-party contact, solver installation, history rewrite or private-repository push is authorized by this protocol.

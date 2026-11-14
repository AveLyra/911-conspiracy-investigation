# WTC 7 drawing mirror: directory groups and the 2012 release account

November 14, 2026 UTC · STL02–STL03 / B188 / H005. A reproducible check of the preserved mirror ZIP directory gives more support to the *directory-level* grouping described in the 2012 release account. It does not establish what each file depicts or whether the files are the drawings NIST counted in 2007. [Earlier count comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/3115aa94e5c8112812916dee4bd6d219ff39129f/investigation/broader-evidence/steel-nist-2007-drawing-count-2026-11-14/README.md)

## Reproduced directory observations

| Mirror parent directory, as labeled | File entries | File extensions |
| --- | ---: | --- |
| `WTC7_Details_1/Detail Sheets 1` | 1,248 | TIFF |
| `WTC7_Details_2/Detail Sheets 2/7WTC - D2` | 1,275 | TIFF |
| `WTC7_E_Sheets/E Sheets/7WTC - E1` | 42 | TIFF |
| `WTC7_E_Sheets/E Sheets` | 22 | PDF |

The paths in this table abbreviate a common archive prefix; [the verifier](verify_directory_groups.py) contains their complete parent paths. The two detail-labeled directories total **2,523** entries; together with the **42** TIFF entries in the E-sheet-labeled subdirectory, they total **2,565 TIFFs**. Adding the **22** PDFs gives **2,587** entries. All four groups have distinct full paths within each group. The archive also lists one PNG and nine directory entries. This test reads the ZIP central directory, not file bytes or drawing images. [Mirror ZIP](https://archive.org/download/911datasets/NIST_WTC7_FOIA_12-009.zip)

The [2012 requester account](https://www1.ae911truth.org/en/ptv-faqs/611-wtc-7-blueprints-exposed-via-foia-request.html) describes **2,523 TIFF fabrication sheets**, **42 TIFF erection sheets**, and **22 PDF erection sheets**. The mirror's directory labels, extensions and counts match those three reported group sizes. The labels do not independently classify all sheet contents, prove every file contains one sheet, or establish that the mirrored ZIP matches the original four disks byte for byte.

NIST's [December 2007 presentation](https://www.nist.gov/system/files/documents/2017/04/28/WTC7_Approach_Summary_18Dec07-Final.pdf#page=5) separately reports **2,565 acquired shop drawings**. The numerical match with all TIFF entries remains a lead: the presentation does not supply the 2007 item inventory or establish the scope of its label. Preserve the 2012 distinctions and NIST's wording rather than treating the counts as proof of an identical set. The previously documented differing 2001–2999 and 2001–3000 missing-identifier observations and completeness accounts remain unresolved. No deliberate omission or NIST holding of a particular missing sheet follows from this test.

## How to reproduce the check

Run `python3 verify_directory_groups.py /path/to/12-009.suffix.bin` on the previously captured **524,288-byte** ZIP tail whose SHA-256 is `a4d62dd226e97a30fa097f861d6491ef84e34451bd4a06f4f6c6e3759de3ca53`. The verifier refuses other bytes, opens the directory with Python's standard library, groups non-directory entries by their exact parent path, checks extensions and full-path uniqueness within each group, and reproduces the totals. It also checks one remaining PNG and nine directory entries. It does not extract or classify images. [Source and test pins](SOURCE-PINS.json)

## Open records

- [ ] Original 2007 transmission and sheet inventory; 12-009 four-disk manifests and any archive construction manifest; map identifiers, page content and versions across the sets.
- [ ] Complete Frankel register, missing fabrication sheets including A2682, and the original communications underlying the different completeness accounts. A missing basename is not proof a drawing was absent under every possible name.
- [ ] W14A field marks, measurements, custody and NIST attribution rationale. No piece-level identification or model calculation was performed here.

Public derivative of the November 6, 2026 UTC radar-member analysis. Native source bytes and full working results are preserved separately.

# Radar returns near Atlantic City do not yet identify ELKIN21

November 6, 2026 UTC · B129 / PD07 · Operational radar and clock comparison. Four raw radar members recovered from the public 84 RADES ZIP contain **34 Mode 3 code 4000 records within 25 nautical miles of Atlantic City International Airport** in the later comparison window. The same sensor logged that code at locations **11.82 nautical miles apart in the same encoded second**. The code and minute therefore cannot identify ELKIN21 on their own. The earlier window has no nearby returns of any code in the tested record families. These files provide no comparable local coverage control for the earlier departure claim. [Public radar ZIP](https://archive.org/download/911datasets/FAA_RADES_NORAD_FOIA_Data.zip) · [Source pins and byte locators](SOURCE-PINS.json)

## Observations kept separate

- **Tower strip, ACY-8, physical p. 2, bottom row.** The left field has **ELKIN** with a superscribed **21** and underlying ink. The adjacent entry appears to read **4000**, and the route area reads **Jersey Scramble**. Another strip higher on that page also appears to show **4000**. The form version, handwritten field meaning and code actually transmitted remain unverified. The later FAA order describes 4000 as a code usable in more than one circumstance, which supplies an additional reason to test for reuse. It does not establish the local 2001 assignment rule. [Tower strips](https://catalog.archives.gov/id/7599652) · [FAA beacon-code guidance, Assignment Criteria, raw HTML lines 508–509](https://www.faa.gov/air_traffic/publications/atpubs/atc_html/chap5_section_2.html)
- **TRACON strip, ACY-7, physical p. 20, top row.** It reads **ELKIN 21** and **2 F16**. The earlier machine screen of the South Arrival audio returned a possible call-sign match and rendered part of the passage as a single F-16. The two source readings and the uncertain identity of the underlying event remain separate. [TRACON strips](https://catalog.archives.gov/id/7599651) · [South Arrival audio screen](https://github.com/AveLyra/911-conspiracy-investigation/blob/16c6aab008b92abe56ef44c13c634ca5875162cc/investigation/broader-evidence/faa-acy-elkin21-voice-screen-2026-11-06/README.md)
- **Departure accounts.** Preserve the June **1428Z/1128L**, July **1528 UTC**, and handwritten **1528**. The voice candidate is bracketed by code readings **15:28:15–15:28:23**. No join between that recorded communication and a radar target has been verified. The radar file's encoded seconds are a separate timebase with an unverified correction and acquisition history. [June email](https://catalog.archives.gov/id/34911961) · [July response](https://catalog.archives.gov/id/34911953) · [Handwritten notes](https://catalog.archives.gov/id/7599650)

## Fixed search windows and results

The screen checks **14:23–14:38** and **15:23–15:38** by encoded whole second, excluding the upper endpoint, using the same 25-nautical-mile radius for each. It uses the modern FAA airport reference **N39°27.45′ W74°34.63′** for approximate geometry. The 2025 chart was read through the public index. The direct download returned HTTP 404. A spherical projection treats sensor range as a surface arc for this screen. No altitude or flight identifier is decoded. [FAA chart supplement, printed p. 160](https://aeronav.faa.gov/afd/07AUG2025/NE_160_07AUG2025.pdf)

| Raw member in WTC branch | Framed records, entire member | In-window records, supported types, all sites | In-window records within 25 nmi, any code | In-window 4000 within 25 nmi |
| --- | ---: | ---: | ---: | ---: |
| `12541400.RS3` | 289,543 | 3,844 | 0 | 0 |
| `12541430.RS3` | 250,794 | 3,198 | 0 | 0 |
| `12541500.rs3` | 238,504 | 1,354 | 23 | 22 |
| `12541530.rs3` | 241,039 | 1,528 | 95 | 12 |

All 34 near-airport code-4000 records come from **PLA**, whose footer identifies **J50 The Plains, VA**. They span **15:26:34–15:34:19** encoded time. Zero are within **5 nmi** and one is within **10 nmi**. At **15:28:22** the supported record with code 4000 is about **21.41 nmi** from ACY at member byte offset **6,044,624**. This is close in recorded time to the voice candidate and still lacks an identity link. At **15:28:57**, offsets **6,175,192** and **6,175,480** in the same member project about **11.82 nmi** apart. The coincidence could include separate aircraft or other observation effects. It establishes that multiple spatially distinct records carry the same code. [Member ranges and point locators](SOURCE-PINS.json)

The zero early near-airport rows occur despite 7,042 in-window records of the selected families across all sites. The four files have no missing encoded whole second within their respective extents when counted across all records. Neither of these checks supplies a per-site coverage guarantee. The data offer a test of code ambiguity and a list of candidates for comparison. They cannot distinguish an earlier local departure from incomplete coverage, an unsupported message family or another code.

## Reproduction and limits

The four HTTP 206 ranges matched the pinned outer ZIP ETag, total size, local member headers, filenames, lengths and ZIP CRCs. Each member also has its own SHA-256. The archive is a public mirror. The specific agency accession, radar product settings and clock correction history have yet to be joined to it. Same-named members in the other branches are kept separate. The prior labeled export was reused for two controls. Its rows **1146** and **1147** match raw offsets **877398** and **947486** in the WTC 14:00 member on PLA, whole second, Mode 3 **1527**, range and bearing. These two positive controls exercise the selected type 2 and 3 records. Their projected positions differ from the export by about **0.20 nmi**. They do not bound projection error or coverage near ACY. The export is from the same radar product family and does not independently authenticate the raw source.

With Python **3.14.0**, save the four payloads at the ranges in the manifest under their listed local basenames. Save the manifest's `members` object to a separate JSON file. Run:

```sh
python3 screen_acy.py members.json wtc-1400.rs3 wtc-1430.rs3 wtc-1500.rs3 wtc-1530.rs3
```

The script verifies CRC and SHA-256 and walks the length-framed members. It checks Mode 3 on the previously export-calibrated `(a, kind) = (7, 2) or (7, 3), b = 2` families only. The public reproducer matched the local output byte for byte. [Screen](screen_acy.py) · [Geometry and footer functions](rs3_reference.py)

## Open records and discriminating tests

- [ ] Locate the **ACY-12 ARTS text**, the original **ACY-10/11 DVRS** and the strip or facility code assignment legend. Seek a linked callsign, assigned and observed code, track identifier, timestamp field and altitude. A comparable track from a nearer radar with known local coverage could test the earlier and later windows without relying on this WTC branch alone.
- [ ] Obtain an independent transcription of the South Arrival clip and a shared event or clock record before measuring offset. Distinguish departure, first contact, handoff and later climb. The selected returns are insufficient to assign the strips, call sign or time to one track.
- [ ] The corrected FAA answer and acknowledgment, signed consideration or action/no-action decision and recommendation disposition under **PD01–PD04** remain open. This test concerns the separate regional record.

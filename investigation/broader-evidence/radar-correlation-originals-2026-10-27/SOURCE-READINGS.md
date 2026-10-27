# Source readings: NTSB production, radar correlation and FAA NTAP

Values below are analyst readings with exact physical page or original-file line locators. PDF pages have no native text layer; these reading-file line numbers are derivative. NTAP lines are one-based after lossless Latin1 splitting of the preserved bytes; the character encoding is not authenticated. No source bytes are corrected or normalized.

## RI01 — public letter, reader page1

July17,2003; NTSB Office of General Counsel; VIA HAND DELIVERY; Daniel Marcus, c/o Dana Hyde. The letter responds to the Commission's July2,2003 request. It says NTSB delivered factual information and technical products to the FBI and that the collected/produced materials were at all times under FBI control. Its request quotation includes raw radar files and NTSB analysis. Footnote1 limits NTSB's account to the aircraft-data part; it says NTSB did not investigate or collect separate records about the government's air-defense response, aside from records already being provided for the first part. This is a claim about that agency's work, not proof the government as a whole had no such records.

## RI02 — public letter, reader page2

The letter says the FBI authorized NTSB that day to provide Commission copies of material NTSB had delivered to the FBI. It references the Moussaoui-related nondisclosure agreement, and excepts a copy of the UA93 CVR recording and an early working draft of its transcript from this NTSB delivery. Footnote2 says FBI possessed the original CVR tape and final transcript draft and would respond to Commission requests. It also says some delivered products incorporate FBI transcript information. Signature image and typed name read Ronald S. Battocchi, General Counsel. The image is a hosted derivative; no native signature authentication or recipient receipt has been acquired.

## RI03 — inventory printed02/21/2002, reader page3 / inventory1of3

UA93 header: DCA01MA065. AA77 header: DCA01MA064. The AA77 rows read:

| Product | Staff | Format | Status | Description |
| --- | --- | --- | --- | --- |
| Animation (AA77) | Grossi/Johnson | copy to DVCAM, DVD, and VHS | complete | RAPS animation with ATC radio transmission text |
| ATC .wav file (AA77) | Gregor | 1 cdrom | complete | recording of all radio sounds to/from subject airplane, single time base |
| ATC Transcript (AA77) | Gregor | report | complete | transcript of all radio sounds to/from subject airplane, single time base |
| FDR “RAPS” Project file (AA77) | Cash | 1 cdrom | complete | project file for FDR readout on RAPS software |
| FDR Data Tables - AA77 | McComb | report | complete | tabular FDR data |
| FDR Factual Report - AA77 | McComb | report | complete | Plots and tabular data of pertinent parameters |
| Flight Path Description Study (AA77) | Ritter | report | complete | Brief flight history, based on FDR, radar, and ATC transcript |

These are inventory rows, not acquired CD contents or confirmed individual delivery receipts. The web text's VMS rendition differs from the visually read VHS; that rendition mismatch is kept separate from a source-record contradiction.

## RI04 — inventory reader page4 / inventory2of3

Miscellaneous rows include ACARS data for all aircraft (Ritter, paper, complete, airline printouts); Autoflight/Navigation Equipment Activity (UA93+AA77), O'Call/Bower, report, complete; FAA ATC paper transcripts and cassette tapes, Rowlett/Gregor/English, paper reports/tapes, complete, described as a box of FAA material; and FBI nondisclosure forms, Cash, paper, complete, for those with access to UA93 CVR information. Inventory3of3 remains unacquired as a page image: its text-extracted Bower-study and two-radar-CD rows are still qualified locators, not visually verified here.

## RR01 — official radar study, physical/printed page1

February15,2002; Recorded Radar Data Study; four flight names; Daniel R. Bower, Ph.D. AA77 is identified as Boeing757-200, N644AA, DCA01MA064. AA11/UA175/UA93 use DCA01MA060/063/065. The subject-aircraft time fields say Eastern Daylight Time.

## RR02 — radar page2, Summary and Data Sources

The study describes a general overview of time correlation and time-synchronized ground tracks. It lists FAA NTAP from New York, Washington, Boston and Cleveland ARTCCs; USAF84thRADES ARSR; and ASR from airport TRACONs. ASR is described as recording approximately every4½seconds and ARSR every12seconds. Positional accuracy decreases with radar distance; the report says an effort was made to align data sets. These are reported method/nominal cadence claims, not measurements from our acquired NTAP subset.

## RR03 — radar page3, clock paragraphs

“the time of day used as the standard time is from the USAF 84th RADES data”

“The 84th RADES found that the clock for the North East Air Defense Sector (NEADS) lagged the clocks for the other sectors by 25.3 seconds.”

“The other sectors were all in agreement with the Global Positioning Satellite (GPS) time. Therefore, 25.3 seconds must be added to the radar data from the 84th RADES.”

The next paragraph says Washington, Cleveland and Boston NTAP required no offset; New York NTAP had an8second offset corrected to align with RADES and other NTAP centers. It does not state the New York correction's sign in this paragraph. Preserve25.3 and8 with these scopes, not as a universal audio-clock correction.

## RR04 — radar page4, SectionII Time Correlation

“Times indicated with the USAF RADES radar data were used as the reference time, and the FDR and ATC clocks were adjusted accordingly.”

The first paragraph says: “HH:MM:SS Eastern Standard Time (EST).”

The next paragraph describes comparing radar altitude versus local time with FDR altitude versus elapsed time using “a single anchor point,” with “a specified number of elapsed seconds on the FDR = 00:00:00 EDT.” It says the anchor differs for each FDR and is further verified by ATC radio callouts and FDR microphone keying.

The following paragraph says: “All the FDR and radar data in this report are given in the correlated local time (EDT).” It refers to FDR factual reports. EST and EDT are both present in this method section; the cause of that label difference has not been adjudicated. No numerical per-recorder anchor, residual table or drift uncertainty is supplied in this inspected method section. The parenthetical aircraft label in the comparison sentence appears UAL83, while the report's headings and references identify UA93; retain the image rather than replacing that character reading with an inferred intended label.

## RR05 — radar page4, primary-target accuracy and dataCD

The preceding paragraph gives published radar-derived primary-height root-mean-square accuracy as+/-3000feet for specially modified ARSR antennas and discusses AA11 after transponder altitude ceased. This is not the error bound for all altitude channels, AA77 radio height or clock time. SectionIII says recorded radar data are on a CD-ROM with per-flight, source and combined directories. A PDF directory list is not the CD itself.

## RR06 — radar pages5–8, selected source-file paths

Page5 shows per-flight directories. Page6 lists `crw91101.txt` under AAL77. Page7 lists `AAL77 DCA ASR 1300 to 1400.txt`, `AAL77 IAD ASR 1210 to 1400.txt`; processed entries include `Aal77 back converted - don't use D targets.urf`, `Aal77 export from RS3.rad`, `aal77 export from RS3.txt`; ZDC entries include `Aal77 zdc 1320 to 1339.txt`, `aal77a zdc 1303 to 1321.txt`, `Aal77a1 zdc 1258 to 1306.txt`, `Aal77a2 zdc 1256 to 1302.txt`, `Aal77a3 zdc also 1256 to 1302.txt`, `Aal77c zdc 1220 to 1249.txt`, `ZDC AAL77 NTAP 6553 code.txt`; ZID entries include `AAL77 zid 1234 to 1258 beacon only.txt`, `ZID AAL77 beacon only.txt`, `ZID AAL77 prim1.txt`, `ZID AAL77 prim2.txt`, `ZID AAL77 prim4.txt`, `ZID bad NTAP.txt`. Preserve literal names without interpreting “bad,” “filtered,” “trimmed” or “don't use” as misconduct. Page8 also names `RADES timeline.doc` and combined/filtered exports. These specific original file contents and transformation definitions are unacquired; no exact join to NARA7596008 is established.

## RR07 — radar page11, SectionIV Ground Tracks Description

It says radar data were supplemented with FDR information where available and plots are overlaid on a simplified map. It defines dotted lines as entire flight paths and solid lines as the specified15minute interval. Neither style is a point-by-point proof of continuous raw radar coverage. The paragraph's flight list includes United Airlines Flight175 twice, while its headings and figures include United93. This is a preserved textual discrepancy, not proof a track was swapped.

## RR08 — radar page12 and figures13–21

Typed author is Daniel R. Bower, Senior Aerospace Engineer; the signature area has a black obscuration already present in the acquired agency PDF. We did not remove, reinterpret or authenticate it. Pages13–21 are map figures seen here in overview; their pixel positions/terminal trajectories were not digitized and do not supply our independent clock measurement.

## NR01 — official NARA item and downloaded bytes

NARA7596008, RG237, series7419198, file unit7595854, agency-assigned identifier `1 ZID 48 ntap AAL 9-11-01.txt`. Catalog says Files Available for Download, ASCII Text37KB; Use:Unrestricted; Access:Possibly Restricted, explaining some series files have FAA redactions. The public link supplied37,242 bytes, hash5409296c7834e0e834f201e6b78bc43042a2920053af49c243384ded9a5f3f0e. That file has489 physical lines, five non-ASCII bytes (0xb8once;0xb3four times),16NULs and terminalCtrlZ. These bytes remain unchanged. A broad catalog media label is not an authenticated strict7bit encoding specification; no tampering inference is made.

## NR02 — NTAP lines20–40,63,81,86,93–98

TapeID isID1635; program `NTAP`, version`1.1-0 00.192`; line63 reports `STEP WAS EXECUTED - COND CODE 0000`. Line93 says `CODE ADD 3743 6553`. Lines95–96 report `FORMAT ERROR ON THE FOLLOWING CARD -` / `ALTLIM`. Line97 requests `PLOT 123400 125800`; line98 reports tape start1234:32greater than requested plot start1234:00. Do not equate condition0000 with all input cards being accepted, or the warning with all output being invalid. Source code, control-card semantics and job/operator follow-up remain missing.

## NR03 — NTAP lines119–121,381–433,437–489

Header line119 prints `PLOT DURATION 1409` and `DATE 09/12/01`; line121 gives start1234:32 and stop1258:00. The elapsed label difference is1408seconds, but the duration field's unit/inclusivity convention is unverified, so no one-second clock error is declared. The processing date is not automatically the event date.

Lines381–433 are the LST3 chronological plot list. The parser finds94 numeric-code entries:80for3743 from1240:34to1256:19, and14for6553 from1237:43to1240:10. Five fixed-point labels and a separate `D FIRE` plot row remain outside that numeric-code count and are preserved as source text. FIRE is not established to mean physical fire. LST1/2/4 repeat or summarize representations of this job's data; they are not additional independent samples.

Code3743successive printed intervals:72at12seconds,2at13seconds,5at11seconds. Code6553:11at12seconds,1at11seconds,1at4seconds. These are label intervals within a selected print list, not calibration, proof of complete radar coverage or evidence that a missing return was deleted. The numerical ALT field is retained raw; its units and physical sensor/identity joins remain unverified.

The raw input states neither UTC/EDT/EST in searchable text. No timezone conversion,25.3second correction, calibrated fit, exact impact time or independently authenticated aircraft identity is inferred from the filename or code alone.

## NR04 — our failed parser control and repair

The first parser run failed because our last-row control wrongly named line435; the original data put it on433. Its end marker also included three next-section header lines. The failed script/receipt remain preserved; v2 fixes those two locations without changing expected values, source hash or acceptance tests. This is an analyst error, not an anomaly in the evidence. Two parsing methods then matched all94 tuples and all4source-row controls; matched byte spans were checked. This verifies extraction only.

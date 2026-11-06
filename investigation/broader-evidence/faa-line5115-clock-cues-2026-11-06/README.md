> Public research derivative of the Command Center line 5115 waveform comparison.

# Locating 8:35 a.m. on the Command Center line 5115 recording

November 6, 2026 UTC · B129 / PD07 · Atlantic City enclosure follow-up

Three public excerpts match portions of the National Archives' **line 5115** audio. Two ways of bracketing the **8:35 a.m. EDT** search target from their published labels place it around **21:34–21:36 into the MP3**. This is a search location, conditional on the excerpt timestamps and interpolation. The recording is a Command Center line. The Atlantic City Tower recording and the destination of the reported Boston Center attempt remain open. [NARA line 5115 object](https://catalog.archives.gov/id/7598742) · [July 7 transmittal](https://catalog.archives.gov/id/7601902)

## Matched excerpts and clock bracket

The source was the **1215–1415 UTC** MP3, 235,725,431 bytes, SHA-256 **27eb01802a6ff6c0c75f2046ec10ec5d4052bf783dfb9df617cba5e2a4bfb71e**. The Rutgers transcript pages supply an embedded MP3 for each excerpt. The published number in each filename is a source label. The matching code estimates where the excerpt begins on the archive file's playback timeline.

| Published label | Median estimated MP3 offset | Refined normalized absolute correlation | Source |
| --- | ---: | ---: | --- |
| **082924**, Boston Center notification to Cleveland/New York, labeled **5115** | **948.689 s** | **0.281–0.296** over three separated templates | [Excerpt 11](https://rutgerslawreview.com/wp-content/uploads/special/911/html/%2811%29%20082924%20AA11%20ZBW%20Notification%20ZOB%20ZNY%205115%20Line.html) |
| **083053**, Command Center summary to unidentified facility, labeled **5115** | **1036.872 s** | **0.230–0.348** over three templates | [Excerpt 12](https://rutgerslawreview.com/wp-content/uploads/special/911/html/%2812%29%20083053%20AA11%20Pascione%20Summation%20to%20Unknown%205115%20Line%20.html) |
| **083940**, Boston Center and New York TRACON, Sparta reference | **1585.317 s** | **0.240–0.330** over three templates | [Excerpt 17](https://rutgerslawreview.com/wp-content/uploads/special/911/html/%2817%29%20083940%20ZBW%20TRACON%20by%20Sparta.html) |
| **090608**, confirmation excerpt, labeled **5114** | **3135.281 s** on the **5115** MP3 | **0.496** over one short template | [Excerpt 47](https://rutgerslawreview.com/wp-content/uploads/special/911/html/%2847%29%20090608%20AA11%20Confirmed%20on%20Tape%20We%20Have%20Planes%20Line%205114.html) |

- **Interpolation.** The **082924–083940** pair places **0835** at **1295.940 file s**. The **083053–083940** pair gives **1293.923 file s**. These two estimates are conditional, share their later anchor, and do not constitute a confidence interval. The published labels have whole-second precision. The decimal offsets locate audio samples for replication.
- **Timing rate.** For the two bracketing fits, playback seconds per elapsed label second were **1.03349** and **1.04069**. The shorter **082924–083053** interval was **88.184 playback seconds** for **89 label seconds**. Preserve both observations. The matching scales, local elapsed fits and original clock calibration measure different things. Differing copy speeds, label placement, excerpt editing and source discontinuities remain untested as explanations.
- **Target screen.** Left-channel speech recognition on **1230–1322 s** and **1320–1405 s** produced no usable speech for the Boston Center lead. This is a negative screening result for the model, with no claim of silence, absence or call completion. The separate Sparta probe at **1582–1642 s** returned Boston Center, New York TRACON and the Sparta cue. Independent human transcription and a tower or switch record are still needed.

## Conflicting channel and duration evidence

**Line designation.** Rutgers labels the **090608** excerpt **5114**, while its nearby 9:05 footnote identifies **5115**. The Commission's final report notes **132–133** cite line **5115** at **9:05** and **9:05–9:07**. The waveform test places the excerpt on the archived **5115** object. This does not identify which line supplied Rutgers' clip, or whether the same exchange was recorded on both. The other public object, **DCC-1938** for **5114**, **1215–1415 UTC**, is a direct next test. [Rutgers section, clip and note xx](https://rutgerslawreview.com/5-united-175/) · [Commission notes 132–133](https://www.911commission.gov/report/911Report_Notes.htm) · [Line 5114 object](https://catalog.archives.gov/id/7598795)

**Duration and timing signal.** The child MP3 is labeled **1215–1415 UTC**, while the parent cassette inventory and machine reading of the spoken introduction give **1215–1515**. Its FFprobe duration is **7366.351750 seconds**. The right channel in five-second windows at **90**, **1200** and **3600 file seconds** has dominant peaks at **100.0**, **99.4** and **99.2 Hz**, respectively. The short sample near 90 seconds has near-symmetric pulses of about **5 ms** at a zero crossing. The prior two brief probes accepted no Format B timing frames with the ACY-13 settings. These checks identify signal features. The oscillator source, physical tape speed, code format and UTC calibration remain open. [Prior acquisition and timing probe](https://github.com/AveLyra/911-conspiracy-investigation/blob/d409488fe3846239e7a29cac62ecf7d174a07bf3/investigation/broader-evidence/faa-acy-headquarters-transmittal-2026-11-06/README.md)

## Reproduction and controls

Both Python scripts require NumPy and SciPy and use FFmpeg **7.1.1** to decode the archive's left channel and the four mono clips. Source hashes and exact URLs are in [SOURCE-PINS.json](SOURCE-PINS.json). Download each Rutgers embed to the named clip file.

```sh
python3 MATCH-WAVEFORMS.py DCC-1912-1215-1415.mp3 EXCERPT_DIRECTORY > matches.json
python3 REFINE-MATCHES.py DCC-1912-1215-1415.mp3 EXCERPT_DIRECTORY matches.json
```

The coarse scan bandpasses **320–1650 Hz** at **4 kHz**, searches declared windows with nine time scales, and uses eight-second templates for the first three clips and a 2.7-second template for the last. Refinement searches smaller offset windows and a finer scale grid. Three templates in each longer clip yield candidate starts within **0.185 s** of one another. On the coarse search, the short **090608** template peaks at **0.385** in its expected window, with **0.147** elsewhere at the winning scale outside the two-second exclusion. An early-window negative control peaks at **0.144**. The refinement's local window does not supply a meaningful second-peak control. The finite search and selected templates do not authenticate the full contents of either line.

## Open TODOs

- [ ] Compare the 090608 excerpt with the exact **DCC-1938 / 7598795** line 5114 object. Test whether the exchange survives on both channels and check each source's title, certification and timing.
- [ ] Recover a recorder specification or calibrated timing reference and the original cassette or independent transfer. Compare the clocks and gaps before assigning exact UTC to the target. Review the target interval by listening and compare with a Boston-side or Atlantic City record.
- [ ] Locate **ACY-14/15**, source DVRS/ARTS, Commission intake and the separate **Form 7230-4**. The conflicting ELKIN21 times remain open.
- [ ] Retain the actual corrected May 2003 QFR and receipt, signed administrative disposition and recommendation-specific response and closure as open under **PD01–PD04**.

The report preserves the excerpt labels, archive title, speech-screen scope and source dependence. The archive and excerpt audio bodies were retained in the Intel store. The public derivative contains prose, the decoder comparison scripts and provenance metadata. [Source pins and results](SOURCE-PINS.json)

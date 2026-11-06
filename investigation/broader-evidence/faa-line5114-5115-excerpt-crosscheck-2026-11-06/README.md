> Public research derivative of the two-line audio comparison.

# The 9:06:08 confirmation excerpt matches both archived Command Center lines

November 6, 2026 UTC · B129 / PD07 · Follow-up to the line 5115 excerpt comparison

The short Rutgers **090608** confirmation excerpt has a waveform counterpart in both the archived **5114** and **5115** recordings. The match appears at approximately **3156.356 seconds** on the line 5114 MP3 and **3135.281 seconds** on the line 5115 MP3. The archives therefore provide two recordings on which to test the exchange. The published Rutgers label and the Commission's citation remain separate, and the waveform comparison does not identify which copy Rutgers used to make its excerpt. [Rutgers excerpt 47](https://rutgerslawreview.com/wp-content/uploads/special/911/html/%2847%29%20090608%20AA11%20Confirmed%20on%20Tape%20We%20Have%20Planes%20Line%205114.html) · [NARA line 5114](https://catalog.archives.gov/id/7598795) · [NARA line 5115](https://catalog.archives.gov/id/7598742)

## Provenance and the labels to preserve

| Record | Observed designation and scope |
| --- | --- |
| **Rutgers UA175 page**, strings **114** and **205** | The **090608** clip link says **line 5114**. Nearby note **xx** cites Command Center **Position 15, line 5115, at 9:05**. [Rutgers UA175 section](https://rutgerslawreview.com/5-united-175/) |
| **Final Commission notes 131–133** | Note **131** cites the New York Center position, **5114**, at **9:02:34**. Notes **132–133** cite the Cleveland/Boston or Boston Center position, **5115**, at **9:05** and **9:05–9:07**. The source labels and the Commission's citation intervals are retained as written. [Commission notes](https://www.911commission.gov/report/911Report_Notes.htm) |
| **NARA DCC-1938 / 7598795** | Finding aid Box **28**, rows **963–966**, identifies the parent cassette **5114 / Position 14 East Area / 1215–1630 UTC** and the first digital child **1215–1415 UTC**. The acquired **236,193,545-byte** MP3 repeats the child designation in its title. FFprobe **7.1.1** gives stereo **44.1 kHz** and **7380.980313 s** playback. The two-hour title range is **7200 s** by endpoint subtraction. A provisional ASR reading of the **0–80 s** introduction gives **1215–1630** for the overall frame and **1215–1315** for the side, with **Position 14 East Area**. The three ranges have different stated scopes. [Finding aid](https://www.archives.gov/research/foia/faa-finding-aid-24-35) · [Archived child](https://catalog.archives.gov/id/7598795) |
| **NARA DCC-1912 / 7598742** | Separately retained **5115 / Position 15 / 1215–1415 UTC** child. Its **7366.351750 s** playback and parent/leader **1215–1515** label remain as previously recorded. The two MP3s have different lengths and SHA-256 values. The offsets are file locators, with no shared UTC calibration implied. [Archived child](https://catalog.archives.gov/id/7598742) · [Previous comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/62a832b36f0d7c7bd32c0956432c263495669f9a/investigation/broader-evidence/faa-line5115-clock-cues-2026-11-06/README.md) |

## Waveform comparison and controls

The script searches **2910–3350 file seconds** on each left channel, using the prior method's **320–1650 Hz** band at **4 kHz** and nine coarse resampling scales. It then refines each best candidate in a small window. Each reported offset estimates the excerpt's start by subtracting the scaled template offset. Local refinement increases the correlation and does not serve as an independent control.

| Excerpt and window | Line 5114 | Line 5115 |
| --- | --- | --- |
| **090234**, two seven-second templates | Estimated starts **2941.240 / 2941.227 s**. Refined correlations **0.386 / 0.362**. | **2921.012 / 2920.989 s**, **0.350 / 0.213**. [Excerpt 44](https://rutgerslawreview.com/wp-content/uploads/special/911/html/%2844%29%20090234%20AA11%20Jones%20thought%20some%20planes%20as%20in%20plural%20Line%205114.html) |
| **090322**, two seven-second templates | **2989.873 / 2989.882 s**, **0.357 / 0.403**. | **3127.185 / 2969.231 s**, **0.125 / 0.286**. The first template's weak peak disagrees with the second by about **158 s** and is not a usable match. [Excerpt 45](https://rutgerslawreview.com/wp-content/uploads/special/911/html/%2845%29%20090322%20AA11%20Nother%20One%20Just%20Hit%20Line%205114.html) |
| **090608**, 2.7-second template starting **0.35 s** into the excerpt | **3156.356 s**, refined **0.549**. Coarse peak **0.293**, off-target peak **0.157** at the winning scale. | **3135.281 s**, refined **0.496**. Coarse peak **0.385**, off-target peak **0.147** at the winning scale. [Excerpt 47](https://rutgerslawreview.com/wp-content/uploads/special/911/html/%2847%29%20090608%20AA11%20Confirmed%20on%20Tape%20We%20Have%20Planes%20Line%205114.html) |
| **090608 wrong-window control**, **820–1080 s** | Coarse peak **0.098**. | Coarse peak **0.144**. |

The **090608** estimated starts differ by about **21.075 playback seconds** between objects. A provisional local speech screen of the 5114 audio at **3090–3240 s** recovered the confirmation phrase near that waveform location. The prior 5115 speech screen also recovered it near the corresponding location. The **090234** pairs provide an additional match across the two lines, while the failed first **090322** template shows why template results must be preserved individually. There was no manual transcript authentication, and these scores do not establish transmission routing, physical clock offsets or independence of the two audio copies. Shared reception, copying and later excerpt selection remain separate possibilities.

## Reproduction

Use Python, NumPy, SciPy and FFmpeg **7.1.1**, with the pinned prior matcher and the exact source bytes listed in [SOURCE-PINS.json](SOURCE-PINS.json).

```sh
python3 COMPARE-TWO-LINES.py MATCH-WAVEFORMS.py DCC-1938-1215-1415.mp3 DCC-1912-1215-1415.mp3 CONTROL_EXCERPT_DIRECTORY excerpt-090608.mp3
```

[Prior matcher at its immutable commit](https://github.com/AveLyra/911-conspiracy-investigation/blob/62a832b36f0d7c7bd32c0956432c263495669f9a/investigation/broader-evidence/faa-line5115-clock-cues-2026-11-06/MATCH-WAVEFORMS.py)

## Open TODOs

- [ ] Obtain the original digitization/cassette lineage and Rutgers excerpt export or edit record to identify the excerpt's source copy. Compare independent time references, source audio and switch or bridge records before assigning routing or clock offsets.
- [ ] Obtain and align the remaining Command Center children as needed. Retain the earlier **0835 EDT** Atlantic City inquiry and its unverified destination, the actual **ACY-14/15** tower recordings, the source DVRS/ARTS, Form **7230-4** and Commission intake as distinct open dependencies.
- [ ] Retain the corrected **May 2003 QFR**, delivery and receipt, signed administrative disposition and recommendation-specific response and closure as open under **PD01–PD04**.

The newly acquired archive MP3 and two control clips are retained separately. The public payload contains only the study, reproduction script and source/verification pins. [Source pins and per-template results](SOURCE-PINS.json)

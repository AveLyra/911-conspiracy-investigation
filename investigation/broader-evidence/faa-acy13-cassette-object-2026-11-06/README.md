> Public research derivative of the ACY-13 object study.

# The ACY-13 cassette copy carries two clock sequences

November 6, 2026 UTC · PD07 / B129 · Atlantic City production and recording custody

The National Archives' **ACY-13** MP3 preserves a decodable timing signal on its right channel. It advances through a first sequence, then returns to an earlier time for the second. The two sequences match the **Clearance Delivery** and **Ground Control** label windows to the printed minute. Within the second sequence, two successive frames give the same **13:15:00** label. This is a result about the archived copy's timing track. The original recorder clock, its accuracy and the cause of the repeated label remain open. [NARA item and download](https://catalog.archives.gov/id/7598655)

## Source observations and measured fields

| Record or test | Observation |
| --- | --- |
| **Box 4 inventory**, PDF p. **12**, row **ACY-13** | Labels Clearance Delivery **1257–1318** and Ground Control **1302–1318**. The MP3 title tag repeats these intervals and adds **UTC**. The July 16 memo describes the two positions and an outer window of **1257–1318 UTC**. [Inventory](https://www.archives.gov/files/faa-inventory.pdf#page=12) · [July 16 memo, PDF p. 1, lines 18–21](https://catalog.archives.gov/id/7599649) |
| **Preparation sheet**, ACY-6 physical p. **1**, circled intervals and lower-right sum | Gives **1257–1318** and **1302–1318**. Its handwritten arithmetic reads **21 + 15** and **36 mins**. Subtracting the printed clock endpoints yields **21 + 16 = 37 minutes** if summed as two windows. This calculation and the handwritten total have different evidentiary roles. Preserve both. [Preparation sheet](https://catalog.archives.gov/id/7599650) |
| **Archived MP3** | **76,665,194 bytes**, SHA-256 **1b82e4f3df0d60c2c370c7bddeb8a426b136a9bcaea83e147740ac00f88efa3f**. FFprobe 7.1.1 reports **2395.719906 s**, two channels at **44.1 kHz**, and one audio stream. A strict FFmpeg decode yielded **105,651,072** stereo sample pairs. The **91,711** packet timestamps were contiguous on FFprobe's MP3 playback timeline. Those timestamps do not establish continuity of the source recorder. The file duration, the label-derived sum and the handwritten sum remain separate. [Download record and provenance](SOURCE-PINS.json) |
| **Speech screening on the left channel** | A local ASR screen of file offsets **0–72 s** returned a rerecording introduction, Clearance Delivery followed by Ground Control, and the **1257–1318 UTC** Clearance Delivery window. A screen of **1352–1398 s** returned the Ground Control announcement and **1302–1318 UTC**. A screen of **2375 s to the end** returned an end announcement. The speech screen supplies provisional segment cues. Its wording and boundaries are machine-derived and have not been independently transcribed. The report publishes no transcript. [Archived MP3](https://catalog.archives.gov/id/7598655) |

## Decoded right-channel result

The candidate tone near file offset **110 s** peaks near **982 Hz** over a four-second Fourier window. The envelope shows three pulse-width bands and the expected Format B marker pattern. The decoder uses binary-coded decimal day, hour, minute and second fields. The later FAA maintenance handbook describes voice on the left and IRIG-B on the right in cassette copies. The handbook describes the copy format. Its 2008 publication date limits its use as evidence of the exact 2004 configuration. [RCC 200-16, Format B, PDF pp. 36–39](https://www.trmc.osd.mil/wiki/download/attachments/113019842/200-16_IRIG_Serial_Time_Code_Formats.pdf?api=v2&modificationDate=1623181164717&version=1#page=36) · [FAA JO 6670.13A, PDF p. 32, lines 18–20](https://www.faa.gov/documentLibrary/media/Order/6670.13A2.pdf#page=32)

| Sequence | Accepted frames | File offsets and decoded endpoints |
| --- | ---: | --- |
| First, consistent with Clearance Delivery | 1,284 | **64.202 s**, day 254 **12:57:09** through **1364.513 s**, day 254 **13:18:32** |
| Second, consistent with Ground Control | 992 | **1384.834 s**, day 254 **13:02:20** through **2384.971 s**, day 254 **13:18:50** |

Day **254** corresponds to September 11 in the label's year, **2001**, which was a common year. The decoder did not authenticate a year field or an external UTC reference. The two accepted frames across the transition are **20.321 file seconds** apart, with the coded reading going back **16 minutes 12 seconds**. This is consistent with sequential copies of two overlapping source windows. The internal duplicate is at file offsets **2152.366 s** and **2153.373 s**. It preserves two **13:15:00** readings about **1.008 file seconds** apart. Among accepted frames within these spans, all other adjacent pairs advance one coded second. Frame detection was threshold-dependent. The analysis makes no claim about undecodable leader, transition or tail content.

The median file interval per one-second code step is **1.01333 s** for the first sequence and **1.00946 s** for the second. These are playback-to-code measurements. They matter if an analyst is tempted to treat MP3 seconds as source-clock seconds across the file. The decoded marker sample indices are reproduction locators. They do not give millisecond accuracy for the original event. A clock or tape-speed explanation is untested.

## Reproduction and controls

Use the exact MP3 pinned in [SOURCE-PINS.json](SOURCE-PINS.json), FFmpeg **7.1.1**, Python and NumPy. The first command streams right-channel PCM into a 35-sample RMS envelope, checks the Format B marker pattern and reads the BCD fields. The second validates the output and tests independent synthetic and channel controls.

```sh
python3 DECODE-TIME-TRACK.py ACY-13.mp3 > acy13-frames.json
python3 VERIFY-DECODE.py ACY-13.mp3 acy13-frames.json
```

- Thresholds **0.22** and **0.25** accepted the same **2,276** coded labels in the same order. Their marker indices differed by at most **two samples**. Threshold **0.18** accepted only **195** frames. Decoder rejection at that threshold is an analysis effect.
- Two synthetic frames with the expected BCD fields decoded correctly. A synthetic frame sequence with a damaged position marker yielded zero accepted frames. At file **110–130 s**, the same check returned **zero** left-channel frames and **19** right-channel frames.
- The additional container check used `ffprobe -show_entries packet=pts,duration` and strict `ffmpeg -xerror -err_detect explode` decoding. This verifies digital readability of the pinned object. It does not authenticate the upstream recording or exclude changes before digitization.

## Open TODOs

- [ ] Find the original **ACY-13** cassette or a separately sourced transfer, its digitization record, and the original DVRS timebase and calibration. Compare the **13:15:00** pair with the source signal and with independently timed events. Preserve the repeat until those inputs can distinguish an upstream clock label, a replay/copy artifact or another mechanism.
- [ ] Seek **ACY-14/15**, original **ACY-10/11** DVRS and the **ACY-12** ARTS export. Those items could test the later **1430 UTC** lead and the conflicting ELKIN21 entries. ACY-13's decoded windows precede both candidate ELKIN21 departure times.
- [ ] Locate the 2004 dispatch and intake record and the distinct **Form 7230-4**. The **May 2003 corrected answer**, its delivery, signed administrative disposition and recommendation-specific implementation or closure remain open under **PD01–PD04**.

The local research preserves the archived MP3, public technical references, raw frame outputs and limited ASR screening separately from this derivative. [Prior inventory and log review](https://github.com/AveLyra/911-conspiracy-investigation/blob/6688af5d11ffe4a9448ccfe4b9ca0f2301d33ce1/investigation/broader-evidence/faa-atlantic-city-position-logs-and-tape-labels-2026-11-06/README.md)

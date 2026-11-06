Public derivative of the November 6, 2026 UTC cassette-photo and clock-track analysis. The research original and source bytes are preserved separately.

# Both cassette-side labels appear in the Atlantic City clock sequences

November 6, 2026 UTC · B129 / PD07 · Atlantic City operational recording custody. The archive's MP3 titles name Arrival Data/Departure Data and Ground Control. The corresponding cassette photos also identify **South Arrival** and **Local Control** on side B. In each MP3 the right-channel timing code advances through a sequence near the side A window, jumps backward and then advances through a sequence near the side B window. This supports a two-side transfer reading for each file and supplies playback locations for the previously unlocated positions. The catalog labels, cassette stickers and decoded endpoints are preserved separately. [Box 115 finding aid, lines 2360–2365](https://www.archives.gov/research/foia/faa-finding-aid-108-126#:~:text=AEA%20%232310) · [Prior acquisition and durations](https://github.com/AveLyra/911-conspiracy-investigation/blob/2b01738ea4a5340767f84058effa1cfdf1dc49a0/investigation/broader-evidence/faa-millville-log-and-later-acy-recording-routes-2026-11-06/README.md)

## Photos, file names and decoded fields

The newly acquired **NAID 7600782** PDF shows both stickers on physical pp. **1–2**. In **NAID 7600783**, the previously acquired Ground Control photo is p. **1**, and the Local Control sticker is on p. **2**. Both cassettes show a separate **120 min** manufacturer marking. The Box 4 inventory independently lists the same channel pairings and minute labels as **ACY-15** and **ACY-14**. The source dependence of these labels and the identity of the physical copies remain open. [ADDD/SAR cassette](https://catalog.archives.gov/id/7600782) · [GC/LC cassette](https://catalog.archives.gov/id/7600783) · [Box 4 inventory, p. 12](https://www.archives.gov/files/faa-inventory.pdf#page=12)

| MP3 / sequence | Cassette sticker | Accepted code endpoints at threshold 0.35, day 254 | Playback bounds of accepted endpoints |
| --- | --- | --- | --- |
| **AEA #2310**, NAID **7598687**, first | A · **ADDD (1425–1531 UTC)** | **14:25:28–15:32:07** | **16.400–3929.211 s**, 3,028 accepted frames |
| **AEA #2310**, second | B · **SAR (1447–1530 UTC)** | **14:47:15–15:30:35** | **3931.353–6502.388 s**, 2,598 accepted frames |
| **AEA #2311**, NAID **7598688**, first | A · **GC (1425–1525 UTC)** | **14:25:40–15:27:35** | **67.383–3791.993 s**, 3,702 accepted frames |
| **AEA #2311**, second | B · **LC (1447–1536 UTC)** | **14:47:06–15:36:36** | **3811.818–6779.912 s**, 2,967 accepted frames |

The two printed side spans add to **109 minutes per cassette**, counting their overlapping source times separately. The MP3s decode to **108:39.327** and **113:01.884**. The second sequences provide evidence for additional recorded content beyond the single window in each MP3 title. The decoded ranges and nominal sums still differ. Keep **15:31** beside **15:32:07** for ADDD, and **15:25** beside **15:27:35** for GC. The **13-second** low-peak interval previously measured at **3734–3747 s** in AEA #2310 precedes the detected clock rollback. It remains a separate observation. [Audio 7598687](https://catalog.archives.gov/id/7598687) · [Audio 7598688](https://catalog.archives.gov/id/7598688) · [Prior amplitude scan](https://github.com/AveLyra/911-conspiracy-investigation/blob/8bda8b7c0179c19a3c3ba7c9646aa6e90f76d2c5/investigation/broader-evidence/faa-acy-recording-segmentation-2026-11-06/README.md)

## Clock checks and locating audio

- **Reproducible rollbacks.** At threshold **0.35**, the accepted code steps backward by **44 min 52 s** in AEA #2310 across **2.142 playback s**, and by **40 min 29 s** in AEA #2311 across **19.825 playback s**. Both files have two coherent sequences at thresholds **0.32, 0.35, 0.38 and 0.42**, with different rejection rates and endpoints. At **0.46** the detector accepts only one sequence in AEA #2311 and very few frames in the second AEA #2310 sequence. Left-channel controls at **0.32, 0.38 and 0.42** accepted zero frames in either file. Rejection counts measure detector behavior and cannot establish gaps in the original recording.
- **Repeated code in Ground Control.** At **0.35** and **0.38**, two successive accepted frames give **15:19:37**, about **1.005 playback s** apart, at **3310.638 s** and **3311.643 s**. The **0.32** run did not produce an adjacent equal-label pair. This is a repeated timing label in the decode. A separate test would be needed to distinguish a source-clock label from a replay, transfer or decoding effect.
- **Event candidates.** At **0.38**, AEA #2310 gives code **15:28:00** at playback **3715.543 s** in the first sequence and **6348.486 s** in the second. AEA #2311 gives the same code at **6263.467 s** in the second sequence. At **0.35**, **14:30:00** is recovered at **284.365 s** and **328.231 s** in the respective first sequences. Use these as candidate playback locators. The June message's **1428Z/1128L**, the July reply's **1528 UTC** and the notes' **1528** remain separate. No transmission was attributed and no clock reading was independently validated as UTC. [Earlier correspondence and strip comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/6688af5d11ffe4a9448ccfe4b9ca0f2301d33ce1/investigation/broader-evidence/faa-atlantic-city-position-logs-and-tape-labels-2026-11-06/README.md)

## Reproduction and scope

The decoder reuses the published ACY-13 pulse-width and BCD method, with source hash, channel and threshold as arguments. The clock field is an IRIG-B-style day/hour/minute/second reading. Day **254** matches September 11 in the sticker's year **2001**. The FAA's later handbook describes voice on the left and IRIG-B on the right for cassette copies. It does not document these transfers. The original DVRS clock, format and calibration remain open. The two sequences and sides are associated by position labels, order and clock ranges. Listening to announcements and matching independently clocked transmissions are separate tests. [Earlier decoder and controls](https://github.com/AveLyra/911-conspiracy-investigation/blob/26a50aad8d004d89fdbcc40b2e35a27e761546d6/investigation/broader-evidence/faa-acy13-cassette-object-2026-11-06/README.md) · [FAA JO 6670.13A, PDF p. 32](https://www.faa.gov/documentLibrary/media/Order/6670.13A2.pdf#page=32) · [RCC 200-16 Format B, PDF pp. 36–39](https://www.trmc.osd.mil/wiki/download/attachments/113019842/200-16_IRIG_Serial_Time_Code_Formats.pdf?api=v2&modificationDate=1623181164717&version=1#page=36)

With FFmpeg **7.1.1**, Python **3.12.14** and NumPy **2.3.5**, run the following for each MP3 using its SHA-256 from the manifest:

```sh
python3 decode_box115.py INPUT.mp3 EXPECTED_SHA256 1 0.32 0.35 0.38 0.42 0.46 > right.json
python3 decode_box115.py INPUT.mp3 EXPECTED_SHA256 0 0.32 0.38 0.42 > left.json
python3 summarize_clock.py right.json left.json
```

Only numerical summaries and scripts are included here. Full source bodies, decoded frame lists and the decoder revision diff remain separately preserved. [Source hashes, results and controls](SOURCE-PINS.json) · [Decoder](decode_box115.py) · [Summarizer](summarize_clock.py)

## Open TODOs

- [ ] Screen the left-channel introductions and transitions to test the side assignments. Seek transfer and digitization documentation, original **ACY-10/11 DVRS** and **ACY-12 ARTS** outputs, and original or independently sourced **ACY-14/15**. Use a separately timed common event to calibrate code-to-UTC and examine the repeated label against another copy.
- [ ] Compare both channels near the candidate times with the facility strips. Establish what each timestamp refers to before linking it to ELKIN21. The early **1246/1248Z** guard and Local Control question remains separate.
- [ ] Carry forward **PD01–PD04**. The actual corrected FAA answer and recipient acknowledgment, the signed action or no-action decision, and the recommendation-specific disposition are still unacquired.

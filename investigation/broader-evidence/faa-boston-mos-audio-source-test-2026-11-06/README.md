# Boston Center MOS archive audio and rerecording timing

November 6, 2026 · B129 / PD07 source acquisition and playback test

Acquired **ZBW-130 / NAID 7597535**, the publicly served 55,238,912-byte MP3 for Boston Center MOS Channel 49. The National Archives finding aid describes a cassette and a digitized audio object labeled **1232–1259 UTC**. This test uses that public transfer. The September 19 timing sheet separately lists three wave files and describes gaps on a rerecording. The predecessor study records the fax and inventory evidence. [Finding aid, box 62 row ZBW-130](https://www.archives.gov/research/foia/faa-finding-aid-60-71) · [Archive audio](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/3-AAL-11/b-Voice-Recordings/4-Interfacility-Coordination/ZBW/3-ZBW-130-MOS-Ch49-1232-1259-UTC.mp3) · [Predecessor study](https://github.com/AveLyra/911-conspiracy-investigation/blob/1fab84c6a046214ee449a7a3e506856623854263/investigation/broader-evidence/faa-boston-mos-and-inventory-2026-11-06/README.md)

## Timing track

FFprobe identified stereo MP3 at 44.1 kHz and a container duration of 1726.149281 seconds. Decoding yielded 76,123,008 samples per channel, or 1726.145306 seconds. At six tested thresholds, the earlier Format B decoder yielded zero accepted frames on either channel. A right-channel sample showed a carrier near 98 Hz and three pulse-width classes near 20, 50 and 80 ms. The Format E test used 100-symbol frames, the double reference marker and all ten periodic position markers. It used the field positions in RCC 200-16 Table 5-9 and the widths in Table 5-11.

The RCC prose in §5.5 calls both **20 ms** and **50 ms** “binary 1”. Table 5-11 labels **20 ms** as binary 0 and **50 ms** as binary 1. Both source descriptions are preserved. The decoder implements the table mapping for this test. [RCC 200-16 §5.5, physical p. 43](https://www.trmc.osd.mil/wiki/download/attachments/113019842/200-16_IRIG_Serial_Time_Code_Formats.pdf?api=v2&modificationDate=1623181164717&version=1#page=43) · [Table 5-9, p. 45](https://www.trmc.osd.mil/wiki/download/attachments/113019842/200-16_IRIG_Serial_Time_Code_Formats.pdf?api=v2&modificationDate=1623181164717&version=1#page=45) · [Table 5-11, p. 47](https://www.trmc.osd.mil/wiki/download/attachments/113019842/200-16_IRIG_Serial_Time_Code_Formats.pdf?api=v2&modificationDate=1623181164717&version=1#page=47)

- **Right channel.** Four RMS thresholds (0.125, 0.15, 0.17 and 0.20) returned the same 161 consecutive 10-second clock readings on day 254, from **12:32:10 to 12:58:50**. At 0.24 there were 151 accepted frames. At 0.15 the first and last accepted frames occurred 69.068 and 1702.367 seconds into playback. Day 254 agrees with September 11 in 2001. The year bits and absolute UTC synchronization were outside this test.
- **Left-channel control.** Zero Format E frames were accepted at the same five thresholds. This supports using the right channel for the embedded timing track on this object.
- **Playback scale.** A single fitted slope was **1.021080 playback seconds per coded second**, with a maximum absolute residual of **1.177 playback seconds**. The local comparisons below interpolate between adjacent accepted markers. The six calculated boundaries changed by at most **0.0052 playback seconds** across the tested thresholds. That is a measure of threshold sensitivity. The clock's accuracy and the transfer or recording equipment responsible for the scale difference remain unverified.

## Listed wave intervals compared with the archive transfer

Sheet labels are in the reported UTC timebase. Playback positions use the embedded clock at threshold 0.15. The intervals between clips are derived from the adjacent sheet boundaries. Levels refer to the archive transfer's left channel only. [September 19 timing sheet, p. 3](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/3-AAL-11/e-Other/3-ZBW-30-20-Fax-cover-9-19-01-partial-transcripts-REDACT-SEALED.pdf#page=3)

| Interval | Sheet clock bounds | Estimated archive playback, seconds | RMS / peak, dBFS |
| --- | --- | ---: | ---: |
| `zbwmos1` | `1237:50–1238:15` | 414.945–440.423 | −16.56 / −0.33 |
| Between clips 1 and 2 | `1238:15–1239:00` | 440.423–486.267 | −40.02 / −23.81 |
| `zbwmos2` | `1239:00–1242:15` | 486.267–685.207 | −15.47 / −0.32 |
| Between clips 2 and 3 | `1242:15–1252:00` | 685.207–1282.955 | −29.15 / −0.13 |
| `zbwmos3` | `1252:00–1253:05` | 1282.955–1349.441 | −14.19 / −0.28 |

The sheet says “The missing gaps of time are dead space on the rerecording.” The corresponding intervals in this MP3 have measurable signal and lower average levels than the listed clips. The longer gap also has a high peak. The statement and the measurements concern separate artifacts, and no speech or particular event was identified in the measured signal. Noise, tones, or transient artifacts can produce a nonzero level. This comparison leaves the actual content and meaning of “dead space” on the rerecording unresolved. [Timing sheet](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/3-AAL-11/e-Other/3-ZBW-30-20-Fax-cover-9-19-01-partial-transcripts-REDACT-SEALED.pdf#page=3) · [Source pins and numeric output](SOURCE-PINS.json)

## Reproduction and remaining inputs

Run with Python 3.13.7, NumPy 2.3.4 and FFmpeg 7.1.1 available. Set `audio` to the downloaded archive MP3. A full rerun matched the two saved frame outputs and numeric summary byte for byte.

```sh
sha=162396368751cd55364bf084e4fdd8b76ecc204e3ea37ec691853f09e9029d2e
python3 decode_mos_e.py "$audio" "$sha" 0 .125 .15 .17 .20 .24 > left.json
python3 decode_mos_e.py "$audio" "$sha" 1 .125 .15 .17 .20 .24 > right.json
python3 summarize_mos.py "$audio" "$sha" right.json left.json
```

- Obtain the native `zbwmos1`, `zbwmos2` and `zbwmos3` WAV files, the full partial transcript, the receiving copy and delivery receipt, and any source-to-transfer documentation. Compare aligned signals, channel maps, and the actual content in and around each interval. Preserve the separate **1237–1259 UTC** partial-transcript description. [August follow-up](https://catalog.archives.gov/id/34913195) · [Transmittal and earlier TODOs](https://github.com/AveLyra/911-conspiracy-investigation/blob/1fab84c6a046214ee449a7a3e506856623854263/investigation/broader-evidence/faa-boston-mos-and-inventory-2026-11-06/README.md)
- Identify independent clock anchors or a calibrated transfer of the source. The observed time-code sequence supports a playback map for this object. An uninterrupted code sequence alone leaves audio continuity and the completeness of the native recording open.
- **PD01–PD04 remain open.** The actual corrected May 2003 answer and receipt, signed administrative determination, recommendation implementation/closure records and applicable follow-up policy remain separate targets. [FAA disposition queue](https://github.com/AveLyra/911-conspiracy-investigation/blob/055ef54a857b46846d0038109bab7e108970f03a/investigation/broader-evidence/faa-postreport-disposition-2026-10-27/README.md)

The source audio, source documents and full frame exports are preserved separately. The public derivative contains analysis, hashes, source links and reproduction code.

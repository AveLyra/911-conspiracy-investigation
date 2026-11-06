Public derivative of the November 6, 2026 UTC Atlantic City audio test. Source bytes remain separately preserved.

# Silence and exact-repeat tests on the Atlantic City recordings

November 6, 2026 UTC · B129 / PD07 · Operational recording integrity. The two preserved NARA MP3s have longer playback durations than the UTC intervals printed in the finding aid. This follow-up checks whether either extra duration can be accounted for by blocks of digital silence or long identical waveform repeats on a fixed sample grid. [Source and duration comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/2b01738ea4a5340767f84058effa1cfdf1dc49a0/investigation/broader-evidence/faa-millville-log-and-later-acy-recording-routes-2026-11-06/README.md) · [NARA Box 115 finding aid, lines 2360–2365](https://www.archives.gov/research/foia/faa-finding-aid-108-126#:~:text=AEA%20%232310)

## Results

| Record | UTC label and nominal span | Decoded playback | Fully zero one-second blocks, both channels | One-second blocks with both channel peaks ≤328 counts, approximately −40 dBFS | Exact loud repeats of at least 39 consecutive blocks on the tested grid |
| --- | --- | ---: | ---: | ---: | ---: |
| AEA #2310, Arrival Data/Departure Data | **1425–1531**, **66 min** | **6519.327347 s** | **0 of 6519** | **13** | **0** |
| AEA #2311, Ground Control | **1425–1525**, **60 min** | **6781.884082 s** | **0 of 6781** | **4** | **0** |

AEA #2310's thirteen low-peak seconds are contiguous at **3734–3747 seconds** from the start of decoded playback, a half-open interval. That is **1:02:14–1:02:27** on a player. AEA #2311's longest low-peak run is **4 seconds**. At stricter peak thresholds of **32** and **104** counts, both files had zero qualifying full seconds. On AEA #2311 the right channel alone had **10** seconds at or below 328 counts. The simultaneous result remains **4**. The final fractional second is reported separately. [Source and results manifest](SOURCE-PINS.json)

There is too little quiet at these thresholds to account for either excess as low-peak padding of that kind. Background noise, tape hiss or a single transient can make an otherwise blank section fail a peak test. The exact-repeat test can miss a copy that starts off the fixed grid, has changed gain, has been re-encoded, has changed playback speed, or contains quieter blocks within the match. It is a test of exact waveform recurrence within each digital release. No between-file comparison, listening or UTC alignment was done.

Keep the Ground Control cassette's **120 min** marking, its **1425–1525 UTC** sticker and the digital playback duration as separate observations. The quiet interval in AEA #2310 is a candidate for inspecting a transfer boundary, with its cause and event time open. Keep the prior **1428Z/1128L** and **1528 UTC** entries as reported. No playback time was assigned to either. [Ground Control cassette photo, p. 1](https://catalog.archives.gov/id/7600783) · [Earlier event comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/6688af5d11ffe4a9448ccfe4b9ca0f2301d33ce1/investigation/broader-evidence/faa-atlantic-city-position-logs-and-tape-labels-2026-11-06/README.md)

## Reproduce the check

Use the two source bodies listed in the manifest. Verify SHA-256 before running. With FFmpeg **7.1.1**, Python **3.12.14** and NumPy **2.3.5**, run:

```sh
python3 check_audio.py --ffmpeg ffmpeg AEA-2310.mp3 AEA-2311.mp3
```

The pinned source files have one stereo **44,100 Hz** stream. The verifier streams signed 16-bit PCM from FFmpeg, takes peak absolute amplitude per channel per full second, and hashes **1,152-sample-frame** blocks where the peak exceeds 328 counts. A repeat must match over **39** or more consecutive eligible blocks, about **1.019 seconds**, with non-overlapping start positions. The grid starts at the first decoded sample. The tested files supplied **249,568** and **259,619** full blocks. A synthetic repeated 50-block sequence, a reversed negative control and the amplitude eligibility checks passed before decoding. [Verifier](check_audio.py)

## Open dependencies

- [ ] Inspect both channels around the quiet interval and near the end of the nominal durations. Seek the digitization side order and timecode records. Use alignment tolerant of gain and speed differences to test analog repeats and compare independently cataloged copies.
- [ ] Obtain independent UTC anchors and the missing Local Control, South Arrival and early guard-channel recordings. Compare clock and event definitions before joining any playback position to the handwritten or headquarters accounts.
- [ ] Carry forward **PD01–PD04**. The corrected FAA answer and acknowledgment, signed decision on administrative action or no action, and recommendation-specific response and closure remain separate from this audio integrity test.

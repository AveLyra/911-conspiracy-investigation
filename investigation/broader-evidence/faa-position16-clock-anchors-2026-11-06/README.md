# ATCSCC position 16 transcript labels and audio positions

November 6, 2026 UTC · B129 / PD07. Four exchanges from FAA transcript AWA-685 match the sequence in the last part of the second DCC-1913 operational audio file, NARA 7598745. The matches are based on speech recognition run without a transcript prompt, followed by comparison with the FAA page images. The filenames and transcript give different time references. The match is between the content of the two copies. Absolute event times and the original recorder's clock remain open. [Prior acquisition and duration comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/8eff8baec0d6fedd4d7301c3017863e89f59f04e/investigation/broader-evidence/faa-position16-transcript-and-archive-2026-11-06/README.md) · [Audio catalog record](https://catalog.archives.gov/id/7598745)

| Exchange | Printed transcript label | ASR segment on the second file's playback clock | Conditional difference if playback zero is 14:15 UTC |
| --- | --- | --- | --- |
| Denver asks about military training flights. The Command Center answers in the negative. | **1504:32**, PDF p. 32 | **3335–3342 s** for the request, then the answer | **363–370 s later** |
| The Command Center begins a broadcast about aircraft requiring an assigned code. | **1506:35**, PDF p. 35 | **3471.42–3474.50 s** for the opening, followed by the code requirement | **376.42–379.50 s later** |
| The Rochester National Guard requests release of a flight from Fort Drum to return to Rochester. | **1508:28**, PDF p. 37 | **3596–3603 s** for the request | **388–395 s later** |
| The Command Center addresses Northeast Air Defense and mentions the CARF cell giving a position. | **1509:02**, PDF p. 38 | **3636–3642 s** | **394–400 s later** |

[FAA transcript, PDF pp. 32–38](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/c-Transcripts/5-AWA-685-Memo-Partial-Transcript-ATCSCC-East-Operational-Position-16.pdf#page=32)

The ranges use model segment boundaries. They give approximate playback locations and are not confidence intervals for actual speech onset. The reported ranges do not agree on one offset under the filename-zero assumption. The test leaves open differing time bases, changes in playback speed, material inserted or omitted during copying, and transcript timing differences. The audio file and the transcript may derive from the same cassette recordings.

The speech recognizer renders the Fort Drum name as **“Ford Prom”** in the later segment. The FAA page reads **“fort drum”**. The match uses the surrounding Rochester, National Guard and return-flight wording in sequence. The broadcast match also retains the FAA spelling **“discreet”** and the model's **“discrete”**.

## Controls and remaining coverage

- **Seeking.** Four two-second waveform probes from the speech clips matched a linear FFmpeg decode at zero measured shift and normalized correlation **1.0**. This rules out a minutes-long difference from FFmpeg seek behavior at those probes. The test checks locations in the digital file and supplies no independent clock.
- **File boundary.** A waveform search over file 7598744 at **7010–7370 s** and 7598745 at **0–360 s** found competing offsets. A separate band-energy search produced a highest boundary score of **0.739**, versus **0.702** in an interior comparison window. Two adjacent boundary probes suggested the same relative offset, while other probes peaked elsewhere. These limited comparisons leave any overlap and its length unresolved.
- **Endpoint.** The transcript still labels the interval through **1515 UTC** and ends at **1516:26**. The final speech scan found a candidate match at **1509:02** and a model reading of an end-of-recording announcement at **3646–3648 s** of file playback. The selected ASR windows did not locate the final Jacksonville exchange from pp. 43–45. The announcement and any gaps in coverage need listening and comparison with the original cassettes or another independently timed recording. [Transcript end, p. 45](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/c-Transcripts/5-AWA-685-Memo-Partial-Transcript-ATCSCC-East-Operational-Position-16.pdf#page=45)

## TODOs

- [ ] Check a separately clocked recording or timecode for the Denver, Rochester and CARF events. Read the duplication log and cassette labels before assigning a time origin or cause to the differences.
- [ ] Review the actual final audio passage and compare the Jacksonville exchange against other candidate copies. Obtain the item-level Tab 4 delivery and Commission intake record to identify which copies the Commission received.
- [ ] Carry the corrected FAA answer, delivery acknowledgment, signed administrative disposition and recommendation records forward as open.

The speech screen used FFmpeg 7.1.1 to make 16 kHz mono clips starting at **3330, 3410, 3490 and 3570 s**, lasting **90, 90, 90 and 80 s**. Whisper.cpp 1.9.2 used the base.en model, CPU, English and zero temperature with fallback disabled by a zero increment. The source pins preserve model and file hashes, physical page and text-line locators, and the numerical results. Working audio and full recognition output stay in the research store. [Source pins](SOURCE-PINS.json)

# ATCSCC position 16 transcript and recordings

November 6, 2026 UTC · B129 / PD07. The November 17, 2003 FAA response reproduction lists two cassettes and a partial transcript for ATCSCC position 16, **1215–1515 UTC**. The National Archives supplies a partial transcript for that operational position and two digitized operational-line recordings under **DCC-1913**. The position, facility and labeled window support a candidate match. The dated production inventory and recipient intake remain necessary to identify the copies actually delivered. [Earlier Tab 4 comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/0c3fb38d52a420d4fe75b215f4e8071bdca5304f/investigation/broader-evidence/faa-november17-fax-response-comparison-2026-11-06/README.md)

| Record | What the source gives |
| --- | --- |
| **AWA-685**, November 5, 2003 | The cover labels an **east operational position 16** partial transcript for **1215–1515 UTC**. The document carries a transcription certification on PDF p. 2. Its last page of transcript gives **1516:25** and **1516:26** immediately before the end label. Keep the stated interval and the later entries together. [Cover, PDF p. 1](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/c-Transcripts/5-AWA-685-Memo-Partial-Transcript-ATCSCC-East-Operational-Position-16.pdf#page=1) · [Endpoint, PDF p. 45](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/c-Transcripts/5-AWA-685-Memo-Partial-Transcript-ATCSCC-East-Operational-Position-16.pdf#page=45) |
| **DCC-1913**, box 27 | The finding aid lists the **operational** phone, **5116**, with digital files **7598744** and **7598745**. The filename windows are **1215–1415 UTC** and **1415–1515 UTC**. [Finding aid, HTML table rows 859–861](https://www.archives.gov/research/foia/faa-finding-aid-24-35#:~:text=DCC%2D1913) · [First catalog item](https://catalog.archives.gov/id/7598744) · [Second catalog item](https://catalog.archives.gov/id/7598745) |
| **DCC-1952**, box 29 | The same finding aid separately lists the **administrative** phone, **4528**, at the same position, with the same two filename windows and different digital IDs **7598825** and **7598826**. The operational wording on AWA-685 points toward DCC-1913. The shared position and windows alone do not identify the line. [Finding aid, HTML table rows 981–983](https://www.archives.gov/research/foia/faa-finding-aid-24-35#:~:text=DCC%2D1952) |

## Endpoint and file duration checks

The PDF text scan found **14 standalone times with seconds later than 1515:00** on physical pp. **43–45**. The latest printed time is **86 seconds** after the stated endpoint. The check counted labels, including two entries labeled **1516:23**. It did not count distinct calls. The cover's window and the final **1516:26** entry were visually checked against the page images.

| DCC-1913 file | Nominal interval in filename | FFprobe duration | Difference |
| --- | --- | --- | --- |
| 7598744 | 7,200 s | 7,373.012969 s | +173.012969 s |
| 7598745 | 3,600 s | 3,650.093781 s | +50.093781 s |

Both downloaded entities are 44.1 kHz stereo MP3s. The decoder reported output times of **02:02:53.008980** and **01:00:50.089796**. These are distinct tool readings from the container durations above. FFmpeg decoded both streams through the end with no reported errors. This verifies playback integrity and records a difference from the nominal filename spans. Neither the durations nor the transcript labels establish the clock origin of either file. The source includes no verified join between a transcript time and a sample offset. Overlap, extra recorded material, and different recorder or transcription time references remain untested explanations.

## TODOs

- [ ] Obtain the cassette labels, duplication and digitization logs, complete Tab 4 inventory and Commission intake. Compare the operational and administrative copies by line and cassette identifier.
- [ ] Match identifiable transcript events near the first-file boundary and in the final minute against the operational recordings. Use independent clock references to test offsets, overlap or material outside the nominal windows. Keep the **1515 UTC** cover and **1516:26** final entry as separate source readings.
- [ ] Preserve the corrected FAA answer, recipient acknowledgment, signed action/no-action decision and recommendation disposition as open. This record concerns the separate production trail.

[Source pins](SOURCE-PINS.json) identify the acquired PDF, finding aids and recording hashes, and record the exact extraction, decoding and access scope. Raw audio stays in the research media store.

# Flight 93 emergency call: audio candidate and competing duration reports

2026-11-14 UTC · AUD016-A1. A new public-source route changes the [previous custody review](https://github.com/AveLyra/911-conspiracy-investigation/blob/5c4e405993fd47d3fdf329e73c5673c91d0dc4ab/investigation/broader-evidence/telephone-felt-public-transcript-2026-11-14/README.md): **a publicly posted audio candidate is now located and preserved for research.** Its origin, completeness and identity as an FBI-released copy have not been independently authenticated. The original physical tape and its custody remain unlocated in this review.

## Different duration observations

- The [National Park Service](https://www.nps.gov/flni/learn/historyculture/phone-calls-from-flight-93.htm), Felt entry, reports a **70-second connection** to the Westmoreland County 911 center. It labels the start 9:58 Eastern Daylight Time.
- In a September 10, 2026 [Click2Houston interview](https://www.click2houston.com/news/local/2026/09/10/i-typed-his-last-words-houston-fbi-employee-remembers-transcribing-flight-93-passengers-911-call/), Carrie Jackson, described as the FBI employee who transcribed the call, recalls: **“I think it was like 5 or 6 minutes long.”** The article places that recollection in the context of the audio she says she transcribed, and separately reports her approximate transcription-work time. Her estimate is a later recollection; this study did not locate a contemporaneous duration measurement from her transcription session.

These statements differ numerically and describe a reported connection and a recollection of audio length. Their relationship is **unresolved**: the call, a recording of it, and a transcription session have different boundaries, and the source of the estimate is not established. Memory error, different content or recording boundaries, and incomplete or differing copies are **untested possibilities**, not findings. The recordings and source documents needed to discriminate among them remain outstanding.

## Audio candidate: what was actually checked

A March 11, 2026 [publisher page](https://charliekallas.substack.com/p/foia-release-of-edward-felt-phone) describes its episode as presenting an audio recording obtained through FOIA. A separate September 9, 2026 [WPXI report](https://cmg-cmg-tv-10080-prod.web.arc-cdn.net/news/local/flight-93-25-years-later-2-men-connected-by-phone-call-911-meet-first-time/JHOH4NSU6ZH4JB5RJGLAYJMH7I/) says its newsroom obtained a recording; this does not establish that its source or bytes are independent of the publisher's episode.

The publisher's public feed offered an MP3 episode, downloaded November 14, 2026 UTC and retained in the verified research media store. Its SHA-256 is `e7e120120b80f0aa40224249a7ac575b539ac99be5676616279a57a8ae4a654b`, length **1,657,984 bytes**. `ffprobe` reports **138.135510 seconds for the entire MP3 container**, mono MP3 at 44,100 Hz. This is an episode duration, **not a measured call duration**. The audio was not transcribed, segmented, independently listened to, or compared against the FBI transcript in this step. The MP3 is a publisher-distributed derivative; no authenticating FBI release, original master, complete custody trail or proven connection to the 2001 tape has been inspected. The publisher's FOIA and metadata statements remain attributed claims. The audio itself is not republished in this repository.

A public [MuckRock request page](https://www.muckrock.com/foi/united-states-of-america-10/audio-recordings-of-edward-felt-202891/) was identified as a possible release trail through a third-party discussion, but the accessed route returned HTTP **403** in this session. The request contents and any agency attachment were **not examined**; no claim that this particular request supplied this MP3 is established. An access error is not evidence of withholding, alteration, or intent.

## Next discriminating work

1. Obtain a publicly accessible agency release and its attachment, release letter and provenance; compare file hashes and inspect any stated redactions and processing.
2. Identify call boundaries in the candidate, then independently compare the bounded audio with the FBI transcript without disclosing private contact information. Do not use whole-episode length as call length.
3. Locate the original or authenticated preservation copy, evidence entry and transfer/disposition records, 911 dispatch records, carrier records and clock definitions. Preserve all conflicting statements pending those checks.

[Source pins](SOURCE-PINS.json) record the exact access times, hashes and scope. The accompanying verifier checks captured public-page and MP3 bytes and selected text/format anchors; it does not authenticate the recording or prove what happened. Previous reports and their limitations remain unchanged. No third party was contacted.

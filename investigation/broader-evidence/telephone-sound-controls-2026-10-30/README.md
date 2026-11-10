# Court telephone presentation: streamed audio and event resources are different objects

October 30, 2026. Existing AUD016-A1 / TC05-B105 / TC06-B110; TEL02 presentation-source/provenance work. This is a new passive file-structure test of two held court assets. It does not supply a carrier record, identify a speaker, validate AA77's zero-duration label, or complete a substantive original-record gate.

## Result in plain language

**The two named presentation files each contain more than one representation of sound. The long MP3 resource extracted previously is not byte-identical to the MP3 sequence assembled from that file's root streaming blocks. The parsed button-sound settings refer to a different, short resource.** Our earlier extraction/decoder results remain valid for the particular resource tested, but cannot alone certify what the presentation played.

This is a limitation on our own evaluation, not evidence of deceptive editing. Re-encoding can change bytes without changing intelligible content. Conversely, equal names or similar nominal lengths cannot establish equal content. Decoded-content alignment and the source/preparation/custody chain remain untested. No listening, transcription, speaker attribution or actual presentation playback occurred.

## Source and actual scope

Input: the previously acquired [official court flights ZIP](https://coop.vaed.uscourts.gov/moussaoui/flights.zip), SHA-256 **3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801**, rehashed before this test. Only **Lyles.swf** and **Ong.swf** were inspected. These are archive member names, not speaker identities authenticated here. The archive, members and [earlier resource/decoder report](https://github.com/AveLyra/911-conspiracy-investigation/blob/3b1c9b18434e58faef2e7f22b4e457af387d856c/investigation/broader-evidence/telephone-court-audio-resources-2026-10-29/README.md) remain unchanged. No new download or decoding pass is represented as performed.

The existing bounded SWF unpack/tag walker was reused, pinned to its previously published bytes. A new parser reads SoundInfo and four button-transition sound slots, then associates root streaming headers/blocks with static root frame positions. It never executes ActionScript, launches Flash, follows embedded links, plays or saves media, or accesses an external transcription service. All payload concatenation/comparison occurred in memory. All contained sprite tags are walked for the specified control-tag checks; stream assembly is restricted to the **root** timeline.

Method fields follow Adobe's 2012 SWF19 specification, acquired earlier from a [mirror](https://open-flash.github.io/mirrors/swf-spec-19.pdf), SHA-256 **6a1625b0929a86329021d365ba079c7e1f51502dfb4ea7d92ec9947841625cdd**. This pass visually read physical pages 27, 182–184, 186, 190 and 201–202 (printed 25, 180–182, 184, 188, 199–200), plus the relevant text paragraph on physical page 28. It is a later format reference, not the authenticated historical authoring version for these SWF5 files. No full 243-page review is claimed.

## Preserve the separate representations and fields

| Field / representation | Lyles.swf | Ong.swf |
|---|---|---|
| Member SHA-256 | `28f2a83db87177a2538ebd36ddfc03b63e7b696b7d16603a793921ff27ce4ec7` | `8c844a2370852e55597a4aa73ef8b8ff0e6c03e3fec982a9cd98aeb937e5a3ec` |
| DefineSound1 tag offset, uncompressed SWF coordinates | 26 | 26 |
| DefineSound1 MP3 bytes | **540,735** | **492,856** |
| DefineSound1 rate code / declared sample count | **3 / 1,987,200** | **1 / 2,726,784** |
| DefineSound1 signed SeekSamples | **0** | **1,669** |
| Prior independent decoder output count for that event resource | **1,987,200** | **2,729,664** |
| Root stream header offset / rate code | **540,795 / 1** | **492,914 / 1** |
| Root header average samples per block / LatencySeek | **918 / 1,633** | **918 / 1,633** |
| Root stream block count / static first–last frame | **541 / 49–589** | **2,894 / 49–2,942** |
| Sum of root block SampleCount prefix fields | **498,240** | **2,658,240** |
| Root concatenated MP3 payload bytes | **89,960** | **479,960** |
| Byte-identical to that file's DefineSound1 MP3? | **No; first differing byte offset 1** | **No; first differing byte offset 9** |

Rate codes, event-definition counts, previous decoded counts, stream block count prefixes and latency fields remain separate observations. We neither choose a preferred duration nor convert count differences into missing conversation, a clock offset or tampering. In particular, Lyles' event and stream rate codes differ. Prior Ong's **2,880-sample decoded-minus-declared** observation is retained unchanged, not explained away by the new fields.

Root concatenated MP3 hashes are respectively **b01692e3acebe4731d1c863da1162a70b2bc21cad3d99f913a3810bb10b9be92** and **076067d2fe207c9efb95d62ed0a1cc33f24df2f60568cdf143631885b15fcfcd**. The prior long-resource hashes remain **53d4d3256cf941cb2ad659e4bfdaed341e440d4dfa1484a3c84b2e07210e197e** and **b1340270d0e8f4b159bb4b057ea57ec227cd021fb12dc5fd37a46b7e3e9b78b5**. Both sides of the comparison are preserved in [RESULTS.json](RESULTS.json).

### Buttons reference a separate short resource

Lyles' four DefineButtonSound records reference resource **224** on the **OverUpToOverDown** transition; Ong's two reference **345** on that transition. Each has SoundInfo flags **0**; all other sound slots are zero. The referenced button and sound definitions exist in each file. The two short MP3 payloads have the same hash, **11285316ce85061a2a8b1f4f4a6dd5e1e88c0d5a39407278493b34354fc6cc35**, each **3,135 bytes**, declared **6,912 samples**, rate code **2**. Multiple buttons/resource definitions are not multiple independently recorded calls. No claim about what the short sound sounds like is made.

The contained tag walk found **no StartSound or StartSound2 tags** in either scoped file. This does not establish that the long resource is unused: action code or another runtime mechanism was not evaluated. Nor do static button-sound slots identify the button's displayed purpose or every effect of clicking it. Parsed sound slots and arbitrary button actions are different mechanisms.

### Matching fields are preserved too

Each root header's LatencySeek **1,633** equals its first root stream block's SeekSamples; both differ from the corresponding event resource's SeekSamples. Header and actual root ShowFrame counts agree: **589** for Lyles, **2,942** for Ong. Each header nominal rate is **12 frames/second**. These structural matches are retained alongside the nonmatches. They do not authenticate the recording's creation, establish actual playback speed or align a historical call clock. Frame 49 is a static authoring position, not a measured moment in the attack.

## Reproduction, controls and limits

[compare_sound_controls.py](compare_sound_controls.py) and [REPRODUCE.md](REPRODUCE.md) reproduce the comparison from the pinned archive and prior helper. It preserves offsets, source/member/payload hashes, root block fields and variable SoundInfo values. Positive controls cover zero flags and all optional fields/two envelopes; negative controls reject all 28 truncated prefixes of the full-field fixture, nonzero reserved bits and a truncated button. These exercise parsing, not recording authenticity.

The full first-run numeric output is **989,449 bytes**, SHA-256 **ea247c441880a3277267235daaa188e3f58b4b63a02c7a3bc1a9dd482947c9f3**. Its complete block ledger remains local; the script regenerates it. The public RESULTS view contains summaries, actual first/last blocks and ledger hashes, not audio. A portable run from the reviewed candidate must match the full output before publication; its actual receipt is separate from a promised result.

**High confidence:** the pinned files contain the reported distinct bytes and static fields, conditional on the reviewed parser and later reference. **Unresolved:** semantic equivalence, any trimming/re-encoding/export cause, runtime control use, complete conversation coverage, speakers, provenance before the court copy, carrier events, clocks and source-to-exhibit construction. No inference of deception, an impossible call or a conspiracy follows from this test.

## Next records and tests

[OPEN-TODOS.md](OPEN-TODOS.md) keeps native source recordings, court exhibit-construction/edit/export records, carrier/operator/recipient records and source-to-call associations open. A separately scoped decoded-content comparison could test whether re-encoding alone accounts for the difference; it has not been performed. This unit supplies no new AA77-specific caller/event or zero-duration-field definition.

The FAA accession search this turn did not recover a transfer dossier; it remains a local TODO, not a new public finding. All five original-record tracks and eighteen substantive criteria remain unfinished. [CHECKLIST.md](CHECKLIST.md), [SOURCES.json](SOURCES.json), [REVISION.diff](REVISION.diff) and [MANIFEST.json](MANIFEST.json) retain request accountability, source relationships, additive text changes and companion hashes. Public commit/ref/body verification is recorded after the actual push, separately from the static test.

# Audio audit of “WTC Building 7 Collapse — 27 Angles”

**Prepared:** 2026-09-02  
**Status:** Reproducible screening analysis; not acoustic-forensics testimony  
**Source:** [CTV911, “WTC Building 7 Collapse — 27 Angles”](https://www.youtube.com/watch?v=cmp7rV2aZhM), uploaded 2024-06-20, 13:01

**2026-09-11 methodological qualification:** The [fresh source/measurement audit](../sherlock-wtc7-investigation/acoustic-audit/report.md) reproduces file loudness and checks the preserved derivatives, but corrects the mono-average description, finds seek-versus-full-decode sample differences, and identifies precise prose times as uncorrected transcript-segment pointers rather than independently measured event onsets. The claimed absence of a distinctive charge sequence across independent views is not independently validated by this four-window quality audit. Retain the original screening discussion below as history; it is not a calibrated detection or source-synchronization result. No fresh listening, explosive identification or NIST blast-analysis reproduction is claimed by the September 11 work.

## Bottom line

**2026-09-11 visual/edit follow-up:** The [source-pinned correspondence audit](../sherlock-wtc7-investigation/acoustic-audit/av-correspondence/report.md) now confirms adjacent-frame shot changes at uploaded-track435s,441.866667s and580.766667s. Foreground turning precedes the old603.700s transcript pointer, while later camera reframing/blur does not establish structural onset. The between-cut passage was screened at every encoded frame, but “no continuous descent recognized” is visibility/resolution-qualified—not proof of no motion. Comparator façade changes are visible before13s; that legacy label is not a first-event time. Digital power near the cuts supplies no original sound synchronization or source classification. These additive corrections control over the older precise timing language below; the original body is preserved as history.

The compilation contains forceful audio, references to explosions, rumbles, and abrupt transients. It is reasonable for a listener to flag those sounds for investigation. But the compilation does not, by itself, establish that the microphones recorded a sequence of demolition charges.

The strongest apparent example needs an important correction. At compilation time 01:06-01:13, the soundtrack says, “All of a sudden a loud, incredibly loud explosion ….” That is a reporter's **spoken description** while the broadcast shows and recounts the collapse; it is not the waveform of the described explosion. It is evidence that a reporter characterized a perceived sound as an explosion, not direct acoustic evidence of the sound's level or source.

The other audio must be treated clip by clip. The 13-minute file is a montage of different cameras, broadcasts, voiceovers, silent passages, and hard edits. A source index linked by the uploader expressly says that at least one documentary version used audio from another source and that one stabilized WTC 7 clip had audio added from an older version. That does not prove that every track is altered. It does rule out treating the compilation as 27 independent, continuous, mutually corroborating microphone records.

## What was preserved and measured

The exact YouTube access copy was retained as separate, unaltered format streams:

| Stream | Local file | SHA-256 |
|---|---|---|
| 720p H.264 video, no audio | [`media/compilations/WTC Building 7 Collapse - 27 Angles [cmp7rV2aZhM].f136.mp4`](media/compilations/WTC%20Building%207%20Collapse%20-%2027%20Angles%20%5Bcmp7rV2aZhM%5D.f136.mp4) | `1ea6063dac3847ee01969987bcee66991056d85ad61839ec301fb888a4456d87` |
| AAC stereo audio, no video | [`media/compilations/WTC Building 7 Collapse - 27 Angles [cmp7rV2aZhM].f140.m4a`](media/compilations/WTC%20Building%207%20Collapse%20-%2027%20Angles%20%5Bcmp7rV2aZhM%5D.f140.m4a) | `d8b75d1f861a327a38e73f00b645c511b27734325305cbecd4e18dc20d71558c` |

The AAC stream measures approximately -18.6 LUFS integrated and reaches approximately 0 dBFS true peak. Those are properties of this uploaded/mastered file. They cannot be converted into sound-pressure level at the original camera because the microphone calibration, gain, automatic gain control, intervening broadcast chain, and editing history are unknown. “Very loud on playback” and “high acoustic pressure at the scene” are different propositions.

## Segment findings

### 1. The “incredibly loud explosion” passage, 00:59.760-01:12.960

The machine-assisted transcript attributes the passage to a reporter recounting what happened after learning that the building was considered compromised. The reporter describes a sudden, exceptionally loud explosion and says video will show the event. The waveform and spectrogram show continuous voiced speech during the key words. The broad vertical/harmonic patterns are consonants and speech energy, not a separate isolated event corresponding to the explosion being described. This is still relevant eyewitness/reportorial evidence, but its correct category is **reported perception**, not **captured blast waveform**.

![Waveform and spectrogram of spoken passage](analysis/figures/27-angles-spoken-explosion-reference.png)

### 2. MSNBC live segment, approximately 09:40-10:09

At 09:43.740 the reporter says that she first thought the crew heard another explosion, then immediately identifies another truck heading south as the likely sound. Visual reaction to the building begins around 10:03.700; the speakers recognize the building's descent around 10:06.700-10:08.700.

On this compilation soundtrack, the reported possible-explosion/truck event is about 20 seconds before the on-camera recognition of collapse. The collapse-onset interval contains speech and urban background sound, but no uniquely identifiable, isolated train of charge-like impulses. This does not prove that no impulsive sound occurred at the building: source distance, propagation delay, broadcast synchronization, microphone directionality, and the compilation edit remain unresolved. It means this particular track cannot honestly be described as a clean recorded charge sequence.

![Waveform and spectrogram of MSNBC passage](analysis/figures/27-angles-msnbc-segment.png)

### 3. The segment beginning near 07:15

The uploader describes the segment as Richard Peskin material and says it is not counted among the 27 because it does not capture the collapse. (The archived source index disputes that attribution, which is another reason to seek the native file.) Inspection agrees that the compilation cuts into an audio-bearing source near 07:15 and then cuts to post-collapse dust near 07:21.9. The descent itself is absent. Stronger later transients therefore cannot be placed before or during collapse initiation from this edit.

The archived source index also says that a NIST-hosted version of similar material had no audio and that a stabilized web version had audio added from an older version. That is a provenance warning, not proof that the audio is fabricated. The native source and its transfer history must be obtained before relying on its synchronization.

![Waveform and spectrogram of edited Peskin passage](analysis/figures/27-angles-peskin-segment.png)

## Positive-control comparison

For a qualitative positive control, the repository now preserves separate video and audio streams of the confirmed 2024 Capital One/Hertz Tower implosion in Lake Charles. The official project record identifies the method as an implosion. In that upload, visible initiation effects beginning around 13 seconds coincide with a dense, rapid series of large broadband impulses extending through the early descent.

![Waveform and spectrogram of confirmed implosion](analysis/figures/hertz-confirmed-implosion-control.png)

This one comparator is not a universal explosive-signature template. Charge size, delay pattern, distance, urban propagation, microphone response, and postproduction all vary. Its value is narrower: it demonstrates the type of repeated time-frequency pattern that can be plainly recoverable when a recording actually contains a close, high-signal explosive sequence. The 27 Angles master does not show that pattern consistently across independently sourced WTC 7 views.

## Evidentiary weight

| Proposition | Weight from this compilation | Reason |
|---|---|---|
| People/reporters described a sound as an explosion | Moderate | The words are genuinely present and should be preserved; speaker, firsthand basis, timing, and descriptive precision still need authentication. |
| The uploaded compilation contains loud passages and transients | Strong | Directly measurable in the access copy. |
| Those levels establish how loud the source event was in physical units | None | A digital file at 0 dBFS supplies no calibrated sound-pressure level. |
| A particular transient came from WTC 7 | Weak unless the source clip is authenticated and synchronized | Edits, mixed provenance, propagation delay, vehicles, speech, impacts, and automatic gain control are confounders. |
| The compilation establishes explosive demolition | Weak | It lacks a consistent, authenticated pre-motion impulse train across independent native recordings. |
| The compilation establishes no explosives were used | Weak | Its provenance and recording limitations also prevent an absolute negative inference. |

The neutral conclusion is therefore asymmetric but not categorical: the compilation contains legitimate leads and explosion testimony; it is weak causal evidence for demolition and weak proof of absence. It does not validate NIST's structural sequence, and it should not be used to overstate NIST's distant-audio analysis. It mainly shows why native source files and metadata matter.

## Verification protocol

To turn the leads into acoustic evidence:

1. obtain each highest-generation, continuous camera file, including at least 30-60 seconds before and after initiation;
2. preserve both channels, codec metadata, sample rate, edit list, timecode, and transfer history;
3. establish camera/microphone location and line of sight;
4. synchronize by multiple visual and acoustic events, then apply source-to-microphone propagation time with uncertainty bounds;
5. detect candidate impulses blind to the causal hypothesis and publish waveform, spectrum, duration, crest factor, clipping, and channel agreement;
6. distinguish speech plosives, edit clicks, vehicles, debris impacts, structural fracture, and reverberation from candidate blast events;
7. require cross-recording agreement after distance correction; and
8. compare against several known implosions and several non-blast urban/structural controls, not one hand-selected example.

The plotting script and derivative-generation notes are in [`analysis/README.md`](analysis/README.md). The machine transcript is a navigation aid only and must be checked against the source before quotation in a filing.

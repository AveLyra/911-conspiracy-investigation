# WTC 7 video and demolition-comparator research

**Status:** Working technical research. Not pleading text, not an expert report, and not a source of procedural facts unless a proposition is separately promoted under the repository's fact-promotion rules.

## Why this package exists

This package preserves the parts of the WTC 7 merits discussion that may explain why access to NIST's underlying modeling records matters. It deliberately does **not** ask a court deciding a FOIA case to determine why WTC 7 collapsed.

The useful litigation proposition is narrow:

> NIST published a detailed and physically possible "probable collapse sequence," but important transition points are model-dependent, the public record contains acknowledged sensitivities and later-stage discrepancies, and withheld executable inputs/results limit independent end-to-end testing.

That proposition is materially different from alleging that NIST's conclusion is false or that a demolition occurred.

## Contents

| File | Purpose |
|---|---|
| `wtc7-video-demolition-comparison.md` | Main assessment: observations, comparison, physics, inference limits, and complaint-use boundary |
| `collapse-warning-and-premature-reporting.md` | Evidence-focused treatment of responder warnings, street audio, and premature CNN/BBC collapse reports |
| `27-angles-audio-audit.md` | Source-level audit of the compilation's explosion language, transients, edits, and confirmed-implosion control |
| `feature-matrix.csv` | Machine-readable comparison of WTC 7 with explosive, nonexplosive induced, mechanical, and accidental fire-collapse modes |
| `source-manifest.csv` | Source provenance, intended use, and limitations |
| `sources/` | Preserved non-NIST source documents and their checksums |
| `analysis/` | Reproducible audio-screening script, figures, transcript aid, and derivative checksums |
| `media/README.md` | Preservation policy, custody cautions, and handling notes for video files |
| `media/video-acquisition-manifest.csv` | File-level provenance, technical metadata, and SHA-256 hashes |
| `media/SHA256SUMS` | Machine-verifiable hashes for the preserved downloads |

## Preservation policy and current limits

- Preserve material source copies when technically obtainable, together with the exact acquisition URL, acquisition date, byte count, technical metadata, and a cryptographic hash. Keep derivatives separate from the preserved download.
- Copyright or licensing status is **not** a reason to exclude relevant material from the internal case file. It is a separate issue to track before redistribution, public filing, or publication.
- A stored copy is not automatically an authenticated exhibit. Authentication, completeness, edit history, original/native status, and chain of custody must be developed separately.
- The three files stored under `media/analysis-source/` are secondary-hosted analysis copies attributed to NIST camera footage. The two full segments under `media/broadcast-archive/` are Internet Archive access derivatives. The 27 Angles compilation and a confirmed-implosion comparator are preserved as separate platform video/audio streams. They are useful for reproduction and source comparison, but none is represented as a broadcaster master or native camera original.
- A YouTube positive-control copy is now preserved for the Capital One/Hertz Tower implosion; acquisition should still prioritize official/project or archival masters and additional controls over social-media encodes.
- A numerical probability of demolition or fire causation. The available case set is not a representative statistical sample, and the hypotheses are not specified tightly enough to support defensible odds.
- Claims that WTC 7 fell "perfectly into its own footprint," that all columns visibly failed simultaneously, or that the absence/presence of explosions is proved by a compilation video.
- Any accusation that physical evidence was intentionally destroyed. The evidentiary limitation can be stated without inferring intent.

## Repository-use rule

Keep this package in `research/`. Do not copy its scientific conclusions into `facts/`, a complaint, or a dispositive-motion fact statement without all of the following:

1. a primary-source pin cite;
2. a clear label distinguishing observation, agency claim, expert opinion, and inference;
3. a relevance explanation tied to a live legal element; and
4. review by counsel and, for engineering opinions, an appropriately qualified expert.

## Proposed reconstruction system

The architecture for turning these preserved sources into calibrated observations, forward simulations, and uncertainty-aware mechanism comparisons is in the [`../collapse-reconstruction-workbench/`](../collapse-reconstruction-workbench/) blueprint. It is a system design, not an implemented model or a new merits conclusion.

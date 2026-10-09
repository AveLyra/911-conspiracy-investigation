# WTC 7: Research, Evidence, and Open Questions

This repository collects scientific and technical research about the collapse
of World Trade Center 7 on September 11, 2001. It is an unfinished research
archive, not an expert report or a finding about the cause.

## In plain language

WTC 7 was a large steel-framed building that collapsed late in the afternoon
of September 11. The National Institute of Standards and Technology (NIST)
concluded that fires caused a sequence of structural failures that led to the
collapse. This project examines how well the available records and engineering
analysis support that explanation, and whether they distinguish it from other
specific explanations, including deliberate removal of structural support.

The project does not assume that NIST is right, and it does not assume that a
conspiracy occurred. It asks what the evidence can actually show. For example:

- Photographs show flames in some visible parts of the building. They cannot,
  by themselves, tell us the temperatures inside the building or whether a
  particular structural connection failed.
- Some published roof-point measurements show rapid downward motion under the
  stated scale and timing assumptions. They do not, by themselves, establish
  that the whole building was in free fall or identify what started the
  collapse.
- Released engineering inputs and experiments can be checked for how they
  were used in NIST's analysis. Finding a modeling question or mismatch would
  not, by itself, show that anyone deliberately manipulated the analysis.
- Records concerning building equipment, warnings, sounds, or access matter to
  a conspiracy hypothesis only if they can be authenticated and connected to
  a specific act, time, place, and mechanism. A lead or unexplained gap alone
  does not establish such a connection.

The current synthesis finds that NIST's proposed sequence is technically
developed and physically motivated, but this project has not independently
verified the complete building-specific chain from fire exposure through
structural failure and collapse. The work also has not established an executed
deliberate-removal operation or earned a defensible ranking of the competing
causes. **Unresolved does not mean the explanations are equally likely.** The
investigation is incomplete, and its reports describe what evidence or test
could change each assessment.

### Where to start

- [Crucial findings and their limits](CRUCIAL-FINDINGS.md)
- [Current scope and questions](investigation/wtc7/CHARTER.md)
- [Current status and limits](investigation/wtc7/STATUS.md)
- [Overall causal-chain assessment](investigation/wtc7/causal-chain-synthesis/report.md)
- [What remains incomplete](investigation/wtc7/completion-audit-2026-09-24/report.md)
- [Sherlock feedback technical requirements and coverage review](investigation/wtc7/feedback-technical-record-2026-10-09/README.md)
- [Feedback digest coverage addendum](investigation/wtc7/feedback-digest-coverage-2026-10-09/README.md)

## Technical explanation

### Explanations being tested

The investigation keeps four explanation families distinct:

1. **NIST's specific fire-triggered sequence.** Test the proposed fire,
   connection, floor, column-restraint, and global-collapse steps against the
   available records and calculations.
2. **Other fire-triggered structural pathways.** A problem with NIST's exact
   sequence would not automatically disprove every fire mechanism. An
   alternative must specify its own initiating and propagation steps.
3. **Deliberate support removal.** Different proposals—such as explosive,
   thermal/chemical, mechanical, or mixed methods—have different observable
   requirements. Reproducing motion after prescribing support loss does not
   establish how that support was lost or whether the loss was deliberate.
4. **Other, mixed, or underdetermined explanations.** Keep these open where
   evidence justifies them. An unspecified mechanism does not gain support
   merely because it is difficult to rule out.

The project separates initiation, support loss, propagation, observed motion,
and intent. Evidence about one stage does not automatically prove the others.
It separately assesses physical compatibility and the broader evidentiary
comparison. It does not infer a probability from historical rarity, motive,
institutional reputation, or the absence of a matched precedent.

### Selected results and their limits

These are entry points, not a substitute for each report's protocols, data,
source pins, and limitations.

| Topic | What the reviewed work reports | What it does not establish |
| --- | --- | --- |
| Fire observations | In one 25-image batch, both reviewers identified flame-like forms in nine images; one reviewer did so in three additional images. Some report-image timing depends partly on fire-development assumptions. | The images do not establish interior temperatures, structural damage, deliberate image alteration, or whether the fire sequence was sufficient to cause collapse. [Report](investigation/wtc7/fire-coverage-batch3/report.md) |
| Motion | A published Camera 3 roof-corner track has a late-window fitted downward acceleration near conventional gravitational acceleration under its assigned calibration. Results vary with tracked point and fitting window. | This is not a verified whole-building center-of-mass trajectory, proof that all supports were removed simultaneously, or identification of an initiating cause. [Report](investigation/wtc7/camera3-conditional-trajectories/report.md) |
| Structural inputs and experiments | Released thermal inputs contain repeated assignments that merit a processing-history check. Connection experiments provide real evidence about certain failure and residual-load behaviors. | The work does not establish inflated temperatures, deliberate manipulation, or that the tested components reproduce WTC 7's heated composite-floor and global-collapse behavior. [Thermal-input report](investigation/wtc7/thermal-assignment-trace/report.md) · [Connection-experiment report](investigation/wtc7/assembly-test-source-audit/report.md) |
| Sounds and flashes | The project examines what selected recordings could detect and searches for specifically cited acoustic records. | A loud sound does not identify an explosive charge; a non-detection has weight only if the source, recording chain, coverage, and detection opportunity support it. The bounded search did not locate two cited emails, which does not prove they do not exist. [Flash-observation report](investigation/wtc7/flash-opportunity/report.md) · [Email search report](investigation/wtc7/acoustic-correspondence-locator/report.md) |
| Access and documentary leads | An official tax decision describes a WTC 7 CCTV maintenance relationship and an equipment-purchase exhibit. | It does not establish 2001 access, demolition preparation, or a collapse mechanism. [Report](investigation/wtc7/procurement-dta817373/report.md) |
| Overall comparison | The present synthesis treats NIST's account as a substantive candidate while finding its complete historical causal chain unverified. | It does not conclude demolition, assign equal odds, or provide a final cause ranking. [Synthesis](investigation/wtc7/causal-chain-synthesis/report.md) |

### How a conspiracy hypothesis could be tested

The relevant question is not whether a fact looks unusual in isolation. A
conspiracy claim would need a supported chain connecting people or entities,
actions, timing, access or means, and a physical or documentary consequence.
Useful discriminating evidence could include authenticated operational
records; independently corroborated access or preparation tied to a relevant
time and location; or physical evidence that links a specified intervention
to observed structural failure. Each item also needs ordinary alternative
explanations tested against it.

The same standard applies to the fire explanation: a technical model is not a
historical observation. Its building-specific inputs, assumptions, handoffs,
failure sequence, and predictions must be compared with evidence that was not
used to tune the model where possible. A mismatch can weaken a specified model
without proving a different cause. Missing records and unresolved analyses
remain gaps until affirmative evidence bridges them.

### How the research is recorded

Most folders under [`investigation/wtc7/`](investigation/wtc7/) are bounded
studies. Depending on the study, a folder may contain:

- a **protocol** describing the question, inputs, and planned method;
- a **report** stating the result and its scope;
- source manifests, retrieval records, and hashes for provenance;
- scripts, data, and run records for reproduction;
- independent or adversarial reviews, validation, and preserved failures.

Read a report together with its linked protocol and validation. A hash checks
whether captured bytes changed; it does not prove who originally created a
file or whether its contents are historically authentic. Repeated copies of
one source are not independent corroboration. Calculations can be reproducible
without being physically validated for this building.

The main technical questions and limits are summarized in the
[charter](investigation/wtc7/CHARTER.md) and the
[completion audit](investigation/wtc7/completion-audit-2026-09-24/report.md).
Study folders preserve detailed work, including disagreements and unsuccessful
or incomplete routes; an individual report is not an accepted overall finding.

## Repository layout

- [`investigation/wtc7/`](investigation/wtc7/) — the WTC 7 investigation:
  questions, reports, protocols, source locators, data, code, and reproduction
  records.
- [`research/`](research/) — related scientific synthesis, video comparison,
  reconstruction workbench, and source-review material.
- [`faraday/`](faraday/) — an MIT-licensed Research Machine source snapshot
  used as the basis for Faraday-related integration work. It is research
  software, not evidence about the collapse.

## Provenance and distribution limits

This is a copy, not a continuation of either source repository's Git history.
The WTC 7 material was copied from the research worktree at source commit
`2fab1389ba8529494dd206a948014cd41cbf97d2`, including its then-present working
changes. Faraday was copied from upstream commit
`8d87c078fae6dcbda1541c4979568d88aa1fb9ae`; its separate local, unpushed
Vindication Machine changes were not included.

The separate Luna case-management chat was excluded. Source media and
investigation materials are retained at the repository owner's direction.
LFS-managed assets are identified in [`.gitattributes`](.gitattributes). The
captured YouTube watch-page HTML is omitted because it contained embedded
Google client-key material; its original SHA-256 and size are retained in
[`youtube-watch-source-note.md`](investigation/wtc7/release25-source-locator/sources/youtube-watch-source-note.md).
Absolute symlink targets that pointed into the original local worktree were
relocated or replaced with path-neutral fixture targets; source files were not
modified.

Individual reports control their own methods, provenance, limitations, and
validation status. Inclusion in this repository is not endorsement or
independent confirmation. Preserve the distinctions between source
observations, derived measurements, model-dependent results, competing
explanations, and causal claims.

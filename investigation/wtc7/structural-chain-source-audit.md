# WTC 7 structural sequence: a bounded source summary

This standalone summary replaces a previously linked, unavailable detailed audit. It describes NIST’s published simulation and key limits; it is not the original audit, an independent structural analysis, or a reconstruction of the collapse. No solver or underlying input deck was run for this summary.

## Published model sequence

[NIST NCSTAR 1-9A, §4.3.1 and §4.3.3](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9a.pdf#page=126) describes a 47-story LS-DYNA analysis initialized with gravity, modeled debris damage and temperatures, followed at 8.5 seconds of calculation time by fire-induced damage transferred from a separate 16-story ANSYS analysis. These are simulation steps; the reported sequence is not direct observation that real damage appeared instantaneously. NIST’s reference time for comparisons with video is the east-penthouse kink, not the start of the historical fires.

In the reported analysis, damage is concentrated near Columns 79–81; sections of Floors 13 and 14 fall onto floors below. NIST describes subsequent loss of lateral restraint and buckling, with failures progressing through the interior. This is a model of a regional failure sequence, not a finding that an entire floor initially fell intact through the full building. [NCSTAR 1-9A, printed p. 79 / PDF p. 130](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9a.pdf#page=130).

## Counterexample within the published modeling

NIST also reports an otherwise similar global run using the **3.5-hour** rather than **4.0-hour** ANSYS fire-damage state. Some girders failed, but the reported damage did not propagate into global collapse; NIST stopped the calculation **4.26 seconds after applying the damage** because the structure was stable and an initiating event had not developed. This is a useful model-sensitivity comparison within that finite run; it does not establish what would happen in every longer or differently parameterized analysis. [NCSTAR 1-9A, §4.4, printed p. 105 / PDF p. 156](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9a.pdf#page=156).

NIST’s broader conclusion is that fire-induced progressive collapse was the probable cause. The simulation description, by itself, does not independently authenticate every thermal history, connection failure, transferred damage state, or load path, nor does a difference between two selected model states establish an alternative cause. NIST also states that uncertainty increases as global collapse progresses. [NIST WTC 7 FAQ](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation).

## Tests that could change the assessment

Recover the member-level fire and damage outputs, damage-mapping and restart inputs, contact and residual-capacity definitions, and corresponding 3.5- and 4.0-hour runs. Independently test plausible boundary and connection variations against observations with stated timing uncertainties. A reproducible analysis showing the sequence persists across independently justified assumptions would strengthen NIST’s pathway; a credible analysis showing it arrests or conflicts with independent observations would weaken that particular pathway. Neither result alone identifies intentional intervention.

## Verification and boundaries

For this summary, the cited report pages were checked against a preserved copy of NIST NCSTAR 1-9A (SHA-256 `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`). The earlier detailed audit’s inspection and derivative claims were not reproduced here. The previous status entry remains historical and should not be taken to mean that its missing analytical files have been restored.

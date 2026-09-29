# Independent reading: NIST audibility-to-detection inference

September 20, 2026. Research-only, prior-informed computational second reader.
Frozen before reading root's observations or exchanging new interpretations.
This is a source-reading audit, not an acoustic reproduction, historical
soundtrack authentication, expert report, or causal ranking.

## Authority, coverage and visual acceptance

Main AGENTS.md, WORKFLOW.md, START-HERE.md and the complete investigation
CHARTER.md control. The source-of-truth-guardian, evidence-falsification-auditor
and PDF skills were applied: distinguish published assertions from reproduced
results, constrain negative evidence by detection opportunity, and inspect
complete pages rather than treating text extraction as visual review.

Protocol SHA-256:
`ea6bcc9ee92aeef7a1d89799401bc5ddfa82e19956d826853422abd65741fa55`.
Source: `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf`,
52,766,002 bytes according to the render receipt, SHA-256 independently
rechecked after reading:
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
Receipt `render01/receipt.json` SHA-256:
`291effcacdf986c7cffa16ca8c385193c66d63bece169836f9c38005424d3dcd`.

Only after root's terminal-receipt admission, I displayed the following complete
120-dpi PNGs at original detail, in batches of two, two, two, two and one:

| Physical / printed page | Admitted file | Actual displays | Visual acceptance and content identity |
|---|---|---:|---|
| 333 / 289 | `render01/p333.png` | 1 | Complete readable header/footer and §5.7.5 text; final paragraph continues on next page. |
| 334 / 290 | `render01/p334.png` | 1 | Complete readable continuation, §5.7.6 and Table 5–3, including final rows. |
| 399 / 355 | `render01/p399.png` | 1 | Complete readable §§8.9, 8.9.1 and opening 8.9.2. |
| 400 / 356 | `render01/p400.png` | 1 | Complete readable 8.9.2 continuation and Table 8–3 with source line. |
| 401 / 357 | `render01/p401.png` | 1 | Complete readable conclusion, footnotes 4–5 and start of §8.9.3. |
| 772 / 706 | `render01/p772.png` | 1 | Complete readable continuation and §D.4, including limitations and comparison paragraph. |
| 773 / 707 | `render01/p773.png` | 1 | Complete Figures D-15 and D-16; waveform/spectrum axes, labels and captions readable. Some raster graph text is soft but no observed missing glyph or panel. |
| 774 / 708 | `render01/p774.png` | 1 | Complete Figures D-17 and D-18, colored curves, legends, dual vertical axes, distance axes and captions readable. |
| 775 / 709 | `render01/p775.png` | 1 | Complete readable §§D.5–D.6, references and footer. |

Total: 9 unique full pages, 9 actual image displays, 0 repeats, 0 failed or
truncated image displays. All nine saved text extractions were read as assistance.
No new historical-media viewing/listening, earlier operational Appendix D pages,
other PDFs, cited references, network retrieval or solver execution occurred.
Incidental operational details on admitted pages are not reproduced here.

The render is **warned, visually usable**, not a clean font-environment result.
Each image command's preserved stderr has fontconfig diagnostics. The inspected
unique diagnostic lines in p333's stderr were inability to load the default
configuration and no writable cache directories. The receipt gives identical
stderr hashes for all nine renders; none of the text extractions has stderr
content according to that receipt. I observed no clipped text, missing glyphs,
missing diagram components or unreadable page identity on any of the nine pages.
That visual assessment does not establish typographic identity to a different
renderer or independently validate the plots' data.

Read-only verification actually performed: `shasum -a 256` on the source,
protocol, receipt and all nine PNGs; all PNG hashes matched the receipt.
`rg -n '"exit"|"status"'` on all eighteen per-command JSON records showed
exit 0 and returned status for every render/text command. Source/protocol pins
matched the admission. `cat` read the protocol, receipt, p333 command records,
and all nine page-text files. The diagnostic check used
`rg --no-filename '^Fontconfig' render01/p333-render.stderr | sort -u`.
These checks exited 0. I did not rerun rendering or claim independent
verification of every byte of the render program or every receipt product.

This reader previously performed the bounded text-only locator for these pages
and is familiar with earlier investigation work. Root and I share the source,
protocol and prior task context. Separate observation freezes limit immediate
interpretation exchange, but do not make this a blinded expert or independent
source-family replication. Root's freeze/hash notice arrived while this note
was being prepared; its contents have not been read.

## Page-pinned evidence ledger

### Recordings and listener observations — pp. 289–290 (physical 333–334)

**NIST's reported review, not observations made by this reader:** §5.7.5 describes
three street-level soundtracks at least 640 m from WTC 7, with numerous intervening
buildings. The most usable, Camera 3 on West Street, ran before and during
collapse; it picked up low-level street sounds and occasionally much louder
nearby operator voices. NIST reports listening and Aftereffects waveform review,
accounting for roughly two seconds of sound travel. It reports no sound/features
attributable to the building until global collapse, then increasing amplitude
without the loud explosive sound it sought.

Camera 3's operators reportedly first responded 2.5 s after global-collapse
initiation; a nearby West Street interview's participants responded just over
3 s after it. These are reported behavioral observations. They do not by
themselves prove an earlier sound was physically absent: attention, interpretation
and reaction latency are additional links.

The third interview, at West Broadway and Leonard Street near Camera 4, did not
show WTC 7 collapse. NIST says it aligned events with Camera 4 and observed a
response 1.3 s after east-penthouse descent began (also expressed relative to
the Camera 4 clip's start). With an approximate sound-travel allowance, NIST
attributes this response to hearing the penthouse collapse. Thus the source
does **not** report universal silence before global collapse: it reports a
location-dependent early response and attributes it to structural collapse.
No new timing correction or error calculation is made here.

Dust/smoke before penthouse descent is reported, with an inference of earlier
interior structural changes continued on p. 290. Table 5–3 explicitly sets
its time origin at initial east-penthouse downward motion and places global
collapse later. These are the report's compiled observations and interpretations,
not a second calibration of source timestamps, onset identity or cause. The
table includes early window opening/breakage; neither this fact nor dust alone
identifies an acoustic source or establishes a particular mechanism.

### Model-to-observation argument — pp. 355–357 (physical 399–401)

§8.9.2 describes a sequential scenario-to-interior-response-to-exterior-acoustics
analysis. Phase III inherits modeled pressure histories and window-failure
locations; it is not an independently measured historical source signal. The
report examines four combinations spanning two floor layouts and two source cases and predicts
audible sound from building faces. P. 356 expressly excludes adjacent-building
effects from that calculation and conditions its approximately 130–140 dB at
1 km statement on unobstructed propagation. These are published predictions,
not new calculations or measurements by us.

Table 8–3 gives illustrative everyday sound levels from Bearden (2000). It is
not a measured noise floor, microphone calibration, impulse detection threshold
or matched recording experiment for the three videos. The selected pages do not
provide enough measurement conventions to equate all entries directly with a
transient modeled waveform or a digital file's amplitude.

P. 357 adds qualitative urban-path reasoning: hard exterior reflections,
street channeling, echoes, potential in-phase addition, and possible wind
influence. Importantly, it also acknowledges attenuation behind buildings.
The reflection discussion is footnoted to Applied Research Associates email
of July 31, 2008; the extended human-audibility claim to Loizeaux Group
International email of August 5, 2008. The emails themselves are not reproduced
or reviewed here. This is attributed technical argument, not a receiver-specific
urban propagation simulation or a demonstrated calibration experiment.

The report combines expected sound, its stated lack of such witness/video
reports and other considerations into the broad conclusion that blast events
could not have occurred. The acoustic contribution should not silently inherit
the certainty of that conclusion. Likewise, the page's asserted absence of a
predicted window-breakage pattern has express coverage limits: views at collapse
were obstructed in part, and the visible-floor/time coverage is qualified.
This reading neither reproduces that visual comparison nor adopts it as complete
coverage. Preparation-detectability assertions are not a substitute for an
acoustic detector validation and are not adjudicated here.

### Acoustic quantities, assumptions and validation — pp. 706–709 (physical 772–775)

§D.4 says representative overpressure waveforms at predicted openings supply
the sound-distance predictions. NLAWS constructs a triangular wave from specified
wave parameters and uses spherical divergence in a constant atmosphere. That is
a specified modeling route, not evidence that the actual building emitted that
wave. The present scope did not examine or validate the upstream source-event,
interior propagation or window-response derivations.

P. 706 describes most of the sound as below 200 Hz and anticipates a low rumble.
Its roughly 40 Hz lower-audibility assertion is the report's statement, not a
hearing threshold independently verified here. The spectrum matters: an expected
low rumble need not have the subjective signature a listener calls a sharp
explosive report. A nondetection judgment needs a defined target signature,
time window and detection criterion rather than relying only on that label.

Figure D-15 (p. 707) shows a modeled pressure/time waveform and corresponding
pressure/frequency spectrum; D-16 shows a different representative waveform at
debris-damaged openings. Their vertical pressure units are psi; time is in
seconds and frequency in hertz. These are not microphone recordings, and no
recording-response transformation is shown. D-17 and D-18 (p. 708) have distance
in meters, overpressure in Pa and a parallel sound-pressure-level dB scale,
with several opening/case curves for each layout. They are smooth predictions,
not empirical receiver points, confidence bands or a camera-location map.
No curve values have been digitized or recalculated.

P. 706 again explicitly calls the work a simple estimate, omits adjacent
buildings and conditions the remote sound-level statement on unobstructed paths.
Its validation paragraph compares close-range predictions with limited published
sound-pressure values, citing Hamby (2004) and Kinney (1985). P. 709 identifies
Hamby's sound-level table and Kinney and Graham's book. This is a reported
plausibility comparison with limited literature, not zero validation; but these
pages do not display measured WTC-area transfer functions, receiver-specific
urban validation, residual/error analysis, or a source-to-camera reproduction.
The cited works were not opened, so their experimental pedigree or applicability
has not been independently established here. §D.5 retains the unobstructed-path
condition in its summary; it should survive downstream summary compression.

## Detection opportunity and strongest competing readings

**Positive support:** NIST did not merely assume there was no sound. It reports
multiple sound-bearing videos, ordinary ambient sounds and louder voices,
listening plus waveform review, a sound-travel allowance, location-specific
behavioral observations and a quantitative acoustic estimate with a limited
literature check. If the analyzed source scenarios, remote-path signal level
and preservation/detector opportunity are approximately right, absence of the
expected conspicuous signature can weigh against those scenarios. The described
signal margin is a reason to test detectability, not to dismiss the argument
solely because exact calibration is unavailable.

**Strongest objection:** The pages do not complete the bridge from a conditional
unobstructed acoustic prediction to detection in each actual, obstructed,
processed recording or to a reliably elicited witness response. There is no
source-specific microphone frequency response, orientation, gain/automatic gain,
limiting/clipping behavior, codec/edit history, original custody record,
band-limited noise floor, target detector criterion, or error-controlled
miss probability supplied here. Approximate synchronization/travel handling is
described but without an uncertainty budget. The low-frequency modeled signature,
different reported site responses and admitted shielding make the transfer
question substantive. These omissions bound our inference; they do not establish
that every such record is absent elsewhere or that attenuation actually erased
the modeled signal.

No physical SPL has been equated to dBFS or between-camera digital amplitudes.
No probability, universal acoustic exclusion, deliberate-intervention conclusion
or finding of NIST wrongdoing follows from this reading. The chosen scenarios'
claimed minimum is not independently established as a bound for every possible
mechanism; thermal, mechanical or other deliberate-removal proposals are not
automatically acoustic predictions of this calculation.

**Nonexplosive alternatives:** The report itself attributes an early response
at one site to penthouse collapse and later rising amplitude to global collapse.
Structural breakage/impacts, glazing/debris, ordinary traffic/sirens, nearby voices
and response to a visible event are plausible categories competing with an
explosive interpretation of an ambiguous recording or reaction. They are not
identified as the cause of an unseen or unheard specific signal by this review.
Conversely, nonresponse is weaker than an instrumentally demonstrated absence.

The strongest defensible result is therefore conditional negative evidence
against the analyzed conspicuous acoustic scenarios, with the end-to-end
detectability and scenario-generalization steps not reproduced. It is neither
an independently validated universal exclusion nor a demonstration that the
published inference has no evidentiary value. No causal ranking changes here.

## Discriminating records and bounded next test

Highest-value existing inputs are the exact three soundtrack originals/access
chains and the NIST event-alignment/waveform review products; original recording
metadata and processing history; the non-operational exported receiver-pressure
time histories with acoustic metric definitions; source-to-recorder path and
ambient-condition assumptions; and the July 31/August 5, 2008 correspondence
supporting the urban-path/audibility claims. Naming them does not authorize
acquisition, outreach, device reconstruction or a new solver run.

A separately declared next test should select one authenticated recording with
the best documented acquisition chain, establish its actual timing and usable
frequency/noise range, and test whether the **published predicted receiver
signature**, under explicitly bounded path and recording-response assumptions,
would have been discernible by a declared criterion. A digital injection test,
if later authorized, would remain a labeled synthetic sensitivity control,
not a historical sound or physical-SPL calibration. Missing response/path bounds
may prevent a quantitative miss-rate claim; that is an acceptance limit rather
than permission to choose favorable assumptions.

Receiver-specific validation and authenticated signal preservation showing a
large detection margin would strengthen the negative inference. Conversely,
documented filtering, obstruction, edits, noise or timing uncertainty sufficient
to defeat the specified detector would weaken it. Either outcome must distinguish
failure of the detection argument from affirmative proof of a collapse mechanism.
Work stops at this nine-page source audit and freeze.

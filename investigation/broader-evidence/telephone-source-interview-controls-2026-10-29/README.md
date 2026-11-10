# Interview-source controls: call identity, warnings and catalog associations

October 29, 2026. This new source review serves TEL02/TEL04 and existing AUD016 telephone questions. It preserves accounts and uncertainties; it does not establish coordinated obstruction or a historical call chronology.

Three public archival PDFs were acquired and all ten page images read: the four-page January8,2004 Arpey memorandum and two different three-page PDFs displaying the April26,2004 American Airlines SOC memorandum. Held Halleck/Houck interview pages3–4 and staff-report pages31/94 were reinspected. Native call logs, interview audio, carrier records and radar feeds were not acquired.

## What the catalog supplies

[NARA's MFR index](https://www.archives.gov/research/9-11/commission-memoranda.html) identifies NAID2609600 as the November19,2003 Marquis/Parfitt/Mulcahy/Bertapelle interview, nine pages. Its [current catalog entry](https://catalog.archives.gov/id/2609600) likewise says November19,2003 and nine paper pages. Yet the exposed [2609600_AASOC.pdf](https://catalog.archives.gov/medialz/legislative/rg-148/2524787/2609600_AASOC.pdf) says April26,2004 on page1 and contains three pages. The viewer also says three pages. Preserve descriptive fields, exposed link and downloaded-body identity separately.

The concrete [counterpart catalog2609603](https://catalog.archives.gov/id/2609603) describes the April26,2004 SOC interview and supplies [t-0148-911MFR-00017.pdf](https://catalog.archives.gov/medialz/legislative/rg-148/2524787/t-0148-911MFR-00017.pdf), also three pages. The acquired hashes are:

- Catalog2609600 PDF: c19d9e7ae4176fb411def7259f7657d2c80bf1bdf1a803c8f4fb1b7af83bab5f; 158,153 bytes.
- Catalog2609603 PDF: 1c331f5a4aa23f7299531ed295b04ee172d9f64bfc0df74b3a8aa8c8966a09f6; 532,100 bytes.

File bytes, extracted strings, page dimensions and decoded image samples differ. Manual reading found the tracked April26 statements in both sets of images; that is not exhaustive proof of textual or rendered equivalence. Export sequence and the catalog association's cause remain unestablished. The November19 nine-page interview remains unacquired. Two file forms are not independent interviews; this mismatch does not establish deliberate substitution or removal. See TI01/TI02/TI07 in [OBSERVATIONS.json](OBSERVATIONS.json).

## Qualification to our starting timing premise

Our initial protocol framed staff-report note259 as differently attributed Halleck–Herndon contact times. The surrounding [staff-report text, PDF/printed p31](https://www.archives.gov/files/research/9-11/staff-report-sept2005.pdf#page=31), requires a more specific distinction: the paragraph bearing note259 concerns notification that United was missing a plane and extension of American's ground stop nationwide. The same page separately describes a **9:16A.M.** Herndon conversation under note264.

[Note259, PDF p94](https://www.archives.gov/files/research/9-11/staff-report-sept2005.pdf#page=94), retains Marquis's approximately **9:00A.M.**, Arpey's **9:05–9:10**, and later AAL information placing a Halleck call after **9:10**. It says evidence relating to this call had not been found in the Commission's reviewed Herndon tapes/transcripts. Note264 separately identifies a recording/transcript source. Read each note with its body paragraph; do not expand the missing-record statement to every call or silently merge the two notes.

The [Arpey MFR, pp2–3](https://catalog.archives.gov/medialz/legislative/rg-148/2524787/t-0148-911MFR-00005.pdf#page=2), says all subsequent times are Central Time. On p3, **8:05–8:10** concerns a report of lost communications/transponder contact with a **United** flight, followed by extension of American's ground stop. It does not explicitly describe Arpey making or hearing the Halleck–Herndon call. With a conventional one-hour CT-to-ET offset, this interval would be9:05–9:10. That conditional arithmetic does not calibrate a historical clock or identify the call.

This qualifies our premise, rather than correcting a historical record. The initial wording is retained in [SCOPE.md](SCOPE.md); differently scoped accounts remain in TI03. Actual AAL answers of April26 and July7,2004, the SOC chronology and staff citation papers are needed to test how the narrative was assembled. The April26 SOC MFR is not assumed to be the separately cited April26 answer to Commission questions.

## Differing recollections of United's missing flight

The held [Halleck/Houck interview p3](https://catalog.archives.gov/medialive/97/6095/2609597/content/arcmedia/9-11/MFR/t-0148-911MFR-00011.pdf#page=3) describes Halleck learning United was missing a plane, contacting his United counterpart and then calling Herndon. It explicitly acknowledges difficulty recalling times and sequence; p4 reiterates that simultaneous events made sequencing hard.

The [April26 SOC memorandum p3](https://catalog.archives.gov/medialz/legislative/rg-148/2524787/t-0148-911MFR-00017.pdf#page=3) places a Herndon call just after the second tower impact, while explaining that SOC personnel thought the second aircraft might be AA77 because they did not yet know United was missing a plane. That memorandum also says Halleck did not know exactly when AA77 was realized missing and records substantial confusion.

This is a knowledge-order tension, not a verified contradiction about one uniquely identified call. Multiple contacts, different knowledge among personnel, imperfect recall and memorandum scope remain untested alternatives. Neither account is controlling. Original call/SOC logs and the later AAL answers are discriminating records. See TI04.

## Warning, information-control and display leads

On [SOC p2](https://catalog.archives.gov/medialz/legislative/rg-148/2524787/t-0148-911MFR-00017.pdf#page=2), personnel said they had not received a Herndon request to warn aircraft of cockpit intrusions and believed they would have complied if received. On p3 they reported no management decision to give such a warning, attributing the situation to confusion, conflicting reports and focus on safe landings. Nonreceipt and no management decision are distinct claims; neither establishes intentional withholding.

Page2 attributes **“contain and control information”** to Marquis and reports restricted internal access to the Flight11 manifest. These identify specific contemporaneous instruction, policy, distribution and access records to seek. The MFR alone does not establish the instruction's exact scope, legitimacy, effect or motive. Preserve timely notifications and ordinary operational controls as well as evidence of omissions. See TI05.

On pp1/3 the MFR distinguishes AAL's ASD from FAA's TSD. It records Commission staff telling Halleck that a primary track associated with AA11 continued south after impact, and SOC personnel saying an AA77 ASD track continued west after Pentagon impact. These are reported display observations, not raw radar or independent post-impact aircraft positions. Actual feeds, track identifiers, coasting/extrapolation definitions and clocks remain missing. Technical interpretation/testing belongs to the assigned technical investigation; none was performed here. See TI06.

## Verification and remaining work

[SOURCE-PINS.json](SOURCE-PINS.json) supplies URLs, access dates, hashes, page counts and source roles. [RESULTS.json](RESULTS.json) preserves exact byte/image/text comparisons; [compare_held_pdfs.py](compare_held_pdfs.py) reproduces the bounded comparison with pypdf and locally held source PDFs. It does not execute embedded content, normalize testimony, infer intent or authenticate prior history. All three downloads remain separate and unchanged. Unobserved Content-Type headers stay null.

[OPEN-TODOS.json](OPEN-TODOS.json) retains the missing November interview, source answers, contemporaneous call/notification records and technical inputs. All18 original five-track input/test criteria remain unfinished. Two new exact FAA cancellation searches found no correction, signed decision or closure record; unchanged failed routes were not repeated.

[CHECKLIST.json](CHECKLIST.json) accounts for the user requirements. [TEXT-CHANGES.diff](TEXT-CHANGES.diff) records additions against absent files at this unique new path, separately from PDF image reading. Earlier reports and original evidence are unchanged. Raw PDFs, scans, OCR/extracted text, contacts, private correspondence and strategy are excluded. Actual commit/ref/file verification is separately receipted; publication does not validate the historical claims.

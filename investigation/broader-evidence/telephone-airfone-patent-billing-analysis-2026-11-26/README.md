# GTE Airfone patent: billing and analysis record paths

## Source and observation

[US patent 5,123,112, Air-to-ground communication system](https://patents.google.com/patent/US5123112A/en), originally assigned to GTE Airfone and published June 16, 1992, was accessed November 26, 2026. The saved public HTML has SHA-256 `26eb036f1e570176641514804d9c5f3bd11e0386d08c469fe14a432b809022fc`. The description of Figure 10 states that the depicted central-processor routine copies *valid* base-station call records to a billing file and *all* base-station call records to an analysis file (Google Patents text lines 930–932; Figure 10, tasks 493–503). The description does not, in that passage, define the validation rule or prove the contents or continued existence of any actual analysis file.

## Interpretation and limits

This is a testable records-location hypothesis: **if** the relevant 2001 installed system used this depicted architecture, the analysis-side file and its collection, validation and retention rules could help determine which events appear in a billing extract. A patent is a description of an invention, not proof of actual implementation, version, deployment on a particular flight, successful logging or record survival. The possibility is not evidence that any specific call was made, omitted or concealed.

The previously reviewed [GTE manager interview and field qualification](https://github.com/AveLyra/911-conspiracy-investigation/blob/f120c724216fa87619a2c966612da8f6a597b1fc/investigation/broader-evidence/telephone-ua93-office-call-field-correction-2026-11-25/README.md) concerns a 2001–02 spreadsheet and is a separate source. Do not transfer the patent's proposed processing rules to that spreadsheet without a configuration and version join. Earlier differing call-duration and connection descriptions remain preserved at their original sources; this patent does not adjudicate them. It also does not establish semantics of the court's zero-duration label or of a different carrier's system.

## TODO and verification

Seek installed 2001 system/configuration and software-version records, source call-event exports, billing and analysis file schemas, validation rules, transfer and retention documentation, and the actual source-to-spreadsheet/exhibit worksheets. Compare any analysis and billing files by authenticated event identifiers while protecting personal data. A match or mismatch must be measured, not assumed.

The patent source was downloaded and hashed; the metadata and Figure 10 description were read. No installation, file existence, call reconstruction or clock alignment was tested. Native research copy and separate public derivative are retained.

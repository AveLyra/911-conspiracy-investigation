# GTE Airfone patent: call-reference numbering and ACIS IDs

TEL03 · November 25, 2026 · bounded public-source study

## Source and observation

[U.S. Patent 6,430,412 B1, “Call handoff”](https://patentimages.storage.googleapis.com/22/63/42/bf5a4fa903b758/US6430412.pdf), assigned to GTE Airfone, was filed October 12, 1999 and issued August 6, 2002. The PDF was accessed November 25, 2026; SHA-256 `e046fcfdde3980fec2c63894cd2eb7bbfb3dbfd64d11f8ae7897c84ac24b8286`. Physical PDF page 38, printed column 14, lines 16–35, describes a **call reference number** used during a handoff to distinguish calls from the same aircraft. In the described design the cabin telecommunications unit allocates numbers sequentially, beginning at 1 each time the aircraft phone system powers up. The page was visually inspected; the [patent text and metadata](https://patents.google.com/patent/US6430412B1/en) offer another locator. The filing date does not establish when this document became public or that the design was deployed in 2001.

## Comparison and limits

A separately preserved [FBI interview of a GTE manager, physical page 24](https://github.com/AveLyra/911-conspiracy-investigation/blob/04a89d22226600e8bb8ed6e2a5c12fbac3150ccf/investigation/broader-evidence/telephone-gte-116622-visual-2026-11-25/README.md) describes a unique **ACIS call ID** in a Flight 93 spreadsheet. The report attributes the description to the interviewee; it is not the native billing dictionary. The patent's call-reference number and the interview's ACIS ID have **not been shown to be the same field or namespace**. Preserve both descriptions separately. The reset rule does not establish that ACIS IDs were reused or that either description is erroneous. There is no established contradiction between them.

The patent describes a design and a handoff message, not a tested September 11 installation, a certified billing-export definition, a specific row, call completion, caller or recipient. The described handoff can include overlapping old and new paths; this does not show that any particular row or duplicate reflects a handoff. Do not infer fraud, coordination, or call content. A competing possibility is that the patent reference and ACIS ID are independent identifiers with independent allocation rules. The parent application and implementation/version history were not examined in this step.

## TODOs and discriminating tests

- [ ] Obtain versioned ACIS and airborne protocol dictionaries, namespace mappings, and the actual Flight 93 equipment/software configuration.
- [ ] Locate source spreadsheets, switch and power-cycle logs, and join/translation worksheets. If they establish an association between identifiers, test uniqueness within the relevant aircraft, system instance and time interval; seek counterexamples and document resets and missing data. This test has not been performed.
- [ ] Continue preserving the unresolved `0`, `130`, and `138` accounts and their provenance in the [existing field correction](https://github.com/AveLyra/911-conspiracy-investigation/blob/04a89d22226600e8bb8ed6e2a5c12fbac3150ccf/investigation/broader-evidence/telephone-ua93-office-call-field-correction-2026-11-25/README.md); this patent does not resolve those values.

Scope: one patent page and the already-reviewed interview description; no operational logs, native vendor dictionary, live test, personal data, raw billing record, or independent validation of the patent's deployment was examined. The native research copy retains the downloaded public patent; this public derivative publishes links and original analysis only. Prior records remain unchanged.

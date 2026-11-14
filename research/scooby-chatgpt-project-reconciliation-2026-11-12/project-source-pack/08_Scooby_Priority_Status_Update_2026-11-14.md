# Scooby priority status update — 14 November 2026 (R08 recovery)

This additive update supersedes the R08 file-access row in `07_Scooby_Priority_Status_Update_2026-11-14.md`. It does not replace the older files or claim a completed numerical benchmark.

## R08 — NIST heated-connection data

**Native source recovery is complete.** In a regular GPT-6 Pro Scooby chat (no Deep Research), all six official NIST XLSX routes were retrieved. Each route redirected from its official `/document/` URL (HTTP 302) to an official `nist.gov/system/files/...` file (HTTP 200). All six passed ZIP CRC and XLSX parsing checks. The unchanged original workbooks total **170,176,394 bytes**. Their workbook hashes, final URLs, retrieval timestamps, MIME types and sheet counts are in `provenance/native_file_manifest.json` inside the recovery package.

The package audit covers **166 delivered members** (165 files independently hashed), **30 sheets**, **nine measurement sheets**, **90,340 timed records**, **1,398 header occurrences**, and **217,389 formula cells**. It preserves formulas and cached values separately, source row numbers, comments and events, exact header cells, quality/gap scans, a corrected instrument map, source records, Technical Notes 2054/2055, drawing media and audit scripts. All 165 SHA-256 checks in the package pass; `unzip -t` reports no errors.

Key source-grounded corrections and limits:

- Fire measurement headers and the original instrumentation drawing identify vertical channels **VD2–VD5**; NIST TN 2055 §2.4 p. 23 says VD1–VD4. The discrepancy remains documented. The drawing supports a provisional west-to-east outer/inner/inner/outer mapping, while workbook dictionary location descriptions conflict; the raw descriptions and provisional diagram-based mapping remain separate. Ambient `CB-DA-AMB` has its own VD1–VD6 mapping and is kept distinct.
- Each fire workbook's measurement clock begins at gas flow, not ignition. Time alignment must state the origin and account for the specific test events. Some SC specimens store time-of-day values without a timezone in the workbook.
- The ambient file has six author-documented deleted intervals. One event has a stored elapsed value of 4,344 seconds that conflicts with timestamp-aligned measurement evidence supporting 5,930 seconds; the original cells are retained and the proposed reconciliation is explicitly derived.
- CB-DA beam-end force is a native formula derived from brace strain, with formula and cached result preserved separately. It is not a direct load-cell measurement.
- NIST documents thermocouple lead-insulation failure around ten minutes after CB-DA ignition; plausible numeric cells cannot automatically be treated as valid physical temperatures. A blank-cell mask alone does not establish sensor validity. Published uncertainty values are not calibration certificates.

**Gate:** source-access and native-file identity pass. A fully specified thermal-and-damage benchmark is **not yet ready**: clock alignment, physical channel-validity windows, thermal-input choices and constitutive assumptions must be fixed in a bounded input specification. Intact ambient and structural-response segments are available for a bounded next study. No structural model, calibration, holdout, Deep Research, contact or paid request was run.

### Deliverables and provenance

- Pro chat: https://chatgpt.com/g/g-p-6aed53a21aec8191b9aab8307b9c8e49-scooby/c/6af86ff2-e864-83ea-b130-fd61999c83c7
- Recovery ZIP: Library ID `libfile_a6fb95dff8b48191b5718515d4e54346`; **279,511,104 bytes**, SHA-256 `513dd716ee4c7df578dcc1e514be0583cc134cee9b8d2405368b4ee602622e6a`.
- Audit HTML: Library ID `libfile_742f577a4f608191850f257e56b77f0d`; the exact report is also included in the ZIP.
- Corrected instrument map CSV: Library ID `libfile_c92e3740fbe0819184a0f864d9e9f47f`; bundled copy in `audit/corrected_instrument_map.csv`.
- Delivery manifest JSON: Library ID `libfile_8cf4ca8b094481919d52d86c66c65230`; captured under `result-files/R08/`.
- GitHub staging preserves the 166 extracted package members plus four sub-100-MB ZIP parts; concatenating parts recreates the exact delivered ZIP hash.

## Other priority status carried forward

R01's complete 704-page accounting is in update 07. R21's selected engineering-value check remains 56/56, with whole-capture and historical/aircraft gates open. R03, R13 and R25 statuses remain those in prior dated updates; this R08 recovery did not reopen their source gaps.

## Suggested next research batch

Prepare a **bounded R08 input specification** before any model run: choose the measured target specimen and response, align each clock and event, freeze sensor-validity windows from documented failure evidence, select thermal inputs and material/connection laws, and define uncertainty and exclusion rules. Start with an ambient or intact structural-response segment that uses only verified channels. Keep fire thermal/damage validation separate until the sensor-validity and constitutive assumptions are justified. Then resume R03/R13 when their identified original media/records are accessible.

> **Historical research:** This document reports a prior source review, not a current instruction or new model run. Missing sources and run artifacts are identified; see the [publication note](../README.md).

# Exact-source acquisition log

Navigation initiated2026-09-10; confirmed completed sessions and source integrity2026-09-11. No new search query was issued; the parent fuel search remains8/8 exhausted.

## Public route and results

Followed actual official links: WTC7 FAQ → Publications and Reports → final reports → NCSTAR1-1J catalog / WTC7 errata catalog → their actual PDF downloads. Five distinct navigation links after the publications index, within the prospective six-link limit. Reopening the same catalog pages and retrying the same exact URL after DNS failure do not add new source branches.

- Equipment catalog: https://www.nist.gov/publications/documentation-fuel-system-emergency-power-world-trade-center-7-federal-building-and
- Equipment PDF: https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=101010
- Errata catalog: https://www.nist.gov/publications/errata-nist-ncstar-1a-nist-ncstar-1-9-and-nist-ncstar-1-9a-federal-building-and-fire
- Errata PDF: https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=901225

Initial restricted downloads failed DNS (curl6, HTTP000, zero body bytes). Approved same-URL network retries used HTTPS-only curl, maximum60s, separate attempt02 output/header paths. Confirmed live sessions11970 and27039 were polled, not restarted; both returned exit0, HTTP200, zero redirects, and the same effective URLs. Bodies:578804 and97156 bytes respectively; SHA256 and page counts are in [SELECTION.md](SELECTION.md). Original headers remain local-only and unprinted; this log does not clear any metadata for export, commit, feedback or bridge transfer.

The `file` utility misleadingly reported zero pages for encrypted NCSTAR1-1J; Poppler and pypdf both locate84. PDF metadata title is a template title, not authoritative identity. Root inspected the complete cover; substantive edition check follows.

## Initial rendering failure and correction

An identity-cover command omitted the previously required explicit font configuration. Session19390 emitted missing-configuration/cache warnings; the output was truncated by the tool and a complete stderr log was not preserved locally. These warnings and that limitation are retained here. After warnings established the configuration fault, a distinct configured-cover command used the existing NIST font config and finished exit0 without warnings (session30966). The initial session was later polled with an interrupt request and returned terminal exit0; no claim that it was interrupted or had warning-free output. A read-only `ps` inspection was denied by the local sandbox; no alternate process-inspection route was attempted. Initial identity PNGs are retained but excluded from accepted visual-fidelity checks.

Configured subsequent rendering uses bundled Poppler, captured local stderr and separate outputs. No FEMA/UQ denial route was retried, no source or case data transmitted to Sherlock/Faraday.

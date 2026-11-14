# NARA disposition case-file series: a possible schedule retrieval route

November 14, 2026 UTC · B129 / PD04–PD05. A National Archives catalog search located a series of original **external disposition case files**, including forms and correspondence. Its container list offers a specific physical-record lead for the disputed schedule citation. **The individual 2002 schedule has not been found or inspected.** This supplements the [approval-face comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/d80eb3d55ba13225cd52792b0756aa8331cf470e/investigation/broader-evidence/faa-schedule-approval-face-2026-11-14/README.md).

## Direct catalog observations

- NARA describes [series 7461357, External Disposition Case Files](https://catalog.archives.gov/id/7461357), as records of federal-agency disposition proposals. Its scope note says a typical file contains a completed Standard Form 115 and correspondence on a proposed disposition. The description gives inclusive dates **1935–2001**, states that the material is **partly restricted**, and describes numerical arrangement by record group and then case number within chronological segments. These are description-level statements, not proof any particular file is present or releasable. [Captured catalog search response](https://catalog.archives.gov/proxy/v3/records/search?q=%22External+Disposition+Case+Files%22&rows=50)
- The same catalog response's container list gives **“Container 9: [UD-24D 4] N1-374-00-001 THRU N1-412-03-011”**; container 8 ends at N1-372-02-009 and container 10 begins at N1-412-03-012. This is a listed range, not a contents inventory. Under a simple numerical comparison of the group, year and sequence components, **N1-398-02-001** lies between the stated endpoints. That arithmetic does not establish that the cited item exists in that box, was filed under that normalized spelling, has been transferred, is publicly accessible, or is the schedule cited by DOT.
- The list also gives other schedule endpoints with year codes after 2001, including **N1-412-03-011**. Preserve this alongside the separate inclusive end date **2001**. The relationship between the date metadata, job-number year codes and container list is unresolved; no error or later accession is assumed.

## Search controls and limits

The [2012 DOT notice](https://www.govinfo.gov/content/pkg/FR-2012-07-20/pdf/2012-17696.pdf#page=4) cites **N1–398–02–1, March 3, 2002**. A catalog exact-phrase search for its zero-padded variant **“N1-398-02-001”** returned zero hits. The same query method also returned zero for **“N1-398-00-001”**, even though NARA separately hosts the [known signed 2000 schedule](https://www.archives.gov/files/records-mgmt/rcs/schedules/departments/department-of-transportation/rg-0398/n1-398-00-001_sf115.pdf). The series-title search returned the series record. The failed known-schedule control means the two zero-hit results do **not** establish either schedule's absence from the catalog or the physical collection; search indexing and punctuation are unresolved. [Exact 2002 query](https://catalog.archives.gov/proxy/v3/records/search?q=%22N1-398-02-001%22&rows=50) · [Known-schedule control](https://catalog.archives.gov/proxy/v3/records/search?q=%22N1-398-00-001%22&rows=50)

No conclusion about the 2006 FAA case, disposal, concealment or motive follows. These catalog results do not resolve the **N1-398-00-1 / N1–398–02–1** citation and date observations already preserved in the predecessor report. The signed schedule and crosswalk remain unacquired.

## TODOs and tests

- [ ] Inspect the relevant NARA case-file finding aid or the contents of **series 7461357, UD-24D 4, container 9**, subject to actual access conditions; seek the specific 2002 job and its SF 115, associated correspondence, amendments and cross-references. A physical range is only a lead.
- [ ] Clarify the series' inclusive-date metadata versus the later-coded container endpoints, without assuming that either description controls the other.
- [ ] Obtain the actual case-specific schedule designation, holds, transfer and disposition documents for **042R0122001 / CC-2006-085**, as well as the corrected answer, delivery acknowledgment and signed action/no-action decision. None was acquired here.

## Reproducibility and source scope

On November 14, 2026 UTC, three catalog search responses were captured and their HTTP statuses, lengths, SHA-256 values, query URLs and hit counts recorded in [SOURCE-PINS.json](SOURCE-PINS.json). The series-title response was inspected for the title, scope, dates, arrangement, access status and container list. The range comparison above is a numerical check of normalized components, not an item-level inventory match. Catalog metadata and coverage can change; the separately preserved response pins the observed state. The public package contains analysis, provenance and an additive text diff; it does not republish the full response.

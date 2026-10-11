# Case 817373 interactive route log

2026-10-04. Research-only selected browser-output record, not raw site HTML,
an HTTP archive or an original exhibit. The separate protocol was saved and
hashed before browser navigation: SHA256
`eefd015e9c25729f165edb2da8bd804ff0f0af1276b0f8bf997e034e5f7a60ab`.
All external actions are root's; peer review is local and not a second search.

## Setup and control selection before submission

Targeted tool discovery found no Tax Appeals case-search connector. The browser
is needed to test the actual form rather than repeat static navigation.
Persistent browser/agent bindings were absent. The documented setup selected
Codex In-app Browser, ID2; its tab list was empty. Created tab1, then made
one navigation to `https://www.dta.ny.gov/`. Complete browser instructions were
read, recovering an explicitly truncated accessibility section before use.
No credentials, browser history, cookies or profile data were inspected.

Navigation and first accessibility observation completed by 13:13:30 UTC
(preceding clock sample 13:12:48 UTC). Actual title: New York State Division
of Tax Appeals Tax Appeals Tribunal. The relevant returned controls were:

```text
26 text Search all Tribunal decisions and orders, Administrative Law Judge determinations and orders and State Tax Commission decisions.
27 container Description: DTA homepage search box, ID: form2
28 text Search Tax Appeals Cases
29 text field (settable) Search Tax Appeals Cases, ID: home-search-input
30 pop up button (collapsed, settable) Description: select search category, Value: in Tribunal Decisions/Orders, ID: home-search-select
31 menu
32 (selected) in Tribunal Decisions/Orders
33 in ALJ Determinations/Orders
34 in State Tax Commission Decisions
35 button Search Cases, ID: home-search-submit
```

The initial full accessibility return was truncated after unrelated footer
content; the complete control subsection above was visible. The page's update
label was October 1, 2026. This is a site update label, not a record date.

**Prospective choice fixed now, before typing or submitting:** enter exactly
`817373` in Search Tax Appeals Cases, leave the observed default
`in Tribunal Decisions/Orders` unchanged, then click Search Cases once.
There is no case-number-specific option in the displayed three-option list.
This is a Tribunal decisions/orders search, not an all-category or original-
exhibit search. No subsequent ALJ/Commission query is authorized by this unit.

The independent prospective review found no blocker and clarified that an
ambiguous/timeout response consumes the single submission attempt; it is not
permission for a second click. A typed field is not a submitted query. Actual
submission/result and closeout will be appended after observation.

## Actual submission and delayed result

The pre-submission log above was frozen at SHA256
`160ce514da2e9d1431a0775c610a38cce29bdeeb15f9c991ee4c10364d3a227e`.
The input action returned field29 with `Value: 817373`; the category was not
changed. At 13:14:21–13:14:24 UTC, root clicked the observed Search Cases
button35 once. It navigated to the actual URL
`https://www.dta.ny.gov/search/?q=817373&site=Tribunal_decisions`, title
`Search DTA: 817373`. These are observed values, not a constructed endpoint.

The first post-click accessibility state showed the query field, a Search
results heading and no entries, explicit zero-result message or loading marker.
It was not classified as a completed zero-hit response. One screenshot, captured
by 13:15:03 UTC, resolved the missing visual context: the first result page had
populated. One subsequent accessibility read recorded the now-visible results
and exact links. This was a delayed change on the same submitted page, not a
second query, navigation or refresh. The loading state was inferred from the
change; no explicit pending indicator was observed. There were no further
page-state reads, clicks, pagination, filter changes or result-source opens.

**Minor protocol deviation:** the protocol conditioned the one follow-up DOM
read on an observed pending state. The initial interface had no explicit
pending marker, so the final accessibility read did not meet that literal
prospective condition. Later population cannot retroactively satisfy it.
The deviation is retained, not repaired by changing the protocol. It added one
same-page observation, not another submission; the independently preserved
screenshot already establishes the populated two-result state.

Selected final accessibility values:

```text
60 text Showing 1 - 2 of 2
62 text within Tribunal Decisions/Orders
66 link ... /pdf/archive/Decisions/817373.dec.pdf ... I:\817373.dec.rtf
69 link ... /pdf/archive/decisions/817373.dec.pdf ... I:\817373.dec.rtf
75 text 1
79 text 10
```

| Returned order | Exact observed locator | Displayed date and disposition |
| --- | --- | --- |
| 1 | `https://www.dta.ny.gov/pdf/archive/Decisions/817373.dec.pdf` | September 12, 2014 search label. Decision metadata for case 817373, not an exhibit/index description. Not opened; bytes and equivalence to the held lowercase-path file untested. |
| 2 | `https://www.dta.ny.gov/pdf/archive/decisions/817373.dec.pdf` | October 16, 2003 search label. This URL matches the held decision's locator. Not reopened; no new byte/version check or original exhibit acquisition. |

Both snippets describe a sales/use tax matter with a period beginning December
1, 1994. Snippets and their displayed dates are not verified issuance or
transaction dates. The held decision was previously read as dated April 3,
2003; these search labels do not supersede that reading. The two case-variant
URLs are retained literally, not silently normalized or declared byte-identical.
They provide no demonstrated independent transaction source. Neither qualified
as a case-detail/index or target-original locator under this protocol.

The populated page also exposed All, ALJ Determinations/Orders, State Tax
Commission Decisions, Advanced search and Remove filter controls. None was
used. The two-result count applies only to this query/category/result page,
not all official holdings or other categories.

## Preserved capture and verification

[result.jpg](result.jpg) is the single unedited browser screenshot, 1280 by720
JPEG; acquired bytes SHA256
`f55d57b73116134934e2602c6563f642ca6567114b345e4e19f89320ac0c6c5f`.
It shows the query, category/count and both result entries; its lower edge
cuts off part of the page-navigation area. This is a viewport capture, not a
full-page export. The subsequent accessibility read supplies pagination and
exact-link context. The screenshot was viewed directly when captured.

The capture was first saved in a new local temporary directory. A default-
permission copy to the isolated worktree failed (`cda7c4`, exit1), and a
subsequent hash attempt correctly reported no file (`16bed6`, exit1). `file`
returned exit0 while printing that the file was missing (`87a721`); exit0 was
not treated as verification. The specifically approved single-file copy then
succeeded (`455b41`, exit0). `shasum -a 256` matched the preserved and temporary
copies (`47fb7d`, exit0); `file` confirmed JPEG1280x720 (`0957cf`, exit0).
No screenshot regeneration or image editing was performed.

Actual route totals: one homepage navigation; one form submission; one initial
post-submit accessibility state, one screenshot and one delayed-result
accessibility read; two displayed result entries; zero of two eligible detail
opens; zero original downloads. No retry, query expansion or barrier bypass.
This is completed bounded interactive coverage, not a custodian response or
complete case-file search. Separate local review remains to be recorded.

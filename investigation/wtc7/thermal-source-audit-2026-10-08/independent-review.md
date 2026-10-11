# Separate AI citation-scope review

October 8, 2026 local. Research-only review of the frozen inputs below.

## Finding

No material correction is required to the report's qualified conclusion. The
optical/video methods and ideal-gas explanation support its distinction between
measured material behavior and inferred pressure, without supplying a calibrated
acoustic result. Preserve the contrary observations: few/possibly no observed
microexplosions in section 3.3, and the authors' description of minimal gas
release in the conclusion. Neither is a quantitative gas or microphone reading
in the inspected text. Mechanical restraint against expansion remains a
hypothesis, not evidence of zero pressure or field silence.

The report appropriately does not infer historical use, rank causes, or turn
unavailable evidence into a demonstrated absence. No new accepted finding,
human acceptance, legal promotion, or source repair follows this review.

## Review scope and independence

A separate AI agent read the protocol, report and access record fully. Before
reading the report, it independently opened the same [author-posted article
text](https://www.researchgate.net/publication/379464804_Identifying_a_combination_of_intermetallic_and_thermite_reactions_that_result_in_a_non-expanding_compact)
and reviewed selected returned passages covering methods, sections 3.3–3.5,
and the conclusion. Relevant reader locators include 816–920, 1232–1236,
1670–1719, 2097–2142 and 2331–2368. These are navigation locators, not preserved
source-byte identifiers. Searches for pressure, sound, acoustic and microphone
supplemented reading; negative matches are not completeness proof.

This was not blind: the reviewer knew root's question and provisional reading.
Both agents used the same extracted webpage, with artifacts. No PDF, figure
pixels, supplements, raw source snapshot, experiment, or complete-paper review
was performed. Recommendations/citing papers after this article's references
were excluded. Root's earlier failed access outcomes remain root-reported;
the reviewer did not repeat those requests. The bibliography and displayed
uploader attribution were observed, not independently authenticated.

## Frozen inputs and checks

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| PROTOCOL.md | 4061 | fd0ce93671d5976ad475a4bc5d9a10f021097ca961ace6c4642f73a3a5b96910 |
| report.md | 3237 | 9da5a443c0cd56ad093d268bd9abadcda706dd797fda90765b4aeb661d52502d |
| source-access.json | 3593 | fdddf71c94e42b1babd6c30bf515db0618d4609d9f4898ac838264c11e948d4a |

Complete local reads and initial hashes/counts succeeded (receipt `5f2ec0`).
Final checks, run from this unit directory:

```sh
shasum -a 256 PROTOCOL.md report.md source-access.json independent-review.md
wc -c PROTOCOL.md report.md source-access.json independent-review.md
wc -w independent-review.md
python3 -m json.tool source-access.json >/dev/null
```

Inputs matched the pins above; the access record parsed successfully. No failed
review command or source repair occurred. Only this new review file was written.

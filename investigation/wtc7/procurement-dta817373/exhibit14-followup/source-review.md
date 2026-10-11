# Local source review: Exhibit14 locators

2026-10-04. Independent research review by `/root/sibling_byte_audit`.
**The selected source identities and locators pass; no protocol blocker found.**
Exactly two complete primary-decision pages were read, physical/printed23–24,
including footnote6, using the existing text and full-page images. No external
query, acquisition, rerender, new code or review of additional decision pages.
This is not inspection or authentication of the original Exhibit14 documents.

## Findings and competing readings

| Target | What these pages actually establish |
| --- | --- |
|Exhibit14 p9|The decision describes a contractor exempt purchase certificate. It says the certificate was **presumably** why sales tax was excluded from the payment; that causal explanation is qualified, not independently verified here.|
|Exhibit14 p10|A photocopy of the canceled check described as payment for invoice12318, excluding the billed sales tax. The check itself was not inspected.|
|Exhibit14 pp11–15|A photocopied invoice12318 itemizing purchased equipment with sales tax billed. These pages supply no invoice date, item list, installation locations or performance date.|
|Exhibit14 p39|A separate maintenance invoice dated December1,1994, billed to Silverstein Properties:950 dollars plus78.38 tax, service December1,1994–January1,1995. **That date does not date invoice12318.**|
|February28,1990 letter/proposal|The letter attributed to Jim Henry transmits a revised contract proposal. This is the letter's stated date, not a date assigned to invoice12318.|
|Maintenance contract and inventory|The account places contract execution in early1990. Petitioner supplied an inventory containing CCTV and access-control equipment. Exact exhibit-page locations for this contract, inventory and letter are not supplied on23–24.|

Footnote6 on23 distinguishes3,314.84 dollars **claimed** as paid tax from712.79
billed on12318 but excluded from its payment, leaving2,602.05 paid for the
maintenance services. The visible superscript6 is a footnote marker, not another
decimal digit in the2,602.05 amount. These are tax amounts, not equipment prices.
The text extraction runs the superscript into the number; the image resolves it.

**Strongest ordinary reading:** the account affirmatively describes a preexisting
working CCTV system, an ordinary maintenance contract, recurring monthly service
charges and equipment procurement/payment documentation. It does not merely
lack accusatory language. Equipment condition is attributed to the1990 letter,
not an independent technical inspection by this reviewer. The initial1,541.66
monthly fee and later950 fee are distinguished; the source qualifies the
inferred reduction as an appearance from the later invoices.

**Strongest contrary/limiting reading:** legitimate maintenance does not exclude
other activity. Access-control equipment appears expressly in the described
inventory, so reducing the document to camera hardware alone would omit content.
But equipment category is not evidence of particular personnel's2001 access,
exclusive security control, structural work or an intervention. A tax decision's
account cannot settle those questions. Originals could alter dates, item scope,
payment relationships or contractual limits; an original-record search does not
require first demonstrating a contradiction or wrongdoing.

Evidence ceiling: A for what the held decision visibly says; its adopted finding
supports the1990s maintenance relationship, but is a derivative description of
the underlying commercial records. Repeated copies of this decision would not
be independent confirmation or recovery of Exhibit14. No-original retrieval
would not itself establish loss, withholding, destruction or concealment.

## Identity, mapping and retained diagnostics

Paths in this table are relative to `../` (the parent procurement unit), except
the present `PROTOCOL.md`. All eight hashes were checked before and after the
two page views and stayed equal. Actual byte counts match the retained records.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
|`source/817373.dec.pdf`|294760|`962c2f2faf8fa7f17ef7a16efa6cbc8d036e4d82b6d8cc86e9237c2ff3234acc`|
|`render01/receipt.json`|20163|`d834d55db51091fd11207e79bfc3cbd762b78f4d3cf7fec9e23df35b6141d7f1`|
|`render01/start.json`|1668|`ff3000a368a6d9be195f1dbe73145d7b415a88b4cf7f7b9b0fae34174aad89f4`|
|`render01/p23.txt`|1827|`1316598efbb846a44bd3018fe5388cc941543b1e8902f49c6c19916730558c31`|
|`render01/p24.txt`|1892|`25d09304939769659f88944464e695294a6f555996eb9a1aea62166dfa2c5641`|
|`render01/p23.png`|203825|`2450c15de088053d262d7c665bb8578dd35f2f8cb13918f4c7aaf852f6ce12d3`|
|`render01/p24.png`|198908|`55fa4d01e5ad89142626662117ba9b36f61eba781f3220cbcb4febe2fc63408d`|
|Current `PROTOCOL.md`|5974|`d248ca7bed2cc7a1b0355c641184822a1b036e9b898a92bfb86a2d1b0a8cb359`|

Complete `render.py` reading confirms physical-page-minus-one mapping and150dpi
full-page generation; its current SHA matches the retained pin
`8562380b6db77be55c3ba557398bf53426f5c50d001d192f60d5ba8104a9e442`.
PNG metadata and receipt both identify1275×1650 RGB full pages. Both complete
views succeeded at original detail; labels23/24, the split paragraph and
footnote6 were readable, with no noticed clipping. No view failed or was retried.
Both pages retain `No common ancestor in structure tree` / `structure tree
broken, assume tree is missing` render diagnostics. Earlier same-renderer
reproduction is a read prior result, not rerun here or a second-engine fidelity
certificate. Hashes establish held-byte integrity, not original-record authenticity.

## Actual commands, scope and failures

`cat` read the complete new protocol/parent report (`7d508f`), integrity review
(`bad986`), renderer and both page texts (`74458d`). `jq` selected the two receipt
page/product records (`f244ff`); `file` checked PNG metadata (`547bee`).
`shasum -a 256` checked the eight before/after pins (`66becb`, `510013`);
`stat -f '%z %N'` confirmed sizes (`14a370`). All named commands exited0.
The two `view_image` calls displayed only p23/p24; no new PDF render occurred.
An initial second command used a working directory missing its leading slash
and failed process creation before execution; the corrected control-pin check
`1f5c8f` exited0. No substantive test or source failed, and nothing was repaired.

Current main AGENTS/WORKFLOW/START-HERE and full CHARTER were reused from complete
earlier reads only after current hashes matched; charter remains54a4a235… and
AGENTS934437bf…. PDF/evidence/source-preservation skills were read fully; their
source-layer and complete-page safeguards shaped this review. Selected receipt
fields, not all37 pages/products, were rechecked. Only this working note was
created. Root owns external retrieval; later result review awaits a separate GO.

# DEM-05 independent final report/receipt review

2026-09-20 UTC. Bounded research-only AI review. No network, additional source,
media, PDF, solver, or historical-measurement work. Only this note was written.
Evidence-audit/source-of-truth controls preserve attribution and source-family
limits; neither interpretation agreement nor hashes authenticate history.

## Reviewed versions and frozen notes

Read report.md and execution.md completely and compared with both previously
read frozen notes. Inspected saved article.html lines 880–951, including the
captions and complete body passage containing the matrix's critical pins.
Those passages match the previously read web article's reported scope.

- report.md: `d6894616d2ba70afc784c13bc53074b1f3d9fe0137b4ca1687697873f53a8176`
- PROTOCOL.md: `4ecb28140b44a1e28c771901f1050a7325411d9103a8d0ef25605e60a5ba99d3`
- execution.md: `4be1ddb1e7bdb5132fe79aeffa6f464e7f9a5be429905b750a99272729063435`
- root-notes.md: `df8c7b00c8f9ebf0bdc19c833a575316c50212cfb0c9419a06bf09fb58ca7d2b`
- observer-notes.md: `8341ad006c0699afb4b427d0dfba56ca9a1af72abde3452516a0e462ea75175d`
- source/inventory.sha256: `053f7bd192374d2335c0e664907015a420a3f390fc703618f5dae8f7b170368f`

Both frozen-note hashes match their original notices; neither note was edited.
These pins identify the actual reviewed versions, not future root revisions.

## Independent receipt checks

From source/, actual commands (all returned exit 0):

```sh
shasum -a 256 -c inventory.sha256
stat -f '%N %z bytes' article.html article.headers
rg -n -i '^(HTTP/|date:|content-type:)' article.headers
ruby -rjson -e 'expected=%w[article.html article.headers].sort; actual=Dir.children(".").reject{|x|x=="inventory.sha256"}.sort; puts JSON.generate({exact_file_set:actual==expected,files:actual.map{|x|{name:x,bytes:File.size(x),regular_file:File.file?(x),symlink:File.symlink?(x)}}}); abort "unexpected source file set" unless actual==expected'
```

Results: both inventory entries OK; exact two-file set excluding the inventory;
article.html 149,540 bytes; article.headers 487 bytes; both regular files and
neither a symlink. Whitelisted headers: HTTP/1.1 200 OK; date Sun, 20 Sep 2026
07:59:22 GMT; content type text/html; charset=UTF-8. No cookies were printed.
The inventory pins are article.html
`76f47c534d30bdae61aafb63ae40e6a808f4b4744335fdf7cf83cc889175834a`
and article.headers
`43f615ff9a9980506f430c7e9fa2ab96880874bc8f8cc3e3280b7c54a6a9586b`.

The saved response verifies these bytes/status fields, not the original client
exit code, effective URL, or client version; those remain root's execution
account. This reviewer did not rerun acquisition. Hash integrity is distinct
from source authenticity, completeness of history, and correctness.

## Disposition

No material discrepancy or scientific overclaim found in the reviewed report.
It preserves both readers' distinction between attributed activity and future
plans, separates objects and evidence layers, and leaves residual mechanical
state unresolved. It does not turn a planned destination into a measured
footprint, transactions into a mass inventory, or shared publications into
independent event-level corroboration. Its confidence labels are explicitly
claim-specific rather than claims of independently verified historical truth.

The report appropriately retains the contrary possibility that later execution
could make the preparation lead more informative, without assuming that it did.
No correction is requested. Root retains responsibility for later report/index
changes and final link/whitespace checks. No new causal ranking follows.

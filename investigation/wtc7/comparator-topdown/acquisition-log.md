# Top-down source retrieval, rendering and coverage

Research only, September 20, 2026 UTC. The unchanged PROTOCOL.md has SHA-256
`dabd740fcf6647b920d72d4be4a50aeeb5b42ae456aad9466edafe6161e1d33a`.

## Initial retrieval and failures

The web reader returned403 for the named intro PDF. The ordinary direct HTTPS
download dispatched in the same tool orchestration returned200, without changed
credentials, proxy, user-agent workaround or access-control bypass. The direct
request completed with1,817,040 bytes at the original URL. No retry of the403
route was made. Exact headers are preserved in `intro-headers.txt`.

Root mistakenly ran pdfinfo while the download session35071 was still live:
the then491,520-byte incomplete file produced parse errors/exit1. That is a
premature inspection failure, not evidence of a corrupt final publication.
The same live handle was polled, not restarted. It later completed exit0.
Only then did full size/content-length and SHA checks and complete pdfinfo pass.

Acquired PDF `C046_006-intro.pdf` SHA-256:
`8ce337aaa3099a3b9a390d4f540a8306500d21961f382d3997aa7ffba9cd53ed`.
One A4 page; PDF1.6; print/copy permitted, modification/annotation disallowed,
no password needed for reading. Original PDF remains unchanged. Embedded
2013 metadata and HTTP2019 last-modified are not interchangeable publication
dates. The page identifies *Report of Taisei Technology Center*,2013 No.46,06.

The preferred bundled Poppler render completed but emitted missing Japanese
CMap/font diagnostics. Root viewed its complete PNG once: major Japanese body
text is absent. This render (`C046_006-intro-page1.png`, SHA-256
`e4412dd92d19b396dc6587e4fad691c2b9700860d698af73936e187d4622d509`)
is retained and excluded as a complete-page reading. Bundled pypdf6.10.0
extraction likewise returned garbled Japanese; it is not translation evidence.
The bundled runtime lacked PyMuPDF; the already-installed Python3.13.7 runtime
has PyMuPDF1.27.2.2/MuPDF1.27.2. No package was installed.

The alternate renderer produced `C046_006-intro-mupdf-page1.png` at150dpi,
RGB/no alpha, with no MuPDF warning text. Its extracted Japanese is legible;
root separately inspects the complete page before relying on it. Source PDF
hash checked unchanged before/after rendering. This is a rendering repair,
not an alteration/reconstruction of source content. Visual review remains
required; successful extraction alone is insufficient.

## Prospective navigation amendment before further retrieval

The admitted source is a one-page overview with no PDF links, not the complete
engineering paper. The initial one publisher index at
<https://www.taisei.co.jp/giken/report/2013_46/> was unavailable through the web
reader; one ordinary direct request returned200/7,295 bytes and is preserved
as `index-2013_46.html` with headers. Its actual navigation supplies
`feature/index.htm`, labeled the special-feature section; the source page is
itself labeled as article06 of that feature.

Before opening further material, extend only the navigation allowance from
one index to **at most three same-publisher HTML pages total**, following this
observed feature link and, if necessary, its explicitly linked article page.
The maximum remains two acquired PDFs of the same article, no search queries,
no guessed full-report URL or other article chase. This disclosed amendment
responds to the site's actual navigation depth; it does not change evidence,
matching criteria, source grades or the requirement to retain unknowns. If no
explicit full-text link is found in those steps, stop that route and report
the summary-only limit. No new authority, private access, media or spending.

## Actual publisher chain and completed full-paper acquisition

The amended route was completed without another search: the feature index's
article06 anchor explicitly points to `../abstract/detail/B046_006.htm` with
the same Japanese title/authors. That article page explicitly separates the
overview `../../intro/C046_006.pdf` from full text `../../paper/A046_006.pdf`.
The source HTML files and their individual response headers are retained.
Both additional HTML requests returned200 (6,935 and7,316 bytes).

Final PDF URL:
<https://www.taisei.co.jp/giken/report/2013_46/paper/A046_006.pdf>.
Download handle68916 completed exit0, HTTP200,1,878,298 bytes at that URL.
Root waited for that terminal result before parsing/hashing this file.
`A046_006-paper.pdf` SHA-256:
`a6a6fb65396ebf8ac4f7e147e40f08a178cbd89fabf97b90a1c4448352aaf4c8`.
`paper-headers.txt` preserves Content-Length1,878,298. pdfinfo26.05.0 reports
8 A4 pages, PDF1.6, print/copy permissions and no required reading password.
All8 pages are within the prospective12-page full-reading cap. There were no
further source requests. Actual total: five successful direct captures (two
PDFs/three HTML pages), two failed web-reader opens, no search queries, no
video/audio acquisition. No actual origin access-control denial was bypassed.

## Exact rendering method and derivative identities

Installed runtime used:
`PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3`,
PyMuPDF1.27.2.2/MuPDF1.27.2. The following is the executed source-to-render
method; source hashing, output identities and warning text were printed by
the root command, not an automatically signed renderer receipt:

```python
p = Path('A046_006-paper.pdf')
pin = hashlib.sha256(p.read_bytes()).hexdigest()
r = fitz.open(p)
assert len(r) <= 12 and not r.needs_pass
for i, page in enumerate(r, 1):
    out = Path(f'A046_006-mupdf-page{i:02}.png')
    assert not out.exists()
    pix = page.get_pixmap(dpi=150, alpha=False)
    pix.save(out)
    print(page.get_text())
    # Root also printed each output's bytes, SHA-256 and width/height.
assert hashlib.sha256(p.read_bytes()).hexdigest() == pin
print(fitz.TOOLS.mupdf_warnings())
```

Imports were `Path` from pathlib, `fitz`, `hashlib`, `json`. No clip, resize,
manual rotation, contrast, OCR reconstruction or source-PDF modification was
applied. Root's recorded MuPDF warning string was empty. Earlier failed
Poppler rendering remains separate; its diagnostics are not suppressed by this
new run. For the one-page intro, the same `get_pixmap(dpi=150, alpha=False)`
method was used after `assert len(doc)==1 and not doc.needs_pass`, with the
source hash checked before/after; output name `C046_006-intro-mupdf-page1.png`.

| Admitted complete-page render | Stored size | SHA-256 |
|---|---|---|
| C046_006-intro-mupdf-page1.png | 1241x1754 | 244c98828893f9d6069d1ea114107d79664c76a9dcb6d44bcbc4ff0483bcb25d |
| A046_006-mupdf-page01.png | 1241x1755 | 3b8b94d9acb64805a4945beafde4cb03c3757aac702817f025d60c51bc3e6dc6 |
| A046_006-mupdf-page02.png | 1241x1755 | ed06952fc14edde07be4800a60dc7868d274a451ee172d630408cab967e25a19 |
| A046_006-mupdf-page03.png | 1241x1755 | 795416c516a9e20323d0f4137490737a3eb90d7b9d99fb66963c774d6ec6934d |
| A046_006-mupdf-page04.png | 1241x1755 | eef270e3a666e118124ccfe5b570680903553cf3b54f5db0494aba1cb7819674 |
| A046_006-mupdf-page05.png | 1241x1755 | 42fa38a90cf9b422599d3bb9b8bd1072979934c04b7c22cb6cc7cccf2c9b57f6 |
| A046_006-mupdf-page06.png | 1241x1755 | 087c43f1c67759439fdc4feec16cd4923fe894a1f44d77a790d0dcbea21aa2ce |
| A046_006-mupdf-page07.png | 1241x1755 | 5196e29a6d40ddad036e9bb01148aa78935130b582fd7b31993a06ac5094cb2a |
| A046_006-mupdf-page08.png | 1241x1755 | 615e00872872d4a2566c7388c1c08e19049b0f3b39cddfeae3bb7ab4f2ef4bfa |

These hashes identify captured derivatives, not independent validation of all
fonts or the historical claims. Root visually inspected every admitted complete
page once, preserving the excluded first render as an additional failed display.
The independent reader has been supplied the same source/render set, without
root's new findings. Their eventual recorded coverage/freeze controls exchange.

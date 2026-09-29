# Independent top-down input and provenance review

September 20, 2026 UTC. Working research only under the
[protocol](PROTOCOL.md), prospective navigation amendment in
[acquisition log](acquisition-log.md), and full investigation charter.
Main AGENTS.md, WORKFLOW.md and START-HERE.md and the evidence-audit,
source-preservation and PDF skills were read. A truncated combined controls
return was followed by complete separate START-HERE/charter reads.

**PASS for the admitted local byte/metadata and publisher-link joins.**
Two PDF pins and saved HTTP lengths agree; Poppler and PyMuPDF report one
overview page and eight full-paper pages; the nine listed MuPDF PNGs have the
corresponding complete-page dimensions and valid checked chunk CRCs.
No new physical authenticity, correct engineering execution, visual fidelity
or translation accuracy follows from these checks.

This reviewer made no network request, viewed no page/image, performed no
PNG-pixel decompression, created no rendering and read no root/second-reader
scientific observation files. Later arithmetic pointers from root are disclosed
below. The only authorized write is this note. No source,
header, HTML, PNG, code, frozen observation or canonical/legal record was edited.

## Admission and actual scope

The original full-paper file was not opened, hashed or parsed until root
explicitly reported terminal transfer completion: session68916, exit0,
HTTP200, 1878298 bytes, SHA-256 shown below. That terminal history is
root-reported, not independently replayed. Before that notice, this reviewer
examined only the controls, saved headers/HTML, admitted introduction PDF
metadata and introduction PNG byte/header identities.

All relative paths here resolve under:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/comparator-topdown/`.

Protocol SHA-256 freshly checked:
`dabd740fcf6647b920d72d4be4a50aeeb5b42ae456aad9466edafe6161e1d33a`.
The acquisition log was a live working record during this audit; the read
version contained the initial failures and prospective three-HTML-page
amendment. This note does not silently revise the original one-index limit.

## Preserved publisher navigation

The saved UTF-8 HTML was parsed for actual anchor hrefs. Relative links were
resolved against the recorded page URLs, with every selected target on
`www.taisei.co.jp`. No URL was guessed and no request was made by this reviewer.

| Saved page and recorded URL | Actual selected href | Resolved target |
|---|---|---|
| index-2013_46.html; https://www.taisei.co.jp/giken/report/2013_46/ | feature/index.htm | https://www.taisei.co.jp/giken/report/2013_46/feature/index.htm |
| feature-index.htm; https://www.taisei.co.jp/giken/report/2013_46/feature/index.htm | ../abstract/detail/B046_006.htm | https://www.taisei.co.jp/giken/report/2013_46/abstract/detail/B046_006.htm |
| article-B046_006.htm; https://www.taisei.co.jp/giken/report/2013_46/abstract/detail/B046_006.htm | ../../intro/C046_006.pdf | https://www.taisei.co.jp/giken/report/2013_46/intro/C046_006.pdf |
| article-B046_006.htm; same recorded URL | ../../paper/A046_006.pdf | https://www.taisei.co.jp/giken/report/2013_46/paper/A046_006.pdf |

The article's line40 explicitly distinguishes overview (`概要`) and full text
(`本文`). The feature index's line89 points to the article. The report index
contains the feature link at lines53/86. A separate PyMuPDF metadata query found
zero link annotations in the admitted single-page introduction. This does not
exclude printed unlinked text or establish any substantive engineering claim.

| Saved HTML | Bytes; saved Content-Length | SHA-256 |
|---|---:|---|
| index-2013_46.html | 7295 | 382d60bd7f6611bf9f1bdcdcb8ff7dadfc60cdaf8e46d7995f00afa7b2c2156f |
| feature-index.htm | 6935 | ec482cb4cf21bcfa437cb69348742ef8f888d584e19e975017155ddf4d71f791 |
| article-B046_006.htm | 7316 | 976f0bded35c9f4224201e38100fdb6fe08dc66c833d5dd29e9ba5973357217b |

Their respective saved response headers are HTTP/2 200 and text/html.
The captured href chain supports the identity of two same-article publisher
documents, not two independent accounts of project execution. Saved headers
are local retrieval records, not a new independently authenticated network
observation.

## Complete admitted PDF bytes and metadata

| PDF | Bytes; saved Content-Length | Pages | SHA-256 |
|---|---:|---:|---|
| C046_006-intro.pdf | 1817040 | 1 | 8ce337aaa3099a3b9a390d4f540a8306500d21961f382d3997aa7ffba9cd53ed |
| A046_006-paper.pdf | 1878298 | 8 | a6a6fb65396ebf8ac4f7e147e40f08a178cbd89fabf97b90a1c4448352aaf4c8 |

Both captured PDF headers report HTTP/2 200 and application/pdf. The complete
current byte arrays match the admission pins, begin with `%PDF-1.6`, end with
`%%EOF` after trailing whitespace, and parse with the reported page counts.
Those checks plus the saved Content-Length joins distinguish current complete
assets from the earlier incomplete introduction download. They do not prove
that every document object or rendering is semantically correct.

Both parsers report PDF1.6. Poppler reports encryption with print/copy allowed,
change/annotation disallowed; PyMuPDF opens without a password
(`needs_pass=0`, permissions integer -1324). No restrictions were removed and
no source was re-exported. Metadata Title/Author fields are empty; the printed
title/authors/edition must come from the separately reviewed pages, not an
invented metadata value.

| Property | Introduction | Full paper |
|---|---|---|
| Creator | Adobe Illustrator CS6 (Macintosh) | PScript5.dll Version 5.2.2 |
| Producer | Adobe PDF library 10.01 | Acrobat Distiller 10.1.2 (Windows) |
| Raw creation date | D:20131107102457+09'00' | D:20131008173339+09'00' |
| Raw modification date | D:20131107191643+09'00' | D:20131030143214+09'00' |
| Encryption reported | Standard V4 R4 128-bit AES | Standard V4 R4 128-bit RC4 |
| MediaBox/CropBox, approximately points | (0,0,595.28,841.89) | (0,0,595.22,842), all eight |
| Rotation | 0 | 0, all eight |
| HTTP Last-Modified | Wed, 25 Sep 2019 04:04:31 GMT | Wed, 25 Sep 2019 04:04:28 GMT |
| HTTP response Date | Sun, 20 Sep 2026 04:09:19 GMT | Sun, 20 Sep 2026 04:13:56 GMT |

Embedded production dates, HTTP modification dates, retrieval dates and the
printed report edition are different facts. This check supplies no original
camera date or authenticated project chronology.

## Listed complete-page render identities

For each current listed output, the PNG SHA-256/byte count was computed,
IHDR read, every chunk CRC checked, and dimensions compared with that source
page's current rectangle at 150/72 scale rounded using MuPDF's integer
rectangle. All nine have bit depth8, RGB color type2, no alpha channel,
compression/filter/interlace fields0; no checked acTL/fcTL/tRNS chunks.
No IDAT was decompressed and no image content was displayed.

| PNG | PDF zero-based page index | Raster | Bytes | SHA-256 |
|---|---:|---|---:|---|
| C046_006-intro-mupdf-page1.png | 0 | 1241×1754 | 797908 | 244c98828893f9d6069d1ea114107d79664c76a9dcb6d44bcbc4ff0483bcb25d |
| A046_006-mupdf-page01.png | 0 | 1241×1755 | 562599 | 3b8b94d9acb64805a4945beafde4cb03c3757aac702817f025d60c51bc3e6dc6 |
| A046_006-mupdf-page02.png | 1 | 1241×1755 | 1042893 | ed06952fc14edde07be4800a60dc7868d274a451ee172d630408cab967e25a19 |
| A046_006-mupdf-page03.png | 2 | 1241×1755 | 662149 | 795416c516a9e20323d0f4137490737a3eb90d7b9d99fb66963c774d6ec6934d |
| A046_006-mupdf-page04.png | 3 | 1241×1755 | 950143 | eef270e3a666e118124ccfe5b570680903553cf3b54f5db0494aba1cb7819674 |
| A046_006-mupdf-page05.png | 4 | 1241×1755 | 950466 | 42fa38a90cf9b422599d3bb9b8bd1072979934c04b7c22cb6cc7cccf2c9b57f6 |
| A046_006-mupdf-page06.png | 5 | 1241×1755 | 1830173 | 087c43f1c67759439fdc4feec16cd4923fe894a1f44d77a790d0dcbea21aa2ce |
| A046_006-mupdf-page07.png | 6 | 1241×1755 | 1360902 | 5196e29a6d40ddad036e9bb01148aa78935130b582fd7b31993a06ac5094cb2a |
| A046_006-mupdf-page08.png | 7 | 1241×1755 | 1152493 | 615e00872872d4a2566c7388c1c08e19049b0f3b39cddfeae3bb7ab4f2ef4bfa |

The introduction's 1754-pixel height versus the paper's 1755 follows its
different page rectangle; this is not a cropping discrepancy. Dimension
agreement alone does **not** prove that the right content occupies every page
or that Japanese glyphs, equations, diagrams and colors rendered correctly.
The producer's naming/page mapping and its reported 150dpi/no-alpha recipe are
consistent with the metadata; this reviewer did not independently regenerate
or pixel-compare the derivatives.

Installed identity independently read: Python3.13.7, PyMuPDF1.27.2.2,
MuPDF1.27.2. Package directory:
`/Users/admin/.pyenv/versions/3.13.7/lib/python3.13/site-packages/pymupdf/`.
The `__init__.py` SHA-256 is
`62cd13e673b2b5c838cb1235d5efec2ccc574941adeb826f6b0d3ba41cb220a0`.

| Runtime component in that directory | Bytes | SHA-256 |
|---|---:|---|
| _extra.so | 222664 | 60204d8011d31b8913cd09f918c4e94f7cd875a2aefd205f23e58d13fa5af7ef |
| _mupdf.so | 12648712 | 2b61537744f934bf3b47577a1f5e6fba3de8dc7ffe8fdfcf828a9697befe7a2a |
| libmupdfcpp.so | 1851664 | a1352e8286cd5631f9ca609be28a0b96c707d22b56921863a6afc2c87e2cdd25 |
| libmupdf.dylib | 32600208 | f8a319d28f46cbfac3616ce176c180b14a2618f68f41210bf8c5db7d8d409645 |

The separate metadata parser was bundled Poppler `pdfinfo`26.05.0 at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo`.
This is two parser families agreeing on counts/basic metadata, not two
independent physical observations or independent successful visual renderings.
The root's actual render invocation and warning history are producer evidence;
no independent render execution is claimed here.

## Failures and preservation limits

The acquisition log retains root's earlier web-reader403, premature
491520-byte introduction parse failure while its transfer was active, warned
Poppler render with missing Japanese content, and garbled pypdf extraction.
This reviewer did not repeat those failures or use the rejected render for
substantive reading. Its preserved byte identity was independently checked:
`C046_006-intro-page1.png`, 536324 bytes, 1241×1754 RGB8,
SHA-256 `e4412dd92d19b396dc6587e4fad691c2b9700860d698af73936e187d4622d509`.
Whether it omits text is attributed to root's visual report, not personally
observed here.

Root reports the alternate MuPDF renders had no warning text and that the
source was unchanged before/after rendering. This review separately establishes
that both **current** PDFs match the admitted transfer pins and remained
unchanged through this review's reads. It does not retrospectively observe
the producer process. No source-byte or dimension mismatch was waived.

A preliminary combined instruction read was truncated and reread completely;
there was no failed PDF/PNG input assertion in this review's own checks.
The later limited arithmetic check below does not validate source execution,
loads or measured motion.

## Actual checks and reproducible commands

All commands ran from the absolute unit directory above. Both inline recipes
below returned exit0/PASS. The final recipe rehashed every PDF/header/PNG it
read before exit, confirming unchanged bytes during that check.
It did not inspect the paper before the admission notice.

Metadata commands actually run, each successfully:

```sh
pdfinfo C046_006-intro.pdf
pdfinfo A046_006-paper.pdf
pdfinfo -v
shasum -a 256 PROTOCOL.md
shasum -a 256 /Users/admin/.pyenv/versions/3.13.7/lib/python3.13/site-packages/pymupdf/libmupdf.dylib
stat -f '%z bytes' /Users/admin/.pyenv/versions/3.13.7/lib/python3.13/site-packages/pymupdf/libmupdf.dylib
```

### Saved-link and initial-admitted-asset check

Actual result:
`PASS local HTML length/href joins and admitted intro bytes/header/render IHDR only; full paper not inspected`.

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import hashlib, json, re, struct
base = Path.cwd()
def sha(b): return hashlib.sha256(b).hexdigest()
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.hrefs=[]
    def handle_starttag(self, tag, attrs):
        if tag.lower()=="a":
            self.hrefs += [v for k,v in attrs if k.lower()=="href"]
assets = [
("index-2013_46.html","index-headers.txt","https://www.taisei.co.jp/giken/report/2013_46/"),
("feature-index.htm","feature-headers.txt","https://www.taisei.co.jp/giken/report/2013_46/feature/index.htm"),
("article-B046_006.htm","article-headers.txt","https://www.taisei.co.jp/giken/report/2013_46/abstract/detail/B046_006.htm")]
checks=[]
parsed={}
for filename, header, url in assets:
    b=(base/filename).read_bytes(); hb=(base/header).read_bytes(); h=hb.decode("iso-8859-1")
    assert re.search(r"^HTTP/2 200\s*$",h,re.M)
    length,=re.findall(r"^content-length: (\d+)\s*$",h,re.M|re.I)
    assert len(b)==int(length)
    assert "content-type: text/html" in h.lower()
    p=Links(); p.feed(b.decode("utf-8")); parsed[filename]=p.hrefs
    checks.append({"file":filename,"bytes":len(b),"sha256":sha(b),"header":header,"header_sha256":sha(hb),"recorded_url":url})
chain=[
("index-2013_46.html",assets[0][2],"feature/index.htm",assets[1][2]),
("feature-index.htm",assets[1][2],"../abstract/detail/B046_006.htm",assets[2][2]),
("article-B046_006.htm",assets[2][2],"../../intro/C046_006.pdf","https://www.taisei.co.jp/giken/report/2013_46/intro/C046_006.pdf"),
("article-B046_006.htm",assets[2][2],"../../paper/A046_006.pdf","https://www.taisei.co.jp/giken/report/2013_46/paper/A046_006.pdf")]
for f,u,href,expected in chain:
    assert href in parsed[f] and urljoin(u,href)==expected
    assert urlparse(expected).hostname=="www.taisei.co.jp"
b=(base/"C046_006-intro.pdf").read_bytes()
assert sha(b)=="8ce337aaa3099a3b9a390d4f540a8306500d21961f382d3997aa7ffba9cd53ed"
assert len(b)==1817040 and b.startswith(b"%PDF-1.6")
assert b.rstrip().endswith(b"%%EOF")
h=(base/"intro-headers.txt").read_bytes()
length,=re.findall(rb"^content-length: (\d+)\s*$",h,re.M|re.I)
assert len(b)==int(length)
renders=[]
for f in ["C046_006-intro-page1.png","C046_006-intro-mupdf-page1.png"]:
    rb=(base/f).read_bytes()
    assert rb[:8]==b"\x89PNG\r\n\x1a\n" and rb[12:16]==b"IHDR"
    w,hh,d,c,comp,fil,inter=struct.unpack(">IIBBBBB",rb[16:29])
    renders.append({"file":f,"bytes":len(rb),"sha256":sha(rb),"IHDR":[w,hh,d,c,comp,fil,inter]})
print(json.dumps({"status":"PASS local HTML length/href joins and admitted intro bytes/header/render IHDR only; full paper not inspected","html":checks,"chain":chain,"intro_sha256":sha(b),"intro_header_sha256":sha(h),"renders":renders},indent=2))

PY
```

### Final admitted metadata/derivative-identity check

Actual result:
`PASS admitted PDF bytes/header lengths/page counts and complete-page PNG metadata; no rendering or PNG-pixel decompression`.

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
import hashlib, json, re, struct, zlib, sys
import pymupdf
base=Path.cwd()
def sha(b): return hashlib.sha256(b).hexdigest()
seen={}
def read(rel):
    b=(base/rel).read_bytes(); seen[rel]=sha(b); return b
assets=[
("C046_006-intro.pdf","intro-headers.txt",1817040,"8ce337aaa3099a3b9a390d4f540a8306500d21961f382d3997aa7ffba9cd53ed",1),
("A046_006-paper.pdf","paper-headers.txt",1878298,"a6a6fb65396ebf8ac4f7e147e40f08a178cbd89fabf97b90a1c4448352aaf4c8",8)]
results=[]
for f,hfile,size,pin,count in assets:
    b=read(f); hb=read(hfile); header=hb.decode("iso-8859-1")
    assert len(b)==size and sha(b)==pin and b.startswith(b"%PDF-1.6") and b.rstrip().endswith(b"%%EOF")
    assert re.search(r"^HTTP/2 200\s*$",header,re.M)
    length,=re.findall(r"^content-length: (\d+)\s*$",header,re.M|re.I)
    assert size==int(length) and "content-type: application/pdf" in header.lower()
    doc=pymupdf.open(stream=b,filetype="pdf")
    assert doc.page_count==count and not doc.needs_pass
    pages=[]
    for i,page in enumerate(doc):
        assert page.rotation==0
        pixrect=(page.rect*pymupdf.Matrix(150/72,150/72)).irect
        name="C046_006-intro-mupdf-page1.png" if count==1 else f"A046_006-mupdf-page{i+1:02d}.png"
        rb=read(name)
        assert rb[:8]==b"\x89PNG\r\n\x1a\n"
        assert rb[12:16]==b"IHDR"
        w,h,depth,ctype,comp,fil,inter=struct.unpack(">IIBBBBB",rb[16:29])
        assert (w,h)==(pixrect.width,pixrect.height)
        assert (depth,ctype,comp,fil,inter)==(8,2,0,0,0)
        pos=8; names=[]
        while pos<len(rb):
            n=struct.unpack(">I",rb[pos:pos+4])[0]; kind=rb[pos+4:pos+8]; data=rb[pos+8:pos+8+n]
            crc=struct.unpack(">I",rb[pos+8+n:pos+12+n])[0]
            assert zlib.crc32(kind+data)&0xffffffff==crc
            names.append(kind.decode("ascii")); pos+=n+12
            if kind==b"IEND": break
        assert pos==len(rb) and names[-1]=="IEND"
        assert not ({"acTL","fcTL","tRNS"} & set(names))
        if count==1: assert sha(rb)=="244c98828893f9d6069d1ea114107d79664c76a9dcb6d44bcbc4ff0483bcb25d"
        pages.append({"pdf_page_index_zero_based":i,"mediabox":list(page.mediabox),"cropbox":list(page.cropbox),
                      "page_rect":list(page.rect),"rotation":page.rotation,"file":name,
                      "bytes":len(rb),"sha256":sha(rb),"IHDR":[w,h,depth,ctype],
                      "dimensions_match_150dpi_full_page_rect":True})
    results.append({"file":f,"bytes":size,"sha256":pin,"header_sha256":sha(hb),"page_count":count,
                    "is_pdf":doc.is_pdf,"needs_pass":doc.needs_pass,"metadata":doc.metadata,
                    "permissions_integer":doc.permissions,"pages":pages})
    doc.close()
runtime={"python":sys.version,"pymupdf_version":pymupdf.VersionBind,"mupdf_version":pymupdf.VersionFitz,
         "pymupdf_init_path":pymupdf.__file__}
runtime["pymupdf_init_sha256"]=sha(Path(pymupdf.__file__).read_bytes())
package=Path(pymupdf.__file__).parent
runtime["native_libraries"]=[{"path":str(p),"bytes":p.stat().st_size,"sha256":sha(p.read_bytes())}
                             for p in sorted(package.glob("*.so"))]
for f,pin in seen.items(): assert sha((base/f).read_bytes())==pin,("changed",f)
print(json.dumps({"status":"PASS admitted PDF bytes/header lengths/page counts and complete-page PNG metadata; no rendering or PNG-pixel decompression",
                  "runtime":runtime,"assets":results},indent=2,ensure_ascii=False))

PY
```

### Introduction link-annotation check

Actual result:
`PASS admitted intro: zero link annotations returned; source unchanged`.

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
import hashlib, pymupdf
p=Path('C046_006-intro.pdf'); b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=='8ce337aaa3099a3b9a390d4f540a8306500d21961f382d3997aa7ffba9cd53ed'
d=pymupdf.open(stream=b,filetype='pdf')
assert d.page_count==1
links=d[0].get_links()
assert links==[]
assert hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(b).hexdigest()
print('PASS admitted intro: zero link annotations returned; source unchanged')
PY
```

## Appended producer-recipe and limited arithmetic check

After this note's initial checks, root appended the actual publisher chain,
executed rendering method and all nine expected render pins to acquisition-log.md.
That read version had SHA-256
`be5e583cd32b2f3877eea471ca4789a32b6bf56f339072d1afbe03497380a2fa`.
This reviewer read the complete addition and independently matched all nine
recorded PNG hashes and dimensions to the current files. The recorded method
uses `page.get_pixmap(dpi=150, alpha=False)` with no clip parameter and checks
source hash equality before/after. It is consistent with the previously
verified page geometry and installed runtime.

Root additionally reports that all nine pages were rerendered in memory with
the same installed MuPDF and their full RGB arrays matched the saved PNGs,
with no warning text or source change. This is useful **same-renderer
reproducibility reported by root**, not an independent renderer, my own
pixel replay, or proof of semantic/glyph fidelity. No newly rendered file or
display was produced by this reviewer.

Root supplied two source-reported arithmetic checks after its observation
freeze; their selection was not blind. Exact rational arithmetic gives
`1500/15 = 100` and `8/2 = 4`. A limited, nonvisual MuPDF text query in the
admitted full paper also located:

- PDF zero-based page3, Figure5 text: `1500 ton` and 15 temporary columns.
- PDF zero-based page4: total1500 tonnes, 15 temporary columns and the authors'
  approximate100-tonne per-column statement.
- PDF zero-based page6: the schedule's eighth-day entry. That first snippet
  alone did not establish the complete eight-day/two-floor interpretation;
  the subsequent exact-locator text check below supplies that narrower bridge.

The first quotient is an average allocation and agrees with the authors'
approximate statement; it is not independent proof of equal reactions,
maximum/dynamic load, load capacity or safety margin. The second quotient is
four days per floor for the source-stated eight-day/two-floor work cycle; it is
an effective-cycle normalization, not a continuous lowering speed, motion
observation, or independent confirmation of that schedule's execution.
The complete-page readers own the broader source-context/visual review.
These text snippets do not replace their reading or a translation audit.

An attempted `rg` lookup of `root-observations.md` returned exit2 because
that guessed filename did not exist. No observation record was read by that
attempt. The arithmetic check used the admitted PDF's limited numeric text
and root-specified constants; the other visual reviewer's freeze was not read.

The following actual read-only command returned exit0:
`PASS all nine recorded renderer pins/dimensions and declared recipe markers; arithmetic 1500/15=100 and 8/2=4`.

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
from fractions import Fraction
import hashlib, json, re, struct
import pymupdf
base=Path.cwd()
b=(base/"acquisition-log.md").read_bytes(); log=b.decode()
pins=re.findall(r"^\| ([^|]+\.png) \| (\d+)x(\d+) \| ([0-9a-f]{64}) \|$",log,re.M)
assert len(pins)==len({p[0] for p in pins})==9
for f,w,h,pin in pins:
    raw=(base/f).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==pin
    assert struct.unpack(">II",raw[16:24])==(int(w),int(h))
for token in ["page.get_pixmap(dpi=150, alpha=False)", "assert hashlib.sha256(p.read_bytes()).hexdigest() == pin",
              "A046_006-mupdf-page{i:02}.png"]:
    assert token in log
assert Fraction(1500,15)==100 and Fraction(8,2)==4
paper=(base/"A046_006-paper.pdf").read_bytes()
assert hashlib.sha256(paper).hexdigest()=="a6a6fb65396ebf8ac4f7e147e40f08a178cbd89fabf97b90a1c4448352aaf4c8"
doc=pymupdf.open(stream=paper,filetype="pdf")
snips=[]
for i,p in enumerate(doc):
    lines=p.get_text().splitlines()
    for j,line in enumerate(lines):
        if re.search(r"1[,，]?500|1500|8日|８日|2層|２層",line):
            snips.append({"page_index":i,"line_index_in_extraction":j,"context":lines[max(0,j-1):j+2]})
assert hashlib.sha256((base/"A046_006-paper.pdf").read_bytes()).hexdigest()==hashlib.sha256(paper).hexdigest()
print(json.dumps({"status":"PASS all nine recorded renderer pins/dimensions and declared recipe markers; arithmetic 1500/15=100 and 8/2=4",
                  "acquisition_log_sha256_at_check":hashlib.sha256(b).hexdigest(),
                  "source_text_numeric_snippets_not_visual_verification":snips},indent=2,ensure_ascii=False))

PY
```


Root subsequently supplied the exact cycle source locator. A separate limited
text check (without viewing or rendering) confirmed `1サイクル（2フロア）8日間`
on PDF zero-based page6 (printed06-7, section3.5) and
`1フロア4日ペース` on zero-based page4 (printed06-5, section3.2), after
removing extraction whitespace solely for text matching. Thus the stated
eight-day/two-floor source bridge is also checked at text level; layout,
translation and actual execution remain separate. Actual command, exit0/PASS:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 - <<'PY'
from pathlib import Path
import hashlib, pymupdf, re
p=Path("A046_006-paper.pdf"); b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=="a6a6fb65396ebf8ac4f7e147e40f08a178cbd89fabf97b90a1c4448352aaf4c8"
d=pymupdf.open(stream=b,filetype="pdf")
for i,pattern in [(6,r"1サイクル[（(]2フロア[）)]8日間"),(4,r"1フロア4日ペース")]:
    text=re.sub(r"\s+","",d[i].get_text())
    m=re.search(pattern,text)
    assert m is not None,(i,pattern)
    print("PDF zero-based page",i,":",text[max(0,m.start()-40):m.end()+40])
assert hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(b).hexdigest()
print("PASS: source text supports eight days per two-floor cycle and stated four-day-per-floor pace; no motion measurement")

PY
```


## Evidentiary ceiling

This local record can support attribution to the captured publisher documents
and exact derivative identities, within the recorded retrieval chain. It does
not turn participant-authored claims into independent evidence of as-executed
loads, support reactions, operating histories, full removal sequence or safety
performance. Photographs and diagrams in a technical publication are not
authenticated original media merely because the PDF and render hashes match.

A scientific reader must separately distinguish the authors' method description,
reported project application, calculations, actual instrumentation and missing
as-executed records. The overview and full paper remain related publications,
not independent historical witnesses. No WTC7 matching, force/motion inference,
causal ranking, actor/intent conclusion or research-to-legal promotion follows
from this integrity pass.

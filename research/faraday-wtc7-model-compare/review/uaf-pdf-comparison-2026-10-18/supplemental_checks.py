"""Additional read-only checks, preserving differences without choosing an edition."""
from collections import Counter
import difflib
import json
from pathlib import Path
import sys
import fitz
import pypdf
from compare_pdfs import SOURCES, digest, filehash, write_json

media, results = map(Path, sys.argv[1:3])
docs = [fitz.open(media / (s["id"] + ".pdf")) for s in SOURCES]
stream_sets = []
for d in docs:
    stream_sets.append(Counter(digest(d.xref_stream(x)) for x in range(1, d.xref_length()) if d.xref_is_stream(x)))
stream_counts = {"total_streams": [sum(c.values()) for c in stream_sets], "shared_decoded_stream_multiset_count": sum((stream_sets[0] & stream_sets[1]).values())}
stream_counts["exclusive_streams"] = []
for i, d in enumerate(docs):
    unique = stream_sets[i] - stream_sets[1-i]
    stream_counts["exclusive_streams"].append([{"xref": x, "decoded_sha256": digest(d.xref_stream(x)), "dictionary": d.xref_object(x)} for x in range(1, d.xref_length()) if d.xref_is_stream(x) and digest(d.xref_stream(x)) in unique])
write_json(results / "stream-multisets.json", stream_counts)

page_details = []
for i in range(125):
    pair = []
    contents = []
    for d in docs:
        p = d[i]
        c = b"\n".join(d.xref_stream(x) for x in p.get_contents())
        contents.append(c)
        images = []
        for image in p.get_images(full=True):
            xref, mask, width, height, bpc, color, alternate, name, filter_name, referencer = image
            images.append({"name": name, "xref": xref, "mask_xref": mask, "width": width, "height": height, "bits_per_component": bpc, "color": color, "decoded_stream_sha256": digest(d.xref_stream(xref)), "raw_stream_sha256": digest(d.xref_stream_raw(xref)), "mask_decoded_sha256": digest(d.xref_stream(mask)) if mask else None, "occurrence_rects": [list(r) for r in p.get_image_rects(xref)]})
        pair.append({"page_xref": p.xref, "content_xrefs": p.get_contents(), "content_sha256": digest(c), "content_bytes": len(c), "images": images})
    # Comparing this raw command channel does not align equivalent operators.
    page_details.append({"page": i+1, "sources": dict(zip([s["id"] for s in SOURCES], pair)), "decoded_page_commands_equal": contents[0] == contents[1], "command_diff": list(difflib.unified_diff(contents[0].decode("latin1").splitlines(), contents[1].decode("latin1").splitlines(), fromfile="march2020", tofile="march-2020", lineterm="")) if contents[0] != contents[1] else []})
write_json(results / "page-resource-and-command-differences.json", page_details)

independent = {"pypdf_version": pypdf.__version__, "module_sha256": filehash(pypdf.__file__), "page_records": []}
readers = [pypdf.PdfReader(media / (s["id"] + ".pdf"), strict=True) for s in SOURCES]
for i in range(125):
    texts = [r.pages[i].extract_text() for r in readers]
    independent["page_records"].append({"page": i+1, "equal": texts[0] == texts[1], "sources": {s["id"]: {"sha256": digest(t.encode()), "bytes": len(t.encode())} for s, t in zip(SOURCES, texts)}, "text_diff": list(difflib.unified_diff(texts[0].splitlines(), texts[1].splitlines(), fromfile="march2020", tofile="march-2020", lineterm="")) if texts[0] != texts[1] else []})
independent["differing_pages"] = [p["page"] for p in independent["page_records"] if not p["equal"]]
write_json(results / "independent-pypdf-text-check.json", independent)
print(json.dumps({"pypdf_differing_pages": independent["differing_pages"], "decoded_command_difference_pages": [r["page"] for r in page_details if not r["decoded_page_commands_equal"]], "stream_counts": {k:v for k,v in stream_counts.items() if k != "exclusive_streams"}}, indent=2))

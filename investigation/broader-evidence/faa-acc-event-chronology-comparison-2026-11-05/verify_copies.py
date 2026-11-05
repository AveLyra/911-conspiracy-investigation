"""Compare the four official AWA-619 PDFs using in-memory renders."""
import hashlib
import json
from pathlib import Path

import pymupdf

IDS = ("7596160", "7597164", "7597932", "7598471")
EQUIVALENT = ("7596160", "7597164", "7598471")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compare(source_dir):
    copies = {}
    for naid in IDS:
        file = source_dir / f"{naid}.pdf"
        data = file.read_bytes()
        assert data.startswith(b"%PDF-"), naid
        with pymupdf.open(file) as doc:
            assert len(doc) == 3, naid
            pages = []
            for page in doc:
                raster = page.get_pixmap(dpi=115, colorspace=pymupdf.csGRAY, alpha=False)
                pages.append({
                    "width": raster.width,
                    "height": raster.height,
                    "gray_sha256": digest(raster.samples),
                    "sorted_text_sha256": digest(page.get_text(sort=True).encode("utf-8")),
                })
        copies[naid] = {"sha256": digest(data), "bytes": len(data), "pages": pages}

    assert len({record["sha256"] for record in copies.values()}) == 4
    reference = copies[EQUIVALENT[0]]["pages"]
    assert all(copies[naid]["pages"] == reference for naid in EQUIVALENT[1:])
    redacted = copies["7597932"]["pages"]
    assert all(
        a["gray_sha256"] != b["gray_sha256"]
        and a["sorted_text_sha256"] != b["sorted_text_sha256"]
        for a, b in zip(reference, redacted)
    )
    return copies


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    args = parser.parse_args()
    print(json.dumps(compare(args.source_dir), indent=2))

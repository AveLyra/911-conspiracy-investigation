"""Create-only complete-page reading derivatives for the declared Q05 set."""
import hashlib
import json
from pathlib import Path
import sys

import pymupdf as fitz

HERE = Path(__file__).resolve().parent
SOURCES = {
    "fema5": {
        "path": HERE / "source/fema403-ch5.pdf",
        "sha256": "8f1f4dd1dd419c7fa2877e20dc8f3c152da0887e85c604e5cf8730a9fd554f22",
        "bytes": 3507765,
        "pages": (16, 17, 19, 24, 28),
    },
    "fema7": {
        "path": HERE / "source/fema403-ch7.pdf",
        "sha256": "fa18b362784df0a2bf1816ecd81e3e5d0c6525ec54c7bc9a6000ad8a3c306887",
        "bytes": 3507094,
        "pages": (8, 9, 10, 13, 14),
    },
    "nist1a": {
        "path": Path("/Users/admin/docs/911/authority/nist/wtc7/ncstar-1a.pdf"),
        "sha256": "03c801bc1338533b54c6a64a66f074165c9429a59df11e2f58a19f5da91aef09",
        "bytes": None,
        "pages": (46, 47),
    },
}


def identity(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def save(path, data):
    with path.open("x") as stream:
        json.dump(data, stream, indent=2, sort_keys=True)
        stream.write("\n")


def main():
    out = HERE / "render01"
    if out.exists():
        raise FileExistsError("Refusing existing reading derivatives")
    pins = {}
    for key, spec in SOURCES.items():
        actual = identity(spec["path"])
        if actual["sha256"] != spec["sha256"]:
            raise RuntimeError(f"source hash mismatch: {key}: {actual}")
        if spec["bytes"] is not None and actual["bytes"] != spec["bytes"]:
            raise RuntimeError(f"source byte mismatch: {key}: {actual}")
        pins[key] = {"path": str(spec["path"]), **actual}
    paths = [HERE / "render.py", HERE / "PROTOCOL.md", HERE / "PAGE-SELECTION.md",
             Path(sys.executable)] + [spec["path"] for spec in SOURCES.values()]
    before = {str(p): identity(p) for p in paths}
    out.mkdir()
    save(out / "start.json", {"pins": pins, "physical_pages":
                               {k: list(v["pages"]) for k, v in SOURCES.items()},
                               "dpi": 150, "python": sys.version,
                               "pymupdf": fitz.VersionBind,
                               "mupdf": fitz.VersionFitz})
    status = "incomplete"
    pages = []
    try:
        for key, spec in SOURCES.items():
            fitz.TOOLS.mupdf_warnings(reset=True)
            with fitz.open(spec["path"]) as doc:
                if not doc.is_pdf or doc.is_repaired or doc.is_encrypted:
                    raise RuntimeError(f"unexpected PDF state: {key}")
                opening = fitz.TOOLS.mupdf_warnings(reset=True)
                if opening:
                    save(out / f"{key}-opening-warning.json", opening)
                for page in spec["pages"]:
                    fitz.TOOLS.mupdf_warnings(reset=True)
                    p = doc[page - 1]
                    pix = p.get_pixmap(dpi=150, alpha=False)
                    stem = f"{key}-p{page}"
                    pix.save(out / f"{stem}.png")
                    with (out / f"{stem}.txt").open("x") as stream:
                        stream.write(p.get_text())
                    pages.append({"source": key, "physical_page": page,
                                  "dimensions": [pix.width, pix.height],
                                  "warnings": fitz.TOOLS.mupdf_warnings(reset=True)})
        status = "complete_not_visual_review"
    finally:
        after = {str(p): identity(p) for p in paths}
        save(out / "receipt.json", {"status": status, "pages": pages,
                                     "before": before, "after": after,
                                     "inputs_unchanged": before == after,
                                     "products": {p.name: identity(p)
                                                  for p in sorted(out.iterdir())}})
    if before != after:
        raise RuntimeError("input changed during rendering")
    print(json.dumps({"status": status, "pages": len(pages),
                      "warnings": sum(bool(p["warnings"]) for p in pages)}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Census Case B parent vs INTFILES layout. Read-only zip namelist."""

from __future__ import annotations

import zipfile
from collections import Counter
from pathlib import Path

ZIP = Path(
    "/Users/admin/docs/911/exhibits/raw/"
    "ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539/"
    "ANSYS Thermal Data.zip"
)


def main() -> None:
    with zipfile.ZipFile(ZIP) as archive:
        names = [i.filename for i in archive.infolist() if not i.is_dir()]

    parent = [n for n in names if n.startswith("CaseB_Temps/") and n.count("/") == 1]
    intfiles = [n for n in names if n.startswith("CaseB_Temps/INTFILES+10%14SEP07/")]
    png = [n for n in names if n.startswith("CaseB_Temps/PNGFILES+10% 14SEP07/")]
    other_b = [
        n
        for n in names
        if n.startswith("CaseB_Temps/")
        and not n.startswith("CaseB_Temps/INTFILES+10%14SEP07/")
        and not n.startswith("CaseB_Temps/PNGFILES+10% 14SEP07/")
    ]

    print("CaseB parent-only files", len(parent))
    for n in sorted(parent)[:40]:
        print("  PARENT", n)
    print("other_b_not_int_or_png", len(other_b))
    for n in sorted(other_b)[:40]:
        print("  OTHER", n)
    print("INTFILES", len(intfiles))
    print("PNG", len(png))

    int_bases = [Path(n).name for n in intfiles]
    parent_ints = [Path(n).name for n in parent if n.lower().endswith(".int")]
    print("parent .int count", len(parent_ints))
    print("INTFILES .int count", sum(1 for b in int_bases if b.lower().endswith(".int")))

    floors = Counter()
    for b in int_bases:
        for fl in ("Fl07", "Fl08", "Fl09", "Fl10", "Fl11", "Fl12", "Fl13", "Fl14"):
            if fl in b and b.endswith(".int"):
                floors[fl] += 1
    print("INTFILES floor globs", dict(floors))
    leftover = [
        b
        for b in int_bases
        if b.endswith(".int") and not any(fl in b for fl in ("Fl07", "Fl08", "Fl09", "Fl10", "Fl11", "Fl12", "Fl13", "Fl14"))
    ]
    print("INTFILES *.int not Fl07-14", len(leftover), leftover[:20])

    a_parent = [n for n in names if n.startswith("CaseA_Temps/") and n.count("/") == 1]
    c_parent = [n for n in names if n.startswith("CaseC_Temps/") and n.count("/") == 1]
    print("CaseA parent-only", len(a_parent), "sample", a_parent[:3])
    print("CaseC parent-only", len(c_parent), "sample", c_parent[:3])


if __name__ == "__main__":
    main()

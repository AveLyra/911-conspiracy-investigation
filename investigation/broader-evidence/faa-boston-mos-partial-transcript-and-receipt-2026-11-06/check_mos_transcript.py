"""Check printed AWA-891 time labels against the ZBW-30 wave-file bounds."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import fitz

TRANSCRIPT_SHA = "0e8bb8e245c24e61a81567db9a76ef5836fe37a60751dd6bae052c01028ffac7"
SECOND = re.compile(r"12[0-5][0-9]:[0-5][0-9]")
MINUTE = re.compile(r"12[0-5][0-9]")
CLIPS = [
    ("1237:50", "1238:15"),
    ("1239:00", "1242:15"),
    ("1252:00", "1253:05"),
]


def clock(label):
    return int(label[:2]) * 3600 + int(label[2:4]) * 60 + int(label[5:])


def compare(path):
    body = path.read_bytes()
    if hashlib.sha256(body).hexdigest() != TRANSCRIPT_SHA:
        raise ValueError("Transcript bytes differ from the pinned AWA-891 copy")
    rows = []
    unparsed = []
    pages = []
    with fitz.open(stream=body, filetype="pdf") as pdf:
        assert len(pdf) == 8
        for page_number, page in enumerate(pdf, 1):
            # Restrict to the transcript time column, below the title and fax headers.
            top = 520 if page_number == 1 else 110
            words = [w[4] for w in page.get_text("words")
                     if 80 <= w[0] <= 112 and w[1] >= top]
            seconds = [word for word in words if SECOND.fullmatch(word)]
            minutes = [word for word in words if MINUTE.fullmatch(word)]
            other = [word for word in words if any(c.isdigit() for c in word)
                     and word not in seconds and word not in minutes]
            rows.extend((page_number, value) for value in seconds)
            unparsed.extend((page_number, value) for value in other)
            pages.append({"page": page_number, "second_tokens": len(seconds),
                          "minute_markers": minutes})
    assert (rows[0], rows[-1]) == ((1, "1237:52"), (8, "1253:06"))
    assert unparsed == [(4, "1240~52"), (7, "1252;30"), (8, "~52:37"), (8, "52:41")]
    assert all(clock(a[1]) <= clock(b[1]) for a, b in zip(rows, rows[1:]))
    gaps = [(CLIPS[0][1], CLIPS[1][0]), (CLIPS[1][1], CLIPS[2][0])]
    gap_hits = [
        [{"page": page, "time": time} for page, time in rows
         if clock(start) < clock(time) < clock(end)]
        for start, end in gaps
    ]
    outside = [
        {"page": page, "time": time}
        for page, time in rows
        if not any(clock(start) <= clock(time) <= clock(end) for start, end in CLIPS)
    ]
    assert gap_hits == [[], []]
    assert outside == [{"page": 8, "time": "1253:06"}]
    return {
        "pages": pages,
        "exact_second_tokens": len(rows),
        "unparsed_numeric_words_in_time_column": unparsed,
        "first_and_last_exact_rows": [rows[0], rows[-1]],
        "clip_bounds": CLIPS,
        "gap_bounds": gaps,
        "strict_interior_gap_hits": gap_hits,
        "outside_closed_clip_intervals": outside,
        "matched_last_minus_first_seconds": clock(rows[-1][1]) - clock(rows[0][1]),
        "inventory_start_minus_first_row_seconds": clock("1237:54") - clock(rows[0][1]),
        "last_row_minus_last_clip_bound_seconds": clock(rows[-1][1]) - clock(CLIPS[-1][1]),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript", type=Path)
    args = parser.parse_args()
    print(json.dumps(compare(args.transcript), indent=2))

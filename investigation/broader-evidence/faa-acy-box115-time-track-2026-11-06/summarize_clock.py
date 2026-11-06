import json
from collections import Counter
from pathlib import Path
from statistics import median
import sys

RATE = 44100


def clock(row):
    return (row["day"] * 24 + row["hour"]) * 3600 + row["minute"] * 60 + row["second"]


def endpoint(row):
    return {"sample": row["sample"], "playback_s": round(row["sample"] / RATE, 6),
            "day": row["day"], "code": f'{row["hour"]:02}:{row["minute"]:02}:{row["second"]:02}'}


def summarize(rows):
    assert all(a["sample"] < b["sample"] for a, b in zip(rows, rows[1:]))
    cuts = [i for i, (a, b) in enumerate(zip(rows, rows[1:]), 1) if clock(b) < clock(a)]
    groups = [rows[a:b] for a, b in zip([0, *cuts], [*cuts, len(rows)]) if a < b]
    segments = []
    for group in groups:
        pairs = list(zip(group, group[1:]))
        advances = Counter(clock(b) - clock(a) for a, b in pairs)
        steps = [(b["sample"] - a["sample"]) / RATE for a, b in pairs if clock(b) - clock(a) == 1]
        segments.append({
            "count": len(group), "start": endpoint(group[0]), "end": endpoint(group[-1]),
            "advance_histogram": dict(sorted(advances.items())),
            "median_playback_s_per_single_code_step": round(median(steps), 8) if steps else None,
            "adjacent_equal_labels": [[endpoint(a), endpoint(b)] for a, b in pairs if clock(a) == clock(b)],
            "candidate_times": [endpoint(r) for r in group if (r["hour"], r["minute"], r["second"]) in
                                [(14,28,0), (14,30,0), (15,28,0)]],
        })
    return {"accepted": len(rows), "segments": segments,
            "clock_rollbacks": [
                {"before": endpoint(rows[i-1]), "after": endpoint(rows[i]),
                 "code_seconds_backward": clock(rows[i-1]) - clock(rows[i])}
                for i in cuts]}


def main():
    results = {}
    for f in map(Path, sys.argv[1:]):
        results[f.name] = {k: summarize(v) for k, v in json.loads(f.read_text()).items()}
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

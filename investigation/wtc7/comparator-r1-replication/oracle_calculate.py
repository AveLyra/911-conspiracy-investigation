#!/usr/bin/env python3
"""Bounded R1 oracle: stdlib-only endpoint enumeration, no helper imports."""
import argparse
import hashlib
import itertools
import json
import platform
import re
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
FRAMES = (239, 434, 441, 442, 443, 444)
FEATURES = ("R1", "B1", "B2")
PINS = {
    "PROTOCOL.md": "2bbc5777dd39dde42a2945d1d049a1a46f8c4b61678308e328e803f0ffa2331a",
    "EXECUTION-2026-09-27.md": "16533732f0d4a9e02b295d46398e5c5fbe8b04f9250dd2eb8130c3373fd86f1f",
    "root-observations.md": "d8d9bfb77b51780e1cef47e7a41577509d37bbfbd7189667e2eb69693fb51352",
    "observer-observations.md": "240a1849e927bebb38803037cc28253132186ddb5049577bab467d7e1769846d",
    "human-observations-2026-09-26.md": "c7714d0abad6d9806a9f3f4a80abacdf9f6404b6ad11cc59b26b2429e45c842d",
}
MAP_PIN = "14c72246559d79812c1eef4b42d977c64d1f28bc97d0f034a945cddb8db5561a"
PTS_PIN = "d8496f26d271eda8955e0fc46b3ff98754c2b5bc06793e8729adf0840a387c3b"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pin_bytes(data, expected):
    actual = hashlib.sha256(data).hexdigest()
    require(actual == expected, "input pin mismatch")
    return {"sha256": actual, "bytes": len(data)}


def point(identity, envelope, **extra):
    require(identity in ("localizable", "ambiguous", "unlocalizable"), "identity")
    if envelope is not None:
        require(isinstance(envelope, (list, tuple)) and len(envelope) == 2, "range pair")
        require(all(type(v) is int for v in envelope), "integer range")
        require(0 <= envelope[0] <= envelope[1] <= 719, "range bounds")
        envelope = list(envelope)
    return {"identity": identity, "y_envelope": envelope, **extra}


def extrema(rt, bt, r0, b0):
    """Evaluate every endpoint combination; no closed-form endpoint helper."""
    operands = [rt, bt, r0, b0]
    for p in operands:
        if p is not None:
            point(p["identity"], p["y_envelope"])
    if any(p is None or p["identity"] != "localizable" or p["y_envelope"] is None
           for p in operands):
        return {"low": None, "high": None, "status": "unresolved"}
    values = [(r - b) - (s - c) for r, b, s, c in
              itertools.product(*(p["y_envelope"] for p in operands))]
    lo, hi = min(values), max(values)
    return {"low": lo, "high": hi,
            "status": "positive" if lo > 0 else "not_positive"}


def comparison(baseline, current):
    refs = {ref: extrema(current.get("R1"), current.get(ref),
                         baseline.get("R1"), baseline.get(ref))
            for ref in ("B1", "B2")}
    states = [refs[ref]["status"] for ref in ("B1", "B2")]
    status = ("unresolved" if "unresolved" in states else
              "positive" if all(s == "positive" for s in states) else "not_positive")
    return {"references": refs, "both_reference_status": status}


def triplets(rows):
    indices = [r["source_index"] for r in rows]
    require(all(type(i) is int for i in indices), "integer source index")
    require(indices == sorted(set(indices)), "ordered distinct comparison indices")
    out = []
    for i in range(len(rows) - 2):
        window = rows[i:i + 3]
        ix = indices[i:i + 3]
        consecutive = ix[1] == ix[0] + 1 and ix[2] == ix[1] + 1
        states = [r["both_reference_status"] for r in window]
        require(all(s in ("positive", "not_positive", "unresolved") for s in states),
                "row status")
        status = ("not_consecutive" if not consecutive else
                  "unresolved" if "unresolved" in states else
                  "confirmed" if all(s == "positive" for s in states) else "not_confirmed")
        out.append({"indices": ix, "consecutive": consecutive, "status": status})
    return out


def parse_ai(text):
    headings = list(re.finditer(r"^## Frame (\d+)\s*$", text, re.M))
    require(tuple(int(m[1]) for m in headings) == FRAMES, "AI frame coverage/order")
    frames, identities = {}, {}
    for n, m in enumerate(headings):
        section = text[m.end():headings[n + 1].start() if n + 1 < len(headings) else len(text)]
        sha = re.findall(r"SHA-256:?\s*`([0-9a-f]{64})`", section)
        require(len(sha) == 1, "AI image identity")
        points = {}
        for line in section.splitlines():
            if not re.match(r"^\| (?:R1|B1|B2) \|", line):
                continue
            fields = [v.strip() for v in line.strip().strip("|").split("|")]
            require(len(fields) == 4, "AI table columns")
            feature, identity, raw, reason = fields
            require(feature not in points and bool(reason), "duplicate feature/reason")
            if raw == "null":
                envelope = None
            else:
                match = re.fullmatch(r"\[(\d+),\s*(\d+)\]", raw)
                require(match is not None, "AI envelope syntax")
                envelope = [int(match[1]), int(match[2])]
            points[feature] = point(identity, envelope, source_literal=raw, reason=reason)
        require(tuple(points) == FEATURES, "AI feature coverage/order")
        index = int(m[1]); frames[index] = points; identities[index] = sha[0]
    return frames, identities


def parse_human(text):
    frames = {}
    for line in text.splitlines():
        if not re.match(r"^\| \d+ \|", line):
            continue
        cells = [v.strip() for v in line.strip().strip("|").split("|")]
        require(len(cells) == 7 and all(re.fullmatch(r"\d+", v) for v in cells),
                "human table syntax")
        values = list(map(int, cells)); index = values[0]
        require(index not in frames, "duplicate human frame")
        frame = {}
        for j, feature in enumerate(FEATURES):
            x, y = values[1 + 2*j:3 + 2*j]
            require(0 <= x < 1280 and 0 <= y < 720, "human coordinate bounds")
            frame[feature] = point("localizable", [y - 1, y + 1],
                                   reported_x=x, reported_y=y, assessed_y_radius=1,
                                   source_identity="user-reported LOCKED; disclosed R1 label inference")
        frames[index] = frame
    require(tuple(frames) == FRAMES, "human frame coverage/order")
    return frames


def selftest():
    passed = []
    def check(name, actual, expected):
        require(actual == expected, "control failed: " + name)
        passed.append(name)
    def rejects(name, fn):
        try:
            fn()
        except (ValueError, KeyError, TypeError):
            passed.append(name)
            return
        raise ValueError("control did not reject: " + name)
    p = lambda a, b=None: point("localizable", [a, a if b is None else b])
    check("known_zero", extrema(p(10), p(40), p(10), p(40)),
          {"low": 0, "high": 0, "status": "not_positive"})
    check("translation_only", extrema(p(17), p(47), p(10), p(40)),
          {"low": 0, "high": 0, "status": "not_positive"})
    check("positive_extrema", extrema(p(28,30), p(38,40), p(18,20), p(38,40)),
          {"low": 6, "high": 14, "status": "positive"})
    check("negative_extrema", extrema(p(8,10), p(38,40), p(18,20), p(38,40)),
          {"low": -14, "high": -6, "status": "not_positive"})
    check("zero_boundary_is_not_positive", extrema(p(22,24), p(38,40), p(18,20), p(38,40)),
          {"low": 0, "high": 8, "status": "not_positive"})
    base = {"R1": p(18,20), "B1": p(38,40), "B2": p(48,50)}
    cur = {"R1": p(28,30), "B1": p(38,40), "B2": p(63,65)}
    out = comparison(base, cur)
    check("reference_disagreement_retained", out, {
        "references": {"B1": {"low": 6, "high": 14, "status": "positive"},
                       "B2": {"low": -9, "high": -1, "status": "not_positive"}},
        "both_reference_status": "not_positive"})
    check("missing_point_unresolved", comparison(base, {"R1":p(28,30), "B1":p(38,40)})["both_reference_status"], "unresolved")
    check("ambiguous_identity_unresolved", extrema(point("ambiguous", [28,30]), p(40), p(10), p(40))["status"], "unresolved")
    check("null_envelope_unresolved", extrema(point("localizable", None), p(40), p(10), p(40))["status"], "unresolved")
    check("unlocalizable_identity_unresolved", extrema(point("unlocalizable", [28,30]), p(40), p(10), p(40))["status"], "unresolved")
    def wr(indices, states=None):
        return [{"source_index":i,"both_reference_status":s} for i,s in
                zip(indices, states or ["positive"]*len(indices))]
    check("consecutive_confirmed", triplets(wr([10,11,12]))[0]["status"], "confirmed")
    check("nonconsecutive_not_confirmed", triplets(wr([10,12,13]))[0]["status"], "not_consecutive")
    check("overlapping_windows_retained", [r["indices"] for r in triplets(wr([10,11,12,13]))], [[10,11,12],[11,12,13]])
    check("triplet_unknown_retained", triplets(wr([10,11,12],["positive","unresolved","positive"]))[0]["status"], "unresolved")
    check("triplet_nonpositive_retained", triplets(wr([10,11,12],["positive","not_positive","positive"]))[0]["status"], "not_confirmed")
    rejects("duplicate_indices", lambda: triplets(wr([10,10,11])))
    rejects("boolean_range", lambda: p(True))
    rejects("inverted_range", lambda: p(20,10))
    rejects("off_raster_range", lambda: p(719,720))
    rejects("unknown_identity", lambda: point("probably", [10,11]))
    rejects("nonfinite_range", lambda: p(float("inf")))
    rejects("wrong_pin", lambda: pin_bytes(b"altered", hashlib.sha256(b"original").hexdigest()))
    ai = "\n".join("## Frame %d\nSHA-256: `%s`.\n%s" %
                   (i,"0"*64,"\n".join("| %s | localizable | [10, 12] | synthetic |"%f for f in FEATURES))
                   for i in FRAMES)
    parsed, identities = parse_ai(ai)
    check("ai_all_18_points", sum(map(len,parsed.values())), 18)
    check("ai_literal_retained", parsed[239]["R1"]["source_literal"], "[10, 12]")
    check("ai_identity_pins_retained", set(identities.values()), {"0"*64})
    rejects("ai_missing_feature", lambda: parse_ai(ai.replace("| B2 | localizable | [10, 12] | synthetic |", "", 1)))
    rejects("ai_duplicate_feature", lambda: parse_ai(ai.replace("| R1 |", "| B1 |", 1)))
    rejects("ai_bad_envelope", lambda: parse_ai(ai.replace("[10, 12]", "[NaN, 12]", 1)))
    rejects("ai_duplicate_frame", lambda: parse_ai(ai.replace("## Frame 434", "## Frame 239", 1)))
    null_ai, _ = parse_ai(ai.replace("[10, 12]", "null", 1))
    check("ai_null_preserved", null_ai[239]["R1"]["y_envelope"], None)
    human = "\n".join("| %d | 10 | 20 | 30 | 40 | 50 | 60 |" % i for i in FRAMES)
    hp = parse_human(human)
    check("human_18_points", sum(map(len,hp.values())),18)
    check("human_radius_one", hp[239]["R1"]["y_envelope"],[19,21])
    check("human_xy_retained", [hp[239]["R1"]["reported_x"],hp[239]["R1"]["reported_y"]],[10,20])
    rejects("human_bad_coordinate", lambda: parse_human(human.replace("| 10 | 20 |", "| 1280 | 20 |", 1)))
    rejects("human_missing_frame", lambda: parse_human("\n".join(human.splitlines()[1:])))
    rejects("human_duplicate_frame", lambda: parse_human(human.replace("| 434 |", "| 239 |",1)))
    return {"status":"PASS_SYNTHETIC_ARITHMETIC_AND_PARSING_ONLY", "count":len(passed), "checks":passed}


def calculate(clearance_path, clearance_sha):
    captured, identities = {}, {}
    def read(path, sha):
        path = path.resolve(); data = path.read_bytes()
        identities[str(path)] = pin_bytes(data, sha); captured[path] = data
        return data
    data = {name: read(HERE/name, sha) for name,sha in PINS.items()}
    require(clearance_path.resolve().parent == HERE and clearance_path.suffix in (".md", ".json"), "clearance location")
    read(clearance_path, clearance_sha)
    arms, pngs = {}, {}
    for arm,name in (("original_root","root-observations.md"),("original_observer","observer-observations.md")):
        arms[arm],pngs[arm] = parse_ai(data[name].decode("utf-8"))
    arms["human_radius_one"] = parse_human(data["human-observations-2026-09-26.md"].decode("utf-8"))
    require(sum(len(points) for arm in arms.values() for points in arm.values()) == 54, "54 input points")
    source = HERE.parent/"comparator-roof-onset"
    selections, inventories = [], []
    for run in ("run02","run03"):
        selections.append(json.loads(read(source/run/"comparator-selected.json", MAP_PIN)))
        inventories.append(json.loads(read(source/run/"comparator-all-frame-pts.json", PTS_PIN))["frames"])
    require(selections[0] == selections[1] and inventories[0] == inventories[1], "paired metadata equality")
    selected, pts = selections[0], inventories[0]
    require([r["source_index"] for r in selected] == list(range(239,481)), "selection domain")
    require(len(pts)==1350, "inventory coverage")
    require(all(type(r["pts"]) is int and r["pts"] == r["best_effort_timestamp"] for r in pts), "inventory PTS")
    require(all(a["pts"] < b["pts"] for a,b in zip(pts,pts[1:])), "increasing PTS")
    clocks=[]
    for i in FRAMES:
        row=selected[i-239]; frame=pts[i]
        require(row["source_index"]==i and row["source_pts"]==frame["pts"], "clock row join")
        require(row["source_time_base"]=="1/30000", "time base")
        require(Fraction(row["source_seconds_exact"]) == Fraction(frame["pts"],30000), "exact source time")
        require((frame["width"],frame["height"])==(1280,720), "source geometry")
        require(row["png"]=="comparator/frame-%04d.png"%(i-238), "output ordinal")
        require(all(pngs[arm][i] == row["sha256"] for arm in pngs), "annotation image join")
        clocks.append({"source_index":i,"source_pts":frame["pts"],"source_time_base":"1/30000",
                       "source_seconds_exact":str(Fraction(frame["pts"],30000)),
                       "png":row["png"],"png_sha256":row["sha256"]})
    results={}
    for name,frames in arms.items():
        rows=[{"source_index":i,**comparison(frames[239],frames[i])} for i in FRAMES[1:]]
        windows=triplets(rows)
        results[name]={"rows":rows,"triplets":windows,
                       "confirmed_window_starts":[r["indices"][0] for r in windows if r["status"]=="confirmed"]}
    require(sum(len(r["references"]) for arm in results.values() for r in arm["rows"])==30,"30 intervals")
    for path,original in captured.items():
        require(path.read_bytes()==original,"input changed during calculation")
    return {"schema_version":1,"status":"COMPLETE_CONDITIONAL_COMPARATOR_ARITHMETIC_ONLY",
            "python":platform.python_version(),"code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "method":"all 16 Cartesian endpoint combinations of (Rt-Bt)-(R0-B0); no interval helper imported",
            "input_identities":identities,"source_clocks":clocks,"annotation_inputs":arms,"results":results,
            "counts":{"arms":3,"point_inputs":54,"comparison_rows":15,"displacement_intervals":30,"three_row_windows":9},
            "limits":["Subjective original AI envelopes and separate assessed human y-radius-one arm remain unchanged.",
                      "Shared baseline, references, access copy and chosen frames; no independent camera or original clock authentication.",
                      "Strict positivity is conditional on supplied ranges; unresolved input is not omitted or called stationary.",
                      "No first physical onset, reference stationarity, full camera-motion solution, support loss, device time, gravity or WTC7 cause inference."]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--clearance",type=Path)
    parser.add_argument("--clearance-sha")
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    controls=selftest()
    if args.test:
        require(args.clearance is None and args.clearance_sha is None and args.out is None,"synthetic-only mode")
        print(json.dumps({"python":platform.python_version(),"code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),**controls},indent=2,sort_keys=True))
        return
    require(args.clearance is not None and args.clearance_sha is not None,"source-clearance receipt required")
    result=calculate(args.clearance,args.clearance_sha)
    result["synthetic_controls"]=controls
    payload=(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode("utf-8")
    if args.out is None:
        print(payload.decode("utf-8"),end="")
    else:
        destination=args.out.resolve()
        require(destination.parent==HERE and destination.name in ("oracle-run01.json","oracle-run02.json"),"fixed output scope")
        with destination.open("xb") as out:
            out.write(payload)
        print(json.dumps({"output":str(destination),"bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest(),"counts":result["counts"]},sort_keys=True))


if __name__=="__main__":
    main()

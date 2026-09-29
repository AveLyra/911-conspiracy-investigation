#!/usr/bin/env python3
"""Independent exact-rational facade-feature verification.

Mathematical core frozen before reading the producer or its output.
All physical interpretations remain outside this arithmetic verifier.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import sys
import argparse


def q(value):
    if value is None or isinstance(value, bool):
        raise ValueError("missing_or_not_numeric")
    return value if isinstance(value, F) else F(str(value))


def exact_fit(times, values, bounds=None):
    """Solve centered, equally spaced linear/quadratic normal equations."""
    if len(times) != len(values) or len(times) < 3:
        raise ValueError("bad_shape")
    t, y = list(map(q, times)), list(map(q, values))
    n = len(t)
    dt = t[1] - t[0]
    if dt <= 0 or any(t[i] - t[i - 1] != dt for i in range(1, n)):
        raise ValueError("not_increasing_equal_grid")
    c, h = (t[0] + t[-1]) / 2, (t[-1] - t[0]) / 2
    u = [(x - c) / h for x in t]
    assert sum(u) == sum(x**3 for x in u) == 0
    s2, s4 = sum(x*x for x in u), sum(x**4 for x in u)
    sy, syu, syu2 = sum(y), sum(a*b for a,b in zip(y,u)), sum(a*b*b for a,b in zip(y,u))
    det = n*s4 - s2*s2
    b1 = syu/s2
    b2 = (n*syu2-s2*sy)/det
    coefs = {1:[sy/n,b1], 2:[(sy-s2*b2)/n,b1,b2]}
    models = {}
    for degree, coeff in coefs.items():
        residual = [v-sum(b*z**k for k,b in enumerate(coeff)) for v,z in zip(y,u)]
        assert all(sum(r*z**k for r,z in zip(residual,u)) == 0 for k in range(degree+1))
        sse = sum(r*r for r in residual)
        if degree == 1:
            eig = [float(n), float(s2)]
        else:
            disc = math.sqrt(float((n-s4)**2+4*s2*s2))
            eig = [float(s2), (float(n+s4)-disc)/2, (float(n+s4)+disc)/2]
        models[degree] = dict(coefficients=coeff, residuals=residual, sse=sse,
                              rmse=math.sqrt(float(sse/n)),
                              condition=math.sqrt(max(eig)/min(eig)))
    weights = [2*(n*z*z-s2)/(h*h*det) for z in u]
    a = 2*b2/(h*h)
    assert sum(weights) == sum(w*z for w,z in zip(weights,t)) == 0
    assert sum(w*z*z for w,z in zip(weights,t)) == 2
    assert sum(w*z for w,z in zip(weights,y)) == a
    if bounds is None:
        interval = None
        bnd = None
    else:
        bnd = [[q(v) for v in pair] for pair in bounds]
        if len(bnd) != n or any(not lo<=v<=hi for v,(lo,hi) in zip(y,bnd)):
            raise ValueError("invalid_bounds")
        interval = [sum(w*(lo if w>=0 else hi) for w,(lo,hi) in zip(weights,bnd)),
                    sum(w*(hi if w>=0 else lo) for w,(lo,hi) in zip(weights,bnd))]
        assert interval[0] <= a <= interval[1]
    return dict(center=c, halfspan=h, time=t, y=y, bounds=bnd, models=models,
                acceleration=a, weights=weights, interval=interval,
                weight_l1=sum(abs(w) for w in weights))


def joint_math(rows):
    """Rows contain original observer A/C x/y boxes, already coverage-filtered.

Each original feature box expands by delta at both endpoints. Intersecting
observers commutes with this uniform expansion: joined L becomes L-delta
and joined U becomes U+delta. Therefore local observer conflict gap g
needs delta>=g/2. A-C intervals expand by 2delta at both endpoints, so a
global separation intersection gap g requires delta>=g/4. The largest
nonnegative requirement over both axes is necessary and sufficient.
"""
    if not rows:
        return dict(status="no_paired_data")
    joined = []
    axes = {}
    for row in rows:
        rr = {"frame": row["frame"], "original": row["original"], "joined": {}}
        for axis in ("x","y"):
            rr["joined"][axis] = {}
            for feature in ("A","C"):
                boxes = [d[feature][axis] for d in row["original"].values()]
                lows, highs = [q(v[0]) for v in boxes], [q(v[1]) for v in boxes]
                if any(a>b for a,b in zip(lows,highs)):
                    raise ValueError("invalid_original_box")
                rr["joined"][axis][feature] = [max(lows),min(highs)]
        joined.append(rr)
    for axis in ("x","y"):
        intervals, conflicts = [], []
        for r in joined:
            aa,cc = r["joined"][axis]["A"],r["joined"][axis]["C"]
            intervals.append((r["frame"],aa[0]-cc[1],aa[1]-cc[0]))
            for feature,box in (("A",aa),("C",cc)):
                if box[0]>box[1]:
                    conflicts.append(dict(frame=r["frame"],feature=feature,box=box,gap=box[0]-box[1]))
        lo,hi = max(v[1] for v in intervals),min(v[2] for v in intervals)
        local = max([F(0)]+[c["gap"]/2 for c in conflicts])
        global_req = max(F(0),(lo-hi)/4)
        axes[axis] = dict(interval=[lo,hi],
                          lower_frames=[r[0] for r in intervals if r[1]==lo],
                          upper_frames=[r[0] for r in intervals if r[2]==hi],
                          intervals=intervals,local_conflicts=conflicts,
                          local_delta=local,global_delta=global_req,
                          delta=max(local,global_req))
    delta = max(axes["x"]["delta"],axes["y"]["delta"])

    def witness(widen):
        constants = {}
        for axis in ("x","y"):
            lo,hi = axes[axis]["interval"]
            lo,hi = lo-2*widen,hi+2*widen
            assert lo<=hi
            constants[axis] = (lo+hi)/2
        out = []
        for row in joined:
            obs = dict(frame=row["frame"],A={},C={})
            for axis in ("x","y"):
                aa,cc = row["joined"][axis]["A"],row["joined"][axis]["C"]
                aL,aU,cL,cU = aa[0]-widen,aa[1]+widen,cc[0]-widen,cc[1]+widen
                sep = constants[axis]
                lo,hi = max(aL,sep+cL),min(aU,sep+cU)
                assert lo<=hi
                av = (lo+hi)/2
                cv = av-sep
                for orig in row["original"].values():
                    assert q(orig["A"][axis][0])-widen <= av <= q(orig["A"][axis][1])+widen
                    assert q(orig["C"][axis][0])-widen <= cv <= q(orig["C"][axis][1])+widen
                obs["A"][axis],obs["C"][axis] = av,cv
            out.append(obs)
        return dict(delta=widen,constants=constants,rows=out)
    feasible = delta == 0
    return dict(status="feasible" if feasible else "infeasible",axes=axes,
                joined=joined,minimum_delta=delta,
                zero_witness=witness(F(0)) if feasible else None,
                minimum_delta_witness=witness(delta))


def own_math_controls():
    checked = []
    for n in (5,9,13,21):
        t = [F(i,5) for i in range(n)]
        for name, yy, aa in (
            ("constant",[F(6)]*n,F(0)),
            ("linear",[7+3*v for v in t],F(0)),
            ("curved",[2-3*v+F(5,2)*v*v for v in t],F(5)),
        ):
            fit = exact_fit(t,yy,[[v-1,v+2] for v in yy])
            assert fit["acceleration"] == aa
            assert not any(fit["models"][2]["residuals"])
            shifted = exact_fit([v+200 for v in t],[v+300 for v in yy])
            assert shifted["acceleration"] == aa
            checked.append(dict(name=f"{name}_{n}",passed=True))
    ts = [F(i,5) for i in range(5)]
    iv = [[F(i)-F(1,3),F(i)+F(2,3)] for i in range(5)]
    expected = exact_fit(ts,list(range(5)),iv)
    vertices = [exact_fit(ts,[iv[i][b] for i,b in enumerate(bits)])["acceleration"] for bits in itertools.product((0,1),repeat=5)]
    assert [min(vertices),max(vertices)] == expected["interval"]
    checked.append(dict(name="all32_signed_interval_vertices",passed=True))
    for name,t,y in (
        ("missing",ts,[1,2,None,4,5]),
        ("ambiguous_nonnumeric",ts,[1,2,"ambiguous",4,5]),
        ("nonfinite",ts,[1,2,float("nan"),4,5]),
        ("duplicate_clock",[0,1,1],[1,2,3]),
    ):
        try:
            exact_fit(t,y)
        except ValueError:
            checked.append(dict(name=name,passed=True))
        else:
            raise AssertionError("rejection_control_failed")

    def original(ax,cx,ay=(0,0),cy=(0,0)):
        return {"A":{"x":ax,"y":ay},"C":{"x":cx,"y":cy}}
    globals_only = [{"frame":0,"original":{"p":original((0,0),(0,0))}},
                    {"frame":1,"original":{"p":original((4,4),(0,0))}}]
    local_only = [{"frame":0,"original":{"p":original((0,0),(0,0)),"q":original((4,4),(0,0))}}]
    touching = [{"frame":0,"original":{"p":original((0,2),(0,0))}},
                {"frame":1,"original":{"p":original((2,4),(0,0))}}]
    mixed = [{"frame":0,"original":{"p":original((0,0),(0,0),(0,0),(0,0))}},
             {"frame":1,"original":{"p":original((4,4),(0,0),(8,8),(0,0))}}]
    for name,rows,expected_delta in (
        ("global_gap_div4",globals_only,F(1)),
        ("local_observer_gap_div2",local_only,F(2)),
        ("touching_is_feasible",touching,F(0)),
        ("two_axis_largest_requirement",mixed,F(2)),
    ):
        s = joint_math(rows)
        assert s["minimum_delta"] == expected_delta
        # Check strict infeasibility just below any positive exact threshold.
        if expected_delta:
            d = expected_delta-F(1,1000)
            assert any(a["local_delta"]>d or a["global_delta"]>d for a in s["axes"].values())
        shifted = []
        for i,row in enumerate(rows):
            originals = {}
            for observer,features in row["original"].items():
                originals[observer] = {
                    feature:{axis:[q(v)+F((i+1)*7,3) for v in box] for axis,box in coords.items()}
                    for feature,coords in features.items()}
            shifted.append(dict(frame=row["frame"],original=originals))
        transformed = joint_math(shifted)
        assert transformed["minimum_delta"] == expected_delta
        assert all(transformed["axes"][a]["interval"]==s["axes"][a]["interval"] for a in ("x","y"))
        checked.append(dict(name=name,passed=True,delta_exact=str(expected_delta)))
    assert joint_math([])=={"status":"no_paired_data"}
    checked.append(dict(name="empty_pairs_not_unconstrained_feasibility",passed=True))
    return checked


# END_INDEPENDENT_MATH

BASE = Path(__file__).resolve().parent
MATH_PREFIX_PIN = "6ac5ade0e3cfae57519099531e8fd966a8b9fb2aab2f1f465fdac485e46f37ff"
TOLERANCE = 1e-8
SELECTED = [258]+list(range(288,349,3))
LATE = SELECTED[1:]
ANNOTATIONS = {
    "root_C": (BASE/"root-observations.json","b0c8fa4339ab36188c20779ec8414d211e1be6ecb39a7597c2a9c90fd5f64838"),
    "independent_C": (BASE/"independent-observations.json","8ee9e5c5884dbcc9645958e96c9c7fa8561953cbb71820d0f699b72874f2c47a"),
    "root_A": (BASE.parent/"camera3-late-reannotation/root-observations.json","20b873f21704b3ccb8ceb75cba3eb09a84ab3431223a0c3f68ef7ce54efa397a"),
    "independent_A": (BASE.parent/"camera3-late-reannotation/independent-observations.json","529db0a68030a3ef26eef26723f0ab8c635fe47d6a743b780014d375ab95808f"),
    "protocol": (BASE/"PROTOCOL.md","d8adc5afa2e8f9b5d986b0d3042f8b420509478fc84dd5dfd7ea26016415c27e"),
}


def fingerprint(path):
    content = path.read_bytes()
    return {"bytes":len(content),"sha256":hashlib.sha256(content).hexdigest()}


def load_json(path):
    return json.loads(path.read_text())


def safe_json(value):
    if isinstance(value,F):
        return str(value)
    if isinstance(value,dict):
        return {str(k):safe_json(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [safe_json(v) for v in value]
    return value


class Check:
    def __init__(self):
        self.failures=[]
        self.counts=Counter()
        self.errors=defaultdict(float)

    def require(self,condition,label):
        self.counts["logical_checks"]+=1
        if not condition:
            self.failures.append(label)

    def equal(self,actual,expected,label,category="scalar"):
        if isinstance(expected,dict):
            self.require(isinstance(actual,dict),label+":dict")
            if not isinstance(actual,dict):
                return
            self.require(set(actual)==set(expected),label+":keys")
            for key,value in expected.items():
                if key in actual:
                    self.equal(actual[key],value,label+"/"+str(key),str(key))
        elif isinstance(expected,(tuple,list)):
            self.require(isinstance(actual,list) and len(actual)==len(expected),label+":length")
            if isinstance(actual,list):
                for i,(a,e) in enumerate(zip(actual,expected)):
                    self.equal(a,e,label+"/"+str(i),category)
        elif expected is None or isinstance(expected,(str,bool)):
            self.require(actual==expected and type(actual) is type(expected),label+":exact")
        elif isinstance(expected,(F,int,float)):
            self.counts["numeric_checks"]+=1
            try:
                error=abs(q(actual)-q(expected))
            except (ValueError,TypeError,ZeroDivisionError):
                self.failures.append(label+":not_numeric")
                return
            self.errors[category]=max(self.errors[category],float(error))
            if isinstance(actual,str) and isinstance(expected,F):
                self.require(error==0,label+":exact_rational")
            elif float(error)>TOLERANCE:
                self.failures.append(label+":tolerance")
        else:
            raise TypeError("unsupported comparison")


def read_observations(check):
    docs={}
    for observer in ("root","independent"):
        cc=load_json(ANNOTATIONS[observer+"_C"][0])
        aa=load_json(ANNOTATIONS[observer+"_A"][0])
        check.require([r["frame"] for r in cc["frames"]]==SELECTED,observer+":Cframes")
        check.require([r["frame"] for r in aa["rows"]]==SELECTED,observer+":Aframes")
        check.require(cc["observer"]==observer,observer+":Clabel")
        docs[observer]={}
        for c,a in zip(cc["frames"],aa["rows"]):
            feature=a["A"]
            acopy={axis:feature[axis] for axis in ("x","y")}
            acopy.update({axis+"_bounds":[feature[axis+"min"],feature[axis+"max"]] for axis in ("x","y")})
            if c["x"] is None or c["y"] is None:
                check.require(all(c[k] is None for k in ("x","y","x_bounds","y_bounds")),f"{observer}/{c['frame']}/null_C")
            else:
                for axis in ("x","y"):
                    check.require(c[axis+"_bounds"][0]<=c[axis]<=c[axis+"_bounds"][1],f"{observer}/{c['frame']}/{axis}/inbox")
            docs[observer][c["frame"]]={"A":acopy,"C":c}
    return docs


def original_rows(docs,observers,frames):
    rows,omitted=[],[]
    for frame in frames:
        if any(docs[o][frame][feat][axis] is None for o in observers for feat in ("A","C") for axis in ("x","y")):
            omitted.append(frame)
            continue
        original={o:{feat:{axis:docs[o][frame][feat][axis+"_bounds"] for axis in ("x","y")} for feat in ("A","C")} for o in observers}
        rows.append(dict(frame=frame,original=original))
    return rows,omitted


def fit_output(frames,values,bounds):
    missing=[f for f,v in zip(frames,values) if v is None]
    if missing:
        return {"status":"missing","missing_frames":missing}
    result=exact_fit([F(f-138,15) for f in frames],values,bounds)
    return {"status":"computed","t":result["time"],"values":result["y"],
            "bounds":result["bounds"],"center":result["center"],"halfspan":result["halfspan"],
            "linear":{k:v for k,v in result["models"][1].items() if k!="condition"},
            "quadratic":{k:v for k,v in result["models"][2].items() if k!="condition"},
            "acceleration":result["acceleration"],"weights":result["weights"],
            "acceleration_bounds":result["interval"]}


def check_comparison(check,docs,actual):
    expected=[]
    for frame in SELECTED:
        row={"frame":frame,"observers":{}}
        for o in ("root","independent"):
            a,c=docs[o][frame]["A"],docs[o][frame]["C"]
            d={"C_localized":c["x"] is not None and c["y"] is not None}
            if d["C_localized"]:
                for axis in ("x","y"):
                    ab,cb=a[axis+"_bounds"],c[axis+"_bounds"]
                    d[axis]={"C":c[axis],"C_bounds":cb,"A":a[axis],"A_bounds":ab,
                             "A_minus_C":a[axis]-c[axis],"separation_bounds":[ab[0]-cb[1],ab[1]-cb[0]]}
                check.counts["localized_observer_comparisons"]+=1
            else:
                check.counts["missing_observer_comparisons"]+=1
            row["observers"][o]=d
        if all(v["C_localized"] for v in row["observers"].values()):
            row["C_overlap"]={axis:[max(docs[o][frame]["C"][axis+"_bounds"][0] for o in docs),
                                    min(docs[o][frame]["C"][axis+"_bounds"][1] for o in docs)]
                              for axis in ("x","y")}
        expected.append(row)
    check.equal(actual,expected,"comparison")
    check.counts["comparison_frames"]=len(expected)


def check_fits(check,docs,actual):
    index={}
    for row in actual:
        key=(row["observer"],row["series"],tuple(row["frames"]))
        check.require(key not in index,"fits:duplicate")
        index[key]=row
    keys=[]
    for observer in ("root","independent"):
        for series in ("C","A-C"):
            for n in (9,13,21):
                for start in range(22-n):
                    frames=LATE[start:start+n]
                    key=(observer,series,tuple(frames))
                    keys.append(key)
                    check.require(key in index,"fits:missing_key")
                    if key not in index:
                        continue
                    values,bounds=[],[]
                    for frame in frames:
                        a,c=docs[observer][frame]["A"],docs[observer][frame]["C"]
                        if c["y"] is None:
                            values.append(None); bounds.append(None)
                        elif series=="C":
                            values.append(c["y"]); bounds.append(c["y_bounds"])
                        else:
                            values.append(a["y"]-c["y"])
                            bounds.append([a["y_bounds"][0]-c["y_bounds"][1],a["y_bounds"][1]-c["y_bounds"][0]])
                    fitted=fit_output(frames,values,bounds)
                    check.equal(index[key],{"observer":observer,"series":series,"frames":frames,"fit":fitted},
                                f"fit/{observer}/{series}/{frames[0]}-{frames[-1]}")
                    if fitted["status"]=="missing":
                        check.counts["missing_fit_windows"]+=1
                    else:
                        check.counts["computed_fit_windows"]+=1
                        check.counts["fit_coefficients"]+=5
                        check.counts["fit_residuals"]+=2*n
                        check.counts["fit_weights"]+=n
                        check.counts["fit_interval_endpoints"]+=2
                        check.counts["computed_"+observer+"_"+series]+=1
                        if series=="A-C":
                            aa=exact_fit([F(f-138,15) for f in frames],[docs[observer][f]["A"]["y"] for f in frames])
                            cc=exact_fit([F(f-138,15) for f in frames],[docs[observer][f]["C"]["y"] for f in frames])
                            check.require(fitted["acceleration"]==aa["acceleration"]-cc["acceleration"],"difference:linearity")
                            check.counts["difference_linearity"]=check.counts["difference_linearity"]+1
    check.require(set(index)==set(keys) and len(actual)==92,"fits:complete92")


def check_joint_result(check,original,actual,label,historical=False):
    """Check independent joined intervals, then actual witness membership.

A valid actual witness need not equal this verifier's preferred witness.
Its coordinates are checked exactly against original widened boxes.
"""
    result=joint_math(original)
    if not original:
        check.equal(actual,{"status":"no_data"},label)
        return result
    axes={}
    for axis in ("x","y"):
        aa=result["axes"][axis]
        per=[]
        for r in result["joined"]:
            a,c=r["joined"][axis]["A"],r["joined"][axis]["C"]
            per.append({"frame":r["frame"],"A":a,"C":c,"separation":[a[0]-c[1],a[1]-c[0]]})
        gap=max(v[feat][0]-v[feat][1] for v in per for feat in ("A","C"))
        axes[axis]={"per_frame":per,"intersection":aa["interval"],
                    "max_lower_frames":aa["lower_frames"],"min_upper_frames":aa["upper_frames"],
                    "local_max_gap":gap,"minimum_delta":aa["delta"],"feasible_original":aa["delta"]==0}
    summary={"status":"computed","axes":axes,"minimum_uniform_delta":result["minimum_delta"],
             "feasible_original":result["status"]=="feasible",
             "witness_separation":result["minimum_delta_witness"]["constants"],
             "witness_delta":result["minimum_delta"],"witness_is_observation":False}
    check.equal({k:v for k,v in actual.items() if k!="witness"},summary,label+"/summary")
    check.require("witness" in actual,label+":missing_witness")
    witness=actual.get("witness",[])
    check.require([v["frame"] for v in witness]==[v["frame"] for v in original],label+":witness_frames")
    d=result["minimum_delta"]
    for row,w in zip(original,witness):
        check.require(set(w)=={"frame","x","y"},label+":witness_keys")
        for axis in ("x","y"):
            check.require(set(w[axis])=={"A","C"},label+":witness_coordinate_keys")
            a,c=q(w[axis]["A"]),q(w[axis]["C"])
            check.require(a-c==result["minimum_delta_witness"]["constants"][axis],label+":exact_constant")
            for obs in row["original"].values():
                for feature,value in (("A",a),("C",c)):
                    lo,hi=map(q,obs[feature][axis])
                    check.require(lo-d<=value<=hi+d,label+":exact_original_box")
                    check.counts["historical_original_box_memberships" if historical else "control_original_box_memberships"]+=1
        check.counts["historical_witness_rows" if historical else "control_witness_rows"]+=1
    if historical:
        check.counts["historical_joint_axes"]+=2
        check.counts["historical_joint_joined_rows"]+=len(original)
    return result


def check_joint(check,docs,actual):
    lookup={(v["observer"],v["coverage"]):v for v in actual}
    check.require(len(lookup)==len(actual)==6,"joint:six_unique_scenarios")
    summaries=[]
    for label,observers in (("root",["root"]),("independent",["independent"]),("combined",["root","independent"])):
        for coverage,frames in (("all",SELECTED),("late",LATE)):
            original,omitted=original_rows(docs,observers,frames)
            key=(label,coverage)
            check.require(key in lookup,"joint:missing_scenario")
            if key not in lookup:
                continue
            out=lookup[key]
            expected_rows=[{"frame":r["frame"],"observers":[{"observer":o,**r["original"][o]} for o in observers]} for r in original]
            check.equal({k:v for k,v in out.items() if k!="result"},
                        {"observer":label,"coverage":coverage,"selected_frames":frames,"omitted":omitted,"rows":expected_rows},
                        f"joint/{label}/{coverage}/sources")
            solution=check_joint_result(check,original,out["result"],f"joint/{label}/{coverage}",True)
            summaries.append({"observer":label,"coverage":coverage,"included":len(original),"omitted":omitted,
                              "status":solution["status"],"minimum_delta":solution["minimum_delta"],
                              "axes":{a:{"interval":v["interval"],"delta":v["delta"],"lower_frames":v["lower_frames"],"upper_frames":v["upper_frames"]} for a,v in solution["axes"].items()}})
    return summaries


def control_rows(entries):
    return [{"frame":row["frame"],"original":{str(i):features for i,features in enumerate(row["observers"])}} for row in entries]


def check_controls(check,actual):
    check.require(set(actual)=={"fits","missing","joint","empty"},"controls:keys")
    t=[F(f-138,15) for f in LATE[:9]]
    names=["constant","linear","curved","translated_pair_difference"]
    check.require([c["name"] for c in actual["fits"]]==names,"controls:fit_names")
    for c in actual["fits"]:
        name=c["name"]
        yy={"constant":[F(7)]*9,"linear":[3+2*z for z in t],
            "curved":[3+2*z+4*z*z for z in t],"translated_pair_difference":[F(10)]*9}[name]
        expected={"name":name,"frames":LATE[:9],"expected_acceleration":8 if name=="curved" else 0,
                  "result":fit_output(LATE[:9],yy,[[y-1,y+1] for y in yy])}
        check.equal(c,expected,"control/fit/"+name)
        check.counts["producer_control_fits"]+=1
    check.equal(actual["missing"],{"frames":LATE[:9],"values":[0]*8+[None],"result":{"status":"missing","missing_frames":[312]}},"control/missing")
    check.equal(actual["empty"],{"rows":[],"result":{"status":"no_data"}},"control/empty")
    # Full retained fixture inputs, not merely expected-delta flags.
    def features(a,c):
        return {"A":dict(x=a,y=a),"C":dict(x=c,y=c)}
    fixtures={
        "constant":[{"frame":0,"observers":[features([9,11],[1,3])]},
                    {"frame":1,"observers":[features([19,21],[11,13])]}],
        "global_conflict":[{"frame":0,"observers":[features([0,0],[0,0])]},
                           {"frame":1,"observers":[features([4,4],[0,0])]}],
        "local_conflict":[{"frame":0,"observers":[features([0,0],[0,0]),features([4,4],[4,4])]}],
        "touching":[{"frame":0,"observers":[features([0,1],[0,1])]},
                    {"frame":1,"observers":[features([2,3],[0,1])]}],
    }
    expected_delta={"constant":0,"global_conflict":1,"local_conflict":2,"touching":0}
    check.require(len(actual["joint"])==4 and {v["name"] for v in actual["joint"]}==set(fixtures),"controls:joint_names")
    for c in actual["joint"]:
        check.equal({k:v for k,v in c.items() if k!="result"},
                    {"name":c["name"],"rows":fixtures[c["name"]],"expected_delta":expected_delta[c["name"]]},
                    "control/joint/"+c["name"]+"/input")
        solution=check_joint_result(check,control_rows(fixtures[c["name"]]),c["result"],"control/joint/"+c["name"])
        check.require(solution["minimum_delta"]==expected_delta[c["name"]],"control:declared_delta")
        check.counts["producer_joint_controls"]+=1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default="verification01.json")
    args=parser.parse_args()
    destination=(BASE/args.output).resolve()
    if destination.parent!=BASE or destination.exists() or destination.suffix!=".json":
        raise ValueError("new_JSON_in_declared_unit_required")
    content=Path(__file__).read_bytes()
    marker=b"# END_INDEPENDENT_MATH\n"
    prefix=content[:content.index(marker)+len(marker)]
    if hashlib.sha256(prefix).hexdigest()!=MATH_PREFIX_PIN:
        raise ValueError("independent_math_prefix_changed")
    check=Check()
    # Execute synthetic math controls before inspecting historical numeric outputs.
    own_controls=own_math_controls()
    before={name:fingerprint(path) for name,(path,pin) in ANNOTATIONS.items()}
    for name,(path,pin) in ANNOTATIONS.items():
        check.require(before[name]["sha256"]==pin,"pin:"+name)
    views=BASE.parent/"camera3-late-reannotation/views01/receipt.json"
    check.require(fingerprint(views)["sha256"]=="8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161","pin:views")
    if check.failures:
        raise ValueError("source_pin_mismatch")
    receipt_path=BASE/"analysis01/receipt.json"
    receipt=load_json(receipt_path)
    code_pin=fingerprint(BASE/"analyze.py")
    check.require(code_pin["sha256"]==receipt["source_code_sha256"],"producer_code_pin")
    expected_inputs={str(path):pin for path,pin in ANNOTATIONS.values()}
    expected_inputs[str(views)]="8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161"
    check.equal(receipt["inputs_before_and_after"],expected_inputs,"producer_input_pins")
    products={name:fingerprint(BASE/"analysis01"/name) for name in ("results.json","controls.json")}
    check.equal(receipt["outputs"],{name:value["sha256"] for name,value in products.items()},"producer_output_pins")
    docs=read_observations(check)
    check_controls(check,load_json(BASE/"analysis01/controls.json"))
    output=load_json(BASE/"analysis01/results.json")
    check.require(set(output)=={"comparison","fits","joint"},"results:keys")
    check_comparison(check,docs,output["comparison"])
    check_fits(check,docs,output["fits"])
    scenarios=check_joint(check,docs,output["joint"])
    after={name:fingerprint(path) for name,(path,pin) in ANNOTATIONS.items()}
    check.equal(after,before,"annotations_unchanged")
    check.equal({name:fingerprint(BASE/"analysis01"/name) for name in products},products,"outputs_unchanged")
    check.equal(fingerprint(BASE/"analyze.py"),code_pin,"producer_code_unchanged")
    record={
        "status":"pass_independent_conditional_arithmetic" if not check.failures else "verification_failed",
        "python":platform.python_version(),"command":[sys.executable,*sys.argv],
        "verifier":fingerprint(Path(__file__)),"independent_math_prefix_sha256":MATH_PREFIX_PIN,
        "absolute_tolerance":TOLERANCE,"exact_joint_arithmetic":True,
        "method":"Fraction equal-grid normal equations and independently derived box-gap feasibility; no producer import or execution",
        "inputs_before":before,"inputs_after":after,"views_receipt":fingerprint(views),
        "producer_code":code_pin,"producer_receipt":fingerprint(receipt_path),"producer_outputs":products,
        "counts":dict(sorted(check.counts.items())),"maximum_absolute_errors":dict(sorted(check.errors.items())),
        "failures":check.failures,"independent_controls":own_controls,
        "joint_scenario_summaries":safe_json(scenarios),
        "limits":[
            "Input image identity, native frame/clock authenticity and architectural material identity are not validated by arithmetic reproduction.",
            "Placement boxes are subjective and uncalibrated; feasible witnesses and minimum widening delta are mathematical sensitivity, not historical estimates.",
            "Missing C frames345/348 remain excluded/uncomputed, never interpolated.",
            "Common image vector constancy is not a necessary or sufficient condition for physical rigidity under perspective/camera motion.",
            "Translated_pair_difference producer fixture retains difference values, not the two original translated arrays; reproduction covers that retained constant input.",
            "Computational review is not human annotation or licensed-engineering validation; research-only with no cause or intent identification.",
        ],
    }
    destination.write_text(json.dumps(record,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({"status":record["status"],"counts":record["counts"],"maximum_absolute_errors":record["maximum_absolute_errors"],
                      "failures":check.failures,"receipt_sha256":fingerprint(destination)["sha256"]},sort_keys=True))
    return 0 if not check.failures else 1


if __name__=="__main__":
    sys.exit(main())

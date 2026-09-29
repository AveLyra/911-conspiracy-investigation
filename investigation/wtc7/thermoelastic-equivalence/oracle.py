#!/usr/bin/env python3
"""Independent exact-rational oracle; synthetic mechanics, not historical data.

Derivation: axial equilibrium (no distributed axial load, constant area) gives
one normalized force n in every series segment. The specified constitutive
law gives eps_i = n*(1 + beta*theta_i**2) + theta_i/1000. Compatibility gives
delta = sum(w_i*eps_i) = n*C + H, where sum(w_i)=1. Thus prescribed length d
requires n=(d-H)/C. A clamp replaces, rather than supplements, the end traction.

This file was developed from PROTOCOL.md without reading/importing the root
calculator, its outputs, or another review. Its checks concern only this law.
"""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import sys


PROTOCOL_PIN = "d9df71946dd097a4b6154d07fb07c8e0dff8206a91c1393f8251ceac9b817bc0"
P = F(1, 1000)
P2 = F(1, 500)
CHECKS = []


def exact(value):
    if type(value) not in (int, F):
        raise TypeError("Only integer/Fraction inputs; no float approximation")
    return F(value)


def bar(theta, beta, weights=None):
    theta = tuple(exact(x) for x in theta)
    beta = exact(beta)
    if not theta:
        raise ValueError("Empty series bar")
    weights = tuple(exact(w) for w in weights) if weights is not None else (
        (F(1, len(theta)),) * len(theta)
    )
    if len(weights) != len(theta):
        raise ValueError("Temperature/length count mismatch")
    if beta < 0 or any(t < 0 for t in theta):
        raise ValueError("Outside declared beta>=0, heating-only fixture domain")
    if any(w <= 0 for w in weights) or sum(weights) != 1:
        raise ValueError("Positive reference lengths must sum exactly to one")
    return {"theta": theta, "beta": beta, "weights": weights}


def strains(state, force):
    force = exact(force)
    return tuple(force * (1 + state["beta"] * t*t) + t/1000
                 for t in state["theta"])


def extension(state, force):
    return sum(w*e for w, e in zip(state["weights"], strains(state, force)))


def components(state):
    # Direct segment sums, separately from the load-response probe.
    thermal = sum(w*t/1000 for w, t in zip(state["weights"], state["theta"]))
    compliance = sum(w*(1 + state["beta"]*t*t)
                     for w, t in zip(state["weights"], state["theta"]))
    return thermal, compliance


def clamp(state, imposed_extension):
    thermal, compliance = components(state)
    return (exact(imposed_extension) - thermal) / compliance


def identify(load1, elongation1, load2, elongation2):
    load1, elongation1, load2, elongation2 = map(
        exact, (load1, elongation1, load2, elongation2))
    if load1 == load2:
        raise ValueError("Coincident loads cannot identify slope/intercept")
    compliance = (elongation2-elongation1)/(load2-load1)
    if compliance <= 0:
        raise ValueError("Nonpositive compliance contradicts positive modulus")
    return elongation1-load1*compliance, compliance


def check(name, condition, kind="positive_control"):
    if not condition:
        raise AssertionError(name)
    CHECKS.append({"name": name, "kind": kind, "passed": True})


def rejection(name, action, exception):
    try:
        action()
    except exception as error:
        CHECKS.append({"name": name, "kind": "expected_rejection", "passed": True,
                       "exception": type(error).__name__, "message": str(error)})
    else:
        raise AssertionError("Expected rejection did not occur: " + name)


def encode(value):
    if isinstance(value, F):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {str(key): encode(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(val) for val in value]
    return value


def state_record(name, state):
    thermal, compliance = components(state)
    record = {"input": state, "thermal_extension_H": thermal,
              "axial_compliance_C": compliance, "load_probes": {}}
    for label, load in (("zero", F(0)), ("p", P), ("p2", P2)):
        delta = extension(state, load)
        record["load_probes"][label] = {
            "force": load, "segment_strains": strains(state, load),
            "total_extension": delta,
            "increment_from_cold_at_same_probe_load": delta-load,
            "increment_from_common_cold_preload_p": delta-P,
        }
        check(f"{name}: affine compatibility at {label}", delta == thermal+load*compliance)
    record["clamps"] = {}
    for label, imposed in (("cold_stress_free", F(0)), ("cold_preloaded", P)):
        force = clamp(state, imposed)
        record["clamps"][label] = {
            "prescribed_total_extension": imposed, "total_force": force,
            "force_change_from_initial": force-(P if label == "cold_preloaded" else 0),
            "segment_strains": strains(state, force),
        }
        check(f"{name}: clamp compatibility {label}", extension(state, force) == imposed)
        recovered = tuple((e-t/1000)/(1+state["beta"]*t*t)
                          for e, t in zip(strains(state, force), state["theta"]))
        check(f"{name}: segment equilibrium {label}", all(n == force for n in recovered))
    record["two_load_identifications"] = []
    for load1, load2 in ((F(0), P), (P, P2), (F(0), P2)):
        found = identify(load1, extension(state, load1), load2, extension(state, load2))
        check(f"{name}: identification {load1},{load2}", found == (thermal, compliance))
        record["two_load_identifications"].append({"loads": (load1, load2), "H_C": found})
    return record


# Exact bivariate polynomial arithmetic, keys = powers (s, q).
def poly_add(*polys):
    result = {}
    for poly in polys:
        for power, coefficient in poly.items():
            result[power] = result.get(power, F(0)) + coefficient
    return {power: coefficient for power, coefficient in result.items() if coefficient}


def poly_scale(poly, scalar):
    return {power: coefficient*scalar for power, coefficient in poly.items() if coefficient*scalar}


def poly_mul(left, right):
    result = {}
    for (s1, q1), a in left.items():
        for (s2, q2), b in right.items():
            power = s1+s2, q1+q2
            result[power] = result.get(power, F(0))+a*b
    return {power: coefficient for power, coefficient in result.items() if coefficient}


def trajectory_proof():
    one = {(0, 0): F(1)}
    s = {(1, 0): F(1)}
    q = {(0, 1): F(1)}
    s2, q2 = poly_mul(s, s), poly_mul(q, q)
    constraint = poly_add(q2, q, poly_scale(s2, -3), poly_scale(s, -3))
    hu, hv = poly_scale(s, P), poly_scale(q, P/3)
    cu, cv = poly_add(one, s2), poly_add(one, poly_scale(q2, F(1, 3)))
    du, dv = poly_add(hu, poly_scale(cu, P)), poly_add(hv, poly_scale(cv, P))
    delta_difference = poly_add(dv, poly_scale(du, -1))
    check("trajectory: exact polynomial loaded-equality residual",
          delta_difference == poly_scale(constraint, F(1, 3000)), "analytic_identity")
    compliance_difference = poly_add(cv, poly_scale(cu, -1))
    for label, d in (("zero", F(0)), ("preloaded", P)):
        # (d-Hv)*Cu - (d-Hu)*Cv is the exact numerator of Nv-Nu.
        numerator = poly_add(
            poly_mul(poly_add(poly_scale(one, d), poly_scale(hv, -1)), cu),
            poly_scale(poly_mul(poly_add(poly_scale(one, d), poly_scale(hu, -1)), cv), -1))
        predicted = poly_add(
            poly_mul(poly_add(du, poly_scale(one, -d)), compliance_difference),
            poly_scale(poly_mul(cu, constraint), F(-1, 3000)))
        check(f"trajectory: exact clamp difference factorization {label}",
              numerator == predicted, "analytic_identity")
    endpoints = []
    for s_value, q_value in ((F(0), F(0)), (F(1), F(2))):
        check(f"trajectory: exact endpoint relation {s_value}",
              q_value*q_value+q_value == 3*(s_value*s_value+s_value), "analytic_identity")
        u, v = bar([s_value]*3, 1), bar([0, 0, q_value], 1)
        check(f"trajectory: endpoint elongation equality {s_value}",
              extension(u, P) == extension(v, P), "analytic_identity")
        endpoints.append({"s": s_value, "q": q_value, "shared_extension_at_p": extension(u, P),
                          "uniform_clamps": [clamp(u, 0), clamp(u, P)],
                          "variable_clamps": [clamp(v, 0), clamp(v, P)]})
    return {
        "constraint": "F(s,q)=q^2+q-3*s^2-3*s=0, 0<=s<=1, q>=0",
        "positive_root": "q=(-1+sqrt(1+12*s+12*s^2))/2",
        "monotonicity": "(2*q+1)*dq/ds=6*s+3>0; q(0)=0, q(1)=2",
        "exact_identity": "delta_variable(p)-delta_uniform(p)=F/3000",
        "strict_inequality_proof": [
            "For s>0, g(x)=x^2+x is strictly increasing for x>=0.",
            "g(s)<3*g(s)=g(q)<g(3*s); therefore s<q<3*s.",
            "On F=0, D=Cv-Cu=s-q/3>0 and R=delta(p)=p*(1+s+s^2)>p.",
            "For d in {0,p}, Nv(d)-Nu(d)=(R-d)*D/(Cu*Cv)>0.",
            "At s=0 both cold reactions agree. These are algebraic state paths, not heat-PDE solutions.",
        ],
        "cross_multiplication_identity":
            "(d-Hv)*Cu-(d-Hu)*Cv=(R-d)*(Cv-Cu)-Cu*F/3000",
        "endpoints": endpoints,
        "no_decimal_sampling_used_as_proof": True,
    }


def run():
    states = {
        "cold": bar([0, 0, 0], 1),
        "variable_modulus_uniform": bar([1, 1, 1], 1),
        "variable_modulus_nonuniform": bar([0, 0, 2], 1),
        "identical_uniform_copy": bar([1, 1, 1], 1),
        "reordered_nonuniform": bar([2, 0, 0], 1),
        "subdivided_uniform": bar([1]*6, 1),
        "subdivided_nonuniform": bar([0, 0, 0, 0, 2, 2], 1),
        "constant_modulus_uniform": bar([1, 1, 1], 0),
        "constant_modulus_nonuniform": bar([0, 0, 3], 0),
    }
    records = {name: state_record(name, state) for name, state in states.items()}
    u, v = states["variable_modulus_uniform"], states["variable_modulus_nonuniform"]
    check("uniform exact H,C", components(u) == (F(1, 1000), F(2)))
    check("nonuniform exact H,C", components(v) == (F(1, 1500), F(7, 3)))
    check("matched single-load extension", extension(u, P) == extension(v, P) == F(3, 1000))
    check("second load discriminates", extension(u, P2) == F(1, 200)
          and extension(v, P2) == F(2, 375), "counterexample")
    check("zero-load extension discriminates", extension(u, 0) != extension(v, 0), "counterexample")
    check("stress-free clamp forces differ", clamp(u, 0) == F(-1, 2000)
          and clamp(v, 0) == F(-1, 3500), "counterexample")
    check("preloaded clamp forces differ", clamp(u, P) == 0
          and clamp(v, P) == F(1, 7000), "counterexample")
    check("preloaded force increments", clamp(u, P)-P == F(-1, 1000)
          and clamp(v, P)-P == F(-3, 3500))
    check("cold clamps", clamp(states["cold"], 0) == 0 and clamp(states["cold"], P) == P)
    for duplicate, original in (
        ("identical_uniform_copy", "variable_modulus_uniform"),
        ("reordered_nonuniform", "variable_modulus_nonuniform"),
        ("subdivided_uniform", "variable_modulus_uniform"),
        ("subdivided_nonuniform", "variable_modulus_nonuniform"),
        ("constant_modulus_nonuniform", "constant_modulus_uniform"),
    ):
        a, b = states[duplicate], states[original]
        check(f"{duplicate}: H,C invariance", components(a) == components(b))
        check(f"{duplicate}: all probes/clamps invariant",
              all(extension(a, n) == extension(b, n) for n in (0, P, P2))
              and all(clamp(a, d) == clamp(b, d) for d in (0, P)))
    for name, action, exception in (
        ("coincident probes", lambda: identify(P, extension(u, P), P, extension(v, P)), ValueError),
        ("negative beta", lambda: bar([0, 0, 1], -1), ValueError),
        ("negative heating theta", lambda: bar([-1, 0, 1], 1), ValueError),
        ("empty geometry", lambda: bar([], 1), ValueError),
        ("mismatched segment counts", lambda: bar([0, 1], 1, [F(1)]), ValueError),
        ("nonpositive segment length", lambda: bar([0, 1], 1, [0, 1]), ValueError),
        ("changed total reference length", lambda: bar([0, 1], 1, [1, 1]), ValueError),
        ("floating input rejected", lambda: bar([0.0, 1, 2], 1), TypeError),
        ("nonphysical identified compliance", lambda: identify(0, 1, 1, 0), ValueError),
    ):
        rejection(name, action, exception)
    trajectory = trajectory_proof()
    return {"states": records, "continuous_path": trajectory, "checks": CHECKS,
            "check_count": len(CHECKS), "failed_checks": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    destination = args.output.resolve()
    if destination.parent != here or destination.name not in {"oracle-run01.json", "oracle-run02.json"}:
        raise ValueError("Only the two declared local oracle output paths are permitted")
    protocol = here / "PROTOCOL.md"
    protocol_hash = hashlib.sha256(protocol.read_bytes()).hexdigest()
    if protocol_hash != PROTOCOL_PIN:
        raise ValueError("Frozen protocol hash mismatch; no results written")
    payload = {
        "status": "synthetic_exact_method_test_not_historical_validation",
        "runtime": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                    "dependencies": "standard library only"},
        "protocol_sha256": protocol_hash,
        "pre_execution_protocol_clarification": {
            "previous_sha256": "020decb3dabf5327886961abdf0da5c6a8adafe3127e7446c30a738626ebaa72",
            "change": "Both cold increment baselines explicitly named before either oracle run; no prior result discarded.",
        },
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation": __doc__,
        "units": {"force": "N/(A*E0)", "extension": "DeltaL/L0", "theta": "(T-T0)/Tscale"},
        "boundary_conventions": {"stress_free_clamp_delta": F(0), "preloaded_clamp_delta": P,
                                 "p": P, "p2": P2, "clamp_replaces_end_traction": True},
        "identification": {
            "two_load_formula": "C=(delta2-delta1)/(n2-n1); H=delta1-n1*C; n1!=n2",
            "one_load_limit": "Matching H+p*C supplies one equation for two state quantities.",
            "sufficient_transfer_conditions": "Equal H and C, including same C plus equality at one load, or equality at two distinct loads at the same thermal state.",
            "unloaded_thermal_only_limit": "At probe zero, equal H alone does not identify C.",
        },
        "limits": ["Synthetic constitutive law, no historical coating or temperature inference.",
                   "Small-strain 1D axial equilibrium; no bending, buckling, plasticity, creep, damage or failure.",
                   "Prescribed temperatures independent of force; no thermal PDE solved.",
                   "Exact arithmetic is not physical, historical or collapse-model validation."],
        **run(),
    }
    serialized = json.dumps(encode(payload), sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    with destination.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(serialized)
    print(json.dumps({"output": destination.name, "checks": len(CHECKS), "failed": 0,
                      "sha256": hashlib.sha256(serialized.encode()).hexdigest()}))


if __name__ == "__main__":
    main()

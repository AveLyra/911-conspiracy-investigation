"""Finite, source-pinned arithmetic audit; not a historical trajectory model."""
import hashlib
import json
import math
from pathlib import Path

A, B, K = 379.62, 0.18562, 3.5126
TIMES = (0, 1, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.4)


def position(t):
    return -A * math.expm1(-((B * t) ** K))


def velocity(t):
    return A * K * B * (B * t) ** (K - 1) * math.exp(-((B * t) ** K))


def acceleration(t):
    x = B * t
    return A * K * B**2 * x ** (K - 2) * math.exp(-(x**K)) * (K - 1 - K * x**K)


def report():
    rows = []
    checks = []
    for t in TIMES:
        z, v, a = position(t), velocity(t), acceleration(t)
        vp = 247.52 * (B * t) ** (K - 1) * math.exp(-((B * t) ** K))
        rows.append(dict(t_s=t, z_fit_ft=z, v_derivative_ft_s=v,
                         a_derivative_ft_s2=a, a_over_report_g=a / 32.2,
                         v_printed_ft_s=vp, v_separate_line_ft_s=-44.773 + 32.196*t))
        if t > 0:
            h = 1e-4
            vdiff = (position(t+h) - position(t-h)) / (2*h)
            adiff = (velocity(t+h) - velocity(t-h)) / (2*h)
            assert math.isclose(v, vdiff, rel_tol=1e-5, abs_tol=1e-5)
            assert math.isclose(a, adiff, rel_tol=1e-5, abs_tol=1e-5)
            checks.append(dict(t_s=t, velocity_difference_abs=abs(v-vdiff),
                               acceleration_difference_abs=abs(a-adiff)))
    assert abs(A*K*B - 247.52) < 0.005
    assert position(0) == velocity(0) == acceleration(0) == 0
    peak_t = ((K - 1) / K) ** (1 / K) / B
    root = Path(__file__).resolve().parents[3]
    source = root / 'authority/nist/wtc7/ncstar-1-9.pdf'
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    assert source_hash == '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f'
    return dict(status='finite_arithmetic_checks_pass',
                source_sha256=source_hash,
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                parameters=dict(A_ft=A,b_inverse_s=B,k=K), rows=rows, difference_checks=checks,
                derivative_coefficient=A*K*B,
                fitted_velocity_maximum=dict(t_s=peak_t,v_ft_s=velocity(peak_t)),
                fitted_stage_distances_ft=[position(1.75),position(4)-position(1.75),
                                          position(5.4)-position(4)],
                limits='Published rounded equations only; not raw-data regression, historical acceleration or causal validation.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as handle:
        json.dump(report(), handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')

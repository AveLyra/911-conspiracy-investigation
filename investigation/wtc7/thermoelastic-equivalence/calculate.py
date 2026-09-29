#!/usr/bin/env python3
"""Exact synthetic series-bar check; not a heat solver or historical model."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import platform
import unittest

HERE = Path(__file__).resolve().parent
PROTOCOL_PIN = 'd9df71946dd097a4b6154d07fb07c8e0dff8206a91c1393f8251ceac9b817bc0'
P = Q(1, 1000)
P2 = Q(1, 500)
ONE = Q(1)
ZERO = Q(0)


def rational(value):
    if not isinstance(value, Q):
        raise ValueError('exact Fraction required')
    return value


def state(theta, weights=None, beta=ONE):
    """Return free thermal extension H and series compliance C, normalized."""
    if not theta:
        raise ValueError('empty bar')
    beta = rational(beta)
    theta = tuple(rational(t) for t in theta)
    if beta < 0 or any(t < 0 for t in theta):
        raise ValueError('outside declared nonnegative domain')
    if weights is None:
        weights = (Q(1, len(theta)),) * len(theta)
    weights = tuple(rational(w) for w in weights)
    if len(weights) != len(theta) or any(w <= 0 for w in weights) or sum(weights) != 1:
        raise ValueError('positive segment fractions summing to one required')
    h = sum((w * t / 1000 for w, t in zip(weights, theta)), ZERO)
    c = sum((w * (1 + beta * t * t) for w, t in zip(weights, theta)), ZERO)
    return h, c


def elongation(hc, load):
    h, c = hc
    return h + rational(load) * c


def restrained(hc, target):
    h, c = hc
    if c <= 0:
        raise ValueError('nonpositive compliance')
    return (rational(target) - h) / c


def identify(load_a, displacement_a, load_b, displacement_b):
    for x in (load_a, displacement_a, load_b, displacement_b):
        rational(x)
    if load_a == load_b:
        raise ValueError('two distinct probing loads required')
    c = (displacement_b - displacement_a) / (load_b - load_a)
    if c <= 0:
        raise ValueError('data incompatible with positive compliance')
    return displacement_a - load_a * c, c


def fixtures():
    return {
        'cold': ((ZERO, ZERO, ZERO), ONE),
        'uniform': ((ONE, ONE, ONE), ONE),
        'variable': ((ZERO, ZERO, Q(2)), ONE),
        'constant_uniform': ((ONE, ONE, ONE), ZERO),
        'constant_variable': ((ZERO, ZERO, Q(3)), ZERO),
    }


def scalar_row(theta, beta):
    hc = state(theta, beta=beta)
    return {
        'theta': theta, 'beta': beta,
        'free_thermal_extension': hc[0], 'axial_compliance': hc[1],
        'probe_loads': [
            {'load': n, 'total_extension': elongation(hc, n),
             'increment_from_own_cold_load': elongation(hc, n) - n,
             'increment_from_reference_preload': elongation(hc, n) - P}
            for n in (ZERO, P, P2)
        ],
        'stress_free_clamp_total_force': restrained(hc, ZERO),
        'preloaded_clamp_total_force': restrained(hc, P),
        'preloaded_clamp_force_increment': restrained(hc, P) - P,
        'identified_at_zero_and_p': identify(ZERO, elongation(hc, ZERO), P, elongation(hc, P)),
        'identified_at_p_and_p2': identify(P, elongation(hc, P), P2, elongation(hc, P2)),
    }


def path_identity():
    """Exact bivariate-polynomial identity, not sampled trajectory proof.

    Keys are powers (s,q). U extension - V extension =
    -(q^2+q-3*s^2-3*s)/3000. Nonnegative q is the specified root.
    """
    direct = {(2, 0): Q(1, 1000), (1, 0): Q(1, 1000),
              (0, 2): Q(-1, 3000), (0, 1): Q(-1, 3000)}
    constraint = {(0, 2): ONE, (0, 1): ONE, (2, 0): Q(-3), (1, 0): Q(-3)}
    scaled = {key: -value / 3000 for key, value in constraint.items()}
    if direct != scaled:
        raise AssertionError('polynomial identity failed')
    return {'difference_polynomial_s_q': {f'{s},{q}': c for (s, q), c in sorted(direct.items())},
            'constraint_multiplier': Q(-1, 3000),
            'endpoints': [{'s': ZERO, 'q': ZERO}, {'s': ONE, 'q': Q(2)}],
            'scope': 'Algebraic identity only; no solved heat-transfer field.'}


class Controls(unittest.TestCase):
    def test_cold(self):
        hc = state((ZERO,) * 3)
        self.assertEqual(hc, (ZERO, ONE))
        self.assertEqual(restrained(hc, ZERO), ZERO)
        self.assertEqual(restrained(hc, P), P)

    def test_uniform_known(self):
        hc = state((ONE,) * 3)
        self.assertEqual(hc, (P, Q(2)))
        self.assertEqual(elongation(hc, P), Q(3, 1000))
        self.assertEqual(restrained(hc, ZERO), Q(-1, 2000))
        self.assertEqual(restrained(hc, P), ZERO)

    def test_variable_known(self):
        hc = state((ZERO, ZERO, Q(2)))
        self.assertEqual(hc, (Q(1, 1500), Q(7, 3)))
        self.assertEqual(elongation(hc, P), Q(3, 1000))
        self.assertEqual(restrained(hc, ZERO), Q(-1, 3500))
        self.assertEqual(restrained(hc, P), Q(1, 7000))

    def test_single_probe_counterexample(self):
        a, b = state((ONE,) * 3), state((ZERO, ZERO, Q(2)))
        self.assertEqual(elongation(a, P), elongation(b, P))
        self.assertNotEqual(elongation(a, P2), elongation(b, P2))
        for target in (ZERO, P):
            self.assertNotEqual(restrained(a, target), restrained(b, target))

    def test_common_compliance_positive_control(self):
        a = state((ONE,) * 3, beta=ZERO)
        b = state((ZERO, ZERO, Q(3)), beta=ZERO)
        self.assertEqual(a, b)
        for target in (ZERO, P):
            self.assertEqual(restrained(a, target), restrained(b, target))

    def test_identical_and_series_refinement(self):
        a = state((ZERO, ZERO, Q(2)))
        self.assertEqual(a, state((ZERO, ZERO, Q(2))))
        self.assertEqual(a, state((ZERO, ZERO, ZERO, ZERO, Q(2), Q(2))))
        self.assertEqual(a, state((ZERO, Q(2)), (Q(2, 3), Q(1, 3))))

    def test_segment_reordering(self):
        self.assertEqual(state((ZERO, ONE, Q(2))), state((Q(2), ZERO, ONE)))

    def test_two_load_identification(self):
        for theta, beta in fixtures().values():
            hc = state(theta, beta=beta)
            for a, b in ((ZERO, P), (P, P2)):
                self.assertEqual(identify(a, elongation(hc, a), b, elongation(hc, b)), hc)

    def test_invalid_inverse(self):
        for args in ((P, P, P, P), (ZERO, ONE, ONE, ZERO)):
            with self.assertRaises(ValueError):
                identify(*args)
        with self.assertRaises(ValueError):
            restrained((ZERO, ZERO), ZERO)

    def test_invalid_segment_domains(self):
        for theta, weights, beta in (((), None, ONE), ((ONE,), (Q(2),), ONE),
            ((ONE, ONE), (ONE, ZERO), ONE), ((ONE,), (Q(1, 2), Q(1, 2)), ONE),
            ((Q(-1),), None, ONE), ((ONE,), None, Q(-1)), ((1.0,), None, ONE)):
            with self.assertRaises(ValueError):
                state(theta, weights, beta)

    def test_reference_labels(self):
        row = scalar_row((ONE,) * 3, ONE)['probe_loads'][2]
        self.assertEqual(row['total_extension'], Q(1, 200))
        self.assertEqual(row['increment_from_own_cold_load'], Q(3, 1000))
        self.assertEqual(row['increment_from_reference_preload'], Q(1, 250))

    def test_full_path_identity_and_endpoints(self):
        r = path_identity()
        for e in r['endpoints']:
            s, q = e['s'], e['q']
            self.assertEqual(q*q + q, 3*(s*s+s))
            self.assertEqual(elongation(state((s,)*3), P),
                             elongation(state((ZERO, ZERO, q)), P))


def encode(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def result():
    protocol_hash = hashlib.sha256((HERE / 'PROTOCOL.md').read_bytes()).hexdigest()
    if protocol_hash != PROTOCOL_PIN:
        raise RuntimeError('protocol pin mismatch')
    return encode({
        'protocol_sha256': protocol_hash,
        'program_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python': platform.python_version(),
        'classification': 'Synthetic exact linear-thermoelastic inference test; no historical inputs.',
        'normalization': {'length': 'L0', 'force': 'A*E0', 'compliance': 'L0/(A*E0)',
                          'preload': P, 'second_probe': P2},
        'cases': {name: scalar_row(theta, beta) for name, (theta, beta) in fixtures().items()},
        'continuous_path': path_identity(),
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.self_test:
        outcome = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        if not outcome.wasSuccessful():
            raise SystemExit(1)
    if args.output:
        data = json.dumps(result(), indent=2, sort_keys=True) + '\n'
        with args.output.open('x') as stream:
            stream.write(data)
        print('Created', args.output)
    elif not args.self_test:
        parser.error('choose --self-test and/or --output')


if __name__ == '__main__':
    main()

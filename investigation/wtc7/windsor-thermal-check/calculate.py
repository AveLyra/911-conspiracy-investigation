"""Bounded arithmetic checks; no reconstruction of a thermal/FEM solver."""
import argparse
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import sys
import unittest

D = Decimal
SOURCE = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/comparator-expansion/windsor/sources/fletcher-santander-2007-draft.pdf')
SOURCE_SHA = '30de182736b632772a9d42b6178eea234ab60c54d7c8bd715bcccb72c637e007'


def positive(*values):
    if any(not v.is_finite() or v <= 0 for v in values):
        raise ValueError('Finite positive inputs required')


def diffusivity(k, rho, cp):
    positive(k, rho, cp)
    return k / (rho * cp)


def scaled_depth(depth_mm, reference_s, time_s):
    """Conditional d proportional to sqrt(t), not a source-specified formula."""
    positive(depth_mm, reference_s, time_s)
    return depth_mm * (time_s / reference_s).sqrt()


def scaled_time(depth_mm, reference_s, target_mm):
    positive(depth_mm, reference_s, target_mm)
    return reference_s * (target_mm / depth_mm) ** 2


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def monotone_compatible(t1, d1, t2, d2):
    positive(t1, d1, t2, d2)
    if t1 == t2:
        return d1 == d2
    return (t2-t1)*(d2-d1) >= 0


def results():
    with localcontext() as ctx:
        ctx.prec = 50
        k, rho, cp = D('1.2'), D('2400'), D('880')
        alpha = diffusivity(k, rho, cp)
        printed_alpha = D('0.57e-6')
        depth, time = D('50.3'), D('3600')
        spacing = D('230') / D('4')
        candidate_t58 = (D('58') / 1000) ** 2 / (4 * printed_alpha)
        candidate_t575 = (spacing / 1000) ** 2 / (4 * printed_alpha)
        values = {
            'alpha_from_k_rho_cp_m2_per_s': alpha,
            'printed_alpha_relative_difference_percent': (printed_alpha/alpha-1)*100,
            'equal_5_endpoint_node_spacing_mm': spacing,
            'sqrt_scaling_d_1400s_mm': scaled_depth(depth, time, D('1400')),
            'sqrt_scaling_d_100s_mm': scaled_depth(depth, time, D('100')),
            'sqrt_scaling_t_58mm_s': scaled_time(depth, time, D('58')),
            'sqrt_scaling_t_57_5mm_s': scaled_time(depth, time, spacing),
            'sqrt_scaling_t_10mm_s': scaled_time(depth, time, D('10')),
            'sqrt_scaling_from_58mm_1400s_d_3600s_mm': scaled_depth(D('58'), D('1400'), time),
            'c_squared_from_50_3mm_3600s': (depth/1000)**2/(printed_alpha*time),
            'c_squared_from_58mm_1400s': (D('58')/1000)**2/(printed_alpha*D('1400')),
            'hypothetical_d_2sqrt_alpha_t_at_1400s_mm': 2000*(printed_alpha*D('1400')).sqrt(),
            'hypothetical_d_2sqrt_alpha_t_at_3600s_mm': 2000*(printed_alpha*time).sqrt(),
            'hypothetical_2sqrt_t_58mm_s': candidate_t58,
            'hypothetical_2sqrt_t_57_5mm_s': candidate_t575,
            'hypothetical_2sqrt_t_58mm_derived_alpha_s': (D('58')/1000)**2/(4*alpha),
        }
        return {
            'source_observations': {'figure4_depth_mm':'50.3', 'figure4_time_s':'3600',
                'prose_spacing_mm':'58', 'prose_time_s_approximate':'1400',
                'rho_kg_m3':'2400', 'k_W_m_K':'1.2', 'cp_J_kg_K':'880',
                'printed_alpha_m2_s':'0.57e-6', 'beam_depth_mm':'230',
                'claimed_node_count':'5'},
            'same_curve_order_check': {
                'prose_time_less_than_figure_time': D('1400') < time,
                'prose_depth_greater_than_figure_depth': D('58') > depth,
                'same_nondecreasing_curve_can_include_both_central_points': monotone_compatible(time, depth, D('1400'), D('58'))},
            'derived_values': {n:str(v) for n,v in values.items()},
            'limits': [
                'Monotone check requires same definition and time origin.',
                'Square-root scaling is a conditional analytic check, not digitized source data.',
                '2sqrt(alpha*t) is a hypothetical numerical reconciliation, not attributed author method.',
                'Equal endpoint-node spacing is an assumption, not a verified ABAQUS case.',
                'No uncertainty distribution, actual temperature, mesh error or structural effect calculated.']}


class Controls(unittest.TestCase):
    def test_diffusivity_units_arithmetic(self):
        self.assertEqual(diffusivity(D(2), D(4), D(5)), D('0.1'))

    def test_constant_reference(self):
        self.assertEqual(scaled_depth(D(7), D(3), D(3)), D(7))

    def test_square_scaling(self):
        self.assertEqual(scaled_depth(D(7), D(3), D(12)), D(14))

    def test_inverse_exact(self):
        self.assertEqual(scaled_time(D(7), D(3), D(14)), D(12))

    def test_units_rescale(self):
        self.assertEqual(scaled_depth(D(7), D(3), D(12)), scaled_depth(D(7), D(180), D(720)))

    def test_roundtrip(self):
        with localcontext() as ctx:
            ctx.prec=50
            result=scaled_depth(D('50.3'), D(3600), scaled_time(D('50.3'), D(3600), D(58)))
            self.assertLess(abs(result-D(58)), D('1e-45'))

    def test_invalid(self):
        for val in (D(0), D(-1), D('Infinity'), D('NaN')):
            with self.subTest(val=str(val)), self.assertRaises(ValueError):
                scaled_time(val, D(1), D(1))

    def test_monotone_conflict(self):
        self.assertFalse(monotone_compatible(D(3600), D('50.3'), D(1400), D(58)))
        self.assertFalse(monotone_compatible(D(1), D(5), D(2), D(4)))

    def test_monotone_acceptance_and_duplicate_time(self):
        self.assertTrue(monotone_compatible(D(1), D(5), D(2), D(6)))
        self.assertTrue(monotone_compatible(D(2), D(6), D(1), D(5)))
        self.assertTrue(monotone_compatible(D(1), D(5), D(2), D(5)))
        self.assertTrue(monotone_compatible(D(1), D(5), D(1), D(5)))
        self.assertFalse(monotone_compatible(D(1), D(5), D(1), D(6)))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--test', action='store_true')
    args=parser.parse_args()
    if args.test:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
        test=unittest.TextTestRunner(verbosity=2).run(suite)
        if not test.wasSuccessful():
            raise SystemExit(1)
        return
    before=identity(SOURCE)
    assert before=={'bytes':195207, 'sha256':SOURCE_SHA}
    output=results()
    output['source_identity']=before
    output['script_identity']=identity(Path(__file__))
    output['python_identity']=identity(Path(sys.executable))
    output['python_version']=sys.version
    assert identity(SOURCE)==before
    text=json.dumps(output,indent=2,sort_keys=True)+'\n'
    if args.output:
        with args.output.open('x') as f:
            f.write(text)
    else:
        print(text,end='')


if __name__=='__main__':
    main()

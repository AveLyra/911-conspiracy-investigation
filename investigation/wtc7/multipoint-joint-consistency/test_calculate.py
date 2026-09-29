import copy
import unittest
from fractions import Fraction as F
from calculate import build, check_certificate, solve, validate_rows


def edge(u, v, b):
    return {'u': u, 'v': v, 'bound': str(b), 'label': 'synthetic'}


def interval_edges(bounds, links):
    edges = []
    for i, (lo, hi) in enumerate(bounds, 1):
        edges += [edge(0, i, hi), edge(i, 0, -F(lo))]
    for u, v, lo, hi in links:
        edges += [edge(u, v, hi), edge(v, u, -F(lo))]
    return edges


class ExactTests(unittest.TestCase):
    def checked(self, bounds, links, feasible):
        edges = interval_edges(bounds, links)
        answer = solve(len(bounds)+1, edges)
        self.assertEqual(answer['feasible'], feasible)
        check_certificate(len(bounds)+1, edges, answer)
        return answer

    def test_constant_linear_and_translation(self):
        for shift in (F(0), F(137, 3)):
            for slope in (F(0), F(-3, 2)):
                values = [shift+slope*i for i in range(5)]
                self.checked([(x-F(1, 200), x+F(1, 200)) for x in values],
                             [(i, i+1, slope, slope) for i in range(1, 5)], True)

    def test_boundary_and_beyond(self):
        self.checked([(0, 1), (0, 1)], [(1, 2, 1, 1)], True)
        self.checked([(0, 1), (0, 1)], [(1, 2, F(1001, 1000), 2)], False)

    def test_individually_feasible_jointly_impossible(self):
        bounds = [(0, F(1, 10))]*3
        links = [(1, 2, F(9, 100), F(1, 10)), (2, 3, F(9, 100), F(1, 10))]
        for link in links:
            self.checked(bounds, [link], True)
        self.checked(bounds, links, False)

    def test_disconnected_and_empty(self):
        self.checked([(0, 0), (-7, -6), (2, 3)], [], True)
        self.checked([], [], True)

    def rows(self):
        rows = []
        for i in range(5):
            row = {'row': i+1, 'time_s': str(F(i, 5))}
            row.update({t+'_'+s: None for t in ('ne', 'ec', 'wc', 'nw') for s in ('y', 'v')})
            row.update(ne_y=str(-F(i, 5)), ne_v='-1')
            rows.append(row)
        return rows

    def test_derivative_build_and_missing(self):
        rows = self.rows()
        graph = build(rows, 'ne', F(2, 5))
        self.assertEqual(graph['unsupported'], [1, 5])
        self.assertEqual(len(graph['supported']), 3)
        check_certificate(6, graph['edges'], solve(6, graph['edges']))
        rows[2]['ne_v'] = None
        self.assertEqual(len(build(rows, 'ne', F(2, 5))['supported']), 2)
        rows[1]['ne_y'] = None
        # This position participates only in the already-blank interior v.
        self.assertEqual(len(build(rows, 'ne', F(2, 5))['supported']), 2)
        rows[2]['ne_y'] = None
        self.assertEqual(len(build(rows, 'ne', F(2, 5))['supported']), 0)

    def test_malformed(self):
        for mode in ('duplicate', 'unsorted', 'time', 'token'):
            rows = self.rows()
            if mode == 'duplicate': rows[1]['row'] = rows[0]['row']
            elif mode == 'unsorted': rows.reverse()
            elif mode == 'time': rows[1]['time_s'] = '0.21'
            else: rows[1]['ne_y'] = 1
            with self.assertRaises(ValueError): validate_rows(rows)

    def test_corrupted_certificates_reject(self):
        edges = interval_edges([(0, 1), (0, 1)], [(1, 2, 2, 2)])
        result = solve(3, edges)
        wrong = copy.deepcopy(result); wrong['cycle_bound_sum'] = '0'
        with self.assertRaises(AssertionError): check_certificate(3, edges, wrong)
        with self.assertRaises(AssertionError): check_certificate(3, edges, {'feasible': True, 'vertices': ['0', '0', '0']})


if __name__ == '__main__':
    unittest.main()

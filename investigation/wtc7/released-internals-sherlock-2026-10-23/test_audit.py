import unittest
from audit import refs, thermal_values, reachable, thermal_node_row


class CensusTests(unittest.TestCase):
    def test_active_and_commented_references(self):
        rows = refs("!/input,WTC7-Fl07-1,int\n /INPUT,'FL2-LOAD1','APDL'\n")
        self.assertEqual([x['commented'] for x in rows], [True, False])
        self.assertEqual(rows[1]['target'], 'FL2-LOAD1.APDL')

    def test_temperature_fields_not_node_or_layer(self):
        self.assertEqual(list(thermal_values('BF,100,TEMP,25\nBFE,90,TEMP,13,50,50,50,50')),
                         [('BF', [25.0]), ('BFE', [50.0] * 4)])

    def test_comments_and_unrelated_fields(self):
        self.assertEqual(list(thermal_values('!BF,100,TEMP,900\nBF,100,TEMP,23!x\nBF,100,VOLT,999')),
                         [('BF', [23.0])])

    def test_cycle_and_missing(self):
        a = [{'target': 'b', 'commented': False}, {'target': 'unused', 'commented': True}]
        b = [{'target': 'a', 'commented': False}, {'target': 'missing', 'commented': False}]
        self.assertEqual(reachable(['a'], {'a': a, 'b': b, 'unused': []}), ({'a', 'b'}, {'missing'}))

    def test_unknown_expression_fails(self):
        with self.assertRaises(ValueError):
            list(thermal_values('BF,100,TEMP,PARAM+10'))

    def test_comma_thermal_card_regression(self):
        self.assertEqual(thermal_node_row('842747, 25.0, 0.00, 2'), (842747, 0.0, 25.0, 2))
        self.assertEqual(thermal_node_row('842747 25.0 0.00 2'), (842747, 0.0, 25.0, 2))


if __name__ == '__main__':
    unittest.main()

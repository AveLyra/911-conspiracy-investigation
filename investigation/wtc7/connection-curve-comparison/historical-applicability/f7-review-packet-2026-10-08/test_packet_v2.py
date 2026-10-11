import copy
from pathlib import Path
import tempfile
import unittest
import packet_v2 as p


class DependencyRepair(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='f7-closure-repair-')
        self.root = Path(self.temp.name)
        self.child = self.root / 'child.txt'
        self.child.write_text('synthetic child')
        self.pin = p.draft.pin(self.child)
        self.receipt = {'inputs': {'child.txt': self.pin}, 'inputs_after': {'child.txt': self.pin}}
        self.candidate = {'inputs': {}, 'inputs_after': {},
                          'slots': [{'id': 'TEST', 'human_response': None}], 'human_accepted': False}

    def tearDown(self):
        self.temp.cleanup()

    def test_missing_child_added_without_scientific_mutation(self):
        saved = copy.deepcopy((self.candidate, self.receipt))
        result = p.extend_closure(self.candidate, self.receipt, self.root, [])
        self.assertEqual(len(result['inputs']), 1)
        self.assertEqual(result['inputs'], result['inputs_after'])
        self.assertEqual(result['slots'], self.candidate['slots'])
        self.assertIs(result['human_accepted'], False)
        self.assertEqual((self.candidate, self.receipt), saved)

    def test_changed_child_rejected(self):
        self.child.write_text('changed')
        with self.assertRaisesRegex(ValueError, 'changed input'):
            p.extend_closure(self.candidate, self.receipt, self.root, [])

    def test_method_pin_included(self):
        method = self.root / 'method.txt'; method.write_text('synthetic method')
        result = p.extend_closure(self.candidate, self.receipt, self.root, [method])
        self.assertEqual(len(result['inputs']), 2)

    def test_candidate_drift_rejected(self):
        self.candidate['inputs_after'] = {'extra': self.pin}
        with self.assertRaisesRegex(ValueError, 'candidate pin drift'):
            p.extend_closure(self.candidate, self.receipt, self.root, [])


if __name__ == '__main__':
    unittest.main()

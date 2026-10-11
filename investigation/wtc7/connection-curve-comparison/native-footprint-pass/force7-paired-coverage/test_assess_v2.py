"""Synthetic binding guards; no new historical peer data is read."""
from pathlib import Path
import os
import tempfile
import unittest
from unittest import mock

import assess_v2 as v
from test_assess import fixture


class BindingTests(unittest.TestCase):
    def test_exact_fixed_paths(self):
        paths = v.validate_bindings(dict(v.BINDINGS))
        self.assertEqual(paths['primary'], v.HERE / 'reader-primary.json')
        self.assertEqual(paths['peer'], v.HERE / 'reader-peer-v2.json')
        self.assertNotEqual(paths['peer'], v.HERE / 'reader-peer.json')

    def test_old_alias_swapped_and_missing_paths_rejected(self):
        for bindings in (
            {'primary': 'reader-primary.json', 'peer': 'reader-peer.json'},
            {'primary': 'reader-peer-v2.json', 'peer': 'reader-primary.json'},
            {'primary': 'reader-primary.json'},
            {'primary': 'reader-primary.json', 'peer': '../reader-peer-v2.json'},
            {'primary': 'reader-primary.json', 'peer': True},
            {'primary': 'reader-primary.json', 'peer': 'reader-peer-v2.json', 'other': 'anything'},
        ):
            with self.subTest(bindings=bindings), self.assertRaises(ValueError):
                v.validate_bindings(bindings)

    def test_no_reader_hash_missing_or_extra(self):
        for pins in ({}, {'primary': '0' * 64}, {'primary': '0' * 64, 'peer': '0' * 64, 'extra': '0' * 64}):
            with self.subTest(pins=pins), self.assertRaises(ValueError):
                v.build(pins)

    def test_legacy_module_globals_unchanged(self):
        a = v.library()
        snapshot = (a.HERE, a.BASE, a.ROLES, a.TARGET.copy(), a.CONTEXT.copy())
        v.validate_bindings(v.BINDINGS)
        loaded = a.methods()
        data = fixture('peer')
        original = a.encode(data)
        a.validate(data, 'peer', loaded)
        self.assertEqual(a.encode(data), original)
        self.assertEqual((a.HERE, a.BASE, a.ROLES, a.TARGET, a.CONTEXT), snapshot)

    def test_role_mismatch_stays_rejected(self):
        a = v.library()
        with self.assertRaises(ValueError):
            a.validate(fixture('primary'), 'peer', a.methods())

    def test_all_preserved_pins_checked(self):
        a = v.library()
        pins = {}
        v.add_preserved(pins, a)
        self.assertEqual(set(pins), set(v.PRESERVED))
        self.assertEqual({name: value['sha256'] for name, value in pins.items()}, v.PRESERVED)

    def test_changed_preserved_input_rejected_without_file_mutation(self):
        a = v.library()
        original_pin = a.pin
        def changed(path):
            result = original_pin(path)
            if Path(path).name == 'reader-peer.py':
                result = {**result, 'sha256': '0' * 64}
            return result
        with mock.patch.object(a, 'pin', side_effect=changed), self.assertRaises(ValueError):
            v.add_preserved({}, a)

    def test_changed_legacy_code_rejected_without_file_mutation(self):
        with mock.patch.object(v, 'LEGACY_SHA', '0' * 64), self.assertRaises(ValueError):
            v.library()

    def test_pre_pinned_json_still_expands_nested_dependencies(self):
        a = v.library()
        with tempfile.TemporaryDirectory(prefix='f7-v2-closure-test-') as directory:
            root = Path(directory)
            leaf, middle, outer = root / 'leaf.txt', root / 'middle.json', root / 'outer.json'
            leaf.write_bytes(b'synthetic dependency only')
            middle.write_bytes(a.encode({'inputs': {'leaf.txt': a.pin(leaf)}}))
            outer.write_bytes(a.encode({'inputs': {'middle.json': a.pin(middle)}}))
            pins = {}
            a.add(pins, outer)
            a.add(pins, middle)
            v.include_reader_inputs(pins, root, {'inputs': {'outer.json': a.pin(outer)}}, a)
            self.assertEqual(set(pins), {os.path.relpath(p.resolve(), a.HERE) for p in (outer, middle, leaf)})
            leaf.write_bytes(b'changed synthetic dependency')
            with self.assertRaises(ValueError):
                v.include_reader_inputs(pins, root, {'inputs': {'outer.json': a.pin(outer)}}, a)

    def test_nested_before_after_mismatch_rejected(self):
        a = v.library()
        with tempfile.TemporaryDirectory(prefix='f7-v2-closure-test-') as directory:
            root = Path(directory)
            child = root / 'child.json'
            child.write_bytes(a.encode({'inputs': {}, 'inputs_after': {'invented': {}}}))
            with self.assertRaisesRegex(ValueError, 'Nested before/after'):
                v.include_reader_inputs({}, root, {'inputs': {'child.json': a.pin(child)}}, a)

    def test_nested_reader_script_pin_is_not_skipped(self):
        a = v.library()
        with tempfile.TemporaryDirectory(prefix='f7-v2-closure-test-') as directory:
            root = Path(directory)
            script, child = root / 'reader-invented.py', root / 'reader-invented.json'
            script.write_bytes(b'# synthetic, never executed\n')
            child.write_bytes(a.encode({'inputs': {}, 'script_pin': a.pin(script)}))
            pins = {}
            a.add(pins, child)
            v.include_reader_inputs(pins, root, {'inputs': {'reader-invented.json': a.pin(child)}}, a)
            self.assertIn(os.path.relpath(script.resolve(), a.HERE), pins)
            script.write_bytes(b'# changed synthetic script\n')
            with self.assertRaises(ValueError):
                v.include_reader_inputs(pins, root, {'inputs': {'reader-invented.json': a.pin(child)}}, a)

    def test_exclusive_output(self):
        with tempfile.TemporaryDirectory(prefix='f7-v2-binding-test-') as directory:
            path = Path(directory) / 'invented.json'
            v.save(path, b'{"synthetic":true}\n')
            with self.assertRaises(FileExistsError):
                v.save(path, b'changed')
            self.assertEqual(path.read_bytes(), b'{"synthetic":true}\n')


if __name__ == '__main__':
    unittest.main()

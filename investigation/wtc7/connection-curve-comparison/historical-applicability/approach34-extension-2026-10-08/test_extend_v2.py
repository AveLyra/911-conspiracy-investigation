"""Synthetic dependency-wrapper tests; no historical curves selected."""
import copy
from pathlib import Path
import tempfile
import unittest
import extend_v2 as v


class Controls(unittest.TestCase):
    def test_relative_path_normalization(self):
        with tempfile.TemporaryDirectory(prefix='extension-pin-test-') as folder:
            root=Path(folder).resolve(); parent=root/'sub'; parent.mkdir()
            file=root/'input'; file.write_bytes(b'fixture')
            e=v.producer(); expected=e.pin(file); pins={}
            v.merge(pins,root,parent,{'../input':expected},e.pin)
            self.assertEqual(pins,{'input':expected})
            v.merge(pins,root,root,{'input':expected},e.pin)
            self.assertEqual(len(pins),1)

    def test_changed_and_conflicting_dependencies_rejected(self):
        with tempfile.TemporaryDirectory(prefix='extension-pin-test-') as folder:
            root=Path(folder).resolve(); file=root/'input'; file.write_bytes(b'fixture')
            e=v.producer(); correct=e.pin(file); bad=copy.deepcopy(correct); bad['bytes']+=1
            with self.assertRaises(ValueError): v.merge({},root,root,{'input':bad},e.pin)
            with self.assertRaises(ValueError): v.merge({'input':bad},root,root,{'input':correct},e.pin)

    def test_unknown_map_and_outside_root_rejected(self):
        with tempfile.TemporaryDirectory(prefix='extension-pin-test-') as folder:
            root=Path(folder).resolve(); e=v.producer()
            for value in ([], {'input':{'sha256':'invalid'}}, {'input':'invalid'}):
                with self.assertRaises(ValueError): v.merge({},root,root,value,e.pin)
            with self.assertRaises(ValueError):
                v.merge({},root,root,{'../outside':{'sha256':'x','bytes':1}},e.pin)

    def test_exclusive_save(self):
        with tempfile.TemporaryDirectory(prefix='extension-pin-test-') as folder:
            path=Path(folder)/'saved'; e=v.producer(); e.save(path,b'fixture')
            with self.assertRaises(FileExistsError): e.save(path,b'replaced')
            self.assertEqual(path.read_bytes(),b'fixture')


if __name__=='__main__': unittest.main()

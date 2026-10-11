"""Synthetic wrapper admission tests; never read historical sources."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import run as r
from test_collect_dv import avi, listing, chunk
from test_dif_metadata import fixture
from storage import decode_chunk


class WrapperTests(unittest.TestCase):
    def test_invalid_clip(self):
        for clip in (0,9,True,'1',None):
            with self.subTest(clip=clip),self.assertRaises(ValueError):
                r.run_clip(clip,Path('unused'))

    def exercise(self, post_change=False, parent_error=False, bad_artifact=False):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); dest=root/'clip1'; source=root/'inputs.json'
            source.write_text(json.dumps({'items':[{'saved_video':{'nb_frames':'1'}}]}))
            original=r.parent.compress_metadata; argv=sys.argv
            def fake_parent():
                dest.mkdir()
                (dest/'partial').write_bytes(b'synthetic')
                if parent_error:raise ValueError('changed source after writes')
                print(json.dumps({'clip':1,'before_after_pins_match':True,'result':{'frames':1,'metadata':{}}}))
            checks=[{'sha256':'same'},{'sha256':'changed' if post_change else 'same'}]
            with patch.object(r,'check_controls',side_effect=checks),patch.object(r.parent,'INPUT',source),patch.object(r.parent,'main',side_effect=fake_parent),patch.object(r,'verify_chunks',side_effect=ValueError('corrupt artifact') if bad_artifact else None):
                if parent_error or post_change or bad_artifact:
                    with self.assertRaises(ValueError):r.run_clip(1,dest)
                    self.assertTrue((dest/'partial').exists())
                    self.assertFalse((root/'clip1-result.json').exists())
                else:
                    output=r.run_clip(1,dest)
                    self.assertTrue(json.loads(output.read_text())['artifact_readback_verified'])
            self.assertIs(r.parent.compress_metadata,original)
            self.assertIs(sys.argv,argv)

    def test_refuses_source_change_without_accepted_manifest(self):self.exercise(parent_error=True)
    def test_refuses_control_change_without_accepted_manifest(self):self.exercise(post_change=True)
    def test_refuses_corrupt_artifact_without_accepted_manifest(self):self.exercise(bad_artifact=True)
    def test_accepts_only_after_parent_and_output_checks(self):self.exercise()

    def test_symlink_results_root_refused(self):
        with tempfile.TemporaryDirectory() as d:
            unit=Path(d)/'unit'; unit.mkdir(); elsewhere=Path(d)/'other';elsewhere.mkdir()
            (unit/'results').symlink_to(elsewhere,target_is_directory=True)
            with patch.object(r,'UNIT',unit),self.assertRaises(ValueError):r.safe_results_root()

    def test_existing_destination_or_result_refused_before_controls(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve()
            for name in ('directory','result'):
                dest=root/name
                final=root/(name+'-result.json')
                if name=='directory':dest.mkdir()
                else:final.write_text('preserve synthetic sentinel')
                with patch.object(r,'check_controls') as controls,self.assertRaises(ValueError):
                    r.run_clip(1,dest)
                controls.assert_not_called()
            self.assertEqual((root/'result-result.json').read_text(),'preserve synthetic sentinel')

    def test_actual_collector_storage_and_wrapper_roundtrip(self):
        # Synthetic AVI only; exercise real extraction, chunk writing, reopening,
        # wrapper post-checks and JSON publication together. Historical input and
        # dependency guards remain separate from this integration fixture.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve(); dest=root/'clip1'; source=root/'inputs.json'
            frames=101
            source.write_text(json.dumps({'items':[{'saved_video':{'nb_frames':str(frames)}}]}))
            frame,slots,allowed=fixture()
            offset=slots[0][-1]
            frame[offset:offset+5]=b'\x13\x01\x02\x03\x04'
            movie=root/'synthetic.avi'
            movie.write_bytes(avi(listing(b'movi',*(chunk(b'00dc',bytes(frame)) for _ in range(frames)))))
            def synthetic_parent():
                collected=r.parent.collect(movie,frames)
                print(json.dumps({'clip':1,'before_after_pins_match':True,'result':collected}))
            original=r.parent.compress_metadata; argv=sys.argv
            with patch.object(r,'check_controls',return_value={'sha256':'synthetic'}),patch.object(r.parent,'INPUT',source),patch.object(r.parent,'main',side_effect=synthetic_parent):
                output=r.run_clip(1,dest)
            result=json.loads(output.read_text())
            metadata=result['result']['metadata']
            self.assertEqual([c['frames'] for c in metadata['chunks']],[100,1])
            actual=b''.join(decode_chunk((dest/c['path']).read_bytes(),c['raw_bytes']) for c in metadata['chunks'])
            self.assertEqual(actual,b''.join(frame[a:b] for a,b in allowed)*frames)
            self.assertEqual(result['result']['target_variants'][0]['frames_present'],frames)
            self.assertTrue(result['artifact_readback_verified'])
            self.assertIs(r.parent.compress_metadata,original)
            self.assertIs(sys.argv,argv)


if __name__=='__main__':unittest.main()

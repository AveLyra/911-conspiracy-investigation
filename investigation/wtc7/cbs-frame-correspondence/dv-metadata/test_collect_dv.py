"""Synthetic RIFF and collector controls; no historical sources."""
import base64
from io import BytesIO
from pathlib import Path
import struct
import unittest
from unittest.mock import patch
import zlib

import collect_dv as c
from test_dif_metadata import fixture


def chunk(kind, data):
    return kind+struct.pack('<I',len(data))+data+(b'\0' if len(data)%2 else b'')


def listing(kind, *children):
    return chunk(b'LIST',kind+b''.join(children))


def avi(*children):
    return chunk(b'RIFF',b'AVI '+b''.join(children))


class CollectorTests(unittest.TestCase):
    def test_direct_movie_and_byte_offsets(self):
        raw=avi(listing(b'movi',chunk(b'00dc',bytes(120000)),chunk(b'01wb',b'abc')))
        frames,n=c.movie_chunks(BytesIO(raw),len(raw))
        self.assertEqual(frames,[[32,120000]])
        self.assertEqual(n,4)

    def test_record_list_and_nonmovie_signature_bait(self):
        raw=avi(chunk(b'JUNK',chunk(b'00dc',b'bad')),listing(b'movi',listing(b'rec ',chunk(b'00db',bytes(120000)))))
        frames,n=c.movie_chunks(BytesIO(raw),len(raw))
        self.assertEqual(len(frames),1)
        self.assertEqual(n,5)

    def test_rejects_truncated_payload_and_unread_picture_tail(self):
        raw=avi(listing(b'movi',chunk(b'00dc',bytes(120000))))
        with self.assertRaises(ValueError):c.movie_chunks(BytesIO(raw[:-1]),len(raw)-1)

    def test_rejects_truncated_actual_read(self):
        with self.assertRaises(ValueError):c.movie_chunks(BytesIO(b'RIFF'),12)

    def test_rejects_short_header(self):
        raw=avi(b'abcd')
        with self.assertRaises(ValueError):c.movie_chunks(BytesIO(raw),len(raw))

    def test_rejects_unsupported_video_size_or_stream(self):
        for item in [chunk(b'00dc',b'bad'),chunk(b'01dc',bytes(120000))]:
            raw=avi(listing(b'movi',item))
            with self.subTest(item=item[:8]),self.assertRaises(ValueError):c.movie_chunks(BytesIO(raw),len(raw))

    def test_rejects_unexpected_hierarchies(self):
        video=chunk(b'00dc',bytes(120000))
        for children in [video,listing(b'hdrl',listing(b'movi',video)),listing(b'movi',listing(b'JUNK',video)),listing(b'movi',listing(b'rec ',listing(b'rec ',video)))]:
            raw=avi(children)
            with self.subTest(prefix=raw[:24]),self.assertRaises(ValueError):c.movie_chunks(BytesIO(raw),len(raw))

    def test_rejects_wrong_riff_or_missing_container_type(self):
        for raw in [chunk(b'RIFF',b'WAVE'),avi(chunk(b'LIST',b'abc')),b'NOPE'+bytes(8)]:
            with self.subTest(raw=raw),self.assertRaises(ValueError):c.movie_chunks(BytesIO(raw),len(raw))

    def test_chunk_and_depth_limits(self):
        raw=avi(listing(b'movi',chunk(b'00dc',bytes(120000))))
        with self.assertRaisesRegex(ValueError,'chunk limit'):c.movie_chunks(BytesIO(raw),len(raw),max_chunks=1)
        with self.assertRaisesRegex(ValueError,'depth limit'):c.movie_chunks(BytesIO(raw),len(raw),max_depth=0)

    def test_lossless_storage(self):
        data=bytes(range(256))*40
        r=c.compress_metadata(data)
        self.assertEqual(zlib.decompress(base64.b64decode(r['data'])),data)
        self.assertEqual(r['bytes'],len(data))

    def test_storage_limit_is_compressed_bytes(self):
        with patch.object(c.zlib,'compress',return_value=bytes(1024*1024+1)):
            with self.assertRaisesRegex(ValueError,'compressed metadata limit'):c.compress_metadata(b'x')

    def test_roundtrip_failure(self):
        with patch.object(c.zlib,'decompress',return_value=b'wrong'):
            with self.assertRaisesRegex(ValueError,'round-trip'):c.compress_metadata(b'x')

    def test_count_reconciliation_precedes_metadata_read(self):
        raw=avi(listing(b'movi',chunk(b'00dc',bytes(120000))))
        with patch.object(Path,'open',return_value=BytesIO(raw)),patch.object(Path,'stat') as stat,patch.object(c,'extract_frame') as extractor:
            stat.return_value.st_size=len(raw)
            with self.assertRaisesRegex(ValueError,'frame count'):c.collect(Path('synthetic'),2)
            extractor.assert_not_called()

    def test_full_collector_metadata_roundtrip_and_conflicting_raw_candidates(self):
        frame,slots,allowed=fixture()
        first=slots[0][-1];second=slots[1][-1]
        frame[first:first+5]=b'\x13\x00\x00\x00\x00'
        frame[second:second+5]=b'\x13\x01\x00\x00\x00'
        raw=avi(listing(b'movi',chunk(b'00dc',bytes(frame)),chunk(b'00dc',bytes(frame))))
        with patch.object(Path,'open',return_value=BytesIO(raw)),patch.object(Path,'stat') as stat:
            stat.return_value.st_size=len(raw)
            r=c.collect(Path('synthetic'),2)
        expected=b''.join(frame[a:b] for a,b in allowed)*2
        self.assertEqual(zlib.decompress(base64.b64decode(r['metadata']['data'])),expected)
        self.assertEqual(r['frames'],2)
        self.assertEqual(sum(sum(s.values()) for s in r['pack_type_counts'].values()),1320)
        self.assertEqual(len(r['target_variants']),2)
        for v in r['target_variants']:
            self.assertEqual([v[k] for k in ('occurrences','frames_present','first_frame','last_frame')],[2,2,0,1])
            self.assertNotIn('valid_clock',v)
            self.assertNotIn('authenticated_camera_time',v)

    def test_empty_missing_and_extra_freeze_dependencies_refused_before_pin(self):
        for names in [set(),c.REQUIRED-{'dif_metadata.py'},c.REQUIRED-{'../sibling-lineage/inputs.json'},c.REQUIRED|{'unexpected'}]:
            with self.subTest(names=names),patch.object(c,'pin') as p:
                with self.assertRaisesRegex(ValueError,'dependency set'):c.verify_freeze({'files':{n:{} for n in names}})
                p.assert_not_called()

    def test_every_required_dependency_checked_and_changes_refused(self):
        expected={'bytes':1,'sha256':'synthetic'}
        freeze={'files':{n:expected for n in c.REQUIRED}}
        with patch.object(c,'pin',return_value=expected) as p:
            c.verify_freeze(freeze)
            self.assertEqual(p.call_count,len(c.REQUIRED))
        with patch.object(c,'pin',return_value={'bytes':0}):
            with self.assertRaisesRegex(ValueError,'changed frozen dependency'):c.verify_freeze(freeze)


if __name__=='__main__':unittest.main()

import struct
import unittest
import zlib
from audit_swf import abc_strings, parse


def tag(code, payload=b"", long=False):
    if long or len(payload) >= 63:
        return struct.pack("<HI", code << 6 | 63, len(payload)) + payload
    return struct.pack("<H", code << 6 | len(payload)) + payload


def swf(items, compressed=False, declared_delta=0):
    body = b"\x08\x00" + struct.pack("<HH", 12 * 256, 1) + items
    header = (b"CWS" if compressed else b"FWS") + b"\x09" + struct.pack("<I", len(body) + 8 + declared_delta)
    return header + (zlib.compress(body) if compressed else body)


class Controls(unittest.TestCase):
    def test_plain_header(self):
        r = parse(swf(tag(1) + tag(0)))
        self.assertEqual(r["rect_twips"], [0, 0, 0, 0])
        self.assertEqual((r["frame_rate"], r["declared_root_frames"]), (12, 1))
        self.assertEqual(r["root_counts"], {"End": 1, "ShowFrame": 1})

    def test_compressed(self):
        r = parse(swf(tag(1) + tag(0), compressed=True))
        self.assertTrue(r["declared_length_matches"])

    def test_nested_video_frame(self):
        nested = struct.pack("<HH", 17, 1) + tag(61, b"payload") + tag(1) + tag(0)
        r = parse(swf(tag(39, nested) + tag(1) + tag(0)))
        self.assertNotIn("VideoFrame", r["root_counts"])
        self.assertEqual(r["recursive_counts"]["VideoFrame"], 1)
        self.assertEqual(r["tags"][0]["children"][0]["ancestry_sprite_ids"], [17])

    def test_video_definition(self):
        p = struct.pack("<HHHHBB", 7, 9, 320, 200, 0, 2)
        r = parse(swf(tag(60, p, long=True) + tag(0)))
        self.assertEqual(r["tags"][0]["video_declaration"]["width"], 320)

    def test_length_conflict_is_retained(self):
        self.assertFalse(parse(swf(tag(0), declared_delta=1))["declared_length_matches"])

    def test_bad_tag_length(self):
        with self.assertRaises(ValueError):
            parse(swf(struct.pack("<H", 1 << 6 | 20)))

    def test_no_end(self):
        with self.assertRaises(ValueError):
            parse(swf(tag(1)))

    def test_truncated_compression(self):
        with self.assertRaises(ValueError):
            parse(swf(tag(0), compressed=True)[:-1])

    def test_abc_strings(self):
        p = struct.pack("<HH", 16, 46) + b"\x01\x01\x01\x03\x05a.flv\x04seek"
        r = abc_strings(p)
        self.assertEqual(r["media_strings"], ["a.flv"])
        self.assertEqual(r["control_names_present"], ["seek"])

    def test_bad_abc_string(self):
        p = struct.pack("<HH", 16, 46) + b"\x01\x01\x01\x02\x08x"
        with self.assertRaises(ValueError):
            abc_strings(p)


if __name__ == "__main__":
    unittest.main()

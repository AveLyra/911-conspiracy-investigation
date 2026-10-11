"""Synthetic-only checks: no historical media or external codec invocation."""

import hashlib
import unittest
from collections import Counter

from dif_metadata import DIFError, extract_frame, iterate_packs


def fixture():
    """Construct a fixed synthetic frame independently in DIF file order."""
    blocks = []
    slots = []
    allowed = []
    for sequence in range(10):
        def append(section, number, take, area=None, positions=()):
            block = len(blocks) % 150
            offset = len(blocks) * 80
            # Bait in excluded bytes: valid-looking timecode/date pack signatures.
            data = bytearray((b"\x13\x62\x63\x52\x53" * 16))
            data[:3] = bytes(((section << 5) | 0x1f,
                              (sequence << 4) | 7, number))
            if take == 80:
                data[3:] = b"\xff" * 77
            if section == 0:
                data[3] = 0x3f  # DSF=0; uninterpreted low header bits preserved.
            if section == 1:
                for slot in range(6):
                    # Preserve arbitrary SSYB IDs, including repeated 0..5.
                    start = 3 + slot * 8
                    data[start:start + 3] = bytes((0x8f, 0xf0 | slot, 0xff))
            for slot, position in enumerate(positions):
                data[position:position + 5] = b"\xff" * 5
                slots.append((area, sequence, number, block, slot,
                              offset + position))
            blocks.append(bytes(data))
            allowed.append((offset, offset + take))
        append(0, 0, 80)
        for sub in range(2):
            append(1, sub, 80, "subcode", (6, 14, 22, 30, 38, 46))
        for vaux in range(3):
            append(2, vaux, 80, "vaux", tuple(3 + 5 * n for n in range(15)))
        for audio in range(9):
            append(3, audio, 8, "aaux", (3,))
            for video in range(15):
                append(4, audio * 15 + video, 3)
    return bytearray(b"".join(blocks)), slots, allowed


class GuardedReader:
    def __init__(self, data, allowed, base=0):
        self.data, self.base = data, base
        self.allowed = bytearray(len(data))
        for start, end in allowed:
            self.allowed[start:end] = b"\x01" * (end - start)
        self.calls = []

    def __call__(self, offset, size):
        start = offset - self.base
        if start < 0 or start + size > len(self.data):
            raise OSError("outside synthetic source")
        if not all(self.allowed[start:start + size]):
            raise AssertionError("attempt to read excluded audio/picture bytes")
        self.calls.append((offset, size))
        return self.data[start:start + size]


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.frame, self.slots, self.allowed = fixture()

    def run_frame(self, frame=None, base=0):
        reader = GuardedReader(self.frame if frame is None else frame,
                               self.allowed, base)
        packed, record = extract_frame(reader, base)
        return packed, record, reader

    def test_layout_count_order_and_direct_roundtrip(self):
        packed, record, reader = self.run_frame(base=417)
        expected = b"".join(self.frame[start:end] for start, end in self.allowed)
        self.assertEqual(packed, expected)
        self.assertEqual(len(packed), 9570)
        self.assertEqual(record["retained_sha256"], hashlib.sha256(expected).hexdigest())
        self.assertEqual(record["frame_offset"], 417)
        self.assertEqual(record["dif_blocks_validated"], 1500)
        self.assertEqual(record["read_calls"], 1450)
        self.assertEqual(record["bytes_read"], sum(n for _, n in reader.calls))
        self.assertEqual(record["bytes_read"], 9570)
        packs = list(iterate_packs(packed))
        self.assertEqual(len(packs), 660)
        self.assertEqual(Counter(p["area"] for p in packs),
                         {"subcode": 120, "vaux": 450, "aaux": 90})
        for p, expected_slot in zip(packs, self.slots):
            keys = ("area", "sequence", "block", "dif_block", "slot",
                    "relative_file_offset")
            self.assertEqual(tuple(p[k] for k in keys), expected_slot)
            off = p["relative_file_offset"]
            self.assertEqual(p["raw"], self.frame[off:off + 5])
            self.assertEqual(p["raw"], packed[p["retained_offset"]:p["retained_offset"] + 5])
        self.assertEqual(packs[0]["relative_file_offset"], 86)
        self.assertEqual(packs[-1]["relative_file_offset"], 118723)
        self.assertEqual(sorted(p["relative_file_offset"] for p in packs),
                         [p["relative_file_offset"] for p in packs])

    def test_target_types_in_every_area_and_conflicting_values_preserved(self):
        types = (0x13, 0x62, 0x63, 0x52, 0x53)
        for i, (_, _, _, _, _, offset) in enumerate(self.slots):
            self.frame[offset:offset + 5] = bytes((types[i % 5], i % 256,
                                                 (i // 256) % 256, 0xff, 0x91))
        packed, _, _ = self.run_frame()
        packs = list(iterate_packs(packed))
        for area in ("subcode", "vaux", "aaux"):
            self.assertEqual({p["raw"][0] for p in packs if p["area"] == area}, set(types))
        self.assertEqual(len({p["raw"] for p in packs}), 660)
        self.assertEqual(len(packs), len(self.slots))

    def test_all_ff_packs_and_excluded_signature_bait(self):
        packed, _, reader = self.run_frame()
        self.assertEqual({p["raw"] for p in iterate_packs(packed)}, {b"\xff" * 5})
        self.assertEqual(sum(n for _, n in reader.calls), 9570)

    def test_unknown_and_partially_available_packs_are_lossless(self):
        values = [b"\x87\x00\x00\x00\x00", b"\x63\xff\x24\xff\x10",
                  b"\x52\xff\xff\xff\xff"]
        for row, value in zip(self.slots, values):
            self.frame[row[-1]:row[-1] + 5] = value
        packed, _, _ = self.run_frame()
        self.assertEqual([p["raw"] for p in list(iterate_packs(packed))[:3]], values)

    def test_ssyb_ids_preserved_not_rejected(self):
        for seq in range(10):
            for block in (1, 2):
                for slot in range(6):
                    offset = seq * 12000 + block * 80 + 3 + slot * 8
                    self.frame[offset:offset + 3] = bytes((seq, 255 - slot, block))
        packed, _, _ = self.run_frame()
        self.assertEqual(packed, b"".join(self.frame[a:b] for a, b in self.allowed))

    def test_reserved_bits_and_fsp_are_preserved_not_interpreted(self):
        for start, _ in self.allowed:
            self.frame[start] &= 0xe0
            self.frame[start + 1] &= 0xf0
        packed, _, _ = self.run_frame()
        self.assertEqual(packed, b"".join(self.frame[a:b] for a, b in self.allowed))

    def test_wrong_section_across_all_block_classes(self):
        for block in (0, 1, 2, 3, 5, 6, 7, 134, 149):
            with self.subTest(block=block):
                damaged = self.frame.copy()
                damaged[9 * 12000 + block * 80] ^= 0x20
                with self.assertRaisesRegex(DIFError, "wrong section"):
                    self.run_frame(damaged)

    def test_wrong_sequence_at_each_sequence_end(self):
        for seq in range(10):
            with self.subTest(seq=seq):
                damaged = self.frame.copy()
                damaged[seq * 12000 + 149 * 80 + 1] ^= 0x10
                with self.assertRaisesRegex(DIFError, "wrong sequence"):
                    self.run_frame(damaged)

    def test_wrong_block_number_across_all_classes(self):
        for block in (0, 1, 2, 3, 5, 6, 7, 134, 149):
            with self.subTest(block=block):
                damaged = self.frame.copy()
                damaged[block * 80 + 2] ^= 0x01
                with self.assertRaisesRegex(DIFError, "wrong block"):
                    self.run_frame(damaged)

    def test_each_of_1500_retained_block_ids_is_checked_before_yield(self):
        packed, _, _ = self.run_frame()
        cursor = 0
        for start, end in self.allowed:
            with self.subTest(file_offset=start):
                damaged = bytearray(packed)
                damaged[cursor + 2] ^= 1
                with self.assertRaisesRegex(DIFError, "wrong block"):
                    next(iterate_packs(bytes(damaged)))
            cursor += end - start
        self.assertEqual(cursor, 9570)

    def test_wrong_fsc_channel_across_all_classes(self):
        for block in (0, 1, 3, 6, 149):
            with self.subTest(block=block):
                damaged = self.frame.copy()
                damaged[9 * 12000 + block * 80 + 1] |= 0x08
                with self.assertRaisesRegex(DIFError, "FSC"):
                    self.run_frame(damaged)

    def test_wrong_dsf_in_every_sequence_header(self):
        for seq in range(10):
            with self.subTest(seq=seq):
                damaged = self.frame.copy()
                damaged[seq * 12000 + 3] |= 0x80
                with self.assertRaisesRegex(DIFError, "DSF"):
                    self.run_frame(damaged)

    def test_shifted_frame_refused_without_resynchronization(self):
        shifted = b"\xff" + bytes(self.frame)
        with self.assertRaises(DIFError):
            extract_frame(lambda o, n: shifted[o:o + n], 0)

    def test_truncated_required_regions(self):
        for length in (0, 479, 12000, 119922):
            with self.subTest(length=length):
                cut = self.frame[:length]
                with self.assertRaisesRegex(DIFError, "read length"):
                    extract_frame(lambda o, n: cut[o:o + n], 0)

    def test_unread_tail_extent_is_callers_responsibility(self):
        # The last read is the final video ID at 119920..119922, not picture data.
        cut = self.frame[:119923]
        packed, _ = extract_frame(lambda o, n: cut[o:o + n], 0)
        self.assertEqual(len(packed), 9570)
        self.assertLess(len(cut), 120000)

    def test_short_and_oversized_reads_refused(self):
        for change in (-1, 1):
            with self.subTest(change=change):
                with self.assertRaisesRegex(DIFError, "read length"):
                    extract_frame(lambda o, n: bytes(n + change), 0)

    def test_reader_exception_preserved_as_cause(self):
        def broken(offset, length):
            raise OSError("synthetic read failure")
        with self.assertRaisesRegex(DIFError, "read failed") as caught:
            extract_frame(broken, 0)
        self.assertIsInstance(caught.exception.__cause__, OSError)

    def test_wrong_reader_value_refused(self):
        for value in (None, "bytes", 480):
            with self.subTest(value=value):
                with self.assertRaisesRegex(DIFError, "non-byte"):
                    extract_frame(lambda o, n: value, 0)

    def test_wrong_frame_size_and_offset_refused_before_reads(self):
        def never(offset, length):
            self.fail("must refuse arguments before reading")
        for size in (0, -1, 119999, 120001, 144000, True, 120000.0):
            with self.subTest(size=size):
                with self.assertRaises(DIFError):
                    extract_frame(never, 0, size)
        for offset in (-1, 0.0, True, None):
            with self.subTest(offset=offset):
                with self.assertRaises(DIFError):
                    extract_frame(never, offset)
        with self.assertRaises(DIFError):
            extract_frame(None, 0)

    def test_pack_iteration_refuses_bad_retention_before_first_yield(self):
        for value in (b"", bytes(9569), bytes(9571), "x" * 9570):
            with self.subTest(length=len(value)):
                with self.assertRaises(DIFError):
                    next(iterate_packs(value))
        packed, _, _ = self.run_frame()
        invalid = packed[:-1] + b"\x00"  # Corrupt final video block ID.
        with self.assertRaisesRegex(DIFError, "wrong block"):
            next(iterate_packs(invalid))


if __name__ == "__main__":
    unittest.main()

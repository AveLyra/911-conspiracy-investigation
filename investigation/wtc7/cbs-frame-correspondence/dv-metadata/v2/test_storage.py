"""Synthetic temporary artifact tests; no case-media access."""

import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zlib

import storage


def data(frames):
    frame = bytes((n * 37 + 17) % 256 for n in range(9570))
    return frame * frames


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="dv-storage-test-")
        self.addCleanup(self.temporary.cleanup)
        # Temporary ancestors may have platform aliases; give the API the actual
        # synthetic directory, then explicitly test refusal of introduced links.
        self.root = Path(self.temporary.name).resolve()

    def write(self, frames=1, name="clip"):
        original = data(frames)
        directory = self.root / name
        manifest = storage.write_chunks(original, frames, directory)
        return original, directory, manifest

    def fixture_copy(self, original_directory, manifest, encoded_transform):
        """Create fresh malformed fixtures exclusively; never alter a prior file."""
        destination = self.root / "malformed"
        destination.mkdir()
        altered = copy.deepcopy(manifest)
        altered["encoded_bytes"] = 0
        for chunk in altered["chunks"]:
            encoded = (original_directory / chunk["path"]).read_bytes()
            encoded = encoded_transform(encoded)
            with (destination / chunk["path"]).open("xb") as stream:
                stream.write(encoded)
            # Update encoded pins so verification reaches strict zlib handling.
            chunk["encoded_bytes"] = len(encoded)
            chunk["encoded_sha256"] = hashlib.sha256(encoded).hexdigest()
            altered["encoded_bytes"] += len(encoded)
        return destination, altered

    def test_roundtrip_boundaries_1_99_100_101_and_2500(self):
        for frames in (1, 99, 100, 101, 2500):
            with self.subTest(frames=frames):
                original, directory, manifest = self.write(frames, str(frames))
                json.dumps(manifest)
                self.assertEqual(len(manifest["chunks"]), (frames + 99) // 100)
                self.assertTrue(manifest["readback"]["compared_to_original_input"])
                self.assertEqual(manifest["raw_bytes"], len(original))
                self.assertEqual(manifest["raw_sha256"], hashlib.sha256(original).hexdigest())
                reconstructed = b"".join(zlib.decompress((directory / c["path"]).read_bytes())
                                         for c in manifest["chunks"])
                self.assertEqual(reconstructed, original)
                self.assertEqual(set(os.listdir(directory)),
                                 {c["path"] for c in manifest["chunks"]})
                verified = storage.verify_chunks(directory, manifest)
                self.assertFalse(verified["compared_to_original_input"])
                self.assertEqual(verified["raw_sha256"], manifest["raw_sha256"])
                for i, c in enumerate(manifest["chunks"]):
                    self.assertEqual(c["path"], f"chunk{i:03d}.zlib")
                    self.assertEqual(c["first_frame"], i * 100)
                    self.assertEqual(c["stop_frame"], min((i + 1) * 100, frames))
                    self.assertLessEqual(c["encoded_bytes"], 1024 * 1024)

    def test_bad_declared_counts_refused_without_directory(self):
        for frames in (0, -1, 2501, True, False, 1.0, None, "1"):
            with self.subTest(frames=frames):
                destination = self.root / "bad"
                with self.assertRaises(storage.StorageError):
                    storage.write_chunks(data(1), frames, destination)
                self.assertFalse(destination.exists())

    def test_bad_raw_types_lengths_and_count_mismatch(self):
        for raw in (None, True, 9570, "x" * 9570, b"", data(1)[:-1],
                    data(1) + b"x", data(2)):
            with self.subTest(kind=type(raw).__name__):
                destination = self.root / "bad"
                with self.assertRaises(storage.StorageError):
                    storage.write_chunks(raw, 1, destination)
                self.assertFalse(destination.exists())

    def test_existing_directory_and_file_unchanged(self):
        directory = self.root / "directory"
        directory.mkdir()
        file = self.root / "file"
        with file.open("xb") as stream:
            stream.write(b"original")
        for destination in (directory, file):
            with self.subTest(destination=destination.name):
                with self.assertRaises(storage.StorageError):
                    storage.write_chunks(data(1), 1, destination)
        self.assertEqual(file.read_bytes(), b"original")
        self.assertEqual(list(directory.iterdir()), [])

    def test_symlink_final_and_ancestor_paths_refused(self):
        actual = self.root / "actual"
        actual.mkdir()
        link = self.root / "link"
        link.symlink_to(actual, target_is_directory=True)
        for destination in (link, link / "output"):
            with self.subTest(destination=str(destination)):
                with self.assertRaises(storage.StorageError):
                    storage.write_chunks(data(1), 1, destination)
        self.assertEqual(list(actual.iterdir()), [])

    def test_path_escape_and_relative_path_refused(self):
        for destination in (self.root / ".." / "escape", Path("relative"), Path("/")):
            with self.subTest(destination=str(destination)):
                with self.assertRaises(storage.StorageError):
                    storage.write_chunks(data(1), 1, destination)
        _, directory, manifest = self.write()
        for path in ("../chunk000.zlib", str(directory / "chunk000.zlib"), "x/chunk000.zlib"):
            bad = copy.deepcopy(manifest)
            bad["chunks"][0]["path"] = path
            with self.assertRaises(storage.StorageError):
                storage.verify_chunks(directory, bad)

    def test_gap_overlap_reordered_and_missing_manifest_entries(self):
        _, directory, manifest = self.write(101)
        variants = []
        for first in (99, 101):
            bad = copy.deepcopy(manifest)
            bad["chunks"][1]["first_frame"] = first
            variants.append(bad)
        bad = copy.deepcopy(manifest)
        bad["chunks"].reverse()
        variants.append(bad)
        bad = copy.deepcopy(manifest)
        bad["chunks"].pop()
        variants.append(bad)
        bad = copy.deepcopy(manifest)
        bad["chunks"][0]["stop_frame"] = 99
        variants.append(bad)
        for bad in variants:
            with self.subTest(chunks=bad["chunks"]):
                with self.assertRaises(storage.StorageError):
                    storage.verify_chunks(directory, bad)

    def test_missing_and_unlisted_files_refused(self):
        _, source, manifest = self.write(101)
        missing = self.root / "missing"
        missing.mkdir()
        with (missing / "chunk000.zlib").open("xb") as stream:
            stream.write((source / "chunk000.zlib").read_bytes())
        with self.assertRaisesRegex(storage.StorageError, "missing or unlisted"):
            storage.verify_chunks(missing, manifest)
        with (source / "unexpected").open("xb") as stream:
            stream.write(b"synthetic extra")
        with self.assertRaisesRegex(storage.StorageError, "missing or unlisted"):
            storage.verify_chunks(source, manifest)

    def test_chunk_symlink_and_hardlink_refused(self):
        _, source, manifest = self.write()
        for kind in ("symlink", "hardlink"):
            destination = self.root / kind
            destination.mkdir()
            target = destination / "chunk000.zlib"
            if kind == "symlink":
                target.symlink_to(source / "chunk000.zlib")
            else:
                os.link(source / "chunk000.zlib", target)
            with self.subTest(kind=kind):
                with self.assertRaises(storage.StorageError):
                    storage.verify_chunks(destination, manifest)

    def test_corrupted_compressed_bytes_refused(self):
        _, source, manifest = self.write()
        def corrupt(encoded):
            changed = bytearray(encoded)
            changed[-1] ^= 1
            return bytes(changed)
        destination, altered = self.fixture_copy(source, manifest, corrupt)
        with self.assertRaises(storage.StorageError):
            storage.verify_chunks(destination, altered)

    def test_truncated_stream_refused_even_with_updated_encoded_pin(self):
        _, source, manifest = self.write()
        destination, altered = self.fixture_copy(source, manifest, lambda x: x[:-1])
        with self.assertRaisesRegex(storage.StorageError, "EOF"):
            storage.verify_chunks(destination, altered)

    def test_trailing_data_and_second_zlib_stream_refused(self):
        raw = data(1)
        encoded = zlib.compress(raw)
        for suffix in (b"junk", zlib.compress(b"second")):
            with self.subTest(suffix=suffix):
                with self.assertRaisesRegex(storage.StorageError, "trailing"):
                    storage.decode_chunk(encoded + suffix, len(raw))

    def test_wrong_raw_lengths_and_bounded_decompression(self):
        encoded = zlib.compress(data(1))
        for length in (1, 9569, 9571, -1, True, 957001):
            with self.subTest(length=length):
                with self.assertRaises(storage.StorageError):
                    storage.decode_chunk(encoded, length)

    def test_encoded_and_raw_hash_mismatches_refused(self):
        _, directory, manifest = self.write()
        for key in ("encoded_sha256", "raw_sha256"):
            bad = copy.deepcopy(manifest)
            bad["chunks"][0][key] = "0" * 64
            with self.subTest(key=key):
                with self.assertRaises(storage.StorageError):
                    storage.verify_chunks(directory, bad)
        bad = copy.deepcopy(manifest)
        bad["raw_sha256"] = "0" * 64
        with self.assertRaisesRegex(storage.StorageError, "whole raw hash"):
            storage.verify_chunks(directory, bad)

    def test_boolean_manifest_counts_refused(self):
        _, directory, manifest = self.write()
        for key in ("frames", "raw_bytes", "bytes_per_frame", "encoded_bytes"):
            bad = copy.deepcopy(manifest)
            bad[key] = True
            with self.subTest(key=key):
                with self.assertRaises(storage.StorageError):
                    storage.verify_chunks(directory, bad)
        bad = copy.deepcopy(manifest)
        bad["chunks"][0]["first_frame"] = False
        with self.assertRaises(storage.StorageError):
            storage.verify_chunks(directory, bad)

    def test_per_chunk_cap_refusal_leaves_created_directory(self):
        destination = self.root / "cap"
        with patch("storage.zlib.compress", return_value=b"x" * (1024 * 1024 + 1)):
            with self.assertRaisesRegex(storage.StorageError, "incomplete output retained"):
                storage.write_chunks(data(1), 1, destination)
        self.assertTrue(destination.is_dir())
        self.assertEqual(list(destination.iterdir()), [])

    def test_total_cap_guard_with_synthetic_reduced_limit(self):
        destination = self.root / "total-cap"
        with patch("storage.MAX_TOTAL_ENCODED_BYTES", 1):
            with self.assertRaisesRegex(storage.StorageError, "total encoded cap"):
                storage.write_chunks(data(1), 1, destination)
        self.assertTrue(destination.is_dir())

    def test_failed_second_chunk_preserves_first(self):
        destination = self.root / "partial"
        real_compress = zlib.compress
        calls = 0
        def fail_second(raw, level):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic storage failure")
            return real_compress(raw, level)
        with patch("storage.zlib.compress", side_effect=fail_second):
            with self.assertRaisesRegex(storage.StorageError, "incomplete output retained"):
                storage.write_chunks(data(101), 101, destination)
        self.assertEqual([p.name for p in destination.iterdir()], ["chunk000.zlib"])
        self.assertEqual(zlib.decompress((destination / "chunk000.zlib").read_bytes()), data(100))
        with self.assertRaises(storage.StorageError):
            storage.write_chunks(data(101), 101, destination)

    def test_exclusive_file_creation_preserves_interposed_target(self):
        destination = self.root / "collision"
        real_compress = zlib.compress
        def interpose(raw, level):
            with (destination / "chunk000.zlib").open("xb") as stream:
                stream.write(b"existing artifact")
            return real_compress(raw, level)
        with patch("storage.zlib.compress", side_effect=interpose):
            with self.assertRaisesRegex(storage.StorageError, "incomplete output retained"):
                storage.write_chunks(data(1), 1, destination)
        self.assertEqual((destination / "chunk000.zlib").read_bytes(), b"existing artifact")


if __name__ == "__main__":
    unittest.main()

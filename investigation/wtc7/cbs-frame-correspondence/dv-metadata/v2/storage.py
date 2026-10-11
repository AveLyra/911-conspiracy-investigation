"""Exclusive, bounded storage of already-extracted raw DV metadata bytes.

This module does not open source media, interpret packs, or invoke subprocesses.
The final directory must not exist; its parent must exist. Every path component
is opened without following symlinks. Created directories/files are never removed
or overwritten here, including after failure. POSIX no-follow/dir-fd support is
required. This is not protection against arbitrary concurrent same-user code.
"""

import hashlib
import os
from pathlib import Path
import re
import stat
import zlib


BYTES_PER_FRAME = 9570
FRAMES_PER_CHUNK = 100
MAX_FRAMES = 2500
MAX_CHUNKS = 25
MAX_RAW_BYTES = 23_925_000
MAX_ENCODED_BYTES = 1024 * 1024
MAX_TOTAL_ENCODED_BYTES = 25 * 1024 * 1024
SCHEMA = "dv-metadata-chunk-storage-v1"


class StorageError(ValueError):
    """Refused input or failed storage verification; no cleanup is implied."""


def _require(condition, message):
    if not condition:
        raise StorageError(message)


def _integer(value, low, high, name):
    _require(type(value) is int and low <= value <= high,
             f"invalid {name}")


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _valid_sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value)


def _path(value):
    try:
        path = Path(value)
    except (TypeError, ValueError) as error:
        raise StorageError("invalid output path") from error
    _require(path.is_absolute() and path.anchor == "/" and len(path.parts) > 1,
             "output must be an absolute non-root path")
    _require(".." not in path.parts, "path traversal is not allowed")
    _require(hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_DIRECTORY"),
             "POSIX no-follow directory support is required")
    return path


def _open_directory(path):
    """Walk each absolute directory component using no-follow directory FDs."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    current = os.open("/", flags)
    try:
        for part in path.parts[1:]:
            following = os.open(part, flags, dir_fd=current)
            os.close(current)
            current = following
        return current
    except BaseException:
        os.close(current)
        raise


def decode_chunk(encoded, expected_raw_bytes):
    """Strict one-stream zlib decoding, bounded by a declared raw chunk size."""
    _require(isinstance(encoded, bytes), "encoded chunk must be bytes")
    _integer(expected_raw_bytes, 1, BYTES_PER_FRAME * FRAMES_PER_CHUNK,
             "expected raw chunk length")
    _require(0 < len(encoded) <= MAX_ENCODED_BYTES, "encoded chunk cap")
    try:
        decoder = zlib.decompressobj()
        raw = decoder.decompress(encoded, expected_raw_bytes + 1)
    except zlib.error as error:
        raise StorageError("invalid zlib chunk") from error
    _require(len(raw) == expected_raw_bytes, "decoded length mismatch")
    _require(decoder.eof, "missing zlib EOF")
    _require(not decoder.unused_data and not decoder.unconsumed_tail,
             "trailing or unconsumed compressed data")
    return raw


def _validate_manifest(manifest):
    _require(isinstance(manifest, dict), "manifest must be a mapping")
    _require(manifest.get("schema") == SCHEMA, "unknown storage schema")
    frames = manifest.get("frames")
    _integer(frames, 1, MAX_FRAMES, "frame count")
    for key, expected in (("bytes_per_frame", BYTES_PER_FRAME),
                          ("chunk_frames", FRAMES_PER_CHUNK)):
        _require(type(manifest.get(key)) is int and manifest[key] == expected,
                 f"invalid {key}")
    raw_bytes = manifest.get("raw_bytes")
    _integer(raw_bytes, 1, MAX_RAW_BYTES, "whole raw length")
    _require(raw_bytes == frames * BYTES_PER_FRAME, "whole raw length/count mismatch")
    _require(_valid_sha(manifest.get("raw_sha256")), "invalid whole raw hash")
    chunks = manifest.get("chunks")
    expected_count = (frames + FRAMES_PER_CHUNK - 1) // FRAMES_PER_CHUNK
    _require(isinstance(chunks, list) and len(chunks) == expected_count
             and len(chunks) <= MAX_CHUNKS, "chunk count mismatch")
    total_encoded = 0
    for index, chunk in enumerate(chunks):
        _require(isinstance(chunk, dict), "chunk entry must be a mapping")
        _require(chunk.get("path") == f"chunk{index:03d}.zlib",
                 "noncanonical chunk path/order")
        first = index * FRAMES_PER_CHUNK
        stop = min(first + FRAMES_PER_CHUNK, frames)
        for key, expected in (("first_frame", first), ("stop_frame", stop),
                              ("frames", stop - first),
                              ("raw_bytes", (stop - first) * BYTES_PER_FRAME)):
            _require(type(chunk.get(key)) is int and chunk[key] == expected,
                     f"invalid chunk {index} {key}")
        _integer(chunk.get("encoded_bytes"), 1, MAX_ENCODED_BYTES,
                 "encoded chunk length")
        _require(_valid_sha(chunk.get("raw_sha256"))
                 and _valid_sha(chunk.get("encoded_sha256")), "invalid chunk hash")
        total_encoded += chunk["encoded_bytes"]
    _require(total_encoded <= MAX_TOTAL_ENCODED_BYTES, "total encoded cap")
    _require(type(manifest.get("encoded_bytes")) is int
             and manifest["encoded_bytes"] == total_encoded,
             "whole encoded length mismatch")


def _verify(directory_fd, manifest, original=None):
    _validate_manifest(manifest)
    names = [chunk["path"] for chunk in manifest["chunks"]]
    _require(set(os.listdir(directory_fd)) == set(names),
             "directory contains missing or unlisted artifacts")
    combined = bytearray()
    for chunk in manifest["chunks"]:
        flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
        fd = os.open(chunk["path"], flags, dir_fd=directory_fd)
        with os.fdopen(fd, "rb") as stream:
            info = os.fstat(stream.fileno())
            _require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                     "chunk must be a regular, unlinked file")
            _require(info.st_size == chunk["encoded_bytes"], "stored length mismatch")
            encoded = stream.read(chunk["encoded_bytes"] + 1)
        _require(len(encoded) == chunk["encoded_bytes"], "short or excessive stored read")
        _require(_sha(encoded) == chunk["encoded_sha256"], "stored hash mismatch")
        raw = decode_chunk(encoded, chunk["raw_bytes"])
        _require(_sha(raw) == chunk["raw_sha256"], "raw chunk hash mismatch")
        combined.extend(raw)
    _require(len(combined) == manifest["raw_bytes"], "concatenated length mismatch")
    _require(_sha(combined) == manifest["raw_sha256"], "whole raw hash mismatch")
    if original is not None:
        _require(combined == original, "concatenation differs from original input")
    return {"chunks_verified": len(names), "frames": manifest["frames"],
            "raw_bytes": len(combined), "raw_sha256": _sha(combined),
            "compared_to_original_input": original is not None}


def verify_chunks(directory, manifest):
    """Read generated artifacts and return verification metadata, never raw data."""
    _validate_manifest(manifest)
    path = _path(directory)
    fd = None
    try:
        fd = _open_directory(path)
        return _verify(fd, manifest)
    except OSError as error:
        raise StorageError("could not safely read chunk directory/artifact") from error
    finally:
        if fd is not None:
            os.close(fd)


def write_chunks(data, declared_frames, directory):
    """Exclusively create and verify a new chunk-only directory.

    The parent already exists. A prior file, directory or symlink at the final
    path is refused, even if empty. Failures never overwrite/delete artifacts:
    anything created stays as explicitly incomplete output for the caller to log.
    The returned JSON-compatible manifest is not written into this directory.
    """
    _integer(declared_frames, 1, MAX_FRAMES, "declared frame count")
    _require(isinstance(data, (bytes, bytearray)), "raw metadata must be bytes")
    _require(len(data) == declared_frames * BYTES_PER_FRAME
             and len(data) <= MAX_RAW_BYTES, "raw length/count mismatch")
    original = bytes(data)
    path = _path(directory)
    parent_fd = directory_fd = None
    created = False
    try:
        parent_fd = _open_directory(path.parent)
        os.mkdir(path.name, mode=0o700, dir_fd=parent_fd)
        created = True
        directory_fd = os.open(path.name,
                               os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                               dir_fd=parent_fd)
        manifest = {"schema": SCHEMA, "frames": declared_frames,
                    "bytes_per_frame": BYTES_PER_FRAME,
                    "chunk_frames": FRAMES_PER_CHUNK,
                    "raw_bytes": len(original), "raw_sha256": _sha(original),
                    "encoded_bytes": 0, "chunks": []}
        for index, first in enumerate(range(0, declared_frames, FRAMES_PER_CHUNK)):
            _require(index < MAX_CHUNKS, "chunk count cap")
            stop = min(first + FRAMES_PER_CHUNK, declared_frames)
            raw = original[first * BYTES_PER_FRAME:stop * BYTES_PER_FRAME]
            encoded = zlib.compress(raw, 9)
            _require(0 < len(encoded) <= MAX_ENCODED_BYTES, "encoded chunk cap")
            manifest["encoded_bytes"] += len(encoded)
            _require(manifest["encoded_bytes"] <= MAX_TOTAL_ENCODED_BYTES,
                     "total encoded cap")
            name = f"chunk{index:03d}.zlib"
            fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o600, dir_fd=directory_fd)
            with os.fdopen(fd, "wb") as stream:
                _require(stream.write(encoded) == len(encoded), "short artifact write")
            manifest["chunks"].append({
                "path": name, "first_frame": first, "stop_frame": stop,
                "frames": stop - first, "raw_bytes": len(raw),
                "raw_sha256": _sha(raw), "encoded_bytes": len(encoded),
                "encoded_sha256": _sha(encoded),
            })
        manifest["readback"] = _verify(directory_fd, manifest, original)
        return manifest
    except Exception as error:
        if created:
            raise StorageError(f"incomplete output retained at {path}: {error}") from error
        if isinstance(error, StorageError):
            raise
        raise StorageError("output creation refused; existing paths are never reused") from error
    finally:
        if directory_fd is not None:
            os.close(directory_fd)
        if parent_fd is not None:
            os.close(parent_fd)

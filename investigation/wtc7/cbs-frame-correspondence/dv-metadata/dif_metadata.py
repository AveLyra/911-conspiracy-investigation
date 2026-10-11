"""Lossless control-byte extraction for one fixed 120,000-byte DV DIF layout.

No decoding, signature search, date/time interpretation, or resynchronization.
The caller must establish the full frame extent against the source/container:
bytes deliberately not read here cannot reveal truncation within those bytes.

Retention, in original file order for each of ten sequences:
* six complete 80-byte control blocks;
* nine groups, each retaining eight audio bytes and fifteen 3-byte video IDs.
This yields 957 bytes/sequence, 9,570 bytes/frame. The layout is based on the
pinned FFmpeg n7.1 dv_format_frame/dv_inject_metadata/dv_inject_audio sources.
Matching it does not establish complete DV codec conformance or clock origin.
"""

from hashlib import sha256


FRAME_BYTES = 120_000
SEQUENCE_BYTES = 12_000
RETAINED_BYTES = 9_570


class DIFError(ValueError):
    """A declared-layout, input, or retained-read failure; never a partial pass."""


def _layout():
    """Yield sequence, physical DIF block, section, block ID, offset, length."""
    for sequence in range(10):
        for block in range(150):
            if block == 0:
                section, number, take = 0, 0, 80
            elif block < 3:
                section, number, take = 1, block - 1, 80
            elif block < 6:
                section, number, take = 2, block - 3, 80
            else:
                group, position = divmod(block - 6, 16)
                if position == 0:
                    section, number, take = 3, group, 8
                else:
                    section, number, take = 4, group * 15 + position - 1, 3
            yield (sequence, block, section, number,
                   sequence * SEQUENCE_BYTES + block * 80, take)


def _blocks(retained):
    cursor = 0
    for sequence, block, section, number, offset, take in _layout():
        yield (sequence, block, section, number, offset, cursor,
               retained[cursor:cursor + take])
        cursor += take


def _validate(retained):
    if not isinstance(retained, bytes) or len(retained) != RETAINED_BYTES:
        raise DIFError("retained data must be exactly 9570 bytes")
    for sequence, block, section, number, offset, _, data in _blocks(retained):
        location = f"sequence {sequence}, DIF {block}, frame offset {offset}"
        if data[0] >> 5 != section:
            raise DIFError(f"wrong section at {location}")
        if data[1] >> 4 != sequence:
            raise DIFError(f"wrong sequence ID at {location}")
        if data[1] & 0x08:
            raise DIFError(f"unsupported FSC channel at {location}")
        if data[2] != number:
            raise DIFError(f"wrong block ID at {location}")
        if section == 0 and data[3] & 0x80:
            raise DIFError(f"unsupported DSF profile at {location}")
    # SSYB IDs, FSP, reserved bits and all metadata contents remain raw.


def extract_frame(read_at, frame_offset, frame_size=FRAME_BYTES):
    """Return (retained bytes, JSON-compatible layout/integrity record).

    read_at(absolute_offset, length) must return exactly length bytes. Errors or
    short/oversized reads refuse the entire result. This function only reads
    retained control bytes. The caller, not this API, checks the physical extent
    of skipped picture/audio bytes and the containing RIFF chunk boundaries.
    """
    if type(frame_size) is not int or frame_size != FRAME_BYTES:
        raise DIFError("only an exactly 120000-byte frame is supported")
    if type(frame_offset) is not int or frame_offset < 0:
        raise DIFError("frame_offset must be a nonnegative integer")
    if not callable(read_at):
        raise DIFError("read_at must be callable")

    pieces = []
    calls = 0

    def read(relative, length):
        nonlocal calls
        absolute = frame_offset + relative
        calls += 1
        try:
            data = read_at(absolute, length)
        except Exception as error:
            raise DIFError(f"read failed at absolute offset {absolute}") from error
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise DIFError(f"non-byte read at absolute offset {absolute}")
        data = bytes(data)
        if len(data) != length:
            raise DIFError(f"read length {len(data)} != {length} at {absolute}")
        return data

    for sequence in range(10):
        start = sequence * SEQUENCE_BYTES
        pieces.append(read(start, 480))
        for group in range(9):
            audio = start + (6 + group * 16) * 80
            pieces.append(read(audio, 8))
            for video in range(15):
                pieces.append(read(audio + (video + 1) * 80, 3))
    retained = b"".join(pieces)
    _validate(retained)
    return retained, {
        "schema": "dv-dif-metadata-retained-v1",
        "frame_offset": frame_offset,
        "declared_frame_bytes": frame_size,
        "retained_bytes": len(retained),
        "retained_sha256": sha256(retained).hexdigest(),
        "sequences": 10,
        "dif_blocks_validated": 1500,
        "read_calls": calls,
        "bytes_read": len(retained),
        "pack_slots": {"subcode": 120, "vaux": 450, "aaux": 90},
        "profile_checks": {"DSF": 0, "FSC": 0},
        "scope": "fixed layout only; caller validates complete source extent",
    }


def iterate_packs(retained):
    """Yield every five-byte slot, including empty, unknown and contradictory.

    ``block`` is the section-specific DIF block number (subcode 0..1, VAUX
    0..2, AAUX/audio 0..8); ``dif_block`` is its physical 0..149 sequence index.
    ``slot`` starts at zero within that block. ``relative_file_offset`` starts
    at the frame, not the file; add the caller's frame_offset for file position.
    ``raw`` is five bytes without interpretation. Full retained bytes additionally
    preserve SSYB IDs, other control contents, padding, and every video DIF ID.
    Validate all retained IDs before yielding even the first pack.
    """
    _validate(retained)
    for sequence, block, section, number, offset, cursor, data in _blocks(retained):
        if section == 1:
            area, positions = "subcode", range(6, 47, 8)
        elif section == 2:
            area, positions = "vaux", range(3, 74, 5)
        elif section == 3:
            area, positions = "aaux", (3,)
        else:
            continue
        for slot, position in enumerate(positions):
            yield {
                "area": area,
                "sequence": sequence,
                "block": number,
                "dif_block": block,
                "slot": slot,
                "relative_file_offset": offset + position,
                "retained_offset": cursor + position,
                "raw": data[position:position + 5],
            }

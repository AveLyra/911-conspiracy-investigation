"""Static SWF DefineFont2/DefineText extraction; never execute ActionScript.

Usage: python3 extract_swf_text.py INPUT.swf OUTPUT.json
References: Adobe SWF file format specification, DefineFont2, DefineText,
TEXTRECORD and GLYPHENTRY. Offsets are zero-based uncompressed SWF bytes.
This extracts text definitions, not proof that a particular screen was shown.
"""
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib


class Bits:
    def __init__(self, data, byte=0):
        self.data, self.bit = data, byte * 8

    def take(self, count, signed=False):
        assert self.bit + count <= len(self.data) * 8
        value = 0
        for _ in range(count):
            value = value * 2 + ((self.data[self.bit // 8] >> (7-self.bit % 8)) & 1)
            self.bit += 1
        return value - (1 << count) if signed and count and value & (1 << (count-1)) else value

    def align(self):
        self.bit = (self.bit + 7) // 8 * 8
        return self.bit // 8

    def rect(self):
        width = self.take(5)
        values = [self.take(width, True) for _ in range(4)]
        self.align()
        return values

    def matrix(self):
        for _ in range(2):
            if self.take(1):
                width = self.take(5)
                self.take(width, True)
                self.take(width, True)
        width = self.take(5)
        self.take(width, True)
        self.take(width, True)
        self.align()


def tags(data, start, stop, path="root"):
    pos = start
    while pos + 2 <= stop:
        offset = pos
        head = struct.unpack_from('<H', data, pos)[0]
        pos += 2
        code, length = head >> 6, head & 63
        if length == 63:
            length = struct.unpack_from('<I', data, pos)[0]
            pos += 4
        assert pos + length <= stop, (offset, code, length, stop)
        yield code, offset, data[pos:pos+length], path
        if code == 39:
            sprite = struct.unpack_from('<H', data, pos)[0]
            yield from tags(data, pos+4, pos+length, path+f'/sprite-{sprite}')
        pos += length
        if code == 0:
            assert pos == stop, (path, pos, stop)
            return
    assert pos == stop


def extract(raw):
    assert raw[:3] in (b'FWS', b'CWS')
    data = raw if raw[:3] == b'FWS' else b'FWS'+raw[3:8]+zlib.decompress(raw[8:])
    assert struct.unpack_from('<I', data, 4)[0] == len(data)
    bits = Bits(data, 8)
    stage = bits.rect()
    start = bits.align()+4
    all_tags = list(tags(data, start, len(data)))
    fonts = {}
    for code, offset, body, path in all_tags:
        if code != 48:
            continue
        fid, flags, language, name_len = struct.unpack_from('<HBBB', body)
        pos = 5
        name = body[pos:pos+name_len].decode('latin1')
        pos += name_len
        count = struct.unpack_from('<H', body, pos)[0]
        pos += 2
        table_start = pos
        width = 4 if flags & 8 else 2
        code_offset = int.from_bytes(body[pos+count*width:pos+(count+1)*width], 'little')
        pos = table_start + code_offset
        code_width = 2 if flags & 4 else 1
        assert pos + count*code_width <= len(body)
        chars = [chr(int.from_bytes(body[pos+i*code_width:pos+(i+1)*code_width], 'little')) for i in range(count)]
        assert fid not in fonts
        fonts[fid] = dict(name=name, count=count, chars=chars, offset=offset)
    texts = []
    for code, offset, body, path in all_tags:
        if code not in (11, 33):
            continue
        tid = struct.unpack_from('<H', body)[0]
        bits = Bits(body, 2)
        rect = bits.rect()
        bits.matrix()
        pos = bits.align()
        glyph_bits, advance_bits = body[pos:pos+2]
        pos += 2
        fid = None
        runs = []
        while body[pos]:
            flags = body[pos]
            pos += 1
            assert flags & 128 and not flags & 112
            if flags & 8:
                fid = struct.unpack_from('<H', body, pos)[0]
                pos += 2
            if flags & 4:
                pos += 4 if code == 33 else 3
            if flags & 1:
                pos += 2
            if flags & 2:
                pos += 2
            if flags & 8:
                pos += 2
            count = body[pos]
            pos += 1
            bits = Bits(body, pos)
            indices = []
            for _ in range(count):
                indices.append(bits.take(glyph_bits))
                bits.take(advance_bits, True)
            assert fid in fonts
            assert all(i < fonts[fid]['count'] for i in indices)
            text = ''.join(fonts[fid]['chars'][i] for i in indices)
            runs.append(dict(font_id=fid, glyph_indices=indices, text=text))
            pos = bits.align()
        assert pos + 1 == len(body)
        texts.append(dict(tag=code, offset=offset, byte_length=len(body), id=tid,
                          container=path, bounds_twips=rect,
                          text=''.join(r['text'] for r in runs), runs=runs))
    return dict(input_sha256=hashlib.sha256(raw).hexdigest(),
                input_bytes=len(raw), uncompressed_bytes=len(data), stage_twips=stage,
                tag_counts=dict(collections.Counter(t[0] for t in all_tags)),
                fonts=fonts, text_definitions=texts,
                scope='Static text definitions only; no display-list, action, runtime or carrier-data validation.')


if __name__ == '__main__':
    result = extract(Path(sys.argv[1]).read_bytes())
    Path(sys.argv[2]).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'text_definitions': len(result['text_definitions']),
                      'fonts': len(result['fonts']), 'input_sha256': result['input_sha256']}))

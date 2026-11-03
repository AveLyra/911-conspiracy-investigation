"""Passive comparison of two court archive members; no actions or audio execution."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile
import zlib
from static_swf_text import Bits, extract, tags

ZIP_SHA256 = '3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801'
MEMBERS = ('UA93.swf', 'UA 93 Calls.swf')
SOUND_CODES = (14, 15, 17, 18, 19, 45, 89)


def digest_multiset(strings):
    counts = Counter(strings)
    encoded = json.dumps(sorted(counts.items()), ensure_ascii=False, separators=(',', ':')).encode()
    return counts, hashlib.sha256(encoded).hexdigest()


def check_controls():
    # A set-only comparison would miss changed multiplicity; normalization would
    # conceal the case and NUL differences. These are comparator controls only.
    a, da = digest_multiset(['A', 'A', 'b\x00'])
    reordered, dr = digest_multiset(['b\x00', 'A', 'A'])
    changed_count, dc = digest_multiset(['A', 'b\x00', 'b\x00'])
    changed_case, dl = digest_multiset(['a', 'A', 'b\x00'])
    stripped_nul, dn = digest_multiset(['A', 'A', 'b'])
    assert a == reordered and da == dr
    assert set(a) == set(changed_count) and a != changed_count and da != dc
    assert a != changed_case and da != dl
    assert a != stripped_nul and da != dn
    return {'order_invariance': True, 'multiplicity_change_rejected': True,
            'case_change_rejected': True, 'nul_removal_rejected': True,
            'scope': 'Comparator behavior only, not an independent SWF reader or historical validation.'}


def analyze(path):
    archive = Path(path).read_bytes()
    assert len(archive) == 28304524 and hashlib.sha256(archive).hexdigest() == ZIP_SHA256
    results, counters = [], []
    with zipfile.ZipFile(path) as zipped:
        inventory = [{'name': x.filename, 'bytes': x.file_size} for x in zipped.infolist()]
        for name in MEMBERS:
            raw = zipped.read(name)
            decoded = extract(raw)
            counter, digest = digest_multiset(x['text'] for x in decoded['text_definitions'])
            counters.append(counter)
            data = raw if raw[:3] == b'FWS' else b'FWS' + raw[3:8] + zlib.decompress(raw[8:])
            bits = Bits(data, 8)
            rect = bits.rect()
            header = bits.align()
            rate, frames = struct.unpack_from('<HH', data, header)
            all_tags = list(tags(data, header + 4, len(data)))
            selected = []
            for definition in decoded['text_definitions']:
                terms = [word for word in ('Gronlund', 'Glick', 'Beamer') if re.search(word, definition['text'], re.I)]
                if terms:
                    selected.append({'id': definition['id'], 'offset': definition['offset'],
                                     'container': definition['container'], 'matching_terms': terms,
                                     'raw_decoded_codepoints': len(definition['text']),
                                     'raw_text_sha256': hashlib.sha256(definition['text'].encode()).hexdigest()})
            results.append({'member': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                            'swf_version': raw[3], 'declared_frame_rate': rate / 256,
                            'declared_root_frames': frames, 'stage_twips': rect,
                            'text_definition_count': len(decoded['text_definitions']), 'distinct_raw_text_count': len(counter),
                            'raw_text_multiset_sha256': digest, 'selected_term_definition_coordinates': selected,
                            'standard_sound_tags': [{'code': code, 'offset': offset, 'container': container,
                                                     'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
                                                    for code, offset, body, container in all_tags if code in SOUND_CODES],
                            'tag_counts': decoded['tag_counts']})
    return {'archive_sha256': ZIP_SHA256, 'archive_bytes': len(archive), 'archive_member_count': len(inventory),
            'gronlund_named_members': [x['name'] for x in inventory if 'gronlund' in x['name'].lower()],
            'selected_members': results, 'original_bytes_equal': results[0]['sha256'] == results[1]['sha256'],
            'exact_raw_decoded_text_multisets_equal': counters[0] == counters[1],
            'common_text_occurrences': sum((counters[0] & counters[1]).values()),
            'text_occurrences_only_first': sum((counters[0] - counters[1]).values()),
            'text_occurrences_only_second': sum((counters[1] - counters[0]).values()),
            'complete_tag_counts_equal': results[0]['tag_counts'] == results[1]['tag_counts'],
            'comparison_controls': check_controls(),
            'limits': 'Exact decoded codepoint multiset and selected tag/header/coordinate metadata. No normalization, full graphics/font-shape/action/display/runtime/audio/voice/carrier/clock/cassette-custody authentication.'}


if __name__ == '__main__':
    import sys
    print(json.dumps(analyze(sys.argv[1]), indent=2))

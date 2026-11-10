"""Passive explicit-placement paths for a frozen court-exhibit text selection.

Uses the preserved static decoder and PlaceObject2 reader. No Flash, actions,
display-list simulation, phone inference or runtime execution.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys
import zipfile

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'telephone-wf334-static-context-2026-11-02'
sys.path.insert(0, str(HERE if (HERE/'structural_context.py').exists() else PREVIOUS))
from structural_context import Bits, tags, extract, place_prefix, check_controls

SELECTED = {340, 433, 912, 1684, 1685, 1689, 1690, 1691, 1692, 1693,
            1694, 1997, 1998, 2001, 2002, 2003, 2129, 2130, 2136,
            2137, 2140, 2141}
ZIP_SHA = '3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801'
SWF_SHA = '844dfb545c8414f9e7da1edc89ffe090a09d00d721a2c65c820e15f5fe201a06'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def independent_prefix(raw, offset, expected):
    """Re-read fixed source fields at the tag offset without place_prefix."""
    header = int.from_bytes(raw[offset:offset+2], 'little')
    assert header >> 6 == 26
    count = header & 63
    p = offset + 2
    if count == 63:
        count = int.from_bytes(raw[p:p+4], 'little')
        p += 4
    assert p + count <= len(raw)
    body = raw[p:p+count]
    assert body[0] & 2
    assert int.from_bytes(body[1:3], 'little') == expected['depth']
    assert int.from_bytes(body[3:5], 'little') == expected['character_id']
    assert sha(body) == expected['body_sha256']

def button_records(body):
    """Read only SWF5-compatible static character records; leave actions opaque."""
    bid, flags, action_offset = struct.unpack_from('<HBH', body)
    assert flags <= 1
    pos, records = 5, []
    while body[pos]:
        begin = pos
        state, cid, depth = struct.unpack_from('<BHH', body, pos)
        assert not state & 0xf0, 'Unsupported filter/blend/reserved bits'
        bits = Bits(body, pos+5)
        bits.matrix()
        add, mult, width = bits.take(1), bits.take(1), bits.take(4)
        for _ in range(4*(add+mult)):
            bits.take(width, True)
        pos = bits.align()
        # Independent fixed-field read at the selected record's byte position.
        assert int.from_bytes(body[begin+1:begin+3], 'little') == cid
        assert int.from_bytes(body[begin+3:begin+5], 'little') == depth
        records.append(dict(record_body_offset=begin, character_id=cid,
                            depth=depth, state_flags=state,
                            states=[s for mask,s in [(1,'up'),(2,'over'),
                                    (4,'down'),(8,'hit-test')] if state & mask],
                            record_hex=body[begin:pos].hex()))
    pos += 1
    if action_offset:
        assert pos == 3+action_offset
    else:
        assert pos == len(body)
    return dict(id=bid, track_as_menu=bool(flags), action_offset=action_offset,
                action_bytes_opaque=len(body)-pos, records=records)

def button_controls():
    empty = button_records(bytes.fromhex('010000000000'))
    assert empty['id']==1 and empty['records']==[]
    one = button_records(bytes.fromhex('01000000000117000200000000'))
    assert one['records'][0]['character_id']==23
    assert one['records'][0]['depth']==2 and one['records'][0]['states']==['up']
    bad = False
    try:
        button_records(bytes.fromhex('01000000001017000200000000'))
    except AssertionError:
        bad = True
    assert bad
    return dict(empty_layout_boundary=1, fixed_single_record=1,
                unsupported_flag_rejection=1,
                scope='Byte layout controls, not independent historical validation')

def analyze(zip_path):
    archive = Path(zip_path).read_bytes()
    assert sha(archive) == ZIP_SHA
    import io
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        raw = z.read('AA77.swf')
    assert sha(raw) == SWF_SHA and raw[:3] == b'FWS'
    decoded = extract(raw)
    # Normalize numeric dictionary keys to JSON strings before sorting. Otherwise
    # Python's numeric key order differs from the preserved JSON's string order.
    normalized = json.dumps(json.loads(json.dumps(decoded)), sort_keys=True,
                            separators=(',', ':')).encode()
    # Frozen from the original October27 extraction, not selected result values.
    assert sha(normalized) == 'beda1abfe4ee23fdc552227aec9f4bfb2f40fa46015b01edbd5266bbe781afd2'
    assert len(decoded['text_definitions']) == 548
    controls = check_controls()
    button_checks = button_controls()
    bits = Bits(raw, 8)
    bits.rect()
    start = bits.align() + 4
    frames = {'root': 1}
    sprites, edges, labels, actions, counts, buttons = {}, [], [], {}, {}, {}
    for code, off, body, path in tags(raw, start, len(raw)):
        frame = frames.setdefault(path, 1)
        counts[code] = counts.get(code, 0) + 1
        if code == 39:
            sid, n = struct.unpack_from('<HH', body)
            assert sid not in sprites
            sprites[sid] = dict(id=sid, definition_offset=off, declared_frames=n)
        elif code == 26:
            x = place_prefix(body)
            if x['character_id'] is not None:
                edges.append(dict(x, container=path, placement_offset=off,
                                  frame_ordinal=frame, body_sha256=sha(body)))
        elif code == 34:
            button = button_records(body)
            assert button['id'] not in buttons
            buttons[button['id']] = dict(button, definition_offset=off,
                                        body_sha256=sha(body))
        elif code == 43:
            labels.append(dict(container=path, tag_offset=off,
                               frame_ordinal=frame,
                               label=body[:body.index(0)].decode('utf-8')))
        elif code == 12:
            actions[path] = actions.get(path, 0) + 1
        elif code == 1:
            frames[path] += 1
    assert not counts.get(4, 0) and not counts.get(70, 0)
    for sid, item in sprites.items():
        assert frames['root/sprite-'+str(sid)]-1 == item['declared_frames']
    assert frames['root']-1 == struct.unpack_from('<H', raw, start-2)[0]
    relevant = set(SELECTED)
    while True:
        previous = set(relevant)
        for edge in edges:
            if edge['character_id'] in relevant and edge['container'] != 'root':
                relevant.add(int(edge['container'].rsplit('sprite-', 1)[1]))
        for bid, button in buttons.items():
            if any(x['character_id'] in relevant for x in button['records']):
                relevant.add(bid)
        if relevant == previous:
            break
    selected_edges = [e for e in edges if e['character_id'] in relevant]
    for edge in selected_edges:
        independent_prefix(raw, edge['placement_offset'], edge)
    contexts = {e['container'] for e in selected_edges}
    selected_labels = [x for x in labels if x['container'] in contexts and
                       x['label'].lower() in {'olson', 'unknown', 'may', 'flight77'}]
    assert len(selected_labels) <= 8
    return dict(zip_sha256=sha(archive), zip_bytes=len(archive),
                swf_sha256=sha(raw), swf_bytes=len(raw), swf_version=raw[3],
                all_548_prior_definitions_identical=True,
                reused_controls=controls, button_controls=button_checks,
                all_sprite_frame_counts_match=True,
                root_declared_frames=frames['root']-1,
                source_counts=dict(sprites=len(sprites),
                                   explicit_character_placements=len(edges),
                                   move_only_updates=counts[26]-len(edges),
                                   DoAction=counts.get(12, 0),
                                   DefineButton2=counts.get(34, 0)),
                selected_text_definitions=[x for x in decoded['text_definitions'] if x['id'] in SELECTED],
                selected_sprite_definitions=[sprites[s] for s in sorted(relevant) if s in sprites],
                selected_button_definitions=[buttons[s] for s in sorted(relevant) if s in buttons],
                selected_placements=selected_edges,
                selected_labels=selected_labels,
                unexecuted_actions={x:actions.get(x, 0) for x in sorted(contexts)},
                independently_rechecked_placement_prefixes=len(selected_edges),
                scope='Explicit authored placement/button character references and local frame ordinals only. No move-only state, display-list removal, clipping, transforms, button state or actions simulated; no runtime/visited trial screen, clock, caller, carrier, event or conversation authentication.')

if __name__ == '__main__':
    result = analyze(sys.argv[1])
    with Path(sys.argv[2]).open('x') as out:
        json.dump(result, out, indent=2)
        out.write('\n')
    print(json.dumps({k:result[k] for k in ['all_548_prior_definitions_identical',
                     'source_counts', 'independently_rechecked_placement_prefixes']}))

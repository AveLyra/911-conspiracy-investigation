"""Peer manual F6 Im3 reading. Literal row sets only; never classify RGB."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent

# Columns, core, fringe, reader-local piece. Inclusive literal row intervals.
# These choices were authored while reading complete lossless raw displays.
SOLID = """
146 87 85-86 SR1A
147 85-87 84 SR1A
148 81-85 80,86-87 SR1A
149 80-82 83-84 SR1A
150 - 78-81 SR1A
151 - 77-79 SR1A
152 - 76 SR1A
154 62-63 60-61 SR1B
155 60-62 59,63 SR1B
156 57-59 56,60 SR1B
157 54-58 53,59 SR1B
158 48-52 47,53-54 SR1B
159 46-50 45,51-52 SR1B
160 42-46 41,47 SR1B
161 39-43 38,44-46 SR1B
162 38-40 37,41 SR1B
163 38-39 37,40 SR1B
168 28-29 27,30 SR2
169 27-29 26,30 SR2
170 24-27 23,28 SR2
171 22-25 21,26-27 SR2
172 20-22 18-19,23-24 SR2
173 18-20 16-17,21-22 SR2
174 15-17 13-14,18-19 SR2
175 12-15 10-11,16-17 SR2
176 9-13 7-8,14-15 SR2
177 7-10 5-6,11-12 SR2
178 3-5 1-2,6-7 SR2
179 1-5 0,6 SR2
366 7-9 6,10 SD1
367 8-10 11-12 SD1
368 9-12 8,13 SD1
369 10-14 8-9,15 SD1
370 13-15 12,16 SD1
371 15-17 14,18 SD1
372 17-18 16,19 SD1
373 18-20 17,21 SD1
374 20-22 19,23 SD1
375 22-24 20-21,25 SD1
376 23-25 22,26-27 SD1
377 25-27 24,28 SD1
378 27-29 26,30 SD1
379 28-30 27,31 SD1
380 30-33 29,34 SD1
381 32-34 30-31,35 SD1
382 34-36 33,37 SD1
383 35-38 34,39 SD1
386 41-43 40,44 SD2
387 43-45 42,46 SD2
388 45-46 44,47 SD2
389 46-48 45,49-50 SD2
390 48-50 47,51-52 SD2
391 49-52 48,53-54 SD2
392 52-54 51,55-56 SD2
393 54-55 53,56-57 SD2
394 56-58 55,59 SD2
395 57-59 56,60 SD2
396 59-61 58,62 SD2
397 61-63 60,64-65 SD2
398 63-65 62,66 SD2
399 64-66 63,67 SD2
400 66-68 65,69 SD2
401 68-70 67,71 SD2
402 70-72 69,73 SD2
403 72-74 71,75 SD2
"""

DASH = """
151 - 87 DR1
152 87 86 DR1
153 87 86 DR1
154 83-87 82 DR1
155 85-87 84 DR1
165 85-87 84 DR2
166 84-86 83,87 DR2
167 - 84 DR2
166 78-80 76-77 DR3
167 76-79 75,80 DR3
168 76-77 75,78 DR3
169 - 76-77 DR3
169 - 80-82 DR4
170 81-84 80,85-86 DR4
171 84-86 82-83,87 DR4
172 - 85-86 DR4
180 85-87 83-84 DR5
181 82-86 80-81,87 DR5
182 81-82 79-80,83 DR5
183 76-77 74-75,78 DR5
184 73-76 71-72,77-78 DR5
185 72-74 71,75-76 DR5
185 67-68 65-66,69 DR6
186 64-67 63,68-69 DR6
187 63-64 62,65-66 DR6
188 59-60 58,61 DR6
189 60-62 59,63-64 DR6
190 62-64 61,65 DR6
191 - 63-64 DR6
191 68 67,69 DR7
192 68-70 67,71 DR7
193 69-70 68,71 DR7
194 69 68,70 DR7
198 63 62,64 DR8
199 62-64 61,65 DR8
200 - 62-63 DR8
200 54-55 53,56 DR9
201 52-55 50-51,56 DR9
202 50-52 49,53 DR9
203 - 50-51 DR9
203 46 45,47 DR10
204 45-46 43-44,47 DR10
205 43-45 41-42,46 DR10
206 41-44 39-40,45 DR10
207 41-42 40,43 DR10
207 - 35-37 DR11
208 34-37 32-33,38 DR11
209 32-35 30-31,36-37 DR11
210 - 31-33 DR11
211 - 27-28 DR12
212 27-28 25-26,29 DR12
213 25-27 23-24,28 DR12
214 23-26 21-22,27 DR12
215 23-24 21-22,25 DR12
215 - 18-19 DR13
216 16-18 14-15,19 DR13
217 15-17 13-14,18 DR13
218 13-15 12,16 DR13
219 - 13-14 DR13
219 - 8-10 DR14
220 8-10 6-7 DR14
221 6-9 4-5,10 DR14
222 4-7 3,8-9 DR14
223 - 4-5 DR14
222 0 1 DR15
223 0 1 DR15
224 - 0-1 DR15
369 - 18-20 DD1
370 18-21 17,22-23 DD1
371 20-23 19,24 DD1
372 - 22-23 DD1
372 27-29 26,30 DD2
373 28-31 27,32 DD2
374 30-32 29,33 DD2
375 32 31,33 DD2
376 - 32-33 DD2
377 - 35-37 DD3
378 36-38 35,39 DD3
379 37-40 36,41 DD3
380 - 39-41 DD3
381 45 44,46 DD4
382 44-45 43,46 DD4
383 43-45 42,46 DD4
386 36-37 35,38 DD5
387 35-37 34,38 DD5
388 36-37 35,38 DD5
389 37-38 36 DD5
390 - 41-43 DD6
391 41-42 40,43 DD6
392 41-42 43 DD6
394 32-34 31,35 DD7
395 30-33 29,34-35 DD7
396 30-31 29,32 DD7
397 30-31 29,32 DD7
398 - 30-31 DD7
398 34-35 36 DD8
399 35-37 34,38 DD8
400 36-38 35,39 DD8
401 38-39 37,40 DD8
402 - 38-39 DD8
402 33-34 32,35 DD9
403 32-34 30-31,35 DD9
404 30-31 29,32-33 DD9
406 24-25 23,26 DD10
407 24-26 23,27 DD10
408 25-27 24,28 DD10
409 - 26-27 DD10
409 31 30,32 DD11
410 31-33 30,34 DD11
411 33 32,34 DD11
412 31-33 30,34 DD11
413 31-32 30,33 DD11
415 22-24 21,25 DD12
416 - 21-23 DD12
417 - 24-25 DD13
418 24-26 23,27 DD13
419 26-28 24-25,29 DD13
420 28-29 27,30 DD13
421 - 29-30 DD13
422 31-32 30,33 DD14
423 29-31 28,32 DD14
424 29-30 28,31 DD14
425 29 28,30 DD14
428 36-39 35,40 DD15
429 37-39 36,40-41 DD15
430 - 42-44 DD16
431 43-44 42,45 DD16
432 43 42,44 DD16
436 - 46-49 DD17
437 48-51 47,52 DD17
439 56-58 55 DD18
"""

# Unassigned mixed-color bands are candidates for F6 only, not assignments
# of another pair's visible ink. No cross-pair labels were consulted.
# x, explicit uncertain rows, candidate route, local band suffix.
BANDS = """
149 79 solid rise-green
150 76-77 solid rise-green
151 74-76 solid rise-green
152 71-75 solid rise-green
153 67-73 solid rise-green
154 64 solid rise-green
162 35-36 solid rise-blue
163 33-36 solid rise-blue
164 34-39 solid rise-green
165 32-36 solid rise-green
166 29-33 solid rise-green
167 26-30 solid rise-green
168 25-26 solid rise-green
180 0-5 solid top-contact
156 84-87 dash low-blue
195 67-69 dash rise-green
196 65-68 dash rise-green
197 63-64 dash rise-green
360 0-5 both top-entry
361 0-1 both top-entry
362 0-5 both blue-contact
363 1-6 both blue-contact
364 2-7 both blue-contact
365 3-8 both blue-contact
366 3-5 both blue-contact
367 4-6 both blue-contact
384 36-45 both red-contact
385 36-44 both red-contact
392 37-40 dash blue-contact
393 37-42 dash blue-contact
394 37-41 dash blue-contact
404 72-77 solid purple-contact
405 72-78 solid purple-contact
406 74-80 solid purple-contact
407 78-82 solid purple-contact
408 80-83 solid purple-contact
409 81-86 solid purple-contact
410 82-87 solid purple-contact
411 84-87 solid purple-contact
412 86-87 solid purple-contact
413 87 solid purple-contact
405 25-30 dash green-contact
413 25-28 dash purple-contact
414 23-28 dash purple-contact
419 30-31 dash purple-contact
425 26-27 dash cyan-contact
426 28-31 dash cyan-contact
427 29-31 dash cyan-contact-a
427 33-36 dash cyan-contact-b
433 41-43 dash cyan-contact
434 40-43 dash cyan-contact
435 42-44 dash cyan-contact
438 48-52 dash cyan-contact
439 59-63 dash purple-contact
"""

# Fixed dependency manifest. These are not additional scientific observations.
PIN_LITERALS = """
../../native-strips01/Im3.jpg 13212 af735345f189bba0eab7a836c5c0c6221ab30055febd81b52b331821fe87259b
../../render01/page-076.png 943120 0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6
../PROTOCOL.md 5438 2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd
../approach34/read_context.py 5071 384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3
../force56-remainder/READERS.md 3332 e2508d4ca55ea9e6f06fef260a7ab17613ecbe533be47376c5c63264c436da2f
../read_context.py 4951 da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18
PROTOCOL.md 6231 fe2abe1dcee3680c3046022f979db59b37c948a37212cdc84066f44724c6c0f7
READERS.md 2663 bfa02c4cd1639efa1b90173c725651d32ad903350ccf1ab83640627756717a4f
read_context.py 4868 f37c9f55ccdc69d6a3d83d01015cbe5eff7b1f2f8aea4febe6c40863812ae5ec
context01.json 3232288 8cdcf742827f98c2c1cb4d2a7920d248bc4b5ff99e8194e8f6c006cb8990d024
context02.json 3232288 8cdcf742827f98c2c1cb4d2a7920d248bc4b5ff99e8194e8f6c006cb8990d024
../../../../../AGENTS.md 3256 0632c96247e3f9764e5046a8d5af6247733fb5c2a095c196e4347f89165e490a
../../../CHARTER.md 24068 54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd
../../../../../../../911/AGENTS.md 15240 934437bfc0ddbe522cc73461819593706d12c0644cb306d263d9f1fe3914a857
../../../../../../../911/START-HERE.md 6383 b291da2b9ab3f1a8e9e69ff5a5d930c689ff2d45a6b2ce06a521e76295fbd560
../../../../../../../911/WORKFLOW.md 5868 17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a
../../../../../../../911/research/sherlock-wtc7-investigation/CHARTER.md 24068 54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd
../../../../../../../../.codex/skills/evidence-falsification-auditor/SKILL.md 4215 7894e7c6150319ec9591ec39ee1d11c3687f37deaf494d8a7c97b515f29c48a2
../../../../../../../../.codex/skills/source-of-truth-guardian/SKILL.md 4218 d283182d3b1f493001ad8952102ff70ebf4d7d0575cbfa1891a38df80e313ab5
../../../../../../../../.codex/skills/evidence-falsification-auditor/references/claim-ledger-template.md 566 daf05820e54f7b6aa622e60b8406505a9d838ea4b5e8bdff6d265af60f6d402c
../../../../../../../../.codex/skills/source-of-truth-guardian/references/audit-checklist.md 841 b17b3fef9af6199f6efb0c7fc4ba772c2504cb76a28b4d0eecc4dfc0b8a78450
"""

# Actual first-pass receipts, not planned ranges; all were untruncated.
RAW_BLOCKS = """
143 150 1a66aa
151 162 eba995
163 178 c2ba63
179 194 75cc43
195 214 8aeba9
215 234 3f30b7
235 259 52e6e5
260 289 e398a2
290 319 79dad6
320 339 2d12c6
340 359 b4137f
360 375 87c97c
376 389 7881ee
390 405 14faf2
406 423 720525
424 441 5a09bc
"""

BAND_REASONS = {
    "rise-green": "Rising red candidate overlaps green-colored/compressed material; unique F6 ownership is unresolved.",
    "rise-blue": "Rising red candidate contacts blue-colored material; mixed cells are not uniquely attributed.",
    "top-contact": "Red/other-color contact reaches the top source/target edge; F6 ownership and continuation are unresolved.",
    "low-blue": "Lower red broken-body candidate meets blue-colored material at the source edge; ownership is unresolved.",
    "top-entry": "Top-edge colored material permits either F6 style as a candidate; no unique entry or continuation is established.",
    "blue-contact": "Blue/purple and red contact prevents unique local ownership; candidate routes are alternatives, not duplicate assignments.",
    "red-contact": "The red solid and broken candidates meet in shared red material; either local style could own these cells.",
    "purple-contact": "Red candidate and purple-colored material are not uniquely separable here; preserve an unassigned band.",
    "green-contact": "Red broken-body candidate crosses green material; the mixed cells are unassigned.",
    "cyan-contact": "Red broken-body candidate meets cyan/blue-colored material; the mixed footprint is not uniquely attributable.",
    "cyan-contact-a": "First separated mixed-color candidate band in this column; red versus cyan/blue ownership is unresolved.",
    "cyan-contact-b": "Second separated mixed-color candidate band in this column; no forced join with the first band.",
}


def pin(path):
    raw = path.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def expected_inputs():
    result = {}
    for line in PIN_LITERALS.strip().splitlines():
        path, size, digest = line.split()
        assert path not in result
        result[path] = {"sha256": digest, "bytes": int(size)}
    return result


def check_pins(expected):
    for path, value in expected.items():
        assert pin(HERE / path) == value, f"Changed input: {path}"


def rows(literal):
    """Expand manually stated inclusive integer runs; never inspect pixels."""
    if literal == "-":
        return []
    out = []
    for item in literal.split(","):
        if "-" in item:
            first, last = map(int, item.split("-"))
            assert first <= last
            out.extend(range(first, last + 1))
        else:
            out.append(int(item))
    assert out == sorted(set(out))
    assert all(0 <= y < 88 for y in out)
    return out


def flags(x, selected):
    if not selected:
        return []
    return [name for name, yes in (
        ("target_left", x == 145), ("target_right", x == 439),
        ("target_top", 0 in selected), ("target_bottom", 87 in selected),
    ) if yes]


def members(literal):
    result = {}
    for line in literal.strip().splitlines():
        column, core, fringe, local = line.split()
        x = int(column)
        assert 145 <= x < 440
        result.setdefault(x, []).append({
            "fragment_id": local, "core": rows(core), "fringe": rows(fringe),
        })
    return result


def make_bands():
    result = []
    for line in BANDS.strip().splitlines():
        column, cells, candidate, suffix = line.split()
        x = int(column)
        selected = rows(cells)
        local = f"U-{x}-{candidate}-{suffix}"
        candidates = ["solid", "dash"] if candidate == "both" else [candidate]
        result.append({
            "x": x, "core": [], "fringe": selected,
            "fragment_id": local,
            "fragment_membership": [{"fragment_id": local, "core": [], "fringe": selected}],
            "status": "identity_conflict", "reason": BAND_REASONS[suffix],
            "boundary_flags": flags(x, selected), "unassigned_band_refs": [],
            "band_id": local, "candidate_routes": candidates,
        })
    return sorted(result, key=lambda b: (b["x"], b["band_id"]))


def make_route(route, literal, bands):
    chosen = members(literal)
    result = []
    for x in range(145, 440):
        parts = chosen.get(x, [])
        core = sorted(y for member in parts for y in member["core"])
        fringe = sorted(y for member in parts for y in member["fringe"])
        refs = [band["band_id"] for band in bands
                if band["x"] == x and route in band["candidate_routes"]]
        boundary = flags(x, core + fringe)
        if boundary:
            status = "boundary_truncated"
        elif refs:
            status = "identity_conflict"
        elif core:
            status = "identified_local_fragment"
        elif fringe:
            status = "fringe_only"
        else:
            status = "no_attributable_cells"
        if parts:
            identities = ", ".join(member["fragment_id"] for member in parts)
            reason = (f"Manual local {route} reading of red F6 material, piece(s) {identities}; "
                      "core is confident visible-stroke attribution and fringe is tentative edge/compression attribution.")
        else:
            reason = (f"Complete column inspected; no cells uniquely attributed to F6 {route}. "
                      "This is nonassignment, not proof of absence, zero response, or physical support.")
        if refs:
            reason += " Same-column unassigned candidate bands preserve competing ownership."
        if boundary:
            reason += " Selected cells touch a target edge; this is not a physical endpoint."
        result.append({
            "x": x, "core": core, "fringe": fringe,
            "fragment_id": parts[0]["fragment_id"] if len(parts) == 1 else None,
            "fragment_membership": parts, "status": status, "reason": reason,
            "boundary_flags": boundary, "unassigned_band_refs": refs,
        })
    return result


def validate(data):
    """Structural arithmetic only: this does not validate visual attribution."""
    assert data["reader"] == "peer" and data["region_id"] == "F6-Im3"
    assert data["human_accepted"] is False and data["physical_support"] is None
    seen = [x for b in data["coverage"]["raw_blocks"]
            for x in range(b["columns"][0], b["columns"][1] + 1)]
    assert seen == list(range(143, 442)) and len(seen) * 88 == 26312
    band_map = {b["band_id"]: b for b in data["unassigned_bands"]}
    assert len(band_map) == len(data["unassigned_bands"])
    all_records = list(data["unassigned_bands"])
    for route in ("solid", "dash"):
        records = data["routes"][route]
        assert [r["x"] for r in records] == list(range(145, 440))
        all_records += records
        for record in records:
            expected_refs = [b["band_id"] for b in data["unassigned_bands"]
                             if b["x"] == record["x"] and route in b["candidate_routes"]]
            assert record["unassigned_band_refs"] == expected_refs
            if not record["core"] and not record["fringe"] and expected_refs:
                assert record["status"] == "identity_conflict"
    for record in all_records:
        core, fringe = record["core"], record["fringe"]
        assert core == sorted(set(core)) and fringe == sorted(set(fringe))
        assert not set(core) & set(fringe)
        assert 145 <= record["x"] < 440 and all(0 <= y < 88 for y in core + fringe)
        pieces = record["fragment_membership"]
        assert record["fragment_id"] == (pieces[0]["fragment_id"] if len(pieces) == 1 else None)
        assert sorted(y for p in pieces for y in p["core"]) == core
        assert sorted(y for p in pieces for y in p["fringe"]) == fringe
        assert record["boundary_flags"] == flags(record["x"], core + fringe)
        assert record["reason"]
    for x in range(145, 440):
        attributed = [set(data["routes"][r][x - 145]["core"] + data["routes"][r][x - 145]["fringe"])
                      for r in ("solid", "dash")]
        assert not attributed[0] & attributed[1]
        uncertain = [set(b["core"] + b["fringe"]) for b in data["unassigned_bands"] if b["x"] == x]
        for i, selected in enumerate(uncertain):
            assert not selected & (attributed[0] | attributed[1])
            assert not any(selected & other for other in uncertain[:i])


def build():
    expected = expected_inputs()
    check_pins(expected)
    original_script_pin = pin(Path(__file__))
    bands = make_bands()
    blocks = [{"columns": [int(a), int(b)], "receipt": receipt}
              for a, b, receipt in (line.split() for line in RAW_BLOCKS.strip().splitlines())]
    result = {
        "region_id": "F6-Im3", "pair": "F6", "source": "Im3.jpg", "reader": "peer",
        "target_box": [145, 0, 440, 88], "context_box": [143, 0, 442, 88],
        "inputs": expected, "script_pin": original_script_pin,
        "coverage": {
            "full_context_inspected": True, "raw_context_cells": 26312,
            "raw_blocks": blocks, "rows": [0, 87],
            "display_convention": "Only exact white (255,255,255) omitted; gN=(N,N,N); equal-RGB runs inclusive and lossless. No truncated blocks accepted.",
            "actual_views": [
                {"path": "../../native-strips01/Im3.jpg", "tool": "view_image", "receipt": "Actual original-detail whole-strip view in the functions.exec call paired with terminal receipt 575a9e; image tool supplied no separate receipt ID."},
                {"path": "../../render01/page-076.png", "tool": "view_image", "receipt": "Actual whole composed-page view in the same call as terminal receipt 575a9e; tool displayed the whole page at 1376x1780 from 1700x2200, without cropping; no separate image receipt ID."},
                {"path": "../../native-strips01/Im3.jpg", "tool": "view_image", "receipt": "Whole native strip reread in the call paired with terminal raw-block receipt 7881ee."},
            ],
            "rereads": [
                {"columns": [390, 405], "receipt": "Additional untruncated show call while finalizing literals; the tool output was forwarded as output text without its chunk ID."},
                {"columns": [406, 423], "receipt": "6db680"},
                {"columns": [424, 441], "receipt": "7aae46"},
            ],
            "synthetic_controls": "read_context.py controls: 17 passing controls, receipt 1a66aa, before raw reading.",
            "prior_knowledge": "Agent force6_im3_peer was assigned this prior-informed region and knew the F6/red, solid-spring/dashed-shell legend, finite target, earlier-region inventory and context overlap from the protocols. No primary F6 annotation or prior F5 annotation was read. This is an independent AI reading of the same pixels, not blind sampling, independent historical evidence or human acceptance.",
            "uncompleted_context": [],
        },
        "routes": {route: make_route(route, literal, bands) for route, literal in (("solid", SOLID), ("dash", DASH))},
        "unassigned_bands": bands, "human_accepted": False, "physical_support": None,
    }
    validate(result)
    check_pins(expected)
    assert pin(Path(__file__)) == original_script_pin
    return result


if __name__ == "__main__":
    data = build()
    destination = HERE / "reader-peer.json"
    with destination.open("x") as output:
        output.write(json.dumps(data, indent=2, sort_keys=True) + "\n")
    check_pins(data["inputs"])
    assert pin(Path(__file__)) == data["script_pin"]
    print(json.dumps({"saved": destination.name, "pin": pin(destination), "route_records": 590}, sort_keys=True))

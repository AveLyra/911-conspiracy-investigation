"""Independent fixed-batch E6/E7 audit. No producer/reader imports or execution."""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import sys

HERE = Path(__file__).resolve().parent
BOXES = {"E6": [515, 57, 690, 85], "E7": [580, 14, 690, 30]}
CONTEXT = {"E6": [513, 55, 692, 87], "E7": [578, 12, 692, 32]}
STATES = {"identified_local_fragment", "fringe_only", "no_attributable_cells",
          "identity_conflict", "boundary_truncated"}
FROZEN = {
    "../native-strips01/Im8.jpg": "0c49df5f6117d3f0e9b206d7c3352edf57849e4ac00ef9764b857b1445947d83",
    "../render01/page-076.png": "0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6",
    "PROTOCOL.md": "2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd",
    "REGIONS.json": "ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131",
    "read_context.py": "da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18",
    "context01.json": "b611904d9f065dcd23860e7bca998b26a07b6c0196b20dd5af9d3b1e854cadfb",
    "context02.json": "b611904d9f065dcd23860e7bca998b26a07b6c0196b20dd5af9d3b1e854cadfb",
    "reader-E6-root.py": "fb6416cdb4bcade2e519259b3acd8ca21cc6bf803bd849475c8a59a7f0cfc75c",
    "reader-E7-root.py": "0ef4b2efc4e210b1c2376db563265b9b3e58c56636fd80d9dae12bc28d1bf4c5",
    "reader-E6-independent.py": "5fd63bfd995df4ebc2c8c51189e93d340521932d91edaa6ef18d986ba3158a88",
    "reader-E6-root.json": "1a13f01b3e6820f4c36644d6369ed881f9ee342dab96ef4683dd5a75930b524e",
    "reader-E7-root.json": "8f929d7bd6154af3a715b6b739483fdc1d5d7e770106128071ad9bb9156adfca",
    "reader-E6-independent.json": "27304b37ffad172602f114bd9cc852d4cba4c2214b9f77aa643dfebeb8fffb2e",
    "reader-E7-independent.json": "090f3651e497f74d25826862b0c27468eb4f26d8385345470989dd1903013504",
    "context-independent-check.json": "1907c06961f35ad093ec959d213ad35dee531c33a3fc9cf86f17e476912cba04",
    "validate_reconcile.py": "59a763e3373ddfb1c4c130ec78f467b0c8ab563a55a9b18c100c8e02a9591543",
}
OUTPUT_PINS = {
    "E6-reconciliation01.json": "54a34943a6b08aaee0b36fa0e4e0c5bd48c3d81307d3ff143b0e306f8f488fd1",
    "E6-reconciliation02.json": "54a34943a6b08aaee0b36fa0e4e0c5bd48c3d81307d3ff143b0e306f8f488fd1",
    "E7-reconciliation01.json": "1ee237c9f84858e6c9489b5630dd751b2dce1840d0492e30d691834fcf3c28b9",
    "E7-reconciliation02.json": "1ee237c9f84858e6c9489b5630dd751b2dce1840d0492e30d691834fcf3c28b9",
}

class AuditError(Exception):
    pass

def need(condition, message):
    if not condition:
        raise AuditError(message)

def pin(path):
    raw = Path(path).read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def read_json(path):
    return json.loads(Path(path).read_text())

def five_operations(left, right):
    """Ordered two-pointer merge; no producer set functions or set operators."""
    out = {k: [] for k in ("intersection", "union", "root_only",
                           "peer_only", "symmetric_difference")}
    i = j = 0
    while i < len(left) or j < len(right):
        if i < len(left) and j < len(right) and left[i] == right[j]:
            out["intersection"].append(left[i])
            out["union"].append(left[i])
            i += 1
            j += 1
        elif i < len(left) and (j == len(right) or left[i] < right[j]):
            value = left[i]
            out["union"].append(value)
            out["root_only"].append(value)
            out["symmetric_difference"].append(value)
            i += 1
        else:
            value = right[j]
            out["union"].append(value)
            out["peer_only"].append(value)
            out["symmetric_difference"].append(value)
            j += 1
    return out

def union(left, right):
    return five_operations(left, right)["union"]

def rows_ok(rows, lo, hi):
    need(isinstance(rows, list), "Rows must be explicit lists")
    need(all(type(y) is int and lo <= y < hi for y in rows), "Noninteger/out-of-bounds row")
    need(all(a < b for a, b in zip(rows, rows[1:])), "Unsorted or duplicate row")
    return rows

def boundary_flags(x, rows, box):
    if not rows:
        return []
    x0, y0, x1, y1 = box
    flags = []
    if y0 in rows:
        flags.append("target_top")
    if y1 - 1 in rows:
        flags.append("target_bottom")
    if x == x0:
        flags.append("target_left")
    if x == x1 - 1:
        flags.append("target_right")
    return flags

def identity_summary(entry):
    membership = entry.get("fragment_membership")
    return {
        "explicit_single_id": entry.get("fragment_id") is not None,
        "membership_count": len(membership) if membership is not None else None,
        "explicit_conflict": entry["status"] == "identity_conflict",
        "unknown_attribution": entry.get("fragment_id") is None and not membership,
    }

def validate_entry(entry, box):
    x0, y0, x1, y1 = box
    need(type(entry["x"]) is int and x0 <= entry["x"] < x1, "Bad x")
    core = rows_ok(entry["core"], y0, y1)
    fringe = rows_ok(entry["fringe"], y0, y1)
    need(not five_operations(core, fringe)["intersection"], "Core/fringe overlap")
    need(entry["status"] in STATES, "Unknown status")
    need(isinstance(entry["note"], str) and bool(entry["note"]), "Missing note")
    fragment = entry.get("fragment_id")
    need(fragment is None or (isinstance(fragment, str) and bool(fragment)), "Bad fragment ID")
    flags = boundary_flags(entry["x"], union(core, fringe), box)
    need(isinstance(entry["boundary_flags"], list), "Flags must be a list")
    need(sorted(flags) == sorted(entry["boundary_flags"]) and
         len(flags) == len(entry["boundary_flags"]), "Boundary flag mismatch")
    if flags:
        need(entry["status"] == "boundary_truncated", "Selected boundary lacks status")
    if entry["status"] == "boundary_truncated":
        need(bool(flags), "Boundary status without selected boundary cell")
    membership = entry.get("fragment_membership")
    if membership is not None:
        need(isinstance(membership, dict), "Bad membership map")
        mc, mf = [], []
        for name, part in membership.items():
            need(isinstance(name, str) and bool(name), "Bad local member ID")
            pc = rows_ok(part["core"], y0, y1)
            pf = rows_ok(part["fringe"], y0, y1)
            need(not five_operations(pc, pf)["intersection"], "Member classes overlap")
            mc, mf = union(mc, pc), union(mf, pf)
        need(mc == core and mf == fringe, "Classwise fragment union mismatch")
        if fragment is not None:
            need(list(membership) == [fragment], "Single ID contradicts membership")
    if entry["status"] == "identified_local_fragment":
        need(bool(core) and (fragment is not None or bool(membership)), "Unidentified local core")
    if entry["status"] == "fringe_only":
        need(not core and bool(fringe), "Invalid fringe-only entry")
    if entry["status"] == "no_attributable_cells":
        need(not core and not fringe, "Empty-attribution status with cells")
    return identity_summary(entry)

def literal_value(node, bindings):
    """Only literals and already-extracted literal names; never eval/exec/call."""
    if isinstance(node, ast.Name):
        need(node.id in bindings, "Unknown literal name: " + node.id)
        return bindings[node.id]
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, (ast.List, ast.Tuple)):
        return [literal_value(n, bindings) for n in node.elts]
    if isinstance(node, ast.Dict):
        return {literal_value(k, bindings): literal_value(v, bindings)
                for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        value = literal_value(node.operand, bindings)
        need(type(value) in (int, float), "Non-numeric unary literal")
        return -value
    raise AuditError("Nonliteral AST node refused: " + type(node).__name__)

def script_literals(path):
    tree = ast.parse(Path(path).read_text(), filename=str(path))
    bindings = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                bindings[node.targets[0].id] = literal_value(node.value, bindings)
            except AuditError:
                pass
    return tree, bindings

def named_dictionary(tree, key, bindings):
    matches = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and k.value == key:
                    matches.append(literal_value(v, bindings))
    need(len(matches) == 1, "Expected one literal metadata dictionary: " + key)
    return matches[0]

def add_run(table, first, last, core, fringe, fragment, state, box):
    need(type(first) is int and type(last) is int and first <= last, "Bad literal run")
    for x in range(first, last + 1):
        need(x not in table, "Literal runs overlap")
        flags = boundary_flags(x, union(core, fringe), box)
        table[x] = {
            "x": x, "core": list(core), "fringe": list(fringe),
            "fragment_id": fragment, "boundary_flags": flags,
            "status": "boundary_truncated" if flags else state,
        }

def root_literal_expansion(pair, record):
    tree, bindings = script_literals(HERE / ("reader-" + pair + "-root.py"))
    manual = named_dictionary(tree, "literal_runs", bindings)
    need(manual == record["literal_runs"], pair + " root AST/JSON literal metadata mismatch")
    need({k: v["sha256"] for k, v in record["inputs"].items()} == bindings["EXPECTED"],
         pair + " root declared expected pins differ from AST")
    box = BOXES[pair]
    expanded = {"solid": {}, "dash": {}}
    solids = manual["solid"] if isinstance(manual["solid"], list) else [manual["solid"]]
    for item in solids:
        add_run(expanded["solid"], *item["columns"], item["core"], item["fringe"],
                item["fragment_id"], "identified_local_fragment", box)
    for fragment, first, last in manual["dash_core_runs"]:
        for x in range(first, last + 1):
            weak = x in manual.get("weak_lower_body_rows", [])
            core = manual["weak_core"] if weak else manual["dash_body_core"]
            fringe = manual["weak_fringe"] if weak else manual["dash_body_fringe"]
            add_run(expanded["dash"], x, x, core, fringe, fragment, "identified_local_fragment", box)
    special = manual.get("dash_last_column")
    if special:
        add_run(expanded["dash"], special["x"], special["x"], special["core"],
                special["fringe"], special["fragment_id"], "boundary_truncated", box)
    other = manual["dash_other_columns"]
    for x in range(box[0], box[2]):
        if x not in expanded["dash"]:
            add_run(expanded["dash"], x, x, other["core"], other["fringe"],
                    other["fragment_id"], other["status"], box)
    return expanded

def independent_e6_expansion():
    tree, literals = script_literals(HERE / "reader-E6-independent.py")
    need(all(key in literals for key in ("SOLID", "DASH_BODIES", "PALE", "EMPTY")),
         "Missing independent E6 literals")
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and
             isinstance(n.func, ast.Name) and n.func.id == "entry"]
    solid_call = [n for n in calls if isinstance(n.args[1], ast.Name)][0]
    body_call = [n for n in calls if isinstance(n.args[4], ast.JoinedStr)][0]
    pale_call = [n for n in calls if isinstance(n.args[3], ast.Constant) and
                 n.args[3].value == "identity_conflict"][0]
    empty_call = [n for n in calls if isinstance(n.args[3], ast.Constant) and
                  n.args[3].value == "no_attributable_cells"][0]
    identifier = body_call.args[4]
    need(len(identifier.values) == 2 and isinstance(identifier.values[0], ast.Constant)
         and isinstance(identifier.values[1], ast.FormattedValue), "Unsupported body ID format")
    fmt = identifier.values[1]
    need(isinstance(fmt.value, ast.Name) and fmt.value.id == "i" and
         isinstance(fmt.format_spec, ast.JoinedStr) and
         len(fmt.format_spec.values) == 1 and fmt.format_spec.values[0].value == "02",
         "Body numbering format changed")
    prefix = identifier.values[0].value
    box = BOXES["E6"]
    expanded = {"solid": {}, "dash": {}}
    solid_id = literal_value(solid_call.args[4], literals)
    for first, last, core, fringe in literals["SOLID"]:
        add_run(expanded["solid"], first, last, core, fringe, solid_id,
                literal_value(solid_call.args[3], literals), box)
    for number, (first, last) in enumerate(literals["DASH_BODIES"], 1):
        add_run(expanded["dash"], first, last,
                literal_value(body_call.args[1], literals), literal_value(body_call.args[2], literals),
                prefix + format(number, "02"), literal_value(body_call.args[3], literals), box)
    for key, call in (("PALE", pale_call), ("EMPTY", empty_call)):
        for x in literals[key]:
            add_run(expanded["dash"], x, x, literal_value(call.args[1], literals),
                    literal_value(call.args[2], literals), literal_value(call.args[4], literals),
                    literal_value(call.args[3], literals), box)
    return expanded

def independent_e7_expansion(record):
    literal = record["literal_manual_transcription"]
    expanded = {"solid": {}, "dash": {}}
    groups = (("solid", literal["solid_runs"]),
              ("dash", literal["dash_body_runs"] + literal["dash_uncertain_fringe_runs"]))
    for route, runs in groups:
        for item in runs:
            add_run(expanded[route], item["first"], item["last"], item["core"], item["fringe"],
                    item["fragment_id"], item["base_status"], BOXES["E7"])
    return expanded

def check_declared_pin(path, declared, watched):
    path = Path(path).resolve()
    actual = pin(path)
    digest = declared if isinstance(declared, str) else declared["sha256"]
    need(actual["sha256"] == digest, "Declared SHA mismatch: " + str(path))
    if isinstance(declared, dict) and "bytes" in declared:
        need(type(declared["bytes"]) is int and actual["bytes"] == declared["bytes"],
             "Declared byte-count mismatch: " + str(path))
    watched[str(path)] = actual
    return str(path)

def reader_dependencies(pair, role, reader, watched):
    files = set()
    if role == "root":
        for name, declared in reader["inputs"].items():
            files.add(check_declared_pin(HERE / name, declared, watched))
        files.add(check_declared_pin(HERE / ("reader-" + pair + "-root.py"),
                                    reader["script_pin"], watched))
    elif pair == "E7":
        for declared in reader["pins"].values():
            files.add(check_declared_pin(declared["path"], declared, watched))
    else:
        names = {"source_sha256": "../native-strips01/Im8.jpg",
                 "protocol_sha256": "PROTOCOL.md", "roster_sha256": "REGIONS.json",
                 "raw_context_sha256": "context01.json",
                 "literal_script_sha256": "reader-E6-independent.py"}
        need(set(reader["pins"]) == set(names), "Unexpected E6 peer declared pin")
        for name, rel in names.items():
            files.add(check_declared_pin(HERE / rel, reader["pins"][name], watched))
    return files

def verify_reader(pair, role, reader, expected):
    box = BOXES[pair]
    need(reader["pair"] == pair and set(reader["routes"]) == {"solid", "dash"}, "Wrong reader pair/routes")
    aliases = [reader[k] for k in ("target_box", "target_rectangle_half_open") if k in reader]
    if "target_box" in reader.get("coverage", {}):
        aliases.append(reader["coverage"]["target_box"])
    need(bool(aliases) and all(v == box for v in aliases), "Target aliases disagree")
    status_counts = Counter()
    for route in ("solid", "dash"):
        entries = reader["routes"][route]
        need([e["x"] for e in entries] == list(range(box[0], box[2])), "Reader coverage/order mismatch")
        need(sorted(expected[route]) == list(range(box[0], box[2])), "Literal coverage mismatch")
        for entry in entries:
            validate_entry(entry, box)
            literal = expected[route][entry["x"]]
            for key, value in literal.items():
                actual = entry[key]
                need(sorted(actual) == sorted(value) if key == "boundary_flags" else actual == value,
                     pair + "/" + role + "/" + route + " literal mismatch " + key + " at " + str(entry["x"]))
            status_counts[entry["status"]] += 1
    return dict(sorted(status_counts.items()))

def require_outputs(names, exists=None):
    if exists is None:
        exists = lambda p: p.is_file()
    missing = [str(p) for p in names if not exists(p)]
    need(not missing, "Reconciliation outputs absent; no historical check performed: " + ", ".join(missing))

def controls():
    checks = {}
    def test(name, fn):
        fn()
        checks[name] = True
    def must_fail(fn):
        try:
            fn()
        except AuditError:
            return
        raise AuditError("Negative control did not fail")
    test("empty_sets", lambda: need(five_operations([], []) ==
         {"intersection": [], "union": [], "root_only": [], "peer_only": [], "symmetric_difference": []}, "empty"))
    test("overlap_and_holes", lambda: need(five_operations([1, 3, 8], [3, 4, 8]) ==
         {"intersection": [3, 8], "union": [1, 3, 4, 8], "root_only": [1],
          "peer_only": [4], "symmetric_difference": [1, 4]}, "overlap"))
    test("disjoint_sets", lambda: need(five_operations([1, 5], [2, 6]) ==
         {"intersection": [], "union": [1, 2, 5, 6], "root_only": [1, 5],
          "peer_only": [2, 6], "symmetric_difference": [1, 2, 5, 6]}, "disjoint"))
    test("identical_sets", lambda: need(five_operations([2, 7], [2, 7]) ==
         {"intersection": [2, 7], "union": [2, 7], "root_only": [],
          "peer_only": [], "symmetric_difference": []}, "identical"))
    test("one_empty_direction", lambda: need(five_operations([], [2])["peer_only"] == [2] and
         five_operations([2], [])["root_only"] == [2], "one empty"))
    test("boundary_selected_only", lambda: need(boundary_flags(2, [], [2, 4, 4, 7]) == [] and
         boundary_flags(2, [4, 6], [2, 4, 4, 7]) == ["target_top", "target_bottom", "target_left"], "flags"))
    test("boolean_row_rejected", lambda: must_fail(lambda: rows_ok([True], 0, 3)))
    test("duplicate_row_rejected", lambda: must_fail(lambda: rows_ok([1, 1], 0, 3)))
    test("nonliteral_call_rejected", lambda: must_fail(lambda: literal_value(ast.parse("f()").body[0].value, {})))
    test("literal_name_expansion", lambda: need(literal_value(ast.parse("{'x': A}").body[0].value,
         {"A": [1, 3]}) == {"x": [1, 3]}, "literal"))
    test("overlapping_manual_runs_rejected", lambda: must_fail(lambda: add_run({2: {}}, 2, 2,
         [4], [], "id", "identified_local_fragment", [2, 4, 4, 7])))
    entry = {"x": 3, "core": [5], "fringe": [], "status": "identified_local_fragment",
             "fragment_id": "a", "note": "synthetic", "boundary_flags": []}
    test("reader_local_names_not_equated", lambda: need(identity_summary(entry) ==
         identity_summary(dict(entry, fragment_id="other-reader-id")), "identity"))
    bad = dict(entry, fragment_membership={"a": {"core": [4], "fringe": []}})
    test("membership_union_mismatch_rejected", lambda: must_fail(lambda: validate_entry(bad, [2, 4, 5, 7])))
    test("missing_outputs_fail_clearly", lambda: must_fail(lambda: require_outputs([Path("invented-output.json")], lambda _: False)))
    return checks

def historical_check():
    require_outputs([HERE / name for name in OUTPUT_PINS])
    watched = {}
    for name, digest in dict(FROZEN, **OUTPUT_PINS).items():
        check_declared_pin(HERE / name, digest, watched)
    watched[str(Path(__file__).resolve())] = pin(__file__)
    context_record = read_json(HERE / "context-independent-check.json")
    need(context_record["status"] == "passed_independent_context_verification" and
         context_record["cells_checked"] == 8008, "Context verification scope/status changed")
    need(context_record["row_major_order_verified"] is True and
         context_record["context_bytes_equal"] is True, "Context verification incomplete")
    for pair, count in (("E6", 5728), ("E7", 2280)):
        item = context_record["pairs"][pair]
        need(item["cells"] == count and item["source_pixels_exact"] is True and
             item["display_roundtrip_exact"] is True, "Context record lacks exact source check")
    for name, declared in context_record["pins"].items():
        check_declared_pin(name, declared, watched)
    context = read_json(HERE / "context01.json")
    need(context["target_boxes"] == BOXES and context["context_boxes"] == CONTEXT, "Context boxes changed")
    for name, declared in context["inputs"].items():
        check_declared_pin(name, declared, watched)
    for field, name in (("source_pin", "../native-strips01/Im8.jpg"),
                        ("protocol_pin", "PROTOCOL.md"), ("roster_pin", "REGIONS.json"),
                        ("script_pin", "read_context.py")):
        check_declared_pin(HERE / name, context[field], watched)
    need((HERE / "context01.json").read_bytes() == (HERE / "context02.json").read_bytes(), "Context repeat differs")
    pair_results = {}
    all_reader_statuses = {}
    for pair in ("E6", "E7"):
        readers = {role: read_json(HERE / ("reader-" + pair + "-" +
                   ("root" if role == "root" else "independent") + ".json"))
                   for role in ("root", "peer")}
        literal = {"root": root_literal_expansion(pair, readers["root"]),
                   "peer": independent_e6_expansion() if pair == "E6" else independent_e7_expansion(readers["peer"])}
        dependencies = set()
        for role, reader in readers.items():
            all_reader_statuses[pair + "-" + role] = verify_reader(pair, role, reader, literal[role])
            dependencies.update(reader_dependencies(pair, role, reader, watched))
            dependencies.add(str((HERE / ("reader-" + pair + "-" +
                             ("root" if role == "root" else "independent") + ".json")).resolve()))
        dependencies.update([str((HERE / "validate_reconcile.py").resolve()),
                             str((HERE.parent / "render01/page-076.png").resolve())])
        expected_inputs = {name: pin(name) for name in sorted(dependencies)}
        a, b = HERE / (pair + "-reconciliation01.json"), HERE / (pair + "-reconciliation02.json")
        need(a.read_bytes() == b.read_bytes(), pair + " reconciliation repeats differ")
        output = read_json(a)
        need(set(output) == {"pair", "rows", "inputs", "inputs_after", "python", "limits",
                             "additional_verifier_pins"}, "Unexpected reconciliation top-level fields")
        need(output["pair"] == pair and output["inputs"] == expected_inputs and
             output["inputs_after"] == expected_inputs, pair + " before/after input pin map differs")
        need(output["additional_verifier_pins"]["composed_page"] ==
             str((HERE.parent / "render01/page-076.png").resolve()), "Additional page pin missing")
        need(bool(output["additional_verifier_pins"]["reason"]) and bool(output["limits"]), "Missing scope limits")
        box = BOXES[pair]
        expected_order = [(route, x) for route in ("solid", "dash") for x in range(box[0], box[2])]
        need([(r["route"], r["x"]) for r in output["rows"]] == expected_order, "Reconciliation row coverage/order")
        by_route = {route: Counter() for route in ("solid", "dash")}
        for row, (route, x) in zip(output["rows"], expected_order):
            need(set(row) == {"route", "x", "root", "peer", "core", "fringe", "outer",
                              "status_equal", "root_identity", "peer_identity"}, "Unexpected row keys")
            left = readers["root"]["routes"][route][x - box[0]]
            right = readers["peer"]["routes"][route][x - box[0]]
            need(row["root"] == left and row["peer"] == right, "Raw reader entry not retained")
            need(type(row["status_equal"]) is bool and row["status_equal"] ==
                 (left["status"] == right["status"]), "Status-equality summary mismatch")
            for role, entry in (("root", left), ("peer", right)):
                actual = row[role + "_identity"]
                expected = identity_summary(entry)
                need(actual == expected, "Identity summary mismatch")
                need(all(type(actual[k]) is bool for k in ("explicit_single_id", "explicit_conflict",
                                                           "unknown_attribution")), "Identity boolean type")
            for cls in ("core", "fringe", "outer"):
                lrows = left[cls] if cls != "outer" else union(left["core"], left["fringe"])
                rrows = right[cls] if cls != "outer" else union(right["core"], right["fringe"])
                need(row[cls] == five_operations(lrows, rrows), pair + " set operation mismatch")
            counts = by_route[route]
            counts["records"] += 1
            counts["outer_differing_records"] += bool(row["outer"]["symmetric_difference"])
            counts["classification_differing_records"] += left["core"] != right["core"] or left["fringe"] != right["fringe"]
            counts["status_differing_records"] += left["status"] != right["status"]
            counts["identity_summary_differing_records"] += identity_summary(left) != identity_summary(right)
        totals = Counter()
        for value in by_route.values():
            totals.update(value)
        pair_results[pair] = {
            "paired_entries": len(output["rows"]),
            "set_operations_checked": len(output["rows"]) * 3 * 5,
            "repeat_outputs_identical": True, "totals": dict(totals),
            "by_route": {k: dict(v) for k, v in by_route.items()},
        }
    need(sum(v["paired_entries"] for v in pair_results.values()) == 570, "Wrong paired total")
    need(sum(v["set_operations_checked"] for v in pair_results.values()) == 8550, "Wrong operation total")
    after = {name: pin(name) for name in watched}
    need(watched == after, "Input changed during independent check")
    return {
        "status": "passed_independent_reconciliation_verification",
        "pairs": pair_results, "reader_status_counts": all_reader_statuses,
        "literal_reader_records_checked": 1140, "paired_entries_checked": 570,
        "set_operations_checked": 8550, "raw_reader_records_retained_checked": 1140,
        "all_source_and_declared_pins_checked": True,
        "inputs_unchanged_during_check": True, "pins": watched,
        "context_verification_reused": {
            "path": str(HERE / "context-independent-check.json"),
            "cells": 8008,
            "scope": "Verified that the pinned prior record reports exact source/roundtrip checks for all cells; did not repeat the 8008-cell image traversal. Same-Pillow-codec limitation remains.",
        },
        "method": "Separate ordered-merge arithmetic for all five set operations; AST extraction of literal root/E6-peer instructions and E7-peer embedded manual transcription; no producer or reader modules imported or executed.",
        "classification_difference_definition": "A paired record whose core or fringe lists differ, separately from outer-set, status, or identity-summary differences.",
        "limits": [
            "Same-source nonblind AI computational verification; this checker author also supplied the E7 independent annotation.",
            "Not a new visual review or evidence that either annotation is accurate; coverage statements remain reader attestations.",
            "Reader-local IDs are retained but never equated across readers. Pale/empty entries are not physical support decisions.",
            "No graphical containment, ordinates, physical support, metrics, human acceptance or causal finding is admitted.",
        ],
        "python": platform.python_version(),
        "command": [sys.executable, "-B", str(Path(__file__).resolve()), "check"],
        "checker_pin": pin(__file__),
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("controls", "check"))
    args = parser.parse_args()
    try:
        tests = controls()
        if args.mode == "controls":
            result = {"status": "passed_synthetic_controls", "tests": tests, "count": len(tests)}
        else:
            result = historical_check()
            result["synthetic_controls"] = tests
            result["synthetic_control_count"] = len(tests)
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    except (AuditError, KeyError, IndexError, TypeError, ValueError, OSError) as exc:
        print("INDEPENDENT CHECK FAILED: " + str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

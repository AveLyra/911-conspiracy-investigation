#!/usr/bin/env python3
"""Five fixed APDL01 fields only; no evaluation or whole-source classifier.

Native mode is operationally HOLD until independent code/privacy clearance.
The old independent helper supplies only guarded reads, manifest selection and
quote splitting. No root producer code or outcomes are imported.
"""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import types
from unittest.mock import patch

HERE = Path(__file__).absolute().parent
HELPER_PIN = "4faf95f175ccd8d17947cc29f777e8bcb714727a034be72cc99c937578524d62"
PROTOCOL_PIN = "5cced3d7159405e035c2c4c0c0eca4995b2052371992977735c618a90ae54fd5"
TARGET_PIN = "e29a710e92720686d6be306c45fa5d9562f3f5dc47b1d585638d8f74b1324dae"
LIST_PIN = "423426c4f3579e241eddff94f603556debc3380edf95f5812b41b425ac122b9d"
OLD_PROTOCOL_PIN = "88aa92198fd2c754db0301c0cd8b1d679caa70cd338cf9debe7113b75691e670"
CAP = 4 * 1024 * 1024
LINE_CAP = 16384
HEX = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
DECIMAL = r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eEdD][+-]?[0-9]+)?"
SIGNED_NUMBER = re.compile(r"[+-]?" + DECIMAL + r"\Z", re.ASCII)
NUMBER_TOKEN = re.compile(DECIMAL, re.ASCII)
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*", re.ASCII)
ELEMENT = re.compile(r"[A-Za-z]+[0-9]+\Z", re.ASCII)
OUTPUT = re.compile(r"followup-independent-(?:run[0-9]{2}|synthetic[0-9]{2})\.json\Z", re.ASCII)
TARGET_KEYS = {"line", "segment", "command", "argument_count", "local_or_material_id", "field_index", "role", "segment_sha256", "field_sha256"}
EXPECTED = ((27, "ET", 5, "1", 2, "ENAME"), (46, "MP", 3, "1", 3, "C0"),
            (281, "MP", 3, "2", 3, "C0"), (2453, "ET", 2, "2", 2, "ENAME"),
            (2654, "ET", 4, "5", 2, "ENAME"))
FAILURES = frozenset(("ARGUMENTS", "PATH", "IO", "CAP", "PIN", "CHANGED", "HELPER",
                     "CONTROLS", "TARGET", "ALLOWLIST", "LINE_CAP", "NUL", "SOURCE",
                     "OUTPUT_EXISTS", "OUTPUT_PATH", "OUTPUT_IO", "SELFTEST", "UNEXPECTED"))


class Refusal(Exception):
    def __init__(self, code):
        self.code = code if code in FAILURES else "UNEXPECTED"
        super().__init__(self.code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def directory_fd(path):
    """Local no-follow directory walk for bootstrap and create-only outputs."""
    if not path.is_absolute() or ".." in path.parts:
        raise Refusal("PATH")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            other = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = other
        return fd
    except BaseException:
        os.close(fd)
        raise


def bootstrap_helper():
    """Hash exact helper bytes before executing that known local Python code."""
    directory, fd = directory_fd(HERE), None
    try:
        fd = os.open("independent_parse.py", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size > CAP:
            raise Refusal("HELPER")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(CAP + 1)
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            raise Refusal("CHANGED")
        if len(data) > CAP or sha(data) != HELPER_PIN:
            raise Refusal("HELPER")
        module = types.ModuleType("independent_followup_guard_helper")
        module.__file__ = str(HERE / "independent_parse.py")
        exec(compile(data, module.__file__, "exec"), module.__dict__)
        return module
    except (OSError, ValueError):
        raise Refusal("HELPER") from None
    finally:
        if fd is not None:
            os.close(fd)
        os.close(directory)


def density_category(raw):
    text = raw.strip()
    if not text:
        return "blank"
    if len(text) > 256:
        return "over_cap"
    if "'" in text or '"' in text:
        return "quote_bearing"
    if len(text) <= 64 and SIGNED_NUMBER.fullmatch(text):
        return "numeric_literal"
    if len(text) <= 32 and IDENT.fullmatch(text):
        return "identifier"
    cursor = depth = token_count = 0
    operand = True
    has_identifier = False
    while cursor < len(text):
        if text[cursor] in " \t\r\n":
            cursor += 1
            continue
        token_count += 1
        if token_count > 128:
            return "unsupported"
        char = text[cursor]
        if operand:
            if char in "+-":
                cursor += 1
                continue
            if char == "(":
                depth += 1
                if depth > 16:
                    return "unsupported"
                cursor += 1
                continue
            number = NUMBER_TOKEN.match(text, cursor)
            identifier = IDENT.match(text, cursor) if number is None else None
            match = number or identifier
            if match is None or len(match.group()) > (64 if number else 32):
                return "unsupported"
            has_identifier |= identifier is not None
            cursor = match.end()
            operand = False
        else:
            if char == ")" and depth > 0:
                depth -= 1
                cursor += 1
            elif char in "+-*/":
                cursor += 2 if text.startswith("**", cursor) else 1
                operand = True
            else:
                return "unsupported"
    if operand or depth:
        return "unsupported"
    return "identifier_arithmetic" if has_identifier else "numeric_arithmetic"


def element_classification(raw, names):
    token = raw.strip()
    if len(token) <= 64 and ELEMENT.fullmatch(token) and token.upper() in names:
        return {"classification": "official_name_match", "name": token.upper()}
    return {"classification": "unresolved"}


def validate_targets(targets):
    if type(targets) is not list or len(targets) != 5:
        raise Refusal("TARGET")
    for item, expected in zip(targets, EXPECTED):
        if type(item) is not dict or set(item) != TARGET_KEYS:
            raise Refusal("TARGET")
        for key in ("line", "segment", "argument_count", "field_index"):
            if type(item[key]) is not int:
                raise Refusal("TARGET")
        actual = tuple(item[key] for key in ("line", "command", "argument_count", "local_or_material_id", "field_index", "role"))
        if actual != expected or item["segment"] != 1:
            raise Refusal("TARGET")
        for key in ("segment_sha256", "field_sha256"):
            if type(item[key]) is not str or not HEX.fullmatch(item[key]):
                raise Refusal("TARGET")
    return targets


def validate_allowlist(document):
    if type(document) is not dict or type(document.get("names")) is not list:
        raise Refusal("ALLOWLIST")
    names = document["names"]
    if not names or any(type(name) is not str or len(name) > 64 or not ELEMENT.fullmatch(name) or name != name.upper() for name in names):
        raise Refusal("ALLOWLIST")
    if names != sorted(set(names)):
        raise Refusal("ALLOWLIST")
    return frozenset(names)


def classify_selected(data, targets, names, splitter):
    """Split LF records, but parse exactly five declared records/fields only."""
    if type(data) is not bytes or len(data) > CAP:
        raise Refusal("CAP")
    if b"\x00" in data:
        raise Refusal("NUL")
    records = data.split(b"\n")
    if data.endswith(b"\n"):
        records.pop()
    # Length checks are integrity safeguards, not classification of other lines.
    if any(len(record) + 1 > LINE_CAP for record in records):
        raise Refusal("LINE_CAP")
    rows = []
    for target in validate_targets(targets):
        if target["line"] > len(records):
            raise Refusal("TARGET")
        text = records[target["line"] - 1].decode("latin1").rstrip("\r")
        segments, unclosed, _ = splitter(text, "$", comments=True)
        if unclosed or len(segments) < target["segment"]:
            raise Refusal("TARGET")
        segment = segments[target["segment"] - 1].strip()
        if sha(segment.encode("latin1")) != target["segment_sha256"]:
            raise Refusal("TARGET")
        fields, unclosed, _ = splitter(segment, ",")
        if unclosed or len(fields) - 1 != target["argument_count"]:
            raise Refusal("TARGET")
        if fields[0].strip().upper() != target["command"]:
            raise Refusal("TARGET")
        if target["command"] == "ET":
            local_id = fields[1].strip()
        else:
            if fields[1].strip().upper() != "DENS":
                raise Refusal("TARGET")
            local_id = fields[2].strip()
        if local_id != target["local_or_material_id"]:
            raise Refusal("TARGET")
        field = fields[target["field_index"]].strip()
        if sha(field.encode("utf-8")) != target["field_sha256"]:
            raise Refusal("TARGET")
        update = element_classification(field, names) if target["command"] == "ET" else {"classification": density_category(field)}
        rows.append({**target, **update})
    return rows


def control_bytes(helper, code_pin):
    if type(code_pin) is not str or not HEX.fullmatch(code_pin):
        raise Refusal("ARGUMENTS")
    pins = {"FOLLOWUP-PROTOCOL.md": PROTOCOL_PIN, "followup-targets.json": TARGET_PIN,
            "element-allowlist.json": LIST_PIN, "independent_parse.py": HELPER_PIN,
            "PROTOCOL.md": OLD_PROTOCOL_PIN, "independent_followup.py": code_pin}
    try:
        return {name: helper.read_guarded(HERE, name, pin) for name, pin in pins.items()}
    except helper.Refusal:
        raise Refusal("CONTROLS") from None


def historical(helper, protocol_pin, target_pin, list_pin, code_pin):
    if (protocol_pin, target_pin, list_pin) != (PROTOCOL_PIN, TARGET_PIN, LIST_PIN):
        raise Refusal("CONTROLS")
    controls = control_bytes(helper, code_pin)
    try:
        targets = validate_targets(json.loads(controls["followup-targets.json"]))
        names = validate_allowlist(json.loads(controls["element-allowlist.json"]))
    except (ValueError, TypeError):
        raise Refusal("CONTROLS") from None
    try:
        manifest = helper.read_guarded(helper.MANIFEST.parent, helper.MANIFEST.name, helper.MANIFEST_SHA, helper.MANIFEST_SIZE, cap=helper.MANIFEST_SIZE)
        relative = helper.manifest_candidate(manifest)
        data = helper.read_guarded(helper.SOURCE_BASE, relative, helper.SOURCE_SHA, helper.SOURCE_SIZE)
        rows = classify_selected(data, targets, names, helper._split)
        helper.read_guarded(helper.SOURCE_BASE, relative, helper.SOURCE_SHA, helper.SOURCE_SIZE)
        helper.read_guarded(helper.MANIFEST.parent, helper.MANIFEST.name, helper.MANIFEST_SHA, helper.MANIFEST_SIZE, cap=helper.MANIFEST_SIZE)
    except helper.Refusal:
        raise Refusal("SOURCE") from None
    if control_bytes(helper, code_pin) != controls:
        raise Refusal("CHANGED")
    return {"status": "ok", "scope": "five_field_lexical_only", "source_alias": "APDL01",
            "source_sha256": helper.SOURCE_SHA, "source_bytes": helper.SOURCE_SIZE,
            "source_name_sha256": helper.NAME_SHA, "manifest_sha256": helper.MANIFEST_SHA,
            "protocol_sha256": PROTOCOL_PIN, "targets_sha256": TARGET_PIN,
            "allowlist_sha256": LIST_PIN, "helper_sha256": HELPER_PIN, "code_sha256": code_pin,
            "pins_rechecked": True, "rows": rows}


def output_name(name):
    if type(name) is not str or not OUTPUT.fullmatch(name):
        raise Refusal("OUTPUT_PATH")


def output_preflight(name):
    output_name(name)
    directory = directory_fd(HERE)
    try:
        try:
            os.stat(name, dir_fd=directory, follow_symlinks=False)
        except FileNotFoundError:
            return
        raise Refusal("OUTPUT_EXISTS")
    except OSError:
        raise Refusal("OUTPUT_IO") from None
    finally:
        os.close(directory)


def save_receipt(name, value):
    output_name(name)
    data = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("ascii")
    directory, fd = directory_fd(HERE), None
    try:
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
        with os.fdopen(fd, "wb", closefd=False) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(fd)
    except FileExistsError:
        raise Refusal("OUTPUT_EXISTS") from None
    except OSError:
        raise Refusal("OUTPUT_IO") from None
    finally:
        if fd is not None:
            os.close(fd)
        os.close(directory)


def selftest(helper):
    checks = []

    def check(label, good):
        checks.append({"test": label, "passed": bool(good)})
        if not good:
            raise Refusal("SELFTEST")

    def refusal(label, operation, code):
        try:
            operation()
        except Refusal as error:
            check(label, error.code == code)
        else:
            check(label, False)

    examples = [
        ("", "blank"), (" \t\r\n", "blank"), ("x" * 257, "over_cap"),
        ("'" + "x" * 256, "over_cap"), ("'x'", "quote_bearing"), ('1+"x"', "quote_bearing"),
        ("-1.2D-3", "numeric_literal"), ("+.5E+03", "numeric_literal"), ("1.", "numeric_literal"),
        ("1" * 64, "numeric_literal"), ("1" * 65, "unsupported"),
        ("_a09", "identifier"), ("a" * 32, "identifier"), ("a" * 33, "unsupported"),
        ("(a)", "identifier_arithmetic"), ("(1)", "numeric_arithmetic"),
        ("1/0", "numeric_arithmetic"), ("1 + -2**3", "numeric_arithmetic"),
        ("a*(b-2.5D+1)/(-c)", "identifier_arithmetic"), ("1\t+\r\n2", "numeric_arithmetic"),
        ("1++2", "numeric_arithmetic"), ("1**-2", "numeric_arithmetic"),
        ("()", "unsupported"), ("(1)(2)", "unsupported"), ("a(1)", "unsupported"),
        ("1 2", "unsupported"), ("a b", "unsupported"), ("1***2", "unsupported"),
        ("1+", "unsupported"), ("+", "unsupported"), ("1,2", "unsupported"),
        ("%a%", "unsupported"), ("a[1]", "unsupported"), ("1==1", "unsupported"),
        ("1\v+2", "unsupported"), ("1\u00a0+2", "unsupported"), ("α+2", "unsupported"),
        ("１２", "unsupported"), ("1e", "unsupported"), (".e3", "unsupported"),
        ("0x10", "unsupported"), ("1_000", "unsupported"),
        ("(" * 16 + "1" + ")" * 16, "numeric_arithmetic"),
        ("(" * 17 + "1" + ")" * 17, "unsupported"),
        ("+" * 127 + "1", "numeric_arithmetic"), ("+" * 128 + "1", "unsupported"),
        ("(" + "a" * 32 + ")", "identifier_arithmetic"),
        ("(" + "a" * 33 + ")", "unsupported"),
        ("+" + "1" * 64, "numeric_arithmetic"),
    ]
    for index, (token, expected) in enumerate(examples):
        check("density_" + str(index), density_category(token) == expected)
    names = frozenset(("SOLID70", "BEAM188", "CONTA174"))
    for token in ("SOLID70", " solid70 ", "BEAM188", "CONTA174"):
        check("element_" + str(len(checks)), element_classification(token, names).get("name") == token.strip().upper())
    for token in ("'SOLID70'", "SOLID70x", "PRIVATE_SENTINEL999", "70", "SOLID 70", "ＳOLID70", "A" * 64 + "1"):
        check("nonmatch_" + str(len(checks)), element_classification(token, names) == {"classification": "unresolved"})
    # Synthetic fixture shares the fixed locator/argument contract, no native bytes.
    lines = [b"UNRELATED_PRIVATE_SENTINEL"] * 2654
    sample = ["ET,1,SOLID70,,,", "MP,DENS,1,PRIVATE_DENSITY+2", "MP,DENS,2,'A,$!''B'",
              "ET,2,BEAM188", "ET,5,CONTA174,,"]
    targets = []
    for expected, segment in zip(EXPECTED, sample):
        line, command, arguments, local, index, role = expected
        lines[line - 1] = (segment + " ! COMMENT_PRIVATE_SENTINEL").encode("latin1")
        fields, _, _ = helper._split(segment, ",")
        targets.append(dict(line=line, segment=1, command=command, argument_count=arguments,
                            local_or_material_id=local, field_index=index, role=role,
                            segment_sha256=sha(segment.encode("latin1")), field_sha256=sha(fields[index].strip().encode("utf-8"))))
    data = b"\n".join(lines)
    rows = classify_selected(data, targets, names, helper._split)
    check("exact_five_in_target_order", [r["line"] for r in rows] == [e[0] for e in EXPECTED])
    check("quote_delimiters_preserved", rows[2]["classification"] == "quote_bearing")
    check("density_shape_only", rows[1]["classification"] == "identifier_arithmetic" and "name" not in rows[1])
    check("privacy_sentinels_absent", "PRIVATE" not in json.dumps(rows) and "A,$!" not in json.dumps(rows))
    check("copied_target_hashes", all({k: r[k] for k in TARGET_KEYS} == t for r, t in zip(rows, targets)))
    check("output_schema_minimal", all(set(r) == TARGET_KEYS | {"classification"} | ({"name"} if r["command"] == "ET" else set()) for r in rows))
    for key, value in (("segment_sha256", "0" * 64), ("field_sha256", "0" * 64), ("argument_count", 4), ("local_or_material_id", "9"), ("field_index", 3), ("segment", 2), ("line", True)):
        changed = [dict(t) for t in targets]
        changed[0][key] = value
        refusal("target_mismatch_" + key, lambda: classify_selected(data, changed, names, helper._split), "TARGET")
    refusal("five_targets_required", lambda: classify_selected(data, targets[:-1], names, helper._split), "TARGET")
    refusal("nul_guard", lambda: classify_selected(data + b"\x00", targets, names, helper._split), "NUL")
    refusal("source_cap", lambda: classify_selected(b"x" * (CAP + 1), targets, names, helper._split), "CAP")
    refusal("line_cap", lambda: classify_selected(data + b"\n" + b"x" * LINE_CAP, targets, names, helper._split), "LINE_CAP")
    boundary = data + b"\n" + b"x" * (LINE_CAP - 1)
    check("line_cap_boundary", classify_selected(boundary, targets, names, helper._split) == rows)
    for label, badsegment in (("wrong_label", "MP,EX,1,PRIVATE_DENSITY+2"), ("wrong_command", "ET,DENS,1,PRIVATE_DENSITY+2")):
        modified = list(lines)
        modified[45] = badsegment.encode("latin1")
        changed = [dict(t) for t in targets]
        changed[1]["segment_sha256"] = sha(modified[45])
        refusal(label, lambda: classify_selected(b"\n".join(modified), changed, names, helper._split), "TARGET")
    # No native call: the altered protocol pin is rejected before control reads.
    refusal("protocol_gate_before_read", lambda: historical(None, "0" * 64, TARGET_PIN, LIST_PIN, "0" * 64), "CONTROLS")
    refusal("bad_code_pin", lambda: control_bytes(None, "not-a-hash"), "ARGUMENTS")
    class RejectingGuard:
        Refusal = helper.Refusal
        @staticmethod
        def read_guarded(*args, **kwargs):
            raise helper.Refusal("PIN")
    refusal("control_pin_failure", lambda: control_bytes(RejectingGuard, "0" * 64), "CONTROLS")
    for invalid in ({"names": ["SOLID70", "SOLID70"]}, {"names": ["solid70"]}, {"names": ["A-1"]}):
        refusal("bad_allowlist_" + str(len(checks)), lambda: validate_allowlist(invalid), "ALLOWLIST")
    for bad_name in ("../out.json", "followup-independent-run01.json/", "PRIVATE_SENTINEL", "producer-run01.json"):
        refusal("output_path_" + str(len(checks)), lambda: output_name(bad_name), "OUTPUT_PATH")
    with patch(__name__ + ".directory_fd", return_value=999), patch(__name__ + ".os.close"), patch(__name__ + ".os.stat", return_value=object()):
        refusal("preflight_exists", lambda: output_preflight("followup-independent-run01.json"), "OUTPUT_EXISTS")
    with patch(__name__ + ".directory_fd", return_value=999), patch(__name__ + ".os.close"), patch(__name__ + ".os.open", side_effect=FileExistsError):
        refusal("atomic_writer_exists", lambda: save_receipt("followup-independent-run01.json", {}), "OUTPUT_EXISTS")
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        status = main(["PRIVATE_CLI_SENTINEL"])
    check("cli_error_sanitized", status == 2 and stdout.getvalue() == "" and stderr.getvalue() == "REFUSED ARGUMENTS\n")
    return {"status": "ok", "scope": "synthetic_only", "native_reads": False, "tests": checks,
            "passed": len(checks), "helper_sha256": HELPER_PIN}


def main(arguments=None):
    args = sys.argv[1:] if arguments is None else arguments
    try:
        if len(args) in (1, 2) and args[0] == "selftest":
            if len(args) == 2:
                output_preflight(args[1])
            helper = bootstrap_helper()
            result = selftest(helper)
            if len(args) == 2:
                save_receipt(args[1], result)
            print("PASS SYNTHETIC " + str(result["passed"]))
            return 0
        if len(args) == 6 and args[0] == "historical":
            if not all(HEX.fullmatch(value) for value in args[1:5]):
                raise Refusal("ARGUMENTS")
            output_preflight(args[5])
            helper = bootstrap_helper()
            result = historical(helper, *args[1:5])
            save_receipt(args[5], result)
            print("PASS FIVE_FIELDS")
            return 0
        raise Refusal("ARGUMENTS")
    except Refusal as error:
        print("REFUSED " + error.code, file=sys.stderr)
        return 2
    except Exception:
        print("REFUSED UNEXPECTED", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

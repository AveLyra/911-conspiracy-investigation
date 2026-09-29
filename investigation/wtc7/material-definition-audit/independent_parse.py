#!/usr/bin/env python3
"""Independent, nonexecuting typed APDL01 audit. No producer/lexer imports.

Only synthetic mode is to be used until the parent approves the privacy gate.
Historical mode additionally checks the caller-supplied protocol and code pins.
All public failures use fixed codes; source paths and arbitrary tokens are never
printed. This program is a lexical field reader, not an APDL interpreter.
"""
from collections import Counter
import contextlib
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).absolute().parent
PROTOCOL = HERE / "PROTOCOL.md"
SOURCE_BASE = Path("/Users/admin/docs/911/exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539")
MANIFEST = Path("/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv")
MANIFEST_SHA = "30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf"
MANIFEST_SIZE = 4698031
SOURCE_SHA = "e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64"
NAME_SHA = "ff5c9a2bc8d8822fa9e3a1acaeb1becbab49aa2d5675c12f98b44261c1e00135"
SOURCE_SIZE = 212384
BYTE_CAP = 4 * 1024 * 1024
LINE_CAP = 16384
ROW_CAP = 10000
FIELD_CAP = 64

MP_LABELS = frozenset("C ENTH DENS KXX KYY KZZ EX EY EZ GXY GYZ GXZ PRXY PRYZ PRXZ NUXY NUYZ NUXZ ALPX ALPY ALPZ CTEX CTEY CTEZ THSX THSY THSZ REFT EMIS HF QRATE ALPD BETD DMPR DMPS MU".split())
TB_LABELS = frozenset("BISO BKIN MISO MKIN KINH PLASTIC ELASTIC MELAS CONCR CREEP DENS CTE THERM USER STATE COND ENTH SPHT FLSPHT LINEAR NONLINEAR".split())
SCHEMAS = {
    "MP": [("Lab", "mp_label"), ("MAT", "id")] + [(f"C{i}", "number") for i in range(5)],
    "MPDATA": [("Lab", "mp_label"), ("MAT", "id"), ("SLOC", "id")] + [(f"C{i}", "number") for i in range(1, 7)],
    "MPTEMP": [("SLOC", "id")] + [(f"T{i}", "number") for i in range(1, 7)],
    "TB": [("Lab", "tb_label"), ("MATID", "id"), ("NTEMP", "id"), ("NPTS", "id"), ("TBOPT", "tb_option"), ("reserved", "blank_only"), ("FuncName", "blank_only")],
    "TBTEMP": [("TEMP", "number"), ("KMOD", "id")],
    "TBDATA": [("STLOC", "id")] + [(f"C{i}", "number") for i in range(1, 7)],
    "ET": [("ITYPE", "id"), ("ENAME", "id")] + [(f"KOP{i}", "id") for i in range(1, 7)] + [("INOPR", "id")],
}
# Only names are counted; no argument of these nonselected commands is emitted.
CONTROL_IO = frozenset("*CFOPEN *CFCLOS *CFWRITE *VWRITE *MWRITE *VREAD *MREAD *SREAD *TREAD /INPUT *USE *ULIB CDREAD NREAD EREAD LDREAD RESUME FILE SET *CREATE *END /SYS /OUTPUT CDWRITE NWRITE EWRITE EDWRITE LSWRITE *IF *ELSE *ELSEIF *ENDIF *DO *ENDDO *DOWHILE *CYCLE *EXIT *GO *GET *VGET *SET *DIM SOLVE LSSOLVE ANTYPE /PREP7 /SOLU /SOLUTION /POST1 /POST26 FINISH SAVE PARSAV PARRES".split())
FORMAT_COMMANDS = frozenset(("*VWRITE", "*MWRITE", "*VREAD", "*MREAD"))
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eEdD][+-]?[0-9]+)?\Z", re.ASCII)
UNSIGNED = re.compile(r"[0-9]+\Z", re.ASCII)
HEX = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
OUTPUT_NAME = re.compile(r"independent-run[A-Za-z0-9_-]{1,64}\.json\Z", re.ASCII)
FAILURE_CODES = frozenset(("ARGUMENTS", "OUTPUT_PATH", "OUTPUT_EXISTS", "OUTPUT_IO", "PATH", "SYMLINK", "NOT_REGULAR", "SOURCE_CAP", "LINE_CAP", "ROW_CAP", "NUL", "PIN", "SIZE", "SOURCE_CHANGED", "MANIFEST_FORMAT", "SOURCE_SELECTION", "PROTOCOL_GATE", "CODE_GATE", "SELFTEST", "UNEXPECTED"))


class Refusal(Exception):
    def __init__(self, code):
        self.code = code if code in FAILURE_CODES else "UNEXPECTED"
        super().__init__(self.code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def hashed_field(text):
    return sha(text.strip().encode("utf-8"))


def _split(text, delimiter, comments=False):
    """Quote-aware split; doubled quotes stay in their original lexeme."""
    pieces, start, cursor, quote = [], 0, 0, None
    while cursor < len(text):
        char = text[cursor]
        if quote is not None:
            if char == quote:
                if cursor + 1 < len(text) and text[cursor + 1] == quote:
                    cursor += 2
                    continue
                quote = None
        elif char in "\"'":
            quote = char
        elif comments and char == "!":
            pieces.append(text[start:cursor])
            return pieces, False, True
        elif char == delimiter:
            pieces.append(text[start:cursor])
            start = cursor + 1
        cursor += 1
    pieces.append(text[start:])
    return pieces, quote is not None, False


def typed_field(value, kind):
    value = value.strip()
    if value == "":
        return {"kind": "blank"}
    if len(value) <= FIELD_CAP and "'" not in value and '"' not in value:
        if kind == "id" and UNSIGNED.fullmatch(value):
            return {"kind": "id", "value": value}
        if kind == "number" and NUMBER.fullmatch(value):
            return {"kind": "number", "value": value}
        upper = value.upper()
        if kind == "mp_label" and upper in MP_LABELS:
            return {"kind": "label", "value": upper}
        if kind in ("tb_label", "tb_option") and upper in TB_LABELS:
            return {"kind": "label", "value": upper}
        if kind == "tb_option" and UNSIGNED.fullmatch(value):
            return {"kind": "id", "value": value}
    return {"kind": "unresolved", "sha256": hashed_field(value)}


def selected_row(command, segment, line_number, slot, line_unclosed=False):
    parts, unclosed, _ = _split(segment, ",")
    arguments = parts[1:]
    schema = SCHEMAS[command]
    trailing = 0
    for value in reversed(arguments):
        if value.strip() != "":
            break
        trailing += 1
    reasons = []
    unsupported_form = parts[0].strip().upper() != command
    if unsupported_form:
        reasons.append("unsupported_command_form")
    if not arguments and command != "MPTEMP":
        reasons.append("no_arguments")
    if unclosed or line_unclosed:
        reasons.append("unmatched_quote")
    if len(arguments) > len(schema) and any(v.strip() for v in arguments[len(schema):]):
        reasons.append("extra_nonblank_fields")
    coded = command in ("MPDATA", "MPTEMP") and bool(arguments) and arguments[0].strip().upper() == "UNBL"
    if coded:
        reasons.append("coded_database_unbl")
    fields = []
    for index, (name, kind) in enumerate(schema):
        value = arguments[index] if index < len(arguments) else ""
        if (coded or unsupported_form) and value.strip():
            parsed = {"kind": "unresolved", "sha256": hashed_field(value)}
        else:
            parsed = typed_field(value, kind)
        if parsed["kind"] == "unresolved" and "unresolved_field" not in reasons:
            reasons.append("unresolved_field")
        fields.append({"field": name, **parsed})
    extra = [{"kind": "unresolved", "sha256": hashed_field(v)} for v in arguments[len(schema):] if v.strip()]
    return {
        "line": line_number, "segment": slot, "command": command,
        "segment_sha256": sha(segment.encode("latin1")),
        "argument_count": len(arguments), "trailing_blank_count": trailing,
        "extra_nonblank": extra, "status": "unresolved" if reasons else "decoded",
        "reasons": reasons, "fields": fields,
    }


def parse_bytes(data):
    if type(data) is not bytes:
        raise Refusal("UNEXPECTED")
    if len(data) > BYTE_CAP:
        raise Refusal("SOURCE_CAP")
    if b"\x00" in data:
        raise Refusal("NUL")
    physical = data.split(b"\n")
    if data.endswith(b"\n"):
        physical.pop()
    if not data:
        physical = []
    rows, formats, unknown = [], [], []
    counts, controls, unknown_counts = Counter(), Counter(), Counter()
    pending = False
    slots = 0
    for line_number, raw_line in enumerate(physical, 1):
        # Conservative shared convention reserves one LF byte on every record,
        # including a final record that does not physically have a trailing LF.
        if len(raw_line) + 1 > LINE_CAP:
            raise Refusal("LINE_CAP")
        text = raw_line.decode("latin1").rstrip("\r")
        if pending or text.lstrip().startswith("("):
            kind = "expected" if pending else "standalone"
            if pending and not text.lstrip().startswith(("(", "%")):
                kind = "unexpected_expected_format"
            formats.append({"line": line_number, "sha256": sha(raw_line), "status": kind})
            counts["format_lines"] += 1
            pending = False
            continue
        segments, unclosed, had_comment = _split(text, "$", comments=True)
        if had_comment:
            counts["lines_with_comments"] += 1
        if unclosed:
            counts["unmatched_quote_lines"] += 1
        if not any(part.strip() for part in segments):
            counts["empty_code_lines"] += 1
        for slot, raw_segment in enumerate(segments, 1):
            slots += 1
            segment = raw_segment.strip()
            if not segment:
                counts["empty_slots"] += 1
                continue
            pieces, _, _ = _split(segment, ",")
            token = pieces[0].strip()
            command = token.upper()
            if command not in SCHEMAS:
                leading = re.match(r"^([A-Za-z][A-Za-z0-9]*)(?=\s|$)", token, re.ASCII)
                if leading and leading.group(1).upper() in SCHEMAS:
                    command = leading.group(1).upper()
            counts["nonempty_segments"] += 1
            if command in SCHEMAS:
                rows.append(selected_row(command, segment, line_number, slot, unclosed))
                counts[command] += 1
                if len(rows) > ROW_CAP:
                    raise Refusal("ROW_CAP")
            elif command in CONTROL_IO:
                controls[command] += 1
                if command in FORMAT_COMMANDS:
                    pending = True
            else:
                token_hash = hashed_field(token)
                unknown_counts[token_hash] += 1
                unknown.append({"line": line_number, "segment": slot, "token_sha256": token_hash, "segment_sha256": sha(segment.encode("latin1")), "kind": "numeric_data" if len(token) <= FIELD_CAP and NUMBER.fullmatch(token) else "unrecognized_token"})
    if pending:
        counts["expected_format_missing_at_eof"] += 1
    return {
        "byte_count": len(data), "source_sha256": sha(data),
        "physical_lines": len(physical), "lf_count": data.count(b"\n"),
        "dollar_slots": slots, "counts": dict(sorted(counts.items())),
        "control_io_counts": dict(sorted(controls.items())),
        "unknown_token_counts": dict(sorted(unknown_counts.items())),
        "unknown_segments": unknown, "format_records": formats,
        "selected_rows": rows,
    }


def relative_parts(relative):
    if type(relative) is not str or not relative or "\\" in relative or "\x00" in relative:
        raise Refusal("PATH")
    parts = relative.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise Refusal("PATH")
    return parts


def _directory_fd(path):
    """Open an absolute directory chain without following any symlink."""
    if not path.is_absolute() or ".." in path.parts:
        raise Refusal("PATH")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            try:
                new_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            except OSError:
                raise Refusal("SYMLINK") from None
            os.close(fd)
            fd = new_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_guarded(root, relative, expected_hash, expected_size=None, cap=BYTE_CAP):
    parts = relative_parts(relative)
    parent = root.joinpath(*parts[:-1])
    directory = _directory_fd(parent)
    fd = None
    try:
        try:
            fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        except OSError:
            raise Refusal("PATH") from None
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise Refusal("NOT_REGULAR")
        if before.st_size > cap:
            raise Refusal("SOURCE_CAP")
        if expected_size is not None and before.st_size != expected_size:
            raise Refusal("SIZE")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(cap + 1)
        after = os.fstat(fd)
        if len(data) > cap:
            raise Refusal("SOURCE_CAP")
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            raise Refusal("SOURCE_CHANGED")
        if sha(data) != expected_hash:
            raise Refusal("PIN")
        if expected_size is not None and len(data) != expected_size:
            raise Refusal("SIZE")
        return data
    finally:
        if fd is not None:
            os.close(fd)
        os.close(directory)


def manifest_candidate(data):
    try:
        records = list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
        candidates = [r for r in records if r.get("extension", "").lower() == ".apdl"]
        matched = [r for r in records if r.get("sha256") == SOURCE_SHA and sha(r.get("filename", "").encode("utf-8")) == NAME_SHA]
        if len(candidates) != 3 or len(matched) != 1 or matched[0] != candidates[0]:
            raise Refusal("SOURCE_SELECTION")
        row = matched[0]
        relative = row["relative_path"]
        if relative_parts(relative)[-1] != row["filename"] or row["size_bytes"] != str(SOURCE_SIZE):
            raise Refusal("SOURCE_SELECTION")
        return relative
    except Refusal:
        raise
    except Exception:
        raise Refusal("MANIFEST_FORMAT") from None


def historical(protocol_pin, code_pin):
    if not HEX.fullmatch(protocol_pin) or not HEX.fullmatch(code_pin):
        raise Refusal("ARGUMENTS")
    try:
        read_guarded(HERE, "PROTOCOL.md", protocol_pin)
    except Refusal:
        raise Refusal("PROTOCOL_GATE") from None
    try:
        read_guarded(HERE, "independent_parse.py", code_pin)
    except Refusal:
        raise Refusal("CODE_GATE") from None
    manifest = read_guarded(MANIFEST.parent, MANIFEST.name, MANIFEST_SHA, MANIFEST_SIZE, cap=MANIFEST_SIZE)
    relative = manifest_candidate(manifest)
    data = read_guarded(SOURCE_BASE, relative, SOURCE_SHA, SOURCE_SIZE)
    result = parse_bytes(data)
    # No output exists until both source/manifest pins have been checked again.
    read_guarded(SOURCE_BASE, relative, SOURCE_SHA, SOURCE_SIZE)
    read_guarded(MANIFEST.parent, MANIFEST.name, MANIFEST_SHA, MANIFEST_SIZE, cap=MANIFEST_SIZE)
    read_guarded(HERE, "PROTOCOL.md", protocol_pin)
    read_guarded(HERE, "independent_parse.py", code_pin)
    return {"status": "ok", "mode": "historical_lexical_only", "source_alias": "APDL01", "source_name_sha256": NAME_SHA, "manifest_sha256": MANIFEST_SHA, "protocol_sha256": protocol_pin, "independent_code_sha256": code_pin, "source_and_manifest_pins_unchanged": True, "result": result}


def write_receipt(name, result):
    if type(name) is not str or not OUTPUT_NAME.fullmatch(name):
        raise Refusal("OUTPUT_PATH")
    # Construct all bytes before opening; never truncate an existing receipt.
    payload = (json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("ascii")
    directory = _directory_fd(HERE)
    fd = None
    try:
        try:
            fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
        except FileExistsError:
            raise Refusal("OUTPUT_EXISTS") from None
        except OSError:
            raise Refusal("OUTPUT_IO") from None
        with os.fdopen(fd, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(fd)
    except OSError:
        raise Refusal("OUTPUT_IO") from None
    finally:
        if fd is not None:
            os.close(fd)
        os.close(directory)


def output_preflight(name):
    if type(name) is not str or not OUTPUT_NAME.fullmatch(name):
        raise Refusal("OUTPUT_PATH")
    directory = _directory_fd(HERE)
    try:
        try:
            os.stat(name, dir_fd=directory, follow_symlinks=False)
        except FileNotFoundError:
            return
        except OSError:
            raise Refusal("OUTPUT_IO") from None
        raise Refusal("OUTPUT_EXISTS")
    finally:
        os.close(directory)


def selftest():
    checks = []

    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})
        if not condition:
            raise Refusal("SELFTEST")

    def row(text):
        return parse_bytes(text.encode("latin1"))["selected_rows"][0]

    def refuses(name, operation, code):
        try:
            operation()
        except Refusal as error:
            check(name, error.code == code)
        else:
            check(name, False)

    specimens = {
        "MP": "MP,EX,01,2.9D+07,0,-.1,1.,+2e-3",
        "MPDATA": "MPDATA,ENTH,1,2,0,1,2,3,4,5",
        "MPTEMP": "MPTEMP,1,0,25,100,300,600,1000",
        "TB": "TB,PLASTIC,1,2,3,MISO,,",
        "TBTEMP": "TBTEMP,2.5D2,1",
        "TBDATA": "TBDATA,1,0,1.0,-2,+3,4D+2,.5",
        "ET": "ET,1,70,0,1,2,3,4,5,6",
    }
    for command, text in specimens.items():
        parsed = row(text)
        check("schema_" + command, parsed["command"] == command and parsed["status"] == "decoded" and len(parsed["fields"]) == len(SCHEMAS[command]))
    check("numeric_lexeme_preservation", row(specimens["MP"])["fields"][2]["value"] == "2.9D+07")
    blank = row("MP,EX,,0")
    check("blank_distinct_zero", blank["fields"][1]["kind"] == "blank" and blank["fields"][2] == {"field": "C0", "kind": "number", "value": "0"})
    check("no_arguments_unresolved", row("MP")["status"] == "unresolved")
    check("mptemp_reset_no_arguments", row("MPTEMP")["status"] == "decoded")
    check("mptemp_reset_blank_arguments", row("MPTEMP,,,")["status"] == "decoded")
    check("argument_count_omitted", row("MP,EX")["argument_count"] == 1 and len(row("MP,EX")["fields"]) == 7)
    check("extra_trailing_blanks", row("TBTEMP,20,1,,,")["status"] == "decoded" and row("TBTEMP,20,1,,,")["trailing_blank_count"] == 3)
    check("extra_nonblank", row("TBTEMP,20,1,77")["status"] == "unresolved")
    check("tb_reserved_unresolved", row("TB,BISO,1,1,1,,3")["status"] == "unresolved")
    check("tb_function_unresolved", row("TB,BISO,1,1,1,,,9")["status"] == "unresolved")
    check("tb_unsigned_option", row("TB,BISO,1,1,1,2")["status"] == "decoded")
    check("quoted_label_unresolved", row("MP,'EX',1,2")["fields"][0]["kind"] == "unresolved")
    check("unknown_label_unresolved", row("MP,UNKNOWN_SENTINEL,1,2")["fields"][0]["kind"] == "unresolved")
    check("expression_unresolved", row("MP,C,1,2+3")["fields"][2]["kind"] == "unresolved")
    check("signed_id_unresolved", row("ET,-1,70")["status"] == "unresolved")
    check("text_element_unresolved", row("ET,1,SOLID70")["status"] == "unresolved")
    check("numeric_cap64", row("MP,C,1," + "1" * 64)["status"] == "decoded")
    check("numeric_cap65", row("MP,C,1," + "1" * 65)["status"] == "unresolved")
    for value in ("NaN", "inf", "1_000", "1e", ".", "0x10", "1 2"):
        check("bad_number_" + str(len(checks)), row("MP,C,1," + value)["status"] == "unresolved")
    parsed = parse_bytes(b"$MP,C,1,2$$ET,1,70 ! COMMENT_SENTINEL\n")
    check("all_dollar_slots", [(r["line"], r["segment"]) for r in parsed["selected_rows"]] == [(1, 2), (1, 4)])
    check("stripped_segment_sha", parsed["selected_rows"][1]["segment_sha256"] == sha(b"ET,1,70"))
    quote = parse_bytes(b"MP,C,1,'QUOTE!$SECRET''TAIL' $ET,1,70\n")
    check("quoted_separators_doubled", len(quote["selected_rows"]) == 2 and quote["selected_rows"][0]["status"] == "unresolved")
    quoted_comma = row("MP,C,1,'FIELD,WITH''QUOTE',3,4")
    check("quoted_comma_preserves_positions", quoted_comma["argument_count"] == 5 and quoted_comma["fields"][2]["kind"] == "unresolved" and quoted_comma["fields"][3]["value"] == "3" and quoted_comma["fields"][4]["value"] == "4")
    double_comma = row('MP,C,1,"FIELD,WITH""QUOTE",3')
    check("double_quoted_comma_preserves_positions", double_comma["argument_count"] == 4 and double_comma["fields"][2]["kind"] == "unresolved" and double_comma["fields"][3]["value"] == "3")
    check("unmatched_quote", "unmatched_quote" in row("MP,C,1,'UNFINISHED")["reasons"])
    malformed = row("MP EX,1,2")
    check("unsupported_command_form_retained", malformed["command"] == "MP" and "unsupported_command_form" in malformed["reasons"] and malformed["status"] == "unresolved")
    earlier = parse_bytes(b"MP,C,1,2 $ UNKNOWN,'UNFINISHED\n")["selected_rows"][0]
    check("unmatched_quote_line_marks_earlier_row", "unmatched_quote" in earlier["reasons"] and earlier["status"] == "unresolved")
    check("unbl_mpdata", "coded_database_unbl" in row("MPDATA,UNBL,EX,1,1,9")["reasons"])
    check("unbl_mptemp", "coded_database_unbl" in row("MPTEMP,UNBL,1,1,9")["reasons"])
    formatted = parse_bytes(b"*VWRITE,PRIVATE_SENTINEL\n('MP,C,1,9 ! $')\nMP,C,1,2\n")
    check("format_line_skipped", len(formatted["format_records"]) == 1 and len(formatted["selected_rows"]) == 1)
    check("standalone_format", len(parse_bytes(b"(F12.5)\n")["format_records"]) == 1)
    check("missing_format_eof", parse_bytes(b"*VREAD,a\n")["counts"]["expected_format_missing_at_eof"] == 1)
    check("unexpected_format_line", parse_bytes(b"*VWRITE,a\nMP,C,1,7\n")["format_records"][0]["status"] == "unexpected_expected_format")
    check("full_token_matching", len(parse_bytes(b"XMP,C,1,2\n")["selected_rows"]) == 0)
    privacy = json.dumps([parsed, quote, formatted, row("MP,UNKNOWN_SENTINEL,1,2"), parse_bytes(b"PRIVATE_COMMAND,/secret/path\n/INPUT,/secret/other\n")])
    check("privacy_sentinels_absent", not any(v in privacy for v in ("COMMENT_SENTINEL", "QUOTE", "SECRET", "TAIL", "PRIVATE_SENTINEL", "UNKNOWN_SENTINEL", "PRIVATE_COMMAND", "/secret/")))
    check("nonascii_unresolved_hash", typed_field("\u00e9", "number") == {"kind": "unresolved", "sha256": sha("\u00e9".encode("utf-8"))})
    refuses("source_byte_cap", lambda: parse_bytes(b" " * (BYTE_CAP + 1)), "SOURCE_CAP")
    refuses("line_byte_cap", lambda: parse_bytes(b" " * (LINE_CAP + 1)), "LINE_CAP")
    check("line_cap_with_reserved_lf_boundary", parse_bytes(b" " * (LINE_CAP - 1) + b"\n")["physical_lines"] == 1)
    refuses("line_cap_reserved_lf_over", lambda: parse_bytes(b" " * LINE_CAP), "LINE_CAP")
    refuses("selected_row_cap", lambda: parse_bytes(b"MP,C,1,2\n" * (ROW_CAP + 1)), "ROW_CAP")
    refuses("nul_refusal", lambda: parse_bytes(b"MP,C,1,2\x00"), "NUL")
    for value in ("../a", "/a", "a/../b", "a//b", "a\\b", "a/./b"):
        refuses("relative_path_refusal_" + str(len(checks)), lambda value=value: relative_parts(value), "PATH")
    refuses("output_scope_refusal", lambda: write_receipt("../independent-run-bad.json", {}), "OUTPUT_PATH")
    # Read only this owned implementation for real fd/hash guard controls.
    own_bytes = read_guarded(HERE, "independent_parse.py", sha(Path(__file__).read_bytes()))
    check("guarded_own_code_read", bool(own_bytes))
    refuses("source_pin_mismatch", lambda: read_guarded(HERE, "independent_parse.py", "0" * 64), "PIN")
    refuses("source_size_mismatch", lambda: read_guarded(HERE, "independent_parse.py", sha(own_bytes), 1), "SIZE")
    refuses("source_path_traversal", lambda: read_guarded(HERE, "../independent_parse.py", sha(own_bytes)), "PATH")
    # The task host's /tmp is a symlink to /private/tmp: metadata-only guard.
    check("symlink_control_available", Path("/tmp").is_symlink())
    refuses("symlink_directory_refusal", lambda: _directory_fd(Path("/tmp")), "SYMLINK")
    refuses("historical_protocol_gate", lambda: historical("0" * 64, "0" * 64), "PROTOCOL_GATE")
    protocol_hash = sha(PROTOCOL.read_bytes())
    refuses("historical_code_gate", lambda: historical(protocol_hash, "0" * 64), "CODE_GATE")
    refuses("manifest_no_candidate", lambda: manifest_candidate(b"relative_path,filename,extension,size_bytes,modified_time_utc,sha256\n"), "SOURCE_SELECTION")
    # Synthetic metadata stream: never opens the real manifest or native body.
    metadata = b"M" * (BYTE_CAP + 1)
    metadata_hash = sha(metadata)
    metadata_stat = SimpleNamespace(st_mode=stat.S_IFREG | 0o600, st_size=len(metadata), st_dev=1, st_ino=1, st_mtime_ns=0)
    with patch.dict(read_guarded.__globals__, {"_directory_fd": lambda path: 101}), patch("os.open", return_value=102), patch("os.close"), patch("os.fstat", return_value=metadata_stat), patch("os.fdopen", side_effect=lambda *args, **kwargs: io.BytesIO(metadata)):
        refuses("oversize_metadata_default_source_cap", lambda: read_guarded(HERE, "synthetic.json", metadata_hash), "SOURCE_CAP")
        check("explicit_metadata_cap", read_guarded(HERE, "synthetic.json", metadata_hash, len(metadata), cap=len(metadata)) == metadata)
    check("native_source_cap_unchanged", BYTE_CAP == 4 * 1024 * 1024)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_status = main(["UNTRUSTED_ARGUMENT_SENTINEL"])
    check("fixed_cli_failure", exit_status == 2 and json.loads(stdout.getvalue()) == {"status": "failure", "code": "ARGUMENTS"})
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_status = main(["synthetic", "UNTRUSTED_OUTPUT_SENTINEL"])
    check("fixed_output_failure", exit_status == 2 and json.loads(stdout.getvalue()) == {"status": "failure", "code": "OUTPUT_PATH"})
    return {"status": "ok", "mode": "synthetic_only", "historical_source_opened": False, "passed": len(checks), "checks": checks, "code_sha256": sha(own_bytes), "python_version": sys.version.split()[0]}


def main(arguments):
    output = None
    try:
        if len(arguments) == 2 and arguments[0] == "synthetic":
            output = arguments[1]
            output_preflight(output)
            result = selftest()
            write_receipt(output, result)
            # Actual create-only refusal is tested on the just-created receipt.
            try:
                write_receipt(output, {"status": "should_not_replace"})
            except Refusal as error:
                if error.code != "OUTPUT_EXISTS":
                    raise Refusal("SELFTEST") from None
            else:
                raise Refusal("SELFTEST")
            print(json.dumps({"status": "ok", "mode": "synthetic_only", "checks": result["passed"], "create_only_refusal": True}))
            return 0
        if len(arguments) == 4 and arguments[0] == "historical":
            output = arguments[1]
            output_preflight(output)
            result = historical(arguments[2], arguments[3])
            write_receipt(output, result)
            print(json.dumps({"status": "ok", "mode": "historical_lexical_only", "rows": len(result["result"]["selected_rows"])}))
            return 0
        raise Refusal("ARGUMENTS")
    except BaseException as error:
        code = error.code if isinstance(error, Refusal) else "UNEXPECTED"
        failure = {"status": "failure", "code": code}
        if output is not None and OUTPUT_NAME.fullmatch(output):
            try:
                write_receipt(output, failure)
            except BaseException:
                pass
        print(json.dumps(failure))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

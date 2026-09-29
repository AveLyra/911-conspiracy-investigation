from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .core import (
    CRWError,
    EvidenceStore,
    SCHEMAS,
    canonical_json,
    create_derivative,
    import_manifests,
    reproduce_derivative,
    utc_now,
    validate_json_file,
)


ROLES = [
    "preserved_source",
    "access_copy",
    "analysis_derivative",
    "comparator_source",
    "model_package",
    "document",
]


def _print(value: Any) -> None:
    sys.stdout.write(canonical_json(value))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crw",
        description="CRW immutable evidence and provenance core",
    )
    parser.add_argument("--version", action="version", version="crw 0.1.0")
    commands = parser.add_subparsers(dest="command", required=True)

    schema = commands.add_parser("schema", help="Validate machine-readable contracts")
    schema_commands = schema.add_subparsers(dest="schema_command", required=True)
    validate = schema_commands.add_parser("validate", help="Validate a JSON object")
    validate.add_argument("path", type=Path)
    validate.add_argument("--schema", required=True, choices=sorted(SCHEMAS))

    evidence = commands.add_parser("evidence", help="Ingest and verify evidence")
    evidence_commands = evidence.add_subparsers(
        dest="evidence_command", required=True
    )
    ingest = evidence_commands.add_parser(
        "ingest", help="Copy bytes into a content-addressed store"
    )
    ingest.add_argument("path", type=Path)
    ingest.add_argument("--store", type=Path, required=True)
    ingest.add_argument("--id", required=True)
    ingest.add_argument("--event-id", required=True)
    ingest.add_argument("--role", choices=ROLES, required=True)
    ingest.add_argument("--acquired-at", default=None)
    ingest.add_argument("--title")
    ingest.add_argument("--source-page")
    ingest.add_argument("--retrieval-uri")
    ingest.add_argument("--authenticity-status", default="unknown")
    ingest.add_argument("--preservation-tier")
    ingest.add_argument("--limitation", action="append", default=[])

    verify = evidence_commands.add_parser(
        "verify", help="Check registered bytes against hashes"
    )
    verify.add_argument("--store", type=Path, required=True)
    verify.add_argument("--id")

    manifest = commands.add_parser(
        "manifest", help="Import manifests without normalizing their fields"
    )
    manifest_commands = manifest.add_subparsers(
        dest="manifest_command", required=True
    )
    import_command = manifest_commands.add_parser(
        "import", help="Preserve rows and emit path/hash reconciliation"
    )
    import_command.add_argument("manifests", type=Path, nargs="+")
    import_command.add_argument("--output", type=Path)

    derivative = commands.add_parser(
        "derivative", help="Create or reproduce registered derivatives"
    )
    derivative_commands = derivative.add_subparsers(
        dest="derivative_command", required=True
    )
    for kind in ("audio", "frames"):
        derive = derivative_commands.add_parser(
            kind, help=f"Create a reproducible {kind} derivative"
        )
        derive.add_argument("--store", type=Path, required=True)
        derive.add_argument("--parent-id", required=True)
        derive.add_argument("--id", required=True)
        derive.add_argument("--limitation")
    reproduce = derivative_commands.add_parser(
        "reproduce", help="Rerun a derivative recipe and compare its hash"
    )
    reproduce.add_argument("--store", type=Path, required=True)
    reproduce.add_argument("--id", required=True)
    return parser


def execute(args: argparse.Namespace) -> int:
    if args.command == "schema":
        errors = validate_json_file(args.path, args.schema)
        _print(
            {
                "path": str(args.path),
                "schema": args.schema,
                "valid": not errors,
                "errors": errors,
            }
        )
        return 0 if not errors else 1

    if args.command == "evidence":
        store = EvidenceStore(args.store)
        if args.evidence_command == "ingest":
            record, duplicate = store.ingest(
                args.path,
                object_id=args.id,
                event_id=args.event_id,
                role=args.role,
                acquired_at=args.acquired_at or utc_now(),
                title=args.title,
                source_page=args.source_page,
                retrieval_uri=args.retrieval_uri,
                authenticity_status=args.authenticity_status,
                preservation_tier=args.preservation_tier,
                limitations=args.limitation,
            )
            _print({"duplicate": duplicate, "record": record})
            return 0
        report = store.verify(args.id)
        _print(report)
        return 0 if report["ok"] else 1

    if args.command == "manifest":
        report = import_manifests(args.manifests)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(canonical_json(report), encoding="utf-8")
        _print(report)
        return 0 if report["totals"]["mismatch"] == 0 else 1

    if args.command == "derivative":
        store = EvidenceStore(args.store)
        if args.derivative_command in {"audio", "frames"}:
            record, duplicate = create_derivative(
                store,
                parent_id=args.parent_id,
                derivative_id=args.id,
                kind=args.derivative_command,
                limitation=args.limitation,
            )
            _print({"duplicate": duplicate, "record": record})
            return 0
        report = reproduce_derivative(store, args.id)
        _print(report)
        return 0 if report["reproduced"] else 1

    raise CRWError(f"Unhandled command: {args.command}")


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    try:
        code = execute(parser.parse_args(argv))
    except CRWError as exc:
        parser.exit(2, f"crw: error: {exc}\n")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.exit(2, f"crw: error: {exc}\n")
    raise SystemExit(code)


if __name__ == "__main__":
    main()

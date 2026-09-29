from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = PROJECT_ROOT / "schemas"
SCHEMAS = {
    "evidence-object": SCHEMA_DIR / "evidence-object.schema.json",
    "observation": SCHEMA_DIR / "observation.schema.json",
    "scenario-run": SCHEMA_DIR / "scenario-run.schema.json",
}


class CRWError(RuntimeError):
    """Expected command failure with a user-facing message."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def validate_data(data: Any, schema_name: str) -> list[str]:
    try:
        schema_path = SCHEMAS[schema_name]
    except KeyError as exc:
        raise CRWError(
            f"Unknown schema {schema_name!r}; choose one of {', '.join(SCHEMAS)}"
        ) from exc
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    messages: list[str] = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path)):
        path = "$"
        for part in error.absolute_path:
            path += f"[{part}]" if isinstance(part, int) else f".{part}"
        messages.append(f"{path}: {error.message}")
    return messages


def validate_json_file(path: Path, schema_name: str) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CRWError(f"Cannot read JSON object {path}: {exc}") from exc
    return validate_data(data, schema_name)


class EvidenceStore:
    """Content-addressed byte store plus immutable evidence records."""

    def __init__(self, root: Path):
        self.root = root.resolve()
        self.blobs = self.root / "blobs" / "sha256"
        self.records = self.root / "records"

    def initialize(self) -> None:
        self.blobs.mkdir(parents=True, exist_ok=True)
        self.records.mkdir(parents=True, exist_ok=True)

    def blob_path(self, digest: str) -> Path:
        return self.blobs / digest[:2] / digest

    def record_path(self, object_id: str) -> Path:
        return self.records / f"{object_id}.json"

    def read_record(self, object_id: str) -> dict[str, Any]:
        path = self.record_path(object_id)
        if not path.is_file():
            raise CRWError(f"Evidence record does not exist: {object_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _preserve_blob(self, source: Path) -> tuple[str, int, bool]:
        if not source.is_file():
            raise CRWError(f"Input is not a file: {source}")
        digest, size = sha256_file(source)
        target = self.blob_path(digest)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            actual_digest, actual_size = sha256_file(target)
            if actual_digest != digest or actual_size != size:
                raise CRWError(f"Stored blob is corrupt and will not be overwritten: {target}")
            return digest, size, True

        temporary = target.with_name(f".{digest}.{os.getpid()}.tmp")
        try:
            with source.open("rb") as incoming, temporary.open("xb") as outgoing:
                shutil.copyfileobj(incoming, outgoing, length=1024 * 1024)
                outgoing.flush()
                os.fsync(outgoing.fileno())
            copied_digest, copied_size = sha256_file(temporary)
            if (copied_digest, copied_size) != (digest, size):
                raise CRWError("Input changed while it was being ingested")
            try:
                os.link(temporary, target)
                duplicate = False
            except FileExistsError:
                stored_digest, stored_size = sha256_file(target)
                if (stored_digest, stored_size) != (digest, size):
                    raise CRWError(
                        f"Concurrent ingest produced a corrupt blob: {target}"
                    )
                duplicate = True
            target.chmod(0o444)
            return digest, size, duplicate
        finally:
            temporary.unlink(missing_ok=True)

    def _write_record(self, record: dict[str, Any]) -> bool:
        errors = validate_data(record, "evidence-object")
        if errors:
            raise CRWError("Invalid evidence record:\n" + "\n".join(errors))
        target = self.record_path(record["id"])
        self.records.mkdir(parents=True, exist_ok=True)
        if target.exists():
            existing = json.loads(target.read_text(encoding="utf-8"))
            if existing["sha256"] != record["sha256"]:
                raise CRWError(
                    f"Immutable ID {record['id']} already identifies different bytes"
                )
            return True
        try:
            with target.open("x", encoding="utf-8") as stream:
                stream.write(canonical_json(record))
                stream.flush()
                os.fsync(stream.fileno())
        except FileExistsError:
            existing = json.loads(target.read_text(encoding="utf-8"))
            if existing["sha256"] != record["sha256"]:
                raise CRWError(
                    f"Immutable ID {record['id']} was concurrently registered"
                )
            return True
        target.chmod(0o444)
        return False

    def ingest(
        self,
        source: Path,
        *,
        object_id: str,
        event_id: str,
        role: str,
        acquired_at: str,
        title: str | None = None,
        source_page: str | None = None,
        retrieval_uri: str | None = None,
        authenticity_status: str = "unknown",
        preservation_tier: str | None = None,
        limitations: Iterable[str] = (),
        technical: dict[str, Any] | None = None,
        lineage: list[dict[str, Any]] | None = None,
    ) -> tuple[dict[str, Any], bool]:
        self.initialize()
        digest, size, blob_duplicate = self._preserve_blob(source)
        record: dict[str, Any] = {
            "id": object_id,
            "event_id": event_id,
            "role": role,
            "title": title or source.name,
            "local_path": str(self.blob_path(digest).relative_to(self.root)),
            "sha256": digest,
            "bytes": size,
            "acquired_at": acquired_at,
            "authenticity_status": authenticity_status,
            "technical": technical or {},
            "lineage": lineage or [],
            "limitations": list(limitations),
            "redistribution_status": None,
        }
        if source_page:
            record["source_page"] = source_page
        if retrieval_uri:
            record["retrieval_uri"] = retrieval_uri
        if preservation_tier:
            record["preservation_tier"] = preservation_tier
        record_duplicate = self._write_record(record)
        return self.read_record(object_id), blob_duplicate or record_duplicate

    def verify(self, object_id: str | None = None) -> dict[str, Any]:
        self.initialize()
        paths = (
            [self.record_path(object_id)]
            if object_id
            else sorted(self.records.glob("*.json"))
        )
        results = []
        for path in paths:
            if not path.is_file():
                results.append(
                    {"id": object_id, "status": "missing_record", "path": str(path)}
                )
                continue
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
                schema_errors = validate_data(record, "evidence-object")
                blob = self.root / record["local_path"]
                if not blob.is_file():
                    status = "missing_blob"
                    actual_hash = None
                    actual_size = None
                else:
                    actual_hash, actual_size = sha256_file(blob)
                    status = (
                        "ok"
                        if actual_hash == record["sha256"]
                        and actual_size == record["bytes"]
                        else "mismatch"
                    )
                if schema_errors:
                    status = "invalid_record"
                results.append(
                    {
                        "id": record.get("id"),
                        "status": status,
                        "expected_sha256": record.get("sha256"),
                        "actual_sha256": actual_hash,
                        "expected_bytes": record.get("bytes"),
                        "actual_bytes": actual_size,
                        "schema_errors": schema_errors,
                    }
                )
            except (OSError, json.JSONDecodeError, KeyError) as exc:
                results.append(
                    {"id": path.stem, "status": "invalid_record", "error": str(exc)}
                )
        return {
            "store": str(self.root),
            "checked": len(results),
            "ok": all(item["status"] == "ok" for item in results),
            "results": results,
        }


def _is_remote(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https", "ftp"}


def import_manifests(manifests: Iterable[Path]) -> dict[str, Any]:
    imported = []
    totals = {"rows": 0, "available": 0, "missing": 0, "remote": 0, "mismatch": 0}
    for manifest in manifests:
        manifest = manifest.resolve()
        with manifest.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            headers = reader.fieldnames or []
            rows = list(reader)
        reconciliation = []
        for index, row in enumerate(rows, start=2):
            path_value = row.get("local_path") or row.get("url_or_repo_path") or ""
            expected_hash = row.get("sha256") or ""
            expected_bytes = row.get("bytes") or ""
            if not path_value:
                status = "no_path"
                resolved = None
            elif _is_remote(path_value):
                status = "remote"
                resolved = None
                totals["remote"] += 1
            else:
                candidate = (manifest.parent / path_value).resolve()
                resolved = str(candidate)
                if not candidate.is_file():
                    status = "missing"
                    totals["missing"] += 1
                else:
                    actual_hash, actual_bytes = sha256_file(candidate)
                    hash_matches = not expected_hash or actual_hash == expected_hash
                    bytes_matches = not expected_bytes or actual_bytes == int(expected_bytes)
                    status = "available" if hash_matches and bytes_matches else "mismatch"
                    totals[status] += 1
            reconciliation.append(
                {
                    "row": index,
                    "id": row.get("record_id") or row.get("id"),
                    "path": path_value,
                    "resolved_path": resolved,
                    "status": status,
                }
            )
        totals["rows"] += len(rows)
        imported.append(
            {
                "manifest": str(manifest),
                "sha256": sha256_file(manifest)[0],
                "headers": headers,
                "row_count": len(rows),
                "rows": rows,
                "reconciliation": reconciliation,
            }
        )
    return {
        "format": "crw-manifest-import-v1",
        "created_at": utc_now(),
        "totals": totals,
        "manifests": imported,
    }


def ffmpeg_version() -> str:
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CRWError("ffmpeg is required for media derivatives") from exc
    return result.stdout.splitlines()[0]


def _run(command: list[str]) -> None:
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise CRWError(f"Required tool is unavailable: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise CRWError(f"Command failed: {detail}") from exc


def _deterministic_zip(directory: Path, target: Path) -> None:
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_STORED) as archive:
        for path in sorted(directory.glob("frame-*.png")):
            info = zipfile.ZipInfo(path.name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def _execute_recipe(parent: Path, kind: str, destination: Path) -> list[str]:
    if kind == "audio":
        command = [
            "ffmpeg",
            "-v",
            "error",
            "-nostdin",
            "-i",
            str(parent),
            "-map",
            "0:a:0",
            "-vn",
            "-c:a",
            "pcm_s16le",
            "-fflags",
            "+bitexact",
            "-flags:a",
            "+bitexact",
            "-map_metadata",
            "-1",
            "-y",
            str(destination),
        ]
        _run(command)
        return command
    if kind == "frames":
        frame_dir = destination.parent / "frames"
        frame_dir.mkdir()
        pattern = frame_dir / "frame-%08d.png"
        command = [
            "ffmpeg",
            "-v",
            "error",
            "-nostdin",
            "-i",
            str(parent),
            "-map",
            "0:v:0",
            "-fps_mode",
            "passthrough",
            "-start_number",
            "0",
            "-map_metadata",
            "-1",
            "-y",
            str(pattern),
        ]
        _run(command)
        _deterministic_zip(frame_dir, destination)
        return command
    raise CRWError(f"Unknown derivative kind: {kind}")


def create_derivative(
    store: EvidenceStore,
    *,
    parent_id: str,
    derivative_id: str,
    kind: str,
    limitation: str | None = None,
) -> tuple[dict[str, Any], bool]:
    parent_record = store.read_record(parent_id)
    parent_path = store.root / parent_record["local_path"]
    verification = store.verify(parent_id)
    if not verification["ok"]:
        raise CRWError(f"Parent {parent_id} failed integrity verification")
    suffix = ".wav" if kind == "audio" else ".zip"
    with tempfile.TemporaryDirectory(prefix="crw-derivative-") as temporary:
        output = Path(temporary) / f"output{suffix}"
        rendered_command = _execute_recipe(parent_path, kind, output)
        created_at = utc_now()
        recipe = {
            "kind": kind,
            "argv_template": [
                "{tool}" if item == "ffmpeg" else "{input}" if item == str(parent_path)
                else "{output}" if item == str(output)
                else "{frame_pattern}" if item.endswith("frame-%08d.png")
                else item
                for item in rendered_command
            ],
            "rendered_argv": rendered_command,
            "packaging": "deterministic-zip-v1" if kind == "frames" else None,
        }
        technical = {
            "derivative_kind": "audio_extraction"
            if kind == "audio"
            else "frame_sequence",
            "recipe": recipe,
            "environment": {
                "python": sys.version.split()[0],
                "platform": platform.platform(),
                "ffmpeg": ffmpeg_version(),
            },
        }
        lineage = [
            {
                "parent_id": parent_id,
                "relation": "extracted_from" if kind == "audio" else "decoded_from",
                "transformation": {
                    "tool": "ffmpeg",
                    "version": technical["environment"]["ffmpeg"],
                    "configuration_uri": "embedded:technical.recipe",
                    "operator": "crw",
                    "created_at": created_at,
                },
            }
        ]
        limitations = [
            limitation
            or (
                "Lossless PCM extraction from the preserved parent; no claim of "
                "native or calibrated source audio."
                if kind == "audio"
                else "Decoded PNG frame sequence; timestamps and source edits require separate analysis."
            )
        ]
        return store.ingest(
            output,
            object_id=derivative_id,
            event_id=parent_record["event_id"],
            role="analysis_derivative",
            acquired_at=created_at,
            title=f"{kind} derivative of {parent_id}",
            authenticity_status=parent_record["authenticity_status"],
            preservation_tier="derived",
            limitations=limitations,
            technical=technical,
            lineage=lineage,
        )


def reproduce_derivative(store: EvidenceStore, derivative_id: str) -> dict[str, Any]:
    derivative = store.read_record(derivative_id)
    lineage = derivative.get("lineage") or []
    if len(lineage) != 1:
        raise CRWError("Reproduction currently requires exactly one parent")
    parent_id = lineage[0]["parent_id"]
    parent = store.read_record(parent_id)
    if not store.verify(parent_id)["ok"]:
        raise CRWError(f"Parent {parent_id} failed integrity verification")
    kind = derivative.get("technical", {}).get("recipe", {}).get("kind")
    parent_path = store.root / parent["local_path"]
    suffix = ".wav" if kind == "audio" else ".zip"
    with tempfile.TemporaryDirectory(prefix="crw-reproduce-") as temporary:
        output = Path(temporary) / f"reproduced{suffix}"
        command = _execute_recipe(parent_path, kind, output)
        actual_hash, actual_bytes = sha256_file(output)
    return {
        "id": derivative_id,
        "parent_id": parent_id,
        "kind": kind,
        "command": command,
        "expected_sha256": derivative["sha256"],
        "actual_sha256": actual_hash,
        "expected_bytes": derivative["bytes"],
        "actual_bytes": actual_bytes,
        "reproduced": actual_hash == derivative["sha256"]
        and actual_bytes == derivative["bytes"],
    }

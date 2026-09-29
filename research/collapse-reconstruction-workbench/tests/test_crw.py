from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from crw.cli import build_parser
from crw.core import (
    CRWError,
    EvidenceStore,
    PROJECT_ROOT,
    create_derivative,
    import_manifests,
    reproduce_derivative,
    validate_json_file,
)


@pytest.mark.parametrize(
    ("fixture", "schema"),
    [
        ("synthetic-evidence.json", "evidence-object"),
        ("synthetic-observation.json", "observation"),
        ("synthetic-scenario-run.json", "scenario-run"),
    ],
)
def test_synthetic_fixtures_validate(fixture: str, schema: str) -> None:
    assert not validate_json_file(PROJECT_ROOT / "examples" / fixture, schema)


def test_schema_errors_include_object_path(tmp_path: Path) -> None:
    source = PROJECT_ROOT / "examples" / "synthetic-evidence.json"
    malformed = json.loads(source.read_text(encoding="utf-8"))
    malformed["sha256"] = "not-a-digest"
    path = tmp_path / "malformed.json"
    path.write_text(json.dumps(malformed), encoding="utf-8")

    errors = validate_json_file(path, "evidence-object")

    assert errors
    assert errors[0].startswith("$.sha256:")


def test_help_parser_is_available() -> None:
    parser = build_parser()
    assert "immutable evidence" in parser.format_help()


def _ingest(store: EvidenceStore, source: Path, object_id: str) -> dict:
    record, _ = store.ingest(
        source,
        object_id=object_id,
        event_id="EVT-SYNTH-TEST",
        role="preserved_source",
        acquired_at="2026-09-05T12:00:00Z",
        authenticity_status="authenticated",
        preservation_tier="native_claimed",
        limitations=["Synthetic test bytes."],
    )
    return record


def test_ingest_deduplicates_and_rejects_id_overwrite(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path / "store")
    first = tmp_path / "first.bin"
    same = tmp_path / "same.bin"
    changed = tmp_path / "changed.bin"
    first.write_bytes(b"preserved bytes")
    same.write_bytes(b"preserved bytes")
    changed.write_bytes(b"different bytes")

    first_record = _ingest(store, first, "EVD-SYNTH-FIRST")
    second_record = _ingest(store, same, "EVD-SYNTH-SECOND")
    _, duplicate = store.ingest(
        same,
        object_id="EVD-SYNTH-SECOND",
        event_id="EVT-SYNTH-TEST",
        role="preserved_source",
        acquired_at="2026-09-05T12:00:00Z",
        authenticity_status="authenticated",
        limitations=["Synthetic test bytes."],
    )

    assert first_record["sha256"] == second_record["sha256"]
    assert first_record["local_path"] == second_record["local_path"]
    assert duplicate
    with pytest.raises(CRWError, match="different bytes"):
        _ingest(store, changed, "EVD-SYNTH-FIRST")


def test_verification_detects_deliberate_alteration(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path / "store")
    source = tmp_path / "source.bin"
    source.write_bytes(b"original")
    record = _ingest(store, source, "EVD-SYNTH-ALTER")
    blob = store.root / record["local_path"]
    blob.chmod(0o644)
    blob.write_bytes(b"altered")

    report = store.verify("EVD-SYNTH-ALTER")

    assert not report["ok"]
    assert report["results"][0]["status"] == "mismatch"


def test_manifest_import_preserves_fields_and_reports_missing(tmp_path: Path) -> None:
    available = tmp_path / "available.bin"
    available.write_bytes(b"available")
    manifest = tmp_path / "manifest.csv"
    manifest.write_text(
        "id,url_or_repo_path,limitations\n"
        'ONE,available.bin,"comma, retained"\n'
        "TWO,missing.bin,unavailable\n"
        "THREE,https://example.invalid/source,remote\n",
        encoding="utf-8",
    )

    report = import_manifests([manifest])

    imported = report["manifests"][0]
    assert imported["headers"] == ["id", "url_or_repo_path", "limitations"]
    assert imported["rows"][0]["limitations"] == "comma, retained"
    assert report["totals"]["rows"] == 3
    assert report["totals"]["available"] == 1
    assert report["totals"]["missing"] == 1
    assert report["totals"]["remote"] == 1


@pytest.fixture
def synthetic_media(tmp_path: Path) -> Path:
    if shutil.which("ffmpeg") is None:
        pytest.skip("ffmpeg is not installed")
    target = tmp_path / "synthetic.mp4"
    command = [
        "ffmpeg",
        "-v",
        "error",
        "-f",
        "lavfi",
        "-i",
        "testsrc=size=32x32:rate=2",
        "-f",
        "lavfi",
        "-i",
        "sine=frequency=440:sample_rate=8000",
        "-t",
        "1",
        "-c:v",
        "mpeg4",
        "-c:a",
        "aac",
        "-shortest",
        str(target),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    return target


def test_audio_and_frames_reproduce(
    tmp_path: Path, synthetic_media: Path
) -> None:
    store = EvidenceStore(tmp_path / "store")
    _ingest(store, synthetic_media, "EVD-SYNTH-MEDIA")

    audio, _ = create_derivative(
        store,
        parent_id="EVD-SYNTH-MEDIA",
        derivative_id="DRV-SYNTH-AUDIO",
        kind="audio",
    )
    frames, _ = create_derivative(
        store,
        parent_id="EVD-SYNTH-MEDIA",
        derivative_id="DRV-SYNTH-FRAMES",
        kind="frames",
    )

    assert audio["technical"]["recipe"]["argv_template"]
    assert frames["technical"]["recipe"]["packaging"] == "deterministic-zip-v1"
    assert reproduce_derivative(store, audio["id"])["reproduced"]
    assert reproduce_derivative(store, frames["id"])["reproduced"]

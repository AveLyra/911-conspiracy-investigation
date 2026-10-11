"""Fixed B/C/D speech hypotheses using the verified local GPU route."""
import json
import math
import platform
import subprocess
import sys
import time
import wave
from datetime import datetime, timezone
from pathlib import Path

from run_asr import BASE, ENV, PINS, check_pins, digest

SOURCE_DIR = PINS["source"][0].parent
CLIPS = [
    ("B", "msnbc", 38, 578, "VID-WTC7-007", "b9758e82432a354fc584b22529b03c84aefc7b192d8579d5b8f95de3b715b292"),
    ("C", "edited", 25, 430, "VID-WTC7-007", "b8557ab9a0f2ac6dc9d3d59d0334de96431340ad34f2e5642c47a5a51a3a09dd"),
    ("D", "comparator", 17, 8, "VID-DEM-002", "2a846dcd29fe82f32f5c0694afd05c99a6c5a6923dae78c5c1ccbf1dc7eb59d0"),
]


def validate(data, duration):
    rows = data.get("transcription")
    if not isinstance(rows, list):
        raise ValueError("Missing/non-list transcription")
    previous = 0
    for row in rows:
        start, end = row["offsets"]["from"], row["offsets"]["to"]
        if (type(start) not in (int, float) or type(end) not in (int, float)
                or not math.isfinite(start) or not math.isfinite(end)
                or not 0 <= previous <= start <= end <= duration * 1000
                or not isinstance(row["text"], str)):
            raise ValueError("Invalid segment or timing")
        previous = end
    return rows


def arguments(audio, prefix):
    return list(map(str, [PINS["whisper"][0], "-m", PINS["model"][0], "-f", audio,
        "-l", "en", "-t", "4", "-p", "1", "-tp", "0", "-nf", "-bs", "5", "-bo", "5",
        "-ojf", "-otxt", "-osrt", "-of", prefix]))


def sources():
    result = {}
    for key, name, duration, start, source_id, expected in CLIPS:
        path = SOURCE_DIR / f"{name}-stereo.wav"
        actual = digest(path)
        if actual != expected:
            raise ValueError(f"Changed source {key}")
        result[key] = {"path": str(path), "sha256": actual, "bytes": path.stat().st_size,
                       "duration_seconds": duration, "track_start_seconds": start, "source_id": source_id}
    return result


def self_test():
    def row(start, end, text="invented"):
        return {"offsets": {"from": start, "to": end}, "text": text}
    valid = [[], [row(0, 38000)], [row(100, 200), row(300, 400)]]
    invalid = [{}, {"transcription": None}] + [
        {"transcription": value} for value in ([row(0, 38001)], [row(-1, 1)],
        [row(3, 2)], [row(0, 10), row(9, 20)], [row(False, 3)],
        [row(0, float("nan"))], [row("0", 3)], [row(0, 1, None)])]
    for rows in valid:
        validate({"transcription": rows}, 38)
    for case in invalid:
        try:
            validate(case, 38)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError("Invalid case accepted")
    old = json.loads((BASE / "run02-gpu/receipt.json").read_text())["commands"][0]["argv"]
    old[old.index("-f") + 1] = "AUDIO"
    old[old.index("-of") + 1] = "PREFIX"
    assert arguments("AUDIO", "PREFIX") == old
    print(f"PASS: {len(valid)} valid, {len(invalid)} invalid invented cases; decoding args match A")


def main():
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return
    if sys.argv[1:]:
        raise ValueError("Only the fixed batch is supported")
    run = BASE / "run03-bcd"
    run.mkdir(exist_ok=False)
    receipt = {"started_at_utc": datetime.now(timezone.utc).isoformat(), "status": "running",
        "python": sys.version, "platform": platform.platform(), "environment": ENV,
        "runner_sha256": digest(Path(__file__)), "shared_runner_sha256": digest(BASE / "run_asr.py"),
        "protocol_sha256": digest(BASE / "BCD-PROTOCOL.md"), "clips": {}, "commands": [],
        "human_reviewed": False, "acoustic_events_detected": None}

    def command(args, name):
        argv = list(map(str, args))
        item = {"name": name, "argv": argv, "timeout_seconds": 300}
        receipt["commands"].append(item)
        print(f"Running {name}", flush=True)
        started = time.monotonic()
        with (run / f"{name}.stdout.log").open("xb") as out, (run / f"{name}.stderr.log").open("xb") as err:
            try:
                result = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                        cwd=run, env=ENV, timeout=300, check=False)
                item["exit_code"] = result.returncode
            except subprocess.TimeoutExpired:
                item["timed_out"] = True
                raise
            finally:
                item["elapsed_seconds"] = time.monotonic() - started
        if result.returncode:
            raise RuntimeError(f"{name} exited {result.returncode}")

    try:
        receipt["runtime_before"] = check_pins()
        receipt["sources_before"] = sources()
        for key, name, duration, start, source_id, expected in CLIPS:
            item = {"status": "started", "outputs": []}
            receipt["clips"][key] = item
            try:
                directory = run / key
                directory.mkdir()
                audio = directory / f"{name}-mono-16k.wav"
                command([PINS["ffmpeg"][0], "-nostdin", "-hide_banner", "-loglevel", "error", "-n",
                    "-i", SOURCE_DIR / f"{name}-stereo.wav", "-map", "0:a:0", "-vn", "-af",
                    "pan=mono|c0=0.5*c0+0.5*c1", "-ar", "16000", "-c:a", "pcm_s16le", "-map_metadata", "-1", audio], f"{key}-convert")
                with wave.open(str(audio), "rb") as wav:
                    params = [wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes()]
                if params != [1, 2, 16000, duration * 16000]:
                    raise ValueError("Converted format mismatch")
                item["converted"] = {"sha256": digest(audio), "properties": params}
                rows = []
                for repeat in (1, 2):
                    destination = directory / f"repeat{repeat}"
                    destination.mkdir()
                    prefix = destination / name
                    command(arguments(audio, prefix), f"{key}-repeat{repeat}")
                    data = json.loads(prefix.with_suffix(".json").read_text())
                    rows.append(validate(data, duration))
                    item["outputs"].append({ext: digest(prefix.with_suffix(ext)) for ext in (".json", ".txt", ".srt")})
                item.update(status="machine_drafts_unreviewed", segment_counts=list(map(len, rows)),
                            transcription_equal=rows[0] == rows[1], bytes_equal=item["outputs"][0] == item["outputs"][1])
            except Exception as exc:
                item.update(status="failed", error={"type": type(exc).__name__, "message": str(exc)})
        receipt["status"] = "machine_drafts_unreviewed" if all(v["status"] != "failed" for v in receipt["clips"].values()) else "partial_failure"
    except Exception as exc:
        receipt.update(status="failed", error={"type": type(exc).__name__, "message": str(exc)})
        raise
    finally:
        try:
            receipt["runtime_after"] = check_pins()
            receipt["sources_after"] = sources()
        except Exception as exc:
            receipt.update(status="failed_postcheck", postcheck_error=str(exc))
        receipt["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        receipt["products"] = {str(p.relative_to(run)): {"bytes": p.stat().st_size, "sha256": digest(p)} for p in sorted(run.rglob("*")) if p.is_file()}
        with (run / "receipt.json").open("x") as handle:
            json.dump(receipt, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        print(json.dumps({"status": receipt["status"], "receipt": str(run / "receipt.json")}), flush=True)
    if receipt["status"] != "machine_drafts_unreviewed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

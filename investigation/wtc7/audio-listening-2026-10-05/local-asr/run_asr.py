"""One fixed-source, unprompted local ASR experiment; preserve every result."""
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import wave
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
PINS = {
    "source": (Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/run01/spoken-stereo.wav"), "5b12b06ab0f2699539e5621b8483d9c96163364cabdace3768c8b296240de127"),
    "model": (Path("/Users/admin/dev/pataphor/data/audio-models/ggml-large-v3-turbo-q5_0.bin"), "394221709cd5ad1f40c46e6031ca61bce88931e6e088c188294c6d5a55ffa7e2"),
    "whisper": (Path("/opt/homebrew/bin/whisper-cli"), "40bca494d49af736058eb3f33cbcebaa020eacf6d0087b623f334946e1ab2128"),
    "ffmpeg": (Path("/opt/homebrew/bin/ffmpeg"), "7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569"),
}
ENV = {"PATH": "/opt/homebrew/bin:/usr/bin:/bin", "LANG": "C", "LC_ALL": "C", "HF_HUB_OFFLINE": "1", "HF_HUB_DISABLE_TELEMETRY": "1"}


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def check_pins():
    result = {}
    for key, (path, expected) in PINS.items():
        actual = digest(path)
        if actual != expected:
            raise ValueError(f"Input changed: {key}")
        result[key] = {"path": str(path), "bytes": path.stat().st_size, "sha256": actual}
    return result


def check_transcription(data):
    rows = data.get("transcription")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Missing/non-list/empty transcription")
    previous_end = 0
    for row in rows:
        start, end = row["offsets"]["from"], row["offsets"]["to"]
        if not (isinstance(start, (int, float)) and isinstance(end, (int, float))
                and 0 <= previous_end <= start <= end <= 18000
                and isinstance(row["text"], str)):
            raise ValueError("Unaccepted segment structure/time bounds")
        previous_end = end
    return rows


def main():
    if sys.argv[1:] == ["--self-test"]:
        good = {"transcription": [{"offsets": {"from": 0, "to": 1000}, "text": "test"}]}
        check_transcription(good)
        bad_cases = [{}, {"transcription": []}, {"transcription": [{"offsets": {"from": 0, "to": 18001}, "text": "x"}]}, {"transcription": [{"offsets": {"from": 1000, "to": 0}, "text": "x"}]}]
        for case in bad_cases:
            try:
                check_transcription(case)
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError("Bad case accepted")
        print("PASS: one valid and four invalid invented output checks")
        return
    if sys.argv[1:]:
        raise ValueError("No arbitrary source or model arguments supported")
    run = BASE / "run01"
    run.mkdir(exist_ok=False)
    receipt = {"started_at_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
               "platform": platform.platform(), "environment": ENV, "commands": [],
               "runner_sha256": digest(Path(__file__)), "protocol_sha256": digest(BASE / "PROTOCOL.md"),
               "status": "running", "human_listening": False, "causal_inference": False}

    def command(args, name, timeout=600):
        args = list(map(str, args))
        record = {"name": name, "argv": args, "timeout_seconds": timeout}
        receipt["commands"].append(record)
        print(f"Running {name}", flush=True)
        started = time.monotonic()
        with (run / f"{name}.stdout.log").open("xb") as out, (run / f"{name}.stderr.log").open("xb") as err:
            try:
                result = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                        env=ENV, cwd=run, timeout=timeout, check=False)
                record["exit_code"] = result.returncode
            except subprocess.TimeoutExpired:
                record["timed_out"] = True
                raise
            finally:
                record["elapsed_seconds"] = time.monotonic() - started
        if result.returncode:
            raise RuntimeError(f"{name} exited {result.returncode}")

    try:
        receipt["inputs_before"] = check_pins()
        command([PINS["whisper"][0], "--help"], "whisper-help")
        command([PINS["whisper"][0], "--version"], "whisper-version")
        command([PINS["ffmpeg"][0], "-version"], "ffmpeg-version")
        audio = run / "spoken-mono-16k.wav"
        command([PINS["ffmpeg"][0], "-nostdin", "-hide_banner", "-loglevel", "error", "-n", "-i", PINS["source"][0],
                 "-map", "0:a:0", "-vn", "-af", "pan=mono|c0=0.5*c0+0.5*c1", "-ar", "16000", "-c:a", "pcm_s16le", "-map_metadata", "-1", audio], "convert")
        with wave.open(str(audio), "rb") as wav:
            properties = [wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes()]
        if properties != [1, 2, 16000, 288000]:
            raise ValueError(f"Unexpected converted format: {properties}")
        receipt["converted_audio"] = {"sha256": digest(audio), "properties": properties}
        outputs = []
        for index in (1, 2):
            destination = run / f"repeat{index}"
            destination.mkdir(exist_ok=False)
            prefix = destination / "spoken"
            command([PINS["whisper"][0], "-m", PINS["model"][0], "-f", audio, "-l", "en", "-t", "4", "-p", "1",
                     "-ng", "-tp", "0", "-nf", "-bs", "5", "-bo", "5", "-ojf", "-otxt", "-osrt", "-of", prefix], f"asr-repeat{index}")
            data = json.loads(prefix.with_suffix(".json").read_text())
            rows = check_transcription(data)
            outputs.append({"rows": rows, "hashes": {ext: digest(prefix.with_suffix(ext)) for ext in (".json", ".txt", ".srt")}})
        receipt["repeat_transcription_equal"] = outputs[0]["rows"] == outputs[1]["rows"]
        receipt["output_hashes"] = [item["hashes"] for item in outputs]
        receipt["repeat_output_bytes_equal"] = outputs[0]["hashes"] == outputs[1]["hashes"]
        receipt["status"] = "executed_with_repeat_comparison_not_accuracy_certification"
    except Exception as exc:
        receipt["status"] = "failed"
        receipt["error"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally:
        try:
            receipt["inputs_after"] = check_pins()
        except Exception as exc:
            receipt["postcheck_error"] = str(exc)
            receipt["status"] = "failed_postcheck"
        receipt["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        receipt["products"] = {str(path.relative_to(run)): {"bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(run.rglob("*")) if path.is_file()}
        with (run / "receipt.json").open("x") as handle:
            json.dump(receipt, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        print(json.dumps({"status": receipt["status"], "receipt": str(run / "receipt.json")}), flush=True)
    if receipt["status"].startswith("failed"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

"""One separately declared GPU alternative; reuse fixed input/output checks."""
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from run_asr import BASE, ENV, PINS, check_pins, check_transcription, digest


def main():
    run = BASE / "run02-gpu"
    run.mkdir(exist_ok=False)
    cpu = json.loads((BASE / "run01/receipt.json").read_text())
    receipt = {"started_at_utc": datetime.now(timezone.utc).isoformat(),
               "status": "running", "commands": [], "environment": ENV,
               "runner_sha256": digest(Path(__file__)),
               "shared_runner_sha256": digest(BASE / "run_asr.py"),
               "protocol_sha256": digest(BASE / "PROTOCOL.md"),
               "addendum_sha256": digest(BASE / "GPU-ADDENDUM.md"),
               "cpu_receipt_sha256": digest(BASE / "run01/receipt.json"),
               "human_listening": False, "causal_inference": False}
    try:
        if cpu["status"] != "failed" or not cpu["commands"][-1].get("timed_out"):
            raise ValueError("Declared CPU timeout prerequisite not met")
        receipt["inputs_before"] = check_pins()
        audio = BASE / "run01/spoken-mono-16k.wav"
        if digest(audio) != cpu["converted_audio"]["sha256"]:
            raise ValueError("Converted input changed")
        receipt["converted_audio"] = cpu["converted_audio"]
        output = []
        for index in (1, 2):
            destination = run / f"repeat{index}"
            destination.mkdir(exist_ok=False)
            prefix = destination / "spoken"
            args = list(map(str, [PINS["whisper"][0], "-m", PINS["model"][0], "-f", audio,
                "-l", "en", "-t", "4", "-p", "1", "-tp", "0", "-nf", "-bs", "5", "-bo", "5",
                "-ojf", "-otxt", "-osrt", "-of", prefix]))
            record = {"name": f"gpu-repeat{index}", "argv": args, "timeout_seconds": 300}
            receipt["commands"].append(record)
            print(f"Running gpu-repeat{index}", flush=True)
            started = time.monotonic()
            with (run / f"repeat{index}.stdout.log").open("xb") as out, (run / f"repeat{index}.stderr.log").open("xb") as err:
                try:
                    result = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                            env=ENV, cwd=run, timeout=300, check=False)
                    record["exit_code"] = result.returncode
                except subprocess.TimeoutExpired:
                    record["timed_out"] = True
                    raise
                finally:
                    record["elapsed_seconds"] = time.monotonic() - started
            if result.returncode:
                raise RuntimeError(f"GPU repeat{index} exited {result.returncode}")
            data = json.loads(prefix.with_suffix(".json").read_text())
            rows = check_transcription(data)
            output.append({"rows": rows, "hashes": {ext: digest(prefix.with_suffix(ext)) for ext in (".json", ".txt", ".srt")}})
        receipt["repeat_transcription_equal"] = output[0]["rows"] == output[1]["rows"]
        receipt["output_hashes"] = [item["hashes"] for item in output]
        receipt["repeat_output_bytes_equal"] = output[0]["hashes"] == output[1]["hashes"]
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

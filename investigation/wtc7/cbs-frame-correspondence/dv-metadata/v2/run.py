"""Versioned binary-artifact storage adapter; no change to frozen extraction."""
import argparse
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT.parent))
import collect_dv as parent
from storage import write_chunks, verify_chunks

REQUIRED = {"PLAN.md", "run.py", "storage.py", "test_storage.py", "test_run.py", "../freeze.json"}


def check_controls():
    path = UNIT/"freeze.json"
    value = json.loads(path.read_text())
    expected_names = REQUIRED | {"../"+n for n in parent.REQUIRED}
    parent.require(set(value["files"])==expected_names, "incomplete v2 frozen dependencies")
    for name, expected in value["files"].items():
        parent.require(parent.pin(UNIT/name)==expected, "changed v2 frozen dependency: "+name)
    return parent.pin(path)


def safe_results_root():
    path = UNIT/"results"
    parent.require(UNIT.absolute()==UNIT.resolve(), "symlink unit path")
    if not path.exists() and not path.is_symlink():
        path.mkdir()
    parent.require(path.is_dir() and not path.is_symlink(), "unsafe results root")
    parent.require(path.resolve().parent==UNIT, "results root escaped unit")
    return path


def run_clip(clip, destination):
    """Write generated binary metadata; accept only after all post-checks."""
    parent.require(type(clip) is int and 1<=clip<=8, "invalid clip")
    final = destination.parent/(destination.name+"-result.json")
    parent.require(not destination.exists() and not destination.is_symlink(), "output directory already exists")
    parent.require(not final.exists() and not final.is_symlink(), "result already exists")
    freeze_pin = check_controls()
    inputs = json.loads(parent.INPUT.read_text())
    frames = int(inputs["items"][clip-1]["saved_video"]["nb_frames"])
    old_compress, old_args = parent.compress_metadata, sys.argv
    capture = io.StringIO()
    try:
        parent.compress_metadata = lambda data: write_chunks(data, frames, destination)
        sys.argv = [str(parent.UNIT/"collect_dv.py"), "--clip", str(clip)]
        with redirect_stdout(capture):
            parent.main()
    finally:
        parent.compress_metadata, sys.argv = old_compress, old_args
    # Parent main performs exact population, source and method before/after gates.
    result = json.loads(capture.getvalue())
    parent.require(result["clip"]==clip and result["before_after_pins_match"] is True,
                   "parent result identity/post-pin failure")
    parent.require(result["result"]["frames"]==frames, "result frame mismatch")
    verify_chunks(destination, result["result"]["metadata"])
    parent.require(check_controls()==freeze_pin, "v2 freeze changed during collection")
    result["schema"] = "dv-metadata-chunked-inventory-v2"
    result["v2_freeze"] = freeze_pin
    result["artifact_readback_verified"] = True
    text = json.dumps(result, separators=(",",":"))+"\n"
    parent.require(len(text.encode("utf-8"))<=8*1024*1024, "v2 result JSON limit")
    with final.open("x", encoding="utf-8") as stream:
        stream.write(text)
    parent.require(json.loads(final.read_text())==result, "result JSON readback mismatch")
    return final


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--clip", type=int, required=True, choices=range(1,9))
    option = args.parse_args()
    root = safe_results_root()
    final = run_clip(option.clip, root/("clip"+str(option.clip)))
    print(json.dumps({"clip":option.clip,"result_path":str(final),"result_pin":parent.pin(final)}))


if __name__ == "__main__":
    main()

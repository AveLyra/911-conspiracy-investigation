#!/usr/bin/env python3
"""One declared refinement selection; reuse frozen PTS-checked extraction."""
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("frame_extraction", HERE / "extract_frames.py")
x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(x)
PLANS = {"compilation": [(580, 581, None), (602, 603, None), (606, 607, None)], "comparator": [(13, 14, None)]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", choices=["refine01", "refine02"])
    args = parser.parse_args()
    out = HERE / args.run
    if out.exists():
        raise FileExistsError("Refusing existing refinement scope")
    before = {label: x.identity(source) for label, (source, _, _) in x.SOURCES.items()}
    for label, (_, pin, size) in x.SOURCES.items():
        if before[label] != {"sha256": pin, "bytes": size}:
            raise ValueError("Source pin mismatch")
    out.mkdir()
    runner = x.Runner(out)
    receipt = {"sources_before": before, "script": x.identity(Path(__file__)),
               "extract_helper": x.identity(HERE / "extract_frames.py"), "protocol": x.identity(HERE / "PROTOCOL.md"),
               "refinement": x.identity(HERE / "REFINEMENT.md"), "status": "started"}
    x.save(out / "start.json", receipt)
    try:
        for label, (source, _, _) in x.SOURCES.items():
            video, frames = x.probe(runner, source, label)
            rows = x.extract(runner, source, label, video, frames, PLANS[label])
            if len(rows) != (90 if label == "compilation" else 30):
                raise ValueError("Unexpected refinement frame count")
            x.sheets(out, label, rows)
        receipt["sources_after"] = {label: x.identity(source) for label, (source, _, _) in x.SOURCES.items()}
        if receipt["sources_after"] != before:
            raise ValueError("Source changed")
        receipt["status"] = "complete"
    except Exception as exc:
        receipt.update(status="failed", failure_type=type(exc).__name__)
        raise
    finally:
        receipt["commands"] = runner.commands
        receipt["products"] = {str(p.relative_to(out)): x.identity(p) for p in sorted(out.rglob("*"))
                               if p.is_file() and ".local." not in p.name and p.name not in ("start.json", "receipt.json")}
        x.save(out / "receipt.json", receipt)
    print({"run": args.run, "status": "complete", "historical_frames": 120})


if __name__ == "__main__":
    main()

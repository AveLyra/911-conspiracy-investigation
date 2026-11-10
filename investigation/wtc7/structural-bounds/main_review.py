"""Separate velocity-based recurrence check; no event-specific inputs."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import bounds

HERE = Path(__file__).resolve().parent


def check(output):
    if output.exists():
        raise FileExistsError("Do not replace review receipt")
    checked_cases,checked_stages = 0,0
    # Declared implementation check grid, not a new physical sensitivity study.
    for pickup in (False,True):
        for stroke in (0.025,0.12,0.4):
            for resistance in (0,0.5,1.7,3,7,13,31):
                rows = bounds.cascade(resistance,stroke,pickup)
                mass,velocity = 1.0,0.0
                for index in range(8):
                    velocity = math.sqrt(velocity*velocity+2)  # unit gravity, unit clear gap
                    if pickup:
                        velocity *= mass/(mass+1)  # impulse-isolated pickup
                        mass += 1
                    accel = 1-resistance/mass
                    terminal_square = velocity*velocity+2*accel*stroke
                    stop = terminal_square <= 0
                    distance = velocity*velocity/(-2*accel) if stop else stroke
                    next_velocity = 0.0 if stop else math.sqrt(terminal_square)
                    row = rows[index]
                    if row["stopped"] != stop or not math.isclose(row["distance"],distance,rel_tol=0,abs_tol=1e-11):
                        raise ValueError("First-stop velocity recurrence disagrees")
                    if not math.isclose(row["kinetic_out"],0.5*mass*next_velocity*next_velocity,rel_tol=0,abs_tol=1e-10):
                        raise ValueError("Velocity and work-energy calculations disagree")
                    checked_stages += 1
                    velocity = next_velocity
                    if stop:
                        if len(rows) != index+1:
                            raise ValueError("Motion continued after first stop")
                        break
                checked_cases += 1
    manifest = json.loads((HERE/"run-v1/manifest.json").read_text())
    for name,expected in manifest["outputs_sha256"].items():
        if hashlib.sha256((HERE/"run-v1"/name).read_bytes()).hexdigest() != expected:
            raise ValueError("Preserved table hash mismatch")
    result = {"status":"separate_velocity_recurrence_matches_idealized_work_energy",
              "cases_checked":checked_cases,"visited_stages_checked":checked_stages,
              "table_hashes_verified":len(manifest["outputs_sha256"]),
              "bounds_sha256":hashlib.sha256((HERE/"bounds.py").read_bytes()).hexdigest(),
              "review_script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope":"Fixed normalized mass/force/gap models only; distinct mathematical implementation, not an independent physical experiment or WTC7 validation."}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",required=True,type=Path)
    check(parser.parse_args().out)

#!/bin/sh
set -eu
HERE="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
CSV="$HERE/discrepancy-index.csv"
JSON="$HERE/phase3-second-sweep.json"
python3 - "$CSV" "$JSON" <<'PY'
import json, sys
from pathlib import Path
csv_path, json_path = Path(sys.argv[1]), Path(sys.argv[2])
ids = [line.split(",", 1)[0] for line in csv_path.read_text().splitlines()[1:] if line]
assert ids[-1] == "DISC-029", ids[-1]
assert "DISC-029" in ids
payload = json.loads(json_path.read_text())
assert payload["member_count"] == 25634
assert payload["shared_basename_count"] == 8364
assert payload["nul_compare"]["B_nul_count"] == 328
assert payload["june_letter"]["pages"] == 2
print("OK phase3", ids[-1], "csv_count", len(ids), "members", payload["member_count"])
PY

"""Read-only, fixed eight-file header collection. Prints JSON; creates no files."""
import hashlib
import json
import platform
from fractions import Fraction
from pathlib import Path

from riff_headers import inventory, fields, video_headers, unique_text, compare


UNIT = Path(__file__).resolve().parent


def pin(path):
    with path.open("rb") as stream:
        sha = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"bytes": path.stat().st_size, "sha256": sha}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prior_payloads(previous):
    """Reconstruct both lossless forms used by the prior saved collector."""
    result = {}
    for row in previous["riff"]["records"]:
        if "payload" not in row:
            continue
        payload = row["payload"]
        require(("hex" in payload) != ("utf8" in payload), "ambiguous prior payload representation")
        data = bytes.fromhex(payload["hex"]) if "hex" in payload else payload["utf8"].encode("utf-8")
        require(len(data) == payload["bytes"] and hashlib.sha256(data).hexdigest() == payload["sha256"], "prior payload reconstruction mismatch")
        require(row["offset"] not in result, "duplicate prior payload offset")
        result[row["offset"]] = data.hex()
    return result


def fixed_inputs():
    freeze_path = UNIT / "freeze.json"
    freeze_pin = pin(freeze_path)
    freeze = json.loads(freeze_path.read_text())
    required = {"PLAN.md", "riff_headers.py", "test_headers.py", "collect.py",
                "inputs.json", "references.md", "../lineage-142/metadata.json"}
    require(set(freeze["files"]) == required, "unexpected frozen dependency set")
    for name, expected in freeze["files"].items():
        require(pin(UNIT / name) == expected, "changed frozen dependency: " + name)
    manifest = json.loads((UNIT / "inputs.json").read_text())
    require([i["clip"] for i in manifest["items"]] == list(range(1, 9)), "unexpected clip population")
    source = (UNIT / manifest["source_root"]).resolve()
    require(source == UNIT.parent.parent / "cbs-vince-source-screen", "unexpected source root")
    dependencies = {}
    acquisitions = {}
    for rec in manifest["acquisition_records"]:
        path = source / rec["path"]
        dependencies[str(path)] = pin(path)
        require(dependencies[str(path)]["sha256"] == rec["sha256"], "changed acquisition")
        acquisitions[rec["path"]] = json.loads(path.read_text())
    for item in manifest["items"]:
        acquisition = acquisitions[item["acquisition_record"]]
        matched = [r for r in acquisition["items"] if r["clip_number"] == item["clip"]]
        require(len(matched) == 1, "ambiguous acquisition clip")
        rec = matched[0]
        require(rec["selected_attempt"] == item["selected_attempt"], "wrong selected attempt")
        attempts = [a for a in rec["attempts"] if a["attempt"] == item["selected_attempt"]]
        require(len(attempts) == 1, "ambiguous attempt")
        a = attempts[0]
        require(a["exit_code"] == 0 and a["bytes"] == rec["catalogue_and_fetch_bytes"], "incomplete selected acquisition")
        raw = Path(item["acquisition_record"]).parent / a["path"]
        require(str(raw) == item["path"] and a["bytes"] == item["bytes"] and a["sha256"] == item["sha256"], "manifest differs from acquisition")
        path = source / item["path"]
        dependencies[str(path)] = pin(path)
        require(dependencies[str(path)] == {k: item[k] for k in ("bytes", "sha256")}, "raw integrity mismatch")
        path = source / item["container_record"]
        dependencies[str(path)] = pin(path)
        require(dependencies[str(path)]["sha256"] == item["container_record_sha256"], "changed saved container inventory")
        container = json.loads(path.read_text())
        streams = [s for s in container["streams"] if s["codec_type"] == "video"]
        require(len(streams) == 1, "unexpected saved video streams")
        require({k: streams[0][k] for k in item["saved_video"]} == item["saved_video"], "changed saved video summary")
    return freeze, freeze_pin, manifest, source, dependencies


def main():
    freeze, freeze_pin, manifest, source, dependencies = fixed_inputs()
    items = []
    for item in manifest["items"]:
        with (source / item["path"]).open("rb") as stream:
            result = inventory(stream, item["bytes"])
        fs = fields(result["records"])
        videos = video_headers(result["records"])
        require(len(videos) == 1, "expected exactly one historical video header")
        video = videos[0]
        saved = item["saved_video"]
        agreement = {"frame_count": video["length"] == int(saved["nb_frames"]) == saved["duration_ts"],
                     "time_base": Fraction(video["time_base"]) == Fraction(saved["time_base"]),
                     "start": video["start"] == saved["start_pts"],
                     "duration_rounding": abs(Fraction(video["duration_seconds_rational"]) - Fraction(saved["duration"])) <= Fraction(1, 2000000)}
        require(all(agreement.values()), "header/saved-inventory mismatch: clip " + str(item["clip"]))
        require(video["start"] == 0, "nonzero stream start requires separate timing treatment")
        pairs = {}
        for name, prefix in (("tape", "rn_"), ("timecode", "tc_")):
            original, alternate = unique_text(fs[prefix + "O"]), unique_text(fs[prefix + "A"])
            pairs[name] = {"comparable": original is not None and alternate is not None,
                           "equal": original == alternate if original is not None and alternate is not None else None}
        items.append({"clip": item["clip"], "source": item, "riff": result,
                      "fields": fs, "video_header": video, "saved_inventory_agreement": agreement,
                      "original_alternate_agreement": pairs})
    previous = json.loads((UNIT / "../lineage-142/metadata.json").read_text())
    old = prior_payloads(previous)
    new = {r["offset"]: r["payload_hex"] for r in items[6]["riff"]["records"] if "payload_hex" in r}
    require(old == new, "Clip 7 retained bytes differ from prior inventory")
    comparisons = [compare(items, drop, lane) for lane in ("O", "A") for drop in (False, True)]
    for path, expected in dependencies.items():
        require(pin(Path(path)) == expected, "dependency changed during collection: " + path)
    for name, expected in freeze["files"].items():
        require(pin(UNIT / name) == expected, "frozen file changed during collection: " + name)
    require(pin(UNIT / "freeze.json") == freeze_pin, "freeze changed during collection")
    output = {"schema": "eight-sibling-header-results-v1", "python": platform.python_version(),
              "freeze": freeze, "freeze_pin": freeze_pin, "dependency_pins": dependencies,
              "all_pins_unchanged_after": True, "clip7_payloads_equal_prior": True,
              "items": items, "conditional_comparisons": comparisons,
              "limits": ["No media probe, decoder, subprocess or essence interpretation invoked.",
                         "Whole-file hashes read essence bytes only for integrity.",
                         "Metadata and conditional arithmetic do not authenticate camera chronology."]}
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

"""Check manually transcribed carrier fields against pinned court text.

python3 verify_fields.py --court-zip /path/to/court-flights.zip \
    [--captures /path/to/28/held/JPEGs]

This does not decode native switch data, authenticate a caller, calibrate clocks,
or establish the reason for any historical discrepancy. Never executes Flash.
"""
import argparse
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import zipfile

from extract_swf_text import extract


def require(condition, message):
    if not condition:
        raise ValueError(message)


def seconds(a, b):
    return int((datetime.strptime(b, "%H:%M:%S") -
                datetime.strptime(a, "%H:%M:%S")).total_seconds())


def run(root, court_zip, captures=None):
    source = json.loads((root / "SOURCE-IMAGES.json").read_text())
    rows = {r["id"]: r for r in
            json.loads((root / "FIELD-OBSERVATIONS.json").read_text())["rows"]}
    pages = json.loads((root / "PAGE-ACCOUNTING.json").read_text())
    pins = json.loads((root / "COURT-PINS.json").read_text())
    images = source["images"]
    require([r["reader_page"] for r in images] == list(range(1, 29)),
            "Reader image accounting changed")
    require(sum(r["bytes"] for r in images) == source["total_bytes"],
            "Image byte accounting changed")
    require(all("?" not in r["public_asset_url"] for r in images),
            "Resource query must not be published")
    image_checks = 0
    if captures is not None:
        for r in images:
            b = (captures / r["filename"]).read_bytes()
            require(len(b) == r["bytes"] and
                    hashlib.sha256(b).hexdigest() == r["sha256"],
                    "Captured image differs; preserve and review separately")
            image_checks += 1
    for r in rows.values():
        source_image = images[r["reader_page"] - 1]
        require(r["source_sha256"] == source_image["sha256"],
                "Manual field points to a different entity")

    bates = [int(r["bates"].split("-")[-1]) for r in pages["portrait_rows"]]
    fax = [int(r["fax_label"]) for r in pages["portrait_rows"]]
    missing_bates = sorted(set(range(600, 646)) - set(bates))
    missing_fax = sorted(set(range(2, 48)) - set(fax))
    require(missing_bates == list(range(609, 632)) and
            missing_fax == list(range(11, 34)), "Manual page labels changed")
    require(pages["reader_images"] - pages["letter_images"] ==
            pages["enclosure_images"] == 27, "Enclosure count changed")
    declared_difference = (pages["letter_declared_enclosures"] -
                           pages["enclosure_images"])

    calculations = []
    for key in ["CE02", "CE03", "CE04"]:
        fields = rows[key]["fields"]
        billing = seconds(fields["Billing Start"], fields["Event Time"])
        answer = seconds(fields["Answer Supervision"], fields["Event Time"])
        require(billing == fields["Duration"],
                "Selected printed Duration differs from billing interval")
        item = dict(observation=key, printed_duration=fields["Duration"],
                    event_minus_billing_seconds=billing,
                    event_minus_answer_seconds=answer)
        if "Start Time" in fields:
            item["event_minus_start_seconds"] = seconds(
                fields["Start Time"], fields["Event Time"])
        calculations.append(item)
    wrong_anchor = calculations[0]["event_minus_start_seconds"]
    require(wrong_anchor == 193 and wrong_anchor != 159,
            "The deliberately wrong start anchor was not rejected")
    require(calculations[1]["event_minus_answer_seconds"] == 146 and
            calculations[1]["printed_duration"] == 158,
            "The counterexample to a universal answer anchor changed")

    raw_zip = court_zip.read_bytes()
    require(hashlib.sha256(raw_zip).hexdigest() == pins["zip_sha256"],
            "Court ZIP differs; preserve and review separately")
    with zipfile.ZipFile(court_zip) as z:
        members = [n for n in z.namelist() if Path(n).name == pins["member"]]
        require(len(members) == 1, "Ambiguous court member")
        swf = z.read(members[0])
    require(hashlib.sha256(swf).hexdigest() == pins["member_sha256"],
            "SWF member differs")
    definitions = {r["id"]: r for r in extract(swf)["text_definitions"]}
    for pin in pins["pins"]:
        actual = definitions[pin["id"]]
        require(all(actual[k] == pin[k] for k in ["tag", "offset", "text"]),
                "Stored court definition differs")
    candidate = (datetime.strptime(rows["CE02"]["fields"]["Start Time"],
                                   "%H:%M:%S") + timedelta(hours=2)
                 ).strftime("%H:%M:%S")
    require(candidate == definitions[1997]["text"] and
            str(rows["CE02"]["fields"]["Duration"]) ==
            definitions[1998]["text"].strip().split()[0],
            "Conditional label comparison differs")
    return dict(
        images_listed=len(images), image_hashes_and_sizes_checked=image_checks,
        image_hash_scope="Supplied held entities only; not release authentication",
        total_captured_bytes=source["total_bytes"],
        portrait_bates_labels=len(bates),
        unobserved_bates_suffixes=missing_bates,
        unobserved_fax_labels=missing_fax,
        declared_minus_held_enclosure_images=declared_difference,
        page_count_equivalence_proves_missing_contents=False,
        selected_interval_calculations=calculations,
        negative_control_wrong_start_anchor_seconds=wrong_anchor,
        negative_control_wrong_start_anchor_rejected=True,
        carrier_zero_field_value=rows["CE01"]["fields"]["Duration"],
        carrier_positive_field_value=rows["CE02"]["fields"]["Duration"],
        static_court_pins_checked=len(pins["pins"]),
        court_zero_label=definitions[1692]["text"],
        conditional_plus_two_hour_label=candidate,
        conditional_duration_field_agrees=True,
        native_call_leg_join_verified=False, caller_identity_verified=False,
        clock_calibration_performed=False, native_field_dictionary_acquired=False,
        historical_discrepancy_adjudicated=False,
        scope="Integrity, manual-input arithmetic and conditional label comparison; "
              "not native carrier decoding or independent conversation evidence")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--court-zip", type=Path, required=True)
    parser.add_argument("--captures", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(Path(__file__).resolve().parent, args.court_zip,
                         args.captures), indent=2))

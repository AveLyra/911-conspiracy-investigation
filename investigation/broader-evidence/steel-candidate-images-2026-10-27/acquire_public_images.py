"""Retrieve the three pinned public images anonymously into a new directory.

python3 acquire_public_images.py NEW_OUTPUT_DIRECTORY IMAGE_SOURCES_JSON

Uses only public Drive IDs and the ordinary download route. No cookies,
Authorization headers, browser state or connector temporary links. Route new
media through the repository's media_path.py guard before calling this program.
Existing output directories are refused. A changed downloaded entity is saved
in the new directory and reported as a variant, never used to replace originals.
"""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request


def run(output, pins):
    output.mkdir(parents=True, exist_ok=False)
    receipts = []
    for pin in pins:
        url = "https://drive.google.com/uc?" + urllib.parse.urlencode(
            dict(export="download", id=pin["id"]))
        with urllib.request.urlopen(url, timeout=60) as response:
            body = response.read()
            status = response.status
            content_type = response.headers.get("content-type")
        digest = hashlib.sha256(body).hexdigest()
        match = len(body) == pin["bytes"] and digest == pin["sha256"]
        filename = pin["filename"] if match else "variant-" + pin["id"] + ".bin"
        with (output / filename).open("xb") as handle:
            handle.write(body)
        receipts.append(dict(id=pin["id"], status=status, content_type=content_type,
                             bytes=len(body), sha256=digest,
                             pinned_entity_matches=match, filename=filename))
        if not match:
            with (output / "ACQUISITION-RESULT.json").open("x") as handle:
                json.dump(receipts, handle, indent=2)
            raise ValueError("Downloaded entity changed; variant preserved separately")
    with (output / "ACQUISITION-RESULT.json").open("x") as handle:
        json.dump(receipts, handle, indent=2)
    return receipts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("pins", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.output, json.loads(args.pins.read_text())), indent=2))

"""Reproduce a strict printed-key subset join. No network; aggregate output only."""
import hashlib
import json
from pathlib import Path
import re
import sys
import fitz

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify.py GTE_BOX13_788_PDF")
    pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    path = Path(sys.argv[1])
    raw = path.read_bytes()
    assert len(raw) == pins["source"]["bytes"]
    assert hashlib.sha256(raw).hexdigest() == pins["source"]["sha256"]
    doc = fitz.open(stream=raw, filetype="pdf")
    assert len(doc) == pins["source"]["pdf_pages"]
    rx = re.compile(pins["join"]["rule"])
    keys = {}
    for page, box in pins["join"]["regions"].items():
        accepted = []
        for word in doc[int(page)-1].get_text("words"):
            if box[0] <= word[0] <= box[2] and box[1] <= word[1] <= box[3]:
                match = rx.match(word[4])
                if match:
                    accepted.append(match.group(1))
        assert len(set(accepted)) == len(accepted), "Duplicate key in selected region"
        assert len(accepted) == pins["join"]["accepted_keys_by_page"][page]
        keys[page] = set(accepted)
    shared = keys["1"] & keys["13"]
    assert len(shared) == pins["join"]["exact_shared_keys"]
    assert len(keys["1"] - keys["13"]) == pins["join"]["page1_only_in_parsed_subset"]
    assert len(keys["13"] - keys["1"]) == pins["join"]["page13_only_in_parsed_subset"]
    errors = [w for w in doc[2].get_text("words") if w[4] == "#NAME?"]
    assert len(errors) == pins["locators"]["page3"]["literal_name_token_count"]
    print(json.dumps({"pdf_pages":len(doc),
        "accepted_text_layer_keys":{k:len(v) for k,v in keys.items()},
        "exact_shared_keys":len(shared),
        "page1_only":len(keys["1"]-keys["13"]),
        "page13_only":len(keys["13"]-keys["1"]),
        "literal_name_tokens_page3":len(errors),
        "pymupdf":fitz.VersionBind,
        "complete_call_or_clock_validation":False}, indent=2))
if __name__ == "__main__":
    main()

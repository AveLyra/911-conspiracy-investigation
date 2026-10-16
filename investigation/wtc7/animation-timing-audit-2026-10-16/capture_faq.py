"""Read an allowlisted public FAQ and preserve selected public statements.

No cookies, credentials, scripts, private correspondence, or link traversal.
The response hash covers acquired HTML, not a 2008 version of the FAQ.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
import urllib.request

URL = "https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation"


class Paragraphs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.current = []
        self.paragraphs = []

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == "p" and self.depth:
            self.depth -= 1
            if not self.depth:
                text = " ".join("".join(self.current).split())
                self.paragraphs.append(text)
                self.current = []

    def handle_data(self, data):
        if self.depth:
            self.current.append(data)


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--output", required=True)
    output = args.parse_args().output
    result = {"requested_url": URL, "accessed_utc": datetime.now(timezone.utc).isoformat(), "scope": "Selected public technical statements; not a historical FAQ snapshot"}
    try:
        request = urllib.request.Request(URL, headers={"User-Agent": "Public-source-record-audit/1.0", "Accept-Encoding": "identity"})
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read(4 * 1024 * 1024 + 1)
            if len(raw) > 4 * 1024 * 1024:
                raise ValueError("response exceeds capture bound")
            result.update({"status": response.status, "final_url": response.url, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "content_type": response.headers.get("Content-Type"), "content_encoding": response.headers.get("Content-Encoding")})
        parser = Paragraphs()
        parser.feed(raw.decode("utf-8", "strict"))
        needles = ["12.9 seconds", "validated against actual events", "exactly as it was received", "Videos were logged", "Only in the later stages", "nonstructural materials", "Both measured time"]
        result["selected_paragraphs"] = [{"paragraph_index": i, "text": text} for i, text in enumerate(parser.paragraphs) if any(needle in text for needle in needles)]
        if not any("12.9 seconds" in x["text"] for x in result["selected_paragraphs"]):
            raise ValueError("expected timing paragraph absent; no silent successful capture")
        result["capture_success"] = True
    except Exception as exc:
        result["capture_success"] = False
        result["failure"] = type(exc).__name__ + ": " + str(exc)
    with open(output, "x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"output": output, "success": result["capture_success"], "sha256": result.get("sha256")}))


if __name__ == "__main__":
    main()

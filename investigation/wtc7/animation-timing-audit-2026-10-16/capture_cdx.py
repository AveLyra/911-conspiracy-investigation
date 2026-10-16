"""Bounded, read-only public index probes; no replay is treated as original media."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request

ASSETS = ["CU animation.flv", "whole building animation.flv", "SkinUnderPlayStopSeekCaptionVol.swf"]


def capture(name):
    original = "http://www.nist.gov/public_affairs/releases/wtc_videos/" + name
    url = "https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode({"url": original, "output": "json", "fl": "timestamp,original,statuscode,mimetype,digest,length", "limit": "1000"})
    result = {"asset_name": name, "queried_original": original, "request_url": url, "accessed_utc": datetime.now(timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Public-source-record-audit/1.0", "Accept-Encoding": "identity"})
        try:
            response = urllib.request.urlopen(req, timeout=35)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            raw = response.read(2 * 1024 * 1024 + 1)
            if len(raw) > 2 * 1024 * 1024:
                raise ValueError("index response exceeds bound")
            result.update({"status": response.status, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "content_type": response.headers.get("Content-Type")})
        try:
            value = json.loads(raw)
            result["json_response"] = value
            result["valid_index_json"] = isinstance(value, list)
        except (ValueError, UnicodeDecodeError):
            result["valid_index_json"] = False
            result["non_json_body_utf8"] = raw.decode("utf-8", "replace")
    except Exception as exc:
        result.update({"valid_index_json": False, "failure": type(exc).__name__ + ": " + str(exc)})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    output = parser.parse_args().output
    with ThreadPoolExecutor(max_workers=3) as pool:
        result = {"method": "Exact-path CDX index requests, capped at 1000 rows; no media playback, replay or WARC retrieval", "attempts": list(pool.map(capture, ASSETS))}
    with open(output, "x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"output": output, "valid_json_responses": sum(x["valid_index_json"] for x in result["attempts"])}))


if __name__ == "__main__":
    main()

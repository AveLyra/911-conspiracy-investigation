"""Bounded public report locator/HEAD audit. Never downloads a PDF body or model."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request

PIN_COMMIT = "3236dd826b7fb203fb8c364af320e5b10101fdbe"
UAF_PAGE = "https://ine.uaf.edu/wtc7"
REPORTS = [
    {"path": "investigation/wtc7/uaf-final-method-audit/source/uaf-final-2020.pdf", "url": "https://files.wtc7report.org/file/public-download/A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March2020.pdf"},
    {"path": "research/steel-video-deep-audit/sources/hulsey-uaf-final-2020.pdf", "url": "https://files.wtc7report.org/file/public-download/A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March-2020.pdf"}
]


class SecureRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.seen = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlparse(newurl).scheme != "https" or len(self.seen) >= 5:
            raise ValueError("redirect outside HTTPS/five-hop boundary")
        self.seen.append({"from": req.full_url, "status": code, "to": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class ReportLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.current = {"href": dict(attrs).get("href", ""), "text": ""}

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            label = " ".join(self.current["text"].split())
            if "final report" in label.lower() or "structural reevaluation" in label.lower():
                self.links.append({"label": label, "href": self.current["href"]})
            self.current = None


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pointer(raw):
    match = re.fullmatch(rb"version https://git-lfs.github.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize ([0-9]+)\n", raw)
    if not match:
        raise ValueError("not the exact expected three-line Git LFS pointer")
    return {"pdf_sha256_as_recorded": match[1].decode(), "pdf_bytes_as_recorded": int(match[2]), "pointer_sha256": sha(raw), "literal_pointer": raw.decode()}


def request(url, method):
    redirect = SecureRedirects()
    result = {"requested_url": url, "method": method, "accessed_utc": datetime.now(timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, method=method, headers={"User-Agent": "Public-source-record-audit/1.0", "Accept-Encoding": "identity"})
        try:
            response = urllib.request.build_opener(redirect).open(req, timeout=25)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            result.update({"status": response.status, "final_url": response.url, "headers": {key: response.headers.get(key) for key in ["Content-Length", "Content-Type", "Last-Modified", "ETag", "Accept-Ranges", "Date"] if response.headers.get(key) is not None}})
            if method == "HEAD":
                result["pdf_body_acquired"] = False
            elif response.status == 200:
                raw = response.read(1048577)
                if len(raw) > 1048576:
                    raise ValueError("institutional page exceeds bound")
                result.update({"html_bytes": len(raw), "html_sha256": sha(raw)})
                parser = ReportLinks()
                parser.feed(raw.decode("utf-8", "strict"))
                result["selected_report_links"] = parser.links
                result["scope"] = "HTML hash plus selected link text/URLs only; no linked asset fetched by this parser"
    except Exception as exc:
        result["failure"] = type(exc).__name__ + ": " + str(exc)
    result["redirects"] = redirect.seen
    return result


def blob(repo, path):
    raw = subprocess.check_output(["git", "-C", repo, "show", PIN_COMMIT + ":" + path])
    return {"path": path, "source_commit": PIN_COMMIT, "git_blob_oid": subprocess.check_output(["git", "-C", repo, "rev-parse", PIN_COMMIT + ":" + path], text=True).strip(), "bytes": len(raw), "sha256": sha(raw), "literal_text": raw.decode("utf-8", "strict")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    entries = []
    for item in REPORTS:
        record = blob(args.repository, item["path"])
        entries.append({"source_url_from_existing_receipt_or_protocol": item["url"], "record": record, "pointer": pointer(record["literal_text"].encode())})
    receipts = [blob(args.repository, p) for p in ["research/steel-video-deep-audit/sources/README.md", "investigation/wtc7/uaf-final-method-audit/PROTOCOL.md", "investigation/wtc7/uaf-final-method-audit/execution.md"]]
    for entry in entries:
        if not any(entry["source_url_from_existing_receipt_or_protocol"] in x["literal_text"] for x in receipts):
            raise ValueError("source URL not corroborated by preserved receipt/protocol")
    jobs = [(UAF_PAGE, "GET")] + [(x["url"], "HEAD") for x in REPORTS]
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda x: request(*x), jobs))
    output = {"audit_date": "2026-10-17", "preserved_pdf_pins": entries, "preserved_receipts": receipts, "public_requests": results, "derived": {"different_recorded_sha256": entries[0]["pointer"]["pdf_sha256_as_recorded"] != entries[1]["pointer"]["pdf_sha256_as_recorded"], "recorded_size_difference_bytes": entries[0]["pointer"]["pdf_bytes_as_recorded"] - entries[1]["pointer"]["pdf_bytes_as_recorded"]}, "limitations": ["Pins identify the payloads recorded in Git history; neither PDF body was read or freshly hashed here.", "HEAD metadata does not independently prove a PDF hash, 125-page count, textual difference, edition order, scientific difference or body equivalence.", "The selected historical UAF report was unavailable at its requested operational-media path. No preservation-copy fallback or media hydration was attempted.", "Different source URL spellings and hash/size pins are preserved without choosing which report is authoritative or inferring alteration, deception, historical cause or intent.", "A comparison of authenticated PDF text, page renders, metadata and native case crosswalks would discriminate content changes from packaging-only differences. It has not been done by this audit."]}
    with open(args.output, "x", encoding="utf-8") as stream:
        json.dump(output, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"output": args.output, "different_pdf_pins": output["derived"]["different_recorded_sha256"], "recorded_size_difference_bytes": output["derived"]["recorded_size_difference_bytes"], "request_statuses": [x.get("status") for x in results]}))


if __name__ == "__main__":
    main()

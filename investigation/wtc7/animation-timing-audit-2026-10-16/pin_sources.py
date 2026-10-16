"""Hash only the explicitly named public source records; no recursive intake."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

PREFIX = "research/911-conspiracy-investigation-public/"
SWF_BASE = "http://www.nist.gov/public_affairs/releases/wtc_videos/"


def pin(path, label, url, kind):
    data = path.read_bytes()
    return {"label": label, "source_url": url, "access_kind": kind, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", required=True)
    parser.add_argument("--media-tree", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root, media = Path(args.case_root), Path(args.media_tree)
    records = []
    for relative, url in [
        ("authority/nist/wtc7/ncstar-1a.pdf", "https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861610"),
        ("authority/nist/wtc7/ncstar-1-9.pdf", "https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf"),
        ("exhibits/processed/exh-013-2011-04-07-dcd-quick-foia-memorandum-opinion.pdf", "https://www.govinfo.gov/content/pkg/USCOURTS-dcd-1_09-cv-02064/pdf/USCOURTS-dcd-1_09-cv-02064-0.pdf"),
        ("exhibits/processed/exh-018-2020-11-30-dcd-cole-v-nist-memorandum-opinion.pdf", "https://law.justia.com/cases/federal/district-courts/district-of-columbia/dcdce/1:2019cv01182/206571/20/")]:
        records.append(pin(root / relative, Path(relative).name, url, "Previously held public PDF, freshly read and hashed; URL is locator, not claim of fresh downloaded-byte equivalence"))
    for name, timestamp, asset in [
        ("CU_animation_20080829100216.swf", "20080829100216", "CU%20animation.swf"),
        ("whole_building_animation_20080829100049.swf", "20080829100049", "whole%20building%20animation.swf"),
        ("CU_animation_20080907013011.swf", "20080907013011", "CU%20animation.swf"),
        ("whole_building_animation_20080907013006.swf", "20080907013006", "whole%20building%20animation.swf")]:
        relative = "research/faraday-wtc7-model-compare/media/derivatives/archived-nist-swf/" + name
        records.append(pin(media / PREFIX / relative, relative, "https://web.archive.org/web/" + timestamp + "id_/" + SWF_BASE + asset, "Held archive response, exact expected SHA-256 checked; not reacquired or authenticated as NIST master"))
    for relative, page in [
        ("investigation/wtc7/causal-chain-synthesis/stable-control-2026-10-05/run02-657.png", "NCSTAR 1-9 printed 591"),
        ("investigation/wtc7/causal-chain-synthesis/stable-control-2026-10-05/run02-658.png", "NCSTAR 1-9 printed 592"),
        ("investigation/wtc7/animation-timing-audit-2026-10-16/ncstar-1-9-p593.png", "NCSTAR 1-9 printed 593"),
        ("investigation/wtc7/animation-timing-audit-2026-10-16/ncstar-1a-p43.png", "NCSTAR 1A printed 43")]:
        records.append(pin(media / PREFIX / relative, relative, None, "Local full-page rendering of named public PDF, visually inspected: " + page + "; raster is retained operationally, not newly published by this text-only commit"))
    for path in [Path("nist-faq-capture-2026-10-16.json"), Path("archive-index-probes-2026-10-16.json")]:
        records.append(pin(path, path.name, None, "New dated acquisition/capture sidecar; see its internal URLs, UTC times, response hash and outcome"))
    result = {"audit_date": "2026-10-16", "hashed_at_utc": datetime.now(timezone.utc).isoformat(), "records": records,
        "additional_web_sources": [
            {"url": "https://www.govinfo.gov/content/pkg/USCOURTS-caDC-18-05123/pdf/USCOURTS-caDC-18-05123-0.pdf", "status": "Primary judicial opinion read through web extraction; no local byte hash acquired"},
            {"url": "https://www.law.cornell.edu/uscode/text/15/7306", "status": "Statutory text read at Cornell mirror; no local byte hash acquired"},
            {"url": "https://www.loc.gov/preservation/digital/formats/fdd/fdd000629.shtml", "status": "Official format-preservation reference read through browser extraction; no local byte hash acquired"},
            {"url": "https://www.adobe.com/content/dam/acom/en/devnet/pdf/swf-file-format-spec.pdf", "status": "Browser fetch returned 404; not acquired"},
            {"url": "https://www.mobilefish.com/download/flash/swf_file_format_spec_v9.pdf", "status": "Adobe-authored document at third-party mirror identified in search. Browser fetch failed; direct urllib fetch returned HTTP 403. No PDF acquired or hashed."}],
        "old_reports": []}
    checkout = Path(__file__).resolve().parents[3]
    for relative in ["research/faraday-wtc7-model-compare/review/animation-version-comparison-2026-10-04.md", "research/faraday-wtc7-model-compare/review/avi-container-stream-header-audit-2026-10-04.md", "investigation/wtc7/causal-chain-synthesis/stable-control-2026-10-05/report.md", "investigation/wtc7/wayback-replay-capture-2026-10-09/cdx-replay-layer-discrepancy-2026-10-10.md"]:
        records_path = checkout / relative
        if records_path.exists():
            result["old_reports"].append(pin(records_path, relative, None, "Existing preserved report; unchanged, not an independent primary source"))
        else:
            data = subprocess.check_output(["git", "show", "HEAD:" + relative], cwd=checkout)
            result["old_reports"].append({"label": relative, "source_url": None, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "access_kind": "Read exact HEAD Git blob because sparse worktree omits this unchanged report; not an independent primary source"})
    with open(args.output, "x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"output": args.output, "pinned_records": len(records), "old_reports": len(result["old_reports"])}))


if __name__ == "__main__":
    main()

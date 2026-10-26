#!/usr/bin/env python3
"""Build a dated additive master from the frozen 152-entry public edition."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = "5bf1d9a3f03b843e0d8b7552ab3c78ae2acd7f63"
OLD = "investigation/wtc7/master-lead-register-2026-10-26"
STUDY = "investigation/broader-evidence/cia-lead-verification-2026-10-26"
WEB = "https://github.com/AveLyra/911-conspiracy-investigation/blob/"
PUBLIC_NOTES = ["README.md", "REPORT.md", "findings.json", "SOURCES.json", "EXCERPT-PINS.json", "SOURCE-EXCERPTS.md", "OPEN-QUESTIONS.json", "CHECKLIST.md", "VISUAL-REVIEW.json", "SOURCE-VERIFICATION.json", "PROTOCOL.md"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(path):
    return subprocess.check_output(["git", "show", BASE + ":" + path], cwd=ROOT)


def write(path, data):
    data = data.encode() if isinstance(data, str) else data
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == data:
            return
        raise FileExistsError(path)
    with path.open("xb") as stream:
        stream.write(data)


def js(path, data):
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def relocate(text):
    def link(match):
        target = match.group(1)
        if target.startswith(("https:", "http:", "#")):
            return match.group(0)
        return "](" + WEB + BASE + "/" + OLD + "/" + target + ")"
    return re.sub(r"\]\(([^)]+)\)", link, text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-study", type=Path, required=True)
    args = parser.parse_args()
    native = args.native_study.resolve()
    public = ROOT / STUDY
    copies = {}
    for name in PUBLIC_NOTES:
        data = (native / name).read_bytes()
        write(public / name, data)
        copies[name] = {"bytes": len(data), "sha256": sha(data)}
    original = json.loads(blob(OLD + "/register.json"))
    findings = json.loads((public / "findings.json").read_text())["findings"]
    sources = json.loads((public / "SOURCES.json").read_text())
    new_entries = []
    report_bytes = (public / "REPORT.md").read_bytes()
    for f in findings:
        locators = []
        urls = []
        for r in f["source_refs"]:
            p = sources["sources"][r["source_id"]]
            urls.append(p["url"])
            locators.append({**r, "source_sha256": p["sha256"], "source_url": p["url"],
                             "review_report": "../../broader-evidence/cia-lead-verification-2026-10-26/REPORT.md#" + f["id"].lower(),
                             "review_report_sha256": sha(report_bytes)})
        new_entries.append({"id": f["master_id"], "original_id": f["id"], "title": f["title"],
                            "category": "CIA dissemination, preservation and oversight records",
                            "status": "Independently checked review statements and source limitations; underlying historical messages remain unacquired.",
                            "original_record": f, "observation": f["observation"], "limit": f["limit"],
                            "next_test": f["next_test"], "locators": locators, "source_urls": list(dict.fromkeys(urls)),
                            "related": f["related"], "independence": "Shared oversight/document chains; not a new independent eyewitness or a proved conspiracy count."})
    register = {"date": "2026-10-26", "edition": "CIA-source verification continuation",
                "entry_count": 160, "prior_entry_count": 152, "new_entry_count": 8,
                "independent_anomaly_count": None, "prior_master_commit": BASE,
                "prior_master_metadata": {k: v for k, v in original.items() if k != "entries"},
                "entries": original["entries"] + new_entries,
                "new_source_catalog": sources, "new_open_questions": json.loads((public / "OPEN-QUESTIONS.json").read_text()),
                "prior_open_targets": original["current_open_targets"],
                "count_semantics": "160 overlapping research entries, including qualifications, contrary findings and low-weight precision questions; not 160 independent anomalies or established conspiracies."}
    js(HERE / "register.json", register)
    old_text = blob(OLD + "/MASTER-LIST.md").decode()
    body = relocate(old_text[old_text.index("## Register\n"):])
    intro = """# September 11 investigation — master list with CIA-source verification

October 26, 2026. **160 overlapping entries: M001–M152 preserved, plus M153–M160 / CL001–CL008.** This is not a count of independent anomalies or demonstrated conspiracies. The new entries were checked against government-review text and source provenance; no original 2000 CIR, hold order, delivery receipt or deletion log was authenticated.

[Independent CIA review](../../broader-evidence/cia-lead-verification-2026-10-26/REPORT.md) · [source URLs and hashes](../../broader-evidence/cia-lead-verification-2026-10-26/SOURCES.json) · [eight unresolved target sets](../../broader-evidence/cia-lead-verification-2026-10-26/OPEN-QUESTIONS.json) · [structured master](register.json) · [text changes](TEXT-CHANGES.diff) · [requirements](CHECKLIST.md).

The CIA report is a third-party-hosted mirror of an agency-issued review; official-host PDF bytes remain unavailable for comparison. The official download still returns maintenance HTML. Fresh DOJ and NARA source responses match the held copies. The anonymous MFR is not treated as an authenticated real-name or CIR-role join.

The preceding 152 records, contrary findings and BR/BPR targets remain unchanged. In the preserved body, only relative file links relocate to the fixed preceding edition. The new continuation narrows review-report availability for BR03 without closing its original-message and routing gaps. The apartment-payment 1A lead and $100,000 informant-payment track remain separate. These broader intelligence-sharing questions do not establish WTC7 access, demolition, manufactured attribution, motive or higher-level attack authorization.

## New-entry navigation

"""
    master = intro + "\n".join(f'- [{e["id"]} / {e["original_id"]} — {e["title"]}](#{e["id"].lower()})' for e in new_entries) + "\n\n" + body
    master += "\n\n## CIA decision, disclosure and preservation continuation\n\n"
    for e in new_entries:
        f = e["original_record"]
        master += f'<a id="{e["id"].lower()}"></a>\n### {e["id"]} — {e["title"]}\n\n'
        master += f'**Original ID:** {f["id"]}. **Type:** {f["claim_type"]}.\n\n{f["observation"]}\n\n'
        for q in f["conflicting_or_qualifying_records"]:
            master += "- " + q + "\n"
        if "additional_context" in f:
            master += "\n" + f["additional_context"] + "\n"
        master += f'\n**Exact source locations and retained excerpts:** [review section](../../broader-evidence/cia-lead-verification-2026-10-26/REPORT.md#{f["id"].lower()}); report SHA-256 `{sha(report_bytes)}`. Primary PDF physical/printed pages, HTML sections and text blocks are retained in register.json.\n\n'
        master += "**Public source links:** " + " · ".join(f'[source {n}]({u})' for n, u in enumerate(e["source_urls"], 1)) + ".\n\n"
        master += f'**Next record/test:** {f["next_test"]}\n\n**Limit:** {f["limit"]}\n\n'
        master += "**Related / overlapping:** " + ", ".join(f'[{i}](#{i.lower()})' for i in f["related"]) + ".\n\n"
    write(HERE / "MASTER-LIST.md", master.rstrip() + "\n")
    write(HERE / "README.md", """# Master list: CIA-source continuation

[Read all 160 entries](MASTER-LIST.md): the earlier M001–M152 remain unchanged, and M153–M160 incorporate eight qualified CIA/DOJ/NARA findings. Counts include overlap, qualifications and a low-weight timing mismatch; they are not independent conspiracies or proven errors.

- [Independent source review](../../broader-evidence/cia-lead-verification-2026-10-26/REPORT.md)
- [Source URLs, hashes and access limits](../../broader-evidence/cia-lead-verification-2026-10-26/SOURCES.json)
- [Structured register and original finding objects](register.json)
- [New unresolved questions](../../broader-evidence/cia-lead-verification-2026-10-26/OPEN-QUESTIONS.json)
- [Requirements and preservation](CHECKLIST.md)
- [Text diff against the immediately preceding master](TEXT-CHANGES.diff)
- [Source and integration checks](VERIFICATION.json)

The [preceding edition](https://github.com/AveLyra/911-conspiracy-investigation/tree/5bf1d9a3f03b843e0d8b7552ab3c78ae2acd7f63/investigation/wtc7/master-lead-register-2026-10-26) stays preserved. No earlier source payload or conflicting record was rewritten. The public update contains reviewed notes and pins, not original PDFs/media, private case information or credentials.

Run `python3 -B verify_cia_master.py`. The checks establish integration/preservation, not native historical-message authentication or motive. The source review separately records nine successful source-check groups, 14 complete CIA page-text reads, four complete MFR pages, 11 source-page visual reads and 42 excerpt pins. Publication bytes are verified separately after committing.
""")
    write(HERE / "CHECKLIST.md", """# CIA continuation: scope and acceptance

| User requirement | Completed artifact | Verification and unresolved limit |
| --- | --- | --- |
| Verify six incoming CIA leads | CL001–CL006 / M153–M158, independent report and source pins | Supported as review statements, not original messages; causal and identity limits explicit |
| Verify separate MFR | CL007 / M159; fresh matching four-page NARA PDF and official index row | Subject and catalog asset join remain unresolved |
| Preserve new timing issue | CL008 / M160; five/eight/week/date wordings | Low-weight precision question; no date adjudication |
| Preserve previous master and source studies | Exact M001–M152 objects and prior body with citation relocation only | Previous edition and original study blobs unchanged |
| Preserve conflict and adverse evidence | Formatting assessments, discovery dates, retention/deletion/copy records, FBI access, no-FBI-misconduct and issue-specific accountability findings | No general exoneration or attack-purpose conclusion |
| Keep questions open | CIAQ001–CIAQ008 and unchanged BR01–BR05/BPR01–BPR10 | Review-report acquisition does not fill native-original gaps |
| Preserve provenance and reading scope | SOURCES.json, EXCERPT-PINS.json, VISUAL-REVIEW.json, source-check receipt | Mirror-to-official CIA byte authentication unavailable; text and visual scopes distinct |
| Record revision and prior status | TEXT-CHANGES.diff and SCOPE.json protected-file pins | No PDF generated; PDF layout is not a text-diff check |
| Commit/push as AveLyra | Verify public remote/account and each new commit's author/committer | Remote checks occur only after commit/push; precommit receipt is not publication proof |
| Preserve privacy and scope | New text/JSON/code files only | No raw PDFs, HTML payloads, rasters, private case files, credentials or redaction reconstruction |

The source study preserves its failed extraction, citation corrections and test-sentinel issues locally. Those are our method errors, not historical discrepancies. No legal-fact promotion, private push, outreach, fee, deletion or history rewrite is part of this update.
""")
    names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE, "--", OLD,
        "investigation/wtc7/master-lead-register-2026-10-25",
        "investigation/broader-evidence/operational-record-followup-2026-10-26",
        "investigation/broader-evidence/bank-phone-integration-2026-10-26",
        "investigation/broader-evidence/bank-phone-records-2026-10-26"], cwd=ROOT, text=True).splitlines()
    protected = {name:{"bytes":len(blob(name)),"sha256":sha(blob(name))} for name in names}
    js(HERE / "SCOPE.json", {"date":"2026-10-26","base_commit":BASE,
        "repository":"AveLyra/911-conspiracy-investigation","public_native_note_copies":copies,"protected_files":protected,
        "scope":"Additive source review and 160-entry master. No raw-source payloads or private case information exported. Earlier publication and evidence files unchanged.",
        "native_source_check":"SOURCE-VERIFICATION.json records nine source-check groups; not a native historical-message authentication.",
        "navigation":"Existing investigation/MASTER-LIST.md is preserved on main by this additive publication. Any change to that existing pointer is prepared separately for PR review under the user's non-overwrite preference."})
    print(json.dumps({"entries":160,"additions":8,"public_note_copies":len(copies),"protected_files":len(protected)}))


if __name__ == "__main__":
    main()

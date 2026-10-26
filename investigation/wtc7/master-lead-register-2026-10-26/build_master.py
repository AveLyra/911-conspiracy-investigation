#!/usr/bin/env python3
"""Build an additive master edition from fixed, already-public research records."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = "838af60393017b74e3fee08bd190bb7a9e8a0f04"
BASELINE_COMMIT = "ddd475b4e3c43a92a713426b6dc4c9f350930abd"
OLD = "investigation/wtc7/master-lead-register-2026-10-25"
RF = "investigation/broader-evidence/operational-record-followup-2026-10-26"
BI = "investigation/broader-evidence/bank-phone-integration-2026-10-26"
BP = "investigation/broader-evidence/bank-phone-records-2026-10-26"
WEB = "https://github.com/AveLyra/911-conspiracy-investigation/blob/"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def raw(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def load(path):
    return json.loads(raw(path))


def put(name, data):
    path = HERE / name
    data = data.encode() if isinstance(data, str) else data
    if path.exists():
        if path.read_bytes() == data:
            return
        raise FileExistsError(f"Refusing to replace {name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def js(name, data):
    put(name, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def fixed(path, lines=None, commit=BASE):
    suffix = "" if lines is None else f"#L{lines[0]}-L{lines[1]}"
    return WEB + commit + "/" + path + suffix


def relocate_baseline(text):
    def link(match):
        target = match.group(1)
        if target.startswith(("https:", "http:", "#")):
            return match.group(0)
        return "](" + fixed(OLD + "/" + target, commit=BASELINE_COMMIT) + ")"
    return re.sub(r"\]\(([^)]+)\)", link, text)


def main():
    old = load(OLD + "/register.json")
    rf = load(RF + "/findings.json")["findings"]
    bp = load(BI + "/integrated-findings.json")["findings"]
    pins = load(RF + "/source-pins.json")
    bp_pins = load(BI + "/sources/published/SOURCES.json")
    targets = load(BI + "/targets-v2.json")
    rf_lines = raw(RF + "/REPORT.md").decode().splitlines(keepends=True)
    headings = [(i, x.rstrip()) for i, x in enumerate(rf_lines) if x.startswith("## ")]
    rf_sources = {
        "RF001": ["MFR-NARA", "MFR-COMMONS", "FBI2016"],
        "RF002": ["MFR-NARA", "FBI2C5"],
        "RF003": ["MFR-NARA", "FBI2C5", "NOTES"],
        "RF004": ["MFR-NARA", "NOTES"],
        "RF005": ["D11182", "P10199"],
        "RF006": ["D11180", "D11182", "P10199", "K9795"],
        "RF007": ["OIG2005", "OIG2006"],
        "RF008": ["K9795", "P10199", "D11182", "MFR-NARA"],
    }
    pin_by_id = {p["id"]: p for p in pins["sources"]}
    source_by_url = {p["url"]: p for p in pins["sources"]}
    for key in ("new_retrievals", "preceding_sources_reused"):
        for p in bp_pins[key]:
            if "sha256" in p and "url" in p:
                source_by_url.setdefault(p["url"], p)

    additions, excerpts, rows = [], [], []
    for n, item in enumerate(rf + bp, 135):
        ident = item["id"]
        if ident.startswith("RF"):
            h = next(i for i, (_, text) in enumerate(headings) if text.startswith(f"## {ident}:"))
            first, header = headings[h]
            stop = headings[h + 1][0]
            excerpt = "".join(rf_lines[first + 1:stop])
            source_path = RF + "/REPORT.md"
            lines = [first + 1, stop]
            title = header.split(": ", 1)[1]
            title = title[:1].upper() + title[1:]
            primary = [pin_by_id[k] for k in rf_sources[ident]]
            urls = [p["url"] for p in primary]
            summary, limit, next_input = item["observation"], item["limit"], item["next_input"]
            scope = "Operational records; a separate September 11 lead, not a WTC 7 mechanism or access finding."
        else:
            excerpt = item["verbatim_published_body"]
            source_path = BP + "/RECORD.md"
            lines = item["source_lines_1based"]
            title = item["heading"].split(" — ", 1)[1]
            urls = list(dict.fromkeys(re.findall(r"\]\((https?://[^)]+)\)", excerpt)))
            primary = [source_by_url[u.split("#", 1)[0]] for u in urls if u.split("#", 1)[0] in source_by_url]
            summary = "Original published bank/telephone entry incorporated verbatim below; this edition adds navigation, not a new historical observation."
            limit = item["integration_limit"]
            next_input = "Retain all BPR01–BPR10 targets and BR01–BR05 statuses; see the current target ledger and the entry's original open test."
            scope = "Bank/telephone metadata, assistance and custody; speakers, content and attack knowledge are not established by call rows alone."
        eid = f"M{n:03}"
        locator = {
            "repository_path": source_path,
            "commit": BASE,
            "source_sha256": sha(raw(source_path)),
            "physical_or_text_convention": "One-based research text lines; primary PDF physical pages/Bates references are stated in the unchanged excerpt.",
            "text_lines_1based": lines,
            "public_report": fixed(source_path, lines),
            "excerpt": excerpt,
            "excerpt_sha256": sha(excerpt.encode()),
        }
        report_text = raw(source_path).decode()
        offset = report_text.index(excerpt)
        excerpt_start = report_text[:offset].count("\n") + 1
        locator["excerpt_text_lines_1based"] = [excerpt_start, excerpt_start + len(excerpt.splitlines()) - 1]
        byte_start = raw(source_path).index(excerpt.encode())
        locator["excerpt_bytes_zero_based_half_open"] = [byte_start, byte_start + len(excerpt.encode())]
        entry = {
            "id": eid, "title": title,
            "category": "Broader operational records" if ident.startswith("RF") else "Bank and telephone records",
            "status": "Existing published research incorporated without adjudicating conflicting accounts.",
            "original_id": ident, "original_record": item,
            "observation": summary, "limit": limit, "next_test": next_input,
            "scope_boundary": scope,
            "locators": [locator], "source_urls": urls,
            "primary_source_pins": [{k: v for k, v in p.items() if k in ("id", "url", "sha256", "bytes", "checked_or_held_date", "accessed_utc")} for p in primary],
            "independence": "Repeated sources and related entries are not independent corroborations; no independent-anomaly count is assigned.",
            "verification": "Exact fixed-commit research excerpt and source-ledger transfer; no new primary-source acquisition, scientific replication or historical adjudication in this integration.",
            "related": [],
        }
        additions.append(entry)
        excerpts.append(f'<a id="{eid.lower()}"></a>\n## {eid} / {ident} — {title}\n\n'
                        f'Source: [{source_path}, lines {lines[0]}–{lines[1]}]({locator["public_report"]}); '
                        f'whole-source SHA-256 `{locator["source_sha256"]}`; exact excerpt SHA-256 `{locator["excerpt_sha256"]}`.\n\n'
                        + excerpt + "\n")
        rows.append(f'| [{eid}](MASTER-LIST.md#{eid.lower()}) | {ident} | {title} |')

    related = {
        "M135": ["M136", "M137", "M138"], "M136": ["M135", "M137"],
        "M137": ["M135", "M136", "M147"], "M138": ["M135", "M139"],
        "M139": ["M140", "M142"], "M140": ["M139"],
        "M141": ["M143", "M151"], "M142": ["M139"],
        "M143": ["M144", "M145", "M151"], "M144": ["M143"],
        "M145": ["M143"], "M146": ["M147", "M148", "M150", "M152"],
        "M147": ["M146", "M148"], "M148": ["M146", "M147", "M152"],
        "M149": ["M150", "M152"], "M150": ["M146", "M149"],
        "M151": ["M141", "M143"], "M152": ["M146", "M148", "M149"],
    }
    for entry in additions:
        entry["related"] = related[entry["id"]]
    register = {
        "date": "2026-10-26", "edition": "Additive broader-record integration; inherited master claims not re-audited",
        "entry_count": 152, "baseline_entry_count": 134, "new_entry_count": 18,
        "independent_anomaly_count": None,
        "baseline_commit": BASELINE_COMMIT, "integration_source_commit": BASE,
        "inherited_register_metadata": {k: v for k, v in old.items() if k != "entries"},
        "entries": old["entries"] + additions,
        "new_primary_source_catalogs": {"operational": pins, "bank_phone": bp_pins},
        "current_open_targets": targets,
        "count_semantics": "152 overlapping research entries, including questions, qualifications, confirming checks and source/provenance leads; not 152 independent anomalies or established conspiracy facts.",
    }
    js("register.json", register)
    js("OPEN-TARGETS.json", targets)
    put("SOURCE-EXCERPTS.md", "# Exact research excerpts for M135–M152\n\n"
        "These are already-public research excerpts, not new witness testimony. Original PDF page references, source wording and open tests remain unchanged. See register.json for primary URLs and hashes.\n\n" + "\n".join(excerpts))
    put("CROSSWALK.md", "# Master ID to original finding ID\n\n"
        "M001–M134 retain their original IDs and structured records. The following mapping incorporates all eight RF and all ten BP findings without treating overlap as independent evidence.\n\n"
        "| Master ID | Original ID | Topic |\n| --- | --- | --- |\n" + "\n".join(rows) + "\n\n"
        "RF and BP IDs remain valid in their original studies. The broader documentary inventory and its S001–S014 source findings are linked dependencies, not silently promoted to additional M entries by this bounded update.\n")
    intro = """# September 11 investigation — integrated public master lead register

October 26, 2026. Research by AveLyra. **152 overlapping entries: unchanged M001–M134 plus M135–M142 (RF001–RF008) and M143–M152 (BP01–BP10).** This is not a count of independent anomalies, proven errors or established conspiracies.

WTC 7 engineering remains a separate evidence track. The appended operational, witness, financial and telephone records do not establish an actor, access chain or demolition mechanism for WTC 7. The published studies contain both questions and confirming/contrary evidence. In particular, BP08's narrow eight-call carrier check supports the matching FBI account; it is retained alongside the conflicts.

[ID crosswalk](CROSSWALK.md) · [structured master and source pins](register.json) · [unchanged research excerpts](SOURCE-EXCERPTS.md) · [current open targets](OPEN-TARGETS.json) · [integration checklist](CHECKLIST.md) · [text changes](TEXT-CHANGES.diff).

The complete earlier register remains frozen at [its original publication](https://github.com/AveLyra/911-conspiracy-investigation/tree/ddd475b4e3c43a92a713426b6dc4c9f350930abd/investigation/wtc7/master-lead-register-2026-10-25). In the inherited body below, scientific wording, IDs, conflicting records and contrary findings are unchanged; only relative source-file links are relocated to that fixed public edition. Original source packages remain unchanged. No historical discrepancy is adjudicated here.

The five BR bundles and all ten BPR targets are preserved verbatim in OPEN-TARGETS.json. The apartment-payment 1A-file lead is distinct from the July 2003 $100,000 informant-payment inquiry; neither is used to close the other. Source/call counts are not counts of people, unique conversations, foreknowledge or independent corroborations.

## New-entry navigation

"""
    old_text = raw(OLD + "/MASTER-LIST.md").decode()
    inherited_body = relocate_baseline(old_text[old_text.index("## Register\n"):])
    master = intro + "\n".join(f'- [{e["id"]} / {e["original_id"]} — {e["title"]}](#{e["id"].lower()})' for e in additions) + "\n\n" + inherited_body
    master += "\n\n## Broader operational-record and bank/telephone additions\n\n"
    for e in additions:
        loc = e["locators"][0]
        master += f'<a id="{e["id"].lower()}"></a>\n### {e["id"]} — {e["title"]}\n\n'
        master += f'**Original ID:** {e["original_id"]}. **Family:** {e["category"]}.\n\n'
        master += f'**Scope and verification:** {e["scope_boundary"]} {e["verification"]}\n\n'
        master += f'**Preserved source text:** [exact excerpt](SOURCE-EXCERPTS.md#{e["id"].lower()}) · [pinned research source]({loc["public_report"]}); SHA-256 `{loc["source_sha256"]}`.\n\n'
        master += loc["excerpt"] + "\n"
        master += f'**Recorded limit:** {e["limit"]}\n\n**Next record/test:** {e["next_test"]}\n\n'
        master += "**Public source URLs:** " + " · ".join(f'[source {i}]({u})' for i, u in enumerate(e["source_urls"], 1)) + ".\n\n"
        master += "**Related / overlapping:** " + ", ".join(f'[{i}](#{i.lower()})' for i in e["related"]) + ".\n\n"
    put("MASTER-LIST.md", master.rstrip() + "\n")
    put("README.md", """# Integrated public master list — October 26, 2026

[Read all 152 entries](MASTER-LIST.md): M001–M134 are preserved, and M135–M152 incorporate all eight operational-record and ten bank/phone findings. These are overlapping research entries, not independent anomalies or established conspiracy findings. The prior 134-entry edition and all source studies remain unchanged.

- [Structured register, original RF/BP records and source hashes](register.json)
- [Original-to-master ID crosswalk](CROSSWALK.md)
- [Exact source excerpts and fixed-commit line references](SOURCE-EXCERPTS.md)
- [All five BR bundles and ten BPR acquisition targets](OPEN-TARGETS.json)
- [Scope, preservation and requirement checklist](CHECKLIST.md)
- [Text diff against the preceding master](TEXT-CHANGES.diff)
- [Integrity verification](VERIFICATION.json)

CALL-ROWS.json, NEXT-RECORDS.md and recount_calls.py are byte-exact redundant copies of the original bank study's public dependencies, included so its preserved excerpt links continue to work. The recount program requires the pinned underlying source PDF to be supplied; it was not rerun in this master-list integration.

The original studies remain at the [operational-record package](../../broader-evidence/operational-record-followup-2026-10-26/README.md) and [bank/phone integration](../../broader-evidence/bank-phone-integration-2026-10-26/README.md). Their historical local/unpublished wording remains a preserved earlier status; publication was completed at 838af603. The new master references that fixed source commit and does not rewrite its history.

The narrow confirming carrier sample is retained alongside reimbursement/sign, amount/source, date, endpoint and count differences. No preferred explanation is selected. Original PDFs and media remain unchanged in local source holdings; this edition copies already-public research text and source catalogs, not raw account/contact data or private case material. Hashes pin captured bytes, not historical truth.

Run `python3 -B verify_master.py`. The checks cover ID/excerpt/link/target preservation and unchanged source files. They do not reauthenticate missing originals, rerun engineering, decide historical intent or establish an actor/demolition connection. PDF/layout verification is not applicable: no PDF was produced. Remote publication must be verified separately after committing.
""")
    put("CHECKLIST.md", """# Requirements, preservation and unresolved work

Scope: integrate the already-published operational-record and bank/phone studies into an additive edition of the public master; do not adjudicate their conflicts or promote research into case facts. Dependencies are fixed public commits ddd475b4 (134-entry baseline) and 838af603 (published operational/integration package, including the bb9e9c5d bank study). The acceptance criteria below are checked by verify_master.py.

| User requirement | Outcome/location | Verification and unresolved issue |
| --- | --- | --- |
| Include operational findings | M135–M142 / RF001–RF008, MASTER-LIST.md and register.json | Original RF objects and research sections retained exactly; historical recollections remain qualified |
| Include bank/phone findings | M143–M152 / BP01–BP10 | Original BP objects, full excerpts, page/Bates references and open tests retained exactly |
| Preserve earlier master | Unchanged M001–M134 records; preceding body preserved except relative-link relocation | All 14 earlier package blobs unchanged; inherited claims not freshly re-audited |
| Preserve source links and provenance | Source catalogs, primary hashes, fixed commit and one-based report-line locators | Copy/source identity does not authenticate every factual assertion; external sources not freshly fetched. Exact excerpt spans are recorded separately from heading/separator-inclusive entry spans |
| Preserve conflicting records | Full excerpts include $1,558 signs, $4,000–$8,000/$9,900, April 19/20, 22/27, CBR/cell, chronology/language/copy-locator differences | Causes remain unresolved; dates/units/scopes are not normalized |
| Preserve contrary/confirming evidence | Existing contrary-findings section; coincidence account; narrow carrier confirmation at M150 / BP08; judicial qualifications | Not a selection containing only incriminating observations |
| Carry unresolved questions | Exact targets-v2 in OPEN-TARGETS.json and register.json; all five BR and ten BPR IDs | Receipt/teller/February 4 carrier originals, earlier interviews, CIA routing, informant payment and full notebook/expert exhibits remain open |
| Keep different payment tracks distinct | Master introduction, M141 and M151 | Apartment-payment 1A attachments do not supply the $100,000 informant voucher |
| Avoid duplicate-evidence inflation | 152 overlapping entries; RF/BP crosswalk and dependence statements | Repeated reports, aliases, mirrors and analysis rows are not independent witnesses/calls |
| Preserve originals and public scope | New directory and additive navigation file only; protected-file pins in SCOPE.json | No raw PDF/media, personal account/contact data, correspondence, credentials or private case material added |
| Revision accountability | TEXT-CHANGES.diff compares the new full master with its immediate predecessor; other new Markdown compared to /dev/null | Earlier source-package status remains unchanged; PDF/layout checks are separate and not applicable |
| Commit/push as AveLyra | Check exact public repository, authenticated account and new author/committer before push | VERIFICATION.json is precommit integrity evidence, not a claim of completed remote verification |

No outreach, fee, private-repository push, source repair, force-push or history rewrite is part of this update. A failure to locate an original is not proof of destruction, concealment or wrongdoing. No independent probability or final causal conclusion is assigned.

The candidate checks found packaging issues: bank entry spans included a separator outside an exact excerpt, the final excerpt has no terminal newline, and preserved relative links needed three byte-exact public dependencies. The corrected candidate records exact excerpt spans and includes those dependencies. Source text and its original line-range fields were not edited; failed candidate/check records remain preserved locally. These were integration issues, not anomalies in the historical evidence.
""")
    for name in ("CALL-ROWS.json", "NEXT-RECORDS.md", "recount_calls.py"):
        put(name, raw(BP + "/" + name))
    protected = {}
    paths = [OLD, RF, BI, BP]
    names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE, "--", *paths], cwd=ROOT, text=True).splitlines()
    for name in names:
        data = raw(name)
        protected[name] = {"bytes": len(data), "sha256": sha(data)}
    js("SCOPE.json", {
        "date": "2026-10-26", "base_commit": BASE, "baseline_commit": BASELINE_COMMIT,
        "repository": "AveLyra/911-conspiracy-investigation", "branch_destination": "main",
        "payload": "New integrated master edition, exact already-public RF/BP research excerpts/source catalogs/open targets, crosswalk, reproducible builder, preservation checks, text diff and additive investigation master pointer.",
        "excluded": ["Raw source PDFs/media", "private case material or strategy", "personal account/contact details", "credentials", "new source adjudication or solver work"],
        "protected_files": protected,
        "primary_source_fetches_this_integration": False,
        "redundant_public_dependencies": {name: {"source": BP + "/" + name, "sha256": sha(raw(BP + "/" + name))} for name in ("CALL-ROWS.json", "NEXT-RECORDS.md", "recount_calls.py")},
        "inherited_body_change": "Only relative file citations relocate to their original fixed public edition; source words and all prior IDs/structured entries remain unchanged.",
        "no_prior_public_files_modified": True,
    })
    nav = ROOT / "investigation/MASTER-LIST.md"
    pointer = """# Current integrated investigation master list

The [October 26, 2026 master](wtc7/master-lead-register-2026-10-26/MASTER-LIST.md) contains **152 overlapping research entries**: unchanged M001–M134 plus eight operational-record and ten bank/phone findings. This count includes questions, source leads, qualifications and a confirming check; it is not a count of independent anomalies or established conspiracy facts.

[ID crosswalk](wtc7/master-lead-register-2026-10-26/CROSSWALK.md) · [source pins and original records](wtc7/master-lead-register-2026-10-26/register.json) · [unresolved targets](wtc7/master-lead-register-2026-10-26/OPEN-TARGETS.json).

The [October 25 edition](wtc7/master-lead-register-2026-10-25/README.md) remains an unchanged historical 134-entry baseline. Conflicting accounts and source studies are preserved; broader operational leads are not presented as evidence of a WTC 7 demolition connection.
"""
    if nav.exists() and nav.read_text() != pointer:
        raise FileExistsError("Existing investigation master pointer differs")
    if not nav.exists():
        nav.write_text(pointer)
    print(json.dumps({"entries": 152, "additions": 18, "protected_files": len(protected), "source_commit": BASE}))


if __name__ == "__main__":
    main()

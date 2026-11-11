# Repository guide: 9/11 research and Faraday software

This index separates the investigation's evidence and dated historical research from the Faraday Research Machine software. The two dated WTC 7 documents and Faraday were relocated under the approved move plan. Compatibility pages remain at the old document paths and a filesystem symlink at the former Faraday path; old GitHub web links through the directory symlink may not work.

## Investigation

- [Developing theory and tests](../urban-moving-systems/developing-theory-2026-11-06/README.md): current working hypothesis, competing explanations and missing links.
- [Master list](../MASTER-LIST.md) and [evidence topic index](../topics/evidence-index.md): current navigation and source leads.
- [WTC 7 historical summaries](../wtc7/historical-summaries/README.md): the dated September findings and October lead review, with scope-specific labels. The old root filenames remain compatibility pages.
- [WTC 7 research](../wtc7/STATUS.md), [Urban Moving Systems](../topics/urban-moving-systems-911-fbi-records.md), and [broader original-record work](../broader-evidence/): topic-specific research.

## Faraday Research Machine

[Faraday](../../tools/faraday/README.md) is a self-contained research-software project, not an evidence report or proof of any historical claim. Its [operating contract](../../tools/faraday/AGENTS.md), [license](../../tools/faraday/LICENSE), executable, source code, schemas, documentation and tests belong together. Moving it without auditing internal relative paths, scripts, links and reproducibility could break the tool. Its presence in this investigation repository does not transfer its governance or evidence standards to historical findings.

## Relocation inventory and protection

The [proposed-path inventory](RELOCATION-INVENTORY.txt) lists the two top-level historical documents and all 256 Faraday paths in the reviewed Git tree. It is the pre-move planning inventory, not the current paths. The approved relocation preserves the pre-move commit, adds root compatibility pages and a Faraday filesystem symlink, and keeps LFS objects outside this move. The directory symlink does not guarantee old GitHub web URLs or Windows compatibility.

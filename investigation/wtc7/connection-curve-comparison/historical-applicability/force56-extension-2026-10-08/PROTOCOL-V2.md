# Version 2: restore carried-forward inventory qualifications

October 8, 2026. Declared after both version-1 integrations, before version-2
outputs. Independent review found the updated F5 inventory prose omitted an
older caution: generic same-column peer band references in the unchanged
Im2/Im4 readings can flag an unrelated route. The new Im3 references are more
specific, but that does not repair the old records. Explicitly retain F6's
older repeated-identifier/unknown-span continuity qualification as well.

Preserve `extend.py`, `test_extend.py`, `run01.json` and `run02.json` unchanged.
Both outputs have SHA256
`79f63ff2618de2d53ad7467a19372b1f5ba97ff36677f6ca61d13d51ff8c6d8f`.
This is a current-inventory wording correction, not an annotation, algorithm,
coordinate, exclusion, model-error or historical finding. Version-1's 168
checked pins and arithmetic remain, but its inventory qualification was incomplete.

The version-2 wrapper first verifies both saved copies and all their input
pins, then deep-copies version 1. Append only these sentences to the indicated
pair's `identity_and_topology_limits`:

- F5: "Older Im2/Im4 peer generic same-column band references can flag an
  unrelated route; those original references and conditional exclusions remain
  unchanged."
- F6: "A repeated fragment ID across an unknown span does not establish
  continuity."

Change only top-level status/version, input maps and an added correction record
beyond those two strings. Every original, conditional decision, coordinate hull,
summary, region, other inventory field, axis and assumption must exactly equal
version 1. The earlier 38 readings still exactly equal the prior approach
extension. No rerunning the historical arithmetic with altered choices.

Pin both version-1 copies and this protocol, wrapper and tests in the new
before/after map. Save `run-v2-01.json` and `run-v2-02.json` exclusively;
require byte equality. Test strict version identity, exact allowed changes,
both mandatory qualifications and refusal to overwrite. The separate checker
must verify version-2 versus version-1 preservation as well as the full
740-row independent arithmetic and transitive-input requirements of the
original protocol. Preserve the initial synthetic path-normalization failure,
initial sandbox-denied save and the version-1 wording omission in validation.

All original evidence and acceptance limits remain. No causal-ranking change,
human acceptance, legal promotion, external disclosure, commit or push.

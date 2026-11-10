# Actual verification outcome

October30,2026. The reviewed candidate code was run a second time against the same pinned court archive/helper using the explicitly recorded bundled Python3.12.14, NumPy2.3.5 and FFmpeg/ffprobe7.1.1.

All non-diagnostic fields matched under the predeclared comparison: exact discrete/string/hash/parameter values and tolerance1e−9 for float metrics. The maximum observed float difference was **0** across203 compared float fields. These are fields from the same related computation, not203 independent observations or sources. In this particular environment the full raw logs were also byte-identical: **57,936 bytes**, SHA-256 **d4a83ea2ad412da6a4fb62aeefdeb81ddabe1e0feec2c8ff50cae284c80574f1**. No diagnostic differences were observed. Every raw log remains preserved unchanged; universal cross-build byte identity is not claimed.

[REPRODUCTION.json](REPRODUCTION.json) is the actual receipt; [REPRODUCE.md](REPRODUCE.md) specifies the commands and limits. Positive/negative sign/gain/DC/noise controls and direct-versus-FFT checks passed. Prior event PCM fingerprints matched the earlier published decodes, and new root PCM counts matched stored block-count prefixes. These are preservation/implementation consistency checks; they do not validate voices, complete conversations, source custody, runtime behavior or a historical clock.

The seven substantive note/code/source/result files in candidatev1 are unchanged in candidatev2. This update adds this verification note and the actual receipt, and regenerates only the additive diff/companion manifest. The immediately preceding candidate and exact local candidatev1→v2 diff remain preserved; no previous report or original evidence is replaced.

Publication remains **TODO** under the current AveLyra SSH constraint. A local public-repository commit is distinct from a remote push. No new public commit/ref or PR is claimed by this note, and all five tracks/eighteen substantive original-record criteria remain unfinished.

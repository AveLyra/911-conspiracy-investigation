# Reproducing the conditional calculation

Run `python3 stoichiometry.py` in a fresh local copy of this directory. It uses only Python's standard library, writes a new `STOICHIOMETRY-RESULT.json` beside the script, and exits nonzero on a failed assertion. It never overwrites an existing result. The published reference output is named **CONDITIONAL-CHECK.json**; it is the same complete result that the report refers to as STOICHIOMETRY-RESULT.json. Compare parsed JSON values rather than platform-specific formatting.

The twelve checks verify conditional algebra and boundary/monotonicity cases. They do not establish the measured Al:O ratio, its uncertainty, metallic aluminum, thermitic identification, specimen identity or historical cause. Rounded atomic masses27/16 and the atom/mass alternatives are explicit assumptions. Native spectra and calibration/geometry records remain needed.

This additive reproduction note and script accompany the five previously published materials files without changing them. Earlier report text, results and prior claims remain preserved in Git history and at their original commits. No original paper, image, laboratory export, private case material or personal/session metadata is included.

# Scooby claim verification: insurance, FAA, timing, FDR and structural models

November 11, 2026. This is a set of **bounded claim checks**, not verification of every claim in the associated reports. Source documents are distinguished from the events or conditions they describe; missing originals and model inputs remain open. No finding below establishes a common operational plan or UMS involvement.

## Insurance benefit investigation — selected financing claim

GMAC's [2001 Form 10-K](https://www.sec.gov/Archives/edgar/data/40729/000004072902000015/gmac10k2001.txt) reports a $563 million loan secured by leasehold interests in four WTC properties, with $483 million of bonds sold and $80 million retained. It says insurance required in connection with financing did not exclude terrorism. This supports the stated financing connection as a contemporaneous corporate filing, while postdating the attacks; it does not supply the original insurance binder, establish every lease provision, calculate the leaseholder's net gain, or establish the policyholder's knowledge. Test those further claims against the original transaction documents, policy schedules, settlement allocations, debt and rebuilding costs.

## Records follow-up — FAA correction

The [August 31, 2006 DOT OIG report, pp. 1–3 and 10–13](https://www.oig.dot.gov/sites/default/files/cc2006085.pdf), records that the FAA's May 22, 2003 response incorrectly stated that DOD had been notified of Flight 77 at 9:24. The OIG says three executives learned of a separate inaccuracy about the Air Force liaison's phone-bridge entry and did not get the Commission record corrected; it recommended correction and consideration of administrative action. The report also says its investigation found no evidence to conclude that FAA officials knowingly made false statements or intentionally failed to correct an inaccurate statement regarding FAA notifications to DOD. The finding of an uncorrected liaison entry and the scoped lack-of-intent finding must both be retained. Whether the recommendation was carried out remains a separate records question.

## Original media and timing — seismic estimate

The [Commission's notes, printed pp. 461–462, note 168](https://www.govinfo.gov/content/pkg/GPO-911REPORT/pdf/GPO-911REPORT-23.pdf#page=15), describe a published Flight 93 seismic estimate of 10:06:05 ± 5 seconds and reject its use to contradict a combined recorder, air-traffic, radar and impact-site estimate, citing weak signal-to-noise and uncertain signal source. This verifies the Commission's stated position and rationale; the independent clock alignments, identification of the seismic event and original media are not reproduced by this check. A small reported uncertainty conditional on a chosen signal is not the same as resolving whether it is the impact signal.

## Korol arrest calculation — first-stage arithmetic

[Korol, Heerema and Sivakumaran, printed pp. 28–31](https://www.challengejournal.com/index.php/cjsmec/article/download/50/41), present an assumed upper-block descent, column resistance and floor-by-floor momentum model. Independently entering the report's quoted inputs with g = 9.81 m/s² gives normal floor mass 1,885,260 kg, mechanical floor mass 2,395,851 kg, upper mass 74,045,872 kg, assumed work for 27 columns 0.789073 GJ, and pre-impact speed 7.416786 m/s, consistent with the paper's rounded 7.42 m/s. Using the computed unequal masses for a perfectly inelastic first floor impact gives 7.232638 m/s; the paper uses a 35/36 floor-count approximation to produce approximately 7.21 m/s. This checks the first stage only, not the later stopping floor, actual energy dissipation, or whether the assumed mechanism represents WTC 7. Model selection and assumption sensitivity remain material.

## Moussaoui exhibit 633 — actual scanned record

The one-page [defense exhibit 633](https://coop.vaed.uscourts.gov/moussaoui/exhibits/defense/633.pdf) was retrieved, rendered, OCR-screened and visually checked. Its header identifies Harry Samit as sender, Charles Frahm and G. Jones as recipients, August 22, 2001 at 10:13 a.m., and subject “747 Information.” The email says an opening EC is attached, describes additional leads and relays redacted French information linking Moussaoui to a deceased person who fought with al-Khattab. The public one-page exhibit does not include that attachment and does not establish that any particular decision-maker opened or reviewed it. The email records what Samit sent or asserted; it does not independently authenticate every allegation in it. Compare actual attachment versions, routing/receipt and attorney review before making claims about the whole dossier.

## Flight 77 FDR — channel validation

The original scanned [NTSB FDR report](https://www.ntsb.gov/about/Documents/AAL77_fdr.pdf), PDF p. 2, says its plotted/tabular output includes validated parameters listed in I-1–I-4; I-5–I-13 identify parameters not properly recorded or not confirmed. On visual and OCR inspection, PDF p. 8, printed I-3 lists pressure altitude in the plotted group; PDF p. 10 introduces the unconfirmed/nonworking group; PDF p. 13, printed I-8 lists “FLT DECK DOOR,” “GMT” and “GPS TIME” in that group. The report does not separate nonworking from unconfirmed for each label. A field in a decoding list is not proof of a functioning aircraft sensor, and its unconfirmed status is not proof that the circuit was absent or that the door was shut. Installation records and raw-channel validation remain open.

## Orabi model — duration and counterfactual

The [published Orabi manuscript, pp. 17–21](https://ira.lib.polyu.edu.hk/bitstream/10397/92640/1/Orabi_Collapse_World_Trade.pdf#page=17), reports that a case with 22 mm protection on the diagonals did not fail in the modeled heating stage. For Model 2 it says the dynamic run was terminated after 2.3 seconds because of file size and computation time; approximately 0.8 m concerns floor deflection over the modeled transfer region, not measured roofline descent. Page 16 describes one hour of pseudo-static heating represented in 0.36 seconds of analysis time before an unscaled dynamic stage. That scheme is not automatically wrong, but independent reproduction should check the transferred state and energy, validate connections, and compare camera-matched outputs. Stopping a calculation is not evidence that physical motion arrested, and the simulation does not by itself validate a complete collapse sequence.

## Method and remaining scope

Checked the cited source passages directly; rendered the two scanned PDFs with PyMuPDF, screened with Tesseract and visually reviewed the pertinent exhibit and recorder page. Recalculated the Korol first stage with a short Python arithmetic script. The commission seismic argument is a reported assessment, not a reanalysis of its underlying data. These seven scoped checks leave most material claims, attachments and contrary evidence across the 30 reports to be verified.

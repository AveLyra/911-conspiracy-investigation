# Korol arrest calculation: recovered report numerical checks

November 12, 2026. This checks selected numerical claims in the recovered body and table of Scooby report 13 against [Korol, Heerema and Sivakumaran (2016), pp. 25–31](https://www.challengejournal.com/index.php/cjsmec/article/download/50/41), and an independently executed [arithmetic reconstruction](reproduce.py). It does not review the full Scooby report, all attachments, or all 30 reports, and it is not a simulation of WTC 7.

## What the paper states

The paper's Eq. 3–5 use an idealized descending block, inelastic impacts, assigned column-work capacity and concrete pulverization work. It reports an upper-block mass of 74,038,000 kg, a first-drop speed of 7.42 m/s, count-based impact factors including 35/36 and 37/38, and an arrest in Storey 11 when Eq. 5's balance becomes negative. On p. 30 it assigns 32.01 GJ to five floors at 101.6 mm concrete depth; on p. 31 Eq. 5 specifies 101.4 mm. The distinction between 101.4 and 101.6 is in the original text, but the source does not establish whether it is a typo or deliberate change.

## Reproduced arithmetic and boundaries

Using the listed floor area and loading, g = 9.81 m/s², uniform 3.89 m storey height and 3.5 column multiplier, the script obtains a block mass of 74,045,872 kg and first-drop speed of 7.416786 m/s. Applying *mass-consistent*, perfectly inelastic collision ratios rather than the paper's floor-count approximations gives 7.232638 and 10.133436 m/s immediately after the two collisions. These are results of the specified alternative arithmetic, not measured building velocities. The paper's 37/38 factor follows a first 35/36 factor, but its intended indexing cannot be established without the authors' calculation.

At the third balance with 101.6 mm concrete depth, the reconstruction gives approximately 6.964891 GJ available before assigned resistance, 2.396443 GJ column work, and 4.603626 GJ full slab work: a **−0.035178 GJ** residual. With slab work reduced to 99% and every other assumption held fixed, it becomes **+0.010858 GJ**; at 95%, +0.195003 GJ. The sign change is a numerical sensitivity to modeled work participation, not a measurement that a real floor provided exactly 99% or that the structure actually continued or arrested. A negative expression in this simplified balance indicates the assigned full work exceeds available energy under the model; it does not resolve the detailed stopping process.

Five floors at the stated area, 101.6 mm depth, 2,400 kg/m³ and 4,900 J/kg calculate to **23.018130 GJ**, not the paper's 32.01 GJ. Producing 32.01 GJ with the other stated values would require approximately 141.289 mm of equivalent concrete. That is an arithmetic inconsistency under these inputs; the authors' original worksheet or an unreported input would be needed to establish its cause. The correction alone does not establish a real collapse trajectory or decide the paper's global energy argument.

## Inference and missing verification

The paper assigns the 3.5 factor to laboratory work and derives a pulverization energy using a particle-size scenario. The precise experiment-to-building transfer, initiation geometry, actual engaged column/slab mass, energy already dissipated in impacts, and timing of fragmentation remain critical assumptions. This pass did not independently inspect the underlying column and concrete studies, drawings, the claimed deck-equivalent geometry, or every sensitivity row in the recovered report; those items remain open rather than being adopted on the basis of the summary.

The strongest alternative to a uniformly descending, full-floor-impact path is a progressively evolving structural failure with portions of the building and debris engaging differently. That alternative requires its own validated mechanics; the sensitivity calculation neither proves NIST's model nor identifies explosives or a participant. The original worksheet, matching geometrical/experimental sources and explicit model of which components engage before a proposed stopping point would help discriminate the predictions.

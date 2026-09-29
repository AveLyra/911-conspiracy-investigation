# Exploratory facade-repetition check

Declared after both first-pass descriptions were frozen and root viewed the
endpoint enlargements, before calculating any intensity profile. The
separate observer's coarse 14–16-cycle reading is now known; this is not a
blind measurement or independent validation of that count. Purpose: test
whether visible facade repetition provides positive support for a roughly
fifteen-cycle span despite the endpoint occlusion/phase ambiguity. No g,
acceleration, absolute floor numbering or steel/thermal inference.

Use the three pinned run01 native grayscale frames only. Select columns
**402 through 411** and rows **202 through 384**, half-open box
`[402,202,412,385)`, to the left of the lower query/foreground boundary and
excluding both query neighborhoods. Compute the per-row arithmetic mean,
retaining all 183 values per image. This is a source-pixel statistic, not
invented imagery or a restoration of an occluded endpoint.

For each full profile and the fixed two parts `[202,293)` and `[293,385)`,
calculate normalized Pearson lag correlations at **every integer lag 8–18**,
both for the unmodified mean profile and after an ordinary least-squares
linear trend removal. Normalize each lag's two overlapping vectors separately.
Keep every result; a vector norm at or below `1e-10` intensity units is
undefined, not zero correlation. Record all maxima tied within `1e-12`.
These are six method/windows per image, not independent evidence sources.

Before using historical images, test pure cosine profiles of periods 12, 13
and 14 over 183 samples under both methods. Each must maximize at its true
integer lag within the declared range. Test constant raw/detrended profiles
and a detrended affine ramp as undefined. These finite algorithm controls do
not validate facade-to-storey identification or infer subpixel periodicity.

Interpretation: a consistent peak near 13 pixels can support a characteristic
facade repetition scale, compatible with a roughly 194.5-pixel tape spanning
about fifteen cycles. It does not uniquely count corresponding endpoint
phases, authenticate one cycle as a physical storey, validate the assigned
length, constrain a historical exposure clock or prove a projective error
bound. Unequal peaks or window sensitivity remain findings; do not change
the strip, lags or method to obtain a desired count. Candidate 14/15/16
equal-storey assignments may be compared dimensionally as explicit scenarios,
not confidence intervals or accepted calibration corrections.

Save the code, inputs/pins, profiles, all correlations, controls and return
status. Obtain independent numerical/interpretive review before reporting
the diagnostic as a result. No new decoder execution or source mutation.

# Exploratory saved-keyframe check

Declared after the initial fits and figure were inspected, before reading
the source project's keyFrames values. The very smooth early trajectories
raise an ordinary provenance question: do all saved coordinates represent
marked frames, or can the application retain interpolated positions? Small
residuals do not answer that question or prove independent measurements.

The tagged PointMass source, already preserved publicly, defines keyFrames
as manually **or automatically** marked steps (comments at715–716 and1189).
Its interpolation code at1178–1315 fills positions between key frames. The
loader at2937–2951 falls back to treating all existing positions as keyframes
when the saved key array is missing/empty. Thus neither all-key membership
nor absent metadata authenticates independent manual annotation.

Authorize this bounded derivative of the same hash-pinned public project:
export only each PointMass sibling ordinal's numeric keyFrames index array,
or a literal missing/empty status. Check integer values in0..441, monotonic
array indices, uniqueness, membership against the already exported71 point
indices, and preserve all results. No arbitrary names, paths, comments,
booleans or other fields; no raw XML display or application execution.
If shape is unexpected, stop with a generic reason without source text.
Keep the original protocol, point export and fits unchanged. Record this
as post-result source follow-up, not prospective confirmation of independence.

An all-key result would rebut only a claim that this saved state explicitly
labels some of these marks as interpolation gaps. It would not establish
manual marking, original exposures, historical absence of interpolation,
annotation uncertainty or causal accuracy. A smaller key set would motivate
testing the effect of the actual interpolation structure, not deleting the
points or assuming deliberate alteration.

## Observed format failure and prospective adaptation

The first check exited1 with `unexpected_integer_array_shape` before any
keyframe values were exported. Original checker SHA-256:
`52caaf25b5e00e9c46b155ba60df5fd546c27d1a0ec3dbd1c8492fe41caca02b`.
A separate shape-only inspection then found one string child in each array,
whose complete text matches a braced, comma-separated integer-list grammar;
no values or arbitrary child names were displayed. This is a serialization
layout difference, not missing data or a scientific contradiction.

Before extracting those numeric values, extend the parser to convert only
that fully validated braced-integer-list form into the original synthetic
indexed-int element structure, then apply the same range/uniqueness checks.
No original array is changed. The prior checker is reconstructible by
removing only the added `children` normalization block and restoring
`for pos,entry in enumerate(arr):`; the original file hash above is the check.
The original rejection is retained as a failed attempt, not counted as pass.

# Separate saved-point/native-frame observations

2026-09-24. Research-only descriptive review by a prior-informed AI observer.
This is not a human, blinded, holdout, structural-expert or physical-kinematics
review. The observer owns only this file. The protocol controls this reading;
the source images and saved coordinates remain unchanged.

## Scope, exposure and interpretation rules

I read the full main AGENTS, WORKFLOW, START-HERE and investigation charter,
the unit PROTOCOL and method-review, the prior source-semantics and complete
project-export reviews, and the earlier paper/frame feature definitions.
Prior work exposed the general footage, paper labels and the distinction
between an upper step corner and its lower foot. The current source-guided
labels, points and key flags are expressly visible; this is not independent
point selection. I did not read root's observations or synthesis before saving
this complete record and did not exchange any substantive classifications.

Protocol SHA-256: `50785dd33e8543a0de76932be36e011693998cffa11a734040b3fb4f1ec3680d`.
Method-review SHA-256: `cfe0b94704f419f18a8efb7992d03c38841242f3a369d21d877fba39f0e43fc6`.
Saved project SHA-256: `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8`.
These three current pins were checked with `shasum -a 256` before viewing.

Root explicitly cleared the representation gates before any historical panel
was viewed here, reporting passing independent representation checks and
repeat products. I did not rerun those pixel/decoder/synthetic tests. The
viewing and file-integrity checks below are my actual coverage, not an
independent certification of the producer or historical raster pipeline.

Every classification is conditional on H0: the saved image x/y displayed on
the current native 720 x 480 raster, x right and y down. No world-axis rotation,
sample-aspect correction, scale change, time shift, fitted transform, new
coordinate or distance cutoff was introduced. Native sample aspect and the
historical engine/display uncertainty are not resolved by these observations.

`building` means the displayed neighborhood is dominated by the target
building's visible outline or face; it does not exclude a bright edge halo
or smoke immediately beside it. `mixed_or_unresolved` means overlapping haze,
building or background prevents a confident host assignment at the displayed
neighborhood. The feature label concerns the visible local appearance, not
whether the original analyst selected a material particle.

`candidate` is a visually compatible neighborhood of the corresponding lower
step foot; it is not a verified coordinate, structural joint or continuing
material identity. `different_feature` is used where the displayed location
looks like a roof-edge segment while a distinguishable lower step turn lies
beside it. No calibrated residual follows. `unresolved` is retained where the
step no longer has a separately readable foot or obscuration prevents the
join. Thus `roof_edge_only` plus `unresolved` does not assert destruction or
prove that a historical point changed. A geometric roof-edge construction
may be legitimate even when no persistent corner can be identified.

## Complete observations

Each row was read in its full native scene and its plain/marked crop pair.
Key membership is literal saved metadata, not a finding of human marking.
PM05 has 35 nonkeys and eight keys; PM08 has 40 keys. Missing counterparts
are not observations: PM08 is absent at 150–204 and PM05 at 408–444.
The 83 present rows below retain all selected entries.

| Frame | Target | Key | Host | Feature | Lower-step relation | Reason / competing reading |
|---|---|---|---|---|---|---|
| 150 | PM05 | false | building | corner_or_junction | candidate | The lower horizontal outline meets the raised left step side near the displayed gap; smoke softens the turn, so projected overlap remains an alternative to a material joint. |
| 156 | PM05 | false | building | corner_or_junction | candidate | The same left lower turn is readable beside the gap with a dark face below; the blurred rim does not isolate one precise physical point. |
| 162 | PM05 | false | building | corner_or_junction | candidate | Both the lower ledge and upright side of the left step remain distinguishable in the neighborhood; haze can broaden their apparent intersection. |
| 168 | PM05 | false | building | corner_or_junction | candidate | A rounded left step foot is visible in the unmarked crop near the indicated location; blur and smoke permit a less sharply localized edge interpretation. |
| 174 | PM05 | false | building | corner_or_junction | candidate | The gap remains near the lower end of the left upright step boundary; the bright smoke above is not itself evidence of the joint's material identity. |
| 180 | PM05 | false | building | corner_or_junction | candidate | The ledge-to-upright change is recognizable near the indicated neighborhood; its softness leaves an edge-band rather than exact-corner reading possible. |
| 186 | PM05 | false | building | corner_or_junction | candidate | The left upright and lower roof outline form a visible turn near the gap; smoke along the upright prevents precise localization. |
| 192 | PM05 | false | building | corner_or_junction | candidate | A lower left step turn remains recognizable with building face beneath it; a projected silhouette join, not a demonstrated connection, is all that is visible. |
| 198 | PM05 | false | building | corner_or_junction | candidate | The displayed neighborhood includes the left step foot and adjoining ledge; the point could represent a selected location in that blurred band rather than an independently resolved corner. |
| 204 | PM05 | false | building | corner_or_junction | candidate | The left step's lower outline turn remains readable near the gap; surrounding haze leaves the exact boundary uncertain. |
| 210 | PM05 | false | building | corner_or_junction | candidate | The gap is near the lower-left turn of the raised outline, with the darker wall below; a broadened smoke/roof boundary remains a competing reading. |
| 210 | PM08 | true | building | corner_or_junction | candidate | The right descending step side meets the lower roof rim near the gap; the bright halo makes the visible junction a neighborhood, not a subpixel mark. |
| 216 | PM05 | false | building | corner_or_junction | candidate | The left lower ledge and short upright still meet close to the displayed neighborhood; smoke obscures the crispness of the turn. |
| 216 | PM08 | true | building | corner_or_junction | candidate | The right lower step foot is distinct beside the displayed gap, with a horizontal rim continuing right; the rim is a projected outline rather than a verified joint. |
| 222 | PM05 | false | building | corner_or_junction | candidate | A visible left step turn lies near the indicated region; blur permits a nearby roof-edge interpretation without resolving a unique material point. |
| 222 | PM08 | true | building | corner_or_junction | candidate | The short right upright ends at the lower roof near the gap; its bright border does not establish where within the band the physical edge lies. |
| 228 | PM05 | false | building | corner_or_junction | candidate | The left step foot is still identifiable near the displayed neighborhood, although rounded; smoke and finite resolution limit the precise correspondence. |
| 228 | PM08 | true | building | corner_or_junction | candidate | The right step-to-ledge turn remains plainly recognizable near the gap; the reading does not distinguish a structural corner from projected silhouette overlap. |
| 234 | PM05 | false | building | corner_or_junction | candidate | The local roof contour still turns upward beside the displayed point neighborhood; the softened transition could be treated as an edge band. |
| 234 | PM08 | true | building | corner_or_junction | candidate | The lower right foot remains distinct with dark face below and bright background above; exact placement within the halo is unresolved. |
| 240 | PM05 | false | building | corner_or_junction | candidate | A lower-left foot is visible near the gap even though the marker is not a proof of its exact location; blur permits a neighboring ledge interpretation. |
| 240 | PM08 | true | building | corner_or_junction | candidate | The right descending step meets the lower rim in the displayed neighborhood; this supports a visual candidate, not persistence of one physical member. |
| 246 | PM05 | false | building | corner_or_junction | candidate | The left step foot is near the gap and is visible in the plain crop; the low-contrast rounded boundary prevents a unique point claim. |
| 246 | PM08 | true | building | corner_or_junction | candidate | The short upright and lower right roof rim still meet near the gap; edge blur remains an alternative explanation for small apparent placement differences. |
| 252 | PM05 | false | building | roof_edge_only | different_feature | The displayed gap looks located on the lower ledge to the left of the separately visible step turn; a broad blurred foot neighborhood is the strongest competing reading, not a measured mismatch. |
| 252 | PM08 | true | building | corner_or_junction | candidate | The right step foot remains readable near the displayed gap; the bright outline does not establish subpixel or material correspondence. |
| 258 | PM05 | false | building | roof_edge_only | different_feature | The plain and marked views place the neighborhood on the lower roof segment before the visible upright to its right; an imprecisely defined broad junction region remains possible. |
| 258 | PM08 | true | building | corner_or_junction | candidate | The right upright terminates near the gap on the lower rim; a silhouette construction remains possible in place of a physical corner measurement. |
| 264 | PM05 | false | building | roof_edge_only | different_feature | A lower horizontal rim is the local feature at the gap, while the distinct left step turn lies to its right; blur limits how sharply those neighborhoods can be separated. |
| 264 | PM08 | true | building | corner_or_junction | candidate | The right lower turn remains recognizable near the gap with the lower ledge extending right; halo width prevents exact localization. |
| 270 | PM05 | false | building | roof_edge_only | different_feature | The indicated neighborhood is on or just below the lower ledge, left of the readable upright step; a broad corner-region selection could explain the apparent offset. |
| 270 | PM08 | true | building | corner_or_junction | candidate | The right lower step foot is still readable beside the gap; the point may select a blurred edge intersection rather than one resolved object. |
| 276 | PM05 | false | building | roof_edge_only | different_feature | The gap sits along the lower ledge before the visible step rise, not on a locally distinct turn; haze makes the foot's extent debatable. |
| 276 | PM08 | true | building | corner_or_junction | candidate | A right lower turn remains visually compatible with the indicated neighborhood; bright background and edge blur do not specify its physical attachment. |
| 282 | PM05 | false | building | roof_edge_only | different_feature | The local outline at the gap is a ledge segment while the step rise is visible to the right; interpreting both as one broad junction neighborhood is a competing reading. |
| 282 | PM08 | true | building | corner_or_junction | candidate | The right upright still joins the lower rim near the gap; the candidate remains an appearance-level correspondence only. |
| 288 | PM05 | false | building | roof_edge_only | different_feature | The gap is slightly into the face beside the lower rim, with the readable step turn to its right; no pixel residual or cutoff is inferred from that qualitative distinction. |
| 288 | PM08 | true | building | corner_or_junction | candidate | The right lower step foot remains discernible near the gap despite a softened contour; a selected roof-rim band remains an alternative to a unique corner. |
| 294 | PM05 | false | building | roof_edge_only | different_feature | A horizontal ledge dominates the point neighborhood while a short rise remains visible to its right; blur can merge these into a broad foot region. |
| 294 | PM08 | true | building | corner_or_junction | candidate | The right step is shorter in appearance but its lower turn is still readable near the gap; no height or movement is measured here. |
| 300 | PM05 | false | building | roof_edge_only | different_feature | The location remains on the lower ledge/upper-face band before the visible step rise; a loose junction-neighborhood interpretation is possible but not a distinct corner at the gap. |
| 300 | PM08 | true | building | corner_or_junction | candidate | The descending right side and lower rim still form a recognizable turn near the gap; blur makes its exact endpoint uncertain. |
| 306 | PM05 | false | building | roof_edge_only | different_feature | The displayed neighborhood is along the lower rim to the left of the remaining short rise; a blurred broad foot rather than a straight segment is a competing reading. |
| 306 | PM08 | true | building | corner_or_junction | candidate | A low right step with a rounded lower turn remains near the gap; it could be treated as a roof-outline construction rather than a persistent material corner. |
| 312 | PM05 | false | building | roof_edge_only | different_feature | The gap lies in the ledge/upper-face band, left of a still discernible shallow step turn; the reduction in contrast makes that separation less secure. |
| 312 | PM08 | true | building | corner_or_junction | candidate | The right lower turn is still visible, although shallow and rounded; exact localization and continued material identity remain unestablished. |
| 318 | PM05 | false | building | roof_edge_only | different_feature | A nearly level lower edge lies at the gap with a small discernible rise to its right; blur or an overly broad definition of the foot could erase this descriptive distinction. |
| 318 | PM08 | true | building | corner_or_junction | candidate | A shallow right step turn remains near the indicated neighborhood; a smoothed roof-rim construction is a serious competing interpretation. |
| 324 | PM05 | false | building | roof_edge_only | unresolved | The local roof boundary is nearly level and smoke-softened; no separate left upright/foot can be confidently assigned at the gap, though a hidden or flattened continuation is possible. |
| 324 | PM08 | true | building | corner_or_junction | candidate | A small sloping right step still has a readable lower turn near the gap; its softness leaves straight-rim selection as an alternative. |
| 330 | PM05 | false | building | roof_edge_only | unresolved | The gap is beside a nearly straight roof/face boundary and no distinct left step foot is resolved; it may preserve a geometric location without a visible corner. |
| 330 | PM08 | true | building | roof_edge_only | different_feature | The gap appears on the lower straight rim to the right of the small remaining step turn; a broad rounded foot neighborhood is possible, but no exact-corner match is established. |
| 336 | PM05 | false | building | roof_edge_only | unresolved | The local boundary reads as a level rim under smoke with no resolved lower left foot; a continuing hidden material point cannot be confirmed or excluded. |
| 336 | PM08 | true | building | roof_edge_only | different_feature | The indicated neighborhood is on the lower rim while a small raised-to-lower transition remains to its left; edge blur permits a broader-junction reading. |
| 342 | PM05 | false | building | roof_edge_only | unresolved | Only a nearly straight roof boundary is identifiable near the gap; smoke could conceal residual shape, so loss of a distinct corner is not proof of physical destruction. |
| 342 | PM08 | true | building | roof_edge_only | unresolved | The gap follows the straight lower rim beside a low rounded shape farther left; that shape no longer supplies a securely separate foot for a correspondence decision. |
| 348 | PM05 | false | building | roof_edge_only | unresolved | A faint level roof/face band remains near the gap without a distinguishable lower step turn; a constructed edge point could still be usable for a different observable. |
| 348 | PM08 | true | building | roof_edge_only | unresolved | A straight rim is readable at the point and a small irregularity remains leftward; its relation to the original step foot cannot be established from the blurred appearance. |
| 354 | PM05 | false | building | roof_edge_only | unresolved | The indicated neighborhood is near a low-contrast straight rim beneath smoke, not a resolved junction; a continuing but obscured location remains possible. |
| 354 | PM08 | true | building | roof_edge_only | unresolved | The local feature is the straight roof rim, with only a blurred bump to its left; the original foot is not independently identifiable. |
| 360 | PM05 | true | building | roof_edge_only | unresolved | The first saved-key row shown here lies near a faint level roof band beneath smoke; key status does not restore a visible corner or establish a fresh human mark. |
| 360 | PM08 | true | building | roof_edge_only | unresolved | A clear straight rim passes near the gap, while no step foot is resolved there; a geometric roof-edge construction remains a plausible selection method. |
| 366 | PM05 | true | building | roof_edge_only | unresolved | A weak roof/upper-face boundary can still be followed near the gap but no junction is resolved; haze could conceal the former feature or obscure a different selected construction. |
| 366 | PM08 | true | building | roof_edge_only | unresolved | The gap is near the straight upper rim of the visible face; the residual darker shape to the left is not a readable lower step foot. |
| 372 | PM05 | true | mixed_or_unresolved | uncertain | unresolved | Haze overlaps the upper face and the boundary near the gap is weak; a faint roof/face band is a competing reading, but no local junction can be identified confidently. |
| 372 | PM08 | true | building | roof_edge_only | unresolved | The point neighborhood remains the straight roof rim with smoke beside it; this does not reveal whether a material point or constructed edge position was followed. |
| 378 | PM05 | true | mixed_or_unresolved | uncertain | unresolved | Smoke and faint face texture overlap around the displayed neighborhood; a buried roof boundary is possible, but a lower step foot is not visually recovered. |
| 378 | PM08 | true | building | roof_edge_only | unresolved | A straight rim is visible at the gap while the nearby outline has no distinct step turn; an edge construction is compatible without establishing original-foot continuity. |
| 384 | PM05 | true | mixed_or_unresolved | uncertain | unresolved | The gap lies in a haze/face mixture without a clean local outline; faint vertical texture may belong to the face but does not identify the former foot. |
| 384 | PM08 | true | building | roof_edge_only | unresolved | The local straight roof edge is readable against a brighter background; the clear outer corner farther right is a different feature and is not substituted. |
| 390 | PM05 | true | mixed_or_unresolved | none_resolved | unresolved | The immediate gap neighborhood is diffuse dark haze/face tone with no distinct edge or junction; a concealed building feature remains possible rather than disproved. |
| 390 | PM08 | true | building | roof_edge_only | unresolved | The gap remains on or beside a straight roof-rim band; no lower step foot is separately visible, although the building outline is still identifiable. |
| 396 | PM05 | true | mixed_or_unresolved | uncertain | unresolved | Faint vertical texture and haze cross the neighborhood; the brighter foreground detail lower in the crop is not the saved target, and neither it nor the texture identifies a foot. |
| 396 | PM08 | true | building | roof_edge_only | unresolved | The straight upper rim remains readable at the point neighborhood; obscuration to the left prevents an independent relation to the former step. |
| 402 | PM05 | true | mixed_or_unresolved | uncertain | unresolved | Smoke/face texture dominates near the gap, with separate foreground detail below-left; a hidden roof-edge continuation is possible but no unique local feature is resolved. |
| 402 | PM08 | true | building | roof_edge_only | unresolved | A straight roof rim is still the local visible feature; its correspondence to the earlier lower foot remains unresolved rather than disproved. |
| 408 | PM08 | true | building | roof_edge_only | unresolved | The gap is near the readable straight top rim with smoke spreading over its left part; no independently identifiable step foot remains at this location. |
| 414 | PM08 | true | building | roof_edge_only | unresolved | The point neighborhood still contains a straight upper rim between face and bright haze; this supports an edge appearance but not one material-point identity. |
| 420 | PM08 | true | building | roof_edge_only | unresolved | A straight rim remains visible at the gap while smoke softens the adjacent left boundary; the former step-foot relation cannot be recovered. |
| 426 | PM08 | true | building | roof_edge_only | unresolved | The rim is still distinguishable near the indicated location, though smoke reduces contrast; a projected edge construction is compatible with the appearance. |
| 432 | PM08 | true | building | roof_edge_only | unresolved | The local roof-rim band is visible beside a diagonal smoke boundary; the diagonal may obscure part of the edge and does not provide a new structural junction. |
| 438 | PM08 | true | mixed_or_unresolved | uncertain | unresolved | Smoke overlaps the gap and the roof edge is clearer to its right than at the point; a continuous rim through the haze is possible but cannot be assigned confidently locally. |
| 444 | PM08 | true | mixed_or_unresolved | uncertain | unresolved | The displayed neighborhood is a haze/upper-face transition with a clearer rim to the right; neither the exact host boundary nor an old step foot is resolved at the gap. |

## Actual viewing manifest

I used `view_image` with `detail="original"` and displayed the returned images
at original detail. All 50 complete 1128 x 648 panels were actually viewed,
in ascending order, in ten batches of five: 150–174, 180–204, 210–234,
240–264, 270–294, 300–324, 330–354, 360–384, 390–414 and 420–444,
each at increment six. Every panel's full unmarked native 720 x 480 scene
and each present plain/marked pair were inspected. No viewing call failed,
no panel was skipped, and the tool reported no resizing. No extra image,
crop, enhancement or historical fit was generated by this observer.

The following SHA-256 manifest was obtained from the actual viewed files
with `shasum -a 256` after viewing. Paths are relative to this unit and all
are under `run01/panels/`. Hash integrity is not historical authentication.

| Viewed panel | SHA-256 |
|---|---|
| frame-0150.png | ba562fe0c6552ae413b27e41ec307d21e086ec41b650ccd322e8c8a3899d9489 |
| frame-0156.png | ba7aa227c4731da1cab030f47ccf801b85e4774fa7ebe6d0421a86a2ac822cec |
| frame-0162.png | 7caf39940cd0f2d58d2f7abe095e6ee8ef495540cd108c5b0fc15d6bd28a83cc |
| frame-0168.png | 152d1d028a09a4509b834cf2bb16a857d32f918e4193495a8fccfde8dc231473 |
| frame-0174.png | 92b1cafbb407aa8e1bf9a2b76a4008f4f56366cae3f216f99609b6e1d5a951b1 |
| frame-0180.png | 82160f797e852ae96cfa6a50ba008d8341c364d25628a302d53c2bb7360650e5 |
| frame-0186.png | d1d0e25c22247bab940894962cda8ef4d648174894bb3b5bfe5362738347de8f |
| frame-0192.png | b479ce53d0c89e5f74b3fbf2158bf8dfa51e457011abb9bb73789bd710beb512 |
| frame-0198.png | 4682adb0728fbb0ee4eaca5f06e228d2a5ae214d2170b86307bc56c82601f7b1 |
| frame-0204.png | 0a03cacf982907ee2c418251496d6173779bdcce6a21a555be9bdb0dec8a2134 |
| frame-0210.png | 0834af920e25ae6bdcdb352506e675cfdaac880e6217845bd16b8fe199d227db |
| frame-0216.png | e3c67a8fa56594ea31822a53fd4b40749b36645228bc0435fb5b621aa57a566c |
| frame-0222.png | 710d2879028517c736c2c6a656b20cab7dc6b836f3f7fa4ee88da4a188b277ef |
| frame-0228.png | 500197ee6ce09a92b8c115a5c9978924a077bf43bc83834d05ddb2f2eb2e08e3 |
| frame-0234.png | e1e9059144b3bcb08a8e5da9384089c2db38de88c5ea17821eaa8fe75ae67046 |
| frame-0240.png | 5c42c0fdc664c75beaa0a9e7e5692a8402fa914526d6b2b26ee6c1d13979e565 |
| frame-0246.png | 32b5caa31e0b77d495256c1b4f84a015c047bcb6467c8cd1bf2d3acb0dfa6b77 |
| frame-0252.png | f56d904a3c3b8aaa8a09c0bcc54dc2ecb6009c667634f1ac57b65a61457e7541 |
| frame-0258.png | a76df173106cfd8ff7d22cf0889ef9158fc5f481b6c250829e785aaf37136ebb |
| frame-0264.png | b53a717206a54adc191b0d07b1a16932ed32b59e03430f458442fb658cc268b5 |
| frame-0270.png | bbf471ca63a73c5143796b4fafd4fe931035f62ed617d58a7ed218594dd63da6 |
| frame-0276.png | 4b226a45d01fb425396d32f5a95c5a6ebc0dfa7c7db23c3f6ad8ceaf0c204b58 |
| frame-0282.png | c4c9c5cbb9280cc0fc65bef7c293fc5d056aa165306c237d448971fa7fc4f2f8 |
| frame-0288.png | 762a5ac5e078adac5ce89bff45469c0444b1a20a8165f91da92bcb7dfa19a624 |
| frame-0294.png | e588da0901b8bdb9f79b911fc831f203c38ad2b3810c2a3b908817f848f6911b |
| frame-0300.png | bc130942f5c59b049cc1b973432838f49270a96c885aa67dd267029e39a1b2dd |
| frame-0306.png | f15ec771280fe48928516f8c20fd92864e42753235e66d3e893595937c9b04e2 |
| frame-0312.png | 10cce848a25cf3df2fbf37aa3b8e341a03c7360eeda7b6d79c1c4e8357c3de07 |
| frame-0318.png | 04b91b0c4a54ccdf1543d0e79758bce3a989715517d518d5cdfc2e6ef1650a8c |
| frame-0324.png | 8d5747ab581447dfb854ea25d4f81039d5b6101d9344a91691173e797e7d6feb |
| frame-0330.png | e314ae4150f669ade396646b45c098e64a5d0828fc9239e37ab9eca2096936ce |
| frame-0336.png | a14d8e54cb4d43bac00788ce2fe45cd13bdda99613add2f818e99a7d22006e28 |
| frame-0342.png | 51186adb2e721226ee5ceca21aade34e2664585b5e946567ab62938b05e6172c |
| frame-0348.png | a98dc08a3ee8bdce8c8408d542af4732f264a12f9e44b0fcdf1b8d91ebfff1ca |
| frame-0354.png | 838cbdf897f2a329b139160e715d02fe249f4d54880ef635795f3d305f02900a |
| frame-0360.png | f3bb097aca80a7b06f5181f9c757347e6997cc224b4f317194caf9fc8deb07a0 |
| frame-0366.png | 0c54c60d6093a58bd221ac7d838602f5499a9cf3c2a0aedc31bcf77f3e2dc3be |
| frame-0372.png | 0d12c427a40615bfd2d2a6ddbd28b87778ab51039fedd9ab4607fb0a576a69df |
| frame-0378.png | d89007f18425295a290989fb0e6e033cf60d9dc67be7a7fe53f875dce8247b55 |
| frame-0384.png | 5943794949abdfb9ab591c1671444eeb81ce0b83cc90fe79b44f2011f50e883b |
| frame-0390.png | 61f909c2f09c7cd34dd0f4de47e825449e8cdd2430b8968c0531cf1bacee9bbd |
| frame-0396.png | 96e5d68d4efa5e61dba2589e25a154ca911b6ec1b432a3464c64593157f198a3 |
| frame-0402.png | 0cf5d37daed2931c86202027bdc85bba0c35d7893ef6e63219290278e969c53d |
| frame-0408.png | ae32a1dcf959ef31588d6c9ddf146cf90f93008f90a3a5565cd2b606e151a9f1 |
| frame-0414.png | bc4e76dcc816ca9a1c1d1374e1411d57300ef392b83d8989455e2bfa39a51164 |
| frame-0420.png | 5c94b20d5f4e163d66fe44a7c70ea7592ae12b7e98baa106d5ddc58b79656bef |
| frame-0426.png | 4b5c06eafc5468f624b2739dbd8aa65379a7da499775164a2e0b6006acf11c0e |
| frame-0432.png | dfc9d4049c1e8d5431e5c17f156ffea54c07f8875940143b413fcc56b3f33122 |
| frame-0438.png | 7351703ffb808f58da4fea03b3768ad4d644a52779cacfeaf447f2292ce4529c |
| frame-0444.png | d1c6681bbd770864b19106086b0fe1335e3b1d4566c17cdea6bc0b82d3ceda0d |

## Verification and ceilings

Only this research note is written. The evidence-falsification and
source-of-truth skills shaped the competing readings and prevent the visual
labels from becoming physical, historical-pipeline, causal or legal findings.
Repo-orchestrator intake confirmed the dedicated research worktree and
pre-existing changes; those changes were not altered. Some preparation text
reads were truncated and were completed in smaller calls before viewing.

An actual read-only `python3 -B` validation parsed this note's tables and
passed: exactly 83 unique ordered PM/frame rows matching the declared 43/40
selections, the saved-key pattern, all three categorical vocabularies,
nonempty reasons, exactly 50 ordered manifest entries, every manifest hash
against its viewed PNG, all 50 PNG-header dimensions of 1128 x 648, and
terminal-newline/trailing-whitespace checks. It made no pixel or motion
measurement. The post-save file hash is supplied to root outside this file
to avoid a self-referential hash.

The actual viewing record supports coverage, not accuracy. Matching source
labels, coordinates or two AI interpretations would not independently
authenticate a publication version, historical engine, material track,
physical scale or collapse mechanism. An obscured or different-looking local
feature does not establish fabrication, invalid acceleration, destruction of
all supports or any cause. Qualified human review and the charter's separate
measurement/calibration gates remain unmet by this observer note.

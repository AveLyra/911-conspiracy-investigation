# Independent OEM report comparison

October 4, 2026. Separate prior-informed AI reading of exactly NCSTAR 1-1J
physical pages 59-61 / printed pages 25-27, before reading root's new notes or
synthesis. This is not a blind, historical, human, or engineering-expert
validation. Prior municipal SK-58 and E5 readings are known; their frozen
records and original sources were not changed or re-viewed.

## Scope, controls, and actual checks

The protocol fixes this manual documentary comparison, not a simulation,
measurement, or whole-report review. Fully read protocol (`db9cff`, exit 0),
main AGENTS, WORKFLOW, START-HERE, and charter. A combined control-file output
was truncated (`60053c`); WORKFLOW/START-HERE and charter were read completely
in `b08393` and `14228c`, both exit 0. AGENTS appeared completely in the first
output. Fully read evidence-falsification, source-of-truth, and PDF skills plus
the two applicable audit references (`413192`, `944691`, `f9ec7e`, `1a6d14`).
These controls require the source-account/installed-condition distinction,
preservation of contrary details, and no promotion into legal or accepted facts.

Protocol SHA-256: `d90c185f2d39ef527677e2302cf586d57de76b276540dafa37226c177fb9e905`.

Ran `shasum -a 256` on the source PDF, three original PNGs, and protocol
(`2564f7`, exit 0). All input pins match the admitted values:

| Input | SHA-256 |
|---|---|
| `equipment-source-followup/sources/ncstar-1-1j-attempt02.pdf` | `7b1fe2a7a94a67c54fdaabe27e3309b439551512cff97e5026e0b62bb51bf623` |
| `root-derivatives/p59.png` | `880960ccfc33489160eeeda73d9900d77977b3ff58c459042826c1db13b25250` |
| `root-derivatives/p60.png` | `8abc1a82fa2ecf87b58bfa34ff531fb8fd19af1fedfe72e5b78492cf6641c798` |
| `root-derivatives/p61.png` | `c0577e09891e1cc0b6607dbc35093f34142c3208f045f6fdacc09f405892594f` |

Read the saved `root-reproduction/receipt.json` (`4f8f1e`, exit 0): it records
the same source pin and matching selected original/reproduction image hashes,
1700x2200 dimensions, and zero rendering-warning bytes. This historical receipt
is not a fresh rerender. Independently compared each selected original PNG
against its reproduction with `cmp`: `110a99`, `1e7815`, `3df3b1`, all exit 0.
No fresh PDF extraction or rendering was performed. This confirms local byte
identity, not historical authenticity or independent source-origin corroboration.

Displayed each complete original PNG once at original detail using `view_image`
and the original-detail display, in order 59, 60, 61. All three pages were
readable and fully read, including headings, qualifications, and references.
**Three first views; zero repeats, crops, OCR, transformations, measurements,
or other primary-page views.** No network, original-record acquisition, model
execution, or main-repository edit. Only this working reading is newly written.

## Complete page ledger

### Physical 59 / printed 25: Chapter 6 and section 6.1

The chapter identifies the Mayor's OEM modification as 1999, describes the
specification for at least one week of self-supported operations, and places
modifications on the first and seventh floors. It names PANYNJ submittal
**W98-7134** as the design submission for approval. The listed team includes
Swanke Hayden Connell, Cosentini, Cantor Seinuk, and Ambassador. This is the
report's attribution, not an approval record reproduced on this page.

The layout account distinguishes:

- A fill pump added at the existing pump suction in the Fuel Oil Pump Room,
  whose alarm drum provided a catch basin/leak detection.
- A **1-1/4-inch fuel-oil-supply (FOS) pipe** from that fill pump to a new
  storage tank in the existing Elevator Room, between center and east passenger
  elevator banks on the first floor.
- Another **1-1/4-inch FOS pipe** back from the tank to an additional transfer
  pump in the Fuel Oil Pump Room. Despite its opposite route, the source calls
  this FOS: it must not silently become the generator fuel-return pipe.
- A transfer-pump discharge connection to an existing FOS riser. The report
  explicitly says **which existing riser is unclear**, although drawings
  reference an earlier approval under submittal **94-7176**.
- A seventh-floor connection from the existing riser to a day tank at the
  north wall of the Generator Room on the building's south side; 1-1/4-inch
  supply pipes to three generators and a distinct **1-1/2-inch fuel-oil-return
  pipe** from generators to the day tank.

The page references Figs. 6-1, 6-2, and 6-3, but these figures are not present
in the selected three pages and were not viewed. It describes an isolated
mezzanine supporting the storage tank and fire separation from the Elevator
Room. This supplies report-level floor/component locations, not independently
verified coordinates for either municipal drawing.

### Physical 60 / printed 26: section 6.2 component details

The page distinguishes the specified fill-pump pair (2 hp, 2,000 gph, LO-207)
from the transfer-pump pair (3/4 hp, 700 gph, LO-203). It describes interlocks,
relief valves, level-controlled lead/lag operation, and alarms. These are
reported component specifications and control functions, not a new operational
test or a demonstrated September 11 pump history.

Its enclosure sentence says that fuel-oil pipes outside the Fuel Oil Pump Room
and Fuel Oil Tank Room **"were 10 gauge conduit and in a 2 h fire rated
enclosure."** That wording is awkward; do not silently turn it into a precise
conduit diameter or equate protective enclosure gauge with the carrying-pipe
diameter. It reports protection, swing-check and anti-siphon valves. It does
not identify SK-58 or E5 or reproduce a fire-rating test.

Other reported components are a **50-gallon alarm drum**, **275-gallon OEM day
tank with a 550-gallon rupture basin**, shutdown/solenoid/alarm functions, and
three seventh-floor generators specified at 500 kW each. The separate OEM
storage tank is **6,000 gallons**; the report locates its support in the
Elevator Room and describes four-hour-rated enclosure construction with an
access hatch, leakage-retaining walls/curbs, and alarms.

The report recounts an original seventh-floor storage-tank location request
and FDNY denial, citing submittal documentation. Its sentence prints the
exception as small **"(>275 gal)"** day tanks; this apparent awkwardness is
retained, not silently corrected or adopted as a verified code threshold.
The page itself supplies neither the underlying denial nor an as-built or
inspection record. None of these capacities identifies the earlier separate
11,000-gallon tank mentioned in another municipal record.

### Physical 61 / printed 27: sections 6.3 and 6.4

The fire-protection account distinguishes the seventh-floor OEM Generator Room
(smoke detectors, no suppression system, existing sprinklers removed) from the
new first-floor Fuel Oil Tank Room (Inergen, removal of sprinkler branches/
heads, retention of standpipe/hose piping) and the Elevator Room below
(sprinkler coverage added). These are separate spaces and modifications; the
page does not say the entire building lacked sprinklers.

The Elevator Room account gives a high-hazard design maximum of **100 square
feet per head** and says heads were spaced at **168 square feet per head**.
That is an apparent within-account design/reported-spacing tension, not a
resolved finding about installed spacing, a code violation, or its causal
effect. It needs the underlying plan/inspection and applicable design basis.

The page also describes explosion-proof tank-room electrical devices, a
four-hour tank-room enclosure with eight-inch CMU walls and top sealing, and
a separate two-hour Generator Room wall assembly, curb and 1-1/2-hour door.
These wall dimensions/ratings must not be confused with six- or eight-inch
conduit or with demonstrated event-day protection.

The reference list supplies specific documentary leads, not reproduced originals:

| Referenced SHCA item | Reported date/identifiers |
|---|---|
| OEM specification manual | April 6, 1998 |
| Architectural drawing | A-1-1, August 23, 1999 |
| Electrical drawings | E1.01, E1.07, E3.01, E6.01, September 25, 1998 |
| Fire-protection drawings | FP1.01, FP2.07, September 25, 1998 |
| Mechanical drawings | M1.01, M1.07, M4.01, March 29, 1999 |

No SK-58, FSK-58, OEM E5, or explicit diameter-revision crosswalk appears in
these references. This bounded absence is not proof the full report or archive
has no such reference. The listed electrical drawing identifiers are not a
license to conflate OEM E5 with another tenant's E-5.

## Comparison and discriminating result

**Positive but bounded join:** the report associates OEM, the same broad
professional/project context, first-floor tank/pump connections, and protective
10-gauge/two-hour enclosure language. The municipal E5's tank-room-to-pump
schematic and SK-58's concrete-filled enclosure fit this general design context.
The first-floor tank/pump route is a plausible candidate for E5's pictured run;
it is not established as its exact segment. The explicitly unclear existing
riser is an adverse limitation on pretending the report supplies complete routing.

**Not a diameter conflict with the fuel-carrying pipes:** the report's
1-1/4-inch supply and 1-1/2-inch generator-return pipes are different component
categories from the municipal six- and eight-inch protective fuel conduit.
They do not resolve or independently contradict the E5/SK-58 conduit difference.
The selected pages supply no protective-conduit diameter or explicit revision
relationship, so **E5 6 inches versus SK-58 8 inches remains unresolved**.

**No discovered bare-line premise:** these pages expressly report enclosure
protection; they do not support attributing a generic unprotected OEM-line
assumption to this part of NIST's account. Conversely, the agreement between
the municipal protection design and the report is not independent proof of
installed protection, integrity after damage, actual fire resistance, or safe
capacity. The report may depend on the same design record family; do not count
it as an independent inspection or performance test.

**Outcome:** an improved component/location hypothesis and exact documentary
leads, but no explicit SK-58/E5 same-segment or revision join, no identified
same-component contradiction with the report, and no new collapse-cause ranking.
The internal sprinkler-spacing tension deserves retention, not conversion into
an explanation of collapse without the missing record and physical chain.

## Claim strength and next discriminator

- **A, direct source content:** the selected report says the things above,
  subject to the quoted awkward wording; local page identity is checked.
- **B for broad project/design consistency, C for candidate segment:** matching
  context and functions make a related OEM design interpretation reasonable;
  exact component/location/revision identity remains assumption-dependent.
- **D for historical installation, performance or causal conclusion:** neither
  report narration nor these municipal design pages independently establishes it.
- **Best next discriminator:** the cited M1.01/M1.07/M4.01 set and W98-7134
  reviewed submittal could explicitly associate the route, containing conduit,
  and approved revision with SK-58/E5. A matching route and revision annotation
  would strengthen the proposed join; a different component, floor, or diameter
  would weaken it. Approval/as-built/inspection evidence is a separate necessary
  test of any claim about actual installation. The first step may be a bounded
  held-input inventory check, not automatic new acquisition.

No new source acquisition, primary-page expansion, engineering calculation,
legal/matrix promotion, user acceptance, transmission, or engine activation
is authorized or claimed by this reading. The overall goal remains incomplete.

# New-subject Responsibility presence investigation 001

## Status

Findings only. This report changes no active Book clause, Witness Grammar
coordinate, runtime path, or test.

The investigation begins at `efcfa977`. The removed unary and ordered-pair
Candidate rules remain removed.

## Question

The immediate question was:

```text
what warrants exact Candidate rule G?
```

That question presupposes the more basic crossing:

```text
one newly addressable exact subject
-> one exact Responsibility concerning that subject
```

Active law gives the anatomy after that crossing:

```text
current Standing
-> exact Responsibility
   -> responsible boundary
   -> subject
   -> exact Act
   -> Authority / Scope / Locality
   -> limits / required relations
-> Act occurrence
-> Yield
-> result
```

It does not give one universal occurrence that creates every Responsibility.
This report asks how the current live roads make each exact Responsibility
present and whether prior Standing alone can recover why it was owed.

## Direct finding

`G` is not presently demonstrated as a separate constitutional subject or
produced object.

On the mature byte-Measurement and recorded-pair Compare roads, the exact rule
is a coordinate of the exact Responsibility record:

```text
byte Measurement Responsibility
└── measurement_rule

recorded-pair Compare Responsibility
└── comparison_rule
```

The runtime record precedes the governed Act and gives later occurrences one
durable exact reference to those Responsibility coordinates. Earlier recovery
established that this record is not evidence of a separate Assignment Act or
Assignment Assertion.

The lower vacancy is prospective:

```text
prior Standing carries exact subject S
!=
one exact Responsibility concerning S is now present
```

All four inspected roads require a choice of exact Responsibility and Act
before their Responsibility can be recorded or used. Some roads recover every
local subject after that choice. None lets prior Standing alone determine and
record the next Responsibility without that choice.

## 1. Active law distinguishes anatomy from presence

### 1.1 General law

`01.Standing.A` says Standing for one exact subject requires one exact
Responsibility. `02.Acts.A` says one exact Responsibility bounds one exact Act
and carries its required coordinates.

These clauses establish:

```text
exact Responsibility required before the governed Act
exact subject carried by that Responsibility
exact lineage retained through Act and result
```

They do not establish:

```text
every addressable subject receives a Responsibility
one universal Responsibility-production Act
one scan of every active clause after every Yield
one automatic next Act
```

### 1.2 Clause-local conditions

Some active clauses say more than general anatomy:

```text
01.Source.D.2
each exact source-byte position reference
-> subject of an exact declared Measurement Responsibility

04.Compare.A
current Standing carrying one earlier and one later exact result
-> one exact Compare Responsibility

04.Compare.C
current Standing carrying one exact Candidate result
-> one exact Compare Responsibility whose subject is that Candidate
```

These are local conditions. They do not form a Book-wide Responsibility
registry or dispatcher. A matching local condition can warrant one exact
Responsibility without a universally named owner.

`01.Source.E.1` is also conditional. It says what one exact Candidate
Responsibility owes after its exact rule, subject boundary, and required
subjects are carried. It does not say which source result requires that
Responsibility or which rule applies.

## 2. What current runtime "assignment" records do

`responsibility_assignment_decomposition_investigation_001.md` already
recovered that the current `*_responsibility_assignment_recorded` events do
not carry an assigner, assignee, Assignment Act, Assignment occurrence,
Authority to assign, or a changed Responsibility relation as result.

Their exact work is:

```text
serialize one exact Responsibility's coordinates
preserve a durable reference
precede its exact Act
let Act and result retain that exact lineage
```

Thus this report uses “Responsibility record” for the mechanical finding while
retaining exact runtime names where needed.

```text
Responsibility record exists
!=
the record explains why the Responsibility was owed
```

Replay can validate a recorded Responsibility and refuse changed coordinates.
Replay does not make the first unrecorded Responsibility present.

## 3. Live-road audit

### 3.1 Declared exact-byte Measurement (`01.Source.D`)

The exact Responsibility record carries:

```text
subject material:
    exact material-acquisition occurrence references
    exact declared source Localities
    completeness boundary

rule:
    BYTE_MEASUREMENT_RULE

other coordinates:
    01.Source.D
    exact Measurement Act and occurrence identities
    exact result boundary
    prior Standing boundary
    Scope / limits / Unknown
```

Immediately before the record, current Locality Standing and exact acquired
material already exist. The public recorder receives the source Localities
from its caller. It validates current Standing, freezes the append boundary,
recovers the exact source material through that boundary, and records the
Responsibility.

What chooses this Responsibility:

```text
caller invokes record_byte_measurement_responsibility_assignment
caller supplies source Localities
runtime constant supplies BYTE_MEASUREMENT_RULE
```

The acquired material warrants the exact subject and bounds. It does not
warrant choosing exact-byte Measurement rather than another Act. No earlier
occurrence carries that choice.

The declared-Measurement runner improves local completeness after the exact
Measurement Responsibility has been chosen. For each installed declaration it
discovers every qualifying subject at one frozen boundary before recording.
That is evidence-driven subject discovery inside one already chosen
Responsibility, not evidence-driven Responsibility discovery.

Disposition:

```text
exact Responsibility record                          yes
exact subject recovered from prior Standing          yes
exact rule carried by Responsibility                  yes
why this Responsibility is owed from prior Standing   no
Responsibility choice                                 runtime declaration + call
```

### 3.2 Source-position recurrence road (`01.Source.D`, `04.Compare`)

The live source-position road is stronger about source-selected subjects.
After an entry function is invoked, it derives:

```text
exact source-position pairs
Compare results carrying every coordinate of each exact bounded result
all recurrent complete findings
all corresponding carried-material findings
all exact reusable material results warranted by those findings
```

For each derived subject, `_record_yielded_result()` records one exact
Responsibility immediately before its Act and Yield. The subject is not chosen
by a caller one coordinate at a time.

The exact Responsibility and Act are nevertheless selected by control flow:

```text
_record_compare
-> COMPARE_RESPONSIBILITY

_record_source_position_result
-> SOURCE_POSITION_MEASUREMENT_RESPONSIBILITY

_record_recurrence_measurement
-> RECURRENCE_MEASUREMENT_RESPONSIBILITY

record_corresponding_coordinate_material_measurements
-> COORDINATE_MEASUREMENT_RESPONSIBILITY

record_recurrent_result_material_measurements
-> RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESPONSIBILITY
```

The caller selects the entry function. The function's constants select the
exact Responsibility. Source evidence then exhausts that Responsibility's
local subjects.

There is also one exact current defect. `_record_responsibility()` carries
`exact_act`, subject, Book clause, Authority, Scope, limits, conflicts, and
Unknown, but carries no exact rule coordinate. Active `04.Compare` requires a
Compare rule, and active `01.Source.D` says its result preserves its exact
rule. The runtime behavior is fixed in Python while the durable Responsibility
record cannot replay which exact rule governed it.

Disposition:

```text
exact Responsibility record                          yes
exact subjects derived from source results            yes
local subject exhaustion after Responsibility choice  yes
exact rule carried by Responsibility                  no
why this Responsibility is owed from prior Standing   no
Responsibility choice                                 invoked function + constants
```

### 3.3 Recorded pair-finding Compare (`04.Compare.A`)

The exact Responsibility record carries:

```text
subject coordinates:
    exact earlier Measurement result
    exact later Measurement result
    exact source references and added occurrence

rule:
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RULE

other coordinates:
    exact input relation
    prior Standing boundary
    exact Compare Act / occurrence / result identities
    Scope / limits / Unknown
```

Active `04.Compare.A` gives an actual local condition: current Standing carrying
one earlier and one later exact pair-position Measurement result carries this
Compare Responsibility. The runtime validates that condition for the exact two
result identities supplied to
`record_recorded_pair_measurement_comparison_responsibility_assignment()`.

The runtime does not discover every qualifying earlier/later pair. The caller
chooses the pair and calls the exact recorder. Replay can prove that the chosen
pair satisfies the clause and that the recorded rule and lineage are exact. It
cannot recover which unrecorded pair should be considered next.

Disposition:

```text
exact clause-local condition                          yes
exact Responsibility record                           yes
exact rule carried by Responsibility                  yes
chosen pair validated from prior Standing             yes
all owed pairs recovered from prior Standing           no
instantiation                                          caller selected
```

### 3.4 Emission (`07.Emission.A`)

Active law says one emission Responsibility carries one exact source-material
result, destination boundary within the invocation Locality, emission Act,
Authority, Scope, Locality, limits, conflicts, known loss, and Unknown.

The live console road does this:

```text
exact Representation
-> caller invokes representation Candidate recorder
-> Candidate Responsibility record preallocates:
     destination boundary and boundary rule
     future emission Act identity and occurrence identity
     future emission result identity
-> Admission
-> Applicability
-> emission attempt / Act Evidence / Yield / result
```

There is no standalone recorded occurrence whose `responsibility` is
`REPRESENTATION_EXACT_MATERIAL_EMISSION_RESPONSIBILITY`. The Candidate
Responsibility record carries the future emission coordinates, while the later
emission events carry the emission Responsibility string. No exact emission
Responsibility reference joins those later events to a preceding exact
emission Responsibility record.

The destination boundary is external input to the console road. The console's
control flow chooses to take Candidate, Admission, Applicability, and emission
steps for each Representation.

Disposition:

```text
exact source material and destination boundary        yes
Admission / Applicability / emission occurrences       yes
standalone exact emission Responsibility record        no
why emission is owed recovered from prior Standing     no
Responsibility choice                                   console control flow
```

## 4. What `declared Measurement Responsibility` means now

Active `01.Source.D` uses `declared` but names no declaration Act, occurrence,
testimony source, or declaration result.

The compact Witness Grammar says only:

```text
subject:        declared_Measurement
Responsibility: declared_Measurement
exact Act:      Measurement
requires:       exact material result, Yield, Locality relation
```

The operational declaration is
`DECLARED_MEASUREMENT_RESPONSIBILITIES`, a Python tuple containing exactly two
`DeclaredMeasurementResponsibility` values. Each value stores:

```text
Book clause identity
Measurement identity
Responsibility-record event type
result event type
subject-discovery callable
recording callable
```

The tuple was introduced on the current road by `60c92279` and later refined
to preserve a common responsible boundary by `56ec4551`. Current tests call
these “curated runtime coordinates.” Earlier investigation already refused the
inference that Python callable identity is a Seed-native assignment condition.

Therefore `declared` currently means, mechanically:

```text
named by active Book law
+ installed in a developer-curated runtime tuple
```

It does not currently mean:

```text
declared by an earlier Seed occurrence
derived from arbitrary prior Standing
supplied as attributed source testimony
complete enumeration of every active Responsibility
```

This tuple is the current bootstrap for those two Measurement roads. It is not
evidence of a general bootstrap physiology.

## 5. Historical false searches

History repeatedly searched above the local crossing:

```text
universal owner
dispatcher / ALL_RESPONSIBILITIES registry
reusable competency
producer of a rule object
```

The relevant recoveries refuse each compression:

* `compare_standing_continuation_recovery_001.md` recovered that one exact
  Compare owner can be local to its instantiated comparison and need not have
  a universal name. It separately refused treating reusable competency as that
  owner.
* `responsibility_assignments_at_one_boundary_investigation_001.md` found no
  Book-wide traversal Responsibility and no need for a collective subject
  containing all Responsibilities.
* `declared_responsibility_force_surface_investigation_001.md` found that an
  `ALL_RESPONSIBILITIES` registry would preserve developer enumeration rather
  than recover the first subject-specific Responsibility.
* `responsibility_assignment_decomposition_investigation_001.md` found no
  irreducible universal Assignment physiology. Exact Responsibility
  coordinates and a durable reference perform the current work.

The smaller shape is clause-local:

```text
one exact prior subject and boundary
+ one exact active clause-local condition
-> one exact occurrence-local Responsibility
```

No permanent office, dispatcher, competency, or separately produced rule
object is required by that shape.

## 6. Apply the finding to exact reusable result W

At `efcfa977`, W has:

```text
exact reusable material
exact source-derived subject coordinates
exact supporting result references
exact Measurement Responsibility ownership
exact Act occurrence and Yield
current Standing addressability
```

No active evidence now causes W to become the subject of a Candidate
Responsibility.

Specifically:

```text
W exists                                      yes
W is exact and addressable                    yes
W is carried by current Standing              yes
one exact Candidate rule applying to W        no
one exact clause-local condition requiring
Candidate work for W                          no
one exact Candidate Responsibility record     no
```

`01.Source.E` begins with one Candidate already available for preservation.
It does not turn material into a Candidate. `01.Source.E.1` begins with one
exact Candidate Responsibility already carrying its exact rule and required
subjects. It does not make that Responsibility present.

Standing relation anatomy also cannot fill the gap. Its three coordinates say
what one relation Assertion carries. They do not warrant a Candidate
Responsibility over W or enumerate assignments of W's material into those
coordinates.

Therefore this is the current exact stop:

```text
current Standing carries W at exact boundary B

missing:
one exact clause-local condition carrying
    subject W
    exact Candidate Act
    exact rule G
    exact Authority / Scope / Locality / limits / Unknown

-> no exact Candidate Responsibility concerning W
```

This does not prove that Seed needs a new generic Responsibility-assignment
mechanism. It proves that no current clause-local condition warrants this one
Responsibility.

## 7. Is this the recurring bootstrap hole?

Across the inspected roads, the same lower boundary is demonstrated:

```text
new exact result becomes addressable
!=
one later Responsibility concerning that result becomes present
```

The repository has several partial answers:

```text
declared Measurements
    developer-curated Responsibility tuple
    + evidence-derived complete local subjects

source-position recurrence
    invoked Responsibility
    + evidence-derived complete local subjects

04.Compare.A
    active clause-local condition
    + caller-selected exact pair

emission
    console-selected continuation
    + no standalone emission Responsibility record
```

This explains why Candidate, Compare continuation, and source-Assertion
acquisition repeatedly stop before Applicability: each needs an exact later
Responsibility, and none follows from result existence.

It does not establish one universal missing mechanism shared by all three.
Their exact clause-local conditions differ, and source-Assertion acquisition
also lacks evidence that material carries an Assertion. The common refusal is
narrower:

```text
availability is not Responsibility
```

## 8. Required answers

### 1. How are clean live Responsibilities instantiated?

By exact Responsibility-local recorders. The recorder validates current
Standing and its exact subjects, writes one durable Responsibility-coordinate
record where that road has one, and the later Act cites it. Which recorder runs
is selected by a runtime tuple, a direct caller, an invoked source-position
function, or console control flow.

### 2. Which instantiations are recoverable from prior Standing?

Subject coordinates are recoverable on every inspected mature road. The
declared-Measurement and source-position roads exhaust local subjects after
their exact Responsibility is selected. `04.Compare.A` validates one supplied
exact pair. No inspected road lets prior Standing alone select the exact
Responsibility and record its first occurrence.

### 3. What does `declared Measurement Responsibility` mean?

Active Book declaration plus installation in the two-entry developer-curated
runtime tuple. It is not a declaration occurrence and not a complete traversal
of active Responsibilities.

### 4. Is G separate?

No separate constitutional G object is recovered. Mature roads carry their
exact rule directly as a Responsibility coordinate. The source-position road
currently omits that required coordinate from its Responsibility record.

### 5. What warrants Responsibility presence for a new subject?

Where recovered, one exact active clause-local condition does. Runtime still
requires a Responsibility-local call to instantiate the record. General
anatomy and subject addressability do not warrant presence.

### 6. Is there a generic evidence-driven result-to-Responsibility path?

No. There are local subject-discovery roads after an exact Responsibility is
chosen. There is no generic automatic result uptake, and W has no current
Candidate-specific local condition.

### 7. Is this beneath the repeated missing stairs?

Yes as a demonstrated common boundary: all later work requires an exact
Responsibility before Applicability, while result availability establishes no
such Responsibility. No as a proposed universal repair: each exact road still
needs its own warranted local condition.

### 8. Smallest next question

No build is warranted yet.

The smallest next question is:

```text
For exact W at exact boundary B,
what exact source evidence or active clause-local condition,
if any,
warrants one exact Candidate Responsibility carrying W and exact rule G?
```

Until that condition is recovered:

```text
do not record a Candidate Responsibility for W
do not add W to the declared-Measurement tuple
do not scan every result after Yield
do not create a dispatcher or universal owner
do not treat G as a separately produced object
```

Separately, the source-position Responsibility record's missing exact rule and
emission's missing standalone exact Responsibility record are concrete active
runtime discrepancies. They do not fill W's missing local condition and should
not be used to smuggle Candidate continuation into those repairs.

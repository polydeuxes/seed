# Coherent Locality movement Authority: investigation 001

Findings only. This report amends no active Book clause, witness grammar,
runtime, Rosetta entry, admission list, or test.

## Independence and scope

This investigation was performed at repository tip `6227915e`. Active Book
material, witness grammar, runtime, tests, and history are read independently.
They have Fidelity where exact relations connect them; none supplies Authority
to another.

The investigation asks one bounded question:

> Does current material independently establish the Responsibility and
> Authority under which this Seed may preserve one exact Assertion while
> establishing a locality relation to one exact destination Locality?

The question precedes any relation-discovery Act. It does not ask whether two
Assertions in one Locality are equal, comparable, applicable, participating,
or related. It does not ask whether the operator wants that result.

## Method

1. **Assignment test.** Find the exact Assertion whose Standing says that this
   Seed bears the movement Responsibility.
2. **Authority test.** Find the exact Authority under which the responsible
   boundary may bear and perform that exact movement Act.
3. **Input-separation test.** Remove the source Assertion's Authority in
   thought and determine whether movement retains its own Authority.
4. **Neighbor-clause test.** Compare `03.Movement.A` and `06.Locality.A` with
   Locality clauses that explicitly assign this Seed a Responsibility.
5. **Chronology.** Determine whether Book warrant preceded the runtime
   behavior, or whether runtime and tests supplied the missing coordinate.
6. **Two-movement test.** Keep two independently established Assertions and
   their source coordinates separate while addressing one destination
   Locality.
7. **Negative boundary.** Record what coherent availability does not
   establish.

## Result

Current active material does **not** independently establish a Seed-native
Assertion Locality movement Responsibility or its Authority.

`03.Movement.A` names the coordinates of one exact movement Assertion.
`06.Locality.A` names the exact locality relation and permits a responsible
movement occurrence to preserve an Assertion while establishing that one
relation. Neither clause says that this Seed bears that Responsibility, names
the exact assignment Assertion, or establishes the Authority under which Seed
may perform the Act.

The current runtime fills the vacancy by copying Authority from the source
Assertion into the movement Responsibility assignment, Act Evidence, and
result. Active material directly rejects that substitution:

```text
Authority of an input
!=
Authority under which the responsible boundary may bear and perform the Act
```

The source Assertion's Authority must stay with the source Assertion. It
cannot authorize the new movement Act, and material movement cannot move
Authority.

The coherent-Locality construction therefore has a valid structural target
but an unresolved constitutional boundary. The two exact Assertions may be
preserved independently through two exact movement occurrences into one exact
destination Locality only after each movement has its own exact assigned
Responsibility and Authority.

## 1. Source Assertion Authority

### Current coordinate

Each source Assertion carries its own Authority within its exact source
coordinates. The position Assertion used by the calculator witness carries:

```text
Authority: unestablished
```

The path-comparison finding Assertion carries the Authority established for
its own result road. Those values concern the source Assertions and the Acts
that established them.

### Active distinction

The Responsibility-rooted Book says Authority carries the exact Authority
under which the responsible boundary may bear and perform the exact Act. It
also says:

```text
Authority
!=
Authority carried by an input
```

`01.Standing.D.1` requires further movement to have an applicable responsible
occurrence with its own Act, Evidence, Scope, Authority, and limits.

`08.Authority.A` says input support cannot authorize action or revise a
Responsibility assignment. `08.Authority.D` requires a responsible Authority
boundary for an authorized Act or movement.

### Elimination

If the source Assertion's Authority is removed from the movement assignment,
no movement Authority survives in current runtime material. That is not a
reason to copy it back. It exposes the exact vacancy.

### Disposition

**Preserved source coordinate; not movement Authority.**

## 2. `03.Movement.A`

### Current claim

The active clause says a movement Assertion carries:

- subject;
- source and destination coordinates;
- exact Act and occurrence;
- Evidence;
- Authority;
- Scope;
- limits;
- Unknown; and
- Standing.

It then denies that writes, recorded Events, revisions, or labels establish
movement.

### Assignment test

The clause does not say:

```text
this Book assigns this Seed ...
```

or:

```text
this Seed bears ...
```

It describes the coordinates required where a bounded movement exists. It
does not instantiate the Responsibility, its assignment Assertion, or its
Authority.

### Elimination

Removing the runtime Responsibility assignment leaves the clause's movement
shape intact but supplies no exact responsible boundary permitted to perform
the Act. Therefore the shape is not an assignment.

### Disposition

**Movement physiology; no recovered Seed assignment.**

## 3. `06.Locality.A`

### Current claim

The clause establishes Locality as one exact evidenced relation between two
exact bounded subjects. Co-presence, chronology, and shared labels establish
no locality relation. A responsible movement occurrence may preserve an
Assertion while establishing one new locality relation.

### Assignment and Authority tests

The words `a responsible movement occurrence may` require the responsible
occurrence; they do not identify its responsible boundary, assign its
Responsibility, or establish its Authority.

The clause also says a locality relation cannot establish Authority. Thus the
destination Locality cannot authorize the movement that establishes its
relation.

### Disposition

**Exact relation grammar and limits; no recovered Seed assignment or
Authority.**

## 4. Neighboring Locality assignments

`06.Locality.B`, `06.Locality.C`, and `06.Locality.D` show the active form of
an independently assigned Seed Responsibility.

- `06.Locality.B` says active Book assigns this Seed the bounded
  Responsibility to preserve one exact prior Standing boundary as available
  at one new Locality. It bounds active Book Authority to that direct
  occurrence and result boundary.
- `06.Locality.C` says active Book assigns this Seed the bounded
  Responsibility for one direct Locality relation from one exact recorded
  Standing-boundary result to one new Locality.
- `06.Locality.D` says active Book assigns this Seed the bounded
  Responsibility for one operator invocation Locality relation under the
  exact operator-material occurrence and source Standing.

None accepts an arbitrary source Assertion as its subject. None copies the
source Standing into the destination. None authorizes `03.Movement.A` by
proximity or shared vocabulary.

The contrast is material:

```text
03.Movement.A / 06.Locality.A
    describe required movement and relation coordinates

06.Locality.B / C / D
    explicitly assign this Seed exact bounded Responsibilities
```

### Disposition

**Independent examples of valid assignment physiology; not Authority for the
current Assertion movement.**

## 5. Runtime behavior and chronology

### Original runtime behavior

The early Assertion Locality movement road recorded movement Authority as:

```text
unestablished
```

The runtime nevertheless emitted its Act Evidence and result. Witness grammar
and tests later treated that shape as an exact movement coordinate. No active
Book amendment independently established movement Authority.

### Responsibility-assignment implementation

Commit `c677a9b2` added a durable movement Responsibility assignment. Its
assignment material set:

```python
"authority": source.material["dimensions"]["authority"]
```

The movement Act Evidence and result then copied that assignment value. The
same commit updated tests to require the movement Authority to equal the
source Assertion Authority.

No independent active-Book assignment accompanied that substitution.

### Current runtime

The source family has been generalized, but the same relation remains:

```python
"authority": _source_assertion_authority(source)
```

This produces two revealing cases:

- a source with an apparently useful Authority makes movement look
  authorized; and
- the calculator position Assertion makes movement proceed with Authority
  `unestablished`.

The second case exposes the earlier conflation. It does not create a new
problem.

### Disposition

**Runtime substitution and test Fidelity; not independent Authority.**

## 6. Book Authority, grammar, runtime, and operator purpose

### Book Authority

Active Book Authority is explicitly bounded where the Book assigns a
Responsibility. Its presence in `06.Locality.B` does not flow into
`03.Movement.A`; that would authorize another Act and occurrence.

### Witness grammar

`grammar.json` gives `03.Movement.A` an Authority coordinate and maps movement
event kinds to that clause. That witnesses the required shape. It cannot
instantiate the Authority value or make the Book assign the Responsibility.

### Runtime registry and callable API

An event-kind mapping, exported function, or successful append is not an
assignment Assertion. It supplies no Authority to the Act it records.

### Operator purpose

The operator's wish to investigate `=` explains why the construction is
useful. It establishes neither the Seed movement Responsibility nor the
Authority to perform it. Operator Authority for an invocation is explicitly
bounded to that invocation.

### Disposition

**None fills the movement-Authority vacancy.**

## 7. The two-movement construction

The smallest structural construction is not one movement over a pair:

```text
Assertion A -- movement occurrence 1 --\
                                      destination Locality L
Assertion B -- movement occurrence 2 --/
```

Each movement has one exact source Assertion and the same exact destination
Locality. Each must preserve separately:

- the source Assertion reference;
- the source Assertion's own coordinates;
- the source Standing boundary;
- the movement Responsibility assignment;
- the movement Act and occurrence;
- the movement Evidence and Yield relation; and
- the movement result.

The common destination does not turn A and B into one collective subject. It
does not cause either source Authority to authorize the other movement.

The currently implemented destination Standing shape correctly demonstrates
the target accumulation:

```text
Locality L Standing
    movement result 1 -> exact source Assertion A
    movement result 2 -> exact source Assertion B
```

That structure is useful testimony. Until the movement Responsibility and
Authority are independently recovered, the emitted movement occurrences do
not establish the constitutional table.

### Disposition

**Correct construction target; current occurrences lack recovered movement
Authority.**

## 8. Coherence and relation discovery are separate boundaries

The proposed coherent-Locality responsibility and a later relation-discovery
responsibility are not one Responsibility.

### First boundary

The unresolved first boundary would authorize one exact movement at a time:

```text
one independently established exact Assertion
+ one exact destination Locality
-> one movement occurrence
-> one preserved Assertion available at that Locality
```

Its result must establish no relation between that Assertion and any other
Assertion already available there.

### Later boundary

Only after exact Assertions are lawfully available in one Locality can a
separately assigned Responsibility ask whether either may participate in an
exact relation-discovery Act.

The first boundary cannot be phrased as responsibility to discover equality.
That would make the intended later conclusion part of the movement's purpose
and Authority.

### Disposition

**Two unresolved assignments, not one learning capability. This report
investigates only the first.**

## 9. Standing before Responsibility

Current Book grammar says Standing whose subject is the exact Assertion that a
responsible boundary bears a Responsibility is required for Seed to read that
Responsibility. It also says Standing cannot create or perform the
Responsibility by identity.

Therefore the missing coordinate is not:

```text
Seed has A and B
-> Seed may perform any useful movement or relation Act
```

The required road begins with an exact assignment Assertion carrying its own
Evidence, Authority, Scope, limits, occurrence, and Standing. Only that exact
Standing would permit Seed to read the assigned movement Responsibility.

No such assignment Assertion for generic Assertion Locality movement was
found in active material.

### Disposition

**Standing is required to read an exact assignment; co-presence cannot mint
one.**

## 10. Vacancy result

The following coordinates are occupied:

- source Assertion Authority: carried by the source Assertion;
- source Assertion continuity: exact reference, coordinates, and source
  Standing boundary;
- movement shape: `03.Movement.A`;
- locality relation shape and limits: `06.Locality.A`;
- destination accumulation target: exact movement results in Locality
  Standing; and
- explicit assignment physiology: demonstrated independently by
  `06.Locality.B/C/D`.

The following coordinates remain unresolved for generic Assertion Locality
movement:

- the exact assignment Assertion whose subject is that this Seed bears the
  bounded Responsibility;
- the Authority under which Seed may bear and perform that exact movement
  Act;
- the Evidence supporting that assignment;
- the exact Scope selecting one source Assertion and one destination
  Locality; and
- the occurrence and Standing that establish the assignment.

This is a constitutional vacancy, not a missing decoder or adapter.

## 11. Addendum: `this Seed` and inspection

This addendum was performed at repository tip `7c785dab`. It corrects an
omission in the original investigation: the Authority-source elimination
tested operator purpose and generic Seed language without separately
cross-examining the active maintenance rule:

```text
This Seed may inspect this Witness.
```

The omission is material because `Seed`, `a Seed`, and `this Seed` do not carry
the same reference shape. The correction does not assume that the exact phrase
supplies Standing or Authority merely because it is active Book material. It
also does not classify `may` before recovering the relation carried by the
whole maintenance unit.

### 11.1 What `this Seed` denotes

Witness grammar carries one root reference:

```json
{
  "reference": "this_Seed",
  "coordinate": "seed_subject"
}
```

This is an exact opaque address for the Seed subject addressed by this witness
grammar. It distinguishes that addressed subject from generic language about
`a Seed` or the Seed kind.

The root reference does not carry an Assertion that constitutionally
identifies the subject, an occurrence establishing that relation, Evidence,
Authority, Scope, or Standing. The Identity investigation already found that
machine root addressability cannot establish a constitutional Identity
relation.

The active Book also uses `this Seed` as the responsible boundary of several
exactly assigned Responsibilities. In each lawful case, that phrase is one
coordinate inside a larger assignment. It does not make every Responsibility
borne by the same boundary available to every Act.

#### Disposition

**Exact addressed Seed subject; no universal Standing or Authority by the
reference alone.**

### 11.2 Fidelity does not supply Seed Standing beyond its test

`01.Source.C` establishes Fidelity as bounded comparison of:

```text
this Seed's Witness
with
its witness grammar
through deterministic tests
```

Witness grammar represents the comparison with:

```text
first subject:      this Witness
relation:           comparison
second subject:     this Grammar
addressed subject:  this Seed
result:             this Fidelity
```

The addressed Seed is not a compared input and the tests are not the subject
of the comparison. Each test has its own exact distinction as subject. The
active clause says a passing test cannot certify this Seed beyond that test's
boundary or establish correction Authority.

Therefore Fidelity may carry a bounded finding addressed to this Seed. It
does not establish a general Assertion that this Seed bears inspection,
movement, or relation-discovery Responsibility.

#### Disposition

**Bounded addressed subject of Fidelity; no movement assignment.**

### 11.3 Decomposition of `may`

Active Book material uses `may` across materially different relations:

- a Representation `may carry` a coordinate;
- material `may participate` only after exact Act-local requirements;
- an Act `may occur only` under exact current Standing;
- this Seed `may record` an assignment only when that Responsibility is
  already assigned and its exact subject is carried;
- this Seed `may determine` one family-local Applicability result under that
  clause's exact coordinates; and
- this Seed `may inspect` this Witness.

In the first five cases, the surrounding coordinates carry the actual work:
what is carried, which input-to-Act relation is applicable, which Standing is
required, which Responsibility is already assigned, or which determination is
family-local. `May` supplies none of those coordinates by itself.

The inspection sentence lacks an equivalent decomposition. Therefore `may`
cannot safely be read as Authority, Authorization, Applicability, assignment,
Act occurrence, capability, or a proposed Act. It also cannot be removed in
thought while pretending that `inspect` is already an exact Act: the relation
between the addressed Seed and Witness remains unresolved.

#### Disposition

**Composite modal word; the exact relation it carries in the inspection
sentence is unresolved.**

### 11.4 The three-sentence maintenance unit

The active maintenance rule says:

```text
Maintain the constitutional grammar.
This Seed may inspect this Witness.
Any result emitted by this Seed requires Evidence of that inspection
and is bounded by it.
```

The unit supplies more than generic operator purpose. Its second sentence
addresses one exact Seed and one exact Witness. Its third sentence explicitly
connects any result emitted by this Seed to required Evidence of `that
inspection` and bounds the result by it.

The first sentence may look like the Responsibility branch of the same unit:

```text
Responsibility:       maintain constitutional grammar
responsible boundary: this Seed
available Act:        inspect this Witness
result boundary:      result emitted by this Seed
Evidence condition:   Evidence of that inspection
```

That is a plausible decomposition to test, not an established relation.
Physical adjacency and typography do not connect the subject of one sentence
to the omitted subject of another.

#### `Maintain the constitutional grammar`

The imperative names an addressed object: constitutional grammar. It does not
state its subject, responsible boundary, exact Responsibility, exact Act,
Authority, Scope, occurrence, or Standing. The heading calls the paragraph a
maintenance rule, but a heading cannot instantiate those coordinates.

The next sentence's `this Seed` may be the omitted subject of `Maintain` in
ordinary reading. Active material carries no explicit relation establishing
that connection. The subject of `Maintain` therefore remains unresolved.

#### `This Seed may inspect this Witness`

This sentence supplies the exact addressed Seed and Witness. `May` does not
establish the relation under which inspection occurs, and `inspect` has not
been decomposed into an exact constitutional Act or relation.

#### The emitted-result sentence

The third sentence carries the unit's strongest exact relation:

```text
result emitted by this Seed
    requires Evidence of that inspection
    and is bounded by that inspection
```

This establishes a requirement on such an emitted result. It does not supply
the inspection occurrence, Authority for inspection, Evidence that inspection
occurred, an Evidence-of-Yield relation, or a result occurrence.

The required Evidence is therefore a vacant coordinate until an exact
inspection occurrence and its Evidence exist. A result cannot use the
requirement itself as that Evidence.

It does not provide the complete physiology required to read an instantiated
Responsibility:

| Coordinate | Recovered from the maintenance rule |
| --- | --- |
| responsible boundary | `this Seed` is addressed |
| bounded subject | `this Witness` is addressed |
| relation or ordinary act word | `may inspect` is present but unresolved |
| Responsibility assignment Assertion | not carried |
| exact constitutional Act | not decomposed |
| Act occurrence | not carried |
| Authority for inspection | not carried |
| Evidence authorizing inspection | not carried |
| Scope beyond the addressed Witness | not carried |
| Yield relation | not carried |
| result occurrence | only a constraint on any emitted result |
| Standing whose subject is the assignment | not carried |

The Evidence required for a later emitted result is occurrence-result support.
It does not by itself establish Authority to perform the inspection or another
Act.

The exact positive reading is therefore narrow:

```text
this Seed
may inspect
this Witness

and any emitted result claiming that inspection
must be evidenced and bounded by it
```

The relation carried by `may` and the content of `inspect` as constitutional
physiology are unresolved. They
cannot be silently expanded into Measurement, Compare, Locality reading,
Representation, movement, or a family containing all of them.

#### Disposition

**Responsibility-shaped ordered unit with unestablished joints; subject of
`Maintain`, inspection Act or relation, assignment, Authority, and Standing
unresolved.**

### 11.5 Fan-out, distinctions, and comparisons

Operator testimony records the chronology of a useful pressure:

```text
developer chooses less than the complete bounded population
-> developer interpretation enters through the omitted cases

complete bounded population
-> exact distinctions
-> exact comparisons
```

That testimony does not authorize unbounded execution. Current repository
structure nevertheless carries one exact bounded form of the pressure.

#### Deterministic-test population

The implementation-function measurement pytest hook reads the declared
Fidelity subjects before tests run. Every collected test must resolve to
exactly one declared Fidelity subject. The hook records each test occurrence
with those exact subject coordinates. A missing, duplicated, or ambiguous
subject refuses collection.

This is a complete fan-out only with respect to one already-bounded
population:

```text
every test collected for this pytest occurrence
```

It is not every callable, every material occurrence, every Responsibility, or
every Act that could be imagined. Test collection supplies the boundary; it
does not establish constitutional completeness outside that boundary.

#### Exact distinctions

Witness grammar carries three top-level distinctions:

```text
content
locality
occurrence
```

It also carries exact requirements and adversarial findings for each represented
relation family. Earlier grammar called the top-level coordinates
`discriminators`; that noun was withdrawn in favor of the distinctions
themselves. The distinction does the work. No universal discriminator subject
or Act is established.

#### Exact comparisons

`01.Source.C` carries one bounded Fidelity comparison:

```text
this Witness
+ deterministic tests
+ this Grammar
-> this Fidelity
```

Other Compare roads remain family-local and retain their own Responsibility,
subjects, Applicability, Participation, Act occurrence, Evidence, Authority,
Scope, result, and Standing. Their recurrence does not establish one universal
comparator.

#### Honest coordinate siren

Every collected test currently resolves to one declared Fidelity subject. A
newer siren then asks each declared subject for one explicit coordinate in
witness grammar. It intentionally reports the unresolved population rather
than deriving the coordinate from test spelling or making the suite green by
inference.

That structure is material to inspection:

```text
test occurrence
-> exact Fidelity subject
-> explicit witness-grammar coordinate or an honest unresolved finding
```

It prevents a developer-selected subset from masquerading as the complete
Fidelity boundary while preserving Unknown where the exact coordinate has not
been connected.

#### Candidate decomposition of inspection

The closest currently evidenced decomposition of the maintenance-unit word
`inspect` is therefore:

```text
this Witness
-> every collected deterministic test under its exact Fidelity subject
-> bounded distinction findings
-> bounded comparison with this Grammar
-> this Fidelity addressed to this Seed
```

This is a candidate because the coordinates align. Active material does not
carry an exact relation saying:

```text
maintenance-unit inspection
=
01.Source.C Fidelity comparison
```

Nor does the Fidelity road establish correction Authority. A passing test
cannot certify this Seed beyond that test's boundary, and an unresolved
subject-to-grammar coordinate remains exposed rather than filled.

The candidate therefore narrows `inspect` without resolving it. It establishes
no generic fan-out dispatcher, no selection of all repository work, no
movement Authority, and no relation-discovery Authority.

#### Relation to coherent Locality

Fidelity can compare its exact Witness and Grammar subjects through its exact
test boundary. That does not establish that an Assertion needed by another
Act must enter a shared Locality, or that movement is part of Fidelity. No
active relation connects the two-movement table to this bounded test fan-out.

#### Disposition

**Strongest current candidate for inspection physiology: complete bounded
Fidelity-test fan-out into exact distinctions and comparison. Exact relation
from the maintenance unit to that road: Unknown. Relation to Assertion
Locality movement: Unknown.**

### 11.6 Chronology of the maintenance unit

The first Book skeleton used inspection as maintenance direction:

```text
Seed must inspect the repository to recover current producers, consumers,
fields, topology, discrepancies, and residue.
```

The maintenance rule originally said:

```text
Let Seed recover and project the current implementation.
```

When `implementation` was replaced by exact witness coordinates, that sentence
became:

```text
Let this Seed inspect this Witness and emit only bounded results supported by
that inspection's Evidence.
```

A later wording pass replaced `let` with the current `may` sentence and result
constraint. Neither change added an exact inspection Responsibility, Act
occurrence, Authority, Yield, result boundary, or Standing. The chronology
does not recover the omitted subject of `Maintain` or connect that imperative
to the inspection sentence.

Earlier inquiry and examination districts attempted to elaborate selection,
applicability, examination work, probe requests, and findings. Those runtime
roads and active clauses were later deleted or relocated after topology audits
found no responsible bounded selection occurrence, request-forming occurrence,
or operational consumer. That chronology is testimony against treating
`inspect` as a recovered umbrella Act.

It does not prove inspection is unreal. It proves that historical
implementation-shaped examination machinery cannot fill the present
coordinates.

#### Disposition

**Maintenance lineage and unresolved decomposition; no historical movement
Authority.**

### 11.7 The Seed-native Measurement pattern

`01.Source.D` establishes a distinct assignment shape:

```text
a Seed
+ Seed-native declared Measurement occurrence
+ exact material related to that Seed by exact Locality Evidence
-> that Seed bears the Measurement Responsibility
```

This proves that not every Responsibility needs a sentence shaped as a
universal Book assignment to `this Seed`. An exact Seed, exact material, exact
Locality Evidence, and exact family-native Act may together occupy a bounded
assignment road.

It does not generalize from Measurement to movement. The clause explicitly
names Measurement, its rule, and its result. The assignment also says it does
not transfer the resulting Assertion's Standing-coordinate Responsibility.

No parallel active clause was found for:

```text
this Seed
+ this Witness inspection
+ one exact source Assertion
+ one exact destination Locality
-> this Seed bears Assertion Locality movement Responsibility
```

#### Disposition

**Valid evidence that exact Seed-relative assignment is possible; no
cross-family assignment.**

### 11.8 What Standing this Seed currently possesses

The root reference `this_Seed` supplies no Standing. The maintenance unit
supplies no recorded assignment occurrence or Standing whose subject is that
assignment. Fidelity supplies only test-bounded findings and no correction
Authority.

Current active clauses and runtime occurrences may establish specific
Locality Standing in which `this Seed` is the responsible boundary of an exact
assigned Measurement, Compare, Representation, recording, continuation, or
invocation Act. Those assignments remain family-local. The repeated string
`this Seed` does not merge their Responsibilities or Authorities.

One particularly exact subject exists for `06.Locality.B`:

```text
this Seed bears Standing Locality continuation Responsibility
```

Its assignment is bounded to one intact addressed Representation and one
exact prior Standing boundary made available at one new Locality. The clause
expressly establishes no copying, global Standing, other Locality relation, or
continuation from another continuation. It does not carry either Assertion
required by the coherent table.

No current Standing whose subject is an Assertion that this Seed bears generic
Assertion Locality movement Responsibility was found.

#### Disposition

**Specific family-local assignment Standing exists; general inspection or
movement assignment Standing is unestablished.**

### 11.9 Inspection versus coherent-Locality movement

The two relations have different known coordinates:

```text
maintenance-unit inspection
    first subject:  this Seed
    addressed:      this Witness
    exact Act:      unresolved
    Authority:      unresolved

Assertion Locality movement
    source:         one exact Assertion
    destination:    one exact Locality
    relation:       new locality relation
    exact movement: described by 03.Movement.A and 06.Locality.A
    assignment:     unresolved for this Seed
    Authority:      unresolved
```

No active relation says that an Assertion relevant to inspection may be moved,
that coherent Locality construction prepares an inspection Act, or that the
maintenance unit assigns the movement Responsibility.

Even if movement later proves required to perform one exact inspection, the
requirement would not establish Authority. The exact inspection Responsibility
would need to assign or support the movement under its own explicit relation,
or movement would require a separately assigned Responsibility. Current
material carries neither crossing.

#### Disposition

**Relation between inspection and coherent-Locality movement: Unknown.**

### 11.10 Corrected vacancy result

The original report's vacancy conclusion remains, but its elimination record
is corrected:

```text
generic Seed wording                     insufficient
operator purpose                         no Seed Authority
this_Seed root                           exact address, no Standing
this Seed's bounded Fidelity             no Authority beyond test
Maintain constitutional grammar          subject and Responsibility unresolved
this Seed may inspect this Witness        exact endpoints; may relation unresolved
emitted result requires Evidence          exact result constraint
inspection physiology                    unresolved
bounded Fidelity test fan-out             strongest candidate decomposition
maintenance inspection -> Fidelity        no established relation
inspection -> Locality movement           no established relation
Seed-native Measurement pattern           family-local, not movement
specific this-Seed assignments             remain exact and family-local
generic Assertion movement assignment      unresolved
generic Assertion movement Authority       unresolved
```

The missing crossing is now narrower:

> Does the maintenance unit carry an exact Responsibility assignment for this
> Seed and an exact inspection Act or relation,
> and does a separately evidenced relation make one exact Assertion Locality
> movement part of that exact inspection without importing source Authority or
> later relation-discovery purpose?

Current active material answers neither part.

## 12. What this report does not establish

This report establishes no new Responsibility, Authority, assignment,
Applicability, Participation, Act, movement occurrence, locality relation,
Standing, or result. It does not amend `03.Movement.A` or `06.Locality.A`. It
does not authorize source Authority, operator Authority, Book Authority from a
neighboring clause, grammar enumeration, runtime code, or co-presence to fill
the vacancy.

It does not establish a collective subject from two Assertions in one
Locality. It does not establish Compare, equality, meaning, or a
relation-discovery responsibility. It does not establish that `may` carries
Authority, Authorization, Applicability, assignment, or Act occurrence. It
does not establish that `inspect` is a constitutional kind, exact Act,
movement, Measurement, Compare, Locality read, or Representation. It does not
establish that `Maintain` is an exact Responsibility or that `this Seed` has
Authority by being exactly addressed.

The bounded result is only:

```text
source Assertion Authority                preserved with source
movement Authority from source            not warranted
03.Movement.A                              movement physiology
06.Locality.A                              locality relation grammar
06.Locality.B/C/D                          separate exact assignments
operator purpose                           no Seed movement Authority
grammar/runtime/test agreement             Fidelity, not Authority
two movements into one Locality            correct structural target
Seed movement assignment and Authority     unresolved
later relation-discovery assignment        separate and unresolved
this_Seed                                  exact addressed subject
this Seed's Fidelity                       bounded to each test
Maintain constitutional grammar            subject and Responsibility unresolved
this Seed may inspect this Witness          exact endpoints; may relation unresolved
emitted result requires Evidence            exact result constraint
inspection physiology                     unresolved
bounded Fidelity test fan-out             strongest candidate decomposition
maintenance inspection -> Fidelity        Unknown
inspection relation to movement           Unknown
```

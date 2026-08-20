# Recurrent-pair position population investigation 001

## Question

Why does Measurement of recurrent byte-pair occurrence position construct the
complete ordered product of the first-byte and second-byte position
populations, and does active grammar require that complete population before
the later shared-position and ordered-path work?

This investigation changes no Book, witness grammar, runtime, test, limit, or
live continuation.

`Discriminator` is Rosetta orientation in this report. It does not name a
Seed Responsibility, Act, relation, result, or carried coordinate.

## Direct finding

The population is not an accidental loop. Commit `814c3806` introduced the
runtime, its specialized machine rendering, and a test that deliberately
requires reverse-order and nonadjacent findings:

```text
earlier recurrence Assertion for b"ab"
+ later material b"ba---ab"
↓
(a at 1, b at 0)
(a at 1, b at 6)
(a at 5, b at 0)
(a at 5, b at 6)
```

The test requires both relative orders and distances `1` and `5`. It proves
that the material and position coordinates must retain the ability to address
those distinctions. The current rule realizes that ability as:

```text
first byte role at every matching position
×
second byte role at every matching distinct position
```

It does not mean only a contiguous occurrence of the two-byte material.

That implementation decision performs exact work: it does not let the caller
supply direction or distance, and it preserves every possible relative
position before later comparison. The test does not independently establish
that every possible position relation must be instantiated for every later
material result.

The complete product is nevertheless not independently required by active
Book grammar or by the shared-position consumer. Active `01.Source.D` requires
an exact Measurement rule and exact subjects, findings, Scope, Locality,
limits, and boundary. It does not declare this specialized product rule. The
specialized machine entry was introduced with the runtime and later removed
when Measurement grammar was reduced to its common coordinates.

The current product is therefore exact implementation testimony, not a
currently recovered constitutional requirement.

## The phrase carrying the compression

The runtime calls its subject an `occurrence_of_recurrent_byte_pair`, while
the calculation does this:

```python
for first_position in positions[first_byte]:
    for second_position in positions[second_byte]:
        if first_position != second_position:
            record(first_position, second_position)
```

The earlier pair Measurement established recurrence of exact adjacent pair
material. The later recurrent-position reader preserves the recurrence
Assertion, its count support, source occurrences, boundary, and exact two-byte
material. The finding calculation then uses only the two byte values from
that exact material.

Thus this phrase:

```text
occurrence of recurrent byte pair
```

currently compresses:

```text
an occurrence of the first byte role
+
a distinct occurrence of the second byte role
+
their ordered position coordinates
```

The adjacency relation that made the earlier material a byte pair does not
bound the later position population. It remains recoverable through the
earlier source support, but it is not applied by the later finding rule.

## What the complete product preserves

The complete product makes these distinctions explicit:

- which byte occupies the first and second Act-local roles;
- both relative position orders;
- every exact distance between the addressed byte occurrences;
- distinct position occurrences despite equal byte material;
- an exact available count before an applied partial-result bound.

The test `test_pair_occurrence_measurement_finds_exact_positions_without_a_sign`
proves that these distinctions are addressable and that the current runtime
instantiates them. Removing the exact material or position coordinates would
change the demonstrated result. Declining to instantiate every combination
before an exact later Responsibility addresses it does not remove those
coordinates.

What remains unsupported is the stronger statement:

```text
every mathematically possible role-position combination
=
every subject required to become a durable Measurement finding
```

Current implementation asserts that statement through its loop. Active Book
does not independently establish it.

## Exact coordinates preserve addressability

No new `CoordinateSpace` subject or result is required here.

For exact recurrent pair `R`, later material `M`, and boundary `B`, the
existing coordinates already preserve:

```text
exact first-byte position population in M
exact second-byte position population in M
ordered first and second roles
same-scalar-position exclusion
exact source acquisition M
exact recurrence Assertion R and its support
exact Locality and completeness boundary B
```

Together these coordinates let later work address an exact ordered position
pair while retaining lineage:

```text
R + M + B + addressed positions (p, q)
↓
recover exact first source occurrence
recover exact second source occurrence
recover exact recurrence subject
recover exact later material and boundary
```

This separates addressability from durable relation occurrence:

```text
exact material, positions, boundary, and carried relation
!=
every addressable ordered position pair recorded as a finding
```

The current ledger already retains the exact pair Assertion reference, later
acquisition reference, material bytes, Locality, boundary, ordered roles, and
position coordinates. A later Responsibility can apply an exact carried
relation to those coordinates without a separately serialized container for
every possible relation.

The current recurrent-position result instead calculates the complete
Cartesian member count, expands a prefix chosen by `occurrence_limit`, and
calls the remainder known loss. That is exact under its present contract. It
does not establish that the complete Cartesian product must become a Seed
subject or a new result object.

Lack of an expanded member Assertion does not mean its source coordinates were
lost. It means no responsible occurrence has established that relation.

The operator's lineage hypothesis is therefore supported:

```text
preserve exact material, positions, boundary, and carried relation
↓
later addressed relation retains exact lineage
```

It does not by itself establish which members may proceed, which relation a
member carries, or whether later work must exhaust every member.

## The carried relation addresses the later coordinate

The earlier premise does more than divide a completed Cartesian population
afterward. It carries an exact position relation that can address the second
coordinate from the first.

For the recurrent adjacent-pair witness:

```text
R:
    second position is after first position
    exact distance is 1

later exact first-byte position p
+ R
↓
address q = p + 1
↓
determine whether q carries the required second byte
```

For report orientation, the same relation may be rendered:

```text
q = p + d

or

q - p = d
```

These equations are Rosetta rendering of exact position coordinates. They do
not declare a new numeric Addition or Subtraction Responsibility.

The result boundary is:

```text
required byte occurs at addressed q
↓
exact later relation under R is available

required byte does not occur at addressed q
↓
no later relation under R is established at p
```

The second branch does not establish a negative relation and does not
establish some other direction or distance. Another exact Responsibility can
later address another `(p, q)` relation through the preserved material and
coordinates without requiring every possible disagreement to have been
precomputed.

This is the decisive population distinction:

```text
preserve complete addressability through exact coordinates
!=
instantiate every possible relation before applying R
```

Under the repeated corpus's carried adjacent relation, the addressed road
reaches 217,511 matching positions. The 39,175,421,423 other combinations
remain addressable through the exact material and position coordinates but do
not become relations under `R` merely because both endpoints occur.

## Earlier association testimony

The earlier recursive pair witness in `scripts/material_pair_investigation.py`
preserves a relation before comparing later material:

```text
recurrent adjacent-pair subject
↓
exact premise occurrences
↓
exact premise position relations

for b"abxxab":
    second position after first position
    distance 1
```

It then constructs later position combinations and compares each combination
with that carried premise relation. Tests prove:

```text
b"ab"       -> same relation
b"ba"       -> different relative order
b"a---b"    -> different distance
```

This is the relevant historical discriminator in Rosetta terms. It is not
derived from language, meaning, or the desired conclusion. It is carried from
exact earlier occurrences and compares only exact position coordinates.

The historical witness carries the required discriminator but its current
implementation still applies it late. Its
`exact_occurrences_of_material_pair(...)` function constructs the complete
Cartesian population before comparison. It demonstrates the missing
separation clearly:

```text
possible later position relation
↓
Compare with exact carried premise relation
↓
same relation or different relation
```

The durable recurrent-position Measurement currently records the first
population. Neither witness uses the carried relation to address `q` directly
before recording or constructing the Cartesian population.

The archived `GoalOrientationAssociation` district supplies no reusable
constitutional road here. Its association coordinates were caller-supplied,
and later recovery classified that district as foreign compatibility
scaffolding. Reintroducing it would restore the bias this investigation is
testing.

## Exact corpus consequence

The repeated 218,058-byte corpus carries:

| coordinate | population |
|---|---:|
| exact bytes | 218,058 |
| adjacent positions | 218,057 |
| exact adjacent pair values | 2,708 |
| recurrent adjacent-pair subjects | 2,162 |
| current Cartesian recurrent-position findings | 39,175,638,934 |
| later positions matching the carried premise relation `second = first + 1` | 217,511 |
| Cartesian positions carrying another order or distance | 39,175,421,423 |

The 217,511 matching positions are the occurrences of the recurrent adjacent
pair values in the repeated material. The remaining 546 adjacent positions
belong to pair values whose count is exactly `1`, so they do not have a
recurrence Assertion.

The current product is about 180,109 times the matching population. This
calculation appended no Seed occurrence; it applies the current pair-count and
Cartesian formulas directly to the exact corpus bytes.

This does not establish that only the 217,511 matching positions can ever
become subjects. The exact material and position coordinates preserve access
to the other 39,175,421,423 combinations if another Responsibility addresses
them. It does establish that co-presence of their endpoints is not enough to
make them relations or required findings under the carried premise relation.

## What shared-position and ordered-path require

Shared-position Applicability accepts two addressed recurrent-position
Assertions. It determines:

```text
first relation second-position coordinate reference
=
second relation first-position coordinate reference
```

When applicable, the Measurement yields an `ordered_relation_path` Assertion
preserving the exact inputs and shared coordinate.

The consumer does not:

- enumerate recurrent-position Assertions;
- require the complete recurrent-position population;
- verify that every possible direction and distance was durably recorded;
- require known loss to be empty;
- use the available Cartesian count as an input coordinate.

Its minimal `b"abc"` witness consumes the adjacent `(a,b)` and `(b,c)`
relations. Those exact inputs exist inside the carried-premise-matching
population. The demonstrated `tatatata` path also has adjacent `ta` then `at`
inputs without requiring every `4 × 4` role-position combination.

Therefore:

```text
shared-position and ordered-path need exact addressed relations
!=
shared-position and ordered-path require all Cartesian relations
```

The current caller-addressed shared-position road has its own population and
exhaustion question. It supplies no warrant for enlarging the upstream
Measurement population.

## Answers to the investigation questions

### What exact Responsibility is currently being performed?

The runtime declares a Responsibility to measure each exact ordered position
for a recurrent byte pair in exact later material. Its calculation interprets
that as every distinct first-role position paired with every distinct
second-role position.

Active Book establishes common Measurement coordinates but does not separately
declare that specialized interpretation. The declared runtime string is not
independent constitutional support.

### What exact subjects does the current runtime require?

The lifecycle subjects are the exact recurrence Assertion and exact later
material result. Inside its finding calculation, every distinct ordered pair
of matching scalar positions becomes a finding without separate Applicability,
Participation, or comparison against the carried premise relation.

### Which distinction motivates the complete product?

The demonstrated motive is to preserve every direction and distance without
letting the caller provide either. The material and exact position coordinates
preserve their addressability. The choice to realize that addressability by
durable exhaustive Cartesian findings is an implementation shape.

### Is the product merely a discovery strategy?

The current product is more than a private loop: its pair subject, source
material, role order, boundary, available count, applied prefix, known loss,
and carried position Assertions become durable result coordinates. It cannot
be removed invisibly.

Expanding every member into a durable Assertion is less than recovered
constitutional necessity because no independent active Responsibility
requires that expansion, and the next consumer does not require its
completeness.

### What does the later consumer actually require?

It requires two exact addressed recurrent-position Assertions whose source,
Locality, boundary, result, and position-coordinate references validate. Its
Applicability result determines whether the addressed coordinates share the
required position. It does not consume or require the complete Cartesian
population.

## The existing adjacent-relation owner

The repository already has an active owner for the exact adjacent relation
used by this corpus experiment.

Every fresh material acquisition presented to the declared-Measurement road
produces a `PositionCoordinateMeasurementSubject`. The direct byte-pair
position Measurement applies this exact rule:

```text
source position p
↓
second position p + 1
↓
exact two-byte material at those positions
```

Its result preserves the material acquisition, Locality, boundary, position
coordinates, and exact adjacent material. The result does not append an event
for every adjacent position. It records a compact bounded account from which
exact Assertion references are derived. Focused tests prove that:

- `b"aaa"` exposes `(aa, 0, 1)` and `(aa, 1, 2)` with their shared coordinate;
- the complete reference reader does not construct a separate occurrence
  population;
- an exact addressed source position resolves only the adjacent pair
  references carrying that coordinate.

Thus the current owner of the corpus relation `second = first + 1` is the
direct `01.Source.D` Measurement, not the Cartesian recurrent-position
Measurement.

The next two existing Responsibilities are also already exact:

```text
direct pair-position Measurement result
+ exact addressed source-byte position coordinate
↓
01.Source.D.2
↓
pair-position references carrying that coordinate, in source order

01.Source.D.2 result
↓
shared-position Applicability and Measurement
↓
ordered_relation_path
```

`test_direct_position_coordinate_assertions_compose_without_recurrence_support`
proves the complete road with the middle position of `b"2+2=5\n"`. The D.2
result carries the exact `2+` and `+2` references. Shared-position reads those
addressed references without reading the complete direct pair-position
population and yields the ordered path.

This road requires no recurrence support, Cartesian position product, numeric
cap, or additional serialized container.

## The equality-shaped path is already demonstrated

The focused direct-path witness already uses the operator's proposed shape.
It addresses the middle position of `b"2+2=5\n"`:

```text
first adjacent relation   2 -> +
second adjacent relation  + -> 2
shared position           +
↓
ordered source coordinates [2, +, 2]
```

The path reader exposes those three exact position-coordinate dictionaries
beside the `ordered_relation_path` Assertion. Each coordinate retains its
source occurrence, exact position, and exact byte material. It also states an
important limit: returning the coordinates beside the path establishes no
material or relation carried by the path.

Therefore the endpoints needed for equality are already exact subjects:

```text
first path position coordinate carrying p
third path position coordinate carrying p
↓
Compare exact endpoint material
```

The current repository does not perform that Compare. It establishes the path
and leaves the endpoint relation open.

An external calculation over the exact 218,058-byte corpus gives the scale of
this possible next road:

| calculation over exact bytes | population |
|---|---:|
| adjacent three-position windows | 218,056 |
| windows whose first and third byte values are equal | 13,019 |
| distinct equal-endpoint three-byte values | 343 |

The most frequent exact values begin with `b"   "` (5,207), `b"\r\n\r"`
(885), `b"\n\r\n"` (885), `b" a "` (418), and `b"ere"` (326). These counts
are observer calculations, not Seed findings.

They show why equality is a useful next distinction without authoring which
language pattern matters. Every exact adjacent path has the same subject
shape; Compare determines which endpoints have equal material. The developer
does not nominate `ere`, `tat`, ` = `, or another favored pattern.

Commit `fef5b41f` introduced the ordered-source-position reader specifically
to expose these three exact coordinates beside the path. It made no Book or
runtime-consumer amendment. Current callers of that reader are proving tests;
no later Seed runtime consumes the endpoint coordinates. The equality road is
therefore an exposed seam, not a relation already established by the reader.

## Mechanical guard against the parallel Candidate road

A focused scaling probe confirms that expanding every direct position
Assertion through the generic Candidate source reader is the wrong mechanical
continuation as well as the wrong Responsibility.

For `N` addressed direct-position references, that reader resolves the direct
result, then resolves each reference by scanning from source position zero to
the addressed position. Measured time was:

| addressed references | wall time |
|---:|---:|
| 63 | 0.128 s |
| 127 | 0.368 s |
| 255 | 1.220 s |
| 511 | 4.403 s |
| 1,023 | 16.626 s |

At 218,057 references the repeated scans imply about 23.8 billion Assertion
identity calculations and an extrapolated duration measured in days. This
profile changes no law. It confirms that routing the direct result through the
global Candidate expansion would miss both the adjacent D.2/shared-position
road and the experiment's practical boundary.

The exact addressed-position reader used by D.2 is different: it can resolve
the at-most-two adjacent pair references carrying the addressed coordinate
without reading the complete direct reference population.

## Compare does different work

Current `04.Compare.A` does not apply a carried position relation to address a
later coordinate. It compares complete earlier and later byte-pair count
Measurement results. Its distinctions are same content, conflict, earlier
finding, later finding, and Unknown across those result populations.

Current `04.Compare.B` also does not compare the first and third coordinates
of the path. It compares each complete pair subject carried beside the path
against recorded pair-count comparison findings. For `p q p`, its subjects
are `pq` and `qp`, not endpoint `p` and endpoint `p`.

The investigation script demonstrates comparison of a later direction and
distance against an earlier premise relation, but it constructs the Cartesian
product first and has no current durable owner. It is useful testimony for the
distinction; it is not the active owner of adjacent coordinate addressing.

Therefore:

```text
direct pair-position Measurement
    owns the exact adjacent relation in current material

01.Source.D.2
    owns exact local resolution around an addressed source position

shared-position Measurement
    owns composition of two exact addressed relations

04.Compare.A
    owns comparison of complete pair-count result populations

04.Compare.B
    owns comparison of path pair subjects with recorded pair findings
```

No current Compare Responsibility performs general projection of arbitrary
carried direction and distance coordinates. No such generalization is needed
to continue the present adjacent-relation experiment. No current Compare
Responsibility compares the exact first and third path coordinates either.

## Exact live stop

The ordinary Witness road already records the direct pair-position Measurement
result. The stop occurs afterward:

```text
direct pair-position result carrying every exact adjacent reference
↓
exact source-byte position becomes a 01.Source.D.2 subject
X
```

The D.2 clause and runtime govern an exact addressed position. Focused callers
supply that exact coordinate. The live console does not carry source-position
coordinates into D.2, and active law does not currently say that every source
position is D.2 work. Treating the complete position population as required
would recreate the global traversal mistake under a smaller name.

This is the earliest live stop. It is not a missing adjacent relation and it
is not a need for `CoordinateSpace`. The adjacent relations and their lineage
are already exactly addressable.

The focused path road then reaches another exact stop:

```text
ordered path beside [p, q, p]
↓
first and third position coordinates become exact Compare subjects
X
```

The second stop is the equality question. The coordinates exist; their equal
material has not become a Compare result or relation merely because the
developer can observe it.

## Smallest missing active position

The missing Compare does not need composite path material. Its exact subjects
are already beside the path:

```text
current Standing carrying ordered path P

subject A
    P first source-position coordinate

subject B
    P third source-position coordinate

rule
    Compare exact material carried by A and B

Act occurrence
    A and B participate under their exact endpoint roles

result
    same-content finding, difference, conflict, or Unknown
    under the exact path and source boundary
```

This result would preserve the path reference, endpoint coordinate references,
source occurrence, Locality, boundary, Authority, Scope, limits, and exact
Compare finding. It would not by itself establish:

- composite `p q p` material carried by the path;
- a generic `is` relation;
- equality of the endpoint occurrences;
- equality of anything outside the exact endpoint material and Scope;
- later Standing.

That is the smallest missing active position exposed by the current witness.
The Book has generic Compare physiology but no exact endpoint-coordinate
Compare clause. Runtime has no endpoint-coordinate Compare occurrence.

## Disposition

The exact answer is:

```text
39,175,638,934
= exact member count calculated by the current Cartesian runtime rule
!= durable finding population independently required by active grammar
!= population required by shared-position / ordered-path

217,511 adjacent recurrent-pair positions
= exact relations already addressable through direct pair-position Measurement
```

The Cartesian rule calculates every possible ordered role-position
combination, then treats expansion of those combinations as its Measurement
finding population. Exact material, positions, boundary, and carried relation
already preserve addressability without making that calculated product a new
Seed object.

No cap correction follows merely from this report. No runtime deletion follows.
Reverse-order and distance distinctions remain addressable through exact
coordinates when another Responsibility carries such a relation. They do not
need to be pre-recorded merely because both endpoints exist.

The exact boundary is:

```text
established
    exact recurrence Assertion and count support
    exact adjacent premise occurrences
    exact premise position relation
    exact later material and scalar positions
    exact Cartesian member count under the current runtime calculation
    direct Measurement of every adjacent position relation
    compact addressability of exact adjacent Assertion references
    01.Source.D.2 resolution for an exact addressed source position
    shared-position composition from an exact D.2 result
    exact ordered source coordinates beside the path
    demonstrated [2, +, 2] path subject
    current partial member expansion and bounded known loss

not established by active grammar
    a Responsibility requiring every Cartesian combination
    to become a durable finding before the carried premise relation is applied
    endpoint co-presence as a relation occurrence
    every source position as required 01.Source.D.2 work
    general Compare projection of arbitrary direction and distance
    endpoint-material Compare for the first and third path coordinates
```

The owner question is answered for the current adjacent relation. Direct
pair-position Measurement establishes it, D.2 resolves it around an addressed
position, and shared-position composes it. Compare A does not own that work.

The remaining live road has two exact joints:

```text
what exact current Standing makes a source-byte position
an addressed D.2 subject?

missing endpoint-coordinate Compare Responsibility takes the first and third
coordinates of the resulting path as its subjects
```

This report does not answer either by enumerating every position, creating a
traversal Responsibility, routing the corpus through Candidate, manufacturing
another coordinate container, or treating equal bytes as an already
established relation.

## Validation

Focused current witnesses:

```text
tests/test_measurement_of_recurrent_byte_pair_occurrence_position.py::
  test_pair_occurrence_measurement_finds_exact_positions_without_a_sign

tests/test_material_pair_investigation.py::
  test_recurrence_and_position_premise_of_pair_discriminate_fresh_material

tests/test_measurement_of_shared_position_of_byte_pair_occurrences.py::
  test_exact_yielded_pair_relations_compose_at_one_shared_position

tests/test_measurement_of_position_coordinates_of_byte_pair_occurrences.py::
  test_full_reference_reader_does_not_construct_the_occurrence_population

tests/test_measurement_of_position_coordinates_of_byte_pair_occurrences.py::
  test_exact_addressed_source_position_reads_only_its_carried_pair_references

tests/test_measurement_of_shared_position_of_byte_pair_occurrences.py::
  test_direct_position_coordinate_assertions_compose_without_recurrence_support

tests/test_measurement_of_shared_position_of_byte_pair_occurrences.py::
  test_ordered_source_positions_remain_beside_the_path_assertion
```

All seven focused witnesses pass. The Book admission gate also passes; the
combined run reports 18 passed. The corpus calculations used the exact sixteen
300-line windows from `tests/book_material_test_witness.py` and appended no
ledger occurrence.

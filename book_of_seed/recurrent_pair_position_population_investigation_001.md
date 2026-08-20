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

The test requires both relative orders and distances `1` and `5`. The current
rule therefore means:

```text
first byte role at every matching position
×
second byte role at every matching distinct position
```

It does not mean only a contiguous occurrence of the two-byte material.

That implementation decision performs exact work: it does not let the caller
supply direction or distance, and it preserves every possible relative
position before later comparison.

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

The complete product preserves distinctions that a narrower implementation
could otherwise author silently:

- which byte occupies the first and second Act-local roles;
- both relative position orders;
- every exact distance between the addressed byte occurrences;
- distinct position occurrences despite equal byte material;
- an exact available count before an applied partial-result bound.

The test `test_pair_occurrence_measurement_finds_exact_positions_without_a_sign`
proves that these distinctions are deliberate. Removing reverse-order or
nonadjacent findings would change the current rule and its demonstrated
result. That cannot be presented as a performance correction.

What remains unsupported is the stronger statement:

```text
every mathematically possible role-position combination
=
every subject required to become a durable Measurement finding
```

Current implementation asserts that statement through its loop. Active Book
does not independently establish it.

## The coordinate space is real material

The Cartesian population is not disposable merely because every member need
not become a durable finding immediately.

For exact recurrent pair `R`, later material `M`, and boundary `B`, the runtime
already determines:

```text
exact first-byte position population in M
exact second-byte position population in M
ordered first and second roles
same-scalar-position exclusion
exact source acquisition M
exact recurrence Assertion R and its support
exact Locality and completeness boundary B
```

Together these coordinates define an exact finite space of possible meetings.
`Meeting` is Rosetta orientation here; it names an ordered member `(p, q)` of
that space, not a new constitutional relation.

That exact space can be the result material from which later work addresses a
member while retaining lineage:

```text
coordinate space C(R, M, B)
+ addressed positions (p, q)
↓
recover exact first source occurrence
recover exact second source occurrence
recover exact recurrence subject
recover exact later material and boundary
```

This separates two populations that the current result shape partially
compresses:

```text
exact bounded coordinate space
!=
every member recorded as a durable finding occurrence
```

The current ledger retains enough exact source coordinates to reconstruct the
space: pair Assertion reference, exact later acquisition reference, exact
material bytes, Locality, boundary, ordered roles, exclusion rule, and
available count. The applied `occurrence_limit` then decides how many members
are expanded into position Assertions and marks the rest as known loss.

Calling every unexpanded member `known loss` is exact under the current result
contract. It also shows the compression: the coordinate space itself is not
given a separately readable result position, so preserving the space and
recording every member are treated as though they were the same work.

The operator's lineage hypothesis is therefore supported:

```text
preserve the exact coordinate space
↓
later addressed meeting retains exact lineage
```

It does not by itself establish which members may proceed, which relation a
member carries, or whether later work must exhaust every member.

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

The historical witness does **not** solve the population problem by itself.
Its `exact_occurrences_of_material_pair(...)` function also constructs the
complete Cartesian population before comparison. It demonstrates the missing
separation clearly:

```text
possible later position relation
↓
Compare with exact carried premise relation
↓
same relation or different relation
```

The durable recurrent-position Measurement currently records the first
population. It does not apply the second distinction before recording that
population.

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

This does not establish that only the 217,511 matching positions may become
subjects. The 39,175,421,423 other combinations carry exact relative-order and
distance differences under the historical comparison rule. It establishes
that the product is created before the already-demonstrated positional
distinction is applied.

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
letting the caller provide either. That distinction is real. The choice to
realize it by durable exhaustive Cartesian findings is an implementation
shape.

### Is the product merely a discovery strategy?

The coordinate space is more than a private strategy: its pair subject, source
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

## Disposition

The exact answer is:

```text
39,175,638,934
= exact member count of the current runtime coordinate space
!= accidental performance defect
!= durable finding population independently required by active grammar
!= population required by shared-position / ordered-path
```

The current rule defines a legitimate exact coordinate space, then treats
expansion of its members as the Measurement finding population before the next
demonstrated exact distinction. The earlier recurrent-pair relation supplies a
non-semantic positional premise, but current durable Measurement begins
recording possible role-position combinations before any comparison with that
premise.

No cap correction follows. No runtime deletion follows. Shrinking the
population to adjacency would remove reverse-order and distance distinctions
that current tests deliberately preserve. Keeping the full product would
require recovering an exact Responsibility whose required findings are all
possible ordered position relations, rather than inferring that requirement
from the present nested loop.

The exact boundary is:

```text
established
    exact recurrence Assertion and count support
    exact adjacent premise occurrences
    exact premise position relation
    exact later material and scalar positions
    exact finite coordinate space and its member count
    current partial member expansion and bounded known loss

not established
    an active Responsibility requiring every coordinate-space member
    to become a durable finding before the carried premise relation is applied
```

The population question must be resolved before assigning a live numeric
bound or connecting the recurrent-position road to the corpus.

## Validation

Focused current witnesses:

```text
tests/test_measurement_of_recurrent_byte_pair_occurrence_position.py::
  test_pair_occurrence_measurement_finds_exact_positions_without_a_sign

tests/test_material_pair_investigation.py::
  test_recurrence_and_position_premise_of_pair_discriminate_fresh_material

tests/test_measurement_of_shared_position_of_byte_pair_occurrences.py::
  test_exact_yielded_pair_relations_compose_at_one_shared_position
```

All three pass. The corpus calculation used the exact sixteen 300-line windows
from `tests/book_material_test_witness.py` and appended no ledger occurrence.

# Inward walk-binding refusal observation 001

## Boundary

This is findings only. No Book, machine grammar, or runtime behavior changes.

The preceding blind operation found this source form:

```text
A B C D D (E D)^n F G
```

with exact scalar material carried across each of its eight edge forms. The
later `H` was adjacent but carried nothing from `G` beyond the responsible
boundary.

Sameness across an edge does not show that the later occurrence requires that
material. This operation therefore stays on the same floor and asks the live
readers:

```text
retain the same append address
retain the same responsible boundary
retain every unrelated coordinate

change or remove one exact carried top coordinate

does the existing later work refuse?
```

No syntax rule is added to obtain the refusal.

## 1. Exact operation

`scripts/observe_inward_walk_binding_refusals.py` reads the already frozen walk
and continuity findings. For each exact edge occurrence it groups the complete
later scalar addresses by their top coordinate. It then performs two separate
controls for each top coordinate:

```text
change every carried scalar addressed beneath only that top coordinate

remove only that top coordinate
```

The material is changed before append. The ledger records exactly the changed
material; this is not post-append corruption. Existing assignment and Act
readers then either continue or refuse.

The clear coordinate lookup is read here. This operation occurs after blind
discovery has already frozen which walk edges and scalar addresses recur. The
lookup permits an exact addressed change; it does not choose the source form.

The operation also gives every `E` assignment an intact `D` result reference
from an earlier iteration while leaving its other coordinates unchanged.

```text
input occurrence artifact SHA-256
52ff0a070b0f9a1f4c117643918ad8f64e92c906a99efe84a01453759e645329

blind coordinate-surface artifact SHA-256
cbbeaf9cb35185a3940e5ab5eabf75c2fe2b077953f0cb113bf4532d3686f559

blind walk artifact SHA-256
6b1080583671b1a5d922d469769ff5361c52af24c703d2c95c81cf3bbd14de92

blind continuity artifact SHA-256
61387c47e498fac5721e89967f01f4d511ce158659a15799a08df6914eeb12cf

separate clear coordinate lookup SHA-256
c77eadf6260f8820da5f71e96dfd5b1d311353c92b071f57b46f6b012af90954

refusal finding SHA-256
60a7f042d3a99b9b9a7dd065a736548e381a9c99b392b019febd0f923d8b0aeb
```

The complete operation took 15.124 seconds. Its 17 focused observer tests took
0.10 seconds.

## 2. Exact result

The eight bound edge forms carry 33 distinct edge/top-coordinate combinations.
Applying each combination to every occurrence of its edge produced:

```text
change controls                         330
change refused                          330
change accepted                           0

remove controls                         330
remove refused                          293
remove accepted                          37

all coordinate controls                 660
all coordinate controls refused         623
all coordinate controls accepted         37
```

Every acceptance is the same exact case:

```text
D -> E
remove addressed_byte_occurrence_reference_determination_result_reference
37 / 37 accepted
```

Every other carried top coordinate is required by the current later reader in
both controls. The required coordinates differ by edge:

```text
A -> B  input relation, Scope, source Locality,
        acquisition occurrence, prior Standing boundary

B -> C  Book clause, completeness boundary, Scope, source Localities,
        source occurrences, prior Standing boundary

C -> D  addressed source coordinate, Scope

D -> D  addressed source coordinate, Book clause, determination rule,
        direct-pair result reference, limits, Responsibility, Scope, Unknown

D -> E  first position Assertion, second position Assertion, Scope

E -> D  addressed source coordinate, Scope

D -> F  Responsibility assignment reference, Scope, source Locality

F -> G  Book clause, source Assertion reference, source occurrences
```

This establishes more than adjacency. Each of the eight edge forms has exact
carried material whose change or absence prevents its later work.

## 3. The D-to-E distinction

The observed `D -> E` carriage contains four top coordinates. Three are
required:

```text
first_position_assertion
second_position_assertion
scope
```

The fourth is conditional:

```text
addressed_byte_occurrence_reference_determination_result_reference
```

Changing any scalar inside that reference is refused in all 37 occurrences.
Giving `E` an intact reference to the wrong earlier `D` iteration is likewise
refused in all 37 occurrences.

But removing the coordinate is accepted in all 37 occurrences.

The current reader explains the result exactly. In
`measurement_of_shared_position_of_byte_pair_occurrences.py::_read_assignment`:

```text
reference present
-> require the exact D.2 result and validate the supplied reference

reference absent
-> derive the two inputs from first_position_assertion
   and second_position_assertion
```

Thus the direct result reference has exact validation when carried, including
iteration identity, but the reader does not require it. The two Assertions and
Scope still bind `D` material into `E`; the explicit result reference is a
larger observed carriage than the current minimum accepted assignment.

This corrects the strongest possible reading of the preceding report:

```text
observed exact carriage
!= every carried coordinate is required grammar
```

## 4. The stop at G to H remains exact

The four `G -> H` transitions have no complete non-boundary scalar address to
exercise. The operation creates no mutation target for them and does not turn
adjacency into work.

```text
A through G  every edge form has counterfactually required carried material
G to H       no exact carried source/result material under this measurement
```

The negative control therefore remains intact.

## 5. What this floor now warrants

The A-through-G form has syntax with teeth at this floor:

```text
all eight edge forms carry exact later requirements
all 330 isolated scalar changes are refused
32 of 33 exact edge/top-coordinate combinations refuse absence
the wrong D iteration is refused
G to H remains adjacent and unbound
```

It is therefore warranted to call A-through-G the first exact enforced Seed
story found by this inward campaign at this floor.

That statement does not make every arrow one universal relation. Some edges
carry the immediate earlier result; others carry source coordinates or results
whose origin precedes both neighboring walks. The concrete arrows remain
different.

Nor does it make all observed carriage constitutional. The optional D-result
reference is the exact counterexample. The enforced story is slightly smaller
than the full continuity surface.

## 6. Stop

Do not climb another floor in this slice.

The first runtime discrepancy exposed by this observation is exact and narrow:

```text
D result reference is emitted into every E assignment
if present, it must be exact
if absent, current E reading still succeeds
```

This report does not decide whether the coordinate should become required or
should cease to be emitted. That question belongs to the active grammar and
the producer/reader contract, not to the blind measurement.

Freeze the enforced A-through-G story, its optional-coordinate refusal, and
the G-to-H boundary for review.

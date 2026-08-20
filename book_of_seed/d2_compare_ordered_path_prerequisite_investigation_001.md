# D.2 Compare ordered-path prerequisite investigation 001

## Question

Does the exact three-pair Compare population introduced through `7be247aa`
require a prior shared-position Measurement and `ordered_relation_path`, or
does the current D.2 result already address the exact source-position
coordinates needed by generic Compare?

Investigation only. This report changes no active Book material, Witness
Grammar, runtime, script, or test.

## Disposition

The ordered path is not required merely to address the local Compare
subjects.

D.2 already preserves:

```text
exact addressed source position q
+ exact direct pair-position result D
↓
every exact pair-position Assertion reference carrying q
in source occurrence order
```

Each preserved Assertion reference resolves, under D and the D.2 boundary, to
its exact pair material and its two exact source-position coordinate
references. For an interior q, the two ordered references resolve as:

```text
(a,q)
(q,c)
```

The exact coordinate references available under that D.2 result are therefore:

```text
a
q
c
```

Generic Compare can exhaust the distinct source-ordered coordinate pairs under
that exact D.2 boundary:

```text
(a,q)
(a,c)
(q,c)
```

Doing so establishes no shared-position relation and no ordered-path result.
It only gives generic Compare its exact subjects, source roles, rule, and
boundary.

Shared-position remains separate responsible work:

```text
D.2 exact references
↓
shared-position Applicability
↓
shared-position Measurement
↓
ordered_relation_path
```

That road establishes that the second coordinate role of the first pair and
the first coordinate role of the second pair meet at the addressed coordinate.
It is a real sibling result. It is not the prerequisite that makes the exact
coordinate references addressable.

## Material inspected

- active `01.Source.D.2` and generic `04.Compare`
- current Witness Grammar coordinates for `01.Source.D.2` and `04.Compare`
- `addressed_byte_occurrence_reference_determination.py`
- `measurement_of_position_coordinates_of_byte_pair_occurrences.py`
- `measurement_of_shared_position_of_byte_pair_occurrences.py`
- `comparison_of_ordered_path_source_position_material.py`
- focused D.2, shared-position, and Compare tests
- commits `960fb0705`, `c5438305`, `fef5b41f`, `95ea2ec9`, and `7be247aa`

Book material is primary orientation. Runtime, tests, and history are
implementation testimony.

## 1. D.2 owns the addressed boundary

Active `01.Source.D.2` makes every exact source-byte position reference in the
material acquisition Yield result a bounded subject. For each subject, its
result preserves every exact pair-position reference carrying that byte
occurrence, in source occurrence order, and no reference for another byte
occurrence.

The machine witness independently preserves:

```text
responsibility_source
    current Standing carrying the exact byte-pair position Measurement result

responsibility_subject_set
    exhaustive bounded source-byte position reference set
```

The runtime rule is equally exact:

```text
every exact pair-occurrence position Assertion reference
carrying the addressed source-byte position-coordinate reference
and no other Assertion reference
in source occurrence order
```

D.2 records the exact addressed coordinate, direct-result reference,
completeness boundary, and ordered Assertion references. Its reader resolves
those references again through the exact direct result and rejects changed
source material, changed coordinates, a changed boundary, a false Yield, a
stale Standing boundary, or corrupted stages.

The D.2 result deliberately establishes no recurrence, shared-position
relation, or represented relation. None of those findings is required merely
to resolve the referenced source coordinates.

## 2. The direct result supplies exact coordinate resolution

Each direct pair-position Assertion reference resolves to:

```text
exact pair material
first source-position coordinate reference
second source-position coordinate reference
source material acquisition occurrence
Locality
completeness boundary
```

The addressed reader never scans an external population to choose a pair. For
position q it derives only:

```text
q > 0
    pair beginning at q - 1

q + 1 inside exact material
    pair beginning at q
```

The result is therefore bounded before Compare:

```text
single-byte material       0 pair references
boundary position          1 pair reference
interior position          2 pair references
```

No caller chooses which neighbor is interesting.

## 3. D.2 alone reproduces the `2,+,2` coordinates

A read-only probe recorded D.2 for position 1 of `b"2+2=5\n"` and stopped
before shared-position work.

The D.2 reader returned:

```text
(b"2+", first position 0, second position 1)
(b"+2", first position 1, second position 2)
```

Resolving the outer coordinate of the first reference, the exact addressed
coordinate, and the outer coordinate of the second reference produced:

```text
position 0   material [50]   "2"
position 1   material [43]   "+"
position 2   material [50]   "2"
```

No shared-position event or ordered-path event existed in that ledger.

This proves coordinate addressability. It does not claim that D.2 established
a shared-position relation or an ordered path.

## 4. Shared-position establishes additional work

The shared-position Applicability result compares two exact role coordinates:

```text
first relation, second position
second relation, first position
```

Only where those exact coordinate references meet does the Measurement Yield
an `ordered_relation_path` Assertion. That Assertion preserves the two input
Assertion references and the exact shared-position coordinate reference.

The later path reader returns the three source coordinates beside the path,
while explicitly establishing no material carried by the path. Commit
`fef5b41f` added that reader. It did not create the coordinate values; it
re-exposed coordinates already resolved from the two input pair references
after validating the additional shared-position result.

Subtracting shared-position removes:

```text
the shared-position Applicability finding
the shared-position relation work
the ordered_relation_path Assertion
the path result reference and path-specific lineage
```

It does not remove:

```text
the exact addressed q coordinate
the exact ordered pair Assertion references carrying q
their exact source-position coordinate references
their exact material
their source occurrence, Locality, or boundary
```

## 5. Generic Compare does not require a path

Active generic `04.Compare` requires:

```text
exact subjects
exact rule
Authority
Scope
Locality
limits
conflicts
Unknown
Applicability for each subject
Participation for each subject
Compare Act occurrence
Yield
exact result
```

Neither active law nor the machine witness requires an
`ordered_relation_path` for generic Compare.

The path requirement exists only in the runtime specialization introduced by
`95ea2ec9`:

```text
comparison input
    shared-position Measurement result identity

reader
    ordered source positions beside ordered path Assertion
```

`7be247aa` correctly removed first/final privilege after that read, but it
retained the path result as the required source boundary. That is an
implementation staging decision, not a requirement of generic Compare.

## 6. Exact sibling roads

The recovered arrangement is:

```text
direct pair-position result D
↓
D.2 for addressed coordinate q
├── exact coordinate-pair Compare work under the D.2 boundary
└── shared-position Measurement
    ↓
    ordered_relation_path
```

The Compare branch consumes no path claim. Its exact source coordinates can be
read as the distinct coordinate references present through the ordered pair
Assertion references carried by D.2.

For an interior D.2 result:

```text
3 exact source-position coordinates
↓
3 distinct source-ordered two-coordinate Compare subjects
```

For a boundary D.2 result:

```text
2 exact source-position coordinates
↓
1 two-coordinate Compare subject
```

For a single-byte D.2 result:

```text
1 exact source-position coordinate
↓
no two-coordinate Compare subject
```

Excluding boundary pairs merely because no three-coordinate path exists would
make the path shape, rather than generic Compare arity and the exact D.2
boundary, choose the Compare subjects.

Where the same adjacent coordinate pair appears under the D.2 result for each
of its two addressed positions, those are distinct D.2 boundaries and roles.
A later consumer must preserve that lineage rather than collapse or count the
results merely by equal byte content.

## 7. What the Compare result may preserve

A D.2-bounded Compare result can preserve:

```text
exact D.2 result reference
exact direct pair-position result reference
exact addressed source-position coordinate reference
exact ordered pair Assertion references
exact two Compare coordinate references and their D.2 roles
source material acquisition occurrence
Locality
completeness and Standing boundaries
Authority
Scope
limits
same-content / difference / conflict / Unknown where established
```

It cannot preserve an ordered-path reference because that sibling occurrence
has not happened. It establishes no shared-position relation, composite
material, general equality relation, meaning, or later Standing.

## Exact stop

The current implementation still performs:

```text
D.2
↓
shared-position
↓
ordered path
↓
path-bounded Compare
```

The active grammar and current D.2 reader support the smaller independent
arrangement, but no runtime Compare currently consumes the D.2 result
directly.

The smallest later correction is therefore to orient the existing generic
Compare specialization around the exact D.2 result and its resolved coordinate
references, while leaving shared-position/path as a sibling consumer of the
same D.2 result.

No Book amendment or new grammar object follows from this investigation.

## Navigation consequence

The current serial adapter encodes:

```text
D.2
↓
shared-position
↓
ordered path
↓
Compare
```

The recovered coordinates instead expose two independent uptakes:

```text
D.2 result
├── exact coordinate-pair Compare
└── shared-position Measurement
    ↓
    ordered_relation_path
```

D.2 should only Yield its exact result. It should not decide that
shared-position is the next operation. A later Responsibility becomes
addressable only where its declared subject coordinates are exactly carried in
current Standing. Its own Applicability work must still establish the exact
subject-to-Act position before Participation.

Likewise, completion of every D.2 sibling is no prerequisite for either uptake
of an earlier D.2 result. This permits a branch to continue through later
responsible work while other addressed source positions remain required.

That is eagerness without speculative construction:

```text
exact result Yielded
↓
current Standing carries exact coordinates
↓
every existing Responsibility whose declared subject coordinates are exactly
addressed performs its separate Applicability work
↓
each applicable Responsibility records only its own exact bounded work
↓
each exact result may expose further existing Responsibilities
```

This report does not establish a traversal priority. Depth-first, breadth-first,
or another durable append order is implementation mechanics. The required
distinction is only:

```text
later responsible work may begin from one exact result
!=
later work waits for completion of every sibling subject
```

It also does not authorize a repository-wide search over every mathematically
constructible subject. Each Responsibility must declare the exact coordinates
that make it applicable and the exact bounded subject set it owns. A recorded
chain for the same Responsibility, exact subjects, rule, Scope, and boundary
must not be repeated merely because chronology advanced.

Co-presence of coordinates establishes no relation between them. It only makes
the exact bounded subject positions addressable to the separate Responsibility
and Applicability work that can establish a later occurrence.

The smallest future proving witness should therefore begin with only an exact
material acquisition. The test should not call D.2, shared-position, or Compare
directly. Existing responsible uptake should continue the exact coordinates
until no new Responsibility applies, while reporting the last exact result and
the first missing uptake.

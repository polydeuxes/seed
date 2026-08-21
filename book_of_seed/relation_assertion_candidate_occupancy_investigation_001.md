# Relation-Assertion Candidate occupancy investigation 001

Date: 2026-08-21

## Question and boundary

The active relation-Assertion anatomy is:

```text
relation Assertion
├── first subject
├── exact relation content
└── second subject
```

This investigation asks whether current Candidate grammar owns preservation of
a bounded possible assignment of source-derived results to those positions
without establishing the relation or its truth.

It uses these raw adversarial witnesses:

```text
is '=' =
'=' is =
```

No grammatical roles are supplied to Seed. An external observer may render
the first line as:

```text
first subject          is
second subject         '='
exact relation content final =
```

That rendering is not an input and is not a finding. The two lines deliberately
refuse an infix rule and refuse any rule under which material `is` or `=` has a
permanent grammatical role.

This report changes no active Book chapter, witness grammar, runtime, or test.
`Occupancy`, `slot`, and `formation` below are report renderings. They name no
additional Seed grammar.

## Finding

Current Candidate grammar does not own the three-position assignment.

It owns a narrower preservation boundary:

```text
exact addressed source Assertion
or
exact ordered pair of source Assertions
↓
Candidate Act
↓
Candidate carrying exact source references
and relation: Unknown
```

The Candidate Act-local roles are:

```text
source Assertion

first source Assertion
second source Assertion
```

They are not the relation-Assertion positions:

```text
first subject
exact relation content
second subject
```

Candidate therefore preserves neutral source material that later work may use.
It does not assign that material to the three relation-Assertion positions.

The first live vacancy remains the responsible work that assigns already
bounded source-derived material to the existing three positions without
deriving the assignment from infix order, spelling, source adjacency, or an
observer-supplied parse.

## 1. Active Candidate subject shape

### 1.1 Book and machine witness

Active `01.Source.E.1` assigns two Candidate Responsibilities through an exact
boundary:

```text
every exact source Assertion separately

every distinct ordered source Assertion pair
```

The machine witness names the subject as:

```text
required_source_Assertion_or_ordered_source_Assertion_pair
```

Neither active rendering names:

- a three-source subject;
- a relation-content source role;
- a first-subject role;
- a second-subject role;
- a rule mapping Candidate source roles to relation-Assertion roles.

The result preserves exact source Assertion references, source coordinates,
and Act-local roles. It explicitly requires a responsible occurrence for any
relation.

### 1.2 Runtime

`candidate_results_from_exact_result_assertions.py` constructs required
subjects in two shapes only:

```text
{
    role: source Assertion,
    source_assertion_references: [A]
}

{
    role: ordered source Assertion pair,
    source_assertion_references: [A, B]
}
```

The resulting Candidate carries either:

```text
source_assertion_reference
source_role = source Assertion
```

or:

```text
first_source_assertion_reference
second_source_assertion_reference
first_source_role  = first source Assertion
second_source_role = second source Assertion
```

Every Candidate result retains:

```text
relation = Unknown
```

Its limits state that the Candidate Act establishes no source Assertion
relation.

Candidate Applicability in this module concerns a required unary or ordered
pair subject entering its exact Candidate Act. The recorded finding is
`applicable` because the Candidate Responsibility has already defined that
subject population. It does not examine or assign relation-Assertion roles.

### 1.3 Candidate Compare does not change the roles

Active `04.Compare.C` makes the Candidate itself the Compare subject. The
Candidate's first and second source Assertion references remain coordinates
carried by that Candidate; the source Assertions do not become Compare
participants.

This preserves the same separation:

```text
Candidate source order
!= Compare subject roles
!= relation-Assertion roles
```

No third relation-content occupant appears in that road.

## 2. The adversarial raw witnesses

### 2.1 Mechanical probe

Both raw values contain the same eight bytes in different source order:

```text
is '=' =
'=' is =
```

A disposable in-memory probe supplied each value through the current operator
material test witness, recorded the existing exact-byte Measurement, froze its
boundary, and recovered the required subjects of both current Candidate
Responsibilities.

Observed for each raw value:

| coordinate | count |
|---|---:|
| source Assertion references visible to Candidate | 10 |
| unary required Candidate subjects | 10 |
| ordered-pair required Candidate subjects | 90 |
| three-source required Candidate subjects | 0 |
| relation-content Candidate roles | 0 |

Every unary subject carried role `source Assertion`. Every ordered subject
carried role `ordered source Assertion pair` and exactly two source references.

The exact-byte Measurement groups equal byte material. Because the two raw
values have the same byte multiset, this entrance gives Candidate the same
source-Assertion population shape. It cannot distinguish the observer's two
proposed parses.

The position and adjacent-pair Measurements can preserve the changed source
order through their separate results. Even with that order addressable,
current Candidate still supplies only unary and ordered-pair Act-local roles.
Source order does not furnish the missing role assignment.

### 2.2 What the witness proves

The pair is a useful refusal witness:

```text
same exact material forms
+ different source arrangement
!= source-independent grammatical roles
```

It catches all of these authored shortcuts:

```text
middle material is relation content
final material cannot be relation content
is always occupies relation content
= always occupies relation content
source order is grammatical role order
```

The correct current result is not the observer's parse. It is:

```text
exact material and source order preserved
relation-Assertion role assignment not established
```

## 3. Source.F and Standing.E begin after the vacancy

### 3.1 Source.F

Active `01.Source.F` begins with:

```text
supplied material carrying a relation Assertion
```

It preserves that Assertion and its source coordinates. It establishes no
relation occurrence.

Thus Source.F preserves an assignment already carried by material. It does not
derive the first subject, relation content, or second subject from unassigned
source material.

No current runtime module implements a Source.F producer that forms those
three coordinates from the bounded results established by the current
Measurement road.

### 3.2 Standing.E

Active `01.Standing.E` requires a relation Assertion that already carries its
three positions. It then requires the exact relation occurrence, Authority,
Scope, Locality, limits, conflicts, and Unknown for relation Standing.

It explicitly refuses a relation occurrence from multiplicity, temporal
order, shared material, provenance, or the relation Assertion itself.

Standing.E therefore governs later establishment. It is not the upstream role
assignment.

### 3.3 Recording

Active `05.Recording.A` preserves an exact Assertion and its source
coordinates. Recording likewise begins after the Assertion content exists.
Record existence establishes no relation.

### 3.4 Generic Compare

Generic Compare requires exact subjects and an exact rule. It may compare two
already-addressed subjects. It does not decide that some source result occupies
first subject, exact relation content, or second subject.

Comparing the bytes for `is` and `=` would establish only the distinction
warranted by that Compare rule, such as same-content or difference. It would
not assign either value a grammatical role.

## 4. Candidate is a neutral carrier, not the missing assignment

The Candidate hypothesis is partly right:

```text
Candidate
= preservation of exact addressed source references
  without relation establishment
```

That is useful quarantine. A Candidate may carry rich source Assertions from
Measurement, Compare, or earlier Candidate results. Its occupants need not be
single bytes or words; exact source references can preserve complex bounded
result coordinates.

But the stronger hypothesis is not established:

```text
Candidate
= possible first-subject / relation-content / second-subject assignment
```

The missing distinctions are concrete:

- Candidate currently has at most two source references in a required subject;
- its first and second labels are source-enumeration roles;
- it has no relation-content role;
- it carries `relation: Unknown` rather than a proposed exact relation
  Assertion;
- no result maps its source roles onto the three Standing.E positions.

Adding a three-reference Candidate specialization would not merely expose a
current runtime route. Active `01.Source.E.1` does not assign such a subject
population or such roles.

## 5. Source order is evidence, not role warrant

The ordered Candidate Responsibility enumerates both directions for every
distinct source Assertion pair:

```text
Candidate(A, B)
Candidate(B, A)
```

This proves that its `first source Assertion` and `second source Assertion`
labels belong to Candidate Act enumeration. They do not establish grammatical
first and second subjects.

Likewise, the current source-position and adjacent-pair results preserve exact
order and lineage. That makes possible bounds addressable. It does not decide
which bound, if any, is relation content.

```text
source order preserved
!= source order ignored
!= grammatical role order established
```

The two adversarial witnesses require exactly this separation.

## 6. Historical testimony

### 6.1 Candidate chronology

The Candidate road first attached an unresolved represented-relation
coordinate to unary Candidates. Ordered-pair Candidates later inherited that
vacancy. Subsequent work exposed source references, Candidate occurrences,
Applicability, Participation, Yield, boundaries, and replay while retaining
the unresolved relation.

No historical Candidate-specific Responsibility assigned a third
relation-content occupant. The current runtime replacement renamed and
decompressed several coordinates, but retained the same substantive boundary:

```text
exact unary or binary source preservation
relation Unknown
```

### 6.2 The removed three-plus-six machine object

Commit `df75bc36` carried three coordinates:

```text
subject
Candidate
Participation relation
```

and six directed pair positions. Those coordinates were already supplied by
the machine grammar. The test did not derive grammatical roles from raw source
material, and its pairs established no relation.

The `role_distinctions` object was removed during the active grammar reorder.
It is testimony that an established three-coordinate basis can expose six
directed pair positions. It is not testimony that Candidate forms a
relation-Assertion basis.

### 6.3 Prior represented-relation investigation

The earlier Candidate represented-relation investigation reached the same
boundary under the prior rendering:

```text
Candidate(A, B)
├── exact source A
├── exact source B
└── represented relation: Unknown
```

It found no Candidate-specific owner that filled the coordinate. The current
active grammar is clearer: a future established relation is a separate
relation Assertion, not a rewrite of the preserved Candidate.

## 7. Exact owner audit

| Existing Responsibility | What it owns | Does it assign all three positions? |
|---|---|:---:|
| `01.Source.E.1` Candidate | unary or ordered-pair source preservation under Act-local roles | no |
| `01.Source.F` relation-Assertion preservation | source preservation after material already carries the Assertion | no |
| `01.Standing.E` relation Standing | later Standing after relation Assertion and responsible relation occurrence | no |
| `05.Recording.A` | recording an already-formed Assertion | no |
| generic Compare | relation finding concerning already-addressed exact subjects under an exact rule | no |
| declared Measurement | exact findings under its declared rule and bounded subject population | no current rule does this work |

The present owner of source-derived assignment to all three positions is:

```text
not established
```

## 8. First actual vacancy

The source road can now carry increasingly constrained exact bounds, source
positions, order, recurrence, internal Compare results, producing-bound
references, and corresponding-coordinate findings.

The destination positions already exist:

```text
first subject
exact relation content
second subject
```

The absent work is the exact Responsibility and Act that can establish a
bounded assignment of existing source-derived results to those positions while
preserving:

- every exact source bound and producing result reference;
- complex occupants where established;
- source order as evidence rather than a universal role rule;
- Authority, Scope, Locality, limits, conflicts, and Unknown;
- the distinction between assigned relation-Assertion material and a later
  responsible relation occurrence.

The assignment cannot be inferred from:

- infix position;
- recurrence by itself;
- literal spelling;
- adjacency;
- common support;
- Candidate source order;
- finite addressability;
- an observer's parse.

This is a real vacancy rather than an omitted Candidate adapter. Active
Candidate grammar does not declare the required three-position subject shape.

## 9. Smallest unbiased proving witnesses

### 9.1 Refusal witness available now

Use both raw values together:

```text
is '=' =
'=' is =
```

The present lawful expectation is:

```text
exact material, positions, order, and later bounded findings preserved
no first-subject / relation-content / second-subject assignment
```

This is the smallest useful witness for detecting infix, literal-role, and
source-order bias. It is not yet a positive role-recovery witness.

### 9.2 Positive preservation witness

Current witness grammar already carries relation declarations whose first
subject, relation, and second subject are explicitly authored coordinates. A
Source.F/Recording proof could preserve such an already-formed relation
Assertion and prove that the three roles, source, and Unknown remain exact.

That would prove preservation only. It would not prove discovery from raw
material.

### 9.3 Positive source-derived witness remains unavailable

A positive source-derived witness must let prior independently established
bounded work make all three roles addressable. Supplying the observer anatomy
for `is '=' =` would merely author the result being tested.

Until the missing Responsibility is recovered, the honest result for both raw
lines is refusal to assign roles.

## Disposition

```text
Candidate preserves exact neutral source references             established
Candidate source references may carry complex bounded results   established
Candidate source roles are relation-Assertion roles              not established
Candidate owns a relation-content source role                    not established
source order assigns grammatical role order                      not established
Source.F derives an Assertion from raw source material            not established
Standing.E forms relation-Assertion content                       not established
raw is '=' = has the observer's proposed anatomy                  not established
raw '=' is = has any fixed material-to-role mapping               not established
source-derived three-position assignment owner                    vacant
```

The current Candidate is a neutral carrier beside the vacancy. It is not the
owner of the vacancy.

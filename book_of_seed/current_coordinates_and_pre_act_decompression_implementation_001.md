# Current-coordinate and pre-Act decompression implementation 001

## Boundary

This pass applies the findings in
`standing_and_responsible_boundary_decompression_investigation_001.md` to the
constitutional surfaces only.

It changes:

```text
Book README and active chapters
Witness Grammar
Book admission
Rosetta translation
constitutional checks
```

It does not propagate the new vocabulary through the runtime. The final
section fixes that runtime divergence as the input to the next pass.

## 1. Current coordinates replace the Standing object

The active grammar no longer declares Standing as an object, branch
container, result, or carried coordinate.

`01.Current` now states the load-bearing physiology directly:

```text
exact subject
+ exact Locality
+ exact through-occurrence boundary
↓ bounded read
exact established coordinates current through that boundary
```

The bounded read establishes no additional coordinate, relation, Act
occurrence, or result.

The exact result of an Act occurrence becomes current for every exact subject
carried with that Act before its occurrence, through a boundary at or after
the result occurrence in the same Locality.

The empty case remains exact:

```text
This Seed first carries no current coordinates.
```

The former `Standing` chapter is now
`chapters/01_current_coordinates.md`. Clause coordinates change from
`01.Standing.*` to `01.Current.*`.

This removes the reified noun. It does not remove current-state physiology.
The exact Locality, recorded occurrences, through-occurrence boundary, and
bounded read remain constitutional.

## 2. Direct pre-Act coordinates replace the Responsibility object

The active grammar no longer declares Responsibility as an object, branch,
duty, owner, assignment, or universal coordinate.

`02.Acts.A` now states the pre-Act construction directly:

```text
exact subject
+ exact Act
+ exact rule where required
+ Scope
+ Locality
+ required relations

all exact before one exact Act occurrence
```

Applicability, Admission, Participation, the Act occurrence, Yield, result,
and bounded current-coordinate read remain separately exact.

Each family clause now carries its actual subjects, Act, rule, Scope,
Locality, boundaries, and relations. No replacement Assignment or Binding
object was added to Witness Grammar.

The active clauses now state clause-local conditions as current-coordinate
requirements. Examples include:

```text
exact byte-pair position Measurement result current
→ addressed byte occurrence Measurement coordinates are exact

earlier + later pair Measurement results current
→ exact Compare subjects, Act, and rule are exact together

exact Candidate result current
→ exact Candidate subject, Compare Act, and rule are exact together
```

This states constitution, not duty. The presence of exact pre-Act coordinates
does not establish Applicability, Participation, or occurrence.

## 3. `responsible boundary` leaves active grammar

The Book and Witness Grammar no longer require `responsible boundary` for an
Act, relation, Scope, Support, source road, movement, Compare, Measurement, or
emission.

No replacement boundary coordinate was added. The exact boundaries already
owned by the source, result, completeness, Locality, and through-occurrence
physiologies remain unchanged.

Rosetta records the current runtime fact narrowly:

```text
responsible_boundary
→ scalar equality copied through pre-Act / Act / Yield / result records
→ no exact boundary occurrence or relation addressed
```

That scalar is implementation cleanup material, not active grammar.

## 4. Witness Grammar now projects only active distinctions

The two former top-level surfaces are gone:

```text
standing
responsibility
```

Witness Grammar now has only:

```text
relations
book_coordinates
```

`01.Current.G` carries the exact empty first-current case directly. Every
clause coordinate carries its own subjects, Acts, rules, requirements,
relations, results, and current-coordinate conditions.

The generic relation surfaces no longer require Responsibility or
`responsible_boundary`. They retain exact subjects, exact relation occurrence,
Scope, Locality, exact Act where the Book requires it, and Unknown.

## 5. Rosetta owns the retired orientations

Rosetta now translates:

```text
Standing
→ bounded current-coordinate read for an exact subject

Responsibility
→ exact subject / Act / rule / Scope / Locality / relation coordinates
  exact before occurrence

Assignment
→ runtime witness word for recorded pre-Act coordinates

responsible boundary
→ unresolved runtime scalar equality thread
```

Rosetta also removes stale live references to deleted representation and
occurrence-wrapper roads. The Book imports none of these translation words.

Rosetta admission is reduced from 1,043 lines to the 568 words carried by its
current pages. Unused historical inflections and Book-only clause letters are
no longer retained as translation vocabulary.

## 6. Precise runtime cleanup frontier

The runtime is intentionally unchanged by this constitutional pass. A lexical
inventory at this commit gives the following frontier:

```text
Responsibility language             1,167 matching lines / 22 runtime files
responsible-boundary language         169 matching lines / 20 runtime files
Standing language                   2,220 matching lines / 23 runtime files
generated Assignment identities       308 matching lines / 16 runtime files
assignment-reference language         768 matching lines / 19 runtime files
retired 01.Standing clause strings      25 matching lines / 13 runtime,
                                              test, and script files
```

These counts are search addresses, not six mechanical replacement jobs.

### 6.1 Pre-Act occurrences and references

Real physiology to retain:

```text
recorded pre-Act occurrence identity
exact subject
exact Act
exact rule where required
Scope
Locality
boundaries
later Act occurrence lineage
```

Cleanup:

```text
*_responsibility_assignment_* event and function vocabulary
responsibility_assignment_occurrences projection key
responsibility_assignment_reference payload keys
Responsibility prose scalars and constants
generated assignment_identity / assignment_subject_identity
```

The reference itself must not be deleted merely because its old name says
Assignment. Where it addresses a real recorded pre-Act occurrence, retain that
exact occurrence reference and its subject/Act/rule/boundary coordinates.

Applicability and governed-Act pre-Act occurrences must remain separate. The
byte-pair road in `ed4848f8` is the live model; other roads must be checked
against their exact subjects and lineage before their generated identities are
removed.

### 6.2 Bounded current-coordinate reads

Real physiology to retain:

```text
Locality
through-event occurrence identity
append boundary
exact recorded occurrences through that boundary
coordinate maps produced by the bounded read
refusal of missing, crossed, reordered, corrupted, or differently localized
occurrences
```

Cleanup:

```text
operator_locality_standing module and API vocabulary
*_standing function parameters and transient keys
recorded Standing labels that actually address a through-occurrence boundary
standing_locality_continuation names
comments and tests that describe the bounded read as an object
```

Do not delete the bounded reader or flatten its Locality/boundary checks. This
is a vocabulary and durable-surface decompression, not removal of current-state
behavior.

Scalar fields such as:

```text
standing = applicable
standing = measured
standing = preserved
```

require their own subtraction. They may be stale status labels, but this pass
does not claim that from their spelling alone.

### 6.3 `responsible_boundary`

The current scalar is copied and equality-checked across many families. The
next pass must remove it only where exact subjects, Acts, relation occurrences,
Locality, Scope, and exact lineage already retain every distinction.

Do not rename it to `boundary`. No exact boundary occurrence is presently
carried by the scalar.

### 6.4 Clause coordinates

Runtime and executable witnesses still carry:

```text
01.Standing.A.1
01.Standing.D.1
01.Standing.E.1
```

Their active coordinates are now:

```text
01.Current.A.1
01.Current.D.1
01.Current.E.1
```

These are exact coordinate updates, not aliases. No compatibility map belongs
between the old and new Book.

### 6.5 Observer scripts and tests

Observer scripts that read top-level `grammar["standing"]`,
`grammar["responsibility"]`, Responsibility branches, or Standing entrances
now describe retired grammar. They should be rewritten from the corrected Book
or retained only as frozen historical observers.

Runtime tests that prove exact lineage remain useful. Tests whose claim is
only that old vocabulary exists should be removed rather than translated into
a new blacklist.

## Validation

```text
Book / Witness Grammar / Rosetta      41 passed
Book-material witness                  9 passed / 8 source-conditional skips
Book admission                        exact and closed
Rosetta admission                     exact and closed
active Book Responsibility hits       0
active Book Standing hits             0
active Book responsible hits          0
Witness Grammar retired hits          0
git diff --check                      passed
```

The runtime-Fidelity file now reports six failures. Four directly expose this
pass's intentional runtime divergence: retired clause coordinates and runtime
material words absent from corrected Book admission. Two expose exact runtime
sirens already present at this boundary: one reference supplying two named
coordinates, and yielded results lacking the exact Act-occurrence identity.
They remain part of the next runtime pass; this constitutional pass does not
silence them.

## Stop

The constitutional surfaces are repaired. The runtime deliberately remains a
contradicting witness whose exact cleanup frontier is fixed above.

No runtime propagation, compatibility vocabulary, generic Assignment object,
Standing object, boundary surrogate, scheduler, or new Act is added in this
pass.

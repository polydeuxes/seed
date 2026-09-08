# Assignment identity and subject identity decompression investigation 001

## Question

After separating Applicability from its governed Act, does either pre-Act
binding require these generated runtime coordinates?

```text
assignment_identity
assignment_subject_identity
```

Or is each binding addressed completely by:

```text
its recorded occurrence
exact subject coordinates
exact Act
exact rule where required
Scope
Locality
Book clause
Standing and result boundaries
later exact lineage
```

This investigation changes no Book or machine grammar. `Responsibility`
remains disputed vocabulary. `Assignment` remains a runtime witness word.

## Direct finding

Neither generated identity adds a distinct grammatical coordinate in the
current audited material.

```text
assignment_identity
    duplicates the durable address already supplied by
    recorded_occurrence_identity

assignment_subject_identity
    names no exact subject relation
    and never occurs as a subject in the audited material
```

The exact bindings remain distinguishable after removing both generated
coordinates:

```text
106 assignment-shaped records
  7 coordinate surfaces before subtraction
  7 coordinate surfaces after subtraction
  0 exact-record collisions after subtraction
```

The carried references also remain exact:

```text
690 reference instances
 67 distinct complete references
 67 distinct references after removing both generated identities
  0 newly merged reference forms
```

Thus neither pre-Act binding requires a separate Assignment identity or a
generated Assignment-subject identity at this boundary.

The real durable identity is the recorded occurrence identity. The real
subject is the exact subject material and subject-to-Act relation carried by
the binding.

This does not authorize repository-wide deletion yet. Current readers require
the two fields because the current serialized shape requires them. That is an
implementation dependency, not a missing grammatical distinction.

## 1. The two seam repairs

Commit `22b1c2d6` first repaired the two runtime discrepancies found by
`e48de8f1`.

### 1.1 Shared-position Applicability

The Applicability Act now consistently addresses:

```text
the exact shared-position Measurement Act
```

at all three carried locations:

```text
Applicability Act top-level addressed_act_identity
first input relation addressed_act_identity
second input relation addressed_act_identity
```

The Applicability result already addressed that same Measurement Act. No Act
or relation was added; the inconsistent top-level coordinate was corrected.

### 1.2 Byte-pair Applicability replay

The pair Applicability reader now reads the ledger occurrence address under:

```text
act_occurrence_event_identity
```

while retaining the constitutional Act-occurrence identity under:

```text
applicability_act_occurrence_identity
```

The public reader can now read a freshly recorded Applicability result,
revalidate its exact source Standing, and refuse a changed Yield result
identity.

Focused seam checks:

```text
7 passed in 5.60 seconds
```

## 2. Fresh material

The inward material was recorded again after the seam repair:

```text
source occurrence counts      231, 327, 359, 423
all occurrences               1,340
known loss                    none
recording wall time           0.449 seconds

artifact SHA-256
5fc27d7eb2941cec7293b5079a97c75e468923f8da67c547a0962bcfb2628a89
```

The repair changes one addressed Act scalar in the shared-position
Applicability Act and one reader coordinate name. It does not add, delete, or
rename either generated assignment identity.

## 3. What `assignment_identity` currently does

Current assignment recorders generate a fresh scalar such as:

```text
byte_position_pair_measurement_assignment_000001
shared_pair_position_assignment_identity_000001
recorded_pair_comparison_assignment_000001
```

The scalar is then:

```text
written into the assignment-shaped record
copied into responsibility_assignment_reference dictionaries
checked for type, presence, uniqueness, and equality
copied through later Act and result lineage
```

No audited reader uses that generated scalar to fetch the durable record.
Readers fetch through:

```text
responsibility_assignment_reference.recorded_occurrence_identity
```

The Standing maps likewise key assignment-shaped records by:

```text
the ledger event identity
```

not by `material["assignment_identity"]`.

Some local variables are named `assignment_identity`, but their value is read
from `recorded_occurrence_identity` and passed to `ledger.get()`. The variable
name compresses the distinction; the fetched address is still the event
occurrence identity.

Therefore the current exact lineage is:

```text
recorded pre-Act occurrence identity
-> later exact reference
-> Act occurrence
-> Yield
-> result
```

The extra assignment scalar echoes beside that lineage. It does not own it.

## 4. What `assignment_subject_identity` currently does

The generated subject scalar has an even narrower use.

Across the fresh 1,340-occurrence material, every scalar value generated as an
`assignment_subject_identity` appears only under the terminal coordinate:

```text
assignment_subject_identity
```

The exact count is:

```text
796 scalar appearances
796 under assignment_subject_identity
  0 under subject
  0 under first_subject
  0 under second_subject
  0 under role
  0 under a relation occurrence
```

The scalar is copied from record to reference and compared back to the same
record. No relation establishes:

```text
assignment_subject_identity
    represents
exact source subject
```

or:

```text
assignment_subject_identity
    is the subject of
exact Act
```

The actual subjects are already carried separately as source references,
Assertion references, position coordinates, path references, roles, and exact
subject-to-Act relations.

Thus the generated subject identity does not identify the binding's subject.
It identifies only itself.

## 5. Subtraction measurement

The measurement removed the two generated coordinates from every current
assignment reference while retaining:

```text
recorded_occurrence_identity
Book clause identity
result boundary identity
family-local reference coordinates
```

The result was:

```text
reference instances                              690
distinct complete references                      67
distinct references without assignment_identity   67
distinct references without subject identity       67
distinct references without either identity        67
newly merged complete reference forms                0
```

Removing one generated identity at a time also created zero merged forms.

The same subtraction was applied to the 106 assignment-shaped records while
retaining their recorded event identities outside the material dictionaries:

```text
assignment-shaped records                         106
exact material collisions after subtraction         0
coordinate surfaces after subtraction                7
```

This is a stronger result than field non-use alone. At this current boundary,
the two generated scalars add neither:

```text
record discrimination
reference discrimination
subject identity
ledger addressability
Standing-map addressability
```

## 6. Current refusal tests

Current readers refuse a changed or missing `assignment_identity` or
`assignment_subject_identity` because they reconstruct the complete authored
dictionary and compare it exactly.

Current tests also assert:

```text
generated identities are nonempty
generated identities differ from lifecycle identities
references repeat the generated values
changed generated values are refused
```

Those checks prove:

```text
the current serialized format requires exact repetition
```

They do not prove:

```text
either repeated scalar carries a distinction absent from the exact record,
subject coordinates, or occurrence lineage
```

This is the same cat-test boundary used for earlier prose wrappers: exact
reader enforcement can protect duplicated material.

## 7. Historical origin

The first active introduction found for both fields is commit `692ac344`,
`Record direct Standing Locality continuation`.

That implementation generated the two scalars together, wrote them into one
assignment dictionary, and copied them into later references. It did not
record:

```text
an Assignment Act
an assigning occurrence
an assigner
an assignee relation
a subject relation for assignment_subject_identity
```

Later roads copied the same storage shape.

The older Assignment investigation therefore correctly rejected Assignment
as a separate assigning event and separate Standing subject. The present
subtraction adds a narrower finding:

```text
even inside the runtime storage shape,
the generated Assignment identity and generated subject identity
add no distinct address or subject relation at the audited boundary
```

## 8. Smallest durable surfaces

The two lawful pre-Act bindings can be addressed without an Assignment object.

### Applicability binding

```text
recorded occurrence identity
Book clause
responsible boundary
exact subject/input reference
exact role
exact governed Act identity
Applicability Act identity
Applicability Act occurrence identity
Applicability result identity
Scope
Locality
Standing boundary
Unknown / conflicts where carried
```

### Governed-Act binding

```text
recorded occurrence identity
Book clause
responsible boundary
exact family-local subjects
exact governed Act identity
exact rule
governed Act occurrence identity
governed result identity
Scope
Locality
Standing boundary
required exact relations
Unknown / conflicts where carried
```

The first coordinate in each list is the durable address of the recorded
binding occurrence. It is not another Assignment identity.

The actual subject coordinates replace `assignment_subject_identity`. A
generated subject scalar cannot replace those coordinates because it carries
none of their material or relations.

The connection between the surfaces remains:

```text
Applicability result concerning exact governed Act position
-> exact applicable position required by Participation
-> governed Act occurrence
```

No assignment-to-assignment relation is needed.

## 9. Does the binding require a new noun?

The subtraction establishes the structure, not its final vocabulary.

Three readings remain:

```text
Responsibility
    carries unsupported duty and obligation pressure

Assignment
    accurately describes current runtime labels
    but may reify a binding that exact coordinates already express

direct binding grammar
    one exact subject is bound to one exact Act
    under its exact rule, Scope, Locality, and boundaries
```

The current material requires the exact binding. It does not require a
separate identity-bearing Assignment object above the binding.

Therefore the no-replacement possibility is now supported:

```text
the Book may need a binding relation
without needing Responsibility or Assignment as a constitutional object
```

This report does not amend the Book to choose that wording.

## 10. DNA/RNA pressure

Biochemical testimony remains compatible with direct binding grammar:

```text
exact participants
+ exact relations
+ exact local conditions
+ one exact reaction position
```

Nothing additional must exist as a duty-bearing or Assignment-bearing object
before eligibility, assembly, reaction occurrence, and consequence can remain
distinct.

This comparison does not name Seed's grammar. It only shows that removing the
extra noun need not remove the exact local structure.

## 11. Disposition

```text
recorded pre-Act occurrence identity as durable address        required
exact subject material / references                            required
exact subject-to-Act relation                                  required
exact Act identity                                             required
exact family-local rule where required                         required
Scope / Locality / boundaries                                  required
Applicability result to Participation connection               required

generated assignment_identity as another durable address       no distinct work found
generated assignment_subject_identity as an exact subject      no relation found
either generated scalar as a reference discriminator           no
either generated scalar as a record discriminator              no
either generated scalar as a Standing-map key                  no
current readers require both fields                            yes, by authored shape

Assignment as assigning event / assignee relation               unsupported
Assignment as required identity-bearing Book object             unsupported
direct exact subject-to-Act binding                              supported
final Book vocabulary                                           unresolved
```

## 12. Smallest next build

The smallest implementation test is one bounded two-Act road, not a
repository-wide schema deletion.

```text
record Applicability's pre-Act binding separately
record the governed-Act pre-Act binding separately
address each by its recorded occurrence identity
carry each exact subject and Act coordinates directly
retain Applicability result -> Participation -> governed occurrence
omit generated assignment_identity
omit generated assignment_subject_identity
```

The byte-position-pair road is the sharpest first discriminator because its
Applicability and Measurement branches already carry different subjects,
different Acts, different results, and different Responsibility prose.

That build must stop if any exact lineage or refusal becomes impossible
without either generated scalar. It must not add:

```text
replacement identity fields
Assignment object
Assignment wrapper
assignment-to-assignment relation
dispatcher
duty or execution promise
```

Book vocabulary should remain unchanged until that one-road subtraction shows
whether direct binding grammar is sufficient in live replay.

## 13. Validation

```text
focused seam checks                                      7 passed
shared-position and pair-Applicability focused files    60 passed
fresh inward recording                                  1,340 occurrences
known loss                                               none
git diff --check                                         passed
```

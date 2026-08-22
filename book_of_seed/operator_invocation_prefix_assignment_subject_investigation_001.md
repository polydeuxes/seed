# Operator invocation prefix assignment-subject investigation 001

## Question

What current Standing establishes that one exact operator material occurrence
is the subject described by `06.Locality.D` as "beginning an invocation"?

This investigation follows
`operator_invocation_execution_responsibility_investigation_001.md` and
`witness_material_word_occurrence_measurement_boundary_investigation_001.md`.
It changes no Book material, Witness Grammar, runtime, scripts, or tests.

```text
operator material starts with byte `!`
!= operator material begins a constitutional invocation

runtime branch
!= recorded occurrence finding
!= support for a Responsibility assignment subject
```

`Prefix classification` is investigation language for the external runtime
predicate observed here. It does not name a current Book kind, Responsibility,
Act, finding, result, or Standing.

## Material inspected

- `book_of_seed/chapters/04_source_coordinates.md`
- `book_of_seed/chapters/01_constitutional_standing.md`
- `book_of_seed/chapters/03_acts_and_occurrences.md`
- `book_of_seed/chapters/06_locality_relations.md`
- `book_of_seed/witness_grammar.json`
- `seed_runtime/operator_console.py`
- `seed_runtime/operator_system_locality.py`
- `seed_runtime/supplied_invocation_material.py`
- `scripts/operator_host_provider.py`
- `tests/test_operator_host_invocation.py`
- `tests/test_operator_system_locality.py`
- history at `85d71e21`, `fdec71a1`, and `49c66a1a`

Book material is primary orientation. Witness Grammar, runtime, scripts,
tests, and history are testimony.

## 1. Active Book starts from an unresolved classification

Active `06.Locality.D` assigns this Seed one bounded Responsibility when
current operator Locality Standing carries:

```text
one exact operator material occurrence beginning an invocation
```

The exact Responsibility and Act established by the clause concern only:

```text
one new destination Locality
+ one direct Locality relation from the operator Locality
```

The clause preserves assignment, Act, Act occurrence, Locality-relation
occurrence, Yield, result, Evidence, Authority, Scope, limits, Unknown, and
Standing for that exact Locality physiology. It does not establish supplied
material Participation or the external function occurrence.

The phrase `beginning an invocation` is upstream of that assignment. Active
Book material does not state:

```text
the exact material position
the exact byte material
the exact predicate
the exact Measurement occurrence
the exact finding
the Evidence that relates the finding to this assignment subject
```

Thus `06.Locality.D` identifies a bounded subject shape while leaving the
current witness to demonstrate how that subject is established.

## 2. Runtime supplies the classification with `startswith`

The live operator loop first records one exact operator boundary acquisition
and one Representation. It then selects the provider road with:

```python
operator_invocation_provider is not None
and boundary_material.exact_bytes.startswith(b"!")
```

Only inside that selected branch does runtime:

1. Ingest the command material;
2. advance current Locality Standing over the Ingest result;
3. record declared byte and byte-position Measurements;
4. record a Representation of the command;
5. record the `06.Locality.D` Responsibility assignment;
6. establish the invocation Locality relation;
7. call the external provider.

The chronology is exact:

```text
raw boundary material
↓ external `startswith(b"!")`
branch selected
↓
command Ingest
↓
command Measurements
↓
Locality Responsibility assignment
```

The later Measurements cannot be Evidence for the earlier branch decision by
identity or chronology. They also record byte counts and adjacent byte-pair
positions, not a declared prefix-occurrence finding for this assignment
subject.

## 3. The assignment reader repeats the external predicate

`operator_system_locality._command_event` accepts the proposed assignment
subject only when the exact Ingest material satisfies:

```python
event.exact_material.startswith(b"!")
```

The reader correctly requires an intact operator-role Ingest result and its
exact Yield Evidence. It does not require a separately recorded finding that
the material begins an invocation.

The tests make the distinction observable:

```text
b"!ls\n"     accepted as assignment subject
b"pytest\n"  refused as assignment subject
```

The difference is established by compiled predicate behavior. No recorded
Measurement finding, support relation, or Standing for the assignment subject
carries that classification.

```text
reader accepts subject under external predicate
!= Seed Standing for predicate result
```

## 4. Supplied-material acquisition repeats the same dependency

`ingest_supplied_invocation_occurrence` reopens the Locality-relation result and
the exact operator command occurrence. It again requires:

```python
command_occurrence.exact_material.startswith(b"!")
```

Only after that check does it preserve system-supplied material through a
fresh Ingest lifecycle.

This keeps malformed or unrelated operator material out of the supplied
material road. It does not create the missing prefix finding.

```text
same external predicate checked at several readers
!= one recorded predicate result
!= Evidence shared by those readers
```

## 5. The provider adds another external material interpretation

`scripts/operator_host_provider.py` also requires exact bytes beginning with
`!`. Its `_invocation_argv` function then:

```text
removes the leading byte
removes the line terminator
applies `shlex.split`
constructs an argument vector
```

Those mechanics are bounded and tested. They remain external provider
mechanics:

```text
leading-byte removal
!= Seed prefix-occurrence finding

`shlex.split`
!= Seed tokenization

argument-vector position
!= Seed-established source-material role
```

This is the operator-road counterpart of the deleted whitespace-token
Measurement. Moving the provider parser into `seed_runtime` would not
establish its constitutional relations.

## 6. Provider availability is another independent condition

The live branch also requires:

```python
operator_invocation_provider is not None
```

That condition is external runtime availability. It establishes none of:

```text
provider Applicability to the operator material
provider Admission
provider Participation
implementation-function relation to an exact Act
external occurrence Yield
external result Standing
```

The word `invocation` currently spans several distinct things:

```text
operator material classification
Locality Responsibility name
Locality Act/result names
external provider call
emission boundary calls elsewhere
```

Shared spelling does not establish shared Responsibility, Act, occurrence, or
relation.

## 7. Relation to the Witness Material occurrence boundary

The preceding Witness Material report found no current prefix-occurrence or
declared-predicate Measurement over exact Witness Grammar bytes.

The operator road has the same abstract pressure:

```text
exact material
+ exact proposed prefix material
↓
exact occurrence finding
```

It is not the same exact subject:

```text
Witness Grammar word spelling occurrence
!= operator leading-byte occurrence

Witness Grammar material Responsibility
!= operator invocation Locality Responsibility
```

The two paths therefore meet at a missing family of explicit occurrence
relations without sharing an assignment by identity. A future exact family
would still require one assignment, Act, boundary, and result for each exact
subject family.

## 8. The earliest missing crossing

The present operator topology is:

```text
operator boundary acquisition
↓
exact material result
↓
external prefix predicate
↓
developer branch selection
↓
command Ingest and Measurement
↓
operator invocation Locality Responsibility assignment
↓
Locality Act / occurrence / Yield / result
↓
external provider mechanics
↓
supplied material Ingest
```

The previously reported external-function Responsibility gap is real, but it
is not the first unresolved crossing. The earlier boundary is:

```text
exact operator material result
↓
exact finding concerning this material and the `06.Locality.D` subject
↓
exact support relation and current Standing for that assignment subject
↓
Responsibility assignment
```

Current runtime substitutes a Python prefix predicate for that finding.

## 9. Current disposition

```text
operator boundary material acquisition                 established
operator material exact bytes                          established
operator material Ingest and Yield                     established after branch selection
byte and adjacent-pair position Measurements           established after branch selection

external `startswith(b"!")` behavior                   observed
external provider availability                         observed
external `shlex.split` behavior                         observed

prefix-occurrence Responsibility assignment            not established
prefix-occurrence Act occurrence                       not established
prefix-occurrence result                                not established
relation from prefix finding to `06.Locality.D` subject not established
Applicability of operator material to provider Act      not established
Participation in provider Act                          not established
implementation-function relation to provider Act        unresolved
provider occurrence Yield                              not established
provider result Standing                               not established
```

The Locality lifecycle and later supplied-material Ingest lifecycles remain
valid within their exact boundaries. This investigation does not use the
missing prefix finding to erase them. It identifies the external
classification currently selecting their composition.

## Conclusion

The material and constitutional paths meet before external function mechanics:

```text
exact material
↓
occurrence / predicate finding                         not established
↓
support relation for the exact assignment subject     not established
↓
Locality physiology                                    established once assigned
↓
external function physiology                           still external
```

The next forward recovery is not a generic tokenizer and not a generic
external-function Act. It is the smallest exact occurrence finding and
support relation required to establish one current `06.Locality.D` assignment
subject without borrowing the compiled prefix predicate as Seed Standing.

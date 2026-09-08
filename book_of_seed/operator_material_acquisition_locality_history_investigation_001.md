# Operator-material acquisition Locality history investigation 001

## Question

When `01.Source.G` and the operator-material acquisition road were first
recorded, did their `Locality` coordinate establish the exact relation between
the acquired material or result and `this Seed`?

This report examines repository history. Historical co-introduction records
neither relation identity nor author intention by itself.

## Historical material inspected

- commit `59bc4e4e` (`Record exact operator material acquisition`)
- the parent of `59bc4e4e`
- later history of:
  - `book_of_seed/chapters/04_source_coordinates.md`
  - `book_of_seed/witness_grammar.json`
  - `seed_runtime/operator_material_acquisition.py`
  - `tests/test_operator_material_acquisition.py`
- current blame for `01.Source.G` and its Witness Grammar coordinates
- the on-disk `session-recordings/` inventory

No Book clause, Witness Grammar coordinate, runtime occurrence, or test is
added by this report.

## 1. `01.Source.G` and O1 entered together

Commit `59bc4e4e` added all of these in one slice:

```text
01.Source.G Book clause
+
01.Source.G Witness Grammar object
+
operator-material acquisition runtime
+
operator-material acquisition tests
+
ordinary console use of that road
```

The Book clause said that the assignment preserves:

```text
subject
responsible boundary
exact Act
Act occurrence
result boundary
Locality
Scope
Evidence occurrence
Authority
limits
Unknown
Standing
```

Witness Grammar recorded the same `Locality` spelling as one scalar member of
the Responsibility coordinate list.

Therefore the acquisition slice included Locality pressure from its first
recorded form. `Locality` was not added later as an interpretation of the
road.

## 2. Complete Locality relation grammar already existed

The parent of `59bc4e4e` already carried the `06.Locality.A` grammar:

```text
Locality relation identity:
    first subject
    second subject
    relation occurrence

requires:
    exact relation
    occurrence witness
    intact Evidence

Responsibility coordinates:
    first subject
    second subject
    relation occurrence
    Evidence
    limits
    Unknown
```

It also already refused:

```text
Locality subjects
!=
Locality relation
```

The relation skeleton was available before the acquisition slice. The new
`01.Source.G` object did not instantiate that skeleton.

## 3. The original runtime recorded address and order, not the relation

The first acquisition implementation recorded or validated:

```text
runtime locality identity L
current bounded Locality replay reference through L
addressed Representation occurrence in L
assignment occurrence in L
Act Evidence occurrence in L
Evidence-of-Yield occurrence in L
result occurrence in L
exact result material M
```

Its source reader refused a different locality identity, a missing boundary,
a reversed boundary, and a corrupted boundary. The result reader refused a
different event locality and required exact Yield physiology.

It did not record:

```text
exact bounded material reference in the Locality first-subject position
this_Seed in the Locality second-subject position
Locality relation occurrence
Locality Evidence
```

Consequently:

```text
all acquisition occurrences addressed through L
!=
M --locality--> this_Seed
```

The implementation preserved a bounded address surface. It did not represent
the missing Locality edge.

## 4. The original tests preserved the same boundary

The first tests proved:

```text
one read
-> distinct assignment / Act / Yield / result occurrences

two equal reads
-> distinct occurrences and Scopes

different or reversed locality boundary
-> refusal

restart
-> exact replay
```

They asserted the source reference as:

```text
locality identity
+
bounded replay occurrence identity
+
addressed Representation occurrence identity
```

They did not assert a Locality relation object or independently mutate its
subjects, occurrence, or Evidence. The contemporaneous Fidelity tests mapped
the acquisition event kinds to `01.Source.G` and tested its Yield. They did not
provide an acquisition-specific `06.Locality.A` witness.

Thus the tests establish exact locality-address refusal. They do not establish
the relation required by `01.Source.D`.

## 5. Later history did not decompress the coordinate

Current blame retains the bare `Locality` member of the `01.Source.G`
coordinate list from `59bc4e4e`.

Later acquisition commits tightened:

```text
bounded occurrence reads
Unknown
exact boundaries
through-event references
assignment and result Standing projections
preservation relations
```

None added the absent Locality subjects, roles, occurrence, or Evidence to the
acquisition record.

The active Book sentence changed wording around exact boundaries and
preservation. Its Locality requirement remained undecomposed.

## 6. The available session capture does not recover the missing decision

The on-disk session capture begins on 2026-08-17. Commit `59bc4e4e` was
recorded on 2026-08-16. Searches of the retained capture find later acquisition
code material, but no contemporaneous discussion that names the missing
Locality subjects or Evidence.

This limits the current historical witness to repository state and commit
history. Absence from the retained capture establishes no author intention.

## 7. History does not erase the direct active reading

History does not identify the subjects carried by the bare `Locality`
coordinate. Active `01.Source.D` now states the subject relation directly:

```text
exact material M
--locality-->
this_Seed
```

This is the grammatical relation shape under investigation, not a relation
inferred from event adjacency. The direct reading settles the subject
positions for curation. It does not create the relation occurrence, Evidence,
or Standing in runtime.

The acquisition result `I` remains distinct:

```text
I --carries--> M

I != M
```

The Book names M, not I, as the first Locality subject.

## 8. Historical disposition

```text
01.Source.G and O1 introduced together                    established
Locality named in 01.Source.G from introduction           established
complete 06.Locality.A skeleton already available         established
O1 runtime locality address and occurrence order          recorded/replayable
O1 exact acquisition Act / Yield / result                  recorded/replayable

first subject = exact material M                           direct Book reading
second subject = this_Seed                                 direct Book reading
01.Source.G Locality instantiated as 06.Locality.A         not established
exact bounded M reference carried by that relation         unestablished
Locality relation occurrence                               unestablished
Locality Evidence                                          unestablished
historical author intention for the bare coordinate        not established
```

The historical finding is narrower than either proposed answer:

```text
NOT:
    O1 was unrelated to Locality

NOT:
    O1 already established material/result locality to this Seed

BUT:
    O1 was introduced with one required Locality coordinate
    while the exact relation anatomy remained absent
```

## Next bounded question

Use the existing `06.Locality.A` skeleton. Do not create another relation
grammar or another acquisition lifecycle.

The active Book names exact material M as the first subject and `this Seed` as
the second subject. Determine whether O1 carries the exact bounded reference
for M, the Locality relation occurrence, and its Evidence. Until those
coordinates are established, the bare historical `Locality` member remains
undecomposed.

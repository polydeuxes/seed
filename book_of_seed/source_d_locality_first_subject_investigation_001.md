# 01.Source.D Locality first-subject investigation 001

## Amendment boundary

The earlier title and filename compressed `exact material` and `exact Ingest
result` into one slash-subject. This amendment removes that compression. It
does not select either coordinate as the first subject of the unresolved
Locality relation.

## Question

What is the exact first subject of the Locality relation required before
`01.Source.D` says this Seed bears one declared Measurement Responsibility
over exact material?

The exact pressure is:

```text
exact Ingest result I
--carries--> exact material M

I != M

exact first subject X
+ exact Locality Evidence relating X to this Seed
+ one Seed-native declared Measurement
↓
this Seed bears the Measurement Responsibility
```

Whether `X` is `M`, `I`, or another exact bounded subject is unresolved. The
active prose names exact material. Current Witness Grammar and runtime
occurrences do not recover the exact first-subject coordinate of that relation.

This investigation does not ask whether an Ingest event and a Measurement
event share one runtime locality label. Active `06.Locality.A` refuses that
substitution.

`I carries M`, `Locality Evidence`, `related to this Seed`, and `bears the
Measurement Responsibility` remain distinct coordinates. This report
establishes no identity among them.

## Active material inspected

- `01.Source.D` in
  `book_of_seed/chapters/04_source_coordinates.md`
- `06.Locality.A` through `06.Locality.D` in
  `book_of_seed/chapters/06_locality_relations.md`
- the Ingest lifecycle in `seed_runtime/material_ingest.py`
- bounded Locality replay in `seed_runtime/operator_locality_standing.py`
- Assertion movement Locality in `seed_runtime/byte_measurement.py`
- Representation and emission Locality in
  `seed_runtime/operator_representation.py`
- Standing Locality continuation in
  `seed_runtime/operator_standing_continuation.py`
- recorded Standing-boundary Locality in
  `seed_runtime/standing_boundary_locality.py`
- operator invocation Locality in
  `seed_runtime/operator_system_locality.py`
- the position-coordinate Measurement family in
  `seed_runtime/measurement_of_position_coordinates_of_byte_pair_occurrences.py`
- the host declaration loop in
  `seed_runtime/standing_measurement_declarations.py`

No Book clause, Witness Grammar coordinate, or runtime occurrence is added by
this report.

## 1. The exact Ingest lifecycle is intact but carries another relation family

`ingest_material()` records:

```text
Ingest Act Evidence
↓
Evidence of Yield relation
↓
exact Ingest result occurrence
```

The result preserves exact coordinates including:

```text
result identity
Ingest Act identity
Act-occurrence identity
source role
source boundary
known loss
Unknown
provenance occurrence references
responsible Act Evidence reference
Evidence-of-Yield relation reference
exact bytes
runtime locality identity
```

`read_exact_ingest_result()` validates the exact occurrence, integrity, bytes,
Act Evidence, Evidence of Yield, and result.

That establishes strong source-result testimony. It does not record:

```text
locality_relation_occurrence_identity
locality_evidence_identity
locality_relation:
    first exact bounded subject
    relation = locality
    second exact bounded subject
```

The Ingest Act Evidence and Evidence of Yield support the Ingest occurrence and
its result. They are not Locality Evidence by identity.

Disposition:

```text
exact Ingest Act/Yield/result physiology          recorded and replayable
exact material carried by exact Ingest result     recorded and replayable
first subject of required Locality relation       not recorded there
exact required Locality relation to this Seed     not recorded there
```

## 2. A runtime locality label is not Locality Evidence

Every Event carries `locality_identity` as a storage and replay boundary. The
Ingest result also carries a `dimensions.scope_locality` string derived from
that label.

Those coordinates support exact bounded replay:

```text
event belongs to runtime locality label L
event is replayed only in L
event is read through exact boundary B
```

Active `06.Locality.A` separately refuses Locality by:

```text
subject identity
co-presence
chronology
shared label
```

Therefore:

```text
source.locality_identity == L
!=
exact evidenced Locality relation
```

and:

```text
dimensions.scope_locality == "locality:L"
!=
Locality relation occurrence
```

Disposition: exact runtime addressability, no Locality relation by identity.

## 3. Bounded Locality replay does not add the relation

`read_operator_locality_standing_through()` reconstructs a validated Locality
accumulator through one exact occurrence. The accumulator contains exact
Ingest, assignment, Measurement, Compare, Candidate, Representation, and
recorded Locality-relation occurrences that the replay encounters.

The replay operation does not create a missing occurrence. An Ingest event
entering the accumulator because it carries locality label `L` does not thereby
acquire Locality Evidence.

The names `read_operator_locality_standing*` remain historical runtime names.
The current Standing investigation already establishes:

```text
bounded Locality replay
!= positive constitutional Standing
```

The same refusal applies here:

```text
bounded Locality replay contains exact Ingest result I
+ I carries exact material M
!= first subject of the required Locality relation established
!= exact required Locality relation to this Seed
```

Disposition: precise replay testimony, not the missing relation occurrence.

## 4. Existing concrete Locality roads have different exact subjects

The repository records several exact Locality relation families. None
establishes which exact subject occupies the first position required by this
investigation.

### 4.1 Assertion movement

Assertion movement preserves one exact Assertion and establishes one new
Locality relation to a destination Locality under its movement Responsibility,
Act, Evidence, Authority, Scope, limits, and occurrence.

Its subjects are the moved Assertion and destination Locality. An Ingest result
has not undergone that movement by identity.

### 4.2 Representation and emission

Representation and emission record distinct locality-evidence occurrences for
their exact addressed material, Acts, attempts, results, and destinations.

Those relations do not retroactively establish `I`, `M`, or another subject as
the first subject of the Locality relation required by `01.Source.D`.

### 4.3 Standing Locality continuation

Standing Locality continuation preserves an exact prior Locality Standing
boundary addressed by one Representation as available at one new Locality.

Its source subject is the addressed prior boundary. It is not every Ingest
result already carrying the destination label.

### 4.4 Recorded Standing-boundary Locality

This family establishes one direct relation from one exact recorded Standing
boundary result to one new Locality. It preserves that exact result reference
and no other reference.

### 4.5 Operator invocation Locality

This family establishes a new Locality and one direct relation from the
operator Locality to it for one exact operator material occurrence beginning an
invocation.

Its relation does not establish that supplied material, an Ingest result
carrying that material, or another exact bounded subject is related to this
Seed by the relation required in `01.Source.D`.

Disposition for all five roads:

```text
exact Locality relation physiology exists         yes
required first subject                             not supplied by identity
required 01.Source.D Locality relation             not supplied by identity
```

## 5. The family-local source read is therefore below assignment physiology

Commit `3f911062` introduced a family-local composite whose original names
included:

```text
PositionCoordinateMeasurementAssignmentSubjectReading
...subjects_from_standing
standing_through_event_occurrence_identity
standing_append_boundary_identity
```

Those names compressed two unestablished claims:

```text
bounded Locality replay = constitutional Standing
exact Ingest source = exact Measurement-assignment subject
```

Commit `0d8beb93` demotes the representation to:

```text
UnassignedPositionCoordinateMeasurementIngestReading

bounded Locality replay
↓
exact Ingest coordinates
+ no assignment/result for this family through B
```

The returned material explicitly establishes neither:

```text
Locality relation
assignment-subject relation
Responsibility assignment
Applicability
Act
Standing
```

The append-boundary token is retained only as replay addressability. It is not
named as a Standing coordinate.

Disposition: useful exact runtime projection, not recovered assignment
physiology.

## 6. Recorder membership is a runtime refusal, not the missing edge

The position-coordinate assignment recorder re-reads the family-local source
surface and refuses a requested source when it is:

```text
absent from bounded replay
missing exact Ingest Act/Yield/result coordinates
already assigned through B
already resulted through B
```

This protects exact negative boundaries. In particular:

```text
Python calls recorder twice for source S
↓
second call refuses and appends nothing
```

The membership test does not establish:

```text
exact first subject X --locality--> this Seed
exact assignment subject --subject_of--> Responsibility R
assignment Evidence
assignment Standing
```

The host still supplies the positive transition from the returned source
identity to the assignment recorder. The code now labels that transition as a
runtime refusal boundary rather than recovered constitutional assignment
physiology.

Disposition: omission and duplicate protection retained; positive relation
unestablished.

## 7. Source Evidence is not assignment Evidence

The composite Ingest-result read carries:

```text
responsible Ingest Act Evidence identity
Ingest Evidence-of-Yield relation identity
```

Those exact references establish `I` as an intact Ingest result carrying `M`.
They establish neither `I` nor `M` as the first subject of the required
Locality relation.

They do not establish:

```text
Evidence for Measurement Responsibility assignment
Standing occurrence for that assignment
Standing-occurrence Evidence
positive assignment Standing
```

Putting both coordinate families in one Python return object would not join
them. The current return object carries only the source family.

Disposition: exact Ingest Evidence intact; Locality first subject unresolved;
assignment Evidence absent.

## 8. Exact current boundary B remains useful and distinct

The family-local read is frozen through one exact occurrence and its resolved
append prefix:

```text
B occurrence address
↓
B append-prefix identity
↓
bounded Locality replay
```

A later assignment does not alter an earlier read through B. Reading through
the later assignment excludes that source from the later unassigned-source
surface.

This proves:

```text
absence of assignment/result through B
```

It does not prove:

```text
Locality relation through B
assignment-subject relation through B
assignment Standing through B
```

The source completeness boundary remains independently tied to the exact
Ingest result. It is not replaced by the later replay boundary.

Disposition: B is an exact immutable replay boundary, not the missing
constitutional edge.

## 9. Elimination matrix

| Candidate source of required Locality Evidence | Exact current status |
|---|---|
| Event `locality_identity` | shared runtime label only |
| `dimensions.scope_locality` | represented scope label only |
| Ingest responsible Act Evidence | Evidence for Ingest Act occurrence |
| Ingest Evidence of Yield | relation from Ingest occurrence to result `I` |
| `I` carries exact material `M` | exact carried-material relation, not the required Locality relation |
| presence in bounded Locality replay | validated co-presence through B |
| Assertion movement Locality | exact different subject family |
| Representation/emission Locality | exact different subject family |
| Standing continuation Locality | exact different subject family |
| recorded-boundary Locality | exact different subject family |
| operator invocation Locality | exact different subject family |
| family-local Python function identity | host orientation only |
| membership in unassigned-source projection | runtime refusal boundary only |

No inspected coordinate establishes the required first subject or supplies the
required relation.

## 10. Current exact topology

```text
exact Ingest Act occurrence
↓
Evidence of Yield
↓
exact Ingest result I
↓ carries
exact material M
↓
bounded Locality replay through B
↓
exact unassigned-source read

────────────────────────────────────────

first subject of required Locality relation   unresolved
exact Locality relation to this Seed          unestablished
Locality-relation occurrence                  unestablished
Locality Evidence                             unestablished
exact assignment-subject relation             unestablished
assignment Evidence                           unestablished
positive assignment Standing                  unestablished
```

The runtime can still record and replay the later assignment lifecycle. That
chain remains implementation testimony until the missing positive coordinates
are recovered.

## 11. Next bounded question

The next investigation belongs before assignment Standing:

```text
What is the exact first subject of the Locality relation
required by 01.Source.D?

Is it the exact material M,
the Ingest result I carrying M,
or another exact bounded subject?

Current Standing: unresolved.
```

The answer is not supplied by choosing an existing Locality family whose
subjects differ. It is also not supplied by adding a `locality_evidence_id`
field to Ingest material without the corresponding Responsibility, Act,
occurrence, Evidence, Authority, Scope, limits, Unknown, and exact relation
subjects.

Whether the Ingest Act also participates in such a relation-producing road, or
whether another exact Responsibility owns it, remains unresolved.

## Disposition

```text
exact Ingest occurrence/result physiology              recorded/replayable
exact result `I` carries exact material `M`             recorded/replayable
exact frozen read through B                            recorded/replayable
family-local unassigned-source projection              implemented testimony
duplicate/malformed source refusal                     implemented testimony

event locality label = Locality relation               refused
bounded replay = positive Standing                     refused
Ingest Evidence = Locality or assignment Evidence      refused
result-reference membership = assignment-subject relation refused
existing different Locality road reused by identity    refused

first subject of required Locality relation             unresolved
required 01.Source.D Locality relation                  unestablished
relation occurrence / Evidence                         unestablished
assignment-subject relation                            unestablished
positive assignment Standing                           unestablished
```

The family-local decomposition remains useful. It has reduced the first spring
transition to an exact missing Locality relation and a separately missing
assignment-subject relation without inventing either one.

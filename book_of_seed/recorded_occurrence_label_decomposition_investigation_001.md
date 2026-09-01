# Recorded occurrence label decomposition investigation 001

## Boundary

This investigation asks whether the durable runtime coordinate named `kind`
carries a Seed distinction or duplicates exact coordinates already carried by
the occurrence.

No Book clause admits `kind`. The active Rosetta also says that a name, label,
or `kind` supplies none of the subject, relation, Act, occurrence, or Standing
it suggests. Runtime use therefore counts as implementation testimony only.

No Book, machine grammar, runtime reader, or durable schema is changed here.

## Operations

### Current process material

`scripts/record_inward_occurrence_material.py` recorded four fresh Localities
from these opaque input boundaries:

```text
8 bytes
11 bytes
12 bytes
14 bytes
```

The four recordings completed in `0.427s` and carried 1,340 occurrences.

```text
occurrence material artifact
sha256 854e74b7eb501635a5d3f8c88522d71490d4ec0c2ef7f2352ae959df69961fb7

label-blind coordinate surface artifact
sha256 159f2e0a91d5a59037e2ba38a5e47003c73e4a3040c7a0edfbce7129d6fba02e
```

The surface operation read top-level coordinate names, immediate value types,
and container member counts. It did not read event labels or scalar values.

Only after the surfaces were fixed were their occupants compared with the
withheld event labels.

```text
event labels                         32
exact coordinate surfaces           33
surfaces carrying two labels         0
```

One label carries two exact surfaces:

```text
operator.material.acquire_responsibility_assignment_recorded
```

The distinguishing coordinate is exact and already carried:

```text
first acquisition in a fresh Locality:
standing_boundary_occurrence_reference = absent

later acquisition:
standing_boundary_occurrence_reference = exact address
```

The label hides this distinction; it does not supply it.

### Every statically resolved live append

The active Fidelity walk resolves every runtime `ledger.append(...)` and
`Event(...)` material expression or raises its siren. Its complete current
surface gives:

```text
persisted labels                     80
top-level coordinate surfaces        65
surfaces carrying two labels          3
```

Sixty-two labels are distinguished by their top-level coordinate names alone.
That is sufficient to distinguish the recorded surfaces. It does not establish
that each distinguishing coordinate is Seed grammar. A constant family field,
schema identity, or another label encoded as a coordinate name could produce
the same result. Those sixty-two surfaces remain to be audited coordinate by
coordinate before repository-wide removal of `Event.kind` is warranted.
The remaining eighteen labels occupy three common surfaces, all in
`source_position_recurrence.py`:

```text
six Responsibility occurrences      one 15-coordinate surface
six Act occurrences                  one  9-coordinate surface
six result occurrences               one  9-coordinate surface
```

This accounts exactly for all 80 labels:

```text
62 distinct surfaces
+ 3 shared surfaces
= 65 surfaces
```

### Exact coordinates inside the three collisions

`scripts/record_pytest_occurrence_material.py` recorded the occurrences made
while the exact source-position witness checks ran.

```text
12 pytest checks passed in 1.90s
recorded occurrences 2,204
artifact sha256 89fd1aef5b9bbb20d713e845f2e38f9ec43a428448170523316e725cfbd89078
```

The top-level surfaces were fixed before their labels were inspected. The
exact coordinates inside each collision then gave this result:

| Shared surface | Exact discriminator already carried |
|---|---|
| six Responsibility occurrences | `exact_act`; separately, `rule` |
| six Act occurrences | `act` |
| six result occurrences | exact `act_occurrence_event_identity` leading to the exact Act occurrence and its `act` |

Every Responsibility occurrence carries one of six exact `exact_act` values
and one of six exact rules. Either coordinate distinguishes the six without
the label.

Every Act occurrence carries one of the same six exact Act values. The `act`
coordinate distinguishes the six without the label.

The result occurrence does not duplicate the Act text. It carries the exact
Act occurrence address instead. All 521 recorded result occurrences resolved
that address intact:

```text
result occurrences checked                  521
missing or crossed Act addresses               0
distinct exact result-to-Act relations          6
```

The six resolved Acts are:

```text
Applicability of exact source-position coordinates to Compare
Compare exact material at two exact source positions
Measure the complete Compare result
Measure recurrence of complete internal Compare results
Measure corresponding carried material across exact recurrence support results
Measure exact material shared by every exact recurrent result
```

Thus the result distinction is relational rather than a missing scalar. The
exact result says which exact Act occurrence yielded it; the Act occurrence
says which exact Act occurred.

## Finding

The audited distinction is real:

```text
this exact occurrence belongs to this exact physiological position
and not another
```

The persisted `kind` coordinate does not own that distinction.

```text
Responsibility occurrence
    exact Responsibility
    exact Act
    exact rule
    exact subject
    exact boundaries

Act occurrence
    exact Responsibility address
    exact Act
    exact subject coordinates

result occurrence
    exact Act occurrence address
    exact Yield
    exact result
```

These exact coordinates and relations distinguish every occurrence in the
current process material and every occurrence in the three deeply audited
source-position collisions. The runtime label duplicates their answer within
that bounded material.

The bounded disposition is therefore:

```text
constitutional Kind                         refused
missing source-position distinction         not found
durable top-level Event.kind                 redundant in the audited current occurrences
exact source-position coordinates/lineage   sufficient
sixty-two unique static surfaces            discriminator ownership Unknown
```

This finding concerns durable top-level `Event.kind`. It does not decide every
other runtime coordinate or identifier containing the word `kind`.

Three separate questions remain open:

```text
subject_kind: "assertion"
result_kind carried by Yield
occurrence_boundary carried by Yield
```

`subject_kind` may duplicate exact Assertion coordinates. `result_kind` may
duplicate the complete exact result and its Act/Yield lineage.
`occurrence_boundary` may be an exact boundary or another family label. None
of those conclusions follows from this investigation; each requires its own
decomposition and refusal operation.

## Why immediate deletion is not one small edit

The redundant label currently performs eight implementation jobs:

```text
Event carries it as a fixed top-level field
occurrence material identity hashes it
append-prefix identity hashes it
SQLite stores it as NOT NULL
SQLite indexes Locality + label
iter_locality_kind reads by it
runtime readers dispatch and refuse by it
Fidelity maps it back to Book clauses
```

Current runtime source contains 363 direct label references and 36
`iter_locality_kind(...)` calls across fourteen modules. SQLite can return
identities for one label without decoding stored occurrence material. Removing
the column while retaining the same queries would force material reads unless
the actual exact coordinates receive an equally exact storage path.

That cost is real. It does not make `kind` Seed grammar.

## Smallest next build

Begin with the collision that most strongly appears to require the label:
`source_position_recurrence.py`.

Replace its internal label dispatch with the exact distinctions already
carried:

```text
Responsibility read
    exact_act + rule + exact subject and boundaries

Act read
    act + exact Responsibility address

result read
    exact Act occurrence address
    -> exact Act occurrence
    -> act
```

The three top-level coordinate surfaces already distinguish Responsibility,
Act, and result. The exact Act lineage distinguishes the six roads within each
surface.

Do not replace `kind` with:

```text
form
type
species
category
result kind
occurrence kind
```

Do not run every reader until one accepts. Resolve the exact coordinates and
relations directly.

After that bounded road no longer reads its label, measure its SQLite cost.
That measurement should determine the smallest exact coordinate index needed
before broader durable-label removal is considered. Separately audit the
smallest discriminator on each of the sixty-two unique surfaces. Any index
must index actual carried coordinates; it must not be another concealed
occurrence category.

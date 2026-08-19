# Declared Measurement exact subject and order investigation 001

## Question

The bounded Measurement loop currently places two declared Measurements in one
host tuple and asks each entry for one value named `subject`:

```text
position-coordinate Measurement
↓
one exact material-acquisition result occurrence

exact-byte Measurement
↓
one exact material-acquisition result set
```

Before this investigation, the first road returned its exact occurrence
identity.  The second road returned only the last occurrence identity in its
set, then ignored that value while recording the complete set.

This report asks:

```text
Does one common scalar subject preserve both declared Measurements?

Does the numeric host order merely serialize independent writes,
or does it change exact carried boundaries?
```

This report changes no Book clause or Witness Grammar coordinate.  The
accompanying runtime correction only makes each already-recorded Measurement
road carry and validate its actual exact subject.  It establishes no
Responsibility assignment, positive Standing, or internal declaration order.

## Active sources inspected

- `01.Source.D`
- `standing_emission_declarations` and `declared_measurements` in Witness
  Grammar
- `seed_runtime/standing_measurement_declarations.py`
- the two exact Measurement implementations
- bounded Locality replay and carried-Standing tests
- the history that introduced the declaration tuple and numeric order

## 1. The common scalar subject was false

The position-coordinate Measurement has this exact subject:

```text
one exact material-acquisition result occurrence
```

Its discovery result is consumed directly by its assignment and Measurement
Act.

The exact-byte Measurement has a different subject:

```text
the complete ordered set of exact material-acquisition result occurrences
through the current boundary
```

Before this correction its discovery function returned:

```python
current_sources[-1]
```

The recording function accepted that scalar as `_subject_identity` and never
read it.  It independently reconstructed the full current source set.

Therefore:

```text
last exact source occurrence
!= complete exact source set

unused scheduler token
!= Measurement subject
```

The correction gives the two roads distinct exact runtime subjects:

```text
PositionCoordinateMeasurementSubject
    one exact acquisition-result occurrence identity

ExactByteOccurrenceMeasurementSubject
    every exact acquisition-result occurrence identity in order
```

Each recorder now refuses the other subject shape.  The exact-byte recorder
also refuses an omitted, added, reordered, or stale acquisition-result
population before appending anything.

These objects are runtime return shapes.  Their names establish no new Book
kind, relation, occurrence, Evidence, Scope, Authority, or Standing.

## 2. The two Measurements do not determine each other's findings

Both roads read exact material-acquisition results.  Neither road uses the
other road's assignment, Act, Yield, or result to determine its own measured
material:

```text
acquisition-result occurrence A
↓
position-coordinate Measurement of A

acquisition-result set (A, B, ...)
↓
exact-byte Measurement of (A, B, ...)
```

Recording the position-coordinate result adds no acquisition-result
occurrence.  Recording the exact-byte result adds no acquisition-result
occurrence.  Their material subjects therefore remain stable across either
Measurement lifecycle.

This does not by itself establish either a dependency or a shared responsible
boundary for their exact occurrences.

## 3. Current serial order changes the exact carried boundary

The current `01.Source.D` text requires current Standing to carry each recorded
occurrence before another declared Responsibility assignment is recorded.  The
runtime follows that text and both assignment records preserve the moving
prior boundary.

With the current numeric order:

```text
position assignment / Act / Yield / result
↓ carried boundary
exact-byte assignment / Act / Yield / result
```

Reversing the writes would produce:

```text
exact-byte assignment / Act / Yield / result
↓ different carried boundary
position assignment / Act / Yield / result
```

Under that current implementation, the measured material and findings may
remain equal while the assignment occurrences, their prior boundaries, later
Evidence, and later result occurrences do not become identical.

Thus:

```text
equal eventual finding populations
!= proof of equal occurrence physiology

serial storage need
!= authority to choose either constitutional order
```

This describes the current runtime.  It does not prove that either Measurement
constitutionally depends on the other's completed lifecycle.

## 4. The serial Standing rule and host loop entered together

History gives the current sentence a narrower evidentiary weight.

Commit `d0e6c025` introduced all of these in one change:

```text
the host declaration tuple
numeric declaration order
the generic discovery / record loop
the Book phrase `declared order`
the requirement to carry each new occurrence before another assignment
```

No earlier general Standing clause says:

```text
one Standing boundary
→ at most one Responsibility assignment
```

The serial sentence therefore cannot serve as independent evidence that the
runtime recovered an older constitutional dependency.  The runtime loop and
the Book sentence were two representations of the same newly introduced
orchestration.

Thus the current implementation collapses two unresolved possibilities:

```text
POSSIBILITY A — constitutional dependency

S0 → position lifecycle → S1 → exact-byte lifecycle


POSSIBILITY B — common responsible boundary, serial recording

             ┌→ position assignment carrying S0
S0 subject ──┤
             └→ exact-byte assignment carrying S0

storage appends those distinct occurrences in one deterministic sequence
without making the first occurrence part of the second assignment's warrant
```

Possibility B does not mean simultaneous writes.  It distinguishes the exact
responsible boundary carried by each assignment from the append order required
by one durable writer.

Current Standing does not decide between A and B.

## 5. The current order is externally addressed

Active `01.Source.D` says `declared order`.  Witness Grammar carries two
`standing_emission_declarations` with numeric coordinates `0` and `1`.
The runtime tuple mirrors those coordinates, and a Fidelity test checks the
mirror.

That is exact external testimony:

```text
Book prose names declared order
Witness Grammar addresses order 0 and order 1
runtime tuple enacts order 0 and order 1
Fidelity compares the two representations
```

It does not establish:

```text
Witness Grammar order has been acquired with positive Standing
↓
this Seed carries that order
↓
this Seed applies that order to these exact assignments
```

The tuple additionally binds each external declaration coordinate to Python
discovery and recording functions.  No exact Seed relation between those
coordinates and functions is established.

Therefore the current loop remains bounded host testimony about one intended
serialization and one proposed constitutional order.  Removing its numeric
field, sorting by another implementation value, or writing two direct calls in
source-code order would not recover the distinction.  Each would only move the
same host decision.

## 6. Current boundary

Recovered:

```text
position-coordinate Measurement exact subject shape       yes
exact-byte Measurement exact source-set subject shape      yes
cross-subject refusal before append                        yes
incomplete exact-byte source-set refusal before append     yes
bounded deterministic external serialization testimony     yes
```

Not recovered:

```text
whether A or B carries the other's lifecycle in its warrant no
whether both assignments carry one earlier boundary         no
positive Standing for a constitutional order                no
Seed-native relation from declaration to implementation    no
Seed-native traversal of all borne Measurement assignments no
lawful separation of append order and responsible boundary no
```

The declaration tuple should not be expanded into a general traversal list.
It also cannot yet be deleted without hiding the unresolved distinction behind
ordinary source-code sequence.

The next lawful crossing is not another scheduler shape.  It is determining
whether all exact assignments applicable at one boundary retain that common
responsible boundary while their occurrence records remain serial, or whether
an exact relation requires one completed lifecycle before the other assignment
becomes applicable.  Only the latter would warrant a constitutional A-before-B
order.

After that distinction is recovered, exact Standing for any required
declaration/order coordinates and the exact relation from declaration to
implementation remain separate work.
The open Witness-acquisition and Locality gates remain separate prerequisites;
this report does not use downstream Measurement results to legitimate either
gate.

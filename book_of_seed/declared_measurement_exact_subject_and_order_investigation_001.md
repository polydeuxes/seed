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

This does not make their exact occurrence order irrelevant.

## 3. Serial order changes the exact carried boundary

`01.Source.D` requires current Standing to carry each recorded occurrence
before another declared Responsibility assignment is recorded.  Both
assignment records preserve the exact prior boundary.

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

The measured material and findings may remain equal.  The assignment
occurrences, their prior boundaries, later Evidence, and later result
occurrences do not become identical.

Thus:

```text
equal eventual finding populations
!= commutative exact occurrence physiology

serial storage need
!= authority to choose either constitutional order
```

## 4. The current order is externally addressed

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

Therefore the current loop remains bounded host testimony about the intended
order.  Removing its numeric field, sorting by another implementation value,
or writing two direct calls in source-code order would not internalize the
order.  Each would only move the same host decision.

## 5. Current boundary

Recovered:

```text
position-coordinate Measurement exact subject shape       yes
exact-byte Measurement exact source-set subject shape      yes
cross-subject refusal before append                        yes
incomplete exact-byte source-set refusal before append     yes
bounded deterministic external order testimony             yes
```

Not recovered:

```text
positive Standing for the declared order                   no
Seed-native relation from declaration to implementation    no
Seed-native traversal of all borne Measurement assignments no
lawful replacement for the host order decision             no
```

The declaration tuple should not be expanded into a general traversal list.
It also cannot yet be deleted without hiding the unresolved order behind
ordinary source-code sequence.

The next lawful crossing is not another scheduler shape.  It is exact Standing
for the declaration/order coordinates, followed by the exact relation, if any,
under which the corresponding Responsibility becomes readable and applicable.
The open Witness-acquisition and Locality gates remain separate prerequisites;
this report does not use downstream Measurement results to legitimate either
gate.

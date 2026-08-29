# Shared-position Measurement binding subtraction census 001

## Proposed control

After the internal recurrent-position Measurement binding event failed
subtraction, the proposed next control was shared-position Measurement:

```text
two internally established recurrent-position results
        ↓
shared-position Measurement binding event
        ↓
Measurement Act
        ↓
result
```

The proposed falsifier was correct:

```text
exact shared-position subject established before Act
    → pressure the separate binding event

host mechanics pair possible inputs before the shared position is established
    → stop
```

## Actual live order

The proposed shape omits the live Applicability lifecycle. The recurrent-result
road is:

```text
two exact recurrent-position result references
        ↓
shared-position Measurement binding event
        ↓
Applicability binding event
        ↓
Applicability Act occurrence
        ↓
applicable | inapplicable result occurrence
        ↓ positive only
shared-position Measurement Act occurrence
        ↓
Measurement result occurrence
```

The Measurement binding is directly addressed by the Applicability binding.
The Applicability result in turn addresses the future Measurement Act identity
minted in the Measurement binding.

This is not a non-Applicability family.

## When the shared coordinate exists

Before Applicability, the two input references establish:

```text
exact containing result occurrences
exact result-local positions
one source material result occurrence
one Locality
one completeness boundary
```

They do not necessarily establish one shared source-position coordinate.
Applicability compares:

```text
first input second-position coordinate
second input first-position coordinate
```

and records `applicable` only when those exact coordinates are equal. The same
public road also records `inapplicable` for an exact pair whose coordinates do
not meet.

Therefore the pre-Applicability Measurement binding is not limited to an
already established shared-position subject. It is prospective material for
the Applicability lifecycle.

## Independent states

The live road preserves:

```text
Measurement binding exists, Applicability absent

Applicability result = inapplicable,
Measurement Act absent

Applicability result = applicable,
Measurement Act absent

Applicability result = applicable,
Measurement Act and result present
```

Moving the binding coordinates directly into the Measurement Act would erase
the negative and positive-before-Act states. Moving them into the Applicability
Act would be Applicability decomposition, not a second clean binding-event
control.

## Cartesian pressure

The runtime accepts two addressed recurrent-position results, records the
Measurement binding, and only afterward establishes whether their position
coordinates meet. Thus this road has the same candidacy pressure already found
around Compare:

```text
addressable inputs
        ↓ host-authored prospective pairing
durable Measurement binding
        ↓
Applicability
```

The current census does not establish a prior Seed occurrence that makes the
two inputs one shared-position Measurement subject before that prospective
binding is appended.

## Finding

```text
shared-position Measurement has no Applicability layer       false
shared position is exact before Applicability                 false in general
binding event can move directly into Measurement Act          not tested
binding coordinates could move into Applicability Act         separate campaign
```

The proposed subtraction stops at its own falsifier.

## Disposition

Do not subtract the shared-position Measurement binding as a simple internal
control. Preserve the current states until the Applicability neighborhood is
tested directly.

Next pressure one actual internal non-Applicability family. Compare-Distinction
Measurement is the narrower control: its exact subject is one prior Compare
result, and its live order is:

```text
exact internal Compare result
        ↓
separate Measurement binding event
        ↓
Measurement Act occurrence
        ↓
Measurement result occurrence
```

If that event independently fails subtraction, stop collecting controls and
return to shared-position/Compare Applicability with the negative and
positive-before-Act states kept intact.

## Amendment after the D.2 control

The D.2-derived subroad supplies the missing positive control. One exact D.2
result already establishes exactly two ordered result-position references with
one addressed source-position coordinate. Its later shared-position
Applicability lifecycle could only return `applicable`.

That subroad now records:

```text
exact D.2 result
        ↓
shared-position Measurement Act
        ↓
Measurement result
```

Both prospective binding events and the forced Applicability lifecycle are
gone. The ordinary recurrent-result road remains unchanged and continues to
record exact negative Applicability results for coordinates that do not meet.

The result therefore narrows this census rather than reversing it:

```text
prior exact occurrence already establishes shared subject  direct Measurement
host-authored prospective pair can be positive or negative  Applicability kept
```

See `d2_shared_position_applicability_subtraction_report_001.md`.

## Amendment after Applicability occurrence-production census

`shared_position_applicability_occurrence_production_census_001.md` finds that
the ordinary recurrent-input lifecycle has no producer call in the active
runtime process. Focused tests create its prospective binding, Applicability
Act/result, Measurement Act, and result through authored calls. The tests prove
that the callable physiology represents both `applicable` and `inapplicable`;
they do not prove what prior Seed occurrence warrants either Applicability Act.

The active inward operation uses only the direct D.2 Measurement road and
therefore produces none of the ordinary binding or Applicability event kinds.

```text
ordinary positive/negative physiology  callable representation control
active inward production               absent
no occurrence                           distinct from inapplicable
D.2 direct production                   established without Applicability
```

The frozen ordinary road must not be used as evidence for moving Cartesian
pair expansion into Applicability Act occurrences.

# Live Applicability Act boundary copy subtraction report 001

## Question

Does one active Applicability Act need to copy the through-occurrence boundary
that was current immediately before it was recorded?

The Act already carries:

```text
two exact subject references
Applicability
addressed Compare
Locality on the occurrence
```

Its exact occurrence also has an established place in Locality occurrence
order.

## Falsifier

Remove only `through_event_occurrence_identity` from the active Applicability
Act.

Preserve:

```text
both subjects current when the Act occurs
subject occurrences before the Act occurrence
positive and negative results
interruption and later resumption
restart and replay
subject substitution refusal
exact coverage readings
```

## Result

The active Applicability Act now carries:

```text
subject_reference:
    shared-position result-position reference
    recorded-pair Compare result reference
act: Applicability
addressed_act: Compare
Locality on the occurrence
```

When no current-coordinate reading is supplied, the reader reconstructs
coordinates through the exact Applicability Act occurrence. During Locality
replay, it consumes the exact coordinates preceding that occurrence.

The reader also validates both exact subject occurrences before the
Applicability Act occurrence. A later coordinate reading cannot be used to
substitute a subject recorded after the Act.

## Coverage control

The interruption control remains exact without a boundary copy on each Act:

```text
through first Applicability Act occurrence   4 exact cross-set members
Acts present                                 1

through later resumed reading                9 exact cross-set members
Acts present                                 9
```

The selected reading boundary defines the coverage question. It is not a
coordinate copied into every member Act.

## Finding

```text
Applicability Act occurrence                 survives
exact subject references                     survive
subject-before-Act order                     survives
selected coverage reading boundary           survives
copied pre-Act through boundary               no distinction found
```

The copied boundary was a replay anchor, not an independently variable
coordinate of this Applicability Act. Exact occurrence order and the selected
reading boundary preserve the two distinct roles without the copy.

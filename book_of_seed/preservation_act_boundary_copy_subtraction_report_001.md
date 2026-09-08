# Preservation Act boundary-copy subtraction report 001

## Question

Does the `06.Locality.C` Preservation Act occurrence need two material fields
that address the same exact operator material occurrence Q?

## Prior shape

```text
subject_reference
    recorded_occurrence_identity = Q

through_occurrence_boundary_reference
    recorded_occurrence_identity = Q
```

The Book requires both the exact subject and its exact through-occurrence
boundary as coordinates of the subject-to-Act binding. It does not require
two copies of Q on the Act occurrence.

## Falsifier

Remove only the Act material's copied boundary reference. Recover the exact
append boundary through Q from the retained subject reference, and preserve:

```text
exact Q subject
exact boundary through Q
Q-before-Act order
Preservation
destination Locality
Act occurrence
Locality relation result
```

The result retains its boundary coordinate during this falsifier so that its
own payload remains a separate pressure.

## Result

The Act reader accepts this smaller exact shape:

```text
Preservation Act occurrence
    act                 Preservation
    subject_reference   Q
    Locality             destination
```

The result writer follows `subject_reference` to place the same exact Q in
the result's through-occurrence boundary coordinate. Restart, replay,
Q-after-Act refusal, changed-subject refusal, and one-result-per-Act refusal
remain unchanged.

```text
Act subject Q                         retained
exact append boundary through Q      retained
copied Act boundary field            absent
result boundary coordinate           retained
```

This subtraction changes no Book coordinate, Act, occurrence, result, or
admitted word.

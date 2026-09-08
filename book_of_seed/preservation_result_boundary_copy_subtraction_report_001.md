# Preservation result boundary-copy subtraction report 001

## Question

Must the `06.Locality.C` relation result payload repeat the exact through-Q
boundary when the result addresses an exact Act occurrence whose exact
subject is Q?

## Prior shape

```text
Locality relation result R
    through_occurrence_boundary_reference Q
    act_occurrence_event_identity          A

A
    subject_reference                      Q
```

The result reader already followed `A` and validated its exact Q subject.
The durable result field repeated that coordinate.

## Falsifier

Remove the boundary reference only from the recorded result material. Keep
the exact readable coordinate by following:

```text
R
→ exact Act occurrence A
→ exact subject Q
→ exact append boundary through Q
```

The reader must still refuse a changed result payload, a changed Act subject,
a Q after A, an absent or corrupted occurrence, and reversed Act/result
order.

## Result

The subtraction passes.

```text
durable R boundary copy                absent
readable through-Q result coordinate   retained
exact Act occurrence reference         retained
exact Q subject                        retained
restart and replay                     retained
```

The destination Locality remains in the result payload during this
falsifier. Its copy is a separate pressure.

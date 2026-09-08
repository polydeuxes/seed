# Preservation result Act-copy subtraction report 001

## Question

Does the `06.Locality.C` relation result need to repeat
`exact_act = Preservation` when it already addresses the exact Preservation
Act occurrence?

## Prior shape

```text
Locality relation result R
    exact_act                      Preservation
    act_occurrence_event_identity A
```

Following `A` reaches the exact Act occurrence and its `act = Preservation`
coordinate. The result's Act label was therefore copied from the occurrence
it addressed.

## Falsifier

Remove only `R.exact_act`. Preserve the exact Act-occurrence reference and
require the result reader to follow it.

```text
R
→ A
→ act = Preservation
```

Changing the referenced Act from Preservation to Measurement must invalidate
the result even though the result no longer contains its own Act label.

## Result

The subtraction passes. The result remains an exact, separate occurrence and
continues to address its exact Preservation Act occurrence.

```text
result exact_act copy             absent
Act occurrence reference          retained
Act = Preservation                retained on A
changed referenced Act            refused
Act-before-result order           retained
one result per Act                retained
restart and replay                retained
```

The through-Q boundary and destination Locality remain on the result during
this falsifier. Their copies require independent pressure.

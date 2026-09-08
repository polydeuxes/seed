# Compare-Distinction Measurement Act boundary census 001

## Question

Is the Act's through-occurrence boundary merely a copy of its exact
Compare-result subject?

## Control

One three-material run records multiple exact Compare results before completing
their Distinction Measurements. It contains this exact order:

```text
Compare-result subject C     evt_000104
through-occurrence boundary B evt_000105
Measurement Act A             evt_000106
```

Thus:

```text
C ≠ B
C → B → A in Ledger append order
```

The Act reader uses B to reconstruct the exact current-coordinate reading under
which C is the Measurement subject. C alone does not identify that reading.

## Falsifier

If every active Act had `C = B`, the boundary field could be a copied subject
coordinate. The multiple-result control instead requires an Act with separate
subject and boundary occurrences and validates their exact append order.

## Disposition

```text
exact Compare-result subject       retained
exact through-occurrence boundary  retained
exact Act occurrence               retained
subject/boundary collapse          refused
```

The boundary is not a durable work population and does not establish future
completion. It is the exact cut for this Act's current-coordinate reading.

No boundary, Act, result, binding occurrence, Applicability, Yield, or relation
is added or removed by this census.

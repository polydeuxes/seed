# Locality continuation result-identity subtraction report 001

## Question

Must the `06.Locality.B` binding mint an opaque future result identity before
the Locality relation result occurs?

## Prior shape

```text
binding occurrence
    result_identity R-token
        ↓ copied
Act occurrence
    binding reference containing R-token
        ↓ copied
relation result occurrence R
    result_identity R-token
    Event.identity
```

The binding authored the token before `R` existed. The Act and result copied
it, and current-coordinate reading required the copies to agree.

## Falsifier

Remove only the prospective family-local result identity. Preserve:

```text
exact source Locality and source cut
fresh destination Locality
binding occurrence
Act occurrence
actual relation result Event.identity
Act-before-result order
one result per Act occurrence
equal source-cut non-collapse
restart and current-coordinate replay
```

## Result

The subtraction passes.

The relation result receives its exact occurrence identity when the Ledger
records it. Separate results remain separate through their actual event
identities and destination Localities.

The binding reference remains exact without a future result field. The
current-coordinate reader accepts this family only when neither the binding
nor result contains the retired result coordinate, while continuing to
validate the binding occurrence and Act occurrence.

The old token had no independent source:

```text
mint token
copy token
require copied token
```

That authored agreement did not distinguish a future result from the actual
result occurrence.

## Disposition

```text
prospective result identity       withdrawn
copied result identity            withdrawn
actual result Event.identity      retained
binding occurrence                unresolved
family-local Act identity         unresolved
family-local Act-occurrence ID    unresolved
```

This result belongs only to the `06.Locality.B` family. It does not generalize
the later lifecycle subtractions without their own falsifiers.

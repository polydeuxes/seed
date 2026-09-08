# Operator destination Locality result-identity subtraction report 001

## Question

Must the `06.Locality.D` binding mint an opaque identity for its relation
result before that result occurrence exists?

## Prior shape

```text
binding occurrence
    result_identity             minted token
        ↓ copied
Locality Act occurrence
    result_identity
        ↓ copied
Locality relation result
    result_identity
    Event.identity              actual result occurrence address
```

No active consumer addressed the family-local token independently from the
actual result occurrence.

## Falsifier

Remove `result_identity` from the binding, Act, and result. Retain:

```text
exact operator material occurrence
exact Locality Act
source and destination Localities
Act occurrence
relation result occurrence
Act-before-result order
one-result-per-Act refusal
```

Two equal-shaped operator destination relations must remain separate through
their exact binding, Act, result, and destination Locality occurrence
identities. Restart and current-coordinate replay must continue to address
the relation result by its actual Event identity.

## Result

The subtraction passes.

```text
prospective result identity     absent
actual result Event.identity    retained
actual Act Event.identity       retained
distinct destination Localities retained
```

Changing the result's exact Act-occurrence reference still invalidates it.
Later supplied material continues to cite the operator occurrence and the
exact relation result occurrence.

This removes one self-authored lifecycle token. It does not authorize removal
of the binding occurrence, the remaining Act identities, any copied payload
coordinate, Locality, Act, or result.

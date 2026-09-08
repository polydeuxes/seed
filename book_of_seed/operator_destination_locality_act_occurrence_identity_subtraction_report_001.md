# Operator destination Locality Act-occurrence identity subtraction report 001

## Question

Does `06.Locality.D` require a family-local Act-occurrence identity in
addition to the actual Locality Act Event identity?

## Prior shape

```text
binding occurrence
    act_occurrence_identity       minted prospective token
        ↓ copied
Locality Act occurrence A
    act_occurrence_identity
    Event.identity                actual Act-occurrence address
        ↓ copied
Locality relation result R
    act_occurrence_identity
    act_occurrence_event_identity A.identity
```

The family-local token was authored before A existed, then required by every
later reader through that same copy chain.

## Falsifier

Remove `act_occurrence_identity` from the binding, Act, and result while
retaining:

```text
A.identity
R.act_occurrence_event_identity = A.identity
A-before-R occurrence order
one result per exact A occurrence
```

Two otherwise equal Locality Acts and results must remain separately
addressable by their actual Ledger occurrence identities. Restart, current-
coordinate replay, and later supplied-material provenance must remain exact.

## Result

The subtraction passes.

```text
family-local Act-occurrence identity  absent
actual Act Event.identity             retained
actual result Event.identity          retained
Act/result occurrence separation      retained
```

Changing the result's Act-event reference still refuses. Changing the
remaining Act identity coordinate on A still refuses during this independent
falsifier.

This result does not authorize removal of the opaque operator-destination Act
identity, the binding occurrence, exact Act `Locality`, or copied subject and
Locality coordinates.

# Locality continuation Act-occurrence identity subtraction report 001

## Question

Does `06.Locality.B` require a family-local Act-occurrence identity in
addition to the actual Ledger identity of its Act occurrence?

## Prior shape

```text
Locality continuation Act occurrence A
    Event.identity             A.identity
    act_occurrence_identity    minted token
        ↓ copied
Locality relation result R
    act_occurrence_identity    same token
    act_occurrence_event_identity A.identity
```

The result writer also used both values when refusing a second result.

## Falsifier

Remove only the family-local token. Use the actual Act event identity for:

```text
Act occurrence address
Act-to-result reference
one-result-per-Act refusal
Act-before-result order
equal source-cut non-collapse
restart and replay
```

Preserve the separate binding occurrence and opaque exact-Act identity for
their later independent pressure.

## Result

The subtraction passes.

The actual Act occurrence is the Ledger event. The result addresses that
event through `act_occurrence_event_identity`. Separate Acts over equal source
cuts retain separate event identities and destination Localities.

The removed token had no independent source. It was minted while recording
`A`, copied into `R`, and validated only against that copy chain.

The result writer now refuses a second result solely when an existing result
addresses the same actual Act occurrence.

## Disposition

```text
family-local Act-occurrence identity withdrawn
actual Act Event.identity             retained
result → actual Act occurrence        retained
prospective result identity           absent from prior subtraction
binding occurrence                    unresolved
opaque exact-Act identity             unresolved
```

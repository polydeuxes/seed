# Operator destination Locality exact-Act identity subtraction report 001

## Question

Does `06.Locality.D` require an opaque
`operator_destination_locality_act_identity` in addition to its exact Act
coordinate and actual Act occurrence?

## Prior shape

```text
binding occurrence
    exact_act                                  Locality
    operator_destination_locality_act_identity minted token
        ↓ copied
Locality Act occurrence A
    act                                        Locality
    operator_destination_locality_act_identity
    Event.identity
        ↓ copied
Locality relation result R
    exact_act                                  Locality
    operator_destination_locality_act_identity
    act_occurrence_event_identity              A.identity
```

The token could be replaced consistently throughout its authored copy chain.
No independent occurrence supplied the value it ought to have had.

## Falsifier

Remove only the opaque token. Preserve:

```text
exact Act = Locality
exact operator material occurrence
operator Locality
operator through-occurrence boundary
destination Locality
actual Act occurrence A
actual relation result R
```

Changing `A.act` away from `Locality` must still invalidate A and R. Separate
operator occurrences must retain separate bindings, Act occurrences, result
occurrences, and destination Localities.

## Result

The subtraction passes.

```text
opaque exact-Act token       absent
exact Act word Locality      retained
actual Act Event.identity    retained
actual result Event.identity retained
```

The exact Act is the independently declared `Locality` coordinate together
with its exact binding coordinates. The Act occurrence is the actual Ledger
event. A third minted identity adds no distinction.

This result does not authorize removing the separate binding occurrence or
any copied subject, boundary, source Locality, or destination Locality
coordinate.

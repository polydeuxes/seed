# Recorded-boundary Locality exact Act identity subtraction report 001

## Question

Does the `06.Locality.C` Preservation Act require a separately minted opaque
Act identity in addition to its exact Act coordinate and Act occurrence?

The prospective occurrence identities and binding event have been removed.
This leaves the exact Act identity as an independent pressure.

## Prior shape

```text
Preservation Act occurrence
    act                 Preservation
    exact_act_identity  minted opaque token
    Event.identity      exact occurrence address
    exact Q subject
    destination Locality
        ↓
Locality relation result
    exact_act           Preservation
    exact_act_identity  copied opaque token
    Act Event.identity  exact Act-occurrence reference
```

The reader required the two opaque token copies to agree. If both copies were
changed together, the writer's own requirement supplied the new expectation;
no independent occurrence or consumer distinguished the replacement token.

## Current shape

```text
Preservation Act occurrence
    act                 Preservation
    Event.identity      exact occurrence address
    exact Q subject
    destination Locality
        ↓
Locality relation result
    exact_act           Preservation
    Act Event.identity  exact Act-occurrence reference
```

`exact_act_identity` is absent from the Act and result payloads. No other
token replaces it.

## Exact distinctions retained

The subtraction does not collapse:

```text
Act                              Preservation
Act occurrence                   exact Act Event.identity
result occurrence                exact result Event.identity
subject                          exact Q occurrence
source cut                       exact boundary through Q
destination                      exact Locality
Act occurrence vs result         separate events
two Preservation occurrences    separate Act event identities
```

Changing `act` away from `Preservation` still causes the Act reader to refuse.
Changing `exact_act` on the result still causes the result reader to refuse.
Thus the Act coordinate survives; only the additional opaque identity fails.

## Controls

The subtraction retains:

```text
zero / one / two current carrier cardinality
validated Q subject before Act occurrence
Act-without-result stoppable floor
one result per Act occurrence
Act-before-result occurrence order
current-coordinate advance and replay
descendant carriage of Q
SQLite reopen
changed-coordinate and corruption refusal
```

The exact Act occurrence remains sufficient to address the result-producing
Act. Content equality between two Act payloads does not collapse their
separate event identities.

## Results

```text
opaque exact Act identities per lifecycle  1 -> 0
exact Act word                            Preservation
actual Act occurrence identity            retained
actual result occurrence identity         retained
binding occurrence                        absent
prospective lifecycle identities          absent
```

Focused operator, current-coordinate, Book grammar, and admission tests:

```text
90 passed
```

Complete suite:

```text
1059 passed
75 skipped
```

Python compilation and `git diff --check` pass.

## Finding

The separately minted `exact_act_identity` adds no exact distinction on the
active recorded-boundary Locality road. The exact Act is `Preservation`; the
Act event identity distinguishes its occurrence.

Remaining copied Act, subject, boundary, and destination fields must be
pressure-tested separately. This result does not authorize their removal.

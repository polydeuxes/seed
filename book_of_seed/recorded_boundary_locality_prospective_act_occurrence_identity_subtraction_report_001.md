# Recorded-boundary Locality prospective Act-occurrence identity subtraction report 001

## Question

Must a `06.Locality.C` Preservation binding mint an identity for an Act
occurrence before that occurrence exists?

This pressure is independent from the prior result-identity subtraction. The
exact Act identity, binding occurrence, actual Act occurrence, and result
occurrence remain under separate coordinates.

## Prior shape

```text
Preservation binding occurrence
    mints act_occurrence_identity
        ↓ copies it
Preservation Act occurrence
    has act_occurrence_identity
    has Event.identity
        ↓ copies both forms
Locality relation result occurrence
```

The result writer accepts the actual Act event identity. The family-local
prospective identity was copied beside that exact occurrence reference.

## Current shape

```text
Preservation binding occurrence
        ↓
Preservation Act occurrence
    addressed by its exact Event.identity
        ↓
Locality relation result occurrence
    addresses that Act Event.identity
```

`act_occurrence_identity` is absent from the binding, Act, and result
payloads. The Act acquires an exact occurrence address when it is recorded.

## Controls

The subtraction retains:

```text
exact Q subject
exact through-Q boundary
source and destination Localities
binding-without-Act stoppable floor
Act-without-result stoppable floor
Act-before-result occurrence order
one result per Act occurrence
current-coordinate advance and replay
descendant carriage of Q
SQLite reopen
changed-coordinate and corruption refusal
```

The binding remains readable before an Act exists. Removing a prospective Act
occurrence token does not remove that floor.

The result remains connected to exactly one Act occurrence through
`act_occurrence_event_identity`. Changed or absent event references continue
to refuse.

## Results

```text
prospective Act-occurrence identities per binding  1 -> 0
actual Act occurrence identity                     retained
actual result occurrence identity                  retained
binding occurrence                                 retained
exact Act identity                                  unresolved
```

Focused operator and current-coordinate tests:

```text
49 passed
```

## Finding

The family-local prospective Act-occurrence identity adds no exact distinction
on the active recorded-boundary Locality road. The actual Act event identity
supplies the occurrence address when Preservation occurs.

The next independent pressure is the separate binding occurrence. Its failure
or survival does not decide whether the exact Act identity survives.

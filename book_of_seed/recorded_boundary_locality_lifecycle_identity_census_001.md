# Recorded-boundary Locality lifecycle identity census 001

## Question

Which identities in the `06.Locality.C` Preservation lifecycle distinguish an
exact constitutional coordinate, and which repeat the identities of Ledger
occurrences that subsequently exist?

This census changes no runtime road, Book clause, event kind, Act, result
kind, or admitted word.

## Current shape

The subject-to-Act binding occurrence mints three family-local identities:

```text
exact_act_identity
act_occurrence_identity
result_identity
```

The lifecycle then records three Ledger occurrences, each with its own exact
event identity:

```text
binding Event.identity
Act Event.identity
result Event.identity
```

The current durable payload repeats the family-local identities across the
binding, Act, and result:

```text
binding
    exact Act identity
    prospective Act-occurrence identity
    prospective result identity

Act occurrence
    exact Act identity
    prospective Act-occurrence identity
    prospective result identity

result occurrence
    exact Act identity
    prospective Act-occurrence identity
    prospective result identity
```

The Act and result also repeat the binding reference, through-occurrence
boundary reference, and destination Locality.

## Census

### Prospective result identity

`result_identity` is minted by the binding before any result occurrence
exists. When the result occurs, its Ledger event identity separately provides
an exact result-occurrence address.

No active consumer addresses the family-local result identity independently
from the result occurrence. Current-coordinate replay addresses the result by
its Ledger event identity and validates it through
`get_recorded_boundary_locality`.

Changing one copied `result_identity` while leaving its copies unchanged
causes refusal because the reader requires equality with the payload it
authored. That is a dependency among copied coordinates, not evidence that the
prospective identity and eventual result occurrence can vary independently.

### Prospective Act-occurrence identity

`act_occurrence_identity` is likewise minted by the binding before the Act
occurrence. The recorded Act event subsequently has its own exact Ledger event
identity.

The result writer and reader address the Act occurrence through its Ledger
event identity. No active consumer uses the family-local Act-occurrence
identity to address a different Act occurrence from that event address.

### Exact Act identity

`exact_act_identity` is not the same claim as either prospective occurrence
identity. The Book distinguishes an exact Preservation Act from its Act
occurrence and Locality relation result occurrence.

The present runtime mints an opaque identity for that exact Act on every
binding. Whether this token independently carries the Act distinction, or
whether exact Act `Preservation` plus its subject and Locality coordinates are
sufficient, requires a separate falsifier.

The failure of either prospective lifecycle identity does not decide this
question.

### Binding occurrence

The binding event currently provides a stoppable floor and carries:

```text
exact Q reference
exact Act identity
destination Locality
prospective lifecycle identities
Book clause copy
```

Prior subtraction campaigns showed that a binding can remain exact through
coordinates on an Act occurrence without requiring a separate binding event.
This census does not apply that result automatically to `06.Locality.C`.

The Preservation road must retain the independently varying floor in which a
binding exists and its Act occurrence does not, unless a subtraction shows
that the floor contains no fact beyond the binding event the runtime authored.

## Active consumers

The active current-coordinate reader uses:

```text
binding Event.identity
    → validate binding occurrence

Act Event.identity
    → validate Act occurrence and binding reference

result Event.identity
    → validate result and recover exact Q boundary
```

It does not publish `result_identity`, `act_occurrence_identity`, or
`exact_act_identity` as separate current-coordinate families.

Descendant Localities carry the exact `Q` occurrence reference recovered from
the result. They do not carry any of the three family-local identities.

## Independent pressure order

The smallest one-coordinate falsifiers are:

```text
1. prospective result identity
2. prospective Act-occurrence identity
3. separate binding occurrence
4. exact Act identity
5. copied subject / Locality / clause coordinates
```

Every step must preserve:

```text
exact Q subject
exact through-Q boundary
source and destination Localities
Act-before-result occurrence order
zero or one result per Act occurrence
current-coordinate replay
SQLite reopen
descendant carriage of Q
changed-coordinate and corruption refusal
```

No field survives merely because the same recorder copied it into every
subsequent payload and the same reader requires those copies to agree.

## Finding

The two prospective lifecycle identities have no independent active consumer:

```text
prospective result identity          unsupported by independent use
prospective Act-occurrence identity  unsupported by independent use
actual Act occurrence identity       exact Ledger coordinate
actual result occurrence identity    exact Ledger coordinate
exact Act identity                    unresolved
binding occurrence                    unresolved
```

The first implementation pressure is the prospective result identity alone.

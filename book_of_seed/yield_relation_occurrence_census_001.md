# Yield relation occurrence census 001

## Question

Does Yield require an occurrence distinct from both its Act occurrence and its
result occurrence?

This census concerns internal Act and result physiology. It does not investigate
external Witness work or Emission.

## Recorded order

Every inspected road records:

```text
subject-to-Act binding
Act occurrence
Yield relation event
result occurrence
```

The Yield event is therefore recorded before its declared second subject, the
exact result occurrence, exists.

`_record_yield_relation()` receives a result identity and a complete result
dictionary. It copies that dictionary into the Yield event and records a map
from every copied coordinate to the future result material. The result is then
recorded with the Yield event identity.

## Addressed coordinates

The separate Yield event has a durable event identity and append position.
Result readers address it through `yield_relation_identity` and refuse a
missing, changed, substituted, or corrupted event. Some source occurrence lists
also include its identity.

The inspected readers use the event to compare:

```text
Act occurrence identity
Act description
result identity
complete result dictionary
result event Locality
exact material where present
```

Those coordinates already exist on the Act occurrence and result occurrence.
No inspected result permits the copied Yield result and the recorded result to
vary independently. No inspected Act permits a second Yield or result.

## Locality control

A Locality Act records its result occurrence as the Locality relation
occurrence. Ordinary material results merely occur at one exact Locality and
establish no second Locality relation.

Yield must not inherit either answer by analogy. Its own discriminator is
whether a distinct occurrence between the Act and result establishes an exact
coordinate that the two endpoint occurrences cannot establish.

## First subtraction test

The operator destination Locality road is the smallest internal control because
its result occurrence is already independently established as the Locality
relation occurrence.

Pressure-test:

```text
binding
Act occurrence
result occurrence

result directly addresses its Act occurrence
```

Remove only the separate Yield event and copied result dictionary. Preserve:

```text
exact binding
exact Act occurrence
exact Locality endpoints
exact result occurrence
Act-before-result order
one result for the Act
reopen
mutation and substitution refusal
```

If an independently addressable distinction disappears, Yield survives. If the
result occurrence establishes every exact endpoint and refusal without the
interposed event, the separate Yield occurrence fails this road.

No global withdrawal is proposed by this census.

# Operator destination Locality binding-occurrence subtraction report 001

## Question

Does `06.Locality.D` require a separate subject-to-Act binding occurrence
before its Locality Act occurrence?

## Prior shape

```text
exact operator material occurrence Q
+ exact current source cut B
        ↓
subject-to-Act binding occurrence
    Q
    B
    Locality
    source Locality
    fresh destination Locality D
        ↓
Locality Act occurrence A in D
        ↓
Locality relation result R in D
```

The binding occurrence allocated `D`, carried the exact coordinates, and
provided a stoppable floor before `A`. The Act and result then copied its
identity.

No prior Seed occurrence produced the binding occurrence. Its remaining
distinction was the occurrence the runtime had appended for that purpose.

## Falsifier

Remove only the separate binding occurrence. Let the Locality Act occurrence
carry the exact subject-to-Act binding coordinates required by `02.Acts.A`:

```text
Q
+ B
+ Locality
+ source Locality
+ fresh D
        ↓
Locality Act occurrence A in D
        ↓
Locality relation result R in D
```

The subtraction must preserve:

```text
exact operator material occurrence Q
exact current source coordinates through B
Q at or before B
B before A
fresh destination Locality D
one destination Locality Act for Q
Act occurrence without result occurrence
Act-before-result order
one result per Act occurrence
separate equal-content operator occurrences
restart and current-coordinate replay
downstream supplied-material source references
changed and corrupted coordinate refusal
```

The test must also show that neither the retired event kind nor a renamed
binding-event reference remains.

## Result

The subtraction passes.

The Locality Act writer validates `Q` in the supplied exact current source
coordinates, retains their exact through-occurrence cut, allocates `D`, and
records `A` in `D`. A prior Act addressing the same `Q` refuses a second
destination.

The Act reader follows only the exact addressed coordinates. It validates the
operator material occurrence and source cut, then checks this global append
order using exact occurrence identities:

```text
Q, B, A
```

When `Q` is itself `B`, the checked order is:

```text
Q, A
```

A substituted boundary after `A` refuses. No unrelated occurrence material
is read to establish that order.

The result still addresses the actual Act occurrence. The Act can be read
before any result exists, and a second result for the same Act refuses.

## Stoppability

Before the subtraction, this floor was representable:

```text
binding occurrence exists
Act occurrence absent
```

Its only positive coordinate was the binding wrapper itself. The prospective
result identity, family-local Act-occurrence identity, and opaque exact-Act
identity had already failed independent subtraction. Moving the surviving
binding coordinates to `A` therefore removes no independently varying fact.

The surviving floors are:

```text
Q exists
A absent

A exists
R absent

A exists
R exists
```

The Act occurrence is the constitutional fact that the Locality Act occurred.
No prior producer occurrence is required merely to explain that occurrence.

## Current durable shape

```text
Locality Act occurrence A
    Event.identity
    Event.locality_identity = D
    act = Locality
    operator material occurrence = Q
    operator material result occurrence = Q
    source Locality
    source cut = B
    destination Locality = D

Locality relation result R
    Event.identity
    Event.locality_identity = D
    exact Act = Locality
    operator material occurrence = Q
    source Locality
    destination Locality = D
    Act occurrence = A
```

This report does not claim that every repeated coordinate in that shape must
remain. It establishes only that the separate binding occurrence is not one
of the required coordinates.

## Disposition

```text
subject-to-Act binding coordinates       retained on A
separate binding occurrence              withdrawn
retired binding event kind               absent
binding-event reference on A and R       absent
exact Locality Act                       retained
exact source cut                         retained
fresh destination Locality               retained
actual Act occurrence                    retained
actual relation result occurrence        retained
```

The next pressure, if any, belongs to copied coordinates on `A` and `R`. It
does not belong to another binding or lifecycle object.

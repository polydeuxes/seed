# Locality continuation binding-occurrence subtraction report 001

## Question

Does `06.Locality.B` require a separate binding occurrence before its Act
occurrence?

## Prior shape

```text
exact source Locality L
+ exact through-occurrence boundary B
        ↓
binding occurrence in fresh destination D
        ↓
Act occurrence A in D
        ↓
Locality relation result R in D
```

The binding allocated `D`, minted an opaque exact-Act identity, carried the
source coordinates, and provided a stoppable floor before `A`.

## Falsifier

Remove only the separate binding occurrence. Let `A` carry the exact binding
coordinates:

```text
source Locality L
+ source cut B
+ opaque exact-Act identity
+ narrated Act coordinate under later pressure
+ fresh destination D
        ↓
Act occurrence A in D
        ↓
relation result R in D
```

Preserve:

```text
exact L and B
intact B occurrence
B before A in global Ledger order
fresh destination D
Act occurrence without result occurrence
Act-before-result order
one result per Act
equal source-cut non-collapse
restart and current-coordinate replay
direct continuation from a prior relation result
```

No new binding, request, work, or completion occurrence may replace the old
wrapper.

## Result

The subtraction passes.

The Act writer validates `L` and `B`, allocates `D`, and records `A` in `D`.
The Act reader validates the exact source coordinates and checks:

```text
B before A
```

through the two exact occurrence identities. A substituted source boundary
recorded after `A` refuses.

The current-coordinate reader now carries no Locality-continuation binding
occurrence. After `A` and before `R`:

```text
Act occurrence current in D       yes
relation result current in D      no
binding occurrence current in D   no occurrence exists
```

After `R`, its exact subject-to-Act coordinates are read through:

```text
R → A → exact source-coordinate reference
```

## Stoppability

The retired floor was:

```text
binding exists
Act absent
```

Its positive coordinate was the wrapper the runtime had appended. The
prospective result identity and family-local Act-occurrence identity had
already failed independent subtraction. Moving the surviving coordinates to
`A` removes no independently varying result or relation.

The surviving floors are:

```text
source cut exists
Act absent

Act exists
result absent

Act exists
result exists
```

## Disposition

```text
source Locality and cut             retained
binding coordinates on Act          retained
separate binding occurrence         withdrawn
retired binding event kind          absent
binding-event reference             absent
fresh destination Locality          retained
actual Act and result occurrences   retained
opaque exact-Act identity            unresolved
Act phrase                           unresolved
copied Act/result coordinates        unresolved
```

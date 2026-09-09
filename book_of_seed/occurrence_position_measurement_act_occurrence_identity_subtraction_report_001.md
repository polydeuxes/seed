# Occurrence-position Measurement Act-occurrence identity subtraction report 001

## Question

Must an occurrence-position Measurement binding mint a family-local identity
for its future Act occurrence in addition to the actual Ledger identity of that
Act occurrence?

## Prior shape

The binding minted `act_occurrence_identity = A*`. The later Act and result
copied `A*`, while the actual Act occurrence had `A.identity` and the result
also addressed `A.identity` through `act_occurrence_event_identity`.

The family-local identity was known only through this lifecycle's copied
values. No independently prior occurrence addressed it.

## Falsifier

Remove `A*` only from occurrence-position Measurement while preserving:

```text
exact binding occurrence
exact Measurement Act coordinate
actual Act occurrence A
actual result occurrence R
R addresses A.identity
binding before A
A before R
one A per binding
one R per A
every ordered occurrence-position finding
current-coordinate replay
SQLite restart
mutation and substitution refusal
```

The prospective result identity had already failed independently. The opaque
exact Act identity and binding occurrence remain for later falsifiers.

## Result

The actual Act occurrence identity is sufficient. Duplicate-Act refusal uses
the exact binding reference; duplicate-result refusal uses the exact Act event
identity. The result still validates and addresses the Act that precedes it.

Current coordinates retain `A.identity` and `R.identity`. They no longer copy
a second Act-occurrence address for this family. Other Measurement families
retain their own identity coordinates pending independent pressure.

## Disposition

```text
prospective family Act-occurrence identity   withdrawn
copied family Act-occurrence identity         withdrawn
actual Act occurrence identity                retained
actual result occurrence identity             retained
binding-before-Act order                       retained
Act-before-result order                        retained
one Act per binding                            retained
one result per Act                             retained
```

No binding occurrence, Act, result, relation, finding, or admitted word is
added or removed.

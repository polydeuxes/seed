# Occurrence-position Measurement result-identity subtraction report 001

## Question

Must an occurrence-position Measurement binding mint the identity of its
future result before that result occurs?

## Prior shape

The binding minted:

```text
measurement_result_identity = prospective identity R*
```

The later result copied `R*` as `result_identity` while also receiving its
actual Ledger occurrence identity `R.identity`.

No independently prior occurrence addressed `R*`. The binding authored the
value, and the result and readers repeated that authored value as their
expectation.

## Falsifier

Remove `R*` only from occurrence-position Measurement while retaining:

```text
exact source Locality
exact completeness boundary
every bounded occurrence and ordered position
binding occurrence
exact Measurement Act
exact Act occurrence A
exact result occurrence R
A before R
one result per A
current-coordinate replay
SQLite restart
separate equal-material occurrences
changed subject, position, boundary, and Locality refusal
```

The binding occurrence, opaque exact Act identity, and prospective family Act
occurrence identity remain in place for their own falsifiers.

## Result

`R.identity` supplies the result's exact address when `R` occurs. Current
coordinates already key the Measurement result by that actual occurrence
identity, and the result continues to address its exact Act occurrence through
`act_occurrence_event_identity`.

The result findings and every source coordinate are unchanged. SQLite reopen
continues the two still-minted family identity sequences without requiring a
reserved future result identity.

## Disposition

```text
prospective Measurement-result identity   withdrawn
copied family result identity              withdrawn
actual result occurrence identity          retained
actual Act occurrence identity             retained
Act-before-result order                     retained
one result per Act                          retained
```

No binding occurrence, Act, result, relation, finding, or admitted word is
added or removed.

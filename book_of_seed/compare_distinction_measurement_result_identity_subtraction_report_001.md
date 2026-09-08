# Compare-Distinction Measurement result-identity subtraction report 001

## Question

Must a Compare-Distinction Measurement Act mint the identity of its future
result before that result occurs?

## Prior shape

The Act occurrence carried:

```text
measurement_result_identity = prospective identity R*
```

The later result copied `R*` as `result_identity` while also receiving its
actual Ledger occurrence identity `R.identity`.

The prospective identity was known only through the values authored by this
lifecycle. No independently prior occurrence addressed it.

## Falsifier

Remove `R*` from the Act and result while preserving:

```text
exact Compare-result subject
exact Measurement Act occurrence A
exact Measurement result occurrence R
A before R
one result per A
complete Distinction findings
current-coordinate replay
restart
equal finding content in separate R occurrences
later exact references to R.identity
```

## Result

The actual result occurrence establishes its address when it occurs. Existing
downstream composition already uses the recorded result occurrence identity,
including the read-only joint between separate Distinction Measurement results.

Equal measured content remains non-collapsing because the two results retain
separate Ledger occurrence identities. The Act and result also remain separate
exact occurrences.

## Disposition

```text
prospective Measurement-result identity   withdrawn
copied family result identity              withdrawn
actual result occurrence identity          retained
actual Act occurrence identity             retained
Act-before-result order                    retained
one result per Act                         retained
```

No binding occurrence, Applicability, Yield, result, or relation is added.

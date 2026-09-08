# Operator source prospective result identity subtraction report 001

## Falsifier

Before subtraction, the operator source binding minted a result identity and
copied it into the later Act occurrence before any material result occurrence
existed.

The test removes only that prospective coordinate:

```text
source binding
    exact Act identity
    future Act occurrence identity
    no result identity

Act occurrence
    no result identity

material result occurrence
    exact result occurrence identity
```

## Result

The binding-only and Act-without-result floors remain exact and durable without
a future result identity. After restart, the exact Act occurrence can record
one material result.

Act-before-result order, one-result refusal, exact bytes, source boundary,
current-coordinate replay, downstream source references, mutation refusal,
and corruption refusal remain unchanged.

The first test retained a family-local result identity at result occurrence.
Changing that identity remained accepted because the reader reused the changed
value as its own expectation. No coordinate independently addressed it.

The exact result occurrence identity already distinguishes equal material
results and supplies downstream source references. The completed subtraction
therefore establishes:

```text
family-local result identity before result occurrence   withdrawn
family-local result identity at result occurrence       withdrawn
exact result occurrence identity                         survives
```

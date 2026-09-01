# Operator source Act occurrence identity subtraction report 001

## Falsifier

The operator source binding previously minted a family-local Act occurrence
identity before the Act occurrence existed. The binding, later Act occurrence,
and result copied that value. The actual Act occurrence also has an exact
Ledger occurrence identity.

This test removes only the prospective family-local coordinate:

```text
source binding
    exact unnamed Act identity
    no future Act occurrence identity

Act occurrence
    exact Ledger occurrence identity

material result occurrence
    exact Act occurrence reference
```

The separate binding occurrence and exact unnamed Act identity remain under
independent pressure.

## Result

The binding-only and Act-without-result floors remain exact. The result
addresses its Act through the actual Act occurrence identity. Act-before-result
order and one-result refusal therefore require no copied family-local identity.

Equal material results still have separate Act occurrences and separate result
occurrences. Current-coordinate replay, durable reopen, source boundaries,
exact bytes, downstream Measurement, refusal of changed required coordinates,
and corruption refusal remain unchanged.

The former binding-only mutation control for the exact unnamed Act identity
changed it to the family-local Act occurrence identity. Removing the latter
exposes that comparison as circular: before an Act occurrence exists, an
arbitrary replacement exact Act identity currently validates as its own
expectation. This does not decide that coordinate here; it supplies its next
independent falsifier.

```text
operator family-local Act occurrence identity   withdrawn
operator exact Act occurrence identity          survives
operator exact unnamed Act identity              still under pressure
operator binding occurrence identity             still under pressure
```

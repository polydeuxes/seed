# Source lifecycle identity census 001

## Question

Which identities on the operator and Witness material-source roads name an
independently variable distinction, and which are minted before their
occurrences exist?

## Recorded shape before subtraction

Both source bindings minted and copied:

```text
exact Act identity
future Act occurrence identity
future result identity
```

The later Act occurrence and result also have exact Ledger occurrence
identities. The binding occurrence has its own Ledger occurrence identity.

The current readers require the family-local identities because the recorders
authored them first. That requirement alone does not distinguish them from the
actual occurrence identities.

## Independent pressure order

The coordinates must be tested separately:

```text
1. future result identity before result occurrence
2. future Act occurrence identity before Act occurrence
3. separate binding occurrence
4. exact unnamed Act identity
```

The result identity test first asks only whether the identity must precede the
result. It does not yet claim that the result identity and result occurrence
identity are the same coordinate.

Likewise, moving or removing the future Act occurrence identity cannot decide
whether the exact unnamed Act identity survives.

## Controls

Every subtraction must retain:

```text
exact source boundary
exact supplied material
source occurrence references
Locality
binding and Act stoppable floors while they remain under pressure
Act-before-result occurrence order
one result per Act occurrence
durable reopen
changed-coordinate and corruption refusal
```

No identity survives merely because a later reader repeats a requirement
authored by the same recorder.

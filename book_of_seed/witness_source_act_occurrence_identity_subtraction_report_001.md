# Witness source Act occurrence identity subtraction report 001

## Independent control

The Witness source binding independently minted a family-local Act occurrence
identity before its Act occurrence existed. The binding, Act occurrence, and
result copied that value even though the actual Act occurrence also has an
exact Ledger occurrence identity.

Removing only the family-local identity preserves:

```text
exact source boundary
exact supplied bytes
source occurrence references
read occurrences and boundary outcomes
exact unnamed Act identity
binding occurrence
Act occurrence and result occurrence order
one result per Act occurrence
separate equal-material Act and result occurrences
durable reopen
```

The result addresses the exact Act occurrence through its Ledger occurrence
identity. Current-coordinate reading and downstream Measurement require no
prospective or copied family-local Act occurrence identity.

## Disposition

```text
Witness family-local Act occurrence identity   withdrawn
Witness exact Act occurrence identity          survives
Witness exact unnamed Act identity              still under pressure
Witness binding occurrence identity             still under pressure
```

The operator and Witness source roads now agree independently on their Act
occurrence coordinate shape.

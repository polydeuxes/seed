# Byte Measurement exact-Act identity subtraction report 001

## Question

Does plain-byte Measurement require an opaque exact-Act identity in addition to
its exact Act and actual occurrences?

This pass follows the independent removal of the prospective result and
Act-occurrence identities. It does not infer a result for byte-pair Measurement
or any other Measurement family.

## Prior shape

The binding minted:

```text
exact_act_identity = opaque M*
```

That binding was the only producer of `M*`. The Act copied it as
`addressed_act_identity`; the result copied it again. Binding references copied
the same value through the lifecycle.

No Ledger occurrence existed at `M*`, and no reader resolved an occurrence
through it. Validation compared the copied values with their common authored
origin.

## Exact Act and exact occurrences

Removing the opaque token does not remove the Act:

```text
binding E
    exact byte-Measurement subjects and boundaries

Act occurrence A
    act = exact-byte Measurement
    exact reference to E
    Act Locality

result occurrence R
    exact reference to A
    exact-byte Measurement
    exact byte findings
```

`E.identity`, `A.identity`, and `R.identity` remain separate occurrence
addresses. The result still addresses its Act occurrence through `A.identity`.

## Falsifier

Remove only:

```text
E.exact_act_identity
binding-reference copy of exact_act_identity
A.addressed_act_identity
R.addressed_act_identity
```

Retain the binding, Act, result, source occurrence references, source
Localities, both boundary domains, complete byte findings, Act/result order,
one Act per binding, one result per Act, replay, restart, corruption refusal,
and downstream byte-pair Measurement and Movement.

Two bindings over equal source coordinates remain separate through their
actual binding identities. Their Acts and results likewise remain separate
actual occurrences.

## Generic result ownership

Current-coordinate reading previously expected every binding reference to
carry `exact_act_identity`. Plain-byte Measurement now uses the smaller exact
reference:

```text
binding occurrence identity
Book clause
exact subject reference
```

The exception is limited to the plain-byte result kind. Byte-pair Measurement
and every other family continue to require their existing reference shapes.

## Disposition

```text
opaque plain-byte exact-Act identity          withdrawn
copied plain-byte addressed-Act identity      withdrawn
exact Measurement Act                         retained
binding, Act, and result occurrences          retained
actual Act and result occurrence identities   retained
byte-pair identities and payloads              unchanged
```

No Act, result, relation, finding, Book clause, Witness Grammar coordinate, or
admitted word is added or removed.

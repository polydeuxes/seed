# `same` coordinate-domain census 001

## Question

Does active `same` collapse content equality, occurrence identity, address
identity, position equality, and Locality identity into one undifferentiated
claim?

This census changes no Book clause, admission, machine grammar, runtime
occurrence, Act, result, relation, identity, or reader.

## Active uses

Every active use names its coordinate domain:

```text
same Locality occurrence order
same content
same result-local position
same-position Measurement
```

The `04.Compare.B` result-reference use retains the qualified Measurement
family; it does not introduce another equality domain.

## Locality equality

Current, Locality continuation, recorded-pair Compare, and checkpoint
Recording all require equality of exact Locality coordinates where they say
`same Locality`.

Changing one Locality identity does not merely change prose. The occurrence
order, source continuation, Compare input order, or Recording coordinates can
no longer be established in that Locality.

```text
same Locality       equal exact Locality identity
same occurrence     not implied
same content        not implied
```

## Content and local-position equality

`01.Current.D.1` supplies the adversarial control:

```text
result A, position 0, content X
result B, position 0, content X
```

Content and local integer position are equal. The exact addresses remain
different because their containing result occurrences differ.

```text
same content
+ same result-local position
!= same exact addressed coordinate
```

This is the exact supplied-material control needed for repeated equal bytes in
separate observations. Equal content does not establish one occurrence or one
real-world source.

## Position equality

The shared-position Measurement compares two exact source-position coordinate
references. Equal references can produce `applicable`; unequal references can
produce `inapplicable` on the preserved representation control.

The equality is therefore narrower than either input identity:

```text
first exact pair-position result
second exact pair-position result
equal shared source-position coordinate
```

The two result positions must remain nonidentical even where the shared
source-position coordinate is equal.

## No global sameness

Active `same` establishes none of these unqualified claims:

```text
equal content       = one occurrence       no
equal local integer = one address          no
equal position      = one input            no
equal Locality      = equal subject        no
```

The qualified coordinate following `same` is load-bearing.

## Finding

```text
Locality equality                    independently variable
content equality                     independently variable
result-local position equality       independently variable
shared source-position equality      independently variable
containing occurrence identity       preserved separately
unqualified same object              absent
`same` coordinate equality           survives
```

## Disposition

Keep `same` in active Book admission.

It names equality under the exact coordinate domain stated with it. It never
establishes occurrence identity, address identity, or equality under another
coordinate domain by itself.

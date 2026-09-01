# Live Applicability addressed Act census 001

## Question

Does `addressed_act: Compare` add an exact distinction to the active
Applicability Act, or does its occurrence kind or a later Compare occurrence
establish the same coordinate?

This census changes no Book clause, runtime occurrence, Act, result, identity,
or reader.

## Book coordinate

`01.Current.E.1` establishes that one Applicability Act occurrence has:

```text
one exact subject-to-Act binding
the exact Act addressed by that binding
Locality
```

On the active road, the binding event has failed subtraction, but its exact
coordinates remain:

```text
two exact subjects
addressed Compare
Locality
```

Thus removing the binding occurrence does not remove the addressed-Act role
from Applicability.

## Declaration test

The active Applicability Act occurrence kind declares `02.Acts.A`. That
declaration establishes an Act occurrence. It does not declare which other Act
the Applicability question addresses.

`04.Compare.B` establishes the exact Compare subjects and result family, but
the active Applicability occurrence still needs an exact coordinate saying
that its question concerns Compare rather than another Act over the same
subjects.

An implementation family name is not an additional Book coordinate.

## Negative control

The two-by-two active control records:

```text
4 Applicability Acts and results
2 applicable
2 inapplicable
2 Compare Acts and results
```

Each positive result can later be followed to one Compare Act. Neither
negative result has a Compare Act occurrence.

For one negative result, the only durable chain is:

```text
exact subjects
→ Applicability Act addressing Compare
→ inapplicable result
```

Changing the Applicability Act's addressed Act from `Compare` to
`Measurement` invalidates the negative result reading. No later occurrence can
recover the removed coordinate because the inapplicable branch correctly has
no Compare occurrence.

## Finding

```text
Applicability                                         survives
exact subjects                                        survive
addressed Compare                                     survives
Locality                                              survives
negative result                                       survives
Compare occurrence on negative branch                 absent
event-kind declaration establishes addressed Compare  no
```

`addressed_act: Compare` is not copied evidence or family narration. It is the
exact Act-relative coordinate that makes `inapplicable` mean:

```text
these exact subjects are inapplicable to Compare
```

rather than an unqualified negative answer.

## Disposition

Keep `addressed_act: Compare` on the active Applicability Act.

The negative branch is the positive control: Applicability can preserve an
exact addressed Act even when that addressed Act never occurs.

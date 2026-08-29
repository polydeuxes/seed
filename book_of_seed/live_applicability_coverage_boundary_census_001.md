# Live Applicability coverage boundary census 001

## Question

Does interrupted Applicability work remain fixed to the exact current sets at
the boundary where the first Act occurred?

Or does a later invocation act upon the exact sets current at its later
boundary?

This census adds no Book word, runtime occurrence, Act, result, identity, or
completion object.

## Falsifier

At boundary `B1`, the active family reads:

```text
2 shared-position result positions
2 recorded-pair Compare results
4 exact cross-set members
```

One Applicability Act is recorded for one member. Work then stops.

A third exact input family is recorded. At later boundary `B2`, the active
sets contain:

```text
3 shared-position result positions
3 recorded-pair Compare results
9 exact cross-set members
```

The same active call is resumed at `B2`.

## Result

Resumption records eight Applicability Acts. Together with the first Act, the
history contains exactly one Act for each of the nine members current at `B2`.

The first Act remains bounded by `B1`. It is not rewritten to carry `B2`.
The eight later Acts carry their own advancing through-occurrence boundaries.

Therefore this road does not establish one fixed work set carried from `B1`
through completion:

```text
members current at B1                  4
Acts recorded before interruption      1
members current at B2                  9
Acts recorded after resumption          8
all members current at B2 covered       yes
first Act rewritten                     no
one shared completion boundary          absent
```

## Exact distinction

The durable facts are the individual Applicability Act occurrences and their
exact subjects and boundaries.

Exhaustive coverage is reconstructed at a selected reading boundary:

```text
exact S(B) and C(B)
+ recorded Applicability Act subjects current through B
→ whether every exact S(B) × C(B) member has one Act
```

This reading does not establish `Population`, `Coverage`, `Completion`,
`Enumeration`, or another occurrence. It also does not make the initial
boundary a durable work extent.

## Finding

```text
fixed B1 member set survives interruption       no
later invocation reads exact sets at B2          yes
later membership can enlarge the exact set       yes
one Act per B2 member after resumption            yes
individual Act boundaries remain exact           yes
durable work-set occurrence                       absent
durable completion occurrence                     absent
```

The prior phrase “one Applicability Act for every exact member of `S(B) ×
C(B)`” remains valid only as a boundary-relative reading. It does not describe
one frozen lifecycle whose members were fixed when the first Act occurred.

## Disposition

Keep the active occurrence shapes unchanged.

Amend the coverage censuses to distinguish:

```text
individual Act coordinates
from
exhaustive coverage reconstructed at one exact reading boundary
```

Do not add a durable population, work, progress, or completion wrapper.

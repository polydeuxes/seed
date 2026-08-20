# Witness acquisition material Locality investigation 001

## Question

When this Seed acquires exact material supplied by this Witness, should the
same successful acquisition establish:

```text
exact material --Locality--> this Seed
```

This investigation distinguishes that relation from the invocation Locality
where the acquisition occurs. It changes no Book, grammar, runtime, or test.

## Direct finding

The two Locality coordinates are compatible and perform different work:

```text
Witness acquisition occurrence
    Locality = invocation Locality I

exact acquired material M
    M --Locality--> this Seed
```

The first records where the acquisition occurs. The second relates the exact
acquired material to this Seed. Establishing the second relation requires no
movement to the operator Locality, no copy of `M`, and no change to its source
or provenance.

Current law does not forbid the second relation. Current law and runtime leave
the Witness road without the exact work that establishes it.

The operator acquisition road contains an explicit clause for this work.
Witness acquisition does not. The material is therefore not deliberately
hidden; it is durably acquired and available in bounded replay, while later
Measurement correctly refuses to treat availability as the missing relation.

## The `hello` case

Supplying `hello` through the current Witness road produces:

```text
external Witness supplies b"hello"
↓
invocation Locality I
↓
Witness acquisition Act occurrence
↓ Yield
exact material result carrying b"hello"
↓
bounded replay availability in I
```

It does not produce:

```text
the exact-material coordinate of that result
    --Locality-->
this Seed
```

Nothing about invocation Locality `I` conflicts with that relation. `I` can
remain the acquisition occurrence's Locality and the material can retain its
Witness source coordinates while the relation uses this Seed as its second
subject.

## What operator acquisition establishes

Active `01.Source.G` addresses exact material supplied at the operator
boundary. Current Standing carries one exact operator acquisition
Responsibility with its subject, boundary, Act, Authority, Scope, Locality,
limits, and Unknown.

Its acquisition occurrence Yields an exact material result. The same
occurrence also establishes:

```text
first subject  = that result's exact-material coordinate
relation       = Locality
second subject = this Seed
relation occurrence = that acquisition result occurrence
```

The Book keeps the material, result, relation, and occurrence distinct even
though the result occurrence also records the relation occurrence.

The machine witness agrees:

```text
01.Source.G
    subject        operator material boundary
    Responsibility preserve exact operator material
    exact Act      operator material acquisition
    relations      Yield, Locality
    result         exact operator material result
```

The runtime result reader verifies the exact material subject, `Locality`
relation, `this Seed` second subject, relation occurrence, acquisition Act,
Yield, boundary, Scope, and intact durable references before exposing the
operator result as a qualifying Measurement source.

## What Witness acquisition establishes

The supplied-material adapter first verifies:

```text
operator command occurrence
operator-to-invocation Locality result
destination invocation Locality
prior supplied occurrence references, where present
```

It then records the Witness acquisition in the destination invocation
Locality. The result preserves:

```text
exact bytes
exact Witness source boundary
known loss
command and invocation provenance
acquisition Act occurrence
Yield
result reference
Unknown
```

The result carries neither a `locality_relation` coordinate nor a relation
occurrence from its exact-material coordinate to this Seed.

More importantly, the active Book has no exact Witness-acquisition companion
to `01.Source.G`. Chapter 11 states that material supplied by this operator
and material supplied by this Witness have separate source Responsibility
branches and occurrences. It does not state the exact current-Standing
coordinates that expose the Witness branch, nor that the Witness acquisition
result occurrence establishes the material-to-this-Seed Locality relation.

The current Witness recorder begins by appending an acquisition Act occurrence
whose payload contains:

```text
responsibility = preserve exact material supplied by this Witness ...
responsible boundary = this Seed
```

Those strings are durable host testimony. They are not the exact
Responsibility branch required before the Act.

## Why the generic clauses do not complete the road

`01.Source.A` applies to supplied source coordinates generally. It says a
responsible occurrence preserves material, source role, source occurrence,
provenance, Authority, Scope, Locality, loss, limits, conflicts, and Unknown.
It also says preservation establishes no source relation.

Therefore:

```text
preserved Locality coordinate
!=
exact material --Locality--> this Seed relation occurrence
```

`06.Locality.D` establishes the operator-Locality to invocation-Locality
relation and preserves provenance from later supplied material to that road.
Its subjects are the two Localities, not `M` and this Seed. It explicitly
establishes no supplied-material Applicability, Participation, or operator
Standing copy.

`06.Locality.A` requires every exact Locality relation to carry its exact
subjects, relation occurrence, Responsibility, Act, Authority, Scope, limits,
and Unknown. Shared Locality, temporal order, source coordinates, and
multiplicity establish no relation.

Consequently none of these crossings is lawful:

```text
event.locality_identity = I
→ M --Locality--> this Seed

scope Locality label
→ M --Locality--> this Seed

command or invocation provenance
→ M --Locality--> this Seed

bounded replay availability
→ M --Locality--> this Seed

responsible-boundary string
→ exact Witness acquisition Responsibility
```

## The earliest stop

The current Witness road lacks the exact Responsibility branch before it
lacks the material Locality relation after it.

```text
exact Witness source boundary supplied to this Seed
↓
current Standing exposing exact Witness acquisition Responsibility
    NOT ESTABLISHED BY AN ACTIVE CLAUSE
↓
exact Witness acquisition Act occurrence
↓ Yield
exact material result
↓
same occurrence establishing M --Locality--> this Seed
    NOT ESTABLISHED BY AN ACTIVE CLAUSE
```

The existing runtime records the lower Act, Yield, and result as host
testimony. Adding only the Locality relation to that result would use the
result of an Act whose prior Responsibility remains unsupported.

Therefore the operator road cannot simply be copied into the Witness recorder
yet.

## Smallest lawful shape to test

The repository supports a narrow proposed shape for later Book recovery:

```text
current Standing carrying the exact Witness source-boundary coordinates
↓
exact Witness material-acquisition Responsibility
├── responsible boundary = this Seed
├── subject = exact Witness source boundary / material boundary
├── exact acquisition Act
├── Authority
├── Scope
├── invocation Locality
├── provenance
├── known loss / limits
└── Unknown
↓
acquisition Act occurrence in invocation Locality I
↓ Yield
exact material result M in I
↓
the same responsible occurrence also records
M --Locality--> this Seed
```

This shape preserves every distinction already established:

```text
invocation Locality remains I
Witness remains the source
provenance remains exact
provider read boundaries remain exact
material is not copied
material does not move to the operator Locality
acquisition result remains distinct from the Locality relation
```

The proposed shape is not active law. The exact current-Standing subject,
Authority, Scope, and limits that expose the Witness acquisition
Responsibility have not been recovered. Those positions must be established
before runtime change.

## Disposition

```text
Witness bytes durably acquired                         yes
Witness bytes available in invocation replay           yes
invocation Locality preserved                          yes
exact source boundary / provenance / known loss        yes

material copied or moved to operator Locality          no
movement required for material-to-Seed relation        no
conflict between invocation Locality and relation      no

Witness acquisition Responsibility branch in active law no
exact Authority and Scope for that branch               no
M --Locality--> this Seed relation occurrence           no
relation Standing                                       no
corpus Measurement                                      no
```

The present stop is an unfinished Witness acquisition road, not a rule that
external material must remain hidden from this Seed. The next constitutional
question is the exact current-Standing branch for Witness acquisition. Once
that branch is established, the successful acquisition occurrence can be
tested as the occurrence that also records the material-to-this-Seed Locality
relation, without movement or copying.

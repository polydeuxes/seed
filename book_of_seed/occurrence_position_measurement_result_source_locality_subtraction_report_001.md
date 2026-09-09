# Occurrence-position Measurement result source-Locality subtraction report 001

## Question

Does an occurrence-position Measurement result need to repeat the source
Locality already carried by its exact Act occurrence?

## Prior shape

The result addressed `A` and also copied:

```text
R.source_localities = [S]
A.source_locality_identity = S
```

The result reader used the result-local copy to reconstruct the finding before
following `R` to `A`.

## Falsifier

Remove only `R.source_localities`. Read `A` first, recover `S` from the exact
Act occurrence, and then validate the result's completeness boundary and
ordered findings under `S`.

Preserve:

```text
source Locality S distinct from recording Locality D
R.Locality = A.Locality = D
R → exact A
A → exact S
exact completeness boundary
ordered result-position findings
restart and current-coordinate replay
changed A.source_locality_identity refusal
```

## Result

The source Locality remains exact through:

```text
R
→ exact Act occurrence A
→ A.source_locality_identity = S
```

The durable position findings continue to be checked against the exact source
Locality and completeness boundary. Removing the result-local copy loses no
independent distinction.

## Disposition

```text
source Locality on A           retained
R → A occurrence address       retained
copied source Locality on R     withdrawn
recording Locality on A and R   retained
```

No Act, result, relation, Locality, identity, or admitted word is added.

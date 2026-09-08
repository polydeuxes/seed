# Locality continuation exact-Act identity subtraction report 001

## Question

Does `06.Locality.B` require an opaque `continuation_act_identity` in addition
to its Act coordinate and actual Act occurrence?

## Prior shape

```text
Act occurrence A
    act                       source-boundary Locality relation
    continuation_act_identity minted token
    Event.identity

relation result R
    exact_act                 source-boundary Locality relation
    continuation_act_identity copied token
    Act occurrence            A.identity
```

No occurrence outside this authored copy chain supplied the token value.

## Falsifier

Remove only the opaque token. Preserve:

```text
exact source Locality and cut
Act coordinate under separate pressure
fresh destination Locality
actual Act occurrence
actual result occurrence
Act-to-result reference
Act-before-result order
one result per Act
equal source-cut non-collapse
restart and replay
```

## Result

The subtraction passes.

Separate Acts over the same exact source cut remain separate through their
actual event identities and destination Localities. Separate results remain
separate through their actual result occurrences.

The opaque token could be changed consistently across the Act and result
without any independent coordinate determining which value was exact. It was
therefore an authored identity chain, not another Act distinction.

## Boundary

This result does not save or withdraw the current Act phrase:

```text
source-boundary Locality relation
```

That phrase may narrate the source subject and relation result rather than
name an exact Act. It requires a separate Act-word falsifier. Removing an
opaque identity does not determine what Act coordinate, if any, survives.

## Disposition

```text
opaque exact-Act identity      withdrawn
actual Act Event.identity      retained
actual result Event.identity   retained
source coordinates             retained
destination Locality           retained
Act phrase                      unresolved
```

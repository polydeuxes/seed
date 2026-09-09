# Byte Measurement result source-Localities copy census 001

## Question

Must the plain-byte Measurement result copy its source Localities when it
already addresses the exact Act occurrence carrying them?

This census changes no runtime road, Book clause, Witness Grammar, admission,
Act, result, or occurrence.

## Current shape

```text
A.source_localities

R.act_occurrence_event_identity = A.identity
R.source_localities = copy of A.source_localities
```

The result reader resolves and validates A before accepting R. A's exact source
Localities are required to reconstruct the bounded source material and validate
A's subject references.

One downstream result-position reader currently reads the copied list from R.
It can instead follow the exact R-to-A occurrence reference after R has been
validated.

## Attempted distinction

No control holds A fixed while giving R a different lawful source-Localities
coordinate. Changing the copied list makes R disagree with the source read and
refuses. The copy provides no independently variable relation.

## Required falsifier

Remove only:

```text
R.source_localities
```

Retain:

```text
A.source_localities
R → A occurrence reference
exact material-result subjects
source completeness boundary
recording cut
Act and result Localities
all byte findings
restart and current-coordinate replay
downstream byte-pair Measurement and Movement
```

Changing A's source Localities must continue to invalidate R. Reintroducing the
copied field on R must be refused as an extra coordinate.

## Family boundary

This census addresses only the plain-byte result copy. The completeness-boundary
copy and every other result family remain unchanged.

## Disposition

```text
source Localities on exact Act A          retained
R → A occurrence reference               retained
source Localities copied onto R           failed census
result source-Localities subtraction      next falsifier
```

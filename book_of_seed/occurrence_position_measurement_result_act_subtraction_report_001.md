# Occurrence-position Measurement result-Act subtraction report 001

## Question

Does an occurrence-position Measurement result need to repeat the exact Act
word carried by its addressed Act occurrence?

## Prior shape

After the binding occurrence was removed, the result still recorded:

```text
exact_act = occurrence position Measurement
act_occurrence_event_identity = A
```

The reader first followed `A`, validated its exact Act and binding coordinates,
then separately required the copied result field to contain the same wording.

## Falsifier

Remove only the result's `exact_act` coordinate and preserve:

```text
R → exact Act occurrence A
A → exact Measurement Act
A → exact subjects and boundaries
one R per A
ordered result-position findings
source and recording Locality distinctions
restart and current-coordinate replay
changed A.act refusal
```

## Result

The exact Act remains recoverable through the actual Act occurrence:

```text
R
→ act_occurrence_event_identity = A
→ A.act = occurrence position Measurement
```

Changing the Act coordinate on `A` invalidates `R`; no result-local copy is
needed to retain the distinction.

## Disposition

```text
exact Act on A             retained
actual Act occurrence A   retained
R → A occurrence address  retained
copied exact Act on R      withdrawn
```

No Act, result, relation, identity, or admitted word is added.

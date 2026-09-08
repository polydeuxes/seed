# Compare-Distinction Measurement result subject-copy subtraction report 001

## Question

Must the Compare-Distinction Measurement result repeat the subject reference
carried by its exact Act occurrence?

## Prior shape

```text
Act occurrence A
    subject_reference = exact Compare result C

result R
    act_occurrence_event_identity = A.identity
    subject_reference = copied C
    source_result_occurrence_identity = copied C
```

The result serialized the same source occurrence in two fields while already
addressing the Act occurrence that carries the subject.

## Falsifier

Remove the nested `R.subject_reference` only. Retain the flat source coordinate
until its active consumers can be pressure-tested independently. Preserve:

```text
R addresses A.identity
A addresses exact C
changed source coordinates refuse
A before R
complete Distinction findings
current-coordinate replay
restart
```

## Result

No active reader or later Act requires the nested result copy. The exact subject
remains on A, and R reaches it through the exact Act-occurrence reference.

## Disposition

```text
subject on Act occurrence             retained
Act-occurrence reference on result    retained
nested subject copy on result         withdrawn
flat source-result coordinate         retained under separate pressure
```

No binding occurrence, Applicability, Yield, result, or relation is added.

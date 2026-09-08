# Compare-Distinction Measurement result source-copy subtraction report 001

## Question

Must the Compare-Distinction Measurement result serialize its exact source
occurrence when its addressed Act occurrence already carries that subject?

## Prior shape

```text
Act occurrence A
    subject = exact Compare result C

result R
    Act occurrence = A.identity
    source_result_occurrence_identity = C.identity
    completeness_boundary.source_result_occurrence_identity = C.identity
```

The result copied the same source occurrence twice in addition to its exact
Act-occurrence reference.

## Falsifier

Remove both durable copies of `C.identity`. Preserve the exact source and full
completeness coordinates through:

```text
R
→ exact Act occurrence A
→ exact subject C

R.completeness_boundary.distinction_count
+ R.findings
+ A.subject
→ exact completeness reading
```

Also preserve automatic Measurement discovery, current-coordinate replay,
restart, later Distinction-result composition, source mutation refusal, and
every exact-material reading.

## Result

The durable result retains its finding count and findings. Its exact source is
recovered through the Act occurrence. The result reader returns the complete
source and boundary coordinates reconstructed from that exact chain.

The automatic Measurement road now uses the exact result reader rather than
inspecting copied result material.

## Disposition

```text
subject on Act occurrence                    retained
Act-occurrence reference on result           retained
result finding count and findings            retained
flat copied source occurrence on result      withdrawn
copied source in completeness boundary       withdrawn
reconstructed exact source/boundary reading  retained
```

No source occurrence, Act, result, binding occurrence, Applicability, Yield, or
relation is added.

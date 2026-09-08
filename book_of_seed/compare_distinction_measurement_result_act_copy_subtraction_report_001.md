# Compare-Distinction Measurement result Act-copy subtraction report 001

## Question

Must the Compare-Distinction Measurement result repeat the exact Act that its
addressed Act occurrence already carries?

## Prior shape

```text
result R
    act_occurrence_event_identity = A.identity
    exact_act = Measurement

Act occurrence A
    act = Measurement
```

The result serialized the Act coordinate twice: once as an exact occurrence
reference and again as copied material.

## Falsifier

Remove `R.exact_act` while preserving:

```text
R addresses exact Act occurrence A
A carries the exact Measurement Act
changed A.Act refuses R
A before R
one result per A
complete Distinction findings
current-coordinate replay
restart
```

## Result

The result reaches the exact Act through `A.identity`. Changing the Act on A to
`Compare` still makes R refuse. The copied Act field adds no independently
variable result coordinate.

## Disposition

```text
exact Act on Act occurrence       retained
exact Act-occurrence reference    retained
copied exact Act on result        withdrawn
```

The Act occurrence and result occurrence remain separate. No binding
occurrence, Applicability, Yield, result, or relation is added.

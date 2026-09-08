# Compare-Distinction Measurement result completeness-copy subtraction report 001

## Question

Must the durable Compare-Distinction Measurement result serialize a count of
the findings whose exact completeness is already validated from its subject?

## Prior shape

After source-copy subtraction, the durable result still carried:

```text
completeness_boundary.distinction_count = len(findings)
findings = exact Distinctions of subject C
Act occurrence = A.identity
A.subject = C
```

The stored count was derived entirely from the stored findings. The source
portion of the completeness coordinate was already recovered through A.

## Falsifier

Remove the durable completeness copy while preserving:

```text
R → exact Act occurrence A → exact subject C
every exact Distinction of C
no omitted, added, changed, or reordered finding
exact reconstructed completeness boundary
current-coordinate replay
restart
```

## Result

The result reader derives the expected Distinctions from C and requires the
durable finding list to equal that exact ordered structure. It returns:

```text
source result occurrence = C.identity
distinction count = len(exact Distinctions of C)
```

as the exact completeness reading. The copied count adds no independently
variable durable coordinate.

## Disposition

```text
exact subject through Act occurrence        retained
exact ordered findings                      retained
exact reconstructed completeness boundary  retained
copied durable finding count                withdrawn
```

Complete result structure remains distinct from exhaustive coverage of a
bounded subject set. No Act, result, boundary, binding occurrence,
Applicability, Yield, or relation is added.

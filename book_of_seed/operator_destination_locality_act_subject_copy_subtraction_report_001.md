# Operator destination Locality Act-subject copy subtraction report 001

## Question

Does the `06.Locality.D` Act need two fields containing the same operator
material result occurrence identity?

## Prior shape

```text
operator_material_occurrence_reference       Q.identity
operator_material_result_occurrence_identity Q.identity
```

The source road records the exact material result as occurrence `Q`. The
Locality Act copied that identity under two field names.

## Falsifier

Remove only `operator_material_result_occurrence_identity` from the Act.
Preserve the exact operator material occurrence reference and require the Act
reader to recover and validate the same exact material result through it.

The subtraction must preserve:

```text
operator material source-family validation
exact material-result validation
operator occurrence identity
source Locality
source cut
Locality Act
destination Locality
Act and relation-result occurrences
separate equal-content occurrences
restart and current-coordinate replay
```

## Result

The subtraction passes.

`operator_material_occurrence_reference` addresses `Q`. Reading `Q` validates
that it is the exact operator material result occurrence. A second copy of
`Q.identity` does not add a result coordinate or distinguish two possible
subjects.

The relation result continues to address the operator occurrence for separate
pressure. This change concerns only the duplicate field on the Act.

## Disposition

```text
Act operator occurrence reference       retained
Act copied material-result identity      withdrawn
exact operator material result reading  retained
result operator occurrence reference    retained for separate pressure
```

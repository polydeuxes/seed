# Material result Locality census 001

## Question

Does one exact material result require a separate material-to-this-Seed
Locality relation in addition to the result occurrence and its exact Locality?

This census concerns the internal coordinates of already recorded material
results. It does not investigate an external Witness or Emission boundary.

## Recorded material result

Operator and Witness material source roads record one exact result occurrence
with:

```text
exact material
source boundary
source occurrence references where established
exact event Locality
source Act occurrence
Yield
result identity
```

The result event therefore already has an exact durable Locality coordinate.

## Nested relation material

The same result material also records:

```text
locality_relation:
    first subject  = this result's exact_material coordinate
    relation       = locality
    second subject = this Seed
    occurrence     = this same result occurrence
```

The operator source road additionally copies the same result identity into a
top-level `locality_relation_occurrence_identity` coordinate.

No separate Locality binding, Locality Act occurrence, Yield, result, event
kind, or reader occurrence exists for this nested material. The source Act and
Yield establish the material result. The nested relation names that result
event as its own occurrence.

## Current-coordinate projection

The current-coordinate reader records the result in
`material_result_occurrences`, then records the nested dictionary again in
`material_locality_relation_occurrences` under the same event identity.

Later Measurement roads either:

- ask a Boolean reader to validate the fixed nested dictionary; or
- reconstruct that same dictionary from the material-result event identity and
  compare it with the projected copy.

No inspected consumer addresses a separately occurring relation or permits the
relation subjects, relation occurrence, or result Locality to vary
independently.

## Book pressure

`01.Source.G` says the Locality relation is separate from the source-boundary
Act occurrence, material, and result. The runtime instead uses the exact
material result occurrence as the relation occurrence.

The two claims cannot both remain exact.

## Subtraction order

The smallest tests are:

```text
top-level copied relation occurrence identity
→ remove first

nested relation dictionary
→ preserve exact result Locality and source physiology

material Locality relation current-coordinate bucket
→ remove only after every live consumer reads the exact result coordinates
```

No replacement relation or bucket is proposed.

## Current finding

The top-level copied occurrence identity was removed first. Operator and
Witness material source roads then removed the nested relation independently.
Each result now resolves its exact Locality from the durable event coordinate
and its intact source Act and Yield.

The current-coordinate `material_locality_relation_occurrences` bucket then
contained only the identities already present in `material_result_occurrences`.
It was removed. Declared Measurement now addresses the exact material result
occurrences at the bounded read's exact Locality without a second membership
test.

The active Book no longer claims a separate material-to-this-Seed Locality
relation. Locality relations with independently recorded result occurrences
remain unchanged.

```text
exact material result occurrence
+ exact event Locality
→ exact material result at that Locality

no separate relation occurrence
→ no relation wrapper
→ no relation bucket
```

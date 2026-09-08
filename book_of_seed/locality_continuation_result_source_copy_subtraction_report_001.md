# Locality continuation result-source copy subtraction report 001

## Question

Must the `06.Locality.B` relation result copy the exact source-coordinate
reference carried by its Preservation Act occurrence?

## Prior shape

```text
Preservation Act occurrence A
    source-coordinate reference S

Locality relation result R
    Act occurrence A
    source-coordinate reference S
```

## Falsifier

Remove only the durable `S` copy from `R`. Preserve `R → A → S`, and return
the exact source coordinates through that reference chain when reading the
result.

## Result

The subtraction passes.

The result addresses its exact Act occurrence. The Act contains the exact
source Locality and through-occurrence boundary. Reading the result follows
and validates those coordinates before returning them.

A source boundary substituted after the Act still refuses through the Act
reader. Direct continuation from a prior relation result, restart, and
current-coordinate replay remain unchanged.

## Disposition

```text
source coordinates on Act occurrence retained
result → Act occurrence           retained
copied source coordinates on result withdrawn
derived result source reading     retained
result destination copy           unresolved
```

# `failure` admission census 001

## Question

Does active Emission law contain an exact coordinate that distinguishes a
`failure` Act occurrence and result from another emission Act occurrence and
result?

## Active claim

`07.Emission.C` previously stated:

```text
failure
→ separate Act occurrence
→ separate result
→ reported count coordinate
```

Occurrence and result nonidentity are exact. A reported count can also be an
exact result coordinate. None of those coordinates says that the occurrence
failed.

The same shape can hold for two successful boundary writes:

```text
separate emission Act occurrences
separate results
separate reported counts
```

Thus `separate` and `reported count` cannot supply the missing outcome
distinction.

## Pressure cases

The following states must not collapse:

```text
no Act occurrence
Act occurrence with no result occurrence
result reporting zero accepted material
result reporting less material than was supplied
result reporting all accepted material
later separate Act occurrence
```

Active Emission law has exact coordinates for the accepted material and the
count reported by the destination boundary. It has no active relation comparing
that count with a supplied or accepted count, no exact failure result kind, and
no recorded failure occurrence that supplies such a discriminator.

Absence of a result cannot stand for failure: Seed already preserves stoppable
Act-without-result states elsewhere. A later separate occurrence cannot stand
for failure either: occurrence order and nonidentity do not classify its
outcome.

## Historical wording

An earlier Emission account described a boundary reporting less material than
was accepted. That exact comparison is not present in active law. Retaining the
word `failure` after its discriminator disappeared lets the classification
label testify for itself.

## Rosetta boundary

Ordinary `fail`, `fails`, `failed`, and `failure` remain admitted to Rosetta.
They can translate context-specific physiology such as:

```text
exact Act occurrence
+ exact result occurrence
+ exact outcome coordinate
+ exact source and occurrence references
```

No generic Failure occurrence or result follows from those words. The relevant
outcome coordinate must be named by the context that supplies it.

## Disposition

```text
failure as a Book-wide result class       withdrawn
separate Act/result occurrence identity   retained where exact
accepted material                         retained
destination-reported count                retained
Rosetta failure forms                     retained as composites
exact negative Emission outcome           not recovered
```

No runtime road, occurrence kind, Act, result, relation, or coordinate is
added.

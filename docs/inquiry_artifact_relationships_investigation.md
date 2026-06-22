# Inquiry Artifact Relationships Investigation

## Central finding

Repository evidence supports a cautious answer:

```text
artifact visibility exists

but artifact relationships are only partially repository-visible
```

The current `seed --inquiry-artifacts` surface makes artifact visibility visible.

It does not yet make artifact relationships, attachment, lineage, or structure visible as first-class repository output.

## Current visibility baseline

The implementation-backed artifact visibility model is:

```text
unknown              repository_visible
boundary             repository_visible

pressure             partially_visible
finding              partially_visible
gap                  partially_visible

supported_conclusion document_visible
unsupported_conclusion document_visible
open_question        document_visible
```

This supports artifact visibility.

It does not by itself support artifact relationship visibility.

## Implementation-backed artifact relationships today

The strongest implementation-backed relationships are endpoint relationships rather than full inquiry-artifact relationships.

Examples:

```text
unknown
    -> unsupported domain

boundary
    -> read-only behavior

boundary
    -> mutation boundary

pressure
    -> capability relationship

pressure
    -> operational meaning
```

These are repository-visible through existing surfaces.

However they are not yet evidence that relationships such as:

```text
gap
    -> pressure

pressure
    -> finding

finding
    -> boundary

boundary
    -> unknown
```

are implementation-backed artifact relationships.

Those richer relationships remain mostly investigation-backed and human-interpreted.

## Repository-visible relationships

Current repository-visible relationships include:

```text
artifact
    -> visibility class

unknown
    -> repository_visible

boundary
    -> repository_visible

pressure
    -> partially_visible

finding
    -> partially_visible

gap
    -> partially_visible
```

and selected endpoint relations inside implementation-backed surfaces:

```text
capability pressure
    -> operational meaning

unsupported domain
    -> unknown

surface behavior
    -> boundary
```

These are meaningful, but they are not yet full artifact-to-artifact structure.

## Human-interpreted relationships

The following relationships currently depend heavily on humans reading investigation chains:

```text
gap
    -> pressure

pressure
    -> finding

finding
    -> boundary

boundary
    -> unknown

finding
    -> supported conclusion

supported conclusion
    -> new pressure

open question
    -> next investigation
```

These appear repeatedly and are useful.

But current evidence does not show them as repository-visible relationships without prose interpretation.

## Do inquiry artifacts behave as labels or related units?

Repository evidence supports both, depending on visibility level.

### As labels

The `--inquiry-artifacts` surface currently exposes artifact categories and visibility status.

That is label-like.

### As related units

Investigation chains repeatedly show artifacts behaving as related units.

Examples:

```text
gap produces pressure

pressure produces finding

finding produces boundary

boundary preserves unknown
```

This related-unit behavior is stronger in documents than in implementation-backed surfaces.

## Structural meaning indicators

Evidence that an artifact relationship is structurally meaningful would include:

```text
repeatability
multiple investigations
multiple surfaces
multiple diagnostics
stable attachment behavior
stable recurrence
visibility without prose interpretation
```

Current status:

```text
repeatability              supported
multiple investigations     supported
multiple surfaces           partially supported
stable attachment behavior  human-interpreted
visibility without prose    weak for artifact-to-artifact relationships
```

## Counterexamples

### Visibility without relationship evidence

The clearest example is:

```text
artifact
    -> visibility class
```

This provides useful visibility, but does not prove artifact structure.

### Relationships supported by prose only

The strongest examples are:

```text
finding
    -> supported conclusion

supported conclusion
    -> new pressure

open question
    -> next investigation
```

These relationships are important, but remain document-visible.

### Partial repository relationship evidence

Examples:

```text
unknown
    -> unsupported domain

boundary
    -> read-only behavior

pressure
    -> capability meaning
```

These show relationship-like structure, but not a general artifact relationship model.

## Historical perspective

The current situation resembles:

```text
entity visibility
    before
relationship visibility
```

or:

```text
artifact visibility
    before
artifact structure
```

This resembles earlier repository-domain evolution where visibility appeared before richer relationship structure.

That analogy is useful but limited.

It does not imply implementation work.

## Important distinctions

### Artifact

A recurring inquiry unit such as unknown, boundary, pressure, finding, or gap.

### Artifact visibility

Whether that unit is repository-visible, partially visible, or document-visible.

### Artifact relationship

A connection between artifacts.

### Artifact attachment

A local qualifying relationship, such as boundary attaching to finding.

### Artifact lineage

A longer relationship across inquiry movement, such as conclusion leading to new pressure.

### Artifact structure

Repeatable relationship, attachment, or lineage behavior that becomes stable enough to be visible beyond prose.

These are not equivalent.

## Supported conclusions

1. Repository-visible artifact visibility exists today.
2. Repository-visible artifact relationships exist only partially today.
3. The strongest implementation-backed relationships are endpoint relations involving unknown, boundary, and pressure.
4. Richer artifact-to-artifact relationships remain mostly human-interpreted.
5. Inquiry artifacts behave as related units in investigation chains, but as mostly labels in the current visibility surface.
6. Repository evidence supports moving conceptually from artifact visibility toward artifact structure, but does not show that structure as implemented.
7. The current situation resembles visibility before relationship visibility in earlier repository domains.

## Unsupported conclusions

- Artifact relationships are fully repository-visible today.
- Attachment is implementation-backed today.
- Lineage is implementation-backed today.
- The current inquiry-artifacts surface implements artifact structure.
- Prose ingestion is required for the next investigation step.
- Inquiry graphs should be implemented.
- The candidate relationships are complete or canonical.

## Open questions

- Which artifact relationship can become repository-visible first?
- Is unknown-to-boundary stronger than boundary-to-unknown?
- Does gap-to-pressure have enough evidence to become structurally meaningful?
- Are supported conclusions too document-visible to participate in artifact structure today?
- What distinguishes stable attachment from repeated prose association?
- Can artifact lineage be visible without inquiry movement visibility?

## Acceptance answers

### Do repository-visible artifact relationships already exist?

Partially. Endpoint relations involving unknown, boundary, and pressure are visible, but richer artifact-to-artifact relationships remain mostly human-interpreted.

### Which artifact relationships are implementation-backed?

The strongest are unknown-to-unsupported-domain, boundary-to-read-only or mutation behavior, and pressure-to-capability meaning. Candidate relationships such as gap-to-pressure or finding-to-boundary are not yet implementation-backed as artifact relationships.

### Which relationships remain human interpreted?

Gap-to-pressure, pressure-to-finding, finding-to-boundary, boundary-to-unknown, finding-to-supported-conclusion, supported-conclusion-to-new-pressure, and open-question-to-next-investigation remain mostly human-interpreted.

### Do inquiry artifacts behave more like isolated labels or related units?

The current surface exposes them mostly as labels with visibility classes. Investigation chains show them behaving as related units.

### Does repository evidence support moving from artifact visibility toward artifact structure?

Yes, as an investigation direction. Visibility, recurrence, and partial endpoint relationships support the idea, but artifact structure is not currently implementation-backed.
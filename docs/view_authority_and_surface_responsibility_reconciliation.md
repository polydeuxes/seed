# View Authority And Surface Responsibility Reconciliation

## Purpose

This document reconciles the intended responsibilities of Seed read surfaces before modifying existing output.

The motivating finding is:

```text
Many output disagreements are actually authority disagreements.
```

A proposed formatting change may appear reasonable while violating the purpose of the view.

## Central Question

Before changing a view, determine:

```text
Who is the consumer?

What authority does the view own?

What information must remain visible?

What information may be summarized?
```

## Observation

Recent local-host audits exposed an apparent defect:

```text
current-facts output appears duplicated.
```

Investigation revealed a deeper issue.

The repository already preserves scoped dimensions.

The disagreement is therefore not simply about formatting.

It is about the responsibility of the view.

## Candidate Surface Taxonomy

A useful distinction is:

```text
Evidence Surfaces
        ≠
Interpretation Surfaces
        ≠
Integrity Surfaces
        ≠
Navigation Surfaces
```

These consumers and goals differ.

## Evidence Surfaces

Primary question:

```text
What does Seed currently know?
```

Candidate examples:

```text
current-facts
current-observations
fact-support
best-fact
```

Properties:

```text
Inspectability
Traceability
Completeness
Minimal interpretation
```

Should generally avoid:

```text
Aggressive summarization
Hidden evidence
Opinionated grouping
```

## Interpretation Surfaces

Primary question:

```text
What should the operator understand?
```

Candidate examples:

```text
impact
entity views
future summaries
```

Properties:

```text
Grouping
Organization
Summarization
Human readability
```

May intentionally reduce detail.

Must preserve a path back to evidence.

## Integrity Surfaces

Primary question:

```text
Where is Seed uncertain?
```

Candidate examples:

```text
contradictions
fact conflicts
graph issues
unsupported facts
capability status
```

Properties:

```text
Uncertainty visibility
Conflict visibility
Missing support visibility
```

## Navigation Surfaces

Primary question:

```text
Where should the operator go next?
```

Candidate examples:

```text
integrity summary
inventory navigation
future dashboards
```

Properties:

```text
Discovery
Routing
Surface selection
```

## Important Boundary

A recurring mistake is:

```text
Interpretation concerns
        ↓
Applied to evidence surfaces
```

Example:

```text
The output is noisy.
```

Potential response:

```text
Hide evidence.
```

This may improve readability while weakening inspectability.

## Local Host Observation Example

Observed concern:

```text
mount output is noisy.
```

For an interpretation surface:

```text
Collapse docker mounts.
Group overlays.
Summarize.
```

may be appropriate.

For an evidence surface:

```text
Preserve visibility.
Preserve grepability.
Preserve scope.
```

may be more appropriate.

The correct solution depends on the authority of the view.

## Surface Consumer Model

A candidate model:

| Consumer | Primary Need |
| --- | --- |
| Operator | Understanding |
| Developer | Debugging |
| Auditor | Evidence inspection |
| Automation | Stable machine-readable structure |
| Reconciliation work | Provenance and support |

Different consumers justify different surfaces.

## Relationship To Boundary Preservation

This finding is another example of boundary preservation.

Examples:

```text
Evidence
    ≠
Interpretation

Inspection
    ≠
Summary

Completeness
    ≠
Readability
```

Crossing these boundaries without intent can degrade a surface.

## Relationship To Supported Ground

A view should not imply conclusions beyond its authority.

Examples:

```text
Listener facts
    ≠
Availability

Availability
    ≠
Health

Health
    ≠
Ownership
```

A surface should clearly communicate what it owns.

## Candidate Current Classification

Current working classification:

```text
current-facts
    = evidence surface

current-observations
    = evidence surface

fact-support
    = justification surface

impact
    = interpretation surface

integrity summary
    = navigation surface

conflicts / contradictions
    = integrity surfaces
```

This classification remains subject to future review.

## Current Conclusion

Before modifying a view:

```text
Determine its authority.
```

Many output disputes are easier to resolve once the responsibility of the surface is explicit.

The immediate local-host finding suggests:

```text
current-facts should become a better evidence surface.
```

It does not necessarily imply:

```text
current-facts should become an interpretation surface.
```

Those responsibilities should remain distinct unless deliberately reconciled.

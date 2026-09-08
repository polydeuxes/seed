# Read Model Inventory And Authority Reconciliation

## Purpose

This document inventories major Seed read surfaces and assigns provisional authority responsibilities.

The goal is to prevent accidental boundary violations when evolving output formats, projections, summaries, dashboards, and operator tooling.

## Motivation

Recent local-host observation audits demonstrated that output disagreements often arise from unclear surface responsibilities.

Example:

```text
Should current-facts summarize noisy mount data?
```

The answer depends on:

```text
What authority does current-facts own?
```

rather than on formatting preference alone.

## Core Finding

Read surfaces are not interchangeable.

Different surfaces exist to answer different questions.

A useful inventory therefore classifies surfaces by:

```text
Primary consumer
Primary question
Authority
Non-authority
```

## Evidence Inspection Surfaces

### current-facts

Primary consumer:

```text
Operator
Developer
Auditor
```

Primary question:

```text
What facts currently exist?
```

Authority:

```text
Fact visibility
Fact inspection
Fact inventory
```

Non-authority:

```text
Interpretation
Prioritization
Executive summary
Health conclusions
```

Properties:

```text
Complete
Inspectable
Greppable
Deterministic
```

### current-observations

Primary question:

```text
What observations have been collected?
```

Authority:

```text
Observation visibility
Observation inspection
```

Non-authority:

```text
Fact reconciliation
Interpretation
```

Properties:

```text
Raw
Evidence-oriented
```

## Justification Surfaces

### fact-support

Primary question:

```text
Why does Seed believe this fact?
```

Authority:

```text
Support visibility
Evidence chains
Provenance
```

Non-authority:

```text
Operational recommendations
Entity summaries
```

### best-fact

Primary question:

```text
Which supported fact currently wins?
```

Authority:

```text
Support comparison
Selection visibility
```

Non-authority:

```text
High-level interpretation
```

## Interpretation Surfaces

### impact

Primary question:

```text
What matters about this entity?
```

Authority:

```text
Grouping
Context
Relationship organization
Human readability
```

Non-authority:

```text
Hidden evidence
Unsupported conclusions
```

Properties:

```text
Summarized
Curated
Operator-oriented
```

### Future Entity Summaries

Primary question:

```text
How should a human understand this entity?
```

Authority:

```text
Interpretation
Organization
```

Must preserve navigation paths back to evidence.

## Integrity Surfaces

### contradictions

Primary question:

```text
What cannot simultaneously be true?
```

Authority:

```text
Conflict visibility
```

### fact-conflicts

Primary question:

```text
What competing facts exist?
```

Authority:

```text
Competing support visibility
```

### graph-issues

Primary question:

```text
What graph integrity problems exist?
```

Authority:

```text
Structural integrity visibility
```

### unsupported-facts

Primary question:

```text
Which facts lack support?
```

Authority:

```text
Support sufficiency visibility
```

## Navigation Surfaces

### integrity-summary

Primary question:

```text
Where should the operator investigate next?
```

Authority:

```text
Navigation
Discovery
Routing
```

Non-authority:

```text
Raw evidence replacement
```

## Relationship To Local Host Findings

The local-host observation audits suggest:

```text
current-facts
```

should primarily remain:

```text
Evidence Inspection Surface
```

This implies:

```text
Expose scope.
Preserve inspectability.
Preserve grepability.
Avoid interpretation.
```

The audits do not imply:

```text
Collapse data.
Summarize aggressively.
Hide evidence.
```

Those responsibilities belong more naturally to interpretation surfaces.

## Surface Evolution Rule

Before changing a read model:

```text
Identify authority.
```

Then ask:

```text
Does this change strengthen that authority?
```

If not, the change may belong in a different surface.

## Current Working Classification

```text
current-facts          → evidence inspection
current-observations   → evidence inspection
fact-support           → justification
best-fact              → justification
impact                 → interpretation
contradictions         → integrity
fact-conflicts         → integrity
graph-issues           → integrity
unsupported-facts      → integrity
integrity-summary      → navigation
```

This inventory is provisional and may evolve as new read models emerge.

## Current Conclusion

Many output disagreements become easier to resolve once surface authority is explicit.

The immediate local-host work should therefore be evaluated against the authority of:

```text
current-facts
```

as an evidence inspection surface rather than as a human-oriented interpretation surface.

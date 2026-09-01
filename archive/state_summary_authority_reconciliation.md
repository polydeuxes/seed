# State Summary Authority Reconciliation

## Purpose

This audit reviews the responsibility and authority of the State Summary surface.

The triggering observation was that State Summary currently contains a mixture of inventory information, integrity information, operational information, and knowledge information.

The central question is:

```text
What is State Summary supposed to be?
```

## Observed Output Categories

Current State Summary contains examples of:

### Inventory

```text
Facts
Observations
Requirements
Capabilities
Entities
```

### Integrity

```text
Conflicts
Stale facts
Graph issues
```

### Observation Accounting

```text
Observation sources
Discovery counts
```

### Knowledge Inventory

```text
Top entities
Aliases
```

### Operational Status

```text
Availability counts
```

These are different concerns.

## Finding: State Summary Is Not Impact

A useful distinction:

```text
State Summary
        ≠
Impact
```

Impact answers:

```text
What matters about this entity?
```

State Summary appears to answer:

```text
What is the current shape of the knowledge system?
```

This is a repository-level perspective rather than an entity-level perspective.

## Finding: State Summary Is Closest To A Knowledge Inventory Surface

The strongest common thread is:

```text
Inventory
```

Examples:

```text
Entity count
Fact count
Observation count
Requirement count
Capability count
Observation source counts
```

These describe the contents of the projected state.

They do not primarily describe entities.

## Finding: Inventory Is Not Knowledge

A useful distinction:

```text
Row counts
        ≠
Knowledge
```

Examples:

```text
1233 facts
1233 observations
```

provide inventory information.

They do not directly explain what Seed has learned.

Knowledge-oriented examples would be:

```text
1 host observed
14 storage devices
52 listening endpoints
28 collapsed interfaces
```

These describe learned structure rather than inventory volume.

A future State Summary may need a clearer distinction between:

```text
Inventory metrics
Knowledge metrics
```

## Finding: Durable Facts Versus Measurements May Be Architecturally Important

One of the most interesting current distinctions is:

```text
Durable facts
Measurement current samples
```

This exposes a conceptual boundary:

```text
Knowledge
        ≠
Measurement
```

The distinction may become increasingly important as additional observation sources arrive.

Examples:

```text
Host inventory
Package inventory
Capabilities
Purpose
Users
```

versus:

```text
CPU utilization
Memory usage
Latency
Temperature
Disk utilization
```

These have different freshness and lifecycle characteristics.

## Finding: Observation Accounting Is Under-Specified

Current output includes:

```text
Observation sources
```

However:

```text
1233 discovery observations
```

is difficult to interpret.

Questions arise:

```text
What counts as discovery?
Why is discovery equal to total observations?
What additional observation sources are expected?
```

The current output may be correct but lacks explanatory context.

## Finding: Availability Authority Is Unclear

Current output includes:

```text
up
down
unknown
```

However recent audits repeatedly established:

```text
availability is not inferred
```

This raises a responsibility question:

```text
What authority does State Summary have regarding availability?
```

The counts may represent future capability placeholders rather than current knowledge.

## Finding: State Summary May Be The Actual Overview Surface

A surprising observation emerged during review.

State Summary already exhibits many characteristics of an overview:

```text
Compact
Repository-wide
Inventory-oriented
Integrity-aware
Navigation-friendly
```

Operator reaction to State Summary was significantly more positive than operator reaction to Impact.

This suggests:

```text
State Summary
    may already be functioning as
    the repository overview surface
```

while Impact is still evolving.

## Candidate Surface Classification

Current working classification:

```text
State Summary
    = knowledge inventory surface
```

Primary questions:

```text
How large is the knowledge base?
What kinds of information exist?
What integrity concerns exist?
What observation sources contributed?
```

Non-authority:

```text
Entity interpretation
Operational dashboards
Health summaries
```

## Relationship To Other Surfaces

```text
State Summary
    → repository overview / inventory

Integrity Summary
    → navigation

Impact
    → entity overview

Impact Section
    → entity drilldown

Current Facts
    → evidence inspection

Fact Support
    → provenance
```

Each surface answers a different question.

## Future Questions

Future work may need to decide:

```text
Should State Summary emphasize inventory?
Should it emphasize knowledge?
Should inventory and knowledge be separate summaries?
```

This audit does not resolve those questions.

It preserves them.

## Current Conclusion

State Summary currently appears closest to a repository-level knowledge inventory and overview surface.

The most important unresolved questions concern:

```text
Inventory versus knowledge
Durable facts versus measurements
Observation accounting semantics
Availability authority
```

Future evolution should clarify these responsibilities before expanding the surface further.

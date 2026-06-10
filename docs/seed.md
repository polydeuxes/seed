# Seed

## Seed Is

Seed is a system for preserving observations, accumulating evidence, normalizing justified claims, connecting justified relationships, selecting explainable projections, and escalating to the operator when authority is required.

Seed does not begin with truth.

Seed begins with observation.

---

## Core Thesis

Seed is claim-centric.

It preserves observations, accumulates evidence, normalizes justified claims, connects justified relationships, selects explainable projections, and escalates to the operator when authority is required.

The detailed conceptual paths are shown below

---

## Architecture Shape

These are conceptual architecture paths, not rigid runtime pipelines. They summarize how Seed's major concepts relate while preserving the boundaries established by the reconciliation documents.

### Knowledge Plane

```text
Observation
        ↓
Evidence
        ↓
Claim
        ↓
Fact / Relationship
        ↓
Projection
```

Claims are the center. Facts are normalized claim forms. Relationships are normalized connection claims. Projections select and communicate preserved knowledge.

### Claim Forms

```text
Claim
├── Fact
├── Relationship
├── Assessment
├── Recommendation
├── Decision
├── Causal Claim
└── Historical Claim
```

Not every claim is a fact. A fact is one normalized claim form. Relationships, assessments, recommendations, decisions, causal claims, and historical claims have their own boundaries.

### Temporal Plane

```text
Event
        ↓
Change
        ↓
State
        ↓
Projection
```

Events describe occurrences. Changes describe transitions. State describes selected conditions. History survives current-state change.

### Operator / Purpose Plane

```text
Operator Intent
        ↓
Question
        ↓
Goal
        ↓
Consequence
        ↓
Recommendation
        ↓
Decision
```

Operators are intent-centric. Questions bridge operator intent and Seed's claim-centric knowledge. Goals are operator-owned. Recommendations explain both evidence path and goal relevance path.

### Capability / Execution Plane

```text
Capability
        ↓
Command
        ↓
Execution
        ↓
Action
```

Capabilities describe possible work. Commands request work. Execution performs work. Actions mutate reality. Capability availability does not imply authorization or execution.

### Cross-Cutting Evaluation Axes

```text
Trust
Authority
Corroboration
Verification
Freshness
Contradiction
Causality
Explanation
```

These are not replacement centers. They qualify, constrain, support, or explain claims, events, recommendations, and projections.

These paths do not imply that all claims become facts, that projections create recommendations or decisions, that recommendations authorize commands, that capabilities imply execution, that events are current state, that sequence implies causality, or that LLM interpretation is authoritative.

---

## Observation

An observation is something reported by a source.

Examples:

```text
local discovery
Prometheus
operator input
inventory import
future providers
future agents
```

An observation is not automatically true.

An observation is preserved when it is safe, attributable, and useful as evidence.

---

## Evidence

Evidence is provenance supporting a claim.

Evidence answers:

```text
Why is this claim present?
Where did it come from?
What source, payload, time, scope, and context support it?
```

Evidence accumulates.

Evidence does not independently determine truth.

---

## Fact

A fact is a normalized claim supported by evidence.

Facts describe things.

Examples:

```text
host operating system
installed package
filesystem measurement
user account
```

Facts are not projections.

Facts are not truth.

Facts are justified claims.

A single observation may justify a scoped fact when the fact does not exceed the observation's scope.

---

## Relationship

A relationship is a normalized claim describing a connection between things.

Relationships describe connections.

Examples:

```text
host has endpoint
endpoint exposes service
host monitored by monitoring system
route targets backend
```

Relationships are not identity.

Related things are not necessarily the same thing.

Relationship promotion should preserve the same rule as fact promotion:

```text
Promote only what the evidence supports.
```

---

## Projection

A projection is a selected interpretation of available evidence, facts, and relationships.

Projections answer:

```text
What does Seed currently present?
What does this surface select, summarize, or explain?
```

Current state is a projection.

Current state is not the only preserved interpretation.

---

## Trust, Authority, And Corroboration

Trust, authority, and corroboration are distinct concepts.

### Trust

Trust answers:

```text
How reliable is this source path expected to be?
```

### Authority

Authority answers:

```text
Is this source allowed to declare or override this kind of claim?
```

### Corroboration

Corroboration answers:

```text
How much compatible support exists, and how independent is that support?
```

None of these independently determine truth.

---

## Identity

Identity requires stronger evidence than relationships.

Examples of stronger identity evidence:

```text
machine identifiers
explicit aliases
inventory declarations
stable provider identities
```

Weak resemblance should not create identity merges.

Examples of weak resemblance:

```text
same username
same mountpoint
same package name
same hostname pattern
same endpoint pattern
```

Resemblance is not identity.

Alias means equivalence.

When evidence is uncertain:

```text
create a relationship
before
creating an alias
```

---

## Operator

The operator is part of the system.

The operator is not merely a consumer of projections.

The operator may provide:

```text
intent
authority
approval
ownership
correction
policy
missing context
boundary decisions
```

Seed should escalate when authority is required.

Seed should continue observing when authority is not required.

An operator may be authoritative for intent, approval, ownership, or policy without being automatically correct about live runtime state.

---

## Alignment Note

When an operator asks Seed or an assistant to perform repository work, the implementation should use the available repository tools directly rather than translating the request into the operator's shell syntax unless the operator specifically asks for commands.

Operator syntax is not necessarily tool syntax.

The useful boundary is:

```text
operator intent
        ↓
available tool capability
        ↓
repository action
```

not:

```text
operator wording
        ↓
shell-only interpretation
```

This preserves the operator's intent while allowing the system to use the authority and tools it actually has.

---

## Documentation

Documentation is not the final authority.

Documentation is evidence supporting claims about the system.

Architectural statements should become traceable to:

```text
observations
evidence
facts
relationships
tests
implementation
```

Documentation should increasingly become a projection of justified claims about the repository.

The long-term goal is not merely to write documents about Seed.

The goal is for Seed to explain which claims about itself are supported, contradicted, stale, unresolved, or implementation-backed.

---

## Architectural Invariants

```text
Evidence accumulates.
Facts normalize.
Relationships connect.
Projections select.
```

```text
Preserve broadly.
Promote carefully.
Explain provenance.
```

```text
Related things are not necessarily the same thing.
Alias means equivalence.
```

```text
Trust affects belief.
Authority affects interpretation.
Corroboration affects support.
None independently determines truth.
```

```text
Current state is a view.
Current state is not the only preserved interpretation.
```

---

## Definition

Seed preserves observations, accumulates evidence, normalizes justified claims, connects justified relationships, selects explainable projections, and escalates to the operator when authority is required.

Seed does not store truth.

Seed stores justified claims and the evidence required to explain them.

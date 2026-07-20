# Self Model Architecture

## Purpose

This document describes how Seed can acquire a model of itself.

The goal is not self-awareness.

The goal is evidence-backed self-description.

It answers:

```text
How can Seed understand its own repository
using the same knowledge mechanisms
it uses for other domains?
```

This is documentation-only.

## Core Insight

Seed does not need a special self-understanding subsystem.

The same acquisition and reconciliation mechanisms used elsewhere can be applied to Seed itself.

Conceptually:

```text
Acquire claims.
Acquire artifacts.
Reconcile them.
Preserve alignment knowledge.
```

## Why A Self Model Exists

A repository contains at least two different realities.

Reality one:

```text
What the repository claims.
```

Reality two:

```text
What the repository contains.
```

These are not automatically identical.

A useful self model preserves both.

## Self Model Inputs

The self model consumes:

```text
Documentation Claims
Repository Artifacts
Support Relationships
Alignment Knowledge
```

It does not consume truth.

## Documentation Path

Documentation Observation acquires:

```text
Documentation
        ↓
Claim
```

Examples:

```text
ToolExecutor owns execution.
ProjectionStore owns cached projections.
Knowledge Acquisition is the active frontier.
ResponseEngine is rejected.
```

These become documentation-backed claims.

## Repository Path

Repository Observation acquires:

```text
Repository
        ↓
Artifact Fact
```

Examples:

```text
ToolExecutor exists.
ProjectionStore exists.
Runtime imports ToolExecutor.
SQLiteProjectionStore exists.
```

These become artifact-backed facts.

## Reconciliation Path

Repository Reconciliation compares:

```text
Claim
        ↕
Artifact Fact
```

through:

```text
Support Relationship
```

Outputs:

```text
supported
partially_supported
missing_support
potential_conflict
not_evaluable
requires_human_review
```

These are alignment outcomes.

Not truth outcomes.

## Alignment Knowledge

The result of reconciliation is:

```text
Alignment Knowledge
```

Examples:

```text
ProjectionStore ownership claim appears supported.
ResponseEngine rejection claim appears supported.
Knowledge Integrity stability claim requires human review.
```

Alignment knowledge is the core product of the self model.

## Claim Support Role

Claim Support connects:

```text
Artifact Facts
        ↓
Support Relationship
        ↓
Claims
```

Claim Support does not determine truth.

Claim Support determines:

```text
Which facts support which claims.
```

## Self Model Representation

Conceptually:

```text
Documentation
        ↓
Claims

Repository
        ↓
Artifact Facts

Artifact Facts
        ↓
Support Relationships
        ↓
Claims

Claims + Support
        ↓
Alignment Knowledge
```

This is the current self-model architecture.

## Process Layer Relationship

The self model operates inside the existing process layer.

```text
Knowledge Acquisition
        ↓
Knowledge Integrity
        ↓
Knowledge Selection
        ↓
Response
```

The self model does not replace the process layer.

It uses it.

## Representation Layer Relationship

The self model also depends on the representation layer.

```text
Observation
        ↓
Evidence
        ↓
Fact
        ↓
Support Relationship
        ↓
Claim
```

Documentation Observation primarily acquires claims.

Repository Observation primarily acquires facts.

Claim Support connects them.

## Why This Generalizes

Nothing in the architecture is Seed-specific.

The same pattern can apply to:

```text
Seed
Home Assistant
Kubernetes
Linux
Nextcloud
Any repository with documentation and artifacts
```

The acquisition model remains identical.

Only the claims and artifacts change.

## What The Self Model Does Not Do

The self model does not:

```text
reason
plan
execute
verify truth
enforce architecture
perform governance
rewrite code
```

It remains read-only.

## Early High-Value Reconciliation Targets

The easiest self-model targets are:

```text
ownership claims
existence claims
rejected concept claims
frontier claims
```

These are:

```text
high-support
low-ambiguity
low-interpretation
```

They should be prioritized before philosophy or status claims.

## Hard Reconciliation Targets

More difficult targets:

```text
status claims
process-role claims
boundary claims
philosophy claims
```

These frequently require:

```text
requires_human_review
not_evaluable
```

outcomes.

## Self Model Queries

A future self model should be able to answer:

```text
What does Seed claim?
What artifacts support those claims?
Which claims appear aligned?
Which claims have weak support?
Which claims have conflicts?
Which claims are not evaluable?
```

These are alignment questions.

Not truth questions.

## Canonical Inputs

Primary documents:

```text
documentation_observation_seed_characterization.md
repository_observation_seed_characterization.md
repository_reconciliation_seed_characterization.md
claim_support_characterization.md
claim_support_design.md
```

These collectively define the current self-model architecture.

## Completion Criteria

A self model exists when Seed can:

```text
acquire claims
acquire artifacts
build support relationships
produce alignment knowledge
```

without introducing reasoning engines, truth engines, or architecture governance systems.

## Conclusion

Seed's self model is an alignment model.

It does not attempt to know whether claims are true.

It attempts to know:

```text
what is claimed
what exists
how they relate
```

That alignment knowledge is sufficient for a useful evidence-backed understanding of the repository.

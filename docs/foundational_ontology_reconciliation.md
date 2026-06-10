# Foundational Ontology Reconciliation

## Purpose

This document reconciles the foundational architectural vocabulary that emerged across the reconciliation chain.

It does not create new architecture.

It identifies concepts that repeatedly appeared as stable architectural primitives and records the boundaries between them.

## Central Finding

Seed is claim-centric.

Claims are the central knowledge primitive around which observations, evidence, facts, relationships, projections, assessments, recommendations, decisions, events, and explanations are organized.

Facts remain important, but facts are normalized claim forms rather than the universal center of the architecture.

## Foundational Ontology

### Knowledge Plane

- Observation
- Evidence
- Claim
- Fact
- Relationship

### Temporal Plane

- Event
- Change
- State

### Interpretation Plane

- Projection
- Assessment
- Consequence
- Recommendation
- Decision

### Operator Plane

- Intent
- Question
- Goal
- Policy
- Authority

### Execution Plane

- Capability
- Command
- Execution
- Action

### Reasoning Plane

- Trust
- Corroboration
- Verification
- Contradiction
- Causality
- Explanation

### Continuation Plane

- Handoff

## Core Boundaries

Claim != Fact

Fact != Truth

Relationship != Identity

Event != State

Change != Contradiction

Projection != Authority

Assessment != Recommendation

Recommendation != Decision

Decision != Command

Capability != Execution

Explanation != Causality

Handoff != Architecture

## Architectural Planes

The planes are conceptual groupings rather than runtime pipelines.

They exist to organize vocabulary and preserve boundaries.

A concept may participate in multiple planes without collapsing those planes together.

## Relationship To Implementation

The ontology is not a schema.

The ontology is not a storage model.

The ontology is not a runtime design.

The ontology is architectural vocabulary.

Implementation may evolve.

The ontology provides the language used to reason about that implementation.

## Architectural Invariants

- Claims are the central knowledge primitive.
- Facts are normalized claim forms.
- Relationships are normalized connection claims.
- Events preserve history.
- Changes preserve transitions.
- Projections communicate selected knowledge.
- Goals remain operator-owned.
- Recommendations are advisory.
- Decisions remain distinct from recommendations.
- Capabilities describe possible work.
- Actions mutate reality.
- Explanations communicate understanding.
- Handoffs preserve continuation alignment.

## Conclusion

The foundational ontology should remain implementation-independent.

Future reconciliations may refine individual concepts, but new concepts should not be introduced lightly.

The ontology exists to provide stable architectural vocabulary for reasoning about Seed.
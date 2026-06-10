# Seed Ontology

## Purpose

This document is Seed's concise reference for stable architectural vocabulary and boundaries. It is not a schema, storage model, runtime design, or reconciliation argument.

For the full ontology audit and boundary reasoning, see [`foundational_ontology_reconciliation.md`](foundational_ontology_reconciliation.md).

## Central Finding

Seed is claim-centric.

Claims are the central knowledge primitive around which observations, evidence, facts, relationships, projections, assessments, recommendations, decisions, events, explanations, attribution, and handoffs are organized.

Facts remain important, but facts are normalized claim forms rather than the universal center of the architecture.

## Foundational Vocabulary

### Knowledge Plane

- Observation
- Evidence
- Claim
- Fact
- Relationship

### Language / Interpretation Plane

- Language Observation
- Interpretation
- Attribution

### Temporal Plane

- Event
- Change
- State

### Projection / Reasoning Plane

- Projection
- Assessment
- Consequence
- Recommendation
- Decision
- Trust
- Corroboration
- Verification
- Contradiction
- Causality
- Explanation

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

### Continuation Plane

- Handoff

## Core Boundaries

- Claim != Fact
- Fact != Truth
- Language Observation != Environmental Verification
- Interpretation != Authority
- Attribution != Consciousness
- Relationship != Identity
- Event != State
- Change != Contradiction
- Projection != Authority
- Assessment != Recommendation
- Recommendation != Decision
- Recommendation != Desire
- Decision != Intent
- Decision != Command
- Capability != Agency
- Capability != Execution
- Execution != Autonomy
- Explanation != Causality
- Handoff != Architecture
- Ontology != Schema

## Architectural Invariants

- Claims are the central knowledge primitive.
- Facts are normalized claim forms.
- Relationships are normalized connection claims.
- Natural language observes a communicative act.
- Interpretation derives candidate meaning.
- Language-derived claims remain supportable and inspectable.
- Attribution is a supportable claim.
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

## Relationship To Implementation

The ontology provides implementation-independent architectural vocabulary. Implementation may realize, serialize, cache, expose, or test these concepts, but implementation vocabulary does not define the ontology exhaustively.

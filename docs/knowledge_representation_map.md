# Knowledge Representation Map

## Purpose

This document captures the representation layer of Seed.

The existing architectural concerns describe how knowledge flows through the system:

```text
Knowledge Acquisition
        ↓
Knowledge Integrity
        ↓
Knowledge Selection
        ↓
Response
```

This document describes what the knowledge itself is.

## Process Versus Representation

Process answers:

```text
How does knowledge move?
```

Representation answers:

```text
What is the structure of knowledge?
```

These are separate architectural axes.

## Representation Model

```text
Observation
        ↓
Evidence
        ↓
Claim
        ↓
Support Relationship
        ↓
Higher-order Claim
```

## Observation

Observations are records of something seen.

Observations are not evidence.

Observations are not facts.

Observations are raw acquisition outputs.

## Evidence

Evidence provides traceable support for observations.

Evidence answers:

```text
Why does this observation exist?
```

Evidence supports facts.

## Fact

Facts are normalized claims derived from evidence.

Facts answer:

```text
What proposition has Seed represented in normalized form?
```

Facts are not raw observations, evidence payloads, selected current state, verified live reality, or universal truth.

Facts may support higher-order claims.

## Support Relationship

Support Relationships connect facts to claims.

```text
Fact
        ↓
Supports
        ↓
Claim
```

Support Relationships are:

* explicit
* deterministic
* inspectable
* read-only

Support Relationships are not truth.

Support Relationships are not reasoning.

## Claim

A claim is a proposition capable of receiving support. Facts are normalized claim forms; higher-order claims may also receive support from facts and relationships.

Examples:

```text
ToolExecutor owns execution.
ProjectionStore owns cached projections.
Knowledge Acquisition is the active frontier.
```

Claims may be supported, partially supported, unsupported, or in tension with observed facts.

## Key Distinction

```text
Evidence supports facts.

Facts may support higher-order claims.
```

These relationships should remain separate.

## Non-Goals

This representation model is not:

```text
ReasoningEngine
InferenceEngine
TruthEngine
ArchitectureEngine
```

The model represents knowledge.

It does not arbitrate truth.

## Canonical Documents

* docs/claim_support_frontier.md
* docs/claim_support_characterization.md
* docs/claim_support_design.md
* docs/documentation_observation_frontier.md
* docs/repository_observation_frontier.md
* docs/repository_reconciliation_frontier.md

## Conclusion

The process layer describes how knowledge moves.

The representation layer describes what knowledge is.

Both are required for understanding Seed.
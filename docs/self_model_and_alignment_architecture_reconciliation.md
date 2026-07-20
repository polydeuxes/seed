# Self Model And Alignment Architecture Reconciliation

## Purpose

This document consolidates the self-model and alignment architecture discovered across the Documentation Observation, Repository Observation, Repository Reconciliation, Claim Support, and Knowledge Representation documents.

It exists to prevent documentation sprawl and vocabulary drift.

It is the canonical compact explanation of:

```text
Claims
Artifacts
Alignment
Self Model
```

This is documentation-only.

## Reconciled Finding

The stable architecture is:

```text
Documentation
        ↓
Documentation Claims

Repository
        ↓
Repository Artifact Facts

Documentation Claims + Repository Artifact Facts
        ↓
Alignment Records

Alignment Records
        ↓
Self Model
```

This is a knowledge acquisition and reconciliation pipeline.

It is not a reasoning engine.

## Core Vocabulary

### Documentation Claim

A documentation-backed statement capable of receiving support.

Example:

```text
ProjectionStore owns cached projected state.
```

### Repository Artifact Fact

A structural fact observed from repository artifacts.

Example:

```text
SQLiteProjectionStore class exists.
```

### Support Relationship

A deterministic relationship between artifact facts and a claim.

Example:

```text
SQLiteProjectionStore class existence supports the ProjectionStore ownership claim.
```

### Alignment Record

The result of comparing claims and artifacts.

Example outcomes:

```text
supported
missing_support
potential_conflict
not_evaluable
```

### Self Model

A derived view over claims, artifacts, support relationships, and alignment records.

The self model answers:

```text
What does Seed claim?
What does Seed contain?
How do the two relate?
```

It does not answer:

```text
Which claim is true?
What should be changed?
What should be implemented next?
```

## Process Layer Relationship

The existing Seed process layer remains:

```text
Knowledge Acquisition
        ↓
Knowledge Integrity
        ↓
Knowledge Selection
        ↓
Response
```

The self-model pipeline does not replace that process.

It uses it.

## Representation Layer Relationship

The reconciled representation layer is:

```text
Observation
        ↓
Evidence
        ↓
Fact
        ↓
Projected Knowledge Structures
```

with a claim-justification branch:

```text
Fact
        ↓
Support Relationship
        ↓
Claim
```

Key distinction:

```text
Evidence supports facts.
Facts support claims.
```

`FactSupport` remains evidence support.

Claim Support remains claim justification support.

## Documentation Observation Role

Documentation Observation acquires claims.

It asks:

```text
What does the repository say?
```

It does not ask:

```text
Is the repository correct?
Does the code match?
Which claim wins?
```

Small implementation-scale slice:

```text
README.md
docs/architectural_knowledge_map.md
        ↓
DocumentationClaim records
```

## Repository Observation Role

Repository Observation acquires artifact facts.

It asks:

```text
What repository artifacts exist?
```

It does not ask:

```text
What do those artifacts mean architecturally?
Do they match documentation?
Are they correct?
```

Small implementation-scale slice:

```text
seed_runtime/
tests/
        ↓
RepositoryArtifactFact records
```

## Repository Reconciliation Role

Repository Reconciliation compares documentation claims and repository artifact facts.

It asks:

```text
How do claims and artifacts relate?
```

Small implementation-scale slice:

```text
DocumentationClaim
+
RepositoryArtifactFact
        ↓
AlignmentRecord
```

Initial outcomes:

```text
supported
missing_support
potential_conflict
not_evaluable
```

## Claim Support Role

Claim Support provides the relationship model used by reconciliation.

It does not generate claims.

It does not generate facts.

It does not determine truth.

It relates facts to claims through deterministic rules.

## What Should Be Implemented First

The smallest safe implementation path is:

1. fixture-level `DocumentationClaim` records;
2. fixture-level `RepositoryArtifactFact` records;
3. deterministic reconciliation rules;
4. fixture-level `AlignmentRecord` output.

Only after that works should extraction from real markdown or repository paths be connected.

## What Should Not Be Implemented Yet

Do not implement yet:

```text
projection integration
Runtime integration
ToolExecutor integration
Claim Support projection
self-model projection
repository-wide scanning
LLM extraction
architecture scoring
truth arbitration
human review workflows
```

## Early High-Value Claim Families

Start with claim families that are easy to compare structurally:

```text
ownership claims
rejected concept claims
frontier claims
existence claims
```

Avoid early implementation for:

```text
philosophy claims
status claims
process-role claims
broad boundary claims
```

These are likely to be `not_evaluable` or require future human review semantics.

## Canonical Documents In This Arc

Conceptual architecture:

* `docs/knowledge_representation_map.md`
* `docs/knowledge_representation_reconciliation.md`
* `docs/claim_support_frontier.md`
* `docs/claim_support_characterization.md`
* `docs/claim_support_design.md`
* `docs/self_model_architecture.md`

Seed-specific characterization:

* `docs/documentation_observation_seed_characterization.md`
* `docs/repository_observation_seed_characterization.md`
* `docs/repository_reconciliation_seed_characterization.md`

Implementation-scale characterization:

* `docs/documentation_observation_v0_implementation_characterization.md`
* `docs/repository_observation_v0_implementation_characterization.md`
* `docs/repository_reconciliation_v0_implementation_characterization.md`

## Rejected Concepts

This arc rejects:

```text
SelfModelEngine
RepositoryEngine
DocumentationEngine
ArchitectureEngine
ReasoningEngine
TruthEngine
ClaimStore
SupportStore
```

It also rejects:

```text
automatic claim-to-claim reasoning
architecture scoring
truth arbitration
runtime-owned self model
ToolExecutor-owned reconciliation
```

## Final Reconciled Statement

Seed's self model is an alignment model.

It is built from:

```text
Documentation Claims
Repository Artifact Facts
Support Relationships
Alignment Records
```

It is useful because it preserves:

```text
what Seed says
what Seed contains
how the two relate
```

without deciding truth, executing code, or enforcing architecture.

## Conclusion

The self-model and alignment architecture is now stable enough for a tiny fixture-level implementation experiment.

The next work should prove the smallest record path:

```text
DocumentationClaim
+
RepositoryArtifactFact
        ↓
AlignmentRecord
```

before adding extraction, projection, or response surfaces.

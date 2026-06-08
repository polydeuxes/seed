# Repository Reconciliation Seed Characterization

## Purpose

This document characterizes Repository Reconciliation using Seed itself as the target repository.

It answers:

```text
Which Seed documentation claims
should be compared
against which Seed repository artifacts?
```

This document is the first concrete self-reconciliation characterization.

It uses:

```text
Documentation Observation Seed Characterization
```

and:

```text
Repository Observation Seed Characterization
```

as inputs.

## Core Model

Repository Reconciliation consumes:

```text
Documentation Claims
```

and:

```text
Repository Facts
```

and produces:

```text
Alignment Knowledge
```

Conceptually:

```text
Claim
        ↓
Support Relationship
        ↓
Artifact Facts
```

Repository Reconciliation should remain read-only.

## Reconciliation Scope

Repository Reconciliation v0 should only compare claims that are capable of receiving structural repository support.

Good candidates:

```text
ownership claims
boundary claims
implementation claims
frontier claims
rejection claims
existence claims
```

Poor candidates:

```text
philosophy claims
quality claims
style claims
operator-experience claims
```

These should usually become:

```text
not_evaluable
```

## Claim Family: Ownership

### Claim

```text
ProjectionStore owns cached projected state.
```

Documentation Sources:

```text
README.md
architectural docs
```

Expected Artifact Facts:

```text
ProjectionStore protocol exists.
SQLiteProjectionStore exists.
InMemoryProjectionStore exists.
Projection cache CLI references ProjectionStore.
```

Expected Outcome:

```text
supported
or
partially_supported
```

### Claim

```text
ToolExecutor owns registered-operation execution.
```

Expected Artifact Facts:

```text
ToolExecutor class exists.
Runtime imports ToolExecutor.
Runtime calls ToolExecutor.
ToolExecutor tests exist.
```

Expected Outcome:

```text
supported
partially_supported
requires_human_review
```

depending on observed execution-path evidence.

### Claim

```text
EventLedger owns append-only event history.
```

Expected Artifact Facts:

```text
EventLedger exists.
EventLedger storage artifacts exist.
EventLedger tests exist.
```

Expected Outcome:

```text
supported
or
partially_supported
```

## Claim Family: Boundary

### Claim

```text
Response does not create knowledge.
```

Expected Artifact Facts:

```text
Response-related output artifacts exist.
Knowledge acquisition artifacts exist elsewhere.
```

Expected Outcome:

```text
requires_human_review
```

Reason:

Structural support alone is unlikely to prove this boundary.

### Claim

```text
Integrity does not determine truth.
```

Expected Outcome:

```text
not_evaluable
```

Repository Observation v0 is unlikely to possess sufficient artifact evidence.

### Claim

```text
Repository Reconciliation does not arbitrate truth.
```

Expected Outcome:

```text
not_evaluable
```

This is primarily an architectural boundary claim.

## Claim Family: Status

### Claim

```text
Knowledge Acquisition is the active capability frontier.
```

Expected Artifact Facts:

```text
Users Observation absent.
Groups Observation absent.
Package Observation absent.
Systemd Observation absent.
```

Expected Outcome:

```text
supported
```

The support comes from frontier semantics.

### Claim

```text
Knowledge Integrity is stable.
```

Expected Outcome:

```text
requires_human_review
```

Architectural stability is not directly observable from repository artifacts.

## Claim Family: Frontier

### Claim

```text
Users Observation is a current priority.
```

Expected Artifact Facts:

```text
Users Observation implementation absent.
Users Observation tests absent.
```

Expected Outcome:

```text
supported
```

### Claim

```text
Documentation Observation is an emerging frontier.
```

Expected Artifact Facts:

```text
Frontier documents exist.
No implementation exists.
```

Expected Outcome:

```text
supported
```

### Claim

```text
Repository Reconciliation is an emerging frontier.
```

Expected Artifact Facts:

```text
Characterization documents exist.
No implementation exists.
```

Expected Outcome:

```text
supported
```

## Claim Family: Rejected Concepts

### Claim

```text
ResponseEngine is rejected.
```

Expected Artifact Facts:

```text
No ResponseEngine artifact exists.
```

Expected Outcome:

```text
supported
```

### Claim

```text
IntegrityEngine is rejected.
```

Expected Artifact Facts:

```text
No IntegrityEngine artifact exists.
```

Expected Outcome:

```text
supported
```

### Claim

```text
ClaimStore is rejected.
```

Expected Artifact Facts:

```text
No ClaimStore artifact exists.
```

Expected Outcome:

```text
supported
```

### Claim

```text
SupportStore is rejected.
```

Expected Artifact Facts:

```text
No SupportStore artifact exists.
```

Expected Outcome:

```text
supported
```

### Conflict Pattern

If a rejected artifact exists:

```text
ResponseEngine class exists.
ClaimStore module exists.
SupportStore package exists.
```

Expected Outcome:

```text
potential_conflict
```

Not:

```text
false
```

Repository Reconciliation does not determine truth.

## Claim Family: Existence

### Claim

```text
Seed contains architectural documentation.
```

Expected Artifact Facts:

```text
docs directory exists.
Architectural documents exist.
```

Expected Outcome:

```text
supported
```

### Claim

```text
Seed contains representation documentation.
```

Expected Artifact Facts:

```text
knowledge_representation_map exists.
knowledge_representation_reconciliation exists.
```

Expected Outcome:

```text
supported
```

## Claim Family: Representation

### Claim

```text
FactSupport exists.
```

Expected Artifact Facts:

```text
FactSupport artifacts exist.
```

Expected Outcome:

```text
supported
```

### Claim

```text
FactSupport and Claim Support are distinct concepts.
```

Expected Artifact Facts:

```text
FactSupport artifacts exist.
Claim Support documentation exists.
```

Expected Outcome:

```text
partially_supported
or
requires_human_review
```

Structural support alone may be insufficient.

## Claim Family: Process Layer

### Claim

```text
Acquisition creates knowledge.
Integrity characterizes knowledge.
Selection chooses knowledge.
Response communicates knowledge.
```

Expected Outcome:

```text
mostly not_evaluable
```

These are architectural-role claims.

Repository Observation v0 primarily observes artifacts.

## Example Alignment Record

Claim:

```text
ProjectionStore owns cached projected state.
```

Repository Facts:

```text
ProjectionStore protocol exists.
SQLiteProjectionStore exists.
InMemoryProjectionStore exists.
```

Support Relationship:

```text
supports
```

Strength:

```text
strong
```

Reason:

```text
Repository artifacts align with the documented ownership concept.
```

## Example Conflict Record

Claim:

```text
ResponseEngine is rejected.
```

Repository Facts:

```text
ResponseEngine class exists.
```

Support Relationship:

```text
potentially_conflicts_with
```

Strength:

```text
strong
```

Reason:

```text
Observed artifact matches a documented rejected concept.
```

## Alignment Categories

Repository Reconciliation over Seed should primarily produce:

```text
supported
partially_supported
missing_support
potential_conflict
not_evaluable
requires_human_review
```

These outcomes describe alignment.

They do not describe truth.

## Query Expectations

Repository Reconciliation over Seed should answer:

```text
Which documented ownership claims have artifact support?
Which frontier claims are supported by implementation absence?
Which rejected concepts appear absent?
Which claims are not evaluable from repository artifacts?
Which claims have potential conflicts?
```

It should not answer:

```text
Which architecture is correct?
Which document should change?
Which implementation should be built?
```

Those remain operator decisions.

## Expected Early Wins

The easiest high-confidence reconciliation targets are:

```text
ownership claims
existence claims
rejected concept claims
frontier claims
```

The hardest are:

```text
status claims
process-role claims
philosophy claims
boundary claims
```

This ordering should guide future implementation.

## Completion Criteria

Seed-specific Repository Reconciliation is characterized when it has:

* claim families;
* artifact families;
* expected support patterns;
* expected conflict patterns;
* example alignment records;
* example conflict records;
* query expectations.

This document provides that characterization.

## Conclusion

Seed now has a concrete reconciliation target.

Documentation Observation can provide claims.

Repository Observation can provide artifacts.

Repository Reconciliation can compare them.

The result is alignment knowledge rather than truth.
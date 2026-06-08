# Repository Reconciliation Frontier

## Purpose

This document defines the frontier that follows Documentation Observation and Repository Observation.

The sequence is:

```text
Documentation Observation
        ↓
Repository Observation
        ↓
Repository Reconciliation
```

Documentation Observation answers:

```text
What does the repository claim?
```

Repository Observation answers:

```text
What repository artifacts exist?
```

Repository Reconciliation answers:

```text
How do those two bodies of knowledge relate?
```

This document covers Repository Reconciliation only.

## Core Insight

Repository Reconciliation is the first place where Seed is allowed to compare claims and artifacts.

This is important because neither observation slice owns interpretation.

Documentation Observation produces:

```text
Claim facts
```

Repository Observation produces:

```text
Artifact facts
```

Repository Reconciliation consumes both.

## Problem

A repository may contain:

```text
Documented ownership
Documented boundaries
Documented non-goals
Documented frontiers
Documented architecture
```

The repository may also contain:

```text
Files
Modules
Classes
Functions
Imports
Tests
Catalogs
Scripts
```

Neither side alone can answer:

```text
Does the repository appear aligned with its documentation?
```

That question requires comparison.

Comparison is reconciliation.

## What Reconciliation Is

Repository Reconciliation is a read-only comparison concern.

It evaluates relationships between:

```text
Documentation facts
```

and:

```text
Repository facts
```

The output is not truth.

The output is a reconciliation result.

Examples:

```text
Aligned
Potentially aligned
Potentially missing
Potentially drifting
Insufficient evidence
Requires human review
```

## What Reconciliation Is Not

Repository Reconciliation is not:

```text
Static analysis
Architecture enforcement
Code review
Design review
Implementation planning
Refactoring guidance
Automated governance
Truth arbitration
```

It does not decide:

```text
which side is correct
which side should change
which architecture should win
```

It reports relationships.

## Why Reconciliation Is Not Observation

Observation asks:

```text
What exists?
```

Reconciliation asks:

```text
How do observed things relate?
```

That is a different concern.

Observation should remain free of interpretation.

Reconciliation should remain free of implementation authority.

## Example

Documentation fact:

```text
README claims ToolExecutor owns registered-operation execution.
```

Repository facts:

```text
ToolExecutor class exists.
Runtime imports ToolExecutor.
Runtime calls ToolExecutor.
```

Possible reconciliation result:

```text
Documentation claim appears supported by repository artifacts.
```

Not:

```text
Documentation claim proven true.
```

Evidence remains partial.

## Reconciliation Inputs

Repository Reconciliation should consume:

```text
Projected documentation facts
Projected repository facts
```

It should not require:

```text
Runtime execution
Provider execution
Test execution
Shell execution
Human approval workflows
```

The comparison should remain read-only.

## Initial Reconciliation Families

Suggested reconciliation families:

| Family | Meaning |
| --- | --- |
| `claim_has_artifact_support` | Repository artifacts appear to support a claim. |
| `claim_missing_artifact_support` | Expected support artifacts were not observed. |
| `claim_has_partial_support` | Some supporting artifacts were observed. |
| `claim_has_conflicting_artifacts` | Observed artifacts may conflict with a claim. |
| `claim_requires_review` | Available evidence is insufficient. |
| `claim_not_evaluable` | No reconciliation rule exists yet. |

These are reconciliation outcomes.

They are not architecture verdicts.

## Initial Claim Families Worth Reconciling

V0 should remain narrow.

Good candidates:

```text
Ownership claims
Boundary claims
Non-goal claims
Implemented-slice claims
Frontier claims
```

Examples:

```text
ToolExecutor owns execution.
ProjectionStore owns cached projections.
Runtime is not a second orchestration loop.
Knowledge Acquisition is the active frontier.
```

Avoid broad architectural narratives in v0.

## Evidence Requirements

Every reconciliation result should preserve both sides of the comparison.

Required metadata:

```text
documentation evidence
repository evidence
reconciliation rule
confidence
```

A user should be able to inspect:

```text
What claim was compared?
What artifact facts were used?
Why was this result produced?
```

## Confidence

Reconciliation confidence should be conservative.

Examples:

High confidence:

```text
Claim references a class.
Class exists.
Class usage exists.
```

Lower confidence:

```text
Claim references a responsibility.
Only naming-based evidence exists.
```

Confidence should remain visible metadata.

## Human Review Boundary

Repository Reconciliation should prefer:

```text
Requires human review
```

over:

```text
Architecture is wrong.
```

The goal is evidence-backed navigation.

Not automated architecture judgment.

## Relationship To Knowledge Integrity

Repository Reconciliation is not Knowledge Integrity.

Integrity asks:

```text
Can projected knowledge be safely interpreted?
```

Reconciliation asks:

```text
How do two bodies of projected knowledge relate?
```

These concerns should remain separate.

## Relationship To Knowledge Selection

Selection may later choose reconciliation results when relevant.

Repository Reconciliation does not own:

```text
ranking
context composition
response choice
```

It only produces reconciliation knowledge.

## Relationship To Response

Response may communicate reconciliation results.

Repository Reconciliation does not own formatting.

It does not own operator communication.

## What V0 Should Answer

Repository Reconciliation v0 should support questions such as:

```text
Does documentation claim ToolExecutor owns execution?
Were supporting artifacts observed?
Does documentation claim ProjectionStore owns cached projections?
Were supporting artifacts observed?
Which claims currently lack observed support?
Which claims require human review?
```

These are evidence-backed comparison questions.

## What V0 Must Not Answer

Repository Reconciliation v0 must not answer:

```text
Which architecture is best?
Should this code be rewritten?
Who made a mistake?
Which document should be deleted?
What should be implemented next?
```

Those require human judgment.

## Rejection Criteria

Do not implement Repository Reconciliation if the work requires:

```text
Runtime changes
ToolExecutor changes
EventLedger ownership changes
ProjectionStore ownership changes
provider execution
shell execution
architecture scoring
automatic governance
automatic architecture enforcement
LLM-required interpretation
```

Do not continue if reconciliation cannot be reduced to explicit evidence-backed comparisons.

## Recommended Next Step

Before implementation, create:

```text
Repository Reconciliation Characterization
```

That characterization should define:

* which claim families are compared;
* which artifact facts support those claims;
* which reconciliation outcomes exist;
* expected examples from Seed;
* confidence rules;
* explanation requirements.

## Conclusion

Repository Reconciliation is the first concern that compares what the repository claims with what the repository contains.

Its role is not to determine truth.

Its role is to produce evidence-backed alignment knowledge that humans and later reasoning systems can inspect.

Observation discovers.

Reconciliation compares.

Those responsibilities should remain separate.
# Claim Support Characterization

## Purpose

This document characterizes Claim Support v0.

It defines what a claim is, what support relationships are, how support strength is represented, and how support differs from evidence.

This is documentation-only.

## Core Question

Claim Support asks:

```text
Which facts support which claims?
```

It does not ask:

```text
Which claims are true?
Which claims should exist?
Which claims should be enforced?
```

## Foundational Distinction

Seed already has:

```text
Observation
        ↓
Evidence
        ↓
Fact
```

Claim Support introduces:

```text
Fact
        ↓
Support Relationship
        ↓
Claim
```

Evidence and support are different.

Evidence supports facts.

Facts support claims.

## What Is A Claim?

A claim is a statement that can receive support.

Examples:

```text
ToolExecutor owns execution.
ProjectionStore owns cached projections.
Knowledge Acquisition is the active frontier.
Node is unhealthy.
ResponseEngine is rejected.
```

Claims may originate from:

```text
documentation
operator statements
projected knowledge
future audit artifacts
```

Claim origin is metadata.

Claim origin does not determine truth.

## What Is Not A Claim?

Examples:

```text
ToolExecutor class exists.
Runtime imports ToolExecutor.
ProjectionStore protocol exists.
```

These are facts.

They do not require support relationships.

They may provide support relationships.

## Claim Families

Initial claim families:

```text
ownership claim
boundary claim
status claim
frontier claim
rejection claim
health claim
capability claim
implementation claim
```

Examples:

```text
ownership:
ToolExecutor owns execution.

boundary:
Runtime does not own execution.

status:
Knowledge Integrity is stable.

frontier:
Users Observation is a current frontier.

rejection:
ResponseEngine is rejected.

health:
Node is unhealthy.

capability:
Package Observation exists.

implementation:
Listening Port Observation is implemented.
```

## Support Relationship Definition

A support relationship is a link between:

```text
fact(s)
```

and:

```text
claim
```

Conceptually:

```text
Fact A
Fact B
Fact C
        ↓
Supports
        ↓
Claim X
```

The relationship should be explicit and inspectable.

## Support Relationship Families

Initial support relationship families:

```text
supports
partially_supports
weakly_supports
fails_to_support
potentially_conflicts_with
```

These are relationship outcomes.

They are not truth outcomes.

## Support Strength Vocabulary

Suggested support strengths:

```text
strong
moderate
weak
none
```

### strong

Multiple direct facts support the claim.

Example:

```text
ToolExecutor class exists.
Runtime calls ToolExecutor.
ToolExecutor tests exist.
```

### moderate

Some direct support exists.

Example:

```text
ToolExecutor class exists.
Runtime imports ToolExecutor.
```

### weak

Only indirect support exists.

Example:

```text
Name similarity.
Path similarity.
```

### none

No support facts observed.

## Support Is Not Truth

Support means:

```text
Observed facts are consistent with the claim.
```

Support does not mean:

```text
Claim is true.
```

Example:

```text
ProjectionStore implementation exists.
```

supports:

```text
ProjectionStore owns cached projections.
```

but does not prove it.

## Negative Support

Claim Support should allow negative relationships.

Example:

Claim:

```text
ResponseEngine is rejected.
```

Fact:

```text
ResponseEngine class exists.
```

Relationship:

```text
potentially_conflicts_with
```

Negative support is not disproof.

It is a relationship indicating tension between facts and claims.

## Can Facts Support Other Facts?

V0 answer:

```text
No.
```

Claim Support should only operate between:

```text
facts
```

and:

```text
claims
```

Fact-to-fact relationships belong elsewhere.

This restriction keeps the model small.

## Can Claims Support Claims?

V0 answer:

```text
No.
```

Claim support chains introduce inference semantics.

Those are intentionally excluded.

## Can Support Relationships Be Observed?

V0 answer:

```text
No.
```

Support relationships are derived relationships.

Observations produce evidence.

Evidence supports facts.

Facts support claims.

Support relationships should not become a new observation source.

## Support Inputs

Support relationships should consume:

```text
claim
fact set
support rule
```

Nothing more.

They should not require:

```text
LLM interpretation
runtime execution
provider execution
human review loops
```

## Support Rule Shape

A support rule should define:

```text
claim family
required fact patterns
support threshold
partial support threshold
conflict patterns
fallback outcome
```

Rules should be deterministic.

Rules should be inspectable.

## Example: Ownership Claim

Claim:

```text
ToolExecutor owns execution.
```

Facts:

```text
ToolExecutor class exists.
Runtime imports ToolExecutor.
Runtime calls ToolExecutor.
```

Relationship:

```text
supports
```

Strength:

```text
strong
```

## Example: Frontier Claim

Claim:

```text
Users Observation is a current frontier.
```

Facts:

```text
Users Observation implementation absent.
Users Observation tests absent.
```

Relationship:

```text
supports
```

Strength:

```text
moderate
```

The support comes from the frontier semantics.

## Example: Health Claim

Claim:

```text
Node is unhealthy.
```

Facts:

```text
Prometheus target down.
SSH unreachable.
Recent uptime reset.
```

Relationship:

```text
supports
```

Strength:

```text
strong
```

This example demonstrates that Claim Support is broader than repository reconciliation.

## Explanation Requirements

Every support relationship should explain:

```text
claim
supporting facts
relationship type
strength
reason
```

Example:

```text
ToolExecutor owns execution is strongly supported because ToolExecutor exists, Runtime imports ToolExecutor, and Runtime calls ToolExecutor.
```

## Projection Questions

Open questions preserved for future work:

```text
Should support relationships themselves be projected?
Should support strengths be projected?
Should support relationships expire?
Should support relationships be versioned?
```

These remain unresolved.

## Non-Goals

Claim Support v0 is not:

```text
Reasoning Engine
Inference Engine
Truth Engine
Architecture Engine
Governance Engine
Planning Engine
```

It should remain deterministic and inspectable.

## Completion Criteria

Claim Support v0 is characterized when it has:

```text
claim definition
claim families
support relationship families
support strength vocabulary
support examples
support rule shape
explanation requirements
non-goals
```

This document provides that characterization.

## Recommended Next Step

The next document should be:

```text
Claim Support Design
```

That design should explain:

* where support rules live;
* how support relationships are created;
* whether support relationships are projected;
* how explanations consume support relationships;
* why Claim Support does not become reasoning.

## Conclusion

Claim Support appears to be a reusable architectural primitive.

Evidence supports facts.

Facts support claims.

Support relationships should remain explicit, deterministic, inspectable, and separate from truth.
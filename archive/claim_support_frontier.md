# Claim Support Frontier

## Purpose

This document preserves a newly identified architectural concept:

```text
Claim Support
```

Claim Support emerged during Repository Reconciliation work.

It appears to be a more general concern than repository reconciliation itself.

This document defines the frontier before implementation.

## Discovery

Seed already has:

```text
Observation
        ↓
Evidence
        ↓
Fact
```

Repository Reconciliation exposed another relationship:

```text
Fact
        ↓
Supports
        ↓
Claim
```

This relationship is different from evidence.

Evidence supports facts.

Facts support claims.

Those are separate concepts.

## Core Insight

The statement:

```text
README claims ToolExecutor owns execution.
```

is a claim.

The statement:

```text
ToolExecutor class exists.
```

is a fact.

The statement:

```text
ToolExecutor class existence supports the execution-ownership claim.
```

is a support relationship.

The support relationship is neither:

```text
observation
evidence
fact
```

nor:

```text
truth
```

It is a comparison relationship.

## Why This Matters

Repository Reconciliation was the first place where this pattern became obvious.

However the same structure appears elsewhere.

Example:

```text
Claim:
Node is unhealthy.

Fact:
Prometheus target is down.

Support:
Target-down fact supports unhealthy-node claim.
```

Example:

```text
Claim:
ProjectionStore owns cached projections.

Fact:
ProjectionStore implementation exists.

Support:
Implementation fact supports ownership claim.
```

Example:

```text
Claim:
Knowledge Acquisition is active frontier.

Fact:
Users Observation is unimplemented.

Support:
Missing implementation supports frontier claim.
```

The pattern is reusable.

## Proposed Conceptual Model

A useful conceptual ladder may be:

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

Support sits between facts and claims.

Support is not proof.

Support is not truth.

Support is a relationship.

## What Claim Support Is

Claim Support is a read-only relationship concern.

It answers:

```text
Which facts support which claims?
```

It does not answer:

```text
Which claims are true?
Which claims should exist?
Which claims should be removed?
```

## What Claim Support Is Not

Claim Support is not:

```text
Inference Engine
Reasoning Engine
Truth Engine
Governance Engine
Architecture Engine
Scoring Engine
```

It should remain deterministic and inspectable.

## Support Relationship Shape

A support relationship conceptually contains:

```text
claim
supporting facts
support rule
support strength
explanation
```

Example:

```text
Claim:
ToolExecutor owns execution.

Supporting facts:
ToolExecutor exists.
Runtime imports ToolExecutor.
Runtime calls ToolExecutor.

Strength:
high
```

## Support Strength

Support should be expressed as relationship strength.

Possible strengths:

```text
strong
moderate
weak
none
```

Strength describes support.

Strength does not describe truth.

## Relationship To Evidence

Evidence produces facts.

Example:

```text
AST node
        ↓
Evidence
        ↓
ToolExecutor class exists
```

Claim Support consumes facts.

Example:

```text
ToolExecutor class exists
        ↓
Supports
        ↓
ToolExecutor owns execution
```

Evidence and support should remain separate concepts.

## Relationship To Repository Reconciliation

Repository Reconciliation appears to be the first consumer of Claim Support.

Conceptually:

```text
Repository Reconciliation
        ↓
uses
        ↓
Claim Support
```

Repository Reconciliation compares:

```text
Documentation claims
Repository facts
```

using support relationships.

Claim Support itself is broader.

## Relationship To Knowledge Integrity

Knowledge Integrity characterizes projected knowledge.

Claim Support relates projected facts to claims.

These are different responsibilities.

Claim Support should not become Integrity.

Integrity should not become Claim Support.

## Relationship To Knowledge Selection

Selection may later choose claims, facts, or support relationships.

Claim Support does not own ranking, prioritization, or context composition.

## Relationship To Response

Response may communicate support relationships.

Claim Support does not own formatting or communication.

## Initial Candidate Consumers

Potential consumers:

```text
Repository Reconciliation
Capability justification
Selection rationale
Integrity explanation
Architecture audits
Future acquisition audits
```

This list is exploratory.

It does not justify implementation.

## Questions To Preserve

Before implementation, these questions need answers:

```text
What is a claim?
Can facts support other facts?
Can support relationships themselves be observed?
How is support strength represented?
Can support be negative?
Can support expire?
Should support be projected?
```

These questions remain open.

## Rejection Criteria

Do not implement Claim Support if the work requires:

```text
Reasoning Engine
Inference Engine
Truth Engine
Architecture Engine
Automatic governance
Automatic planning
Automatic architecture scoring
LLM-required interpretation
```

Do not continue if support relationships cannot be reduced to explicit inspectable inputs and outputs.

## Recommended Next Step

Before design work:

```text
Claim Support Characterization
```

should define:

* claim families;
* support relationship types;
* support strength vocabulary;
* support examples;
* support explanation requirements;
* support non-goals.

## Conclusion

Claim Support appears to be a reusable architectural primitive.

Repository Reconciliation revealed it.

The primitive itself may be broader than repository reconciliation.

Evidence supports facts.

Facts support claims.

Those relationships should remain separate, explicit, and inspectable.

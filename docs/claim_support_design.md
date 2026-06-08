# Claim Support Design

## Purpose

This document defines the smallest safe design for Claim Support v0.

It answers:

```text
How do facts support claims
without creating a reasoning engine,
inference engine,
or truth system?
```

This is documentation-only.

## Design Goal

Claim Support should be a reusable architectural primitive.

Its responsibility is:

```text
Relate facts to claims.
```

Nothing more.

Claim Support should not determine truth.

Claim Support should not generate claims.

Claim Support should not generate facts.

## Conceptual Position

Claim Support sits between facts and claims.

Conceptually:

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

Evidence produces facts.

Claim Support consumes facts.

## Primary Constraint

Claim Support must not create:

```text
ReasoningEngine
InferenceEngine
TruthEngine
GovernanceEngine
ArchitectureEngine
PlanningEngine
```

Claim Support should remain:

```text
deterministic
inspectable
read-only
```

## Ownership

Claim Support does not own:

```text
Observation
Evidence
Fact creation
Knowledge Integrity
Knowledge Selection
Response
```

Claim Support consumes facts and claims.

It produces support relationships.

## Inputs

Claim Support should consume:

```text
claim
fact set
support rule
```

Nothing else.

No runtime execution.

No provider execution.

No LLM interpretation.

## Output

Claim Support should produce:

```text
support relationship
```

Conceptually:

```text
claim
supporting facts
relationship type
support strength
explanation
```

The output is not a truth verdict.

## Support Relationship Shape

Conceptual structure:

```text
SupportRelationship
  claim
  supporting_facts
  relationship_type
  strength
  rule_id
  explanation
```

The structure should remain explicit.

## Relationship Types

V0 relationship types:

```text
supports
partially_supports
weakly_supports
fails_to_support
potentially_conflicts_with
```

These relationship types are deterministic outputs.

They are not truth values.

## Strength Model

V0 strength vocabulary:

```text
strong
moderate
weak
none
```

Strength represents support quality.

Strength does not represent certainty.

## Rule Model

Support relationships should be produced by explicit rules.

Conceptually:

```text
claim family
required facts
support threshold
partial threshold
conflict patterns
fallback outcome
```

Rules should be inspectable.

Rules should be deterministic.

Rules should not require model interpretation.

## Rule Example: Ownership Claim

Claim:

```text
ToolExecutor owns execution.
```

Support rule:

```text
Required:
ToolExecutor class exists.

Additional support:
Runtime imports ToolExecutor.
Runtime calls ToolExecutor.
```

Possible outcomes:

```text
class only -> partially_supports
class + import -> partially_supports
class + import + call -> supports
missing class -> fails_to_support
```

## Rule Example: Rejection Claim

Claim:

```text
ResponseEngine is rejected.
```

Rule:

```text
No ResponseEngine symbol observed.
```

Outcomes:

```text
no symbol -> supports
symbol exists -> potentially_conflicts_with
```

## Rule Example: Frontier Claim

Claim:

```text
Users Observation is a current frontier.
```

Rule:

```text
Implementation absent.
Tests absent.
```

Outcome:

```text
supports
```

The rule interprets absence according to frontier semantics.

## Determinism Requirement

The same:

```text
claim
fact set
rule set
```

must produce the same support relationship.

Claim Support should be reproducible.

## Explanation Requirement

Every support relationship should explain itself.

Example:

```text
ToolExecutor owns execution is strongly supported because ToolExecutor exists, Runtime imports ToolExecutor, and Runtime calls ToolExecutor.
```

The explanation should cite:

```text
claim
facts
rule
relationship type
strength
```

## Projection Question

A major open question is:

```text
Should support relationships be projected knowledge?
```

Current design recommendation:

```text
Yes.
```

Reason:

Support relationships appear reusable across:

```text
Repository Reconciliation
Integrity explanations
Selection rationale
Capability justification
Architecture audits
```

If support relationships are reusable, they should be available as projected knowledge.

## Why Projection Appears Safe

Support relationships are:

```text
read-only
deterministic
inspectable
rule-derived
```

Those properties match existing projection goals.

They do not require:

```text
truth arbitration
reasoning
planning
execution
```

## Expiration Question

Open question:

```text
Can support relationships become stale?
```

Current recommendation:

```text
Treat support relationships as derived knowledge.
```

If supporting facts change, support relationships should be recomputed.

No separate support-expiration system is currently justified.

## Relationship To Repository Reconciliation

Repository Reconciliation should consume Claim Support.

Conceptually:

```text
Repository Reconciliation
        ↓
uses
        ↓
Claim Support
```

Repository Reconciliation becomes a domain-specific application of support relationships.

## Relationship To Integrity

Integrity may later characterize support relationships.

Example:

```text
support relationship built from stale facts
```

Claim Support does not own integrity.

## Relationship To Selection

Selection may choose support relationships when building context.

Claim Support does not own ranking.

## Relationship To Response

Response may communicate support relationships.

Claim Support does not own formatting.

## Runtime Impact

None.

Claim Support should not require Runtime changes.

## ToolExecutor Impact

None.

Claim Support should not require ToolExecutor changes.

## EventLedger Impact

None to ownership.

Support relationships may eventually be derived from projected knowledge.

EventLedger ownership remains unchanged.

## ProjectionStore Impact

None to ownership.

If support relationships are projected, they should use existing projection mechanisms.

ProjectionStore ownership remains unchanged.

## Tests To Consider Later

If implemented, tests should verify:

```text
same inputs produce same outputs
support strength thresholds work
conflict rules work
explanations are generated
claims are not treated as facts
facts are not treated as claims
```

Tests should not require models.

## Success Criteria

Claim Support v0 succeeds if:

```text
facts can be related to claims
through deterministic support rules
producing inspectable support relationships
without introducing reasoning or truth systems.
```

## Failure Criteria

The design fails if implementation requires:

```text
ReasoningEngine
InferenceEngine
TruthEngine
GovernanceEngine
ArchitectureEngine
LLM-required interpretation
claim-to-claim inference
fact-to-fact support chains
```

## Conclusion

Claim Support appears to be a foundational knowledge primitive.

Evidence supports facts.

Facts support claims.

Claim Support should preserve that relationship in a deterministic, inspectable, reusable form without becoming a reasoning system.
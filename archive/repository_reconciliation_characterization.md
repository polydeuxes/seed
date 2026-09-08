# Repository Reconciliation Characterization

## Purpose

This document characterizes Repository Reconciliation v0.

It defines how Seed should compare documentation-derived claim facts with repository-derived artifact facts without determining architectural truth, enforcing design, or recommending implementation.

This is documentation-only.

## Core Question

Repository Reconciliation asks:

```text
How do documentation claims relate to repository artifacts?
```

It does not ask:

```text
Which source is correct?
What should be changed?
Who is wrong?
What should be implemented next?
```

## Inputs

Repository Reconciliation consumes two projected knowledge sets:

```text
Documentation facts
Repository facts
```

Documentation facts describe what repository documentation claims.

Repository facts describe what repository artifacts contain.

Reconciliation compares them.

## Output

Repository Reconciliation should produce reconciliation facts.

A reconciliation fact is a read-only comparison result.

It should include:

```text
documentation claim
repository artifact evidence
reconciliation rule
outcome
confidence
explanation
```

The output is not truth.

The output is alignment knowledge.

## V0 Outcomes

Repository Reconciliation v0 should use a small outcome vocabulary:

```text
supported
partially_supported
missing_support
potential_conflict
not_evaluable
requires_human_review
```

### supported

Use when repository artifacts directly support a documentation claim.

Example:

```text
Documentation claim:
ProjectionStore owns cached projected state.

Repository artifacts:
ProjectionStore class exists.
SQLiteProjectionStore class exists.
Projection cache status CLI references ProjectionStore.

Outcome:
supported
```

### partially_supported

Use when some expected artifact support exists but important support is missing or indirect.

Example:

```text
Documentation claim:
ToolExecutor owns registered-operation execution.

Repository artifacts:
ToolExecutor class exists.
Runtime imports ToolExecutor.
No direct call/use fact is available in v0.

Outcome:
partially_supported
```

### missing_support

Use when a documentation claim expects an artifact but no matching artifact fact exists.

Example:

```text
Documentation claim:
Repository contains Documentation Observation implementation.

Repository artifacts:
No documentation observation source, parser, or tests exist.

Outcome:
missing_support
```

### potential_conflict

Use when observed artifacts appear to conflict with a documented boundary.

Example:

```text
Documentation claim:
ToolExecutor owns execution.

Repository artifacts:
Runtime directly executes external commands without ToolExecutor.

Outcome:
potential_conflict
```

This outcome should be conservative and require explicit artifact evidence.

### not_evaluable

Use when no v0 rule exists for comparing the claim.

Example:

```text
Documentation claim:
Seed emphasizes small-context decision making.

Repository artifacts:
No v0 rule maps this claim to structural artifacts.

Outcome:
not_evaluable
```

### requires_human_review

Use when evidence exists but is ambiguous or insufficient for a safe outcome.

Example:

```text
Documentation claim:
Runtime is not a second orchestration loop.

Repository artifacts:
Runtime routes decisions and calls ToolExecutor.

Outcome:
requires_human_review
```

The reconciliation surface should show the evidence rather than decide the architecture.

## V0 Claim Families

Repository Reconciliation v0 should only compare narrow claim families.

In scope:

```text
ownership claims
boundary claims
non-goal claims
implemented-slice claims
frontier claims
existence claims
```

Out of scope:

```text
broad philosophy claims
quality claims
performance claims
security claims
maintainability claims
architectural elegance claims
operator-experience claims
```

## Support Model

Support means:

```text
Observed repository artifacts are consistent with a documentation claim.
```

Support does not mean:

```text
The claim is proven true.
```

## Support Strength

Support strength should depend on artifact evidence type.

Strong artifact evidence:

```text
matching class exists
matching function exists
matching module exists
explicit import exists
explicit method call exists if call observation exists
matching test exists
```

Moderate artifact evidence:

```text
matching file exists
matching package exists
matching catalog exists
matching script exists
```

Weak artifact evidence:

```text
filename similarity
path similarity
term appears in nearby symbol names
```

Weak evidence should not produce `supported` by itself.

## Example: ToolExecutor Owns Execution

Documentation claim:

```text
ToolExecutor owns registered-operation execution.
```

Possible repository evidence:

```text
ToolExecutor class exists.
ToolExecutor module exists.
Runtime imports ToolExecutor.
Runtime calls ToolExecutor.
Tests cover ToolExecutor execution behavior.
```

Expected outcome rules:

```text
ToolExecutor class exists only -> partially_supported
ToolExecutor class + Runtime import -> partially_supported
ToolExecutor class + Runtime call -> supported
ToolExecutor absent -> missing_support
Runtime executes operations directly without ToolExecutor -> potential_conflict
```

## Example: ProjectionStore Owns Cached Projected State

Documentation claim:

```text
ProjectionStore owns cached projected state.
```

Possible repository evidence:

```text
ProjectionStore protocol exists.
InMemoryProjectionStore exists.
SQLiteProjectionStore exists.
projection_snapshots storage exists.
state cache CLI references ProjectionStore.
```

Expected outcome rules:

```text
ProjectionStore protocol + concrete implementation -> supported
ProjectionStore protocol only -> partially_supported
No ProjectionStore symbols -> missing_support
Separate unrelated cache implementation bypasses ProjectionStore -> potential_conflict
```

## Example: Response Is Not A ResponseEngine

Documentation claim:

```text
ResponseEngine is rejected.
```

Possible repository evidence:

```text
No ResponseEngine class exists.
Response behavior exists across runtime envelopes, CLI output, explanations, and state views.
```

Expected outcome rules:

```text
No ResponseEngine symbol -> supported
ResponseEngine symbol exists -> potential_conflict
```

This does not prove the distributed response model is correct.

It only checks a rejected-concept claim against artifacts.

## Example: Knowledge Acquisition Frontier

Documentation claim:

```text
Users Observation is a current frontier.
```

Possible repository evidence:

```text
No Users Observation implementation exists.
No Users Observation tests exist.
```

Expected outcome:

```text
supported
```

Why: a frontier claim may be supported by absence of implementation when the claim says the work remains future.

This requires claim-family awareness.

## Example: Implemented Observation Slice

Documentation claim:

```text
Listening Port Observation is implemented.
```

Possible repository evidence:

```text
listening port observer source exists.
local host observer references listening port data.
tests cover listening port observation.
```

Expected outcome rules:

```text
source + tests exist -> supported
source exists but no tests observed -> partially_supported
no source observed -> missing_support
```

## Evidence Requirements

Every reconciliation result should retain:

```text
documentation fact id or evidence reference
repository fact ids or evidence references
reconciliation rule id
outcome
confidence
reason
```

The reason should be concise and evidence-specific.

Example:

```text
ProjectionStore claim is supported because repository facts show a ProjectionStore protocol and SQLiteProjectionStore implementation.
```

## Rule Requirements

Reconciliation rules should be explicit.

A rule should define:

```text
claim family
required artifact patterns
support threshold
partial support threshold
conflict patterns
fallback outcome
```

Rules should be deterministic.

Rules should be inspectable.

Rules should not require an LLM.

## Confidence Rules

Suggested confidence levels:

```text
high
medium
low
```

High confidence:

```text
Direct symbol/path evidence satisfies the rule.
```

Medium confidence:

```text
Partial direct evidence exists but some expected support is absent.
```

Low confidence:

```text
Only pattern-based evidence exists or evidence is ambiguous.
```

`requires_human_review` should usually be low or medium confidence.

## Explanation Requirements

Repository Reconciliation should be explainable.

A user should be able to ask:

```text
Why is this claim marked partially_supported?
```

and receive:

```text
The documentation claim says ToolExecutor owns registered-operation execution.
Repository artifacts show a ToolExecutor class and Runtime import, but v0 did not observe a direct call/use relationship, so the result is partially_supported.
```

## Non-Goals

Repository Reconciliation v0 is not:

```text
architecture enforcement
code review
design review
implementation planning
automated refactoring
automated issue creation
runtime validation
static analysis
security analysis
quality scoring
```

## Completion Criteria

Repository Reconciliation v0 is characterized when it has:

```text
outcome vocabulary
claim families
support model
support strength rules
example claim-to-artifact comparisons
confidence rules
evidence requirements
explanation requirements
non-goals
```

This document provides that characterization.

## Recommended Next Step

The next document should be:

```text
Repository Reconciliation Design
```

That design should explain:

* where reconciliation rules live;
* how rules consume documentation and repository facts;
* how outcomes are projected;
* how explanations cite both sides;
* why reconciliation does not become architecture enforcement;
* why Runtime, ToolExecutor, EventLedger ownership, and ProjectionStore ownership remain unchanged.

## Conclusion

Repository Reconciliation is where Seed begins forming alignment knowledge.

It compares claims and artifacts.

It does not decide truth.

It should remain read-only, evidence-backed, deterministic, and explainable.

# Repository Reconciliation v0 Implementation Characterization

## Purpose

This document characterizes the smallest useful implementation slice for Repository Reconciliation v0.

It intentionally defines only a tiny deterministic comparison path.

The goal is to prove:

```text
Documentation Claim
+
Repository Artifact Fact
        ↓
Alignment Record
```

without implementing broad self-model behavior.

## Implementation Slice

Repository Reconciliation v0 should consume fixture-level or extractor-level records from:

```text
Documentation Observation v0
Repository Observation v0
```

and produce minimal alignment records.

No projection.

No runtime integration.

No ToolExecutor integration.

No broad architecture evaluation.

## Inputs

Input one:

```text
DocumentationClaim
```

Input two:

```text
RepositoryArtifactFact
```

These inputs may initially come from fixture data or small deterministic extractors.

They do not need to be projected state in v0.

## Output

Output:

```text
AlignmentRecord
```

Conceptual record:

```text
AlignmentRecord
  claim
  artifact_facts
  outcome
  rule_id
  reason
```

This is an implementation convenience.

It is not a new store.

## V0 Outcome Vocabulary

Keep v0 deliberately small.

Allowed outcomes:

```text
supported
missing_support
potential_conflict
not_evaluable
```

Do not include in v0:

```text
partially_supported
requires_human_review
confidence
support strength
```

Those can come later.

## V0 Claim Families

Only compare:

```text
ownership claims
rejected concept claims
frontier claims
```

Everything else should become:

```text
not_evaluable
```

## Ownership Claim Rules

### ProjectionStore owns cached projected state

Claim pattern:

```text
ProjectionStore owns cached projected state.
```

Supporting artifact patterns:

```text
ProjectionStore class or protocol exists.
SQLiteProjectionStore exists.
InMemoryProjectionStore exists.
```

Outcome rules:

```text
any matching ProjectionStore artifact -> supported
no matching artifact -> missing_support
```

### ToolExecutor owns registered-operation execution

Claim pattern:

```text
ToolExecutor owns registered-operation execution.
```

Supporting artifact patterns:

```text
ToolExecutor class exists.
ToolExecutor module exists.
```

Outcome rules:

```text
matching ToolExecutor artifact -> supported
no matching artifact -> missing_support
```

V0 does not require call graph evidence.

## Rejected Concept Rules

Rejected concept claim pattern:

```text
X is rejected.
```

where X may be:

```text
ResponseEngine
IntegrityEngine
SelectionEngine
CaveatEngine
ContextEngine
ReasoningEngine
TruthEngine
ClaimStore
SupportStore
WorkflowEngine
Planner
```

Outcome rules:

```text
matching artifact absent -> supported
matching artifact present -> potential_conflict
```

This does not prove the rejection claim true.

It only says repository artifacts do or do not conflict with the documented rejection.

## Frontier Claim Rules

Frontier claim pattern:

```text
X Observation is a current frontier.
```

or:

```text
X Observation is a current capability-growth priority.
```

Supporting artifact pattern:

```text
X Observation implementation absent.
```

Outcome rules:

```text
implementation absent -> supported
implementation present -> potential_conflict
```

V0 treats frontier claims as supported by absence because the claim describes future or active work.

## Not Evaluable Rules

Claims outside the v0 family list become:

```text
not_evaluable
```

Examples:

```text
Seed is knowledge-first.
Response communicates knowledge.
Integrity does not determine truth.
Knowledge Integrity is stable.
```

V0 should not attempt to reconcile these.

## Matching Boundary

Matching should be conservative.

Allowed matching:

```text
exact symbol match
exact file/module stem match
explicit normalized claim target
```

Disallowed matching:

```text
semantic similarity
LLM interpretation
fuzzy architecture matching
broad grep summaries
```

## Evidence Preservation

Each alignment record should preserve references to:

```text
documentation claim record
repository artifact fact records used
rule id
outcome
reason
```

If no artifact supports or conflicts with a claim, preserve the claim record and the rule used to determine absence.

## Tests To Add Later

If implemented, tests should use fixture records.

Test categories:

```text
ownership claim supported by matching artifact
ownership claim missing support when artifact absent
rejected concept supported by artifact absence
rejected concept potential conflict when artifact present
frontier claim supported by implementation absence
unknown claim family not_evaluable
```

Tests should not parse real repo state initially.

Tests should not call Runtime, ToolExecutor, EventLedger, or ProjectionStore.

## Success Criteria

Repository Reconciliation v0 succeeds when:

```text
Given a small set of documentation claim records
and repository artifact fact records,
Seed can produce deterministic alignment records
for ownership, rejected concept, and frontier claims.
```

## Failure Criteria

The slice fails if implementation requires:

```text
projection integration
runtime invocation
ToolExecutor integration
call graph construction
LLM interpretation
architecture scoring
truth arbitration
human review loops
```

## Recommended Next Step

Implement a fixture-only reconciliation helper before connecting to real extractors.

Suggested order:

1. define claim and artifact fixture records;
2. define three deterministic rule families;
3. produce alignment records;
4. add tests for supported, missing_support, potential_conflict, and not_evaluable.

Do not project alignment records yet.

Do not integrate with Runtime.

## Conclusion

Repository Reconciliation v0 should be tiny.

It should prove that claims and artifacts can be compared deterministically.

Only after that works should Seed consider richer support relationships, projection, explanation, or self-model integration.

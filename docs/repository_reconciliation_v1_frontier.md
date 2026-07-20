# Repository Reconciliation v1 Frontier

## Purpose

This document defines the next frontier for Repository Reconciliation after the fixture-level self-model acquisition pipeline proved that documentation claims, repository artifact facts, and alignment records can compose end-to-end.

It is documentation-only. It does not modify production code, tests, runtime behavior, repository observation, documentation observation, tool execution, event storage, projection behavior, or package exports.

The motivating question is:

```text
How should Seed move beyond the v0 hard-coded reconciliation rules
without pretending it understands more than it does?
```

## Current Baseline

Seed now has a minimal self-model acquisition spine:

```text
Documentation text
        ↓
DocumentationClaim

Python source text
        ↓
RepositoryArtifactFact

DocumentationClaim
+
RepositoryArtifactFact
        ↓
AlignmentRecord
```

The current v0 reconciliation rules are deliberately narrow:

- ownership claims for `ToolExecutor`;
- ownership claims for `ProjectionStore` and known projection-store implementations;
- rejected-concept claims matching a narrow text pattern;
- frontier claims matching a narrow observation text pattern.

This is correct for v0. The system should not over-generalize from symbol existence to architectural truth.

## Problem Statement

The next gap is not acquisition.

Documentation Observation v0 can extract explicit claims from supplied documentation text. Repository Observation v0 can extract artifact facts from supplied Python source text. Reconciliation v0 can produce alignment records from supplied claims and artifact facts.

The next gap is semantics and generalization:

```text
What evidence should support a broader class of claims?
```

Especially:

```text
What does it mean for code to support an ownership claim?
```

## Why v0 Should Not Simply Search Symbols

A naive v1 could say:

```text
If documentation says X owns Y,
and repository artifacts mention X,
then the claim is supported.
```

That is too weak.

Symbol existence proves only that an artifact exists. It does not prove:

- ownership;
- responsibility;
- route authority;
- behavioral boundary;
- runtime usage;
- invariants;
- architectural intent.

For example:

```text
class MagicExecutor:
    pass
```

would prove that `MagicExecutor` exists, but it would not prove that `MagicExecutor owns all execution`.

Therefore v1 must distinguish:

```text
symbol existence support
```

from:

```text
behavioral / architectural ownership support
```

## Claim Families To Consider For v1

v1 should not support every claim family.

Candidate families, from safest to riskiest:

### Existence claims

Examples:

```text
ToolExecutor exists.
ProjectionStore exists.
Runtime defines handle_user_message.
```

These are the easiest to support from repository artifacts.

Likely evidence:

- module fact;
- class fact;
- function fact;
- import fact.

### Rejected-concept claims

Examples:

```text
ResponseEngine is rejected.
InputEngine is rejected.
```

Current v0 semantics are reasonable:

- no matching artifact mention -> `supported`;
- matching artifact mention -> `potential_conflict`.

v1 may need better artifact-kind filtering so documentation mentions or tests do not count the same as production class definitions.

### Frontier claims

Examples:

```text
Users Observation is a current capability-growth priority.
```

Current v0 semantics are reasonable but conservative:

- no matching implementation artifact -> `supported`;
- matching implementation artifact -> `potential_conflict`.

v1 may need explicit mapping between frontier names and implementation symbols.

### Ownership claims

Examples:

```text
ToolExecutor owns registered-operation execution.
ProjectionStore owns cached projected-state snapshots.
Runtime remains canonical user-message intake and route owner.
```

Ownership claims are harder than existence claims.

They may require evidence from several artifact kinds:

- symbol/class existence;
- method/function existence;
- route call sites;
- imports;
- tests asserting boundaries;
- architecture metadata such as `__seed_arch__`;
- invariants documentation;
- absence of competing owners.

v1 should expand ownership only with explicit rules, not broad inference.

## Possible v1 Evidence Levels

v1 may need to distinguish evidence levels without adding confidence scores yet.

Suggested internal vocabulary, documentation-only:

```text
existence_evidence
structural_evidence
behavioral_evidence
boundary_evidence
negative_evidence
```

### `existence_evidence`

The artifact exists.

Examples:

- class definition exists;
- function definition exists;
- module exists.

This is enough for existence claims, but usually insufficient for ownership claims.

### `structural_evidence`

The artifact has expected structural shape.

Examples:

- `Runtime` defines `handle_user_message`;
- `ToolExecutor` defines `execute`;
- `ProjectionStore` defines a protocol or store methods.

This may partially support ownership claims.

### `behavioral_evidence`

The artifact participates in the claimed behavior.

Examples:

- `Runtime._route` calls `ToolExecutor.execute` only for `call_tool` decisions;
- projection cache helpers call `ProjectionStore` methods;
- state projection reads events from `EventLedger`.

This is stronger support for ownership claims.

### `boundary_evidence`

Tests or invariant docs preserve the claimed boundary.

Examples:

- tests assert `request_tool` does not execute;
- docs assert `call_tool` is the only runtime path to `ToolExecutor`;
- tests assert projection cache does not append ledger events.

This is strong support for architectural ownership and boundary claims.

### `negative_evidence`

The artifact is absent, or a competing pattern is absent, within an explicitly scoped acquisition set.

This must be used carefully.

Absence from a fixture is not repository-wide absence. Absence can support a claim only when acquisition scope is explicit and sufficient.

## v1 Ownership Strategy

v1 should not generalize ownership as:

```text
X owns Y if symbol X exists.
```

Instead, v1 should start with explicit ownership rule profiles.

Example profile shape, documentation-only:

```text
OwnershipRuleProfile:
  owner_symbol: ToolExecutor
  claim_patterns:
    - owns registered-operation execution
    - owns execution
  required_evidence:
    - class ToolExecutor exists
    - function or method execute exists
  optional_evidence:
    - Runtime routes call_tool to ToolExecutor
    - tests assert request_tool does not execute
    - docs/invariants.md preserves call_tool-only boundary
  conflict_evidence:
    - another executor class is routed from Runtime for call_tool
```

This keeps generalization explicit and auditable.

## Suggested v1 Claim Outcomes

Do not add new outcomes yet unless necessary.

The current outcomes are still sufficient:

```text
supported
missing_support
potential_conflict
not_evaluable
```

But v1 should be clearer about why a claim is supported.

Instead of only:

```text
outcome=supported
```

v1 should preserve rule reasons such as:

```text
supported by existence evidence
supported by structural evidence
supported by boundary evidence
```

This can remain in `rule_id` and `reason` before adding new fields.

## What v1 Should Not Do

v1 should not:

- add repository scanning as part of reconciliation itself;
- read files from disk inside reconciliation;
- use LLMs;
- infer arbitrary ownership from symbol existence;
- treat documentation as truth;
- treat artifact existence as behavioral support;
- treat absence from a fixture as repository-wide absence;
- add confidence scoring prematurely;
- add graph construction prematurely;
- integrate with Runtime;
- integrate with ToolExecutor;
- integrate with EventLedger;
- integrate with ProjectionStore;
- add a ReconciliationEngine.

## Relationship To Acquisition

Repository Reconciliation should remain downstream of acquisition.

```text
Documentation Observation
        ↓
DocumentationClaim

Repository Observation
        ↓
RepositoryArtifactFact

Repository Reconciliation
        ↓
AlignmentRecord
```

Repository Reconciliation should not own:

- markdown parsing;
- AST parsing;
- repository traversal;
- file IO;
- runtime routing;
- tool execution;
- projection.

It should consume supplied claim and artifact records.

## Recommended Next Implementation Slice

The safest v1 implementation slice is not broad ownership inference.

Recommended first slice:

```text
Add existence-claim reconciliation.
```

Example claims:

```text
ToolExecutor exists.
ProjectionStore exists.
Runtime defines handle_user_message.
```

Why this slice:

- artifact evidence is straightforward;
- semantics are less ambiguous;
- it exercises generalized symbol matching without pretending to prove ownership;
- it prepares for stronger ownership support later.

Suggested fixture tests:

- documentation claim `ToolExecutor exists.` + class artifact `ToolExecutor` -> `supported`;
- documentation claim `MagicExecutor exists.` + no matching artifact -> `missing_support` if the claim pattern is recognized and artifact acquisition scope is supplied;
- documentation claim `Runtime defines handle_user_message.` + class/function artifacts -> `supported`;
- unrelated existence claim outside recognized pattern -> `not_evaluable`.

Only after existence claims are stable should v1 expand ownership profiles.

## Recommended Next Documentation Slice

Before implementing ownership v1, create:

```text
docs/ownership_claim_support_characterization.md
```

Purpose:

```text
Define what kinds of evidence can support ownership claims,
using ToolExecutor, ProjectionStore, Runtime, EventLedger, and StateProjector as examples.
```

This should prevent the system from flattening ownership into symbol existence.

## Documentation-Only Status

This document defines the Repository Reconciliation v1 frontier only. It does not modify production code, tests, reconciliation behavior, acquisition behavior, runtime behavior, tool execution, event storage, projection behavior, package exports, or local CLI behavior.

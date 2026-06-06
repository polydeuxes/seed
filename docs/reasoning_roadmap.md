# Reasoning system roadmap

Seed's accepted Core MVP is a knowledge and capability-discovery runtime:

```text
Input / observations
-> evidence / facts
-> relationships / entity types
-> explanations / current state
-> ToolNeed
-> capability_resolution
-> registered operation candidates
-> provider/handoff recommendations
```

The runtime is canonical. `ToolExecutor` is the only registered-operation executor.
`ProjectionStore` owns cached projected state snapshots. `EventLedger` owns
append-only events.

This roadmap captures the next reasoning-system foundation areas without adding
runtime behavior, planning orchestration, workflow execution, host mutation,
network calls, shell execution, or LLM-driven projection logic.

Future capability growth should follow the [Capability Extension Methodology](capability_extension_methodology.md): identify the gap, reduce it to the narrowest fact, choose the least-privileged source of truth, prefer read-only observation, and keep observation, inference, verification, and execution separate.

## 1. Explicit invariants

### Purpose

Make Seed's architectural and runtime boundaries executable and reviewable so the
repo can prevent architecture drift before it reaches runtime behavior.

### Why Seed needs it

Seed has recently been cleaned up around the Core MVP. Explicit invariants keep
that cleanup durable by asserting boundaries such as:

- `Runtime` is the only canonical runtime.
- `call_tool` is the only `Runtime` path into `ToolExecutor`.
- `request_tool` never executes.
- `ToolExecutor` is the only registered-operation executor.
- `CapabilityCatalog` never executes.
- `CapabilityRecommendation.operation` is provider/handoff metadata only.
- `EventLedger` owns append-only events.
- `ProjectionStore` owns cached projected state.
- `ProjectionStore` never owns events.
- `EventLedger` never owns projection snapshots.
- `RuntimeLoop` must not be present or reachable.
- `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and
  `ExecutionAuthorization` are not Core MVP runtime artifacts.

### Current repo support

- `Runtime` routes validated decisions to owner services.
- `ToolExecutor` owns registered-operation execution.
- `ToolNeedService.resolve_capability` returns read-only capability-resolution
  metadata.
- `CapabilityCatalog` exposes provider and handoff suggestions as catalog
  metadata.
- `EventLedger` and `SQLiteEventLedger` expose append/list event APIs.
- `ProjectionStore`, `InMemoryProjectionStore`, and `SQLiteProjectionStore`
  expose snapshot load/save/clear APIs.
- Generated architecture metadata already marks major ownership boundaries.

### Missing pieces

- A single invariant test module that guards the accepted boundaries.
- A human-readable invariant document that maps each boundary to the owning
  module and failure mode.
- Clear quarantine tests for historical planning artifacts.

### Explicit non-goals

- Do not add `RuntimeLoop`.
- Do not wire planning artifacts into `Runtime`.
- Do not add selection services, schedulers, retry engines, secret systems, or
  workflow orchestration.
- Do not make `CapabilityCatalog` executable.
- Do not call `ToolExecutor` from `request_tool`.

### Smallest safe next implementation

Add `tests/test_architecture_invariants.py` with small behavior- or API-based
checks for the accepted boundaries.

## 2. Rule inventory / explain-rules

### Purpose

Prepare Seed to answer: "What deterministic rules does Seed apply?"

### Why Seed needs it

Seed's reasoning is catalog- and projection-driven. Users and developers need a
read-only explanation surface that can list deterministic rules without implying
there is a new rule engine or hidden planner.

### Current repo support

Related systems already own deterministic rules or rule-like metadata:

- `PredicateCatalog`
- `RelationshipCatalog`
- `EntityTypeCatalog`
- `InferenceCatalog`
- `StateProjector`
- `GraphValidator`

### Missing pieces

- A deterministic rule inventory format.
- A helper that reads existing catalogs and emits a stable inventory.
- A way to distinguish catalog rules, projection rules, inference rules, graph
  validation rules, and capability-resolution rules.

### Explicit non-goals

- Do not build a new rule engine.
- Do not add LLM-driven projection logic.
- Do not add planning orchestration.
- Do not invent rules that are not represented by current code or catalogs.

### Smallest safe next implementation

Add a read-only CLI/doc helper that emits a deterministic rules inventory from
existing catalogs and known validation/projection rule owners.

## 3. Contradiction handling

### Purpose

Make conflict-related semantics explicit, auditable, and explainable.

### Why Seed needs it

Knowledge runtimes encounter incompatible observations. Seed should preserve
provenance and report contradictions instead of silently choosing a truth when
current evidence conflicts.

### Current repo support

- `Fact`
- `FactSupport`
- `FactConflict`
- `PredicateCatalog` cardinality
- Confidence and provenance fields
- Graph validation issues

### Missing pieces

Seed needs stronger explicit semantics for:

- `conflict`
- `superseded`
- `uncertain`
- `disputed`
- `stale`

### Explicit non-goals

- Do not automatically resolve truth conflicts.
- Do not add a truth-maintenance engine.
- Do not collapse conflicting facts without preserving evidence and provenance.

### Smallest safe next implementation

Document current conflict behavior and add focused tests around single-cardinality
predicate conflicts.

## 4. Temporal reasoning

### Purpose

Define how Seed can explain belief state across event time.

### Why Seed needs it

Seed is event-sourced. It should eventually answer:

- What was true at time T?
- When did fact X become true?
- Why did fact X stop being current?
- Which event changed this belief?

### Current repo support

- `EventLedger` timestamps
- `StateProjector`
- `ProjectionStore`
- Fact support/provenance

### Missing pieces

- Explicit as-of projection semantics by event id or timestamp.
- Audit trails that connect current facts back to changing events.
- Tests that define current-vs-historical projection expectations.

### Explicit non-goals

- Do not build a full temporal database.
- Do not replace the append-only ledger with mutable historical state.
- Do not make `ProjectionStore` own temporal truth.

### Smallest safe next implementation

Audit whether `StateProjector` can project as-of an event id or timestamp using
existing event order and timestamps.

## 5. Capability verification

### Purpose

Separate capability claims, recommendations, registered operation candidates, and
verified capability evidence.

### Why Seed needs it

Capability discovery should not imply capability truth. Seed should distinguish:

- Claimed capability
- Recommended capability
- Registered operation candidate
- Verified capability

Example flow:

1. `ssh_access` is requested.
2. `verify_ssh_access` is registered as an operation candidate.
3. Observation/evidence proves SSH is reachable.
4. Capability confidence increases.

### Current repo support

- `ToolNeed`
- `ToolSpec.capabilities`
- `ToolRegistry.list_tools_for_capability`
- `CapabilityCatalog`
- `Observation`, `Evidence`, and `Fact` models

### Missing pieces

- Capability Verification Inventory v1 is implemented as a read-only inventory
  over `Fact`, `FactSupport`, `PredicateCatalog`, projected capability surfaces,
  and supporting evidence.
- A richer scoped `CapabilityVerification` model remains future work only if
  callers need target objects beyond fact subjects/dimensions.
- Further auditable confidence policy changes remain future work; v1 reports
  existing support confidence without inventing new policy.

### Explicit non-goals

- Do not execute verification from `capability_resolution`.
- Do not mutate hosts.
- Do not add network calls.
- Do not make recommended providers executable.

### Smallest safe next implementation

Implemented: Capability Verification Inventory v1. Seed now has a read-only
`--capability-status` query that derives `verified`, `provider_reported`,
`unverified`, `stale`, and `unknown` statuses from projected facts and evidence.
This is inventory only: no verification execution, no verification engine, no
runtime changes, no orchestration, no provider calls, no host mutation, no shell
execution, no scheduling, and no retries.

## 6. Self-observation

### Purpose

Allow Seed to observe its own repository as just another system, using the same
knowledge path as external observations.

### Why Seed needs it

The repo already contains architecture metadata. Turning that metadata into
read-only observations would let Seed explain its own architecture without
self-modification or a special internal executor.

### Current repo support

- Architecture generator
- AST metadata
- `architecture_graph.json`
- `ObservationSource` pattern
- Facts, relationships, and entity types

### Future direction

Repo AST -> Observations -> Facts -> Relationships.

Example observations/facts:

- `Runtime` routes_to `ToolExecutor`.
- `ToolExecutor` owns execution.
- `ProjectionStore` owns cache.
- `RuntimeLoop` is absent.

### Missing pieces

- A read-only repository observation source design.
- Stable mapping from AST/architecture metadata to Seed observations.
- Tests that confirm self-observation does not imply self-mutation.

### Explicit non-goals

- Do not let Seed modify its own code.
- Do not create self-mutation.
- Do not add shell execution, network calls, or host mutation.

### Smallest safe next implementation

Design a read-only `RepositoryObservationSource`, but do not implement it unless
explicitly requested later.

## Seed Prompting Principles

Seed-generated work requests should follow the Codex Prompt Protocol in
`docs/codex_prompt_protocol.md`. The protocol preserves the narrative-first
structure that has kept recent Seed work aligned with the accepted architecture:
context before implementation, ownership before placement, non-goals before
expansion, and constraints before tasks.

Future prompt generation should preserve:

- context;
- ownership;
- non-goals;
- constraints;
- test requirements.

This note is documentation only. It does not implement prompt generation,
automatic prompt construction, LLM orchestration, runtime behavior, or
`ToolExecutor` behavior.

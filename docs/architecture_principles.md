# Seed Architecture Direction

Seed is primarily a reasoning system. Its durable architectural center is the ability to turn inputs and observations into explainable knowledge, then use that knowledge to reason about capability gaps and possible integrations.

Seed is primarily:

- State reasoning.
- Capability reasoning.
- Knowledge projection.
- Explanation.

Seed is not:

- Workflow orchestration.
- Internal execution management.
- A scheduler replacement.
- An AWX replacement.
- A Temporal replacement.
- A Prometheus replacement.

The current core MVP is:

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

Runtime is canonical. `RuntimeLoop` was accidental architecture drift and has been removed or quarantined from the current core architecture. `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization` are not current-core architecture.

For knowledge-facing work, keep the relationship between
[Knowledge Acquisition and Selection](knowledge_acquisition_and_selection.md),
[Knowledge Integrity](knowledge_maintenance_reconciliation.md), and the
[Knowledge Lifecycle](knowledge_lifecycle_reconciliation.md) explicit.
Acquisition creates and projects evidence-backed knowledge, Integrity
characterizes whether projected knowledge is supported or caveated, and
Selection/Response consume already-projected knowledge without creating facts,
mutating projections, or executing operations.

## Core Loop

```text
Input
  -> Observation
  -> Evidence
  -> Fact
  -> State Projection
  -> Explanation
  -> Capability Resolution
  -> Response
```

Ownership in the core loop should remain explicit:

- Input handling belongs to the canonical `Runtime` boundary and its adapters.
- Observation normalization and ingestion belong to the observation ingestion path.
- Evidence and fact creation belong to ingestion, extraction, and explicitly named state-writing services.
- Event history belongs to `EventLedger`.
- Projected current state belongs to `StateProjector` and `ProjectionStore`.
- Explanations are read-only views over projected state and evidence.
- Capability-gap creation and capability resolution belong to `ToolNeedService`.
- Registered operation inventory belongs to `ToolRegistry`.
- Capability metadata and provider/handoff recommendations belong to `CapabilityCatalog`.
- Execution belongs only to `ToolExecutor`.

## Ownership Principle

Always ask:

> Who owns this behavior?

Do not start with:

> Who calls this behavior?

Callers are allowed to route, adapt, format, or request behavior. They should not imply ownership of the behavior.

Concrete Seed examples:

- `Runtime` is canonical for runtime routing, but it does not own tool execution. `ToolExecutor` owns execution.
- CLI and API may expose projected state, but they do not own projection. `ProjectionStore` owns cached projected state, and `EventLedger` owns append-only history.
- `StateProjector` reads events to derive state, but it does not own event creation.
- `ToolNeedService` owns capability-gap creation and capability resolution, even when a runtime path or CLI command calls it.
- `ToolRegistry` owns registered operation inventory; runtime callers should not construct a competing operation inventory.
- `CapabilityCatalog` owns capability metadata and provider/handoff recommendations; provider recommendation metadata should not become an execution path.

Architecture drift often starts when a caller grows a local copy of behavior that already has a canonical owner. New code should first identify the lowest-level owner that implements the behavior, then route through that owner.

## Externalization Principle

If another mature system already owns a concern, prefer integration over reimplementation.

Seed should consume signals, events, metadata, and results from mature systems. Seed should not reimplement the operational responsibilities those systems already own.

Examples:

- Prometheus owns metrics collection, alerting rules, and time-series storage. Seed should consume relevant observations, alerts, or metric-derived facts; it should not become Prometheus.
- Ansible owns playbook execution and host automation. Seed should reason about whether an Ansible-backed operation is relevant; it should not become Ansible.
- Temporal owns durable workflow orchestration. Seed should consume workflow state or recommend workflow-capable providers; it should not become Temporal.
- AWX owns operational Ansible controller workflows, credentials, and job execution. Seed should reason about AWX capabilities and job results; it should not become AWX.
- Kubernetes owns cluster scheduling and reconciliation. Seed should consume cluster state and reason about implications; it should not become Kubernetes.
- Postgres owns relational persistence and query execution. Seed should store and query through explicit persistence boundaries; it should not recreate database semantics in application services.

Seed should own reasoning about what external data means, what capability is needed, and which registered operations or providers appear relevant. External systems should own their mature execution, scheduling, storage, authorization, retry, and reconciliation domains.

## Logic-First Principle

Seed should behave like a deterministic reasoning system before it behaves like an execution system. Its core value is in explainable transformations between knowledge layers.

Examples:

```text
Observation -> Evidence
Evidence -> Fact
Fact + Rule -> Inferred Fact
ToolNeed + Registry -> Operation Candidates
ToolNeed + CapabilityCatalog -> Recommendations
```

Logic-first design means that each transition should be explainable, deterministic where possible, and owned by a named subsystem. Facts should be traceable to evidence. Inferred facts should be traceable to facts and rules. Capability recommendations should be traceable to ToolNeeds, registered operations, and catalog metadata.

## Function-Block Principle

Every major subsystem should be drawable.

If ownership cannot be drawn clearly, ownership is probably wrong.

A useful function block shows:

- Inputs.
- Outputs.
- Canonical owner.
- Read dependencies.
- Write dependencies.
- Whether the block reasons, projects, validates, or executes.

Function blocks should expose ownership problems early. If a diagram needs two owners for the same behavior, or if a read-only projection block starts executing work, the design is drifting.

## Execution Boundary

Execution starts at `ToolExecutor`.

Everything before `ToolExecutor` should remain reasoning-oriented and read-only with respect to host execution. Pre-execution components may create events, project state, validate decisions, identify ToolNeeds, match registered operation candidates, or recommend providers. They should not run registered operations, mutate hosts, invoke provider-side execution, implement retries, or manage external workflow lifecycles.

`ToolExecutor` is the only execution owner. Runtime and decision-validation paths may decide whether a `call_tool` decision is valid and may delegate to `ToolExecutor`, but they do not become execution owners.

## Capability Hierarchy

```text
ToolNeed
    ↓
Capability
    ↓
Registered Operations
    ↓
Provider Recommendations
```

The hierarchy separates reasoning concepts from executable inventory:

- `ToolNeed` describes a capability gap or requested capability.
- A capability describes what kind of ability would satisfy the need.
- Registered operations are executable entries owned by `ToolRegistry`.
- Provider recommendations are metadata owned by `CapabilityCatalog`.

Capabilities are not executable.

Registered operations are executable.

Provider recommendations are metadata. They can guide a human, runtime response, or integration decision, but they do not execute work by themselves.

# Repository invariants

These invariants describe the accepted Seed architecture. They are intended to be
readable documentation today and executable architecture checks over time.

## Runtime invariants

- `Runtime` is canonical.
- `RuntimeLoop` must not exist in active runtime paths.
- `request_tool` records and resolves a capability gap; it does not execute.
- `call_tool` is the only `Runtime` path to `ToolExecutor`.

## Execution invariants

- `ToolExecutor` owns registered-operation execution.
- `ToolExecutionPolicyService` evaluates execution policy; it does not execute.
- `PendingActionService` owns pending-action lifecycle events.
- `CapabilityCatalog` is read-only capability/provider metadata; it does not
  execute.
- `CapabilityRecommendation.operation` is provider/handoff metadata, not a
  registered operation invocation.

## Projection invariants

- `EventLedger` owns append-only events.
- `ProjectionStore` owns cached projected-state snapshots.
- `StateProjector` owns projection from events to current state.
- `ProjectionStore` must not append events.
- `EventLedger` must not store projection snapshots.

## Capability invariants

- `ToolNeed` is a capability gap, not an executable tool.
- `ToolSpec.name` is the registered operation name.
- `ToolSpec.capabilities` are inert discovery metadata.
- `ToolRegistry` exposes registered operations by capability.
- Capability resolution is read-only.
- Capability resolution never implies verification.
- ToolNeed creation never implies verification.
- Known capability catalog metadata never implies verification.
- Provider recommendation never implies verification.
- CapabilityRecommendation operation metadata never implies verification.
- Registered operation candidate discovery never implies verification.
- A `verify_*` operation name never implies verification.
- Evidence-like objects are not verified capabilities without a scoped
  verification status model.

## Capability extension invariants

- Observation must not imply execution.
- Observation must not imply availability.
- Capability resolution must not imply verification.
- Write access must not be required for observation.
- Prefer least-privileged observation sources.
- Observation must not claim more than the selected source directly supports.
- Read-only observation must remain separate from mutation, provider calls, and
  registered-operation execution.

## Capability verification invariants

- Capability verification is not implemented in the current runtime.
- Requested capability, known capability, candidate capability, and
  provider-recommended capability are not synonyms for verified capability.
- Unverified is the default state for requested, known, candidate, and
  provider-recommended capabilities unless a future scoped verification model
  proves otherwise.
- Stale verification must not be treated as current positive verification.
- Failed verification requires accepted negative evidence; it is not merely the
  absence of positive evidence.
- Future verification should be modeled as a separate scoped read model with
  explicit status, evidence, target, freshness, and boundary semantics.
- `Runtime` must not add implicit verification behavior during capability
  resolution.
- `ToolExecutor` must not interpret capability metadata as verification.
- `CapabilityCatalog` remains read-only metadata and must not become a
  verification authority by catalog presence alone.

## Historical/quarantine invariants

- `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and
  `ExecutionAuthorization` are not Core MVP artifacts.
- If retained, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and
  `ExecutionAuthorization` are historical or legacy compatibility artifacts only.
- Historical planning artifacts must not become active runtime orchestration,
  scheduling, retry, selection, or execution systems.

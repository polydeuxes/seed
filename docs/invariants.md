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

## Historical/quarantine invariants

- `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and
  `ExecutionAuthorization` are not Core MVP artifacts.
- If retained, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and
  `ExecutionAuthorization` are historical or legacy compatibility artifacts only.
- Historical planning artifacts must not become active runtime orchestration,
  scheduling, retry, selection, or execution systems.

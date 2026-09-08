# Operational Responsibility Slice 003

## selected execution boundary

Execution realization is not execution recording.

This slice selected the recovered boundary:

```text
Execution Realization
  !=
Execution Recording
```

The boundary was selected because the registered-operation executor already preserves separate architectural concerns in surrounding services: `ToolExecutionPolicyService` stops before execution and eventing, `ToolExecutor` owns registered-operation execution, and `FactExtractionService` observes completed tool-call events after recording. Inside the allowed execution path, however, the callable invocation and output validation were embedded directly between event-ledger writes.

## implementation evidence

Repository evidence supporting this boundary already existed before this slice:

- `docs/audit/core_mvp_inventory_audit.md` classifies `ToolExecutionPolicyService` as validation-before-policy preflight that is explicitly non-executing and non-eventing.
- `docs/audit/core_mvp_inventory_audit.md` classifies `ToolExecutor` as registered-operation execution, policy outcome routing, pending-action creation/resume, events, and output validation.
- `docs/audit/capability_operation_vocabulary_audit.md` distinguishes `ToolExecutionPolicyService` as policy sequencing with no direct execution from `ToolExecutor` as the service that executes and emits results/events.
- `operational_responsibility_slice_002.md` lists registered operation validation versus registered operation execution, and execution result recording versus mutation or cluster truth, as already recovered boundaries requiring fresh implementation evidence before further slices.

Direct implementation evidence in this slice:

- `ToolExecutor.execute()` delegates validation and policy preflight to `ToolExecutionPolicyService.evaluate_with_state_factory()` before any allowed execution path runs.
- `_execute_allowed_tool_call()` appends `tool.call.started`, appends `tool.call.failed` on exceptions, appends `tool.call.completed` on success, and calls `FactExtractionService.observe_tool_result()` after completion.
- Before this slice, `_execute_allowed_tool_call()` also loaded the registered callable, invoked it, and validated its output inline between those recording operations.
- After this slice, `_realize_registered_operation()` owns the registered callable invocation and output validation while `_execute_allowed_tool_call()` retains event recording and result shaping.

## before

Before this slice, `_execute_allowed_tool_call()` compressed two recovered responsibilities in one method body:

1. Execution recording:
   - append `tool.call.started`;
   - append `tool.call.failed`;
   - append `tool.call.completed`;
   - trigger post-completion fact extraction from the completed event.
2. Execution realization:
   - resolve the registered implementation;
   - call the registered function with `ToolContext` and arguments;
   - validate the returned output schema.

The behavior was already correct, but the implementation made the recovered architecture less visible because the actual registered callable realization appeared as inline code inside the event-recording corridor.

## after

After this slice, `_execute_allowed_tool_call()` remains the compatibility-preserving allowed-call orchestration and recording path. It still creates the same `ToolContext`, catches the same exception class, appends the same events, returns the same `ToolCallResult` shapes, and triggers fact extraction after the same completed event.

The new private `_realize_registered_operation()` method owns only the implementation-local realization step:

- load the registered implementation;
- invoke the callable;
- validate the output schema;
- return the realized output to the recording path.

The abstraction is private and implementation-local. It does not rename public concepts, serialized fields, CLI vocabulary, events, schemas, manifests, APIs, or JSON payloads.

## boundary made explicit

The boundary made more explicit is:

```text
Execution Realization
  !=
Execution Recording
```

The implementation now shows that executing the registered callable and recording the lifecycle of that execution are neighboring but separate responsibilities. Recording remains in `_execute_allowed_tool_call()`, while realization is concentrated in `_realize_registered_operation()`.

This better reflects the recovered execution architecture because the registered callable can be seen as the realization step inside an already-authorized allowed call, not as the same responsibility as ledger event creation or completed-event observation.

## compatibility preserved

No.

No compatibility boundary changed.

Preserved boundaries:

- no public rename;
- no schema change;
- no event change;
- no manifest change;
- no CLI change;
- no API change;
- no JSON shape change;
- no ledger change;
- no policy behavior change;
- no runtime routing change;
- no behavior change intended.

## files changed

- `seed_runtime/execution.py`
  - Added private `_realize_registered_operation()` implementation-local method.
  - Updated `_execute_allowed_tool_call()` to delegate callable invocation and output validation to that method while preserving event recording.
- `operational_responsibility_slice_003.md`
  - Added this report.

## LOC changed

Implementation LOC changed, excluding this report:

```text
seed_runtime/execution.py: +20 / -6 / net +14
```

## tests executed

```text
pytest -q tests/test_execution.py tests/test_tool_validation.py tests/test_runtime_loop.py
```

Result:

```text
26 passed in 0.93s
```

## remaining compressed execution boundaries

The following recovered execution boundaries remain candidates for future slices, subject to fresh implementation evidence before any change:

- Registered operation validation versus registered operation execution in the call-tool path.
- Policy denial routing versus pending-action lifecycle creation in the call-tool path.
- Pending-action approval/resume event context reconstruction versus allowed execution realization.
- Execution result recording versus downstream fact/evidence observation.

No future slice should assume these are currently compressed without first re-reading implementation evidence.

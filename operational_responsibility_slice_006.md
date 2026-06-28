# Operational Responsibility Slice 006

## Selected architectural boundary

Execution Recording != Post-Execution Knowledge Extraction.

The selected boundary is the terminal boundary in the registered-operation execution path. Execution recording preserves runtime history by appending durable tool-call events. Post-execution knowledge extraction consumes a completed execution record and promotes the recorded output into evidence through the existing fact-extraction service.

## Implementation evidence

- `ToolExecutor._execute_allowed_tool_call` is the allowed registered-operation path after validation and policy authorization.
- Before this slice, the success branch of `_execute_allowed_tool_call` appended `tool.call.completed` and immediately called `self.fact_extraction.observe_tool_result(completed_event)` in the same method body.
- `FactExtractionService.observe_tool_result` already represented the post-execution extraction responsibility: it accepts `tool.call.completed` or legacy `tool.result` events and appends `evidence.observed`.
- The implementation therefore already had separate recording and extraction behaviors, but the transition from execution recording to post-execution knowledge extraction was compressed at the call site.

## Before

`ToolExecutor._execute_allowed_tool_call` mixed the end of execution recording with post-execution knowledge extraction:

1. Append `tool.call.started`.
2. Realize the registered implementation.
3. Append `tool.call.failed` on implementation/output-validation failure.
4. Append `tool.call.completed` on success.
5. Immediately call `FactExtractionService.observe_tool_result` from the same success branch.
6. Return the existing `ToolCallResult`.

That made the architectural handoff from durable execution history to evidence extraction implicit inside one implementation block.

## After

`ToolExecutor._execute_allowed_tool_call` now delegates the existing success behavior to two implementation-local responsibilities:

1. `_record_completed_tool_call(...)` appends the `tool.call.completed` runtime-history event and returns the event.
2. `_extract_post_execution_knowledge(completed_event)` consumes that durable completion event and invokes the unchanged `FactExtractionService.observe_tool_result` pipeline.

The order, payloads, event kinds, causation, correlation, result shape, and extraction behavior remain unchanged.

## Boundary made explicit

The recovered boundary is directly observable inside `seed_runtime/execution.py`:

```text
registered implementation output
    -> _record_completed_tool_call(...)
    -> tool.call.completed event
    -> _extract_post_execution_knowledge(completed_event)
    -> evidence extraction
```

Execution recording no longer appears to own knowledge extraction. Knowledge extraction no longer appears to be part of event recording; it consumes the completed execution record after that record exists.

## Compatibility preserved

No compatibility boundary changed.

Preserved boundaries:

- No public rename.
- No schema change.
- No event change.
- No manifest change.
- No CLI change.
- No API/JSON/ledger change.
- No execution behavior change.
- No event recording semantics change.
- No fact extraction behavior change.
- No projection behavior change.
- `ToolExecutor.execute` continues to return the same `ToolCallResult` shape.

## Files changed

- `seed_runtime/execution.py`
  - Added `_record_completed_tool_call` as the implementation-local execution-recording responsibility for successful tool calls.
  - Added `_extract_post_execution_knowledge` as the implementation-local post-execution extraction handoff.
  - Preserved the existing call order and result payload.
- `tests/test_execution.py`
  - Added a regression test proving post-execution knowledge extraction receives an already-recorded `tool.call.completed` event while preserving the historical event sequence.
- `docs/generated/architecture/architecture_graph.json`
  - Refreshed generated architecture graph output so the implementation-local calls are visible to the architecture generator.

## LOC changed

From `git diff --stat` before commit:

```text
docs/generated/architecture/architecture_graph.json |  8 +++++
seed_runtime/execution.py                          | 40 ++++++++++++++++++----
tests/test_execution.py                            | 25 ++++++++++++++
3 files changed, 66 insertions(+), 7 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_execution.py
python scripts/generate_architecture.py
pytest -q tests/test_fact_extraction.py tests/test_execution.py tests/test_architecture_generator.py
```

Results:

```text
6 passed
11 passed
```

## Remaining compressed operational boundaries

Potential future slices, if implementation evidence confirms compression, should remain one boundary at a time:

- Pending-action creation vs. policy denial routing in `ToolExecutor._policy_denied`.
- Approved pending action resumption vs. fresh call authorization in `ToolExecutor.resume_approved_tool_call`.
- Policy outcome recording vs. pending-action lifecycle ownership.
- RuntimeLoop-specific tool-result recording vs. RuntimeLoop-specific evidence event id collection.

These are observations for future investigation only; this slice changes exactly one boundary.

## Questions

### 1. Where were execution recording and post-execution knowledge extraction previously mixed?

They were mixed inside the success branch of `ToolExecutor._execute_allowed_tool_call`, where the method appended `tool.call.completed` and immediately called `self.fact_extraction.observe_tool_result(completed_event)` in the same implementation block.

### 2. Which recovered architectural boundary became more explicit?

Execution Recording != Post-Execution Knowledge Extraction.

### 3. How does the implementation now better reflect recovered architecture?

The implementation now records the completed execution through `_record_completed_tool_call` and then hands that durable completion event to `_extract_post_execution_knowledge`. The fact-extraction pipeline still behaves exactly as before, but its ownership is visible as post-execution extraction rather than event recording.

### 4. Did any compatibility boundary change?

No.

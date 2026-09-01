# Operational Responsibility Slice 005

## Selected architectural boundary

Registered Operation Validation != Policy Authorization.

The selected boundary follows the current registered-operation call path after an already selected `call_tool` operation has been resolved and before dispatch realizes the implementation. Validation answers whether the named registered operation exists, is executable by registration status, and accepts the provided input shape. Policy authorization answers whether that validated operation may execute now.

## Implementation evidence

- `DecisionValidator._validate_tool_call` validates the model/runtime `call_tool` decision by delegating to `ToolValidationService.validate_tool_input`, which checks tool-name presence and input schema against current state/registry visibility before routing.
- `ToolValidationService.select_operation` resolves the already selected operation name from a `call_tool` decision and explicitly avoids capability recommendation or provider selection.
- `ToolExecutionPolicyService.evaluate_with_state_factory` is the transition point used by `ToolExecutor.execute` before any tool-call event is recorded or registered implementation is realized.
- Before this slice, `ToolExecutionPolicyService._evaluate` performed existence validation, status validation, input validation, lazy state projection, and policy evaluation in one method.
- `ToolExecutor.execute` already treated non-valid validation as failure and non-allow policy as denial/pending routing, so behavior did not require semantic changes.

## Before

`ToolExecutionPolicyService._evaluate` mixed the operation-contract validation sequence and policy authorization sequence in one implementation body:

1. Validate existence.
2. Validate registration status.
3. Validate input schema.
4. Project state through the supplied state provider.
5. Evaluate `PolicyGate`.
6. Return the historical combined `ToolExecutionPolicyResult`.

That made the transition from a validated selected operation to an authorized executable operation implicit inside one method.

## After

`ToolExecutionPolicyService._evaluate` now delegates to two implementation-local responsibilities:

1. `_validate_registered_operation_call` returns `RegisteredOperationValidationResult` after existence, status, and input-schema validation only.
2. `_authorize_validated_operation` accepts only that validated result, projects state lazily, evaluates policy, and returns the existing `ToolExecutionPolicyResult` shape.

The public service result and caller behavior remain unchanged.

## Boundary made explicit

The recovered boundary is directly observable inside `seed_runtime/tool_execution_policy.py`:

```text
selected registered operation + valid input
    -> RegisteredOperationValidationResult
    -> policy authorization
    -> ToolExecutionPolicyResult
```

Validation no longer appears to authorize execution. Authorization no longer appears to own operation-contract validation.

## Compatibility preserved

No compatibility boundary changed.

Preserved boundaries:

- No public rename.
- No schema change.
- No event change.
- No manifest change.
- No CLI change.
- No API/JSON/ledger change.
- No authorization behavior change.
- No validation behavior change.
- `ToolExecutor.execute` continues to consume `ToolExecutionPolicyResult` as before.

## Files changed

- `seed_runtime/tool_execution_policy.py`
  - Added `RegisteredOperationValidationResult`.
  - Split the internal `_evaluate` body into validation and authorization responsibilities.
  - Preserved the existing `ToolExecutionPolicyResult` compatibility shape.
- `tests/test_tool_execution_policy.py`
  - Added tests proving registered-operation validation stops before policy authorization.
  - Added tests proving policy authorization consumes a validated operation and still produces the same allow result.
  - Refreshed generated architecture graph output so `tests/test_architecture_generator.py` remains stable after running the generator.

## LOC changed

From `git diff --stat` before commit:

```text
operational_responsibility_slice_005.md            | 137 +++++++++++++++++++++
seed_runtime/tool_execution_policy.py              | 111 +++++++++++++++--
tests/test_tool_execution_policy.py                |  37 ++++++
4 files changed, 288 insertions(+), 21 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_tool_execution_policy.py
pytest -q tests/test_tool_execution_policy.py tests/test_tool_validation.py tests/test_execution.py
pytest -q tests/test_architecture_generator.py
pytest -q
```

Results:

```text
11 passed
25 passed
2 passed
1554 passed
```

## Remaining compressed operational boundaries

Potential future slices, if implementation evidence confirms compression, should remain one boundary at a time:

- Pending-action creation vs. policy denial routing in `ToolExecutor._policy_denied`.
- Approved pending action resumption vs. fresh call authorization in `ToolExecutor.resume_approved_tool_call`.
- Policy outcome recording vs. pending-action lifecycle ownership.
- Output validation vs. result fact extraction after registered implementation realization.

These are observations for future investigation only; this slice changes exactly one boundary.

## Questions

### 1. Where were registered operation validation and policy authorization previously mixed?

They were mixed inside `ToolExecutionPolicyService._evaluate`, which performed existence, registration-status, and input-schema validation and then immediately projected state and evaluated policy in the same method body.

### 2. Which recovered architectural boundary became more explicit?

Registered Operation Validation != Policy Authorization.

### 3. How does the implementation now better reflect recovered architecture?

The implementation now has a validation result (`RegisteredOperationValidationResult`) that represents the validated selected registered operation before authorization, and a separate authorization method (`_authorize_validated_operation`) that evaluates policy only after validation succeeds.

### 4. Did any compatibility boundary change?

No.

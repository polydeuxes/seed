# Runtime Decision Responsibility Reconciliation

## Scope

This report is observational. It identifies what the current implementation demonstrates about the relationship among `Decision`, `Runtime`, policy, registry, and execution. It does not propose a planner, orchestration layer, runtime redesign, or execution redesign.

## Commands executed

```text
python - <<'PY'
from seed_runtime.context import DecisionInputComposer
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionProducer, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService
...
PY
```

Observed runtime routes:

```text
answer => answer ['input.user_message', 'model.decision.proposed', 'response.answer']
ask_question => question ['input.user_message', 'model.decision.proposed', 'response.question']
request_tool => tool_need ['input.user_message', 'model.decision.proposed', 'tool_need.created']
call_tool => invalid_decision ['input.user_message', 'model.decision.proposed', 'model.decision.intent_rejected']
refuse => refusal ['input.user_message', 'model.decision.proposed', 'response.refusal']
invalid_call_tool => invalid_decision {'errors': ['$.message must be a string']} ['input.user_message', 'model.decision.proposed', 'model.decision.invalid']
```

The `call_tool` observation used input text that did not satisfy the deterministic echo intent guard. Existing tests cover the successful echo path when the user input is exactly `echo <message>`.

```text
pytest -q tests/test_runtime_loop.py tests/test_execution.py tests/test_policy.py tests/test_execution_proposals.py
```

Result:

```text
35 passed in 0.79s
```

## Files inspected

Required files inspected:

- `seed_runtime/runtime.py`
- `seed_runtime/execution.py`
- `seed_runtime/policy.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/registry.py`

Directly supporting files inspected:

- `seed_runtime/models.py`
- `seed_runtime/decisions.py`
- `seed_runtime/tool_intent.py`
- `tests/test_runtime_loop.py`
- `tests/test_execution.py`
- `tests/test_policy.py`
- `tests/test_execution_proposals.py`

## Files changed

- `docs/runtime_decision_reconciliation.md`

## LOC changed

- Added 196 lines.

## Reconciliation

### Decision responsibility

`Decision` is a structured, model-produced command/result envelope. It carries one already-selected kind plus the fields required by that kind: answer text, a question, a tool name and arguments, a tool need, a state patch, or a refusal reason.

The current `Decision` model does not choose inquiry strategy. Its type permits a fixed set of kinds: `answer`, `ask_question`, `call_tool`, `request_tool`, `propose_action_plan`, `propose_handoff_plan`, `propose_state_patch`, and `refuse`. The model fields are payload fields for one of those selected kinds.


The strongest implementation-backed conclusion is that `Decision` means "what has already been selected for the runtime to route," not "a reasoning process that determines what evidence is needed next."

### Runtime responsibility

`Runtime` owns the session loop boundary around a user message. It records the input, projects state, composes context, asks the decision model for a `Decision`, records the proposed decision, validates it, applies deterministic tool-intent checks, retries parse/validation/intent failures within its configured retry budget, and routes valid decisions to the owning service.

Runtime is separate from the other responsibilities:

- It does not define the decision schema; `Decision` does.
- It does not execute registered tools; `ToolExecutor` does.
- It does not decide policy outcomes; `PolicyGate` and `ToolExecutionPolicyService` do.
- It does not own tool registration; `ToolRegistry` does.

Runtime therefore coordinates already-existing responsibilities. It contains routing logic, retry prompting, event recording around the model decision, and service delegation. The runtime loop demonstrates coordination rather than reasoning.

### Execution responsibility

`ToolExecutor` remains an execution responsibility. It evaluates execution policy, records failure/policy/execution events, loads registered implementations, calls the operation, validates output, observes tool-result facts, and handles approved pending-action resumption.

It does not decide inquiry strategy. It receives a tool name and arguments that have already reached the execution boundary. Before executing, it uses `ToolExecutionPolicyService` to resolve the tool, validate status and input, and evaluate policy. If allowed, it starts the call, invokes the registered callable, validates output, records completion, and observes tool-result evidence.

### Policy responsibility

`PolicyGate` maps a registered tool's policy action, risk class, scope, and existing approvals into an auditable `PolicyDecision`. It owns allow/block/confirmation/approval outcomes. It does not route runtime decisions and does not execute tools.

`ToolExecutionPolicyService` owns the combined execution preflight: tool existence, tool status, input schema validation, and policy evaluation. Its docstring explicitly states that it does not execute tools, append events, create pending actions, or collapse non-allow outcomes; callers route the result.

### Registry responsibility

`ToolRegistry` is the registered operation catalog. It loads manifests, registers toolkits, resolves tools by name, lists model-visible tools, lists tools by capability, and raises for unknown tools. It owns discoverability and registered operation identity, not reasoning or execution.

### Reasoning boundary

The implementation boundary for reasoning is outside these components. Runtime asks a `DecisionProducer` protocol to `decide(decision_input)`. The repository then treats the returned object as a proposed decision to validate and route. The reviewed implementation does not contain an internal responsibility that determines what additional evidence is required as an inquiry strategy.

### Decision boundary

The decision boundary is the structured `Decision` object plus validation. Once the model has emitted a `Decision`, Runtime records `model.decision.proposed`, validates the object, applies deterministic intent rules for tool calls, and routes by `decision.kind`. That boundary represents an already-proposed decision entering deterministic runtime handling.

### Execution boundary

The execution boundary begins when a valid `call_tool` decision reaches `ToolExecutor.execute`. Execution preflight resolves and validates the registered operation and evaluates policy. Actual execution starts only after an allow outcome, at which point `tool.call.started` is recorded and the registered implementation is invoked.

## Answers to required questions

### 1. What bounded responsibility does the current Decision model actually own?


### 2. What bounded responsibility does Runtime own?

Runtime owns the deterministic user-message loop and routing boundary: input event recording, state projection, context composition, model invocation, decision event recording, validation retry handling, intent-guard enforcement, and dispatch to owner services.

It does not own Decision, Execution, Policy, or Registry behavior. It coordinates them.

### 3. What bounded responsibility does ToolExecutor own?

`ToolExecutor` owns registered tool execution after validation and policy checks. It remains purely execution-side: preflight through `ToolExecutionPolicyService`, policy-denied handling, pending-action creation for non-allow policy outcomes, registered implementation loading, function invocation, output validation, result event recording, and fact extraction from completed tool results.

### 4. Does the current Decision model express what should happen or what has already been decided?

It expresses what has already been proposed/decided by the model for Runtime to validate and route. The event name is `model.decision.proposed`, and Runtime branches on the already-present `decision.kind`. The model does not encode an inquiry-selection process; it encodes a selected outcome.

### 5. Can the existing Decision model naturally represent additional observation required without introducing planning?

Partially, but only in an operationally coarse way. `ask_question` can represent that more user input is required, and `request_tool` can record that a missing capability/tool is needed. The model does not naturally represent "additional observation required" as a first-class evidence requirement, inquiry gap, or observation request. Representing that more precisely would require using `request_tool` as an indirect capability need or adding another responsibility/surface, which is outside this observational report.

### 6. Does Runtime perform reasoning, or does it merely coordinate existing responsibilities?

Runtime coordinates. It does not choose inquiry strategy. It composes context, asks the model to decide, validates and retries invalid outputs, and routes valid decisions. Its retry prompts ask for corrected JSON decisions after parse, validation, or intent failures; they do not perform inquiry reasoning.

### 7. Does current implementation reveal a missing responsibility between reasoning and execution, or does one existing component already own that transition?

The current implementation reveals that no reviewed component owns the full `reasoning -> decision -> execution` transition as an inquiry responsibility.

Existing components own narrower transitions:

- External/model reasoning to structured proposal: `DecisionProducer.decide(decision_input)` boundary.
- Valid tool call to execution/preflight: `ToolExecutor` plus `ToolExecutionPolicyService` and `PolicyGate`.

Those are not the same as a responsibility that determines what additional evidence bounded inquiry requires before execution. The repository currently relies on model/CLI selection, runtime validation/routing, tool intent guardrails, policy checks, and registered execution.

Strongest contradictory evidence: `Runtime` has an architecture summary that says it routes validated model decisions to owner services; it includes `request_tool` and `call_tool` paths, and its retry prompts can ask the model for corrected decisions. That is a real transition from a model decision to execution. However, it is a routing and validation transition, not an implementation-backed responsibility for inquiry strategy selection.

### 8. If Runtime, Decision, Policy, Registry, and Execution were removed independently, what observable responsibility would disappear for each?

- Removing `Decision` would remove the structured vocabulary that lets model output become a typed runtime route (`answer`, `ask_question`, `request_tool`, `call_tool`, `propose_state_patch`, `refuse`, and legacy side-path kinds).
- Removing `Runtime` would remove the user-message loop that records inputs, composes context, invokes the model, records proposed decisions, retries invalid decisions, and routes valid decisions to owner services.
- Removing `Policy` would remove deterministic allow/block/confirmation/approval decisions based on action risk and approval state.
- Removing `Registry` would remove registered tool identity, manifest loading, visible-tool listing, capability-to-tool lookup, and unknown-tool rejection.
- Removing `Execution` would remove registered callable invocation, execution event recording, output validation, policy-denied execution responses, pending-action creation from execution policy outcomes, approved-call resumption, and tool-result fact observation.

## Strongest supporting evidence

- `Runtime.__seed_arch__` explicitly identifies the owner as `runtime_orchestration` and summarizes Runtime as routing validated model decisions to owner services.
- `Runtime._route` branches on the already-present `decision.kind` and delegates `request_tool` to `ToolNeedService`, `call_tool` to `ToolExecutor`, and state patches to `StatePatchService`.
- `ToolExecutor.__seed_arch__` identifies the owner as `registered_tool_execution` and the layer as `execution`.
- `ToolExecutionPolicyService` explicitly states it does not execute tools, append events, create pending actions, or collapse non-allow policy outcomes.
- Tests assert routing behavior, validation retries, parse retries, policy outcomes, blocked execution, schema failure before execution, successful execution, and that execution proposals do not start tool calls.

## Strongest contradictory evidence

The strongest contradictory evidence is that Runtime already contains a deterministic bridge from model decision to owner service. It records `model.decision.proposed`, validates the decision, applies a deterministic tool-intent guard, retries invalid decisions, and then dispatches to tool need creation or tool execution. This is a real `decision -> execution` bridge for `call_tool`.

However, the bridge begins after a model has already emitted a concrete `Decision`. It does not determine what evidence bounded inquiry requires, and it does not choose whether observation or execution is the right next inquiry step except by routing the already-selected `decision.kind`.

## Recommended bounded implementation slice

No implementation slice is recommended by this observational investigation. The bounded output of this task is this repository-saved reconciliation report.

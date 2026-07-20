# Seed-owned tool execution corridor excision 001

## Constitutional checksum

Controlling authority for this pass:

```text
Seed has four things:

Observations <> Views

Operator ingress shell <> Seed egress shell

Capabilities are derived from evidence.

Everything is external grammar
which must be translated into constitutional grammar.
```

Seed does not have tools, does not own external mechanism execution, and must not preserve the former tool/runtime path as compatibility, experiment, historical projection support, or future architecture.

## Executable road recovered

Repository evidence before editing exposed this first-causal executable road:

1. A caller supplied `tool_name` and `arguments` to `ToolExecutor.execute(...)`.
2. `ToolExecutionPolicyService.evaluate_with_state_factory(...)` resolved a registered tool through `ToolValidationService` and `ToolRegistry`.
3. Validation checked existence, registered status, and input schema.
4. `PolicyGate` evaluated the registered tool's `policy_action` and projected approvals.
5. Non-allow policy produced `tool.policy.blocked` or `tool.approval.required`; approval/confirmation paths created pending tool-call actions.
6. Allow policy entered `_execute_allowed_tool_call(...)`.
7. The executor appended `tool.call.started`.
8. `_realize_registered_operation(...)` imported and invoked the registered implementation callable with a `ToolContext`.
9. Output schema validation ran against the returned value.
10. Success appended `tool.call.completed`; failure appended `tool.call.failed`.
11. Completed events were passed to `FactExtractionService.observe_tool_result(...)`.
12. `FactExtractionService` recorded returned output as `evidence.observed` with `kind=tool.output` and `source=tool:<name>`.
13. `ToolExecutor.resume_approved_tool_call(...)` projected a pending action, required approved state, reloaded the registered tool, invoked the same allowed-call path, then marked the pending action completed.

## Complete dependency closure deleted

Deleted the executable corridor and its solely supporting artifacts:

- Executor: `seed_runtime/execution.py`.
- Validation: `seed_runtime/tool_validation.py`.
- Tool execution policy sequencing: `seed_runtime/tool_execution_policy.py`.
- Tool-call pending action service: `seed_runtime/pending_actions.py`.
- Post-tool-result evidence extraction: `seed_runtime/fact_extraction.py`.
- Registered toolkit/operation registry: `seed_runtime/registry.py`.
- Generated/bundled toolkit implementations and manifests: `toolkits/`.
- Toolkit builder/validator package: `seed_builder/`.
- Executor, registry, validation, policy, pending-action, toolkit, and fact-extraction tests and fixtures that existed to prove the deleted road.

## Files and symbols removed

Removed symbols included:

- `ToolExecutor`, `ToolCallResult`, `ToolContext`, and `ToolCallStatus`.
- `ToolValidationService`, `ToolValidationResult`, and operation-selection helpers.
- `ToolExecutionPolicyService`, `ToolExecutionPolicyResult`, and registered-operation validation result helpers.
- `PendingActionService` for pending tool calls.
- `FactExtractionService`, `FactExtractionResult`, `FactExtractionError`, and `ToolResultFactExtractor`.
- `ToolRegistry`, toolkit manifest loading, and registered-operation index helpers.
- Generated/core toolkit operation modules and manifests.

Residual model vocabulary such as `ToolNeed`, `ToolSpec`, and `Toolkit` was not broadly removed in this bounded pass unless it was part of the executable road. Adjacent capability-gap and provider-recommendation families remain bounded follow-up territory.

## Events removed from active production/projection paths

Removed active append/projection support for the Seed-owned execution lifecycle:

- `tool.call.started`
- `tool.call.completed`
- `tool.call.failed`
- `tool.policy.blocked`
- `tool.approval.required`
- `pending_action.created`
- `pending_action.approved`
- `pending_action.completed`
- `pending_action.cancelled`
- `pending_action.status_changed`
- `tool.registered`

`StateProjector` no longer replays tool-registration or pending tool-call lifecycle events into state, and the local CLI no longer seeds dev-only registered providers. Empty compatibility fields remain on `State`/snapshot payloads for adjacent read-model stability, but no active event producer or replay branch populates them from the deleted corridor.

## CLI/API surfaces removed

Removed or corrected active surfaces that exposed the deleted corridor:

- Removed `SeedAPI` registry dependency and `get_toolkits()` / `get_tools()` surfaces.
- Removed `scripts/seed_local.py --registered-provider` parsing, seeding, help text, and event-summary support.
- Removed generated architecture nodes/edges for `ToolExecutor`, `ToolRegistry`, and `RegisteredOperation`.
- Corrected the active architecture overview so it no longer states that runtime owns tool execution or pending-action services.

## Projection and extraction dependencies removed

- Removed state replay of pending tool-call actions.
- Removed state replay of registered tools.
- Removed active projection dependencies that populated pending tool-call state and registered tools from execution-corridor events; empty state/snapshot fields remain only for adjacent read-model stability.
- Removed post-tool-result extraction entirely; no surviving active code accepts `tool.call.completed` or `tool.result` as Seed-owned execution evidence.

## Tests and fixtures removed

Removed tests whose production road was deleted, including executor, execution-policy, validation, registry, pending-action resume, toolkit, API registry listing, and post-tool-result extraction tests.

Additional tests that imported deleted executor/registry modules only to assert non-use were removed because their independent instantiation of deleted nouns would preserve historical breadcrumbs after the production road was removed.

## Active documentation corrected

- Regenerated `docs/generated/architecture/architecture_graph.json`, `docs/generated/architecture/runtime_ownership.mmd`, and `docs/generated/architecture/runtime_ownership.dot` without the deleted executor/registry nodes.
- Corrected `docs/architecture.md` present-tense runtime ownership text.

Older audit/investigation reports still contain historical statements about the former tool corridor. Those are not active architecture surfaces and were not bulk-rewritten in this bounded deletion pass.

## Legitimate observation machinery preserved

Preserved observation collection, normalization, ingestion, evidence/fact projection, and diagnostic/reporting machinery that invokes operating-system or network mechanisms as observation-source implementation rather than as Seed-owned tool execution. Examples preserved include repository observation, local host observations, Prometheus observation sources, JSON observation ingestion, and read-only diagnostic/status surfaces.

## Adjacent contaminated families remaining

Intentionally left for later bounded passes unless mechanically required here:

- `ToolNeed` / capability-gap vocabulary.
- `ToolSpec` / `Toolkit` model vocabulary retained for adjacent capability/projection compatibility.
- Capability catalog/provider recommendation/handoff/action-plan/execution-proposal families.
- Legacy approvals and execution-authorization metadata.
- Historical audit documents describing the former path.

These do not provide a surviving active path that selects, authorizes, invokes, resumes, or records a Seed-owned tool result after this pass.

## Verification results

Commands run:

```bash
rg -n "seed_runtime\\.(execution|tool_validation|tool_execution_policy|pending_actions|fact_extraction|registry)|from seed_runtime\\.(execution|tool_validation|tool_execution_policy|pending_actions|fact_extraction|registry)|ToolExecutor|ToolCallResult|ToolContext|ToolValidationService|ToolExecutionPolicyService|ToolRegistry|FactExtractionService|ToolResultFactExtractor|tool\\.call\\.(started|completed|failed)|tool\\.policy\\.blocked|tool\\.approval\\.required|pending_action\\.(created|approved|completed|cancelled|status_changed)|tool\\.registered" seed_runtime scripts tests docs/generated scripts/generate_architecture.py
python -m compileall -q seed_runtime scripts
python scripts/seed_local.py --help
printf 'hello\nexit\n' | python scripts/seed_local.py
pytest -q
```

The targeted active-code/test/generated search finds only `execution_status` / `execution_proposals` false positives from the substring `execution`, plus the present report when included in the search scope; it finds no surviving active implementation, test, script, export, or generated-architecture occurrences of the deleted tool corridor symbols or lifecycle event kinds.

## Bounded answer

Can any surviving active Seed-owned path select, authorize, invoke, resume, or record the result of an external mechanism as a tool?

No. The executor, registry, validation/policy sequencer, pending-action resume service, tool-result extraction service, active lifecycle event replay, CLI/API registry surfaces, toolkit implementations, and tests/fixtures for that road have been removed. Active search and verification commands above support that answer.

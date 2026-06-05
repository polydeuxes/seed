# RuntimeLoop Thin Runtime Plan

This plan keeps `RuntimeLoop` as a thin orchestration boundary and prevents it from
becoming a second `Runtime` or `ToolExecutor`. It is cleanup-only: no feature
changes, no event changes, no `RuntimeResult` changes, no decision kind changes,
and no caller migration.

## RuntimeLoop responsibility

`RuntimeLoop` should own only the deterministic sequencing needed for one run:

1. Append the input event.
2. Load and project state.
3. Compose provider context.
4. Ask the `DecisionProvider` for a decision.
5. Call shared decision routing/services.
6. Journal the result.
7. Return `RuntimeResult`.

Everything else should have an explicit service owner so business rules remain
shared, testable, and independently replaceable.

## RuntimeLoop-owned logic to move behind service boundaries

The current `RuntimeLoop` still contains business logic that should be owned by
services over time:

- `_validate_decision`: RuntimeLoop-specific validation rules for provider
  decisions. This PR extracts it to `RuntimeLoopDecisionValidator`.
- `_build_tool_need`: request-tool payload normalization and `ToolNeed` creation.
- `_run_tool_decision`: tool-call dispatch behavior, policy result handling,
  handler execution, output validation, evidence extraction, and result shaping.
- `_run_request_tool_decision`: request-tool event creation, recommendation lookup,
  journaling, and result shaping.
- `_compose_context`: provider context/tool projection composition.

## This PR: extract one low-risk service

Only decision validation moves in this PR.

New owner:

- `seed_runtime/runtime_loop_decisions.py`
- `RuntimeLoopDecisionValidator.validate_decision(...)`

`RuntimeLoop` delegates validation to the service and preserves the existing
malformed-decision path exactly. The validator keeps the same accepted decision
kinds and the same validation error messages.

## Non-goals

This cleanup intentionally does not:

- Remove `Runtime` or `RuntimeLoop`.
- Migrate CLI/API callers.
- Touch `ToolExecutor`.
- Touch `ContextComposer`.
- Add approval/resume behavior.
- Add `state_patch` behavior.
- Add retry-loop behavior.
- Change events, journaling payloads, `RuntimeResult`, or decision kinds.

## Follow-up extraction order

Future cleanup PRs can move one service at a time, preserving behavior at each
step:

1. Request-tool construction service for `_build_tool_need`.
2. RuntimeLoop request-tool routing service for `_run_request_tool_decision`.
3. RuntimeLoop tool-call routing/execution adapter for `_run_tool_decision`.
4. RuntimeLoop context service for `_compose_context`.

Each follow-up should include parity tests before and after extraction and should
avoid changing CLI/API or old `Runtime` behavior.

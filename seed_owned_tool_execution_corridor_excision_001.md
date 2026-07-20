# Seed-owned tool execution corridor excision 001

## Operator-supplied audit orientation

The following orientation was supplied to help locate artifacts that might belong
to the abandoned Seed-owned tool road. It was used as a search lens, not as
independent constitutional warrant:

```text
Observations <> Views

Operator ingress shell <> Seed egress shell

Capabilities are derived from evidence.
```

Deletion decisions in this pass were based upon repository evidence showing that
the removed corridor selected, authorized, invoked, resumed, and recorded
external mechanisms as Seed-owned tools. The orientation above is therefore not a
controlling authority, not a constitutional checksum, and not proof that every
artifact outside a short vocabulary list must be deleted.

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

Deleted the executable corridor and its solely supporting production artifacts:

- Executor: `seed_runtime/execution.py`.
- Validation: `seed_runtime/tool_validation.py`.
- Tool execution policy sequencing: `seed_runtime/tool_execution_policy.py`.
- Tool-call pending action service: `seed_runtime/pending_actions.py`.
- Post-tool-result evidence extraction: `seed_runtime/fact_extraction.py`.
- Registered toolkit/operation registry: `seed_runtime/registry.py`.
- Generated/bundled toolkit implementations and manifests: `toolkits/`.
- Toolkit builder/validator package: `seed_builder/`.

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

## Test restoration correction

The correction rule is responsibility-based, not filename-, import-, or substring-based:

- Tests solely dependent upon the deleted responsibility were removed.
- Tests proving independent responsibilities were preserved or rewritten without contaminated fixtures.

A test file is not wholly dependent on the deleted executable corridor merely because one fixture, negative guard, compatibility import, or example mentioned a deleted noun. This correction restored independent witness for claims, repository observations, facts, evidence, contradictions, confidence, operator ingress, read-only views, evidence-derived capability, candidate/frontier views, and CLI/API boundaries.

### Deleted test-file classification

A = solely proves the deleted executable tool corridor; B = mixed deleted-road and independent coverage; C = wholly independent of the deleted corridor.

- A, intentionally left deleted: `tests/test_action_resume.py`, `tests/test_architecture_invariants.py`, `tests/test_builder_generator.py`, `tests/test_environment_inventory_toolkit.py`, `tests/test_execution.py`, `tests/test_execution_proposals.py`, `tests/test_fact_extraction.py`, `tests/test_host_notes_toolkit.py`, `tests/test_pending_actions.py`, `tests/test_preconditions.py`, `tests/test_registry.py`, `tests/test_ssh_access_toolkit.py`, `tests/test_tool_execution_policy.py`, `tests/test_tool_recommendations.py`, `tests/test_tool_validation.py`, `tests/test_toolkit_registration.py`, `tests/test_toolkit_validator.py`.
- B, restored and surgically repaired: `tests/test_api.py`, `tests/test_candidate_examination_work.py`, `tests/test_candidate_requests.py`, `tests/test_capability_candidates.py`, `tests/test_capability_inventory.py`, `tests/test_capability_promotion_readiness.py`, `tests/test_capability_verification_inspection.py`, `tests/test_capability_verification_invariants.py`, `tests/test_confidence.py`, `tests/test_contradictions.py`, `tests/test_examination_frontier.py`, `tests/test_integrity_summary.py`, `tests/test_seed_local_script.py`, `tests/test_self_model_acquisition_pipeline.py`, `tests/test_single_capability_state_projection.py`, `tests/test_verification_evidence.py`.
- C, restored unchanged except for mechanical expectation/import updates needed by the surviving implementation: `tests/test_architecture_generator.py`, `tests/test_consumer_dependency_audit.py`, `tests/test_documentation_observation.py`, `tests/test_emitter_attribution_audit.py`, `tests/test_emitter_consumer_audit.py`, `tests/test_existence_claim_reconciliation.py`, `tests/test_input_inspector.py`, `tests/test_observation_inventory.py`, `tests/test_observation_utilization.py`, `tests/test_relationship_observation.py`, `tests/test_recommendation_ranker.py`, `tests/test_self_model_alignment.py`, `tests/test_structure_claim_reconciliation.py`, `tests/test_structure_observation.py`.
### Test-count honesty

PR 1881 reported `2146 passed` and `15 failed`; PR 1882 reported `1642 passed`. A smaller green suite was not treated as sufficient evidence. Repository evidence in this correction accounts for 30 restored test files (16 mixed B files plus 14 independent C files) and 17 intentionally deleted A files. The restored set includes `tests/test_capability_verification_invariants.py`, which now protects surviving capability-verification distinctions without enforcing present-tense claims about the deleted corridor. Contaminated tests/fixtures were rewritten instead of reviving production tool machinery.

Final collected test count for this follow-up: 2067. Final pass/fail result: 2067 passed, 0 failed.

## Active documentation corrected

- Regenerated `docs/generated/architecture/architecture_graph.json`, `docs/generated/architecture/runtime_ownership.mmd`, and `docs/generated/architecture/runtime_ownership.dot` without the deleted executor/registry nodes.
- Corrected `docs/architecture.md` present-tense runtime ownership text.
- Corrected `docs/invariants.md`, `docs/capability_verification_vocabulary.md`, and `tests/test_capability_verification_invariants.py` so active invariants, capability-verification vocabulary, and documentation tests no longer warrant runtime tool routing, executor/policy/pending-action services, registry/spec exposure, or registered-operation execution as current Seed architecture.

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
python -m compileall -q seed_runtime scripts
python scripts/seed_local.py --help
printf 'hello\nexit\n' | python scripts/seed_local.py
pytest --collect-only -q
pytest -q
rg -n "seed_runtime\.(execution|tool_validation|tool_execution_policy|pending_actions|fact_extraction|registry)|from seed_runtime\.(execution|tool_validation|tool_execution_policy|pending_actions|fact_extraction|registry)|ToolExecutor|ToolCallResult|ToolContext|ToolValidationService|ToolExecutionPolicyService|ToolRegistry|FactExtractionService|ToolResultFactExtractor|tool\.call\.(started|completed|failed)|tool\.policy\.blocked|tool\.approval\.required|pending_action\.(created|approved|completed|cancelled|status_changed)|tool\.registered" seed_runtime scripts tests docs/generated scripts/generate_architecture.py
```

Final verification collected 2067 tests and `pytest -q` reported 2067 passed. The targeted active-code/test/generated search is interpreted with the bounded correction rule: benign historical report text and neutral fixture strings are not executable contamination. Active implementation, CLI/API, test, and generated architecture paths contain no surviving Seed-owned executable-tool corridor.

## Bounded answers

Do any active invariants, capability-verification documents, or tests still warrant the deleted Seed-owned tool execution corridor as current architecture?

No. This final correction removed test-enforced active documentation claims about the deleted tool corridor from `docs/invariants.md`, `docs/capability_verification_vocabulary.md`, and `tests/test_capability_verification_invariants.py`. Historical audit reports may still mention deleted artifacts as historical subjects. The executor, registry, validation/policy sequencer, pending-action resume service, tool-result extraction service, active lifecycle event replay, CLI/API registry surfaces, and toolkit implementations remain deleted.

Are the independently restored tests for claims, observations, facts, evidence, ingress, capability standing, and views still present and passing?

Yes. Restored and repaired tests cover claims and repository observations; facts, evidence, contradictions, and confidence; operator ingress; read-only views; evidence-derived capability; and candidate/frontier presentation without restoring production tool machinery.

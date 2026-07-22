# Pure foreign planning/control shell excision 001

## Governing conclusion

PR 1917 left a connected compatibility skeleton around deleted conversational-agent and execution architecture. This operation deletes the pure foreign planning/control shell rather than preserving compatibility artifacts whose only warrant was agent planning, readiness, handoff, policy routing, pending tool-call workflow, or builder-candidate workflow.

Useful distinctions remain in repository testimony. Implementation absence is the intended result.

## Pre-excision dependency topology

The removed topology was:

```text
ToolNeed / recommendation inputs -> ActionPlanService -> ActionPlan
ActionPlan -> lifecycle events -> readiness / precondition reports -> HandoffPlanService -> HandoffPlan
ToolSpec + Approval -> PolicyGate -> PolicyDecision
historical tool-call road -> PendingAction
historical builder road -> ToolkitCandidate
```

## Models removed

Removed active model/schema artifacts:

- `ActionPlanStatus`
- `PendingActionStatus`
- `PolicyOutcome`
- `ActionPlan`
- `HandoffPlan`
- `PolicyDecision`
- `PendingAction`
- `ToolkitCandidate`
- handoff-only approval-claim validation helpers

## Services and files removed

Removed implementation modules:

- `seed_runtime/action_plans.py`
- `seed_runtime/preconditions.py`
- `seed_runtime/handoff_plans.py`
- `seed_runtime/policy.py`

No replacement planning, policy, readiness, handoff, pending-action, or builder architecture was introduced.

## Events removed

Removed active event production, replay, and active validation/projection support for:

- `action_plan.created`
- `action_plan.accepted`
- `action_plan.approved`
- `action_plan.rejected`
- `action_plan.superseded`
- `handoff_plan.created`

## State fields removed

Removed State fields:

- `action_plans`
- `action_plan_approvals`
- `handoff_plans`
- `pending_actions`

## Projection and snapshot support removed

Projection replay branches, affected-scope handling, projection-shape production entries, and snapshot serialization/deserialization for the removed State fields were deleted.

## CLI surfaces removed

Removed parser, validation, dispatch, formatter, and help/example surfaces for:

- `--accept-plan`
- `--approve-plan`
- `--reject-plan`
- `--supersede-plan`
- `--preconditions`
- `--handoff`

## Tests removed or updated

Deleted dedicated tests for action plans, handoff plans, policy routing, and public quarantined exports. Shared tests were updated to stop expecting removed State fields, event graph nodes, emitter attribution rows, and CLI parser behavior.

## Active documentation corrected

Active implementation documentation was not rewritten into a replacement architecture. Surviving references in `docs/` are audit/reconciliation records that describe now-removed historical or quarantined surfaces and should be read as testimony, not active command instructions.

## Historical testimony preserved

The requested historical reports remain preserved:

- `book_of_seed/agentic_planning_tool_prototype_contamination_recovery_001.md`
- `book_of_seed/execution_proposal_authorization_island_excision_001.md`
- `book_of_seed/seed_egress_external_realization_grammar_recovery_001.md`
- `book_of_seed/remaining_agent_runtime_schema_deletion_topology_001.md`

Other Book testimony mentioning removed terms remains historical/audit testimony.

## Mixed families intentionally left unresolved

The following mixed families remain intentionally unresolved and were not redesigned:

- `Actor`
- `ToolNeed`, `ToolNeedStatus`, `ToolNeedService`
- `ToolSpec`, `Toolkit`
- `Approval`, `RiskClass`
- `CapabilityRecommendation`, `CapabilityCatalog`
- recommendation ranking and service surfaces
- `model_visible`
- `backend_type`, `operation`, provider metadata

## HandoffBackendType/catalog boundary treatment

`HandoffBackendType` remains because `CapabilityRecommendation.backend_type` and capability catalog metadata still consume it. It is recorded as unresolved mixed residue and was not renamed or reinterpreted.

## Approval/RiskClass boundary treatment

`Approval` and `RiskClass` remain where used by approval state, registered operation testimony, ToolSpec risk metadata, and capability/recommendation surfaces. The deleted policy-routing shell no longer turns those fields into `PolicyDecision` outcomes.

## ToolSpec/ToolNeed boundary treatment

`ToolNeed`, `ToolSpec`, `Toolkit`, capability observations, capability inventory, and recommendation/catalog testimony remain as mixed boundaries for later recovery. Direct plan/handoff/readiness consumers were removed.

## Verification

Verification commands used for this operation include repository searches for deleted symbol/event/CLI families, compile checks, CLI help, focused tests, full tests, and diff checks. Surviving matches are classified as historical testimony, audit/reconciliation records, fixture text for diagnostic tests, or unresolved mixed capability residue; no active implementation producer, model, service, State field, or CLI dispatch path remains for the deleted shell.

## Remaining foreign residue

Remaining exposed residue includes mixed capability acquisition vocabulary, `ToolNeed` lifecycle vocabulary, provider/backend metadata, policy action labels on `ToolSpec`, `Approval`, `RiskClass`, and audit/documentation testimony about deleted paths.

## Lawful stopping point

This operation stops at deletion of the pure foreign planning/control shell. It does not perform capability-catalog recovery, ToolNeed recovery, approval/risk recovery, Actor recovery, registered-operation recovery, or any replacement workflow/control design.

## Final direct answers

1. Was `ActionPlan` deleted? Yes.
2. Was `ActionPlanService` deleted? Yes.
3. Was `seed_runtime/action_plans.py` deleted? Yes.
4. Were all `action_plan.*` active event paths deleted? Yes.
5. Were `State.action_plans` and `State.action_plan_approvals` deleted? Yes.
6. Were all ActionPlan lifecycle CLI surfaces deleted? Yes.
7. Was `seed_runtime/preconditions.py` deleted? Yes.
8. Were `Precondition`, `PreconditionReport`, and `PreconditionEvaluator` deleted? Yes.
9. Was all `executable` / `plan_ready` readiness grammar owned by that module deleted? Yes.
10. Was `HandoffPlan` deleted? Yes.
11. Was `HandoffPlanService` deleted? Yes.
12. Was `seed_runtime/handoff_plans.py` deleted? Yes.
13. Was `handoff_plan.created` active support deleted? Yes.
14. Was `State.handoff_plans` deleted? Yes.
15. Was `--handoff` deleted? Yes.
16. Was `PolicyDecision` deleted? Yes.
17. Was `PolicyOutcome` deleted? Yes.
18. Was `PolicyGate` deleted? Yes.
19. Was `seed_runtime/policy.py` deleted? Yes.
20. Was `PendingAction` deleted? Yes.
21. Was `State.pending_actions` deleted? Yes.
22. Was `ToolkitCandidate` deleted? Yes.
23. Was active `seed-builder-v1` builder schema deleted? Yes.
24. Which mixed families remain intentionally unresolved? Actor, ToolNeed/ToolNeedStatus/ToolNeedService, ToolSpec/Toolkit, Approval/RiskClass, CapabilityRecommendation/CapabilityCatalog, recommendation/ranking services, model-visible/backend/operation/provider metadata.
25. Did `HandoffBackendType` remain because of capability-catalog use, or become dead and get removed? It remains because capability-catalog metadata consumes it.
26. Which `Approval` and `RiskClass` surfaces remain? Approval model/state/approval ledger projection and RiskClass use in ToolSpec and capability/recommendation metadata remain.
27. Which `ToolNeed`, `ToolSpec`, and recommendation surfaces remain? ToolNeed model/state/service, ToolSpec/Toolkit registered-operation metadata, capability catalog, capability recommendation, and ranker/service surfaces remain.
28. Which historical reports remain? The four required reports remain, along with existing Book testimony and audit/reconciliation records.
29. Was any replacement planning, policy, readiness, handoff, pending-action, builder, workflow, or control architecture introduced? No.
30. Which remaining foreign residue is now exposed? Mixed capability acquisition and recommendation vocabulary, ToolNeed lifecycle vocabulary, provider/backend metadata, ToolSpec policy action labels, Approval/RiskClass surfaces, and historical audit documentation.
31. What is the smallest lawful next recovery? A separate mixed-boundary recovery of one exposed family, likely ToolNeed/capability acquisition or ToolSpec policy-action/risk metadata, backed by implementation evidence.
32. Where must this operation stop? It must stop before redesigning capability catalogs, approvals, risks, ToolNeed, ToolSpec, Actor, recommendations, registered operations, or any replacement control architecture.

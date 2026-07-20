# Planning/execution artifact quarantine audit

Current Core MVP path:

```text
Input/observations
-> facts/evidence
-> relationships/entity types
-> explanations/current state
-> ToolNeed
-> capability_resolution
-> registered operation candidates
-> provider/handoff recommendations
```

Canonical Runtime does not own internal workflow execution, execution authorization workflows, or action-plan orchestration. The artifacts below are retained only for historical projection compatibility and explicit experimental/legacy CLI side paths unless a future architecture decision promotes them again.

## Artifact inventory

| Artifact | Defined in | Main callers | Reachable from canonical `Runtime`? | Required for `ToolNeed` / `capability_resolution`? | Required for read-only state/query commands? | Required for `ToolExecutor` / pending actions? | Current classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ActionPlan` | `seed_runtime/models.py`; helper service in `seed_runtime/action_plans.py` | `scripts/seed_local.py --plan`, lifecycle CLI commands, tests, historical projection in `seed_runtime/state.py` | No. `DecisionValidator` rejects `propose_action_plan`, and `Runtime._route` has no action-plan branch. | No. `Runtime` records `ToolNeed` and resolves capabilities through `ToolNeedService`/`ToolRecommendationService`. | Only for reading/projecting historical `action_plan.*` events and legacy CLI inspection. | No. `ToolExecutor` executes explicit validated tool calls and pending-action policy remains separate. | Quarantined legacy/experimental. |
| `HandoffPlan` | `seed_runtime/models.py`; helper service in `seed_runtime/handoff_plans.py` | `scripts/seed_local.py --handoff`, tests, historical projection in `seed_runtime/state.py` | No. `DecisionValidator` rejects `propose_handoff_plan`, and `Runtime._route` has no handoff-plan branch. | No. Provider/handoff recommendations are emitted as recommendation metadata, not `HandoffPlan` orchestration. | Only for reading/projecting historical `handoff_plan.created` events and legacy CLI inspection. | No. Non-executable by model validation and service construction. | Quarantined legacy/experimental. |
| `ExecutionProposal` | `seed_runtime/execution_proposals.py`; projected as `state.execution_proposals` | `scripts/seed_local.py --proposal`, `--authorize-proposal`, tests, historical projection | No. Canonical `Runtime` never imports or routes it. | No. | Only for legacy CLI reports and historical `execution_proposal.created` projection. | No. Proposal creation is inspect-only and does not call `ToolExecutor`. | Quarantined legacy/experimental; delete candidate after compatibility review. |
| `ExecutionAuthorization` | `seed_runtime/models.py`; grant helper in `ActionPlanService.grant_execution_authorization` | `scripts/seed_local.py --authorize-proposal`, precondition tests/reports, historical projection | No. Canonical `Runtime` never imports or routes it. | No. | Only for legacy precondition/proposal inspection and historical projection. | No. It does not grant credentials or invoke execution. | Quarantined legacy/experimental; delete candidate after compatibility review. |
| Precondition proposal helpers | `seed_runtime/preconditions.py`, `ActionPlanService.precondition_report`, `ExecutionProposalService.diagnose_failure` | `scripts/seed_local.py --preconditions` / `--proposal`, tests | No. Canonical `Runtime` never invokes them. | No. | Useful only for legacy CLI inspection of stored ActionPlans. | No. Inspect-only. | Quarantined legacy/experimental; delete candidate with ActionPlan/ExecutionProposal side paths. |
| CLI `--plan` | `scripts/seed_local.py` | One-shot local CLI after a ToolNeed response | No. It wraps CLI output after Runtime response; it is not a Runtime decision route. | No. | No, except as an experimental local side-path to create legacy plan events. | No. | Retained but help marks experimental/legacy. |
| CLI `--handoff` | `scripts/seed_local.py` | Local CLI handoff generation for accepted legacy plans | No. It is a separate command path requiring `--db`. | No. | Only for legacy handoff inspection. | No. | Retained but help marks experimental/legacy. |

## Safely quarantined now

- Current-core docs now stop at `ToolNeed`, `capability_resolution`, registered operation candidates, and provider/handoff recommendations.
- CLI help labels `--plan`, `--preconditions`, `--proposal`, `--handoff`, and `--authorize-proposal` as experimental/legacy side paths.
- Canonical Runtime remains unwired: `propose_action_plan` and `propose_handoff_plan` are rejected during decision validation and never routed.
- Projection compatibility remains for historical `action_plan.*`, `handoff_plan.created`, `execution_proposal.created`, and `execution_authorization.granted` events.

## Later delete candidates

Delete only after a migration/compatibility decision confirms no stored ledgers or tests need these historical events:

1. `ExecutionProposalService` and `execution_proposal.created` projection.
2. `ExecutionAuthorization` and `execution_authorization.granted` projection.
3. Precondition helpers tied only to ActionPlan/ExecutionProposal inspection.
4. `ActionPlanService` lifecycle helpers and `action_plan.*` projection.
5. `HandoffPlanService` and `handoff_plan.created` projection.
6. Experimental/legacy CLI flags: `--plan`, `--preconditions`, `--proposal`, `--handoff`, `--authorize-proposal`.

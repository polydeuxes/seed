# Execution proposal / authorization island excision 001

## Governing conclusion

PR 1914 recovered an active provider-specific prototype island in which a stored `ActionPlan` could be converted into an `ExecutionProposal`, then linked to an `ExecutionAuthorization`, then projected as `authorized=True` and `executable=True`. The authorization record established only caller-supplied, secret-free metadata linked by identifiers, argument fingerprint, and expiry. It did not establish a verified granting subject, competent authority, credentials, target permission, provider availability, operation applicability, execution capability, or lawful execution permission. The implementation crossing therefore strengthened metadata into invented executable standing and was removed.

## Exact pre-excision topology

The pre-excision topology was:

```text
stored ActionPlan
  -> ExecutionProposalService.create_proposal(...)
  -> ExecutionProposal
  -> ActionPlanService.grant_execution_authorization(...)
  -> ExecutionAuthorization
  -> execution_authorization.granted projection
  -> State.execution_proposals[proposal].authorized = True
  -> State.execution_proposals[proposal].executable = True
```

Producer surfaces were `ExecutionProposalService`, `ActionPlanService.grant_execution_authorization(...)`, CLI `--proposal`, CLI `--authorize-proposal`, and the hidden compatibility alias `--authorize-execution`. Artifacts were `ExecutionProposal`, `ExecutionProposalFailure`, `ExecutionAuthorization`, `execution_proposal.created`, `execution_authorization.granted`, `State.execution_proposals`, `State.execution_authorizations`, and proposal fields including `arguments_fingerprint`, `authorized`, and `executable`. Consumers were `StateProjector`, projection snapshot serialization, precondition authorization checks, CLI formatters, and dedicated proposal/authorization tests.

## Producer / artifact / consumer recovery

Recovered producers:

- `seed_runtime/execution_proposals.py` produced proposal and proposal-failure models and optionally emitted `execution_proposal.created`.
- `ActionPlanService.grant_execution_authorization(...)` produced `ExecutionAuthorization` and emitted `execution_authorization.granted`.
- `scripts/seed_local.py --proposal` and `--authorize-proposal` exposed both producers as active CLI behavior.

Recovered artifacts:

- `ExecutionProposal`, `ExecutionProposalFailure`, `ExecutionAuthorization`.
- `execution_proposal.created`, `execution_authorization.granted`.
- `State.execution_proposals`, `State.execution_authorizations`.
- `arguments_fingerprint`, proposal `authorized`, and proposal `executable`.

Recovered consumers:

- `StateProjector` replayed proposal and authorization events.
- Projection snapshot serialization/deserialization included proposal and authorization collections.
- Precondition reporting checked current authorization against proposal fingerprint linkage.
- CLI proposal, authorization, proposal-failure, and precondition formatting rendered island-owned output.
- Dedicated tests preserved proposal creation, failure diagnosis, authorization creation, authorization expiry/fingerprint matching, projection mutation, and proposal/authorization CLI behavior.

## Why ExecutionAuthorization did not establish executable standing

`ExecutionAuthorization` recorded a grant label, proposal id, plan id, tool name, argument fingerprint, expiry, and secret-free metadata flags. Those fields could show that Seed stored a bounded metadata record, but they could not prove that the grantor was a verified subject, that the grantor had competent authority, that credentials existed, that the target permission was lawful, that the provider was available, that the operation was applicable, or that execution capability existed. Matching those metadata fields during projection was therefore insufficient warrant for `executable=True`.

## Exact active crossing removed

The removed crossing was the `StateProjector` branch for `execution_authorization.granted` that loaded `ExecutionAuthorization`, stored it in `State.execution_authorizations`, looked up a linked proposal in `State.execution_proposals`, compared proposal id, action-plan id, tool name, argument fingerprint, and expiry, then replaced the projected proposal with `authorized=True` and `executable=True`.

## Models removed

- Removed `ExecutionProposal`.
- Removed `ExecutionProposalFailure`.
- Removed `ExecutionAuthorization`.

## Services removed

- Removed `seed_runtime/execution_proposals.py` and `ExecutionProposalService`.
- Removed `ActionPlanService.grant_execution_authorization(...)`.

## Events removed

- Removed active production and validation for `execution_proposal.created`.
- Removed active production and validation for `execution_authorization.granted`.
- Removed projection handling for both event kinds.

## Projected-state fields removed

- Removed `State.execution_proposals`.
- Removed `State.execution_authorizations`.
- Removed projection snapshot payload serialization and deserialization for both collections.
- Removed projection-shape stage output entries for both collections.

## CLI surfaces removed

- Removed `--proposal`.
- Removed `--authorize-proposal`.
- Removed hidden `--authorize-execution` compatibility alias.
- Removed proposal failure formatting owned only by this island.
- Removed authorization grant formatting owned only by this island.
- Removed grant metadata and TTL parser options owned only by this island.

## Tests removed or updated

Deleted `tests/test_execution_proposals.py`, which was dedicated to proposal creation, failure diagnosis, authorization creation, expiry/fingerprint linkage, projection mutation, and proposal/authorization behavior. Removed proposal/authorization-specific CLI tests from `tests/test_seed_local_script.py`. Updated adjacent tests to assert structural absence of proposal/authorization state collections rather than preserving empty compatibility shells.

## Imports and exports removed

Removed imports of `ExecutionProposalService` and `ExecutionAuthorization` from runtime, CLI, event-ledger, state, and projection-store code. Removed direct references to proposal/authorization projected-state fields from projection-shape and projection-store code.

## ActionPlan responsibilities preserved

Preserved `ActionPlan`, `ActionPlanService.create_plan(...)`, `accept_plan(...)`, `approve_plan(...)`, `reject_plan(...)`, `supersede_plan(...)`, `precondition_report(...)`, action-plan lifecycle events, and action-plan projection. This operation did not validate `ActionPlan` itself.

## HandoffPlan responsibilities preserved

Preserved `HandoffPlan`, `HandoffPlanService`, `handoff_plan.created`, provider recommendation, and capability catalog behavior. Only direct dead proposal/authorization references adjacent to handoff tests were updated.

## Precondition responsibilities preserved

Preserved independent action-plan precondition evaluation and reporting for target host, provider registration, and approval presence. Removed only proposal/authorization-specific authorization checks and proposal authorization output.

## Historical evidence preserved

Preserved `book_of_seed/agentic_planning_tool_prototype_contamination_recovery_001.md` as PR 1914 recovery testimony. Historical reports may still mention the removed island as witness evidence. This report supersedes PR 1914's preservation recommendation for this island.

## Remaining adjacent residue

Adjacent prototype residue remains outside this bounded operation: `Actor`, `PolicyDecision`, `ToolNeed`, `ToolNeedService`, `ToolSpec`, `Toolkit`, `ToolkitCandidate`, `ActionPlan`, `HandoffPlan`, `ProviderRecommendation`, `PendingAction`, `request_tool`, `call_tool`, and `model_visible`. `ExecutionStatus`, status emission/consumption, progress cadence, execution timing, diagnostic timing, duration measurements, and `emit_progress_if_due(...)` were left untouched except for no-op adjacency inspection.

## Surviving reference classification

The required post-excision search found no active implementation, service, event production, event projection, projected-state field, CLI dispatch, or canonical usage in `seed_runtime` or `scripts`. Surviving references were classified as follows:

- `tests/test_inquiry_orientation.py`, `tests/test_capability_candidates.py`, `tests/test_handoff_plans.py`, `tests/test_capability_verification_inspection.py`: focused structural absence tests.
- `tests/test_examination_probe_request.py`: unrelated forbidden-output vocabulary fixture.
- `book_of_seed/agentic_planning_tool_prototype_contamination_recovery_001.md`: historical PR 1914 recovery testimony.
- `book_of_seed/execution_proposal_authorization_island_excision_001.md`: this excision report.
- Other `book_of_seed` and `docs/audit` references: historical testimony or audit records describing prior/quarantined state, not active implementation instructions.
- CLI parser search results for `authorize` in `scripts/seed_local.py`: unrelated ordinary language in capability/diagnostic descriptions that says those surfaces do not authorize or execute.

## Verification

Verification commands run:

```bash
rg -n 'ExecutionProposal|ExecutionProposalFailure|ExecutionProposalService|ExecutionAuthorization|grant_execution_authorization|execution_proposal\.created|execution_authorization\.granted|execution_proposals|execution_authorizations|arguments_fingerprint' seed_runtime scripts tests book_of_seed docs
rg -n 'authorized.*executable|executable.*authorized|authorized": True|executable": True' seed_runtime scripts tests
rg -n 'proposal|authorization|authorize|grant' scripts/seed_local.py
python -m compileall -q seed_runtime scripts
python scripts/seed_local.py --help
pytest -q tests/test_action_plans.py tests/test_handoff_plans.py tests/test_projection_store.py tests/test_seed_local_script.py::test_parser_excludes_execution_proposal_and_authorization_surfaces tests/test_seed_local_script.py::test_cli_preconditions_prints_inspect_only_report_without_registering_tools tests/test_seed_local_script.py::test_cli_preconditions_target_host_fact_satisfies_host_requirement
pytest -q tests/test_state_projector.py tests/test_action_plans.py tests/test_handoff_plans.py tests/test_projection_store.py tests/test_seed_local_script.py
git diff --check
pytest -q
```

## Lawful stopping point

This operation stops at absence of the execution-proposal / authorization island. It does not decide `ActionPlan`, `HandoffPlan`, precondition grammar generally, adjacent provider/tool prototype residue, `ExecutionStatus`, or timing districts.

## Final direct answers

1. Was `ExecutionProposal` deleted? Yes.
2. Was `ExecutionProposalFailure` deleted? Yes.
3. Was `ExecutionProposalService` deleted? Yes.
4. Was `ExecutionAuthorization` deleted? Yes.
5. Was `grant_execution_authorization(...)` deleted? Yes.
6. Were proposal and authorization events deleted? Yes, active production, validation, and projection were deleted.
7. Were proposal and authorization projected-state fields deleted? Yes.
8. Was the authorization-to-`executable=True` crossing deleted? Yes.
9. Were proposal and authorization CLI surfaces deleted? Yes.
10. Were dedicated tests deleted rather than rewritten around replacements? Yes.
11. Which `ActionPlan` responsibilities remain? Creation, accept, approve, reject, supersede, precondition reporting, lifecycle events, and projection remain.
12. Which `HandoffPlan` responsibilities remain? Handoff model, handoff service, `handoff_plan.created`, provider recommendation, and capability catalog behavior remain.
13. Which precondition responsibilities remain? Target-host, provider-registration, approval-presence, declaration, evaluation, and CLI reporting responsibilities remain.
14. Which historical evidence remains? PR 1914 recovery report, this excision report, Git history, and explicitly historical/audit testimony remain.
15. Does any renamed proposal, authorization, grant, or execution-permission replacement exist? No.
16. Was `ExecutionStatus` left untouched? Yes.
17. Which adjacent prototype residue remains? `Actor`, `PolicyDecision`, `ToolNeed`, `ToolNeedService`, `ToolSpec`, `Toolkit`, `ToolkitCandidate`, `ActionPlan`, `HandoffPlan`, `ProviderRecommendation`, `PendingAction`, `request_tool`, `call_tool`, and `model_visible` remain.
18. Where must this operation stop? At the deletion boundary for this island, before redesigning execution proper, timing/status, broader ActionPlan/HandoffPlan standing, or a replacement execution architecture.

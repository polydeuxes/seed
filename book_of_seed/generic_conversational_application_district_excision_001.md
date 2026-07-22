# Generic Conversational Application District Excision 001

## Governing conclusion
PR 1912 deleted the active generic conversational application road. The removed district included generic `user` message ingress, free-form runtime handling, model-produced decision routing, `RuntimeResponse`, the generic `SeedAPI`, the generic HTTP message server, the interactive shell, and the model-decision compatibility tombstone vocabulary.

This report is corrected after PR 1912 to keep that bounded conclusion from being read as a broader architectural validation. PR 1912 proved deletion of the active conversational application road. It did not prove that every adjacent planning, policy, tool, capability, builder, provider, actor, or execution family was independently Seed-shaped. Those families remain open for the next recovery.

## Deleted district topology
The excised active road was: free-form CLI/HTTP/shell text -> `LocalSeedApp` / `SeedAPI` -> `Runtime.handle_user_message(...)` -> `input.user_message` and `runtime.decision_authority_unsupported` ledger events -> `RuntimeResponse` -> generic CLI/HTTP serialization.

## Files and surfaces removed
- Deleted `seed_runtime/runtime.py` and `seed_runtime/api.py`.
- Removed `RuntimeResponse` from `seed_runtime/models.py`.
- Removed the `Runtime` import and all `LocalSeedApp`, `build_local_app`, `LocalSeedApp.run`, `run_http`, `run_shell`, `format_response_summary`, and `format_cli_output` surfaces from `scripts/seed_local.py`.
- Removed `--http`, `--host`, and `--port` parser behavior, generic `/message` and `/health` serving, one-shot free-form message execution, and the no-argument interactive shell fallback.
- Deleted tests dedicated to `SeedAPI`, `RuntimeResponse`, `Runtime.handle_user_message`, the unsupported model-decision response, and tombstone events.
- Deleted `book_of_seed/runtime_unsupported_response_active_road_fidelity_recovery_001.md`.

## Post-excision correction
This correction removes the obsolete runtime-ownership architecture-generator family and its generated artifacts. It also removes stale architectural/canonical assertions that survived adjacent to the PR 1912 deletion:

- `seed_runtime/execution_proposals.py::ExecutionProposalFailure` is no longer used as a representative refusal anchor in the refusal chapter.
- `ToolNeedService.__seed_arch__` is removed, so `ToolNeedService` is not presented through generated ownership metadata as settled runtime architecture.
- No replacement ownership metadata, generated architecture graph, repository-wide ownership graph, constitutional graph generator, topology generator, or new metadata convention is introduced.

Removing architecture metadata does not validate the implementation. Preserving adjacent implementation temporarily does not establish constitutional ownership.

## Responsibilities preserved without broader validation
Observation ingestion, JSON observation import/export/diff, repository observation, Prometheus observation as provider-specific HTTP observation, state projection/read-model views, evidence views, diagnostics, lifecycle operations, bounded question-family dispatch, and projection-cache operations remained as direct CLI/module roads. `LocalSeedApp` wrappers were not replaced; surviving CLI code calls ledger, observation, and projection owners directly.

Explicit planning, proposal, authorization, ToolNeed, policy, provider recommendation, and tool-generation surfaces survived outside the bounded conversational-road excision. Their survival is not evidence that they are independently faithful Seed responsibilities. They are retained temporarily pending a separate contamination recovery.

## District-dependent scaffolds removed
The runtime input boundary, generic API adapter, local app container, conversational response formatting, HTTP message server, interactive shell loop, one-shot free-text path, `input.user_message`, `runtime.decision_authority_unsupported`, `model_decision_authority_excised`, and `DecisionProducer.decide -> Runtime._route` tombstone vocabulary were removed from active implementation.

## Adjacent unresolved residue preserved
Constructible interpretation, candidate request/route inspection, bounded question-family surfaces, warrants, applicability/admission families, goal artifacts, planning lifecycle, proposal lifecycle, authorization lifecycle, capability/tool-need vocabulary, provider recommendation vocabulary, user/model actor vocabulary, and request_tool / call_tool architecture vocabulary were not wired into a replacement runtime. They are outside the bounded conversational-road excision, are not established as independently faithful by PR 1912, and remain unresolved adjacent prototype residue unless separately recovered.

## Book contamination corrected
The PR 1911 recovery report was deleted. The refusal chapter no longer canonizes refusal as a `Decision` kind, no longer anchors to `models.py::Decision`, and no longer uses `ExecutionProposalFailure` as a representative refusal anchor. It preserves only refusal/non-performance distinctions.

## Remaining occurrences classified
- `user`: remaining implementation occurrences include legacy observation source vocabulary such as `source_type="user"`, action-plan approval defaults, operating-system local user account observation predicates, user approval vocabulary, third-party/provider wording, fixture text, and historical Book quotations. They do not create generic conversational ingress. Where they participate in actor, planning, approval, source, or prototype-routing surfaces, they are unresolved adjacent prototype residue.
- `model`: remaining occurrences include Pydantic/domain models, read models, provider/model historical reports, external model history, and actor grammar such as `Actor = Literal["user", "model", ...]`. No active model-produced runtime decision route remains. Actor vocabulary remains unresolved adjacent prototype residue where it carries user/model/system/builder/approver roles.
- `Decision`: remaining Book occurrences include historical/tool-road recovery testimony. Active implementation contains `PolicyDecision`, a policy gate outcome, not universal conversational decision routing. `PolicyDecision` remains unresolved adjacent prototype residue for future policy-family recovery.
- `API`: remaining occurrences are ordinary external-provider/API wording or historical reports; `seed_runtime.api.SeedAPI` is deleted.
- `HTTP`: remaining active HTTP usage is provider observation/client behavior such as Prometheus observation, not a generic Seed message server.
- `ToolSpec.visibility = "model_visible"`, `ToolNeed` status/generation vocabulary, `ToolkitCandidate` and tool generation, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, `ExecutionProposalFailure`, `ExecutionAuthorization`, `PendingAction`, provider recommendations, and request_tool / call_tool vocabulary survived PR 1912 but are unresolved adjacent prototype residue, not independently validated Seed architecture.
- Required residual search terms in tests, where present, are fixture text for reconciliation tests or historical reports; those tests exercise claim reconciliation behavior, not a live runtime path.

## Adjacent residue ledger for next operation
| Subject | Current file or surface | Why adjacent to the old prototype | Current standing |
| --- | --- | --- | --- |
| Actor / user / model / system / builder / approver | `seed_runtime/events.py`, `seed_runtime/models.py`, tests, Book references | Preserves old actor vocabulary near user/model conversational framing and approval roles. | Unknown |
| PolicyDecision | `seed_runtime/policy.py` | Survived as decision-shaped policy outcome adjacent to deleted model-decision routing. | Unknown |
| ToolNeed and ToolNeedService | `seed_runtime/models.py`, `seed_runtime/tool_needs.py` | Preserves request/capability-gap lifecycle that was formerly routed from request_tool decisions. | Unknown |
| ToolSpec and model_visible | `seed_runtime/tools.py` | Preserves model-facing tool visibility vocabulary. | Unknown |
| ToolkitCandidate and tool generation | `seed_runtime/tool_generation.py` | Preserves tool-generation candidate vocabulary adjacent to prototype tool routing. | Unknown |
| ActionPlan | `seed_runtime/planning.py` | Preserves planning lifecycle vocabulary adjacent to prototype action routing. | Unknown |
| HandoffPlan | `seed_runtime/handoffs.py` | Preserves handoff planning vocabulary adjacent to tool/provider routing. | Unknown |
| ExecutionProposal and ExecutionProposalFailure | `seed_runtime/execution_proposals.py` | Preserves proposal/failure vocabulary adjacent to authorization and execution prototype paths. | Unknown |
| ExecutionAuthorization | `seed_runtime/execution_authorization.py` | Preserves authorization lifecycle vocabulary adjacent to proposal/execution paths. | Unknown |
| PendingAction | `seed_runtime/execution.py`, `seed_runtime/models.py` | Preserves pending execution vocabulary adjacent to tool-call and approval paths. | Unknown |
| Provider recommendations | `seed_runtime/provider_recommendations.py`, capability catalog surfaces | Preserves recommendation ranking for providers/handoffs adjacent to capability/tool need routing. | Unknown |
| request_tool / call_tool vocabulary | `seed_runtime/models.py`, `seed_runtime/execution.py`, historical docs/tests | Preserves explicit prototype tool-routing vocabulary after Runtime deletion. | Unknown |
| Remaining runtime_service or runtime ownership metadata | Surviving `__seed_arch__` metadata in implementation and historical docs | May still encode ownership/layer claims inherited from runtime architecture framing. | Unknown |

## CLI behavior after excision
The CLI remains an explicit command surface. No explicit operation prints help. Free-form positional text raises a parser error: free-form message mode is not supported. `ask --question-family ...` remains the only supported positional-token dispatch because it is an existing bounded question-family surface.

## Tests and verification
Verification commands run in the original excision included searches for removed runtime/API/response/tombstone vocabulary, compile checks, CLI help, diff checks, and focused/full pytest runs. This correction adds searches for the deleted architecture-generator family, the refusal chapter anchor, removed ToolNeedService architecture metadata, and adjacent unresolved residue, followed by compile, CLI help, diff, focused checks, and full pytest.

## Direct answers
1. Yes, the obsolete runtime-ownership generator was deleted.
2. Yes, all generated runtime-ownership artifacts were deleted.
3. Yes, its dedicated test was deleted.
4. Yes, `ExecutionProposalFailure` was removed from the refusal chapter.
5. Yes, `ToolNeedService.__seed_arch__` was removed.
6. No replacement ownership metadata was introduced.
7. No, this report no longer claims planning/proposal/authorization families are independently faithful.
8. Adjacent prototype families that remain include Actor/user/model/system/builder/approver, PolicyDecision, ToolNeed and ToolNeedService, ToolSpec/model_visible, ToolkitCandidate/tool generation, ActionPlan, HandoffPlan, ExecutionProposal and ExecutionProposalFailure, ExecutionAuthorization, PendingAction, provider recommendations, request_tool / call_tool vocabulary, and remaining runtime_service or runtime ownership metadata.
9. Each remaining family listed in the adjacent residue ledger currently has Unknown standing unless and until a separate recovery narrows it.
10. No broader prototype family was deleted or redesigned.
11. No CLI, observation, projection, or Prometheus behavior changed.
12. This correction stops at preserving PR 1912 conversational-road deletion, deleting the obsolete runtime-ownership generator and artifacts, removing the stale refusal anchor and ToolNeedService architecture metadata, and marking adjacent prototype residue unresolved for the next contamination survey.

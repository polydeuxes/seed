# Generic Conversational Application District Excision 001

## Governing conclusion
The generic conversational application district is foreign to Seed.  The removed district included generic `user` message ingress, free-form runtime handling, model-produced decision routing, `RuntimeResponse`, the generic `SeedAPI`, the generic HTTP message server, the interactive shell, and the model-decision compatibility tombstone vocabulary.

## Deleted district topology
The excised active road was: free-form CLI/HTTP/shell text -> `LocalSeedApp` / `SeedAPI` -> `Runtime.handle_user_message(...)` -> `input.user_message` and `runtime.decision_authority_unsupported` ledger events -> `RuntimeResponse` -> generic CLI/HTTP serialization.

## Files and surfaces removed
- Deleted `seed_runtime/runtime.py` and `seed_runtime/api.py`.
- Removed `RuntimeResponse` from `seed_runtime/models.py`.
- Removed the `Runtime` import and all `LocalSeedApp`, `build_local_app`, `LocalSeedApp.run`, `run_http`, `run_shell`, `format_response_summary`, and `format_cli_output` surfaces from `scripts/seed_local.py`.
- Removed `--http`, `--host`, and `--port` parser behavior, generic `/message` and `/health` serving, one-shot free-form message execution, and the no-argument interactive shell fallback.
- Deleted tests dedicated to `SeedAPI`, `RuntimeResponse`, `Runtime.handle_user_message`, the unsupported model-decision response, and tombstone events.
- Deleted `book_of_seed/runtime_unsupported_response_active_road_fidelity_recovery_001.md`.

## Independent responsibilities preserved
Observation ingestion, JSON observation import/export/diff, repository observation, Prometheus observation as provider-specific HTTP observation, state projection/read-model views, evidence views, diagnostics, lifecycle operations, explicit planning/proposal/authorization side paths, bounded question-family dispatch, and projection-cache operations remain as direct CLI/module roads.  `LocalSeedApp` wrappers were not replaced; surviving CLI code calls ledger, observation, and projection owners directly.

## District-dependent scaffolds removed
The runtime input boundary, generic API adapter, local app container, conversational response formatting, HTTP message server, interactive shell loop, one-shot free-text path, `input.user_message`, `runtime.decision_authority_unsupported`, `model_decision_authority_excised`, and `DecisionProducer.decide -> Runtime._route` tombstone vocabulary were removed from active implementation.

## Adjacent Unknowns preserved
Constructible interpretation, candidate request/route inspection, bounded question-family surfaces, warrants, applicability/admission families, and goal artifacts were not wired into a replacement runtime.  They are preserved only as independent or Unknown constitutional witnesses where they already existed outside the deleted road.

## Book contamination removed
The PR 1911 recovery report was deleted.  The refusal chapter no longer canonizes refusal as a `Decision` kind and no longer anchors to `models.py::Decision`; it preserves only refusal/non-performance distinctions.

## Remaining occurrences classified
- `user`: remaining implementation occurrences are legacy observation source vocabulary (`source_type="user"`), action-plan approval defaults, operating-system local user account observation predicates, third-party/provider wording, and historical Book quotations.  They do not create generic conversational ingress.
- `model`: remaining occurrences refer to Pydantic/domain models, read models, provider/model historical reports, or external model history; no active model-produced runtime decision route remains.
- `Decision`: remaining Book occurrences are historical/tool-road recovery testimony.  Active implementation contains `PolicyDecision`, a policy gate outcome, not universal conversational decision routing.
- `API`: remaining occurrences are ordinary external-provider/API wording or historical reports; `seed_runtime.api.SeedAPI` is deleted.
- `HTTP`: remaining active HTTP usage is provider observation/client behavior such as Prometheus observation, not a generic Seed message server.
- Required residual search terms in tests (`handle_user_message`) are fixture text for self-model/existence/structure reconciliation tests; those tests exercise claim reconciliation behavior, not a live runtime path.

## CLI behavior after excision
The CLI remains an explicit command surface.  No explicit operation prints help.  Free-form positional text now raises a parser error: free-form message mode is not supported.  `ask --question-family ...` remains the only supported positional-token dispatch because it is an existing bounded question-family surface.

## Tests and verification
Verification commands run in this excision:
- `rg -n 'RuntimeResponse|handle_user_message|SeedAPI|LocalSeedApp|build_local_app|run_shell|run_http|input\.user_message|runtime\.decision_authority_unsupported|model_decision_authority_excised|DecisionProducer\.decide|Runtime\._route|No Seed-owned runtime decision authority|free-text input|user message' .`
- `rg -n '\buser\b|user_input|user_message|actor="user"|source_type="user"' seed_runtime scripts tests book_of_seed`
- `rg -n '\bDecision\b|decision authority|decision producer|decision routing|model-produced Decision|runtime decision' seed_runtime scripts tests book_of_seed`
- `python -m compileall -q seed_runtime scripts`
- `python scripts/seed_local.py --help`
- `git diff --check`
- focused and full pytest runs recorded in the implementation turn.

## Direct answers
1. Yes, the generic user-message/model-Decision/runtime-response district was removed from active implementation.
2. Yes, `LocalSeedApp` was deleted.
3. Yes, the interactive free-text shell was deleted.
4. Yes, the generic HTTP message server was deleted.
5. Yes, `SeedAPI` was deleted.
6. Yes, `Runtime` was deleted.
7. Yes, `RuntimeResponse` was deleted.
8. Yes, the tombstone events and response vocabulary were deleted from active implementation.
9. Independent observation, projection, diagnostic, provider observation, read-model/evidence, lifecycle, and explicit bounded command responsibilities survived.
10. Adjacent constructible interpretation artifacts survived only where independent or Unknown; this excision did not decide their future architecture.
11. Remaining `user` occurrences are legacy observation source vocabulary, action-plan approval defaults, OS account vocabulary, third-party/provider wording, fixture text, or historical quotations.
12. Remaining `Decision` occurrences are historical Book testimony or policy-gate `PolicyDecision`, not generic model-produced runtime routing.
13. No generic conversational, API, HTTP, or response replacement was introduced.
14. The operation stops at removing the foreign district and preserving independently evidenced Seed roads without inventing replacement ingress.

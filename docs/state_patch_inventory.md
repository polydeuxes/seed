# State Patch Inventory

This inventory is source-file based and describes the existing state patch behavior before any RuntimeLoop parity decision. It intentionally does not propose or implement behavior changes.

## 1. Models

### Decision fields involved

- The legacy `seed_runtime.models.DecisionKind` includes `"propose_state_patch"` alongside `answer`, `ask_question`, `call_tool`, `request_tool`, `propose_action_plan`, `propose_handoff_plan`, and `refuse`.
  [`seed_runtime/models.py:42-51`](../seed_runtime/models.py#L42-L51)
- `seed_runtime.models.Decision` carries `kind`, required `reason`, and optional per-kind payload fields. State patch decisions use the optional `state_patch: dict[str, Any] | None` field.
  [`seed_runtime/models.py:205-215`](../seed_runtime/models.py#L205-L215)
- Runtime response values are represented by `RuntimeResponse(kind: str, message: str, payload: dict[str, Any])`.
  [`seed_runtime/models.py:318-321`](../seed_runtime/models.py#L318-L321)
- Legacy model-client prompt schemas/examples include `propose_state_patch` with `state_patch: {}` as a decision shape, and include `state_patch` among known decision fields.
  [`seed_runtime/model_client.py:195-221`](../seed_runtime/model_client.py#L195-L221)
  [`seed_runtime/model_clients.py:42-60`](../seed_runtime/model_clients.py#L42-L60)

### Patch payload shape

`StatePatchService` accepts two payload forms:

1. **Explicit operation list:** `state_patch["ops"]` or `state_patch["operations"]` is read first. If present, it must be a list of object operations; each operation is copied before application.
   [`seed_runtime/state_patches.py:53-61`](../seed_runtime/state_patches.py#L53-L61)
2. **Legacy collection shape:** when neither `ops` nor `operations` is present, the service expands collection keys into operations in this order:
   - `entities[]` -> `{"op": "upsert_entity", "entity": entity}`
   - `evidence[]` -> `{"op": "observe_evidence", "evidence": evidence}`
   - `facts[]` -> `{"op": "observe_fact", "fact": fact}`
   - `goals[]` -> `{"op": "create_goal", "goal": goal}`

   [`seed_runtime/state_patches.py:63-72`](../seed_runtime/state_patches.py#L63-L72)

For individual operations, the service accepts either a nested payload under the operation-specific key (`entity`, `evidence`, `fact`, or `goal`) or an inline payload made from all operation fields except `op` and `operation`.
[`seed_runtime/state_patches.py:145-149`](../seed_runtime/state_patches.py#L145-L149)

### Supported operations

- `upsert_entity`: appends `entity.upserted` with payload `{"entity": ...}`.
  [`seed_runtime/state_patches.py:82-94`](../seed_runtime/state_patches.py#L82-L94)
- `observe_evidence`: appends `evidence.observed` with payload `{"evidence": ...}`.
  [`seed_runtime/state_patches.py:95-112`](../seed_runtime/state_patches.py#L95-L112)
- `observe_fact`: appends `fact.observed` with payload `{"fact": ...}`.
  [`seed_runtime/state_patches.py:113-126`](../seed_runtime/state_patches.py#L113-L126)
- `create_goal`: appends `goal.created` with payload `{"goal": ...}`.
  [`seed_runtime/state_patches.py:127-142`](../seed_runtime/state_patches.py#L127-L142)

All emitted state patch events use actor `system`, carry the provided `session_id`, and carry the model decision event id as `causation_id` when routed through `Runtime`.
[`seed_runtime/runtime.py:311-318`](../seed_runtime/runtime.py#L311-L318)
[`seed_runtime/state_patches.py:87-94`](../seed_runtime/state_patches.py#L87-L94)
[`seed_runtime/state_patches.py:105-112`](../seed_runtime/state_patches.py#L105-L112)
[`seed_runtime/state_patches.py:119-126`](../seed_runtime/state_patches.py#L119-L126)
[`seed_runtime/state_patches.py:134-142`](../seed_runtime/state_patches.py#L134-L142)

### Validation and defaulting rules

There are two validation layers:

1. `DecisionValidator` only checks that `propose_state_patch` has a truthy `decision.state_patch`; it does not inspect operations or entity/fact/evidence/goal fields.
   [`seed_runtime/decisions.py:42-62`](../seed_runtime/decisions.py#L42-L62)
2. `StatePatchService` validates the patch shape and operations during application:
   - `ops`/`operations`, if present, must be a list.
     [`seed_runtime/state_patches.py:53-57`](../seed_runtime/state_patches.py#L53-L57)
   - Every operation and every extracted payload must be an object.
     [`seed_runtime/state_patches.py:58-61`](../seed_runtime/state_patches.py#L58-L61)
     [`seed_runtime/state_patches.py:151-154`](../seed_runtime/state_patches.py#L151-L154)
   - Unsupported operations raise `StatePatchError("unsupported state patch op ...")`.
     [`seed_runtime/state_patches.py:82-143`](../seed_runtime/state_patches.py#L82-L143)
   - Required fields are checked after defaults are filled; missing or `None` fields raise `StatePatchError("<label> missing required field(s): ...")`.
     [`seed_runtime/state_patches.py:156-159`](../seed_runtime/state_patches.py#L156-L159)

Operation-specific defaults and required fields:

| Operation | Defaults added | Required after defaults |
| --- | --- | --- |
| `upsert_entity` | `id = new_id("ent")` | `id`, `kind`, `name` |
| `observe_evidence` | `id = new_id("evd")`, `workspace_id = workspace_id`, `observed_at = utc_now()`, `payload = {}`, `confidence = 1.0` | `id`, `workspace_id`, `source`, `kind` |
| `observe_fact` | `id = new_id("fact")`, `evidence_ids = []`, `observed_at = utc_now()` | `id`, `subject_id`, `predicate`, `value` |
| `create_goal` | `id = new_id("goal")`, `workspace_id = workspace_id`, `status = "active"`, `created_from_event_id = causation_id` when supplied | `id`, `workspace_id`, `summary` |

[`seed_runtime/state_patches.py:82-142`](../seed_runtime/state_patches.py#L82-L142)

### Result shape

- The service returns a frozen dataclass `StatePatchResult` containing the list of appended `Event` objects.
  [`seed_runtime/state_patches.py:15-19`](../seed_runtime/state_patches.py#L15-L19)
- Runtime success responses have `kind="state_updated"`, message `Applied N state patch operation(s).`, and payload containing `event_ids` and serialized full `events`.
  [`seed_runtime/runtime.py:333-340`](../seed_runtime/runtime.py#L333-L340)
- Runtime failure responses have `kind="invalid_state_patch"`, message `State patch failed validation.`, and payload `{"errors": [<error>]}`.
  [`seed_runtime/runtime.py:319-332`](../seed_runtime/runtime.py#L319-L332)

## 2. Old `Runtime` behavior

### Validation and routing

`Runtime.handle_user_message` appends `input.user_message`, projects state, composes context, asks the model for a `Decision`, appends `model.decision.proposed`, runs `DecisionValidator`, runs `ToolIntentGuard`, and only then routes by decision kind.
[`seed_runtime/runtime.py:68-126`](../seed_runtime/runtime.py#L68-L126)

For `propose_state_patch`, the initial validation is only the `DecisionValidator` truthiness check for `state_patch`.
[`seed_runtime/decisions.py:54-56`](../seed_runtime/decisions.py#L54-L56)
If validation passes, `_route` dispatches to `self.state_patch_service.apply(workspace_id, decision.state_patch or {}, session_id=session_id, causation_id=decision_event.id)`.
[`seed_runtime/runtime.py:311-318`](../seed_runtime/runtime.py#L311-L318)
The service is constructed inside `Runtime.__init__` as `StatePatchService(ledger, projector)`.
[`seed_runtime/runtime.py:37-65`](../seed_runtime/runtime.py#L37-L65)

### Emitted events

A successful state patch route emits:

1. `input.user_message` from `Runtime.handle_user_message`.
2. `model.decision.proposed` with serialized decision and retry attempt.
3. One state projection source event per operation: `entity.upserted`, `evidence.observed`, `fact.observed`, or `goal.created`.

[`seed_runtime/runtime.py:71-77`](../seed_runtime/runtime.py#L71-L77)
[`seed_runtime/runtime.py:110-117`](../seed_runtime/runtime.py#L110-L117)
[`seed_runtime/state_patches.py:82-142`](../seed_runtime/state_patches.py#L82-L142)

A state patch application failure emits `state.patch.rejected` with payload `{"error": str(exc), "state_patch": decision.state_patch or {}}`, actor `system`, the current session id, and causation id set to the model decision event.
[`seed_runtime/runtime.py:319-327`](../seed_runtime/runtime.py#L319-L327)

### Failure behavior

- If the decision omits `state_patch` or supplies a falsy value, the decision is invalid before routing. Runtime appends `model.decision.invalid`, may retry, and eventually returns `RuntimeResponse(kind="invalid_decision", message="Model decision failed validation.", payload={"errors": [...]})` if retries are exhausted.
  [`seed_runtime/decisions.py:54-56`](../seed_runtime/decisions.py#L54-L56)
  [`seed_runtime/runtime.py:150-171`](../seed_runtime/runtime.py#L150-L171)
- If service-level validation raises `StatePatchError`, Runtime catches it, appends `state.patch.rejected`, and returns `invalid_state_patch` as described above.
  [`seed_runtime/runtime.py:319-332`](../seed_runtime/runtime.py#L319-L332)
- Application is sequential. `StatePatchService.apply` appends each operation as it is processed and does not perform an explicit preflight of all operations or rollback already appended events if a later operation fails.
  [`seed_runtime/state_patches.py:40-51`](../seed_runtime/state_patches.py#L40-L51)

### Success behavior

On success, the service returns every appended event and Runtime returns `state_updated` with event ids plus serialized event payloads. Runtime does not append a separate `state.patch.applied` summary event; the domain events are the durable state mutation events.
[`seed_runtime/state_patches.py:40-51`](../seed_runtime/state_patches.py#L40-L51)
[`seed_runtime/runtime.py:333-340`](../seed_runtime/runtime.py#L333-L340)

## 3. Projection behavior

`StateProjector.apply` consumes the same domain event kinds emitted by `StatePatchService`:

- `entity.upserted`: reads `payload["entity"]` or the payload itself, constructs an `Entity`, and stores it by id.
- `evidence.observed`: reads `payload["evidence"]` or the payload itself, parses/defaults `observed_at`, constructs `Evidence`, and stores it by id.
- `fact.observed`: normalizes the fact event payload, marks it non-inferred, constructs `Fact`, stores it by id, and refreshes relationship projections.
- `goal.created`: reads `payload["goal"]` or the payload itself, constructs `Goal`, and stores it by id.

[`seed_runtime/state.py:746-782`](../seed_runtime/state.py#L746-L782)

After replaying events, projection also recomputes alias resolution, measurement-history retention, observed/inferred fact splits, fact supports/conflicts, relationship projections, entity type assertions, graph issues, and entity aliases.
[`seed_runtime/state.py:709-744`](../seed_runtime/state.py#L709-L744)

## 4. CLI/API behavior

### CLI

The local CLI builds both old `Runtime` and new `RuntimeLoop`, but `LocalSeedApp.run` uses `RuntimeLoop.run` by default and maps the `RuntimeResult` back to the existing CLI response shape.
[`scripts/seed_local.py:223-245`](../scripts/seed_local.py#L223-L245)
[`scripts/seed_local.py:650-695`](../scripts/seed_local.py#L650-L695)

The old Runtime path remains reachable through `LocalSeedApp.run_legacy`, which calls `self.runtime.handle_user_message(...)` and returns the serialized response plus all ledger events.
[`scripts/seed_local.py:290-299`](../scripts/seed_local.py#L290-L299)
However, current CLI command routing selects `run_legacy` only when `--plan` is used; ordinary one-shot messages and shell messages use `app.run`, and the HTTP local server uses `app.run` unless the request is raw.
[`scripts/seed_local.py:3394-3418`](../scripts/seed_local.py#L3394-L3418)
[`scripts/seed_local.py:3450-3480`](../scripts/seed_local.py#L3450-L3480)
[`scripts/seed_local.py:3961-3975`](../scripts/seed_local.py#L3961-L3975)

There is no dedicated CLI flag that submits a state patch directly. CLI state-writing flags seed facts, observations, aliases, local-host observations, Prometheus observations, and registered-provider/tool state through separate ingestion helpers rather than through `StatePatchService`.
[`scripts/seed_local.py:1545-1626`](../scripts/seed_local.py#L1545-L1626)

### API

`SeedAPI` wraps `RuntimeLoop`, not old `Runtime`. `post_user_message` converts `(workspace_id, session_id, text)` into `RuntimeInput(... metadata={"session_id": session_id})` and calls `runtime.run`.
[`seed_runtime/api.py:15-32`](../seed_runtime/api.py#L15-L32)
Because RuntimeLoop lacks a state patch decision kind today, the API path does not expose state patch behavior.
[`seed_runtime/runtime_loop.py:32-68`](../seed_runtime/runtime_loop.py#L32-L68)
[`seed_runtime/runtime_loop.py:725-729`](../seed_runtime/runtime_loop.py#L725-L729)

## 5. RuntimeLoop behavior

RuntimeLoop's local `DecisionKind` is `Literal["answer", "call_tool", "request_tool"]`; its `Decision` dataclass has no `state_patch` field.
[`seed_runtime/runtime_loop.py:32-68`](../seed_runtime/runtime_loop.py#L32-L68)
Its validation rejects every proposed decision whose kind is not one of `answer`, `call_tool`, or `request_tool` with the error `decision kind must be 'answer', 'call_tool', or 'request_tool'`.
[`seed_runtime/runtime_loop.py:725-729`](../seed_runtime/runtime_loop.py#L725-L729)
There is no RuntimeLoop branch that routes `propose_state_patch`, and RuntimeLoop does not construct or call `StatePatchService`.
[`seed_runtime/runtime_loop.py:123-157`](../seed_runtime/runtime_loop.py#L123-L157)
[`seed_runtime/runtime_loop.py:218-688`](../seed_runtime/runtime_loop.py#L218-L688)

## 6. Test coverage

- `tests/test_decisions.py::test_propose_state_patch_requires_state_patch` verifies that `DecisionValidator` accepts a `propose_state_patch` decision with a truthy `state_patch` and rejects one with no `state_patch` using the exact validation error.
  [`tests/test_decisions.py:100-115`](../tests/test_decisions.py#L100-L115)
- `tests/test_state_patches.py::test_state_patch_service_applies_minimum_supported_ops` covers all four supported operations, verifies emitted event kinds and causation ids, verifies defaulted `observed_at`, verifies evidence workspace defaulting, verifies fact evidence ids, and verifies goal `created_from_event_id` projection.
  [`tests/test_state_patches.py:29-99`](../tests/test_state_patches.py#L29-L99)
- `tests/test_state_patches.py::test_state_patch_service_accepts_legacy_collection_shape` covers the legacy `entities`/`facts` collection expansion and resulting event order.
  [`tests/test_state_patches.py:101-123`](../tests/test_state_patches.py#L101-L123)
- `tests/test_state_patches.py::test_state_patch_service_rejects_unknown_op` covers an unsupported operation error and verifies no events were appended for that single-operation failure.
  [`tests/test_state_patches.py:126-137`](../tests/test_state_patches.py#L126-L137)
- `tests/test_state_patches.py::test_runtime_routes_propose_state_patch_to_state_updated_response` covers old Runtime routing for a successful `propose_state_patch`, the response kind/message, emitted event sequence, and projected entity/goal state.
  [`tests/test_state_patches.py:140-179`](../tests/test_state_patches.py#L140-L179)
- RuntimeLoop tests cover malformed provider outputs and validation rejection generally, but there is no dedicated RuntimeLoop state patch test because RuntimeLoop has no state patch decision kind.
  [`tests/test_runtime_loop.py:738-749`](../tests/test_runtime_loop.py#L738-L749)

Notable gaps in direct tests:

- No direct Runtime-route test for service-level state patch rejection (`state.patch.rejected` / `invalid_state_patch`). The route exists in source.
  [`seed_runtime/runtime.py:319-332`](../seed_runtime/runtime.py#L319-L332)
- No direct test for non-list `ops`, non-object operations, missing operation payload fields, inline operation payloads, or partial-application behavior when an earlier operation succeeds and a later one fails.
  [`seed_runtime/state_patches.py:40-61`](../seed_runtime/state_patches.py#L40-L61)
  [`seed_runtime/state_patches.py:145-159`](../seed_runtime/state_patches.py#L145-L159)

## 7. Migration risks

If old `Runtime` were removed before state patch parity exists, these behaviors would be lost from user-message runtime paths:

- The legacy model decision kind `propose_state_patch` would no longer have a runtime route, even though the shared `Decision` model and legacy prompt schemas still describe it.
  [`seed_runtime/models.py:42-51`](../seed_runtime/models.py#L42-L51)
  [`seed_runtime/model_client.py:214-218`](../seed_runtime/model_client.py#L214-L218)
- Model-proposed writes of entities, evidence, facts, and goals through `StatePatchService` would no longer be reachable through a runtime decision.
  [`seed_runtime/runtime.py:311-340`](../seed_runtime/runtime.py#L311-L340)
  [`seed_runtime/state_patches.py:82-142`](../seed_runtime/state_patches.py#L82-L142)
- The `state_updated` and `invalid_state_patch` response contracts would disappear from the runtime message path.
  [`seed_runtime/runtime.py:319-340`](../seed_runtime/runtime.py#L319-L340)
- The `state.patch.rejected` event would no longer be emitted for state patch application errors.
  [`seed_runtime/runtime.py:319-327`](../seed_runtime/runtime.py#L319-L327)
- CLI `--plan` currently uses `run_legacy`; removing old Runtime would also remove any incidental access to state patch behavior through that legacy path, although the default CLI and API paths already use RuntimeLoop and therefore do not expose state patches.
  [`scripts/seed_local.py:290-299`](../scripts/seed_local.py#L290-L299)
  [`scripts/seed_local.py:3961-3975`](../scripts/seed_local.py#L3961-L3975)
  [`seed_runtime/api.py:15-32`](../seed_runtime/api.py#L15-L32)

## 8. Extraction candidates: possible shared service boundary only

No implementation is proposed here. If state patches are later ported, the clean existing boundary is already `StatePatchService.apply(workspace_id, state_patch, session_id=None, causation_id=None) -> StatePatchResult`.
[`seed_runtime/state_patches.py:26-51`](../seed_runtime/state_patches.py#L26-L51)
A shared route-level boundary could preserve the current separation:

- `DecisionValidator` remains responsible only for decision-level presence checks.
  [`seed_runtime/decisions.py:54-56`](../seed_runtime/decisions.py#L54-L56)
- `StatePatchService` remains responsible for patch expansion, operation validation/defaulting, and domain event appends.
  [`seed_runtime/state_patches.py:53-159`](../seed_runtime/state_patches.py#L53-L159)
- The runtime layer remains responsible for decision routing, response shaping, and rejection-event emission.
  [`seed_runtime/runtime.py:311-340`](../seed_runtime/runtime.py#L311-L340)

The main design choice for parity is whether RuntimeLoop should intentionally add a `propose_state_patch` decision kind and call the existing service, adapt state patch semantics into a different RuntimeLoop-specific write path, or leave model-proposed state mutation as old-Runtime-only / unsupported.

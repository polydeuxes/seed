# Runtime Unsupported Response Active-Road Fidelity Recovery 001

## Scope and negative authority

This is one bounded, report-only Fidelity recovery of the current producer-to-`RuntimeResponse`-to-consumer road for free-text input at `Runtime.handle_user_message(...)` on current merged `main` after PR 1910. It does not amend the Book, production code, tests, CLI behavior, API behavior, events, response text, runtime wiring, or any decision-authority route.

Negative authority preserved: response returned does not prove a current consumer; callable handler does not prove an entrypoint; recorded input does not prove interpretation, question formation, addressability, verified user identity, operator receipt, understanding, acceptance, or reliance; route-local absence does not prove Seed-wide authority absence; `unsupported` does not by itself classify the input as unsupported; the reason string `model_decision_authority_excised` does not by itself prove historical excision, current causation, or faithful explanation.

## Book clauses actually needed

The recovery used only current clauses needed to judge the boundary:

- `refusal-and-non-performance.md`: refusal is a lawful decision not to perform when authority, safety, capability, or required conditions are absent; refusal is distinct from execution failure, policy block, missing capability, or abandonment.
- `stopping-and-completion.md`: stopping is grounded in sufficiency, exhaustion, impossibility, refusal, or operator conditions and is not completion, global impossibility, or failure.
- `communication-and-handoff.md`: egress representation preserves result standing without strengthening it; delivery, rendering, API emission, or convenience does not prove receipt, understanding, reliance, action authority, or stronger truth.
- `external-and-constitutional-grammar.md`: implementation and serialization grammar are not constitutional grammar; external/model-produced decision grammar may be addressed or refused without becoming Seed-native authority.
- `orientation-and-movement.md`: event recording, runtime values, route changes, or displayed labels are not constitutional movement unless warrant, subject, evidence, authority, scope, and limits are preserved.
- `authority-scope.md`: downstream reliance must remain bounded to the role, purpose, provenance, evidence, authority, scope, confidence, Unknowns, and negative authority preserved by the warrant; internal records and provider/model outputs do not create or enlarge authority.

## Search and path method

Commands used as repository evidence:

```bash
rg -n "RuntimeResponse|handle_user_message|decision_authority_unsupported|input\.user_message|model_decision_authority_excised|No Seed-owned runtime" -S .
rg -n "handle_user_message\(" -S --glob '!tests/**' --glob '!*.md' .
rg -n "RuntimeResponse\(" -S --glob '!tests/**' --glob '!*.md' .
rg -n "response\[|response\.|to_plain\(response\)|handle_user_message|post_user_message" scripts seed_runtime -S
sed -n '1,140p' seed_runtime/runtime.py
sed -n '300,330p' seed_runtime/models.py
sed -n '1,80p' seed_runtime/api.py
sed -n '500,590p' scripts/seed_local.py
sed -n '2680,2805p' scripts/seed_local.py
sed -n '6460,6538p' scripts/seed_local.py
sed -n '8070,8110p' scripts/seed_local.py
```

Tests, fixtures, reports, and docs were treated as testimony, not as proof of active non-test handoff. Production Python files were used to establish current executable paths.

## RuntimeResponse definition and artifact standing

`RuntimeResponse` is a Pydantic `SeedModel` envelope with `kind: str`, `message: str`, and `payload: dict[str, Any]` defaulting to an empty dict. Its artifact standing is transport/presentation preservation of a bounded runtime result. The class definition alone does not perform refusal, establish authority absence, prove a consumer, or establish operator receipt.

All non-test direct constructions found in current production code within the requested search scope are the single construction in `seed_runtime/runtime.py`: `RuntimeResponse(kind="unsupported", message="No Seed-owned runtime decision authority is configured for free-text input.", payload={"reason": "model_decision_authority_excised", "input_event_id": input_event.id})`. No other non-test `RuntimeResponse(...)` construction is evidenced by the search.

## Producer act recovery

- **Entrypoint:** `Runtime.handle_user_message(workspace_id, session_id, text)`.
- **Non-test callers evidenced:** `SeedAPI.post_user_message(...)`; `LocalSeedApp.run(text)`; `run_http(...).Handler.do_POST` via `app.run(text)`; `run_shell(...)` via `app.run(text)`; one-shot CLI message path in `main(...)` via `app.run(message)`.
- **Input standing consumed:** a caller-supplied Python `str` named `text`, with workspace/session identifiers supplied by the caller. It is treated as user-message material for ledger recording, not interpreted as a question, intent, command, principal, authority grant, or domain observation.
- **Branch condition evaluated:** no runtime decision-authority registry, supplied decision producer, capability standing, authority profile, or route availability is inspected. The handler is a single unconditional boundary after receiving `text`.
- **Events/artifacts produced within the branch:** an `input.user_message` event; a `runtime.decision_authority_unsupported` event causally tied to the input event id; and the `RuntimeResponse` artifact that references the input event id.
- **Exact act performed by the producer:** it records caller-supplied text as an input event, records a system event that this route cannot route Seed runtime movement through LLM/model-produced `Decision` grammar, and returns a bounded unsupported/stopping response instead of invoking a decision producer or router.
- **Best characterization:** mixed but bounded: bounded refusal + stopping result + route-local absence-of-authority report + compatibility tombstone production. It is not faithfully an unsupported-input classification and not a current configuration-wide or Seed-wide authority census.
- **Warrant for the act:** current implementation has no decision producer dependency or branch in `Runtime.__init__`/`handle_user_message`; `__seed_arch__` has empty `routes` and summarizes that user input is recorded and model-produced Decisions are refused as Seed authority; `build_local_app(...)` constructs `Runtime(ledger, projector)` without decision authority.
- **Stronger standings explicitly refused:** no interpretation, question formation, decision composition, tool routing, state patch, execution, current consumer reliance, global authority absence, or constitutional impossibility of free text is established.

## Handler branch recovery

Current handler structure:

```text
available text from caller
↓
Runtime.handle_user_message(...)
├─ append input.user_message event with payload.text and actor="user"
├─ append runtime.decision_authority_unsupported event with reason, removed_boundary,
│  actor="system", and causation_id=input_event.id
└─ return RuntimeResponse(kind="unsupported", message=static message,
   payload.reason="model_decision_authority_excised",
   payload.input_event_id=input_event.id)
```

There is no evidenced decision-authority configuration inspection, no registry lookup, no supplied model/decision dependency, no route-availability computation, no state projection despite a retained `projector` field, no interpretation, and no question formation in the handler.

## Event and response sibling/causal relations

- `input.user_message`: produced by `Runtime.handle_user_message`; caused by the caller-supplied `text`; identity is the appended event id; standing established is only that the ledger accepted an event recording text under actor label `user` in a workspace/session. It does not establish verified identity, input truth, interpretation, addressability beyond event identity, question formation, operator authority, or external occurrence independently from the append.
- `runtime.decision_authority_unsupported`: produced by the same handler; cause/reference is `causation_id=input_event.id`; standing established is a system record that the branch recorded unsupported decision authority for this input event. It does not consume the first event to compute meaning; it records the same branch result with a causal reference.
- `RuntimeResponse`: produced by the same handler after the events; it references `input_event.id` in `payload.input_event_id`. It is not derived by consuming event contents; it is a sibling output of the branch with a provenance/audit reference to the input event identity.

Actual relation: events and response are sibling outputs of one handler branch; the second event and response both reference the input event id. No current consumer is evidenced that resolves or verifies `payload.input_event_id`.

## Current non-test producer paths

Evidenced current non-test executable paths that produce the response:

1. `SeedAPI.post_user_message(...) -> Runtime.handle_user_message(...) -> RuntimeResponse`.
2. `LocalSeedApp.run(text) -> Runtime.handle_user_message(...) -> to_plain(response)`.
3. HTTP local app: `run_http(...).Handler.do_POST -> app.run(text) -> Runtime.handle_user_message(...) -> JSON body`.
4. Interactive local shell: `run_shell(...) -> app.run(text) -> format_cli_output(...)`.
5. One-shot local CLI message path: `main(argv) -> build_local_app(...) -> app.run(message) -> format_cli_output(...)`.

No separate production path was found that directly constructs this `RuntimeResponse` outside `Runtime.handle_user_message(...)`.

## Possible consumers

Possible consumers identified from signatures, tests, docs, and production references include tests, API methods, CLI formatting helpers, HTTP serialization, shell printing, and one-shot CLI printing. Tests and docs are testimony only. Production possible consumers became current consumers only where the produced instance or its serialized representation is handed to them in executable non-test code.

## Current non-test consumers

- **`SeedAPI.post_user_message(...)`:** receives the exact produced `RuntimeResponse` from `Runtime.handle_user_message(...)` and returns the same instance to its caller. It reads no fields and does not serialize, render, or branch on the fields. Standing inferred: API shell pass-through only.
- **`LocalSeedApp.run(text)`:** receives the exact produced `RuntimeResponse`, serializes it with `to_plain(response)`, and returns a dict containing `response` and all workspace events. Fields are not individually inspected before serialization. Standing inferred: transport representation of the bounded runtime result plus ledger snapshot.
- **HTTP local adapter `run_http(...).Handler.do_POST`:** obtains `app.run(text)` output and serializes the returned dict to JSON. It does not inspect `kind`, `message`, `payload.reason`, or `payload.input_event_id` from the response. Standing inferred: JSON transport representation.
- **`format_response_summary(result)`:** consumes the serialized response dict from `LocalSeedApp.run`; reads `message`, `payload`, `payload.output`, `kind`, and `payload.recommendations`. For the unsupported response, it prints `message` because present; it does not read `reason` or `input_event_id`, and does not branch on `kind` except fallback when `message` is empty.
- **`format_cli_output(...)`:** consumes the result dict by calling `format_response_summary(result)` and may append serialized events when requested. It does not strengthen unsupported standing.
- **`run_shell(...)`:** receives `app.run(text)` dict and prints `format_cli_output(...)`; it communicates presentation material but does not prove operator receipt or reliance.
- **One-shot CLI path in `main(...)`:** receives `app.run(message)` dict and prints `format_cli_output(...)`; same limits as shell.

## Consumer-local field reliance

- `kind`: currently serialized by `LocalSeedApp.run` and returned by API pass-through; CLI summary reads it only as a fallback when `message` is absent. For the target response, no current production consumer branches on `kind="unsupported"`.
- `message`: CLI summary reads and prints it; HTTP serialization returns it as JSON; API pass-through returns it in the object.
- `payload`: CLI summary reads the payload dict for generic optional fields `output` and `recommendations`; unsupported-specific `reason` and `input_event_id` are not read by current production consumers found.
- `reason`: serialized but not production-branch-consumed or rendered by default CLI summary.
- `input_event_id`: serialized but not production-resolved, verified, joined, or rendered by default CLI summary.

## Active-road classification

**Active.** A current non-test executable call path produces the `RuntimeResponse` and passes the produced instance or serialized representation to current non-test consumers: `LocalSeedApp.run` serializes it, HTTP returns the serialized dict as JSON, and CLI/shell paths render `response.message`. `SeedAPI.post_user_message` also passes through the exact instance. The classification is about executable paths only, not actual occurrence, operator receipt, understanding, acceptance, or reliance.

## Response-assertion cross-examination

Tested assertion: `No Seed-owned runtime decision authority is configured for free-text input.`

- **Current repository condition warranting it:** this handler has no decision-authority dependency, no configured producer, no registry lookup, no route branch, and `__seed_arch__["routes"]` is empty while its summary says it refuses model-produced Decisions as Seed authority.
- **Configuration inspected by `Runtime`:** not evidenced. The handler does not inspect a configuration, registry, supplied dependency, capability standing, authority profile, or route availability.
- **What the handler establishes:** this exact runtime input boundary records input and does not invoke decision authority for free-text routing.
- **What it does not establish:** no Seed-owned decision authority exists anywhere; no authority is constitutionally possible; free text is inadmissible; input itself is unsupported; another route could not have Seed-owned decision authority.
- **Derived from current state or static:** static response string, warranted only by route-local implementation shape, not by a current configuration-wide judgment.
- **Could remain unchanged if another Seed-owned decision authority existed elsewhere:** yes. Because the handler does not inspect other components or a registry, the string could remain unchanged even if another Seed-owned decision authority were implemented elsewhere.

## Unsupported classification recovery

`kind="unsupported"` most faithfully classifies the response outcome / route capability-authority condition at this handler boundary: no supported continuation from free-text input into Seed-owned runtime decision routing occurs here. It does not classify the supplied material itself as unsupported, does not classify its representation as inadmissible, does not classify an interpretation as false, and does not prove question formation or execution failure. It is also compatibility-facing because the reason preserves the prior/excised model-decision vocabulary.

## Historical reason-string cross-examination

`payload.reason="model_decision_authority_excised"` preserves a compact compatibility/historical tombstone label: the unsupported result is attributed to removal/excision of model-decision authority. Current implementation and contemporary reports testify that an earlier `DecisionProducer.decide -> Runtime._route` corridor was removed/replaced, and the current event payload names `removed_boundary` with that exact corridor. This operation did not reopen broad history. The independently warranted current fact is route-local absence in this handler; the historical excision claim is described and partially corroborated by targeted current/historical repository testimony, but the reason string alone is not proof of prior activity, removal cause, or current causation.

## Fidelity classification

**Mixed boundary: faithful route-local refusal/stopping result with stale or over-broad static wording risk; no active downstream Fidelity crossing evidenced.**

The producer has warrant for standing S: this handler records input and refuses/stops rather than routing free text through model-produced decision authority. The `RuntimeResponse` mostly preserves S as an unsupported outcome with a message and input-event reference. Current consumers serialize or render the message but do not inspect `reason` or `input_event_id` and do not branch into stronger operational standing. The message text is stronger than the handler's inspection if read Seed-wide or configuration-wide; however, no current consumer was found that strengthens it beyond presentation/transport. Therefore the boundary is representationally asymmetric but not an evidenced Fidelity crossing.

## Current assertions actually warranted

- `Runtime.handle_user_message(...)` is callable and returns a `RuntimeResponse`.
- The handler appends `input.user_message` and `runtime.decision_authority_unsupported` events before returning.
- The second event has `causation_id` equal to the input event id.
- The returned response has `kind="unsupported"`, the static message, `payload.reason="model_decision_authority_excised"`, and `payload.input_event_id` equal to the input event id.
- `LocalSeedApp.run`, local HTTP, local shell, one-shot CLI, and `SeedAPI.post_user_message` provide current non-test handoff/consumer paths.
- The CLI summary renders the response message when present.

## Historical assertions actually warranted

- Current event payload names `removed_boundary="DecisionProducer.decide -> Runtime._route"`.
- Current and historical repository reports describe an internal model-decision authority excision campaign and state that the old routing runtime was replaced by an input boundary returning the unsupported response.
- This is targeted historical testimony, not a full historical proof of active prior road, exact cause, or universal constitutional explanation.

## Stronger or stale assertions actually evidenced

- The message's surface wording can be read as configuration-wide or Seed-wide: `No Seed-owned runtime decision authority is configured for free-text input.` The implementation only warrants route-local absence from this handler because it performs no global inspection.
- The reason string is stale/historical vocabulary in a current response. It is useful as a compatibility tombstone but does not itself establish historical fact or current cause.
- The event reason says LLM/model-produced Decisions are external grammar and cannot route Seed runtime movement. That is current branch testimony; it does not prove all possible non-model free-text decision authority is absent.

## Representational asymmetries that are not crossings

- Static message may over-suggest global configuration absence, but no consumer was found that relies on it as global authority standing.
- `kind="unsupported"` may invite unsupported-input reading, but current consumers do not branch that way.
- `input_event_id` may look like proof or causation, but no consumer resolves it; it functions as a reference/provenance/audit pointer.
- Event ordering may look pipeline-like, but the response and events are sibling outputs of one branch, with references rather than evidenced event-content consumption.

## Smallest possible repair class, if any

No implementation repair is warranted by this report-only operation because no active downstream Fidelity crossing is evidenced. If a future repair were requested, the smallest class would be wording/documentation clarification that the message is route-local/static and compatibility-facing, not a runtime-wide authority census. This operation does not implement that repair.

## Remaining Unknowns

- Whether an external web framework adapter outside this repository calls `SeedAPI.post_user_message` and how it renders the returned object: Unknown.
- Whether any operator receives, understands, accepts, or relies on CLI/HTTP output during an actual run: Unknown.
- Full historical proof of prior active `DecisionProducer.decide -> Runtime._route` operation and exact removal causation: Unknown in this bounded inquiry.
- Whether Seed-owned decision authority exists elsewhere in a form not reached by this handler: not established by this handler; repository-wide global absence was not proven.

## Lawful stopping point

The operation stops at reporting the current executable road and its Fidelity standing. It must not change `RuntimeResponse`, rename `unsupported`, alter event names, remove or rewrite the tombstone, wire interpretation or question formation into `Runtime`, add a conversation loop, add decision authority, add generic ingress, or design a Null exit.

## Final direct answers

1. **Road classification:** Active.
2. **Current non-test entrypoint producing it:** `Runtime.handle_user_message(...)`; reached by `SeedAPI.post_user_message(...)`, `LocalSeedApp.run(...)`, local HTTP POST, shell, and one-shot CLI paths.
3. **Exact producer act:** record the caller text as `input.user_message`, record `runtime.decision_authority_unsupported` causally referencing that event, and return a bounded unsupported/stopping `RuntimeResponse` without invoking decision authority.
4. **Standing preserved by `RuntimeResponse`:** route-local unsupported/stopping/refusal outcome for this free-text handler, plus a reference to the input event identity.
5. **What `kind="unsupported"` classifies:** response outcome / route capability-authority condition, not the input itself.
6. **Current condition warranting the message:** this handler has no decision producer, no routes, no decision-authority inspection, and unconditionally returns the unsupported response after recording events.
7. **Message scope:** static and route-local as warranted; configuration-wide or Seed-wide is not established.
8. **Standing preserved by `model_decision_authority_excised`:** compatibility/historical tombstone testimony that the unsupported result is associated with excised model-decision authority.
9. **Historical excision independently evidenced:** partially by targeted current/historical repository testimony and `removed_boundary` naming; not fully proven by the reason string alone.
10. **`input_event_id` contribution:** event identity/provenance/audit reference; not independent proof, verified occurrence, or consumed event contents.
11. **Event/response relation:** sibling outputs of one branch; the second event and response reference the input event id.
12. **Current non-test consumers:** `SeedAPI.post_user_message`, `LocalSeedApp.run`, local HTTP JSON writer, CLI/shell `format_cli_output`/`format_response_summary`, and their printing/serialization paths.
13. **Consumer strengthening:** not evidenced.
14. **Boundary classification:** mixed boundary: faithful route-local refusal/stopping result with stale compatibility tombstone vocabulary; no Fidelity crossing evidenced.
15. **Repair warranted:** no implementation repair warranted in this operation.
16. **Where to stop:** at the report; do not amend runtime, response shape, events, CLI/API behavior, tests, Book clauses, or wiring.

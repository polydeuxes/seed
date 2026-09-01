# Seed-Native Evidence Acquisition Topology Audit 001

## 1. Bounded question

When Seed lacks evidence needed to continue a bounded inquiry, what repository-backed topology currently governs recognition of that need, capability resolution, authorization, execution, result observation, and renewed reasoning?

This audit asks a topology and ownership question, not a naming question. It treats the inherited `request_tool` / `call_tool` path as evidence to inspect, not as constitutional authority.

## 2. Orientation warning

Clean local ownership does not prove correct Seed-native orientation.

The current implementation has many well-separated owners: decision validation, capability need recording, capability resolution, registered operation cataloging, registered operation validation, policy authorization, execution, durable event recording, and post-execution evidence observation. The important audit question is whether these owners are connected by a Seed-native path that begins with evidence insufficiency in a bounded inquiry and ends with admitted evidence and renewed inquiry movement.

The strongest warning from implementation evidence is that the canonical runtime still begins by asking a `DecisionProducer` for one structured `Decision`, records that proposal as `model.decision.proposed`, and then routes `request_tool` and `call_tool` branches from that model-facing artifact. That makes a substantial portion of the evidence-acquisition path visible only after LLM-shaped output exists.

## 3. Repositories and surfaces inspected

Repository root: `/workspace/seed`.

Implementation surfaces inspected directly:

- `seed_runtime/runtime.py`
- `seed_runtime/decisions.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/tool_intent.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/registry.py`
- `seed_runtime/execution.py`
- `seed_runtime/fact_extraction.py`
- `seed_runtime/evidence.py`
- `seed_runtime/state.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/models.py`

Tests inspected directly:

- `tests/test_runtime_loop.py`
- `tests/test_tool_needs.py`
- `tests/test_execution.py`
- `tests/test_fact_extraction.py`
- `tests/test_inquiry_orientation.py`
- `tests/test_question_surface_inventory.py`

Prior testimony sampled and verified against implementation rather than accepted as authority:

- `IMPLEMENTATION.md`
- `implementation_promotion_grammar_recovery_investigation.md`
- `constitutional_permission_bridge_investigation.md`
- `constitutional_constrained_movement_reconciliation.md`
- `constitutional_absence_of_evidence_boundary_investigation.md`
- `inquiry_artifacts.py` as implementation-backed artifact visibility testimony

## 4. Independent neighborhood testimonies

### 4.1 Inquiry and question formation

- **Producer:** `Runtime.handle_user_message` records `input.user_message`; the model-facing `DecisionProducer` then produces a `Decision` from a composed packet.
- **Artifact:** `input.user_message`, `DecisionInputPacket`, and model-produced `Decision`.
- **Consumer:** `DecisionValidator`, `ToolIntentGuard`, and `Runtime._route`.
- **Owned responsibility:** Runtime orchestration of already-formed decisions; recording user input and proposed model decision; routing validated branches.
- **Refused responsibility:** It does not independently decide that evidence is insufficient, formulate an evidence need, or resume an inquiry after new evidence arrives.
- **Triggering input:** A user message.
- **Emitted output:** Runtime response kinds such as `answer`, `question`, `tool_need`, `tool_result`, `refusal`, and ledger events.
- **Mutation behavior:** Appends events to the ledger.
- **Provenance preserved:** The proposed decision event is caused by the user input event; later routed events use the decision event as causation.
- **Relevant tests:** `tests/test_runtime_loop.py` proves routes for answer, question, request_tool, call_tool, refusal, invalid decisions, and tool result extraction.
- **Strongest counterevidence:** The runtime can route `ask_question` and `refuse`, so not every inquiry pressure becomes a tool call. However, the actual evidence-need and tool-call branches still originate as `Decision.kind` values.

### 4.2 Inquiry orientation and work recovery

- **Producer:** `record_inquiry_note` preserves operator prose outside the event ledger; `build_inquiry_orientation` composes a read-only orientation view.
- **Artifact:** `InquiryNoteRecord`, `InquiryOrientationView`, and local composition artifacts such as `_InquiryOrientationEvidence` and `_InquiryOrientationAnswer`.
- **Consumer:** CLI/reporting surfaces and tests that inspect orientation material.
- **Owned responsibility:** Read-only lexical orientation over already projected state and source navigation.
- **Refused responsibility:** It explicitly does not create facts, goals, tool needs, decisions, proposals, plans, or executions.
- **Triggering input:** Operator-recorded inquiry note or selected note.
- **Emitted output:** Read-only related-material view with uncertainty and authority boundary.
- **Mutation behavior:** Note recording writes isolated JSONL probe storage; orientation rendering does not mutate the event ledger or projected state.
- **Provenance preserved:** Raw note, note id, timestamp, source, and support strings for related material.
- **Relevant tests:** `tests/test_inquiry_orientation.py` verifies no facts or tool needs are created and verifies evidence/selection/answer composition boundaries.
- **Strongest counterevidence:** Orientation has local artifacts named evidence and answer, but they are bounded to orientation rendering and explicitly not generalized inquiry movement or evidence acquisition.

### 4.3 Capability need and capability resolution

- **Producer:** `ToolNeedService.create_from_decision` consumes a model `Decision(kind="request_tool")` and creates a `ToolNeed`; `ToolNeedService.resolve_capability` consumes that `ToolNeed` plus catalog/registry inputs.
- **Artifact:** `ToolNeed` and capability resolution payload containing `known_capability`, `registered_operations`, `provider_recommendations`, and `handoff_candidates`.
- **Consumer:** Runtime `request_tool` branch and projected `State.open_tool_needs`.
- **Owned responsibility:** Capability-gap creation from request_tool decisions and read-only capability resolution that separates catalog recommendations from registry operation candidates.
- **Refused responsibility:** It does not execute, authorize, create pending actions, mutate registry/catalog state, or select a final operation.
- **Triggering input:** A validated `request_tool` decision. No repository evidence showed this producer being triggered directly by a Seed-native evidence sufficiency evaluation.
- **Emitted output:** `tool_need.created`, optional `tool_need.status_changed`, and response payload metadata.
- **Mutation behavior:** Appends tool-need events; resolution itself is read-only.
- **Provenance preserved:** `ToolNeed.requested_by_event_id` links to the model decision event.
- **Relevant tests:** `tests/test_tool_needs.py` proves deduplicated need creation; `tests/test_runtime_loop.py` proves request_tool records and projects an open need.
- **Strongest counterevidence:** The service docstring and architecture metadata already describe capability-gap creation and capability resolution as a Seed service, and its resolution method separates registered operation candidates from provider/handoff metadata. But the creation entry point remains model-decision-shaped.

### 4.4 Operation or tool registration

- **Producer:** Toolkit manifests loaded by `ToolRegistry.load_manifest` / `toolkit_from_manifest`.
- **Artifact:** `ToolSpec` inside an in-memory registered operation index; `Toolkit` metadata.
- **Consumer:** Decision input composition, validation, capability resolution, policy service, and executor.
- **Owned responsibility:** Registered operation cataloging, lookup, listing, and capability mapping.
- **Refused responsibility:** It does not authorize execution, validate a particular call, execute, observe results, or promote evidence.
- **Triggering input:** Manifest load or explicit toolkit registration.
- **Emitted output:** Registered `ToolSpec` lookup/list results.
- **Mutation behavior:** In-memory registry mutation only; not event-ledger mutation.
- **Provenance preserved:** Toolkit id/name/source/status and tool metadata from manifest.
- **Relevant tests:** Runtime and execution tests load `toolkits/core/echo/toolkit.yaml`; registry/toolkit tests cover registration behavior.
- **Strongest counterevidence:** The registry names entries "tools" and filters `model_visible`, which is LLM-facing vocabulary, but its `ToolSpec` also acts as the registered operation contract for execution.

### 4.5 Operation validation

- **Producer:** `ToolValidationService` and `ToolExecutionPolicyService._validate_registered_operation_call`.
- **Artifact:** `OperationSelectionResult`, `ToolValidationResult`, and `RegisteredOperationValidationResult`.
- **Consumer:** `DecisionValidator` for `call_tool`; `ToolExecutionPolicyService` before policy authorization; `ToolExecutor` for failures.
- **Owned responsibility:** Existence lookup, registered status, input schema validation, output schema validation, and explicit operation-selection boundary for a named operation.
- **Refused responsibility:** It does not choose among capabilities or providers; it starts from an already-selected operation name and does not authorize policy or execute.
- **Triggering input:** A `call_tool` decision name/arguments or executor call.
- **Emitted output:** Validation result or errors.
- **Mutation behavior:** None.
- **Provenance preserved:** Error phase is preserved by policy service and executor failure events.
- **Relevant tests:** `tests/test_execution.py` verifies invalid input fails before execution and records `phase=input_validation`; tool validation tests cover validation.
- **Strongest counterevidence:** `DecisionValidator._validate_tool_call` performs input validation as part of model-decision validation, so operation validation appears both as a model-decision check and as execution-path protection.

### 4.6 Policy authorization

- **Producer:** `ToolExecutionPolicyService` using `PolicyGate`.
- **Artifact:** `ToolExecutionPolicyResult` containing validated tool, validation result, `PolicyDecision`, `allowed_to_execute`, and phase/error.
- **Consumer:** `ToolExecutor.execute`.
- **Owned responsibility:** Authorize a validated registered operation call for execution after contract validation.
- **Refused responsibility:** It does not execute, append events, create pending actions, collapse non-allow outcomes, or create capability needs.
- **Triggering input:** An executor or caller asks to evaluate tool name and arguments against projected state/scope.
- **Emitted output:** Combined validation+policy compatibility result.
- **Mutation behavior:** None; state projection may be read lazily after validation succeeds.
- **Provenance preserved:** Policy decision carries action, outcome, reason, risk class, and optional approval id.
- **Relevant tests:** `tests/test_tool_execution_policy.py` and `tests/test_execution.py` verify validation-before-policy and block/approval behavior.
- **Strongest counterevidence:** The compatibility result combines validation and policy in one object, but the implementation has explicit internal artifacts for validation and authorization boundaries.

### 4.7 Execution

- **Producer:** `ToolExecutor.execute` and `_execute_allowed_tool_call`.
- **Artifact:** `ToolCallResult`, `tool.call.started`, `tool.call.completed`, `tool.call.failed`, `tool.policy.blocked`, `tool.approval.required`, and possible pending action.
- **Consumer:** Runtime call_tool branch, event ledger/projector, fact extraction service, and callers receiving `ToolCallResult`.
- **Owned responsibility:** Execute only registered operations after validation and policy checks; record started/completed/failed; invoke registered callable; validate output.
- **Refused responsibility:** It does not formulate evidence needs, choose operations from a capability gap, or decide inquiry continuation after extraction.
- **Triggering input:** Direct executor call or `Runtime._route` for `Decision(kind="call_tool")`.
- **Emitted output:** `ToolCallResult` and durable execution events.
- **Mutation behavior:** Event-ledger writes; registered callable may have external effects depending on policy/action, but execution path distinguishes policy and pending actions.
- **Provenance preserved:** `causation_id` and optional `correlation_id` flow into started/completed/failed and pending-action events.
- **Relevant tests:** `tests/test_execution.py` proves successful execution, validation failure before execution, policy block before execution, output-schema failure, completion event, and recording-before-extraction.
- **Strongest counterevidence:** Direct `ToolExecutor.execute` can be called without an LLM, proving the executor substrate is not intrinsically model-bound. But the canonical runtime route into it is `call_tool` from a model decision.

### 4.8 Event recording

- **Producer:** `EventLedger.append` via runtime, tool-need service, executor, pending action service, and fact extraction service.
- **Artifact:** `Event` with kind, workspace, actor, timestamp, payload, session, causation, and correlation ids.
- **Consumer:** `StateProjector`, tests, diagnostics, context composition, and reports.
- **Owned responsibility:** Durable append-only recording of runtime events.
- **Refused responsibility:** It does not interpret whether an event is evidence, fact, authorized execution, or lawful inquiry movement.
- **Triggering input:** Service append calls.
- **Emitted output:** `Event` object.
- **Mutation behavior:** Ledger append.
- **Provenance preserved:** Event metadata and causation/correlation fields.
- **Relevant tests:** Runtime, execution, and fact extraction tests assert exact event sequences.
- **Strongest counterevidence:** Event correlation exists mechanically, but there is no tested end-to-end correlation that binds original inquiry to evidence need to execution result to resumed inquiry.

### 4.9 Post-execution extraction

- **Producer:** `FactExtractionService.observe_tool_result` called by `ToolExecutor._extract_post_execution_knowledge` after completed execution is recorded.
- **Artifact:** `FactExtractionResult` and `evidence.observed` event containing `Evidence(kind="tool.output")`.
- **Consumer:** Event ledger and state projector; decision input composer can include projected evidence in later model context.
- **Owned responsibility:** Turn successful tool result payloads into evidence observations.
- **Refused responsibility:** It intentionally does not infer facts unless future explicit mapping is added.
- **Triggering input:** Completed `tool.call.completed` or legacy `tool.result` event.
- **Emitted output:** `evidence.observed` event.
- **Mutation behavior:** Appends an evidence event; does not create facts.
- **Provenance preserved:** Evidence source includes tool name; evidence observed_at equals result timestamp; evidence event causation points to completed event and preserves correlation id.
- **Relevant tests:** `tests/test_fact_extraction.py` verifies completed tool calls become evidence, failed calls are rejected, and projected state/context include evidence but no facts.
- **Strongest counterevidence:** The module name says fact extraction, but behavior is evidence observation only; that naming may obscure the boundary.

### 4.10 Evidence/fact ingestion

- **Producer:** State projector consumes `evidence.observed` and fact events from ledger; observation ingestors elsewhere create facts from observations.
- **Artifact:** `State.evidence`, `State.facts`, `State.observed_facts`, `State.inferred_facts`, fact supports, conflicts, and stale recommendations.
- **Consumer:** Decision input composition, read-model views, source navigation, capability inventory, and diagnostics.
- **Owned responsibility:** Projection of evidence and facts from events; deterministic inference over fact sets.
- **Refused responsibility:** Projection does not decide that evidence satisfies an inquiry, does not resume the original question, and does not promote generic tool output into facts.
- **Triggering input:** Event replay.
- **Emitted output:** Projected state.
- **Mutation behavior:** In-memory projection state; no new event writes during projection.
- **Provenance preserved:** Evidence ids, fact evidence ids/supports, event-derived source information.
- **Relevant tests:** `tests/test_fact_extraction.py` asserts projected evidence with empty facts after tool output; many fact/evidence tests cover fact supports.
- **Strongest counterevidence:** Later `DecisionInputComposer` can include projected evidence in future context, but there is no inquiry-bound admission/resumption artifact.

### 4.11 Answer or inquiry continuation

- **Producer:** Model-produced `Decision(kind="answer" | "ask_question" | "refuse")`, routed by runtime.
- **Artifact:** `response.answer`, `response.question`, or `response.refusal` event and `RuntimeResponse`.
- **Consumer:** User/interface and future projected state/context.
- **Owned responsibility:** Record model-proposed answers/questions/refusals after validation.
- **Refused responsibility:** It does not verify that newly observed evidence answers the prior inquiry or that inquiry movement is lawful.
- **Triggering input:** User message plus model decision.
- **Emitted output:** Response event and runtime response.
- **Mutation behavior:** Appends response events.
- **Provenance preserved:** Response events point to the model decision event.
- **Relevant tests:** `tests/test_runtime_loop.py` proves answer/question/refusal routes.
- **Strongest counterevidence:** The model can receive prior projected evidence on a later turn, but this is not an implementation-backed resumed bounded inquiry chain.

## 5. Producer / artifact / consumer table

| Responsibility | Producer | Artifact | Consumer | Current trigger | Boundary finding |
|---|---|---|---|---|---|
| User/inquiry input recording | `Runtime.handle_user_message` | `input.user_message` | Context composer, model decision producer | User message | Seed records input, but does not derive evidence need from insufficiency. |
| Model decision proposal | `DecisionProducer` | `Decision`, `model.decision.proposed` | Validator, intent guard, runtime router | Runtime asks model | LLM-facing decision is the canonical branch point. |
| Evidence insufficiency | No direct general owner located | None direct; closest is `Decision(kind="request_tool")` | ToolNeedService after validation | Model-produced request | Translated immediately into tool need vocabulary. |
| Missing capability | `ToolNeedService.create_from_decision` | `ToolNeed`, `tool_need.created` | State projector, capability resolution | Validated `request_tool` decision | Missing capability exists, but not as an inquiry-sufficiency artifact. |
| Capability resolution | `ToolNeedService.resolve_capability` | Resolution payload | Runtime response/user/model context later | Existing `ToolNeed` | Distinct from execution and operation selection. |
| Operation registration | `ToolRegistry` | `ToolSpec` / `Toolkit` | Validation, executor, context composer | Manifest load | Registered operation substrate exists. |
| Operation selection | `ToolValidationService.select_operation` | `OperationSelectionResult` | Validation/policy | Already selected name | Distinct from capability resolution, but not a capability-to-operation chooser. |
| Operation contract validation | `ToolExecutionPolicyService._validate_registered_operation_call` | `RegisteredOperationValidationResult` | Policy authorization | Executor evaluation | Distinct from authorization. |
| Authorization | `ToolExecutionPolicyService` / `PolicyGate` | `ToolExecutionPolicyResult`, `PolicyDecision` | ToolExecutor | Valid registered operation | Distinct from execution. |
| Execution | `ToolExecutor` | `ToolCallResult`, tool call events | Runtime, ledger, extraction | Authorized operation | Distinct from recording/extraction internally. |
| Completed execution record | `ToolExecutor._record_completed_tool_call` | `tool.call.completed` | FactExtractionService, StateProjector | Successful operation output | Records result, not yet evidence admission. |
| Result observation | `FactExtractionService.observe_tool_result` | `evidence.observed`, `Evidence` | StateProjector, context composer | Completed event | Observes output as evidence, not fact. |
| Fact promotion | Observation/fact ingestors and projector | `Fact` and supports | State read models | Explicit fact events/ingestion | Generic tool output is not promoted. |
| Renewed inquiry | No direct owner located | None direct | N/A | N/A | Disconnected from evidence observation. |
| Answer/lawful stop | Runtime route from model decision | `response.answer`, `response.question`, `response.refusal` | User/future context | Model decision | Exists as model-routed response, not as inquiry-sufficiency adjudication. |

## 6. Current implementation topology

Implementation-backed current path:

```text
User message
  -> input.user_message event
  -> DecisionInputPacket composed from projected state and visible tools/evidence
  -> DecisionProducer returns model-shaped Decision
  -> model.decision.proposed event
  -> DecisionValidator and ToolIntentGuard
  -> Runtime route by Decision.kind
```

For `request_tool`:

```text
Decision(kind=request_tool)
  -> ToolNeedService.create_from_decision
  -> tool_need.created event
  -> ToolRecommendationService.recommend_for
  -> ToolNeedService.resolve_capability
  -> response payload with ToolNeed, provider recommendations, registered operation candidates, handoff candidates
  -> projected open_tool_needs
```

For `call_tool`:

```text
Decision(kind=call_tool, tool_name, tool_arguments)
  -> ToolValidationService / ToolExecutionPolicyService validates registered operation contract
  -> PolicyGate authorization
  -> if blocked: policy event and no execution
  -> if confirmation/approval required: policy event + pending_action.created
  -> if allowed: tool.call.started
  -> registered callable invocation
  -> output schema validation
  -> tool.call.completed
  -> FactExtractionService.observe_tool_result
  -> evidence.observed
  -> projected State.evidence
```

For answer/continuation:

```text
Later user message or current route
  -> DecisionProducer may see projected evidence in context
  -> model-shaped answer/question/refusal
  -> response.answer / response.question / response.refusal
```

The last transition is not a preserved resumed-inquiry bridge. It is another model-decision cycle over projected state.

## 7. LLM-oriented topology

The LLM-facing topology currently visible is:

```text
DecisionInputPacket with visible tools/evidence
  -> LLM/model proposes exactly one Decision
  -> request_tool means missing capability request
  -> call_tool means selected registered operation call
  -> answer/question/refuse means response movement
```

LLM participation by artifact:

| Artifact/route | Does LLM originate constitutional need? | Express bounded need? | Select operation? | Request execution? | Authorize execution? | Interpret results? | Promote evidence/facts? | Could responsibility operate without LLM? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `Decision(kind=request_tool)` | Currently yes in runtime route; constitutionally not proven | Possibly, but no separate need artifact precedes it | No | No | No | No | No | ToolNeedService could, but no direct non-LLM evidence-need producer is wired. |
| `Decision(kind=call_tool)` | No direct evidence need represented | No | Yes, by naming tool | Yes, proposes call | No; policy service authorizes | No | No | ToolExecutor can be called directly with name/args. |
| `Decision(kind=answer)` | No | May answer from context | No | No | No | Yes, as model response | No durable fact promotion | A non-LLM answer composer is not generally present for runtime inquiries. |
| `Decision(kind=ask_question)` | No | May express insufficient user information | No | No | No | N/A | No | A deterministic question former is not visible in canonical runtime. |
| `Decision(kind=refuse)` | No | May express lawful stop/refusal | No | No | No | Yes, as model response | No | Policy can refuse execution separately; inquiry refusal remains model-routed. |
| `ToolIntentGuard` | No | No | Constrains model-selected operation | Blocks mismatched request | No | No | No | Yes; deterministic guard is model-adjacent but not model-dependent. |

Findings:

- The LLM does not authorize execution; policy authorization is repository-owned.
- The LLM does select/request a registered operation in the canonical runtime `call_tool` branch.
- The LLM currently originates the only canonical runtime artifact that becomes a `ToolNeed`.
- The LLM does not promote execution results into evidence; `FactExtractionService` observes tool output as evidence.
- The LLM may later interpret projected evidence if another decision cycle is run, but no repository-backed resumed-inquiry artifact binds that interpretation to the original evidence need.

## 8. Recovered Seed-native topology, if supported

Supported Seed-native substrate can be recovered only as a partial topology:

```text
Registered operation catalog
  -> operation selection by name
  -> operation contract validation
  -> policy authorization
  -> permitted execution
  -> durable execution result
  -> evidence observation from successful result
  -> projected evidence available to later context
```

Supported but disconnected capability side:

```text
ToolNeed
  -> read-only capability resolution
  -> registered operation candidates and non-executable provider/handoff metadata
```

Supported answer/stop side:

```text
model-routed answer/question/refusal events
read-only inquiry orientation views
Unknown / gap visibility in diagnostic and report surfaces
```

Unsupported as a connected Seed-native topology:

```text
Bounded Inquiry
  -> Evidence Sufficiency Evaluation
  -> Evidence Need
  -> Capability Resolution
  -> Candidate Operation
  -> Registered Operation Validation
  -> Policy Authorization
  -> Permitted Execution
  -> Execution Result
  -> Result Observation
  -> Evidence Extraction
  -> Evidence Admission
  -> Resumed Bounded Inquiry
  -> Bounded Answer or Lawful Stop
```

The middle execution spine is implementation-backed. The first three nodes and last three nodes are not connected by repository-backed inquiry artifacts.

## 9. Reusable Seed-native substrate

Reusable substrate that is not inherently LLM-owned:

1. `ToolNeed` as a capability-gap record, provided a future producer can create it from a Seed-native evidence need without lying about provenance.
2. `ToolNeedService.resolve_capability` as read-only capability resolution separating catalog knowledge, provider recommendations, handoff candidates, and registered operation candidates.
3. `ToolRegistry` and `ToolSpec` as registered operation catalog and contract metadata.
4. `ToolValidationService` / `RegisteredOperationValidationResult` as operation-selection and contract-validation boundaries.
5. `ToolExecutionPolicyService` / `PolicyGate` as authorization separate from validation and execution.
6. `ToolExecutor` as execution of already validated/authorized registered operations.
7. Event ledger causation/correlation fields as durable provenance substrate.
8. `FactExtractionService.observe_tool_result` as post-execution evidence observation.
9. `StateProjector` as evidence/fact projection without automatic fact promotion.
10. Inquiry orientation local artifacts as read-only orientation substrate, explicitly not evidence acquisition.

## 10. LLM-only adapters or triggers

- `DecisionProducer` and `DecisionInputPacket` are model-facing runtime adapters.
- `Decision.kind` values are the canonical runtime branch selector.
- `request_tool` is both a model-expressed capability request and the current trigger for Seed `ToolNeed` creation. It is not yet a direct Seed-native evidence-need artifact.
- `call_tool` is a model-proposed operation call in runtime. It is not constitutional authorization; repository policy owns authorization. It is also not just dispatch, because it carries the model-selected operation name and arguments that validation/policy consume.
- `visible_tools` and `model_visible` registry filtering are LLM presentation surfaces over registered operations.
- `ToolIntentGuard` is deterministic but exists to constrain model tool-call intent.

## 11. Disconnected roads

1. **Evidence insufficiency -> evidence need:** No direct artifact was found for "available evidence is insufficient for this bounded inquiry". Closest artifacts are `ask_question`, `request_tool`, read-only orientation uncertainty, diagnostic gaps, and Unknown documentation, but none is a general evidence-need object.
2. **Evidence need -> capability need:** `ToolNeed` can represent a missing capability, but only after a `request_tool` decision or direct service call. No implementation-backed producer translates inquiry evidence insufficiency into a capability need.
3. **Capability resolution -> operation selection:** Resolution lists registered operation candidates, but no owner selects a candidate operation from a capability need. Existing operation selection starts from an already named operation.
4. **Capability need -> lawful refusal preserving unresolved need:** Policy can block execution while preserving policy event/pending action behavior, and tool needs can remain open, but no bridge records refused execution as unresolved evidence need for an inquiry.
5. **Execution evidence -> evidence admission for original inquiry:** Tool output becomes `Evidence`; generic fact promotion is intentionally absent. No owner adjudicates whether evidence satisfies the original inquiry.
6. **Evidence admission -> renewed inquiry:** Later context may include evidence, but no resumed-inquiry artifact correlates original inquiry, evidence need, operation, result, observed evidence, and answer/stop.

## 12. Absent artifacts or owners

Absent or not implementation-visible as general Seed-native owners:

- `EvidenceNeed` or equivalent direct artifact.
- Evidence sufficiency evaluator for a bounded inquiry.
- Capability resolver triggered by inquiry pressure rather than `request_tool` decision.
- Candidate operation selector from capability/evidence need.
- Evidence admission owner that distinguishes observed output from accepted evidence for a specific inquiry.
- Inquiry resumption owner that consumes newly admitted evidence and resumes the prior bounded question.
- Correlation artifact spanning original inquiry -> evidence need -> operation -> execution result -> extracted evidence -> resumed inquiry.

These are absence findings for this topology audit, not implementation warrants to build them now.

## 13. Strongest counterevidence

The strongest evidence for a more positive classification is substantial:

- `ToolNeedService.resolve_capability` already separates registered operation candidates from provider/handoff metadata and refuses execution.
- `ToolExecutionPolicyService` explicitly separates registered operation validation from policy authorization and refuses execution/event/pending-action ownership.
- `ToolExecutor` executes only after validation and policy, records durable result events, and invokes post-execution extraction only after recording.
- `FactExtractionService` observes tool outputs as evidence while refusing generic fact inference.
- `StateProjector` projects `evidence.observed` and facts separately.
- Tests prove validation-before-execution, policy-block-before-execution, completion recording before extraction, evidence projection, no facts from generic tool output, and open tool-need projection.
- Direct executor calls in tests prove execution substrate can operate without an LLM.

This counterevidence prevents classifying the repository as entirely lacking required ownership. The reason it does not prove classification A is that the repository-backed path from bounded inquiry evidence insufficiency to need creation and resumed inquiry remains disconnected/model-triggered.

## 14. Preserved Unknowns

- Whether an uninspected CLI surface outside the sampled files provides a more complete evidence-acquisition bridge. The likely surfaces were searched and no such bridge was found, but this audit did not exhaustively inspect every script and prior report.
- Whether future or experimental docs contain a proposed `EvidenceNeed` grammar. Documents are testimony, not current implementation.
- Whether a specific operational diagnostic can already create a finding that later becomes a capability need. Diagnostic gaps exist, but this audit found no general inquiry-bound road from finding to execution evidence and renewed inquiry.
- Whether a future non-LLM decision producer could use current `Decision` schema as a compatibility adapter while preserving Seed-native need provenance. The substrate permits this possibility, but it is not current topology.

## 15. Primary classification

**B. Seed-native substrate exists but is disconnected.**

The major responsibilities exist independently: capability-gap recording, capability resolution, operation registration, validation, policy authorization, execution, result recording, evidence observation, and projection. However, no lawful bridge connects a bounded inquiry's evidence insufficiency to an evidence need, capability/operation selection, execution evidence admission, and renewed inquiry movement.

Secondary observation: parts of the path are compressed into LLM/tool orientation, especially the current triggers for `ToolNeed` creation and operation call selection. This is serious, but not the primary classification because repository evidence shows substantial Seed-owned substrate once a need or call exists.

## 16. Implementation-warrant decision

No production implementation is warranted in this audit.

Reason:

- The gap is topology-wide and would require designing at least an evidence-need artifact, sufficiency evaluator, capability-to-operation selection boundary, evidence admission owner, and inquiry resumption owner.
- The task explicitly prohibits redesigning the runtime, creating an Eye subsystem, adding operation synthesis, autonomous planning, or a universal evidence-acquisition framework.
- A vocabulary problem alone does not warrant renaming.
- Disconnected topology alone does not warrant wiring.
- Existing tests already prove the local boundaries around validation, policy, execution, and extraction.

Therefore this commit adds only the audit report.

## 17. Exact next bounded question

What is the smallest repository-backed artifact that can represent an unresolved inquiry-specific evidence need without selecting an operation, requesting execution, or changing existing `request_tool` / `call_tool` compatibility behavior?

## 18. Files changed

- Added `seed_native_evidence_acquisition_topology_audit_001.md`.

No fixtures, tests, or production code were modified.

## 19. Tests or probes executed

Commands/probes executed during the audit:

```text
pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' && git status --short
cat AGENTS.md && rg --files seed_runtime scripts tests
sed -n ... seed_runtime/tool_needs.py seed_runtime/tool_intent.py seed_runtime/tool_execution_policy.py seed_runtime/execution.py
sed -n ... seed_runtime/registry.py seed_runtime/tool_validation.py seed_runtime/fact_extraction.py
sed -n ... seed_runtime/runtime.py seed_runtime/decisions.py seed_runtime/inquiry_orientation.py seed_runtime/inquiry_artifacts.py
sed -n ... seed_runtime/models.py seed_runtime/evidence.py seed_runtime/state.py
rg -n 'tool_need|evidence.observed|tool.call|response.answer|open_tool_needs|facts|evidence' ...
sed -n ... tests/test_runtime_loop.py tests/test_execution.py tests/test_fact_extraction.py seed_runtime/state.py
rg --files -g '*.md'
rg -n 'capability.*operation|ToolExecutor|request_tool|call_tool|evidence admission|lawful stop|constitutional sufficiency' -g '*.md' -g '*.py'
```

Programmatic checks run after writing the report:

```text
pytest -q tests/test_runtime_loop.py tests/test_tool_needs.py tests/test_execution.py tests/test_fact_extraction.py tests/test_inquiry_orientation.py
```

## 20. Confidence statement

Confidence is **moderate-high**.

High confidence:

- The execution spine is well separated into registration, validation, authorization, execution, recording, extraction, and projection.
- Generic successful tool output is observed as evidence, not promoted as fact.
- Runtime `request_tool` and `call_tool` branches are currently model-decision-routed.

Moderate confidence:

- No complete Seed-native evidence-acquisition bridge exists. The repository is large and contains many prior audit documents; this audit inspected the likely implementation neighborhoods and representative prior testimony but did not exhaust every document.

Final classification sentence:

Seed-native substrate exists but its evidence-acquisition path is disconnected.

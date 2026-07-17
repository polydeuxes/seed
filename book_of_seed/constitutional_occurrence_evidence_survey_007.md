# Constitutional Occurrence Evidence Survey 007

## Repository state examined

- `git rev-parse HEAD`: `5f090e28d005854c599b31934490ab35c21fb8c5`.
- `git status --short` before survey changes: no output.
- PR 1748 is present in the surveyed checkout as commit `5f090e2 Add uptake standing characterization pass 006 (#1748)`.
- `book_of_seed/uptake_standing_characterization_pass_006.md` exists.

Repository implementation evidence controls the findings below. Prior Book chapters and reports were used only for orientation.

## Districts surveyed

- Selection occurrence: `seed_runtime/examination_work_selection.py::select_examination_work`.
- Establishment occurrence: `seed_runtime/bounded_operator_goal_establishment.py::establish_bounded_operator_goal_from_admitted_interpretation`.
- Execution occurrence: `seed_runtime/execution.py::ToolExecutor.execute` and its allowed-call branch.
- Recording occurrence: `seed_runtime/events.py::EventLedger.append` and execution completion recording.
- Knowledge-extraction occurrence: `seed_runtime/fact_extraction.py::FactExtractionService.observe_tool_result`.

## Examples selected

The selection example uses examination work selection rather than reopening the advancement-family taxonomy because its producer warrant is explicit: a frontier, a policy projection, and a selector handoff must agree before a selected or no-selection artifact is returned. The establishment example uses the admitted-interpretation goal boundary because it checks consumer and purpose identity, selected-candidate identity, applicability, upstream unknowns, and conflicts. The execution example uses the actual registered-tool executor, not proposals. The recording example uses the append-only event ledger plus `_record_completed_tool_call`. The knowledge-extraction example uses the service that turns completed tool result events into evidence observations.

## Cross-district occurrence matrix

| district | responsible act | act subject | producer boundary | producer warrant | result artifact | direct construction possible? | live observer evidence | producer attribution preserved? | event or record produced? | consumer verification available? | what proves occurrence locally? | what remains only testimony? | what remains unproven? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| selection | Apply a policy to a frontier and either select one eligible work item or lawfully produce no selection, unknown, conflict, or invalid. | Examination work item under a policy/frontier relation. | `select_examination_work(frontier, policy, handoff)`. | Handoff identity matches policy; policy references frontier; handoff fields match policy fields; referenced work exists; eligible policy references are frontier-eligible. | `ExaminationWorkSelection`. | Yes: it is a frozen dataclass and can be instantiated with matching-looking fields. | Caller observing successful return knows this boundary returned an artifact after its in-body validations. | Partially: artifact preserves artifact type, selection id, policy/frontier/inquiry references, handoff reference, convention, state, reason, read-only/no-ledger/no-mutation fields; it does not preserve a producer invocation certificate. | No event ledger write; artifact says read-only and `writes_event_ledger=False`. | Consumers can check fields and references but do not prove this exact producer ran unless they observed the call or have an external record. | The live call reaching return after `_validate` and branch selection. | Artifact fields testify that selection state/reason was produced under referenced inputs. | A later consumer cannot distinguish producer return from direct construction solely from the artifact. |
| establishment | Establish or refuse/provisionally establish bounded operator goal orientation from an admitted interpretation. | Bounded operator goal orientation over selected admitted meaning. | `establish_bounded_operator_goal_from_admitted_interpretation(admission, ...)`. | Admission artifact type; consumer and purpose refs; admission/projection/selection identity coherence; applicability; no unknowns/conflicts; selected candidate present. | `BoundedOperatorGoalEstablishment`. | Yes: the dataclass can be directly instantiated with `establishment_state="established"`. | Caller observing successful return knows the establishment boundary validated the admission and constructed the result. | Partially: ingress type/ref, lineage, upstream source/warrant/selection/applicability/admission refs, snapshots, states, reasons, read-only/no-ledger/no-mutation fields survive; producer identity and invocation evidence do not. | No event ledger write by this boundary. | Downstream boundaries can rely on the establishment assertion as an artifact assertion and check fields/lineage; they cannot prove occurrence of the producer without call-context or record evidence. | The live return from this owner after mismatch, unknown, conflict, applicability, and selected-ref tests. | The artifact preserves the assertion and lineage as testimony from the constructed result. | Direct construction can imitate established-looking state; upstream producers are not re-run or proven. |
| execution | Invoke a registered operation after validation and policy allow, then return completed/failed/blocked/approval status. | Registered tool operation and its output or failure/policy outcome. | `ToolExecutor.execute(...)`, especially `_execute_allowed_tool_call`. | Tool validation, state-based policy evaluation, policy allow for execution; registered operation loading and output-schema validation for completion. | `ToolCallResult`. | Yes: `ToolCallResult` is a model with fields that can be constructed. | Caller observing return knows `execute` returned a status; if observing the whole call, it may know the call entered started/completed/failed branches. | Result preserves tool name, status, message, output/error/policy/pending action, and event IDs in payload for some branches; it does not cryptographically prove the callable ran. | Yes for allowed execution: `tool.call.started` and then `tool.call.completed` or `tool.call.failed`; blocked/approval branches record their own policy events. | Ledger events can corroborate that Seed recorded started/completed/failed execution. Output validation proves the returned output met schema, not every external effect. | Invocation plus started-event append; completion branch requires callable return and output validation before completed-event append. | Completed/failed event payloads testify to tool output or error. | External side effects are not necessarily independently verified; a constructed `ToolCallResult` alone does not prove execution. |
| recording | Append a durable in-memory event with kind, actor, payload, workspace, timestamp, causation, and correlation. | Event occurrence/assertion as a ledger entry. | `EventLedger.append(...)` and `_store`. | Event construction with secret-field rejection in `Event`; execution-authorization validation; unique event id in `_store`. | `Event`. | Yes: `Event` can be directly constructed; `append_many` can store pre-built events after validation. | Caller observing returned `Event` from `append` knows recording occurred in this ledger instance. | Event preserves actor, kind, timestamp, payload, session, causation, correlation; it does not preserve the recorder's full call stack or independently verify all payload claims. | Yes: the event is the record. | Later consumers can query ledger by id/workspace and see the record if it remains in that ledger/store. | Successful `_store` of a unique event in the ledger. | Payload claims remain testimony or recorded assertions unless separately verified. | The prior act named by payload/kind may not have happened; the act may happen without recording in other districts. |
| knowledge extraction | Convert a completed tool-result event into an `Evidence` observation event. | Tool output as evidence, not inferred facts. | `FactExtractionService.observe_tool_result(event)`. | Event kind must be `tool.call.completed` or legacy `tool.result`; payload must name tool; ledger append succeeds. | `FactExtractionResult` containing `evidence.observed` event(s). | Yes: result and evidence-like events can be constructed directly. | Caller observing return knows extraction boundary accepted the event and appended evidence. | Evidence preserves source `tool:<name>`, kind `tool.output`, observed_at from source event timestamp, payload output, confidence; evidence event causation points to source event. It does not preserve proof that original tool execution really occurred beyond the source event record. | Yes: appends `evidence.observed`. | Consumers can inspect evidence event and causation id; they can verify extraction occurred if the event is in the ledger. | Source-event kind/tool-name checks plus evidence-event append. | The source event's claim that a tool completed remains recorded testimony unless the execution record is trusted under its own boundary. | Extraction does not infer facts and does not prove external effects. |

## Selection occurrence result

The selection act is the policy-governed choice over a supplied frontier. The exact act occurs when `select_examination_work` validates handoff, policy, and frontier coherence, evaluates the policy kind and sufficiency, and returns an `ExaminationWorkSelection` with a selected, no-selection, unknown, conflict, or invalid-like state. Its warrant is local and explicit: matching projection ids, frontier ids, policy fields, eligible references, prerequisites, no-selection conditions, and frontier eligibility.

The artifact reports the selection state, selected work reference, basis, reason, non-selected eligible work, no-selection reasons, boundary notes, and read-only/no-ledger/no-mutation status. The artifact can be directly constructed. Therefore artifact existence differs from responsible selection occurrence. A live caller may know the boundary returned after validation, but later consumers that only receive the artifact can at most validate represented coherence unless a separate record or testimony of production travels with it. Selection occurrence is not recorded beyond call context in this example.

## Establishment occurrence result

The establishment act is the establishment or refusal of bounded operator goal orientation from an exact admitted interpretation. The subject receiving standing is not the upstream interpretation itself but the downstream bounded operator goal orientation. Prior standing required by this owner is admission-shaped standing: the object must be a `DownstreamInterpretationAdmission`, must name the bounded-goal consumer and purpose, must match projection and selected-candidate identities, must be admitted and applicable, and must have no unknown or conflicting upstream lineage.

The resulting `BoundedOperatorGoalEstablishment` preserves the establishment assertion through `establishment_state`, `establishment_reason`, intended outcome, known/unresolved scope, sufficiency state, lineage, upstream reference groups, admitted meaning snapshot, and read-only/no-ledger/no-mutation fields. It does not preserve producer identity as a verified invocation, and it does not prove upstream producers ran. Direct construction can imitate an established-looking state. Downstream need projections rely on the establishment assertion as represented input, but that reliance is not proof of the establishment producer's occurrence unless the producer call was observed or recorded externally.

Establishment assertion is therefore not merely the presence of a field named `established`. It is the result of this boundary's admission, identity, applicability, unknown, and conflict checks when the boundary actually runs.

## Execution occurrence result

The operational execution boundary is `ToolExecutor.execute`. Before invocation, a caller may know the requested workspace, session, tool name, arguments, scope, and any causation/correlation ids. The executor then evaluates validation and policy using projected state. For allowed calls, `_execute_allowed_tool_call` records `tool.call.started`, invokes the registered callable through `_realize_registered_operation`, validates output schema, records `tool.call.completed`, extracts post-execution evidence, and returns a completed `ToolCallResult`. If the callable raises, it records `tool.call.failed` and returns a failed result. If validation or policy blocks the call, it returns/records the appropriate non-completion branch.

Function return proves that the executor boundary returned a status to the observer. In the completed allowed branch, the combination of started event, callable return, output-schema validation, completed event, and returned result is stronger local occurrence evidence. Result recording preserves a durable execution record, but it still does not independently prove every claimed external effect. A `ToolCallResult` can be constructed without execution; the result artifact alone is not an execution seal.

The required distinctions hold: proposal differs from authorization, authorization differs from invocation, invocation differs from completed execution, and completed execution differs from recorded execution.

## Recording occurrence result

The recording act is ledger append: a new `Event` is constructed and stored under a unique id in append order. Recording asserts that Seed recorded an event of a kind with payload, actor, time, workspace, and causal metadata. For execution completion, `_record_completed_tool_call` records `tool.call.completed` with tool name and output after successful realization and validation.

Recording does not automatically establish the truth of the recorded claim. The recorder consumes payload supplied by the caller or by the execution branch; it validates event storage conditions and some model boundaries, not all external facts represented by payload. Producer attribution that survives recording is actor, kind, causation/correlation/session, timestamp, workspace, and payload contents. Recording can occur for externally constructed events through batch append. Conversely, many read-only selection and establishment acts occur without event-ledger writes. Thus act occurrence differs from recording occurrence; record existence differs from recorded assertion truth.

## Knowledge-extraction occurrence result

The extraction act in `FactExtractionService.observe_tool_result` accepts a completed tool-result event and records its output as evidence. Upstream material is treated as a source event carrying tool output testimony. The new assertion is not a fact; it is an `Evidence` object with source `tool:<name>`, kind `tool.output`, observed timestamp copied from the source event, output payload, and confidence, preserved inside an `evidence.observed` event with causation back to the source event.

Extraction does not prove the original operational act occurred. It establishes only that, under its own warrant, a completed-tool-result-shaped event was converted into evidence. Provenance is represented by source name, evidence kind, observed time, payload, and causation id. It is not independently verified provenance.

## Observer-testimony result

A direct observer of a responsible call may testify to what it witnessed: the boundary was invoked in that context, it returned or raised, and any result/exception visible to the observer. If the observer also observes a ledger append or provider response, it may testify to that observation. For external execution effects, the observer knows only what the boundary and provider response expose unless it independently observes the effect.

Unpreserved observer knowledge has call-context standing only. It does not travel to later consumers unless recorded as testimony, event, evidence, report, or another durable artifact. Preserved testimony remains testimony unless a later boundary establishes a stronger claim.

## Artifact-provenance result

Current artifacts preserve mixed provenance, not a universal occurrence seal:

- Selection artifacts preserve stable selection identity, input references, policy/handoff references, state, reason, and boundary flags.
- Establishment artifacts preserve ingress references, lineage, upstream source/warrant/selection/applicability/admission refs, snapshots, state, reasons, and boundary flags.
- Execution results preserve status, tool name, output/error/policy/pending action, and sometimes event ids.
- Events preserve id, kind, workspace, actor, timestamp, payload, session, causation, and correlation.
- Evidence preserves evidence id, source, kind, observed_at, payload, confidence, and workspace.

These are represented provenance fields. They are not automatically verified provenance. Stable identifiers make comparison and replay easier, but they are not occurrence seals.

## Recording requirement result

Event recording is not required for every constitutional occurrence. The selection and establishment examples are read-only, non-mutating, and explicitly do not write the event ledger while still performing bounded constitutional acts when their responsible boundaries run. Recording is required only for occurrence claims that are meant to travel through ledger history or later evidence extraction. Recording is neither universal occurrence nor universal truth.

## Occurrence layers supported

Repository evidence supports several separable occurrence claims, but not as a universal stage model:

- Boundary invocation occurred: local to an observer or reflected indirectly by returned/recorded outputs.
- Assertion-bearing branch occurred: knowable to an observer of branch output or exception; sometimes inferable from result fields, but direct construction weakens later proof.
- Result construction occurred: visible to the caller receiving the object; later consumers see only object existence unless production evidence travels.
- External effect occurred: uniquely burdened by provider/tool behavior and not guaranteed by result shape or even by successful return for every claimed effect.
- Recording occurred: proven locally by ledger storage and later by retrievable event records.
- Knowledge extraction occurred: proven by an `evidence.observed` event caused by an accepted source event.

These are separate acts in some districts and evidence layers in others. The repository does not support promoting them into mandatory universal stages.

## Cross-district invariants

- Act is not act artifact.
- Artifact existence is not act occurrence.
- Producer function body existence is not evidence that one invocation occurred.
- Observing a live invocation is not durable occurrence evidence unless preserved.
- Call history is not artifact provenance unless represented.
- Producer attribution fields do not automatically prove producer occurrence.
- Recording is not truth of the recorded claim.
- Event is not explanation.
- Execution result is not execution record.
- Consumer reconstruction is not original occurrence proof.
- Stable identifier is not occurrence seal.
- Successful return does not prove every claimed effect occurred.
- Failed act does not imply no occurrence; a failed execution branch is itself an occurred invocation/failed-recording path when recorded.

## District-specific differences

Selection and establishment are internal, read-only, non-mutating acts whose occurrence evidence is strongest at the live validated boundary and weakens when only artifacts travel. Execution is operational and may involve external effects, so its occurrence evidence separates invocation, callable return/exception, output validation, result, and event recording. Recording has its own occurrence proof in ledger storage but does not prove the prior act. Knowledge extraction has a narrow warrant over source-event shape and records evidence, not facts or external truth.

## Claims contradicted

- The existence of a responsible producer definition is sufficient evidence that an act occurred. It is not; invocation and branch return are separate evidence claims.
- An act artifact carries occurrence standing for later consumers merely because it has fields consistent with responsible production. Direct construction prevents that conclusion unless production evidence travels.
- Recording preserves truth of occurrence automatically. The recorder may preserve testimony or a result event without independently verifying every prior act or external effect.
- Event recording is required for constitutional occurrence. Read-only selection and establishment boundaries contradict this.
- Execution is the only district with evidence burden. Selection and establishment also require producer-boundary occurrence evidence, though their external-effect burden differs.

## Claims remaining unresolved

- Whether any future artifact family preserves an explicit producer-to-result occurrence seal.
- Which production boundaries, outside the surveyed districts, intentionally make producer occurrence travel as durable evidence.
- How much weight later consumers should assign to unrecorded operator or observer testimony when no repository artifact preserves it.
- Whether persistent storage backends strengthen event-record durability beyond the in-memory ledger surveyed here.

## Book chapters updated

- `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`.
- `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`.
- `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md`.
- `book_of_seed/03-goals-and-advancement/construction-and-establishment.md`.
- `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`.
- `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md`.
- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`.
- `book_of_seed/06-state-and-projection/events-facts-and-state.md`.
- `book_of_seed/07-operational-realization/execution-and-recording.md`.

## Bounded resolution

Occurrence evidence is distributed across boundary, artifact, observer, and record. Responsible validated boundaries provide the strongest local evidence that internal selection or establishment occurred when observed live. Artifacts carry assertions and represented provenance but usually not proof of responsible production. Records preserve that something was recorded and can carry testimony or execution lineage forward, but they do not automatically prove the truth or external effects of recorded claims. Different act districts require different occurrence evidence.

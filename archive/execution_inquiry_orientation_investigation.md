# Execution inquiry orientation investigation

## Implementation summary



## Bounded execution questions recovered

| Bounded execution question | Primary answer owner | Supporting contributors | Authority boundary | Implementation participants |
| --- | --- | --- | --- | --- |
| How did this registered tool call execute? | `ToolExecutor` result and event sequence. | Tool registry, input/output validation, policy evaluation, event ledger, fact extraction. | Executes only registered operations after validation and policy checks; writes tool call events as execution records. | `seed_runtime.execution.ToolExecutor`, `ToolExecutionPolicyService`, `ToolValidationService`, `PolicyGate`, `EventLedger`, `FactExtractionService`. |
| Why did this tool call end this way? | `ToolCallResult` plus policy/failure/completion event payloads. | Policy decision, validation phase, exception capture, pending action creation for confirmation/approval paths. | Policy may block or require approval before execution; validation failures and execution failures are represented as failed results/events. | `ToolExecutor.execute`, `_policy_denied`, `_failed`, `_execute_allowed_tool_call`, pending action service. |
| What execution activity is visible to the operator right now? | Execution status consumer/rendering surface. | Observation lifecycle phases, progress cadence, CLI rendering, in-memory recording for tests. | Transient, renderer-independent, non-authoritative activity visibility; does not own execution state. | `ExecutionStatus`, `CliExecutionStatusConsumer`, `RecordingExecutionStatusConsumer`, `ObservationProducerLifecycle`, `emit_status`. |
| How did observations become projected state? | Projection shape visibility and state projection implementation. | Event replay, alias projection, measurement retention, inference, fact support, relationship/entity projection, finalization. | Read-only projection-shape view; projection stages derive from event ledger and do not write the event ledger. | `seed_runtime.projection_shape`, `StateProjector`, `ProjectionStore`, `State`, projection diagnostics. |
| Why was or was not projection/cache reuse possible? | Projection cache/store implementation and projection diagnostics. | Snapshot version, last event id, state projection version, dependent summary/index snapshot keys. | Event ledgers own append-only history; projection stores own reusable derived snapshots. | `ProjectionStore`, `ProjectionSnapshot`, `SummaryProjectionSnapshot`, `DerivedIndexSnapshot`, cached projector/store methods. |
| Where did this operational conclusion come from? | Reasoning path question surface. | Source evidence, conclusions, consumers, existing projection/diagnostic evidence. | Read-only audit; no recording, event-ledger writes, or cluster mutation. | `question_surface_inventory` derivation-explanation row and `reasoning_path` surface. |
| Why was this operational conclusion selected? | Selection path question surface. | Candidates, factors, alternatives, selected outcome. | Read-only audit; explicit target required; no recording, event-ledger writes, or cluster mutation. | `question_surface_inventory` selection-explanation row and `selection_path` surface. |
| Can Seed reach this execution-related knowledge from preserved/projected/read-model/inquiry/rendered evidence? | Knowledge reachability audit. | Preserved evidence, projected state, read models, inquiry surfaces, rendered surfaces. | Read-only audit over projected and repository evidence; no recording or mutation. | `knowledge_reachability`, inquiry orientation support, projected/read-model surface scanning. |
| Which surfaces declare and constrain execution/diagnostic answers? | Diagnostic inventory and diagnostic shape audit. | Registry declarations, implementation shape specs, CLI flags, record scope, event-ledger writes, cluster mutation flags. | Static/read-only registry and implementation audit; shape audit checks declarations instead of executing target surfaces. | `diagnostic_inventory`, `diagnostic_shape_audit`, `question_surface_inventory`. |

## Execution question to answer-owner mappings

1. **Concrete registered execution** is owned by `ToolExecutor`, not by question inventory. The executor advertises ownership as registered tool execution and records started/completed/failed tool call events.
3. **Operator-visible progress** is owned by execution-status consumers, but these consumers explicitly do not own execution state.
4. **Projection transformation questions** are owned by projection shape/state projection surfaces, with event replay and projection stages as supporting contributors.
5. **Derivation and selection questions** are owned by bounded question surfaces (`reasoning_path` and `selection_path`) rather than by low-level execution concepts.
6. **Surface authority questions** are owned by diagnostic inventory and shape audit.

## Supporting contributor mappings

The following concepts look primary when the investigation starts from implementation concepts, but become contributors when the investigation starts from bounded questions:

| Concept | Inquiry-oriented role | Evidence-backed reason |
| --- | --- | --- |
| Event history | Shared supporting evidence. | Runtime trace and projection stages both reconstruct from append-only events; tool execution writes events. |
| Observation ingestion | Supporting contributor. | Execution status exposes observation lifecycle phases, and projection consumes recorded observations, but neither makes ingestion the bounded execution question. |
| State projection | Answer owner for projection-shape questions; contributor for policy/runtime questions. | Tool execution uses projected state as policy input, while projection shape exposes stages directly. |
| Projection diagnostics | Supporting contributor. | They explain build/cache behavior but are constrained by diagnostic inventory/shape audit boundaries. |
| Projection cache | Implementation detail for cache-reuse questions. | Projection store owns reusable snapshots derived from event history. |
| Dependent read-model caches | Implementation detail. | Summary and derived-index snapshots are keyed by state projection version and last event id. |
| Runtime trace | Answer owner for “what happened during this runtime run?” | It reconstructs a run without replaying or mutating it. |
| Runtime why | Bounded answer composition, not a separate owner found in code. | The implementation supports “why” through decision reason, policy denial, errors, reasoning path, and selection path rather than a standalone runtime-why owner. |
| Execution status | Presentation concern/supporting evidence. | It is transient, renderer-independent, non-authoritative activity visibility. |
| Audit snapshots | Shared supporting evidence. | Snapshots preserve audit outputs and git metadata for before/after comparison, but only for supported audit kinds. |
| Formatters | Presentation concern. | Question-surface rows name human formatters, while authority remains with read-only builders/surfaces. |

## Authority boundaries

Current execution inquiry boundaries are explicit and conservative:

- Tool execution is bounded to registered operations after validation and policy checks, with policy denials, approval requirements, and failures recorded as outcomes rather than silently executing.
- Runtime trace is read-only reconstruction over append-only events and does not replay or mutate a run.
- Execution status is transient operator feedback and cannot modify execution state.
- Projection shape and question-surface inventory are read-only diagnostic surfaces with no event-ledger writes or cluster mutation.
- Diagnostic inventory and shape audit preserve visibility boundaries for record scope, event-ledger writes, diagnostic facts, and cluster mutation.
- Inquiry artifacts are repository-visible only as bounded classifications and explicitly do not create a generalized inquiry graph.

## Implementation participant mappings

| Participant | Participates in answers by | Inquiry role |
| --- | --- | --- |
| `ToolExecutor` | Validating, policy-checking, executing, recording tool call outcomes. | Answer owner for concrete registered execution. |
| `ToolExecutionPolicyService` / `PolicyGate` | Producing allow/block/approval outcomes. | Supporting contributor to “why ended this way.” |
| `ToolValidationService` | Checking registered tool status, input schema, output schema. | Supporting contributor to execution outcome questions. |
| `EventLedger` | Preserving append-only execution/runtime/projection source events. | Shared supporting evidence. |
| `ExecutionStatusConsumer` implementations | Rendering or recording transient progress/status updates. | Presentation/supporting evidence, not execution authority. |
| `StateProjector` / projection shape | Transforming event history into projected state and exposing stage shape. | Answer owner for projection transformation questions. |
| `ProjectionStore` | Saving/loading reusable state, summary, and derived index snapshots. | Implementation detail for cache-reuse questions. |
| `reasoning_path` / `selection_path` | Explaining derivation and selection for operational conclusions. | Answer owners for bounded why/selection inquiries. |
| `diagnostic_inventory` / `diagnostic_shape_audit` | Declaring and checking surface shape, record scope, mutation boundaries. | Authority-boundary answer owners. |

## Inquiry-oriented findings

- The repository already contains a `Question -> Bounded Surface -> Supporting Contributors -> Implementation Evidence -> Answer` pattern for operational questions through `question_surface_inventory`.
- Execution questions are partially represented in that pattern through projection shape, derivation explanation, selection explanation, knowledge reachability, and surface inventory/shape validation.
- Inquiry can own the question orientation only where an existing bounded surface exists. Implementation still owns the actual execution answer.

## Implementation-oriented findings

- Prior implementation concepts remain valid evidence, but several are not primary question owners when viewed from bounded inquiry.
- `ToolExecutor` is a direct execution answer owner because it performs the registered operation and records outcomes.
- Runtime trace and projection shape are read-only answer owners because their implementation explicitly builds bounded views.
- Execution status and formatters are presentation concerns unless consumed as supporting evidence for operator-visible activity.
- Projection cache and dependent read-model caches are implementation details that answer cache-reuse questions only through projection/cache diagnostics and store metadata.

## Orientation corrections discovered

- Starting from implementation concepts overstates concepts such as projection cache, formatters, and execution status as primary execution concepts. Starting from bounded questions reclassifies them as contributors, implementation details, or presentation concerns.
- The current implementation does not require a new execution question-family implementation to recover the model. Existing question surfaces and execution services already imply the model.
- The repository supports inquiry owning question framing only within declared surfaces; it does not support promoting every investigation phrase into repository knowledge.

## Agreements with previous investigations

- The investigation agrees that these concepts make execution explainable.
- The correction is role-oriented: several concepts are evidence or contributors, not necessarily answer owners.

## Contradictions discovered

- No repository evidence supports treating “runtime why” as a standalone implemented answer owner. The evidence supports composing why-answers from decision records, policy events, tool/error events, reasoning path, and selection path.
- No repository evidence supports adding new Question Families or inquiry surfaces for this investigation.
- No repository evidence supports treating presentation vocabulary as preserved/projected knowledge without knowledge reachability evidence.

## Smallest truthful execution inquiry model already implied

```text
Bounded execution question
  -> existing answer owner or bounded surface
  -> supporting contributors
  -> authority boundary from implementation/diagnostic declarations
  -> implementation evidence
  -> bounded answer
```

For current execution, the smallest implied model is:

1. **Registered execution answer**: `ToolExecutor` answers how a registered tool call executed and why it completed, failed, blocked, or required approval.
3. **Projection answer**: projection shape/state projection answers how event history becomes projected state.
4. **Cache answer**: projection store/snapshot metadata answers cache reuse boundaries.
5. **Operational why/selection answer**: reasoning and selection path surfaces answer derivation and selection questions for operational conclusions.
6. **Visibility/authority answer**: diagnostic inventory and shape audit answer which surfaces exist and what boundaries constrain them.

This model is already present and should not be extended by this investigation.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules' && git status --short`
- `cat AGENTS.md && rg --files`
- `rg "inquiry|investigation|execution" seed_runtime tests -n`
- `find . -maxdepth 3 -type d | sort`
- `rg "execution concepts|bounded execution|inquiry" -n .`
- `python -m scripts.seed_local --question-surface-inventory --json`
- `python -m scripts.seed_local --inquiry-artifacts --json`
- `python -m scripts.seed_local --diagnostic-inventory --json`
- `python -m scripts.seed_local --diagnostic-shape-audit --json`
- `python -m scripts.seed_local --projection-shape --json`
- `sed -n` inspections of implementation files listed below

## Files inspected

- `AGENTS.md`
- `scripts/seed_local.py`
- `seed_runtime/execution.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/audit_snapshots.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/projection_shape.py`
- `tests/test_execution.py`
- `tests/test_execution_status.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Files changed

- `docs/execution_inquiry_orientation_investigation.md`

## LOC changed

- 1 file changed, 137 insertions(+), 196 deletions(-).

## Tests run

- `pytest -q tests/test_execution.py tests/test_execution_status.py tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Concluding question

Does the repository naturally organize execution around
bounded execution questions,

with implementation serving those questions,

rather than around implementation concepts themselves?

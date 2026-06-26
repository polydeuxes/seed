# Work Responsibility Reconciliation

## Implementation summary

This reconciliation recovers existing repository conclusions about responsibility, ownership, authority, and work-class distinctions. It is documentary only. It does not implement runtime behavior, add diagnostic surfaces, add CLI flags, change inventories, or propose a new responsibility model.

Repository authority wins over the prompt. The recovered answer is that Seed has already established a responsibility-oriented architecture, but it has not established a full taxonomy of critical, optional, background, maintenance, and pending work as current runtime states.

## Documents reviewed

Required documents reviewed:

- `docs/runtime_responsibility_reconciliation.md`
- `docs/runtime_runtime_loop_responsibility_audit.md`
- `docs/question_ownership_responsibility_reconciliation.md`
- `docs/responsibility_ownership_organization_reconciliation.md`
- `docs/bounded_answer_responsibility_investigation.md`
- `docs/answer_responsibility_implementation_characterization.md`
- `docs/local_cli_responsibility_boundary_audit.md`

Additional materially relevant documents reviewed:

- `docs/answer_responsibility_gap_analysis.md`
- `docs/answer_responsibility_auditability_investigation.md`
- `docs/runtime_orientation_evidence_inventory.md`
- `docs/inquiry_orientation_surface_family_observation.md`
- `docs/inquiry_state_reasoning_reconciliation.md`
- `docs/presentation_conversation_responsibility_reconciliation.md`

Implementation files referenced through those documents and spot-checked by search:

- `seed_runtime/runtime.py`
- `seed_runtime/runtime_loop.py`
- `seed_runtime/runtime_loop_context.py`
- `seed_runtime/execution.py`
- `seed_runtime/pending_actions.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/reasoning_path_audit.py`
- `scripts/seed_local.py`

## Repository conclusions recovered

### 1. Responsibilities already established

Seed has already established responsibility at several implementation-backed boundaries:

| Established responsibility | Repository conclusion recovered |
| --- | --- |
| Runtime orchestration | `Runtime` routes validated decisions to owner services and records response events. It does not own all target behavior. |
| Decision production and validation | The decision producer creates decisions; the validator enforces supported decision shapes before runtime routing. |
| Registered tool execution | `ToolExecutor` owns registered operation execution after registry lookup, validation, and policy checks. |
| Pending-action lifecycle | `PendingActionService` owns pending-action events; `ToolExecutor` owns resume execution today. RuntimeLoop currently has a parity gap here, not duplicate ownership. |
| State projection and projection cache | `StateProjector` owns derivation of projected state; `ProjectionStore` owns reusable projected snapshots and indexes. |
| Event history | `EventLedger` is the append-only historical event store; runtime and services append specific event vocabularies but do not replace ledger authority. |
| Observation collection | Observation sources and collection services own bounded observation production and ingestion boundaries, not projection semantics or runtime governance. |
| Diagnostic inventory and shape audit | Diagnostic inventory owns mechanical visibility of diagnostic surfaces; diagnostic shape audit owns registry-to-implementation shape validation. |
| Bounded operator questions | A bounded question is owned by the subsystem that emits the operator-facing answer shape, boundary, uncertainty, and capability for that question. |
| CLI/local operator entry point | The CLI owns argument parsing, local orchestration, read-model dispatch, and terminal formatting. It should not own domain taxonomy, projection semantics, evidence semantics, capability policy, or runtime behavior. |

The repository has therefore already answered that responsibility is not a generic object classification. It is a scoped implementation boundary: a service, inventory, projection stage, diagnostic/read model, or output shape owns a bounded responsibility and states what it does not own.

### 2. Whether Seed already distinguishes classes of work

Seed distinguishes some work-like classes, but under narrower implementation terminology:

| Recent discussion vocabulary | Existing repository terminology, if present | Reconciliation |
| --- | --- | --- |
| Operator requests | `input.user_message`, bounded request/response runtime path, bounded operator question, operator-facing answer shape | Present. Operator-originated input and operator-facing answers are implementation-backed. |
| Runtime work | Runtime orchestration, decision validation, owner-service routing, response/event emission | Present, but as orchestration and routing, not as a generic runtime state machine. |
| Diagnostic work | Diagnostic surface, diagnostic inventory, diagnostic shape audit, read-only diagnostic/read-model surface | Present. Diagnostics are read-only unless explicitly declared otherwise and must not silently become cluster truth. |
| Maintenance work | No established general runtime class found | Absent as a repository-backed work class in the reviewed evidence. Some docs recommend future cleanup or extraction, but recommendations are not current runtime work classes. |
| Background work | Observation collection phases, transient `ExecutionStatus`, self-observation process/resource facts | Partially present as collection/progress/resource visibility, but not as a generic background-process owner or durable background-active state. |
| Pending work | Pending actions, tool needs/capability gaps, approval/confirmation requirements | Present as explicit pending-action/tool-need lifecycle concepts, not as generic unscheduled work. |
| Blocked work | Policy denied/approval required, unknowns, unavailable evidence, capability gaps | Present only in bounded surfaces and policy/tool paths. Not a global runtime class. |
| Optional work | No established general runtime class found | Absent as a repository-backed work class in the reviewed evidence. |
| Critical work | No established general runtime class found | Absent as a repository-backed work class in the reviewed evidence. |

The strongest repository answer is therefore: Seed already distinguishes operator requests, runtime orchestration, diagnostics, observations, pending actions, tool needs, and bounded answer responsibility. It does not yet distinguish a complete work taxonomy such as critical/optional/background/maintenance as first-class current runtime states.

### 3. Current meanings of responsibility, ownership, and authority

#### Responsibility

Responsibility means the implementation-backed obligation of a surface or service to produce, route, validate, compose, execute, project, or render a bounded result while preserving its boundary. Responsibility is recovered from implementation shape, service boundaries, result dataclasses, inventory rows, event vocabularies, tests, and authority-boundary text.

For answer surfaces specifically, responsibility is the bounded answer contract: the view object, builder logic, unknown/caveat preservation, formatter sections, and authority boundary that determine what answer the operator receives.

#### Ownership

Ownership is the primary owner boundary for a responsibility. It is not automatically granted by data contribution or by vocabulary appearing in prose. The question-ownership reconciliation states the pattern most directly: a bounded question is owned by the subsystem whose implementation emits the operator-facing answer shape for that question.

Ownership is often exclusive at the primary answer-owner boundary and layered at the evidence-contribution boundary. Multiple contributors can feed one answer owner; contributor loss degrades evidence, while answer-owner loss removes the operator capability for that bounded question.

#### Authority

Authority is the evidence and boundary that make a responsibility legitimate and limit its claims. It appears as authority boundaries, constrained authority profiles, projection-stage influences/non-influences, diagnostic inventory fields, read-only/no-mutation boundaries, event-ledger boundaries, and negative authority text.

Authority differs from ownership because it limits what the owner may conclude. It differs from responsibility because it is not the work itself; it is the justification and constraint for the work. A surface can own an answer while explicitly lacking authority to infer runtime status, mutate state, inspect files, promote diagnostic findings into cluster truth, or generalize beyond its input evidence.

### 4. Whether Seed already describes how it determines what naturally comes next

The repository has partial, bounded evidence for next-step orientation, but not a general autonomous determination of what naturally comes next.

Evidence that exists:

- Runtime handles one operator message at a time: input is recorded, state is projected, context is composed, one decision is produced and validated, and the decision is routed to answer, tool need, tool execution, state patch, or refusal.
- Tool requests create tool needs and recommendations; pending actions preserve approval/confirmation boundaries before execution.
- Operational Story, Reasoning Path Audit, Selection Path Audit, Inquiry Orientation, Knowledge Reachability, and Reference Selection provide bounded orientation, derivation, selection, or reachability answers from existing evidence.
- Inquiry Orientation is explicitly limited: it can find related preserved material and preserve uncertainty, but it does not assert importance, ownership, intent, recommended action, or the next safe move.

Evidence absent:

- No reviewed source establishes a global planner, scheduler, autonomous next-work selector, or durable current-work queue.
- No reviewed source establishes `current_mode`, `current_owner`, or `runtime_context` as repository-native current runtime state.
- No reviewed source establishes that absence of work is a recorded `idle`, `unscheduled`, or `no-current-work` fact.

Conclusion: Seed determines local next handling inside bounded flows and bounded answer surfaces. It does not currently describe a general mechanism for determining what naturally comes next across all work.

### 5. Critical, optional, background, and maintenance work

Repository evidence currently supports the following:

| Class | Repository-backed conclusion |
| --- | --- |
| Critical work | Absent as a current implementation-backed work class. The repository has policy, approval, risk, pressure, impact, and authority concepts, but the reviewed evidence does not define a general `critical work` class. |
| Optional work | Absent as a current implementation-backed work class. Recommendations and future work sections exist, but those are not an implemented optional-work taxonomy. |
| Background work | Partially present only as observation/progress/resource visibility. The repository explicitly does not expose a generic background-process owner or durable `background-active` state. |
| Maintenance work | Absent as a current implementation-backed work class. Cleanup/extraction recommendations appear in audits, but repository evidence does not promote them into a runtime work category. |

This reconciliation therefore rejects promoting the recent operator discussion vocabulary into repository fact.

## Terminology reconciliation

| Do not promote as repository fact | Repository-backed terminology to use instead |
| --- | --- |
| `operator-critical work` | policy outcome, risk/impact/pressure evidence, bounded operator question, approval requirement, pending action, or capability gap, depending on actual evidence |
| `runtime-owned work` | runtime orchestration, owner-service routing, decision validation, response/event emission |
| `diagnostic/background work` | diagnostic surface, diagnostic inventory entry, read-only diagnostic/read-model surface, observation collection phase, transient execution status |
| `maintenance work` | future extraction/cleanup recommendation only, unless an implementation artifact says otherwise |
| `blocked/pending work` | pending action, tool need, capability gap, policy denied, approval required, unknowns/limitations |
| `current_mode` | no repository-backed current runtime state found |
| `current_owner` | responsibility owner, answer owner, service owner, or actor/event owner only when implemented evidence supports it |
| `runtime_context` | `ContextPacket`, `RuntimeContext`, projected state, or decision-context view only in their specific implementation scopes |
| `idle` / `unscheduled` / `no-current-work` | absence of implementation-backed state; do not infer as fact |

## Agreements between old and recent work

Recent runtime-orientation discussion agrees with existing repository direction when it stays within these boundaries:

1. It treats runtime visibility as evidence-backed rather than as presentation vocabulary.
2. It uses event history, actors, causation/correlation, decision journals, projected state, pending actions, and bounded diagnostic/read-model surfaces as evidence.
3. It distinguishes observation/progress visibility from cluster truth.
4. It recognizes that diagnostic findings must remain scoped and must not silently become host/service/filesystem/runtime truth.
5. It treats bounded inquiries as read-only orientation unless an implementation-backed owner and authority boundary exists.

## Contradictions between old and recent work

Recent work contradicts repository direction if it does any of the following:

1. Treats `current_mode`, `current_owner`, or `runtime_context` as established repository facts without implementation evidence.
2. Replaces responsibility/authority/evidence boundaries with a new runtime-state framing.
3. Treats `background-active`, `idle`, `unscheduled`, `critical`, `optional`, or `maintenance` as existing Seed runtime states.
4. Infers what Seed should do next from presentation labels rather than from bounded answer surfaces, event history, projected state, pending actions, or explicit policy/tool evidence.
5. Treats RuntimeLoop-era migration wording as current-core guidance despite the audit's stale/quarantined warning that current architecture treats `Runtime` as canonical and `RuntimeLoop` as deprecated/experimental.

## Unresolved questions

These questions remain unresolved by existing repository evidence and should not be answered by vocabulary alone:

1. Should Seed ever introduce a durable current-runtime-activity artifact? Existing evidence says it is absent, not that it must be built.
2. Should critical/optional/background/maintenance become implemented categories? Existing evidence does not establish them.
3. If a future surface asks what naturally comes next, which existing bounded owner would own that answer, and what authority would constrain it?
4. How should RuntimeLoop-specific historical artifacts continue to be quarantined or retired without changing current runtime behavior?
5. Which future responsibility documents, if any, should be reconciled into implementation-backed inventories rather than remaining prose?

## Files changed

- `docs/work_responsibility_reconciliation.md`

## LOC changed

- Added 187 lines.
- Removed 0 lines.

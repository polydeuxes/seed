# Boundary Localization Characterization

## Smallest truthful answer

The repository does **not** currently recover one universal boundary-localization engine. It does independently recover a recurring discipline: **read-only, evidence-backed localization surfaces identify a smallest supported attention boundary, expose why broader or narrower work is unsupported, and terminate before the repair, revision, replay, promotion, or execution step begins**.

The discipline is cross-family recurring, but its owner is implementation-local or family-local:

- projection replay localizes by cache/snapshot/event-ledger boundaries;
- projection shape localizes by stage influence and non-influence boundaries;
- orientation localizes by deterministic related-material evidence and explicitly refuses intent, ownership, recommendations, and next moves;
- pressure localizes operational attention by ranked visibility-surface evidence and recommended inspections, not plans;
- selection/reference-selection localize implemented selection references without mutating selection behavior;
- candidate/readiness surfaces localize possible promotion or capability attention without admission, selection, authorization, or execution;
- source navigation and knowledge reachability localize repository/presentation knowledge boundaries without semantic promotion.

Therefore the implementation-backed discipline is best characterized as **bounded localization by evidence and non-claim boundaries**: a family-local read-only implementation narrows attention to the smallest place its evidence supports, preserves everything outside through explicit `does_not_influence`, unknown, non-selected, limitation, or boundary notes, and stops before a downstream owner performs reconstruction, revision, replay, promotion, or execution.

## Evidence reviewed

### Replay scope visibility and replay execution

`projection_store.projected_state_with_cache_status` determines replay locality from snapshot state and event-ledger position. If a snapshot matches the current last event, it returns the cached state with `events_applied=0`. If a usable snapshot exists but is behind, it computes `remaining_events = _events_after_snapshot(events, snapshot.last_event_id)`, emits `incremental_projection_replay`, calls `projector.project_from_state(snapshot_state, replay_events)`, and returns status with `incremental_replay=True` and `events_applied=len(remaining_events)`. If those conditions fail, it emits full `projection_replay` and calls `projector.project(...)` over the workspace.

This is a concrete localization rule for replay work: begin after the snapshot boundary when safe; otherwise begin at full replay. It is not a general repair rule and not explanation revision.

### Projection influence lineage

`projection_shape.py` exposes projection stages with `consumes`, `produces`, `influences`, `does_not_influence`, and `authority_boundary`. For example, `event_replay` consumes the event ledger, produces projected runtime structures, influences projection finalization, and does not influence the event ledger. Subsequent stages separately mark identity-resolution, selection-bearing, derivation-bearing, validation-only, explanatory-only, and projection-boundary authority.

This localizes attention by implementation stage and explicitly preserves outside regions via `does_not_influence`. It identifies where influence can and cannot travel. It does not execute replay or repair.

### Orientation insufficiency and inquiry orientation

`inquiry_orientation.py` records inquiry notes in an isolated JSONL probe store, then builds a read-only orientation view by tokenizing note prose and collecting deterministic overlaps from projected fact supports and source navigation. Its authority boundary states that the note is preserved operator prose, not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction; matches do not assert importance, ownership, intent, concern, recommended action, or next safe move.

This is a strong localization surface: it identifies potentially related material before inquiry work, but refuses narrower semantic claims and broader workflow authority. It terminates at related-material visibility.

### Replay selection and operational selection

`selection_path_audit.py` explains implemented selection evidence without changing selection behavior. It composes pressure audit and operational story, uses the first pressure item when the target is current focus or primary pressure, and otherwise returns `unknown` when the target is not implemented. Its boundary is read-only: no fact recording, event-ledger writes, or cluster mutation.

This localizes why an operational conclusion was selected among pressure candidates. It is not replay, repair, or execution.

`reference_selection.py` similarly localizes comparison references. Only the `history` domain is implementation-backed; unsupported domains return `unknown` with limitations. History selection uses impact and snapshot-policy evidence and keeps limitations such as no accepted-baseline creation, lifecycle, registry, persistence, runtime behavior, or policy introduction.

### Affected scope recovery and pressure recovery

`pressure_audit.py` ranks operational pressure from existing visibility surfaces: diagnostic shape, ownership ambiguity, capability needs, orphaned predicates, and fragile predicates. It returns scored pressure items with evidence, reason, and a recommended inspection command. The builder explicitly ranks operational pressure without planning, recording, or mutating state.

This identifies a smallest visible operational pressure surface to inspect next. It does not authorize repair; the recommended command is inspection, not execution.

### Candidate admission and implementation readiness

`capability_candidates.py` preserves package-derived capability candidates from projected facts only. Boundary notes reject capability proof, execution authority, execution decision, tool invocation, capability selection, policy evaluation, and tool execution. Its rationale states observed package evidence is associated with a candidate but is not proof, permission, selection, planning, or execution.

`capability_promotion_readiness.py` joins candidate support with verification evidence and classifies promotion readiness as supported only when both are present. Its module contract says it does not create `capability_verified` facts, select capabilities, evaluate policy, invoke tools, plan, or execute. Boundary notes reject promotion, verified-capability creation, inventory modification, capability selection, policy evaluation, tool execution, and execution authority.

These surfaces localize a possible future promotion boundary, not admission itself.

### Source navigation and implementation relationship grammar

`source_navigation.py` uses only projected `defines` and `imports` facts. It does not inspect files, parse source, ingest observations, infer behavior, infer reachability, or infer ownership. It localizes a query to definition/import/support rows and emits non-claims rejecting calls, behavior, capability ownership, runtime reachability, ownership authority, dependency correctness, truth, and semantic relevance.

This is implementation-backed locality without repair: it tells where source evidence is, not what architectural change to make.

### Knowledge reachability and presentation vocabulary

`knowledge_reachability.py` audits candidates through stages: Preserved, Projected, Read Model, Inquiry Orientation, and Rendered. Candidate kinds include `presentation_label` and `unknown`, and default seeds include presentation terms such as continuation, source navigation, current work position, active edge, storage topology, state build, and projection cache. This supports the reading discipline that presentation vocabulary must not be promoted into preserved/projected knowledge without implementation evidence.

### Inquiry artifacts and bounded inquiry

`inquiry_artifacts.py` exposes artifacts such as unknown, boundary, pressure, finding, supported conclusion, unsupported conclusion, open question, and gap with classifications and limitations. Its boundary is read-only and explicitly rejects recording, event-ledger writes, cluster mutation, inquiry movement inference, inquiry graph creation, pressure transformation inference, and workflow/planning behavior.

This supports a methodological locality: some inquiry artifacts are visible, but the implementation refuses to turn them into movement or workflow.

## Candidate survey

| Candidate owner | Identifies where work belongs? | Merely observes? | Authorizes work? | Executes work? | Insufficient/stale boundary? | Preserves outside boundary? | Stops before reconstruction? | Characterization |
|---|---:|---:|---:|---:|---|---:|---:|---|
| Projection cache/replay | Yes, for replay start point | No; it executes replay after selection | No cluster/work authorization | Yes, replay only | Stale snapshot / full miss | Yes, via event range and cache status | No; this owner continues into replay | Runtime replay-local localization plus execution, not general boundary localization |
| Projection shape | Yes, by stage influence | Yes | No | No | Influence boundary, not stale repair | Yes, `does_not_influence` | Yes | Strong read-only localization pattern |
| Inquiry orientation | Yes, potentially related material | Yes | No | No | Insufficient semantic boundary | Yes, authority boundary and uncertainty | Yes | Strong explanation-local localization pattern |
| Pressure audit | Yes, ranked operational pressure | Yes | No | No | Insufficient/ambiguous operational visibility | Partly, by omitted zero-score candidates and recommended inspection only | Yes | Operational attention localization |
| Selection path | Yes, implemented selection path | Yes | No | No | Unknown when target unsupported | Yes, non-selected and unknowns | Yes | Selection-explanation localization, not replay selection |
| Reference selection | Yes, comparison reference domain | Yes | No | No | Unsupported domains; unavailable history reference | Yes, alternatives and limitations | Yes | Reference-boundary localization |
| Source navigation | Yes, source fact/support location | Yes | No | No | Unknown definition/support | Yes, non-claims | Yes | Repository evidence locality |
| Knowledge reachability | Yes, first loss across stages | Yes | No | No | Insufficient preservation/projection/read-model/rendering | Yes, candidate kinds and first-loss stage | Yes | Knowledge-boundary localization |
| Capability candidates | Yes, possible candidate names | Yes | No | No | Insufficient capability proof | Yes, boundary notes | Yes | Candidate preservation only, not admission |
| Promotion readiness | Yes, possible future promotion support | Yes | No | No | Missing verification support | Yes, no promotion/fact creation | Yes | Readiness localization only |
| Inquiry artifacts | Partly, artifact visibility classification | Yes | No | No | Unknown/document/partial visibility | Yes, limitations and no workflow | Yes | Methodology/visibility locality, not runtime engine |

## Neighbor analysis

### Boundary Localization != Lawful Revision

Boundary localization can identify where explanation or implementation attention belongs, but lawful revision is the later act of changing architectural explanation. Orientation, source navigation, projection shape, pressure audit, selection path, candidate, and readiness surfaces all expose boundaries while refusing mutation, planning, or fact creation. The repository therefore supports localization-before-revision, not localization-as-revision.

### Boundary Localization != Replay Scope

Replay scope is one runtime-local instance of boundary localization. Projection cache status decides full replay versus incremental replay from events after a snapshot. Projection shape also describes `event_replay` as a stage. But orientation, source navigation, pressure audit, and candidate readiness localize boundaries without replay. Replay scope is not the universal owner.

### Boundary Localization != Replay Selection

Selection-path audit explains operational selection from pressure ordering and unknown targets. Reference selection explains comparison-reference choice. Replay selection is governed by projection-cache conditions. These are separate implementation owners with separate evidence inputs.

### Boundary Localization != Candidate Admission

Capability candidates and promotion readiness identify possible candidates and readiness support while explicitly rejecting capability proof, selection, permission, policy evaluation, fact creation, and execution. Candidate admission would require a later owner; localization only preserves the candidate boundary.

### Boundary Localization != Pressure

Pressure audit ranks operational pressure and recommends inspection. It localizes operational attention, but pressure itself is one evidence class among several. Source navigation, orientation, projection shape, knowledge reachability, and readiness can localize without pressure scoring.

### Boundary Localization != Orientation

Inquiry orientation is the clearest explanation-facing localizer, but not the only one. It uses lexical overlap and source navigation; projection cache, projection shape, reference selection, and candidate readiness use different evidence and boundaries.

## Negative authority

### Localization is not repair

Read-only localization surfaces repeatedly reject repair behavior: inquiry orientation refuses plans and commands; pressure audit ranks without planning, recording, or mutating; source navigation refuses behavior/reachability/ownership claims; capability readiness refuses fact creation, promotion, selection, policy evaluation, and execution. Localization identifies a boundary; repair belongs to a downstream owner not recovered here as universal.

### Localization is not replay

Projection replay may use boundary localization, but many localizers do not replay: projection shape is read-only visibility; inquiry orientation reads projected state; source navigation uses projected source facts; candidate and readiness inspections read projected facts and local PATH evidence; inquiry artifacts expose visibility. The repository rejects replay as the general identity.

### Localization is not admission

Candidate and readiness surfaces are explicit negative authority. Candidate evidence is not capability proof or permission. Readiness support is not promotion and does not create `capability_verified` facts. The repository preserves a pre-admission boundary.

### Localization is not execution

Most reviewed surfaces explicitly set or describe read-only, no event-ledger write, no cluster mutation, no tool execution, no provider call, no observation execution, or no policy evaluation. Projection replay is the special replay-execution owner, not the general localization owner.

### Every family does not localize boundaries the same way

Families use different evidence and stopping rules:

- replay uses event-ledger position and snapshot validity;
- projection shape uses stage influence and non-influence metadata;
- orientation uses deterministic lexical overlap and uncertainty;
- pressure uses ranked audit candidates;
- selection/reference selection use implemented selection surfaces and candidate alternatives;
- capability candidate/readiness uses package facts and verification evidence;
- source navigation uses projected `defines`/`imports` support;
- knowledge reachability uses staged preservation/projection/read-model/orientation/rendering checks.

The recurrence is disciplined locality, not a shared implementation owner.

## Locality

Current status:

- **Implementation-local:** yes. Several modules implement bounded locality within their own family.
- **Family-local:** yes. Replay, projection shape, orientation, pressure, source navigation, capability readiness, and knowledge reachability each have family-local localization rules.
- **Cross-family recurring:** yes, as a pattern of read-only evidence-backed boundary identification plus explicit non-claims.
- **Methodological:** yes, documentation and inquiry-artifact surfaces preserve unknowns, gaps, open questions, and limitations without converting them into workflow.
- **Constitutional:** not established. There is no universal constitutional participant or engine that owns boundary localization across families.
- **Still unknown:** universal owner, shared participant, and future admission criteria remain unknown.

## Typed unknowns

| Unknown | Preserved answer |
|---|---|
| Universal localization owner | Unknown. No single implementation owner spans replay, explanation, candidates, source navigation, orientation, pressure, and readiness. |
| Shared constitutional participant | Unknown. Recurrence is visible, but no constitutional runtime role is implemented. |
| Explanation vs runtime localization | Partly separated. Runtime replay localizes by snapshots/events; explanation and orientation localize by evidence/lexical/source boundaries. A shared owner is not implemented. |
| Locality admission | Unknown. Candidate/readiness surfaces can identify possible future support but explicitly do not admit or promote. |
| Future implementation opportunities | Unknown and not recommended here. The task is characterization only. |
| Stale versus insufficient boundary | Both occur, but not universally. Replay cache handles stale snapshot/full miss. Orientation, source navigation, candidates, readiness, and reachability mostly handle insufficient evidence/support. |

## Lawful termination

This characterization stops at the recurring implementation-backed discipline because the evidence does not support a stronger claim. It does not invent a universal localization engine, does not merge replay scope with explanation scope, does not recommend implementation, and does not promote methodology into architecture.

The lawful stop is:

> Boundary localization exists today as a cross-family recurring discipline of family-local, read-only, evidence-backed boundary identification. It determines where attention may lawfully begin by exposing the smallest supported boundary and explicit non-claims, but it does not itself repair, replay, revise, admit, authorize, or execute except in the special projection replay owner that both chooses and performs replay.

## Remaining questions

1. Should future work name a first-class boundary-localization inventory surface, or would that over-promote a methodology pattern?
2. What evidence would be sufficient to distinguish a constitutional localization participant from repeated family-local boundaries?
3. Should explanation-local and runtime-local localization remain deliberately separate?
4. Can locality admission ever be implemented without becoming candidate admission, planning, or repair?
5. Which future operational surfaces, if added, would need diagnostic-inventory and diagnostic-shape-audit registration under the repository visibility contract?

## Confidence

**Medium-high** that a recurring discipline exists: multiple implementation modules independently identify bounded attention areas with explicit evidence and non-claims.

**Medium** on the exact name `boundary localization`: the behavior is implementation-backed, but the repository does not expose a current first-class owner with that name.

**Low** on any constitutional or universal claim: repository authority does not support a universal engine, shared participant, or common implementation owner.

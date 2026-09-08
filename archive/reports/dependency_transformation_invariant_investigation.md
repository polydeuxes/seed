# Dependency Transformation Invariant Investigation

## Scope

This bounded investigation reviews whether completed implementation responsibility families consistently define responsibilities by the explicit dependencies they consume and the explicit dependencies they produce, rather than primarily by execution sequence.

It does not recover ownership, introduce a dependency framework, propose runtime changes, rename vocabulary, add orchestration, or promote grammar theory. Repository authority wins.

## Implementation evidence reviewed

Reviewed completed responsibility families and adjacent investigations:

- Operational Responsibility slices, especially execution recording and post-execution knowledge extraction.
- Execution Visibility slices, especially state-summary cache debug visibility and projection-cache diagnostic payload separation.
- Observation-Derived Capability slices, especially admitted capability state, executable operation contract state, requested capabilities, and capability inventory construction.
- Answer Composition slices and completion audit, especially Operational Story payload composition and compatibility handoff.
- Projection Influence Lineage slices and completion audit, especially lineage, replay assessment, replay justification, replay selection, execution request, finalization, and publication.
- Read-Model Ownership slices and completion audit, especially construction inputs, dependency identity, cache lookup request/result, construction request/result, and cache publication request/result.
- Repository Dependency Ordering Invariant Investigation.
- Inquiry Anchor Dependency-Head Investigation.
- Architectural Recovery Methodology Characterization.

## Central answer

The completed families repeatedly expose responsibilities through implementation-local objects or records that make consumed and produced dependencies explicit. The strongest evidence is in Projection Influence Lineage and Read-Model Ownership, where the code names the consumed object on each boundary and returns another object that the next boundary consumes.

However, the evidence does **not** support a repository-wide universal invariant as strong as "all responsibilities are defined by explicit dependency transformation." Several families use weaker forms: method extraction around a durable event, grouped source records before presentation, payload separation before compatibility handoff, or diagnostic report payloads with compatibility accessors. Execution order and shared state still matter in some paths, especially because many boundaries consume projected `State` and existing cache/store operations rather than purely immutable dependency objects.

Supported formulation:

```text
Across completed recovery families, successful responsibility boundaries commonly make their consumed implementation evidence explicit and hand an implementation-local result, request, payload, event, or durable record to the next responsibility while preserving compatibility.
```

Unsupported stronger formulation:

```text
Explicit dependency transformation is the single repository-wide architecture that defines every responsibility.
```

## Family evidence

### Operational Responsibility

The strongest Operational Responsibility evidence is the handoff from durable execution recording into post-execution knowledge extraction.

Implementation evidence:

- `_execute_allowed_tool_call` records a completed tool-call event, stores it in `completed_event`, passes that exact event to `_extract_post_execution_knowledge(completed_event)`, and returns the completed event id in the result payload.
- `_record_completed_tool_call(...)` appends `tool.call.completed` and returns the durable `Event`.
- `_extract_post_execution_knowledge(completed_event: Event)` consumes the already-recorded event and calls fact extraction.

Dependency transformation recovered:

```text
tool execution output
-> durable tool.call.completed Event
-> post-execution fact extraction input
```

Strength: moderate to strong. The consumed/produced dependency is explicit at the event boundary. The family is not modeled as request/result dataclasses; it is a method boundary around an existing durable event.

Counterexample/limit: the responsibility remains embedded in `_execute_allowed_tool_call`; execution order is still visible and important because fact extraction must occur after event recording. This supports explicit durable handoff more than it supports a general dependency-transformation framework.

### Execution Visibility

Execution Visibility exposes separated payloads inside a compatibility-preserving debug report.

Implementation evidence:

- `_StateBuildVisibilityPayload` carries cache eligibility, summary cache status, current/cached last event ids, and notes.
- `_ProjectionCacheDiagnosticPayload` carries state-cache status, cached state last event id, projection timings, and projection counters.
- `StateSummaryCacheDebugReport` consumes both payloads and exposes legacy accessors such as `cache_eligible`, `summary_cache_status`, and `state_cache_status`.

Dependency transformation recovered:

```text
state-build/cache observations + projection-cache diagnostic observations
-> separated visibility/diagnostic payloads
-> compatibility report/accessors
```

Strength: moderate. The consumed dependencies are observed values rather than a single explicit upstream dependency object. The produced values are explicit payloads, but the public report is a compatibility wrapper.

Counterexample/limit: this family is partially organized by report shape and operator visibility, not by a chain of responsibility eligibility. The debug path also measures and formats within one command-local surface. Execution Visibility is weaker evidence for a repository-wide dependency transformation invariant.

### Observation-Derived Capability

Observation-Derived Capability separates sources before capability inventory presentation.

Implementation evidence:

- `_AdmittedCapabilityState` represents projected capability knowledge admitted from verification facts.
- `_ExecutableOperationContractState` represents capability labels derived from registered executable operation contracts and explicitly does not verify capability existence.
- `_CapabilityInventorySources` consumes admitted capability state, executable operation contracts, and requested capabilities, then produces the unchanged capability universe through `capability_universe()`.
- `_capability_inventory_sources(state)` constructs those separated sources before `_inventory_capabilities(state)` builds the inventory universe.

Dependency transformation recovered:

```text
projected verification facts + registered operation contracts + requested needs
-> separated inventory sources
-> capability universe
-> capability inventory entries
```

Strength: moderate. The source objects are explicit and prevent conflating admitted capability knowledge with operation-contract metadata.

Counterexample/limit: the implementation still consumes `State` directly and derives multiple source sets from it. This supports explicit source separation, not a fully externalized dependency graph.

### Answer Composition

Answer Composition separates answer material, reasoning, supporting evidence, boundary, and limitations before returning public compatibility objects.

Implementation evidence:

- Operational Story defines implementation-local payloads for answer, reasoning, supporting evidence, boundary, and limitations.
- `build_operational_story(...)` constructs upstream audits, selects `primary` pressure, calls `_compose_operational_story_payloads(...)`, and then builds the public `OperationalStory` from the returned payloads.
- `_compose_operational_story_payloads(...)` returns a tuple of the five payloads.

Dependency transformation recovered:

```text
selected operational evidence and audit outputs
-> answer/reason/support/boundary/limitations payloads
-> public OperationalStory compatibility object
```

Strength: moderate. The handoff objects are explicit and tested in the family, but they are composition payloads rather than durable records.

Counterexample/limit: Answer Composition is complete as representative reusable composition, not as universal conversion of every answer-like surface. Some inquiry surfaces remain surface-specific or compressed, so this family cannot prove a repository-wide invariant by itself.

### Projection Influence Lineage

Projection Influence Lineage is the strongest evidence for explicit consumed and produced dependencies.

Implementation evidence:

- `_ReplayScopeAssessment` consumes `_ProjectionInfluenceLineage` and records `replay_required`.
- `_ReplaySelectionJustification` consumes `_ReplayScopeAssessment` and records compatible replay targets.
- `_ReplaySelection` consumes `_ReplaySelectionJustification` and produces selected replay targets.
- `_ReplayExecutionRequest` consumes `_ReplaySelection`.
- `_ProjectionPublicationRequest` consumes finalized `State`.
- `_ProjectionPublication` consumes the publication request and produces `visible_state`.
- `project_from_state(...)` executes the chain by recovering lineage, assessing scope, justifying selection, selecting replay targets, creating the execution request, executing it to produce finalized state, and publishing finalized projection state.

Dependency transformation recovered:

```text
projection influence lineage
-> replay scope assessment
-> replay selection justification
-> replay selection
-> replay execution request
-> finalized State
-> projection publication request
-> visible State publication
```

Strength: strong. Each responsibility names the input dependency and produces the next dependency. Execution order is present, but the ordering is explained by the consumed object required by the next function.

Counterexample/limit: selection intentionally does not narrow replay; execution still performs full event replay and finalization for compatibility. Therefore the explicit objects preserve existing behavior rather than proving a new planning/orchestration architecture.

### Read-Model Ownership

Read-Model Ownership is also strong evidence for explicit consumed and produced dependencies.

Implementation evidence:

- `ReadModelConstructionInputs` wraps the already-published visible `State`.
- `ReadModelDependencyIdentity` preserves `state_projection_version` and `state_last_event_id`.
- `ReadModelCacheLookupRequest` consumes dependency identity.
- `ReadModelCacheLookupResult` consumes the lookup request and carries an optional snapshot plus `cache_hit`.
- `ReadModelConstructionRequest` consumes construction inputs, dependency identity, and optional cache lookup.
- `ReadModelConstructionResult` consumes the construction request and carries the read model.
- `ReadModelCachePublicationRequest` consumes the construction result.
- `ReadModelCachePublicationResult` consumes the publication request and carries the snapshot.

Dependency transformation recovered:

```text
visible projected State
-> read-model construction inputs
-> dependency identity
-> cache lookup request/result
-> construction request/result
-> cache publication request/result
```

Strength: strong. Request/result dataclasses explicitly define the dependencies each boundary consumes and produces.

Counterexample/limit: cache storage and save/load operations remain existing callables; cache invalidation, storage policy, projection publication, rendering, and scheduling are explicitly outside this family. This is an explicit local lifecycle, not a universal repository mechanism.

## Evidence from adjacent investigations

### Repository Dependency Ordering Invariant Investigation

This investigation supported explicit dependency ordering across families, but its emphasis was ordering. It found recurring structures such as construction before publication and assessment/justification before selection/execution. That evidence is compatible with dependency transformation, but it does not by itself prove dependency transformation as the deeper invariant.

Current interpretation: dependency ordering is often a symptom of explicit consumed/produced dependencies, but not every ordered path proves a dependency object exists.

### Inquiry Anchor Dependency-Head Investigation

This investigation found that multiple inquiry-like surfaces establish a local identity before evidence selection or reasoning: `question_family`, `domain`/`subject`, `target`, `domain`, selected note, `query`, or primary pressure/focus. It explicitly rejected a single ontology.

Current interpretation: inquiry surfaces support dependency-centered roles, because evidence selection depends on an established value. They do not prove a common dependency transformation abstraction, because the identities differ and some surfaces stop with unsupported or unknown results.

### Architectural Recovery Methodology Characterization

This investigation found a recurring implementation-local bounded handoff grammar across completed families and explicitly limited the conclusion: family mechanisms differ, shared abstractions are unsupported, and Execution Visibility is weaker evidence for generalization.

Current interpretation: the methodology characterization strongly supports bounded local handoffs and identity/provenance preservation. It does not support promoting a shared dependency framework.

## Recurring dependency transformations

The following transformations recur with implementation support:

| Recurring transformation | Strong examples | Supported conclusion |
| --- | --- | --- |
| Durable record consumed by later responsibility | `tool.call.completed` event consumed by post-execution fact extraction | Some operational boundaries are defined by durable records rather than ownership prose. |
| Source records grouped before presentation | capability inventory sources, state-build/projection-cache payloads | Presentation often consumes explicitly separated source groups. |
| Assessment before selection/execution | replay scope assessment -> justification -> selection -> execution request | Selection/execution commonly consumes assessment/justification objects in recovered families. |
| Construction before publication | read-model construction result -> cache publication request/result; finalized projection state -> publication request/publication | Publication boundaries often consume already-constructed values. |
| Compatibility handoff after private payloads | Operational Story payloads -> public `OperationalStory`; debug payloads -> report accessors | Compatibility objects often consume private payloads rather than owning upstream derivation. |
| Identity-preserving handoff | visible `State` wrapped as construction inputs; finalized `State` published as visible state | Some recoveries make handoff visible without changing object identity or behavior. |

## Counterexamples and limits

1. **Execution Visibility is visibility/report shaped.** It separates payloads, but the command-local debug path is still partly about measurement, formatting, and legacy accessors.
2. **Observation-Derived Capability consumes shared `State`.** Source objects are separated after reading shared projected state; the upstream consumed dependencies are not all explicit external objects.
3. **Operational Responsibility remains order-sensitive.** The durable event handoff is explicit, but correct behavior still requires recording before extraction.
4. **Answer Composition is bounded, not universal.** Completed evidence covers representative answer-composition surfaces; not every answer-like surface has the same payload shape.
5. **Read models and projection lineage are local lifecycles.** Their explicit request/result chains are strong but deliberately exclude cache policy, invalidation, scheduling, rendering, and broader orchestration.
6. **Adjacent investigations reject universal ontology/framework claims.** Inquiry identities are role-equivalent but not one ontology; methodology evidence supports bounded handoffs but not shared abstraction.

These limits prevent treating explicit dependency transformation as an unconditional repository-wide invariant.

## Answers to central questions

### 1. Do completed responsibility families consistently define responsibilities through explicit consumed and produced dependencies?

Mostly yes, but only at the level of bounded implementation-local handoffs. Projection Influence Lineage and Read-Model Ownership do this directly with private records and request/result dataclasses. Operational Responsibility does it with a durable event. Observation-Derived Capability does it with source-state grouping. Answer Composition does it with private payloads before compatibility objects. Execution Visibility does it more weakly with report payloads and accessors.

The evidence does not support saying every responsibility is primarily defined this way. Some paths still rely on existing shared `State`, command-local sequencing, cache/store callables, and compatibility report shapes.

### 2. Where is the strongest implementation evidence?

Strongest:

1. Projection Influence Lineage: lineage -> assessment -> justification -> selection -> execution request -> finalized state -> publication request -> visible state.
2. Read-Model Ownership: visible state -> construction inputs -> dependency identity -> lookup request/result -> construction request/result -> publication request/result.
3. Operational Responsibility event handoff: completed tool-call event -> post-execution extraction.

Moderate:

- Answer Composition payloads -> public compatibility object.
- Observation-Derived Capability source grouping -> inventory universe.

Weakest reviewed family:

- Execution Visibility, because its strongest boundary is diagnostic/visibility payload separation inside a compatibility report rather than a full dependency transformation chain.

### 3. Which families instead rely primarily on execution order or shared state?

No completed family relies **only** on execution order, but several retain meaningful order/shared-state dependence:

- Operational Responsibility requires event recording before extraction.
- Observation-Derived Capability derives separated source objects from shared projected `State`.
- Execution Visibility collects command-local measurements and cache statuses in one debug path before formatting/reporting.
- Answer Composition builds several upstream audits before payload composition; the payloads are explicit, but source acquisition is not a uniform dependency chain.

Projection Influence Lineage and Read-Model Ownership are least dependent on implicit ordering because the next boundary's input object is explicit.

### 4. Which dependency transformations recur across families?

Recurring transformations are durable-record handoff, source grouping before presentation, assessment/justification before selection, construction before publication, private payloads before compatibility handoff, and identity-preserving transition of existing state/result objects.

The recurrence is strongest when a function signature consumes the prior object and returns the next object. It is weaker when a report merely groups observed values or when a shared `State` is read and then divided into source sets.

### 5. Does implementation evidence support treating explicit dependency transformation as a repository architectural invariant?

It supports a cautious, bounded invariant:

```text
Recovered responsibility boundaries commonly preserve implementation authority by making the consumed evidence explicit and handing explicit local records, payloads, requests, results, or durable events to downstream responsibilities.
```

It does not support a stronger repository-wide architectural invariant that every responsibility is fundamentally a dependency transformer or that a shared dependency framework should be introduced.

## Supported conclusions

- The repository has not merely been recovering ownership labels. In the strongest completed families, recovery made responsibilities visible by naming what each boundary consumes and what it produces for the next boundary.
- Explicit consumed/produced dependency objects recur across multiple completed families.
- The recurrence is implementation-backed, especially in Projection Influence Lineage and Read-Model Ownership.
- The recurrence remains heterogeneous: durable events, dataclasses, private payloads, source groups, report payloads, and compatibility objects all appear.
- Dependency transformation is stronger than mere execution order in the strongest families because downstream boundaries consume explicit objects produced upstream.
- The implementation does not support a shared dependency ontology, framework, planner, or grammar abstraction.

## Unsupported conclusions

The reviewed evidence does not support concluding that:

- every responsibility in the repository is defined primarily by explicit dependency transformation;
- dependency transformation replaces responsibility ownership as the recovery lens;
- dependency ordering alone proves dependency transformation;
- inquiry identities form one dependency ontology;
- Execution Visibility proves the same invariant as Read-Model Ownership or Projection Influence Lineage;
- a dependency framework, orchestration layer, planner, or common request/result base class should be implemented;
- cache invalidation, scheduling, storage policy, rendering, mutation authority, or ownership should be recovered from this investigation.

## Confidence

Medium-high that explicit consumed/produced dependency handoffs are a recurring implementation pattern across completed responsibility families.

Medium that this recurrence should be treated as an architectural invariant of the recovery methodology.

Low that it should be treated as a universal repository architecture or implementation abstraction.

## Recommended next action

Do not implement anything from this investigation.

Use the finding as a review constraint for future bounded investigations: when a proposed responsibility boundary is investigated, ask what implementation evidence it consumes and what explicit event, request, result, payload, source group, or compatibility handoff it produces. If that evidence is absent, do not infer the boundary from execution sequence or architectural preference alone.

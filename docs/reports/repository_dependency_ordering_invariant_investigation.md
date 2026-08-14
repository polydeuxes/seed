# Repository Dependency Ordering Invariant Investigation

## Scope

This is a bounded implementation investigation into whether explicit dependency ordering recurs across completed responsibility families.

It does not recover ownership, introduce a dependency framework, change runtime behavior, propose planners, or promote new vocabulary. It reviews implementation evidence already present in code and completed family reports.

Reviewed families and investigations:

- Operational Responsibility
- Execution Visibility
- Observation-Derived Capability
- Answer Composition
- Projection Influence Lineage
- Read-Model Ownership
- Architectural Recovery Methodology Characterization
- Evidence Contract Family Investigation
- Inquiry Anchor Dependency-Head Investigation

## Implementation evidence reviewed

### Operational Responsibility

`ToolExecutor._execute_allowed_tool_call(...)` records `tool.call.started`, realizes the registered operation, records failure or completion, and only then invokes post-execution knowledge extraction. The completion path explicitly calls `_record_completed_tool_call(...)`, receives the durable completed event, and passes that event into `_extract_post_execution_knowledge(...)`.

Evidence:

```text
registered operation output
-> tool.call.completed event recorded
-> completed event consumed by post-execution knowledge extraction
-> ToolCallResult returned
```

The implementation therefore supports an ordered transition from execution recording to post-execution extraction. Extraction depends on the completed event existing first.

`operational_responsibility_slice_006.md` records the same boundary as `Execution Recording != Post-Execution Knowledge Extraction` and states that extraction consumes a completed execution record rather than being part of recording.

### Execution Visibility

`execution_visibility_slice_005.md` records an implementation separation between state-build visibility and projection-cache diagnostics. The evidence is not primarily a sequential runtime pipeline; it is an ownership separation inside one report shape:

```text
StateSummaryCacheDebugReport
-> visibility payload
-> projection diagnostics payload
-> compatibility accessors / formatter
```

This supports dependency-preserving handoff into compatibility presentation, but it is weaker evidence for a universal execution-order invariant because the two payloads are separated for visibility and compatibility rather than because one must always complete before the other begins.

### Observation-Derived Capability

`build_capability_inventory(...)` derives the inventory universe from `_inventory_capabilities(...)`, which delegates to `_capability_inventory_sources(state).capability_universe()`. `_capability_inventory_sources(...)` preserves separate source inputs:

- admitted capability knowledge from projected `capability_verified` facts;
- executable operation contract metadata from registered `ToolSpec` records;
- requested capability needs.

`observation_derived_capability_slice_005.md` records the handoff as:

```text
admitted repository capability knowledge
!= executable operation contract metadata

separated inventory sources
-> capability inventory presentation universe
```

This is evidence for construction from bounded prerequisite sources before inventory presentation. It is not evidence that capability admission and executable operation contracts are one ordered pipeline; the implementation keeps them separate and then joins them for presentation.

### Answer Composition

`build_operational_story(...)` first builds supporting evidence surfaces, selects the primary pressure/focus, derives an investigation path from that focus, composes implementation-local answer/reasoning/support/boundary/limitations payloads, and only then creates the public `OperationalStory` compatibility object.

The family completion audit records the recurring answer-composition sequence as:

```text
Repository Knowledge
↓
Answer Composition
  Answer
  Reason
  Supporting Evidence
  Boundary
  Limitations
↓
Compatibility Object
↓
Rendering
```

This is strong evidence that answer objects are downstream of evidence collection and composition. It does not prove that all repository outputs are answers or that all evidence gathering is subject-specific.

### Projection Influence Lineage

`seed_runtime/state.py` contains an explicit chain:

```text
_recover_projection_influence_lineage(events)
-> _assess_replay_scope(lineage)
-> _justify_replay_selection(scope_assessment)
-> _select_replay_targets(justification)
-> _execute_replay_selection(request)
```

The functions preserve distinct prerequisites:

- lineage recovers source event, affected scope, and affected projection evidence;
- scope assessment consumes lineage and answers replay necessity;
- selection justification consumes assessment and preserves why the compatible target set is used;
- replay selection consumes the justification and returns selected targets;
- replay execution consumes the selected request and rejects unsupported target tuples.

The projection influence lineage reports record the same pattern as lineage before assessment, assessment/justification before selection, and selection before execution. This is among the strongest implementation evidence for ordered responsibility transitions.

### Read-Model Ownership

`ReadModelConstructionRequest` is explicitly documented as a request to construct a read model after cache lookup did not reuse one. It consumes already-visible state inputs, an already-derived dependency identity, and an already-resolved cache lookup result. `construct_read_model(...)` then invokes the existing builder with that request.

The same module also has a post-construction cache publication request: `ReadModelCachePublicationRequest` consumes an already-constructed read model and passes it toward existing cache publication.

Evidence:

```text
published/visible State
-> construction inputs
-> dependency identity
-> cache lookup result
-> construction request
-> constructed read model
-> cache publication request
-> cache snapshot publication
```

The read-model ownership reports repeatedly preserve cache lookup before construction and construction before cache publication. This is strong evidence for explicit prerequisites and bounded handoffs.

### Architectural Recovery Methodology Characterization

The methodology evidence is weaker as direct implementation evidence because it is mostly a characterization of repository working method. However, `inquiry_lineage_architectural_projection_slice_methodology.md` states that the repository advanced by completing one responsibility family before moving to another and that responsibility families provide stopping conditions before transition.

That supports a methodological ordering pattern:

```text
bounded family evidence
-> family completion/stopping condition
-> next architectural area
```

It is not sufficient by itself to prove a runtime or repository-wide architectural invariant. It is useful corroborating evidence that completed families were recovered in bounded sequences rather than all at once.

### Evidence Contract Family Investigation

`grammar_observation_evidence_contract_audit.md` records a durable contract where Grammar Observation should consume candidate agreement, independent streams, supporting evidence references, provenance, and non-promotion boundary from Observation Agreement. It also states that Observation Agreement constructs agreement records only after grouping supplied evidence and finding at least two independent streams.

Evidence:

```text
bounded observations
-> independent stream agreement
-> candidate agreement record with provenance/non-promotion
-> downstream grammar visibility consumes emitted agreement
```

This is strong evidence for evidence-before-downstream-observation ordering, while also limiting the claim: downstream consumers should not depend on the current exact text matching algorithm.

### Inquiry Anchor Dependency-Head Investigation

`inquiry_anchor_dependency_head_investigation.md` found that inquiry-like surfaces repeatedly require a surface-local identity before evidence selection and reasoning:

- bounded ask validates exact `question_family` and required arguments before routing;
- Reasoning Path requires `domain` and `subject` before subject/domain evidence filtering;
- Selection Path requires and normalizes `target` before matching implemented selection surfaces;
- Reference Selection branches on `domain` and stops unsupported domains;
- Inquiry Orientation preserves/selects an `InquiryNoteRecord` before lexical evidence matching;
- Source Navigation normalizes `query` before projected source-fact matching;
- Operational Story uses primary pressure/focus selected from pressure evidence before answer composition.

This is strong evidence for identity-before-subject-specific-reasoning, but the investigation explicitly limits the conclusion: these identities are not one ontology, and broad upstream audits can be built before subject-specific filtering.

## Recurring dependency orderings

The following orderings recur across multiple reviewed families with implementation support.

### Established evidence or identity before narrower reasoning

Supported examples:

- Inquiry-like surfaces establish `question_family`, `domain`/`subject`, `target`, selected note, `query`, or primary focus before subject-specific evidence selection and reasoning.
- Answer Composition builds evidence surfaces and payloads before constructing the public answer object.
- Evidence Contract work requires candidate agreement evidence before Grammar Observation consumes it.

Supported conclusion: the implementation repeatedly makes reasoning downstream of some established surface-local dependency.

Unsupported stronger conclusion: the repository has one universal identity, one universal reasoning pipeline, or a single implemented inquiry ontology.

### Verification, admission, or agreement before presentation/promotion-like use

Supported examples:

- Observation-Derived Capability inventory consumes admitted capability facts and registered operation metadata before inventory presentation.
- Evidence Contract work requires independent stream agreement before downstream grammar visibility treats the candidate as consumable evidence.
- Earlier verification-before-promotion phrasing is consistent with this pattern, but the reviewed evidence supports it only where concrete admitted facts, agreement records, or verification facts exist.

Supported conclusion: several families preserve verification/agreement/admission before presentation or downstream use.

Unsupported stronger conclusion: every promotion-like action in the repository is governed by one common verification owner.

### Construction before publication or compatibility handoff

Supported examples:

- Read-Model Ownership constructs read models before cache publication requests.
- Projection Influence Lineage publishes finalized projection state only after replay execution/finalization establishes the visible state.
- Answer Composition composes implementation-local payloads before compatibility object construction and rendering.

Supported conclusion: construction-before-publication/handoff is a recurring implementation structure.

Unsupported stronger conclusion: all construction/publication boundaries are fully recovered or uniformly named.

### Assessment or justification before selection/execution

Supported examples:

- Projection Influence Lineage assesses replay scope, justifies replay selection, selects targets, then executes the selected request.
- Selection Path validates/normalizes a target and matches implemented selection evidence before returning selected or unknown outcomes.
- Reference Selection branches on supported domain before selecting the history reference.

Supported conclusion: assessment/validation/justification before selection is recurring in projection and inquiry-oriented selection surfaces.

Unsupported stronger conclusion: selection never performs any assessment internally; some boundaries remain compressed or only locally explicit.

### Bounded handoff preserving compatibility

Supported examples:

- Operational Responsibility hands durable completed events to fact extraction without changing event shapes.
- Read-Model Ownership hands construction requests/results through existing builders and cache publication without changing read-model semantics.
- Execution Visibility splits payloads while preserving legacy report property accessors.
- Answer Composition builds compatibility objects after internal payload composition.

Supported conclusion: explicit dependency ordering often appears as a compatibility-preserving handoff rather than a new public surface.

## Family-specific orderings

Some orderings are strong locally but should not be promoted to repository-wide rules without more evidence.

- `tool.call.completed` before post-execution fact extraction is specific to registered-operation execution recording.
- State-build visibility vs projection-cache diagnostics is a visibility/report boundary, not a universal runtime order.
- Capability inventory source separation is about joining admitted capabilities, requested capabilities, and executable contracts for presentation; it does not prove those sources are sequentially produced by one pipeline.
- Projection influence lineage's chain from lineage to assessment to justification to selection to execution is very strong locally but tied to projection replay compatibility.
- Read-model cache lookup before construction and construction before cache publication is strong for dependent read models, not necessarily for all repository materialization.
- Inquiry identity-before-reasoning is strong for reviewed inquiry-like surfaces, but the identities differ and some upstream evidence surfaces are built before subject-specific filtering.

## Counterexamples and limits

### Separation is sometimes parallel source composition, not sequential dependency

Observation-Derived Capability inventory joins admitted capabilities, executable operation contracts, and requested capabilities. The implementation preserves separate source ownership before presentation, but the sources are not all ordered prerequisites of each other. This is a counterexample to a universal linear pipeline.

### Visibility decomposition is not always prerequisite execution

Execution Visibility slice 005 separates state-build visibility payloads from projection-cache diagnostic payloads inside a compatibility report. The separation is implementation-backed, but it is not strong evidence that one responsibility must always finish before the other begins.

### Broad evidence surfaces may be built before identity-specific filtering

Reasoning Path builds broad upstream surfaces, including ownership discrepancies, capability needs, pressure, privilege, and operational story, before filtering by `domain` and `subject`. This limits identity-before-reasoning to subject-specific selection and reasoning; it does not mean all data collection waits for the identity.

### Unsupported identities stop reasoning rather than forcing inference

Reference Selection returns unsupported-domain results outside `history`. Selection Path returns an unknown outcome for targets that do not match implemented selection surfaces. These are counterexamples to any claim that establishing a dependency always guarantees a downstream answer.

### Completed reports are not all equally strong implementation evidence

Family reports often describe boundaries after implementation work. They are useful when they point to concrete code and tests, but they cannot alone prove a repository-wide invariant. The strongest claims in this investigation rely on code paths where one object or function consumes another already-established object.

## Answers to central questions

### 1. Does the repository consistently exhibit explicit dependency ordering across completed responsibility families?

Mostly yes across the reviewed completed families, but not as one universal linear sequence.

Implementation repeatedly exhibits structures equivalent to:

```text
Dependency established
-> bounded work
-> handoff
-> next dependency established
```

The strongest examples are Projection Influence Lineage, Read-Model Ownership, Operational Responsibility, Answer Composition, Evidence Contract, and inquiry-like identity-before-reasoning surfaces.

The consistency is architectural rather than lexical: each family uses different objects and different local responsibilities. The repository does not consistently implement one shared dependency framework.

### 2. Where is the strongest implementation evidence?

Strongest evidence:

1. Projection Influence Lineage: lineage recovery feeds scope assessment, selection justification, target selection, and execution.
2. Read-Model Ownership: cache lookup/dependency identity/visible state feed construction requests; constructed read models feed cache publication requests.
3. Operational Responsibility: completed execution events are recorded before fact extraction consumes them.
4. Answer Composition: evidence and payload composition precede compatibility answer objects and rendering.
5. Inquiry Anchor Dependency-Head investigation: surface-local identities precede subject-specific evidence selection and reasoning.
6. Evidence Contract audit: candidate agreement with provenance and non-promotion precedes downstream grammar visibility consumption.

### 3. Which dependency orderings appear repository-wide?

The following orderings recur broadly enough to treat as repository-level patterns:

- established local dependency before narrower responsibility begins;
- evidence/identity before subject-specific reasoning;
- assessment/validation/justification before selection;
- construction before publication or compatibility handoff;
- durable record/evidence before downstream extraction or consumption;
- compatibility-preserving handoff after internal responsibility boundaries.

These are patterns across families, not proof of a single shared mechanism.

### 4. Which observed orderings are family-specific rather than recurring?

Family-specific orderings include:

- `tool.call.started` / implementation realization / `tool.call.completed` / fact extraction in Operational Responsibility;
- state-build visibility vs projection-cache diagnostics in Execution Visibility;
- admitted capability facts plus executable operation contracts plus requested capabilities before capability inventory presentation in Observation-Derived Capability;
- projection lineage to replay assessment/selection/execution in Projection Influence Lineage;
- cache lookup and dependency identity before read-model construction in Read-Model Ownership;
- exact `question_family`, `domain`, `subject`, `target`, note, query, or focus dependencies in inquiry-like surfaces.

Each is implementation-backed locally. None should be renamed into a universal sequence without further evidence.

### 5. Does implementation evidence support treating explicit dependency ordering as a repository architectural invariant?

Yes, with bounded wording.

Supported invariant:

```text
Completed responsibility families repeatedly make one responsibility eligible by first establishing the dependency object, evidence record, validation result, assessment, construction result, or compatibility handoff that the next responsibility consumes.
```

Unsupported invariant:

```text
The repository has one universal dependency framework, one universal grammar, one inquiry identity ontology, or one linear pipeline shared by all families.
```

The evidence supports explicit dependency ordering as a recurring architectural invariant of responsibility eligibility, not as a single global execution model.

## Supported conclusions

- The repository has not only been recovering owners; it has repeatedly been recovering boundaries where one responsibility becomes eligible only after another dependency exists.
- The recurrence crosses completed families: operational execution, projection replay, read-model construction/publication, answer composition, evidence contracts, and inquiry-like surfaces.
- The invariant is dependency-role shaped, not vocabulary shaped. Different families use different objects and different names.
- The most defensible generalization is eligibility ordering: established dependency first, bounded responsibility second, handoff third.
- Many orderings are compatibility-preserving internal changes, which explains why they recur without public schema or CLI churn.

## Unsupported conclusions

- A new dependency framework should be implemented.
- Ownership recovery should be resumed from this investigation.
- Inquiry identities are one ontology.
- The ordering is about language or dependency parsing.
- Every family follows the exact sequence `identity -> validation -> evidence selection -> reasoning -> answer`.
- Every responsibility in the repository executes sequentially rather than through separated or parallel source composition.
- Completed reports alone prove the invariant without code-level handoff evidence.

## Confidence

Medium-high confidence that explicit dependency ordering is a recurring architectural invariant across the reviewed completed responsibility families.

High confidence for Projection Influence Lineage, Read-Model Ownership, Operational Responsibility, Answer Composition, Evidence Contract, and inquiry-like identity-before-reasoning surfaces because concrete code paths consume already-established predecessor objects.

Medium confidence for Execution Visibility and Observation-Derived Capability as evidence for repository-wide ordering because they show boundary-preserving source separation and presentation handoffs, but not always strict sequential prerequisite execution.

Low confidence for any stronger claim that the repository has a universal dependency grammar, universal owner model, or global orchestrator.

## Recommended next action

Do not implement runtime changes, ownership recovery, orchestration, grammar, or a dependency framework from this investigation.

The next action should be a bounded audit only if needed: enumerate a small set of concrete code handoff shapes already present in the repository, distinguishing strict prerequisite ordering from parallel source composition and compatibility presentation. If no operational task depends on that distinction, stop here and treat this report as the current bounded evidence record.

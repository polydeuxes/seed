# Representation Transformation Discipline Investigation

## Scope

This is a bounded implementation investigation of whether current Seed implementation already distinguishes a recurring responsibility shaped like:

```text
representation
  -> bounded transformation
  -> representation
```

This report recovers implementation evidence only. It does not recover ownership, introduce representation abstractions, redesign observations, redesign explanation, introduce automation, introduce planners, or recommend implementation changes.

Repository authority wins.

## Implementation evidence reviewed

Primary implementation evidence reviewed:

- `seed_runtime/observations.py`
  - `Observation`
  - `ObservationIngestor.ingest_many(...)`
  - `ObservationIngestor.observation_to_evidence(...)`
  - `ObservationIngestor.observation_to_fact(...)`
- `seed_runtime/evidence.py`
  - `Evidence`
- `seed_runtime/facts.py`
  - `Fact`
  - `FactSupport`
  - `FactConflict`
- `seed_runtime/state.py`
  - `State`
  - `StateProjector.project_from_state(...)`
  - `StateProjector.finalize(...)`
  - `_project_inferred_facts(...)`
  - `_project_fact_supports(...)`
  - current fact support query methods
- `seed_runtime/explanations.py`
  - `FactExplanation`
  - `BeliefExplanation`
  - `Explanation`
  - `ExplanationBuilder`
- `seed_runtime/context.py`
  - `DecisionInputPacket`
  - `DecisionInputComposer.compose(...)`
- `seed_runtime/inquiry_orientation.py`
  - `InquiryNoteRecord`
  - `RelatedMaterial`
  - `InquiryOrientationView`
  - `_ArchitecturalOrientationEvidence`
  - `_ArchitecturalOrientationAnswer`
  - `build_inquiry_orientation(...)`
- `seed_runtime/operational_story.py`
  - `OperationalStory`
  - `_OperationalStory*Payload` implementation-local payloads
  - `build_operational_story(...)`
  - `_compose_operational_story_payloads(...)`
- `seed_runtime/question_surface_inventory.py`
  - `QuestionSurfaceInventoryRow`
  - `QuestionFamilyDefinition`
  - `ComposedQuestionFamilyExplanation`
  - `build_question_surface_inventory(...)`
  - `build_question_family_definition(...)`
  - `build_composed_question_family_explanation(...)`

Prior investigations reviewed as context, not as authority over code:

- `provider_representation_to_observation_investigation.md`
- `intermediate_structure_responsibility_investigation.md`
- `provider_grammar_to_observation_grammar_investigation.md`
- `implementation_promotion_grammar_recovery_investigation.md`
- `grammar_observation_evidence_contract_audit.md`
- `implementation_evidence_primary_architectural_object_audit.md`
- `expression_composition_explanation_investigation.md`
- `implementation_grammar_visibility_audit.md`
- `structure_observation_substrate_responsibility_audit.md`

Commands used to review implementation evidence included:

```bash
rg --files | rg '(^seed_runtime/|seed_local|explan|inquiry|story|context|observation|evidence|fact)' | head -200
rg "class (Observation|Evidence|Fact|ExplanationBuilder|DecisionInputComposer|OperationalStory|Inquiry|Question|CurrentFact)|def .*fact|def .*evidence|ExplanationBuilder|DecisionInputComposer" -n tests seed_runtime scripts
sed -n '1,260p' seed_runtime/observations.py
sed -n '1,260p' seed_runtime/facts.py
sed -n '893,1160p' seed_runtime/state.py
sed -n '1702,1812p' seed_runtime/state.py
sed -n '1,260p' seed_runtime/explanations.py
sed -n '1,220p' seed_runtime/context.py
sed -n '1,260p' seed_runtime/inquiry_orientation.py
sed -n '1,260p' seed_runtime/operational_story.py
sed -n '1,760p' seed_runtime/question_surface_inventory.py
```

## Implementation representations currently present

The reviewed implementation does not expose one generic `Representation` type. It does, however, define multiple concrete representations with explicit fields and downstream consumers.

| Representation | Implementation evidence | Notes |
| --- | --- | --- |
| Provider-native / source-local representations | Prior investigations found Prometheus JSON, dpkg status text, systemctl JSON stdout, Git stdout, Python source/AST, and local platform/file values. | These are not uniformly modeled by a shared type. Some are decoded directly inside adapters; some first become Seed-owned structural records. |
| Implementation-local structural records | Prior investigations identified `PackageRecord`, `RelationshipFact`, `RepositoryArtifactFact`, and `RepositoryObservation`. | These records are outside the canonical observation model in some paths and become canonical observations in others. |
| Canonical `Observation` | `Observation` stores source type, observed time, subject, predicate, value, confidence, metadata, dimensions, and expiry. | This is the canonical ingestion-facing observed claim shape. |
| `Evidence` | `Evidence` stores workspace, source, kind, observed time, payload, and confidence. | This is provenance/source-payload representation. |
| `Fact` | `Fact` stores subject, predicate, value, dimensions, evidence ids, source type, confidence, observation time, expiry, and optional inference provenance. | This is projected claim representation. |
| Projected `State` | `State` stores facts, observed facts, inferred facts, fact supports, conflicts, evidence, observations, relationships, aliases, entity type assertions, graph issues, goals, tools, and other projected collections. | This is the current inspectable projection over event history. |
| `FactSupport` | `FactSupport` stores subject/predicate/value plus dimensions, supporting fact ids, source types, confidence, observation times, expiry status, predicate semantics, and support kind. | This is the claim-support projection consumed by current fact views and explanations. |
| `FactConflict` | `FactConflict` stores disagreement among facts for a subject/predicate/dimensions group. | This is a projected competing-claim representation consumed by explanations and conflict views. |
| Structured explanation models | `FactExplanation`, `BeliefExplanation`, and `Explanation`. | These are explanation representations produced from projected state/fact supports. |
| `DecisionInputPacket` | Model-facing packet containing current input, goal, entities, facts, tools, open needs, schema, evidence, retry prompt, and budget trace. | This is answer-composition/runtime decision input, not a human explanation. |
| Inquiry orientation records/views | `InquiryNoteRecord`, `RelatedMaterial`, `_ArchitecturalOrientationEvidence`, `_ArchitecturalOrientationAnswer`, and `InquiryOrientationView`. | These are read-only inquiry-orientation representations. |
| Operational story payloads/view | `_OperationalStoryAnswerPayload`, `_OperationalStoryReasoningPayload`, `_OperationalStorySupportingEvidencePayload`, `_OperationalStoryBoundaryPayload`, `_OperationalStoryLimitationsPayload`, and `OperationalStory`. | These are read-only operational explanation/story representations. |
| Question-family inventory/explanation | `QuestionSurfaceInventoryRow`, `QuestionFamilyDefinition`, and `ComposedQuestionFamilyExplanation`. | These represent static inventory metadata and a composed question-family explanation surface. |

## Producer and consumer relationships

### Observation ingestion

`ObservationIngestor.ingest_many(...)` consumes canonical `Observation` objects. For each observation, it produces `Evidence` with `observation_to_evidence(...)`, optionally produces a `Fact` with `observation_to_fact(...)`, and appends observation, evidence, and fact events. The implementation preserves the observation id, source type, subject, predicate, value, metadata, dimensions, expiry, confidence, and observed time into evidence/fact fields where applicable. It removes the canonical `Observation` wrapper at the fact boundary: the fact carries subject/predicate/value/dimensions/evidence ids/source/confidence/time/expiry/inferred status, not observation metadata as first-class fact fields.

Downstream, `StateProjector.apply(...)` consumes the event payloads and rebuilds `State.observations`, `State.evidence`, and `State.facts` from the persisted events.

### Tool result evidence extraction

`FactExtractionService.observe_tool_result(...)` is a counterexample to mandatory Fact production. It consumes successful tool result events and produces `Evidence` only. Its docstring states that the generic service intentionally does not infer facts unless an explicit mapping is added. The produced evidence is then appended as an `evidence.observed` event and later consumed by state projection.

### Event replay and projected state

`StateProjector.project_from_state(...)` consumes ledger events and produces visible projected `State`. Within that path the implementation recovers projection influence lineage, replay assessment, replay justification, replay selection, a replay execution request, a finalized state, and a projection publication. These implementation-local records show transition chaining inside projection itself, but they are scoped to compatible replay/publication evidence rather than domain knowledge modeling.

`StateProjector.apply(...)` decodes event payloads into concrete models: observation events into `Observation`, evidence events into `Evidence`, and fact events into `Fact`. `StateProjector.finalize(...)` then rebuilds derived projections: alias resolver, measurement history retention, inferred facts, observed/inferred partitions, fact supports, relationships, entity type assertions, graph issues, aliases, and conflicts.

### Fact promotion and inference

Observed `Fact` instances are produced by ingestion. Inferred facts are produced in `_project_inferred_facts(...)`, which consumes current observed source facts selected by `_current_belief_source_facts(...)` and calls `infer_facts(...)`. The implementation preserves source fact and inference rule provenance on inferred facts when the inference layer supplies it, and partitions observed vs inferred facts before recombining them into `state.facts`.

This is an explicit transformation from current observed fact representation to inferred fact representation, but it is compressed because inference-rule internals are outside the reviewed code path and not all fact production comes from inference.

### Fact support projection

`_project_fact_supports(...)` consumes iterable `Fact` records and produces `FactSupport` records. Its authority is grouping and support aggregation by subject, predicate, dimensions, and value, with special treatment for measurement predicates. Durable facts aggregate all supporting fact ids, source types, confidence, earliest/latest observation time, and expiry. Measurement predicates intentionally collapse to the latest current sample with `support_kind="current_sample"`; repeated historical samples do not strengthen support in the same way.

Downstream, `State.get_fact_supports(...)`, `State.get_fact_support(...)`, current fact views, CLI fact-support/current-facts surfaces, `ExplanationBuilder`, Inquiry Orientation, and several audits consume this support representation.

### ExplanationBuilder

`ExplanationBuilder.why(...)` consumes projected `State`, especially fact supports, fact conflicts, facts, evidence ids, alias resolution, and predicate cardinality. It produces `Explanation`, which contains current beliefs, competing beliefs, optional conflict, and nested fact explanations.

Its authority is bounded to deterministic explanation of current/ambiguous/no-current-belief state for one subject/predicate query. It does not ingest observations, infer facts, write events, mutate state, or render prose. It intentionally removes raw event payloads and full evidence payloads from explanation output: explanations carry evidence ids and fact/evidence linkage rather than embedding all evidence payload content.

Downstream consumers are tests, CLI explanation formatting paths, and any model/operator surface that asks for why-style structured fact provenance.

### DecisionInputComposer

`DecisionInputComposer.compose(...)` consumes `State`, an input `Event`, and visible tools from `ToolRegistry`. It orders goals, entities, facts, and evidence, applies a `ContextBudget`, attaches selected evidence payloads only for fact evidence that survived evidence budget selection, and produces `DecisionInputPacket`.

Its authority is model-context selection and shaping. It removes unselected facts/evidence/goals/entities under budget, removes inferred-only provenance fields from non-inferred fact payloads, and preserves the context-budget trace. Downstream, runtime/model decision code consumes `DecisionInputPacket`.

This is a clear representation-to-representation transition, but it consumes multiple related representations from `State` plus registry tools and the current input event. It is therefore not strict evidence for a universal "one input representation only" discipline.

### Inquiry Orientation

`build_inquiry_orientation(...)` consumes projected `State` and an `InquiryNoteRecord`, calls `_compose_architectural_orientation_answer(...)`, and produces `InquiryOrientationView`. The intermediate `_ArchitecturalOrientationEvidence` holds collected `RelatedMaterial`; `_ArchitecturalOrientationAnswer` holds answer material, reason, support, boundary, and limitations before rendering.

Its authority is deterministic lexical overlap between a preserved inquiry note and existing projected fact supports/source-navigation matches. It intentionally removes semantic intent, planning, routing, ownership, importance, and action recommendations; its authority boundary says lexical overlap does not assert operator intent or next safe move.

Downstream, `format_inquiry_orientation(...)` renders the view.

### Operational Story

`build_operational_story(...)` consumes operational read-model/audit outputs: pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path audit. `_compose_operational_story_payloads(...)` transforms those into separate answer, reasoning, supporting-evidence, boundary, and limitations payloads, and then `build_operational_story(...)` produces `OperationalStory`.

Its authority is read-only operational explanation from already-existing visibility surfaces. It preserves focus, pressure, capabilities, constraints, correlation gaps, impact, recent changes, observed outcomes, investigation path, support, unknowns, and boundary flags. It intentionally removes provider acquisition, recording, event-ledger writes, cluster mutation, and planning authority. Downstream, `operational_story_json(...)` and `format_operational_story(...)` consume `OperationalStory`.

This is strong evidence of bounded transformation, but not of a single-input rule: the story consumes several operational surfaces.

### Question-family explanation

`build_question_surface_inventory(...)` produces `QuestionSurfaceInventoryRow` records from static implementation maps, diagnostic inventory names, and diagnostic shape specs. `build_question_family_definition(...)` consumes inventory rows and produces `QuestionFamilyDefinition`. `build_composed_question_family_explanation(...)` consumes the definition and produces `ComposedQuestionFamilyExplanation` with ordered sections for definition, answer responsibility, boundary, and diagnostic relationship.

Its authority is static read-only question-family visibility. It removes routing/inference beyond inventory mappings, does not dispatch operator questions, and does not execute diagnostics. Downstream, JSON and human formatters consume the definition and composed explanation representations.

## Recurring transformation evidence

The implementation repeatedly uses named functions or builders to cross representation boundaries:

1. `Observation` -> `Evidence` via `observation_to_evidence(...)`.
2. `Observation` + `Evidence` -> `Fact` via `observation_to_fact(...)`.
3. tool completion `Event` -> `Evidence` via `FactExtractionService.observe_tool_result(...)`.
4. ledger `Event` payloads -> projected `State` collections via `StateProjector.apply(...)`.
5. projected `State` facts -> inferred `Fact` records via `_project_inferred_facts(...)` and `infer_facts(...)`.
6. `Fact` records -> `FactSupport` records via `_project_fact_supports(...)`.
7. `FactSupport` + facts/conflicts/aliases -> structured `Explanation` via `ExplanationBuilder.why(...)`.
8. `State` + input event + registry tools -> `DecisionInputPacket` via `DecisionInputComposer.compose(...)`.
9. `State` + `InquiryNoteRecord` -> `_ArchitecturalOrientationEvidence` -> `_ArchitecturalOrientationAnswer` -> `InquiryOrientationView`.
10. operational read models/audits -> `_OperationalStory*Payload` records -> `OperationalStory`.
11. question-family inventory rows -> `QuestionFamilyDefinition` -> `ComposedQuestionFamilyExplanation`.

These are not accidental identical shapes. The functions and dataclasses name the consumed and produced representations, and the code preserves some fields while discarding others at each boundary.

## Intentionally preserved and removed information

| Transition | Preserved | Removed or bounded out |
| --- | --- | --- |
| Observation -> Evidence | observation id, source type, subject, predicate, value, metadata, dimensions, expiry, confidence, observed time | Fact claim status; evidence is source payload/provenance, not current truth. |
| Observation + Evidence -> Fact | subject, predicate, value, dimensions, evidence id, source type, confidence, observed time, expiry, inferred flag | Observation metadata becomes non-first-class for facts; evidence payload is referenced, not embedded. |
| Tool event -> Evidence | tool name/source, event output payload, workspace/session/causation/correlation, event timestamp | Fact inference is intentionally absent in generic extraction. |
| Events -> State | typed observations, evidence, facts, and derived state collections | Raw event stream order is not the read-model API; projection summarizes into typed collections and indexes. |
| Facts -> FactSupport | subject, predicate, value/current sample, dimensions, support fact ids, source types, confidence, observation times, expiry, semantics/support kind | Raw duplicate fact rows as the current surface; expired facts by default; old measurement samples by default. |
| FactSupport/facts -> Explanation | current/competing belief structure, support confidence, fact ids, evidence ids, source types, observation times, inference provenance, alias resolution chains, conflicts | Full raw event/evidence payloads, mutation authority, prose rendering. |
| State/input/tools -> DecisionInputPacket | selected current input, goal, entities, facts, tools, open needs, evidence, schema, budget trace | Unselected material under budget; non-inferred fact source/inference fields; invisible tools. |
| Inquiry note + State -> InquiryOrientationView | raw note, related material, support strings, surface family, uncertainty, authority boundary | Semantic intent, ownership, priority, routing, plan/action recommendation, mutation. |
| Operational audits -> OperationalStory | focus, pressure, support, capabilities, constraints, gaps, impact, outcomes, investigation path, unknowns, read-only boundary | Recording, event writes, provider acquisition, cluster mutation, operational planning. |
| Question-family inventory -> composed explanation | definition, answer responsibility, boundary, diagnostic relationship, implementation reason | Question dispatch/execution, arbitrary explanation logic, architectural redesign. |

## Explicit representation transitions

The following transitions are explicit enough to treat as implementation-backed recurring evidence:

- Canonical observation promotion is explicit because `ObservationIngestor` has named conversion functions for evidence and facts.
- Fact support projection is explicit because `FactSupport` is a model and `_project_fact_supports(...)` has separate durable vs measurement support construction.
- Structured fact explanation is explicit because `ExplanationBuilder` produces named `Explanation`, `BeliefExplanation`, and `FactExplanation` models from `State` support queries.
- Decision input composition is explicit because `DecisionInputPacket` is a dataclass and `DecisionInputComposer.compose(...)` deterministically selects and serializes state and registry material into that packet.
- Inquiry Orientation is explicit because implementation-local evidence and answer dataclasses separate evidence collection from answer/view rendering.
- Operational Story is explicit because implementation-local answer/reasoning/support/boundary/limitations payloads are composed before the public story object.
- Question-family explanation is explicit because inventory row, definition, and composed explanation are separate dataclasses with named builder functions.

## Transitions that remain implementation-compressed

The following remain compressed or non-uniform:

- Provider-native representation -> canonical `Observation` is not uniformly staged. Prior investigations found some explicit intermediate records, while Prometheus/Systemd/local host paths still combine provider decoding, identity choice, predicate choice, and observation construction inside source adapters.
- `Evidence` -> `Fact` is explicit for canonical observations, but generic tool-output evidence intentionally stops at evidence. There is no universal evidence-to-fact promotion responsibility.
- Inference from current observed facts to inferred facts is explicit at `_project_inferred_facts(...)`, but the detailed inference-rule transformation is delegated to `infer_facts(...)` and the inference catalog, so this report should not overstate one uniform transformation grammar.
- Current fact views were part of the requested review, but the core implementation evidence reviewed here shows current fact support access and CLI/view consumption rather than one universal current-fact representation independent of `FactSupport`.
- Answer Composition is not one subsystem. ExplanationBuilder, DecisionInputComposer, Inquiry Orientation, Operational Story, and Question-family explanation each compose bounded outputs locally.
- Several surfaces consume multiple related representations, not one. Operational Story consumes multiple audits/read models; DecisionInputComposer consumes state sections, tools, and current input; Inquiry Orientation consumes note records plus state-derived matches.

## Counterexamples and limits

The implementation does not support the strongest possible claim that every responsibility consumes exactly one representation and produces exactly one representation.

Counterexamples:

1. `ObservationIngestor.observation_to_fact(...)` consumes both `Observation` and `Evidence` to produce a `Fact` because the fact must link to evidence ids.
2. `DecisionInputComposer.compose(...)` consumes `State`, `Event`, and `ToolRegistry` material to produce a packet.
3. `build_operational_story(...)` consumes several operational audit/read-model outputs, not one upstream representation.
4. `FactExtractionService.observe_tool_result(...)` produces evidence but intentionally no fact, so representation transformation does not always proceed to the next knowledge representation.
5. Provider adapters are non-uniform: some paths have structural intermediate records, while others directly produce canonical observations from provider-local data.
6. Explanation composition exists as multiple surface-local builders, not as one generalized explanation subsystem.

These counterexamples prevent a conclusion that Seed has a uniform, formal representation-transformation abstraction or a strict one-input/one-output rule.

## Answers to central questions

### 1. What implementation representations currently exist?

Current implementation representations include provider-native/source-local payloads, implementation-local structural records, canonical `Observation`, `Evidence`, `Fact`, projected `State`, `FactSupport`, `FactConflict`, structured explanation models, `DecisionInputPacket`, inquiry-orientation records/views, operational-story payloads/views, and question-family inventory/definition/composed-explanation records.

### 2. Which responsibilities consume each representation?

- Provider-native/source-local payloads are consumed by observation providers/adapters and structural extraction helpers.
- Implementation-local structural records are consumed by canonical observation emitters, repository/source navigation surfaces, or self-model/reconciliation paths depending on the record.
- `Observation` is consumed by `ObservationIngestor` and state projection when replaying observation events.
- `Evidence` is consumed by state projection, fact explanation support, context composition, confidence/contradiction/operational audits, and fact provenance consumers.
- `Fact` is consumed by state finalization, inference, fact support projection, relationship projection, current fact views, ExplanationBuilder, context composition, and many diagnostics/audits.
- `FactSupport` is consumed by current fact queries/views, ExplanationBuilder, Inquiry Orientation, and operational/diagnostic views that need supported current claims.
- Structured explanation models are consumed by explanation JSON/human surfaces and tests.
- `DecisionInputPacket` is consumed by model/runtime decision paths.
- Inquiry, operational-story, and question-family representations are consumed by their JSON/human formatters and tests.

### 3. Which responsibilities produce each representation?

- Provider adapters and source readers produce provider-native/source-local payloads.
- Structural extraction/parsing helpers produce implementation-local structural records.
- Observation sources and normalizers produce canonical `Observation` records.
- `ObservationIngestor` and `FactExtractionService` produce `Evidence`.
- `ObservationIngestor`, CLI fact seeding, event replay, and inference produce `Fact` records.
- `StateProjector` produces projected `State`.
- `_project_fact_supports(...)` produces `FactSupport`.
- `_project_fact_conflicts(...)` produces `FactConflict`.
- `ExplanationBuilder` produces structured explanations.
- `DecisionInputComposer` produces `DecisionInputPacket`.
- Inquiry Orientation builders produce inquiry-orientation representations.
- Operational Story builders produce story payloads and `OperationalStory`.
- Question-family inventory/explanation builders produce inventory rows, definitions, and composed explanations.

### 4. Does implementation consistently transform one representation into another under bounded authority?

Yes, in the weaker implementation-backed sense: many responsibilities are bounded transformations between named concrete representations, with explicit preservation/removal choices. No, in the stronger literal sense: the implementation does not consistently restrict each responsibility to exactly one consumed representation, and it does not centralize this pattern in a shared abstraction.

The best-supported conclusion is that Seed shows a recurring **bounded representation transition** discipline across multiple families, not a universal one-input/one-output representation architecture.

### 5. Which representation transitions are already explicit?

Explicit transitions include Observation -> Evidence, Observation + Evidence -> Fact, tool event -> Evidence, event payloads -> projected State collections, facts -> FactSupport, FactSupport/facts/conflicts/aliases -> structured Explanation, State/input/tools -> DecisionInputPacket, note/state matches -> InquiryOrientationView, operational audits -> OperationalStory, and question-family inventory -> definition -> composed explanation.

### 6. Which remain implementation-compressed?

Compressed transitions include provider-native data -> Observation in several provider adapters, generic Evidence -> Fact promotion outside observation ingestion, inference-rule internals, current fact view representation boundaries that are mostly support/view surfaces rather than separate domain models, and any generalized Answer Composition boundary.

### 7. Does implementation evidence support a recurring representation-transformation discipline?

Yes, with bounded confidence. The implementation repeatedly names representation models and builder/projector/composer functions that consume one or more concrete representations, exercise local authority, and produce another concrete representation. The recurrence is visible across observations, evidence, facts, fact support, explanations, inquiry orientation, operational story, decision input composition, and question-family explanation.

However, implementation evidence does not support a claim that the discipline is universal, abstracted, or always one-input/one-output. The recurrence is implementation-local and surface-specific.

### 8. If so, what implementation vocabulary best characterizes that recurrence?

The safest vocabulary is:

> bounded representation transition

This vocabulary is implementation-backed because the code repeatedly uses bounded builders/projectors/composers/converters to turn one concrete representation set into another while preserving selected evidence and removing out-of-scope authority.

Secondary vocabulary supported by specific surfaces:

- `conversion` for `ObservationIngestor.observation_to_evidence(...)` and `observation_to_fact(...)`.
- `projection` for `StateProjector`, `_project_fact_supports(...)`, relationships, conflicts, and state finalization.
- `composition` for `ExplanationBuilder`, `DecisionInputComposer`, Inquiry Orientation, Operational Story, and question-family explanation.
- `selection` for current belief, context budget, inquiry related material, and operational primary pressure.

Unsupported vocabulary:

- A generalized `Representation` abstraction.
- A single explanation subsystem.
- A universal ownership boundary.
- A uniform provider-to-observation grammar across all providers.
- A strict one-input/one-output transformation law.

## Supported conclusions

1. Implementation currently contains multiple concrete representations, not one generic representation abstraction.
2. Many responsibilities are bounded transformations between those concrete representations.
3. Observation ingestion, fact support projection, ExplanationBuilder, Inquiry Orientation, Operational Story, DecisionInputComposer, and question-family explanation all show named transformation boundaries.
4. The recurring pattern is strongest where the implementation has explicit dataclasses/models on both sides of the boundary.
5. The recurring pattern is weaker in provider adapters and generalized answer composition because responsibilities remain compressed or surface-local.
6. The implementation-backed discipline is best characterized as bounded representation transition, with local variants named conversion, projection, selection, and composition.

## Unsupported conclusions

The reviewed implementation does not support concluding that:

- Seed has or needs a shared `Representation` abstraction.
- Every transformation consumes exactly one representation.
- Every transformation produces exactly one downstream representation.
- Evidence always promotes to facts.
- Provider-native representations are uniformly decoded into intermediate structural records before observations.
- Explanation composition is a single subsystem.
- Presentation vocabulary should become preserved knowledge without reachability evidence.
- Any ownership recovery follows from these transitions.

## Confidence

Confidence: **medium-high** for the existence of recurring bounded representation transitions across the reviewed families.

Confidence: **low** for any stronger claim that implementation follows a uniform formal representation-transformation architecture.

The distinction matters: repository evidence supports a recurring implementation discipline, but it remains local, concrete, and non-uniform.

## Recommended next investigation

Recommended next investigation:

> Determine whether provider-native-to-observation paths should be described as multiple adapter-local transition shapes or whether implementation evidence already supports a narrower recurring provider decoding discipline.

This should remain evidence recovery only. It should focus on provider/source adapters where the current investigation found compression: Prometheus, Systemd, local host files/platform values, repository source observation, package records, relationship facts, and observation normalizers. It should not introduce abstractions or redesign providers.

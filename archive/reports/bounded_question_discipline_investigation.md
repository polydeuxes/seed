# Bounded Question Discipline Investigation

## 1. Executive summary

This investigation finds **partial but real implementation support** for a recurring discipline that often looks like:

```text
bounded question -> bounded work -> bounded answer -> next responsibility
```

The recurrence is strongest where implementation already has explicit query or answer surfaces: `ExplanationBuilder.why(...)`, `DecisionInputComposer.compose(...)`, bounded `ask --question-family`, Inquiry Orientation, Operational Story composition, and capability promotion-readiness inspection. In those areas, code names, docstrings, return shapes, boundary fields, and tests show responsibilities answering narrow questions and preserving explicit non-authority over adjacent questions.

The recurrence is also present, but less explicitly named as questions, in Observation, Evidence, Fact promotion, and Fact support. Those responsibilities are implementation-backed as bounded work and bounded answers, but their question discipline is inferred from shapes and handoffs rather than represented as first-class question objects. Observation answers what was observed. Evidence answers what provenance payload supports later facts. Fact promotion answers whether an observation becomes a projected fact, with an explicit suppression counterexample. Fact support answers which current facts support a subject/predicate/value and whether support is aggregate or current-sample.

The repository does **not** support a conclusion that Seed has a universal Question abstraction, universal inquiry ontology, or uniform question pipeline. Current implementation supports a **local, repeated discipline of bounded answer surfaces with authority boundaries**, not a generalized architecture of Questions.

## 2. Implementation evidence reviewed

Primary implementation evidence reviewed:

- `seed_runtime/observations.py`: canonical `Observation`, ingestion to observation/evidence/fact events, fact-promotion suppression.
- `seed_runtime/evidence.py`: provenance `Evidence` shape.
- `seed_runtime/facts.py`: `FactSupport` shape and semantics.
- `seed_runtime/state.py`: projection of observations, evidence, facts, and fact supports.
- `seed_runtime/explanations.py`: `ExplanationBuilder.why(...)` and explanation result shapes.
- `seed_runtime/context.py`: `DecisionInputComposer.compose(...)` and `DecisionInputPacket`.
- `seed_runtime/inquiry_orientation.py`: inquiry note recording, evidence collection, answer composition, uncertainty, and authority boundary.
- `seed_runtime/question_surface_inventory.py`: question-family inventory, dispatch eligibility, required arguments, composed question-family explanation.
- `scripts/seed_local.py`: bounded `ask --question-family` dispatch behavior.
- `seed_runtime/operational_story.py`: operational answer/reason/support/boundary/limitations payload composition.
- `seed_runtime/capability_promotion_readiness.py`: read-only promotion-readiness inspection.

Relevant existing investigation/readiness documents reviewed for implementation-backed context and counterpressure:

- `docs/inquiry_presentation_answer_implementation_audit.md`.
- `docs/why_not_explanation_characterization.md`.
- `docs/decision_model_context_naming_audit.md`.
- `intermediate_structure_responsibility_investigation.md`.
- `responsibility_authority_frontier_reconciliation.md`.
- `repository_program_identity_investigation.md`.

## 3. Responsibility-by-responsibility question inventory

### 3.1 Observation

| Question inventory item | Implementation-backed answer |
| --- | --- |
| Prerequisite question already answerable | A source/provider has produced a concrete subject, predicate, value, timestamp, confidence, and metadata acceptable to the canonical observation shape. |
| Question answered by responsibility | “What was observed from which source type, with what confidence and dimensions?” |
| Intentionally unanswered | Whether the observation is true cluster knowledge, sufficient evidence, selected support, a decision input, or an explanation. |
| Downstream question made answerable | Evidence can ask what provenance payload supports the observed signal; fact promotion can ask whether the observation should become a fact. |
| Implementation evidence | `Observation` requires source type, timestamp, subject, predicate, value, confidence, metadata, dimensions, and optional expiry. `ObservationIngestor.ingest_many(...)` emits an `observation.observed` event before evidence and optional fact events. |

Observation is strongly bounded as acquisition output, but not every observation path has an explicit named question object. The discipline is implementation-backed through required fields and event ordering rather than a question abstraction.

### 3.2 Evidence

| Question inventory item | Implementation-backed answer |
| --- | --- |
| Prerequisite question already answerable | An observation or source payload exists and can be preserved as provenance. |
| Question answered by responsibility | “What observed source payload supports later understanding?” |
| Intentionally unanswered | Whether a fact is current, selected, conflicting, sufficient, or explanatory. |
| Downstream question made answerable | Fact promotion and fact support can refer to evidence IDs; explanation can list evidence behind supporting facts. |
| Implementation evidence | `Evidence` preserves workspace, source, kind, observed time, payload, and confidence. `observation_to_evidence(...)` copies observation identity, source type, subject, predicate, value, metadata, dimensions, and expiry into an evidence payload. |

Evidence therefore answers a provenance question, not a truth-selection question.

### 3.3 Fact promotion

| Question inventory item | Implementation-backed answer |
| --- | --- |
| Prerequisite question already answerable | Observation and evidence have been created for a candidate observed claim. |
| Question answered by responsibility | “Should this observation become an observed or inferred fact event?” |
| Intentionally unanswered | Whether the fact wins current support, whether it is explained, whether it authorizes action, or whether diagnostics should mutate cluster truth. |
| Downstream question made answerable | Fact support can group facts; explanations and decision input can consume projected facts. |
| Implementation evidence | `ObservationIngestor.ingest_many(...)` creates evidence for every observation, calls `_should_suppress_fact_promotion(...)`, and only appends `fact.observed`/`fact.inferred` if a fact is returned. `observation_to_fact(...)` attaches evidence IDs and preserves confidence, dimensions, source type, expiry, and inferred status. |

This is one of the clearest bounded-question seams because the Prometheus suppression function proves that observation and evidence can proceed while fact promotion intentionally withholds fact creation.

### 3.4 Fact support

| Question inventory item | Implementation-backed answer |
| --- | --- |
| Prerequisite question already answerable | Projected facts exist, with subject, predicate, value, dimensions, evidence IDs, confidence, source type, and time. |
| Question answered by responsibility | “Which projected facts currently support this subject/predicate/value claim, and how should support be characterized?” |
| Intentionally unanswered | Why a user should believe a claim in narrative terms, what action should happen, and whether unsupported or missing facts are false. |
| Downstream question made answerable | `ExplanationBuilder` can explain current, ambiguous, or absent current beliefs; integrity and decision surfaces can consume selected fact/evidence material. |
| Implementation evidence | `FactSupport` carries subject, predicate, value, dimensions, supporting fact IDs, source types, confidence, observed/latest observed times, expiry, predicate semantics, and support kind. `_project_fact_supports(...)` groups facts and distinguishes durable aggregate support from measurement current samples. |

Fact support is explicitly a support projection, not explanation or decision authority.

### 3.5 ExplanationBuilder

| Question inventory item | Implementation-backed answer |
| --- | --- |
| Prerequisite question already answerable | Projected state can provide fact supports and conflicts for a subject/predicate. |
| Question answered by responsibility | “Why is this subject/predicate current, ambiguous, or not currently believed?” |
| Intentionally unanswered | Dedicated `why-not(subject, predicate, value)` taxonomy, missing-observation proof, disproof, action selection, and mutation. |
| Downstream question made answerable | A caller can present current beliefs, competing beliefs, conflict, recursive fact provenance, evidence IDs, and entity-resolution chain. |
| Implementation evidence | `ExplanationBuilder.why(...)` returns statuses `current`, `ambiguous`, or `no_current_belief` from projected fact supports and conflicts. `Explanation` explicitly separates current and competing beliefs for future modes without changing reasoning behavior. Existing why-not characterization confirms missing observation/evidence is not disproof and that dedicated why-not is not currently implemented. |

ExplanationBuilder is a strong implementation-backed question owner: it owns a `why` question over projected state and avoids broader why-not/action authority.

### 3.6 DecisionInputComposer

| Question inventory item | Implementation-backed answer |
| --- | --- |
| Prerequisite question already answerable | Projected state, current input event, registry-visible tools, and budget rules exist. |
| Question answered by responsibility | “What bounded input packet should be supplied to decision production?” |
| Intentionally unanswered | What decision to make, whether to plan, how to execute, and whether inquiry semantics should be inferred from context. |
| Downstream question made answerable | A decision producer can ask which response kind is allowed using current input, active goal, selected facts/evidence/entities/tools/open tool needs, and schema. |
| Implementation evidence | `DecisionInputComposer.compose(...)` orders state material, budget-selects sections, embeds evidence only when selected, lists visible tools, and returns a `DecisionInputPacket` with a finite decision schema. Existing naming audit rejects planner/reasoning-engine/inquiry-engine/autonomous-orchestrator names because implementation only supports bounded decision input and proposed decision production. |

DecisionInputComposer is bounded work that authorizes a downstream decision question without answering it.

### 3.7 Inquiry Orientation

| Question inventory item | Implementation-backed answer |
| --- | --- |
| Prerequisite question already answerable | A raw inquiry note exists in the isolated probe store, and projected read models/source navigation are available. |
| Question answered by responsibility | “What existing projected or source-navigation material is lexically related to this preserved operator note?” |
| Intentionally unanswered | Whether the note is a fact, claim, goal, requirement, authorization, command, intent, ownership claim, recommendation, or next safe move. |
| Downstream question made answerable | A human or later surface can see related material, support strings, uncertainty, and boundary before deciding whether further investigation is warranted. |
| Implementation evidence | `AUTHORITY_BOUNDARY` explicitly states the note is not fact/claim/goal/tool need/requirement/capability/decision/proposal/plan/authorization/command/runtime instruction and that matches are deterministic lexical overlaps only. `_collect_architectural_orientation_evidence(...)` gathers fact and source-navigation matches, then `_compose_architectural_orientation_answer(...)` returns answer, reason, support, boundary, and limitations. |

Inquiry Orientation strongly follows bounded question discipline and strongly rejects promotion from presentation vocabulary to knowledge.

### 3.8 Bounded ask and Question-family explanation

| Question inventory item | Implementation-backed answer |
| --- | --- |
| Prerequisite question already answerable | The operator names an exact registered `QuestionFamily`; required surface arguments are explicitly provided where needed. |
| Question answered by responsibility | “Which existing bounded answering surface is responsible for this exact question family?” and, for presentation, “What definition, answer responsibility, boundary, and diagnostic relationship describe it?” |
| Intentionally unanswered | Free-text semantic routing, unknown family inference, diagnostic-only answering, and missing parameter inference. |
| Downstream question made answerable | The selected surface can answer its bounded question, or presentation can show question-family definition/explanation. |
| Implementation evidence | `bounded_status_for_question_family(...)` derives eligibility from exact maps; `apply_bounded_ask_dispatch(...)` rejects unknown families, rejects free-text misuse, enforces required surface argument counts, blocks diagnostic-only families as answer surfaces, and sets the mapped surface flag. `build_composed_question_family_explanation(...)` composes definition, answer responsibility, boundary, and diagnostic relationship from existing question-family definition fields. |

This is the most explicit implementation of question-family discipline, but it is a dispatcher to existing surfaces, not a universal inquiry engine.

### 3.9 Operational Story

| Question inventory item | Implementation-backed answer |
| --- | --- |
| Prerequisite question already answerable | Existing audits can provide pressure, capability needs, privilege discovery, correlation findings, impact metrics, and investigation path. |
| Question answered by responsibility | “What current operational story is justified by existing visibility surfaces?” |
| Intentionally unanswered | Planning, recording, event-ledger writes, cluster mutation, and facts creation. |
| Downstream question made answerable | Operators can see focus, pressure, evidence, constraints, gaps, impact, recent changes, outcomes, investigation path, unknowns, and boundary. |
| Implementation evidence | `build_operational_story(...)` composes existing audits, then `_compose_operational_story_payloads(...)` separates answer, reasoning, supporting evidence, boundary, and limitations payloads. The boundary payload states read-only mode, `records_facts=False`, `writes_event_ledger=False`, and `mutates_cluster=False`. |

Operational Story has a strong answer-composition discipline, but it is a composition surface rather than a primitive inquiry abstraction.

### 3.10 Existing inquiry/readiness/responsibility investigations

| Investigation family | Implementation-backed contribution |
| --- | --- |
| Inquiry-oriented investigations | Existing audit states exact question-family inquiry currently reaches the family-owned answering surface and that `--question-family-explanation` is a separate presentation composition surface. |
| Readiness investigations | Capability promotion readiness asks whether future promotion would be supportable, while explicitly not promoting, selecting, authorizing, evaluating policy, invoking tools, or executing. |
| Responsibility recovery investigations | Existing reconciliation documents consistently caution against promoting bounded local identities into universal ontology or ownership recovery. |

These documents support the investigation's cautious conclusion: the implementation repeatedly creates bounded answer surfaces and boundaries, but prior investigations warn against overgeneralizing those repetitions into universal representations or abstractions.

## 4. Recurring inquiry discipline

### 4.1 Supported recurrence

The following recurrence is supported by implementation evidence in multiple slices:

1. **A prerequisite answer must already exist.**
   - Observation requires source-shaped data.
   - Evidence requires an observed payload.
   - Fact promotion requires observation plus evidence.
   - Fact support requires projected facts.
   - Explanation requires fact supports and conflicts.
   - Decision input requires projected state, input event, tool registry, and budget selection.
   - Bounded ask requires an exact registered question family.
   - Operational Story requires existing audit outputs.

2. **The responsibility performs bounded work.**
   - Ingestion emits events in a fixed sequence.
   - Support projection groups facts and handles measurement predicates differently from durable predicates.
   - Explanation traverses projected state provenance deterministically.
   - Inquiry Orientation performs deterministic lexical matching only.
   - Operational Story composes already existing surfaces.

3. **The responsibility returns a bounded answer shape.**
   - `Evidence`, `Fact`, `FactSupport`, `Explanation`, `DecisionInputPacket`, `InquiryOrientationView`, `ComposedQuestionFamilyExplanation`, `OperationalStory`, and `CapabilityPromotionReadinessInspection` are explicit answer/result records.

4. **The responsibility preserves authority boundaries.**
   - Suppressed fact promotion proves observation/evidence does not automatically become fact truth.
   - Inquiry Orientation's boundary rejects fact/intent/ownership/action promotion.
   - Operational Story exposes read-only/no-record/no-ledger/no-cluster-mutation boundary.
   - Promotion readiness exposes “readiness not promotion” boundary notes.
   - Question-family dispatch rejects unknown, diagnostic-only, and under-parameterized asks.

### 4.2 What is not supported

The implementation does not support these stronger claims:

- That every responsibility is best modeled as a `Question` object.
- That Seed has a universal inquiry ontology.
- That all responsibilities expose the same answer grammar.
- That inquiry dispatch performs semantic free-text routing.
- That ExplanationBuilder implements a complete why-not or missing-evidence taxonomy.
- That operational composition authorizes plans, proposals, execution, or cluster mutation.

## 5. Counterexamples and failure points

### 5.1 Responsibilities with bounded work but implicit questions

Observation, Evidence, Fact promotion, and Fact support answer bounded questions, but the questions are inferred from implementation shapes and handoffs. The implementation does not encode them as explicit QuestionFamily rows. This weakens any claim of consistent inquiry discipline across all layers.

### 5.2 Direct observation-to-fact promotion is default

`ObservationIngestor.ingest_many(...)` normally creates observation, evidence, and fact events in one batch. Although this preserves ordering and provenance, it means the promotion question is mostly implicit and automatic except for explicit suppression cases. This is bounded work, but not a rich deliberative inquiry stage.

### 5.3 Explanation is positive/current-belief oriented

`ExplanationBuilder.why(...)` explains current, ambiguous, or no-current-belief states, but existing why-not characterization shows missing observation/evidence does not become disproof and no dedicated why-not value query exists. Therefore explanation discipline is bounded, not complete.

### 5.4 Inquiry dispatch is exact, not semantic

`ask --question-family` is implementation-backed but intentionally narrow. It does not prove a general inquiry system; it proves exact family dispatch to existing surfaces.

### 5.5 Operational Story composes surfaces opportunistically from current audits

Operational Story has strong payload separation, but it depends on available audit surfaces and reports unknowns when inputs are missing. It does not prove every downstream operational question has a prerequisite gate.

## 6. Supported conclusions

1. **Many responsibilities are implementation-backed owners of bounded answers to bounded questions.**
   Observation, Evidence, Fact promotion, Fact support, ExplanationBuilder, DecisionInputComposer, Inquiry Orientation, bounded question-family dispatch, Operational Story, and Promotion Readiness all show bounded inputs, bounded work, bounded outputs, and explicit or inferable authority boundaries.

2. **The recurring discipline is strongest in inquiry/presentation/diagnostic surfaces.**
   Question-family inventory, Inquiry Orientation, ExplanationBuilder, Operational Story, and Promotion Readiness use explicit answer, reason, support, boundary, limitation, readiness, or status records.

3. **The repository supports “bounded question discipline” only as a local recurring implementation pattern, not as a universal abstraction.**
   Existing code and investigations repeatedly reject overbroad promotion from local surface names or presentation vocabulary into preserved knowledge, ownership, or universal ontology.

4. **Downstream authority is commonly gated by prior bounded answers.**
   Evidence follows observation; facts follow evidence unless suppressed; fact support follows projected facts; explanation follows support; decision input follows budgeted projected state; bounded ask follows exact registered families; Operational Story follows existing audits.

5. **Authority boundaries are as important as answers.**
   The strongest evidence for the discipline is not just answer production, but explicit non-authority: no promotion, no fact creation, no semantic intent, no unknown-family routing, no execution, no mutation.

## 7. Unsupported conclusions

The implementation does not currently support concluding that:

- Seed should introduce a `Question` abstraction.
- Inquiry should be redesigned around bounded questions.
- Responsibilities should be recovered as ownership domains.
- Every responsibility explicitly names its prerequisite question.
- Every downstream responsibility enforces prerequisite questions uniformly.
- The bounded-question pattern extends consistently and equally across all implementation layers.
- Presentation vocabulary can be promoted into repository knowledge without reachability evidence.

## 8. Confidence

- **High confidence** that multiple reviewed responsibilities answer bounded questions with implementation-backed answer shapes and boundaries.
- **High confidence** that exact question-family dispatch and question-family explanation are real but narrow.
- **High confidence** that Inquiry Orientation, Operational Story, and Promotion Readiness explicitly separate answer/support/boundary/limitations or readiness/non-promotion.
- **Medium confidence** that Observation, Evidence, Fact promotion, and Fact support should be described as question owners; their bounded work is clear, but question language is mostly inferred from shapes and event handoffs.
- **Low confidence** in any universal claim that the repository architecture is best understood primarily as a question system.

Overall confidence: **medium-high for a recurring local discipline; low for a universal inquiry architecture**.

## 9. Recommended next investigation

Recommended next investigation:

```text
answer_boundary_consistency_investigation.md
```

Scope should remain investigative and implementation-backed. It should compare existing answer/result shapes across diagnostic, inquiry, explanation, operational, and promotion-readiness surfaces to determine whether the recurring boundary vocabulary itself is consistent:

- answer/result/status;
- reason/rationale;
- support/evidence;
- boundary/authority;
- limitations/unknowns;
- mutation/recording flags.

The investigation should not introduce abstractions, planners, automation, or ownership recovery. It should only determine whether existing answer surfaces already preserve consistent boundary fields or whether consistency is accidental and local.

## Acceptance answer

Across the repository, responsibilities are best understood as **owners of bounded work that often answers bounded questions**, rather than as pure owners of bounded questions. The stronger “bounded question owner” reading is implementation-backed for inquiry, explanation, readiness, and operational composition surfaces. It is weaker but still plausible for observation, evidence, fact promotion, and fact support because their question discipline is embodied in event ordering, record shapes, support projections, and boundaries rather than explicit question-family definitions.

A recurring question discipline exists as a **local implementation pattern**:

```text
prerequisite bounded answer -> bounded work -> bounded answer/result -> downstream bounded question
```

The recurrence fails as a universal discipline where questions are implicit, where fact promotion is automatic by default, where why-not explanation is intentionally incomplete, and where exact inquiry dispatch refuses to become semantic routing.

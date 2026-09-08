# Expression Composition Explanation Investigation

## Scope

This is a bounded implementation investigation of whether current Seed implementation distinguishes this progression:

```text
identity
  -> expressions
  -> composed explanation
```

The investigation is evidence recovery only. It does not recover ownership, redesign Answer Composition, redesign Inquiry, introduce language or prose abstractions, recommend implementation changes, or introduce automation.

## Implementation Evidence Reviewed

Runtime implementation reviewed:

- `seed_runtime/explanations.py`
- `seed_runtime/facts.py`
- `seed_runtime/evidence.py`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/context.py`
- `seed_runtime/context_selection.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/source_navigation.py`

Prior implementation investigations reviewed as context, not as authority over code:

- `docs/bounded_answer_responsibility_investigation.md`
- `docs/architectural_orientation_answer_composition_audit.md`
- `docs/selection_rationale_characterization.md`
- `repository_dependency_ordering_invariant_investigation.md`
- `incremental_state_evolution_architecture_investigation.md`
- `implementation_responsibility_family_stack_audit.md`

The strongest implementation evidence is in runtime code. Prior investigations are useful where they identify already-implemented surfaces, but this report treats the implementation as authoritative.

## Expression Sources

Current implementation has multiple independently justified expression sources about subjects, but they are not represented by one generalized `Expression` abstraction.

### Evidence payloads

`Evidence` represents an observed source payload with source, kind, observed time, payload, and confidence. It can support one or more facts.

Evidence source fields:

- `id`
- `workspace_id`
- `source`
- `kind`
- `observed_at`
- `payload`
- `confidence`

This is expression-like provenance, but implementation vocabulary is `Evidence`, not `Expression`.

### Fact supports

`FactSupport` is the clearest implementation point where multiple fact records can become one justified claim. It carries subject, predicate, value, dimensions, supporting fact ids, source types, confidence, observation times, expiry, predicate semantics, and support kind.

Important boundary: `FactSupport` is still knowledge representation. It aggregates support for a claim; it does not by itself produce a human explanation.

### Current fact views

`build_fact_view(state)` renders deterministic read-only fact views from current projected claims. Its docstring says current fact views render the support projection instead of raw fact rows so identical durable claims are shown once while supporting provenance remains attached.

This means current facts are a convergence and presentation surface for projected claim support, not a generalized explanation-composition surface.

### Documentation and repository artifact observations

Repository documentation and source/repository artifacts appear through projected facts, source navigation rows, and inquiry-orientation related material. In the reviewed implementation, they participate as fact supports and source-navigation matches rather than as a single generalized expression layer.

### Diagnostic and operational observations

Operational Story consumes outputs from pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path audit. These are expression-like operational surfaces. Operational Story composes them into a coherent answer object.

Inquiry Orientation consumes projected fact supports and source-navigation matches derived from an inquiry note. These are expression-like matches selected by deterministic lexical overlap.

## Identity Versus Expression

### Supported distinction

Implementation distinguishes identity from expression in several places.

1. `ExplanationBuilder.why(subject, predicate)` asks projected state for supports for a subject and predicate. It then builds belief explanations from those supports. Identity is the query anchor; supports and fact/evidence provenance are the material being explained.

2. `ExplanationBuilder._resolution_chain(start, target)` walks `state.entity_aliases` to expose how the queried subject and the fact subject are connected. This is identity-resolution evidence included inside a fact explanation. It does not compose language or decide what the fact means.

3. `ExplanationBuilder._conflict(subject, predicate)` canonicalizes the subject through `state.alias_resolver.canonical(subject)` before matching conflicts. This shows alias/canonical identity handling as a lookup boundary for fact conflicts, not as explanation composition.

4. `observation_normalizers.py` explicitly says identity normalization runs first so canonical observations inherit raw endpoint subjects and participate in aliases derived earlier in the batch. That is identity projection before downstream fact/explanation surfaces.

### Unsupported extension

Implementation does not show a generalized identity convergence subsystem that owns all identity-to-expression progression. Alias projection and canonical subject selection are used by fact support, conflict lookup, and explanation provenance, but they do not produce composed explanations.

## Expression Convergence Evidence

### First convergence for knowledge claims: fact support projection

For knowledge claims, multiple expressions first converge in projected fact support. `FactSupport` records the subject/predicate/value claim plus the supporting fact ids and source types. `State.get_fact_supports(subject, predicate)` and `State.get_fact_support(subject, predicate)` are then consumed by explanation code.

This is the first recurring convergence point for multiple facts about one subject/predicate/value. It is not yet a human explanation; it is a support projection.

### Current fact convergence: state view over supports

`build_fact_view(state)` uses `state.fact_supports` or a fallback from raw facts. It sorts supports deterministically and produces `FactView` rows with subject, predicate, object, confidence, dimensions, and supporting event ids.

This is expression convergence for current facts. It selects the support projection and exposes attached provenance, but it does not compose a prose explanation.

### Decision-input convergence: context packet composition

`DecisionInputComposer.compose(...)` orders goals, entities, facts, evidence, and open tool needs, then applies a context budget. It attaches selected evidence payloads to selected facts only when the evidence survived the budget selection.

This is expression selection for model-visible decision context. It orders and budgets expressions. It does not itself produce a human explanation; it produces `DecisionInputPacket` input for a later decision.

### Inquiry-orientation convergence: lexical material selection

`build_inquiry_orientation(state, note)` calls `_compose_architectural_orientation_answer(state, note)`. That function collects evidence through `_collect_architectural_orientation_evidence`, which combines `_fact_matches` and `_source_navigation_matches`, deduplicates and limits them, and returns related material.

This is a bounded convergence of projected fact supports and source-navigation rows around a preserved inquiry note. The implementation explicitly calls the intermediate object `_ArchitecturalOrientationEvidence` and the composed object `_ArchitecturalOrientationAnswer`.

### Operational-story convergence: multi-surface answer payloads

`build_operational_story(state, repo_root)` gathers pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path audit outputs, selects the primary pressure, then calls `_compose_operational_story_payloads(...)`.

`_compose_operational_story_payloads(...)` creates separate implementation-local payloads for answer material, reasoning material, supporting evidence, boundary, and limitations, then `build_operational_story` copies those payloads into the public `OperationalStory` compatibility object.

This is the strongest implementation-backed convergence and composition evidence for a coherent explanation-like answer.

### Question-family explanation convergence

`build_composed_question_family_explanation(question_family, rows)` builds a question-family definition and composes existing definition, answer responsibility, boundary, and diagnostic relationship fields into ordered presentation sections. The function's own docstring scopes this as composition of existing QuestionFamily explanation fields for presentation only.

This is explanation structure over inventory metadata. It is narrower than general expression composition.

## Expression Selection Evidence

Implementation has selection mechanisms, but they are surface-specific.

### Fact explanation selection

`ExplanationBuilder.why(...)` selects supports for a subject/predicate query. For multi-valued predicates, all supports become current beliefs. For single-valued predicates, `get_fact_support(...)` selects the best support; other support values become competing beliefs. Conflict information is attached if present.

Selection here is current belief selection and competing belief selection. Composition is recursive fact-provenance explanation for the selected supports.

### Context selection

`context_selection.py` orders facts by freshness, observation time, confidence, and id; evidence by observation time, confidence, and id; goals by active status and id; and entities by confidence, name, and id. `DecisionInputComposer.compose(...)` then applies a context budget.

This is explicit expression selection and ordering for model-visible context, but not human explanation composition.

### Inquiry-orientation selection

Inquiry Orientation tokenizes the note, selects fact supports whose subject, predicate, value, or path dimension overlaps note tokens, selects source-navigation matches for each token, deduplicates, sorts, and limits the related material.

This is explicit selection and ordering before a bounded orientation answer is returned.

### Operational-story selection

Operational Story selects `primary = pressure_audit.pressures[0] if pressure_audit.pressures else None` and derives focus, pressure, supporting evidence, and investigation domain from that primary pressure. It also transforms capability, privilege, correlation, and impact items into answer fields.

This is explicit surface-specific selection before answer payload composition.

## Expression Ordering Evidence

Ordering appears in several implementation-local places:

- `context_selection.py` orders facts, evidence, goals, and entities before budget selection.
- Inquiry Orientation sorts and deduplicates related material by material type, label, surface, and support before limiting results.
- `build_fact_view(state)` sorts fact supports by subject, predicate, stable value, dimensions, and supporting fact ids.
- Operational Story preserves investigation path order by copying each step's `order` into the reasoning payload.
- Question-family composed explanation orders sections as Definition, Answer responsibility, Boundary, and Diagnostic relationship.

Ordering is therefore implementation-backed, but it is not centralized in a generalized expression-composition subsystem.

## Expression Combination Evidence

Expression combination is also surface-specific.

### Fact support combination

Fact support combines multiple supporting fact ids and source types into one supported claim. This is claim-support composition, not explanation composition.

### ExplanationBuilder combination

`ExplanationBuilder` combines support records, facts, evidence ids, source types, inference provenance, confidence fields, conflict state, and alias-resolution chains into nested explanation objects.

This is the clearest knowledge-to-explanation transition for facts. It produces structured explanation data (`Explanation`, `BeliefExplanation`, `FactExplanation`), not prose. Human rendering, if any, is separate from this builder.

### Inquiry Orientation combination

Inquiry Orientation combines fact-support matches and source-navigation matches into an answer object with answer material, reason, support, boundary, and limitations, then renders it in `format_inquiry_orientation`.

This is a bounded inquiry explanation surface. It does not infer semantic intent from language; it uses deterministic lexical overlap and an explicit authority boundary.

### Operational Story combination

Operational Story combines multiple operational diagnostic/read-model surfaces into answer, reasoning, supporting evidence, boundary, and limitations payloads. `format_operational_story` renders those fields into human sections.

This is the strongest implemented example of multiple independently justified operational expressions becoming one coherent explanation-like output.

### Question-family explanation combination

Question-family composition combines inventory-derived fields into ordered sections for presentation. It is implemented, but narrow: it composes explanation fields about question-family inventory, not arbitrary subject expressions.

## Transition From Knowledge Representation To Human Explanation

The transition occurs at different boundaries depending on the surface.

### Fact why path

- Knowledge representation: facts, evidence, aliases, fact supports, conflicts.
- Structured explanation: `ExplanationBuilder.why(...)` returns `Explanation` with current beliefs, competing beliefs, conflicts, nested fact explanations, evidence ids, source types, and entity-resolution chains.
- Human explanation: not centralized in the reviewed `ExplanationBuilder`; the builder produces structured objects.

Conclusion: fact why has structured explanation composition, but the human prose transition is not the builder itself.

### Current facts path

- Knowledge representation: projected fact supports.
- Presentation view: `build_fact_view(state)` creates deterministic fact rows with support ids.
- Human explanation: current facts remain a compact view, not a composed explanatory narrative.

Conclusion: current facts expose support, not explanation composition.

### Inquiry Orientation path

- Knowledge representation: projected fact supports and source navigation rows.
- Selection/composition: `_collect_architectural_orientation_evidence(...)` and `_compose_architectural_orientation_answer(...)`.
- Human explanation: `format_inquiry_orientation(view)` renders inquiry note, related material, support/why-related, uncertainty, and authority boundary.

Conclusion: this path implements a bounded transition from selected expressions to rendered explanatory orientation.

### Operational Story path

- Knowledge representation/read models: pressure, capability needs, privilege discovery, correlation, impact, investigation path.
- Selection/composition: `build_operational_story(...)` and `_compose_operational_story_payloads(...)`.
- Human explanation: `format_operational_story(story)` renders current focus, primary pressure, supporting evidence, missing capabilities, access constraints, correlation gaps, recent changes, observed outcomes, investigation path, unknowns, and boundary.

Conclusion: this path implements the strongest transition from multiple operational expressions to one coherent human explanation surface.

### Question-family explanation path

- Knowledge representation/read model: question-surface inventory rows and derived question-family definition.
- Selection/composition: `build_composed_question_family_explanation(...)`.
- Human explanation: `format_composed_question_family_explanation(...)`.

Conclusion: this path has an explicit composition-to-rendering boundary, but its domain is question-family inventory explanation.

## Implementation Boundaries

### Identity projection does not perform explanation composition

Alias resolution and canonical subject selection support identity matching, conflict lookup, and provenance chains. They do not select expression meaning, compose language, or produce a coherent explanation.

### Expression selection is not the same as expression composition

`context_selection.py` and `DecisionInputComposer.compose(...)` select and order model-visible material. They do not produce final human explanation. Conversely, Operational Story and Inquiry Orientation do compose selected material into answer objects and renderable sections.

### Fact support is not human explanation

`FactSupport` is a support projection. It can aggregate multiple observations into one claim, but it remains representation-layer material until consumed by an explanation or presentation surface.

### Explanation composition is not generalized

The implementation contains recurring local composition patterns, but no generalized `Expression`, `ExpressionSelector`, `ExpressionComposer`, or identity-to-explanation subsystem. Current responsibilities remain partially implementation-compressed inside surface-specific builders such as `ExplanationBuilder`, `build_inquiry_orientation`, `build_operational_story`, and `build_composed_question_family_explanation`.

### Rendering is not always composition

`format_*` functions render already-composed or already-selected structures. The strongest composition occurs before rendering, in `ExplanationBuilder.why`, `_compose_architectural_orientation_answer`, `_compose_operational_story_payloads`, and `build_composed_question_family_explanation`.

## Counterexamples Reviewed

### Explanations generated directly from one fact

`ExplanationBuilder._explain_fact(...)` can produce a `FactExplanation` for one fact, including evidence ids, confidence, inference details, source fact, and entity-resolution chain. Therefore explanation can emerge around one fact when the selected support contains one fact. This is a counterexample to any claim that explanation always requires multiple expressions.

### Identity projection performing explanation

No implementation evidence was found that identity projection itself composes explanation. Identity handling appears as normalization, canonicalization, alias lists, conflict lookup, and resolution-chain evidence inside explanations.

### Alias resolution composing language

No implementation evidence was found that alias resolution composes language. Alias resolution is consumed by explanation and state conflict paths, but it does not produce prose or answer sections.

### Answer surfaces bypassing expression selection

Some surfaces are narrow composition over already-derived fields. `build_composed_question_family_explanation(...)` composes fields from `build_question_family_definition(...)`; it does not independently search across arbitrary expressions. Current fact views similarly present already-projected supports. These are bypasses of broad expression selection, but not necessarily defects: they are bounded to their source read models.

### Explanation emerging without explicit composition

Current facts and some inventory renderers can produce user-visible output without explicit explanation-composition semantics. They may render support or metadata directly. Therefore not every explanatory-looking output is evidence of a recurring explanation-composition responsibility.

## Answers To Central Questions

### 1. Does implementation distinguish identity from expression?

Yes, with bounded evidence. Identity appears in alias normalization, canonical subject selection, alias-resolution chains, and conflict lookup. Expressions appear as evidence, facts, fact supports, source-navigation rows, diagnostic/read-model outputs, and related material. The distinction is implemented by usage and data flow, not by a single general abstraction.

### 2. Where do multiple justified expressions first converge?

For knowledge claims, they first converge in fact support projection (`FactSupport` and `state.fact_supports`). For current fact presentation, they converge in `build_fact_view(state)`. For answer-like surfaces, convergence occurs locally in Inquiry Orientation's evidence collection and Operational Story's multi-surface builder.

### 3. Does implementation distinguish expression selection from expression composition?

Partially. Context selection clearly orders and budgets expressions without producing human explanation. Inquiry Orientation and Operational Story perform selection before composition. `ExplanationBuilder.why(...)` combines support selection and explanation-object construction in one class, so that path remains more compressed.

### 4. Where does explanatory structure first appear?

For fact why queries, explanatory structure first appears in `ExplanationBuilder.why(...)` and the `Explanation`, `BeliefExplanation`, and `FactExplanation` objects. For inquiry orientation, it appears in `_ArchitecturalOrientationAnswer`. For operational story, it appears in the implementation-local answer, reasoning, support, boundary, and limitations payloads. For question-family inventory explanation, it appears in `build_composed_question_family_explanation(...)` sections.

### 5. Which responsibilities consume expressions?

Expression consumers include:

- Fact support projection and current fact views.
- `ExplanationBuilder` for why/current/competing belief explanations.
- `DecisionInputComposer` for model-visible context packets.
- Inquiry Orientation for bounded note-to-related-material orientation.
- Operational Story for current operational explanation.
- Question-family composed explanation for inventory explanation fields.
- Source Navigation as a bounded lookup/navigation surface over source facts.

### 6. Which responsibilities produce explanations?

Explanation producers include:

- `ExplanationBuilder.why(...)`, producing structured fact/belief explanations.
- Inquiry Orientation, producing an `InquiryOrientationView` and formatted orientation explanation.
- Operational Story, producing an `OperationalStory` and formatted operational explanation.
- Question-family composed explanation, producing structured and formatted explanation of question-family metadata.

Current facts and decision-input context produce presentation/context, not necessarily explanations.

### 7. Does implementation evidence support a recurring explanation-composition responsibility?

Yes, but only as a recurring surface-local responsibility, not as a generalized subsystem. The recurring pattern is:

```text
existing projected/read-model material
  -> bounded selection/order/derivation
  -> implementation-local answer/explanation payload
  -> compatibility object or view
  -> formatter
```

The pattern is strongest in Operational Story and Inquiry Orientation, and present in fact why explanations and question-family explanation. It is not implemented as a repository-wide identity -> expressions -> composed explanation pipeline.

### 8. If so, what implementation vocabulary best characterizes that responsibility?

The best implementation-backed vocabulary is **bounded answer/explanation composition over existing projected state and read-model surfaces**.

More precise surface-local vocabulary:

- Fact why: **projected fact provenance explanation**.
- Current facts: **fact-support view**, not full explanation composition.
- Decision context: **context selection and budgeting**, not human explanation composition.
- Inquiry Orientation: **read-only inquiry-note orientation answer composition**.
- Operational Story: **read-only operational story composition from visibility surfaces**.
- Question Family: **composed question-family explanation fields for presentation**.

The unsupported vocabulary is a generalized **identity convergence** or generalized **expression composition subsystem**.

## Supported Conclusions

1. Implementation distinguishes identity handling from expression/provenance handling in bounded mechanisms.
2. Multiple justified expressions converge first in fact supports for knowledge claims.
3. Current facts present support projections; they do not by themselves compose explanatory meaning.
4. `ExplanationBuilder` composes structured why explanations from selected fact supports, facts, evidence ids, conflicts, inference provenance, and alias-resolution chains.
5. `DecisionInputComposer` selects, orders, and budgets expressions for model-visible decision context, but does not produce human explanation.
6. Inquiry Orientation composes selected fact-support and source-navigation matches into a bounded explanation-like orientation view with support, uncertainty, and authority boundary.
7. Operational Story is the strongest implemented recurring answer-composition example: it joins multiple read-model/diagnostic surfaces into answer, reasoning, evidence, boundary, and limitations payloads, then renders them.
8. Question-family explanation composes inventory-derived fields into a structured explanation for presentation.
9. Implementation supports recurring surface-local explanation composition, but not a generalized expression-composition subsystem.

## Unsupported Conclusions

1. Unsupported: Seed has a generalized identity convergence subsystem.
2. Unsupported: Alias projection determines what expressions collectively mean.
3. Unsupported: All explanatory output passes through explicit expression selection.
4. Unsupported: Current facts are themselves composed explanations.
5. Unsupported: There is one repository-wide `identity -> expressions -> composed explanation` implementation path.
6. Unsupported: Presentation vocabulary alone proves implementation knowledge or ownership.
7. Unsupported: Explanation composition always requires multiple expressions; one selected fact can produce a structured fact explanation.

## Confidence

Confidence is high that implementation distinguishes identity handling from expression/provenance handling in bounded code paths.

Confidence is high that fact support projection is the primary convergence point for multiple knowledge claims about a subject/predicate/value.

Confidence is high that Operational Story and Inquiry Orientation implement bounded answer/explanation composition over existing surfaces.

Confidence is medium that the recurring pattern should be characterized as one responsibility family, because the implementation uses repeated local composition shapes but does not centralize them into a shared subsystem.

Confidence is high that a generalized expression-composition subsystem is not implementation-backed in the reviewed code.

## Recommended Next Investigation

If further investigation is needed, the next bounded implementation investigation should enumerate all `format_*`, `*_json`, `build_*_explanation`, and `build_*_story` surfaces and classify each as one of:

1. direct rendering of a read model;
2. selection/order/budgeting without explanation;
3. structured provenance explanation;
4. bounded answer composition;
5. broad operational explanation composition.

That investigation should remain observational and should not redesign answer composition, introduce language abstractions, or promote presentation vocabulary into repository knowledge without implementation evidence.

## Acceptance Answer

Once Seed knows what subject is being discussed, implementation progresses from many independently justified expressions to explanation through bounded, surface-local paths.

For facts, the path is:

```text
facts/evidence/aliases
  -> fact support projection
  -> current or competing belief selection
  -> structured fact provenance explanation
```

For inquiry orientation, the path is:

```text
preserved note + projected fact supports + source navigation
  -> lexical match selection
  -> related-material answer composition
  -> rendered orientation with support, uncertainty, and boundary
```

For operational story, the path is:

```text
pressure/capability/privilege/correlation/impact/investigation surfaces
  -> primary focus and field selection
  -> answer/reason/support/boundary/limitations payloads
  -> rendered operational explanation
```

Therefore implementation already recovers explanation-composition responsibility in several bounded surfaces, especially Operational Story and Inquiry Orientation. However, explanation composition remains implementation-compressed and surface-local. The reviewed implementation does not support a generalized identity-to-expression-to-explanation subsystem.

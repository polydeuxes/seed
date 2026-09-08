---
status: investigation
scope: relationship preservation across abstraction boundaries
created: 2026-06-22
---

# Relationship Preservation Across Abstraction Boundaries Investigation

## Purpose and boundary

This investigation asks whether current repository self-knowledge surfaces are better understood as relationship-preservation surfaces, or as relationship-preserving translations, rather than as translation or context-preservation surfaces alone.

This is an investigation only. It does not implement relationship systems, redesign projections, modify ontology, create navigation systems, build assistants, add diagnostics, change command behavior, alter architecture, or mutate cluster knowledge. Repository authority remains implementation-backed behavior, tests, executable diagnostics, and existing repository-visible documents.

The vocabulary in this document is descriptive. It is not promoted into preserved cluster knowledge, official ontology, routing behavior, or implementation plan by being used here.

## Evidence reviewed

Implementation-backed surfaces reviewed:

- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/capability_relationship.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/component_audit.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`

Prior investigations reviewed:

- `docs/context_preservation_surface_investigation.md`
- `docs/translation_surfaces_pattern_investigation.md`
- `docs/reasoning_space_translation_investigation.md`
- `docs/repository_navigation_question_surface_discoverability_investigation.md`
- `docs/observation_space_visibility_investigation.md`
- `docs/repository_shape_coverage_investigation.md`
- `docs/traceability_gap_analysis_investigation.md`
- `docs/projection_self_description_investigation.md`
- `docs/reference_selection_traceability_investigation.md`

## Central finding

Yes: current evidence supports relationship preservation as a deeper explanation for many useful self-knowledge surfaces than value preservation alone.

The stronger repository-backed formulation is:

```text
useful self-knowledge surfaces often preserve relationships across abstraction boundaries

translation is the movement between spaces
context preservation is the interpretive envelope
relationship preservation is the load-bearing structure that often makes the preserved context useful
```

The evidence does not require choosing only one label. The most supported phrase is:

```text
relationship-preserving translation
```

That phrase fits the strongest reviewed surfaces because they do not merely move values into a new shape. They preserve a relationship such as evidence-to-conclusion, candidate-to-outcome, reference-to-comparison, capability-pressure-to-operational-meaning, projection-stage-to-influence, component-to-role, or registry-to-implementation.

## Preserved relationship types

The following groupings are descriptive, not proposed ontology.

| Relationship type | Example shape | Strongest current surfaces | What disappears if the relationship disappears |
| --- | --- | --- | --- |
| Derivation / support | evidence -> intermediate conclusion -> derived conclusion -> consumer/story impact | `reasoning_path`, `operational_story` | A conclusion remains visible, but the support chain and downstream use vanish. |
| Selection | candidate set -> selected item -> non-selected alternatives -> outcome | `selection_path`, `reference_selection`, pressure/story surfaces | A selected focus or reference remains visible, but why it won over alternatives disappears. |
| Comparison / reference | selected reference -> comparison question -> alternatives/limits/authority | `reference_selection`, history/impact/snapshot-policy surfaces | A comparison can still be reported, but the frame becomes implicit and easy to overread. |
| Operational meaning | pressure/capability/current access -> benefit/constraint/unknown expectation | `capability_relationship`, `operational_story` | Capability need can collapse into acquisition guidance, expectation, or generic missingness. |
| Influence / non-influence | stage -> consumes/produces/influences/does-not-influence | `projection_shape` | Projection output remains visible, but implementation emergence and negative boundaries disappear. |
| Component role | component name -> definitions/references/tests/consumers/graph/architecture/status | `component_audit` | A name remains searchable, but distributed role evidence must be reconstructed manually. |
| Governance / conformance | registry declaration -> implementation spec -> observed field/status | `diagnostic_inventory`, `diagnostic_shape_audit` | A command list remains visible, but operational contract, ledger behavior, mutation boundary, and conformance relation disappear. |
| Composition | specialized surfaces -> current story/focus/impact/investigation path | `operational_story`, `ops_brief` family | Individual facts remain visible, but current operational significance is not preserved. |
| Observation-domain pressure | predicate/provider/capability evidence -> candidate observation domain/gap | observation-space investigation, `observation_inventory`, `observation_utilization`, `capability_relationship` | Predicate facts remain visible, but domain coverage, absence, and partiality must be inferred manually. |
| Boundary / authority | output -> read-only/recording/event-ledger/mutation/unknown/unsupported boundary | most reviewed surfaces | Explanatory output can be mistaken for truth promotion, policy, expectation, or mutation authority. |

## Surface-by-surface assessment

### `reasoning_path`

`reasoning_path` preserves a derivation relationship. Its fields carry evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and a read-only/no-ledger/no-mutation boundary.

The useful part is not only that evidence is translated into derivation-space. The useful part is the preserved relation:

```text
evidence -> conclusion -> consumer/story impact
```

If that relationship disappeared, the conclusion or capability pressure could still be visible, but the reason it exists and where it matters would be compressed away.

Classification: strong relationship-preserving translation.

### `selection_path`

`selection_path` preserves a selection relationship. Its model carries target, selected result, candidates, selection factors, non-selected candidates, evidence, outcome, unknowns, and a read-only boundary.

The useful relation is:

```text
candidate set -> selection factors -> selected outcome
candidate set -> non-selected remainder
```

If that relationship disappeared, a current focus could still be shown, but selection would become opaque. That is not merely context loss; it is loss of the candidate-to-outcome relationship.

Classification: strong relationship-preserving translation.

### `reference_selection`

`reference_selection` preserves a comparison-reference relationship. It carries the domain/question, selected reference, selection rationale, alternatives, authority boundary, limitations, and ledger/mutation boundaries.

The useful relation is:

```text
comparison question -> selected reference -> alternatives/limitations/authority
```

If that relationship disappeared, history or impact output could still compare something, but the comparison frame would be implicit. The surface is valuable because it preserves what the comparison is anchored to.

Classification: strong relationship-preserving translation.

### `capability_relationship`

`capability_relationship` preserves an operational relationship between capability need, current access, benefit, pressure, reasoning, known limitations, and explicit unknown attainability/expectation.

The useful relation is:

```text
capability pressure -> current access -> operational benefit
capability pressure -> unknown attainability / unknown expectation
```

If that relationship disappeared, a capability need could be misread as a deployment plan, acquisition recommendation, or operator expectation. The preserved relationship keeps pressure visible without overclaiming intent.

Classification: relationship-preserving operational translation.

### `projection_shape`

`projection_shape` preserves implementation-flow relationships across projection stages. Stages carry consumes, produces, influences, does-not-influence, authority boundary, and implementation-backed confidence.

The useful relation is:

```text
stage -> consumes
stage -> produces
stage -> influences
stage -> does_not_influence
```

If that relationship disappeared, projection could still expose final read models and facts, but the implementation path from event replay, alias projection, measurement retention, inference, support projection, relationship projection, graph issue construction, and conflict handling would become a reconstructed guess.

Classification: strong relationship-preserving self-description.

### `component_audit`

`component_audit` preserves a component-role relationship. It collects definitions, references, tests, consumers, operational graph evidence, architecture evidence, overlap, status evidence, unresolved questions, and read-only boundaries around a named component.

The useful relation is:

```text
component name -> repository evidence bundle -> role/status/unresolved questions
```

If that relationship disappeared, all the source evidence could still exist, but its relationship to the component would be distributed, expensive, and error-prone to reconstruct.

Classification: strong relationship preservation with comparatively local translation.

### `operational_story`

`operational_story` preserves composition relationships across pressure, capability, privilege, correlation, impact, recent changes, observed outcomes, and investigation path.

The useful relation is:

```text
specialized diagnostic evidence -> current operational narrative
pressure -> focus
capability/constraint/impact -> story meaning
```

If that relationship disappeared, individual surfaces could still report facts, but their current operational meaning would be weaker.

Classification: relationship-preserving composition surface.

### `diagnostic_inventory` and `diagnostic_shape_audit`

`diagnostic_inventory` preserves public diagnostic surface contracts: name, flags, state/repo use, JSON/record support, record scope, emitted fact kind, event-ledger writes, mutation behavior, diagnostic-fact reads, and description.

`diagnostic_shape_audit` preserves a conformance relationship between the registry declaration and implementation evidence: audited field, declared value, observed value, and status.

The useful relation is:

```text
public surface declaration -> implementation evidence -> conformance status
```

If that relationship disappeared, diagnostics could still be listed, but the operational contract and implementation-backed confidence would not be visible.

Classification: registry-to-implementation relationship preservation.

## Relationship preservation versus context preservation

The context-preservation investigation already found that useful surfaces preserve reasons, alternatives, comparison frames, operational boundaries, implementation emergence, unknowns, and authority limits. This investigation refines that finding.

Context preservation asks:

```text
what surrounding interpretive material survives the abstraction boundary?
```

Relationship preservation asks:

```text
what relation among things survives the abstraction boundary?
```

They overlap heavily because many context fields are useful precisely because they preserve relationships. For example:

- reasoning context is mostly evidence-to-conclusion relationship preservation;
- selection context is mostly candidate-to-outcome relationship preservation;
- reference context is mostly comparison-to-reference relationship preservation;
- projection context is mostly stage-to-influence relationship preservation;
- component context is mostly component-to-role relationship preservation;
- diagnostic governance context is mostly registry-to-implementation relationship preservation.

They diverge in two directions:

1. Context can exist without strong preserved relationships. A raw summary may include surrounding prose, limits, or descriptions while still failing to show why values relate.
2. Relationships can be preserved with minimal surrounding context. A compact stage row containing consumes/produces/influences/does-not-influence preserves a strong relationship even without narrative explanation.

The evidence therefore supports this hierarchy for many reviewed surfaces:

```text
values alone are weak
context makes values interpretable
relationships often explain why the context is load-bearing
```

## Relationship preservation versus translation

Translation explains the motion:

```text
one reasoning space -> another explanatory shape
```

Relationship preservation explains what must survive that motion:

```text
source relation -> target-visible relation
```

A translation can be weak if it moves values but drops the relation that made them meaningful. The prior translation investigation already identified several surfaces as moving between reasoning spaces. This investigation adds that the strongest translations preserve relationships rather than only values.

Supported refinement:

```text
translation is not replaced
translation is strengthened when it preserves relationships
```

## Relationship preservation versus traceability, explanation, and navigation

These concepts are adjacent but not equivalent.

| Concept | Relationship to this investigation | Not equivalent because |
| --- | --- | --- |
| Relationship preservation | Preserves a meaningful relation across an abstraction boundary. | It may be compact and not provide full explanation. |
| Context preservation | Preserves interpretive material around output. | Context can be present without a clear relationship. |
| Translation | Re-expresses evidence across reasoning spaces. | Translation can drop relationships. |
| Traceability | Lets a worker follow a relation or missing explanatory layer. | Traceability depends on preserved relationships but emphasizes followability and gaps. |
| Explanation | Answers why/how/compared-to-what/what-it-means. | Explanation may use preserved relationships but may also add prose or synthesis. |
| Navigation | Helps find the right surface/document/command. | Navigation can route to a relationship-poor answer, and relationship preservation can exist after the surface is already selected. |

## Counterexamples and limits

### Context exists but relationships are weak

- Raw current-state views and simple fact listings can provide readable context around stored values while preserving little rationale, selection history, alternatives, or authority relation.
- `diagnostic_inventory` used only as a flat command list preserves surface names and descriptions, but its strongest relationship-preservation value appears only when record behavior, event-ledger writes, mutation boundary, emitted fact scope, and implementation conformance are considered.
- `observation_inventory` and `observation_utilization` preserve provider/predicate visibility and predicate use, but the observation-space investigation shows that predicate/provider evidence does not yet preserve first-class observation-domain relationships.

### Relationships are preserved with minimal surrounding context

- `projection_shape` rows preserve consumes/produces/influences/does-not-influence relationships with minimal narrative.
- `diagnostic_shape_audit` rows preserve declared-vs-observed conformance relationships through compact fields.
- `selection_path` can preserve candidate/non-selected/outcome relationships even when unsupported targets return explicit unknowns.
- `reference_selection` preserves selected-reference/alternative-reference relationships even when its implementation-backed domain is only `history`.

These counterexamples show that relationship preservation, context preservation, and translation are related but separable.

## Difficult or currently impossible relationships to preserve

The evidence supports several current relationship gaps:

| Difficult relationship | Current status | Evidence-backed interpretation |
| --- | --- | --- |
| predicate -> observation domain | Not first-class | Predicate/provider inventory exists, but domain coverage, absence, and partiality are inferred by investigation rather than implementation-backed domain relationship. |
| question -> answering surface | Mostly implicit | Surface descriptions and docs exist, but question-to-surface routing is not a current implementation surface. |
| pressure -> observation-space gap | Manual/investigative | Capability pressure can be related to observation gaps, but not through a first-class implemented pressure-to-domain relationship. |
| answer -> follow-up surface | Mostly manual | A worker often infers whether to move from component to consumer, derivation to selection, selection to reference, or pressure to capability. |
| component -> complete repository catalog role | Partial/query-driven | `component_audit` is per-component and evidence-backed, but not a full component catalog. |
| relationship-preservation family membership | Investigation-only | No implementation-backed registry classifies surfaces as relationship-preserving. |

These gaps do not imply implementation work. They only bound what current evidence can support.

## Relationship to earlier findings

### Context preservation

The context-preservation investigation appears to have already found the edge of this pattern. Its strongest context types are mostly relation types: reasoning, selection, reference, operational, component, projection, diagnostic-governance, authority/boundary, and observation-domain context.

This investigation does not invalidate context preservation. It narrows why some preserved context is useful: it often preserves a relationship that would otherwise disappear.

### Translation surfaces

The translation investigations described motion between reasoning spaces. This investigation finds that the strongest translation surfaces are not just evidence-to-schema converters. They are relationship-preserving translations.

### Reasoning-space translation

Reasoning-space translation identified that workers manually translate natural questions into repository units and surfaces. This investigation adds that the missing thing is often a relationship between units, not just a missing target surface.

### Discoverability

Question-to-surface discoverability can be reinterpreted as a relationship visibility problem in some cases:

```text
question -> answering surface
surface -> follow-up surface
answer -> explanatory layer
```

But this is not all navigation. Some discoverability gaps remain ordinary naming, inventory, or routing gaps.

### Observation-space visibility

Observation-space visibility is the strongest counterpressure. Predicate/provider facts exist and some context exists, but predicate-to-domain and pressure-to-domain relationships are not first-class. This explains why those surfaces are useful but incomplete.

### Repository shape coverage

Shape coverage asked which domains have visible shape. This investigation reframes the strongest shaped domains as domains where relationships are visible: diagnostics, projection, operational relationships, components, capabilities, selection, references, reasoning, and boundaries.

### Traceability

Traceability gap analysis is closely related. A traceability gap often exists when an output is visible but a relationship layer is missing: derivation, selection, reference, or authority. Traceability emphasizes following the relation; relationship preservation emphasizes keeping the relation visible through abstraction.

## Supported conclusions

1. Current self-knowledge surfaces preserve recurring relationship types: derivation, selection, comparison/reference, operational meaning, influence/non-influence, component role, governance/conformance, composition, observation-domain pressure, and authority/boundary.
2. Relationship preservation is a stronger explanation than context preservation for the load-bearing usefulness of many reviewed surfaces, but it does not replace context preservation.
3. The strongest supported pattern is relationship-preserving translation.
4. Some context-preservation findings are relationship-preservation findings in disguise, especially reasoning, selection, reference, projection, component, and diagnostic-governance contexts.
5. Some context remains non-relational or weakly relational, so context preservation and relationship preservation should remain distinct.
6. Useful self-knowledge surfaces tend to preserve at least one relationship plus unknowns and authority boundaries.
7. Observation-domain visibility remains the clearest case where values and partial context exist but key relationships are still difficult to preserve.

## Unsupported conclusions

The evidence does not support these stronger claims:

- That Seed has or needs a general relationship-preservation framework.
- That relationship preservation is official ontology or preserved cluster vocabulary.
- That every context-preserving surface should become a relationship surface.
- That every relationship should be promoted into facts, graph edges, catalogs, or diagnostics.
- That relationship preservation replaces translation, context preservation, traceability, explanation, or navigation.
- That question-to-surface routing should be implemented.
- That observation-domain relationships should be implemented now.
- That preserved diagnostic or investigation relationships should become cluster truth.
- That relationship categories in this document are complete, canonical, or stable.

## Open questions

- What minimum evidence distinguishes a real preserved relationship from a prose association?
- Are unknowns and authority boundaries part of relationship preservation, or separate context needed to keep preserved relationships safe?
- Which existing surfaces preserve relationships strongly but were overlooked because they do not cross abstraction boundaries dramatically?
- Is observation-domain coverage missing a relationship-preserving translation, or can predicate/provider utilization surfaces grow enough without a new concept?
- Can documentation reliably preserve relationships without executable checks, or does it drift into context-only prose over time?
- Is there a reusable distinction between relationship preservation inside one reasoning space and relationship preservation across abstraction boundaries?

## Acceptance answers

### What relationships do current self-knowledge surfaces preserve?

They preserve evidence-to-conclusion, candidate-to-selection, reference-to-comparison, capability-pressure-to-operational-meaning, projection-stage-to-influence, component-to-role, diagnostic-registry-to-implementation, specialized-surface-to-operational-story, and output-to-authority-boundary relationships.

### Is relationship preservation a stronger explanation than context preservation?

Yes, for the strongest reviewed surfaces. Context preservation explains why output remains interpretable. Relationship preservation explains why the preserved context is load-bearing: it keeps the relation that would otherwise disappear when crossing abstraction boundaries.

### Why are some context-preserving surfaces useful while others are not?

The useful ones preserve relationships needed to answer why, why this one, compared to what, what does this pressure mean, what influences this, what role does this component play, or what authority boundary applies. Weaker context-preserving surfaces may expose values, descriptions, or surrounding prose without preserving the relationship that makes the output actionable or trustworthy.

### Are recent findings converging on relationship preservation across abstraction boundaries?

Partially yes. Translation, context preservation, observation-domain visibility, discoverability, repository shape, and traceability findings appear to converge on a recurring pressure: relationships are easier to lose than values when moving between abstraction levels. The supported conclusion is not that relationship preservation replaces those concepts, but that many useful self-knowledge surfaces are best understood as relationship-preserving translations across abstraction boundaries.

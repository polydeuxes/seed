---
status: investigation
scope: repeatedly reconstructed relationships as self-knowledge surface pressure
created: 2026-06-22
---

# Repeatedly Reconstructed Relationships Investigation

## Purpose and boundary

This investigation asks whether valuable repository self-knowledge surfaces tend to emerge after the same relationship has been reconstructed manually across repeated work.

This is an investigation only. It does not implement relationship systems, create new surfaces, redesign projections, change ontology, build navigation systems, add assistant behavior, change architecture, alter commands, or mutate cluster knowledge. Repository authority remains implementation-backed behavior, tests, executable diagnostics, and existing repository-visible documents.

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

Investigation documents reviewed:

- `docs/relationship_preservation_across_abstraction_boundaries_investigation.md`
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

Repository evidence supports a recurring pattern:

```text
relationship repeatedly reconstructed manually
    -> explanatory gap becomes visible
    -> scoped self-knowledge surface preserves part of the relationship
    -> unknowns and authority boundaries remain explicit
```

This pattern is strongest for derivation, selection, comparison/reference, capability meaning, projection influence, component role, operational composition, and diagnostic conformance.

The evidence does not support treating this as a general rule for creating surfaces. It supports the narrower finding that repeated relationship reconstruction is one recurring driver of self-knowledge surface emergence.

## Relationship reconstruction pressure model

A relationship reconstruction pressure appears when:

1. a value, output, or result exists;
2. the relationship needed to interpret it is implicit;
3. operators repeatedly reconstruct that relationship from code, docs, diagnostics, history, or memory;
4. later work names the absence as an explanatory gap;
5. a scoped surface may eventually preserve the relation as fields rather than prose alone.

This reframes the missingness question:

```text
not only: what fact is missing?
not only: what surface is missing?
also: what relationship keeps being reconstructed?
```

## Relationship preservation strength

| Relationship | Current class | Evidence-backed status | Reconstruction pressure |
| --- | --- | --- | --- |
| evidence -> conclusion | well preserved, scoped | `reasoning_path` carries evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and boundary | High historically; traceability work records conclusion visibility without derivation visibility. |
| candidate -> selected outcome | well preserved, scoped | `selection_path` carries candidates, selected result, selection factors, non-selected candidates, evidence, outcome, unknowns, and boundary | High historically; selected focus/result existed before candidate-to-outcome rationale was explicit. |
| comparison question -> selected reference | well preserved for history, unknown elsewhere | `reference_selection` carries selected reference, rationale, alternatives, authority boundary, limitations, and unsupported-domain unknowns | High historically; comparison existed while meaningful reference and baseline/expectation boundary were contested. |
| capability pressure -> operational meaning | well preserved, scoped | `capability_relationship` carries current access, operational benefit, pressure, unknown attainability, unknown expectation, reasoning, and limitations | High; capability pressure risked becoming acquisition guidance or expectation. |
| projection stage -> influence/non-influence | well preserved for declared stages | `projection_shape` carries stage, consumes, produces, influences, does-not-influence, authority boundary, and confidence | High; prior projection self-description required reconstructing stage behavior from code/timing labels. |
| component -> repository role | partially to well preserved, query-scoped | `component_audit` carries definitions, references, tests, consumers, graph evidence, architecture evidence, status, overlap, unresolved questions, and boundary | High for named components; still not a full component catalog. |
| specialized diagnostics -> operational story | partially preserved | `operational_story` composes focus, pressure, evidence, capabilities, constraints, gaps, impact, changes, outcomes, investigation path, unknowns, and boundary | High; operational meaning otherwise requires reading multiple surfaces together. |
| registry declaration -> implementation conformance | well preserved for registered diagnostics | `diagnostic_inventory` declares surface contracts; `diagnostic_shape_audit` checks declared fields against implementation evidence | High; diagnostic shape and boundary would otherwise be reconstructed from code and CLI. |
| predicate/provider -> observation domain | manually reconstructed | Observation-space investigation relates predicates, providers, capability pressure, and candidate domains; no first-class domain relation exists | Still high; current evidence says this relation is inferred manually. |
| pressure -> observation-space gap | manually reconstructed | Observation-space investigation maps capability pressure to candidate domains and gap types; no first-class pressure-to-domain surface exists | Still high. |
| question -> answering surface | manually reconstructed | Discoverability investigation says Seed often has answering surfaces but weaker question-to-surface discovery before selection | Still high. |
| surface -> follow-up surface | manually reconstructed | Reasoning-space translation says workers infer follow-up spaces manually | Still high. |
| answer -> next investigation | document/operator knowledge | Investigation documents preserve inquiry movement; implementation-backed surfaces do not generally preserve answer-to-next-investigation as a first-class relation | High in practice, weak as implementation-backed self-knowledge. |
| authority boundary -> acceptance/expectation/mutation authority | partially preserved | Many surfaces preserve read-only and mutation boundaries; general authority-gap analysis remains investigation-only | Medium-high. |

## Evidence of surface emergence after reconstruction

### Derivation: `reasoning_path`

Traceability work records that a conclusion could exist while derivation visibility was missing. `reasoning_path` now preserves evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and boundary.

```text
conclusion exists
    -> why does it exist?
    -> evidence/support chain reconstructed manually
    -> reasoning_path preserves scoped derivation relation
```

### Selection: `selection_path`

Traceability work separates selection from derivation. `selection_path` now preserves candidate set, selected result, selection factors, non-selected candidates, evidence, outcome, unknowns, and boundary.

```text
selected result exists
    -> why this result rather than another?
    -> candidate-to-outcome relation reconstructed manually
    -> selection_path preserves scoped selection relation
```

### Comparison/reference: `reference_selection`

Reference-selection investigations distinguish comparison output from the meaningful reference that anchors it. `reference_selection` preserves selected reference, rationale, alternatives, authority boundary, limitations, and unsupported-domain unknowns for history.

```text
comparison exists
    -> compared to what?
    -> reference and authority boundary reconstructed manually
    -> reference_selection preserves scoped reference relation
```

### Capability meaning: `capability_relationship`

Capability pressure risked being misread as deployment intent or acquisition guidance. `capability_relationship` preserves the relation among capability, current access, benefit, pressure, unknown attainability, unknown expectation, reasoning, and limitations.

```text
capability need exists
    -> what does this mean operationally?
    -> access/benefit/pressure/expectation boundary reconstructed manually
    -> capability_relationship preserves scoped operational relation
```

### Projection influence: `projection_shape`

Projection self-description previously exposed docstrings, timing labels, state fields, and query methods, but not a structured stage model. `projection_shape` now preserves consumes, produces, influences, does-not-influence, authority boundary, and confidence.

```text
projection output exists
    -> what stage produced or influenced it?
    -> implementation flow reconstructed manually
    -> projection_shape preserves stage relation
```

### Component role: `component_audit`

Component role questions required collecting definitions, references, tests, consumers, operational graph evidence, architecture evidence, overlap, status, and unresolved questions. `component_audit` now preserves that relationship for a named component.

```text
component name exists
    -> what role does it play?
    -> repository evidence bundle reconstructed manually
    -> component_audit preserves scoped component-role relation
```

### Diagnostic governance: `diagnostic_inventory` and `diagnostic_shape_audit`

Diagnostic governance previously required reconstructing CLI flags, registry entries, JSON/record support, fact emission, event-ledger writes, mutation behavior, implementation functions, and markers. Inventory and shape audit preserve the registry-to-implementation relationship.

```text
diagnostic surface exists
    -> what contract does it have?
    -> does implementation match declaration?
    -> inventory and shape audit preserve registry/conformance relation
```

## Relationships still reconstructed manually

### predicate/provider -> observation domain

Observation inventory and utilization expose provider and predicate evidence, but observation-domain coverage is not first-class. The observation-space investigation says operational pressure can be related back to observation-space coverage only by investigation, not by an implemented domain model.

Current class: manually reconstructed.

### pressure -> observation-space gap

Capability pressure can be related to missing evidence inside a partially observed domain or to a missing observation category. Current implementation preserves capability pressure and operational meaning, but not a first-class pressure-to-domain relation.

Current class: manually reconstructed.

### question -> answering surface

The discoverability investigation found that Seed often has the answering surface but lacks an even path from question to surface. Surface self-description is stronger after selection than before selection.

Current class: manually reconstructed.

### surface -> follow-up surface

Reasoning-space translation evidence says workers infer follow-up spaces manually: component to consumer, derivation to selection, selection to reference, pressure to capability, projection to fact support.

Current class: manually reconstructed.

### answer -> next investigation

Investigation documents preserve inquiry movement and open questions. Implementation-backed surfaces can show some unknowns and investigation paths, but they do not generally preserve answer-to-next-investigation as a first-class relation.

Current class: document/operator knowledge.

### authority boundary -> acceptance/expectation/mutation authority

Specific read-only and mutation boundaries recur across surfaces. General authority-gap recognition remains investigation-only.

Current class: partially preserved.

## Relationship classes that generate investigation work

| Class | Current preservation | Investigation pressure |
| --- | --- | --- |
| Derivation | well preserved, scoped | Lower now for implemented diagnostic conclusions; not universal proof. |
| Selection | well preserved, scoped | Lower for current focus/pressure selection; unsupported targets remain unknown. |
| Comparison/reference | partially to well preserved | Lower for history; high outside supported domain. |
| Influence/projection flow | well preserved for declared stages | Lower for projection stages; scoped to projection shape. |
| Operational meaning | partially to well preserved | Lower for capability pressure; high for pressure-to-domain gaps. |
| Component role | partially to well preserved | Lower for named components; high for complete catalog/reachability. |
| Diagnostic governance | well preserved for registered diagnostics | Lower for registered diagnostics; ordinary library code remains less governed. |
| Coverage | manually reconstructed | High; predicate/provider-to-domain remains not first-class. |
| Navigation/discoverability | manually reconstructed | High; surface choice before selection remains weak. |
| Follow-up/continuation | document/operator knowledge | High; answer-to-next-investigation remains mostly documentary. |
| Authority acceptance | partially preserved | Medium-high; specific boundaries preserved, general gap recognition absent. |
| Ownership | partially preserved | High where ownership, role, definition, consumption, and reachability are conflated. |
| Unknown | unknown/varies | Unknowns are often preserved locally, but unknown-class reconstruction is not centralized. |

## Document-only relationship knowledge

Some relationship knowledge currently exists primarily in investigations or operator reasoning rather than implementation-backed self-knowledge surfaces.

| Relationship | Current location | Implementation-backed? | Risk if investigations vanished |
| --- | --- | --- | --- |
| predicate/provider -> observation domain | observation-space investigation | No first-class domain relation | Domain coverage and absence reasoning would be reconstructed again. |
| pressure -> observation-domain gap | observation-space investigation | Not first-class | Missing evidence vs missing domain distinction would weaken. |
| question -> answering surface | discoverability investigation, docs map, operator knowledge | Partial via inventories/descriptions, not as router | Workers would need exact surface vocabulary before asking. |
| surface -> follow-up surface | reasoning-space translation investigation | No | Cross-surface continuation would remain manual. |
| answer -> next investigation | investigation lineage and handoff practice | Weak/partial | Why one answer opened the next branch would disappear. |
| translation -> context -> relationship progression | recent investigations | No implementation surface classifies the progression | The explanatory lens would vanish as implementation-backed knowledge. |
| relationship-preservation family membership | relationship-preservation investigation | No | Surfaces would remain individually useful but less comparable. |
| authority gap as general analyzer | traceability gap investigation | No | Specific boundaries remain, but general authority-gap recognition disappears. |

## What would disappear if investigations vanished?

If only implementation-backed self-knowledge surfaces remained, the following would still be preserved reasonably well:

- scoped evidence/intermediate/derived conclusion relations;
- scoped candidate/selection/outcome relations;
- history comparison/reference relations;
- capability/access/benefit/pressure relations;
- projection stage consumes/produces/influence/non-influence relations;
- component evidence bundle relations for named components;
- operational story composition fields;
- diagnostic registry/conformance relations.

The following would mostly disappear or become expensive manual reconstruction again:

- the claim that these surfaces form a relationship-preservation pattern;
- the progression from translation to context preservation to relationship preservation;
- predicate/provider-to-observation-domain interpretation;
- pressure-to-observation-gap classification;
- question-to-answering-surface mappings;
- surface-to-follow-up-surface mappings;
- answer-to-next-investigation continuity;
- general authority-gap interpretation beyond individual boundary fields;
- the distinction between missing data, missing explanatory layer, missing domain, missing surface, and missing authority when no current surface directly encodes the distinction.

## Supported conclusions

1. Several successful self-knowledge surfaces appear to have emerged from repeatedly reconstructed relationships.
2. The strongest examples are derivation, selection, reference, capability operational meaning, projection influence, component role, operational composition, and diagnostic registry/conformance.
3. Relationship reconstruction pressure is a recurring driver of surface creation, but not the only driver and not an implementation rule.
4. The most valuable surfaces tend to preserve relationships that were previously expensive, ambiguous, or unsafe to reconstruct manually.
5. Relationships still reconstructed manually include predicate/provider-to-observation-domain, pressure-to-observation-gap, question-to-answering-surface, surface-to-follow-up-surface, answer-to-next-investigation, and general authority-gap relations.
6. Some relationship knowledge currently exists only in investigation documents and operator practice, not implementation-backed surfaces.
7. The question `what relationship keeps being reconstructed?` is better aligned with recent evidence than asking only `what fact is missing?` or `what surface is missing?`.

## Unsupported conclusions

The evidence does not support these stronger claims:

- That every self-knowledge surface emerges from repeated relationship reconstruction.
- That repeated reconstruction should automatically trigger implementation.
- That Seed has or needs a general relationship-reconstruction detector.
- That relationship reconstruction pressure is official ontology or preserved cluster vocabulary.
- That document-only relationship knowledge should be promoted into runtime facts.
- That question-to-surface or surface-to-follow-up navigation should be implemented now.
- That observation-domain relationships should be implemented now.
- That relationship classes listed here are complete, canonical, or stable.
- That implementation-backed surfaces would be useless without investigations.
- That investigations have equal authority to implementation and tests.

## Open questions

- What threshold distinguishes repeated reconstruction pressure from ordinary one-off investigation work?
- How many independent investigations or operator questions must reconstruct a relationship before it becomes meaningful surface pressure?
- Which document-only relationships are stable enough to preserve more formally, if any?
- Can repeated reconstruction pressure be recognized without creating a roadmap, backlog, or implementation trigger?
- Are unknowns and unsupported domains themselves reconstructed relationships, or boundary context?
- Does repeated reconstruction happen more often around abstraction-boundary relationships than relationships inside one surface?
- How much relationship knowledge can remain safely in documents before it causes drift or rework?

## Acceptance answers

### Which relationships are repeatedly reconstructed by operators?

The strongest evidence supports repeated reconstruction of evidence-to-conclusion, candidate-to-selected-outcome, comparison-question-to-reference, capability-pressure-to-operational-meaning, implementation-stage-to-projection-influence, component-to-repository-role, registry-to-implementation-conformance, predicate/provider-to-observation-domain, pressure-to-observation-gap, question-to-answering-surface, surface-to-follow-up-surface, and answer-to-next-investigation relationships.

### Did those relationships lead to self-knowledge surfaces?

Some did. Derivation led to `reasoning_path`; selection led to `selection_path`; comparison/reference led to `reference_selection`; capability pressure meaning led to `capability_relationship`; projection influence led to `projection_shape`; component role led to `component_audit`; diagnostic contract/conformance led to `diagnostic_inventory` and `diagnostic_shape_audit`; operational composition led to `operational_story`.

### Which important relationships remain manual today?

Predicate/provider-to-observation-domain, pressure-to-observation-gap, question-to-answering-surface, surface-to-follow-up-surface, answer-to-next-investigation, complete component catalog role, and general authority-gap recognition remain manual, document-backed, or only partially preserved.

### Can relationship reconstruction pressure explain why certain self-knowledge surfaces emerge?

Partially yes. It explains why several high-value surfaces preserve relationships rather than only values: the relationship was repeatedly needed, expensive to reconstruct, and unsafe to leave implicit. It does not explain every surface or imply implementation work by itself.

### What relationship knowledge currently exists only in investigations rather than repository-visible surfaces?

The strongest document-only relationship knowledge is the translation-to-context-to-relationship progression, relationship-preservation family membership, predicate/provider-to-observation-domain coverage, pressure-to-observation-gap classification, question-to-answering-surface mapping, surface-to-follow-up-surface mapping, answer-to-next-investigation continuity, and general authority-gap interpretation.

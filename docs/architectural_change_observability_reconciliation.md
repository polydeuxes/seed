# Architectural Change Observability Reconciliation

## Scope And Boundary

This reconciliation asks whether Seed's current implementation-backed disciplines make architectural change consequences observable. It does not propose enforcement, immutability, plugin policy, fork detection, licensing, repository protection, or governance.

Repository authority wins. Evidence here is limited to implemented code, tests, diagnostics, and existing reconciliations that are backed by implementation or executable surfaces.

## Finding

Seed can partially observe the consequences of architectural change. The strongest support is not a single "architecture monitor" but a recurring discipline: responsibilities are represented as bounded surfaces, projection stages, fact support, inquiry artifacts, diagnostic contracts, authority-constrained evaluators, and read-only explanatory diagnostics. When one of those responsibilities is removed, current mechanisms often reveal not only that something changed, but which explanatory capability, boundary, provenance path, or uncertainty field disappeared.

The support is strongest for registered diagnostics and projected-state responsibilities. It is weaker for ordinary library internals and historical prose-only concepts.

## Files Inspected

- `AGENTS.md`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/explanations.py`
- `seed_runtime/facts.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/question_surface_inventory.py`
- `docs/repeatedly_reconstructed_relationships_investigation.md`
- `docs/reasoning_chain_visibility_investigation.md`
- `docs/repository_shape_coverage_investigation.md`
- `docs/translation_surfaces_pattern_investigation.md`
- `docs/relationship_preservation_across_abstraction_boundaries_investigation.md`
- `docs/seed_self_knowledge_usefulness_exercise.md`

## Implementation-Backed Evidence

### Diagnostic surfaces declare responsibilities and boundaries

`DiagnosticInventoryEntry` is not only a command list. It declares CLI flags, state/file use, JSON and record support, record scope, emitted diagnostic or cluster facts, event-ledger writes, mutation behavior, diagnostic-fact reads, and a description. This means architectural changes to diagnostic surfaces can be compared against a declared operational shape.

The registry also encodes the diagnostic recording boundary: recorded diagnostic facts use `record_scope=diagnostic_run`, event-ledger writing is explicit, and `mutates_cluster` is explicit. Removing those fields would not merely remove metadata; it would remove Seed's ability to distinguish read-only diagnostic observation from cluster mutation.

### Diagnostic shape audit compares declarations to implementation evidence

`diagnostic_shape_audit` binds registry declarations to implementation specs and audited fields such as record support, JSON support, record scope, diagnostic facts, event-ledger writes, repository-file reads, projected-state reads, diagnostic-fact reads, and cluster mutation. The app currently reports 44 diagnostics audited, 396 consistent rows, and zero mismatches.

That result is implementation-backed evidence that current registered operational surfaces have a conformance mechanism. If a diagnostic implementation changed without its registry/spec changing, this mechanism can reveal the regression as a field-level mismatch instead of only a vague command failure.

### Projection shape explains stage capability, not only existence

`projection_shape` represents each projection stage with `consumes`, `produces`, `influences`, `does_not_influence`, an `authority_boundary`, and implementation-backed confidence. This is a self-explanation of subsystem contribution. For example, event replay consumes the event ledger and produces projected entities, observations, evidence, facts, goals, tool needs, approvals, execution authorizations, proposals, plans, and tools; alias projection consumes facts, produces alias indexes, and influences measurement retention, inference, conflict handling, and current fact selection.

A simplification that removes alias projection, fact support projection, inference, validation, or explanation inputs would therefore remove named produced artifacts and influence edges. Seed can describe the lost capability in the vocabulary already used by the projection-shape surface.

### Fact support and explanation preserve provenance and deterministic explanation

Fact support records preserve the subject, predicate, value, dimensions, supporting fact ids, source types, confidence, observation times, expiration state, predicate semantics, and support kind. `ExplanationBuilder.why` does not add a hidden reasoning mechanism; it traverses projected support, competing beliefs, conflicts, supporting facts, evidence ids, source types, confidence, observations, and inference links.

Removing fact support, evidence IDs, source fact links, conflict projection, or explanation traversal would therefore produce more than a test failure. It would make Seed unable to answer why a current belief is current, which facts supported it, which evidence IDs were involved, and which alternatives competed with it.

### Inquiry state renders uncertainty and authority boundary

Inquiry orientation is explicitly bounded and read-only. It renders related material, support/why-related text, uncertainty, and authority boundary. The implementation preserves uncertainty even when related material exists, and it states that deterministic lexical overlap is not interpretation, routing, or execution authority.

Removing this subsystem would naturally create unanswered inquiries such as why related material was selected, what remains uncertain, and what authority boundary applies to an inquiry note.

### Question-surface inventory maps questions to responsibilities

The app's `--question-surface-inventory` output lists question families, answering surfaces, responsibilities, and boundaries. This supports the claim that Seed can explain what a subsystem provides, rather than merely documenting that it exists. Examples include derivation explanation through `reasoning_path`, knowledge reachability through `knowledge_reachability`, surface shape validation through `diagnostic_shape_audit`, and projection stage visibility through `projection_shape`.

## Answers To Required Questions

### 1. Do current disciplines expose loss of authority, uncertainty, provenance, boundary visibility, and deterministic explanation?

Yes, in implementation-backed areas.

| Responsibility lost | Existing exposure mechanism | Consequence made observable |
| --- | --- | --- |
| Authority | authority-constrained evaluators, question-surface boundaries, projection-stage authority boundaries, diagnostic inventory mutation/ledger fields | Seed can say whether a surface is read-only, whether it writes events, whether it mutates cluster state, and which authority boundary a projection stage occupies. |
| Uncertainty | ownership authority evaluators, inquiry orientation, operational graph/story surfaces, capability relationship records | Seed can preserve unknown ownership, unknown attainability, unknown expectation, and uncertainty outside a bounded observation goal. |
| Provenance | fact support, evidence IDs, source types, source fact links, explanation traversal, source navigation | Seed can explain which facts and evidence support current beliefs. |
| Boundary visibility | diagnostic inventory, diagnostic shape audit, projection shape, question-surface inventory | Seed can distinguish registry declaration, implementation shape, projection influence, read-only use, recording, event-ledger writes, and mutation. |
| Deterministic explanation | `ExplanationBuilder.why`, reasoning-path and selection-path diagnostics, projection shape | Seed can render why-oriented outputs from projected state and existing diagnostics without invoking hidden reasoning. |

The qualification is important: these losses are naturally exposed where surfaces are registered, projected, or otherwise shaped. There is no complete repository-wide architectural-diff engine for every internal module.

### 2. Can Seed explain what capability a subsystem provides?

Yes for many implemented surfaces. The strongest evidence is structural rather than prose-only:

- `projection_shape` explains stages through consumed inputs, produced outputs, influence edges, non-influence edges, and authority boundaries.
- `diagnostic_inventory` explains operational surfaces through flags, state/repo use, record behavior, ledger behavior, mutation boundary, diagnostic-fact behavior, and descriptions.
- `question_surface_inventory` maps question families to answering surfaces, responsibility, and authority boundary.
- Existing reconciliations identify recurring translation surfaces such as `reasoning_path`, `selection_path`, `reference_selection`, `capability_relationship`, `projection_shape`, `component_audit`, `diagnostic_inventory`, and `diagnostic_shape_audit` as explaining relations, not merely naming modules.

### 3. Does the repository contain mechanisms that reveal architectural regressions?

Yes, implementation-backed mechanisms include:

- `diagnostic_shape_audit`: reveals registry/spec/implementation mismatch for registered diagnostic surfaces.
- `diagnostic_inventory`: reveals lost or changed public operational surface contracts.
- `projection_shape`: reveals lost projection-stage products, influence edges, and authority boundaries.
- `knowledge_reachability`: audits reachability across preserved, projected, read-model, inquiry, and rendered surfaces.
- `reasoning_path`, `selection_path`, and `reference_selection`: reveal broken or missing derivation, selection, and comparison/reference explanations in their scoped domains.
- `audit_snapshot` and `audit_compare`: provide behavioral comparison of selected audit outputs.
- Fact support, conflicts, and explanations: reveal lost provenance and current-belief explanation capability.

### 4. Can "architectural simplification is itself an observable inquiry" be supported?

Supported, with scope. Seed already treats questions as bounded inquiries with authority, uncertainty, provenance, and explanation boundaries. If simplification removes a responsibility, the observable inquiry becomes: what outputs, influence edges, support links, boundaries, or uncertainty fields disappeared?

This is not enforcement. It is an inquiry over existing surfaces: compare diagnostic shape, projection shape, knowledge reachability, explanations, reasoning paths, and audit snapshots before and after a change.

### 5. Would removing a subsystem naturally create new unanswered inquiries?

Yes. Current concepts imply predictable unanswered inquiries:

- Removing uncertainty rendering: why is uncertainty absent, and did the bounded question become overclaimed?
- Removing authority fields: why is authority unknown, and can read-only observation still be distinguished from mutation?
- Removing fact support/provenance: why can this claim no longer be reconciled to evidence?
- Removing inquiry orientation: why can this inquiry no longer explain its related material or boundary?
- Removing projection-stage shape: what consumed input, produced output, or influence edge was lost?

These are natural because the repository already preserves support, boundary, uncertainty, and responsibility as explicit outputs in multiple subsystems.

### 6. Does the architecture favor preventing change or making consequences observable?

Current implementation favors making consequences observable. The strongest implementation evidence is read-only diagnostics, explicit non-mutation boundaries, diagnostic recording scope, event-ledger distinctions, field-level shape audit, and explanatory projection surfaces. None of the reviewed mechanisms locks the architecture, prevents simplification, enforces immutability, detects forks, or governs plugins.

### 7. Is this recurring discipline or incidental property?

It is a recurring discipline, not merely incidental, but it is still uneven.

Recurring evidence:

- Diagnostic surfaces are systematically registered and shape-audited.
- Projection stages are described by inputs, outputs, influence, non-influence, and authority boundary.
- Explanations derive from projected support and provenance instead of hidden reasoning.
- Inquiry orientation renders uncertainty and authority boundary.
- Question-surface inventory presents responsibility and boundary for answering surfaces.
- Existing investigations repeatedly identify translation, relationship preservation, reasoning-chain visibility, and shape coverage as recurring patterns.

Unevenness:

- The discipline is strongest for operational diagnostics and projected-state machinery.
- Ordinary internal code does not have the same universal responsibility registry.
- Some architectural relationships remain reconstructable but fragmented across surfaces.
- Documentation can name concepts that are not implementation-backed; repository authority prevents promoting them without evidence.

## Observable Architectural Responsibilities

| Responsibility | Implementation-backed surface |
| --- | --- |
| Diagnostic public contract | `diagnostic_inventory` |
| Registry-to-implementation conformance | `diagnostic_shape_audit` |
| Projection responsibility and influence | `projection_shape` |
| Current-belief support and provenance | `FactSupport`, explanations, state fact-support projection |
| Deterministic why explanation | `ExplanationBuilder.why`, reasoning-path diagnostics |
| Inquiry uncertainty and authority boundary | inquiry orientation |
| Question-to-surface responsibility routing | question-surface inventory |
| Bounded authority-aware observation | container, service, and listener authority evaluators |
| Behavioral comparison | audit snapshots and audit compare |

## Observable Architectural Regressions

Seed can currently make these regressions visible in scoped ways:

- A diagnostic surface exists in code but not in inventory.
- A diagnostic inventory declaration disagrees with implementation shape.
- A diagnostic that writes events or records facts lacks the expected diagnostic-run scope or non-mutation boundary.
- A projection stage no longer produces expected read-model material or influence edges.
- Current belief explanation loses supporting fact IDs, evidence IDs, source types, or conflict visibility.
- Inquiry orientation loses uncertainty or authority boundary text.
- Knowledge stops reaching rendered or inquiry surfaces.
- A reasoning path loses evidence, intermediate conclusions, derived conclusions, consumers, or story impact.

## Contradictory Evidence And Limits

- There is no single repository-wide architecture-change observability command.
- Shape audit is static and scoped to registered diagnostics; it does not prove runtime truth for every subsystem.
- Projection shape is implementation-backed but manually enumerated; it is not automatic semantic extraction from all projection code.
- Documentation remains mixed: historical reconciliations are evidence, not necessarily current canonical architecture.
- Some relationships are reconstructable only by joining multiple surfaces manually.
- A simplification could remove both a responsibility and the surface that would have reported it; current discipline makes this visible only if tests, inventory, snapshots, or adjacent surfaces are still run and preserved.

## Remaining Uncertainty

- How much ordinary non-diagnostic library code should become shape-visible remains unresolved.
- Whether architectural observability should become a first-class diagnostic is not answered here.
- The current repository can often explain what was lost, but not uniformly across every subsystem.
- The strongest evidence comes from recently added operational surfaces; older domains may be less explicit.

## Acceptance Answers

### Can Seed observe the consequences of architectural change?

Yes, partially and implementation-backed. Seed can observe many consequences through diagnostic inventory, shape audit, projection shape, fact support/explanation, inquiry orientation, question-surface responsibility mapping, knowledge reachability, reasoning/selection/reference diagnostics, and audit comparison.

### Does Seed naturally explain what was lost, or merely detect that something changed?

In the strongest domains, it explains what was lost. The explanation is field- and relation-level: lost record scope, lost mutation boundary, lost produced projection artifact, lost influence edge, lost supporting fact IDs, lost evidence IDs, lost uncertainty, lost authority boundary, or lost reasoning-path consumer. In weaker domains, it may only detect that output changed or leave reconstruction to manual comparison.

### Is architectural observability intentional discipline or only consequence of current design?

It is an intentional discipline emerging from implementation. The recurrence across diagnostic inventory, diagnostic shape audit, projection shape, explanation, inquiry orientation, question-surface inventory, and prior reconciliations shows a repeated architectural preference for bounded, explainable, authority-aware visibility. It is not yet complete enough to call a universal architecture observability system.

## Files Changed

- `docs/architectural_change_observability_reconciliation.md`

## LOC Changed

- Added 221 lines.

## Tests And App Checks Run

- `python scripts/seed_local.py --diagnostic-shape-audit --status mismatch` — passed; no mismatches.
- `python scripts/seed_local.py --projection-shape --json | head -60` — passed; confirmed projection shape exposes stage consumes/produces/influences/authority boundary and read-only boundary.
- `python scripts/seed_local.py --question-surface-inventory | head -80` — passed; confirmed question families map to responsibilities and boundaries.
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed.

## Recommended Next Bounded Investigation

Investigate whether one existing non-diagnostic subsystem can be represented with the same implementation-backed shape vocabulary already used by diagnostics and projection stages: responsibility, consumes, produces, influences, authority boundary, provenance contribution, uncertainty contribution, and tests that fail when the responsibility becomes invisible.

# Repository Orientation Audit

## Scope and method

This audit records repository-supported understanding only. It does not create theory, reconciliation, architecture proposals, future-state designs, or new lens/view/orientation models.

## Files inspected

Required files inspected:

- `docs/state_summary_scope_review.md`
- `docs/lens_vs_orientation_observation.md`
- `docs/inquiry_as_bridge_observation.md`
- `docs/inquiry_as_movement_observation.md`
- `docs/unresolvedness_observation.md`
- `docs/descriptive_vs_architectural_vocabulary_observation.md`
- `docs/promotion_and_reconciliation_observation.md`

Additional lens/view/orientation files discovered through references and inspected:

- `docs/lens_catalog_observation.md`
- `docs/lens_view_reconciliation.md`
- `docs/lens_orientation_and_dashboard_observation.md`
- `docs/lens_as_observation_and_compression_pattern.md`
- `docs/lens_implementation_frontier_observation.md`
- `docs/lens_view_architecture_audit.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/orientation_object_observation.md`
- `docs/work_shape_and_orientation_observation.md`
- `docs/orientation_bundle_load_bearing_observation.md`
- `docs/orientation_non_convergence_audit.md`

## Per-document records

### `docs/state_summary_scope_review.md`

- Major findings: State Summary has two layers: compact projected world-model summary and richer operator State Summary. Repository evidence supports State Summary as a deterministic, read-only summary of projected State/read model.
- Explicit uncertainties: State Summary contains sections that appear overloaded, especially top entities, availability, graph issues/conflicts/stale facts, storage/filesystem interpretation, and observation source counts.
- Explicit non-conclusions: The review does not redesign implementation, remove output, add output, rename commands, or introduce a dashboard or node-specific operational view.
- Architectural findings: State Summary should describe shape, identity, and integrity-adjacent accounting of projected State; it should not be the default authority for every operator interpretation of State.
- Descriptive findings: Top entities, endpoint visibility, host/service/storage prominence buckets, availability by scope, legacy availability, filesystem shape summaries, shared-storage candidates, and bounded detail selection appear to be lenses over State.

### `docs/lens_vs_orientation_observation.md`

- Major findings: State is strongly supported as current deterministic projected world/read model; lens evidence supports bounded, deterministic, read-only viewing; orientation evidence is less implementation-backed and more continuation- and participant-facing.
- Explicit uncertainties: The candidate State/Lens/Orientation distinction is treated as observation, not conclusion; `Lens` is not canonical runtime vocabulary and `Orientation` is even less settled.
- Explicit non-conclusions: The document does not implement lenses, redesign runtime behavior, modify State Summary, modify Inquiry Orientation, introduce ontology, create policy, or promote lens, orientation, or concern to canon.
- Architectural findings: Lens-like behavior selects, groups, ranks, suppresses, formats, scopes, or caveats projected material; Inquiry Orientation is a special relation-sensitive lens candidate rather than a simple State-only lens.
- Descriptive findings: Candidate shorthands are recorded: State answers what exists in projected State, Lens answers how projected State or preserved knowledge is viewed, and Orientation answers where attention, relevance, pressure, or continuation is directed.

### `docs/inquiry_as_bridge_observation.md`

- Major findings: Inquiry does not reduce to a single stable object; inquiry-note evidence, projected facts, source-navigation links, repository documents, and handoff/continuation materials make Inquiry Orientation a compound case.
- Explicit uncertainties: The Lens/Orientation distinction may be wrong or too sharp; Inquiry Orientation may be a compound phrase rather than evidence for separate Lens, Inquiry, and Orientation concepts.
- Explicit non-conclusions: The document does not modify implementation, Inquiry Orientation, State Summary, lens behavior, ontology, runtime concepts, or policy; it does not conclude that Inquiry Orientation should be changed or that Lens, Inquiry, and Orientation should become a formal pipeline.
- Architectural findings: Inquiry Orientation begins with preserved inquiry-note evidence and produces related material plus authority/uncertainty framing without mutating State.
- Descriptive findings: Inquiry is tested as a bridge: Lens may preserve and shape inquiry evidence, and Orientation may expose what becomes live for attention and continuation.

### `docs/inquiry_as_movement_observation.md`

- Major findings: Inquiry is stronger as movement than as a stable middle object between Lens and Orientation; implementation has `InquiryNote`, `RelatedMaterial`, and `InquiryOrientationView`, but not an `Inquiry` object.
- Explicit uncertainties: Whether inquiry should remain descriptive vocabulary, whether to add an architectural `Inquiry` object, and whether reachability gaps are caused by missing relation indexes remain unresolved.
- Explicit non-conclusions: The document does not modify implementation, Inquiry Orientation, State Summary, lenses, ontology, runtime concepts, or policy.
- Architectural findings: Existing tests check that recording an inquiry note does not change facts, goals, tool needs, plans, or tools; orientation output includes uncertainty and authority boundary sections and does not mutate State.
- Descriptive findings: Orientation is adjacent to movement but not identical to it; Orientation relates participants to currently relevant material and continuation position more than it names question direction or pursuit.

### `docs/unresolvedness_observation.md`

- Major findings: Repository evidence supports unresolvedness as useful descriptive language for gaps, differences, uncertainty, incomplete work, unfinished understanding, and unsettled questions.
- Explicit uncertainties: The candidate model is intentionally weaker than a conclusion; repository authority wins wherever it fails.
- Explicit non-conclusions: The document does not modify implementation, Inquiry Orientation, State Summary, continuation behavior, handoff behavior, ontology, runtime concepts, or policy, and does not add unresolvedness to Inquiry Orientation.
- Architectural findings: Inquiry Orientation exists as `InquiryOrientationView`, but the repository does not implement an `Inquiry` runtime object.
- Descriptive findings: State answers what exists in projected State, and Orientation answers where attention is currently directed or how a participant is situated relative to current material; Orientation may orient a participant toward, away from, or around unresolvedness.

### `docs/descriptive_vs_architectural_vocabulary_observation.md`

- Major findings: Descriptive vocabulary helps participants see, explain, group, or preserve recurring pressure; architectural vocabulary participates in repository structure, authority, implementation, projection, validation, reconciliation, or runtime behavior.
- Explicit uncertainties: The distinction may describe concept maturity, authority routing, evidence strength, or delayed promotion rather than a sharp boundary.
- Explicit non-conclusions: The document does not modify implementation, ontology, Inquiry Orientation, State Summary, runtime concepts, policy, or repository primitives, and does not promote any term.
- Architectural findings: Context Views, State projections, Confidence, Evidence Graph, Contradiction Detection, and State Summary are architectural when they define what gets projected, selected, omitted, rendered, or used by decision providers.
- Descriptive findings: Orientation appears closer to architectural vocabulary than many descriptive terms, but its status remains careful; orientation-related work investigates load-bearing roles without making every orientation phrase architectural.

### `docs/promotion_and_reconciliation_observation.md`

- Major findings: The prior contrast tested is “descriptive vocabulary explains; architectural vocabulary participates.” Current evidence shows promotion is not inevitable, not necessarily desirable, and not always a simple pipeline.
- Explicit uncertainties: The document does not assume promotion is desirable, inevitable, safe, or even a real repository process.
- Explicit non-conclusions: The document does not modify implementation, ontology, Inquiry Orientation, State Summary, runtime behavior, projection behavior, catalogs, validation, tests, policy, or repository primitives; it does not introduce a promotion pipeline or promote any concept.
- Architectural findings: Observation, Evidence, Fact, Relationship, and capability verification readiness show bounded architectural participation; capability readiness is architectural but explicitly not promotion.
- Descriptive findings: Orientation shows stronger participation than some descriptive vocabulary but remains an example where participation does not equal settled promotion.

### `docs/lens_catalog_observation.md`

- Major findings: Repository evidence supports a cautious working definition of lens as a deterministic, read-only way of viewing projected State for a bounded question, attention pattern, or interpretive purpose.
- Explicit uncertainties: It is exploratory and does not authorize a lens framework, command, dashboard, registry, ontology, or runtime API.
- Explicit non-conclusions: The document does not implement lenses, add commands, redesign State Summary, redesign Inquiry Orientation, introduce dashboards, or promote a new canonical concept.
- Architectural findings: Multiple candidate lenses can view the same deterministic State; Inquiry Orientation appears as a relation-sensitive lens, not a simple State-only lens.
- Descriptive findings: HomeOps Dashboard and Node Detail are plausible composed attention surfaces, but not implementation conclusions.

### `docs/lens_view_reconciliation.md`

- Major findings: The repository supports a common model only as architectural vocabulary for current evidence; it does not yet support a formal lens framework, registry, view composition API, HomeOps surface, or Seed Ops surface.
- Explicit uncertainties: Open questions include sufficient authority to define HomeOps or Seed Ops and boundaries for view composition.
- Explicit non-conclusions: It does not implement lenses, implement views, redesign State Summary, create HomeOps, create Seed Ops, or promote a new canonical primitive.
- Architectural findings: View presents read-only projected or lens-shaped material to a consumer; State Summary is a combination: compact State View plus richer operator-facing summary plus embedded lens-like selections.
- Descriptive findings: HomeOps appears closer to a future View composed from lenses than to a Lens, but repository evidence does not support creating it now or treating State Summary as HomeOps.

### `docs/lens_orientation_and_dashboard_observation.md`

- Major findings: The document records a shift while discussing inquiry orientation, State Summary, dashboards, and lens-based observation; orientation may be less about what Seed knows and more about a participant’s relationship to what Seed knows.
- Explicit uncertainties: It does not reconcile orientation and does not define canonical architecture.
- Explicit non-conclusions: It does not propose runtime behavior, output format, taxonomy, or surface.
- Architectural findings: State versus lens framing distinguishes State as material, lens as selection/organization/interpretation, and dashboard as operator-facing surface.
- Descriptive findings: Orientation is described as interaction, comparable to seeing rather than the thing seen.

### `docs/lens_as_observation_and_compression_pattern.md`

- Major findings: Lens language appears to help participants observe, compress, and notice scattered evidence or pressure.
- Explicit uncertainties: It does not define `lens` canonically.
- Explicit non-conclusions: It does not retitle existing concepts as lenses, reconcile them, or promote lens vocabulary.
- Architectural findings: Broad terms become unsafe if they replace source authority, support paths, caveats, relationships, policy boundaries, or validated architecture.
- Descriptive findings: Lens is primarily recorded as an observation and compression pattern in repository practice.

### `docs/lens_implementation_frontier_observation.md`

- Major findings: Candidate lenses already partially exist in State Summary, storage projection, availability grouping, projection integrity, source navigation, and Inquiry Orientation; HomeOps Dashboard remains conceptual and architecturally blocked.
- Explicit uncertainties: Inquiry Orientation V1 is implemented as an isolated probe, while generalization remains unresolved.
- Explicit non-conclusions: It does not implement lenses, alter CLI behavior, create dashboards, modify Inquiry Orientation, redesign State Summary, or recommend State Summary redesign.
- Architectural findings: Inquiry Orientation V1 is classified as a real prototype lens with unresolved generality.
- Descriptive findings: HomeOps Dashboard is a candidate/operator-value idea with low implementation readiness.

### `docs/lens_view_architecture_audit.md`

- Major findings: Repository support is stronger for `State Views` and `Context Views` than for a general `lens` primitive; lens language exists mostly in exploratory observations and scope reviews.
- Explicit uncertainties: The repository has not established a formal `Lens -> many Views` contract.
- Explicit non-conclusions: It does not implement views, implement dashboards, redesign State Summary, create Seed Ops, create HomeOps, or promote a formal lens/view framework.
- Architectural findings: State Views and Context Views are deterministic read-only projections of an already-built State object; views expose selected structures to a consumer and are not merely presentation.
- Descriptive findings: HomeOps appears as an operator-oriented possibility in lens/dashboard documents, but not as an implemented or authorized surface.

### `docs/view_authority_and_surface_responsibility_reconciliation.md`

- Major findings: Output surfaces can carry authority risk because labels, grouping, omission, and placement can imply stronger claims than the underlying facts support.
- Explicit uncertainties: Integrity surfaces answer where Seed is uncertain.
- Explicit non-conclusions: It does not create new view runtime behavior.
- Architectural findings: Evidence, interpretation, integrity, and navigation surfaces have distinct responsibilities and authority boundaries.
- Descriptive findings: View responsibility includes presentation and surface responsibility, not only data production.

### `docs/orientation_object_observation.md`

- Major findings: Orientation is investigated as a possible object-like concept under repository evidence, especially around attention, relevance, pressure, activation, and continuity.
- Explicit uncertainties: It is a working description under test, not a definition.
- Explicit non-conclusions: It does not define a new architecture, ontology, interface, or remediation plan.
- Architectural findings: Orientation-related evidence is tested against existing surfaces such as Inquiry Orientation, current work, active edge, continuation, and handoff.
- Descriptive findings: Orientation tends to describe attention and situated relation rather than identity, agency, or subjecthood.

### `docs/work_shape_and_orientation_observation.md`

- Major findings: Work shape and orientation are inspected as repository language around current work, continuation, active edge, and handoff.
- Explicit uncertainties: The authority boundary does not treat the observation as implementing or promoting orientation.
- Explicit non-conclusions: It does not change implementation or architecture.
- Architectural findings: Existing repository terms such as current work position and active edge remain the stronger concrete surfaces.
- Descriptive findings: Orientation language helps describe how work is recognizable and situated.

### `docs/orientation_bundle_load_bearing_observation.md`

- Major findings: Orientation appears as a possible bundle of elements rather than a single settled object.
- Explicit uncertainties: The review does not assume all elements are required, complete, independent, or sufficient.
- Explicit non-conclusions: It does not promote orientation to a runtime primitive or ontology object.
- Architectural findings: Candidate load-bearing elements are checked against existing documented surfaces.
- Descriptive findings: Orientation may bundle current concern, reference point, active edge, continuity, and authority awareness.

### `docs/orientation_non_convergence_audit.md`

- Major findings: Orientation does not converge as an implemented runtime primitive and is strongest as handoff and understanding prose.
- Explicit uncertainties: Orientation may still survive as useful prose compression or name the experienced result of several repository mechanisms.
- Explicit non-conclusions: It does not defend orientation, attack orientation, propose implementation, or propose remediation.
- Architectural findings: Orientation is absent from core runtime contracts and has not converged into a single documentation authority surface.
- Descriptive findings: Orientation overlaps with reference point, current concern, active edge, selection, attention target, continuity, preservation, navigation, and authority awareness.

## Findings Matrix

| Concept | Evidence found | Participates architecturally? | Appears descriptive? | Appears architectural? | Explicit uncertainty? | Referenced by which documents? |
|---|---|---:|---:|---:|---:|---|
| State | Current deterministic projected world/read model produced from event history; State answers what exists in projected State. | Yes | Yes, as shorthand in observations | Yes | Low for projected-State authority; caveat that `exists` means projected State, not unqualified truth | `state_summary_scope_review`, `lens_vs_orientation_observation`, `lens_catalog_observation`, `lens_view_reconciliation`, `lens_view_architecture_audit`, `unresolvedness_observation` |
| Lens | Bounded deterministic read-only viewing of projected State or preserved knowledge; selects, groups, ranks, suppresses, formats, scopes, or caveats material. | Partly; implemented behavior exists in views/summaries, but no canonical lens primitive | Yes | Partly as architectural description, not runtime primitive | Yes | `lens_vs_orientation_observation`, `lens_catalog_observation`, `lens_view_reconciliation`, `lens_as_observation_and_compression_pattern`, `lens_implementation_frontier_observation`, `lens_view_architecture_audit`, `state_summary_scope_review` |
| View | State Views and Context Views are implemented deterministic read-only projections; view presents read-only projected or lens-shaped material to a consumer. | Yes | Yes, when used as output/surface language | Yes, especially implemented State Views/Context Views | Yes for general lens/view composition and formal framework | `lens_view_reconciliation`, `lens_view_architecture_audit`, `view_authority_and_surface_responsibility_reconciliation`, `state_summary_scope_review` |
| Orientation | Evidence around directedness, continuation, activation, work position, attention, relevance, pressure, and participant relation. | Limited; Inquiry Orientation exists, but orientation itself does not converge as runtime primitive | Yes | Partly/locally, especially Inquiry Orientation and handoff surfaces | Yes | `lens_vs_orientation_observation`, `inquiry_as_bridge_observation`, `inquiry_as_movement_observation`, `unresolvedness_observation`, `descriptive_vs_architectural_vocabulary_observation`, `promotion_and_reconciliation_observation`, `orientation_non_convergence_audit`, `orientation_object_observation`, `orientation_bundle_load_bearing_observation` |
| State Summary | Deterministic read-only summary of projected State/read model; combination of compact State View plus richer operator-facing summary with embedded lens-like selections. | Yes | Yes, as operator-facing summary language | Yes | Yes, overloaded responsibilities identified | `state_summary_scope_review`, `lens_view_reconciliation`, `lens_view_architecture_audit`, `lens_vs_orientation_observation`, `lens_implementation_frontier_observation` |
| HomeOps | Appears in exploratory lens/dashboard and State Summary boundary documents; repository says State Summary is not HomeOps. | No implemented authority found | Yes | No repository authority found for implemented architectural concept | Yes | `state_summary_scope_review`, `lens_catalog_observation`, `lens_view_reconciliation`, `lens_implementation_frontier_observation`, `lens_view_architecture_audit` |

## Per-concept findings

### State

- What is State? Repository evidence supports State as the current deterministic projected world/read model produced from event history. The safe shorthand is that State answers what exists in projected State.
- What is State not? State is not unqualified real-world truth; `exists` is safe only when read as `exists in projected State`. State is not the lens, view, orientation, dashboard, or operator interpretation over projected material.
- How much authority exists? Authority is strong for projected-State/read-model meaning. The inspected observations treat State as the strongest of the State/Lens/Orientation concepts.

### Lens

- What findings exist? Lens is a bounded deterministic read-only way of viewing projected State or preserved knowledge for a bounded question, attention pattern, or interpretive purpose.
- What participation exists? Lens-like behavior appears in State Summary sections, storage projection, availability grouping, projection integrity, source navigation, and Inquiry Orientation V1.
- What uncertainties remain? Lens is not a canonical runtime primitive, no formal lens registry or API exists, and the repository does not yet establish a formal `Lens -> many Views` contract.

### View

- Does repository authority establish View as a category? Yes for implemented `State Views` and `Context Views`, and for the responsibility that a view presents read-only projected or lens-shaped material to a consumer.
- Or is View currently hypothesis/explanation? A general formal lens/view framework and composition contract remain unsupported; View has stronger evidence than Lens where implemented modules exist.
- What evidence exists? `State Views` and `Context Views` are deterministic read-only projections from State. View responsibility includes exposing selected structure to a consumer and preserving authority boundaries.

### Orientation

- What findings exist? Orientation evidence concerns directedness, continuation, activation, work position, attention, relevance, pressure, and participant relation to known or preserved material.
- Is Orientation architectural? Partly and locally where `InquiryOrientationView` and Inquiry Orientation behavior exist. Orientation as a general concept has not converged into an implemented runtime primitive or single authority surface.
- Descriptive? Yes. Multiple documents record orientation as handoff/understanding prose, participant relation, or useful compression.
- Unsettled? Yes. Orientation overlaps with reference point, current concern, active edge, selection, attention target, continuity, preservation, navigation, and authority awareness.

### State Summary

- What findings exist? State Summary is a deterministic, read-only summary of projected State/read model. It currently has compact projected world-model summary and richer operator State Summary layers.
- What overloaded responsibilities were identified? Top entities, availability, graph issues/conflicts/stale facts, storage/filesystem interpretation, and observation source counts.
- What responsibilities appear architectural? Projection identity, State cardinality, fact lifecycle accounting, support/provenance accounting, and count-level projection-integrity accounting.
- What responsibilities appear lens-like? Top entities by kind, endpoint visibility without names, host/service/storage prominence buckets, alias counts, availability by scope, legacy all-entity availability, filesystem shape summaries, shared-storage candidates, topology ambiguity summaries, mount filtering, display priority, and bounded detail selection.

### HomeOps

- Is HomeOps a Lens? Older exploratory language can call HomeOps a lens, but reconciliation says HomeOps appears closer to a future View composed from lenses than to a Lens.
- View? Repository evidence supports only future/operator-oriented possibility language, not implementation.
- Projection? No repository authority found.
- Operator concept? Yes as exploratory/operator-oriented context or attention surface language.
- Unknown? Yes for current architecture. No repository authority found for HomeOps as an implemented architectural concept.

## Confirmed findings

- State has strong repository authority as projected State/read model.
- Lens has repository support as exploratory/bounded read-only viewing vocabulary and as partially existing behavior, but not as a canonical runtime primitive.
- View has implementation-backed authority for State Views and Context Views.
- Orientation remains unsettled as a general concept and is strongest as handoff/understanding prose plus local Inquiry Orientation behavior.
- State Summary is a combination: compact State View/read-model summary plus richer operator-facing summary plus embedded lens-like selections.
- HomeOps is not State Summary and is not implemented; it appears only as exploratory/operator-oriented future surface language.

## Major uncertainties

- Whether Lens should remain vocabulary, become a primitive, or only describe existing read/view projections.
- Whether a formal `Lens -> many Views` contract exists or should exist; current repository authority says it is not established.
- Whether Orientation is distinct from reference point, current concern, active edge, selection, attention target, continuity, preservation, navigation, and authority awareness.
- Whether Inquiry Orientation is a special lens, a compound surface, or evidence that the Lens/Orientation distinction is too sharp.
- What would count as sufficient repository authority to define HomeOps or Seed Ops.

## Unsupported hypotheses currently being assumed

- State/Lens/Orientation is a formal ontology.
- Lens is a canonical runtime primitive.
- A lens registry, lens runtime API, or view composition API exists.
- View is only presentation.
- Orientation is a settled architectural primitive.
- Inquiry Orientation proves a formal Lens -> Inquiry -> Orientation pipeline.
- State Summary is a HomeOps dashboard, node dashboard, runtime health checker, attention queue, recommendation engine, or the only canonical way operators interact with State.
- HomeOps is an implemented Lens, View, Projection, surface, or architectural category.

# Explanation Selection / Sequencing / Composition Topology Audit 001

## Bounded audit question

For several shared explanation rendering projections associated with one bounded inquiry, what establishes membership, what preserves constitutional lineage order, what may determine operator encounter order, and what responsibility merely composes the result?

This audit does not implement selection, sequencing, or composition. It does not modify source or tests. It treats repository implementation as authority and preserves the distinction between constitutional reasoning order and operator encounter order.

## Reviewed evidence

Primary implementation and report evidence reviewed:

- `seed_runtime/shared_explanation_rendering_projection.py` and `tests/test_shared_explanation_rendering_projection.py` for the current shared rendering projection boundary.
- `shared_explanation_presentation_contract_audit_001.md` and `shared_explanation_rendering_projection_slice_001.md` for prior explanation rendering analysis.
- `seed_runtime/operator_authority_scope_binding.py` and `tests/test_operator_authority_scope_binding.py` for ingress authority/scope explanation ownership.
- `seed_runtime/representation_grammar_applicability.py` and `tests/test_representation_grammar_applicability.py` for representation grammar applicability explanation ownership.
- `seed_runtime/capability_reachability_projection.py` and `tests/test_capability_reachability_projection.py` for the reachability stage that can follow ingress and grammar applicability.
- `capability_demand_realization_reachability_topology_audit_001.md`, `capability_derivation_operational_realization_topology_audit_001.md`, and `capability_reachability_projection_slice_001.md` for topology and reachability lineage evidence.
- `seed_runtime/reasoning_path_audit.py` and `tests/test_reasoning_path_audit.py` for derivation-path visibility, supporting evidence, derived conclusions, consumers, and Unknown handling.
- `seed_runtime/selection_path_audit.py`, `tests/test_selection_path_audit.py`, `constitutional_relationship_selection_path_completion_audit.md`, and `selection_path_answer_composition_completion_audit.md` for selection-path visibility and candidate preservation.
- `answer_composition_projection_navigation_audit.md`, `answer_composition_slice_005.md` through `answer_composition_slice_008.md`, and `reasoning_path_answer_composition_completion_audit.md` for answer composition precedent.
- `docs/contradiction_discovery_and_visibility_reconciliation.md`, `docs/knowledge_acquisition_and_selection.md`, `docs/operator_interface_and_projection_authority_reconciliation.md`, `docs/container_ownership_answer_ordering_reconciliation.md`, and `docs/projection_self_description_investigation.md` for visibility, explanation, context composition, projection authority, and presentation-order boundary evidence.

## Current implementation anchor

`SharedExplanationRenderingProjection` consumes exactly one already-produced stage-local explanation. Its own boundary says it does not compare, aggregate, order, or compose explanations. Its rendering boundary says shared field names are display labels only and all constitutional meaning remains authored and owned by the source stage.

The projection preserves source explanation identity, source artifact owner, source explanation type, producer, attempted movement, source state, source reason, Unknowns, conflicts, prohibited downstream movement, explanation boundary, opaque stage-owned material, read-only state, event-ledger state, mutation state, and rendering convention.

Therefore the current shared projection is a per-explanation rendering adapter. It is not the selector of several explanations, not the sequencer of several explanations, not a constitutional lineage owner, and not a bounded-view composer.

## Membership-selection findings

Question: which projections belong to this bounded inquiry?

Membership is established by an upstream bounded inquiry identity and source-reference relationship, not by display order or severity. Repository evidence supports membership only when each candidate projection can be tied to the same bounded inquiry, demand, handoff, source artifact, selected work, or projected subject under review.

For explanation rendering projections, membership selection should inspect:

- source explanation identity;
- source artifact owner and source artifact type;
- attempted movement;
- inquiry or demand reference when exposed by the source stage;
- handoff references and upstream/downstream artifact references;
- relevance evidence connecting the stage result to the bounded inquiry;
- required explanation roles for the bounded inquiry;
- duplicate source explanations or alternative projections from the same stage;
- missing expected stages;
- unrelated projections that merely share labels such as `blocked`, `unknown`, or `read_only`.

Selection must not mean choosing only the most severe, most blocking, latest, first-returned, or most prominent result. The reachability implementation is direct evidence: multiple supporting candidates establish no preference among them, reachability does not select a realization, and Unknown or unsupported candidates are preserved separately. That same discipline applies here: a later immediate blocker does not erase ingress or grammar applicability projections that belong to the same inquiry.

Current owner status: no implemented multi-explanation membership selector exists. Membership is therefore not owned by `SharedExplanationRenderingProjection`; it must be an upstream bounded-inquiry selection responsibility if implemented later.

## Constitutional-lineage findings

Question: in what order were these results constitutionally produced or depended upon?

Constitutional lineage order is preserved by source-stage provenance, handoff identity, dependency references, derivation paths, and stage-owned source artifacts. It is not derived from timestamps, artifact IDs, lexical sort, registration order, implementation call order, or display position.

Existing evidence supports lineage preservation through:

- stage-owned explanation identity and source artifact ownership in shared rendering projections;
- inquiry, artifact, work-contract, capability-demand, candidate-set, and handoff references in the capability road;
- reasoning-path separation of evidence, intermediate conclusions, derived conclusions, consumers, story impact, and Unknowns;
- selection-path candidate set, selection factors, non-selected candidates, evidence, outcome, and Unknowns;
- explicit non-mutation and read-only boundaries that prevent presentation from becoming a new derivation.

For the required reordered case, the constitutional lineage may remain:

```text
ingress permitted
-> grammar applicable
-> reachability blocked
```

This order is preserved by each stage's source explanation, source owner, handoff/dependency references, and attempted movement. Displaying the final answer first does not change this lineage if the presentation explicitly labels the reachability result as the later derived conclusion and labels ingress and grammar as established prerequisites.

Current owner status: lineage order belongs to the constitutional stages and their handoff/provenance/derivation artifacts. A future presentation sequencer may carry and expose that order, but it must not invent or overwrite it.

## Operator-encounter-order findings

Question: in what order should the operator encounter already-established results so the explanation is coherent?

Repository evidence permits operator-facing presentation to be a read-only explanation over already-established results. Presentation may lawfully reorder material for comprehension when it preserves source meaning and derivation provenance. The supported operator encounter order may lead with:

```text
answer
immediate reason
support
missing boundary
limitations and Unknowns
next lawful movement
```

This is lawful only as presentation flow, not as constitutional derivation. It is especially appropriate when the operator's immediate question is whether the bounded inquiry can currently advance. In that case, the clearest presentation can be:

```text
The inquiry cannot currently advance.

The required realization is unreachable.

Ingress authority and grammar applicability
are already established.

No execution is authorized.
```

The presentation must also retain the constitutional lineage order:

```text
ingress permitted
-> grammar applicable
-> reachability blocked
```

Both orders remain explicit by rendering separate fields or sections such as `constitutional_lineage_order` and `operator_encounter_order`, or by otherwise making clear that the answer-first presentation is a display sequence over already-produced stage results.

Current owner status: operator encounter order is a presentation-sequencing responsibility over selected projections. It is not owned by membership selection, not owned by constitutional lineage preservation, and not owned by mere composition.

## Composition findings

Question: how are already-selected and already-sequenced projections preserved as one bounded presentation?

Composition merely preserves already-selected and already-sequenced projections as one bounded view. It should carry:

- bounded inquiry identity;
- selected projection references;
- constitutional lineage order supplied by provenance/handoffs;
- operator encounter order supplied by presentation sequencing;
- each projection's source owner and source explanation identity;
- each projection's stage-owned material without reinterpretation;
- Unknowns and conflicts without resolution;
- read-only, event-ledger, and mutation boundaries.

Composition must not select relevance, invent precedence, compare source states, resolve conflicts, deduplicate by meaning, rank blockers, normalize severity, re-derive conclusions, or authorize/observe/emit/execute. It can concatenate, nest, or otherwise preserve the bounded presentation after selection and sequencing have already occurred.

Current owner status: no implemented bounded multi-explanation composition owner exists. Existing answer-composition and operational-story evidence supports composition as a separate bounded responsibility, but the current shared explanation projection explicitly refuses composition.

## Proving-case results

### Same order

A same-order case is a straightforward derivation where the clearest operator encounter order follows constitutional lineage:

```text
ingress blocked
-> no bounded constitutional question formulation may advance
```

The operator can encounter ingress source state, first missing boundary, reconsideration transition, prohibited movement, Unknowns/conflicts, and read-only guarantees in the same order the ingress explanation was produced. No display reordering is required.

### Reordered explanation

For the required case:

```text
ingress permitted
-> grammar applicable
-> reachability blocked
```

presentation may lawfully lead with:

```text
The inquiry cannot currently advance.
The required realization is unreachable.
Ingress authority and grammar applicability are already established.
No execution is authorized.
```

The reachability result is encounter-first because it answers the operator's advance/no-advance question. It is not constitutionally first. The presentation must preserve lineage labels or references showing that ingress permission and grammar applicability preceded the reachability result as established prerequisites.

### Multiple supporting stages

Several projections may support one result. Ingress permission, grammar applicability, candidate-realization testimony, and reachability projection can all belong to one bounded explanation. The immediate blocker is not the only relevant explanation. Supporting stages must not be discarded merely because the later reachability projection contains the immediate blocker.

### Unknown and conflict

Unknowns and conflicts are placed for comprehension where the operator needs them to understand limits and lawful next movement. They may appear after answer and immediate reason, or adjacent to the stage that owns them. Placement must not hide, resolve, normalize, or downgrade them. The shared rendering projection preserves Unknowns and conflicts verbatim; reasoning-path and selection-path audits preserve typed Unknowns when evidence is absent.

### Duplicate or alternative projections

Multiple projections from the same stage may belong if they are distinct source explanations, alternative lawful stage results, or duplicate renderings that must be preserved for auditability. Deduplication is a membership-selection or composition policy question only if repository evidence defines identity-equivalence. Current shared rendering does not own deduplication. In absence of evidence, preserve distinct source identities and label duplicates rather than collapse meanings.

### Missing stage

An absent expected stage must not be invented. Depending on implemented evidence, it may be omitted, represented as an Unknown, or treated as a membership gap. The reasoning-path audit precedent supports explicit Unknowns when no derivation-path evidence is available. However, absence alone must not become a fabricated stage result or an unsupported negative conclusion.

## Lawful ordering evidence

Supported operator encounter ordering sources:

- operator question shape, such as asking whether the inquiry can advance;
- answer before support when the answer is already established by selected projections;
- immediate boundary before established prerequisites when comprehension requires the current stopping point first;
- support after immediate reason to show why the result is lawful;
- limitations, Unknowns, and conflicts near the relevant stage or before next lawful movement;
- next lawful movement after boundary and limitations;
- explicit operator-requested presentation preference, when it does not alter source meaning;
- repository-defined surface order for a specific implemented view, if present and tested.

These sources justify encounter order only as presentation. They do not establish constitutional priority.

## Rejected ordering evidence

Unsupported ordering sources:

- creation timestamp;
- artifact ID;
- lexical order;
- registry order;
- severity normalization;
- implementation call order;
- first result returned;
- highest blocker rank;
- most severe state;
- shortest explanation;
- most recent report;
- display prominence in another view;
- arbitrary global conversational script.

No reviewed evidence supports a universal conversation planner, priority engine, blocker ranking system, severity normalizer, or global composition manager.

## Lineage-versus-display preservation

Required preservation:

```text
constitutional_lineage_order != operator_encounter_order
```

A bounded view may therefore expose both:

```text
constitutional_lineage_order:
1. ingress authority/scope binding: permitted
2. representation grammar applicability: applicable
3. capability reachability: blocked

operator_encounter_order:
1. answer: cannot currently advance
2. immediate reason: required realization unreachable / blocked
3. support: ingress permitted and grammar applicable
4. limitations: Unknowns/conflicts and non-authorization boundary
5. next lawful movement: supply or change the missing bounded evidence/authority/dependency, if stage-owned explanation says so
```

The second order is a presentation sequence over already-established results. It must carry source references so the operator does not confuse encounter order with derivation order.

## Unknown and conflict treatment

Unknowns and conflicts remain source-owned. Presentation may group them for comprehension, but may not resolve them. If Unknowns are stage-specific, they should remain attached to that stage while also being visible in a bounded summary. If conflicts are present, the view should preserve the conflict references and explain that composition does not choose a winner.

## Duplicate and missing-stage treatment

Duplicate or alternative projections:

- preserve source explanation identity;
- preserve source artifact owner;
- preserve stage-owned material;
- label duplicate source identity if exact duplicate detection is available;
- otherwise do not collapse.

Missing stage:

- do not invent a stage result;
- omit if the bounded inquiry does not require it;
- represent as Unknown if an expected dependency is absent and implementation supports Unknown preservation;
- treat as membership failure only when the bounded view's contract requires that stage and the source evidence is absent.

## Topology classification

Classification: **A. Selection, lineage preservation, presentation sequencing, and composition are four independent responsibilities.**

Rationale:

1. Shared rendering explicitly consumes exactly one explanation and refuses comparison, aggregation, ordering, and composition.
2. Membership requires bounded-inquiry/source-reference selection evidence that shared rendering does not own.
3. Constitutional lineage is preserved by source stages, handoffs, provenance, and derivation paths, not by presentation ordering.
4. Operator encounter order is a presentation sequencing responsibility that may lawfully differ from lineage for comprehension.
5. Composition merely preserves the selected and sequenced results as one bounded view and must not select, sequence by constitutional derivation, compare states, or re-derive conclusions.

Topology B is insufficient because sequencing and composition have different failure modes: sequencing chooses encounter order, while composition merely preserves the already sequenced view. Topology C is too narrow because selection is not fully established upstream in current implementation. Topology D is unsupported because existing constitutional view composition does not own the complete topology. Topology E is weaker than the evidence warrants because the shared projection's explicit single-explanation boundary and the existing derivation/selection path separations strongly establish independent responsibilities.

## Strongest supporting evidence

The strongest support is the shared rendering projection's explicit single-explanation boundary: it consumes exactly one already-produced explanation and does not compare, aggregate, order, or compose explanations. This makes membership selection, presentation sequencing, and composition necessarily outside the current projection.

The second strongest support is the repository's repeated separation between read-only projection, selected source evidence, derivation paths, candidate sets, Unknown preservation, and non-mutation boundaries. Reasoning-path and selection-path audits already separate selected evidence, conclusions, consumers, lineage, Unknowns, and display rendering.

The third strongest support is reachability topology evidence: demand, candidate realizations, reachability projection, and later selection are distinct; reachability can preserve multiple supporting, blocked, unsupported, unknown, and conflicting candidates without selecting among them.

## Strongest counterevidence

The strongest counterevidence is that some existing answer-composition and operational-story surfaces already combine multiple inputs into one operator-facing view. That could suggest sequencing and composition share an owner. However, those surfaces are bounded to their own implemented responsibilities and do not establish a multi-explanation topology for shared explanation rendering projections.

The second counterevidence is that human renderers already impose line order. But line order inside one projection is rendering order for one explanation, not membership selection, constitutional lineage across several explanations, or bounded multi-projection composition.

The third counterevidence is that selection-path audit includes candidate ordering by pressure score and category name. That ordering is implementation-specific selection evidence for pressure surfaces, not a lawful universal explanation encounter order and not applicable to constitutional lineage.

## Exact current compressions

Current shared rendering compressions:

- one source explanation is represented as one `SharedExplanationRenderingProjection`;
- source state and source reason are common labels over stage-owned meanings;
- stage-specific fields are packed into `stage_owned_material`;
- Unknowns and conflicts are preserved as tuples;
- human rendering line order is presentation only;
- JSON rendering converts tuples to lists;
- read-only/event-ledger/mutation flags are carried from the source explanation;
- no membership, multi-explanation ordering, deduplication, or composition fields exist.

Current ingress explanation compressions:

- established authority/scope evidence is one semicolon-style string;
- first missing boundary is one string;
- reconsideration transition is one string;
- authority resolvability is one stage-local boolean;
- provenance and known loss are not exposed at the ingress explanation-artifact level.

Current grammar-applicability explanation compressions:

- established applicability evidence is a tuple of support strings;
- handoff boundary is one `next_handoff_boundary` string;
- reconsideration evidence is a tuple;
- authority treatment is a stage-local explanatory string;
- known loss and provenance are preserved as tuples.

Current reachability compressions:

- reachability state summarizes candidate evidence as `reachable`, `blocked`, `unsupported`, `unknown`, or `conflict`;
- supporting, blocked, unsupported, unknown, and conflicting candidate references are preserved separately;
- dependency, authority, representation, method, grammar, behavior, Unknown, and conflict details are compressed into reference lists and summary dimensions;
- reachability does not select a realization.

## Whether one implementation slice is warranted

No implementation slice is warranted yet for selection, sequencing, or composition.

A future slice may become warranted only after one narrower bounded question identifies the source of bounded-inquiry membership evidence and the minimal data shape needed to carry both constitutional lineage order and operator encounter order without changing source meanings. Implementing composition now would risk inventing selection policy, blocker precedence, or a global conversation planner.

## Exact next bounded question

Given a set of already-produced `SharedExplanationRenderingProjection` records and one explicit bounded inquiry reference, what minimum read-only membership evidence is required to decide which projections belong to that inquiry while preserving source explanation identity, source owner, stage-owned material, Unknowns, conflicts, and handoff/provenance references without sequencing, composing, deduplicating by meaning, ranking blockers, or re-deriving conclusions?

## Preserved Unknowns

- No implemented multi-explanation membership selector exists.
- No implemented operator encounter sequencer exists for several shared explanation projections.
- No implemented bounded composition owner exists for several shared explanation projections.
- The exact future data shape for bounded inquiry identity across all stage explanations is not yet implemented.
- Whether duplicate renderings should be collapsed, preserved, or labeled remains unimplemented.
- Whether absent expected stages should be omitted, represented as Unknown, or treated as membership failure depends on a future bounded view contract.
- Whether a recurring answer/immediate-reason/support/limitations/next-movement order is universal is not established.
- Future explanation owners may introduce provenance, known loss, or conflict structures not currently present.

## Confidence

Confidence: high that current shared rendering does not own membership, sequencing, or composition; high that constitutional lineage order must be preserved separately from display order; medium-high that topology A is the supported classification; medium for any future implementation shape because the multi-explanation bounded view is not implemented.

## Final answer

For one bounded inquiry:

- membership is owned by a bounded-inquiry membership-selection responsibility that uses inquiry identity, source references, relevance evidence, required explanation roles, and missing/duplicate handling;
- constitutional order is preserved by source stages, handoff/provenance records, and derivation-path lineage, then carried forward without deriving it from display order;
- conversational order is owned by a presentation-sequencing responsibility that may order already-established results for operator comprehension while preserving derivation provenance;
- the view is composed by a bounded composition responsibility that only preserves the already-selected and already-sequenced projections as one read-only presentation.

Explanation selection, sequencing,
and composition topology audit complete.

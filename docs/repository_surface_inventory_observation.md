---
doc_type: observation
status: exploratory
domain: repository surface inventory
related:
  - authority_owner_observation.md
  - view_authority_and_surface_responsibility_reconciliation.md
  - source_navigation_surface_reconciliation.md
  - inquiry_note_orientation_surface_reachability_observation.md
  - state_summary_authority_reconciliation.md
---

# Repository Surface Inventory Observation

## Status

Exploratory observation only.

This document investigates recurring repository language such as:

```text
surface accepts
surface refuses
surface preserves
surface projects
surface reconciles
surface navigates
surface validates
```

It does not modify implementation, projection behavior, relationship catalogs,
Inquiry Orientation, State Summary, runtime concepts, ontology, or policy. It
does not conclude that `surface` is a repository concept or that a formal
surface taxonomy should be introduced. Repository authority remains with the
implementation, tests, catalogs, and more specific reconciliations in their own
scopes.

## Question

Central questions:

```text
What repository surfaces exist?
What consequences do they control?
What do they accept?
What do they refuse?
How do surfaces differ?
```

The working pattern under investigation is:

```text
description
    ->
evidence or pressure
    ->
repository surface
    ->
acceptance or refusal
    ->
bounded consequences
```

This pattern is treated as a candidate reading, not as a settled repository
model.

## Repository evidence reviewed

Evidence reviewed for this observation included:

- `seed_runtime/events.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/evidence.py`
- `seed_runtime/facts.py`
- `seed_runtime/relationship_catalog.py`
- `relationship_catalog/core.json`
- `seed_runtime/inference_catalog.py`
- `inference_catalog/core.json`
- `seed_runtime/source_navigation.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/state.py`
- `seed_runtime/graph_validation.py`
- `seed_runtime/context_views.py`
- `scripts/seed_local.py`
- `13-knowledge-and-evidence.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/authority_owner_observation.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/inquiry_note_orientation_surface_reachability_observation.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/contradiction_handling_audit.md`
- `docs/context_composition_vocabulary.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/capability_verification_promotion_reconciliation.md`

Search terms included `surface`, `accepts`, `refuses`, `preserves`, `projects`,
`reconciles`, `validates`, `EventLedger`, `ProjectionStore`, `Evidence`, `Fact`,
`FactSupport`, `RelationshipCatalog`, `InferenceCatalog`, `source navigation`,
`Inquiry Orientation`, `State Summary`, `GraphValidationIssue`, `current belief`,
`active edge`, `current work position`, `handoff`, and `continuation`.

## Candidate surface inventory

The repository evidence supports some candidate surfaces more strongly than
others. The table below uses `surface` descriptively: a bounded place where
something enters, something is preserved, projected, selected, or rendered, and
some consequences are allowed or refused.

| Candidate | Evidence strength | What enters | What exits | Preserved / promoted | Refused or bounded consequence |
| --- | --- | --- | --- | --- | --- |
| `EventLedger` | Strong implementation evidence | Events and pre-built event batches | Append-order event history | Runtime event history, IDs, workspace order | Duplicate event IDs and invalid execution-authorization events are refused; semantic truth is not decided here. |
| `ProjectionStore` | Strong implementation evidence | Projected snapshots and dependent summary/index snapshots | Cached State, summary, and derived-index snapshots | Reusable derived read models keyed by projection versions and last event IDs | Stale/mismatched snapshots are not accepted as current; it does not own event history or semantic truth. |
| Evidence | Strong documentation and model evidence | Observed source payloads | Evidence records usable by fact extraction and support | Original payload, source, kind, time, confidence | Unsupported promotion directly to current truth is refused by the evidence-to-fact path. |
| Fact | Strong model evidence | Interpreted claims with provenance fields | Projected facts used by state/support | Subject, predicate, value, dimensions, evidence links, source type, confidence, expiry/inference metadata | Unknown provenance source types and invalid confidence are refused; a fact alone is not necessarily current belief. |
| FactSupport / current belief | Strong model and documentation evidence | Projected facts grouped by subject/predicate/value | Aggregate durable support or current measurement sample; best/current belief when unambiguous | Support counts, source types, confidence, recency, support kind | Conflicting values remain separate; measurement samples do not become durable conflicts; ambiguity may refuse a single best belief. |
| RelationshipCatalog | Strong implementation/catalog evidence | Relationship definitions and fact predicates | Canonical relationship definitions and predicate-to-relationship mappings | Relationship names, kinds, endpoint types, source predicates | Duplicate names and arbitrary relationship meaning are refused; prose similarity does not authorize relationship semantics. |
| InferenceCatalog | Strong implementation/catalog evidence | Deterministic inference rules | Matching rules and inferred-fact candidates | Rule IDs, trigger predicate/value, output predicate/value, confidence, reason | Duplicate rule IDs and invalid confidence are refused; rules are local deterministic projections, not open reasoning authority. |
| Source navigation | Moderate-to-strong reconciliation evidence | Preserved source facts, support, symbols, files, modules, operator question shapes | Orientation to source artifacts and support chains | Navigation over imports/definitions/source relationships | It refuses to create new source facts, strengthen facts, execute grep-like acquisition, or assert reachability/ownership by itself. |
| Inquiry Orientation | Strong implementation/probe evidence | Preserved operator prose plus projected read models | Bounded related-material view, uncertainty text, authority boundary | Raw inquiry note in isolated probe store; deterministic lexical overlap | It refuses fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, and runtime-instruction promotion. |
| State Summary | Moderate-to-strong documentation and implementation evidence | Projected State and summary-cache inputs | Operator-facing inventory/knowledge/integrity summary | Counts, current shape, bounded filesystem/storage-topology interpretations | It refuses to be Impact, ownership authority, topology truth, or full evidence detail; presentation classification is bounded. |
| Graph validation | Strong implementation/audit evidence | Projected relationships, entity types, catalog expectations | `GraphValidationIssue` records | Warnings/errors with expected/actual endpoint information | It refuses to repair, remove, rewrite, or block projected edges merely because an issue is reported. |
| Contradiction/conflict views | Strong audit evidence | Projected facts, predicate/cardinality semantics, optional evidence graph | `FactConflict`, standalone `Contradiction`, confidence-view flags | Visible disagreement, competing values, support links | They refuse truth arbitration, fact mutation, confidence mutation in core facts/supports, and unified automatic resolution. |
| Context Views / context composition | Moderate-to-strong documentation/code evidence | Projected State, Evidence Graph, Contradictions, Confidence, requirements/capabilities/current input | Decision-ready read-only context packets | Selected context with evidence counts, contradiction flags, issues, metadata | It refuses acquisition, execution, provider calls, mutation, replay, new persistence, and truth selection. |
| Handoff plans / handoff metadata | Moderate evidence in adjacent docs/code | Accepted action-plan/provider metadata | Non-executable provider handoff recommendation/plan | Boundary to external execution/provider systems | It refuses to execute, approve, schedule, retry, or imply external work has run without provider evidence. |
| Current work position / active edge / continuation | Weak-to-moderate as surface; stronger as pressure/orientation language | Inquiry, handoff, continuation, selected active context | Orientation for safe continuation when documented | Work-position/continuation relevance in observations and reconciliations | Evidence is not yet strong enough to treat these as concrete surfaces; they may be inputs, outputs, or interpretive pressures. |

## Surface comparison

The reviewed candidates differ more by consequence than by vocabulary.

### Preservation-oriented surfaces

`EventLedger`, Evidence, inquiry-note storage, and some source-observation paths
primarily preserve material. Their consequence is retention and later
inspectability. They are comparatively weak truth surfaces: preservation alone
does not establish current belief, ownership, relationship meaning, intent, or
execution authorization.

### Projection-oriented surfaces

`ProjectionStore`, State projection, FactSupport, relationship projection,
inference projection, graph validation, confidence, contradiction, and Context
Views depend on already-preserved material. Their consequence is derived read
models. Several of them explicitly remain read-only and report-oriented.

### Vocabulary/catalog surfaces

`RelationshipCatalog`, `PredicateCatalog`, and `InferenceCatalog` look like
bounded vocabulary/rule surfaces. They accept only cataloged entries with stable
identifiers, endpoint/type/cardinality/rule metadata, and valid confidence or
structure. Their consequences are downstream projection and validation behavior,
not direct observation or execution.

### Operator-facing surfaces

State Summary, source navigation, Inquiry Orientation, explanations, current
facts, fact support, graph issues, integrity summaries, and CLI renderings are
operator-facing read surfaces. Their consequence is visibility, orientation,
selection, or explanation. They vary in how much detail they should preserve:
`view_authority_and_surface_responsibility_reconciliation.md` distinguishes
Evidence Surfaces, Interpretation Surfaces, Integrity Surfaces, and Navigation
Surfaces as a useful but non-binding way to avoid applying summarization pressure
to evidence views.

### Boundary surfaces

Handoff metadata and provider recommendations appear to be boundary surfaces:
they can describe or recommend external-provider work but must not become
internal execution, approval, retry, scheduling, or proof that external work ran.

## Acceptance and refusal boundaries

The strongest acceptance/refusal patterns found were:

1. **Observed payloads are accepted as Evidence, not immediate truth.**
   Evidence preserves source payloads; facts are projected interpretations; fact
   support and current belief are further derived.
2. **Facts are accepted as claims with provenance, not as final current belief.**
   Current belief depends on support, predicate semantics, confidence, source
   type, recency, and conflict/measurement rules.
3. **Cataloged vocabulary is accepted for relationship/inference consequences.**
   Relationship and inference catalogs bound downstream meanings; arbitrary prose
   or shared wording does not create catalog authority.
4. **Validation accepts issues as visible outputs, not as repair commands.**
   Graph validation reports warnings/errors while preserving projected edges and
   source facts.
5. **Inquiry notes accept operator prose only as preserved prose.**
   Inquiry Orientation can render related material and uncertainty, but refuses
   promotion to fact, goal, tool need, requirement, capability, decision,
   proposal, plan, authorization, command, or runtime instruction.
6. **State Summary accepts projected-state aggregation, not entity-level Impact
   authority.** It can summarize current knowledge-system shape while refusing
   ownership/topology truth from presentation groupings.
7. **Source navigation accepts preserved source relationships as prerequisites.**
   It refuses to become new source observation, grep acquisition, fact
   strengthening, behavior reachability proof, or source ownership proof.
8. **Handoff accepts external-provider boundary metadata, not execution.**
   Handoff surfaces can preserve a non-executable plan/recommendation while
   refusing to imply approval or completed external work.

These patterns support the candidate shape:

```text
surface
    -> accepts bounded input
    -> refuses over-promotion
    -> produces bounded consequences
```

but they do not prove that the repository has a single surface theory.

## Authority observations

Repository evidence supports localized authority more strongly than one
repository-wide authority owner.

Possible authority locations observed:

- **Inside surfaces:** `EventLedger` owns append-only event history;
  `ProjectionStore` owns reusable snapshots; catalogs own bounded vocabulary;
  Inquiry Orientation owns its explicit authority-boundary rendering.
- **Between surfaces:** the knowledge path places consequential transitions
  between Observation, Evidence, Fact, FactSupport, State Projection, Context
  Composition, and decisions. Authority-like behavior often appears in the
  transition rules rather than in one object.
- **Across multiple surfaces:** current belief depends on facts, support,
  predicate semantics, confidence, source type, recency, expiration, aliasing,
  and conflict behavior. No single surface alone owns all of that consequence.
- **Nowhere in particular:** some language, especially `active edge`, `current
  work position`, and `continuation`, may be pressure or orientation vocabulary
  rather than surface authority.

The phrase `bounded authority surfaces` remains plausible as descriptive
shorthand, but this observation does not conclude that authority should be
attached to surfaces as ontology or implementation.

## Inquiry-related surfaces

Inquiry-related evidence is a useful comparison case because it sharply limits
promotion.

### Inquiry notes

Inquiry notes appear to be inputs to a surface more than authority surfaces by
themselves. They are preserved operator prose in an isolated JSONL probe store.
They enter Inquiry Orientation but do not become facts, goals, tool needs,
requirements, capabilities, decisions, proposals, plans, authorizations,
commands, or runtime instructions.

### Inquiry Orientation

Inquiry Orientation behaves more like an operator-facing navigation/orientation
surface. It accepts a preserved note and already-projected read models; it exits
as related material, support text, uncertainty, and an authority boundary. Its
strongest refusal is semantic over-promotion from lexical overlap.

### Current work position and active edge

Current work position and active edge have stronger evidence as continuation and
selection pressures than as implementation surfaces. They may describe why some
material matters now, what should be preserved for continuation, or where
handoff should orient future work. Evidence reviewed here is insufficient to
claim that either is a concrete surface with stable inputs/outputs.

### Continuation and handoff

Continuation and handoff materials behave partly like preservation and boundary
surfaces: they preserve selected orientation for future work and draw a boundary
around external execution. They are not enough to imply runtime action,
approval, or completed provider work.

## Alternative explanations

This investigation considered several alternatives.

### Surface language is misleading

Supported as a caution. Some candidates are models, catalogs, stores, read
views, CLI renderings, or documents rather than surfaces. Calling them surfaces
may blur implementation responsibility.

### The repository contains mechanisms, not surfaces

Plausible. `EventLedger`, `ProjectionStore`, catalogs, projectors, validators,
and renderers are concrete mechanisms. Surface language is useful only when it
highlights their bounded inputs/consequences without pretending to introduce a
new architectural object.

### The observed pattern is accidental

Partially plausible. Repeated refusal language may come from a documentation
style that carefully prevents over-promotion. However, the same bounded pattern
appears across implementation validation, catalog loading, evidence/fact
projection, read-only context views, Inquiry Orientation, source navigation, and
handoff boundaries, so it is probably not entirely accidental.

### Listed candidates are implementation details rather than surfaces

Often true. `FactSupport`, `ProjectionStore`, and catalogs are implementation
or model details. They can still behave like consequence-bearing boundaries, but
that does not make `surface` their canonical name.

### Authority is emergent and surface inventory adds little explanatory value

Plausible. Current belief and operator-facing authority often emerge from
multiple mechanisms. A surface inventory can help prevent accidental promotion,
but it may add little if treated as a taxonomy or ownership model.

## Uncertainties

Open uncertainties:

1. Whether `surface` should remain only descriptive shorthand.
2. Whether the evidence/interpretation/integrity/navigation distinction is
   broadly useful or only locally useful for view responsibility.
3. Whether current work position, active edge, continuation, and handoff should
   be considered surfaces, inputs to surfaces, outputs of surfaces, or pressures
   across surfaces.
4. Whether authority should be described as residing inside surfaces, between
   surfaces, across surfaces, or emergent from projection paths.
5. Whether source navigation and Inquiry Orientation are both navigation
   surfaces or only superficially similar operator-facing views.
6. Whether State Summary is a single surface or a composition of inventory,
   knowledge, integrity, and observation-accounting slices.
7. Whether graph validation is a surface or simply a validator whose outputs
   are surfaced elsewhere.
8. Whether catalog refusal should be treated as authority, validation, or plain
   data-shape enforcement.

## Non-conclusions

This observation does not conclude that:

- `Surface` is a repository concept.
- A formal surface taxonomy should be added.
- Authority should be attached to surfaces.
- Surface should become ontology.
- Runtime architecture should change.
- Relationship catalogs should change.
- Projection behavior should change.
- Inquiry Orientation or State Summary should change.
- Current work position, active edge, or continuation are first-class surfaces.
- Handoff surfaces should execute or authorize external work.

## Candidate inventory summary

The strongest candidate surfaces are:

```text
EventLedger
ProjectionStore
Evidence
Fact
FactSupport / current belief
RelationshipCatalog
InferenceCatalog
Graph validation
Inquiry Orientation
State Summary
Source navigation
Contradiction/conflict views
Context Views / context composition
Handoff boundary metadata
```

The weakest or most uncertain candidates are:

```text
current work position
active edge
continuation
handoff as continuation orientation rather than provider-boundary metadata
```

The strongest recurring pattern is not a taxonomy. It is a bounded consequence
pattern:

```text
preserve without promoting too far
project without resolving too much
validate without repairing silently
navigate without creating truth
summarize without becoming ownership authority
handoff without executing
orient inquiry without interpreting intent
```

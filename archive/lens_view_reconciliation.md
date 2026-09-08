---
status: reconciliation
scope: lens/view findings reconciliation
created: 2026-06-17
---

# Lens / View Reconciliation

## Status

This is documentation only. It does not implement lenses, implement views,
redesign State Summary, create HomeOps, create Seed Ops, or promote a new
runtime abstraction. It reconciles recent lens/view findings against repository
authority.

The repository supports a common model, but only as an architectural vocabulary
for current evidence. It does not yet support a formal lens framework, lens
registry, view composition API, HomeOps product surface, or Seed Ops product
surface.

## Purpose

This document reconciles `docs/lens_view_architecture_audit.md` and
`docs/lens_implementation_frontier_observation.md` around the responsibilities
of:

- State
- Read Projections
- Lens
- View
- State Summary
- HomeOps
- Seed Ops

It also evaluates the candidate chain:

```text
Event Ledger
    ->
State Projection
    ->
Projected State
    ->
Read Projections
    ->
Lens
    ->
View
```

## Repository evidence reviewed

Primary reconciliation inputs:

- `docs/lens_view_architecture_audit.md`
- `docs/lens_implementation_frontier_observation.md`

Implementation evidence:

- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/context_views.py`
- `seed_runtime/projection_store.py`

Supporting architectural evidence:

- `docs/state_summary_scope_review.md`
- `docs/lens_catalog_observation.md`
- `docs/lens_orientation_and_dashboard_observation.md`
- `docs/operator_surface_family_observation.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`

Search evidence:

- Repository search finds `HomeOps` only in exploratory lens/dashboard and State
  Summary boundary documents.
- Repository search finds `Seed Ops` only in the lens/view architecture audit,
  where it is explicitly not implemented and not canonically defined.

## Reconciled model

Repository evidence supports this model with two qualifications:

```text
Event Ledger
    ->
State Projection
    ->
Projected State
    ->
Read Projections
    ->
Lens-like bounded interpretation/selection
    ->
View/operator surface
```

The model is supported because `StateProjector` reads append-only events and
produces projected `State`; `State Views`, `Context Views`, State Summary
aggregation, source navigation, integrity summary, and storage projection all
operate as deterministic read-only surfaces over already-projected State or
repository knowledge.

The qualifications are important:

1. `Read Projection`, `Lens`, and `View` are not always separate implementation
   layers today. Existing code often combines read projection, lens-like
   semantics, and view payload construction in one helper.
2. `Lens` is not a canonical runtime primitive yet. It is currently a useful
   architectural description for bounded question-answering, attention shaping,
   compression, classification, or interpretation over projected State.

Therefore, the candidate model is directionally correct as a conceptual chain,
but too linear if read as an implemented pipeline. Current repository evidence
shows overlapping layers rather than a formal sequence of modules.

## State responsibilities

State responsibilities are strongly supported by implementation authority.
`StateProjector` is documented as rebuilding current inspectable state from
ledger events. `State` contains the projected read model: entities, facts,
observed and inferred facts, relationships, aliases, entity type assertions,
graph issues, fact support, conflicts, evidence, observations, goals, tool needs,
approvals, pending actions, plans, handoffs, and tool specs.

State is responsible for:

- holding current projected knowledge derived from event history;
- preserving evidence-backed facts, observations, relationships, aliases,
  entity type assertions, conflicts, graph issues, goals, capabilities, plans,
  and tools;
- exposing deterministic query helpers over projected content;
- carrying projection identity through `last_event_id` and
  `projection_version`;
- being rebuildable from ledger events and safe to cache as a projection.

State is not responsible for:

- rendering operator dashboards;
- deciding operational priority;
- performing live probes or health checks;
- executing tools, provider calls, shell commands, networks, or LLM calls;
- turning projected evidence into unsupported real-world truth.

Answer to reconciliation question 1: **State contains the projected knowledge
and integrity structures produced from event history; it is the current
inspectable world/read model, not a UI, dashboard, runtime probe, or action
authority.**

## Read Projection responsibilities

Repository evidence uses projection in two senses.

First, State Projection replays ledger events into `State` and rebuilds derived
indexes. This includes alias resolution, relationship projection, entity type
projection, inferred facts, fact support, conflicts, stale-fact structures, and
graph validation.

Second, read/view projections transform already-projected State into deterministic
read-only structures for consumers. `state_views.py` explicitly defines State
Views as deterministic projections of an already-built State object that do not
read ledgers, append events, invoke providers, evaluate policy, or execute
runtime behavior. `context_views.py` applies the same boundary to decision-ready
Context Views.

Read Projections are responsible for:

- selecting and shaping data from projected State;
- grouping, sorting, counting, summarizing, or exposing fields for a bounded
  consumer;
- preserving read-only determinism;
- retaining projection identity and provenance where needed;
- avoiding event appends, State mutation, provider calls, tool execution,
  runtime probes, policy decisions, and separate hidden stores.

Answer to reconciliation question 2: **Read Projections derive deterministic
read-only structures from already-projected State. They may structure or
summarize knowledge, but they do not create new authority, mutate State, or
perform runtime behavior.**

## Lens responsibilities

Lens authority is weaker than State or implemented Views. The repository treats
lens language as exploratory but convergent.

The reconciled responsibility is:

```text
A lens answers a bounded question over projected State or repository knowledge.
```

Lens-like responsibilities include:

- deciding what projected material matters to a bounded question;
- selecting, grouping, ranking, suppressing, caveating, or classifying projected
  content;
- compressing details while preserving a path back to evidence/provenance;
- exposing authority and non-authority boundaries;
- supporting reuse by multiple operator surfaces where caveats survive.

Lens non-responsibilities include:

- not owning State;
- not appending events;
- not executing probes or remediation;
- not deciding goals, policy, recommendations, or operator intent;
- not becoming real-world truth merely because it presents projected facts.

Answer to reconciliation question 3: **Lens is best understood as a bounded
question-answering or attention-shaping interpretation over projected State. It
is not yet a formal implemented primitive.**

## View responsibilities

The repository has stronger authority for views than for lenses. Existing view
modules produce deterministic read-only structures, and architectural documents
also use view/surface language for operator-facing presentations.

Views are responsible for:

- presenting or exposing one or more read projections or lens-shaped results to a
  consumer;
- preserving the authority boundaries of their inputs;
- choosing rendering shape, grouping, compatibility fields, and operator-facing
  labels;
- staying read-only unless separately authorized by another architecture.

A view may be very small, such as a `FactView`, or broader, such as an operator
State Summary. A view can embody lens-like decisions when the code both derives
and presents bounded semantics.

Answer to reconciliation question 4: **A View presents read-only projected or
lens-shaped material to an actor or downstream component; it may contain one or
more lenses, but presentation does not add truth, action, or probe authority.**

## State Summary reconciliation

State Summary is best understood as a **Combination**.

Evidence supports two State Summary layers:

1. The compact `StateSummary` in `seed_runtime/state_views.py` is closest to a
   State View: it counts facts, observations, requirements, capabilities,
   issues, and projection identity.
2. The richer operator `state_summary(state)` in
   `seed_runtime/state_summary_views.py` is an operator summary that combines
   State/projection counts with top-entity prominence, endpoint suppression,
   entity-kind classification, availability by scope, observation-source counts,
   integrity-adjacent counts, and storage projection helpers nearby in the same
   module.

`docs/state_summary_scope_review.md` already states that State Summary is a
deterministic read-only summary of projected State/read model, while warning it
should not be treated as a HomeOps dashboard, node dashboard, health checker,
operational attention queue, recommendation engine, storage-topology authority,
or only operator interface.

Answer to reconciliation question 5: **State Summary is a Combination: compact
State View plus richer operator-facing summary plus several embedded lens-like
selections. It is not best classified as only a State View, only a HomeOps View,
or only a Lens.**

## HomeOps classification

HomeOps appears closer to a **View** than a Lens if the term means a dashboard or
operator surface. It would likely compose multiple lenses: availability,
integrity, inventory, storage, entity navigation, provenance, relationship, and
possibly capability-readiness lenses.

However, some older exploratory language calls this a `HomeOps Lens`. The
reconciliation is that `HomeOps` names an operator context/attention surface more
than a single bounded question. Because it would gather many bounded signals, it
is more view-like or dashboard-like than lens-like.

Answer to reconciliation question 6 for HomeOps: **HomeOps appears closer to a
future View composed from lenses. Repository evidence does not support creating
it now or treating State Summary as HomeOps.**

## Seed Ops classification

Seed Ops has weaker evidence than HomeOps. Repository search shows it only in the
lens/view architecture audit, which says Seed Ops is not implemented and not
canonically defined.

If the term emerges, the safest classification is a future operator surface or
view family over Seed-runtime knowledge, not a single current lens and not State
itself. A Seed Ops surface might eventually compose lenses around projection
health, source navigation, capability readiness, execution status, repository
knowledge, or self-model integrity, but that is a hypothesis requiring separate
authority.

Answer to reconciliation question 6 for Seed Ops: **Seed Ops appears closer to a
future View or view family than a Lens, but the evidence is sparse and unresolved.**

## Lens reuse across views

Repository evidence supports lens reuse as plausible but not formally specified.

The strongest evidence is conceptual and architectural:

- one deterministic projected State can support many read-only surfaces;
- State Summary, Projection Integrity, storage projection, source navigation,
  Context Views, and Inquiry Orientation all select from shared projected
  knowledge;
- `docs/lens_catalog_observation.md` explicitly describes overlapping lenses,
  such as availability participating in both operational availability and
  HomeOps-style attention;
- `docs/lens_view_architecture_audit.md` notes that an availability lens could
  support State Summary counts or a future HomeOps-oriented panel, but also says
  the repository has not established a formal `Lens -> many Views` contract.

Answer to reconciliation question 7: **Yes, a single lens can plausibly
participate in multiple views, but only as an emerging architectural principle.
The repository supports the idea; it does not yet define the contract.**

## Emerging lens/view contract

A future lens/view contract, if authorized, should preserve these boundaries:

- Input: already-projected State or documented repository knowledge.
- Determinism: same projected inputs produce the same lens output.
- Read-only behavior: no event append, State mutation, tool execution, provider
  call, policy decision, network/shell call, LLM call, or runtime probe.
- Bounded question: each lens states the question or attention pattern it
  answers.
- Authority statement: each lens states what it may and may not claim.
- Provenance path: compressed output preserves a route back to evidence or
  source material.
- View composition: views may present one or more lenses, but must preserve
  upstream caveats and not upgrade projection evidence into live truth or action
  priority.

This contract is an emergent reconciliation, not an implemented API.

## Remaining open questions

Answer to reconciliation question 8: **The main unresolved architectural
question is where the repository should draw the formal boundary between read
projection, lens, and view if a lens architecture is ever implemented.**

Specific unresolved questions:

- Should lenses become named runtime objects, plain helper functions, schema
  payloads, registry entries, or documentation-only authority boundaries?
- Which current State Summary sections should merely be labeled as embedded
  lenses versus eventually extracted into separate surfaces?
- What exact contract allows one lens to participate in multiple views without
  losing caveats or provenance?
- How should view composition represent source authority, uncertainty, stale
  facts, contradictions, and projection integrity?
- What would count as sufficient repository authority to define HomeOps or Seed
  Ops as product surfaces?

## Conclusion

The expected findings are mostly supported, with precision adjustments:

- **State contains knowledge:** supported, if `knowledge` means projected,
  evidence-backed, inspectable read-model content rather than environmental
  truth.
- **Read Projections derive structures:** supported strongly.
- **Lens answers bounded questions:** supported as emerging architecture, not as
  an implemented primitive.
- **View presents one or more lenses:** supported directionally, but current
  implementation often combines projection, lens-like semantics, and view shape.
- **State Summary currently combines multiple concerns:** supported strongly.
- **HomeOps is likely a future view:** supported more strongly than treating it
  as a single lens, though it remains conceptual.
- **Seed Ops is likely a future view:** plausible but weakly evidenced; treat as
  unresolved future view-family vocabulary.

The reconciled model is therefore:

```text
Event Ledger
    -> State Projection
    -> Projected State
    -> deterministic Read Projections
    -> bounded Lens-like interpretations
    -> Views / operator surfaces composed from one or more lenses
```

This model should guide vocabulary and future analysis, but it should not be
used as authorization to implement lenses, implement views, redesign State
Summary, create HomeOps, or create Seed Ops.

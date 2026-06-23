---
title: Answer Composition Visibility Investigation
status: investigation
authority: architecture-focused investigation only; not implementation proposal, natural-language interface proposal, routing engine proposal, planner proposal, schema, or universal answer composer
created: 2026-06-23
scope: repository-level review of whether Seed already has bounded answer compositions and whether their visibility is missing
---

# Answer Composition Visibility Investigation

## Purpose

This investigation asks:

```text
What is an answer composition?
Does Seed already have them?
Does Seed know that it has them?
```

The investigation is intentionally not a proposal for a chat interface, LLM
router, planner, natural-language query layer, global reasoning engine, universal
answer composer, or implementation branch. Repository authority wins.

The architectural pressure under review is narrower:

```text
Seed already combines multiple repository surfaces to answer bounded question
families, but those combinations are not consistently visible as answer
compositions.
```

## Method and authority boundary

The review treated implementation files and tests as authority for existing
behavior, reconciliations as authority inside their stated boundaries,
investigations/frontiers/observations as evidence of pressure, and repository
maps as routing evidence. This document records an architectural investigation
only. It does not add a diagnostic, audit, probe, CLI flag, view, recordable
output, or runtime behavior.

## Files inspected

Implementation and CLI-adjacent surfaces inspected:

- `seed_runtime/operational_story.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/integrity_summary.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/ops_brief.py`
- `seed_runtime/observation_sources.py`
- `scripts/seed_local.py`

Tests and support files inspected:

- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`
- `tests/test_inquiry_orientation.py`
- `tests/test_knowledge_reachability.py`
- `tests/test_operational_surface_inventory.py`
- `tests/test_seed_local_script.py`

Documentation inspected as architectural evidence:

- `README.md`
- `AGENTS.md`
- `docs/repository_self_explanation_investigation.md`
- `docs/reasoning_chain_visibility_investigation.md`
- `docs/implicit_observation_workflow_investigation.md`
- `docs/operator_navigation_reconciliation.md`
- `docs/read_model_inventory_and_authority_reconciliation.md`
- `docs/lens_orientation_and_dashboard_observation.md`
- `docs/lens_view_architecture_audit.md`
- `docs/lens_catalog_observation.md`
- `docs/lens_implementation_frontier_observation.md`
- `docs/repository_orientation_audit.md`
- `docs/state_summary_scope_review.md`
- `docs/state_summary_decomposition_audit.md`
- `docs/view_branch_continuity_reconciliation.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/projection_self_knowledge_observation.md`
- `docs/audit/projection_authority_provenance_audit.md`
- `docs/architectural_findings_preservation.md`
- `docs/architectural_findings_vocabulary.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/source_navigation_query_surface_design_audit.md`
- `docs/source_navigation_without_grep_audit.md`
- `docs/inquiry_as_bridge_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuability_observation.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_failure_observation.md`

Search terms included:

```text
answer
composition
operational story
storyboard
ops brief
dashboard
State Summary
projection shape
diagnostic inventory
diagnostic shape audit
inquiry orientation
source navigation
current work position
active edge
continuation
self-knowledge
self-explanation
known answer
question answered
view
surface
projection
diagnostic
```

## Central finding

Seed appears to already possess bounded answer compositions. The strongest
examples are not universal answer generators. They are read-only, scoped
compositions over existing repository knowledge that answer known question
families:

- `OperationalStory` composes pressure, capability needs, privilege constraints,
  correlation gaps, impact, observed outcomes, investigation path, unknowns, and
  an explicit read-only boundary.
- `ProjectionIntegritySummary` composes existing projected integrity signals into
  a bounded integrity answer while preserving caveats that the counts are not
  truth, correctness, repair, or provider availability decisions.
- State Summary composes projected State into a bounded operator overview, while
  storage helper comments and boundaries prevent the overview from becoming
  topology or ownership authority.
- Inquiry Orientation composes a preserved inquiry note with projected facts and
  source navigation matches to answer a bounded related-material question while
  preserving uncertainty and non-authority.
- Source Navigation composes preserved `defines` and `imports` facts into a
  source-location answer without inspecting files or inferring behavior.
- Projection Shape composes stage-level consumes/produces/influences boundaries
  into an implementation-backed answer to projection-topology questions.
- Diagnostic Inventory plus Diagnostic Shape Audit compose declarations and
  implementation specs into an answer about whether operational visibility
  surfaces are registered and shape-consistent.
- Reasoning Path and Selection Path audits preserve selected multi-hop chains for
  bounded diagnostic and selection questions.

The missing thing is therefore more likely:

```text
answer composition visibility
```

than:

```text
answer composition itself
```

That conclusion is architectural, not an implementation mandate. Existing
repository evidence repeatedly warns against new engines, universal formatters,
parallel truth systems, and runtime/tool-executor centralization when distributed
composition already exists.

## Working definition: answer composition

An **answer composition** is a bounded repository construction that:

1. names or implies a question family;
2. consumes more than raw isolated output, usually by selecting, joining,
   aggregating, ordering, contextualizing, or narrating repository material;
3. preserves the source authority of the consumed material;
4. states or carries boundaries about what it does not claim;
5. preserves uncertainty, caveats, unknowns, alternatives, or non-selected
   remainder when the source material cannot support stronger claims; and
6. has output responsibilities that are narrower than universal answer
   generation.

This definition intentionally allows single-surface answer compositions when the
single surface is itself a composed read model. It also distinguishes answer
composition from mere rendering. A formatter may present a result; the answer
composition is the semantic selection/join/aggregation/narrative that makes the
result answer a question family.

## Candidate answer-composition classes

Repository evidence supports the following distinctions, though not all are
formal repository vocabulary today.

| Candidate class | What qualifies | Existing evidence | Boundary |
| --- | --- | --- | --- |
| Single-surface answer | One exposed surface answers a bounded question because its internal read model already composes source material. | Source Navigation, Projection Shape, Projection Integrity Summary, State Summary. | Not a universal answer; not automatically self-describing as an answer composition. |
| Multi-surface answer | A surface explicitly joins multiple other surfaces or audits. | Operational Story, Reasoning Path Audit, Selection Path Audit, Inquiry Orientation. | Requires preserving each source's authority and uncertainty. |
| Narrative answer | A composition organizes findings into an operator-understandable story or chain. | Operational Story; reasoning-chain visibility investigation. | Narrative does not imply planning, recommendation, or mutation. |
| Operational answer | A composition answers current operational pressure, integrity, visibility, or surface-contract questions. | Operational Story, Ops Brief, Diagnostic Inventory, Diagnostic Shape Audit, Projection Integrity Summary. | Operational visibility is not cluster mutation and must preserve diagnostic boundaries. |
| Investigative answer | A composition answers how evidence, candidates, paths, or unknowns support a finding. | Reasoning Path Audit, Selection Path Audit, Inquiry Orientation, Source Navigation. | Does not turn lexical matches, candidate paths, or selected examples into truth. |
| Continuation answer | A composition preserves what matters for safe resumption or current work position. | Current Work Position, Active Edge, continuation and handoff documents, repository self-explanation investigation. | Much of this remains documented pressure, not an implemented answer-composition registry. |

## Existing composition examples

### 1. Operational Story

Question family:

```text
What is the current operational story, and which pressure, capabilities,
constraints, gaps, impact, outcomes, path, unknowns, and boundaries make it up?
```

Knowledge consumed:

- pressure audit;
- capability needs;
- privilege discovery;
- correlation audit;
- impact audit;
- investigation path audit;
- projected State.

Authority:

- read-only view;
- no fact recording;
- no event-ledger writes;
- no cluster mutation;
- no plans or implementation advice.

Uncertainty preserved:

- missing pressure;
- missing capability needs;
- unknown impact;
- bounded investigation path.

This is the strongest implemented example of answer composition because it
explicitly uses `build_operational_story()` to join several visibility surfaces
and returns an object with pressure, capabilities, constraints, correlation gaps,
impact, recent changes, observed outcomes, investigation path, unknowns, and a
boundary.

### 2. Projection Integrity Summary

Question family:

```text
What integrity signals are visible in projected State right now?
```

Knowledge consumed:

- evidence summary;
- fact conflicts;
- contradictions;
- graph issues;
- stale facts;
- refresh recommendations;
- capability inventory;
- projection version and last event id.

Authority:

- read-only projected-State integrity summary;
- not truth, correctness, repair, verification, provider availability, or action.

Uncertainty preserved:

- caveats explicitly state that unsupported/unverified/stale/contradicted/missing
  evidence does not mean false;
- refresh recommendations remain inventory signals only.

This is an answer composition because it joins existing integrity views into a
specific answer while carefully refusing stronger claims.

### 3. State Summary / storage shape fragments

Question family:

```text
What exists in projected State, and what bounded shape should the operator see
first?
```

Knowledge consumed:

- projected entities, facts, observations, integrity signals, availability,
  storage rows, and related State-derived summaries depending on section.

Authority:

- repository overview and read model;
- not HomeOps dashboard, runtime health checker, topology truth, storage identity,
  or ownership authority.

Uncertainty preserved:

- storage topology candidate/ambiguity boundaries;
- classification basis says mountpoint classification is presentation-only.

State Summary is not a universal answer, but it is a composed answer to a known
overview question. The dashboard investigations are especially important here:
repository evidence warns that forcing `one State -> one dashboard` is the wrong
shape, while `many lenses -> many views` better matches the observed need.

### 4. Inquiry Orientation

Question family:

```text
Given a preserved inquiry note, what already projected material may be related,
and how weak is that relation?
```

Knowledge consumed:

- isolated inquiry note JSONL records;
- projected State fact supports;
- Source Navigation rows.

Authority:

- inquiry note is preserved operator prose only;
- matches are deterministic lexical overlaps;
- no facts, goals, tool needs, requirements, decisions, proposals, plans,
  authorizations, commands, runtime instructions, ownership claims, intent claims,
  or next-safe-move claims.

Uncertainty preserved:

- matches may be incomplete or incidental;
- no matches do not prove unrelatedness.

Inquiry Orientation is composition without semantic overreach. It may be the best
example of answer composition preserving uncertainty as a first-class output
responsibility.

### 5. Source Navigation

Question family:

```text
Where do preserved repository source facts say this symbol, module, or path is
defined or imported?
```

Knowledge consumed:

- projected `FactSupport` rows for `defines` and `imports`.

Authority:

- read-only source navigation over preserved source facts;
- no file inspection;
- no source parsing;
- no behavior, reachability, or ownership inference.

Uncertainty preserved:

- absent rows mean no preserved source facts matched, not that the source does
  not exist or cannot be relevant.

This is a single-surface answer composition: the view is narrow, but it answers a
known repository navigation question.

### 6. Projection Shape

Question family:

```text
What does each projection stage consume, produce, influence, not influence, and
what authority boundary applies?
```

Knowledge consumed:

- implementation-backed projection-stage declarations.

Authority:

- stage-level projection topology;
- not instance-specific evidence, runtime planning, or universal causality.

Uncertainty preserved:

- confidence is implementation-backed at stage level;
- unsupported instance-specific chains must use other surfaces.

Projection Shape is not a view in the dashboard sense. It is a repository
self-knowledge composition about projection behavior.

### 7. Diagnostic Inventory and Diagnostic Shape Audit

Question family:

```text
Which operational diagnostic surfaces exist, what shape do they declare, and do
implementation specs agree with those declarations?
```

Knowledge consumed:

- diagnostic inventory registry declarations;
- static implementation specs;
- source markers for JSON, record, repo-file, projected-state, diagnostic-fact,
  event-ledger, and mutation behavior.

Authority:

- operational visibility contract;
- diagnostic facts remain diagnostic scoped;
- read-only surfaces must preserve `mutates_cluster=false` unless intentionally
  operational.

Uncertainty preserved:

- shape-audit statuses include consistent, warning, mismatch, and unknown.

This is an answer composition about repository operational self-visibility. It
already proves that Seed can know some surfaces and their boundaries without a
universal answer engine.

### 8. Reasoning Path and Selection Path audits

Question families:

```text
How did this bounded diagnostic conclusion become visible?
Why was this item selected from candidates?
```

Knowledge consumed:

- ownership discrepancies;
- capability needs;
- pressure audit;
- privilege discovery;
- operational story;
- selection candidates and factors.

Authority:

- read-only chain visibility;
- no event-ledger write;
- no cluster mutation;
- no planning or universal reasoning claim.

Uncertainty preserved:

- unsupported paths and unknowns are explicit;
- non-selected candidates are preserved in selection paths.

These surfaces are important because they show that Seed already contains scoped
chain-preserving answer constructions.

## View, surface, projection, diagnostic, answer composition

The repository does not support treating these terms as synonyms.

| Term | Architectural role | Relationship to answer composition |
| --- | --- | --- |
| Surface | Any exposed operator/developer-facing output or interaction point. | A surface may host an answer composition, but many surfaces are simple inventories or renderings. |
| View | A read model or presentation-oriented selection over repository material. | A view can be an answer composition if it answers a bounded question with source authority and uncertainty. |
| Projection | Derived State or read-model construction from ledger/facts/catalogs/rules. | Projection can supply inputs to a composition; projection shape can itself answer topology questions. |
| Diagnostic | A visibility/checking surface with operational contract boundaries. | Diagnostic compositions answer inspection/audit questions and must preserve diagnostic scope. |
| Answer composition | A bounded construction that maps question family to inputs, authority, uncertainty, and output responsibilities. | May be implemented as a view, diagnostic, projection-backed summary, narrative, or documentation-only composition. |

This distinction matters because `composition vs view` is the main tension. A
view can answer a question, but composition visibility asks whether Seed knows
what question family the view answers, what it consumes, and what boundaries it
must preserve.

## Required tensions

### Composition vs view

A view is an exposed read shape. A composition is the semantic responsibility
that makes a read shape answer a bounded question. Operational Story is both a
view and a composition. Source Navigation is a view with a very narrow answer
composition. State Summary is a composed overview, but dashboard documents warn
against treating it as the answer to every operator question.

### Composition vs explanation

Explanation often answers `why?` for a fact, decision, response, conflict, or
surface. Answer composition can use explanation, but it is broader: it also names
question family, inputs, authority boundaries, uncertainty handling, and output
responsibilities. Repository self-explanation is therefore adjacent: it asks how
Seed relates a user question to governing knowledge. Composition visibility asks
whether Seed knows its existing bounded answer constructions.

### Composition vs navigation

Navigation helps the operator find where to look next. Composition may remove a
manual join by presenting the already-known combination. Operator Navigation
Reconciliation says each surface answers a different question and should suggest
the next one. Composition visibility would not replace navigation; it would make
known cross-surface answers discoverable as known compositions.

### Composition vs orientation

Orientation concerns the relation between participant, current concern, inquiry,
active edge, continuation, and preserved knowledge. Answer composition may
support orientation by packaging a bounded answer, but orientation remains more
situational and participant-relative. Inquiry Orientation is a composition whose
answer is explicitly weak and uncertain; it does not become a general orientation
engine.

### Composition visibility vs composition execution

The repository can describe a composition without executing an automatic answer
composer. A composition description can name:

- question families;
- required inputs;
- authority boundaries;
- uncertainty handling;
- output responsibilities;
- known non-authority;
- existing surfaces that already perform the composition.

That is architectural visibility, not runtime execution.

### Repository self-explanation vs composition visibility

Repository self-explanation asks how Seed relates an operator question to
relevant knowledge, governing findings, evidence surfaces, authority boundaries,
uncertainty, and use relation. Answer composition visibility is a narrower
candidate branch inside that pressure: it concerns question families already
served by bounded compositions. It does not solve all self-explanation, but it
explains why self-explanation pressure persists even when concrete compositions
exist.

### Operator discovery vs repository self-knowledge

Operators can often infer that a composition exists by reading many files or
running several commands. The repository does not always expose the composition
as a named architectural object with question family, consumed knowledge,
authority, and uncertainty. This produces the recurring experience:

```text
the operator knows compositions exist
the repository does not appear to know them
```

Diagnostic Inventory is the counterexample: for diagnostics, the repository does
know the surface inventory and audits shape consistency. That supports the
plausibility of composition visibility as an architectural concern while also
warning that not every surface needs another registry.

## Strongest supporting evidence

1. **Operational Story is explicitly composed.** Its module docstring calls it a
   read-only operational story view composed from existing visibility surfaces,
   and its builder joins pressure, capability needs, privilege discovery,
   correlation, impact, and investigation path.
2. **Projection Integrity Summary is explicitly a composition.** It aggregates
   already-derived integrity signals while preserving caveats and non-authority.
3. **Projection Shape exposes consumes/produces/influences/boundaries.** Seed can
   already represent a bounded answer to architecture-topology questions without
   a universal engine.
4. **Inquiry Orientation composes note + State + Source Navigation while
   preserving weak lexical authority.** It proves composition can preserve
   uncertainty instead of overstating answers.
5. **Diagnostic Inventory / Shape Audit prove visibility over operational
   surfaces is an accepted architectural responsibility.** The repository already
   treats invisible operational surfaces as a problem.
6. **Reasoning Chain Visibility found scoped chain-preserving surfaces and
   fragmented chain visibility elsewhere.** This is highly analogous to answer
   compositions: local compositions exist, but discoverability and consistency
   are uneven.
7. **Architectural Findings Preservation says behavior, ownership, and
   composition often already existed; gaps were vocabulary, discoverability,
   status, and handoff clarity.** This directly supports `composition visibility`
   over `composition engine`.

## Strongest contradictory evidence

1. **No canonical `answer composition` vocabulary appears to exist.** The term is
   not an established repository concept in the way diagnostic inventory,
   projection shape, source navigation, or inquiry orientation are.
2. **Many examples are views, lenses, diagnostics, or summaries, not explicitly
   answer compositions.** Reclassifying them risks creating presentation
   vocabulary without implementation-backed repository knowledge.
3. **Dashboard and lens documents explicitly warn against premature dashboard or
   view-framework implementation.** Composition visibility could accidentally
   repeat that mistake if treated as a framework or engine.
4. **Current composition examples have heterogeneous ownership.** Operational
   Story, Projection Integrity Summary, Source Navigation, Inquiry Orientation,
   Diagnostic Inventory, and Projection Shape each own different concerns.
   Centralizing them could violate repository authority.
5. **Some continuation/current-work/active-edge material remains documentation
   pressure rather than implemented surface behavior.** It can inform the
   investigation but should not be promoted into runtime knowledge without
   implementation evidence such as knowledge-reachability audits.

## Is Seed missing answer composition or answer composition visibility?

The stronger answer is:

```text
Seed is missing answer composition visibility more than answer composition.
```

Seed already contains bounded compositions. What is inconsistent is whether the
repository can identify, for each composition:

```text
what classes of questions it answers
what knowledge it consumes
what authority boundaries apply
what uncertainty it preserves
what output responsibilities it owns
what it explicitly does not answer
```

This does not mean every view should gain a new metadata layer. It means the
architectural pressure is real enough to be a branch candidate: characterize
existing known answer compositions before inventing any execution mechanism.

## Is answer composition visibility meaningful or merely compression?

Answer composition visibility is more than compression over navigation,
orientation, explanation, and continuation, but it is not independent of them.

It is meaningful because it names a missing repository self-knowledge relation:

```text
known bounded question family
    -> required repository inputs
    -> source authority boundaries
    -> uncertainty and remainder
    -> output responsibility
    -> existing surface(s) that perform or approximate the composition
```

Navigation alone answers where to go. Explanation answers why something is
supportable. Orientation answers why material matters here/now for a participant
or inquiry. Continuation answers what must be preserved for safe resumption.
Composition visibility answers which bounded answer constructions Seed already
has and what they are allowed to claim.

That said, the branch should remain cautious. Repository history repeatedly
rejects universal engines and central layers when distributed behavior already
exists. The first architectural question should be characterization and boundary,
not implementation.

## Candidate boundaries for a future branch

A future `answer composition visibility` branch, if accepted, should be bounded
as follows:

### In scope

- inventorying existing bounded answer compositions;
- naming question families they answer;
- recording consumed repository knowledge and source surfaces;
- preserving authority boundaries and non-authority;
- preserving uncertainty, unknowns, alternatives, and caveats;
- distinguishing implemented compositions from documentation-only pressure;
- mapping compositions to repository self-explanation and operator discovery
  concerns.

### Out of scope

- universal answer engine;
- natural-language interface;
- LLM routing;
- automatic planner;
- global reasoning layer;
- dashboard framework;
- runtime or ToolExecutor centralization;
- projection mutation;
- parallel truth system;
- automatic claim promotion from diagnostic findings;
- implementation before an accepted boundary.

## Relationship to repository self-explanation

Repository self-explanation remains the broader pressure. Answer composition
visibility explains one recurring failure mode inside it:

```text
The answer construction exists, but the repository does not expose that it is a
known construction with known inputs, authority, and uncertainty.
```

This investigation therefore refines the self-explanation pressure rather than
replacing it. It suggests that some self-explanation questions may be answered by
making existing compositions visible, while other self-explanation questions may
still require navigation, documentation authority, source navigation, inquiry
orientation, reachability, or continuation work.

## Relationship to operator experience

The operator experience reported in the prompt is strongly supported:

```text
knowledge exists
navigation exists
explanation exists
but operators manually reconstruct answers across multiple repository surfaces
```

Existing compositions reduce that burden in some places. Operational Story and
Reasoning Path Audit are clear examples. But because the repository does not
uniformly present those constructions as known answer compositions, operators
must still infer:

- whether a surface is a raw view, a diagnostic, or a composed answer;
- which question family it answers;
- which source surfaces it consumes;
- which boundaries prevent overclaiming;
- where uncertainty is preserved;
- which adjacent questions remain unanswered.

## Open questions

1. What minimum evidence is required before a surface can be called an answer
   composition rather than a view, diagnostic, or summary?
2. Should answer composition visibility be documentation-only first, or should it
   eventually be tested the way diagnostic inventory visibility is tested?
3. Which existing compositions are implemented, which are only documented, and
   which are merely operator-inferred?
4. Is `OperationalStory` the right exemplar, or is it too operational-specific
   to generalize from?
5. How should composition visibility relate to existing read-model authority
   inventories without duplicating them?
6. Should composition visibility include negative entries such as `State Summary
   does not answer HomeOps dashboard questions`?
7. Can composition visibility remain decentralized, or would any central
   inventory inevitably invite a universal answer-engine interpretation?
8. What role, if any, should knowledge-reachability audits play before promoting
   presentation vocabulary such as current work position, active edge, or
   continuation into composition metadata?

## Determination

`answer composition visibility` is a meaningful architectural branch candidate.

The evidence supports the branch because Seed already has bounded answer
compositions, especially operational story, projection integrity summary,
inquiry orientation, source navigation, projection shape, diagnostic inventory
with shape audit, and reasoning/selection path audits. The evidence also shows
that Seed does not consistently identify these as answer compositions with
question families, consumed knowledge, authority boundaries, uncertainty, and
output responsibilities.

The branch should begin as architectural characterization only. The next move
should not be implementation, a registry, a CLI, a router, a planner, or an
engine. Repository authority wins.

## Recommended next architectural question

```text
Which existing Seed surfaces qualify as implemented known answer compositions,
and what minimum metadata is sufficient to describe their question family,
inputs, authority boundary, uncertainty handling, and non-authority without
creating a composition engine?
```

## Change record

Files changed:

- `docs/answer_composition_visibility_investigation.md`

LOC changed:

- Added one documentation-only investigation file.

Tests run:

- Documentation-only change; no tests required by the operational visibility
  contract because no diagnostic, audit, probe, view, operational CLI flag, or
  recordable output was added or modified.

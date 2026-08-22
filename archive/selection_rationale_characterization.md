# Selection Rationale Characterization

## Executive Summary

Seed already performs selection in several read-only places, but the reason for
selection is mostly implicit in code paths, ordering keys, projection fields, and
budget traces. The current system can usually answer **what was selected**: a
support group, a stale fact view, a capability inventory entry, or an
explanation belief.

The missing architectural concept is **Selection Rationale**: a vocabulary for
explaining why an already-known candidate was surfaced for a current surface,
view, answer, context packet, or representative current state instead of other
available candidates. Selection Rationale is not a new engine. It does not decide
truth, create knowledge, execute tools, call providers, verify capabilities,
mutate state, append events, rank with an LLM, or introduce a parallel truth
system.

The safest next step is documentation-only: create a **Selection Rationale
Vocabulary v1** that names rationale surfaces, reason categories, reason codes,
inclusion-vs-ordering distinctions, and candidate comparison concepts without
changing runtime behavior.

## Purpose

This document characterizes Seed's current selection behavior and the rationale
signals already available around it.

It answers:

- what Selection Rationale means in Seed terms;
- which current surfaces already perform selection;
- which selection rules and signals are already present;
- how Selection Rationale differs from Explanation, Context Composition,
  Integrity, and Truth Selection;
- which candidate-selection cases need rationale language;
- which gaps should be documented before any future implementation is considered.

## Scope

This is an audit and characterization document only.

It covers read-only selection over already-projected or already-known knowledge,
ordering helpers, decision context views, current-state fact selection,
fact-support views, stale fact views, capability inventory entries, and
explanation belief selection.

It does **not** implement selection rationale. It does **not** add adapters,
runtime behavior, schema classes, read models, engines, providers, routes,
execution behavior, projection mutation, or event appends.

## Files Inspected

Documentation inspected:

- `docs/context_composition_reconciliation.md`
- `docs/context_composition_vocabulary.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/projection_integrity_summary_characterization.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/knowledge_lifecycle_reconciliation.md`

Runtime files inspected:

- `seed_runtime/context_views.py`
- `seed_runtime/state.py`
- `seed_runtime/explanations.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/facts.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/confidence.py`
- `seed_runtime/contradictions.py`

Adjacent repository checks:

- documentation invariant tests under `tests/`
- test suite execution with `pytest`

## Current Selection Surfaces

### ContextComposer

`ContextComposer.compose(...)` builds model-visible `ContextPacket`s from the
current input event, projected state, registry-visible tools, open tool needs,
ordered goals, entities, facts, and evidence. It delegates ordering to

Current selected outputs include:

- current input;
- at most one active goal after budget selection;
- entities;
- recent facts;
- recent evidence;
- visible tools;
- open tool needs;
- a decision schema;
- context-budget trace metadata.

Rationale status: the surface exposes what was included and includes a budget
trace, but it does not attach per-item selected-because or excluded-because
records.


per-section limits, and optional global `max_items`. It assumes each section is
already ordered from most to least useful.


- effective priorities;
- section limits;
- optional global max item count;
- selected counts;
- dropped counts;
- section order.

Rationale status: this is the strongest existing context-packet rationale signal
because it records section-level selection accounting. It is not a full rationale
contract because it does not identify the per-item rule or compare included and
excluded candidates.

### context_selection ordering helpers


- facts: fresh/unexpired before expired, then newer observations, higher
  confidence, and ID tie-break;
- evidence: newer observations, higher confidence, and ID tie-break;
- goals: active before inactive, then ID tie-break;
- entities: higher confidence, then name and ID tie-break.

Rationale status: these helpers encode ordering rationale, but the rationale is
implicit in sort keys rather than exposed as stable reason records.


from projected `State`, the Evidence Graph, Contradiction Detection, and
Confidence Aggregation. It selects facts, issues, requirements, and
capabilities, and carries projection metadata.

Current selected outputs include:

- requirement views;
- capability views;
- summary counts;
- `projection_version`;
- `last_event_id`.

Rationale status: the view exposes confidence, contradicted status,
evidence-count, issue severity, and projection metadata. It does not preserve a
candidate comparison record or an explicit selected-because reason.


excluded by default unless `include_unsupported=True`. Selected facts are ordered
by support presence, descending confidence, subject, predicate, stable object
value, and fact ID.

Rationale status: this is a clear deterministic selection rule. Existing signals
include support count, unsupported status, confidence, contradicted status, and
evidence count. Missing signals include explicit inclusion/exclusion reason codes
and an ordering rationale trace.

### State.get_best_fact

`State.get_best_fact(...)` returns the representative fact for the best-supported
current belief. It first asks `get_fact_support(...)` for the unambiguous
strongest support, then selects the representative supporting fact by confidence,
observed-vs-inferred preference, observation time, and ID.

Rationale status: this surface has an implicit two-stage rationale: strongest
support group first, representative fact second. That distinction is not named in
a stable rationale contract.

### State.get_current_facts

`State.get_current_facts(...)` uses predicate cardinality. For single-cardinality
predicates, it returns the `get_best_fact(...)` result if one exists. For
multi-cardinality predicates, it returns one representative fact for every
support group and sorts the result by value.

Rationale status: the key rationale signal is predicate cardinality. Current
behavior distinguishes single-current-state selection from multi-current-state
selection, but no rationale vocabulary names that distinction.

### State.get_fact_support and State.get_fact_supports

`State.get_fact_supports(...)` returns aggregate support groups for a subject and
predicate, with alias resolution and optional dimension filtering. `State.get_fact_support(...)`
returns the unambiguous strongest aggregate support if exactly one candidate has
the top support tie key.

Rationale status: support groups already expose confidence, supporting fact IDs,
source types, observation timestamps, latest observation timestamps, expiry,
predicate semantics, and support kind. The selection of an unambiguous best
support is implicit and currently returns `None` when tied.

### stale fact views

`State.get_stale_facts(...)` returns expired facts sorted by expiry timestamp and
ID. `State.get_stale_fact_refresh_recommendations(...)` maps stale fact
predicates to deterministic refresh-capability recommendations and includes a
human-readable reason.

Rationale status: stale fact surfacing is already separated from current facts.
The main rationale signals are expiry, stale status, predicate, recommended
capability, and recommendation reason.

### capability inventory

`build_capability_inventory(...)` produces deterministic read-only verification
beliefs for capabilities from registered tools, open `ToolNeed`s, and
`capability_verified` fact subjects. It derives `verified`, `provider_reported`,
`unverified`, `stale`, or `unknown` states from current and expired fact support.
It exposes supporting facts, supporting evidence, support summary, age, and a
reason string.

Rationale status: capability inventory already has explicit reason text and
support metadata. It remains capability-verification inventory, not a general
selection-rationale system.

### explanation selection

`ExplanationBuilder.why(...)` selects current and competing belief explanations
from `State.get_fact_supports(...)` and `State.get_fact_support(...)`. It reports
`current`, `ambiguous`, or `no_current_belief`, and includes conflict details when
present.

Rationale status: explanation selection explains why a claim exists and which
beliefs are current or competing. It can share data with Selection Rationale, but
it should not be collapsed into Selection Rationale.

## Current Selection Behavior

Current behavior can be grouped into several deterministic families.

### Section-level context selection

Model-visible context selection first orders items inside sections, then applies
section priority, section limits, and optional global limits. Current input and
active goals have high default priorities; open tool needs, recent facts, recent
evidence, entities, and historical events have lower default priorities.

### Intra-section ordering

The ordering helpers prefer:

- fresh facts over expired facts;
- newer facts/evidence over older facts/evidence;
- higher-confidence facts/evidence/entities over lower-confidence candidates;
- active goals over inactive goals;
- deterministic IDs, names, subjects, predicates, and stable values as
  tie-breakers.

### Decision-context fact selection

Decision-context facts are derived from confidence aggregation. Unsupported facts
are omitted by default. Remaining facts are sorted so supported facts come before
unsupported facts when unsupported facts are included, then by descending
confidence and deterministic tie-breakers.

### Issue selection

Decision-context issues are surfaced when contradictions or graph-validation
issues exist. Contradiction issues carry contradiction IDs, subject/predicate
summaries, values, and severity. Graph issues carry graph-validation IDs,
summaries, and severity. Issues are sorted deterministically.

### Current-state selection

Current-state fact selection uses support aggregation and predicate semantics:

- durable facts aggregate independent support for a subject/predicate/value;
- measurement facts select the latest current sample instead of strengthening
  repeated values;
- single-cardinality predicates return one representative current fact when an
  unambiguous strongest support exists;
- multi-cardinality predicates return one representative per support group.

### Stale-state selection

Expired facts are excluded from ordinary current support unless callers include
expired facts. They can still be surfaced separately by stale fact views and
refresh recommendations.

### Capability selection

Capability inventory selection starts from the union of known capability names in
projected tools, open tool needs, and verification fact subjects. It then selects
a current support, stale support, or missing-verification state and records a
capability verification status.

### Explanation selection

Explanation selection follows current fact support semantics. Multi-cardinality
queries explain all current support groups. Single-cardinality queries explain
the unambiguous best support when present, otherwise they expose ambiguity or no
current belief.

## Current Rationale Signals

Seed already carries many fields that can serve as selection-rationale signals:

- section priority;
- section limits;
- optional global max item count;
- selected counts;
- dropped counts;
- section order;
- freshness / unexpired status;
- expiry timestamp;
- stale status;
- recency / observed-at timestamp;
- latest observed-at timestamp;
- confidence;
- aggregate support confidence;
- support count;
- supporting fact IDs;
- supporting evidence IDs;
- evidence count;
- source types;
- active goal status;
- open `ToolNeed` status;
- contradicted status;
- unsupported status;
- graph issue severity;
- contradiction severity;
- contradiction reason;
- predicate cardinality;
- predicate semantics (`durable` vs `measurement`);
- support kind (`aggregate` vs `current_sample`);
- measurement latest-current behavior;
- capability status;
- capability reason text;
- capability age;
- projection version;
- last event ID;
- deterministic tie-breakers such as IDs, names, stable values, subjects, and
  predicates.

These signals are sufficient to characterize many selection outcomes after the
fact, but they are not yet organized into a canonical selection-rationale
contract.

## Selection Rationale Definition

**Selection Rationale is a read-only account of why an already-known candidate
was selected for a current surface, view, answer, context packet, or
representative current state over other available candidates.**

In Seed terms, Selection Rationale:

- explains selection;
- is projection-backed when the selected candidate comes from projected state;
- is context-aware because selection is surface-specific;
- is evidence-aware when evidence participates in selection;
- is deterministic when the underlying selection rule is deterministic;
- may describe inclusion, exclusion, ordering, or representative choice;
- may reference confidence, support, contradiction, staleness, freshness,
  cardinality, capability status, budget, and provenance signals;
- does not decide truth;
- does not create knowledge;
- does not execute tools;
- does not call providers;
- does not verify capabilities;
- does not mutate state;
- does not mutate projections;
- does not append events.

## Selection Rationale vs Explanation

Explanation answers:

> Why does this claim exist?

Selection Rationale answers:

> Why was this candidate surfaced now?

They may share supporting evidence, support groups, conflict signals, temporal
metadata, confidence, provenance, and source mappings. They remain distinct
concerns.

Explanation is claim-centered. It describes current and competing beliefs,
supporting facts, evidence IDs, source types, observation timestamps, inference
links, confidence caps, and conflicts for a queried subject and predicate.

Selection Rationale is surface-centered. It describes why one candidate was
included, excluded, ordered ahead of another candidate, or chosen as a
representative for a current surface. A selected context fact may need Selection
Rationale even if the claim's Explanation is unchanged. Conversely, a claim may
have a full Explanation even when it was not selected for a specific context
packet.

Do not collapse Selection Rationale into Explanation.

## Selection Rationale vs Context Composition

Context Composition answers:

> What matters right now?

Selection Rationale answers:

> Why did this item count as mattering right now?

Context Composition is the read-only selection and formatting boundary that
assembles decision-ready or model-visible knowledge from already-known state.
Selection Rationale is the account of the selection result at that boundary.

important rationale signals, but they are not a full rationale contract. They
describe section priorities, limits, selected/dropped counts, section order, and
intra-section ordering keys. They do not provide stable per-item selected-because
or excluded-because metadata.

## Selection Rationale vs Integrity

Integrity characterizes projected knowledge. It identifies conditions such as:

- unsupported;
- conflicted;
- contradicted;
- stale;
- expired;
- graph-invalid;
- unverified.

Selection Rationale may use integrity signals as reasons. For example, a context
issue may be surfaced because a contradiction exists, an unsupported fact may be
excluded by default, or a stale fact may be surfaced separately because it is
expired.

Selection Rationale does not repair, resolve, suppress, arbitrate, or mutate
integrity conditions. It explains why integrity signals affected selection.

## Selection Rationale vs Truth Selection

Truth Selection asks which belief should represent the current state for a
subject, predicate, dimensions, and value space. Seed already has current-state
selection behavior in fact support aggregation, `get_fact_support(...)`,
`get_best_fact(...)`, measurement latest-sample semantics, predicate cardinality,
and ambiguity handling.

Selection Rationale is not a parallel truth system. It explains an already-run
selection decision. It can say a fact was selected because it belonged to the
unambiguous strongest support group, because it was the latest measurement
sample, or because the predicate is multi-cardinality. It should not introduce
new arbitration rules or override current-state semantics.

## Candidate Selection Cases

### Current fact selected vs competing fact

Selection rationale should identify:

- the selected support group;
- competing support groups;
- whether the selected support group was unambiguous;
- aggregate confidence;
- support count;
- source types;
- representative fact tie-breakers such as confidence, observed-vs-inferred
  status, observation time, and ID.

### Measurement selected vs older measurement

Selection rationale should identify:

- predicate semantics as `measurement`;
- support kind as `current_sample`;
- latest observation timestamp;
- selected sample ID;
- older samples that were not current;
- the fact that repeated measurement values do not strengthen support in the way
  durable facts do.

### Context fact included vs excluded

Selection rationale should identify:

- whether the fact was supported or unsupported;
- whether unsupported facts were included for that view;
- confidence;
- contradicted status;
- evidence count;
- section limit and budget state when selection occurred;
- ordering position and tie-breakers.

### Evidence included vs excluded

Selection rationale should identify:

- evidence recency;
- evidence confidence;
- evidence ID tie-breaker;
- section limit and dropped-count effects;
- whether selected facts reference that evidence inside the same packet.

### Active goal selected vs inactive goal

Selection rationale should identify:

- goal status;
- the active-goal-first ordering rule;
- the active-goal section limit;
- ID tie-breakers among goals with the same status.

### Open ToolNeed included

Selection rationale should identify:

- open `ToolNeed` status;
- capability requested by the need;
- deterministic name ordering;
- open-tool-needs section priority and limit;
- whether the need also contributes to capability inventory.

### Capability surfaced vs not surfaced

Selection rationale should identify:

- whether the capability came from registered tool metadata, an open tool need,
  or a `capability_verified` fact subject;
- selected capability verification state;
- current, stale, or missing verification support;
- support confidence;
- supporting facts and evidence;
- capability reason text;
- age and expiry when available.

### Issue surfaced because contradiction or graph issue exists

Selection rationale should identify:

- issue source (`contradiction` or `graph_issue`);
- issue ID;
- severity;
- contradiction reason or graph-validation reason;
- affected fact IDs and values when available;
- supporting event IDs and evidence when available.

### Stale fact surfaced separately from current facts

Selection rationale should identify:

- expired/stale status;
- expiry timestamp;
- exclusion from current support by default;
- separate stale-fact view inclusion;
- recommended refresh capability;
- recommendation reason.

## Existing Gaps

Seed is missing:

- a canonical vocabulary for Selection Rationale;
- stable reason-code names for inclusion, exclusion, ordering, and
  representative-choice rationales;
- per-item selected-because metadata;
- explicit excluded-because metadata;
- candidate comparison records;
- source mapping from selected output back to the selection rule that produced
  it;
- a distinction between rationale for inclusion and rationale for ordering;
- a distinction between rationale for current-state selection and context
  selection;
- a distinction between section-level budget rationale and item-level rationale;
- a way to explain a `None` selection caused by ambiguity without treating it as
  failure;
- stable vocabulary for candidate sets, selected candidates, excluded candidates,
  dropped candidates, competing candidates, tie-breakers, and representative
  candidates;
- vocabulary for whether a rationale was deterministic, budget-driven,
  integrity-driven, temporal, support-driven, capability-driven, or
  surface-driven.

## Complexity Traps

Avoid these traps:

1. **Building a SelectionEngine.** Current behavior already performs selection in
   concrete surfaces. Characterization does not require a new engine.
2. **Creating a parallel truth system.** Selection Rationale must explain current
   truth selection; it must not re-decide truth.
3. **Collapsing Explanation and Selection Rationale.** Claims can be explained
   independently from why they were selected for a surface.
4. **Collapsing Context Composition and Selection Rationale.** Context
   Composition selects and formats; Selection Rationale accounts for that
   selection.
5. **Treating budget traces as a complete rationale contract.** Budget traces are
   useful section-level signals, not full per-item rationales.
6. **Treating capability inventory as verification execution.** Capability
   inventory is read-only and support-backed; it does not verify a capability.
7. **Treating stale surfacing as refresh execution.** Stale fact recommendations
   are recommendations, not tool calls.
8. **Adding LLM ranking.** Existing selection is deterministic; rationale should
   not introduce opaque ranking.
9. **Mutating projections to store rationale.** Rationale should be read-only and
   derivable from projected state and selection traces.
10. **Over-generalizing provider, routing, planning, and orchestration.** These
    are outside Selection Rationale.

## Recommended Next Step

Create **Selection Rationale Vocabulary v1** as a documentation-only follow-up.

That vocabulary should define:

- `selection_surface`;
- `candidate_set`;
- `selected_candidate`;
- `excluded_candidate`;
- `dropped_candidate`;
- `competing_candidate`;
- `representative_candidate`;
- `inclusion_reason`;
- `exclusion_reason`;
- `ordering_reason`;
- `tie_breaker`;
- `selection_rule`;
- `rationale_signal`;
- `budget_rationale`;
- `support_rationale`;
- `temporal_rationale`;
- `integrity_rationale`;
- `capability_rationale`;
- `projection_rationale`.

The vocabulary should remain documentation-only unless a later invariant test
requires a small documentation-linked inventory. Do not recommend engines,
runtime integration, ToolExecutor integration, provider integration, or new
execution behavior.

## Non-Goals

Selection Rationale is not:

- truth arbitration;
- explanation generation;
- verification execution;
- provider selection;
- runtime routing;
- ToolExecutor behavior;
- policy authorization;
- planning;
- orchestration;
- LLM ranking;
- fact mutation;
- projection mutation;
- event append;
- a parallel truth system;
- a ContextEngine;
- a SelectionEngine;
- a ReasoningEngine;
- a Planner;
- a WorkflowEngine.

## Future Work

Future work should proceed in this order:

1. Draft `docs/selection_rationale_vocabulary.md` as documentation only.
2. Align the vocabulary with Context Composition, Explanation Contract,
   Projection Integrity, Knowledge Classification, and Knowledge Lifecycle
   terminology.
3. Decide whether documentation invariant tests need to assert the presence of
   Selection Rationale vocabulary terms.
4. Only after vocabulary stabilization, consider whether existing surfaces can
   expose rationale using already-available traces and projected metadata without
   changing selection behavior.
5. Keep any later implementation read-only, projection-backed, deterministic
   where the underlying rule is deterministic, and explicitly separate from
   Runtime, ToolExecutor, provider behavior, planning, orchestration, and truth
   mutation.

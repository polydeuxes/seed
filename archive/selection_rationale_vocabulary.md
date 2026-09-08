# Selection Rationale Vocabulary v1

## Executive Summary

Selection Rationale Vocabulary v1 defines the canonical language Seed uses when
it talks about why an already-known candidate was selected, ordered, included,
excluded, or treated as current for a particular surface.

The vocabulary preserves the conclusion of
`docs/selection_rationale_characterization.md`: selection behavior already exists
across context packets, context budgets, ordering helpers, decision context
views, current fact queries, fact support aggregation, measurement handling,
capability inventory classification, stale fact views, and explanation surfaces.
The missing architectural artifact is stable vocabulary, not a new selection
runtime.

Selection Rationale is documentation-only in v1. It does not introduce a
`SelectionEngine`, `ContextEngine`, `ReasoningEngine`, planner, workflow engine,
provider ranking system, LLM ranking path, schema class, read model, inventory,
adapter, runtime route, ToolExecutor behavior, event append, projection mutation,
fact mutation, or parallel truth system.

## Purpose

This document defines the terms Seed should use when discussing selection
rationale. It is intended to play the same role for selection rationale that
existing vocabulary documents play for explanation contracts, capability
verification, context composition, and knowledge classification.

The purpose is to:

- define Selection Rationale in Seed terms;
- name canonical candidate, surface, signal, basis, outcome, rationale, and
  status concepts;
- distinguish context, current-state, ordering, budget, capability, integrity,
  and temporal selection rationales;
- map the vocabulary to existing repository structures;
- preserve the boundary between Selection Rationale, Explanation, Context
  Composition, Integrity, Why-Not vocabulary, runtime behavior, ToolExecutor
  behavior, provider behavior, and truth mutation;
- give future documentation work a stable terminology foundation.

This document is not an implementation plan. It does not require current code to
emit rationale objects.

## What Is Selection Rationale

**Selection Rationale** is a read-only explanation of why an already-known
candidate was selected for a current surface over other available candidates.

In Seed terms, Selection Rationale explains an already-performed selection. It
can explain:

- why a candidate was selected;
- why a candidate was ordered ahead of another candidate;
- why a candidate was included in a surface;
- why a candidate was excluded when the exclusion is known from existing signals;
- why one current-state candidate represents the current state;
- why a stale, unsupported, contradicted, unverified, or ambiguous candidate was
  or was not surfaced.

Selection Rationale does not determine truth, create knowledge, acquire
knowledge, verify capabilities, execute tools, call providers, evaluate policy,
authorize execution, plan workflows, mutate `State`, mutate projections, append
events, select runtime routes, or rank with an LLM.

Selection Rationale is surface-centered. The same fact, support group,
capability entry, issue, or explanation fragment may have different rationales on
different surfaces because each surface has different selection rules, limits,
defaults, and purposes.

## Canonical Vocabulary

### Selection Rationale

A read-only account of why an already-known candidate had a specific selection
outcome for a specific selection surface.

Selection Rationale is explanatory vocabulary. It is not a selector, engine,
policy, verifier, planner, executor, provider router, or truth arbiter.

### Candidate

An already-known item that could be considered by a selection surface.

Examples include a projected fact, `FactSupport` group, evidence record, entity,
goal, open `ToolNeed`, context issue, graph issue, contradiction, capability
inventory entry, stale fact, refresh recommendation, explanation belief, or
context packet section item.

A candidate must already exist in projected state, a read-only view, registered
metadata, or an already-computed trace. Selection Rationale does not create
candidates.

### Selected Candidate

A candidate that appears in the selected output of a selection surface.

fact returned by `State.get_current_facts(...)`, or a
`CapabilityInventoryEntry` returned by `build_capability_inventory(...)`.

### Excluded Candidate

A candidate that was available to a selection surface but did not appear in the
selected output.

Exclusion may be explicit when an existing trace or status exposes it, such as a
not selected because another support group was unambiguous best support, because
a fact expired and expired facts were not included, or because a section limit
was reached.

An Excluded Candidate is not necessarily false, invalid, unavailable, or
unimportant globally. It was not selected for the current surface under the
current rules.

### Selection Surface

A concrete place where Seed selects, orders, limits, or formats already-known
candidates for a current use.

Existing selection surfaces include `ContextPacket`, `ContextComposer`,
`State.get_best_fact(...)`, `State.get_current_facts(...)`,
`State.get_stale_facts()`, `State.get_stale_fact_refresh_recommendations(...)`,
`build_capability_inventory(...)`, and `ExplanationBuilder.why(...)`.

### Selection Signal

An existing data point that can help explain a selection outcome.

Signals include priority, limit, section order, selected count, dropped count,
confidence, support count, evidence count, contradiction count, unsupported
status, contradicted status, graph issue severity, predicate cardinality,
predicate semantics, support kind, observed time, latest observed time,
expiration time, stale status, capability verification state, active goal status,
open tool need name, entity confidence, and deterministic ID tie-breaks.

### Selection Basis

The set of signals, rules, and surface defaults used to explain a selection
outcome.

A basis is descriptive. It reports which known signals participated in the
selection; it does not invent new signals or modify existing behavior.

### Selection Rule

A surface-owned rule that determines or contributes to selection, ordering,
inclusion, exclusion, or representative choice.

`context_selection.order_facts(...)` ordering keys,
`State.get_fact_support(...)` unambiguous best-support selection,
`State.get_best_fact(...)` representative fact tie-breaks,
measurement latest-current sample semantics, predicate cardinality handling, and
capability inventory support-state ranking.

### Selection Outcome

The result of applying a selection rule to a candidate for a surface.

Canonical outcome words are:

- **selected**: included in the surface output;
- **excluded**: not included in the surface output when the candidate was known;
- **ordered**: placed before, after, or tied with another candidate;
- **current**: selected as representative of current state;
- **competing**: available as an alternative current-state or explanation belief;
- **dropped**: omitted due to a budget or limit;
- **ambiguous**: no single selected current candidate exists because available
  candidates do not resolve to one unambiguous current value;
- **not applicable**: the surface does not consider that candidate kind.

### Inclusion Rationale

A rationale that explains why a selected candidate appeared in the selected
output.

Inclusion may be based on surface scope, section priority, being within a limit,
being supported, being current, being active, being recent, being a capability
candidate in the inventory universe, being a stale fact view item, or being an
issue that the surface reports.

### Exclusion Rationale

A rationale that explains why a known candidate did not appear in the selected
output.

Exclusion may be based on unsupported filtering, expiry filtering, section
limits, global limits, lower ordering position, not being the unambiguous best
support, predicate cardinality, dimension filtering, alias scope, candidate kind,
or surface defaults.

Exclusion Rationale is closely related to Why-Not vocabulary, but it remains
surface-centered: it explains non-selection for a specific surface.

### Ordering Rationale

A rationale that explains relative position among candidates.

Ordering Rationale names ordering keys such as freshness, recency, confidence,
active status, support count, evidence count, state rank, name, value, or ID
tie-break. It does not imply truth unless the existing surface uses ordering as
part of current-state selection.

### Current-State Rationale

A rationale that explains why a fact or support group represents the current
state for a subject, predicate, dimensions, and cardinality.

Current-State Rationale may refer to unambiguous strongest support, predicate
cardinality, measurement latest-current sample semantics, expiry filtering,
confidence, observed-vs-inferred representative selection, observation time, and
ID tie-break.

### Context Rationale

A rationale that explains why a candidate mattered for a current context surface.

Context Rationale may refer to current input, active goals, open tool needs,
recent facts, recent evidence, entities, context section priority, section limit,
global item budget, evidence presence, confidence, contradiction status,
unsupported filtering, or issue reporting.

### Tie-Break

A deterministic fallback used when higher-priority selection signals are equal or
insufficient to create stable ordering.

Examples include fact ID, evidence ID, goal ID, entity name, entity ID, stable
value serialization, or capability name. A tie-break explains deterministic
ordering; it should not be treated as semantic superiority.

### Priority

A relative weight that determines which section or candidate category is
considered before another category.

`DEFAULT_SECTION_PRIORITIES` and configurable `priorities`. Priority is a
selection signal, not a truth signal.

### Limit

A cap on how many candidates from a section, category, or surface may be
selected.

`DEFAULT_SECTION_LIMITS` and configurable `section_limits`, plus optional global
`max_items`. A limit can explain dropped or excluded candidates without implying
that dropped candidates are false.

### Budget

The combined priority, limit, and count accounting used to select bounded
context.

`max_items`, selected counts, dropped counts, and section order. Budget is a
section-level rationale signal; it is not a full per-item rationale contract.

### Status

A normalized word describing implementation or selection-state condition.

For selection outcomes, use outcome words such as selected, excluded, ordered,
current, competing, dropped, ambiguous, or not applicable. For implementation
status, use the Selection Status Vocabulary section below. For integrity or
capability status, preserve the existing domain status words such as
unsupported, contradicted, stale, unverified, provider_reported, verified, or
unknown.

### Reason

A short human-readable explanation of a selection outcome.

A reason may summarize a basis such as "selected because the fact is within the
recent_facts section limit," "excluded because unsupported facts are omitted by
default," or "current because this is the unambiguous strongest support." Reason
is vocabulary; v1 does not require a `reason` field in code.

### Signal

A synonym for Selection Signal when the context is clear.

Prefer **Selection Signal** in formal documentation to avoid confusing selection
signals with integrity, evidence, capability, or runtime signals.

### Evidence-Aware Selection

Selection whose rationale references evidence-derived signals such as support
count, evidence count, supporting event IDs, explicit fact confidence, Evidence
Graph support, unsupported status, source types, or provenance.

Evidence-aware selection does not create evidence and does not prove truth. It
uses already-known evidence metadata as selection context.

### Integrity-Aware Selection

Selection whose rationale references integrity signals such as contradiction,
conflict, unsupported status, stale or expired status, graph issue severity, or
confidence penalties from contradiction metadata.

Integrity-aware selection does not repair integrity and does not become an
integrity system.

### Temporal Selection

Selection whose rationale references time-based signals such as observed time,
latest observed time, recency, freshness, expiry, stale status, age, or
measurement latest-current sample semantics.

Temporal selection does not create as-of reasoning unless a surface explicitly
supports as-of semantics. Current repository behavior is latest-current and
expiry-aware, not a general temporal query engine.

### Capability Selection

Selection whose rationale references capability-related candidates or statuses,
such as registered tool capabilities, open `ToolNeed`s, `capability_verified`
fact support, capability inventory state, provider-reported status, unverified
status, stale verification support, unknown value mapping, or refresh capability
recommendations for stale facts.

Capability Selection is not capability verification execution, provider
availability, authorization, reachability, or tool execution.

## Selection Categories

### Context Selection Rationale

Context Selection Rationale explains why a candidate was included in or excluded
It is concerned with what was surfaced now for a model-visible packet,
decision-ready view, answer, capability-gap discussion, or explanation context.

It differs from current-state rationale because it is about surfacing and
formatting candidates, not selecting the true or representative current belief.

### Current-State Selection Rationale

Current-State Selection Rationale explains why Seed treated a fact or support
group as current for a subject, predicate, dimensions, and cardinality.

It is anchored in existing state behavior such as fact support aggregation,
`State.get_fact_support(...)`, `State.get_best_fact(...)`,
`State.get_current_facts(...)`, predicate cardinality, expiry filtering, and
measurement latest-current sample semantics.

It differs from context rationale because a current fact can exist without being
selected into a particular context packet.

### Ordering Rationale

Ordering Rationale explains relative order among candidates that are otherwise
eligible for a surface.

It is anchored in deterministic ordering helpers and sort keys. It differs from
inclusion rationale because an item can be eligible and ordered but still dropped
by a later limit.

### Budget Rationale

Budget Rationale explains selection outcomes caused by section priorities,
section limits, selected counts, dropped counts, section order, or optional
global `max_items`.

It differs from ordering rationale because budgeting applies caps after items are
already ordered inside sections. It differs from truth or integrity rationale
because budget constraints do not determine correctness.

### Capability Selection Rationale

Capability Selection Rationale explains why a capability-related candidate was
reported with a particular inventory or context status.

It is anchored in `build_capability_inventory(...)`, registered tool
capabilities, open `ToolNeed`s, `capability_verified` fact subjects,
`FactSupport`, stale verification facts, and deterministic status mapping. It
differs from verification execution because it reports projected support; it does
not test or prove capability availability.

### Integrity-Aware Selection Rationale

Integrity-Aware Selection Rationale explains how integrity metadata affected
selection or surfacing.

It may mention unsupported facts, contradictions, fact conflicts, graph issues,
staleness, expiry, confidence penalties, or issue severity. It differs from
Integrity itself because it only explains why those signals affected a selection
surface; it does not characterize, resolve, or mutate the underlying knowledge.

### Temporal Selection Rationale

Temporal Selection Rationale explains how time-related metadata affected
selection or ordering.

It may mention freshness, recency, observed time, latest observed time,
expiration time, stale status, age seconds, or measurement latest-current sample
selection. It differs from integrity-aware rationale when the time signal is
purely about recency or currentness rather than a stale/expired warning.

## Selection Status Vocabulary

Use these words to classify repository support for selection-rationale concepts:

### Implemented

The selection behavior or signal exists in code or documentation today and is
observable through an existing surface.


### Partial

Some relevant behavior or signal exists, but the concept is not fully normalized,
not exposed per item, or not consistently named across surfaces.

Example: Inclusion Rationale is partially present because selected outputs and
budget traces exist, but selected candidates do not carry stable per-item
selected-because records.

### Missing

The concept does not currently exist as a repository artifact.

Example: a canonical Selection Rationale object or schema class is missing, and
that absence is intentional for this vocabulary document.

### Implicit

The selection behavior exists in code paths, sort keys, defaults, or data
relationships, but is not surfaced as explicit rationale terminology.

Example: `context_selection.order_facts(...)` implicitly encodes freshness,
recency, confidence, and ID tie-break rationale.

### Unknown

The repository does not provide enough evidence to assign implemented, partial,
missing, or implicit status for a specific concept.

Use Unknown sparingly. Do not use it to mean false, failed, unavailable, or
unsupported.

## Relationship To Existing Structures

The vocabulary maps to existing repository structures as follows:

| Vocabulary term | Existing repository concept | Relationship |
| --- | --- | --- |
| Selection Surface | `ContextPacket` | Model-visible context output containing selected current input, active goal, entities, facts, tools, open tool needs, decision schema, evidence, and context budget trace. |
| Selection Surface | Capability inventory | `build_capability_inventory(...)` selects/report capability verification beliefs from tools, `ToolNeed`s, and `capability_verified` facts. |
| Selection Surface | Current fact queries | `State.get_fact_support(...)`, `State.get_best_fact(...)`, and `State.get_current_facts(...)` select current support and representative facts. |
| Candidate | Projected `Fact` | Can be selected into context, support groups, current fact results, stale views, evidence-aware views, or explanations. |
| Candidate | `FactSupport` | Aggregate current-support group used by current-state selection, explanation selection, and capability inventory. |
| Candidate | `FactConflict` / `Contradiction` / `GraphValidationIssue` | Integrity candidates that may be surfaced as issues or used as rationale signals. |
| Candidate | `CapabilityInventoryEntry` | Capability status candidate selected into inventory output. |
| Ordering Rationale | `context_selection.order_facts(...)` | Fresh/unexpired facts before expired facts, then newer observations, higher confidence, and fact ID tie-break. |
| Ordering Rationale | `context_selection.order_evidence(...)` | Newer evidence before older evidence, then higher confidence and evidence ID tie-break. |
| Ordering Rationale | `context_selection.order_goals(...)` | Active goals before inactive goals, then goal ID tie-break. |
| Ordering Rationale | `context_selection.order_entities(...)` | Higher confidence entities first, then name and ID tie-breaks. |
| Current-State Rationale | `State.get_fact_support(...)` | Returns one unambiguous best support group or `None` when current support is ambiguous. |
| Current-State Rationale | `State.get_best_fact(...)` | Selects a representative fact from the best support using confidence, observed-vs-inferred preference, observed time, and ID. |
| Current-State Rationale | `State.get_current_facts(...)` | Uses predicate cardinality: single-cardinality returns one best fact; multi-cardinality returns one representative per support group. |
| Temporal Selection | Measurement support projection | Measurement predicates use latest-current sample semantics and `support_kind="current_sample"`. |
| Temporal Selection | `State.get_stale_facts()` | Surfaces expired facts separately from current fact selection. |
| Temporal Selection | Capability inventory age/stale metadata | Reports stale capability verification support and `age_seconds` from support timestamps. |
| Evidence-Aware Selection | Evidence Graph and `FactConfidence` | Provides support counts, unsupported status, evidence confidence, contradiction counts, reasons, and supporting event IDs. |
| Integrity-Aware Selection | `build_contradictions(...)` and graph issues | Provides contradictions, affected facts, severity, reasons, evidence views, and graph issue summaries. |
| Capability Selection | `build_capability_inventory(...)` | Maps support values and stale support to `verified`, `provider_reported`, `unverified`, `stale`, or `unknown`. |
| Explanation selection surface | `ExplanationBuilder.why(...)` | Selects current beliefs, competing beliefs, ambiguity, no-current-belief status, and conflict details for why queries. |

These mappings are descriptive. They do not require any structure to emit a new
rationale object.

## Relationship To Explanation

Explanation answers:

> Why does this claim exist?

Selection Rationale answers:

> Why was this candidate surfaced?

Explanation and Selection Rationale may share evidence, support, provenance,
temporal metadata, conflicts, contradiction data, graph issues, confidence
signals, capability status, and stale status. They remain distinct concerns.

`ExplanationBuilder.why(...)` explains current and competing beliefs for a
subject and predicate. Selection Rationale explains why a candidate was selected,
excluded, ordered, or treated as current for a specific selection surface.

A claim can have a complete Explanation but be excluded from a particular
`ContextPacket` because a limit was reached. A candidate can be selected for a
context surface because it is contradicted or stale, even though the Explanation
of the claim remains about support and provenance. Do not collapse Explanation
into Selection Rationale, and do not collapse Selection Rationale into
Explanation.

## Relationship To Context Composition

Context Composition answers:

> What matters now?

Selection Rationale answers:

> Why did this item count as mattering now?

Context Composition owns selection and formatting of context. Selection
Rationale explains selection after it happened.

Current context composition structures already expose important rationale
signals:

- `ContextComposer` chooses and formats packet sections;
- `context_selection` helpers provide deterministic intra-section ordering;
  limits, and trace accounting;
  capabilities from read-only projected inputs.

Selection Rationale should use these signals as vocabulary. It should not create
a new context owner or change context composition behavior.

## Relationship To Integrity

Integrity characterizes knowledge. Selection Rationale characterizes selection.

Integrity signals include unsupported status, contradicted status, fact
conflicts, conservative contradictions, graph validation issues, stale or expired
facts, confidence reductions, and capability verification states. These signals
may participate in rationale. For example:

- a contradiction can explain why an issue was surfaced;
- unsupported status can explain why a fact was excluded by default from a
  decision context view;
- stale status can explain why a fact appears in a stale-fact view rather than a
  current fact query;
- unverified or stale capability status can explain why a capability inventory
  entry is not reported as verified.

Integrity does not become selection. Selection does not become integrity.
Selection Rationale must not repair contradictions, resolve conflicts, delete
stale facts, alter confidence, verify capabilities, suppress graph issues, or
mutate projections.

## Relationship To Why-Not Vocabulary

Why-Not Vocabulary names negative-adjacent states Seed can already report from
existing read models. Selection Rationale names why a known candidate had a
selection outcome for a specific surface.

The overlap is intentional but bounded.

### Shared Concepts

Selection Rationale and Why-Not vocabulary can both refer to:

- inclusion;
- exclusion;
- no current belief;
- ambiguity;
- support and missing support;
- unsupported facts;
- evidence and missing evidence;
- competing beliefs;
- conflicts and contradictions;
- stale or expired facts;
- capability states such as verified, provider_reported, unverified, stale, and
  unknown;
- graph issues;
- missing or non-selected candidates.

### Key Difference

Selection Rationale asks:

> Why was candidate A selected, ordered, included, excluded, or treated as
> current on this surface?

Why-Not asks:

> Why is candidate B not believed, not verified, not current, not present, not
> selected, unsupported, stale, conflicted, absent, or otherwise negative-adjacent?

Selection Rationale is anchored to a selection surface and an outcome. Why-Not is
anchored to a negative-adjacent question or status.

For example:

- Selection Rationale may say fact A was selected because it was in the
  unambiguous strongest support group.
- Why-Not may say fact B was not current because it was competing support, stale,
  unsupported, filtered by dimensions, or not the unambiguous best support.
- Selection Rationale may say a capability entry was selected into inventory
  because it appeared in registered tool capabilities, open `ToolNeed`s, or
  `capability_verified` fact subjects.
- Why-Not may say a capability is unverified because no scoped
  `capability_verified` fact exists, because support is stale, or because the
  projected value maps to provider_reported or unknown.

### Terminology Alignment

Do not create competing terms for why-not statuses. Use the Why-Not vocabulary
words when discussing negative-adjacent conditions: Unknown, Not Believed,
Unsupported, Unverified, Stale, Conflicted, Contradicted, Ambiguous, Missing,
and Not Selected when those terms fit the surface.

Use Selection Rationale terms when discussing selection mechanics: Candidate,
Selected Candidate, Excluded Candidate, Selection Surface, Selection Signal,
Selection Basis, Selection Rule, Selection Outcome, Inclusion Rationale,
Exclusion Rationale, Ordering Rationale, Current-State Rationale, Context
Rationale, Tie-Break, Priority, Limit, and Budget.

Selection Rationale should not replace Why-Not vocabulary. Why-Not vocabulary
should not become a selection engine.

## Proposed Vocabulary Shape

The following shape is documentation-only. It is not a schema, runtime contract,
read model, adapter, inventory, event payload, or implementation requirement.

A Selection Rationale description may be discussed with these vocabulary slots:

```text
Selection Rationale
  surface: the selection surface being explained
  candidate: the candidate being explained
  outcome: selected | excluded | ordered | current | competing | dropped | ambiguous | not applicable
  basis: summary of the selection rules and signals that explain the outcome
  signals: known signals such as priority, limit, support, confidence, recency, expiry, status, count, or tie-break
  reason: short human-readable rationale
  status: implemented | partial | missing | implicit | unknown, when classifying repository support
  notes: boundary notes, caveats, or surface-specific defaults
  extensions: future documentation-only refinements, if needed
```

Use this shape to write consistent documentation. Do not add these fields to
runtime objects unless a separate future design explicitly approves a read-only
implementation.

## Complexity Traps

### SelectionEngine

A SelectionEngine is a trap because current selection behavior already lives in
concrete surfaces. Creating a new engine would obscure existing ownership and
risk changing selection behavior.

### ContextEngine

A ContextEngine is a trap because Context Composition already owns context
selection and formatting through existing context structures. Selection Rationale
should explain context selection, not become a new context owner.

### ReasoningEngine

A ReasoningEngine is a trap because rationale vocabulary is not a reasoning
system. It should not infer new knowledge, arbitrate truth, or create hidden
reasoning paths.

### Truth Selection

Truth Selection is a trap when it means a parallel truth system. Current-state
selection already exists in `State` and fact support aggregation. Selection
Rationale may describe that behavior but must not re-decide truth.

### LLM Ranking

LLM Ranking is a trap because existing selection and ordering are deterministic
where implemented. Rationale should not introduce opaque model-ranked ordering.

### Provider Ranking

Provider Ranking is a trap because capability inventory and provider-reported
signals are not provider selection, provider availability, or provider execution.

### Execution Selection

Execution Selection is a trap because choosing what to execute belongs to
runtime, policy, approval, and ToolExecutor boundaries, not Selection Rationale.

### Policy Selection

Policy Selection is a trap because rationale vocabulary must not authorize,
block, or route execution.

### Planner Integration

Planner Integration is a trap because rationale vocabulary should not become
planning, workflow decomposition, or action scheduling.

### Workflow Integration

Workflow Integration is a trap because explaining why something was surfaced is
not orchestration.

### Parallel Truth Systems

Parallel Truth Systems are a trap because Selection Rationale must explain
already-known selection outcomes without creating a second source of truth.

### Projection Mutation

Projection Mutation is a trap because rationale should be read-only and derived
from existing projections, traces, and metadata.

### Runtime Or ToolExecutor Integration

Runtime and ToolExecutor integration is a trap because this vocabulary document
has no execution role. It must not add runtime routes, ToolExecutor behavior,
provider behavior, event appends, or tool calls.

## Non-Goals

Selection Rationale Vocabulary v1 does not:

- implement selection rationale;
- implement adapters;
- implement inventories;
- implement read models;
- implement runtime behavior;
- implement ToolExecutor behavior;
- create schema classes;
- create rationale engines;
- add selection metadata;
- add explanation metadata;
- mutate projections;
- mutate facts;
- append events;
- add provider behavior;
- change `Runtime`;
- change `ToolExecutor`;
- change `EventLedger` ownership;
- change `ProjectionStore` ownership;
- change `StateProjector` semantics;
- change `ContextComposer` behavior;
- change selection ordering;
- change current fact selection;
- change explanation behavior;
- change capability inventory behavior;
- add `SelectionEngine`;
- add `ContextEngine`;
- add `ReasoningEngine`;
- add `Planner`;
- add `WorkflowEngine`;
- add runtime routes;
- add execution behavior;
- add provider behavior;
- add LLM ranking;
- create parallel truth systems.

## Future Work

Recommended future work should remain documentation-oriented.

The safest next step is **Selection Rationale Reconciliation**: a documentation
follow-up that checks this vocabulary against existing selection surfaces and
records any terminology conflicts, without changing runtime or projection
behavior.

A later **Selection Rationale Inventory** may be useful only if reconciliation
finds that documentation needs a stable list of surfaces, signals, and implicit
rules. Such an inventory should remain documentation-only unless a separate
future decision explicitly approves read-only implementation.

Do not recommend engines, runtime integration, ToolExecutor integration, LLM
ranking, provider selection, execution behavior, policy behavior, projection
mutation, fact mutation, event appends, or parallel truth systems as future work
from this vocabulary.

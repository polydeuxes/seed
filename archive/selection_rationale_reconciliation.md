# Executive Summary

Seed can already explain parts of selection, but not through one centralized
Selection Rationale surface.

The strongest existing rationale signals are implemented as deterministic
selection rules, ordering keys, projection fields, support groups, confidence
reasons, contradiction records, graph issue records, capability-inventory
reasons, and context-budget trace accounting. These signals answer many
"why included," "why ordered," and "why current" questions when a reader knows
which surface owns the selection.

filter. Most other exclusions remain implicit: a candidate is not current because
another support group is unambiguously strongest, because a predicate is
single-cardinality, because it expired, because a goal is inactive and sorted
behind active goals, or because a surface does not consider that candidate kind.

Selection Rationale is therefore **distributed and partially unified, but still
fragmented**. It is not missing as behavior. It is missing as a composed audit
view that gathers the already-existing sources without changing them.

Recommended next step: a documentation-only **Selection Rationale Summary
Characterization** is justified if the project wants one canonical map from
selection questions to existing sources and surfaces. No engine, runtime
integration, ToolExecutor integration, provider integration, LLM ranking, schema
class, inventory, read model, route, event append, or projection mutation is
supported by this audit.

# Purpose

This reconciliation audits existing Selection Rationale information in Seed.

It asks:

- what selection-rationale information already exists;
- how complete the existing information is;
- how fragmented the information is across modules and documents;
- which modules are sources, consumers, and outputs;
- where inclusion, exclusion, ordering, current-state, and integrity-aware
  rationale can already be recovered;
- how Selection Rationale relates to Why-Not concepts;
- what future documentation-only composition opportunities are supported by the
  current repository.

This document is an audit, not an implementation plan.

# Scope

In scope:

- context budget priorities, limits, and accounting;
- deterministic ordering helpers;
- fact support, current fact, stale fact, conflict, confidence, contradiction,
  evidence graph, and capability inventory projections;
- explanation outputs that separate current and competing beliefs;
- Why-Not vocabulary overlap.

Out of scope:

- changing runtime behavior;
- implementing selection rationale;
- adding inventories, read models, routes, engines, adapters, schema classes, or
  rationale metadata;
- mutating projections or appending events;
- integrating with `Runtime`, `ToolExecutor`, providers, policy, planners,
  workflows, LLM rankers, or execution systems.

# Files Inspected

Documentation inspected:

- `docs/selection_rationale_characterization.md`
- `docs/selection_rationale_vocabulary.md`
- `docs/context_composition_reconciliation.md`
- `docs/context_composition_vocabulary.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/why_not_vocabulary.md`
- `docs/why_not_explanation_characterization.md`
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
- `seed_runtime/confidence.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/evidence_graph.py`

# Existing Rationale Sources

A rationale source is an existing rule, field, projection, status, count, or
reason string that can explain selection without inventing new behavior.

| Source | Existing rationale information | Role | Status |
| --- | --- | --- | --- |
| `order_facts(...)` | Fresh/unexpired facts before expired facts, then newer observations, higher confidence, and fact id. | Source and consumer for context fact ordering. | Implemented, implicit per item |
| `order_evidence(...)` | Newer evidence, higher confidence, and evidence id. | Source and consumer for evidence ordering. | Implemented, implicit per item |
| `order_goals(...)` | Active goals before inactive goals, then goal id. | Source and consumer for goal ordering. | Implemented, implicit per item |
| `order_entities(...)` | Higher confidence, entity name, and entity id. | Source and consumer for entity ordering. | Implemented, implicit per item |
| `FactSupport` | Supporting fact ids, source types, aggregate confidence, observation range, latest observation, expiry, predicate semantics, and support kind. | Source and output. | Implemented |
| Predicate cardinality | Single-cardinality predicates select one representative; multi-cardinality predicates allow multiple current facts. | Source and consumer in current-state selection. | Implemented |
| Measurement semantics | Measurement predicates select the latest current sample rather than aggregating repeated values. | Source and consumer in support projection. | Implemented |
| Support tie key | Durable support uses confidence and support count; measurement support uses latest observation, confidence, and support count. | Source and consumer for current support selection. | Implemented, implicit |
| Representative fact tie key | Best/current representative fact uses confidence, observed-vs-inferred status, observed time, and id. | Source and consumer. | Implemented, implicit |
| Staleness and expiry | Expired facts are excluded from normal support/current selection and exposed through stale views. | Source, consumer, and output. | Implemented |
| Stale refresh recommendation reason | Maps a stale fact predicate to a deterministic refresh capability. | Output rationale. | Implemented |
| Confidence aggregation | Evidence count, explicit fact confidence, contradiction penalty, unsupported status, supporting event ids, and textual reasons. | Source and output. | Implemented |
| Contradiction handling | Exclusive-predicate multi-value detection, severity, fact ids, values, evidence, supporting events, and reason. | Source and output. | Implemented |
| Graph issue handling | `State.graph_issues` and `get_graph_issues(...)` expose graph-invalid warnings/errors. | Source and output. | Implemented |
| Evidence graph | Fact-evidence views, links, unsupported fact views, supporting events, and evidence summary counts. | Source and output. | Implemented |
| Capability inventory | Capability universe from tools, tool needs, and verification facts; state ranking; support, evidence, age, and reason. | Source, consumer, and output. | Implemented |
| Explanation builder | Current beliefs, competing beliefs, ambiguity, conflicts, evidence ids, support confidence, source types, inference chain, and alias resolution. | Consumer and output. | Implemented |

## Source, Consumer, Output Classification

  `context_selection` ordering helpers, `FactSupport`, predicate cardinality,
  measurement semantics, confidence aggregation, contradiction detection,
  Evidence Graph, stale fact handling, graph issues, and capability verification
  facts.
  `State.get_best_fact(...)`, `State.get_current_facts(...)`,
  `State.get_fact_support(...)`, `build_capability_inventory(...)`, and
  `ExplanationBuilder.why(...)`.
- **Primary rationale outputs:** `ContextPacket.context_budget`,
  fact and refresh recommendation views, `FactConfidence`, `Contradiction`,
  `EvidenceGraph` / `FactEvidenceView`, `CapabilityInventoryEntry`, and
  `Explanation`.

# Existing Rationale Surfaces

A rationale surface is an existing output or view where rationale information is
visible to callers.

| Surface | Direct rationale exposed | Indirect rationale exposed | No rationale / gap |
| --- | --- | --- | --- |
| `ContextPacket` | `context_budget` trace exposes priorities, limits, selected counts, dropped counts, and section order. | Included facts may carry selected evidence only when that evidence survived the same budget pass. | No per-item included-because or excluded-because. |
| `CapabilityInventoryEntry` | Direct `state`, supporting facts/evidence, support summary, age, and reason. | Capability inclusion can be inferred from the inventory universe. | No explicit excluded capabilities outside the universe. |
| `FactSupport` | Direct support group fields and support kind. | Current-state selection can be inferred by comparing support tie keys. | Does not state "selected because" directly. |
| Current fact queries | Returned current facts. | Current rationale recoverable from support group, cardinality, expiry, and representative tie keys. | Competing facts not returned by `get_best_fact(...)`. |
| Stale fact views | Expired facts sorted by expiry and id. | Separateness is explained by expiry semantics. | No richer stale rationale beyond expiry and refresh recommendation reason. |
| Issue views | Contradictions and graph issues expose reason/severity/summary. | Integrity-aware selection is visible through issue inclusion. | Issue inclusion is not linked back to all context surfaces. |
| Explanation outputs | Current vs competing beliefs, ambiguity, conflict, supporting facts/evidence, source types, inference chain, alias resolution. | Why-not overlap for competing/non-current beliefs. | Not a general selection-rationale surface for context budget, capability inventory, or issue views. |
| Evidence Graph | Fact-evidence links, unsupported views, supporting event ids, explanations. | Unsupported filtering and support strength can be inferred. | Does not decide which context candidates to include. |
| Confidence records | Direct reasons, unsupported and contradicted flags, support counts, confidence. | Decision-context ordering and inclusion can be explained from these fields. | Not linked to context packet ordering helpers. |

# Inclusion Rationale

Can Seed already explain why candidate A was included?

| Candidate / surface | Finding | Classification |
| --- | --- | --- |
| Fact in `ContextPacket` | Facts are ordered by freshness, observation recency, confidence, and id, then admitted by the `recent_facts` section limit/global budget. | Partial because item-level rationale is implicit. |
| Evidence in `ContextPacket` | Evidence is ordered by recency, confidence, and id, then admitted by the `recent_evidence` section limit/global budget. | Partial |
| Entity in `ContextPacket` | Entities are ordered by confidence/name/id, then admitted by the `entities` section limit/global budget. | Partial |
| Open tool need in `ContextPacket` | Open needs are selected from `State.open_tool_needs`, sorted by name, and budgeted under the open-tool-needs section. | Partial |
| Visible tool in `ContextPacket` | Registered tools are included if `ToolRegistry.list_tools(visible_only=True)` returns them. This is visibility rationale, not selection-rationale metadata. | Implicit |
| Graph issue in issue views | Included because the projected state contains graph validation warnings/errors and issue surfaces include them. | Implemented |
| Capability in inventory | Included when it appears in the inventory universe: registered tool capability, open/known tool need capability, or `capability_verified` fact subject. | Implemented |
| Stale fact in stale view | Included because `is_fact_expired(...)` returns true; stale refresh recommendation adds a predicate-to-capability reason. | Implemented |
| Current belief in explanation | Included as current when the support group is current under predicate cardinality and unambiguous strongest support rules. | Implemented |

Overall inclusion finding: **mostly Partial-to-Implemented**. The data and rules
exist, but most item-level inclusion explanations require reading the owning
surface's rule rather than a single rationale record.

# Exclusion Rationale

Can Seed already explain why candidate B was excluded?

| Candidate / surface | Finding | Classification |
| --- | --- | --- |
| Evidence dropped from `ContextPacket` by budget | Same as facts: section/global budget counts exist, but no per-evidence dropped reason exists. | Partial |
| Entity dropped from `ContextPacket` by budget | Same section-level accounting exists. | Partial |
| Goal not selected in `ContextPacket` | Only one goal is admitted by default; inactive goals sort behind active ones. Exclusion can be inferred from ordering and limit. | Partial |
| Unsupported fact surfaced elsewhere | Evidence Graph exposes unsupported fact views and confidence records expose unsupported reasons, so exclusion from one surface can coexist with visibility elsewhere. | Implemented as integrity surface, not as context exclusion trace |
| Expired fact excluded from support/current selection | Normal support projection skips expired facts unless `include_expired=True`; stale views expose expired facts separately. | Implemented |
| Competing support not selected as current | If a single-cardinality predicate has an unambiguous strongest support, lower-ranked supports become competing rather than current. | Partial because comparison is implicit. |
| Ambiguous support not selected as current | If multiple supports tie for the top support key, `get_fact_support(...)` returns no current support. Explanation can show ambiguity. | Implemented for explanation; implicit in state API. |
| Capability outside inventory universe | Not explainable from existing inventory output because unknown capabilities outside registered tools, tool needs, and verification facts are not candidates. | Missing / not applicable |
| Graph issue excluded from a non-issue surface | Not generally explained; issue surfaces own graph issue visibility. | Implicit |

Overall exclusion finding: **Partial**. Seed has some explicit exclusion reasons,
especially unsupported filtering and section-level budget drops, but most
exclusions require reconstructing candidate sets and applying implicit rules.

# Ordering Rationale

Can Seed explain why candidate A appears before candidate B?

| Ordering area | Existing rule | Classification |
| --- | --- | --- |
| Decision-context facts | Supported before unsupported, then higher confidence, subject, predicate, stable value, and fact id. | Implemented |
| Current support groups | Measurements prefer latest observation, then confidence and support count; durable supports prefer confidence and support count. | Implemented, implicit |
| Representative current facts | Higher confidence, observed facts before inferred facts, newer observation time, then id. | Implemented, implicit |
| Current multi-cardinality facts | Representatives are sorted by stable value. | Implemented, implicit |
| Stale facts | Earlier `expires_at` then fact id. | Implemented |
| Capability inventory entries | Capabilities are sorted by capability name; support selection ranks verification state, confidence, latest observation, and value. | Implemented, implicit |
| Evidence graph nodes/links | Deterministic node/link ordering by internal stable keys. | Implemented |
| Contradictions | Deterministic contradiction key over subject, predicate, id, and severity. | Implemented |

Overall ordering finding: **Implemented but implicit**. Ordering is deterministic
and inspectable in code, but most surfaces do not emit a human-readable ordering
rationale per pair of candidates.

# Current-State Rationale

Current-state rationale is concentrated in `State` and explanations.

## `State.get_fact_supports(...)`

- Resolves subject aliases by default, except endpoint-scoped predicates.
- Filters by predicate and optional dimensions.
- Uses projected `fact_supports` when possible, or rebuilds support groups from
  projected facts.
- Excludes expired facts unless `include_expired=True`.
- For durable predicates, groups facts by subject, predicate, dimensions, and
  value, aggregates independent support confidence, records source types,
  observation range, latest observation, expiry, and support kind.
- For measurement predicates, groups by subject, predicate, and dimensions while
  ignoring value in the grouping key, then selects the latest sample as the
  current sample.

Classification: **Implemented** for support-group rationale; **Partial** for
candidate-level comparison because tie-key details are implicit.

## `State.get_fact_support(...)`

- Calls `get_fact_supports(...)`.
- Selects an unambiguous strongest support.
- For measurements, strongest means latest observed time, confidence, and support
  count.
- For durable supports, strongest means confidence and support count.
- Returns `None` when no candidate exists or multiple candidates tie for the top
  support key.

Classification: **Implemented** for current support selection; **Partial** for
why a competing support lost because no comparison record is emitted.

## `State.get_best_fact(...)`

- Starts from the unambiguous best support.
- Chooses a representative supporting fact by confidence, observed-vs-inferred
  status, observed time, and id.
- Excludes expired supporting facts unless `include_expired=True`.

Classification: **Implemented** for representative current fact selection;
**Partial** for explaining non-selected supporting facts.

## `State.get_current_facts(...)`

- For single-cardinality predicates, returns the representative best fact.
- For multi-cardinality predicates, returns one representative fact per support
  group and sorts representatives by stable value.
- Respects expiry, alias, and dimension filters through support queries.

Classification: **Implemented** for predicate-cardinality-aware current state;
**Partial** for explicit rationale output.

## Measurements

Measurement rationale is strong and explicit in projection behavior: measurement
predicates represent volatile samples, their support groups use
`support_kind="current_sample"`, and the latest observed sample becomes current
for the subject/predicate/dimensions group. The rationale is **Implemented** in
state support projection and **indirectly exposed** through `FactSupport` fields.

# Integrity-Aware Rationale

Integrity signals already participate in selection, but with clear boundaries.

| Integrity signal | Participation in selection | Boundary | Classification |
| --- | --- | --- | --- |
| Conflicted / contradicted | Contradiction detection and fact conflicts identify multi-value disagreements; confidence aggregation penalizes contradicted facts; decision context surfaces contradicted flags and issues; explanations include conflict. | Contradictions do not resolve truth or mutate facts. | Implemented |
| Stale / expired | Expired facts are normally excluded from support/current selection and context ordering places expired facts after fresh ones; stale views expose them separately with refresh recommendations. | Staleness does not refresh facts or call tools. | Implemented |
| Graph-invalid | Graph validation issues are stored on `State`, queryable by severity, and surfaced as context issues. | Graph issues do not repair graph structure. | Implemented |
| Unverified | Capability inventory emits `unverified` when no `capability_verified` fact exists in the inventory universe; stale verification facts become `stale`. | Verification state does not execute verification or select providers. | Implemented |
| Confidence | Context and decision views order/filter/summarize facts using confidence and support counts; current-state support uses confidence as a ranking key. | Confidence is support strength, not truth. | Implemented |
| Evidence support | Evidence Graph and confidence aggregation provide support counts, event ids, evidence nodes, links, and unsupported views. | Evidence views are read-only and do not append events. | Implemented |

Integrity-aware rationale finding: **Implemented but distributed**. Integrity
signals strongly inform selection surfaces, yet no single integrity-aware
selection rationale surface composes them all.

# Relationship To Why-Not

Why-Not and Selection Rationale overlap, but they are not the same concern.

## Shared concepts

- candidate vs selected candidate;
- excluded, absent, non-current, competing, unsupported, stale, contradicted, and
  ambiguous outcomes;
- surface-specific scope;
- known-vs-unknown candidate distinction;
- support, confidence, evidence, predicate cardinality, expiry, and conflict as
  reasons;
- need to avoid inventing reasons that existing projections do not support.

## Shared signals

- unsupported fact flags and unsupported fact views;
- `FactSupport` groups and support tie keys;
- current and competing beliefs in explanation outputs;
- contradiction and conflict records;
- stale fact views and refresh recommendation reasons;
- graph issues;
- capability verification states and reasons.

## Shared vocabulary

Selection Rationale vocabulary terms such as Selected Candidate, Excluded
Candidate, Selection Surface, Selection Signal, Inclusion Rationale, Exclusion
Rationale, Ordering Rationale, Current-State Rationale, Tie-Break, Ambiguity,
Integrity Signal, and Candidate Universe overlap naturally with Why-Not concepts
around absent or non-selected alternatives.

## Distinct concepts

- **Selection Rationale** asks why a surface included, excluded, ordered, or made
  current an already-known candidate.
- **Why-Not** asks why an expected outcome, answer, action, capability, fact, or
  candidate did not happen or did not appear.
- Selection Rationale is surface-centered and can explain positive inclusion and
  ordering, not only absence.
- Why-Not may need to address non-candidates, missing evidence, missing
  capability, policy/execution non-occurrence, or unavailable knowledge. Those
  cases are outside Selection Rationale unless the candidate was within a
  selection surface's candidate universe.

## Potential duplication

Potential duplication exists if future work creates separate records for:

- excluded context candidates and Why-Not absence reasons;
- competing current-state facts and Why-Not non-current facts;
- unsupported filtering and unsupported Why-Not reasons;
- stale fact separation and Why-Not stale/non-current reasons;
- capability inventory `unverified` reasons and Why-Not capability absence
  reasons.

## Potential conflict

Potential conflict would arise if Why-Not and Selection Rationale independently
rank truth, choose providers, execute verification, infer missing candidates, or
reinterpret confidence. Both vocabularies should remain read-only over existing
projection and selection surfaces.

Relationship finding: **overlapping but distinct**. Why-Not is the closest
adjacent explanation vocabulary for exclusion, but Selection Rationale also
covers inclusion, ordering, current-state choice, and section-level context
admission.

# Fragmentation Assessment

Selection Rationale is **distributed, fragmented, and partially unified**.

It is not centralized. There is no single Selection Rationale object, inventory,
summary, navigation view, or explanation endpoint.

It is not wholly missing. The repository already contains substantial rationale
information:

- ordering surfaces: `order_facts(...)`, `order_evidence(...)`,
  `order_goals(...)`, and `order_entities(...)`;
- current-state surfaces: `FactSupport`, `get_fact_supports(...)`,
  `get_fact_support(...)`, `get_best_fact(...)`, `get_current_facts(...)`, and
  fact conflicts;
- integrity surfaces: confidence records, Evidence Graph, unsupported views,
  contradiction records, graph issues, stale fact views, and stale refresh
  recommendations;
- capability surfaces: capability inventory entries, support summaries,
  evidence summaries, state ranking, and reason fields;
- explanation surfaces: current beliefs, competing beliefs, ambiguity, conflict,
  support confidence, evidence ids, source types, inference chain, and alias
  resolution.

## Evidence of partial unification

  Detection, and Confidence Aggregation into one read-only decision surface.
- `ExplanationBuilder.why(...)` already composes support, current-vs-competing
  belief status, conflict, provenance, inference, and alias resolution for a
  query.
- `CapabilityInventoryEntry` already composes verification facts, support,
  evidence, staleness, age, and reason for capabilities.
  counts, and section order for context packet selection.

## Evidence of fragmentation

- Context selection rationale is separated between `ContextComposer`, ordering
- Decision-context fact rationale is separated between confidence aggregation,
  evidence graph, contradiction handling, unsupported filtering, and summary
  counts.
- Current-state rationale is separated between support projection, predicate
  catalog/cardinality, measurement semantics, support tie keys, representative
  fact tie keys, and explanations.
- Capability rationale is separated from context and explanation surfaces even
  though it uses the same support/evidence/stale signals.
- Exclusion rationale is mostly reconstructed from selected outputs, counts,
  filters, and ordering, rather than emitted as first-class per-candidate
  records.
- Integrity signals influence selection but are surfaced by separate integrity
  views.

## Duplication assessment

The audit found **conceptual overlap** more than direct duplication:

- contradiction/conflict concepts appear in contradiction views, fact conflicts,
- unsupported concepts appear in Evidence Graph, Confidence, Decision Context,
  and Why-Not vocabulary;
- stale concepts appear in context ordering, support/current selection, stale
  views, stale refresh recommendations, and capability inventory;
- current-vs-competing belief concepts appear in State and explanations;
- capability support concepts reuse `FactSupport` rather than inventing a new
  support engine.

This overlap is useful but fragmented. It does not currently create a parallel
truth system.

# Composition Opportunities

The following are future documentation or characterization opportunities only.
They are supported by the audit, but no implementation is required by this
reconciliation.

## Selection Rationale Summary Characterization

A summary characterization could map common questions to existing sources:

- why included in context;
- why dropped by context budget;
- why ordered before another item;
- why current;
- why competing;
- why unsupported;
- why stale;
- why contradicted;
- why capability is unverified/stale/verified.

This is the strongest supported next step because it composes existing knowledge
without changing runtime behavior.

## Selection Rationale Inventory Characterization

An inventory characterization could list existing rationale signals and surfaces
without creating a runtime inventory:

- signals by domain: budget, ordering, support, confidence, integrity,
  staleness, capability, explanation;
  `FactSupport`, `FactConfidence`, `Contradiction`, `EvidenceGraph`,
  `CapabilityInventoryEntry`, `Explanation`;
- explicit vs implicit rationale coverage.

This is also supported, but it should remain documentation-only unless a later
separate design justifies an actual read model.

## Selection Rationale Navigation Characterization

A navigation characterization could describe how an operator moves from one
surface to another:

- from a context fact to its confidence/evidence/contradiction records;
- from a dropped section count to budget priorities and limits;
- from a current fact to support groups and competing beliefs;
- from a stale fact to refresh recommendation;
- from a capability entry to support and evidence summaries.

This should not imply a new route or UI.

# Complexity Traps

The audit does not support creating any of the following:

- **SelectionEngine.** Selection already occurs in surface-owned code paths. A
  new engine would centralize ownership that currently belongs to context,
  state, integrity, capability inventory, and explanation surfaces.
- **ReasoningEngine.** Rationale is descriptive over projected knowledge; it is
  not a new reasoning subsystem.
- **ContextEngine.** Context composition already exists as `ContextComposer`,
  would duplicate existing context boundaries.
- **Planner or WorkflowEngine.** Selection rationale does not plan actions,
  schedule work, or orchestrate execution.
- **Runtime integration.** Existing rationale sources are read-only over
  projected state and should not change runtime flow.
- **ToolExecutor integration.** Explanations of capability state, stale facts, or
  unsupported facts must not execute tools.
- **LLM ranking.** Current ordering is deterministic and inspectable. LLM ranking
  would add opaque behavior and weaken auditability.
- **Truth selection system.** Support, confidence, contradiction, and current
  state already exist. A parallel truth system would conflict with projection
  ownership.
- **Provider ranking.** Capability inventory and context selection do not choose
  providers or execution targets.
- **Execution ranking.** Rationale describes selected knowledge, not selected
  actions.
- **Parallel inventories/read models.** A runtime inventory or read model would
  duplicate existing surfaces unless separately justified.
- **Rationale metadata on every object.** Existing surfaces already expose many
  signals. Blanket metadata would risk duplicating source-of-truth fields and
  drifting from owning rules.

# Recommended Next Step

Recommended: **Selection Rationale Summary Characterization**.

Reason:

- Selection behavior already exists.
- Rationale signals already exist.
- Rationale vocabulary already exists.
- The main gap is fragmentation: operators and maintainers must know which
  surface owns which rationale.
- A summary characterization can compose findings without implementing new
  behavior.

Not recommended now:

- SelectionEngine;
- ContextEngine;
- ReasoningEngine;
- Planner;
- WorkflowEngine;
- runtime routes;
- ToolExecutor integration;
- provider integration;
- LLM ranking;
- schema classes;
- runtime inventories;
- read models;
- rationale traces beyond existing trace surfaces.

If no additional documentation is desired, another valid outcome is **no
implementation required**: existing surfaces are sufficient for many audit needs
when read together.

# Non-Goals

This reconciliation does not:

- implement selection rationale;
- implement inventories;
- implement read models;
- implement runtime behavior;
- implement adapters;
- implement schema classes;
- add rationale metadata;
- add rationale traces;
- add runtime routes;
- mutate projections;
- append events;
- create engines;
- change `Runtime`;
- change `ToolExecutor`;
- change `EventLedger` ownership;
- change `ProjectionStore` ownership;
- change `ContextComposer` behavior;
- change selection ordering;
- change current fact selection;
- change capability inventory behavior;
- change explanation behavior;
- add provider behavior;
- create parallel truth systems.

# Conclusion

Seed can already explain selection in many cases, but explanation is distributed
across existing surfaces rather than centralized.

The repository can explain inclusion best where the surface has explicit
filtering, support/current-state selection, stale views, contradiction issues,
graph issues, and capability inventory entries. It can explain ordering well
because ordering keys are deterministic. It can explain current-state rationale
through `FactSupport`, predicate cardinality, measurement semantics, support tie
keys, representative fact tie keys, and explanation outputs.

The repository is weakest at explicit per-candidate exclusion rationale. Some
exclusion is explicit, especially unsupported filtering and section-level budget
counts, but most exclusion remains implicit in ordering, limits, candidate
universes, predicate cardinality, expiry, and unambiguous-best-support rules.

Therefore Selection Rationale should be treated as an existing but fragmented
cross-surface concern. The next safe step, if any, is documentation-only summary
or inventory characterization. No runtime behavior, ToolExecutor behavior,
projection mutation, event append, engine, route, provider integration, LLM
ranking, or parallel truth system is warranted by this audit.

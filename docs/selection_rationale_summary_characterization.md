# Executive Summary

A Selection Rationale Summary would be a documentation-level composition of
existing selection-rationale signals, not a new runtime feature. The repository
already exposes substantial rationale information through context budgets,
context ordering helpers, decision-context views, fact support, confidence
aggregation, contradiction and graph issue views, stale fact views, capability
inventory entries, and explanation outputs.

The audit finds that most direct user/operator questions about a selected item
are already answerable when the caller knows which owning surface to inspect:
why a fact is current, why a context item was admitted, why a section dropped
items, why a capability is verified/unverified/stale, why a stale fact was
surfaced, why an issue exists, or why an explanation reports ambiguity or
competition.

The strongest unanswered questions are not per-item explanation questions. They
are cross-surface aggregate questions, such as how often budget limits caused
exclusion, how often selected context facts relied on support aggregation versus
current samples, how often selected facts relied on temporal ordering, or which
rationale signal categories dominate a corpus of selections. Those questions are
not answered by existing surfaces because there is no single rationale event
stream, rationale classifier, or cross-surface statistics layer. However, the
audit did not find a strong current user/operator need that would justify adding
such a layer now.

Recommended outcome: **C. Summary not justified** as an implementation or read
model. A documentation-only characterization is useful as an audit artifact and
question map, but a first-class Selection Rationale Summary is not currently
justified because the existing surfaces already answer the strongest concrete
per-item questions, while the unanswered aggregate questions would require new
classification/statistics concepts that are not otherwise demanded by the
repository.

# Purpose

This document characterizes whether Seed genuinely needs a Selection Rationale
Summary.

The primary question is:

> What user/operator question would a Selection Rationale Summary answer that
> existing rationale surfaces cannot already answer?

This is an audit. It does not implement a summary, inventory, navigation view,
read model, runtime behavior, route, adapter, schema class, rationale metadata,
explanation metadata, projection mutation, event append, engine, or parallel
truth system.

# Scope

In scope:

- existing Selection Rationale characterization, vocabulary, and reconciliation
  documents;
- existing Why-Not characterization and vocabulary documents;
- existing Projection Integrity Summary and Drilldown characterization documents;
- context composition documents;
- runtime context composition, budgeting, ordering, decision-context views,
  current-fact selection, fact support, stale fact handling, capability
  inventory, confidence aggregation, contradictions, Evidence Graph, and
  explanations;
- determining whether a Selection Rationale Summary should be aggregate,
  inventory, navigation, explanation, summary, view, or report;
- determining which user/operator questions are already answerable and which are
  not easily answerable.

Out of scope:

- implementing a Selection Rationale Summary;
- adding rationale inventories, read models, routes, adapters, schema classes, or
  metadata;
- changing `Runtime`, `ToolExecutor`, `EventLedger`, `ProjectionStore`,
  `ContextComposer`, `ContextBudget`, selection ordering, current fact
  selection, capability inventory, explanations, execution behavior, provider
  behavior, or projection behavior;
- appending events, mutating projections, or creating engines.

# Files Inspected

Documentation inspected:

- `docs/selection_rationale_characterization.md`
- `docs/selection_rationale_vocabulary.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/projection_integrity_summary_characterization.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/why_not_vocabulary.md`
- `docs/why_not_explanation_characterization.md`
- `docs/context_composition_reconciliation.md`
- `docs/context_composition_vocabulary.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/knowledge_lifecycle_reconciliation.md`

Runtime files inspected:

- `seed_runtime/context.py`
- `seed_runtime/context_budget.py`
- `seed_runtime/context_selection.py`
- `seed_runtime/context_views.py`
- `seed_runtime/state.py`
- `seed_runtime/explanations.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/confidence.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/evidence_graph.py`

# Existing Questions Already Answerable

The following questions are already answerable by existing surfaces, although
several require reading the owning surface's deterministic rule rather than a
single rationale object.

| Question | Existing answerability | Existing surfaces |
| --- | --- | --- |
| Why was this fact selected for a model-visible context packet? | Partially answerable. Facts are ordered by freshness, observation recency, confidence, and id, then admitted by `ContextBudget` section/global limits. The packet contains section-level budget trace, but not per-fact reason text. | `ContextComposer`, `order_facts(...)`, `ContextBudget`, `BudgetTrace` |
| Why was this fact selected for `DecisionContextView`? | Answerable. Confidence records are filtered for unsupported facts by default, then sorted by support presence, confidence, subject, predicate, stable object value, and fact id. | `select_context_facts(...)`, `FactConfidence`, `ContextSummary` |
| Why was this fact not selected for `DecisionContextView`? | Answerable for unsupported facts because the default selector excludes unsupported records unless `include_unsupported=True`. | `select_context_facts(...)`, `FactConfidence`, Evidence Graph unsupported views |
| Why was this fact not selected as the current fact? | Partially answerable. Single-cardinality current selection uses the unambiguous strongest support group, then chooses a representative supporting fact by confidence, observed-vs-inferred status, observation time, and id. Ties can produce ambiguity. | `State.get_fact_support(...)`, `State.get_best_fact(...)`, `ExplanationBuilder.why(...)` |
| Why is this current fact current? | Answerable. Fact support exposes support kind, support confidence, supporting fact ids, source types, observation range, latest observation time, expiry, and predicate semantics; explanations expose current and competing beliefs. | `FactSupport`, `State.get_fact_supports(...)`, `State.get_fact_support(...)`, `State.get_current_facts(...)`, `ExplanationBuilder.why(...)` |
| Why was this capability surfaced? | Answerable within the capability inventory universe. Capabilities come from registered tools, tool needs, and `capability_verified` fact subjects; entries include state, reason, support summary, facts, evidence, and age. | `build_capability_inventory(...)`, `CapabilityInventoryEntry` |
| Why was this issue surfaced? | Answerable. Contradiction issues are produced by contradiction detection over exclusive-predicate multi-value conflicts; graph issues come from projected state validation and carry reason/severity. | `Contradiction`, `ContradictionSummary`, `State.graph_issues`, `DecisionContextView` issues |
| Why was this stale fact surfaced? | Answerable. Stale facts are expired facts, sorted by expiry and id; refresh recommendations map predicates to deterministic refresh capabilities and include reason text. | `State.get_stale_facts()`, `State.get_stale_fact_refresh_recommendations()` |
| Why was this context item included? | Partially answerable. Section priorities, section limits, global budget, section ordering, and deterministic within-section ordering identify inclusion conditions. | `ContextComposer`, `ContextBudget`, `BudgetTrace`, `context_selection.py` |
| Why was this context item excluded? | Partially answerable. Section-level dropped counts and deterministic ordered inputs identify suffix drops, but no per-item excluded-because record exists. | `BudgetTrace`, ordered input sections, `ContextBudget` |
| Why is this belief current, competing, ambiguous, or absent? | Answerable for fact queries. The explanation builder reports current beliefs, competing beliefs, ambiguity/no-current status, conflicts, supporting facts, evidence ids, source types, inference chains, and alias resolution. | `ExplanationBuilder.why(...)`, `FactSupport`, `FactConflict` |

# Existing Questions Not Easily Answerable

The hard gaps are cross-surface, aggregate, or classification-oriented questions.
They are not easily answerable because Seed does not emit rationale records,
rationale classifications per selected item, or a cross-surface rationale event
stream.

Supported examples from the audit:

- **How many context items were dropped due to budget constraints across many
  packets?** `BudgetTrace.dropped_counts` exists for one budget pass, but there is
  no aggregate store or historical summary across packets.
- **How many exclusions occurred because of section limits versus global
  `max_items`?** `BudgetTrace` exposes selected and dropped counts, limits, max
  items, and section order, but it does not classify each drop by precise cause
  when both section and global limits can interact.
- **How many selected context facts relied on temporal ordering?** `order_facts`
  uses freshness and observation recency, but no selected fact carries a
  `temporal_rationale` classification.
- **How many selections relied on integrity signals?** Integrity signals such as
  unsupported, contradicted, confidence, staleness, graph issues, and capability
  verification are available, but no summary classifies selections by signal
  category.
- **How many current facts were selected through aggregate support versus current
  sample semantics?** `FactSupport.support_kind` distinguishes `aggregate` and
  `current_sample`, but there is no repository-wide current-selection summary.
- **Which rationale signals dominate current selection?** Selection rules use
  budget, ordering, support, confidence, temporal, integrity, stale, and
  capability signals, but no surface weights or counts their dominance.
- **What kinds of rationale are most common across the repository?** Existing
  vocabulary names categories, but the runtime does not count rationale category
  frequency.
- **How many context items were excluded as non-candidates rather than dropped
  candidates?** Candidate universes are surface-specific, and existing outputs
  generally omit non-candidates.

These gaps do not automatically justify implementation. They justify, at most,
future audit questions about whether operators need cross-run rationale
analytics. Without that need, adding statistics or classifiers would risk
inventing a parallel rationale system.

# Existing Rationale Surfaces

| Surface | Existing summary information | Existing aggregate information | Existing rationale information | Assessment |
| --- | --- | --- | --- | --- |
| `ContextBudget` | Section priorities, section limits, optional `max_items`. | Per-pass `selected_counts` and `dropped_counts` via `BudgetTrace`. | Explains section admission order and section/global cap effects. | Strong section-level rationale; not per-item. |
| `BudgetTrace` | Per-pass budget trace dictionary. | Selected and dropped counts per section. | Effective priorities, limits, max items, selected counts, dropped counts, section order. | Strongest existing context-packet summary-like rationale surface. |
| `ContextComposer` | Composed `ContextPacket` with `context_budget`. | None beyond attached trace. | Uses ordering helpers, budgeted sections, selected evidence inclusion for facts, and visible tool listing. | Rationale is recoverable from composition rules. |
| `context_selection.py` helpers | None as output. | None. | Deterministic ordering by freshness/recency/confidence/status/id/name. | Strong implicit ordering rationale. |
| `DecisionContextView` | `ContextSummary` counts facts, issues, contradicted facts, strong/weak/unsupported included facts. | Included fact and issue counts. | Fact confidence, contradiction flags, evidence counts, issues, requirements, capabilities, projection metadata. | Existing partial rationale summary for decision context only. |
| `select_context_facts(...)` | None as standalone output. | None. | Unsupported filtering and deterministic ordering by support presence/confidence/stable identifiers. | Direct rule but no reason records. |
| Fact Support | Individual support groups. | None across all supports. | Supporting fact ids, source types, confidence, observation range, expiry, predicate semantics, support kind. | Strong current-state rationale surface. |
| Capability Inventory | Inventory entries with state and reason. | No explicit aggregate summary in inspected file. | Capability universe, verification state, support summary, evidence summaries, age, stale/unverified reasons. | Strong capability-specific rationale surface. |
| Issue Views | Context issue summaries; contradiction and graph issue records. | Contradiction summary counts; graph issue counts exist through state/summary-like integrity surfaces. | Reasons, severity, affected facts, values, evidence/supporting events. | Strong issue rationale, not selection-wide. |
| Stale Fact Views | Stale fact list and refresh recommendations. | No broad stale aggregate in inspected runtime file. | Expiry status, ordering by expiry/id, predicate-to-capability refresh reason. | Strong stale rationale for stale-specific questions. |
| Explanation outputs | Query explanation status with current/competing beliefs. | None. | Current beliefs, competing beliefs, ambiguity/no-current status, conflict, support confidence, facts, evidence ids, source types, inference chain, alias resolution. | Strong per-query explanation, not context-budget rationale. |
| Confidence Aggregation | `ConfidenceSummary`. | Fact count, strong/weak/unsupported/contradicted counts, average confidence. | Per-fact support count, contradiction count, unsupported/contradicted flags, reasons, supporting events. | Strong integrity rationale input for fact selection. |
| Contradictions | `ContradictionSummary`. | Contradiction, affected fact, severity counts. | Exclusive-predicate conflict reason, values, fact ids, evidence, supporting events. | Strong integrity rationale for issue surfacing. |
| Evidence Graph | `EvidenceSummary`. | Evidence count, linked fact count, unsupported fact count, average confidence. | Fact-evidence links, unsupported fact views, supporting event ids, explanations. | Strong support/unsupported rationale. |

# Existing Summary-Like Surfaces

The repository already contains several surfaces that behave like summaries, but
none is a general Selection Rationale Summary.

- **Projection Integrity Summary.** Its characterization identified that
  integrity signals exist and can be composed into a read-only summary; it solved
  the problem of collecting support, conflict, graph, stale, verification, and
  caveat signals without turning them into truth or execution logic.
- **Projection Integrity Drilldown / Integrity Navigation.** These documents
  characterize movement from summary-level integrity signals to underlying facts,
  evidence, conflicts, stale facts, and verification signals. They are integrity
  navigation aids, not selection-rationale surfaces.
- **Capability Inventory.** This is summary-like for capability verification. It
  answers why a capability is verified, unverified, stale, provider-reported, or
  unknown inside a defined capability universe. It does not summarize rationale
  for context facts, issue views, or current-state selection.
- **State Summary.** State-level summary concepts can describe current projected
  state and counts, but they are not rationale summaries. They summarize what is
  projected, not why a particular surface selected an item.
- **Issue Views.** Contradiction and graph issue views summarize integrity
  problems and include reasons/severity. They function as issue rationale
  summaries, not selection rationale summaries.
- **Explanation surfaces.** Explanations summarize support, provenance,
  conflicts, current/competing beliefs, inference, and alias resolution for one
  query. They are the strongest answer to fact-level "why" questions, but they do
  not summarize context budgets, capability inventories, or issue inclusion.
- **`ContextSummary`.** This is the closest implemented selection-adjacent
  summary. It summarizes facts and issues included in a `DecisionContextView`,
  including contradicted, strongly supported, weakly supported, and unsupported
  included facts. It does not summarize exclusions or cross-surface rationale.
- **`BudgetTrace`.** This is the closest implemented context-packet rationale
  summary. It summarizes priorities, limits, selected counts, dropped counts, and
  section order for one budget pass. It does not include item identifiers or
  reason classifications.

Finding: existing summary-like surfaces cover their own domains well. None is a
full Selection Rationale Summary, but the absence of a single summary does not by
itself prove one is needed.

# Summary Candidate Categories

| Candidate category | Classification | Reasoning |
| --- | --- | --- |
| Selection Rationale Summary | **Unnecessary for implementation; Partial as documentation.** | Per-item user/operator questions are already mostly answerable from owning surfaces. A documentation map is useful, but an implemented summary would duplicate existing outputs unless a concrete cross-surface aggregate need appears. |
| Selection Rationale Inventory | **Partial.** | An inventory of rationale signals and surfaces is supported by reconciliation findings, but implementing an inventory read model would duplicate existing domain surfaces. Documentation-only inventory language is enough now. |
| Selection Rationale Navigation | **Partial.** | Navigation from context fact to confidence/evidence, budget drop to limits, current fact to support, stale fact to refresh recommendation, and capability to support/evidence is meaningful. No route/UI/read model is justified. |
| Selection Rationale Drilldown | **Partial.** | Drilldown is meaningful as a documentation pattern for following existing references, but not as a new runtime object. Existing surfaces already provide most drilldown targets. |
| Selection Rationale Statistics | **Unsupported now.** | Aggregate questions are not easily answerable, but the repository lacks a demonstrated need for cross-run rationale analytics and lacks rationale classifications/events from which statistics could be safely derived. |
| Selection Rationale Classification | **Unsupported now.** | Vocabulary categories exist, but runtime items do not carry stable rationale classifications. Adding classifications would be metadata implementation, which this audit does not justify. |

# Relationship To Integrity Summary

Projection Integrity Summary and Selection Rationale Summary are not equivalent.

Projection Integrity Summary solved a clearer problem:

- integrity signals were numerous, implemented, and domain-coherent;
- unsupported facts, fact conflicts, contradictions, graph issues, stale facts,
  refresh recommendations, current knowledge views, and capability inventory
  entries could be composed as read-only integrity status;
- the operator question was concrete: "What integrity caveats affect projected
  knowledge right now?"

Selection Rationale has a weaker equivalent problem:

- rationale signals are numerous and implemented, but they are surface-owned by
  context composition, decision context, current-state support, integrity,
  capability inventory, and explanations;
- most concrete item-level questions already have an owning surface;
- the remaining unanswered questions are mostly aggregate/statistical and would
  require new rationale classification or history rather than simple composition;
- there is no equally strong single operator question comparable to "What is the
  current integrity state of projections?"

Therefore, the existence of Projection Integrity Summary does not imply that
Selection Rationale needs an equivalent summary. Integrity Summary addressed a
cohesive integrity-status gap. Selection Rationale fragmentation more strongly
supports vocabulary and documentation navigation than implementation.

# Relationship To Why-Not

Selection Rationale and Why-Not overlap most strongly around exclusion,
non-current, absent, unsupported, stale, contradicted, and ambiguous outcomes.

Overlap:

- both need candidate/universe boundaries;
- both use support, confidence, evidence, predicate cardinality, expiry,
  contradictions, graph issues, and capability verification state;
- both must avoid inventing reasons for non-candidates or unknown facts;
- both can explain why an expected item did not appear when the expected item was
  actually in a selection surface's candidate universe.

Differences:

- Selection Rationale is surface-centered: why this surface included, excluded,
  ordered, or made current an already-known candidate.
- Why-Not is expectation-centered: why an expected answer, action, capability,
  fact, outcome, or candidate did not happen or did not appear.
- Selection Rationale covers positive inclusion and ordering; Why-Not primarily
  covers absence or non-occurrence.
- Why-Not may need to discuss missing evidence, missing observations,
  unavailable capabilities, policy/execution non-occurrence, or unknown
  candidates that were never part of a selection surface.

Risks:

- duplicating excluded-candidate records and Why-Not absence records;
- separately classifying competing facts and non-current facts;
- creating two explanations for unsupported filtering, stale separation, or
  capability unverified status;
- letting either concept rank truth, choose providers, execute verification, or
  reinterpret confidence.

Finding: a Selection Rationale Summary would duplicate Why-Not concepts if it
became an absence/exclusion explanation system. If future work proceeds, it must
remain surface-scoped and should reuse Why-Not vocabulary for absence-oriented
questions rather than create parallel explanations.

# Fragmentation Assessment

Selection rationale is distributed, fragmented, and partially unified.

Evidence of distribution:

- context-packet rationale is split across `ContextComposer`, ordering helpers,
  `ContextBudget`, and `BudgetTrace`;
- decision-context rationale is split across confidence aggregation, Evidence
  Graph, contradictions, unsupported filtering, context issue formatting, and
  `ContextSummary`;
- current-state rationale is split across `FactSupport`, predicate cardinality,
  measurement semantics, support tie keys, representative fact tie keys, and
  explanations;
- capability rationale is owned by capability inventory and support/evidence
  summaries;
- stale rationale is owned by expiry semantics, stale views, and refresh
  recommendations;
- issue rationale is owned by contradiction detection and graph validation.

Evidence of partial unification:

- `BudgetTrace` unifies context-budget accounting for one budget pass;
- `DecisionContextView` composes facts, issues, requirements, capabilities, and
  summary counts;
- `ExplanationBuilder.why(...)` composes support, current/competing beliefs,
  conflicts, provenance, inference, and alias resolution for one query;
- `CapabilityInventoryEntry` composes capability state, support, evidence,
  staleness, age, and reason;
- confidence, contradiction, and evidence summaries already provide integrity
  aggregate counts.

Does fragmentation justify a summary?

- Fragmentation **does justify vocabulary and documentation navigation** because
  operators need to know which surface owns which rationale question.
- Fragmentation **does not by itself justify implementation** because the
  fragmented surfaces are intentionally owned by their domains and already answer
  many questions.
- A summary would be justified only if a recurring user/operator question cannot
  be answered without cross-surface composition. This audit found plausible
  aggregate questions, but no strong evidence that they are needed now.

# Composition Opportunities

The following opportunities are documentation-only unless a later audit finds a
stronger need.

## Summary

A short documentation map could list common questions and point to existing
surfaces. This document already performs that function. No implementation is
needed.

## Inventory

A documentation inventory of rationale surfaces is useful for maintainers:

- budget and section-level accounting;
- ordering helpers;
- support/current-state rules;
- confidence and evidence support;
- contradictions and graph issues;
- stale facts and refresh recommendations;
- capability verification inventory;
- explanation outputs.

No runtime inventory is justified.

## Navigation

Documentation can describe drill paths:

- context item -> budget trace -> ordering helper -> owning state collection;
- decision-context fact -> confidence record -> Evidence Graph -> contradiction
  record;
- current fact -> support groups -> competing beliefs -> explanation output;
- stale fact -> expiry -> refresh recommendation;
- capability entry -> support summary -> supporting facts/evidence.

No route, UI, adapter, or read model is justified.

## Drilldown

Drilldown is meaningful only as a way to follow existing identifiers and fields.
It should not create new rationale records.

## Statistics

Statistics would be meaningful only if operators need cross-run/cross-surface
analytics. Implementing statistics would require stable rationale
classifications, candidate histories, or trace records that do not exist today.
This is not recommended now.

# Rejection Criteria

Selection Rationale Summary should **not** exist as an implementation when any of
the following hold:

- existing surfaces answer the concrete user/operator question;
- the only benefit is renaming existing `BudgetTrace`, `ContextSummary`,
  `FactSupport`, capability inventory, or explanation outputs;
- the summary would duplicate Why-Not absence/exclusion explanations;
- no unanswered user/operator question is strong enough to justify cross-surface
  composition;
- there is no meaningful aggregate value beyond documentation;
- the summary would require new rationale metadata on facts, context items,
  capabilities, issues, explanations, or projections;
- the summary would require a new read model, inventory, route, adapter, schema
  class, event type, projection mutation, or persisted trace;
- the summary would centralize ownership that currently belongs to context,
  state, integrity, capability inventory, and explanation surfaces;
- the summary would classify or rank truth, provider quality, execution options,
  tool choices, or LLM relevance;
- the summary would be useful only for hypothetical analytics not supported by a
  current operator need.

# Complexity Traps

Avoid these traps:

1. **SelectionEngine.** Selection already occurs in surface-owned deterministic
   code paths. A new engine would duplicate or override context, state,
   integrity, capability, and explanation ownership.
2. **ReasoningEngine.** Rationale describes why existing surfaces selected or
   excluded known candidates. It is not a new reasoning subsystem.
3. **ContextEngine.** Context composition already has `ContextComposer`,
   `ContextBudget`, ordering helpers, `BudgetTrace`, and `DecisionContextView`.
4. **Planner or WorkflowEngine.** Selection rationale does not plan work,
   schedule actions, or orchestrate execution.
5. **Runtime integration.** Existing rationale signals are read-only over
   projected state and context composition; runtime flow should not change.
6. **ToolExecutor integration.** Capability state, stale refresh recommendations,
   and unsupported evidence explanations must not execute tools.
7. **LLM ranking.** Existing ordering is deterministic and inspectable. LLM
   ranking would add opaque selection behavior.
8. **Truth ranking.** Support, confidence, contradictions, conflicts, and current
   state already define projection-backed belief surfaces. A rationale summary
   must not create another truth system.
9. **Provider ranking.** Capability inventory states verification support; it
   does not select providers.
10. **Execution ranking.** Selection rationale describes selected knowledge, not
    selected actions.
11. **Parallel inventories.** A new rationale inventory would duplicate existing
    capability, evidence, contradiction, confidence, stale, and context summaries.
12. **Parallel read models.** A Selection Rationale read model would risk drift
    from the owning rules unless a concrete need justifies it.
13. **Rationale metadata everywhere.** Blanket metadata would duplicate source
    fields and make rationale stale when ordering or selection rules change.
14. **Explanation metadata everywhere.** Explanations already expose support,
    evidence, conflict, provenance, inference, and alias resolution for queries;
    broad metadata expansion would blur explanation and selection ownership.

# Recommended Outcome

Recommended outcome: **C. Summary not justified**.

Justification:

- Selection rationale information is already present across existing surfaces.
- Most concrete per-item questions are already answerable by the owning surface.
- Existing summary-like surfaces already summarize their own domains:
  `BudgetTrace` for budget passes, `ContextSummary` for decision context,
  confidence/evidence/contradiction summaries for integrity inputs, capability
  inventory for capability verification, and explanations for fact queries.
- The primary remaining gaps are cross-surface aggregate/statistical questions,
  not direct item-level explanation questions.
- Answering those aggregate/statistical questions would require new rationale
  classifications, histories, inventories, or read models, none of which is
  justified by this audit.
- Fragmentation justifies vocabulary and documentation navigation, which now
  exist through the characterization, vocabulary, reconciliation, and this audit.

If future evidence shows operators need cross-run rationale analytics, the next
step should be another documentation-only design that defines the exact question,
source fields, and non-goals before any implementation is considered.

# Non-Goals

This characterization does not:

- implement a Selection Rationale Summary;
- implement a Selection Rationale Inventory, Navigation, Drilldown, Statistics,
  or Classification surface;
- implement runtime behavior;
- add routes, adapters, schema classes, rationale metadata, explanation metadata,
  inventories, read models, engines, event types, provider behavior, execution
  behavior, or LLM ranking;
- mutate projections;
- append events;
- change `Runtime`;
- change `ToolExecutor`;
- change `EventLedger` ownership;
- change `ProjectionStore` ownership;
- change `ContextComposer` behavior;
- change `ContextBudget` behavior;
- change selection ordering;
- change current fact selection;
- change capability inventory behavior;
- change explanation behavior;
- create a parallel truth system.

# Conclusion

A Selection Rationale Summary is understandable as a concept: it would be a
cross-surface report or map that composes why known candidates were selected,
excluded, ordered, made current, or surfaced. It could also become an inventory,
navigation guide, drilldown aid, statistics layer, or classification system.

The audit rejects implementation now. The existing repository already answers
most strong concrete questions through existing rationale surfaces. The remaining
questions are mostly aggregate analytics questions, and those would require new
classification/statistics machinery rather than simple composition. That is too
much complexity without a demonstrated operator need.

Therefore, Selection Rationale Summary should remain documentation-only and
non-implemented. The safe architectural stance is to keep rationale ownership
distributed across existing surfaces, use Selection Rationale vocabulary to name
those surfaces consistently, and avoid new engines, read models, inventories,
routes, metadata, runtime integrations, ToolExecutor integrations, provider
rankings, execution rankings, LLM rankings, projection mutations, event appends,
or parallel truth systems.

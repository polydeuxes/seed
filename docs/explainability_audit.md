# Executive Summary

Seed already has an implicit explainability stack, but it is unevenly surfaced.
The strongest existing path is fact-level explanation over projected state:
`ExplanationBuilder` can answer a read-only `why(subject, predicate)` query by
walking `FactSupport`, facts, evidence IDs, recursive inference source facts,
entity alias resolution, current/competing beliefs, and projected conflicts.
This is deterministic and state-derived; it is not an LLM explanation layer or a
runtime reasoning engine.

Seed can already explain, or partly explain:

- why a projected fact/value is believed, when it has current support;
- which fact IDs, evidence IDs, source types, confidence values, and observation
  timestamps support a current belief;
- which inference rule and source fact produced an inferred fact;
- when a single-cardinality predicate has competing supported values;
- which facts are stale by expiry and which refresh capability is recommended;
- which capability verification inventory entry is `verified`, `unverified`,
  `provider_reported`, `stale`, or `unknown` from projected
  `capability_verified` support;
- which deterministic predicate, relationship, entity-type, inference, graph
  validation, and capability catalog rules exist in the rule inventory;
- graph validation issues with relationship IDs, source fact IDs, type mismatch
  reasons, expected/actual types, and hints.

Seed cannot yet consistently answer every operator-facing `why` question because
several explanations are only raw read-model output rather than a unified
explanation contract. In particular, Seed does not have a first-class
"why stale", "why current", "why this support won", "why not verified", or
"which rule inventory entry caused this exact projection" API. The data often
exists, but the explanation boundary is incomplete.

This audit is documentation-only. It does not add reasoning engines, LLM
reasoning, runtime behavior, execution behavior, orchestration, or projection
semantics.

# Existing Explainability Surfaces

## Explicit explanation module

`seed_runtime/explanations.py` is the clearest existing explanation surface. It
contains `FactExplanation`, `BeliefExplanation`, `Explanation`, and
`ExplanationBuilder`. `ExplanationBuilder.why(subject, predicate)` reads only a
projected `State`, asks the state for fact support, separates current and
competing beliefs, attaches a `FactConflict` when present, and recursively walks
inferred source facts. It also exposes alias/entity resolution paths for fact
subjects.

Current capabilities:

- current belief explanation for a subject/predicate;
- multi-valued predicate explanation that returns all current supported values;
- ambiguous single-valued predicate explanation that returns competing supported
  values and conflict metadata;
- recursive inferred-fact explanation through `source_fact_id` and
  `inference_rule_id`;
- confidence cap visibility for inferred facts whose confidence was capped by a
  source fact;
- evidence IDs, source types, support confidence, observation times, and latest
  observation times.

Current limitations:

- explains by subject/predicate, not by arbitrary fact ID;
- does not expose why a stale or pruned measurement fact stopped being current;
- does not explicitly narrate the support ranking/tie-break rule that made one
  support current;
- exposes `FactConflict.reason`, but does not turn conflict metadata into a full
  contradiction explanation;
- does not join to full `Evidence` payloads unless callers separately use the
  Evidence Graph / `--why-fact` path.

## FactSupport and current-state surfaces

`FactSupport` aggregates claims by subject, predicate, dimensions, and value for
durable predicates; for measurement predicates it marks the support as a
`current_sample`. It records supporting fact IDs, source types, aggregate
confidence, earliest/latest observation time, expiry state, predicate semantics,
and support kind.

`State.get_fact_supports`, `State.get_fact_support`, `State.get_best_fact`, and
`State.get_current_facts` form the current fact read model. For
single-cardinality predicates, `get_current_facts` delegates to `get_best_fact`.
For multi-cardinality predicates, it returns one representative fact for each
current supported value. This is explainability-relevant because the same support
records drive both current facts and `ExplanationBuilder`.

Current limitations:

- support records are projected facts about support, not human explanations;
- current selection is visible in code/tests, but there is no dedicated
  "selection rationale" object;
- `get_current_facts` returns representative facts rather than the whole support
  object, so callers can lose the reason a value is current unless they also ask
  for `FactSupport`.

## Evidence and Evidence Graph

`Evidence` stores source payload provenance: ID, workspace, source, kind,
`observed_at`, payload, and confidence. `seed_runtime/evidence_graph.py` builds a
read-only Evidence Graph from projected `State`; it does not read the ledger,
append events, call providers, execute tools, or persist another evidence store.
It exposes evidence nodes, evidence links, fact evidence views, summaries,
unsupported fact views, and concise generated explanation strings such as
"Seed believes this fact because it is supported by N evidence records".

The CLI formats this through:

- `--evidence-graph` / `format_evidence_graph`;
- `--why-fact` / `format_why_fact`;
- unsupported fact output.

Current limitations:

- Evidence Graph explanations are fact/evidence summaries, not complete current
  belief explanations;
- support/evidence joins are split between `ExplanationBuilder` and Evidence
  Graph helpers;
- missing evidence is reported, but not classified by why it is missing.

## Contradiction and conflict surfaces

Seed has two related surfaces:

1. `FactConflict`, projected in `State.fact_conflicts`, detects multiple current
   values for single-cardinality durable predicates under alias-aware projected
   support. It records subject, predicate, dimensions, values, winning value,
   best fact ID, conflicting fact IDs, and a reason.
2. `seed_runtime/contradictions.py` builds a conservative read-only
   contradiction view over exact subject/predicate facts for exclusive
   predicates. It can attach per-fact evidence through the Evidence Graph and
   computes summaries and fact-specific contradiction lookup.

The CLI formats active fact conflicts, read-only contradictions, graph issues,
and impact output. These are sufficient building blocks for an explanation layer,
but not yet one unified contradiction explanation API.

## Capability verification inventory

`seed_runtime/capability_inventory.py` is explicitly a read-only capability
verification inventory. It interprets already-projected State only; it does not
execute tools, call providers, append events, schedule work, or route through
Runtime behavior.

The inventory universe is the union of:

- registered tool capabilities;
- `ToolNeed.capability` values;
- fact subjects with predicate `capability_verified`.

Each `CapabilityInventoryEntry` contains capability, state, supporting facts,
supporting evidence summaries, support metadata, observation times, age, and a
reason. State is derived from the current or expired `capability_verified`
`FactSupport` value: `verified`, `provider_reported`, `unverified`, `unknown`,
or `stale`.

Current limitations:

- this is an inventory, not a general capability explanation API;
- `unverified` usually means "no `capability_verified` fact is present", not a
  negative verification proof;
- provider recommendations, registered-operation candidates, and catalog-known
  capabilities are resolution metadata, not verification evidence unless a
  separate fact/evidence claim exists.

## Stale fact reporting

`State.get_stale_facts()` returns facts that are expired by `Fact.expires_at`.
`State.get_stale_fact_refresh_recommendations()` maps stale predicates to a
refresh capability and includes a deterministic reason string. The CLI prints
stale fact details and stale refresh recommendations.

Current limitations:

- Seed can report `expired: true` and `expires_at`, but there is no dedicated
  `why_stale(fact_id)` helper;
- measurement facts can disappear from projected state because measurement
  history is retained by limit; that is temporal current-sample behavior, not
  stale-fact expiry, and lacks a user-facing explanation surface;
- there is no as-of projection API for explaining what was current at a previous
  event or timestamp.

## Impact output

`format_entity_impact` summarizes an entity using projected state only:
canonical entity, entity types, aliases, availability, local observation status,
local network configuration, endpoint availability by role, group membership,
dependencies, dependents, active conflicts, and graph issues.

This is an explainability surface because it puts together current facts,
relationships, conflicts, and graph validation issues. However, it is an impact
view rather than a provenance explanation. It generally does not include
supporting fact IDs or evidence IDs except through embedded conflict/graph issue
metadata.

## Rule inventory

`RuleInventoryBuilder` collects existing deterministic metadata into stable
`RuleInventoryEntry` records. It includes predicate catalog entries, predicate
mappings, relationship entries, entity type entries, inference entries, graph
validation entries, and capability resolution entries. It explicitly does not
execute tools, append events, project state, inspect live hosts, or introduce a
rule engine.

The rule inventory can answer "what rules exist?" and "what rule-like catalog
entry says this predicate/relationship/inference exists?". It cannot yet answer
"which exact inventory entry was applied to this exact projected artifact?"
except where artifacts already carry a direct source such as
`inference_rule_id`, `source_fact_id`, or relationship catalog metadata.

## Current facts and state projection

`--current-facts` prints the current value(s) for a subject/predicate through
`State.get_current_facts`. State projection also materializes facts, observed and
inferred facts, relationships, aliases, entity type assertions, graph issues,
FactSupport, FactConflict, evidence, observations, tool needs, and tools.

This means current state is explainability-ready, but not all projected indexes
have operator-facing explanation helpers.

# Fact Explanations

## Can Seed explain why fact X exists?

Partially.

If the question is framed as "why does Seed currently believe subject/predicate
value?", yes: `ExplanationBuilder.why()` can return current or competing beliefs
with supporting fact IDs, evidence IDs, source types, support confidence, and
observation timestamps. `--why-fact` can also show Evidence Graph details for a
matching fact query.

If the question is framed as "why does fact ID X exist in State?", not fully.
The pieces are present (`Fact.evidence_ids`, `Fact.source_type`,
`Fact.source_fact_id`, `Fact.inference_rule_id`, Evidence Graph views), but there
is no dedicated fact-ID explanation helper that reconstructs the event/projection
path for any arbitrary fact ID.

Missing pieces:

- fact-ID-oriented explanation helper;
- a single response that joins `Fact`, `FactSupport`, full `Evidence` payload
  summaries, source event IDs, and inference chain;
- explicit distinction between "fact exists in projected State" and "fact is
  current".

## Can Seed explain why fact X is current?

Partially.

Seed has the core data: `FactSupport` says whether support is durable aggregate
or current measurement sample, current queries exclude expired facts by default,
and current selection uses support ranking. `ExplanationBuilder` returns the
current belief and its support metadata.

What is missing is an explicit current-selection rationale. The system does not
currently emit a structured explanation like:

- predicate is single-cardinality or multi-cardinality;
- expired facts were excluded;
- durable support won by aggregate confidence/support count;
- measurement support won because it was the latest sample by `observed_at` and
  fact ID;
- tie produced ambiguity rather than a winner.

## Can Seed explain why fact X won over competing facts?

Partially.

For durable single-cardinality conflicts, `FactConflict` records values,
`winning_value`, `best_fact_id`, and `conflicting_fact_ids`. `ExplanationBuilder`
returns current and competing beliefs when a winner exists, or marks the query
ambiguous when no unambiguous best support exists.

Missing pieces:

- a direct "winner rationale" that names the rank/tie-break inputs;
- evidence comparison for each side in the same explanation response;
- explicit reporting when there was no winner because supports tied.

## Can Seed explain why fact X became stale?

Partially.

Seed can report that a fact is stale because `Fact.expires_at` has passed, and it
can recommend a refresh capability for the stale predicate. It cannot yet provide
a dedicated stale explanation object. Measurement replacement is also not the
same as staleness: older measurement samples may be pruned from projected state
by measurement history limit without becoming stale facts.

Missing pieces:

- `why_stale(fact_id)` or equivalent read-only helper;
- explicit distinction among expired, excluded-from-current, measurement-pruned,
  and superseded-by-better-support;
- as-of/timeline support if the operator asks when it became stale.

# Contradiction Explanations

## Can Seed explain why these facts conflict?

Mostly for simple/current cases.

`FactConflict` explains conflicts as multiple values for the same
subject/predicate/dimensions under a single-cardinality predicate. The read-only
contradiction detector explains exact-subject exclusive predicate conflicts with
severity and the reason "exclusive predicate has multiple values". Graph issues
explain relationship/type conflicts with expected and actual types plus source
fact IDs.

Limitations:

- `FactConflict` and `Contradiction` are separate surfaces with different
  grouping rules;
- contradiction severity/reason is intentionally coarse in v1;
- there is no unified `explain_conflict(conflict_id)` contract.

## What evidence supports each side?

The Evidence Graph and contradiction detector can attach evidence per
conflicting fact. CLI contradiction output includes the fact IDs and compact
evidence references for each side when evidence is available. `ExplanationBuilder`
can expose evidence IDs for current and competing beliefs.

Limitations:

- `FactConflict` itself does not carry evidence-by-side;
- callers must join through Evidence Graph or use CLI output;
- full evidence payloads remain separate from the conflict object.

## Which side is projected as current?

For `FactConflict`, yes when projection has an unambiguous best fact: it records
`winning_value` and `best_fact_id`. When support ties, current belief can be
ambiguous and there is no winning side.

For the generic contradiction detector, not by itself. It reports contradictions
conservatively and does not arbitrate truth. A caller can separately ask State for
current support or ExplanationBuilder for current/competing beliefs.

## Is conflict reporting sufficient for an explanation layer?

It is sufficient as a building block, not as a complete explanation layer.
Existing conflict reporting has the essential facts, values, reasons, winning
metadata, and evidence joins, but it lacks a stable operator-facing explanation
shape that combines current support, each side's evidence, selection/tie logic,
and graph issue context.

# Capability Explanations

## Can Seed explain why capability X is verified?

Yes, if verification is represented as current `capability_verified` support.
`CapabilityInventoryEntry` exposes the derived state, supporting fact IDs,
supporting evidence summaries, support value, confidence, source types,
observed/latest observed timestamps, expiry metadata, age, and reason. A
`verified` state comes from a current support value normalized to one of the
verified values.

## Can Seed explain why capability X is unverified?

Partially.

The inventory can say `unverified` because no `capability_verified` fact is
present in projected State. It can also derive `unverified` from a current support
value such as `false`, `no`, or `unverified`. These are useful but not yet a full
why-not capability explanation. It does not prove absence of capability, inspect
providers, execute verifiers, or explain missing evidence beyond the absence of a
verification fact.

## Can Seed explain why capability X is provider_reported?

Yes, if a current `capability_verified` support value normalizes to
`provider_reported` / `provider-reported`. The entry can include supporting facts
and evidence summaries. This means Seed can distinguish provider-reported status
from verified status, provided the fact/evidence was modeled that way.

## Can Seed explain why capability X appears in capability resolution?

Partially.

Capability resolution metadata in `ToolNeedService.resolve_capability()` explains
why a capability appears downstream of a `ToolNeed`: a requested capability is
looked up in `CapabilityCatalog`, visible registry operations are listed by
capability, provider recommendations are passed through, and catalog handoff
candidates are surfaced. The `ToolNeed` itself records capability, summary,
reason, requested-by event ID, risk hint, desired inputs, and desired outputs.

However, capability resolution is not verification. A capability can appear
because it is requested, catalog-known, registered as an operation candidate, or
recommended by a provider/catalog; none of those imply current availability or
verified status.

## What evidence is already available?

- `capability_verified` facts and their `FactSupport` records;
- `Evidence` / Evidence Graph nodes attached to those facts;
- `ToolNeed` event/projection metadata;
- `ToolSpec` registry metadata for registered operation candidates;
- `CapabilityCatalogEntry` and recommendation metadata;
- provider recommendation reason lists passed into capability resolution.

# Temporal Explanations

## Can Seed explain why fact X is stale?

Partially.

Stale fact reporting exposes `expired: true` and `expires_at`; stale refresh
recommendations expose the predicate-to-refresh-capability mapping reason. This
is enough to explain expiry-based staleness, but the answer is split across raw
stale fact output and refresh recommendation output.

Missing:

- a single stale explanation helper;
- explicit "current time vs expires_at" comparison in output;
- distinction between expired facts and other ways facts stop being current.

## Can Seed explain why fact X is current?

Partially.

Current fact selection is deterministic and characterized by tests/docs.
Durable facts use support aggregation and single/multi predicate cardinality;
measurement predicates keep latest-current sample semantics; expired facts are
excluded by default. `ExplanationBuilder` exposes the current belief and support.

Missing:

- structured current-selection rationale;
- direct reference to predicate catalog semantics in the explanation;
- explicit reporting of excluded expired or non-winning supports.

## Can Seed explain why fact X replaced another fact?

Not directly.

Seed can show current support and competing support. For measurement predicates,
newer samples replace older current samples by latest measurement semantics. For
durable single-cardinality predicates, stronger support can win over competing
support without deleting older facts. But there is no "replacement" concept in
projected state for durable facts, and no what-changed/as-of explanation helper.

## Can Seed explain why a measurement is no longer current?

Partially from docs/tests, not from a direct user-facing helper.

`FactSupport` marks measurements as `predicate_semantics="measurement"` and
`support_kind="current_sample"`; projection retains latest samples per resolved
subject/predicate/dimensions up to `measurement_history_limit`. Current behavior
is deterministic, but Seed does not yet expose a measurement-specific explanation
that says an older sample is no longer current because a newer sample exists or
because it was pruned from projected history.

# Rule Explanations

## Can Seed explain which rule caused this conclusion?

For inferred facts, yes: `Fact.inference_rule_id` and `source_fact_id` are
preserved, and `ExplanationBuilder` recursively exposes them. `--inferred-facts`
also prints the source fact ID and inference rule ID for inferred facts.

For catalog-derived relationships/entity type assertions/graph validations,
partially: projected artifacts carry source fact IDs, source relationship IDs,
relationship IDs, and reasons, while Rule Inventory lists the static catalog or
validation entries. There is not yet a general artifact-to-rule-inventory lookup.

## Can Seed explain which predicate semantics apply?

Partially.

Predicate semantics live in `PredicateCatalog` and are reflected in
`FactSupport.predicate_semantics`, `support_kind`, and current selection behavior.
Rule Inventory can list predicate kind, value type, cardinality, and allowed
values. Explanations do not yet always include the predicate catalog entry that
controlled the behavior.

## Can Seed explain which inventory entry supports this projection?

Partially.

Rule Inventory has stable entries with IDs and sources. Some projected artifacts
carry enough data to infer the relevant inventory entry:

- predicate facts map to `predicate.<predicate>`;
- inferred facts map to inference rule IDs;
- relationships can map through relationship catalog definitions and source fact
  predicates;
- graph issues map to graph validation inventory entries;
- capability resolution maps to capability catalog / registry / recommendation
  entries.

Missing is a read-only resolver that takes a projected artifact and returns the
matching inventory entry IDs without changing projection behavior.


# Existing Architecture Fit

The architecture path `Observation -> Evidence -> Fact -> FactSupport ->
Projection -> Explanation` already exists implicitly, but it is not yet a single
formal explanation layer.

## Already implemented

- `Observation`, `Evidence`, and `Fact` models preserve observed source payloads,
  provenance links, source type, confidence, observation time, and optional
  expiry.
- `FactSupport` projects aggregate durable support and current measurement
  samples from facts.
- `StateProjector` produces projected `State` indexes including facts, support,
  conflicts, relationships, aliases, entity types, graph issues, evidence,
  observations, tool needs, and tools.
- `ExplanationBuilder` composes current and competing belief explanations from
  projected support, facts, inference metadata, alias resolution, evidence IDs,
  and conflict metadata.
- Evidence Graph, Contradictions, Capability Inventory, Rule Inventory, stale fact
  reporting, impact output, graph issue output, and current-facts output provide
  additional read-only explainability surfaces.

## Partially implemented

- Fact explanations exist for subject/predicate beliefs and fact/evidence views,
  but not arbitrary fact IDs through one helper.
- Contradiction explanations expose values, fact IDs, reasons, severity, and
  evidence joins, but are split across `FactConflict`, generic contradictions,
  and graph issues.
- Capability explanations exist as inventory entries, but capability resolution
  and capability verification are separate read models that are not composed into
  one answer.
- Temporal explanations expose expiry and current support metadata, but do not
  provide stale/current/replacement explanation helpers.
- Rule explanations expose inference rule IDs and static inventory entries, but
  do not consistently map every projected artifact back to inventory entry IDs.

## Missing

- A unified, read-only explanation contract across fact, contradiction,
  capability, temporal, and rule questions.
- Selection-rationale metadata for current support winners, ties, expiry
  exclusions, and measurement latest-current behavior.
- A read-only artifact-to-rule-inventory mapping helper.
- A joined explanation view that combines `ExplanationBuilder` support chains with
  Evidence Graph payload summaries and stale/capability/conflict metadata.

# Existing Building Blocks

Reusable components already present:

- `Fact`: subject, predicate, value, dimensions, evidence IDs, source type,
  confidence, observed time, optional expiry, inference metadata.
- `FactSupport`: support grouping, supporting fact IDs, source types, aggregate
  confidence, observed/latest observed timestamps, expiry, predicate semantics,
  support kind.
- `Evidence`: source payload provenance with confidence and observed time.
- Evidence Graph: read-only evidence nodes, links, fact views, unsupported fact
  views, evidence summaries, and concise fact/evidence explanations.
- `ExplanationBuilder`: deterministic projected-state why explanations for
  subject/predicate current and competing beliefs.
- `FactConflict`: current projected support conflicts with winning/best and
  conflicting fact IDs.
- Contradiction detector: conservative read-only exact-subject exclusive
  predicate contradiction reporting with optional Evidence Graph attachments.
- `GraphValidationIssue`: graph/type issue reason, source facts, relationship
  IDs, expected/actual types, severity, and hints.
- Capability Inventory: read-only capability verification entries with support,
  evidence, reason, age, and stale/unverified/provider-reported/verified states.
- `ToolNeed` and capability resolution metadata: requested capability, reason,
  registered operation candidates, provider recommendation reasons, handoff
  candidates, and catalog-known status.
- Temporal metadata: event timestamps, observation/evidence/fact observed times,
  fact expiry, FactSupport first/latest observed times, stale fact views, and
  stale refresh recommendations.
- Predicate Catalog: predicate kind, value type, cardinality, allowed values,
  measurement classification, and mappings.
- Inference Catalog: deterministic inference rules with IDs, conditions,
  effects, confidence, and reason.
- Relationship Catalog: relationship definitions, kinds, expected subject/object
  types, derived predicates.
- Entity Type Catalog and entity type assertions: current entity type support and
  assertion provenance.
- Rule Inventory: source-attributed catalog and deterministic rule metadata.
- CLI formatters: `--why`, `--why-fact`, `--current-facts`, `--fact-conflicts`,
  `--contradictions`, `--graph-issues`, `--impact`, `--stale-facts`,
  `--stale-fact-refresh-recommendations`, `--capability-inventory`, and
  `--explain-rules`.

# Missing Concepts

These are conceptual/documentation/API gaps, not recommendations for new runtime
behavior:

1. **Unified explanation contract.** Existing surfaces are separate read models.
   There is no single stable response shape for fact, contradiction, capability,
   temporal, and rule explanations.
2. **Fact-ID explanation.** Seed can explain subject/predicate beliefs and
   fact/evidence views, but not arbitrary fact IDs through one helper.
3. **Current-selection rationale.** Support ranking, predicate cardinality,
   expiry filtering, measurement latest-sample logic, and tie/ambiguity behavior
   are not emitted as structured explanation metadata.
4. **Stale explanation.** Stale facts and refresh recommendations exist, but
   there is no `why_stale` helper that joins fact, expiry, current time,
   excluded support, and refresh reason.
5. **Replacement / what-changed explanation.** Seed lacks as-of projection and
   cannot directly explain when or why a belief changed across historical time.
6. **Measurement no-longer-current explanation.** Current-sample semantics are
   characterized, but older measurement samples do not have a user-facing
   explanation path.
7. **Conflict explanation unification.** `FactConflict`, generic
   contradictions, and graph issues are separate. They should remain separate
   building blocks, but a read-only explanation helper could compose them.
8. **Capability why-not explanation.** Inventory can report `unverified`, but
   missing verification evidence, catalog-known status, registered candidates,
   and provider recommendations are not presented as one why-not answer.
9. **Artifact-to-rule inventory mapping.** Rule Inventory lists static rules;
   projected artifacts do not consistently link to inventory entry IDs.
10. **Evidence payload join in explanations.** `ExplanationBuilder` exposes
    evidence IDs; Evidence Graph exposes evidence summaries. A single read-only
    join would improve operator answers without changing projection.

# Recommended Smallest Next Step

The smallest safe next step is **documentation plus characterization tests for a
read-only explanation inventory contract**.

Specifically:

1. Document a small set of explanation question types that Seed should support
   using existing read models only:
   - `why_current(subject, predicate)`;
   - `why_fact(fact_id)`;
   - `why_stale(fact_id)`;
   - `why_conflict(subject, predicate)`;
   - `why_capability(capability)`;
   - `which_rules(projected_artifact)`.
2. For each question type, inventory which existing fields must be returned and
   which existing helper supplies them (`FactSupport`, Evidence Graph,
   `FactConflict`, Capability Inventory, Rule Inventory, temporal metadata).
3. Add characterization tests around the existing helpers and CLI output so that
   future read-only explanation helpers cannot accidentally add runtime,
   execution, or projection behavior.
4. Only after that documentation/test pass, consider tiny read-only composition
   helpers that join existing read models. Those helpers should not create new
   facts, mutate State, execute tools, call providers, invoke LLMs, or change
   projection semantics.

Do not start with a reasoning engine, truth-maintenance system, runtime hook,
automatic verification, orchestration, or LLM-generated explanations. The
building blocks already exist; the immediate risk is inconsistent composition and
terminology, not lack of a reasoner.

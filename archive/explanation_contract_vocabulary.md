# Executive Summary

Seed already has explanation-producing structures. The missing piece is a stable
vocabulary for describing those structures consistently.

Explanation Contract Vocabulary v1 defines documentation-only language for
read-only, projection-backed, evidence-backed, and inventory-backed
explanations. It names how existing Seed concepts such as `ExplanationBuilder`,
`FactSupport`, `Evidence`, `FactConflict`, `Contradiction`,
`CapabilityInventoryEntry`, `RuleInventoryEntry`, temporal metadata, graph
issues, and current-state views relate to a common explanation shape.

This document does not implement an explanation contract. It does not add
adapters, runtime behavior, tool execution behavior, provider calls, LLM
reasoning, schema classes, explanation models, projection changes, inventories,
or an explanation engine. It is vocabulary only.

# Purpose

The purpose of this document is to define the canonical language Seed uses when
discussing explanations.

This document serves the same kind of stabilizing role for explainability that
capability verification vocabulary, availability vocabulary, and capability
extension methodology documents serve for their domains: it names concepts and
boundaries so future work can refer to them without implying new behavior.

The vocabulary is intended to:

- describe existing explanation-producing surfaces consistently;
- distinguish explanation from truth selection, verification, and execution;
- preserve existing ownership boundaries for facts, evidence, projections,
  contradictions, capabilities, rules, temporal metadata, Runtime, and
  ToolExecutor;
- provide a common read-only field shape for documentation and future
  characterization work;
- keep surface-specific details in clearly labeled `extensions` rather than
  flattening them into a parallel truth system.

# What Is An Explanation

An **explanation** is a read-only description of a claim using Seed's existing
projected facts, support records, evidence, conflicts, inventories, rules,
temporal metadata, and provenance.

In Seed terms, an explanation describes:

- a claim;
- the subject the claim is about;
- why the claim exists in the current read model;
- supporting facts;
- supporting evidence;
- competing facts or values;
- conflicts and contradictions;
- relevant deterministic rules or catalog metadata;
- temporal context such as observation time, latest observation time, expiry,
  age, staleness, or current-sample semantics;
- provenance such as evidence source, source type, source fact, inference rule,
  supporting event IDs, and provider/import/discovery context;
- notes that make limitations explicit.

An explanation does not determine truth. Seed's projected state and support
selection semantics determine current beliefs. An explanation may report those
semantics, but it must not select differently.

An explanation does not execute tools, call providers, verify capabilities,
route Runtime behavior, invoke ToolExecutor behavior, call an LLM for reasoning,
append events, mutate projections, select beliefs, resolve contradictions, or
create a second source of truth.

# Canonical Vocabulary

## Explanation

An **Explanation** is a read-only account of a claim assembled from existing
Seed structures. It may be a fact explanation, capability explanation,
contradiction explanation, rule explanation, temporal explanation, graph
explanation, current-state explanation, or another documented category.

An Explanation is not an engine, runtime path, execution hook, verifier,
orchestrator, schema implementation, or persistence store.

## Claim

A **Claim** is the proposition being explained.

For facts, the claim is usually the subject/predicate/value represented by a
`Fact` or `FactSupport`. For capabilities, the claim is a capability verification
or inventory state such as `verified`, `provider_reported`, `unverified`,
`stale`, or `unknown`. For contradictions, the claim is that incompatible values
exist for a subject and predicate. For rules, the claim is that a deterministic
catalog or validation rule exists and has documented conditions and effects.

A Claim is not proof by itself. It must be interpreted through support,
evidence, temporal context, and provenance.

## Subject

A **Subject** is the entity, fact, capability, rule, graph relationship, or
state-view item the claim is about.

Examples include a fact subject ID, a query subject passed to
`ExplanationBuilder.why(subject, predicate)`, a capability name in
`CapabilityInventoryEntry`, a contradiction subject, a rule inventory entry ID,
or a graph relationship/source fact referenced by graph validation output.

## Status

A **Status** is the read-only classification attached to an explanation.

Status vocabularies are category-specific. Examples include:

- fact explanation status: `current`, `ambiguous`, `no_current_belief`;
- capability verification state: `verified`, `provider_reported`, `unverified`,
  `stale`, `unknown`;
- contradiction severity/status: high/medium/low severity plus a reason;
- temporal status: current, expired, stale, current sample, or not current when
  existing temporal metadata supports that statement.

A Status reports existing read-model state. It does not cause the state.

## Supporting Fact

A **Supporting Fact** is a projected `Fact` or fact ID that contributes to the
claim being explained.

Supporting facts are normally exposed through `FactSupport.supporting_fact_ids`,
`BeliefExplanation.supporting_fact_ids`, capability inventory supporting facts,
contradiction fact IDs, graph issue source fact IDs, or stale fact outputs.

Supporting facts remain owned by state projection. Explanation vocabulary must
not duplicate or rewrite fact truth.

## Supporting Evidence

**Supporting Evidence** is an `Evidence` record, evidence ID, evidence graph
node, fact evidence view, or compact evidence summary that supports a fact or
claim.

Supporting evidence may include source, kind, observed time, payload summary,
confidence, supporting event IDs, or evidence-by-side for contradictions.

Supporting evidence remains provenance data. It does not execute a check, call a
provider, or verify a claim by itself.

## Competing Fact

A **Competing Fact** is a projected fact, support record, or supported value that
asserts a different value for the same or comparable subject/predicate scope.

In `ExplanationBuilder`, competing beliefs are supported values other than the
current best value for a single-cardinality predicate. In contradiction views,
competing facts are the fact IDs grouped on opposite sides of an exclusive
predicate disagreement. In graph validation, competing or incompatible facts may
be reflected as type or relationship issues.

A competing fact is not automatically false. Seed may have current support,
ambiguity, stale support, or conflict metadata explaining how the competing fact
is represented.

## Conflict

A **Conflict** is a read-only representation that two or more claims are in
tension.

Current Seed conflict structures include `FactConflict` for disagreements among
fact supports, `Contradiction` for conservative exact-subject exclusive-predicate
contradictions, and `GraphValidationIssue` for relationship/type mismatches.

`FactConflict` belongs to projected State and groups disagreements by
alias-canonical subject, predicate, and dimensions for non-expired,
non-measurement, non-multi-cardinality facts. `Contradiction` belongs to the
standalone read-only contradiction detector and groups exact subject/predicate
exclusive-predicate disagreements. `GraphValidationIssue` belongs to graph
validation and reports relationship/type issues without repairing projected
edges.

A Conflict describes disagreement. It does not resolve the disagreement unless
existing projected support has already selected a current value and exposes that
selection. Conflict explanations may report attached conflicts, competing
beliefs, severity, reasons, evidence, and confidence-view penalties, but they
must not create a hidden lifecycle such as disputed/superseded facts or change
core confidence.

## Rule

A **Rule** is deterministic catalog, validation, mapping, inference, or
capability-resolution metadata that explains how Seed classifies or derives
something.

Canonical rule vocabulary maps to `RuleInventoryEntry`, predicate catalog
entries, predicate mappings, relationship catalog entries, entity type catalog
entries, inference catalog entries, graph validation entries, and capability
resolution inventory entries.

A Rule explanation documents existing metadata. It must not introduce a rule
engine or execute rule behavior.

## Temporal Metadata

**Temporal Metadata** is time-related context attached to facts, support,
evidence, capabilities, measurements, stale facts, or state views.

Examples include `observed_at`, `latest_observed_at`, `expires_at`, `expired`,
`age_seconds`, measurement `current_sample` support, stale fact data, refresh
recommendation context, last event ID, and projection version.

Temporal metadata may explain freshness, expiry, staleness, age, or why a
measurement is current. It does not create as-of history or timeline behavior
unless such behavior exists elsewhere.

## Provenance

**Provenance** is the origin and derivation context for a claim.

Examples include `Evidence.source`, `Evidence.kind`, evidence IDs, source types,
supporting event IDs, `source_fact_id`, `inference_rule_id`, provider/import or
discovery source type, evidence graph links, and capability evidence summaries.

Provenance is evidence lineage. It is not LLM-generated rationale and must not be
invented.

## Note

A **Note** is explanatory text that states limitations, caveats, boundary
conditions, or operator-facing context without adding new truth.

Notes may say that a why-not answer is missing, that selection rationale is only
partial, that replacement rationale is distinct from explanation, or that stale
rationale is represented through existing temporal metadata.

## Extension

An **Extension** is a namespaced place for category-specific fields that do not
belong in the common vocabulary.

Examples include recursive source-fact explanation details, capability evidence
summary fields, contradiction severity fields, graph issue hints,
measurement-specific metadata, or inventory category metadata.

Extensions must preserve ownership. They must not become a hidden parallel
schema, engine, verifier, or truth store.

# Explanation Categories

## Fact Explanation

A **Fact Explanation** explains a projected fact, current belief, ambiguous
belief, or absence of current belief for a subject and predicate.

Primary existing structures include `ExplanationBuilder`, `Explanation`,
`BeliefExplanation`, `FactExplanation`, `FactSupport`, `Fact`, and supporting
`Evidence` IDs. Fact explanations focus on facts, support confidence, evidence
IDs, source types, observation timestamps, recursive inferred source facts,
inference rule IDs, confidence caps, current beliefs, competing beliefs, and
fact conflicts.

Fact explanations differ from capability explanations because their subject is a
fact or subject/predicate query rather than a capability verification target.
They differ from rule explanations because they report data and support rather
than merely catalog metadata.

## Capability Explanation

A **Capability Explanation** explains the read-only inventory state for a
capability.

Primary existing structures include `CapabilityInventoryEntry`,
`CapabilitySupportSummary`, `CapabilityEvidenceSummary`, the
`capability_verified` predicate, `FactSupport`, `Fact`, and `Evidence`.
Capability explanations may report states such as `verified`,
`provider_reported`, `unverified`, `stale`, or `unknown`, along with supporting
facts, supporting evidence, support confidence, age, expiry, and a reason string.

Capability explanations differ from execution and verification. They report what
already exists in projected state and inventory. They do not run verifiers,
contact providers, inspect hosts, or prove availability.

## Contradiction Explanation

A **Contradiction Explanation** explains disagreement among projected facts or
relationships.

Primary existing structures include `FactConflict`, `Contradiction`,
`ContradictionSummary`, Evidence Graph fact evidence views, and graph validation
issues. Contradiction explanations may report subject, predicate, values, fact
IDs, severity, reason, evidence by fact ID, supporting event IDs, winning value
when existing support selected one, best fact ID, and conflicting fact IDs.

Contradiction explanations differ from fact explanations because the focus is the
relationship among incompatible claims. They do not resolve truth beyond what
existing projection support already reports.

## Rule Explanation

A **Rule Explanation** explains deterministic rule-like metadata.

Primary existing structures include `RuleInventoryEntry` and the catalogs or
static validation metadata it summarizes. Rule explanations may report an ID,
category, source, summary, `if_conditions`, `then_effects`, and metadata.

Rule explanations differ from fact explanations because they explain rule
availability and meaning, not a specific current projected belief. They must not
become a rule engine.

## Temporal Explanation

A **Temporal Explanation** explains freshness, observation timing, expiry,
staleness, current-sample behavior, or age.

Primary existing structures include `Fact.observed_at`, `Fact.expires_at`,
`FactSupport.observed_at`, `FactSupport.latest_observed_at`,
`FactSupport.expired`, `FactSupport.expires_at`, capability inventory
`age_seconds`, stale fact outputs, stale fact refresh recommendations,
measurement support semantics, last event ID, and projection version.

Temporal explanations differ from replacement rationale. Temporal metadata can
show expiry or current measurement semantics, but Seed does not currently expose
a general what-changed/as-of replacement explanation.

## Graph Explanation

A **Graph Explanation** explains relationship projection, evidence links, or
validation issues in graph-shaped read models.

Primary existing structures include the Evidence Graph, fact evidence views,
graph validation issues, relationship catalog metadata, source fact IDs,
expected/actual type data, issue reasons, and hints.

Graph explanations differ from contradiction explanations because they often
focus on graph validity, provenance links, or relationship/type expectations
rather than exclusive-predicate factual disagreement.

## Current-State Explanation

A **Current-State Explanation** explains what the current projected state reports
for summaries, views, current facts, requirements, capabilities, issues, stale
facts, or impact/unhealthy views.

Primary existing structures include State current fact/support methods, State
Views, stale fact reporting, capability inventory, contradiction summaries, graph
issues, last event ID, and projection version.

Current-state explanations differ from fact explanations because they may
summarize a broader read view. They remain projection-backed and must not gather
new observations.

# Explanation Boundaries

Explainability is:

- **Read-only**: it interprets existing facts, support, evidence, conflicts,
  inventories, catalogs, graph issues, stale outputs, and state views.
- **Projection-backed**: current belief/status answers come from projected
  `State`, `FactSupport`, `FactConflict`, graph issues, and state views.
- **Evidence-backed**: provenance and support details reuse `Evidence` and the
  Evidence Graph.
- **Inventory-backed**: capability and rule explanations reuse Capability
  Inventory and Rule Inventory.

Explainability is not:

- execution;
- verification;
- Runtime routing;
- ToolExecutor behavior;
- provider interaction;
- LLM reasoning;
- orchestration;
- projection mutation;
- event appending;
- truth selection;
- contradiction resolution;
- schema implementation;
- an explanation engine;
- a parallel truth system.

# Relationship To Existing Structures

The vocabulary maps to existing repository concepts as follows:

| Vocabulary term | Existing Seed structures | Notes |
| --- | --- | --- |
| Explanation | `ExplanationBuilder` outputs; Evidence Graph summaries; Capability Inventory entries; Rule Inventory entries; contradiction and graph issue outputs; state views | Common language only; no new runtime contract is implemented here. |
| Claim | `Fact` subject/predicate/value; `FactSupport` subject/predicate/value; capability inventory state; contradiction assertion; rule inventory entry summary | A claim is what is being explained, not proof by itself. |
| Subject | `Explanation.query_subject`; `Fact.subject_id`; `FactSupport.subject`; `CapabilityInventoryEntry.capability`; `Contradiction.subject`; `RuleInventoryEntry.id`; graph issue relationship/fact references | Subject meaning is category-specific. |
| Status | `Explanation.status`; `CapabilityInventoryEntry.state`; contradiction severity/reason; stale/expired/current-sample temporal metadata | Status reports existing read-model classification. |
| Supporting Fact | `Fact`; `FactSupport.supporting_fact_ids`; `BeliefExplanation.supporting_fact_ids`; `CapabilityInventoryEntry.supporting_facts`; `Contradiction.fact_ids`; graph issue source fact IDs | Facts remain owned by projection. |
| Supporting Evidence | `Evidence`; evidence IDs on `Fact`/`FactExplanation`/`BeliefExplanation`; Evidence Graph nodes and fact evidence views; `CapabilityEvidenceSummary`; contradiction `evidence_by_fact_id` | Evidence remains provenance-backed. |
| Competing Fact | `Explanation.competing_beliefs`; `FactConflict.conflicting_fact_ids`; `Contradiction.fact_ids` grouped by value; graph validation incompatibilities | Competing does not mean false. |
| Conflict | `FactConflict`; `Contradiction`; graph validation issue | Conflict describes disagreement and may include an existing winning value only when projection already exposed one. |
| Rule | `RuleInventoryEntry`; predicate catalog; predicate mapping catalog; relationship catalog; entity type catalog; inference catalog; graph validation inventory entries; capability resolution entries | Rule Inventory is descriptive, not executable. |
| Temporal Metadata | `observed_at`; `latest_observed_at`; `expires_at`; `expired`; `age_seconds`; measurement `current_sample`; stale fact data; refresh recommendations; last event ID; projection version | Existing temporal metadata supports partial stale rationale. |
| Provenance | `Evidence.source`; `Evidence.kind`; evidence IDs; source types; `source_fact_id`; `inference_rule_id`; supporting event IDs; Evidence Graph links | Provenance must be source-derived, not invented. |
| Note | Existing reason strings, limitations, audit notes, stale/capability reasons, contradiction reasons, graph hints | Notes clarify without adding truth. |
| Extension | Recursive fact explanation details; capability support/evidence summaries; contradiction severity fields; graph issue metadata; rule metadata | Surface-specific fields should remain namespaced. |

Additional relationship mappings:

- `Explanation` maps most directly to `ExplanationBuilder.why(...)` output for
  fact and belief queries.
- `Supporting Fact` maps to `FactSupport` aggregation and to the `Fact` records
  named by supporting fact IDs.
- `Supporting Evidence` maps to `Evidence` and Evidence Graph outputs.
- `Conflict` maps to both `FactConflict` and `Contradiction`; the terms overlap
  but are not identical because they have different grouping and projection
  surfaces.
- `Rule` maps to `RuleInventoryEntry` rather than to a runtime rule engine.
- `Temporal Metadata` maps to stale metadata, expiry timestamps, observation
  timestamps, current-sample support, and capability inventory age.
- `Provenance` maps to evidence provenance and source/inference lineage.
- `Capability Explanation` maps to Capability Inventory entries and their
  supporting facts/evidence.

# Proposed Vocabulary Shape

The following shape is a vocabulary shape only:

```text
Explanation
  subject
  claim
  status
  supporting_facts
  supporting_evidence
  competing_facts
  conflicts
  rules
  temporal_metadata
  provenance
  notes
  extensions
```

Field meanings:

- `subject`: the entity, fact, capability, rule, graph item, or state-view item
  being explained.
- `claim`: the proposition being explained.
- `status`: the category-specific read-only classification.
- `supporting_facts`: projected facts or fact IDs that support the claim.
- `supporting_evidence`: evidence records, evidence IDs, evidence summaries, or
  evidence graph views that support the claim.
- `competing_facts`: facts, support records, or values that assert a competing
  claim.
- `conflicts`: conflict, contradiction, or graph issue data already present in
  projected/read-only structures.
- `rules`: deterministic catalog, mapping, inference, validation, or inventory
  metadata relevant to the claim.
- `temporal_metadata`: observation, latest observation, expiry, stale, age,
  current-sample, event-boundary, or projection-version metadata.
- `provenance`: source, kind, evidence lineage, source fact, inference rule,
  event, provider/import/discovery, or graph link metadata.
- `notes`: limitations, caveats, reasons, or operator-facing clarifications that
  do not add truth.
- `extensions`: category-specific fields retained under their existing owners.

This is not an implementation. It is not a runtime contract. It is not a schema
class. It is not a model definition. It is not an adapter requirement. It does
not require any caller or module to emit this object today.

# Why-Not Explanations

Status: **missing** as a general explanation category, with narrow partial data
available in specific read models.

Why-not explanations answer questions such as "why is this not verified?" or
"why is there no current belief?" Seed currently exposes some relevant facts:

- `Explanation.status = no_current_belief` can report that no current
  subject/predicate belief exists for a fact query.
- Capability Inventory can report `unverified` with a reason such as absence of
  a `capability_verified` fact.
- Evidence Graph and unsupported fact outputs can show missing or absent support
  in limited contexts.

Seed does not currently implement a general why-not explanation contract. A
why-not explanation must not silently execute tools, call providers, inspect the
host, check the network, verify a capability, invoke Runtime, invoke
ToolExecutor, or ask an LLM to infer missing causes.

# Selection Rationale

Status: **partial**.

Selection rationale is distinct from explanation. A fact explanation can show
the current belief, support confidence, supporting facts, evidence IDs, source
types, competing beliefs, and conflict metadata. It does not necessarily explain
each ranking or tie-break input that led one support to become current.

Existing partial data includes:

- `FactSupport` records for supported values;
- support confidence and source types;
- observation and latest observation timestamps;
- predicate cardinality and semantics from predicate metadata;
- `FactConflict.winning_value`, `best_fact_id`, and `conflicting_fact_ids` when a
  conflict is projected;
- `Explanation.current_beliefs` and `Explanation.competing_beliefs` for current
  subject/predicate queries.

Missing pieces include a dedicated structured rationale that states which
selection rule or tie-break was applied, which expired facts were excluded, and
why ambiguity rather than a winner occurred. This document does not implement
that rationale.

# Replacement Rationale

Status: **missing** as a general explanation category, with partial temporal and
current-state data for measurement cases.

Replacement rationale is distinct from explanation. It answers why one fact,
measurement, or support record replaced another as current. Seed can show current
support and competing support, and measurement predicates have current-sample
semantics. Durable single-cardinality predicates can have stronger support win
over competing support without deleting the older fact.

Seed does not currently expose a general replacement concept in projected state
and does not provide a what-changed/as-of replacement explanation helper. This
document does not add one.

# Stale Rationale

Status: **partial**.

Stale rationale is partially represented through existing temporal metadata.
Seed can represent facts with `expires_at`, determine expiry through existing
stale fact semantics, expose expired support metadata, and recommend a refresh
capability for some stale predicates. Capability Inventory can classify expired
verification support as `stale` and include support age/expiry metadata.

Stale rationale is not yet a unified explanation contract. There is no dedicated
`why_stale(fact_id)` helper that joins fact, expiry, current time, source,
evidence, refresh recommendation, and as-of timeline context into one stable
object. Measurement replacement or pruning is also not the same as expiry-based
staleness.

# Non-Goals

This vocabulary document does not propose or implement:

- an `ExplanationEngine`;
- a `ReasoningEngine`;
- a `WhySubsystem`;
- Runtime explanation paths;
- ToolExecutor explanation hooks;
- provider-backed explanation checks;
- LLM-generated explanations;
- projection mutation;
- event appending;
- a parallel truth system;
- schema classes;
- explanation models;
- adapters;
- inventories;
- executable rules;
- capability verification behavior;
- tool execution behavior;
- orchestration behavior;
- changes to EventLedger ownership;
- changes to ProjectionStore ownership;
- changes to current support selection semantics.

# Future Work

Future work should remain documentation-oriented unless a separate roadmap item
explicitly authorizes implementation.

Acceptable future documentation work includes:

- adding examples that map existing `ExplanationBuilder`, Evidence Graph,
  Capability Inventory, Rule Inventory, contradiction, graph issue, stale fact,
  and State View outputs into the vocabulary shape;
- documenting category-specific status vocabularies in more detail;
- documenting how surface-specific fields should be placed under `extensions`;
- adding documentation-only examples for why-not, selection, replacement, and
  stale rationale gaps;
- adding characterization tests that verify documentation examples against
  existing behavior without changing Runtime, ToolExecutor, projection, or
  execution semantics.

Future work must not propose explanation engines, Runtime integration,
ToolExecutor integration, projection mutation, provider calls, LLM reasoning,
parallel truth systems, or execution behavior.

# Executive Summary

Seed already has enough read-only explainability building blocks to describe many explanation-like outputs, but those outputs are split across several surfaces rather than normalized through one contract. The existing surfaces expose facts, support, evidence, conflicts, rule metadata, capability verification inventory entries, stale-fact refresh recommendations, graph issues, impact summaries, and current-state views.

This audit does **not** recommend a new explanation engine. It finds that a common read-only explanation contract is feasible as an inventory/schema exercise because most surfaces already expose the same recurring concepts: subject, claim, status, supporting facts, supporting evidence, conflicts, rules, temporal metadata, provenance, and notes/reasons. The contract would describe existing outputs; it should not generate explanations, call Runtime, call ToolExecutor, execute tools, mutate projections, or add LLM reasoning.

The smallest safe next step is to document a read-only explanation contract inventory, then add characterization tests that map existing surfaces into that contract shape without changing behavior.

# Existing Explanation-Producing Surfaces

## ExplanationBuilder / `--why`

`ExplanationBuilder.why(subject, predicate)` is the most explicit explanation-producing surface. It reads projected `State`, gathers `FactSupport`, chooses current and competing beliefs, attaches a `FactConflict` when present, and recursively follows inferred facts through `source_fact_id` and `inference_rule_id`.

It exposes:

- query subject and predicate;
- status: `current`, `ambiguous`, or `no_current_belief`;
- current beliefs and competing beliefs;
- belief subject, predicate, value, support confidence, supporting fact IDs, evidence IDs, source types, first/latest observation times;
- recursive fact explanations containing fact ID, subject, predicate, value, evidence IDs, source type, observed/inferred confidence, confidence cap, inference rule ID, source fact ID, source fact, and entity-resolution path;
- attached `FactConflict` reason and conflict metadata when active.

Absent or partial:

- no arbitrary fact-ID explanation API;
- no full `Evidence.payload` join in the same object;
- no explicit selection-rationale object for why one support won;
- no why-not contract;
- no dedicated stale/replacement rationale.

## Why-fact output / Evidence Graph fact view

`--why-fact` formats `FactEvidenceView` from the Evidence Graph. It explains a matching fact-like claim by showing the fact triple, confidence, a generated evidence summary string, evidence nodes, and supporting event IDs.

It exposes:

- subject, predicate, object/value;
- confidence;
- evidence nodes with evidence ID, type, summary, source event/run IDs, confidence, created time;
- supporting event IDs;
- a concise generated explanation string from the evidence graph.

Absent or partial:

- no current-vs-competing belief status;
- no `FactSupport` aggregate fields unless separately queried;
- no conflict join unless contradiction/conflict surfaces are also queried;
- no rules or inference metadata except what is indirectly visible through fact IDs/source IDs.

## Evidence Graph

The Evidence Graph is a read-only projection over projected `State`. It exposes evidence nodes, evidence links, fact evidence views, and summary counts.

It exposes:

- evidence nodes: ID, type, summary, source event ID, source run ID, confidence, created time;
- evidence links: source evidence ID, target fact ID, relationship, strength;
- fact evidence views: fact ID, subject, predicate, object, confidence, evidence list, supporting event IDs, explanation string;
- summary: evidence count, linked fact count, unsupported fact count, average confidence, last event ID, projection version;
- unsupported fact views.

Absent or partial:

- no status field beyond linked/unsupported summary;
- no current selection, conflict, or stale rationale by itself;
- evidence relationships are link-level facts, not a unified explanation contract.

## FactSupport

`FactSupport` is not a prose explanation, but it is the core implied explanation of a supported claim. It groups projected facts by subject/predicate/dimensions/value for durable predicates and identifies current samples for measurement predicates.

It exposes:

- subject, predicate, value, dimensions;
- supporting fact IDs;
- source types;
- aggregate confidence;
- first and latest observation times;
- expired/expires-at metadata;
- predicate semantics: durable or measurement;
- support kind: aggregate or current sample.

Absent or partial:

- no full evidence records;
- no competing supports inline;
- no explicit rule IDs except through the facts it supports;
- no narrative notes beyond field names.

## FactConflict and contradiction reporting

Seed has two conflict-like surfaces:

1. `FactConflict`, projected from current facts/supports for single-cardinality durable disagreements.
2. The standalone `Contradiction` detector, which reports conservative exact subject/predicate conflicts for exclusive predicates and can attach evidence views.

`FactConflict` exposes:

- subject, predicate, dimensions;
- competing values;
- winning value, when unambiguous;
- best fact ID;
- conflicting fact IDs;
- reason.

`Contradiction` exposes:

- contradiction ID;
- subject, predicate;
- fact IDs and values;
- severity and reason;
- evidence by fact ID;
- supporting event IDs;
- summary counts by severity and affected facts.

Absent or partial:

- `FactConflict` does not include full evidence views;
- `Contradiction` does not use the predicate catalog cardinality semantics described by `FactConflict`;
- neither surface has a unified explanation object with supporting/competing facts separated by role.

## Capability verification inventory

The capability verification inventory is a read-only interpretation of projected state. It derives entries from registered tools, ToolNeeds, and `capability_verified` facts.

It exposes:

- capability as the subject;
- state/status: `verified`, `unverified`, `stale`, `provider_reported`, or `unknown`;
- supporting fact IDs;
- supporting evidence summaries;
- support summary with predicate, value, confidence, supporting fact IDs, source types, observed/latest observed times, expired, and expires-at;
- observed/latest observed time and age in seconds;
- reason.

Absent or partial:

- no explicit conflict list for disputed capability verification states;
- no scoped target model beyond the capability string in this inventory;
- no Runtime or ToolExecutor verification behavior, by design;
- no failed-verification semantics unless represented as future facts/evidence.

## Capability resolution and ToolNeed surfaces

Capability resolution is read-only metadata associated with requested capability gaps. `ToolNeed` and `ToolNeedService.resolve_capability` expose capability-gap and recommendation information, not verification.

They expose:

- requested capability, name, summary, reason, status, desired inputs/outputs;
- matching registered operation candidates as metadata;
- provider/handoff recommendations from the capability catalog;
- rank/recommendation metadata where available.

Absent or partial:

- no verification claim;
- no supporting evidence unless a future capability verification fact exists;
- no execution or availability assertion;
- no explanation contract that distinguishes request, candidate, recommendation, and verification in one shape.

## Rule Inventory

The Rule Inventory is a read-only catalog of deterministic rule-like metadata.

It exposes:

- rule entry ID;
- category;
- source;
- summary;
- if-conditions;
- then-effects;
- metadata.

It covers predicate catalog entries, predicate mappings, relationship catalog entries, entity type entries, inference catalog rules, graph validation checks, and capability-resolution recommendation rules.

Absent or partial:

- no per-fact link from an explanation to the exact inventory entry except inferred facts carrying `inference_rule_id`;
- no runtime rule engine;
- no execution behavior;
- no current-state selection rule object beyond inventory text/metadata.

## Stale fact reporting and refresh recommendations

Stale fact reporting comes from `State.get_stale_facts()` and CLI formatting. Refresh recommendations come from `State.get_stale_fact_refresh_recommendations()` using predicate-to-capability mapping.

They expose:

- stale fact subject, predicate, value;
- source type and confidence;
- expired boolean and expires-at timestamp;
- refresh recommendation fact ID, subject, predicate, value, recommended capability, and reason.

Absent or partial:

- no stale explanation object that joins stale fact, current replacement, previous support, and refresh recommendation;
- no replacement rationale when a fresh fact supersedes a stale fact;
- no as-of temporal explanation.

## Impact output

`--impact` formats an entity-centered projected-state summary.

It exposes:

- canonical entity and entity types;
- aliases;
- availability status and local observation status;
- local network configuration facts;
- endpoint availability grouped by role;
- groups/memberships, dependencies, and dependents;
- active conflicts;
- graph issues.

Absent or partial:

- it is an impact/summary view, not a normalized explanation;
- supporting facts/evidence are usually not listed for each line;
- rules and selection rationale are not attached.

## Current-facts and State View output

`--current-facts` and State View builders expose current projected state as read-only views.

They expose:

- current fact subject, predicate, object/value, confidence, and supporting event IDs in `FactView`;
- observation summaries with supporting IDs;
- requirement names/statuses;
- capability names/statuses;
- issue summaries/severity/supporting IDs;
- state summary counts and projection metadata.

Absent or partial:

- no support aggregate or evidence list for each current fact unless other surfaces are queried;
- no conflict/rule/stale rationale inline;
- no explanation status beyond view-specific statuses.

## Graph issues

Graph validation issues are explanation-like because they identify why projected relationships are suspect.

They expose:

- issue ID, severity, subject, relationship, object;
- reason;
- relationship IDs and source fact IDs;
- expected and actual subject/object types;
- hint.

Absent or partial:

- not modeled as fact explanations;
- no evidence join unless source fact IDs are used to query evidence separately.

# Common Explanation Fields

The table below summarizes whether each candidate explanation field already exists across the audited surfaces.

| Field | Exists today? | Existing carriers | Notes |
| --- | --- | --- | --- |
| `subject` | Implemented | `Fact`, `FactSupport`, `Explanation`, `BeliefExplanation`, `FactEvidenceView`, `FactConflict`, `Contradiction`, `CapabilityInventoryEntry`, `RuleInventoryEntry` (rule ID/source as subject-like), State Views | Usually an entity/capability/rule/fact. |
| `claim` | Implemented | fact triple, belief value, capability verification state/value, contradiction values, rule summary/effects, issue summary | Claim spelling varies by surface. |
| `status` | Partially implemented | `Explanation.status`, capability inventory `state`, ToolNeed status, State View statuses, issue severity, contradiction severity, stale `expired` | No universal status vocabulary. |
| `supporting_facts` | Implemented | `FactSupport.supporting_fact_ids`, `BeliefExplanation.supporting_fact_ids`, capability inventory `supporting_facts`, graph issue `source_fact_ids`, contradiction fact IDs | Role is not always separated into support vs conflict. |
| `supporting_evidence` | Implemented | `Evidence`, Evidence Graph nodes/views, capability evidence summaries, fact `evidence_ids`, contradiction evidence by fact ID | Full payload joins are split from `ExplanationBuilder`. |
| `competing_facts` | Partially implemented | `Explanation.competing_beliefs`, `FactConflict.conflicting_fact_ids`, `Contradiction.fact_ids` | No generic field name. |
| `conflicts` | Implemented | `FactConflict`, `Contradiction`, graph issues, issue views | Conflict shape varies. |
| `rules` | Partially implemented | `Fact.inference_rule_id`, `RuleInventoryEntry`, inference catalog metadata, graph validation inventory | Rule inventory is not linked to every output. |
| `temporal_metadata` | Implemented | observed/latest observed times, evidence observed/created times, expires-at, expired, age seconds, projection version/last event | No single temporal metadata object. |
| `provenance` | Implemented | evidence IDs, source type, source event/run IDs, source fact ID, source paths in rule inventory, supporting event IDs | Provenance is strong but dispersed. |
| `notes` | Implemented | `reason`, `summary`, `explanation`, hints, if/then text | Field names differ. |

Common fields across most explanation-producing surfaces are: subject, claim/value, status or severity, supporting IDs, provenance, temporal metadata, and notes/reason. Less common fields are rules, competing facts, and explicit selection/replacement rationale.

# Fact Explanation Fit

`Fact`, `FactSupport`, and `Evidence` already imply a minimal fact explanation structure:

```yaml
subject: FactSupport.subject or Fact.subject_id
claim:
  predicate: FactSupport.predicate or Fact.predicate
  value: FactSupport.value or Fact.value
status: current | ambiguous | no_current_belief | stale | unsupported
supporting_facts: FactSupport.supporting_fact_ids
supporting_evidence: Fact.evidence_ids plus Evidence Graph nodes
confidence: FactSupport.confidence or Fact.confidence
temporal_metadata:
  observed_at: Fact.observed_at
  latest_observed_at: FactSupport.latest_observed_at
  expires_at: Fact.expires_at or FactSupport.expires_at
  expired: FactSupport.expired / is_fact_expired(Fact)
provenance:
  source_type: Fact.source_type
  source_fact_id: Fact.source_fact_id
  inference_rule_id: Fact.inference_rule_id
notes:
  evidence graph explanation string or support semantics
```

A fact explanation can already be represented using existing models for current/ambiguous facts:

- `ExplanationBuilder` provides the current/competing belief framing.
- `FactSupport` provides support aggregation.
- `Fact` provides provenance, confidence, inference, expiry, and evidence IDs.
- `EvidenceGraph` provides evidence nodes and source event/run IDs.

The missing piece is not data; it is a unified read-only shape that joins these pieces consistently without changing projection behavior.

# Contradiction Explanation Fit

Contradiction-specific fields already exist:

- `FactConflict.subject`, `predicate`, `dimensions`, `values`, `winning_value`, `best_fact_id`, `conflicting_fact_ids`, and `reason`;
- `Contradiction.contradiction_id`, `subject`, `predicate`, `fact_ids`, `values`, `severity`, `reason`, `evidence_by_fact_id`, and `supporting_event_ids`;
- graph validation issue fields such as severity, reason, source fact IDs, relationship IDs, expected/actual types, and hints.

Contradiction explanations fit a generalized explanation shape if:

- the subject is the conflicting entity/predicate pair or graph relationship;
- the claim is "these values cannot all be current for this predicate/relationship";
- status maps to `conflicted`, `ambiguous`, or issue severity;
- supporting facts are the fact IDs participating in the conflict;
- competing facts are the same facts grouped by value;
- supporting evidence comes from `evidence_by_fact_id` or Evidence Graph lookup;
- notes contain the existing reason/hint.

What remains unique is the contradiction-specific role split: winning fact, conflicting facts, all values, severity, graph expected/actual types, and relationship IDs. A generalized contract should preserve these as structured extension metadata rather than flattening them away.

# Capability Explanation Fit

Capability-related claims already expose explanation fields through the verification inventory, ToolNeed, capability resolution, and capability catalog/ranker outputs.

Existing fields:

- subject: capability slug or ToolNeed ID/capability;
- claim: verification state, requested capability, registered operation candidate, or provider recommendation;
- status: inventory state (`verified`, `unverified`, `stale`, `provider_reported`, `unknown`) or ToolNeed status;
- supporting facts: `capability_verified` support fact IDs when present;
- supporting evidence: capability evidence summaries;
- temporal metadata: observed/latest observed timestamps, expires-at, expired, age seconds;
- provenance: source types, evidence IDs/source events, catalog source/provider metadata, requested-by event IDs;
- notes: reason fields and recommendation metadata.

Capability explanations differ from fact explanations because capability resolution is not itself verification. A capability explanation must preserve the distinction among:

- requested capability gap;
- catalog-known capability;
- registered operation candidate;
- provider/handoff recommendation;
- verified capability claim supported by facts/evidence.

Only the last category is evidence-backed verification. A generalized explanation shape can represent capability claims, but its status vocabulary must avoid implying execution, availability, or verification from request/recommendation metadata alone.

# Rule Explanation Fit

Rule explanations can fit the same broad shape as long as rules are treated as read-only metadata, not as an engine.

Existing fields:

- subject: rule entry ID;
- claim: summary plus if/then rule statement;
- status: generally `documented` or `inventory_entry` rather than current/verified;
- supporting facts/evidence: usually absent, except inferred facts can reference `inference_rule_id`;
- rules: the entry itself;
- temporal metadata: absent for static catalog entries;
- provenance: source path and metadata;
- notes: summary, conditions, effects, metadata reason.

Rule-specific fields that remain unique:

- category;
- source path;
- if-conditions;
- then-effects;
- catalog metadata;
- inference confidence/reason for inference rules;
- graph validation expected/actual semantics;
- capability-resolution `executable: false` metadata and provider/recommendation lists.

A common contract should therefore include `rules` as references or embedded inventory entries, not duplicate the Rule Inventory.

# Temporal Explanation Fit

Temporal explanation fields already exist:

- `Fact.observed_at`;
- `Fact.expires_at`;
- `FactSupport.observed_at` and `latest_observed_at`;
- `FactSupport.expired` and `expires_at`;
- `Evidence.observed_at` / evidence node created time;
- capability inventory `observed_at`, `latest_observed_at`, `age_seconds`, `expired`, `expires_at`;
- state/evidence/contradiction summaries `last_event_id` and `projection_version`;
- stale fact output `expired` and `expires_at`;
- stale refresh recommendation reason and recommended capability;
- measurement support semantics: `current_sample` rather than durable aggregate.

These fit a generalized explanation shape as `temporal_metadata` with optional fields:

```yaml
temporal_metadata:
  observed_at: ...
  latest_observed_at: ...
  expires_at: ...
  expired: ...
  age_seconds: ...
  projection_version: ...
  last_event_id: ...
  predicate_semantics: durable | measurement
  support_kind: aggregate | current_sample
```

Missing temporal concepts include:

- explicit stale rationale object;
- explicit replacement rationale when fresh current support supersedes stale support;
- explicit selection rationale for latest measurement sample;
- as-of temporal explanations;
- fact history explanation independent of event-ledger inspection.

# Existing Building Blocks

Reusable structures already present:

- `Fact`: claim, confidence, source type, evidence IDs, observation time, expiry, inference metadata, source fact link.
- `FactSupport`: claim support aggregation, current sample semantics, support IDs, source types, confidence, temporal and expiry metadata.
- `Evidence`: payload provenance, source/kind, observation time, confidence.
- `EvidenceGraph`, `EvidenceNode`, `EvidenceLink`, `FactEvidenceView`, `EvidenceSummary`: evidence/fact read-only graph and concise evidence explanations.
- `FactConflict`: projected conflict among durable single-cardinality facts.
- `Contradiction`: conservative contradiction report with severity, evidence views, and supporting event IDs.
- `CapabilityInventoryEntry`, `CapabilitySupportSummary`, `CapabilityEvidenceSummary`: capability verification inventory entries derived from facts/support/evidence.
- `ToolNeed` and capability resolution metadata: requested capability gaps and read-only candidate/recommendation metadata.
- `RuleInventoryEntry`: source-attributed deterministic rule metadata.
- `GraphValidationIssue` and Issue Views: relationship/graph explanation-like issues.
- `Explanation`, `BeliefExplanation`, `FactExplanation`: explicit why-query shape for fact beliefs.
- State View classes: current facts, observations, requirements, capabilities, issues, and summary counts.
- Stale fact refresh recommendation: deterministic stale refresh capability recommendation.

What should be reused:

- fact/support/evidence/conflict/rule/capability inventory structures and their IDs;
- Evidence Graph for evidence joins;
- Rule Inventory for rule metadata;
- existing temporal metadata fields;
- existing reason/summary/hint fields.

What should not be duplicated:

- a second evidence store;
- a second conflict detector for the same semantics;
- a new rule engine;
- a new explanation generator;
- Runtime or ToolExecutor behavior;
- projection semantics;
- LLM-generated explanations.

# Explanation Contract Feasibility

A common read-only explanation contract is feasible as a descriptive schema over current outputs. A contract like the following could describe existing surfaces without adding behavior:

```yaml
Explanation:
  subject: string
  claim:
    predicate: string | null
    value: any | null
    summary: string | null
  status: string
  supporting_facts: list
  supporting_evidence: list
  competing_facts: list
  conflicts: list
  rules: list
  temporal_metadata: object
  provenance: object
  notes: list
  extensions: object
```

Field fit:

- `subject`: feasible for facts, capabilities, rules, graph issues, contradictions, and impact/current-state lines.
- `claim`: feasible if represented flexibly as predicate/value plus summary.
- `status`: feasible but needs a vocabulary inventory because current statuses differ by surface.
- `supporting_facts`: feasible through `FactSupport`, fact IDs, graph issue source fact IDs, capability inventory support, and state views.
- `supporting_evidence`: feasible through Evidence Graph and capability evidence summaries.
- `competing_facts`: feasible for fact conflicts/contradictions and competing beliefs.
- `conflicts`: feasible using `FactConflict`, `Contradiction`, and graph issues.
- `rules`: feasible using `Fact.inference_rule_id` and Rule Inventory entries, but not all outputs currently link to specific rules.
- `temporal_metadata`: feasible using existing observed/latest/expires/age/projection fields.
- `provenance`: feasible using evidence IDs, source types, source facts, source events/runs, catalog source paths, and requested-by event IDs.
- `notes`: feasible using existing reason, summary, explanation, hint, if/then, and recommendation text.

The contract should be read-only and adapter-like. It should describe and normalize already-produced output. It should not decide truth, select facts differently, execute refreshes, verify capabilities, generate prose with an LLM, mutate projections, or call Runtime/ToolExecutor.

# Missing Concepts

| Concept | Classification | Notes |
| --- | --- | --- |
| Unified explanation contract | Missing | No single schema spans fact, contradiction, capability, rule, stale, impact, and current-state outputs. |
| Fact explanation | Already implemented | `ExplanationBuilder`, `FactSupport`, `Fact`, and Evidence Graph cover most required fields, though joins are split. |
| Capability explanation | Partially implemented | Capability inventory explains verification facts; ToolNeed/resolution explain requests/recommendations, but status vocabulary must avoid implying verification. |
| Contradiction explanation | Partially implemented | `FactConflict` and `Contradiction` expose core fields; full unified evidence/support/rule shape is absent. |
| Rule explanation | Partially implemented | Rule Inventory exists; per-output linkage to rule entries is partial. |
| Temporal explanation | Partially implemented | Temporal fields and stale reporting exist; stale/replacement/as-of rationale is missing. |
| Why-not explanation | Missing | No first-class API for why a claim is not current/verified/selected. |
| Selection rationale | Missing | Support ranking/current selection exists in code but not as a first-class read model. |
| Replacement rationale | Missing | No object explaining why a newer/fresher value replaced an older/stale/current value. |
| Stale rationale | Partially implemented | Expiry and refresh recommendation reason exist; no unified stale explanation joins current replacement and evidence. |

# Recommended Smallest Next Step

The smallest safe next step is documentation plus characterization only:

1. Add a read-only explanation contract inventory document that defines field names and maps each existing surface into those fields.
2. Add characterization tests that assert existing surfaces can be losslessly summarized into that shape using adapters/local fixtures, without changing production behavior.
3. Keep the contract explicitly read-only and non-executable.

Do **not** implement an explanation engine. Do **not** add Runtime behavior. Do **not** add ToolExecutor behavior. Do **not** change EventLedger ownership, ProjectionStore ownership, projection semantics, execution behavior, orchestration, or LLM reasoning.

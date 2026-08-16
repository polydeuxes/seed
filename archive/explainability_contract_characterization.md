# Executive Summary

This characterization finds that Seed's existing explanation-producing surfaces can be represented by a common **read-only** explanation shape without changing Runtime behavior, ToolExecutor behavior, EventLedger ownership, ProjectionStore ownership, projection semantics, orchestration, or execution behavior.

The proposed shape is feasible as a descriptive schema over current outputs:

```yaml
Explanation:
  subject: string
  claim: object
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

This is **not** a recommendation to implement a new explanation system. The existing code already exposes most required facts, evidence, conflicts, rules, temporal metadata, provenance, and reason strings. The main gap is not raw data; it is the absence of a unified contract or read-only adapter that names the fields consistently across surfaces.

Key findings:

- Fact explanations already fit the shape with minimal adaptation from `Explanation`, `BeliefExplanation`, `FactExplanation`, `FactSupport`, `Fact`, and `FactEvidenceView`.
- Contradiction explanations fit the same shape if contradiction-specific details such as severity, values, winning/conflicting facts, graph expected/actual types, and relationship IDs remain in `extensions`.
- Capability explanations fit the same shape if the schema preserves the distinction between verified capability facts and non-verifying request/catalog/recommendation metadata.
- Rule explanations fit as metadata explanations whose subject is a rule entry and whose `rules` field reuses `RuleInventoryEntry` rather than duplicating rule catalogs.
- Temporal explanations fit through existing observation, expiry, age, projection, stale, and current-sample fields, but stale/replacement/selection rationale is only partial.
- Why-not, replacement rationale, and first-class selection rationale remain missing as named read models.

The smallest safe next step is documentation and characterization only: define a read-only field vocabulary and, if desired later, add read-only adapter characterization tests that map current objects into the common shape without changing production behavior.

# Existing Explanation Surfaces

The following surfaces already expose explanation data:

1. **`ExplanationBuilder` / `Explanation` / `BeliefExplanation` / `FactExplanation` / `--why`**
   - Most explicit fact-belief explanation surface.
   - Exposes query subject/predicate, status, current beliefs, competing beliefs, supporting fact IDs, evidence IDs, confidence, source types, temporal metadata, recursive inference/source-fact links, entity-resolution path, and optional `FactConflict`.

2. **`--why-fact` / `FactEvidenceView`**
   - Evidence-oriented explanation for a matched fact-like claim.
   - Exposes fact ID, subject, predicate, object/value, confidence, evidence nodes, supporting event IDs, and a concise evidence explanation string.

3. **`FactSupport`**
   - Core support aggregate/current-sample surface.
   - Exposes subject, predicate, value, dimensions, supporting fact IDs, source types, confidence, observed/latest observed time, expiry fields, predicate semantics, and support kind.

4. **`Evidence` / Evidence Graph**
   - Read-only evidence/fact/provenance graph.
   - Exposes evidence nodes, links, fact evidence views, unsupported fact views, summary counts, last event ID, and projection version.

5. **`FactConflict` / `--fact-conflicts`**
   - Projected conflict among current facts/supports.
   - Exposes subject, predicate, dimensions, values, winning value, best fact ID, conflicting fact IDs, expiry status in CLI formatting, and reason.

6. **`Contradiction` / `--contradictions`**
   - Conservative read-only contradiction detector.
   - Exposes contradiction ID, subject, predicate, fact IDs, values, severity, reason, evidence by fact ID, supporting event IDs, summary counts, last event ID, and projection version.

7. **`GraphValidationIssue` / `--graph-issues` / Issue Views**
   - Graph relationship explanation-like issue surface.
   - Exposes issue ID, severity, subject, relationship, object, relationship IDs, source fact IDs, reason, hint, expected/actual subject types, and expected/actual object types.

8. **Capability Verification Inventory**
   - Read-only verification inventory derived from `capability_verified` facts/support/evidence.
   - Exposes capability, verification state, supporting fact IDs, supporting evidence summaries, support summary, observed/latest observed time, age seconds, expiry fields, and reason.

9. **`ToolNeed` and capability resolution metadata**
   - Capability-gap and recommendation explanation surface.
   - Exposes requested capability, need status/reason/request event, desired inputs/outputs/risk hints, known-capability flag, registered operation candidates, provider recommendations, and handoff candidates.

10. **Provider recommendations / capability catalog recommendation metadata**
    - Non-executable recommendation explanation surface.
    - Exposes provider, score, reasons, backend/operation handoff metadata, and catalog source metadata.

11. **Rule Inventory**
    - Read-only deterministic rule metadata inventory.
    - Exposes rule ID, category, source, summary, if-conditions, then-effects, and metadata for predicates, mappings, relationships, entity types, inference rules, graph validation, and capability resolution.

12. **Inference metadata**
    - Exposed on inferred facts and recursive fact explanations.
    - Exposes `inference_rule_id`, `source_fact_id`, inferred confidence, confidence cap, and source fact traversal.

13. **Predicate semantics**
    - Exposed through predicate catalog/rule inventory and `FactSupport`.
    - Distinguishes durable vs measurement semantics and single vs multi current cardinality.

14. **Stale fact reporting / refresh recommendations**
    - Temporal explanation-like surface.
    - Exposes stale fact subject/predicate/value/source/confidence/expiry and deterministic refresh capability recommendation with reason.

15. **Impact output**
    - Entity-centered projected-state explanation-like summary.
    - Exposes relevant projected facts, local network facts, graph issues, and operator-readable notes, but is a summary view rather than a normalized explanation object.

16. **Current-state views / `--current-facts`**
    - Current projected state explanation-like surfaces.
    - Expose current fact subject/predicate/object/confidence/supporting event IDs, observations, requirements, capabilities, issues, and state summary counts.

# Explanation Field Mapping Matrix

Legend:

- **implemented**: field is directly present on the surface or its immediate formatter/model.
- **partial**: field is present indirectly, with a different name, or requires a read-only join to another existing surface.
- **missing**: field is not exposed by that surface.

| Surface | subject | claim | status | supporting_facts | supporting_evidence | competing_facts | conflicts | rules | temporal_metadata | provenance | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ExplanationBuilder` / `Explanation` / `--why` | implemented | implemented | implemented | implemented | partial | implemented | implemented | partial | implemented | implemented | partial |
| `FactExplanation` | implemented | implemented | partial | partial | implemented | missing | missing | implemented | implemented | implemented | partial |
| `BeliefExplanation` | implemented | implemented | partial | implemented | implemented | missing | missing | partial | implemented | implemented | partial |
| `FactSupport` | implemented | implemented | partial | implemented | missing | missing | missing | partial | implemented | implemented | missing |
| `Fact` | implemented | implemented | partial | missing | implemented | missing | missing | implemented | implemented | implemented | missing |
| `Evidence` | partial | partial | missing | missing | implemented | missing | missing | missing | implemented | implemented | partial |
| Evidence Graph / `FactEvidenceView` / `--why-fact` | implemented | implemented | partial | partial | implemented | missing | missing | partial | implemented | implemented | implemented |
| Unsupported fact views | implemented | implemented | implemented | partial | implemented | missing | missing | missing | partial | partial | implemented |
| `FactConflict` / `--fact-conflicts` | implemented | implemented | implemented | implemented | partial | implemented | implemented | missing | partial | partial | implemented |
| `Contradiction` / `--contradictions` | implemented | implemented | implemented | implemented | implemented | implemented | implemented | missing | partial | implemented | implemented |
| `GraphValidationIssue` / Issue Views | implemented | implemented | implemented | implemented | missing | partial | implemented | implemented | missing | implemented | implemented |
| Capability Verification Inventory | implemented | implemented | implemented | implemented | implemented | missing | missing | partial | implemented | implemented | implemented |
| `ToolNeed` | implemented | implemented | implemented | missing | missing | missing | missing | missing | missing | implemented | implemented |
| Capability resolution metadata | implemented | implemented | partial | missing | missing | partial | missing | implemented | missing | implemented | implemented |
| Provider recommendations | implemented | implemented | partial | missing | missing | partial | missing | partial | missing | implemented | implemented |
| Rule Inventory | implemented | implemented | implemented | missing | missing | missing | missing | implemented | missing | implemented | implemented |
| Inference metadata | partial | implemented | partial | implemented | partial | missing | missing | implemented | partial | implemented | implemented |
| Predicate semantics | implemented | implemented | implemented | missing | missing | missing | missing | implemented | missing | implemented | implemented |
| Stale fact reporting | implemented | implemented | implemented | missing | partial | missing | missing | partial | implemented | implemented | partial |
| Stale refresh recommendations | implemented | implemented | partial | implemented | missing | missing | missing | partial | partial | partial | implemented |
| Impact output | implemented | partial | partial | partial | partial | partial | partial | missing | partial | partial | implemented |
| Current facts / State Views | implemented | implemented | implemented | partial | missing | missing | partial | missing | partial | implemented | partial |

Matrix findings:

- `subject`, `claim`, `status`, `provenance`, and `notes` are broadly present, though names differ.
- `supporting_facts`, `supporting_evidence`, and `temporal_metadata` are present in the fact/evidence/capability/stale surfaces and can usually be joined read-only.
- `competing_facts` and `conflicts` are concentrated in fact conflict, contradiction, graph issue, and `--why` surfaces.
- `rules` are present through `RuleInventoryEntry` and inference metadata, but not all explanation-like outputs currently link to a specific rule entry.
- `extensions` is necessary to avoid flattening domain-specific fields such as contradiction severity, graph expected/actual types, capability recommendations, operation candidates, stale refresh capability, and predicate semantics.

# Fact Explanation Characterization

Current fact explanations can already fit the common explanation shape.

Direct mappings:

| Common field | Current source |
| --- | --- |
| `subject` | `Explanation.query_subject`, `BeliefExplanation.subject`, `FactExplanation.subject`, `Fact.subject_id`, `FactSupport.subject`, `FactEvidenceView.subject` |
| `claim` | predicate/value from `BeliefExplanation`, `FactExplanation`, `Fact`, `FactSupport`, or `FactEvidenceView.object` |
| `status` | `Explanation.status`; derived `current`, `ambiguous`, `no_current_belief`, `unsupported`, or `expired` from current APIs |
| `supporting_facts` | `BeliefExplanation.supporting_fact_ids`, `FactSupport.supporting_fact_ids`, source fact traversal for inferred facts |
| `supporting_evidence` | `Fact.evidence_ids`, `BeliefExplanation.evidence_ids`, `FactExplanation.evidence_ids`, `FactEvidenceView.evidence` |
| `competing_facts` | `Explanation.competing_beliefs`, `FactConflict.conflicting_fact_ids`, contradiction fact groups |
| `conflicts` | `Explanation.conflict`, `FactConflict`, `Contradiction` lookup |
| `rules` | `Fact.inference_rule_id`, `FactExplanation.inference_rule_id`, Rule Inventory lookup |
| `temporal_metadata` | `Fact.observed_at`, `Fact.expires_at`, `FactSupport.observed_at`, `FactSupport.latest_observed_at`, `FactSupport.expired`, `FactSupport.expires_at`, `FactEvidenceView.evidence.created_at` |
| `provenance` | `source_type`, `source_types`, evidence IDs, source fact ID, entity-resolution path, evidence node source event/run IDs |
| `notes` | Evidence Graph explanation string, conflict reason, formatter reason text such as “best-supported current belief” or “latest current measurement” |

Adaptation required:

- Normalize `query_subject`/`query_predicate`, `subject`/`predicate`/`value`, and `object` into one `claim` object.
- Join `FactSupport` to `Fact` and Evidence Graph when full evidence nodes are desired.
- Map `Explanation.current_beliefs` to current/supporting facts and `Explanation.competing_beliefs` to competing facts.
- Preserve recursive inferred fact details in `extensions.inference` rather than losing them.
- Add a read-only status vocabulary if a future adapter maps `current`, `ambiguous`, `no_current_belief`, `unsupported`, and `expired` into one field.

No behavior change is needed for fact explanation fit.

# Contradiction Explanation Characterization

Contradiction explanations can fit the same shape.

Shared fields:

| Common field | Current contradiction/graph source |
| --- | --- |
| `subject` | `FactConflict.subject`, `Contradiction.subject`, `GraphValidationIssue.subject` plus relationship/object context |
| `claim` | conflicting predicate/values, exclusive-predicate contradiction claim, or invalid relationship claim |
| `status` | `FactConflict` can map to `conflicted`; `Contradiction.severity`; `GraphValidationIssue.severity` |
| `supporting_facts` | `FactConflict.best_fact_id` and `conflicting_fact_ids`; `Contradiction.fact_ids`; `GraphValidationIssue.source_fact_ids` |
| `supporting_evidence` | `Contradiction.evidence_by_fact_id`; Evidence Graph lookup for `FactConflict`/graph issue facts |
| `competing_facts` | facts grouped by value, `FactConflict.conflicting_fact_ids`, `Contradiction.fact_ids` |
| `conflicts` | `FactConflict`, `Contradiction`, `GraphValidationIssue` itself |
| `rules` | exclusive predicate set, graph validation rules, relationship catalog/type expectations if linked through Rule Inventory |
| `temporal_metadata` | partial: fact expiry status in conflict formatting; contradiction summary projection metadata; evidence node times |
| `provenance` | fact IDs, relationship IDs, source fact IDs, supporting event IDs |
| `notes` | `reason`, graph issue `hint`, expected/actual type details |

Unique fields that should remain in `extensions`:

- `contradiction_id`.
- `severity` and severity counts.
- `values` and value grouping.
- `winning_value`, `best_fact_id`, and `conflicting_fact_ids` for `FactConflict`.
- `relationship_ids` for graph issues.
- expected/actual subject/object types for graph issues.
- graph issue `hint`.
- exclusive-predicate classification reason.

Contradiction surfaces do not require a separate explanation engine. A read-only adapter could map them into the common shape while preserving contradiction-specific fields in `extensions`.

# Capability Explanation Characterization

Capability explanations can fit the same shape, but their semantics differ from fact explanations.

Shared/reusable fields:

| Common field | Current capability source |
| --- | --- |
| `subject` | capability slug, `ToolNeed.id`, `ToolNeed.capability`, catalog capability |
| `claim` | `capability_verified` claim, requested capability gap, known-capability metadata, registered operation candidate, provider/handoff recommendation |
| `status` | `CapabilityInventoryEntry.state`, `ToolNeed.status`, operation candidate status, known/unverified/provider-reported/stale flags |
| `supporting_facts` | `CapabilityInventoryEntry.supporting_facts`, `CapabilitySupportSummary.supporting_fact_ids` |
| `supporting_evidence` | `CapabilityInventoryEntry.supporting_evidence` |
| `competing_facts` | partial: registered operations/recommendations may be alternatives, but not competing verified facts |
| `conflicts` | missing unless capability verification facts later conflict through normal fact conflict/contradiction surfaces |
| `rules` | capability resolution invariants, catalog entries, Rule Inventory capability-resolution entries |
| `temporal_metadata` | `observed_at`, `latest_observed_at`, `age_seconds`, support `expired`, support `expires_at` |
| `provenance` | source types, evidence summaries, requested-by event ID, catalog/recommendation/provider metadata |
| `notes` | inventory `reason`, ToolNeed `reason`, provider recommendation reasons, catalog recommendation metadata |

Important distinction:

- A requested capability, known catalog capability, registered operation candidate, or provider recommendation is **not** verified capability evidence.
- Only `capability_verified` facts/support/evidence represent verification claims.
- A common explanation shape is feasible only if `status` does not collapse recommendation, availability, execution, and verification into one meaning.

Capability-specific data that should remain in `extensions`:

- registered operation candidates;
- provider recommendation scores/reasons;
- handoff candidates;
- known-capability flag;
- desired inputs/outputs and risk hints;
- catalog backend/operation metadata;
- explicit marker that resolution metadata is non-executable and non-verifying.

# Rule Explanation Characterization

Rule explanations can fit the same shape as read-only metadata explanations.

Reusable fields:

| Common field | Current rule source |
| --- | --- |
| `subject` | `RuleInventoryEntry.id` |
| `claim` | `summary` plus `if_conditions`/`then_effects` |
| `status` | inventory/documented/static rule status |
| `supporting_facts` | usually missing; inferred facts can point back through `inference_rule_id` |
| `supporting_evidence` | usually missing for static catalog rules |
| `competing_facts` | missing |
| `conflicts` | missing except graph validation rules describe issue generation semantics |
| `rules` | `RuleInventoryEntry` itself |
| `temporal_metadata` | usually missing/static |
| `provenance` | `source` and `metadata` |
| `notes` | `summary`, conditions, effects, inference reason, metadata |

Rule-specific fields that should remain in `extensions` or embedded `rules` entries:

- category;
- source path;
- if-conditions;
- then-effects;
- predicate kind/value type/cardinality;
- mapping value maps;
- relationship subject/object expectations;
- inference confidence/reason;
- graph validation rule metadata;
- capability-resolution metadata.

The Rule Inventory should be reused directly. A common explanation shape should reference or embed existing `RuleInventoryEntry` objects; it should not duplicate rule catalogs or introduce a rule engine.

# Temporal Explanation Characterization

Temporal explanation fields already exist across facts, supports, evidence, capability inventory, stale reporting, and summaries.

Already existing temporal fields:

- `Fact.observed_at`.
- `Fact.expires_at`.
- `FactSupport.observed_at`.
- `FactSupport.latest_observed_at`.
- `FactSupport.expired`.
- `FactSupport.expires_at`.
- `FactSupport.predicate_semantics` (`durable` or `measurement`).
- `FactSupport.support_kind` (`aggregate` or `current_sample`).
- `Evidence.observed_at`.
- `EvidenceNode.created_at`.
- `CapabilityInventoryEntry.observed_at`.
- `CapabilityInventoryEntry.latest_observed_at`.
- `CapabilityInventoryEntry.age_seconds`.
- `CapabilitySupportSummary.expired`.
- `CapabilitySupportSummary.expires_at`.
- Evidence/contradiction/state summary `last_event_id`.
- Evidence/contradiction/state summary `projection_version`.
- stale fact `expired` and `expires_at` output.
- stale refresh recommendation reason and recommended capability.

Fit to common shape:

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

Temporal gaps:

- no first-class stale rationale object joining stale fact, previous support, evidence, current replacement, and refresh recommendation;
- no first-class replacement rationale when newer/fresher values supersede older values;
- no first-class selection rationale for latest measurement sample or strongest support selection;
- no as-of explanation read model independent of event-ledger inspection;
- fact support is a current projection, not an append-only support history.

# Contract Feasibility Analysis

The proposed read-only schema is sufficient to represent existing explanation-producing surfaces if `claim`, `status`, and `extensions` remain flexible.

```yaml
Explanation:
  subject: string
  claim:
    predicate: string | null
    value: any | null
    summary: string | null
    object: any | null
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

Feasibility by field:

- `subject`: feasible for facts, contradictions, graph issues, capabilities, rules, stale facts, impact lines, and current views.
- `claim`: feasible if represented as structured predicate/value/object plus summary text.
- `status`: feasible, but requires a status vocabulary inventory because surfaces use `current`, `ambiguous`, `no_current_belief`, severity, verification state, issue severity, ToolNeed status, operation status, `expired`, and implicit inventory/static statuses.
- `supporting_facts`: feasible through fact IDs, support IDs, source fact IDs, graph issue source facts, and capability support.
- `supporting_evidence`: feasible through Evidence Graph and capability evidence summaries.
- `competing_facts`: feasible for `--why`, `FactConflict`, `Contradiction`, graph ambiguity, and recommendation alternatives; not universal.
- `conflicts`: feasible through `FactConflict`, `Contradiction`, and `GraphValidationIssue`.
- `rules`: feasible through `Fact.inference_rule_id`, `FactExplanation.inference_rule_id`, predicate semantics, and Rule Inventory entries; linkage is partial.
- `temporal_metadata`: feasible through existing observed/latest/expires/expired/age/projection/current-sample fields.
- `provenance`: feasible through source types, evidence IDs, event/run IDs, source facts, catalog sources, requested-by event IDs, and provider metadata.
- `notes`: feasible through existing reason, summary, explanation, hint, condition/effect, and recommendation strings.
- `extensions`: required for domain-specific data and to avoid lossy normalization.

Conclusion: existing explanation-producing surfaces **can** be represented by this shape as a read-only schema/adaptation exercise. The shape should not imply a new explanation engine, new reasoning engine, LLM-generated explanations, Runtime changes, ToolExecutor changes, projection changes, or execution behavior.

# Reuse Analysis

Structures to reuse directly:

- `Fact`: claim, source type, evidence IDs, observation time, expiry, inference metadata, source fact link.
- `FactSupport`: support aggregation/current sample, supporting facts, source types, confidence, temporal and expiry metadata, predicate semantics, support kind.
- `Evidence`: source/kind/payload, observation time, confidence.
- Evidence Graph (`EvidenceGraph`, `EvidenceNode`, `EvidenceLink`, `FactEvidenceView`, `EvidenceSummary`): evidence joins, evidence summaries, unsupported facts, provenance links.
- `FactConflict`: current projected conflict metadata.
- `Contradiction`: conservative contradiction report with evidence views and supporting events.
- `GraphValidationIssue`: relationship/graph issue explanation data.
- `CapabilityInventoryEntry`, `CapabilitySupportSummary`, `CapabilityEvidenceSummary`: capability verification read model.
- `ToolNeed`: capability gap metadata and request provenance.
- capability resolution metadata: known capability, operation candidates, provider recommendations, handoff candidates.
- `RuleInventoryEntry`: deterministic rule metadata.
- `Explanation`, `BeliefExplanation`, `FactExplanation`, and `ExplanationBuilder`: existing why-query shape.
- State View classes (`FactView`, `ObservationView`, `RequirementView`, `CapabilityView`, `IssueView`, `StateSummary`): current projected-state surfaces.
- `StaleFactRefreshRecommendation`: stale refresh recommendation metadata.
- Existing temporal metadata fields on facts, supports, evidence, capability inventory, and summaries.

What should be adapted:

- Field names, not behavior: map existing names into common names (`query_subject` -> `subject`, predicate/value/object -> `claim`, source types/evidence IDs/source events -> `provenance`).
- Status labels: document a read-only vocabulary rather than changing producers.
- Evidence joins: use the existing Evidence Graph when a surface exposes only evidence IDs.
- Rule links: use `inference_rule_id` and Rule Inventory lookups where available.
- Domain-specific payloads: place contradiction, capability, graph, stale, and selection-specific details in `extensions`.

What should not be duplicated:

- Evidence storage or evidence graph construction.
- Conflict or contradiction detection.
- Rule catalogs or rule engines.
- Capability verification logic.
- Runtime decisions or ToolExecutor execution semantics.
- ProjectionStore/EventLedger responsibilities.
- Projection semantics.
- LLM-generated prose or reasoning.

# Gap Analysis

| Capability | Classification | Finding |
| --- | --- | --- |
| Unified explanation contract | missing | No single schema currently spans fact, contradiction, capability, rule, stale, impact, and current-state surfaces. |
| Fact explanation | already implemented | `ExplanationBuilder`, `Explanation`, `BeliefExplanation`, `FactExplanation`, `FactSupport`, `Fact`, and Evidence Graph cover the required data, though joins are split. |
| Contradiction explanation | partially implemented | `FactConflict`, `Contradiction`, and `GraphValidationIssue` expose core explanation data, but no unified shape joins conflicts, evidence, rules, and temporal metadata. |
| Capability explanation | partially implemented | Capability verification inventory explains verified/stale/unverified/provider-reported states; ToolNeed/resolution/recommendations explain gaps and candidates, but these are not the same as verification. |
| Rule explanation | partially implemented | Rule Inventory exists and inferred facts reference rule IDs, but not all surfaces link directly to rule entries. |
| Temporal explanation | partially implemented | Observed/expiry/latest/age/current-sample/projection fields exist; stale/replacement/as-of rationale is not first-class. |
| Why-not explanation | missing | No first-class API or read model explains why a requested claim is not current, not selected, not verified, or unsupported. |
| Selection rationale | missing | Current selection logic exists in support and best-fact selection, and CLI text names best-supported/latest measurement reasons, but no structured selection rationale read model exists. |
| Replacement rationale | missing | No object explains why a newer, fresher, higher-confidence, or non-expired value replaced another value. |
| Stale rationale | partially implemented | Expiry and refresh recommendation reasons exist, but no unified stale explanation joins stale fact, support/evidence, current replacement, and refresh recommendation. |

# Recommended Smallest Next Step

The smallest safe next step is **read-only characterization documentation plus optional read-only adapter characterization tests**.

Recommended sequence:

1. Keep this characterization as the source inventory for field names and fit.
2. If implementation is desired later, first add tests with local fixtures that demonstrate existing objects can be summarized into the common shape without changing any producers.
3. Only after those tests, consider a read-only adapter/schema module that maps existing surfaces into the shape.

Constraints for the next step:

- Do not implement an explanation engine.
- Do not implement a reasoning engine.
- Do not use LLM-generated explanations.
- Do not change Runtime behavior.
- Do not change ToolExecutor behavior.
- Do not change EventLedger ownership.
- Do not change ProjectionStore ownership.
- Do not change projection semantics.
- Do not add execution behavior, scheduling, orchestration, or provider calls.


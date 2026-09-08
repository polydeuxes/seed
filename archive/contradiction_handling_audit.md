# Executive Summary

Seed already has several read-only conflict and contradiction concepts, but they are projection and audit views rather than a truth-arbitration engine.

Current behavior is conservative:

- **Facts are append-only ledger-derived records** in projected state; Seed does not rewrite older facts when a new contradictory fact arrives.
- **Single-cardinality durable predicates** can produce `FactConflict` records when multiple non-expired values exist for the same resolved subject, predicate, and dimensions.
- **Multi-cardinality predicates** intentionally preserve multiple values and do not report those values as conflicts.
- **Measurement predicates** prefer the latest retained sample and treat prior retained samples as history, not durable disagreement.
- **Evidence is preserved separately** as observations, evidence records, fact evidence links, and fact support groups.
- **Graph validation surfaces topology/type problems** as deterministic `GraphValidationIssue` warnings/errors; it reports issues but does not remove or repair edges.
- **Explanation support exists for “why X?” and basic “why X is ambiguous/conflicting?”** through current beliefs, competing beliefs, and attached `FactConflict`; there is no explicit “why not Y?” API.
- **Confidence degradation exists only in the separate read-only confidence projection** that applies a contradiction penalty to facts found by the standalone contradiction detector. It does not change `Fact.confidence`, `FactSupport.confidence`, or projection selection behavior.

The smallest safe next step is to add **documentation-backed characterization tests** that pin the current contradiction semantics across `FactConflict`, standalone `Contradiction`, measurements, multi-cardinality predicates, graph issues, and explanations. Do not add resolution behavior or automatic truth arbitration.

# Current Conflict Model

Seed currently has two overlapping but distinct conflict views.

## Projection-level fact conflicts

`FactConflict` is a projected model for disagreement among facts for one subject and predicate. It stores the resolved subject, predicate, dimensions, observed values, optional winning value, optional best fact id, conflicting fact ids, and a reason string.

`StateProjector.project()` derives `state.fact_conflicts` after replaying events, resolving aliases, retaining measurement history, projecting inferred facts, projecting fact supports, projecting relationships/types, and validating graph issues. `State.get_fact_conflicts()` returns the cached projected conflicts by default or recomputes them with expired facts included on request.

Projection-level conflicts are created by `_project_fact_conflicts()` when all of the following are true:

- facts are non-expired unless `include_expired=True`;
- the predicate is not a measurement predicate;
- the predicate is not cataloged as multi-cardinality;
- facts share the same alias-canonical subject, predicate, and dimensions;
- more than one distinct value exists.

When a best fact can be selected, `FactConflict.winning_value` and `best_fact_id` identify it, while `conflicting_fact_ids` identifies facts with other values. If no unambiguous best support exists, the conflict records all grouped facts as conflicting and leaves winning fields empty.

## Standalone contradiction audit view

`seed_runtime.contradictions` provides a separate read-only contradiction detector. It is explicitly documented as a projection view over already-projected `State` and optional Evidence Graph; it does not read the ledger, append events, mutate facts, execute runtime behavior, call providers, evaluate policy, execute tools, or persist a separate contradiction store.

The standalone detector reports `Contradiction` records for exact subject/predicate groups whose predicate is in a conservative exclusive set or caller-supplied exclusive predicates. It does not use predicate catalog cardinality. It groups by exact `fact.subject_id` rather than alias-canonical subject. It includes fact ids, values, severity, reason, optional per-fact evidence views, and supporting event ids. Severity is currently always classified as `high` with reason `exclusive predicate has multiple values`.

## Graph-level issue reporting

`GraphValidator` validates projected catalog relationships against relationship and entity-type catalogs. It returns `GraphValidationIssue` warning/error records for suspicious or invalid relationship endpoints. It reports mismatches but does not remove relationships, alter entity types, rewrite aliases, or block state projection.

## Explanation-level conflict exposure

`ExplanationBuilder.why(subject, predicate)` explains current values, ambiguous values, or no current belief. For single-cardinality predicates it can include a matching `FactConflict` and competing belief explanations. For multi-cardinality predicates it returns all supports as current beliefs and does not attach conflict data.

# Existing Structures

## Fact

`Fact` is the core claim model. It includes:

- `id`
- `subject_id`
- `predicate`
- `value`
- `dimensions`
- `evidence_ids`
- `source_type`
- `confidence`
- `observed_at`
- `expires_at`
- `inferred`
- `source_fact_id`
- `inference_rule_id`

Conflict-relevant properties are the subject/predicate/value/dimensions tuple, evidence links, confidence, timestamps, expiration, and inference provenance.

## FactSupport

`FactSupport` is the projected support record for a single subject/predicate/value claim. Durable facts aggregate support across independent observations; measurement facts use the latest current sample. It stores supporting fact ids, source types, aggregate/current confidence, first/latest observation timestamps, expiration state, predicate semantics, and support kind.

## FactConflict

`FactConflict` is the projection-level fact disagreement record. It stores the values that disagree and the best/winning value if current support selection is unambiguous.

## PredicateCatalog

`PredicateCatalog` defines canonical predicates with:

- kind: `measurement` or `durable_fact`
- value type
- cardinality: `single` or `multi`
- allowed values
- provider mappings

Unknown predicates default to `single` cardinality.

Core examples:

- `runtime`, `os`, `architecture`, `managed_by`: durable single-cardinality
- `availability_status`, `health_status`, filesystem size/free predicates: measurement single-cardinality
- `alias`, `ansible_host`, `endpoint_role`, `group`, `ip_address`, `prometheus_instance`: durable multi-cardinality

## StateProjector and State

`StateProjector` rebuilds `State` from ledger events. Conflict-relevant projected state includes:

- `facts`
- `observed_facts`
- `inferred_facts`
- `fact_supports`
- `fact_conflicts`
- `observations`
- `evidence`
- `relationships`
- `entity_relationships`
- `entity_aliases`
- `entity_type_assertions`
- `graph_issues`
- `alias_resolver`

Supported event kinds that create conflict-relevant state are:

- `observation.observed`: stores the observation.
- `evidence.observed`: stores an evidence payload.
- `fact.observed`: stores an observed fact.
- `fact.inferred`: stores an inferred fact; projection may also rebuild deterministic inferred facts from current observed facts.
- `entity.upserted`: stores entities used in identity/type context.

Only facts create fact conflicts. Observations and evidence provide provenance and support but do not themselves create conflicts without corresponding facts.

## Evidence Graph

`EvidenceGraph` is read-only and derived from projected state. It creates evidence nodes, support links, and `FactEvidenceView` records for facts. The relationship vocabulary includes `supports`, `contradicts`, `mentions`, and `derived_from`, but current graph construction creates support links from evidence to facts; contradiction links are not automatically populated.

## Confidence projection

`seed_runtime.confidence` is a read-only confidence view over projected state, evidence graph, and standalone contradiction detection. It can mark facts as `contradicted`, count contradictions, and apply a contradiction penalty in the confidence view. It does not mutate fact confidence or projection support confidence.

# Cardinality Behavior

## Single-cardinality durable predicates

When conflicting values appear for a single-cardinality durable predicate, Seed preserves all facts and all support groups. It then attempts to select an unambiguous best support.

Selection behavior:

1. Fact supports are grouped by subject, predicate, dimensions, and value.
2. Durable support confidence is aggregated across independent evidence/source identities.
3. The best support is selected by support confidence and then supporting fact count.
4. If exactly one support has the top key, it is the current belief.
5. If multiple supports tie for top key, no best support exists and the value is ambiguous.

If a best support exists, `get_best_fact()` chooses a representative fact inside that support by confidence, observed-vs-inferred preference, timestamp, and id. `get_current_facts()` for a single-cardinality predicate returns only that best fact.

A `FactConflict` is recorded for non-expired, non-measurement, single-cardinality predicates with distinct values. Its winning fields are populated only when selection is unambiguous.

This behavior is deterministic because grouping, support selection, representative fact selection, conflict sorting, and ids use deterministic keys.

## Multi-cardinality durable predicates

For multi-cardinality durable predicates such as `ip_address`, `alias`, and `group`, Seed preserves multiple values as current beliefs. `get_current_facts()` returns one representative fact per supported value. `_project_fact_conflicts()` explicitly skips multi-cardinality predicates, so these multiple values are not fact conflicts.

## Measurement predicates

Measurement predicates are single-cardinality in the catalog, but they do not use durable conflict semantics. Projection retains only the latest sample by default, or a bounded debug history when configured. Fact support for measurements uses `support_kind="current_sample"` and points only to the latest sample for a subject/predicate/dimensions series. Retained older samples are treated as historical/debug samples and are skipped by conflict projection.

Examples:

- `availability_status=up` followed by `availability_status=down` results in current support for the newer sample, not a durable conflict.
- Filesystem measurements with different dimensions coexist without conflict.

# Evidence Disagreement Behavior

If two observations produce facts such as:

- Observation A: `service=running`
- Observation B: `service=stopped`

then current behavior depends on predicate semantics:

- For a durable single-cardinality predicate, both observations, both evidence records, and both facts are preserved in projected state unless the facts expire or are measurement-pruned. Seed builds separate `FactSupport` records for each value and records a `FactConflict` if the values are distinct.
- For a durable multi-cardinality predicate, both values are preserved as current supported values and no conflict is recorded.
- For a measurement predicate, the latest sample is current; older samples may be pruned by default or retained as debug history, but they are not considered conflicts.

Support is tracked separately. Repeated durable observations of the same value aggregate confidence. Different values do not combine into one support group; they compete through support selection.

Confidence is not degraded in the core fact or support projection merely because disagreement exists. `FactSupport.confidence` is aggregate support for that value. The separate confidence projection can reduce its own `FactConfidence.confidence` for facts included in standalone `Contradiction` records, but that read-only score does not change `Fact.confidence`, `FactSupport.confidence`, or current-belief selection.

# Graph-Level Contradictions

Seed can represent contradictory or suspicious topology because graph projection is additive and validation is report-only.

## Entity type mismatch

Projected relationships are checked against expected subject/object entity types. If an endpoint type is unknown, the issue is a warning. If a known independent type contradicts the expected type, the issue is an error. Ambiguous current types generally surface as warnings unless excluding the relationship's own type assertion reveals a single incompatible independent type.

## Relationship mismatch

Catalog relationships are projected from matching facts. If the projected edge's subject or object does not satisfy the catalog definition, `GraphValidator` records a `GraphValidationIssue` with severity, reason, expected types, actual types, source fact ids, and relationship ids. The edge remains present.

## Alias mismatch

Alias resolution is deterministic and built from explicit alias-like facts (`alias`, `ip_address`, `hostname`, and predicates ending with `_instance`). Alias facts form connected components and select a canonical name. There is no dedicated alias contradiction model. Conflicting or overly broad alias evidence can merge identities; downstream effects may surface as graph validation issues or fact conflicts after canonicalization, but alias disagreement itself is not reported as a named contradiction type.

# Temporal Support Already Present

Seed already has limited temporal support:

## Current

Current belief is computed from non-expired projected facts and support selection. For measurements, current means latest retained sample for the subject/predicate/dimensions series. For durable single-cardinality predicates, current means the unambiguous strongest support, if any. For durable multi-cardinality predicates, current includes every supported value.

## Historical

The append-only ledger retains all events. Projected measurement state retains only the latest sample by default, while `measurement_history_limit` can retain a bounded debug history. Durable facts remain in projected state unless expired or otherwise absent from replay.

## Stale

Facts support `expires_at`, and `is_fact_expired()` determines expiration. `State.get_stale_facts()` returns expired facts. `State.get_stale_fact_refresh_recommendations()` maps stale facts to deterministic refresh-capability recommendations. Expired facts are excluded from normal fact supports and conflicts by default but can be included in support/conflict queries with `include_expired=True`.

## Superseded

Superseded exists for `ActionPlan` status events, not for `Fact` or `FactSupport`. There is no fact-level supersession marker, superseded-by link, or superseded conflict status.

# Explainability Coverage

## Can Seed answer “Why does it believe X?”

Partially yes. `ExplanationBuilder.why(subject, predicate)` returns current beliefs with supporting fact ids, evidence ids, source types, confidence, observed/latest timestamps, recursive source facts for inference, confidence caps for inferred facts, and alias resolution chains.

## Can Seed answer “Why does it NOT believe Y?”

Not directly. There is no explicit `why_not()` API and no negative-belief model. If a queried single-cardinality predicate has competing supports but no unambiguous best support, `why()` returns `status="ambiguous"` and competing beliefs. If no support exists, it returns `status="no_current_belief"`. That helps explain absence or ambiguity but does not provide a purpose-built explanation of why a specific alternative value is rejected.

## Can Seed answer “Why are X and Y in conflict?”

Partially yes. For single-cardinality durable predicate conflicts, `why()` can attach the matching `FactConflict` and include competing belief explanations with supporting facts/evidence. The standalone contradiction detector can also list conflicting facts, values, severity, reason, evidence views, and supporting event ids for exclusive predicates. There is no unified conflict-explanation API that combines projection `FactConflict`, standalone `Contradiction`, graph issues, confidence penalties, and temporal status into one answer.

# Missing Concepts

| Concept | Classification | Current state |
| --- | --- | --- |
| conflict | Partially implemented | `FactConflict`, standalone `Contradiction`, graph issues, explanation conflict attachment, and confidence-view contradiction penalties exist, but they are not unified and do not resolve truth. |
| superseded | Partially implemented | Present for `ActionPlan` status only. Missing for facts, supports, evidence, and conflicts. |
| uncertain | Partially implemented | Confidence values, ambiguous explanations, unknown entity types, unsupported confidence reasons, and no-current-belief statuses exist. There is no first-class `uncertain` fact/support/conflict state. |
| disputed | Missing | Disputed is not a named state. Disagreement appears as conflicts/contradictions/graph issues, but there is no `disputed` marker or lifecycle. |
| stale | Partially implemented | `expires_at`, stale-fact listing, refresh recommendations, and include-expired query switches exist. There is no richer stale lifecycle beyond expiration. |
| confidence degradation | Partially implemented | The read-only confidence projection applies a contradiction penalty to its own confidence records. Core fact/support confidence and current-belief selection are not degraded by conflicts. |
| competing evidence | Partially implemented | Separate supports per value, competing beliefs in explanations, evidence graph support views, and standalone contradiction evidence attachment exist. There is no normalized competing-evidence object spanning all conflict types. |

# Recommended Smallest Next Step

Status: **implemented as characterization coverage** in `tests/test_contradiction_characterization.py`. The tests pin current contradiction behavior without changing projection, runtime, execution, or conflict-resolution semantics:

1. durable single-cardinality conflicts preserve both values, both facts, separate supports, and projected `FactConflict`;
2. tie-strength durable conflicts remain ambiguous with no winning value and no truth arbitration;
3. multi-cardinality values (`alias`, `ip_address`, and `group`) remain current without conflict solely because multiple values exist;
4. measurements choose the latest current sample without conflict, while `measurement_history_limit` can retain bounded debug history;
5. expired facts are stale, excluded from default conflicts/current belief, and visible in conflict queries only with `include_expired=True`;
6. `ExplanationBuilder.why()` exposes active conflict metadata and competing beliefs as currently designed;
7. projected `State.get_fact_conflicts()` acts as the small read-only conflict inventory over projected state;
8. graph validation reports `GraphValidationIssue` while leaving invalid projected edges and source facts intact.

The existing standalone `--contradictions` CLI remains the read-only contradiction audit surface for exact-subject/exclusive-predicate scans. No new CLI flag, conflict engine, runtime behavior, fact mutation, competing-evidence deletion, LLM reasoning, ToolExecutor behavior, or automatic truth arbitration was added.

# Files Inspected

- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/predicate_catalog.py`
- `predicate_catalog/core.json`
- `seed_runtime/contradictions.py`
- `seed_runtime/evidence.py`
- `seed_runtime/observations.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/confidence.py`
- `seed_runtime/explanations.py`
- `seed_runtime/models.py`
- `tests/test_fact_support_aggregation.py`
- `tests/test_contradictions.py`
- `tests/test_explanations.py`
- `tests/test_graph_validation.py`
- `tests/test_evidence_facts.py`
- `tests/test_state_projector.py`

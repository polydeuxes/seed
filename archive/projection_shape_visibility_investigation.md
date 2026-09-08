# Projection Shape Visibility Investigation

## Scope

This investigation reviews whether Seed's projection layer is difficult to explain because the implementation is immature or because the implemented projection stages lack an explicit shape-visibility contract. It does not propose new runtime behavior, new projection declarations, ontology changes, or redesigns.

Repository evidence indicates that projection behavior is substantial and deterministic, but its stage composition is mostly encoded in implementation order, helper calls, dataclass fields, CLI formatters, and tests rather than in a projection-specific shape inventory.

## Evidence Reviewed

- `StateProjector.project_from_state(...)` replays append-only ledger events and then delegates derived index rebuilding to `finalize(...)`.
- `StateProjector.finalize(...)` names the projection steps in diagnostic timing labels and assigns outputs onto `State` fields.
- `State` exposes query methods for current beliefs, support groups, conflicts, relationships, entity types, graph issues, stale facts, and relationship traversal.
- Helper functions implement support aggregation, current-belief source selection, inferred fact projection, relationship projection, entity-type projection, and graph validation.
- Operational visibility work uses explicit registries/specs for diagnostic surfaces, including declared flags, record scope, event-ledger writes, projected-state use, and mutation boundaries.

## Projection Stages Identified

The following stages are identifiable from implementation evidence. Names here are descriptive, not new repository objects.

| Stage | Consumes | Produces | Influences | Does not appear to influence | Authority boundary |
| --- | --- | --- | --- | --- | --- |
| Event replay | Ledger events | Base `State` collections such as entities, observations, evidence, facts, goals, needs, approvals, plans, tools | Every later projection step | N/A | Event history is the input authority; replayed state is rebuildable projected state. |
| Initial alias projection | Current facts before inference | `AliasResolver` | Measurement retention subject grouping; inferred fact projection; later canonical subject selection | It does not itself append facts or events | Alias facts are explicit identity inputs; resolver is derived. |
| Measurement history retention | Facts, measurement predicate semantics, alias canonicalization | Pruned projected `state.facts` for current retained measurement samples | Fact support, inferred facts, relationships, entity types, conflicts, current facts | It does not delete ledger events | Projection-cache retention only; ledger remains append-only authority. |
| Inferred fact projection | Current observed source facts, inference catalog, predicate catalog, alias resolver | Inferred facts merged back into `state.facts` | Fact support, relationships, entity types, graph validation, conflicts, current facts | Does not create observed facts or evidence | Derived interpretation from deterministic rules; inferred facts are weaker source type. |
| Observed/inferred partition | `state.facts` | `observed_facts`, `inferred_facts` | Explanation and inspection of fact provenance | Does not select current beliefs alone | Exposes source partition, not separate truth. |
| Measurement provenance pruning | Retained projected measurement facts, evidence, observations | Pruned projected evidence/observation maps | Explanation surfaces over retained measurement samples | Does not mutate ledger provenance | Projection-only cleanup for hidden samples. |
| Fact support projection | Non-expired facts by subject/predicate/dimensions/value | `fact_supports` | Current-belief selection, fact conflicts, `--best-fact`, `--current-facts`, why/explanation surfaces | Directly does not build relationships or graph issues | Selection-bearing aggregate support surface. |
| Legacy relationship projection | Facts whose values are strings | `entity_relationships` | Backward-compatible `find_entities` and fallback `find_related` | Does not feed graph validation in inspected code | Compatibility/read model. |
| Catalog relationship projection | Facts, relationship catalog, evidence suppressions | `relationships` | Relationship queries, dependency traversal, entity-type assertions, graph validation | Does not feed current fact selection | Derived interpretation from fact predicates and catalog definitions. |
| Entity type assertion projection | Entities, facts, catalog relationships, entity type catalog | `entity_type_assertions`; current entity types via selection method | Graph validation, entity type CLI, classification diagnostics | Does not feed fact support/current belief selection | Derived classification; strongest type selection is local to entity types. |
| Graph issue construction | Catalog relationships, entity types, relationship and entity-type catalogs | `graph_issues` | Graph issue CLI, unhealthy/down summaries, integrity/diagnostic views | Does not feed fact support, fact conflict, relationship construction, or current-belief selection | Validation-only issue surface. |
| Alias list materialization | Alias resolver | `entity_aliases` | Alias visibility/inspection | Does not change canonicalization after materialization | Exposes alias resolver output. |
| Fact conflict handling | Facts, predicate catalog, alias resolver, fact support/current best fact | `fact_conflicts` | Conflict CLI, integrity/explanation surfaces | Does not feed relationship projection or graph validation in finalize order | Explanatory/diagnostic conflict surface over current belief candidates. |

## Projection Interactions Identified

### Replay and finalization ordering is explicit in code

Projection composition is most clearly visible in `StateProjector.finalize(...)`: alias projection happens before measurement retention and inference; inferred facts are generated before final support, relationship, type, graph, alias-list, and conflict projections; graph validation runs after relationship and entity-type assertion construction; conflicts run last. This means stage identity exists, but it is embedded as ordered statements and diagnostic timing labels rather than as a projection shape declaration.

### Current-belief selection is support-centered

Current facts are selected through fact supports. For single-cardinality predicates, `State.get_current_facts(...)` calls `get_best_fact(...)`; `get_best_fact(...)` calls `get_fact_support(...)`; and `get_fact_support(...)` selects one unambiguous best support. Multi-cardinality predicates return representatives for all support groups. Thus `fact_supports`, predicate cardinality, alias resolution, expiration filtering, dimensions, source weighting, confidence, support count, and measurement recency participate in current-belief selection.

Fact conflicts are downstream of this selection logic. Conflict projection groups non-measurement, non-multi predicates by canonical subject/predicate/dimensions, then calls `state.get_best_fact(...)` to identify the winning value when there is an unambiguous current belief. That makes conflicts explanatory about selection outcomes rather than the primary selector.

### Inference uses current observed beliefs as source inputs

Inference is not run over all observed fact values indiscriminately. `_project_inferred_facts(...)` builds `current_observed_facts` using `_current_belief_source_facts(...)`, which projects supports from observed facts, applies predicate cardinality, selects unambiguous best support for single-cardinality predicates, and uses representatives as deterministic inference inputs. This makes inference selection-bearing in its own upstream input choice, and derived facts then influence later support, relationship, entity-type, graph, conflict, and current-fact outputs.

### Relationship construction is fact/catalog-centered

Catalog relationships are projected directly from facts whose values can be interpreted as relationship objects and from relationship-catalog definitions for those predicates. Relationship construction consumes evidence only for suppression of specific Prometheus-derived relationship cases. It does not consume fact conflicts, graph issues, or current entity types. Therefore, existing evidence supports saying that relationship projection is derived interpretation over facts/catalog definitions, not an output of graph validation or conflict handling.

### Entity type construction composes entities, facts, and relationships

Entity type assertions are derived from explicit entity kind, host-like fact predicates, endpoint-looking subjects, relationship-type rules, and unknown fallback assertions. Current entity types are then selected by strongest confidence and assertion count per type. Entity type outputs feed graph validation, but current entity type selection does not feed fact support selection.

### Graph validation is validation-only over projected graph and types

`GraphValidator.validate(...)` iterates over `state.relationships`, looks up relationship definitions, asks the state for current entity types on each side, and emits deterministic issues when expected and actual types mismatch, are unknown, or are ambiguous. It does not mutate facts, relationships, entity type assertions, or current beliefs.

### Diagnostic surfaces are more self-described than projection stages

Diagnostic inventory entries explicitly declare CLI flags, projected-state use, JSON support, record support, record scope, event-ledger writes, cluster mutation, diagnostic-fact reads, and descriptions. Diagnostic shape audit specs then map inventory rows to implementation modules/functions/CLI flags/markers and produce consistency rows. Projection stages have implementation evidence and timing labels, but not comparable declarative fields for consumes, produces, influences, non-influence, and authority boundary.

## Authority Observations

1. **Append-only event history remains authoritative input.** `project_from_state(...)` states that event history remains authority and reused derived state is only an optimization.
2. **`ProjectionStore`/projected state is cache/read model, not truth source.** Architecture docs describe `ProjectionStore` as a deterministic cache of current projected state derived from `EventLedger` and explicitly distinguish it from source of truth.
3. **Current belief is selected, not asserted as absolute truth.** Support aggregation, predicate cardinality, expiration, source type, confidence, and recency drive selected current facts; ambiguity can intentionally result in no single best support.
4. **Graph issues are validation findings.** They describe suspicious or invalid projected relationship/type combinations and carry expected/actual type evidence; they do not rewrite graph or fact state.
5. **Conflicts are explanatory/diagnostic over competing durable claims.** Conflict construction identifies multiple values and optionally a winning current fact; it does not appear to block relationship projection or graph validation.
6. **Inferred facts are derived interpretation.** They are deterministic and source-typed as inferred, and repository docs cap inferred-fact authority below source fact confidence.

## Selection Observations

Selection-bearing concepts supported by implementation evidence:

- `FactSupport` aggregation: groups facts by subject, predicate, dimensions, and value/current sample.
- Predicate cardinality: single predicates select one unambiguous best support; multi predicates keep all support groups.
- Measurement semantics: latest retained/current sample participates differently from durable support aggregation.
- Alias resolution: canonical subject grouping influences support selection for most predicates, while endpoint-scoped predicates opt out.
- Expiration: expired facts are excluded by default from support and conflict projection.
- Source weighting and independent evidence identity: support confidence is aggregated using source-type weights and evidence/fact identity.
- Inference source selection: inferred facts derive from selected current observed facts.
- Entity type current selection: strongest confidence and support count choose current entity type(s), including ambiguity.

Concepts not supported as current-belief selectors in inspected code:

- `fact_conflicts` do not select current beliefs; they call the selection path to explain conflicts.
- `relationships` do not select current facts.
- `graph_issues` do not select facts or relationships.
- `entity_type_assertions` select current entity types, but not current fact values.

## Validation Observations

Graph validation consumes projected catalog relationships and current entity types. It excludes identity relationships, checks subject/object expected types against current entity types, emits warnings for unknown/ambiguous type conditions, emits errors for incompatible known types, and adds hints for some monitored endpoint cases. This supports classifying graph validation as validation-only over derived graph/type projections.

## Candidate Projection-Shape Observations

Existing implementation evidence supports describing many projection stages with the proposed vocabulary:

- **stage**: supported by finalization timing labels and helper-function boundaries.
- **consumes**: inferable from helper function parameters and state fields read.
- **produces**: explicit from `state.<field> = ...` assignments and dataclass output types.
- **influences**: inferable from later stage inputs and public query methods.
- **does_not_influence**: partially supported when finalize order and function bodies show no downstream read path, but this is weaker than positive influence evidence because it depends on scanned code scope.
- **authority boundary**: supported by docs and method comments for event history, projection cache, diagnostics, inference, and validation, but not uniformly declared per projection stage.

The vocabulary is therefore evidence-compatible as an investigation lens. It is not currently an implemented model.

## Supported Conclusions

1. Projection implementation is not immature in the areas reviewed. It includes event replay, cache finalization, alias resolution, measurement retention, inference, support aggregation, conflict projection, catalog relationships, entity type assertions, graph validation, current-fact selection, and read-only inspection surfaces.
2. Projection explanation is weak because the stage graph is implicit. Maintainers can reconstruct it from `finalize(...)`, helper bodies, query methods, docs, and tests, but there is no projection-stage inventory comparable to diagnostic inventory/shape audit.
3. Projection stages can be described with consumes/produces/influences/authority-boundary vocabulary using existing evidence for most positive relationships.
4. `does_not_influence` claims are possible but should be treated as lower-confidence unless backed by tests or exhaustive static analysis, because absence of a read in inspected code is weaker evidence than an explicit boundary declaration.
5. Operational and diagnostic surfaces have stronger visibility contracts than projection concepts. Diagnostic surfaces declare shape metadata and are audited against implementation; projection concepts are visible as outputs but less self-described as composing stages.
6. The difficulty appears primarily to be missing explicit projection shape visibility, not absence of projection machinery.

## Unsupported Conclusions

The reviewed evidence does not support claiming that:

- projection behavior should be redesigned;
- a new projection-shape runtime surface must be implemented;
- graph validation should affect current-belief selection;
- fact conflicts should block relationship projection;
- relationships should be rebuilt from current facts only rather than projected facts;
- diagnostic findings should become cluster truth;
- presentation vocabulary should be promoted into preserved knowledge without implementation evidence.

## Open Questions

- Should projection timing labels in `ProjectionBuildDiagnostics` be treated as stable stage names, or are they only debug labels?
- Which tests, if any, should be considered authoritative for negative influence claims such as “fact conflicts do not influence relationship projection”?
- Should legacy direct string-fact relationships remain described as a projection stage alongside catalog relationships, or only as compatibility behavior?
- Are inferred facts intended to influence all downstream projections exactly like observed facts except through source type/confidence, or are some downstream consumers expected to distinguish them more strongly?
- Is measurement history retention best described as a projection stage, a cache-retention policy, or both?
- Are relationship suppression rules evidence-specific exceptions within relationship projection, or should they be documented as a distinct authority boundary?

## Acceptance Answer

Projection is difficult to understand mainly because projection lacks explicit shape visibility. The implementation is broad enough to answer the core interaction questions when read manually, but the repository does not provide a projection-stage self-model equivalent to the diagnostic inventory and diagnostic shape audit. Existing implementation evidence supports describing many stages in terms of `stage`, `consumes`, `produces`, `influences`, and `authority boundary`; it supports `does_not_influence` more cautiously, because non-influence is inferred from implementation absence rather than declared as a stable contract.

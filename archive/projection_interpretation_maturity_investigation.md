# Projection Interpretation Maturity Investigation

This investigation is documentation-only. It does not implement projection logic, alter schemas, change ontology definitions, add diagnostics, change runtime behavior, or prescribe redesign work.

## Scope and evidence base

The inspected implementation shows projection as a concrete state-construction pipeline, not a hypothetical concept. `State` materializes facts, observed/inferred partitions, aggregate supports, conflicts, aliases, catalog relationships, legacy relationships, entity type assertions, graph issues, evidence, and operational objects. `StateProjector._finalize_projection(...)` is the main construction sequence after event replay.

Primary files inspected:

- `seed_runtime/state.py`
- `seed_runtime/facts.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/inference_catalog.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/confidence.py`
- `seed_runtime/context_views.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/fact_index.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/operational_graph.py`
- `seed_runtime/impact_audit.py`
- `seed_runtime/architecture_conformance_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`

## What projection currently produces

Projection currently produces a `State` read model from append-only events and then derives multiple indexes/read models over that state:

1. **Retained facts.** Durable facts remain; measurement facts are reduced to recent current samples per canonicalized subject/predicate/dimensions according to the configured measurement history limit.
2. **Inferred facts.** Deterministic inference rules can add facts derived from observed facts.
3. **Observed/inferred partitions.** Facts are partitioned into `observed_facts` and `inferred_facts` after inference.
4. **Alias resolver and alias list.** Alias resolution is built from facts before and after inference and then materialized as `entity_aliases`.
5. **Fact supports.** Facts are grouped into support records by subject, predicate, dimensions, and value, with durable and measurement predicates treated differently.
6. **Current belief read model.** `get_fact_support(...)`, `get_best_fact(...)`, and `get_current_facts(...)` select representative current facts from support groups.
7. **Legacy relationships.** Object-like fact values are projected into legacy entity relationship records.
8. **Catalog relationships.** Relationship-catalog definitions project selected predicates into typed relationship edges.
9. **Entity type assertions.** Entity kinds, host-like facts, endpoint-looking subjects, and selected relationships all produce type assertions.
10. **Graph validation issues.** Catalog relationship edges are validated against expected subject/object types using current entity type assertions.
11. **Fact conflicts.** Single-cardinality, non-measurement facts with multiple values under a canonical subject/predicate/dimensions key are reported as conflicts with a selected winner when possible.
12. **Downstream read-only views.** Contradictions, confidence, decision context, source navigation, fact indexes, integrity summaries, knowledge reachability, and audit surfaces consume projected state without becoming projection authority themselves.

## Construction order observed

The finalization order is significant because several concepts consume earlier projections:

```text
alias resolver, initial
measurement evidence scan
measurement history retention before inference
inferred fact projection
alias resolver, post-inference
measurement history retention after inference
observed/inferred partition
measurement provenance pruning
fact support construction
legacy relationship projection
catalog relationship projection
entity type assertion projection
graph issue construction
alias list materialization
fact conflict handling
```

This order supports an interpretation that projection has an integrated **construction layer**, while higher-level semantic interpretation is distributed across read methods and views rather than centralized in one interpreter.

## Projection concepts and interactions

| Concept | Current role | Integrated with | Notable limits |
|---|---|---|---|
| Events | Authoritative input material for state replay. | State fields and later finalization. | Interpretation is mostly in finalization/read models, not raw events. |
| Facts | Main claim substrate. | Supports, inference, aliases, relationships, types, conflicts, views. | Facts can participate differently depending on predicate semantics and catalog membership. |
| Measurement facts | Volatile samples. | Retention, support current-sample selection, expiry, current facts. | Excluded from conflict projection. |
| Durable facts | Persistent claims. | Aggregate support, conflict detection, current facts, relationship/type derivation. | Single-cardinality belief can become unavailable if best support is tied. |
| Inferred facts | Deterministic projection outputs from inference catalog rules. | Alias rebuild, support, relationships, types, conflicts. | Rule language is local predicate/value transformation, not broad semantic reasoning. |
| Aliases | Canonicalization and lookup expansion. | Measurement retention, support queries, conflict grouping, subject resolution. | Relationship projection itself uses fact subjects/values rather than clearly rewriting all relationship endpoints through aliases. |
| Fact supports | Aggregated support groups and support strength. | Current belief selection, source navigation, fact index, knowledge reachability, conflicts indirectly via best-fact selection. | Supports do not directly validate graph semantics or relationship correctness. |
| Fact conflicts | Report multiple current values for exclusive/single-cardinality facts. | Current belief winner, CLI/views, integrity summaries. | They do not appear to suppress relationships, alter type assertions, or feed graph validation directly. |
| Relationship catalog | Bounded vocabulary mapping predicates to relationships and expected types. | Catalog relationship projection, graph validation. | Relationship projection is predicate/catalog driven, not conflict-aware. |
| Entity type assertions | Type evidence from entities, facts, and selected relationship rules. | Current type selection, graph validation. | Type assertions are selected independently of fact conflict records. |
| Graph issues | Validation output over projected relationships and current entity types. | Decision context and integrity/visibility surfaces. | Issues do not mutate projected facts/relationships; they are findings about the graph. |
| Downstream views | Read-only interpretation and presentation. | Context, confidence, contradictions, source navigation, audits. | Each view interprets a subset; no single downstream view explains the whole projection. |

## Where interpretation actually occurs

Interpretation is **distributed**.

### Central construction interpretation

`StateProjector._finalize_projection(...)` centralizes construction sequencing. It decides when aliases exist, when inference runs, when measurements are retained, when supports/relationships/types/issues/conflicts are materialized, and therefore determines which derived products are available to later consumers.

### Support-selection interpretation

Current belief is primarily interpreted through support selection:

- `get_fact_supports(...)` resolves aliases except for endpoint-scoped predicates, filters supports by predicate/dimensions, and may rebuild alias-aware supports on demand.
- `get_fact_support(...)` returns only an unambiguous strongest support group.
- `get_best_fact(...)` selects a representative fact from the winning support group.
- `get_current_facts(...)` uses predicate cardinality: single-cardinality predicates return only one best fact, while multi-cardinality predicates return one representative per support group.

This is the clearest current-belief interpreter in the repository.

### Relationship/type/validation interpretation

Relationship interpretation is catalog-driven: relationship definitions map fact predicates into named edges with expected subject/object types. Entity type interpretation then combines entity declarations, fact predicate heuristics, endpoint subject shape, and relationship-derived type rules. Graph validation then evaluates catalog relationships against selected current entity types.

This forms an integrated chain:

```text
facts -> catalog relationships -> relationship-derived type assertions -> current entity types -> graph issues
```

However, this chain is not visibly governed by `FactConflict` records.

### Downstream view interpretation

Some interpretation happens after state projection:

- `contradictions.py` builds a separate contradiction view over projected facts and optional evidence graph.
- `confidence.py` combines projected facts, evidence graph support, and contradictions into confidence records.
- `context_views.py` selects context facts and issues for decision context.
- `source_navigation.py` turns `state.fact_supports` for `defines`/`imports` into source navigation rows.
- `knowledge_reachability.py` indexes projected facts and support rows into reachability surfaces.
- `impact_audit.py`, `selection_path_audit.py`, `reference_selection.py`, and `architecture_conformance_audit.py` interpret repository/audit artifacts rather than core projection semantics.

These views make projection more observable, but they do not appear to be the central semantic interpreter for supports, conflicts, aliases, relationships, types, and graph issues as one combined object.

## Contradiction and relationship interactions

### How fact conflicts influence relationships

Evidence found: `state.fact_conflicts` is materialized after graph issue construction in finalization. Catalog relationships are projected before conflicts are calculated. The relationship projection path consumes facts, relationship catalog definitions, and evidence for a small suppression case, not projected conflict records.

Conclusion: fact conflicts are implemented and visible, but they do **not** appear to influence relationship projection in the current construction order.

### How relationships influence type assertions

Evidence found: `_project_entity_type_assertions(...)` iterates `state.relationships` and applies `_RELATIONSHIP_TYPE_RULES` for relationships such as `member_of`, `runs_on`, `monitored_by`, and `provides`. The matching side receives a type assertion with source `relationship_projection` and provenance back to the relationship id.

Conclusion: relationships are integrated into type assertion projection for a bounded rule set.

### How type assertions influence graph validation

Evidence found: `GraphValidator.validate(...)` iterates catalog relationships, looks up the relationship definition, obtains current subject/object types via `state.get_current_entity_types(...)`, and checks those actual types against catalog-expected types.

Conclusion: type assertions directly drive graph validation.

### How graph issues influence projected understanding

Evidence found: graph issues are stored in `state.graph_issues` and consumed by downstream views such as decision context. They do not rewrite facts, relationships, aliases, supports, or entity type assertions during projection.

Conclusion: graph issues are integrated as validation findings and visibility signals, not as feedback that changes the projected graph.

### How aliases influence conflict detection

Evidence found: `_project_fact_conflicts(...)` groups facts by `state.alias_resolver.canonical(fact.subject_id)`, predicate, and dimensions. Alias projection therefore can merge fact subjects before conflict detection.

Conclusion: aliases directly influence conflict detection.

### How aliases influence relationship projection

Evidence found: measurement retention and support querying use canonical subjects, and conflict grouping uses canonical subjects. Catalog relationship projection consumes facts and catalog definitions; from inspected evidence, relationship endpoints are formed from fact subjects/values rather than from a conflict-like or support-selected canonical current belief layer.

Conclusion: aliases are strongly integrated with support/current/conflict interpretation, but their influence on catalog relationship projection appears more limited or indirect than their influence on conflicts and current fact queries.

## Relationship to current surfaces

| Surface | Projection concepts visible | Projection concepts implicit or absent |
|---|---|---|
| `current_facts` | Current belief, support selection, predicate cardinality, representative fact choice. | Relationship/type/graph validation context usually absent. |
| `fact_support` | Support groups, confidence, source types, supporting facts, measurement current sample vs durable aggregate. | Graph validation and relationship interpretation absent. |
| `fact_conflicts` | Conflict records, competing values, winning value/best fact. | Relationship suppression or graph feedback absent. |
| `source_navigation` | Fact supports for `defines` and `imports`, representative support/fact ids. | It intentionally does not infer behavior/reachability/ownership. |
| `impact_audit` | Compares observable audit snapshots. | Does not explain state projection concept interactions. |
| `architecture_conformance` | Uses operational graph/audit classes and can classify projection-related code. | Does not interpret fact supports/conflicts/aliases as projection semantics. |
| `reasoning_path` | Reasoning/traceability vocabulary if present in local surfaces. | No evidence that it centralizes projection interpretation. |
| `selection_path` | Selection/explanation vocabulary for why a path or item was selected. | Does not replace current-belief support selection. |
| `reference_selection` | Reference choice for historical comparison domains. | Separate from state projection semantics. |
| `operational_graph` | Operational/module/class relationship visibility. | Describes code structure, not projected knowledge truth. |

## Maturity observations by concept

| Concept | Maturity assessment | Evidence-based rationale |
|---|---|---|
| State projection construction | Implemented and integrated | Event replay plus finalization materializes multiple derived indexes in one ordered pipeline. |
| Fact support aggregation | Implemented and integrated | Supports drive current facts, source navigation, fact index, knowledge reachability, and conflict winner selection. |
| Current belief selection | Implemented and integrated | Single-vs-multi predicate cardinality and unambiguous support selection are explicit. |
| Measurement currentness | Implemented and integrated | Measurement retention, current-sample support, and conflict exclusion are explicit. |
| Inference | Implemented but bounded | Inference rules are deterministic predicate/value transformations and join later support/relationship/type/conflict paths. |
| Alias resolution | Implemented and integrated for facts/support/conflicts | Alias resolver affects measurement retention, support lookup, and conflict grouping. Its effect on relationship endpoints appears less comprehensive. |
| Catalog relationship projection | Implemented and integrated with types/validation | Relationship edges feed relationship-derived type assertions and graph validation. |
| Legacy relationship projection | Implemented but loosely connected | It remains available for older direct-fact relationship queries, while catalog relationships drive newer validation. |
| Entity type assertions | Implemented and integrated with graph validation | Multiple type sources are ranked into current entity types, and validation consumes them. |
| Graph validation | Implemented and integrated as findings | It validates relationship/type compatibility and surfaces issues; it does not feed back into belief selection. |
| Fact conflicts | Implemented and partially integrated | Conflicts use aliases and current best fact selection, but do not appear to alter relationships, types, or graph issues. |
| Contradiction view | Implemented but parallel | `contradictions.py` is separate from `FactConflict`; confidence/context use it, but core relationship projection does not. |
| Confidence aggregation | Implemented as downstream interpretation | It consumes evidence and contradictions to rank facts for context, not to rewrite state projection. |
| Decision context | Implemented as downstream selection | It combines facts, confidence, contradictions, requirements, capabilities, and graph issues for decision-ready output. |
| Whole-projection interpretation | Implemented but distributed / semantically immature at higher layer | No single interpreter combines support, conflict, alias, relationship, type, and graph issue outcomes into one explained projection narrative. |

## Supported conclusions

1. Projection is substantial and real. It produces retained facts, inferred facts, support groups, conflicts, aliases, relationships, entity type assertions, graph validation issues, and many downstream read-only views.
2. Projection is mature at the construction/read-model layer. The finalization pipeline is ordered and the major outputs are materialized on `State`.
3. Current belief selection is mature and support-centered. The most explicit interpretation of “what Seed currently believes” is support aggregation plus unambiguous best-support selection plus predicate cardinality.
4. Relationship/type/validation is an integrated sub-pipeline. Catalog relationships feed relationship-derived type assertions; current entity types feed graph validation.
5. Conflict handling is integrated with aliasing and support selection, but loosely connected to relationship/type/validation semantics. Conflicts describe competing fact values; they do not appear to suppress relationships or alter graph validation.
6. Alias resolution is strong for fact lookup/currentness/conflict grouping, but less clearly a global semantic identity layer for all relationship interpretation.
7. Graph issues are validation findings, not projection feedback. They increase understanding by surfacing suspicious/invalid edges but do not change the projected facts or relationships.
8. Higher-level projection interpretation is distributed among state methods and downstream views. There is no evidence of a single centralized projection interpreter that explains how all concepts combine into an interpreted projection.
9. The most evidence-supported maturity answer is: projection is mostly complete at the state-construction and current-belief layers, while still semantically immature or under-integrated at the higher interpretive layer that would explain supports, conflicts, aliases, relationships, types, and graph validation as one combined meaning.

## Unsupported conclusions

The inspected evidence does **not** support concluding that:

- Fact conflicts currently govern relationship projection.
- Graph validation issues currently rewrite projected understanding.
- Aliases universally canonicalize every relationship endpoint in the same way they influence fact support/conflict queries.
- Relationship projection currently waits for conflict resolution or only projects winning current facts.
- Confidence aggregation changes core projected state.
- Downstream visibility surfaces such as `impact_audit`, `selection_path`, `reference_selection`, or `operational_graph` are the central projection interpreter.
- Projection is merely observation-limited; some concepts are implemented but remain loosely connected at the interpretive layer.

## Open questions preserved by the evidence

1. When a conflict exists for a predicate that also derives a catalog relationship, should the projected relationship reflect all fact values or only current selected belief? Current evidence shows relationship projection happens before conflict projection, but this document does not prescribe a change.
2. Should alias canonicalization be considered an identity layer for relationship endpoints, or only a fact support/current/conflict convenience? Current evidence supports the latter more strongly.
3. Should graph issues remain pure findings, or should any downstream view treat them as belief qualifications? Current evidence shows findings are surfaced, not fed back.
4. How should the repository distinguish `FactConflict` from the separate contradiction view in `contradictions.py` when explaining projection maturity? Current evidence shows both exist with overlapping but different purposes.
5. Which downstream surface, if any, should be considered the canonical human explanation of an interpreted projection? Current evidence suggests none currently owns the whole explanation.

## Short answer to acceptance questions

**What does projection currently do?** It replays events into state, retains current fact history, derives inferred facts, aggregates supports, materializes aliases, projects relationships, derives entity types, validates the graph, and reports fact conflicts, then downstream views interpret parts of that state.

**How do major concepts interact?** Supports drive current facts and conflict winners; aliases influence support lookup, measurement retention, and conflict grouping; relationships drive selected type assertions; type assertions drive graph validation; graph issues and conflicts are surfaced as findings rather than feedback into relationship construction.

**What appears integrated?** State construction, supports/current belief, measurement handling, relationship-to-type-to-validation, alias-to-support/conflict, and downstream visibility of supports/issues/conflicts.

**What appears isolated or loosely connected?** Fact conflicts are loosely connected to relationship/type/graph interpretation; graph issues do not affect projected beliefs; contradiction/confidence/context are downstream parallel interpretations; operational/reasoning/selection/reference surfaces do not centralize core projection interpretation.

**Is projection mostly complete and observation-limited, or semantically immature despite substantial implementation?** The evidence supports a mixed answer: projection is complete and mature at the construction/current-belief layers, but higher-level projection interpretation remains semantically immature or under-integrated because no single implemented layer explains how supports, conflicts, aliases, relationships, entity types, and graph validation combine into one interpreted projection.

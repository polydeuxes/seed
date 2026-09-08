# Projection Self-Description Investigation

## Scope

This investigation asks how projection describes itself today. It is documentation-only: it does not implement projection inventories, projection shape declarations, projection surfaces, ontology changes, or architecture changes.

Repository authority wins. The investigation treats implementation, tests, and existing repository documents as evidence, and distinguishes declared repository-visible self-description from reconstruction performed by reading implementation order.

## Evidence Reviewed

Primary projection evidence:

- `StateProjector` and `State` in `seed_runtime/state.py`.
- `ProjectionBuildDiagnostics` timing labels in `seed_runtime/state.py`.
- `ProjectionStore` boundary text and snapshot constants in `seed_runtime/projection_store.py`.
- projection-facing query and CLI surfaces referenced by existing investigations.
- tests covering projection store/event-ledger ownership boundaries and projection-facing read models.

Comparison surfaces:

- diagnostic inventory in `seed_runtime/diagnostic_inventory.py`.
- diagnostic shape audit in `seed_runtime/diagnostic_shape_audit.py`.
- operational graph in `seed_runtime/operational_graph.py`.
- architecture conformance and component audit implementation specs.
- `reasoning_path`, `selection_path`, `reference_selection`, and `operational_story` surfaces.

Related investigations reviewed:

- `docs/projection_interpretation_maturity_investigation.md`.
- `docs/projection_shape_visibility_investigation.md`.
- `docs/projection_self_description_observation.md`.
- traceability, significance, baseline, and reference-selection investigations that characterize reasoning/selection/reference visibility.

## How Projection Describes Itself Today

Projection describes itself through several partial mechanisms, none of which is a first-class projection self-model.

### 1. Class and dataclass docstrings

Projection exposes important concepts through type names and docstrings:

- `ProjectionBuildDiagnostics` is explicitly optional and non-authoritative timing/counter output.
- `EntityTypeAssertion` is one evidence-backed entity classification assertion.
- `EntityRelationship` is a catalog-defined semantic edge projected deterministically from a fact.
- `GraphValidationIssue` is a suspicious or invalid projected relationship edge.
- `LegacyEntityRelationship` is a backward-compatible direct string-fact projection.
- `EntityAlias` is an explicit alias edge projected from alias-like facts.
- `AliasResolver` is a deterministic identity resolver built only from explicit alias facts.
- `StateProjector` rebuilds inspectable state from ledger events.

These declarations are real self-description. They identify projection products and some authority boundaries, especially deterministic derivation, evidence backing, graph validation status, and alias-source limits.

They do not declare a projection-stage model. They do not answer, as structured data, which stage consumes which fields, which stage produces a given output, which downstream outputs are influenced, or which stage has selection authority.

### 2. Finalization timing labels

`StateProjector.finalize(...)` gives the clearest repository-visible stage vocabulary through timing labels and assignment order. The labels name:

1. initial alias projection;
2. measurement evidence scan;
3. measurement history retention before inference;
4. inferred fact projection;
5. post-inference alias projection;
6. measurement history retention after inference;
7. observed/inferred fact partition;
8. inferred fact partition;
9. measurement provenance pruning;
10. fact support construction;
11. legacy relationship projection;
12. catalog relationship projection;
13. entity type assertion projection;
14. graph issue construction;
15. alias list materialization;
16. fact conflict handling.

This is the closest thing projection has to a stage list. However, it is diagnostic timing vocabulary embedded in control flow, not a projection inventory. The timing labels are not accompanied by stable fields for consumes, produces, authority, selection behavior, recordability, or mutation boundary.

### 3. State fields and query methods

Projection exposes outputs through `State` fields and methods. Current-belief and visibility methods include:

- `get_current_facts(...)`;
- `get_fact_supports(...)`;
- `get_fact_support(...)`;
- `get_fact_conflicts(...)`;
- `get_stale_facts(...)`;
- `get_stale_fact_refresh_recommendations(...)`;
- relationship and entity-type traversal helpers elsewhere in `State`.

These methods let callers inspect projected products and some selected current beliefs. They describe use enough for consumers to query projection, but they do not describe projection provenance at the level of “this stage produced this result from these inputs.”

### 4. Projection cache boundaries

`ProjectionStore` describes itself as a snapshot/cache owner: event ledgers own append-only historical events; projection stores own reusable snapshots of projected state derived from those events. `StateProjector.project_from_state(...)` similarly states that event history remains authority and derived state reuse is an optimization.

This is strong authority self-description for the event/projection-store boundary. It is not a full self-model of the internal projection stages.

### 5. Diagnostics and downstream views over projection

Projection-adjacent CLI/read surfaces expose projected facts, supports, conflicts, unsupported facts, graph issues, state summaries, current facts, and capability inventory. These surfaces make projection outputs visible. Some are registered diagnostic surfaces with shape metadata.

They are downstream visibility, not projection-stage self-description. They usually answer “what is the current projected output?” rather than “which projection stage created this output and under what authority?”

## Explicit Projection Concepts

The repository explicitly declares these projection concepts:

| Concept | Explicit evidence | What is declared |
| --- | --- | --- |
| Projected `State` | `StateProjector` docstring and methods | Inspectable state is rebuilt from ledger events. |
| Event authority | `project_from_state(...)` docstring | Event history remains authority; derived state reuse is optimization. |
| Projection cache | `projection_store.py` module docstring | Projection stores own reusable snapshots derived from events, not append-only history. |
| Projection diagnostics | `ProjectionBuildDiagnostics` | Timing/counter output is optional and non-authoritative. |
| Alias resolver | `AliasResolver` docstring and alias predicates | Alias resolution is deterministic and built only from explicit alias facts. |
| Entity aliases | `EntityAlias` | Alias edges are explicit and projected from alias-like facts. |
| Fact supports | `FactSupport` state field/query methods | Aggregated support groups are queryable and drive current belief. |
| Current facts | `get_current_facts(...)` | Current facts are selected through predicate cardinality and best support logic. |
| Fact conflicts | `FactConflict` state field/query methods | Projected conflicts are queryable findings over competing facts. |
| Catalog relationships | `EntityRelationship` | Semantic edges are catalog-defined and deterministically projected from facts. |
| Legacy relationships | `LegacyEntityRelationship` | Direct string-fact relationships remain backward-compatible read model output. |
| Entity type assertions | `EntityTypeAssertion` | Entity classifications are evidence-backed assertions. |
| Graph validation issues | `GraphValidationIssue` | Issues are suspicious/invalid projected relationship edges. |
| Measurement staleness | stale-fact query methods | Expired/stale facts can be listed and mapped to refresh recommendations. |

These declarations show projection is not hidden. It has named products, methods, and some boundary docstrings.

## Implied Projection Concepts

The following concepts are mostly implied by implementation reconstruction:

| Implied concept | Where it is reconstructed from | Why it is not self-described |
| --- | --- | --- |
| Stage graph | `finalize(...)` order and helper calls | There is no projection-stage registry or stage object. |
| Stage consumes | helper parameters and state fields read | Not declared as structured metadata. |
| Stage produces | assignments to `state.<field>` | Explicit in code, not exposed as a discoverable model. |
| Stage influence | later reads of earlier outputs | Requires code tracing. |
| Non-influence | absence of reads in inspected code | Requires negative inference; not declared. |
| Selection-bearing stages | support selection, inference source selection, entity-type current selection | Distributed across methods/helpers. |
| Validation-only boundaries | graph validator behavior and finalize order | Inferred from lack of mutation and output type. |
| Output provenance by stage | finalization assignment locations | Not attached to individual output records. |
| Interpretation selected by a stage | best-support and current-type selection logic | No record on the selected output saying why that stage selected it. |
| Relationship validation provenance | `GraphValidator.validate(...)` output fields and relationship IDs | Issues retain relationship/fact IDs, but not a general projection-stage provenance model. |

## Projection Boundaries

### Explicit boundaries

Projection has several explicit boundaries:

1. **Event ledger versus projection cache.** Event history is authority; projection reuse is an optimization, and projection stores own snapshots derived from events.
2. **Projection diagnostics versus authority.** Build diagnostics are optional and non-authoritative.
3. **Alias authority.** Alias resolution is built only from explicit alias facts, with endpoint identity boundary behavior in code.
4. **Graph validation output.** Graph issues are validation findings over projected relationships and types, not graph rewrites.
5. **Read-only downstream diagnostics.** Many operational/diagnostic surfaces declare no event-ledger writes and no cluster mutation through diagnostic inventory.

### Inferred boundaries

Other boundaries must be inferred:

1. **Relationship projection versus current-fact selection.** Catalog relationships are built from facts/catalog definitions and do not appear to consume `fact_conflicts` or `graph_issues`; this is inferred from finalization order and helper bodies.
2. **Fact conflicts versus relationship suppression.** Conflicts are produced after relationships and graph issues, so they do not appear to suppress those outputs.
3. **Entity types versus fact support.** Entity type assertions feed graph validation, but current entity type selection does not appear to feed fact support selection.
4. **Graph validation versus mutation.** Validation produces `graph_issues`; non-mutation is inferred from the validator's output-only behavior and downstream tests, rather than from a projection-stage declaration.
5. **Inference downstream reach.** Inferred facts re-enter `state.facts` and therefore influence support, relationships, types, graph issues, and conflicts; this is reconstructed from placement before those stages.

## Projection Authority Visibility

Projection authority visibility is strongest at the outer boundary and weaker inside the projection pipeline.

Strongly visible authority:

- append-only event history is the input authority;
- `ProjectionStore` is a reusable derived snapshot/cache, not event authority;
- `ProjectionBuildDiagnostics` is non-authoritative;
- graph issues are findings over projected relationships/types;
- diagnostic surfaces registered in inventory declare whether they write the event ledger or mutate cluster state.

Weakly visible authority:

- which projection stage has authority to select a current fact;
- which stage has authority to select current entity type;
- whether timing labels are stable stage names or only debug labels;
- which outputs are authoritative enough for later stages versus only explanatory;
- how inferred facts should be interpreted downstream beyond source type/confidence;
- whether a particular output can answer “who produced me?” without code inspection.

The result is an uneven authority model: repository-visible authority exists, but it is boundary-oriented rather than stage-oriented.

## Comparison With Operational and Diagnostic Surfaces

Operational/diagnostic surfaces describe themselves more explicitly than projection stages.

### Diagnostic inventory

Diagnostic inventory entries declare:

- surface name;
- CLI flags;
- projected-state usage;
- repository-file usage;
- JSON support;
- record support;
- record scope;
- diagnostic fact emission;
- cluster fact emission;
- event-ledger writes;
- cluster mutation;
- diagnostic-fact reads;
- human-readable description.

This lets the repository answer questions such as: “Does this surface use projected state?”, “Can it record?”, “Does it write the event ledger?”, and “Is it cluster-mutating?” without reading the implementation body.

Projection has no equivalent stage inventory. It cannot answer the same class of questions for “catalog relationship projection” or “fact support construction” as structured repository-visible metadata.

### Diagnostic shape audit

Diagnostic shape audit maps diagnostic names to implementation modules, build/format/json functions, CLI flags, file markers, diagnostic fact-read markers, and mutation markers. It can check whether inventory and implementation remain aligned.

Projection has no equivalent shape audit for stage declarations. The repository can time finalization steps, but it does not audit that declared projection stages consume/produce the fields they claim to consume/produce, because there are no such declarations.

### Operational graph, architecture conformance, and component audit

Operational graph and conformance surfaces expose node/edge classifications, evidence categories, confidence reasons, architecture-versus-operation comparison, component consumers, and unresolved questions. They are still read models, but they present explicit explanatory structure about their own domain.

Projection exposes products and query methods. It does not present an equivalent projection graph that says, for example, “fact support construction consumes retained facts and produces `fact_supports`, which are consumed by current-fact selection and fact-conflict handling.” That statement can be reconstructed, but projection does not currently answer it directly.

### Reasoning, selection, reference, and operational story surfaces

`reasoning_path`, `selection_path`, `reference_selection`, and `operational_story` show a pattern: operational surfaces increasingly explain derivation, selection, comparison reference, and narrative composition. They also have diagnostic inventory/shape-audit metadata.

Projection participates as substrate for many of those surfaces, but projection itself does not expose a comparable self-description of derivation path, selection path, or reference/authority boundary for its internal stages.

## Can Projection Answer the Self-Knowledge Questions Today?

| Question | Can projection answer directly? | Current evidence path |
| --- | --- | --- |
| What stages exist? | Partially | Timing labels and `finalize(...)` order name stages, but no projection-stage inventory exists. |
| What does each stage consume? | No, not directly | Reconstruct from helper parameters and state reads. |
| What does each stage produce? | Partially | State assignments and dataclass types identify outputs; not exposed as structured stage metadata. |
| What authority does each stage possess? | Mostly no | Outer event/cache boundaries are explicit; per-stage authority is inferred from code and docs. |
| What stage produced a particular output? | Partially | Field assignments identify producers for state-level collections; individual records generally do not carry producer-stage provenance. |
| What stage selected a particular interpretation? | Mostly no | Current-fact and type selection logic exists, but selected outputs do not generally carry selection-stage explanations. |
| What stage validated a particular relationship? | Partially | Graph issues identify relationships/facts and validation details; the general answer requires knowing `GraphValidator` is invoked during graph issue construction. |

## Relationship To Visibility

Projection is difficult to understand primarily because its behavior is visible but not self-described as a coherent projection model.

It is not completely hidden:

- projection products have names;
- finalization order is visible;
- timing labels expose stage-like names;
- query methods expose selected outputs;
- CLI/read surfaces expose many projected products;
- tests preserve some boundaries.

It is not merely disorganized presentation:

- the implementation order is coherent;
- earlier investigations reconstructed a plausible stage composition;
- projection concepts have consistent products and consumers.

The main gap is self-description:

- projection does not expose a first-class stage inventory;
- projection does not expose a stage shape audit;
- projection does not attach stage provenance to individual outputs;
- projection does not declare consumes/produces/influences/non-influences as repository-visible metadata;
- projection authority declarations are concentrated at outer boundaries and scattered in docstrings, tests, and docs.

## Relationship To Existing Work

Prior investigations required manual reconstruction.

`projection_interpretation_maturity` reconstructed what projection produces, the significance of finalization order, and interactions among facts, supports, aliases, conflicts, relationships, entity types, graph issues, and downstream views. Projection itself did not provide that full interpretation as a self-report.

`projection_shape_visibility` reconstructed a table of stages, consumes, produces, influence, non-influence, and authority boundaries. The document explicitly treated those names as descriptive and noted that the vocabulary was not an implemented model.

`reasoning_path`, `selection_path`, `reference_selection`, `architecture_conformance`, and `operational_story` demonstrate that the repository can expose derivation/selection/reference/composition information when a surface is intentionally built for that purpose. Projection currently lacks a comparable internal projection-oriented surface.

The explanatory gaps that remained were not “projection does nothing” gaps. They were “projection cannot describe itself at the stage/provenance/authority level without implementation inspection” gaps.

## Supported Conclusions

1. Projection has substantial repository-visible behavior and named products.
2. Projection does possess partial self-description through docstrings, type names, timing labels, state fields, query methods, cache boundary docs, diagnostic outputs, and tests.
3. Projection does not possess a first-class repository-visible self-model comparable to diagnostic inventory plus diagnostic shape audit.
4. Projection stages are currently understood primarily through implementation reconstruction: finalization order, helper bodies, state assignments, query methods, tests, and timing labels.
5. Projection is difficult to understand because its behavior is visible but not organized into self-description that answers stage, provenance, selection, influence, and authority questions directly.
6. Projection authority is most explicit at the event-ledger/projection-cache boundary and weakest at per-stage internal boundaries.
7. Operational and diagnostic surfaces expose richer self-description: inventory declarations, shape-audit mappings, surface classifications, mutation boundaries, record scopes, and implementation mappings.
8. Existing projection investigations did require manual reconstruction; projection could not answer their full questions itself as repository-visible self-knowledge.

## Unsupported Conclusions

The reviewed evidence does not support claiming that:

- projection lacks implementation maturity;
- projection behavior is hidden or unknowable;
- projection outputs are untrustworthy merely because self-description is weak;
- timing labels are stable public stage declarations;
- every inferred non-influence relationship is a guaranteed architectural contract;
- projection should be redesigned;
- projection inventories, shape declarations, or new surfaces should be implemented;
- ontology or architecture changes are required by this investigation.

## Open Questions

- Are `ProjectionBuildDiagnostics` timing labels intended to be stable enough for users to treat as stage names?
- Which projection boundaries are contractual, and which are current implementation facts?
- Should individual projected outputs carry producer-stage provenance, or is field-level provenance sufficient for the current repository? This investigation does not recommend either answer.
- Is inferred-fact downstream authority fully described by source type/confidence, or are additional boundaries embedded in consumers?
- Which negative influence claims have test coverage, and which are only code-inspection conclusions?
- Are legacy relationship projection and catalog relationship projection intended to remain separate conceptual stages, or is that merely compatibility structure?

## Acceptance Answer

Projection currently possesses a fragmented, partial repository-visible self-description, not a first-class repository-visible self-model.

Projection can name many products and expose many outputs. It can reveal a stage-like order through finalization timing labels. It explicitly describes outer authority boundaries such as event history versus projection cache. But it cannot directly answer most internal self-knowledge questions—what each stage consumes, produces, influences, validates, selects, or authorizes—without manual implementation reconstruction.

Therefore, projection is currently understood primarily through implementation reconstruction. The difficulty is not that projection behavior is absent or completely hidden. The difficulty is that projection behavior is visible but incompletely and implicitly self-described.

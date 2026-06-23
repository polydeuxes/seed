# Observation Model Implementation Audit

## Purpose

This audit reconciles the candidate observation model against implementation evidence in the repository. It does not add a new visibility system, operation, observer, projection, diagnostic, or ontology. It inventories what the code and tests already implement.

Candidate model under audit:

```text
observed material
    x
prerequisite evidence
    x
observation operation
    ->
bounded visibility output
```

Repository implementation evidence wins over prior investigation conclusions.

## Implementation evidence reviewed

Primary implementation surfaces reviewed:

- `seed_runtime/documentation_structure.py` for repository Markdown document observation, structural recurrence, structural drilldown, and JSON/text rendering.
- `seed_runtime/diagnostic_inventory.py` for registered diagnostic and audit surfaces.
- `seed_runtime/diagnostic_shape_audit.py` for static implementation specs and diagnostic shape consistency checks.
- `seed_runtime/observation_inventory.py` for AST-discovered observation providers, predicates, and predicate families.
- `seed_runtime/classification_coverage.py` for projected entity classification coverage and unknown-contributor visibility.
- `seed_runtime/operational_surface_inventory.py`, `seed_runtime/consumer_dependency_audit.py`, `seed_runtime/emitter_consumer_audit.py`, `seed_runtime/emitter_attribution_audit.py`, and `seed_runtime/component_audit.py` as implementation-backed meta-visibility surfaces over CLI surfaces, emitters, consumers, and components.
- Tests for the above surfaces, especially `tests/test_documentation_structure.py`, `tests/test_diagnostic_inventory.py`, `tests/test_diagnostic_shape_audit.py`, `tests/test_observation_inventory.py`, and `tests/test_classification_coverage.py`.

Prior investigation documents reviewed for reconciliation:

- `docs/repository_visibility_layer_reconciliation.md`
- `docs/lexical_recurrence_visibility_investigation.md`
- `docs/observation_operation_reconciliation_investigation.md`
- `docs/observation_operation_boundary_investigation.md`
- `docs/structural_recurrence_visibility_investigation.md`
- `docs/structural_drilldown_investigation.md`
- `docs/structural_membership_investigation.md`
- `docs/structural_coverage_visibility_investigation.md`
- `docs/repository_shape_coverage_investigation.md`
- `docs/documentation_structure_recurrence_surface_review.md`
- `docs/documentation_structure_phase_3_investigation.md`

Commands used during this audit:

```bash
rg --files
rg -n "repository_visibility_layer_reconciliation|lexical_recurrence|observation_operation|drilldown|membership|coverage|recurrence|distribution|material" .
rg --files docs | rg 'repository_visibility_layer_reconciliation|observation_operation|recurrence|drilldown|membership|coverage|documentation_structure'
python scripts/seed_local.py --observation-inventory --json
python scripts/seed_local.py --documentation-structure --recurrence --summary-only --json
python scripts/seed_local.py --diagnostic-inventory --json
```

## Executive finding

The implementation already supports a narrower but stronger model than several architectural investigations suggest.

Implemented today:

- **Structure** as a first-class observed material, especially Markdown documentation structure.
- **Operational/diagnostic surfaces** as observed material in meta-audit inventories.
- **Projected entity classification state** as observed material for coverage diagnostics.
- **Observation provider/predicate families** as observed material through AST inventory.
- **Relationship/evidence-like graph issues and relationship categories** as projected-state audit material in classification coverage and graph issue summaries.
- **Measurements** as factual observation predicates and counts in projected diagnostics, but not as a general `measurement x distribution` observation model.
- **Events** as state/projection inputs and event-ledger writes for some diagnostics, but not as a general event-observation material class for recurrence/distribution/drilldown.
- **Language** is investigated but is not implemented as a lexical recurrence surface.
- **Artifact** is only partially implemented, mostly through document/file paths and operational surface artifacts; it is not implemented as a general artifact material class.

Operations implemented today:

- **Inventory/membership** is widely implemented, though often named as inventory rather than membership.
- **Recurrence** is fully implemented for documentation structure.
- **Distribution** is implemented for several bounded count surfaces: documentation recurrence distributions, classification distributions, unknown predicate/category rankings, observation predicate families, and diagnostic/audit summaries.
- **Drilldown** is fully implemented only for exact documentation section-label structure; partial drilldowns exist elsewhere as examples, issue categories, source paths, implementation evidence, and top contributors.
- **Coverage** is implemented for entity classification coverage and diagnostic/operational surface visibility coverage; it is partially implemented for documentation structure through missing-common-section and corpus-count views.

The architecture is ahead of implementation for general material/operation matrices. The implementation is ahead of architecture in recognizing operational surfaces, diagnostic shapes, emitters, consumers, and component dependencies as observable material.

## Implemented observed material classes

### 1. Structure — implemented

Documentation structure is the strongest implemented material class. The implementation explicitly states it is read-only structural observation for repository Markdown documentation and defines a boundary that forbids prose interpretation, claim extraction, authority inference, shape inference, event-ledger writes, and repository mutation.

Implemented structural units include:

- document path
- line count, byte count, blank/nonblank line counts
- front matter presence and keys
- heading records with level, text, and line number
- section records with start/end lines, level, parent heading path, and child counts
- link records with raw targets and local-doc classifications
- code block records with info string, language, start/end lines, and closure
- structure status

This is fully implementation-backed. It is not merely an architectural conclusion.

### 2. Operational/diagnostic surfaces — implemented

The diagnostic inventory registry implements operational surfaces as observable material. Each diagnostic entry records its name, CLI flags, whether it uses projected state or repository files, JSON/record support, record scope, event-ledger writes, cluster mutation, diagnostic fact emission, and description.

The diagnostic shape audit adds implementation specs for these surfaces, including module path, build/format/json/record functions, CLI flags, JSON flags, repo-file markers, diagnostic-fact read markers, and mutation markers. This means diagnostic surfaces are not just operator-facing commands; they are inventoryable and shape-auditable implementation material.

### 3. Observation providers, predicates, and families — implemented

`observation_inventory` implements an AST-backed inventory over provider classes under `seed_runtime/`. It discovers classes implementing `collect()`, extracts observation predicate literals, groups predicates by prefix family, and emits providers, predicates, families, counts, and metadata describing how discovery was performed.

This is an implementation-backed material class best named **observation surface material** or **observation predicate material**. It overlaps with relationship evidence and measurements when predicates describe relationships or measured values, but the implemented inventory unit is provider/predicate/family rather than semantic measurement or relationship type.

### 4. Projected entity classification state — implemented

`classification_coverage` observes projected entity classification state. It counts total entities, classified entities, unknown entities, unknown percentage, distribution by classification, catalog type counts, unknown-subject/object graph issues, both-unknown issues, concrete mismatch issues, top unknown predicates, unknown predicate examples, top unknown relationship categories, and top unknown graph issue categories.

This is an implemented **coverage material** over projected state. It also exposes relationship/evidence-like material through graph issues and relationship categories.

### 5. Relationship evidence — partially implemented

Relationship evidence exists in implementation, but not as a general observation-model material class.

Implemented evidence:

- Graph validation issues are counted and categorized in classification coverage.
- Relationships involving unknown entities are grouped by relationship kind.
- Consumer, emitter, attribution, component, and operational graph audits inventory implementation-backed edges among emitters, consumers, components, and surfaces.

Not implemented:

- A general `relationship evidence x recurrence` operation.
- A general relationship-evidence drilldown with source-location provenance for arbitrary relationships.
- A normalized relationship-evidence material registry mapped into the candidate observation matrix.

### 6. Measurements — partially implemented

Measurements exist as values and counts, but not as a general observed material class.

Implemented evidence:

- Observation predicates include measurement-like families such as CPU counts, disk/free bytes, filesystem size/available bytes, memory totals, listener ports, and process attributes.
- Documentation structure includes line counts, byte counts, blank/nonblank counts, section counts, heading depth, and code-fence counts.
- Classification coverage includes entity counts, unknown percentages, and category counts.

Not implemented:

- A first-class measurement material class with generic recurrence, distribution, drilldown, coverage, denominator, and unit handling.
- A general `measurement x distribution` operation beyond local surfaces.

### 7. Events — partially implemented, mostly as ledger/projection input

Events exist in the runtime and ledger boundary, but the observation model does not currently expose events as a general observed material class.

Implemented evidence:

- Diagnostic inventory records whether a diagnostic writes the event ledger and whether it mutates cluster state.
- Classification coverage can record diagnostic facts with `record_scope="diagnostic_run"` and `mutates_cluster=false` according to the registry.
- State projection code consumes events to materialize projected state.

Not implemented:

- Event recurrence as a general visibility operation.
- Event distribution/drilldown/membership/coverage surfaces for event classes.
- Event corpus boundaries and denominators as an observation model cell.

### 8. Language — investigated, not implemented

Prior lexical recurrence investigations describe exact-language recurrence as a possible observable operation, but no implementation-backed CLI or module currently provides a lexical recurrence surface. Documentation structure records heading text and section labels, but that is structural label material, not general lexical recurrence over prose or terms.

### 9. Artifact — partially implemented

Artifacts are visible mainly as paths, documents, audit snapshots, and implementation files.

Implemented evidence:

- Documentation structure observes Markdown document paths and selected documents.
- Diagnostic inventory observes CLI flags and module-backed diagnostic surfaces.
- Audit snapshot/compare surfaces observe local audit snapshot artifacts.
- Component and emitter/consumer audits observe files/modules as implementation evidence.

Not implemented:

- A general artifact material class with recurrence/distribution/drilldown/membership/coverage operations across arbitrary repository artifacts.

## Implemented observation operations

### Recurrence

Fully implemented for documentation structure.

The recurrence report counts repeated section labels, front matter keys, heading depths, code fence languages, link target classes, skeleton signatures, common section labels, documents missing common sections, and structural outliers. It also emits recurrence distributions and applies configurable min-count/top/limit bounds.

Partially or implicitly implemented elsewhere:

- Observation inventory counts providers per predicate and predicates per family, which is a recurrence-like count of predicate occurrence across providers, but the operation is exposed as inventory rather than recurrence.
- Diagnostic inventory counts surfaces and flags implicitly through inventory rows, not a recurrence operation.
- Classification coverage counts distributions and top unknown contributors, not recurrence over repeated observed material across a corpus.

### Distribution

Implemented in several bounded forms:

- Documentation recurrence distributions by occurrence-count buckets.
- Classification distribution by entity type and unknown percentage.
- Unknown predicate, relationship category, and graph issue category top counts.
- Observation inventory family/predicate/provider counts.
- Diagnostic shape audit summary counts by status.

Distribution is implemented as local count surfaces, not yet as a generic observation operation available for any material class.

### Drilldown

Fully implemented for exact documentation section-label drilldown. The accepted `--where` grammar supports only `section-label:<exact label>`, and the drilldown report returns category, key, occurrences, document count, and matching path/line/depth records.

Partially implemented elsewhere:

- Classification coverage includes unknown predicate examples and top contributors, but not source-location drilldown to all supporting facts.
- Diagnostic shape audit can report per-diagnostic field rows, which is a shape-audit drilldown but not named as an observation-model drilldown.
- Emitter/consumer and component audits expose implementation evidence paths and relationships, which behave as operational drilldown over implementation surfaces.

Not implemented:

- General drilldown for arbitrary structural rows beyond section labels.
- Lexical recurrence drilldown.
- Relationship-evidence drilldown for all relationships.
- Measurement drilldown with source/unit/range provenance.

### Membership

Implemented primarily as inventory and selection rather than under the operation name `membership`.

Implemented membership-like surfaces:

- Documentation structure selects matching documents and emits document/section/link/code-block membership in a bounded corpus.
- Observation inventory groups predicates into families and providers into predicate provider sets.
- Diagnostic inventory declares each surface's membership in the diagnostic registry.
- Operational surface inventory and visibility coverage audit compare discovered CLI surfaces against declared diagnostic inventory membership.
- Classification coverage groups entities into known/unknown classification sets.

Missing:

- A general operation named membership with a common report shape across materials.
- Explicit corpus-boundary/denominator metadata for all membership surfaces.

### Coverage

Implemented for specific domains:

- Entity classification coverage is fully implemented as a diagnostic over projected entity state.
- Visibility coverage audit compares discovered operational surfaces with diagnostic inventory visibility.
- Documentation recurrence has partial structural coverage through common-section presence/missing counts and output document counts.
- Diagnostic shape audit covers registry declarations against implementation specs by status.

Not implemented:

- General material coverage for all candidate material classes.
- Repository-wide artifact/structure/language/relationship/measurement coverage matrix.
- Lexical coverage.

### Inventory

Inventory is an implemented operation even though it was not listed in the candidate operation examples.

Implemented inventory surfaces include:

- diagnostic inventory
- observation inventory
- operational surface inventory
- capability/rule/catalog inventories elsewhere in the repository
- documentation structure inventory of document features

Architecturally, this is a mismatch: implementation repeatedly uses inventory as a primary visibility operation, while the candidate operation list emphasizes recurrence, distribution, drilldown, membership, and coverage.

### Audit/shape audit

Audit is also an implemented operation that the candidate model does not explicitly recognize.

Implemented audit surfaces compare declared shape against implementation evidence, emit consistency/mismatch/warning/unknown statuses, and inventory implementation markers. This is stronger than ordinary inventory because it reconciles expected shape against code evidence.

## Implemented prerequisite evidence

### Strongly implemented prerequisite evidence

- **Occurrence records:** documentation sections, headings, links, code blocks, observed predicates, diagnostic rows, graph issues, and unknown predicate examples.
- **Source locations:** documentation heading/section line numbers and drilldown path/line/depth records.
- **Line numbers:** implemented for documentation headings, sections, and code blocks.
- **Ranges:** implemented for documentation sections and code blocks via start/end lines.
- **Corpus boundaries:** implemented for documentation docs corpus and projected entity set, but inconsistently surfaced across all diagnostics.
- **Denominators:** implemented for documents, entities, classified/unknown counts, provider/predicate/family counts, and audited diagnostics.
- **Membership sets:** implemented for providers per predicate, predicates per family, unknown entity sets, documents missing common sections, and diagnostic registry entries.
- **Normalization rules:** implemented locally, such as predicate-family prefix extraction, exact section-label matching, code-fence language normalization to `none`, classification order, and diagnostic registry declarations.
- **Boundary declarations:** implemented for documentation structure and diagnostic registry fields such as read-only, event-ledger writes, record scope, and cluster mutation.

### Partial prerequisite evidence

- **Source-location provenance outside documentation structure:** file/module paths are available for implementation audits, but line-level provenance is not universal.
- **Corpus boundaries for operational surfaces:** diagnostic inventory and operational surface inventory define surfaces by implementation discovery, but not every audit exposes the same denominator vocabulary.
- **Measurement units:** some predicates encode units in names, e.g. `_bytes`, but there is no general unit metadata registry for measurement operations.
- **Relationship source evidence:** graph issue categories and relationship kinds are visible, but arbitrary relationship source locations are not uniformly exposed.

### Missing prerequisite evidence for candidate expansions

- Lexical token/phrase occurrence records across corpus prose.
- Lexical normalization rules and explicit non-semantic boundaries for implemented output.
- Relationship recurrence denominators and relationship occurrence records independent of graph validation issues.
- Measurement distribution denominators and unit metadata across all measurement-like predicates.
- Event-class corpus boundaries and event occurrence records for event recurrence/distribution/drilldown.

## Material/operation support matrix

Status meanings:

- **Fully implemented:** explicit implementation and tests/CLI support for this material-operation pair.
- **Partially implemented:** some implementation evidence exists, but scope is narrow or report shape is not general.
- **Implicitly implemented:** behavior exists under another name or as a supporting count, but not as an explicit operation.
- **Not implemented:** no implementation-backed evidence found.

| Material class | Recurrence | Distribution | Drilldown | Membership | Coverage | Inventory/Audit |
| --- | --- | --- | --- | --- | --- | --- |
| Structure/documentation structure | Fully implemented for section labels, front matter keys, heading depths, code fence languages, skeleton signatures, common/missing sections, outliers | Fully implemented within recurrence report | Fully implemented for exact section-label only; partial for other structural units | Partially implemented through document/section/link/code-block records and filters | Partially implemented through document counts and missing common sections | Fully implemented through documentation structure surface and diagnostic registry |
| Language/lexical material | Not implemented | Not implemented | Not implemented | Not implemented | Not implemented | Investigated only |
| Artifact/repository files | Implicitly implemented through document path counts and audit snapshots | Partially implemented through docs counts and audit snapshot listing/comparison | Partially implemented through selected document and implementation evidence paths | Partially implemented through docs corpus and registries | Partially implemented for operational surface visibility; not general artifact coverage | Fully implemented for operational/diagnostic artifacts, partial for repository artifacts |
| Observation providers/predicates | Implicitly implemented as provider/predicate counts | Fully implemented as predicate/family/provider count summaries | Partially implemented through provider examples and JSON rows | Fully implemented as providers per predicate and predicates per family | Partially implemented through inventory summary, not coverage denominator over all possible providers | Fully implemented |
| Projected entity classifications | Not implemented as recurrence | Fully implemented as classification distribution and unknown contributors | Partially implemented via top unknown predicates/examples/categories | Fully implemented for classified vs unknown grouping | Fully implemented for entity classification coverage | Fully implemented as diagnostic |
| Relationship evidence | Not implemented generally | Partially implemented for relationship categories involving unknown entities and graph issue categories | Partially implemented in graph issue summaries/audits; not general relationship drilldown | Partially implemented through relationships involving unknown entities and audit edges | Partially implemented through graph issue impact and visibility audits | Partially implemented in graph/component/emitter/consumer audits |
| Measurements | Not implemented generally | Partially implemented through local count and byte/value distributions | Not implemented generally | Implicitly implemented through predicate inventories | Partially implemented for classification/documentation counts; not general measurement coverage | Partially implemented through observation predicate inventory |
| Events | Not implemented generally | Not implemented generally | Not implemented generally | Implicitly through ledger/projection mechanisms only | Partially implemented only as diagnostic write/record boundary fields | Partially implemented as operational boundary metadata |
| Operational/diagnostic surfaces | Implicitly implemented through repeated CLI flag and surface inventories | Fully implemented through diagnostic inventory and shape audit summaries | Partially implemented through per-surface shape audit rows and implementation evidence | Fully implemented through registry membership and discovered-surface comparison | Fully implemented for visibility coverage audit and diagnostic shape audit | Fully implemented |

## Supported matrix cells that may be under-recognized

### Operational surface x coverage

The visibility coverage audit compares discovered operational CLI surfaces with diagnostic inventory visibility. This is a real implemented `operational surface x coverage` cell, even though the candidate architecture examples focus on artifact/language/structure.

### Diagnostic surface x shape audit

Diagnostic shape audit is an implemented `diagnostic surface x audit` cell. It checks declared diagnostic shape against implementation markers. This is not captured by recurrence/distribution/drilldown/membership/coverage alone.

### Observation predicate x inventory/membership/distribution

Observation inventory implements provider/predicate/family inventory, provider-count distribution per predicate, and predicate-count/provider-count summaries per family. This is not framed as recurrence, but it is a concrete operation/material pairing.

### Structure x coverage

Documentation structure recurrence includes common-section labels and documents missing common sections. This is partial structure coverage, even if not exposed as `--coverage`.

### Relationship evidence x distribution

Classification coverage computes top unknown relationship categories and graph issue categories. This is a bounded relationship-evidence distribution, but only for unknown-entity impact and graph validation issue context.

### Measurement x distribution

Documentation structure and classification coverage expose measurement-like distributions and counts. This is partially implemented but not generalized.

## Missing or unsupported cells predicted by architecture/investigations

### Language x recurrence

Lexical recurrence is investigated, including possible support for frequency, distribution, membership, coverage, and drilldown style visibility. Implementation evidence does not show an operator-facing or module-level lexical recurrence surface. Heading/section label counts are structural-label recurrence, not prose/phrase recurrence.

### Artifact x recurrence and artifact x coverage

Implementation can inventory document paths and operational artifacts, but there is no general artifact recurrence or artifact coverage model across repository files, generated files, records, snapshots, and code artifacts.

### Relationship x recurrence

Relationship categories and graph issues are counted in specific diagnostics, but recurrence of relationship evidence across a corpus is not implemented.

### Event x recurrence/distribution/drilldown

Events are part of projection and diagnostic recording boundaries, but there is no general event observation operation matrix.

### Measurement x generalized distribution/coverage

Measurement-like values exist, but there is no generic measurement operation with denominator, unit metadata, source location, and bounded distribution output across all measurement predicates.

### General operation/material matrix

No implementation currently registers a complete material/operation matrix or declares per-material supported operations in a single inventory. This audit itself is a static reconciliation document, not an implementation surface.

## Architectural mismatches

### Architecture ahead of implementation

- The candidate model implies broad composability: material class x prerequisite evidence x operation -> bounded output. Implementation is narrower and surface-specific.
- Lexical/language recurrence is investigated but not implemented.
- Artifact, relationship evidence, event, and measurement material classes are not generalized.
- Recurrence, drilldown, membership, coverage, and distribution do not share a common implementation contract across materials.
- Prerequisite evidence such as denominators, ranges, source locations, and normalization rules exists, but inconsistently by surface.

### Implementation ahead of architecture

- Inventory is a primary implemented visibility operation, but it is not prominent in the candidate operation list.
- Audit/shape-audit is a primary implemented reconciliation operation, but it is not represented in the candidate operation list.
- Operational/diagnostic surfaces are first-class observable material in code.
- Emitter/consumer/component implementation evidence is observable material, which prior material classes do not clearly name.
- Diagnostic boundary metadata such as `record_scope`, `writes_event_ledger`, and `mutates_cluster` is mature and implementation-backed.

### Vocabulary mismatch

Some candidate terms are usable as audit labels, but not all are repository-native implementation names:

- `membership` often appears as inventory grouping or set membership rather than a CLI operation.
- `coverage` appears in named diagnostics for classification and visibility, but documentation structure coverage is expressed as missing/common section counts.
- `distribution` appears as local count summaries and top contributors, not a universal operation.
- `artifact`, `language`, `relationship evidence`, `events`, and `measurements` are not registered as formal material classes.

## Supported conclusions

1. Structure/documentation structure is implemented as observed material.
2. Structural recurrence is fully implemented for repository Markdown documentation.
3. Structural drilldown is fully implemented only for exact section-label targets.
4. Structural coverage is partially implemented through missing/common section and corpus-count reports.
5. Classification coverage is fully implemented for projected entity classification state.
6. Operational and diagnostic surfaces are implemented as observable material through diagnostic inventory, operational surface inventory, visibility coverage audit, and diagnostic shape audit.
7. Observation providers/predicates/families are implemented as observable material through AST inventory.
8. Relationship evidence is partially implemented through graph issues, unknown relationship categories, and implementation relationship audits.
9. Measurements are partially implemented as values/counts within specific diagnostics and observation predicates.
10. Events are implemented as ledger/projection/recording boundary material, not as a general observation material class.
11. Language recurrence remains investigation-only.
12. The repository currently favors surface-specific implementations over a generalized observation matrix.

## Unsupported conclusions

The following conclusions are not supported by implementation evidence today:

- Lexical recurrence exists as a repository CLI or read model.
- Exact language fragments can be inventoried, distributed, covered, or drilled down through an implemented visibility surface.
- Artifact recurrence is generally implemented.
- Relationship recurrence is generally implemented.
- Measurement distribution is generally implemented across all measurements.
- Event recurrence/distribution/drilldown is implemented.
- Every material class supports recurrence, distribution, drilldown, membership, and coverage.
- Candidate material classes are formally registered in implementation.
- Candidate operations are formally registered in implementation as a shared operation taxonomy.

## Recommended next step

Do not expand architecture yet.

Recommended next step: add an implementation-backed **observation model capability inventory** only if the project wants this matrix to become an operational surface. That inventory should be derived from existing registries and implementation specs rather than from investigation documents. It should start by naming only implemented cells:

- documentation structure x recurrence
- documentation structure x section-label drilldown
- documentation structure x partial coverage
- classification state x coverage/distribution
- diagnostic surface x inventory/shape audit/coverage
- observation predicate x inventory/membership/distribution
- operational surface x visibility coverage

Until such an inventory exists, treat this audit as reconciliation evidence rather than repository truth. The architecture is currently ahead of implementation for generalized material/operation composability, while implementation is ahead of architecture for operational-surface inventory, diagnostic shape audit, and implementation-edge visibility.

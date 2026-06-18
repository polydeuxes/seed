# Source Navigation Entity Typing Graph Issue Audit

## Status

Documentation-only audit. No runtime behavior, source ingestion, graph validation, relationship catalog, entity type catalog, projection semantics, or type assertion logic is changed here.

The immediate finding is that the current warning family is triggered by a specific projection mismatch: repository-source `defines` facts use Python module identities and dotted symbol identities, while the catalog validates every `defines` edge as `document -> concept`. Repository evidence also shows a larger modeling boundary: repository-source module/symbol relationships and documentation metadata relationships currently share the same `defines` predicate/relationship even though their authority differs.

## Runtime evidence

Prompt-supplied runtime evidence reported:

```text
warnings: 1839
errors: 0
total: 1839

warning | defines | subject type is unknown; expected document; object type is unknown; expected concept: 1839
```

A fresh in-memory observation of this checkout on 2026-06-18 produced the same family with a slightly different count because the working tree/test corpus currently contains 170 observed Python files:

```text
1847 graph issues
warning | defines | subject type is unknown; expected document; object type is unknown; expected concept: 1847
relationship families affected in this run: defines only
repository source counters: files_scanned=170, files_skipped=0, definitions_imports_extracted=3684
```

The fresh check used an in-memory `EventLedger`, `RepositorySourceObservationSource('.')`, `ObservationCollectionService`, and `StateProjector`; it did not write repository files or persistent state.

## Files inspected

Minimum requested files and adjusted repository equivalents inspected:

- `seed_runtime/observation_sources.py`
- `seed_runtime/state.py`
- `seed_runtime/facts.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/knowledge/documentation_observation.py`
- `seed_runtime/source_navigation.py`
- `relationship_catalog/core.json`
- `entity_type_catalog/core.json`
- `tests/test_graph_validation.py`
- `tests/test_seed_local_script.py`
- `tests/test_source_navigation.py`
- `tests/test_relationship_observation.py`
- `tests/test_documentation_observation.py`
- `tests/test_state_projector.py`
- `tests/test_relationship_catalog.py`
- `docs/source_navigation_without_grep_audit.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/source_navigation_query_surface_design_audit.md`
- `docs/source_observation_queryability_audit.md`
- `docs/repository_observation_source_design.md`

No `docs/lens/source-navigation` directory exists in this checkout.

## Source ingestion shape

### What `--observe-repository-source` emits

`RepositorySourceObservationSource.collect()` discovers allowlisted Python files, reads each file, extracts Python import relationship facts and Python definition relationship facts, and turns each extracted relationship into one `Observation`.

For each source relationship observation, the emitted shape is:

```text
subject = relationship.subject
predicate = relationship.relationship_kind
value = relationship.object
metadata.source_name = repository_source
metadata.source_path = relationship.path
metadata.evidence = relationship.evidence
metadata.relationship_family = relationship.relationship_kind
metadata.repository_root = repository root
dimensions.path = relationship.path
source_type = discovery
confidence = 1.0
```

For Python source files, `relationship.subject` is a module-like identity derived from the path by removing `.py`, stripping leading path syntax, replacing `/` with `.`, and trimming `.__init__`. For example, `seed_runtime/_pydantic_compat.py` becomes `seed_runtime._pydantic_compat`.

### Per source artifact emission answers

For each scanned Python source artifact, repository-source observation currently emits:

| Fact kind | Emitted? | Evidence |
| --- | --- | --- |
| `defines` facts | Yes, for top-level `def`, `async def`, and `class` declarations. | `extract_python_definition_relationship_facts()` emits `RelationshipFact(relationship_kind="defines", subject=<module>, object=<module>.<name>, path=<source_path>, evidence=<line evidence>)`. |
| `imports` facts | Yes, for top-level static `import` and `from ... import ...` statements in the module body. | `extract_python_import_relationship_facts()` emits `RelationshipFact(relationship_kind="imports", subject=<module>, object=<module or imported alias name>, path=<source_path>, evidence=<import evidence>)`. |
| `path` facts | No separate `path` predicate fact. The path is preserved as `dimensions.path` and in metadata/evidence. |
| entity type facts | No. Repository-source observation does not emit facts whose predicate asserts `entity_type`, `document`, `concept`, `domain`, or equivalent. |
| document identity facts | No. Python module identities are not emitted as explicit documents. |
| concept identity facts | No. Dotted symbol identities are not emitted as explicit concepts. |
| domain identity facts | No. Repository-source observation does not emit source domain classifications. |

Documentation metadata extraction is different: `documentation_navigation_relationship_facts()` maps explicit front matter to `depends_on`, `related_to`, `belongs_to_domain`, and `defines` relationship facts using stable document path, domain, and concept identities. However, that helper also emits relationship facts, not entity type facts.

## Relationship projection shape

Catalog relationship projection is generic. `_project_catalog_relationships()` converts any fact whose predicate appears in the relationship catalog into an `EntityRelationship`. The projected subject is `fact.subject_id`; the projected object is the stringified fact value, unless the catalog definition supplies a fixed object. The metadata records the source predicate, expected catalog subject/object types, dimensions, evidence ids, and inferred flag.

The built-in relationship catalog declares:

```text
defines:
  relationship_kind = topology
  subject_type = document
  object_type = concept
  derived_from_predicates = ["defines"]
```

Therefore every fact with predicate `defines` becomes a catalog `defines` relationship expected to be `document -> concept`.

For repository-source Python definitions specifically:

```text
source path: seed_runtime/_pydantic_compat.py
relationship fact subject: seed_runtime._pydantic_compat
relationship fact predicate: defines
relationship fact object: seed_runtime._pydantic_compat.BaseModel
projected relationship subject: seed_runtime._pydantic_compat
projected relationship: defines
projected relationship object: seed_runtime._pydantic_compat.BaseModel
expected subject type: document
expected object type: concept
```

The subject is a Python module identity, not the source file path. The object is a dotted Python symbol identity, not a prose concept label. The path is preserved as a dimension/metadata field, not as the relationship subject.

`imports` facts are preserved as current facts and legacy entity relationships, but `imports` is not present in `relationship_catalog/core.json`, so `imports` facts do not become catalog relationships and are not graph-validated by `GraphValidator`.

## Entity typing shape

`StateProjector` projects entity type assertions after catalog relationships are projected. Current mechanisms are:

1. Existing `Entity` objects with non-`unknown` `kind` become type assertions if the kind exists in the entity type catalog.
2. Subjects of host predicates become `host`.
3. Subjects that look like `host:port` become `endpoint`.
4. A small relationship-derived rule table assigns only:
   - `member_of` object -> `group`
   - `runs_on` subject -> `service`
   - `monitored_by` object -> `monitoring_system`
   - `provides` object -> `capability`
5. Every entity seen in facts or catalog relationships without a supported type derivation receives an `unknown` assertion.

`document`, `concept`, and `domain` are now catalog-valid entity types, but the current projector has no generic mechanism that assigns those types from `defines`, `depends_on`, `related`, or `domain` facts. There is also no source-ingestion entity type fact for repository modules, source paths, dotted symbols, document paths, front matter concepts, or domains.

Repository source-navigation subjects/objects are eligible only in the weak sense that they are seen as entities by projection and therefore receive fallback `unknown` assertions. They are not eligible for `document`, `concept`, or `domain` assignment under existing rules.

## Authority boundary analysis

Repository evidence does not support an unqualified implementation statement that all repository-source `defines` subjects are documents and all defined symbols are concepts.

Evidence supporting caution:

- `relationship_observation.py` explicitly says definition relationships are syntactic declaration evidence only and do not prove invocation, behavior, reachability, capability authority, or runtime ownership.
- Source navigation docs distinguish source observation from source navigation and preserve boundaries such as `defines != invocation`, `module identity != path identity`, `symbol identity != behavior`, and `navigation != authority`.
- Tests assert that definition observation does not emit calls, ownership claims, implemented-by claims, or capability authority.
- Documentation metadata `defines` is explicitly front-matter concept metadata; Python source `defines` is AST declaration evidence. Both currently use the same predicate string, but they do not carry the same authority.

A narrower statement may be repository-authoritative if phrased carefully:

```text
Python module identity = observed source module artifact identity.
Dotted symbol identity = observed source declaration identity.
```

But the current catalogs do not contain `source_module`, `source_file`, `source_symbol`, or similar entity types. The available `document` description says "A source or knowledge document," which may include source artifacts, but existing docs/tests warn that `module identity != path identity` and do not settle whether a module string should be typed as a document. The available `concept` description says "A named concept defined by a document," which is stronger and less clearly applicable to every Python class/function symbol.

Therefore this is not merely a missing emission line unless the next implementation slice first confirms or narrows the ontology: either source modules/symbols are intentionally classified under document/concept, or source-specific entity/relationship vocabulary is needed.

## Scope analysis

Fresh runtime projection of repository-source observations found graph issues only for `defines` relationships. This is consistent with the catalog and code:

- `defines` is cataloged as `document -> concept`, so repository-source `defines` facts become validated catalog relationships and warn when both ends are unknown.
- `imports` is not cataloged, so repository-source `imports` facts do not create catalog graph issues.
- `depends_on`, `related_to`, and `belongs_to_domain` are cataloged and have the same absence of document/domain type derivation risk, but `--observe-repository-source` does not emit those predicates. They are emitted by documentation metadata extraction when front matter exists, and current projection has no document/domain typing mechanism for them.
- Operational relationships such as `member_of`, `runs_on`, `monitored_by`, and `provides` have relationship-derived type rules for at least one side and/or host predicate rules, so they are not the same issue family.

Affected relationship families observed in the repository-source runtime check:

```text
defines only
```

Potentially affected if documentation navigation facts are ingested without separate entity typing:

```text
defines
depends_on
related_to
belongs_to_domain
```

Not currently affected by graph validation because they are not catalog relationships:

```text
imports
source navigation read-model rows
```

## Storage/ownership analogy check

The storage lesson was that visibility is not ownership and a measurement subject is not automatically the host that owns the resource. A similar boundary exists here:

```text
source-navigation subject != automatically document
module path != automatically document
source module identity != source file identity
source file visibility != documentation authority
source symbol name != automatically concept
defined symbol != behavior, reachability, capability, or ownership
```

The strongest analogy is `defined symbol != concept`. A Python class/function name is visible syntactic structure. It may be useful as a navigable source declaration, but classifying it as a knowledge concept could overclaim unless repository ontology explicitly defines source symbols as concepts or introduces source-specific types.

The second analogy is `module identity != document`. The ingestion subject is a module-like dotted name, while the evidence path is a file path dimension. Treating the module string as the document may collapse two identities that source-navigation docs explicitly keep distinct.

## Possible fix classes

### A. Source ingestion emits entity_type document/concept/domain

Benefit:

- Directly eliminates unknown-type warnings for repository-source `defines` if module subjects are typed `document` and symbol objects are typed `concept`.
- Keeps graph validation unchanged.

Risks:

- May overclaim that every Python module identity is a document and every top-level class/function symbol is a concept.
- Could collapse module identity, file path identity, and documentation identity.
- Would add authority to ingestion that current tests/docs intentionally avoid for behavior and ownership; type authority must be justified separately.

Authority required:

- A repository decision that source modules/files are within `document` or a narrower explicit mapping from source artifact to document.
- A repository decision that source declarations are within `concept`, or only a subset of declarations are concepts.

### B. Relationship projection derives types for source-navigation relationships

Benefit:

- Centralizes deterministic typing near relationship projection rather than changing source ingestion.
- Could make `defines` subject/object types follow catalog expectations.

Risks:

- Circularity risk: the same relationship being validated would manufacture the types needed to pass validation.
- Current validator already has special handling to avoid circular support in ambiguous cases; adding `defines` to relationship-derived rules would need careful authority treatment.
- Same overclaim risk as A, but less visible at ingestion boundaries.

Authority required:

- A model-level rule that a `defines` edge itself proves its endpoint types. Existing code intentionally only derives selected operational types from selected relationships, not document/concept/domain.

### C. Graph validator treats source-navigation relationships specially

Benefit:

- Could preserve warnings for documentation `defines` while avoiding noisy warnings for repository-source `defines`.
- Can account for metadata such as `dimensions.path` or `source_name=repository_source`.

Risks:

- Violates the explicit audit boundary if used as suppression rather than modeling.
- Makes validation depend on source-specific exceptions instead of clear entity/relationship vocabulary.
- Could hide real missing authority.

Authority required:

- A principled validation rule that source declaration edges have a different contract from document/concept edges. If that is true, changing the relationship vocabulary is probably cleaner than validator special-casing.

### D. Relationship catalog should not validate `defines` as `document -> concept`

Benefit:

- Recognizes that one predicate currently carries at least two meanings: documentation metadata concept definition and source declaration definition.
- Avoids forcing source relationships into a document/concept model.

Risks:

- Weakens useful validation for authored documentation navigation if changed globally.
- Could make documentation metadata less precise unless split into separate relationships/predicates.

Authority required:

- Evidence that current `defines` is intentionally broader than document/concept, or a decision to split vocabulary.

### E. Catalog expected types should be different

Benefit:

- If source declarations are the dominant meaning of `defines`, types like `source_artifact -> source_symbol` would be more accurate.
- Avoids pretending every symbol is a concept.

Risks:

- Requires adding source-specific entity types and probably preserving separate documentation concept-definition semantics.
- Could break tests asserting `defines.object_type == concept` unless tests are updated with a new settled model.

Authority required:

- New ontology terms for source artifacts/symbols and clear relationship definitions.

### F. Keep warnings because authority is genuinely missing

Benefit:

- Honest: the graph is saying the endpoints are untyped under the current model.
- Avoids fake facts, validation suppression, and premature ontology collapse.

Risks:

- Leaves high-volume warnings that may obscure other graph issues.
- Does not improve operator confidence or graph usability.

Authority required:

- Acceptance that current source relationships are useful as facts/read-model rows but are not yet fully modeled graph entities.

## Recommendation for next implementation slice

Do not immediately add repository-source `document`/`concept` type assertions.

Recommended next slice is a characterization/modeling slice before behavior changes:

1. Add focused tests or an audit fixture that contrasts documentation metadata `defines` with repository-source Python `defines`.
2. Decide whether to split source declaration vocabulary from documentation concept vocabulary, for example:
   - `source_defines` / `declares` as `source_module_or_file -> source_symbol`, while keeping documentation `defines` as `document -> concept`; or
   - explicitly document and test that `document` includes source modules and `concept` includes source declarations.
3. If the repository chooses the second option, add narrow entity typing with explicit authority comments and tests that preserve `defines != behavior/ownership/reachability`.
4. If the repository chooses the first option, update catalog/projection/source ingestion coherently rather than special-casing graph validation.

Current evidence leans toward a larger authority/modeling issue rather than a narrow ingestion omission, because the same predicate name is shared by source declaration facts and documentation concept metadata while only one `document -> concept` validation contract exists.

## Non-conclusions

This audit does not conclude that:

- Python modules are documents.
- Python files are documents.
- Python classes/functions are concepts.
- Documentation front matter and Python AST declarations have the same authority.
- Graph warnings should be suppressed.
- Catalog expectations should be changed without a vocabulary decision.
- Source ingestion should emit fake type facts.
- Projection should infer document/concept/domain types from relationships without an authority decision.

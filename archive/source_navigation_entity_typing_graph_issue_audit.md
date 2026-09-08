# Source Navigation Entity Typing Graph Issue Audit

## Scope

This is an implementation visibility audit. It uses repository artifacts as the only authority and does not reconcile relationship semantics, propose ontology changes, or redesign predicates.

## Files Inspected

- `entity_type_catalog/core.json`
- `relationship_catalog/core.json`
- `seed_runtime/entity_type_catalog.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/state.py`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observations.py`
- `seed_runtime/source_navigation.py`
- `tests/test_graph_validation.py`
- `tests/test_observation_sources.py`
- `tests/test_relationship_observation.py`
- `tests/test_source_navigation.py`
- `tests/test_state_projector.py`

## Entity Types Found

The built-in entity type catalog currently contains:

- `host`
- `service`
- `group`
- `endpoint`
- `monitoring_system`
- `capability`
- `document`
- `concept`
- `domain`
- `unknown`

These are catalog vocabulary entries only. They do not, by themselves, assign those types to repository source modules or source symbols.

## Repository Artifact Types Currently Existing

Repository-supported relationship endpoints currently include only the catalog entity types above. For repository documentation relationships, `document`, `concept`, and `domain` exist as expected endpoint types for `depends_on`, `related_to`, `belongs_to_domain`, and `defines`.

No separate implemented entity type was found for Python module, Python source file, class, function, async function, or imported symbol. The source extraction path records Python definitions and imports as facts, but it records them into the generic fact and relationship projection system rather than into source-specific entity classifications.

## Classification Mechanisms Found

Entity type assignment is implemented in `seed_runtime/state.py` by `_project_entity_type_assertions`. It can assign types from these mechanisms:

1. Existing `Entity.kind` values when the kind exists in the entity type catalog.
2. Host facts whose predicates are in host predicate rules.
3. Endpoint-looking subjects matching the host:port recognizer.
4. A small relationship-derived rule table:
   - `member_of` object -> `group`
   - `runs_on` subject -> `service`
   - `monitored_by` object -> `monitoring_system`
   - `provides` object -> `capability`
5. Fallback `unknown` assertions for entities that participated in state but did not receive a supported type.

No classification mechanism was found that assigns:

- `document` to repository source module subjects such as `seed_runtime._pydantic_compat`.
- `concept` to source symbols such as `seed_runtime._pydantic_compat.BaseModel`.
- any source-specific type to Python module or symbol endpoints.

## Promotion Mechanisms Found

Observation ingestion promotes observations into facts unless explicitly suppressed. Repository source observation creates observations for import and definition relationships. Observation ingestion then converts those observations into `fact.observed` events.

The promotion path preserves source relationship information as fact subject, predicate, value, dimensions, evidence, and metadata. It does not promote source-path metadata or relationship evidence into entity type assertions.

Source navigation is read-only. It projects existing `imports` and `defines` fact support rows and does not classify entities, inspect files, parse source, or write events.

## Source Observation Pathway

For repository source observation:

1. `RepositorySourceObservationSource.discover_source_files` finds allowlisted Python files under configured roots.
2. Each file is read as text.
3. `extract_python_import_relationship_facts` emits `imports` relationship facts.
4. `extract_python_definition_relationship_facts` emits `defines` relationship facts for top-level classes, functions, and async functions.
5. `RepositorySourceObservationSource._relationship_observation` converts each relationship fact to an observation with:
   - `subject` set to the module identity, for example `seed_runtime._pydantic_compat`.
   - `predicate` set to `imports` or `defines`.
   - `value` set to the imported name or defined qualified symbol, for example `seed_runtime._pydantic_compat.BaseModel`.
   - dimensions containing `path`.
   - metadata preserving source path, evidence text, relationship family, and repository root.
6. `ObservationIngestor.ingest_many` writes observation, evidence, and promoted fact events.
7. `StateProjector.finalize` builds fact support, catalog relationships, entity type assertions, and graph issues.

## Lifecycle Trace: `seed_runtime._pydantic_compat`

`seed_runtime._pydantic_compat` enters the graph as the subject of repository source facts. In the representative `defines` path, `extract_python_definition_relationship_facts` derives the subject from `seed_runtime/_pydantic_compat.py` and emits `seed_runtime._pydantic_compat defines seed_runtime._pydantic_compat.BaseModel`.

After observation ingestion, the module identity is preserved as the fact subject and as the subject of the projected `defines` relationship. During entity type projection, it is added to the set of participating entities because it is a fact subject and relationship subject.

It remains `unknown` because none of the current entity type assertion rules match it:

- It is not an upserted `Entity` with a non-unknown kind.
- Its facts are `imports` and `defines`, not host-classifying predicates.
- It does not look like a host:port endpoint.
- The `defines` relationship has no relationship-derived type rule.
- It receives only the fallback unknown assertion.

## Lifecycle Trace: `seed_runtime._pydantic_compat.BaseModel`

`seed_runtime._pydantic_compat.BaseModel` enters the graph as the object of a repository source `defines` fact. The extractor builds this qualified symbol from the module subject and AST node name.

After observation ingestion, the symbol identity is preserved as the fact value and then as the object of the projected `defines` relationship. During entity type projection, it is added to the participating entity set from projected relationships.

It remains `unknown` because none of the current entity type assertion rules classify relationship objects for `defines`; no rule maps `defines` object to `concept`; no source-symbol classifier exists; and no explicit `Entity` kind is created for the symbol.

## Relationship Generation and Validation

Catalog relationship projection maps fact predicates through `relationship_catalog/core.json`. The `defines` predicate maps to the `defines` relationship with expected subject type `document` and expected object type `concept`.

Graph validation does not assign types. It reads current entity types for each projected edge endpoint and compares them with relationship catalog expectations. If an endpoint has no non-unknown assertion, `State.get_current_entity_types` returns `unknown`, and `GraphValidator` emits a warning such as:

```text
subject type is unknown; expected document; object type is unknown; expected concept
```

This warning is therefore downstream of missing endpoint classification. It is not evidence, by itself, that the `defines` relationship authority is wrong or right.

## Unknown Entity Pathways Found

A repository source endpoint becomes `unknown` when it participates in facts or relationships but is not covered by any entity type assertion mechanism. Source modules and source symbols follow this pathway today.

The fallback unknown assertion is intentionally explicit: entities without supported type derivation receive an `unknown` assertion with reason `no supported entity type derivation`.

## Quantitative Check

A local in-memory projection of repository source observations for the `seed_runtime` root produced:

- observations: 1562
- facts: 1562
- catalog relationships: 647
- graph issues: 647
- entity type assertions: 726
- issues involving unknown endpoint types: 647 / 647 = 100.0%

All graph issues in that check had the same reason:

```text
subject type is unknown; expected document; object type is unknown; expected concept
```

For the representative endpoints:

- `seed_runtime._pydantic_compat` projected as `unknown` with reason `no supported entity type derivation`.
- `seed_runtime._pydantic_compat.BaseModel` projected as `unknown` with reason `no supported entity type derivation`.

## Required Question Answers

### What repository artifact types currently exist?

The catalog has generic `document`, `concept`, and `domain` types usable for repository knowledge/documentation endpoints. It does not have implemented source-code artifact types for Python modules, Python files, classes, functions, async functions, or imported symbols.

### What entity types can be assigned today?

The assignment path can currently assign `host`, `service`, `group`, `endpoint`, `monitoring_system`, `capability`, and `unknown` from implemented rules. It can also accept any catalog type from explicit upserted `Entity.kind` values, including `document`, `concept`, and `domain`, if such entities are provided. No observed repository source pathway currently emits those explicit entity upserts.

### What repository artifacts are currently classified?

Repository source facts are observed and projected, but the source-module and source-symbol endpoints observed from Python source are not classified into repository-supported non-unknown types by the implemented projection path.

Documentation navigation artifacts can use `document`, `concept`, and `domain` identities in relationship facts, but this audit found the type catalog entries and relationship expectations, not a general source-module classifier.

### What repository artifacts remain unknown?

Python module subjects such as `seed_runtime._pydantic_compat` and Python symbol objects such as `seed_runtime._pydantic_compat.BaseModel` remain unknown in the repository source observation path.

### Why do source modules remain unknown?

Source modules remain unknown because source observation records them as relationship subjects, but entity type projection has no rule that classifies module identities or source paths as `document` or another non-unknown type.

### Why do source symbols remain unknown?

Source symbols remain unknown because definition extraction records them as relationship objects, but entity type projection has no rule that classifies `defines` objects as `concept` or as source symbols.

### Is classification information available but not promoted?

Partial classification information is available but not promoted. The repository source observation path preserves `relationship_family`, `source_path`, and definition evidence text. The extractor also knows whether a definition is a class, function, or async function while composing evidence text. However, this information is not represented as entity type assertions and the extracted symbol kind is not carried as a structured field in `RelationshipFact`.

### Is classification absent?

Non-unknown endpoint classification is absent at projection time for source modules and source symbols. The available metadata is insufficiently structured for full symbol-kind classification and is not consumed by `_project_entity_type_assertions` for document/concept assignment.

### Where is type assignment expected to occur?

In the current implementation, type assignment occurs during state finalization in `_project_entity_type_assertions`, after facts and catalog relationships are projected and before graph validation.

### Where is type assignment currently occurring?

Type assignment currently occurs only in `_project_entity_type_assertions`, using explicit entity kinds, host predicates, endpoint shape, selected relationship-derived rules, and fallback unknown assertions.

### What percentage of graph issues are caused by unknown endpoint types?

In the local `seed_runtime` repository source projection check, 100.0% of graph issues were caused by unknown endpoint types.

### Would graph issues become more informative if endpoint types existed?

Yes. If source module and symbol endpoints had supported non-unknown classifications, graph validation could distinguish actual type mismatches from missing classification. Current warnings collapse all observed `defines` source relationships into unknown-endpoint visibility warnings, so they cannot yet answer whether a relationship expectation is satisfied or mismatched for those endpoints.

## Root Cause Findings

1. The primary observed problem for the representative examples is a classification visibility gap.
2. Repository source observation and relationship generation are successfully preserving `defines` facts and projected relationships.
3. Entity type projection does not consume repository source observation metadata or `defines` edges to assign non-unknown types to source modules or source symbols.
4. Graph validation reports unknown endpoints because it runs after type projection and only sees fallback unknown assertions for those endpoints.

## Supported Conclusions

- `document`, `concept`, and `domain` exist in the entity type catalog.
- The `defines` relationship expects `document` -> `concept` according to the relationship catalog.
- Source modules and source symbols are included in projected relationships.
- Source modules and source symbols receive fallback `unknown` assertions in the current projection path.
- Unknown endpoint types account for all graph issues in the measured `seed_runtime` repository source projection check.
- The representative issue is fundamentally a classification visibility gap before it can be assessed as a relationship mismatch.

## Unsupported Conclusions

- This audit does not conclude that `defines` authority is wrong.
- This audit does not conclude that `defines` authority is correct.
- This audit does not conclude that relationship predicates should change.
- This audit does not conclude that ontology should be expanded.
- This audit does not conclude that source modules should necessarily be classified as `document` or that source symbols should necessarily be classified as `concept`; it only records that current validation expects those types and current projection does not assign them.

## Implementation Opportunities Directly Supported by Evidence

- Add a repository-source endpoint classification path before graph validation, if repository authority decides source modules and symbols should satisfy existing relationship catalog expectations.
- Preserve structured definition kind from Python extraction if future source-symbol classification needs to distinguish classes, functions, and async functions.
- Add tests that trace repository source observations through fact promotion, relationship projection, entity type assertion projection, and graph validation for representative module and symbol endpoints.
- Add diagnostics that report graph issue counts grouped by unknown endpoint type versus concrete type mismatch so operators can distinguish classification visibility gaps from relationship mismatches.

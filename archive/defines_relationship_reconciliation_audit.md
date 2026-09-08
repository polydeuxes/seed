# Defines Relationship Reconciliation Audit

## Status and Boundary

Documentation-only modeling audit. No source ingestion, graph validation, relationship catalog, entity catalog, projection behavior, warning behavior, entity types, or relationship types are changed here.

This audit asks whether the current `defines` relationship is one thing, or whether multiple authorities have accumulated under the same relationship spelling.

## Runtime context

- Date: 2026-06-18.
- Repository path: `/workspace/seed`.
- Working mode: repository evidence review plus documentation-only report creation.
- Orientation authority: `docs/source_navigation_entity_typing_graph_issue_audit.md`.
- Relevant prior finding: repository-source `defines` facts currently use Python module identities and dotted symbol identities, while the relationship catalog validates every `defines` relationship as `document -> concept`.

## Files inspected

Minimum requested files inspected:

- `relationship_catalog/core.json`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/knowledge/documentation_observation.py`
- `seed_runtime/source_navigation.py`
- `tests/test_relationship_observation.py`
- `tests/test_documentation_observation.py`
- `tests/test_source_navigation.py`
- `docs/source_navigation_entity_typing_graph_issue_audit.md`

Additional files inspected because they contain producers, projections, validation expectations, or related claim language:

- `seed_runtime/observation_sources.py`
- `seed_runtime/knowledge/repository_observation.py`
- `seed_runtime/knowledge/self_model_alignment.py`
- `tests/test_relationship_catalog.py`
- `tests/test_graph_validation.py`
- `tests/test_observation_sources.py`
- `tests/test_existence_claim_reconciliation.py`
- `tests/test_structure_claim_reconciliation.py`
- `tests/test_self_model_acquisition_pipeline.py`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/repository_observation_validation_audit.md`
- `docs/source_observation_duplicate_fact_audit.md`
- `docs/repository_observation_external_tooling_audit.md`
- `docs/behavior_claim_reconciliation.md`
- `docs/self_model_acquisition_architecture_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`

## All current producers of `defines`

This inventory distinguishes producers of the actual relationship predicate `defines` from documentation or reconciliation code that parses prose containing the word `defines`.

| Producer | Produces actual `defines` predicate? | Subject | Object | Authority | Purpose | Example |
| --- | --- | --- | --- | --- | --- | --- |
| `extract_python_definition_relationship_facts()` in `seed_runtime/knowledge/relationship_observation.py` | Yes | Module-like identity derived from Python source path, for example `fixtures.source` | Dotted symbol identity, for example `fixtures.source.build_state_summary` | Python AST over caller-provided source text | Preserve top-level Python declaration evidence for source observation/navigation | `fixtures.source defines function build_state_summary at fixtures/source.py:1-2.` |
| `RepositorySourceObservationSource.collect()` in `seed_runtime/observation_sources.py` | Yes, by converting extracted definition relationship facts into `Observation` records | Same as extracted relationship subject | Same as extracted relationship object | Read-only allowlisted repository source scan using the relationship observation adapter | Operational ingestion path that turns Python source `defines` relationships into observations/facts | Observation with `predicate=defines`, `subject=<module>`, `value=<module>.<symbol>`, `dimensions.path=<source_path>` |
| `documentation_navigation_relationship_facts()` in `seed_runtime/knowledge/relationship_observation.py` | Yes | Stable normalized documentation path, for example `docs/source.md` | Authored concept label from front matter, for example `structural navigation` | Explicit authored documentation front matter already supplied by caller | Map documentation navigation metadata to relationship facts | `docs/source.md defines concept structural navigation.` |
| `extract_documentation_navigation_relationship_facts()` in `seed_runtime/knowledge/documentation_observation.py` | Yes, by parsing front matter and delegating to documentation navigation relationship facts | Documentation path | Front-matter concept value | YAML-like front matter only; prose ignored | Documentation metadata observation for navigation graph | Front matter `defines: [structural navigation, architectural navigation]` yields two `defines` relationships |
| `extract_documentation_claims()` in `seed_runtime/knowledge/documentation_observation.py` | No actual relationship fact; parses claim text | Claim subject token such as `Runtime` | Claim object token such as `handle_user_message` or method token | Explicit simple documentation prose line outside code fences | Classify claim family as `existence` for `X defines Y.` or `structure` for `X defines method Y.` | `Runtime defines handle_user_message.` becomes an existence claim, not a `RelationshipFact` |
| `extract_repository_artifact_facts()` in `seed_runtime/knowledge/repository_observation.py` | No actual relationship fact; emits artifact facts with prose containing `defines method` | Class symbol in fact text and `parent_symbol` metadata | Method symbol | Python AST over caller-provided source text | Structural artifact evidence for reconciliation | `Class Runtime defines method handle_user_message in seed_runtime/runtime.py.` |
| Self-model reconciliation rules in `seed_runtime/knowledge/self_model_alignment.py` | No actual relationship fact; evaluates parsed claims | Documentation claim owner symbol | Documentation claim defined symbol or method symbol | Reconciliation rule over documentation claims plus repository artifact facts | Support/missing-support classification for existence/structure claims | `existence.defines.supported` requires owner and defined symbols in same path; `structure.defines_method.supported` requires class and method containment |
| Tests and fixture builders | Sometimes actual predicate in fixtures; otherwise assertions/examples | Varies | Varies | Test authority only | Lock current behavior and warnings | `tests/test_graph_validation.py` projects a fact with predicate `defines` and expects unknown endpoint type warning under `document -> concept` |

## Meaning inventory

Repository evidence shows at least four meanings of the word `defines`, of which two are current actual relationship-predicate meanings.

### Meaning 1: source declaration relationship

Claim actually made:

```text
Python module-like source identity defines a top-level Python declaration symbol.
```

Evidence and limits:

- Extracted only for top-level `def`, `async def`, and `class` AST nodes.
- Subject is path-derived module identity, not the preserved file path itself.
- Object is a dotted symbol identity, not an authored concept label.
- The adapter explicitly says definition relationships are syntactic declaration evidence only and do not prove invocation, behavior, reachability, capability authority, or runtime ownership.
- Tests assert no call relationships, no ownership claims, no implemented-by claims, and no capability authority are emitted from definition observation.

Classification: syntactic declaration / source navigation edge.

### Meaning 2: documentation front-matter concept definition relationship

Claim actually made:

```text
Documentation document defines an authored concept named in front matter.
```

Evidence and limits:

- Extracted only from supported YAML-like front matter fields.
- Prose body content is explicitly ignored for navigation metadata.
- Subject is stable normalized document path.
- Object is front-matter `defines` value, treated by helper evidence as `object_kind="concept"`.
- This shape matches the relationship catalog contract most directly.

Classification: documentation declaration / concept definition metadata.

### Meaning 3: documentation prose existence claim using `defines`

Claim actually made:

```text
A named artifact X defines another named artifact Y in a narrow same-path existence sense.
```

Evidence and limits:

- Parsed from simple documentation lines matching `X defines Y.`.
- Classified as an existence claim, not a `RelationshipFact`.
- Reconciliation support requires artifact facts for both symbols from the same source path.
- It does not require method containment and does not become a graph `defines` edge by itself.

Classification: knowledge/reconciliation claim, existence family.

### Meaning 4: documentation prose structure claim using `defines method`

Claim actually made:

```text
A class or owner symbol X structurally contains method Y.
```

Evidence and limits:

- Parsed from simple documentation lines matching `X defines method Y.`.
- Classified as a structure claim, not a relationship graph edge.
- Reconciliation support requires a class artifact and a method artifact whose `parent_symbol` is the owner symbol.
- This is stronger than the broad same-path existence form.

Classification: structure claim / containment evidence.

## Authority inventory

| Authority | What it can support | What it does not support |
| --- | --- | --- |
| Relationship catalog | `defines` is a topology relationship expected to connect `document -> concept` | It does not distinguish source declaration `defines` from documentation concept `defines` |
| Python AST relationship observation | Top-level source declarations in caller-provided Python text | Concept definition, documentation authority, behavior, calls, reachability, capability ownership, or runtime ownership |
| Repository source observation source | Read-only conversion of allowlisted source relationship facts into observations | New ontology decisions about document/concept typing |
| Documentation front matter observation | Explicit document navigation metadata, including authored `defines` concept values | Prose-derived concepts or inferred concepts from body text |
| Documentation claim extraction | Narrow prose claim families: existence `X defines Y.` and structure `X defines method Y.` | Direct relationship graph facts |
| Repository artifact extraction | Module/class/function/method/import artifact facts and class-method containment metadata | Relationship catalog authority or source-navigation graph semantics |
| Self-model reconciliation | Whether narrow claims are supported by artifact facts | Renaming or redefining `defines` globally |
| Graph validator | Endpoint type compatibility for projected catalog relationships | It does not decide which modeling authority should own overloaded terms |

## Compatibility analysis with `document -> concept`

### Fits most directly

Documentation front-matter `defines` fits `document -> concept` best:

- subject is a documentation path;
- object is an explicit authored concept value;
- evidence string calls the object kind `concept`;
- the catalog defines `defines` as `document -> concept`.

### Does not currently fit without an extra ontology decision

Repository-source Python declaration `defines` does not currently fit `document -> concept` as emitted:

- subject is a module-like identity derived from path, not an explicit document entity;
- object is a dotted Python symbol identity, not an explicit concept entity;
- path is preserved as metadata/dimension rather than relationship subject;
- source declaration authority is syntactic, not conceptual/documentation authority;
- current projection does not assert `document` or `concept` types for these endpoints.

This does not prove that source modules could never be modeled as documents or source symbols could never be modeled as concepts. It only shows that current repository evidence has not established that authority for all source declaration `defines` uses.

### Not relationship-predicate uses

Documentation prose `X defines Y.` and `X defines method Y.` are not direct graph `defines` relationship uses. They are compatible with neither nor incompatible with `document -> concept` at the relationship-catalog layer because they are claim/reconciliation inputs, not emitted `RelationshipFact` predicates. They do, however, show that repository language already distinguishes existence-level same-path definition from structure-level method containment.

## Required questions

### Question 1: How many distinct meanings of `defines` currently exist?

Four meanings are present in repository evidence:

1. Source declaration relationship: module-like identity -> dotted source symbol.
2. Documentation concept metadata relationship: document path -> concept label.
3. Existence claim phrase: `X defines Y.` supported by same-path artifacts.
4. Structure claim phrase: `X defines method Y.` supported by class/method containment.

Only the first two are actual current relationship-predicate producers of `defines`.

### Question 2: For each meaning, what claim is actually being made?

- Source declaration: a Python module-like source artifact has a top-level syntactic declaration for a class/function/async function symbol.
- Documentation concept metadata: a document explicitly declares that it defines an authored concept value.
- Existence claim: documentation claims two named artifacts are related by a narrow same-path definition/existence rule.
- Structure claim: documentation claims a class/owner symbol contains a method symbol.

### Question 3: Are all current uses compatible with `document -> concept`?

No.

- Fits: documentation front-matter `defines` relationships.
- Does not currently fit: repository-source Python declaration `defines` relationships, unless a future authority decision says module-like identities are documents and dotted declaration identities are concepts.
- Outside direct compatibility: prose claim uses, because they are not relationship graph edges.

### Question 4: Is the graph validator exposing a real modeling inconsistency or merely a missing type assertion?

Repository evidence supports treating the warnings as a real modeling inconsistency, not merely a missing type assertion.

The endpoint types are indeed missing at projection time, but adding type assertions would not be a neutral mechanical fix unless the repository first establishes that source module identities are documents and source symbol identities are concepts. The same predicate spelling currently carries documentation concept-definition authority and source syntactic-declaration authority. The validator is exposing that the catalog has one `document -> concept` contract while repository-source facts use a different source-navigation shape.

### Question 5: Candidate models

#### Model A: all `defines` = `document -> concept`

Benefits:

- Aligns every graph `defines` edge with the existing relationship catalog.
- Preserves one relationship spelling and one validation contract.
- Could make documentation metadata and repository-source definitions easier to query under one relationship.

Risks:

- May overclaim that every Python module-like identity is a document.
- May overclaim that every Python top-level class/function symbol is a concept.
- May collapse module identity, source path identity, source symbol identity, and documentation concept identity.
- Would require explicit authority before adding type assertions or relying on this interpretation.

Repository support:

- The catalog currently says `defines` expects `document -> concept`.
- Documentation metadata producer already emits document path -> concept label.

Repository conflicts:

- Source observation docs and tests constrain Python definition relationships to syntactic declaration evidence only.
- Source navigation preserves module-like subject and dotted symbol object, with path only as dimension/metadata.
- Prior orientation audit says repository evidence does not support unqualified classification of all repository-source subjects as documents and symbols as concepts.

#### Model B: documentation `defines` != source declaration `defines`

Benefits:

- Preserves distinct authorities: authored concept metadata vs Python AST declaration evidence.
- Explains why documentation metadata fits `document -> concept` while source declarations do not.
- Avoids making source symbols concepts by default.
- Matches repository language separating declaration, structure, behavior, ownership, and navigation.

Risks:

- Requires future vocabulary/catalog/projection decision if implemented later.
- Queries using the single word `defines` would need disambiguation.
- Existing tests and tooling that expect one predicate spelling would need review in a later implementation phase.

Repository support:

- Two actual predicate producers have different subjects, objects, authorities, and purposes.
- Tests verify source definitions are not calls, ownership, implemented-by, or authority claims.
- Documentation navigation metadata is explicitly front-matter concept metadata.

Repository conflicts:

- The current relationship catalog has only one `defines` relationship.
- Current repository-source observations already use predicate `defines`, not a source-specific predicate.

#### Model C: `defines` is intentionally broad; `document -> concept` is too narrow

Benefits:

- Acknowledges observed broad use of the word across source declarations, documentation metadata, existence claims, and structure claims.
- Could retain one broad relationship family if future ontology describes broad endpoint types.
- Avoids forcing source declarations into documentation concept vocabulary.

Risks:

- Weakens useful graph validation for documentation metadata unless replaced with a more precise contract.
- Could make `defines` too vague to distinguish concept definition from source declaration and method containment.
- Broadness could hide authority boundaries the repository has repeatedly documented.

Repository support:

- The word `defines` is used in several repository contexts.
- Source navigation and reconciliation docs already treat `defines` as more than a single documentation concept edge in prose.

Repository conflicts:

- The current catalog is not broad; it explicitly expects `document -> concept`.
- Tests assert the catalog object type for `defines` is `concept`.
- Documentation metadata helper evidence uses `object_kind="concept"` for front-matter `defines`.

#### Model D: current warnings are correct; authority has never been established

Benefits:

- Treats graph warnings as honest signals that endpoint types are unknown under the current catalog contract.
- Avoids fake type assertions and warning suppression.
- Keeps the audit boundary intact until modeling authority is settled.

Risks:

- Leaves high-volume warnings in graph validation.
- Does not improve source-navigation graph precision.
- Can make it harder to notice unrelated graph issues if warning volume remains high.

Repository support:

- Current projection lacks document/concept/domain type derivation for these facts.
- Prior audit found the warning family specifically arises from repository-source `defines` against `document -> concept` expectations.
- Current source declaration authority is syntactic only.

Repository conflicts:

- Documentation front-matter `defines` does have a plausible `document -> concept` shape, so saying authority has never been established globally may be too broad. More precise wording is that source-declaration authority has not been established as `document -> concept`, while documentation metadata authority largely has.

## Storage analogy analysis

The analogy resembles `visibility != ownership`, but the closest version here is:

```text
source declaration != concept definition
```

Supported parts:

- A source declaration is visible syntactic structure, not automatically a conceptual definition.
- A module-like subject is not automatically the same identity as a document path.
- A dotted symbol name is not automatically a knowledge concept.
- Source navigation docs and tests preserve boundaries such as definition not implying call, behavior, reachability, capability authority, or runtime ownership.

Potentially misleading parts:

- Unlike storage visibility vs ownership, `defines` can be a legitimate concept-definition relationship in documentation metadata.
- Source declarations may eventually be modeled as document/concept-adjacent entities if the repository explicitly decides that source artifacts are documents or source symbols are concepts.
- Therefore the analogy should not be used to conclude that source declarations can never participate in a concept model; it only cautions against assuming that they already do.

## Major findings

1. `defines` is not currently evidenced as a single settled authority.
2. There are two actual relationship-predicate producers of `defines`: repository-source Python declarations and documentation front-matter concept metadata.
3. Those two producers differ in subject identity, object identity, authority, and purpose.
4. Repository prose/reconciliation code adds at least two more meanings of the word `defines`: existence same-path definition and structure method containment.
5. Documentation front-matter `defines` fits the catalog's `document -> concept` contract most directly.
6. Repository-source Python declaration `defines` does not currently fit `document -> concept` without a future ontology decision.
7. The graph validator is exposing a real modeling inconsistency: one catalog relationship contract is being applied to facts emitted under at least two authorities.
8. The issue should not be reduced to a missing type assertion unless authority is first established for module-as-document and symbol-as-concept typing.

## Recommended next investigation

Do not implement a model yet. The next investigation should be a vocabulary/authority reconciliation that answers only these questions:

1. Is a Python module-like identity a `document`, a `source artifact`, both, or neither?
2. Is a dotted Python declaration identity a `concept`, a `source symbol`, both, or neither?
3. Should authored documentation concept metadata and source declaration evidence share one relationship, or should they be split by authority?
4. If one broad `defines` relationship is retained, what endpoint contract can validate both documentation and source meanings without erasing authority boundaries?
5. How should prose claim families `X defines Y.` and `X defines method Y.` relate, if at all, to graph relationships?

## Non-conclusions

This audit does not conclude that:

- a relationship should be renamed;
- a relationship should be split;
- source modules should be typed as documents;
- source symbols should be typed as concepts;
- documentation metadata and Python declarations have the same authority;
- graph warnings should be suppressed;
- catalogs should be changed;
- projection should infer new types;
- source ingestion should emit entity type facts;
- new entity types or relationship types should be added.

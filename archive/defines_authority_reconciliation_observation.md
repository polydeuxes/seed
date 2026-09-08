# Defines Authority Reconciliation Observation

## Status

Documentation-only authority reconciliation observation. No source ingestion, graph validation, catalogs, entity typing, projection behavior, relationship names, relationship families, or warning behavior are changed here.

This document follows the prior `defines` audit and asks what authority is actually present when the repository says:

```text
X defines Y
```

The purpose is to understand authority before changing behavior. It intentionally does not recommend implementation.

## Files inspected

Required files inspected:

- `docs/defines_relationship_reconciliation_audit.md`
- `relationship_catalog/core.json`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/knowledge/documentation_observation.py`
- `seed_runtime/source_navigation.py`
- `docs/relationship_fact_reconciliation.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/self_model_acquisition_architecture_reconciliation.md`
- `docs/behavior_claim_reconciliation.md`
- `tests/test_relationship_observation.py`
- `tests/test_documentation_observation.py`
- `tests/test_source_navigation.py`

Additional supporting files inspected by targeted search and referenced through the prior audit:

- `seed_runtime/observation_sources.py`
- `seed_runtime/knowledge/repository_observation.py`
- `seed_runtime/knowledge/self_model_alignment.py`
- `tests/test_graph_validation.py`
- `tests/test_relationship_catalog.py`

## Authority inventory

This inventory is grouped by authority, not by implementation module.

### Authority family 1: documentation navigation metadata authority

Statement shape:

```text
document defines concept
```

Example:

```text
docs/navigation.md defines structural navigation
```

Authority being claimed:

- An authored documentation file declares that it defines a concept named in front matter.
- The authority comes from explicit YAML-like front matter supplied to the documentation observation helper.
- The document path is the subject identity.
- The concept string is the object identity.

Boundary crossed:

- Authored document metadata is converted into relationship facts.
- A document navigation surface crosses into graph relationship observation.
- Body prose is not crossed into metadata authority.

Evidence supporting the claim:

- `documentation_navigation_relationship_facts()` maps supplied `defines` metadata to `RelationshipFact` records with `object_kind="concept"`.
- `observe_documentation_metadata()` parses only supported front matter keys, including `defines`.
- Tests assert that front matter `defines` values produce `("defines", "docs/source.md", "structural navigation")` and that prose body references are ignored.
- The relationship catalog currently declares `defines` as `document -> concept`.

Evidence not supporting the claim:

- The metadata parser does not inspect prose for concept meaning.
- The metadata path does not prove repository-source declaration, behavior, ownership, reachability, or runtime authority.
- A front-matter concept label is not validated here as an ontology node beyond the relationship fact shape.

Authority classification candidates present in repository evidence:

- Strongly supported: documentation navigation metadata.
- Supported by catalog shape: documentation classification as `document -> concept`.
- Weak or unsupported by current evidence: full ontology, teaching completeness, behavioral knowledge declaration.

### Authority family 2: repository-source declaration authority

Statement shape:

```text
module-like source identity defines dotted source symbol identity
```

Example:

```text
seed_runtime.state defines seed_runtime.state.StateProjector
```

Authority being claimed:

- A Python module-like identity derived from a source path contains a top-level syntactic declaration for a function, async function, or class symbol.
- The authority comes from Python AST parsing of caller-provided source text.
- The subject is a module-like identity, not the path itself.
- The object is a dotted symbol identity, not an authored concept label.

Boundary crossed:

- Source syntax is converted into relationship evidence.
- Source paths are normalized into module-like identities for subjects.
- Source declarations are projected into preserved facts and then into source navigation rows.

Evidence supporting the claim:

- `extract_python_definition_relationship_facts()` emits only `defines` relationships for top-level Python function, async function, and class declarations.
- Its docstring states definition relationships are declaration evidence only and are not call, behavior, ownership-of-capability, or runtime reachability claims.
- Tests assert function and class definitions produce `relationship_kind == "defines"`, module-like subjects, dotted objects, and source-path evidence.
- Tests assert definition observation does not emit call relationships, ownership claims, capability authority, or implemented-by claims.
- `source_navigation.py` projects preserved `defines` facts for operator navigation without reading files, parsing source, or inferring behavior, reachability, or ownership.

Evidence not supporting the claim:

- The source definition extractor does not prove invocation, behavior, reachability, ownership-of-capability, runtime ownership, or concept formation.
- The source navigation surface does not infer behavior or reachability from definitions.
- The relationship catalog does not currently declare a `module -> symbol` `defines` shape.
- The emitted endpoints are not, by this authority alone, established as `document` and `concept`.

Authority classification candidates present in repository evidence:

- Strongly supported: syntactic declaration and source navigation anchor.
- Narrowly supported in navigation docs: ownership of the definition location, scoped to the symbol definition.
- Not supported: ownership of behavior, ownership of capability, semantic meaning, concept formation, runtime reachability.

### Authority family 3: documentation prose existence-claim authority

Statement shape:

```text
X defines Y.
```

Authority being claimed:

- Documentation prose can make a narrow existence-family claim that two named artifacts are associated under a same-path support rule.
- This is a documentation claim, not a relationship graph `defines` edge.

Boundary crossed:

- Simple prose lines outside code fences are classified into claim families.
- Reconciliation later evaluates the claim against repository artifact facts.

Evidence supporting the claim:

- `extract_documentation_claims()` recognizes `X defines Y.` as an existence claim.
- Self-model reconciliation documentation states existence support can come from direct artifact facts and must not be upgraded into ownership support.
- Behavior reconciliation documentation says same-path co-occurrence may support narrow `Runtime defines handle_user_message.` but not method containment or behavior.

Evidence not supporting the claim:

- This path does not emit a `RelationshipFact` predicate named `defines`.
- Same-path support does not prove direct containment, behavior, ownership, invocation, or concept definition.

### Authority family 4: documentation prose structure-claim authority

Statement shape:

```text
X defines method Y.
```

Authority being claimed:

- Documentation prose can make a structure-family claim that a class or owner symbol directly contains or declares a method.
- This is stronger than the broad existence form because support requires method parent metadata.
- It is still not behavior.

Boundary crossed:

- Simple prose is classified into structure claims.
- Repository artifact facts with `parent_symbol` metadata are used as support.

Evidence supporting the claim:

- `extract_documentation_claims()` recognizes `X defines method Y.` as a structure claim.
- Self-model acquisition documentation states that `X defines method Y.` requires a class fact for `X` and a method fact for `Y` with `parent_symbol == X`.
- Behavior reconciliation documentation states method containment is not behavior.

Evidence not supporting the claim:

- Structure-claim authority does not emit graph `defines` facts.
- Method containment does not prove invocation, routing, mutation, event emission, storage, validation, ownership, or runtime participation.

## Evidence inventory

### Catalog evidence

`relationship_catalog/core.json` currently defines one catalog relationship named `defines`:

```text
relationship: defines
relationship_kind: topology
subject_type: document
object_type: concept
derived_from_predicates: [defines]
```

Catalog authority therefore supports a single validated graph shape for `defines`: `document -> concept`.

### Source extraction evidence

Repository-source extraction emits `defines` for top-level Python declarations and explicitly limits the authority of those facts. The emitted example shape is:

```text
fixtures.source defines fixtures.source.build_state_summary
```

The supporting tests assert:

- function definitions emit `defines`;
- class definitions emit `defines`;
- import observation remains separate;
- calls are not emitted;
- ownership claims are not emitted;
- file reading is not performed by the extractor.

### Documentation metadata evidence

Documentation metadata observation emits `defines` only from front matter. The tests assert:

```text
---
defines:
  - structural navigation
  - architectural navigation
---
```

produces:

```text
docs/source.md defines structural navigation
docs/source.md defines architectural navigation
```

The same tests state that body prose saying a document defines something must be ignored for navigation metadata.

### Source navigation evidence

Source navigation consumes preserved source facts and exposes definitions and imports for operator lookup. It is read-only and explicitly says it does not inspect files, parse source, ingest observations, or infer behavior, reachability, or ownership.

The navigation reconciliation document gives `module defines symbol` as a supported navigation shape, but also preserves distinctions such as:

```text
imports != defines
defines != invokes
ownership != reachability
```

It also states a `defines` relationship can identify the source artifact that owns the canonical declaration of a symbol, while scoping that ownership to the definition location rather than behavior or capability ownership.

### Prior reconciliation evidence

Prior reconciliation documents repeatedly separate weaker evidence from stronger conclusions:

- artifact fact versus relationship fact;
- structure versus behavior;
- behavior versus ownership;
- candidate evidence versus supported fact;
- static containment versus runtime participation.

These distinctions matter because source declaration `defines` is static declaration evidence, while documentation concept `defines` is authored navigation metadata.

## Meaning inventory

### Meaning 1: concept definition by documentation metadata

```text
document defines concept
```

Meaning currently supported:

- The document front matter declares a concept label for documentation navigation and graph topology.

Meaning not supported:

- The document body proves the concept.
- The concept label is a complete ontology assertion.
- The document proves source declaration, runtime behavior, or capability ownership.

### Meaning 2: source declaration by module-like source identity

```text
module defines symbol
```

Meaning currently supported:

- A module-like source identity has a top-level syntactic declaration for a dotted symbol.
- The fact can anchor operator source navigation to a source path and definition location.

Meaning not supported:

- The symbol is invoked.
- The symbol owns behavior or capability authority.
- The symbol is a concept.
- The module-like subject is a document under current emitted evidence alone.

### Meaning 3: same-path existence claim in documentation prose

```text
X defines Y.
```

Meaning currently supported:

- A narrow existence-family claim may be supported by same-path artifact evidence.

Meaning not supported:

- Direct containment.
- Method membership.
- Runtime behavior.
- Ownership.
- A graph `defines` relationship.

### Meaning 4: direct method containment claim in documentation prose

```text
X defines method Y.
```

Meaning currently supported:

- A structure-family claim may be supported when a method artifact has `parent_symbol == X`.

Meaning not supported:

- Behavior, invocation, reachability, or ownership.
- A graph `defines` relationship.

## Required questions

### Question 1: Are these the same kind of claim?

```text
docs/navigation.md defines structural navigation
```

and

```text
seed_runtime.state defines StateProjector
```

No, repository evidence shows they are not the same kind of claim.

What differs:

| Dimension | `docs/navigation.md defines structural navigation` | `seed_runtime.state defines StateProjector` |
| --- | --- | --- |
| Authority | Authored documentation front matter | Python AST source declaration |
| Subject identity | Document path | Module-like source identity |
| Object identity | Authored concept label | Dotted Python symbol identity, or short symbol in prose examples |
| Boundary crossed | Metadata to graph topology | Source syntax to source navigation fact |
| Supported meaning | Documentation navigation/concept metadata | Top-level syntactic declaration and definition-location navigation |
| Not supported | Source declaration or behavior | Concept formation, behavior, reachability, capability ownership |
| Catalog fit | Directly matches `document -> concept` | Does not currently match without additional entity typing/authority decisions |

### Question 2: For repository-source definitions, what is asserted?

For:

```text
module defines symbol
```

Repository evidence supports the following assertions:

| Candidate meaning | Supported? | Evidence-based assessment |
| --- | --- | --- |
| Existence | Yes, narrowly | A top-level source declaration exists for the symbol. |
| Containment | Partly, syntactic/module-level | The top-level declaration is in the parsed module source. This is not the same as class-method containment. |
| Declaration | Yes, strongly | The extractor explicitly emits declaration evidence for top-level function, async function, and class declarations. |
| Ownership | Only scoped definition-location ownership | Source navigation docs allow ownership of the canonical declaration location, but not behavior or capability ownership. |
| Meaning | No | AST declaration does not establish semantic meaning. |
| Concept formation | No | Dotted symbols are not established as concepts by source extraction. |
| Navigation | Yes | Source navigation uses preserved `defines` facts for symbol, module, and path lookup. |

### Question 3: For documentation metadata definitions, what authority is present?

For:

```text
document defines concept
```

Repository evidence supports:

| Candidate authority | Supported? | Evidence-based assessment |
| --- | --- | --- |
| Navigation metadata | Yes, strongly | Extracted from front matter and used by documentation navigation relationship facts. |
| Ontology | Partly/weakly | Catalog object type is `concept`, but the parser does not validate a broader ontology. |
| Teaching aid | Not directly | A document may teach, but the extractor only observes metadata. |
| Knowledge declaration | Limited | It declares metadata, not prose-derived truth. |
| Documentation classification | Yes | Front matter declares document classification fields and concept associations. |

### Question 4: Would an operator expect both shapes in the same graph relationship family?

Repository evidence supports a mixed answer.

Why an operator might expect them together:

- Both use the same predicate spelling, `defines`.
- Both can answer a broad discovery question: where is this thing introduced or declared?
- Source navigation reconciliation treats preserved definitions as important operator navigation anchors.

Why an operator might not expect them together:

- The catalog says `defines` is `document -> concept`.
- Documentation metadata authority and source AST declaration authority cross different boundaries.
- One object is an authored concept label; the other is a dotted source symbol.
- Prior reconciliation documents warn against collapsing structure, behavior, ownership, and navigation.
- The prior audit found validator warnings because source `defines` facts do not satisfy the catalog's endpoint contract.

Evidence-based observation:

- The repository currently carries both under the same spelling in preserved facts, but it does not yet carry a single authority explanation that makes them the same graph relationship family without ambiguity.

### Question 5: Candidate reconciliation outcomes

This section evaluates outcomes only. It does not choose one.

#### Outcome A: One authority, all `defines` relationships mean the same thing

Repository support:

- The relationship catalog has one `defines` relationship.
- Both documentation metadata and source declaration producers use the same predicate spelling.
- Operator navigation can benefit from one broad discovery vocabulary.

Repository conflicts:

- The catalog shape is `document -> concept`, while source facts are module-like identity -> dotted symbol identity.
- Source extraction explicitly limits authority to syntactic declaration evidence.
- Documentation metadata explicitly comes from front matter and ignores body prose.
- Prior reconciliation work preserves distinctions between declarations, structure, behavior, reachability, and ownership.

Authority clarity:

- Clear only if the repository explicitly establishes one common authority for both documents/concepts and modules/symbols.
- Not clear under current evidence.

Risk:

- Overclaims that modules are documents or symbols are concepts without authority.
- Collapses source declaration into concept definition.
- May treat navigation convenience as ontology.

#### Outcome B: Shared vocabulary, different authorities, same spelling

Repository support:

- This describes current observable behavior: the same spelling is used by documentation metadata and source declaration producers.
- Tests lock both documentation front-matter and source declaration emissions.
- Prior audit found multiple meanings accumulated under `defines`.

Repository conflicts:

- The relationship catalog has only one endpoint contract for the spelling.
- Graph validation has no authority-specific distinction if the predicate remains identical.
- Operators may see one relationship name and assume one meaning.

Authority clarity:

- Medium if documentation clearly records each authority and boundary.
- Low at graph-validation time unless another mechanism carries authority context.

Risk:

- Persistent warning pressure.
- Query ambiguity.
- Human misunderstanding because same spelling hides authority differences.

#### Outcome C: Different authorities, different relationships

Repository support:

- Prior reconciliations repeatedly separate evidence types and claim families when authority differs.
- Source declaration and documentation concept metadata have different subjects, objects, evidence, and boundaries.
- The current validator pressure is consistent with overloaded meaning.

Repository conflicts:

- Current catalog and tests use the spelling `defines` for both actual relationship producers.
- Source navigation currently filters `defines` facts.
- Any relationship split would be an implementation change outside this document's boundary.

Authority clarity:

- High as an analytical model: documentation concept definition and source declaration would no longer be forced to share one contract.
- Not established as an implementation decision here.

Risk:

- Migration cost.
- Backward compatibility concerns.
- Query and documentation updates would be required if ever implemented.
- Could prematurely split vocabulary if a valid shared authority is later articulated.

## Pressure analysis

The warning volume reported by the prior audit is best understood as pressure from unresolved relationship meaning, with missing endpoint types as the immediate validator symptom.

Evidence for missing-type pressure:

- The catalog requires `defines` endpoints to type as `document -> concept`.
- Source `defines` facts are emitted with module-like subjects and dotted symbol objects.
- Projection currently does not assert those source endpoints as `document` and `concept`.

Evidence that missing types are not the whole issue:

- Adding endpoint type assertions would itself make an authority claim: module-like source identities are documents and dotted symbols are concepts.
- Source extraction documentation explicitly says definitions are syntactic declaration evidence only.
- Documentation metadata `defines` is authored front-matter concept metadata, not source AST declaration.
- Prior reconciliation documents repeatedly warn that static evidence must not be upgraded into stronger semantic, behavior, or ownership claims.

Pressure source identified:

```text
relationship meaning unresolved
```

The missing types are the place where the validator reports the problem. The deeper pressure is that one catalog relationship spelling currently carries at least two actual relationship authorities with different endpoint shapes.

## Analogy analysis

Prior reconciliation patterns include:

```text
measurement != ownership
visibility != ownership
candidate != fact
ambiguity != truth
```

Repository evidence supports a cautious similar distinction:

```text
declaration != concept definition
```

Support for the analogy:

- Source declaration evidence is explicitly bounded to syntax.
- Documentation concept definition evidence is explicit metadata.
- Structure reconciliation distinguishes `X defines Y.` from `X defines method Y.`.
- Behavior reconciliation states method containment is not behavior.
- Relationship fact reconciliation separates artifact facts from relationship facts and says definitions/declarations do not prove flow, execution, routing, storage, emission, or validation.

Why the analogy may be too strong if stated absolutely:

- A future ontology could intentionally model some declarations as concepts with explicit authority.
- Documentation can use a source symbol as a concept label if authored that way.
- Operator navigation may reasonably use one word, `defines`, for both discovery paths.

Evidence-based formulation:

```text
Under current repository evidence, source declaration is not automatically concept definition.
```

That formulation matches previous reconciliation style without forbidding a future explicit authority decision.

## Major findings

1. The repository currently carries at least two actual `defines` relationship authorities: documentation metadata concept definition and repository-source syntactic declaration.
2. The documentation metadata authority directly matches the current catalog shape `document -> concept`.
3. The repository-source authority emits module-like subjects and dotted symbol objects, and it does not by itself establish document/concept endpoint authority.
4. Documentation prose uses `defines` in additional claim families, but those are not actual graph `defines` relationship producers.
5. The warning pressure is not merely a missing-type problem; missing types expose unresolved relationship meaning.
6. Source navigation evidence supports declaration-location navigation and narrowly scoped definition-location ownership, but not behavior, capability ownership, semantic meaning, or concept formation.
7. Repository evidence supports the cautious distinction `declaration != concept definition` under current authority boundaries.

## Remaining uncertainties

- Whether the repository should eventually model source modules as documents is not decided here.
- Whether the repository should eventually model source symbols as concepts is not decided here.
- Whether one shared `defines` vocabulary can be made authoritative with additional context is not decided here.
- Whether graph validation should become authority-aware is not decided here.
- Whether documentation front-matter concepts should be validated against an entity catalog is not decided here.
- Whether source navigation should preserve the same predicate spelling forever is not decided here.

## Non-conclusions

This observation does not conclude that any relationship should be renamed.

This observation does not conclude that any relationship should be split.

This observation does not conclude that entity types should be added.

This observation does not conclude that catalog entries should be changed.

This observation does not conclude that graph validation should be weakened or warnings suppressed.

This observation does not conclude that source ingestion, projection behavior, documentation metadata extraction, or source navigation should be modified.

The only conclusion is observational: current repository evidence shows multiple authorities being carried under the same `defines` vocabulary, and authority must be understood before behavior changes are considered.

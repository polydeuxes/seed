# Repository Observation Source Design

## Scope

This design defines architecture boundaries and vocabulary for a possible future
Repository Self Observation acquisition domain. It is documentation only.

It does not implement repository observation, repository scanning, repository
indexing, repository mutation, repository repair, repository governance,
repository management, self-modification, capability execution, provider
execution, verification execution, refresh execution, architecture enforcement,
documentation enforcement, test enforcement, code generation, `Runtime`
integration, `ToolExecutor` integration, `EventLedger` ownership changes,
`ProjectionStore` ownership changes, new predicates, new observation sources, or
new runtime behavior.

The intended future shape remains:

```text
Observation -> Evidence -> Fact -> Projection -> Explanation -> Response
```

Repository observation, if implemented later, should answer bounded questions
about what repository-local evidence says. It must not decide what Seed should
change, repair, execute, verify, or enforce.

## Files inspected

Minimum requested sources inspected:

- `docs/self_observation_reconciliation.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/capability_extension_methodology.md`
- `docs/context_composition_vocabulary.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/invariants.md`
- `docs/architecture.md`
- `docs/architecture_principles.md`
- `docs/reasoning_roadmap.md`
- `README.md`

Relevant generated architecture documentation inspected:


Additional nearby architecture documentation considered where it clarified
repository-local knowledge shape:

- `docs/self_observation_audit.md`
- `docs/canonical_documentation_reconciliation.md`
- `docs/capability_ownership_matrix.md`
- `docs/capability_verification_vocabulary.md`
- `docs/rule_inventory.md`
- `docs/knowledge_acquisition_status.md`

## Design finding

Repository Self Observation is a valid future acquisition domain only when it is
narrow, read-only, evidence-backed, projection-backed, and knowledge-first. The
repository already contains many structured knowledge surfaces: catalogs,
architecture metadata, generated architecture artifacts, documentation,
invariants, tests, roadmap documents, and ownership labels. Those surfaces can
support future facts about Seed itself, but only if each fact says no more than
its selected source directly supports.

The safe framing is:

```text
Seed observes selected repository evidence to explain what Seed knows about its
own declared architecture and vocabulary.
```

The unsafe framings are:

```text
Seed manages its repository.
Seed fixes its repository.
Seed verifies itself because a test exists.
Seed executes a capability because a capability is defined.
Seed routes Runtime behavior from repository metadata.
Seed enforces architecture because an invariant is documented.
Seed treats LLM-generated summaries as repository truth.
```

## Repository-local observation sources

A repository-local observation source is a bounded, named, read-only source that
exists inside the repository and can provide evidence for one or more repository
facts. Future implementation should prefer explicit source selection over broad
repository indexing.

Candidate sources:

| Source | Natural evidence | Appropriate use | Boundary |
| --- | --- | --- | --- |
| Canonical architecture docs | `docs/architecture.md`, `docs/architecture_principles.md`, `docs/invariants.md` | Declared architecture boundaries and invariants | Documentation claims are declarations, not runtime verification. |
| Knowledge vocabulary docs | knowledge acquisition, lifecycle, classification, context, and explanation vocabulary docs | Declared vocabulary ownership and conceptual boundaries | Vocabulary existence does not add behavior. |
| Capability methodology docs | `docs/capability_extension_methodology.md` and capability verification vocabulary docs | Question/evidence/fact methodology and capability non-inference boundaries | Capability methodology does not authorize execution. |
| Catalog source or generated inventories | Predicate, entity type, relationship, inference, and capability catalogs or deterministic inventory docs | Declared vocabulary entries and catalog ownership | Catalog entry existence does not imply implementation, verification, or availability. |
| Test files and invariant tests | Explicit test files, test names, and test metadata | Test inventory facts, if later selected narrowly | Test existence does not mean the test passes or is canonical. Running tests is outside observation. |
| Roadmap and reconciliation docs | Roadmap, audit, reconciliation, and status docs | Roadmap item declarations, future-candidate status, boundary decisions | Roadmap mention does not mean completion or commitment. |
| Canonical/generated documentation sets | Promoted docs and generated architecture artifacts | Document identity, generated-document identity, declared source relationships | File existence does not imply canonical status unless a canonical source says so. |
| Ownership metadata embedded in source | `__seed_arch__`-style static metadata | Ownership labels for named components | Static metadata is declaration evidence, not behavior execution or enforcement. |

Sources that should not be used as repository observation sources for this
domain:

- live `Runtime` calls;
- `ToolExecutor` calls;
- provider APIs;
- network calls;
- shell commands or subprocess output;
- mutation results;
- test execution results;
- code-generation output produced on demand by observation;
- LLM-generated summaries without source-grounded evidence;
- broad recursive repository scans presented as a first slice.

## Candidate observation domains

| Domain | Status | Rationale |
| --- | --- | --- |
| Predicates | Future candidate | Predicate catalogs and vocabulary docs are natural read-only evidence for declared predicate identity and classification. |
| Entity Types | Future candidate | Entity type catalogs and rule inventory docs can support entity-type existence and declared purpose facts. |
| Relationships | Future candidate | Relationship catalogs and generated architecture edges can support relationship-vocabulary and declared topology facts. |
| Capabilities | Future candidate | Capability catalogs and capability docs can support declared capability metadata, with strict non-execution boundaries. |
| Operations | Future candidate, narrow only | Registered operation catalogs can support operation-contract existence, but observation must never execute or imply availability. |
| Implementations | Future candidate, narrow only | Static architecture metadata can support declared component identity and owner labels; avoid code comprehension or quality claims. |
| Providers | Future candidate, narrow only | Provider recommendation metadata can support provider-definition facts, not provider availability or credentials. |
| Tests | Future candidate, narrow only | Explicit test files can support test-exists facts, not passing, coverage, or enforcement claims. |
| Invariants | Future candidate | Invariant documentation can support invariant-declared facts, not enforced architecture claims. |
| Canonical Documents | Future candidate | Canonical documentation reconciliation can support document role facts when explicit. |
| Generated Documents | Future candidate | Generated architecture artifacts can support generated-artifact identity and source facts. |
| Roadmap Items | Future candidate | Roadmap and reconciliation docs can support roadmap-item-exists or status-declared facts. |
| Architecture Metadata | Implemented as repository artifacts; future candidate as facts | Generated graph and static metadata already exist as artifacts, but are not projected repository facts. |
| Ownership Metadata | Strongest first candidate | Owner labels in generated architecture artifacts are explicit and bounded. |
| Generated Architecture Artifacts | Strongest first evidence source | Existing generated architecture graph is structured, source-attributed, and narrower than broad repository indexing. |

Domains that should remain external to Repository Self Observation:

- package vulnerability state;
- dependency freshness or update recommendations;
- GitHub issue state, pull request state, or CI state from remote services;
- team/process governance;
- deployment state;
- production runtime health;
- external provider availability;
- license compliance judgments unless later backed by a separate explicit
  evidence source and vocabulary;
- code quality scoring;
- broad semantic code understanding generated by an LLM.

Domains that should never be observed by this acquisition domain:

- secrets and credentials;
- private keys and tokens;
- uncommitted operator-local personal data;
- arbitrary file contents unrelated to explicit repository observation sources;
- build artifacts created only by executing code during observation;
- mutation outcomes;
- generated patches;
- automatic remediation plans treated as facts.

## Domain question/evidence/fact sketches

The following sketches define possible future vocabulary shape. They are not new
predicates and do not implement behavior.

### Predicates

Question: What predicates exist?

Evidence: Predicate catalog entries or deterministic predicate inventory docs.

Potential fact: `predicate_exists(predicate_id)`; optional declared attributes
such as class, cardinality, or support policy if directly present.

Potential non-inferences:

- `predicate_exists` != capability implemented;
- `predicate_exists` != observation source implemented;
- `predicate_exists` != predicate currently populated;
- `predicate_exists` != predicate verified;
- `predicate_exists` != predicate canonical unless a canonical catalog source
  explicitly says so.

### Entity Types

Question: What entity types are declared?

Evidence: Entity type catalog entries, rule inventory docs, or explicit entity
vocabulary documentation.

Potential fact: `entity_type_declared(entity_type_id)`; optional declared parent
or allowed relationship metadata if directly present.

Potential non-inferences:

- `entity_type_declared` != any entity currently exists;
- `entity_type_declared` != all entities are correctly typed;
- `entity_type_declared` != graph validation has passed;
- `entity_type_declared` != ownership over matching external resources.

### Relationships

Question: What relationship vocabulary or declared architecture relationships
exist?

Evidence: Relationship catalog entries, rule inventory docs, generated
architecture graph edges, or generated diagrams.

Potential fact: `relationship_defined(relationship_id)` or
`architecture_edge_declared(from_component, relation, to_component)`.

Potential non-inferences:

- `relationship_defined` != relationship currently true;
- `architecture_edge_declared` != runtime call occurred;
- `architecture_edge_declared` != reachability;
- `relationship_defined` != architecture enforced;
- generated edge existence != source code currently conforms unless freshness and
  source provenance independently support that narrower claim.

### Capabilities

Question: What capabilities are declared or recommended?

Evidence: Capability catalog entries, capability ownership matrix, capability
verification vocabulary, and capability extension methodology docs.

Potential fact: `capability_defined(capability_id)`; optional
`capability_provider_recommended` if directly declared by read-only metadata.

Potential non-inferences:

- `capability_defined` != capability verified;
- `capability_defined` != capability executable;
- `capability_defined` != user authorized execution;
- `capability_defined` != provider available;
- `capability_defined` != implementation exists;
- provider recommendation != provider integration.

### Operations

Question: What registered operation contracts are declared?

Evidence: Tool registry metadata, registered operation catalog documentation, or
architecture graph nodes/edges that name registered operation ownership.

Potential fact: `registered_operation_declared(operation_id)`.

Potential non-inferences:

- `registered_operation_declared` != operation executed;
- `registered_operation_declared` != operation available in this process;
- `registered_operation_declared` != policy permits execution;
- `registered_operation_declared` != provider capability;
- observation must not call `ToolExecutor` to test it.

### Implementations

Question: Which implementation components are declared, and what owner labels do
they carry?

Evidence: Generated architecture graph nodes and static architecture metadata
embedded in source.

Potential fact: `component_declared(component_id)` or
`architecture_owner_declared(component_id, owner_label)`.

Potential non-inferences:

- `component_declared` != code quality;
- `component_declared` != runtime activity;
- `architecture_owner_declared` != operational responsibility outside the
  repository;
- static metadata != architectural compliance;
- component summary != complete behavior specification.

### Providers

Question: What provider recommendation metadata is declared?

Evidence: Capability catalog provider recommendation metadata and provider
vocabulary docs.

Potential fact: `provider_defined(provider_id)` or
`provider_recommended_for_capability(provider_id, capability_id)`.

Potential non-inferences:

- `provider_defined` != provider available;
- `provider_defined` != provider configured;
- `provider_defined` != credentials exist;
- `provider_defined` != network reachable;
- `provider_defined` != execution permitted.

### Tests

Question: What tests are declared for a selected architecture concern?

Evidence: Explicit test files, test names, test inventories, or documentation
that names invariant tests.

Potential fact: `test_exists(test_id)` or
`test_targets_architecture_concern(test_id, concern_id)`.

Potential non-inferences:

- `test_exists` != test passing;
- `test_exists` != coverage complete;
- `test_exists` != invariant enforced;
- `test_exists` != test recently run;
- `test_exists` != behavior verified;
- repository observation must not execute tests.

### Invariants

Question: What invariants are documented?

Evidence: `docs/invariants.md` and any future explicit invariant catalog.

Potential fact: `invariant_exists(invariant_id)` or
`invariant_declares_boundary(invariant_id, boundary_id)`.

Potential non-inferences:

- `invariant_exists` != invariant enforced;
- `invariant_exists` != test exists;
- `invariant_exists` != test passing;
- `invariant_exists` != architecture currently compliant;
- documented invariant != automatic remediation authority.

### Canonical Documents

Question: Which documents are canonical for a named architecture concern?

Evidence: Canonical documentation reconciliation docs, README document map, or
explicit documentation status metadata.

Potential fact: `canonical_document_declared(document_path, concern_id)`.

Potential non-inferences:

- `document_exists` != document canonical;
- `canonical_document_declared` != document complete;
- `canonical_document_declared` != document up to date;
- `canonical_document_declared` != enforcement;
- `canonical_document_declared` != generated artifact freshness.

### Generated Documents

Question: Which architecture documents are generated artifacts?

Evidence: Generated architecture docs, generated graph, generated diagrams, and
explicit generation notes.

Potential fact: `generated_document_declared(document_path, generator_id)` or
`generated_artifact_contains_component(artifact_path, component_id)`.

Potential non-inferences:

- generated artifact exists != artifact fresh;
- generated artifact exists != source conforms;
- generated artifact exists != generator should run;
- generated artifact exists != repository mutation permitted.

### Roadmap Items

Question: What roadmap or reconciliation items are declared?

Evidence: `docs/reasoning_roadmap.md`, roadmap reconciliation docs, audits, and
status docs.

Potential fact: `roadmap_item_exists(roadmap_item_id)` or
`roadmap_item_status_declared(roadmap_item_id, status)`.

Potential non-inferences:

- `roadmap_item_exists` != roadmap completed;
- `roadmap_item_exists` != implementation approved;
- `roadmap_item_exists` != execution scheduled;
- `roadmap_item_status_declared` != test verification;
- roadmap text != product commitment.

### Architecture Metadata and Ownership Metadata

Question: Which components, layers, owners, and route labels are declared by the
architecture artifact?

records, plus generated diagrams as secondary documentation evidence.

Potential fact: `architecture_component_declared(component_id)`;
`architecture_owner_declared(component_id, owner_label)`;
`architecture_route_declared(from_component, to_component, route_label)`.

Potential non-inferences:

- architecture owner label != runtime owner change;
- route label != runtime call happened;
- owner label != self-management authority;
- component exists != component is active;
- generated graph != automatic architecture enforcement.

## Appropriate repository-local evidence

Future repository observation should treat evidence as explicit source/support
records with enough provenance for explanation. Appropriate evidence fields
include:

- source file path;
- generated artifact path;
- source kind, such as documentation, generated architecture graph, catalog,
  static metadata, test declaration, or roadmap document;
- section heading, node ID, edge ID, catalog entry ID, or test name when known;
- line range when the selected source is line-oriented;
- JSON pointer or object key when the selected source is structured;
- generator identity when evidence comes from a generated artifact;
- observed-at timestamp of the read-only observation event;
- payload summary small enough to avoid turning evidence into a repository index.

Evidence should not include:

- secret values;
- large arbitrary file payloads;
- LLM-generated claims without source attribution;
- command output produced by executing tools during observation;
- unbounded recursive file lists;
- inferred truth beyond the selected source.

## Candidate fact families

Future fact families should remain small and source-shaped:

1. **Repository identity facts** — repository root identity, selected artifact
   identity, document identity, component identity.
2. **Repository vocabulary facts** — predicate, entity type, relationship,
   capability, operation, provider, and invariant declarations.
3. **Repository architecture facts** — generated component, owner, layer, route,
   and boundary declarations.
4. **Repository documentation facts** — canonical-document declarations,
   generated-document declarations, and document-concern links.
5. **Repository roadmap facts** — roadmap item declarations and explicitly stated
   roadmap status.
6. **Repository test-inventory facts** — selected test declaration facts only;
   no execution outcome facts.
7. **Repository integrity signal facts** — only weak, evidence-backed signals such
   as generated-artifact-declared or source-provenance-present. These must not be
   named or treated as enforcement, compliance, repair, freshness, or pass/fail
   facts unless a later explicit source and vocabulary is designed.

Facts should never include:

- secrets;
- inferred code quality;
- inferred documentation quality;
- inferred architecture compliance;
- inferred test pass/fail results;
- inferred provider availability;
- inferred runtime health;
- inferred capability verification;
- inferred mutation authority;
- suggested patches;
- remediation plans;
- LLM-created repository truth.

## Knowledge classification fit

Repository-local knowledge fits the existing documentation-only knowledge
classes with the same caution that classification is not behavior.

| Class | Repository-local fit | Examples | Boundary |
| --- | --- | --- | --- |
| Identity | Names or distinguishes repository subjects | repository root, document path, generated artifact, component ID, predicate ID | Identity does not imply ownership over mutation or global uniqueness outside the repository. |
| Configuration | Declared settings or vocabulary entries | catalog declarations, invariant declarations, owner labels, route labels, provider recommendations | Configuration does not imply availability, correctness, verification, or execution. |
| Topology | Structure and relationships among repository concepts | generated graph edges, component-to-owner links, document-to-concern links, test-to-concern links | Topology does not imply runtime reachability, active calls, enforcement, or management. |
| Description | Human-readable summaries and metadata | component summaries, document purposes, roadmap descriptions, capability descriptions | Description does not imply implementation quality, completeness, or fitness. |
| State | Volatile or status-like repository declarations | roadmap status, generated-artifact declared status, test-inventory presence, possible future freshness metadata | State must be treated conservatively and must not become verification, refresh, or enforcement behavior. |

Repository observation differs from host observation because many repository
facts are declarations about Seed's own architecture rather than live operational
measurements. Host observation often reads operating-system surfaces; repository
observation should read committed source, generated artifacts, and docs.
Repository declarations are usually more stable but also more prone to
non-inference mistakes: a declared invariant, test, capability, or owner label is
not proof that the runtime, tests, providers, or architecture currently behave as
declared.

## Capability Extension Methodology fit

Repository observation follows the existing methodology when it starts with a
question and chooses the narrowest evidence-backed fact.

| Methodology step | Repository observation interpretation |
| --- | --- |
| Question | Ask one bounded repository question, such as: "Which component owns this declared architecture behavior?" |
| Evidence | Read one explicitly named source, such as the generated architecture graph node for the component. |
| Fact | Project only the directly supported declaration, such as a component owner label. |
| Non-inference | Preserve that the owner label is not verification, enforcement, runtime routing, or management authority. |
| Projection | Let existing projection concepts expose the latest-current repository fact if future implementation adds events. |
| Explanation | Explain the fact from evidence path, object key or line range, and source kind. |
| Response | Communicate what is known, what source supports it, and what remains unknown. |

Repository observation should not start from a desired capability such as
"repair architecture drift" or "manage docs." It should start from an answerable
knowledge question and remain within acquisition.

## Ownership model

Repository observation should preserve existing ownership and avoid creating new
engines.

| Concern | Recommended owner model | Notes |
| --- | --- | --- |
| Repository observation sources | Future narrow acquisition adapter under existing observation/acquisition concepts | No `RepositoryEngine`, no scheduler, no planner, no runtime owner. |
| Repository evidence | Existing evidence/provenance model | Evidence records should cite repository source path/object/line and remain auditable. |
| Repository facts | Existing fact model and predicate governance, if predicates are later added deliberately | No facts in this design phase. Future facts should be narrow declarations. |
| Repository projections | Existing `StateProjector` / `ProjectionStore` ownership | Projection remains derived from append-only events; no separate repository state store. |
| Repository explanations | Existing explanation/evidence graph concepts | Explanations read projected facts and evidence; they do not inspect the repository live. |
| Repository integrity signals | Existing integrity vocabulary only if explicitly designed later | Avoid `RepositoryIntegrityEngine`; signals are read-only and non-remediating. |
| Architecture metadata | Existing generated architecture artifact ownership | Generated artifacts may become evidence, not runtime control surfaces. |
| Capability metadata | Existing `CapabilityCatalog` ownership | Capability observation must not move provider recommendation or execution ownership. |
| Registered operations | Existing `ToolRegistry`/`ToolExecutor` boundary | Operation declarations are not operation execution. |
| Runtime routing | Existing `Runtime` ownership | Repository observation must not alter routing or decision behavior. |
| Event history | Existing `EventLedger` ownership | No separate event ledger or repository audit database. |

## Boundaries to preserve

Repository observation must remain:

- read-only;
- evidence-backed;
- projection-backed;
- knowledge-first;
- bounded to explicit source selections;
- explanation-oriented;
- compatible with existing acquisition, projection, and explanation ownership.

Repository observation must not imply:

- self-modification;
- self-repair;
- self-management;
- repository mutation;
- capability execution;
- provider execution;
- `Runtime` execution;
- `ToolExecutor` execution;
- verification execution;
- refresh execution;
- architecture enforcement;
- documentation enforcement;
- test enforcement;
- code generation;
- automatic remediation;
- hidden scheduling;
- policy bypass;
- broad indexing;
- LLM reasoning as truth.

## Important non-inferences

These non-inferences should be carried into any future predicate, test, or
explanation vocabulary:

- `predicate_exists` != capability implemented;
- `predicate_exists` != observation source implemented;
- `predicate_exists` != fact currently populated;
- `entity_type_declared` != matching entities currently exist;
- `relationship_defined` != relationship currently true;
- `architecture_edge_declared` != runtime call occurred;
- `capability_defined` != capability verified;
- `capability_defined` != capability executable;
- `registered_operation_declared` != operation executed;
- `registered_operation_declared` != policy permits execution;
- `test_exists` != test passing;
- `test_exists` != coverage complete;
- `document_exists` != document canonical;
- `canonical_document_declared` != document current or complete;
- `generated_document_exists` != generated document fresh;
- `provider_defined` != provider available;
- `provider_defined` != credentials configured;
- `roadmap_item_exists` != roadmap completed;
- `invariant_exists` != invariant enforced;
- `owner_label_declared` != ownership over runtime mutation;
- `component_declared` != component active;
- `source_metadata_exists` != source behavior correct;
- `catalog_entry_exists` != provider integration;
- `evidence_source_read` != repository-wide scan;
- `repository_fact_projected` != permission to modify the repository.

## Complexity traps to avoid

Repository observation should not introduce or imply any of the following:

- `RepositoryEngine`;
- `RepositoryManager`;
- `RepositoryMaintenanceEngine`;
- `RepositoryIntegrityEngine`;
- `SelfModificationEngine`;
- `ArchitectureEnforcementEngine`;
- `DocumentationEnforcementEngine`;
- `RepositoryPlanner`;
- `RepositoryAgent`;
- `RepositoryRepairLoop`;
- `RepositoryGovernanceEngine`;
- automatic remediation;
- automatic repository correction;
- repository-wide semantic indexing as a first step;
- LLM-generated repository truth;
- hidden test runners;
- hidden documentation generators;
- hidden architecture generators;
- hidden provider calls;
- hidden shell/subprocess calls.

The safest mental model is a narrow acquisition adapter reading one named
repository artifact, not an engine managing a repository.

## Recommended acquisition order

Repository observation should grow from the most explicit, most structured, and
least volatile evidence toward less structured evidence only after vocabulary and
boundaries remain stable.

1. **Generated architecture ownership metadata** — ask which component has which
   narrowest, strongest first target because the artifact is structured and
   already close to the architecture vocabulary.
2. **Generated architecture edge metadata** — ask which declared route or edge
   exists between named components. Keep this separate from runtime-call claims.
3. **Invariant declarations** — ask which invariant statements exist for a named
   boundary. Do not infer enforcement.
4. **Canonical document declarations** — ask which document is declared canonical
   for a concern, where explicit documentation supports that claim.
5. **Catalog vocabulary declarations** — ask which predicates, entity types,
   relationships, capabilities, providers, or operations are declared by a
   selected catalog source.
6. **Generated document identity** — ask which generated artifacts exist and what
   generator/source metadata is declared.
7. **Roadmap item declarations** — ask which roadmap items exist or have an
   explicitly stated status.
8. **Selected test inventory** — ask only whether a named test declaration exists
   for a named concern. Do not execute tests or infer passing status.

This order intentionally delays tests, broad catalog coverage, roadmap state,
and freshness-like integrity signals because they create stronger temptation to
infer verification, enforcement, scheduling, or remediation.

## Recommended smallest future implementation slice

The smallest safe implementation slice, if a later task explicitly asks for
code, should be:

> Answer: "What evidence says which component owns a named architecture behavior
> or component?"

Recommended shape:

- Source: a single explicitly named generated artifact,
- Input: a named component ID only; no repository scan and no free-form code
  search.
- Evidence: graph node ID, owner label, layer, summary, artifact path, and JSON
  object pointer.
- Potential fact family: `architecture_component_declared` and
  `architecture_owner_declared` only, if future predicate design approves those
  names or equivalents.
- Projection: existing event/fact/projection path only; no repository state
  store.
- Explanation: show the artifact evidence and the non-inferences.
- Explicit exclusions: no `Runtime` changes, no `ToolExecutor` changes, no test
  execution, no architecture generation, no source-code scanning, no provider
  calls, no mutation, no repair, no enforcement.

A deliberately narrow example future question:

```text
Which generated architecture evidence declares ToolExecutor's owner?
```

A deliberately narrow example future answer shape:

```text
The generated architecture graph declares component ToolExecutor with owner
registered_tool_execution. This is a generated architecture declaration. It does
not mean ToolExecutor was invoked, that an operation is available, that policy
permits execution, or that architecture enforcement has run.
```

This slice fits existing acquisition architecture because it starts with a
question, reads a bounded read-only source, records evidence, projects a narrow
fact, and answers through explanation without execution.

## Final design conclusion

Repository Self Observation should become first-class only as a conservative
Knowledge Acquisition domain. Its sources should be explicit repository-local
artifacts and docs, its evidence should preserve path/object/line provenance,
its facts should be narrow declarations, and its projections should remain
ordinary read-only projected knowledge. It should not create new engines,
runtime owners, managers, planners, repair loops, governance loops, or automatic
enforcement behavior.

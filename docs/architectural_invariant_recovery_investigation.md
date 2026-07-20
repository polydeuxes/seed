# Architectural invariant recovery investigation

## Scope and method

This is a recovery report only. It does not propose a universal grammar, architectural framework, ontology, runtime redesign, shared interface, or abstraction layer. It asks whether implementation-backed recurrence already exists across independently recovered grammars, and where that recurrence stops.

Commands used during this investigation:

```bash
pwd && rg --files -g 'AGENTS.md' -g '*investigation*.md' -g '*.py' | head -200
cat AGENTS.md
sed -n '1,220p' implementation_promotion_grammar_recovery_investigation.md
sed -n '1,180p' implementation_execution_grammar_recovery_investigation.md
rg --files docs | rg 'relationship|artifact|operation|capability|authority|structure|presentation|answer|execution' | head -80
sed -n '1,220p' operation_capability_observation_recovery_investigation.md
sed -n '1,180p' tool_vocabulary_orientation_recovery_investigation.md
sed -n '1,180p' docs/implementation_relationship_grammar_investigation.md
sed -n '1,170p' docs/implementation_artifact_explanation_grammar_investigation.md
sed -n '1,120p' seed_runtime/observations.py
sed -n '1,120p' seed_runtime/capability_candidates.py
sed -n '1,120p' seed_runtime/registry.py
sed -n '1,100p' seed_runtime/diagnostic_inventory.py
sed -n '1,100p' seed_runtime/projection_shape.py
```

Primary evidence reviewed includes:

- `implementation_promotion_grammar_recovery_investigation.md`
- `implementation_execution_grammar_recovery_investigation.md`
- `operation_capability_observation_recovery_investigation.md`
- `tool_vocabulary_orientation_recovery_investigation.md`
- `docs/implementation_relationship_grammar_investigation.md`
- `docs/implementation_artifact_explanation_grammar_investigation.md`
- `seed_runtime/observations.py`
- `seed_runtime/capability_candidates.py`
- `seed_runtime/capability_verification.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/registry.py`
- `seed_runtime/execution.py`
- `seed_runtime/runtime.py`
- `seed_runtime/state.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/documentation_structure.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/knowledge_reachability.py`

Repository implementation is treated as authority over investigation vocabulary.

## Executive answer

Yes. Independently recovered grammars preserve recurring architectural invariants, but the recurrence is not a single lifecycle and not one promotion grammar.

The strongest invariant is not:

```text
observation -> one universal promotion pipeline -> execution
```

The implementation-backed recurrence is instead:

```text
bounded input
  -> preserved support / provenance / declaration
  -> owner-specific validation or derivation
  -> bounded output / projection / registration / rendering
  -> explicit termination
  -> explicit non-promotion boundary
```

This recurrence appears across observation, capability, execution, promotion, relationships, presentation, projection, diagnostics, documentation structure, repository artifacts, and question/inquiry surfaces. The terms, owners, registries, validators, and outputs differ intentionally.

Therefore, the grammars feel structurally similar because they repeatedly preserve responsibility boundaries: each family distinguishes input from authority, support from proof, candidate from registration, projection from ledger truth, presentation from knowledge, diagnostic recording from cluster mutation, and rendering from promotion.

The repository does **not** support the stronger conclusion that one grammar should replace the others.

## Grammar-by-grammar recovery

| Recovered grammar / family | Owner | Input | Support preservation | Validation | Promotion or output | Termination | Explicit boundaries | Explicit non-promotion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Observation ingestion | `ObservationIngestor` | `Observation` | Observation event plus derived evidence event preserve source, dimensions, confidence, expiry, and metadata. | Secret rejection, confidence bounds, fact-suppression rules, event construction. | Optional `Fact` event. | Observation/evidence/fact events appended, or observation/evidence only when fact promotion is suppressed. | Observation, evidence, and fact are separate records. | `_should_suppress_fact_promotion()` proves observation can be preserved without fact promotion. |
| Fact support / current belief | `StateProjector` and `State` support helpers | Fact events and evidence IDs | Fact support keeps supporting facts/evidence and source confidence. | Predicate semantics, expiration, measurement retention, conflict handling. | `FactSupport`, current belief, ambiguity/conflict, explanations. | Projected state / support indexes. | Projection is rebuilt from events; support is not the event ledger. | Competing facts can remain ambiguous; measurements can retain current sample rather than aggregate truth. |
| Capability candidate | `build_capability_candidates()` | Projected `package_installed` facts | Candidate evidence records fact ID, source, confidence, evidence IDs, and summaries. | Known package-to-candidate mapping only. | `CapabilityCandidateInspection`. | Read-only inspection result. | Candidate boundary is `capability_candidate_preservation_only`. | Candidate is not capability proof, permission, selection, policy evaluation, invocation, or execution. |
| Capability verification / inventory | `build_capability_verification_inspection()` and `build_capability_inventory()` | Candidates, PATH metadata, projected `capability_verified` facts | Verification evidence and fact support are preserved separately from candidates. | Candidate/inventory join, stale handling, verified/provider-reported state derivation. | Verified/stale/provider-reported/unverified read-model status. | Inventory or verification-inspection row. | Verification is a read model, not operation authority. | Candidate evidence without `capability_verified` support remains unverified. |
| Registered operation | `ToolRegistry`, toolkit manifest loader, toolkit registration service | Toolkit manifest / `Toolkit` / `ToolSpec` | Manifest fields preserve implementation, schema, policy action, visibility, status, capabilities. | Manifest required fields, duplicate checks, capability normalization, status/visibility filtering. | Registered operation catalog entries and `tool.registered` events. | Registry entry and model-visible list. | Registration is manifest/catalog authority, not discovery. | Package/binary/provider evidence and recommendations do not become registered operations. |
| Registered operation execution | `ToolExecutor` through `Runtime.call_tool` | Runtime decision naming a registered tool | Tool-call events and outputs preserve execution record. | Decision validation, registry lookup, policy service, schema validation, pending approval path. | Tool result plus ledger events/fact extraction when applicable. | Completed, failed, blocked, or pending result. | `ToolExecutor` owns registered-operation execution only. | Requesting a tool, catalog recommendation, and provider operation strings do not execute. |
| Runtime response / inquiry termination | `Runtime._route()` | Model decision | Response events preserve answer/question/refusal. | Decision validation before routing. | `RuntimeResponse` and response event. | Answer, question, or refusal. | Response branches bypass `ToolExecutor`. | Answer rendering does not imply operation execution. |
| Declarative state patch | `StatePatchService` | State patch operations | Translated ledger events preserve evidence/fact/entity update records. | Patch validation and allowed operation translation. | Ledger events and later projected state. | `state_updated` response with event IDs. | Ledger mutation is Seed-internal state mutation, not provider/tool execution. | State patch is not registered operation execution. |
| Projection | `StateProjector`, projection store/read-model helpers | Event ledger | Replayed events, derived indexes, cache/debug metadata. | Event application, finalization, catalogs, inference, graph validation. | Projected `State`, relationship/fact/entity/support indexes, read models. | Projected state, cache hit/miss, timing/report surface. | Projection reads event authority; it does not own event creation. | Projection diagnostics/cache are not new authority. |
| Relationships | Relationship observation adapter, `RelationshipCatalog`, `StateProjector` | Static syntax, document metadata, or fact predicates | Relationship facts preserve source syntax/metadata/fact support. | Catalog mapping, endpoint kinds, graph validation. | `RelationshipFact` / `EntityRelationship` / graph views. | Relationship projection / graph validation. | Relationship evidence is bounded to observed relationship kind. | Imports/definitions/front matter do not prove behavior, calls, ownership, or reachability. |
| Presentation / explanation | `ExplanationBuilder`, question surface inventory, audit builders, CLI renderers | Projected state, support, conflicts, audit inputs | Explanations preserve current support, ambiguity, unknowns, consumers, selected/non-selected evidence. | Surface-specific builders and inventory rows. | Human/JSON report, explanation, answer responsibility row. | Rendered answer/report. | Presentation vocabulary is not automatically knowledge. | Rendering current work, source navigation, topology, or cache terms does not promote repository knowledge. |
| Diagnostics | `DIAGNOSTIC_INVENTORY`, diagnostic implementations, shape audit | CLI surface declarations and implementation specs | Inventory rows preserve flags, dependencies, record support, ledger writes, mutation status. | `diagnostic_shape_audit` checks registry/spec conformance. | Visible diagnostic surface and optional diagnostic-scoped facts. | Report, JSON, or diagnostic-run recording. | Diagnostic recording is scoped; cluster mutation is explicit. | Recordable diagnostics use `record_scope=diagnostic_run` and `mutates_cluster=false` unless intentionally different. |
| Documentation structure | `documentation_structure` diagnostic family | Repository markdown/prose structure | Headings, front matter, links, code fences, skeletons, recurrence, outliers. | Structural parsing and recurrence checks. | Structural visibility report. | Documentation-structure report. | Structure visibility is not claim extraction. | No prose interpretation, authority inference, ontology promotion, ledger write, or repo mutation. |
| Repository artifact explanation | Artifact-local classes plus distributed inventories/audits | Code artifacts, CLI surfaces, registries, dataclasses | Identity, responsibility, inputs, outputs, consumers, preservation/cache, authority boundaries, unknowns. | Docstrings, `__seed_arch__`, inventory rows, audit builders, tests. | Explanation grammar recovered for artifacts/surfaces. | Explanation record/report. | Explanation fields are distributed, not universal. | Missing local owner/consumer fields are not proof that the artifact has no boundary. |
| Question / answer responsibility | `QuestionSurfaceInventoryRow` and answer-responsibility investigations | Question families and answering surfaces | Examples, surface, bounded ask status, answer responsibility, authority boundary. | Inventory row construction and diagnostic linkage. | Question surface inventory / bounded answer surface. | Selected answer surface or unknown/bounded result. | Question family mapping is surface responsibility, not ontology. | A question label does not create preserved knowledge by itself. |

## Recurring architectural invariants

### 1. Owner-specific responsibility recurs

Most families have an implementation owner for the transition they perform:

- observation ingestion owns observation/evidence/optional fact emission;
- projection owns event replay and derived indexes;
- capability candidate recovery owns evidence-derived candidate preservation;
- capability inventory owns verification-state read models;
- registry owns registered operation catalog state;
- executor owns registered operation execution;
- diagnostics own inventory-backed visibility and shape auditing;
- documentation structure owns read-only structural observation;
- presentation/audit surfaces own bounded reports.

The invariant is **not** one shared owner. The invariant is that ownerless promotion is repeatedly rejected.

### 2. Bounded input recurs

Each family accepts a narrower input than its vocabulary might suggest:

- observations are typed records, not arbitrary truth;
- package facts are candidate input, not capability proof;
- manifests are operation-contract input, not observed executable truth;
- event history is projection input, not generated by projection;
- static syntax/front matter are relationship input, not behavioral proof;
- CLI diagnostic rows are visibility declarations, not cluster mutation authority;
- markdown structure is structural input, not semantic claim authority.

### 3. Support preservation recurs

Support preservation appears under different names: evidence, support, metadata, manifest schema, fact IDs, source confidence, registry row fields, audit evidence, consumers, unknowns, cache identity, and event IDs.

The implementation repeatedly preserves why an output exists rather than emitting unsupported conclusions.

### 4. Validation or derivation recurs, but validators differ

Validation recurs as a boundary, but there is no universal validator:

- observation ingestion validates confidence and suppression rules;
- state projection validates through event application, catalogs, retention, inference, graph checks;
- capability candidates use package mapping and later verification joins;
- registered operations use manifest validation and registry uniqueness;
- execution uses decision validation, registry lookup, policy, and schema validation;
- diagnostics use inventory declarations and shape-audit specs;
- documentation structure uses structural parsing rather than semantic validation.

The invariant is **validation before authority-bearing output**, not a common validation mechanism.

### 5. Output is bounded to the family

Outputs do not escape their family by default:

- observation can terminate at observation/evidence without fact;
- candidate terminates as candidate inspection;
- verification terminates as read-model status;
- registered operation terminates in registry catalog state;
- execution terminates in tool-call result/events;
- projection terminates in projected read model;
- relationship projection terminates in bounded relationship facts/views;
- diagnostics terminate in reports or diagnostic-scoped facts;
- documentation structure terminates in structural reports.

### 6. Explicit non-promotion recurs

The most stable invariant is negative: many families explicitly say what their output is **not**.

Examples:

- observation is not always fact;
- evidence is not proof;
- candidate is not capability, permission, selection, policy, invocation, or execution;
- provider recommendation is not registered operation;
- registry metadata is not execution;
- projection cache/timing is not ledger authority;
- relationship syntax is not runtime behavior;
- presentation vocabulary is not knowledge;
- diagnostic recording is not cluster mutation;
- documentation structure is not claim extraction or ontology promotion.

### 7. Termination recurs

The grammars repeatedly terminate in explicit artifacts:

- event appended;
- fact suppressed or emitted;
- projected state built;
- inspection row returned;
- registry entry stored;
- runtime response returned;
- tool result completed/failed/blocked/pending;
- diagnostic report rendered or diagnostic-run facts recorded;
- documentation-structure report emitted.

Termination type varies, but undefined termination is uncommon in the strongest implementation-backed surfaces.

### 8. Authority is preserved as boundary, not centralized

Authority recurs through boundaries rather than one authority source:

- event ledger authority for projection;
- manifest/registry authority for registered operations;
- projected fact support for verification/read models;
- diagnostic inventory for operational visibility;
- static syntax/front matter/fact predicates for relationships;
- implementation evidence for presentation vocabulary promotion;
- structural parsing for documentation shape.

This explains recurrence without inventing a universal authority framework.

## Non-recurring properties

The following properties intentionally differ and should not be treated as invariants:

| Property | Does it recur? | Implementation-backed reason |
| --- | --- | --- |
| Validation owner | No. | Validators are ingestor, projector, registry, executor/policy service, diagnostic shape audit, documentation parser, relationship catalog, and audit builders depending on family. |
| Promotion mechanism | No. | Some families append events, some derive read models, some register manifests, some render reports, some only inspect. |
| Authority source | No. | Authority can come from event history, manifest declarations, projected fact support, registry rows, static syntax, markdown structure, or implementation tests. |
| Termination type | No. | Termination may be event, state, report, response, registry entry, pending action, failure, or diagnostic recording. |
| Registry/catalog presence | No. | Diagnostics and tools have registries; relationships have a catalog; observation ingestion and projection do not require the same kind of registry. |
| Projection | No. | Projection is central for state/facts/relationships/capability inventory, but documentation structure, manifest validation, and some presentation inventories can operate over repo files/static rows. |
| Execution | No. | Only registered operations execute through `ToolExecutor`; projection, diagnostics, state patches, and response rendering perform work without being registered-operation execution. |
| Owner field locality | No. | Some artifacts have explicit `__seed_arch__` owners; many read models have responsibility and boundary but no local owner field. |
| Catalog-driven semantics | No. | Relationship and diagnostic families are catalog/inventory-heavy; observation and runtime response branches are event/route-heavy. |
| Recordability | No. | Some diagnostics support record, most presentation/structure surfaces are read-only, and execution writes operational events. |

## Strongest level of recurrence

The recurrence is strongest at the level of **responsibility, boundary, support, and termination**.

It is weaker at the level of lifecycle because each family has different steps. It is weaker at the level of ownership if ownership means an identical owner field, but stronger if ownership means that each transition has an implementation-responsible component. It is weaker at the level of authority if authority is expected to be centralized, but strong if authority means explicit source-of-authority boundaries.

Ranked from strongest to weakest implementation-backed recurrence:

1. **Boundary / non-promotion** — strongest; repeatedly encoded in docstrings, inventory fields, audit outputs, and reports.
2. **Support preservation** — strong; evidence/support/provenance/metadata recur widely.
3. **Termination** — strong; outputs are usually explicit and bounded.
4. **Responsibility / owner-specific transition** — strong, though owner fields are sometimes implicit or distributed.
5. **Authority boundary** — strong, but authority sources differ.
6. **Validation** — strong as a concept, weak as a common mechanism.
7. **Lifecycle** — partial; similar shapes recur but no universal lifecycle exists.

## Why the grammars feel structurally similar

The grammars feel structurally similar because they repeatedly enforce the same architectural separation:

```text
input is not authority
support is not proof by itself
candidate is not registration
registration is not execution
projection is not ledger truth
presentation is not knowledge
recorded diagnostic output is not cluster mutation
structure is not semantic claim
```

They also preserve comparable slots even when names differ:

```text
who owns this transition?
what input is accepted?
what support is retained?
what validation or derivation occurred?
what output was produced?
where does it terminate?
what does this output explicitly not mean?
```

That shared responsibility shape is enough to explain the perceived similarity without asserting a universal grammar.

## Counterexamples and families that do not fully fit

### Counterexamples that intentionally preserve recurrence by refusing promotion

1. **Suppressed fact promotion:** some observations are recorded as observation/evidence without creating facts.
2. **Capability candidates:** candidate boundaries explicitly reject capability proof, permission, selection, policy evaluation, invocation, and execution.
3. **Verification evidence:** PATH binary metadata can support inspection while remaining non-invocation and non-registration.
4. **Provider recommendations:** catalog provider operation strings remain handoff/recommendation metadata unless separately registered.
5. **Runtime `request_tool`:** creates/resolves a capability need but does not execute.
6. **Projection:** event replay builds projected state but does not write the event ledger.
7. **Relationship observation:** syntax/front matter/fact mappings produce bounded relationships, not behavior or ownership proof.
8. **Diagnostics:** recordable diagnostics remain diagnostic-run scoped and non-cluster-mutating unless declared otherwise.
9. **Documentation structure:** structure reports intentionally refuse prose interpretation and ontology promotion.
10. **Presentation labels:** UI/report terms require implementation evidence before becoming knowledge.

### Families that only partially fit the recurring pattern

- **Runtime trace/status visibility:** strong responsibility and boundary, but often transient and not promoted into durable knowledge.
- **State-build/current-facts CLI surfaces:** real boundaries and outputs, but explanation is distributed across CLI helpers, projection store, timing reports, and tests rather than one artifact-local grammar.
- **Repository artifact explanation:** identity/responsibility/input/output/boundary recur, but owner and consumers are sometimes implicit.
- **Question family inventories:** strong surface responsibility and boundary, but question-family labels are not themselves knowledge or ontology.

### Potential violations to watch

The investigation did not find a strong implementation-backed family where all of the following are absent: owner/responsibility, boundary, support, termination, and non-promotion. The weaker cases are distributed-visibility cases, not clearly boundaryless promotion cases.

Risks for future investigation:

- a new diagnostic surface without inventory/shape-audit coverage;
- a presentation label reused as preserved knowledge without reachability evidence;
- a provider operation string treated as registered operation;
- a capability candidate treated as verified capability;
- projection/cache status treated as event authority;
- relationship syntax treated as behavioral proof;
- documentation recurrence treated as semantic claim extraction.

## Lexical, structural, operational, and knowledge promotion

These preserve similar invariants while differing in implementation.

| Promotion class | Preserved invariants | Different implementation |
| --- | --- | --- |
| Lexical | Vocabulary is bounded by implementation evidence; labels can be observed without becoming knowledge. | Tool vocabulary and presentation labels are recovered through docs, inventories, and reachability audits, not event promotion. |
| Structural | Structure is observed, support is preserved, semantic non-promotion is explicit. | Documentation structure parses markdown/prose shape; relationship observation parses syntax/front matter; both avoid broad meaning promotion. |
| Operational | Registration/execution boundaries are explicit; support and validation precede bounded operation output. | Tool manifests/registry/policy/executor differ from capability candidates and provider recommendations. |
| Knowledge | Observation/evidence/fact/support/projection boundaries preserve provenance and authority. | Ingestion/projection/fact support differ from relationship catalogs, diagnostics, and presentation surfaces. |

The invariant is the boundary discipline, not a shared implementation.

## Supported conclusions

1. Architectural invariants recur across independent grammars, especially responsibility, boundary, support preservation, authority boundary, termination, and explicit non-promotion.
2. The recurrence is implementation-backed and visible in code, tests, registries, diagnostics, and prior recovery reports.
3. The recurrence does not imply a universal grammar or single lifecycle.
4. Independently recovered grammars feel similar because they preserve similar architectural slots while assigning different owners and outputs.
5. Authority is recurring as a boundary discipline, not as one central authority source.
6. Support preservation is a stable reference frame for future recovery because each family requires evidence/provenance/declaration before stronger outputs are accepted.
7. Non-promotion boundaries are among the most reliable invariants in the repository.
8. Future recovery can use these invariants as a checklist without turning them into a new ontology.

## Unsupported conclusions

The implementation does not support these conclusions:

- one universal promotion grammar exists;
- one execution lifecycle owns all work;
- `ToolExecutor` owns projection, diagnostics, state patches, provider recommendations, or response rendering;
- observed packages/binaries/manuals are promoted into registered operations;
- provider operation strings are registered operations;
- candidate capability evidence is verified capability;
- documentation recurrence is semantic knowledge;
- presentation vocabulary is repository knowledge without reachability/implementation evidence;
- projection cache/status is ledger authority;
- relationship syntax proves behavior, calls, ownership, or reachability;
- all families share the same registry, catalog, validator, or termination artifact.

## Recommended next investigation

The next recovery-only investigation should examine **boundary failure modes in newly added surfaces**:

```text
When new visibility, diagnostic, presentation, or capability surfaces are added,
which implementation checks prevent them from bypassing inventory, support,
authority, termination, and non-promotion boundaries?
```

Suggested focus:

- recently added diagnostic surfaces and whether they are covered by diagnostic inventory and shape audit;
- presentation labels that might be mistaken for preserved knowledge;
- capability/provider/operation strings that might be mistaken for registered operations;
- relationship or documentation-structure recurrence that might be mistaken for semantic authority;
- cache/read-model outputs that might be mistaken for event-ledger authority.

This should remain a recovery investigation, not a proposal for a common framework.

## Acceptance answer

Implementation-backed architectural properties that recur are:

```text
owner or responsibility
bounded input
support preservation
validation or derivation before stronger output
bounded output
explicit authority boundary
explicit non-promotion
explicit termination
```

Properties that intentionally differ are:

```text
validator
registry/catalog mechanism
authority source
promotion mechanism
termination artifact
execution involvement
projection involvement
recording behavior
owner field locality
```

The invariant properties provide a stable reference frame for future recovery because they describe recurring implementation discipline without requiring shared vocabulary or a universal framework.

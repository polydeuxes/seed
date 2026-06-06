# Self-observation architecture audit

## Scope

This audit asks how Seed could treat its own repository as an observation source.
It is documentation only. It does not implement repository ingestion, self-modify
code, change `Runtime`, or add execution behavior.

## Files inspected

Architecture and ownership sources:

- `scripts/generate_architecture.py`
- `docs/generated/architecture/architecture_graph.json`
- `docs/generated/architecture/runtime_ownership.mmd`
- `docs/generated/architecture/runtime_ownership.dot`
- `docs/architecture_visualization_phase1.md`
- `docs/invariants.md`
- `docs/rule_inventory.md`
- `docs/capability_verification_audit.md`
- `docs/contradiction_handling_audit.md`
- `docs/temporal_reasoning_audit.md`
- `docs/tool_execution_ownership_audit.md`
- `docs/runtime_runtime_loop_responsibility_audit.md`
- `docs/runtime_loop_thin_runtime_plan.md`
- `docs/runtime_parity_inventory.md`

Runtime modeling and reasoning sources:

- `seed_runtime/observations.py`
- `seed_runtime/evidence.py`
- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/explanations.py`
- `seed_runtime/rule_inventory.py`
- `seed_runtime/entity_type_catalog.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/predicate_catalog.py`
- `seed_runtime/inference_catalog.py`
- `seed_runtime/runtime.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/execution.py`
- `seed_runtime/registry.py`
- `seed_runtime/capability_catalog.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/events.py`

Catalog and invariant checks:

- `entity_type_catalog/core.json`
- `relationship_catalog/core.json`
- `predicate_catalog/core.json`
- `inference_catalog/core.json`
- `tests/test_architecture_generator.py`
- `tests/test_architecture_invariants.py`
- `tests/test_rule_inventory.py`
- `tests/test_observations.py`
- `tests/test_evidence_facts.py`
- `tests/test_explanations.py`

## 1. Existing self-observation assets

Seed already has several repository-knowledge assets, but they are not yet wired
into the canonical observation pipeline as repository observations.

### Architecture generator

`scripts/generate_architecture.py` is the strongest current self-observation
asset. It performs a static Python AST scan over a selected set of runtime files,
extracts class-local `__seed_arch__` metadata, extracts limited `self.*` calls,
and emits three generated artifacts:

- `docs/generated/architecture/architecture_graph.json`
- `docs/generated/architecture/runtime_ownership.mmd`
- `docs/generated/architecture/runtime_ownership.dot`

Important properties:

- The scan is static and does not import runtime modules.
- Source coverage is explicit and limited to selected architecture-critical
  runtime files.
- The generated graph has source attribution through file paths and line numbers
  on source-backed nodes.
- The graph distinguishes source-backed nodes from synthetic external nodes.
- Edges are semantically labeled from ownership metadata, not inferred only from
  Python imports.
- Route metadata preserves runtime branch boundaries such as `request_tool` and
  `call_tool`.

This is close to a repository observation source in shape, but today it emits
architecture artifacts rather than `Observation`, `Evidence`, `Fact`, or
projected `EntityRelationship` records.

### `__seed_arch__` metadata

The current metadata embedded in source files already records ownership,
architectural layer, summaries, routes, events, and labeled edges for important
runtime components.

Source-backed components include:

| Component | Current owner | Layer | Repository source |
| --- | --- | --- | --- |
| `Runtime` | `runtime_orchestration` | `runtime` | `seed_runtime/runtime.py` |
| `ToolNeedService` | `tool_need_capability_resolution` | `runtime_service` | `seed_runtime/tool_needs.py` |
| `ToolExecutor` | `registered_tool_execution` | `execution` | `seed_runtime/execution.py` |
| `ToolRegistry` | `registered_operation_catalog` | `registry` | `seed_runtime/registry.py` |
| `CapabilityCatalog` | `capability_metadata` | `catalog` | `seed_runtime/capability_catalog.py` |
| `StateProjector` | `state_projection` | `state` | `seed_runtime/state.py` |
| `ProjectionStore` | `projection_cache` | `state` | `seed_runtime/projection_store.py` |
| `EventLedger` | `event_history` | `events` | `seed_runtime/events.py` |

Synthetic or external nodes currently generated from referenced edges include:

- `ToolRecommendationService`
- `RegisteredOperation`
- `ProviderRecommendation`
- `HandoffCandidate`
- `GraphValidator`
- `State`

These synthetic nodes are useful because they let the graph represent important
concepts even when the generator is not scanning a defining class or the concept
is not a source-backed runtime class in the selected file set.

### Generated architecture graph

The generated JSON graph already contains repository-derived nodes and
relationships. Examples of current generated facts in graph form:

- `Runtime` routes `request_tool` to `ToolNeedService`.
- `Runtime` routes `call_tool` only to `ToolExecutor`.
- `RuntimeLoop` is absent from the generated node set.
- `ToolExecutor` requires `ToolRegistry`.
- `ToolExecutor` may execute `RegisteredOperation`.
- `ToolExecutor` records tool-call events in `EventLedger`.
- `ToolNeedService` records tool-need events in `EventLedger`.
- `ToolNeedService` may expose registered operations through `ToolRegistry`.
- `ToolNeedService` may suggest providers and handoffs through
  `CapabilityCatalog`.
- `CapabilityCatalog` may suggest `ProviderRecommendation` and
  `HandoffCandidate` metadata.
- `StateProjector` reads `EventLedger`, produces `State`, and validates the
  projected graph through `GraphValidator`.
- `ProjectionStore` loads or saves projected snapshots and uses
  `StateProjector` when snapshots are stale.

The generated graph is already a compact repository knowledge base, but it is
not stored in Seed's event ledger and not projected as ordinary Seed facts.

### Ownership metadata

Ownership is already explicit in two places:

1. `__seed_arch__` metadata in source files records owner labels for generated
   architecture nodes.
2. `docs/invariants.md` and recent audit documents state architectural ownership
   rules in human-readable form.

The strongest current ownership statements are:

- `Runtime` is canonical and delegates behavior to owner services.
- `RuntimeLoop` must not exist in active runtime paths.
- `request_tool` records and resolves a capability gap; it does not execute.
- `call_tool` is the only `Runtime` path to `ToolExecutor`.
- `ToolExecutor` owns registered-operation execution.
- `ToolExecutionPolicyService` evaluates execution policy and does not execute.
- `CapabilityCatalog` is read-only capability/provider metadata and does not
  execute.
- `EventLedger` owns append-only events.
- `StateProjector` owns event-to-state projection.
- `ProjectionStore` owns cached projected-state snapshots.

### Rule inventory

`docs/rule_inventory.md` and `seed_runtime/rule_inventory.py` provide a
read-only inventory of deterministic rule-like metadata. Current rule inventory
coverage includes:

- predicate catalog entries;
- predicate mapping entries;
- relationship catalog entries;
- entity type catalog entries;
- inference catalog entries;
- graph validation rules;
- capability resolution rules.

This matters for self-observation because repository-derived architecture facts
would need deterministic predicate, entity type, relationship, and validation
metadata before they could be projected safely into state.

### Invariants

`docs/invariants.md` is the clearest compact specification of accepted
architecture behavior. The invariant set is already suitable as a source of
expected repository facts, for example:

- expected absence: `RuntimeLoop` must not exist in active runtime paths;
- expected route: `Runtime.call_tool` reaches `ToolExecutor`;
- prohibited route: `Runtime.request_tool` must not execute through
  `ToolExecutor`;
- owner assertion: `ToolExecutor` owns registered-operation execution;
- cache boundary: `ProjectionStore` must not append events.

Today these invariants are documented and partly tested, but not represented as
Seed observations or facts.

### Documentation inventory

Seed has a strong documentation inventory by topic, but not a generated or
canonical documentation index. Existing documentation clusters include:

- architecture and principles: `docs/architecture.md`,
  `docs/architecture_principles.md`,
  `docs/architecture_visualization_phase1.md`;
- invariant and ownership audits: `docs/invariants.md`,
  `docs/tool_execution_ownership_audit.md`,
  `docs/runtime_runtime_loop_responsibility_audit.md`;
- deterministic reasoning and rules: `docs/rule_inventory.md`,
  `docs/logic_model.md`, `docs/reasoning_roadmap.md`;
- capability and runtime inventories: `docs/capability_verification_audit.md`,
  `docs/runtime_parity_inventory.md`, `docs/capability_ownership_matrix.md`;
- temporal and contradiction audits: `docs/temporal_reasoning_audit.md`,
  `docs/contradiction_handling_audit.md`.

A repository observation source could eventually turn this documentation index
into evidence-backed facts such as "document X states invariant Y" or
"document X audits component Y", but that inventory is not currently generated.

## 2. Observation model fit

Repository information naturally maps to Seed's existing observation model if it
is treated as an external source payload, not as live runtime behavior.

### Mapping repository data to existing concepts

| Repository concept | Existing Seed concept fit | Example |
| --- | --- | --- |
| Static scan result | `Observation` | observed source file contains `Runtime.__seed_arch__` |
| Raw graph node/edge payload | `Evidence` | JSON node for `ToolExecutor` with file and line |
| Stable derived claim | `Fact` | `ToolExecutor owner registered_tool_execution` |
| Architecture edge | projected relationship | `Runtime routes_to ToolExecutor` |
| Component class or catalog entry | entity | `Runtime`, `ToolExecutor`, `ProjectionStore` |
| Repository component category | `EntityType` | `runtime_component`, `service`, `catalog`, `tool` |
| Documentation invariant | `Fact` or expected-fact rule | `RuntimeLoop absent` |

### Example fits

- `Runtime routes_to ToolExecutor`
  - entity: `Runtime`
  - predicate or relationship: `routes_to`
  - object: `ToolExecutor`
  - evidence: generated architecture edge with path `call_tool only`
  - source type: likely a future `repository` source type, or an interim
    `imported` source type if no new source type is added.

- `ToolExecutor owns execution`
  - entity: `ToolExecutor`
  - predicate: `architecture_owner`
  - value: `registered_tool_execution`
  - relationship variant: `owns_behavior` -> `registered_operation_execution`
  - evidence: `__seed_arch__` metadata plus invariant documentation.

- `ProjectionStore owns cache`
  - entity: `ProjectionStore`
  - predicate: `architecture_owner`
  - value: `projection_cache`
  - relationship variant: `owns_behavior` -> `projection_cache`.

- `RuntimeLoop absent`
  - entity: `RuntimeLoop`
  - predicate: `repository_presence`
  - value: `absent`
  - evidence: generated graph node set and invariant test asserting absence.

### Fit cautions

The model fit is natural, but the existing runtime source vocabulary does not
currently include `repository` as an observation or fact source type. Seed would
also need explicit architecture predicates and relationship definitions before
repository facts could be validated by the existing projection machinery.

## 3. Entity modeling

If the repository became an observation source, the likely entity model would
include both code entities and architecture-domain entities.

### Candidate entities

| Entity kind | Examples | Notes |
| --- | --- | --- |
| repository | `seed` | Root observed source. |
| file | `seed_runtime/runtime.py`, `docs/invariants.md` | Useful for provenance and drift reports. |
| module | `seed_runtime.runtime`, `seed_runtime.execution` | Derived from Python paths. |
| class | `Runtime`, `ToolExecutor`, `StateProjector` | Already extracted by the generator. |
| service | `ToolNeedService`, `ToolExecutionPolicyService` | Architecture role over classes. |
| runtime component | `Runtime`, `EventLedger`, `ProjectionStore` | Higher-level component identity. |
| catalog | `CapabilityCatalog`, `PredicateCatalog`, `RelationshipCatalog` | Read-only metadata owners. |
| generated artifact | `architecture_graph.json`, `runtime_ownership.mmd` | Useful for generation freshness. |
| invariant | `runtime_loop_absent`, `call_tool_only_path` | Expected architecture truths. |
| rule inventory entry | `capability_resolution.registered_operation_candidates` | Deterministic rule metadata. |
| capability | `weather_lookup`, `ssh_access` | Already cataloged as capability metadata. |
| tool or operation | `echo`, generated toolkit operations | Existing registry/toolkit concepts. |
| architecture owner | `registered_tool_execution`, `projection_cache` | Could be entities or controlled values. |

### Candidate relationships

| Relationship | Example | Source today |
| --- | --- | --- |
| `contains` | repository contains file | repository inventory, not implemented |
| `defines` | file defines class | AST scan, partially available |
| `has_owner` | `ToolExecutor` has owner `registered_tool_execution` | `__seed_arch__` |
| `in_layer` | `Runtime` in layer `runtime` | `__seed_arch__` |
| `routes_to` | `Runtime` routes to `ToolExecutor` | generated graph routes/edges |
| `route_limited_to` | `Runtime` routes to `ToolExecutor` only on `call_tool` | generated graph edge path |
| `records_event` | `ToolExecutor` records tool-call events | generated graph edge |
| `reads_from` | `StateProjector` reads `EventLedger` | generated graph edge |
| `writes_to` | `ToolNeedService` records in `EventLedger` | generated graph edge |
| `projects_to` | `StateProjector` produces `State` | generated graph edge |
| `validates_with` | `StateProjector` validates with `GraphValidator` | generated graph edge |
| `requires` | `ToolExecutor` requires `ToolRegistry` | generated graph edge |
| `may_execute` | `ToolExecutor` may execute `RegisteredOperation` | generated graph edge |
| `may_suggest` | `CapabilityCatalog` may suggest provider/handoff metadata | generated graph edge |
| `documents` | `docs/invariants.md` documents runtime invariants | documentation inventory, not implemented |
| `expects_absence` | invariant expects `RuntimeLoop` absent | documentation/test, not implemented as fact |
| `supersedes` / `quarantines` | legacy planning artifacts are historical | docs only |

### Entity type gaps

The checked-in `entity_type_catalog/core.json` currently models operational
entities such as host, service, group, endpoint, monitoring system, capability,
and unknown. It does not contain repository-specific entity types such as
`module`, `class`, `runtime_component`, `catalog`, `invariant`, or `generated_artifact`.

Similarly, the checked-in `relationship_catalog/core.json` currently contains
operational relationships such as `member_of`, `alias_of`, `monitored_by`,
`provides`, and `runs_on`. It does not contain architecture relationships such
as `routes_to`, `owns_behavior`, `defines`, `documents`, or `expects_absence`.

## 4. Explainability

Seed's existing reasoning structures are a good conceptual fit for explaining
repository-derived architecture facts, but they cannot answer these architecture
questions as first-class projected state until repository observations and
architecture predicates/relationships exist.

### Current explainability structures

Existing structures that would help explain repository facts:

- `ObservationIngestor` preserves observation -> evidence -> fact provenance.
- `Evidence` stores source payload, source name, observed time, and confidence.
- `Fact` stores subject, predicate, value, evidence ids, source type, confidence,
  dimensions, and derivation links.
- `StateProjector` projects facts and relationships from the ledger into
  inspectable state.
- `GraphValidator` validates projected relationship type expectations.
- `EvidenceGraph` builds support graphs over facts and evidence.
- `ExplanationBuilder` explains current facts, competing beliefs, support, and
  source facts.
- `RuleInventoryBuilder` exposes deterministic rules and rule-like catalog
  entries with source attribution.

### Could Seed answer "Why does Runtime own execution?"

Not exactly, because the current invariant says the opposite: `Runtime` does not
own execution. The repository knowledge currently says:

- `Runtime` owns orchestration and routing.
- `ToolExecutor` owns registered-operation execution.
- `Runtime.call_tool` is the only runtime branch that routes to `ToolExecutor`.
- `Runtime.request_tool` records and resolves a capability gap and must not
  execute.

With repository facts, Seed could answer a corrected question such as:

> Why does `ToolExecutor` own execution, and what does `Runtime` own?

The explanation could cite the `ToolExecutor.__seed_arch__` owner metadata, the
`Runtime -> ToolExecutor` generated edge for `call_tool`, and the invariant that
`call_tool` is the only `Runtime` path to `ToolExecutor`.

### Could Seed show execution owners?

Partially today. The generated graph can show owner labels for nodes, and the
invariant documentation identifies execution ownership. A first-class Seed answer
would require repository-derived facts such as:

- `ToolExecutor has_owner registered_tool_execution`
- `ToolExecutionPolicyService has_owner execution_policy_evaluation`
- `CapabilityCatalog has_owner capability_metadata`
- `RegisteredOperation has_owner registered_tool_implementation`

Only some of these exist in generated graph JSON today.

### Could Seed show unreachable components?

Partially. The generated graph can be analyzed to find nodes with no incoming or
outgoing edges, referenced-only nodes, or source files not included in the graph.
However, no committed artifact currently classifies components as reachable,
unreachable, active, inactive, legacy, or quarantined. Such classification would
be a repository-analysis layer, not runtime behavior.

### Could Seed show experimental components?

Mostly missing. Some documents classify historical or quarantined artifacts, but
there is no canonical `experimental` flag in `__seed_arch__`, generated graph
nodes, catalogs, or documentation inventory. Seed would need a documented
repository metadata convention before it could reliably answer this.

### Using existing reasoning structures

If repository observations were ingested as facts, existing explanation
machinery could plausibly answer:

- "Why is `ToolExecutor` the execution owner?"
- "Which facts support the `Runtime -> ToolExecutor` route?"
- "Which generated edge supports this relationship?"
- "Which invariant expects `RuntimeLoop` to be absent?"
- "Which components are owned by `capability_metadata`?"

However, the current system does not yet have repository source types,
architecture predicates, architecture relationship definitions, or repository
normalizers. Therefore this is an architectural fit, not an implemented
capability.

## 5. Missing concepts classification

| Concept | Classification | Current basis | Gap |
| --- | --- | --- | --- |
| Repository observation | Missing | Architecture generator statically scans files and emits artifacts | No `ObservationSource` or ingestor converts repository scans into observations. |
| Repository facts | Missing | Generated graph has fact-like nodes and edges | No canonical predicates or facts such as `has_owner`, `routes_to`, or `repository_presence`. |
| Repository relationships | Missing | Generated graph has labeled edges | No relationship catalog entries for architecture relationships and no projection into `EntityRelationship`. |
| Architecture drift detection | Partially implemented | Tests regenerate architecture artifacts and assert stability | No semantic drift report comparing expected architecture facts to observed repository facts. |
| Ownership reasoning | Partially implemented | `__seed_arch__`, generated graph, invariants, and rule inventory document owners | Ownership is not normalized into queryable facts or explanation responses. |
| Self-audit | Partially implemented | Multiple audit docs, invariant tests, rule inventory, generated graph | Audits are manual documentation plus tests, not a unified self-observation capability. |
| Documentation inventory | Partially implemented | Many docs exist by topic and are listed in this audit | No generated documentation index or doc-to-topic/doc-to-invariant fact projection. |
| Repository entity types | Missing | Operational entity catalog exists | No `module`, `class`, `runtime_component`, `catalog`, or `invariant` entity types. |
| Repository predicates | Missing | Operational predicate catalog exists | No architecture predicate vocabulary such as `architecture_owner` or `repository_presence`. |
| Repository source confidence policy | Missing | Existing source types have confidence defaults | No confidence/default provenance semantics for repository scans. |
| Generated graph provenance | Partially implemented | Nodes carry file and line; generator records source file set | No evidence ids, observation ids, or ledger events. |
| Unreachable component detection | Missing | Graph data could support it | No documented reachability semantics or generated report. |
| Experimental component classification | Missing | Some docs describe historical/quarantined artifacts | No canonical metadata flag or classification catalog. |

## 6. Safety boundaries and explicit non-goals

A repository self-observation capability should remain observational and
explanatory unless a separate, explicitly approved design changes that boundary.

Explicit non-goals:

- Do not implement code modification.
- Do not implement autonomous refactoring.
- Do not implement self-rewriting.
- Do not implement runtime mutation.
- Do not make repository observations trigger execution.
- Do not make architecture drift detection edit code.
- Do not make generated graph discrepancies auto-fix source metadata.
- Do not add agentic self-improvement behavior.
- Do not mutate `Runtime` or add new runtime routing behavior.
- Do not ingest repository contents into state without explicit source,
  predicate, relationship, and safety design.

Safe boundaries for future work:

- Static reads only.
- Deterministic generation only.
- Source-attributed evidence only.
- Human-reviewed documentation and inventories.
- CI checks that report drift without modifying source code.
- Optional design documents before any implementation.

## Smallest safe next step

The smallest safe next step is an **observation-source design document** for
repository architecture facts. It should not ingest the repository and should not
change runtime behavior.

Recommended contents:

1. Define a repository observation source contract for generated architecture
   artifacts.
2. Propose a minimal architecture predicate vocabulary, for example
   `architecture_owner`, `architecture_layer`, `repository_presence`, and
   `architecture_route`.
3. Propose minimal architecture entity types, for example `module`, `class`,
   `runtime_component`, `catalog`, `generated_artifact`, and `invariant`.
4. Propose minimal relationship catalog additions, for example `defines`,
   `has_owner`, `routes_to`, `requires`, `records_event`, and `documents`.
5. Define provenance rules mapping generated graph nodes/edges to evidence
   payloads.
6. Define read-only drift reports comparing observed repository facts with
   expected invariants.
7. Re-state non-goals: no code modification, no autonomous refactoring, no
   self-rewriting, and no runtime mutation.

This keeps the next step in documentation and inventory/design territory while
preserving a clear path to future repository observation if it is explicitly
approved later.

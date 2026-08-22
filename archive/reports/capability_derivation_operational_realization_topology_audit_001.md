# Capability Derivation and Operational Realization Topology Audit 001

## 1. Bounded question

Can Seed support a capability as an evidence-backed projection derived from more primitive capabilities, while keeping its operational realization replaceable?

## 2. Governing orientation

The operator testimony was treated as testimony, not fact: tools, capabilities, operational realizations, observation translators, and projections may be distinct; Seed may begin from minimal warranted contact with reality; external grammars may be translated into Seed observations; specialization should be warranted by measured pressure. This audit did not promote Shell, JSON, Prometheus, Git, or an exoskeleton into repository fact without implementation evidence.

## 3. Methodology

I ran the requested read-only `rg` probes, then inspected implementation bodies and callers for capability inventory, candidates, verification, promotion readiness, needs, catalog, registry, execution, observation sources, repository observation, structure observation, events, projection/cache, tests, and relevant docs. Classification below is based on inspected code, not search matches alone.

## 4. Inspected neighborhoods

Primary inspected files: `seed_runtime/capability_inventory.py`, `seed_runtime/capability_candidates.py`, `seed_runtime/capability_verification.py`, `seed_runtime/capability_promotion_readiness.py`, `seed_runtime/verification_evidence.py`, `seed_runtime/tool_needs.py`, `seed_runtime/capability_catalog.py`, `seed_runtime/registry.py`, `seed_runtime/execution.py`, `seed_runtime/tool_validation.py`, `seed_runtime/tool_execution_policy.py`, `seed_runtime/observation_sources.py`, `seed_runtime/repository_observation.py`, `seed_runtime/knowledge/repository_observation.py`, `seed_runtime/structure_observation.py`, `seed_runtime/events.py`, `seed_runtime/projection_store.py`, `scripts/seed_local.py`, and capability/observation/execution tests.

## 5. Terminology

* **Capability**: implementation-backed bounded ability claim represented by names, needs, candidates, or `capability_verified` facts depending on surface.
* **Tool**: registered executable operation contract (`ToolSpec`) managed by `ToolRegistry` and executed only by `ToolExecutor`.
* **Realization**: concrete callable/provider/observer path used to perform work; current code usually stores this as `ToolSpec.implementation`, provider recommendation metadata, or observer class behavior rather than as a separate capability-realization object.
* **Observation translator**: code that maps external/provider or source grammar into `Observation` or repository artifact facts.
* **Projection**: read-only view over projected State, catalog, registry, or observed evidence.

## 6. Capability responsibility inventory

| Artifact/service | Responsibility | Refused responsibility | Candidate | Verify | Project | Select realization | Execute | Translate grammar | Observations | Evidence | Authority | Success/failure | Freshness | Scope | Constraints/cost | LLM-free |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `CapabilityCatalog` | Load known capability metadata and provider/handoff suggestions. | Does not execute tools. | Partial metadata | No | Yes metadata | Recommends providers only | No | No | No | Catalog provenance only | No | No | No | Limited via capability name | No | Yes |
| `ToolNeedService` | Create capability gaps and resolve needs to catalog/registry metadata. | Does not execute, authorize, create pending actions, or mutate catalog/registry. | Yes, need/gap | No | Yes | Lists registry/provider candidates | No | No | No | Requested-by event | No | Need status | No | Desired inputs/outputs | No | Yes |
| `ToolRegistry` | Load/manages registered operations and capability labels. | Does not prove capability availability. | Registered operation candidates | No | Yes operation inventory | No | No | Manifest JSON | No | Manifest only | No | Status field | No | Capability slug | No | Yes |
| `ToolExecutor` | Validate, authorize via policy, invoke registered callable, record results. | Does not do provider recommendation or capability verification. | No | No direct | No | Uses selected tool name | Yes | Implementation-specific | Via fact extraction after result | Execution events | Policy-gated only | Records completed/failed/blocked | No | Scope arg | No timing/memory | Yes |
| `CapabilityCandidates` | Preserve package-derived capability candidates. | Candidate is not proof, authority, selection, or execution. | Yes | No | Yes | No | No | No | No | Fact/evidence summaries | No | No | No | Filter only | No | Yes |
| `VerificationEvidence` | Observe binary paths for candidates without invoking binaries. | Not verification, permission, selection, or execution. | No | Evidence only | Yes | No | No | Filesystem/PATH metadata | No | Binary path evidence | No | No | No | PATH only | No | Yes |
| `CapabilityInventory` | Project verification state from `capability_verified` facts plus ToolSpecs/ToolNeeds universe. | Does not admit capabilities, verify existence, select, authorize, or execute. | No | Reads verification facts | Yes | No | No | No | No | Compact support summaries | No | State includes stale/unverified | Yes via fact expiry | Capability subject | No | Yes |
| `CapabilityVerification` | Join candidates, acquired evidence, and inventory status. | Does not promote, select, authorize, or execute. | No | Inspection only | Yes | No | No | No | No | Candidate + verification evidence | No | Status only | Via inventory | Candidate filter | No | Yes |
| `CapabilityPromotionReadiness` | Explain whether future promotion would be supportable. | Does not create `capability_verified` facts or execute. | No | Readiness only | Yes | No | No | No | No | Support joins | No | Missing/supportable statuses | Partial | Candidate filter | No | Yes |
| `PrometheusObservationSource` | HTTP acquire, JSON decode, validate Prometheus vector grammar, translate to `Observation`. | Does not expose independent JSON or Prometheus capability. | No | Operational success only | Counters/errors only | No | HTTP GET | Yes | Yes | Observation metadata | No | `last_error`, empty list | Sample times | Base URL/queries | Fetch seconds/counters only | Yes |
| `RepositoryArtifactObservationAdapter` | Parse caller-supplied Python text to artifact facts. | Does not read files, scan repos, import modules, infer ownership, or execute. | No | No | Facts | No | No | Python AST | Repository artifact facts | Preserves source path/symbol | No | Syntax failure degrades | No | Source path/text | No | Yes |
| `GitRepositoryObservationProvider` | Use `git` subprocess to observe repository state. | Does not create a Git capability. | No | Operational availability only | Observation object | No | Subprocess Git | Git output parsing | Repository observation | Reason/status fields | No | Unavailable reasons | No | Repository path | No | Yes |
| `StructureObservationBoundary` | Shared boundary for structural extraction. | Owns no substrate parsing, grammar, responsibility, lexicon, or mutation. | No | No | Boundary | No | No | No | No | Boundary only | No | No | No | No | No | Yes |

## 7. Producer/artifact/consumer table

| Producer | Artifact | Consumer | Trigger | Owned responsibility |
|---|---|---|---|---|
| Model/runtime decision | `tool_need.created` event / `ToolNeed` | State projector, ToolNeedService resolution, CLI capability needs | `request_tool` decision | Preserve missing capability pressure. |
| `CapabilityCatalog.load` | `CapabilityCatalogEntry` / recommendations | ToolNeedService, recommendation views | CLI/runtime startup or explicit load | Capability metadata/provider suggestion. |
| `ToolRegistry.load_manifest` | `ToolSpec` registered operations | ToolNeedService, ToolExecutor, inventory | Manifest load | Operation contract inventory. |
| `ToolExecutor` | `tool.call.*` events | StateProjector, FactExtractionService | `call_tool`/approved pending action | Registered operation execution. |
| Fact extraction/projector | Facts, evidence, FactSupport | Capability inventory and evidence graph | Projection replay | Knowledge from events. |
| `CapabilityCandidates` | Candidate inspection | Verification and promotion inspections | CLI read-only surface | Package-observed candidate visibility. |
| `VerificationEvidence` | Binary-path evidence inspection | Capability verification/promotion readiness | CLI read-only surface | Local non-executing evidence acquisition. |
| `CapabilityInventory` | Verification entries | CLI/status, verification inspection | CLI read-only surface | Verification-state projection. |
| Prometheus source | `Observation` list | Ingestion/state projection | `--observe-prometheus` or caller | Provider acquisition + translation. |
| Repository observers | Repository observation/artifact facts | Diagnostics/snapshot/history/source views | CLI/caller | Repository state or source artifact observation. |

## 8. Capability-recognition topology

Current topology is a union of distinct signals:

```text
configured: CapabilityCatalog YAML -> known capability metadata/provider recommendation
registered: ToolSpec.capabilities -> operation-contract capability labels
requested: ToolNeed.capability -> capability pressure
observed/discovered: package_installed facts -> capability candidates
reachable: binary path observed in PATH -> verification evidence only
verified/successful/fresh: capability_verified FactSupport -> inventory state/age/stale
authorized: ToolExecutionPolicy outcome -> operation execution authorization, not capability proof
sufficient: not implemented as capability sufficiency
```

Installed package and binary presence are deliberately not capability proof. Registered operations widen the inventory universe but are not admitted capability knowledge. Verification is only projected from `capability_verified` facts.

## 9. Capability candidate topology

Candidates originate from `package_installed` facts mapped through a static table to `ssh_client`, `python_runtime`, `docker_client`, `git_client`, and `http_client`. Candidate creation is evidence-backed by projected package facts, but candidate status explicitly refuses capability proof, authority, policy evaluation, selection, and execution.

## 10. Capability verification topology

Verification surfaces currently prove different things:

* Package candidates prove package observations only.
* Verification evidence proves binary path reachability through filesystem metadata only; binaries are not invoked.
* Capability inventory verifies only if projected `capability_verified` facts exist and are current.
* Tool execution success proves a registered operation completed and may yield facts, but no inspected code automatically promotes successful execution to capability verification.
* Prometheus collection validates HTTP response shape, JSON object, success status, vector result type, and sample decoding for that run, but does not emit an independent capability verification fact.

Thus verification can establish contract validity and execution success for operations, and output/translation validity inside observers, but bounded usefulness as a capability is not a first-class derived projection.

## 11. Capability projection topology

Current projections:

| Projection | Provenance | Freshness | Scope | Authority | Dependency | Realization | Success/failure | Uncertainty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `--current-capabilities` / CapabilityView | Partial from state | Partial | Capability | No | No | No | Status | Partial |
| `--capability-status` / inventory | Evidence summaries/source types | Yes for facts | Capability subject | No | No | No | Verified/unverified/stale/provider_reported/unknown | Yes |
| `--capability-candidates` | Fact/evidence IDs | No | Candidate/filter | No | No | No | No | Yes boundary notes |
| `--verification-evidence` | Binary path/source | No | PATH/filter | No | No | Binary name only | No | Yes boundary notes |
| `--capability-verification` | Candidate + inventory | Via inventory | Candidate/filter | No | No | No | Status | Yes notes |
| `--capability-promotion-readiness` | Candidate + verification evidence | Partial | Candidate/filter | No | No | No | Supportable/unsupported | Yes notes |
| ToolNeed resolution | Requested-by/catalog/registry | No | Need capability | No | No | Registered/provider candidates | Need status | Partial |

No projection exposes prerequisite capability edges or stable realization identities as separable from provider/tool implementation.

## 12. Capability dependency topology

No inspected production type represents `capability A requires capability B`. Imports, provider metadata, operation registration, observation call chains, and documentation statements exist, but they are not true capability dependencies. `ToolSpec.capabilities` is a list of labels for one operation, not prerequisites. `CapabilityCatalog` recommendations can include provider/backend/operation metadata, not dependency graphs.

## 13. Derived capability topology

No implemented capability is explicitly derived from another capability. Some behavior is composition-like (Prometheus HTTP + JSON + translation; Git subprocess + output parsing; Python AST over caller-supplied text), but the repository represents these as observer/provider implementation internals, not derived capability projections.

## 14. Operational realization topology

Representative realization mapping:

* `python_runtime`, `git_client`, etc. candidates: package table and binary-path evidence; no executable realization selected.
* Registered operation capability: `ToolSpec.implementation` import reference invoked by `ToolExecutor`.
* Prometheus observation: `PrometheusObservationSource` with `urlopen`, `json.loads`, provider-specific validation, and observation-shaping helpers.
* Repository state observation: `GitRepositoryObservationProvider` using `subprocess.run([git,...])` and parsing porcelain output.
* Repository artifact observation: `RepositoryArtifactObservationAdapter` using `ast.parse` on caller-supplied text.

Capability identity is often tied to implementation labels or provider classes because there is no separate capability-realization record.

## 15. Alternative realization topology

Alternatives exist as adjacent mechanisms, not equivalent realizations of one capability:

* Catalog provider recommendations vs registered operations for a `ToolNeed` are separate metadata streams.
* Repository state can be observed by Git subprocess, while repository artifacts are observed from source text; these are differently scoped, not equivalent.
* Prometheus provider observation and local passive observation may emit overlapping predicates (for example filesystem or OS facts), but inventory surfaces treat them as providers/predicates, not alternative realizations of a shared capability.
* Projection cache vs rebuild is an execution/performance path for state projection, not a capability realization selection.

## 16. External grammar translation topology

| External/provider representation | Decoder | Translator | Seed artifact | Compression |
|---|---|---|---|---|
| Prometheus HTTP JSON | `json.loads` + shape checks | `_prometheus_decoded_sample`, `_prometheus_observation_shapes` | `Observation` | Acquisition, JSON decode, provider grammar, identity shaping, and translation are compressed in one observer. |
| Git command output | `subprocess.run` text output | porcelain-line parsing | `RepositoryObservation` | Acquisition and Git grammar parsing compressed in provider. |
| Python source text | `ast.parse` | artifact fact constructors | `RepositoryArtifactFact` | Pure translator over caller-supplied text; source acquisition refused. |
| Local JSON inventory | `json.loads` | source collection/import path | observations | JSON decode is implementation detail, not capability. |
| Strict model JSON | `json.loads` | decision/intent parsers | decisions/classifications | Parser implementation detail, not operational capability. |

## 17. Capability-use topology

There is no full road from `required capability -> projected available capability -> selected realization -> operation`. The implemented roads are narrower:

* `request_tool` creates a `ToolNeed`, then resolves read-only catalog and registered operation candidates.
* `call_tool` executes a named registered tool after registry lookup, schema validation, policy, and approval gates.
* Observer CLIs directly instantiate providers such as Prometheus or repository observers.

Capability verification status is not currently used as a mandatory selector or gate for realization selection.

## 18. Capability failure topology

* Dependency absent: not represented as dependency failure; callers see no candidate, unavailable observation, or validation failure.
* Authority unavailable: operation policy blocks/requires confirmation/approval; capability status does not weaken.
* Execution fails: `tool.call.failed` recorded for registered tools; observers may return empty observations and `last_error`.
* Invalid output: registered output schema failure becomes tool failure; Prometheus invalid shape raises/sets `last_error` and returns empty list.
* Translation fails: repository artifact syntax failure degrades to module fact with parse failure; Prometheus skips invalid samples or fails whole collection depending on level.
* Evidence stale: capability inventory can report `stale` from expired `capability_verified` FactSupport.
* Partial support: mostly represented as unverified/unknown, unavailable reason, or boundary notes rather than partial capability status.

## 19. Capability learning topology

Seed can answer limited questions about how a verified capability was established when a `capability_verified` fact exists: inventory exposes supporting facts, source types, evidence IDs, summaries, confidence, and observation times. It cannot currently answer how many attempts, which dependency chain, which realization, or which validation run taught Seed that a derived capability works.

## 20. Specialization topology

No implementation-backed road exists from repeated capability composition to measured resource pressure to specialized realization. There are timing/counter surfaces for selected diagnostics and Prometheus collection, projection cache behavior, and event batching/storage, but no capability-realization boundary or workload evidence that would justify specialization.

## 21. JSON probe

JSON parsing is explicit as implementation code (`json.loads`, strict parsers, manifest/catalog/event/projection readers), but not represented as a capability. There is no derivation `shell -> decoder reachable -> JSON decoding capability`. Multiple implementations could parse JSON in ordinary Python terms, but the repository lacks a stable JSON capability identity or realization registry. A dedicated JSON parser would currently be a new implementation detail or registered operation unless accompanied by capability projection semantics.

## 22. Prometheus probe

Prometheus observation compresses acquisition, JSON decoding, provider grammar validation, sample decoding, identity shaping, and observation translation. It does not depend on an independently represented HTTP, JSON, or Prometheus grammar capability. Successful bounded observations support facts/observations but do not become a Prometheus capability projection unless another process emits `capability_verified` facts.

## 23. Repository observation probe

Repository artifact observation and repository state observation are distinct:

* Artifact observation is a pure translator over caller-supplied Python source text and explicitly refuses filesystem scanning/import/runtime integration.
* Repository state observation acquires from filesystem/Git, executes Git subprocesses, and parses Git output.

The repository does not represent them as one derived repository capability or as dependencies on independent source-acquisition/Git grammar capabilities.

## 24. Low-resource deployment probe

Current artifacts could support discussion of smaller realizations only indirectly: provider recommendations, registered operations, observer classes, and projection cache behavior exist. They do not represent RAM/storage/CPU/power/network/security constraints or realization burden, so a low-resource deployment does not require a new constitutional architecture in evidence, but it would require a missing selection/measurement projection before implementation-backed realization selection.

## 25. Runtime efficiency evidence

Implemented evidence is partial and scattered:

* Prometheus records `http_api_fetch_seconds`, metric family count, sample count, and observation count for a collection.
* Knowledge reachability/projection surfaces include timing and cache metadata.
* Event ledger/projection store serializes JSON payloads but does not attribute byte cost to capability learning.
* Predicate facts include memory/storage observations for hosts, but not runtime memory of Seed realizations.

CPU time, startup latency, peak/RSS memory, process count, dependency startup cost, network payload size, input/output payload size per realization, and repeated recomposition cost are mostly absent.

## 26. Learning efficiency evidence

Current code can count events, facts, supports, observations, and evidence in a projected state, but it does not attribute these to a bounded capability-learning effort. There is no retained minimal support set, no learning elapsed-time metric, no verification attempt count, no compacted evidence policy for learned capabilities, and no ledger byte accounting per capability. Ledger size is serializable but not semantically attributable as learning cost.

## 27. Deployment efficiency evidence

Deployment constraints are mostly absent. Some observer metadata indicates read-only behavior, shell/subprocess avoidance, base URL, timeout, safe query allowlists, and binary availability; host observations can include memory/storage facts. There is no first-class capability deployment profile for RAM, storage, CPU, power, network, dependency availability, target architecture, target OS, workload frequency, acceptable latency, or attack surface.

## 28. Ultimate payload comparison

Current implementation-backed evidence for total lifetime burden is insufficient:

| Term | Current evidence |
|---|---|
| Learning ledger footprint | Events exist, but not attributed to capability learning. |
| Retained evidence footprint | Fact/evidence IDs exist, no minimal support set or byte footprint. |
| Implementation footprint | File/module references inferable manually, not measured. |
| Dependency footprint | Binary/package/provider hints exist, not complete dependency footprint. |
| Deployment footprint | Mostly absent. |
| Recurring runtime cost | Partial timing/counters for selected diagnostics/providers. |
| Failure/recovery cost | Failure events/reasons exist, not costed. |
| Maintenance/re-verification cost | Staleness exists for facts, no re-verification cost. |

Seed cannot currently answer how much a capability cost to learn, retain, deploy, and repeatedly exercise.

## 29. Projection memory analysis

Representing JSON and Prometheus as derived capability projections would not inherently have to consume more memory than dedicated tools if projections stored compact metadata and references. Current capability inventory uses compact evidence summaries and support IDs rather than copying full evidence bodies. However, projection cost for such derived capabilities is unmeasured. Memory could be dominated by retained evidence, event ledger, loaded dependencies, runtime implementation, model context, or caches rather than projection metadata. Repository evidence supports only that current projections can be compact; it does not prove memory superiority or inferiority.

## 30. Existing owners

Existing owners include capability metadata (`CapabilityCatalog`), capability-gap creation/resolution (`ToolNeedService`), registered operation catalog (`ToolRegistry`), registered operation execution (`ToolExecutor`), validation/policy (`ToolValidationService`, `ToolExecutionPolicyService`), candidate preservation (`CapabilityCandidates`), verification evidence acquisition (`VerificationEvidence`), capability inventory projection (`CapabilityInventory`), observation providers/translators (`PrometheusObservationSource`, local observers), repository artifact translation, repository state observation, structure observation boundary, event history, and projection cache.

## 31. Missing owners

Missing owners: capability dependency projection, derived capability projection, realization identity/selection, realization equivalence, capability sufficiency for bounded need, lawful stopping after sufficient competency, capability-learning attempt ledger, minimal support-set retention, capability-specific efficiency attribution, deployment constraint profile, and total lifetime burden comparison.

## 32. Existing roads

Existing roads: need creation, read-only capability resolution to catalog/registry metadata, registered operation validation/policy/execution, tool result fact extraction, package-to-candidate preservation, binary-path evidence acquisition, candidate-to-verification inspection, capability inventory from `capability_verified` facts, observer-specific acquisition/translation, fact freshness via expiry, projection cache reuse.

## 33. Missing roads

Missing roads: evidence need to required capability, required capability to dependency chain, dependency chain to available bases, candidate realization validation, successful validation to `capability_verified` promotion, verified capability to selected realization, capability sufficiency to lawful stop, capability failure to weakened status by authority/scope, repeated recomposition to specialization decision.

## 34. Existing projections

Existing projections include capability status/inventory, candidates, verification evidence, verification inspection, promotion readiness, capability needs, capability relationship/privilege views, tool resolution payloads, observation inventory/utilization/domains/permission, operational graph, projection shape/stage views, event/state projections, and projection cache summaries.

## 35. Missing projections

Missing projections: prerequisite graph, realization graph, translator inventory as capability support, capability-to-observer mapping, capability freshness by scope/target/authority, support-set minimization, realization efficiency comparison, deployment-specific realization selection, learning-cost attribution, and total lifetime burden.

## 36. Strongest counterevidence

* Capability inventory intentionally separates admitted `capability_verified` facts from executable operation contract metadata; this contradicts any claim that registered tools are sufficient capability proof.
* Candidate and verification evidence modules repeatedly refuse promotion, authority, selection, and execution; installed packages/binaries are not capabilities.
* `ToolExecutor` is intentionally limited to registered operation execution; a general Shell primitive is not present and many local observers explicitly avoid shell/subprocess use.
* Prometheus and repository observers own concrete acquisition/translation responsibilities today, so deriving them might duplicate existing observer-specific contracts unless a projection owner is carefully bounded.
* Docs and code already distinguish capability, provider, adapter, execution path, and execution at story level; a new derivation model must not erase those boundaries.
* Ledger/event payloads are not attributed enough to measure bounded learning footprint safely.

## 37. Preserved Unknowns

* Whether any deployment outside this repository already treats capabilities as derived projections.
* Whether future capability promotion is intended to be manual, policy-driven, or automatic.
* Whether Shell can be made a safe general realization in Seed; current evidence is mixed because many observers forbid shell/subprocess.
* Whether JSON should be a capability or remain parser infrastructure.
* Whether Prometheus acquisition should be decomposed without harming provenance and deterministic observer contracts.
* Whether projection memory would matter relative to ledger/model/cache memory.

## 38. Supported conclusions

1. Seed has first-class capability names, needs, candidates, verification evidence, verification inventory, provider recommendations, registered operation labels, execution policy, and observation translators.
2. Capability derivation and capability dependencies are not implemented as first-class roads.
3. Current capabilities/operations are partially separable at metadata boundaries, but realization identity is not first-class.
4. JSON is an implementation detail; Prometheus is a provider observer, not a derived capability from JSON/HTTP capabilities.
5. Runtime efficiency is partially measurable in isolated surfaces; learning and lifetime burden are not attributable.

## 39. Unsupported conclusions

Unsupported: Seed already implements derived capability graphs; Shell is a primitive capability; JSON decoding is a capability; Prometheus observation depends on independent JSON capability; successful execution automatically verifies capability; failed execution weakens capability status; low-resource specialization can be selected from current evidence; projection memory costs are known; total lifetime burden can be compared.

## 40. Primary classification

B. Seed has capability and realization substrate, but derivation and dependency roads are disconnected.

## 41. Secondary efficiency classification

2. Runtime efficiency is partially measurable, but learning and lifetime burden are not.

## 42. Exact next bounded question

What existing read-only projection fields are sufficient to show, for one capability name, the distinction among requested capability, registered operation label, provider recommendation, candidate evidence, verification evidence, and verified `capability_verified` support without adding dependency or realization selection behavior?

## 43. Implementation-warrant decision

No implementation warranted.

## 44. Files changed

Only `capability_derivation_operational_realization_topology_audit_001.md` was added. No source files, tests, diagnostic registries, or existing docs were modified.

## 45. Probes/tests executed

Read-only probes executed:

```bash
rg -n "Capability|capability|ToolSpec|ToolNeed|OperationSelection|verification|promotion|readiness" seed_runtime scripts tests
rg -n "Prometheus|JSON|json.loads|jq|shell|subprocess|RepositoryObservation|StructureObservation" seed_runtime scripts tests
rg -n "timing|duration|elapsed|memory|rss|payload|serialized|bytes|cache|ledger" seed_runtime scripts tests
rg -n "dependency|requires|prerequisite|derived capability|realization|provider|adapter|translator" . -g '*.py' -g '*.md'
```

Focused inspections used `sed` on the files listed in section 4. No tests were run because the task was review-only and changed one Markdown audit artifact.

## 46. Confidence statement

Confidence is high for the classification that capability derivation/dependency roads are disconnected: the inspected capability modules explicitly preserve candidates, evidence, and inventory without promotion, selection, authority, or execution, while observer implementations compress acquisition/translation without exposing independent derived capability dependencies. Confidence is medium for efficiency classification because timing/counter surfaces are broad and scattered; the absence of attributable learning/lifetime burden was clear in inspected capability paths, but a complete performance-surface audit would require a separate bounded review.

## Required questions answered

1. Smallest implementation-backed capability unit: currently a normalized capability slug appearing in `ToolNeed`, `ToolSpec.capabilities`, candidate maps, catalog entries, or `capability_verified` fact subjects; only `capability_verified` support makes it verified.
2. Tool vs capability: yes, partially; ToolSpec/ToolRegistry are distinct from capability inventory/candidates/needs.
3. Capability vs registered operation: yes; registry labels are operation-contract metadata, not proof.
4. Capability vs realization: partially; ToolSpec implementation exists, but no first-class realization object.
5. Realization vs translator: partially in docs/code boundaries, not generally in capability projection.
6. Capability dependencies: no first-class representation.
7. Explicitly derived capabilities: no.
8. Derived capabilities: story-level/compressed implementation only, not implementation-backed projection.
9. Multiple realizations for same capability: recommendations/candidates can be multiple, but equivalence is not represented.
10. Realization change without capability identity change: possible manually for ToolSpec/catalog metadata, not governed as capability semantics.
11. Shell: represented as an interactive CLI function and a user shell fact/metadata in places, not as a capability/tool/provider primitive.
12. JSON parsing: explicit code, not capability.
13. JSON inside observers: yes, including Prometheus and inventory/import/projection paths.
14. Prometheus depends on independent JSON capability: no.
15. Repository artifact depends on independent source acquisition capability: no; it requires caller-supplied text.
16. Observers compressing acquisition/translation: Prometheus, Git repository state, local host/package/storage/listener observers in `observation_sources.py`.
17. Pure translators over caller input: repository artifact observation; some normalizers and relationship/grammar observation helpers.
18. Structure Observation: owns shared boundary/constraints, not substrate parsing or grammar.
19. Verification evidence: `capability_verified` facts for verification; packages/binaries as candidate/support evidence; operation success as execution evidence only.
20. Successful executions capability evidence: not automatically.
21. Failed executions capability evidence: not automatically, though failure events are evidence of attempted operation failure.
22. Staleness can weaken status: yes for expired verification facts.
23. Authority unavailable weakens status: no; policy affects execution, not capability status.
24. Status varies by scope/target: not first-class beyond subjects/needs/tool scope args.
25. Capability freshness: implemented only through fact expiry/age in inventory.
26. Sufficiency for current job: not implemented.
27. Lawful stopping after sufficient competency: not implemented as capability logic.
28. Evidence need to required capability: partial via diagnostics/tool needs, not general.
29. Required capability to realization selection: no complete road.
30. Realization selection based on evidence/config: current selection is mostly explicit tool name, registry/config, or direct observer construction; recommendations are metadata.
31. Runtime cost measured: partially.
32. Memory cost measured: no for realizations.
33. Serialized payload size measured: serialized payloads exist; sizes not generally measured/attributed.
34. Ledger growth for bounded learning: no.
35. Elapsed capability-learning time: no.
36. Minimal support set: no.
37. Total lifetime burden comparison: no.
38. Dedicated JSON parser: currently a new realization/implementation detail; it would become a new capability only if projected/verified as such.
39. Low-resource deployment new constitutional architecture: no evidence that it requires one; missing projection/measurement owners would be needed.
40. Exoskeleton metaphor: best mapped to deployment-specific realization selection, but not implemented.
41. Existing owners: listed in section 30.
42. Missing roads: listed in section 33.
43. Missing projections: listed in section 35.
44. Missing measurement evidence: memory, CPU, payload bytes, learning attribution, minimal support, lifetime burden.
45. Smallest next bounded slice: the exact bounded question in section 42; no implementation now.

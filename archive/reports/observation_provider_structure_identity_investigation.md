# Observation Provider Structure Identity Investigation

## Scope

This is a bounded implementation investigation of whether current observation providers only acquire observations or also interpret observed structures into service, endpoint, provider, or capability-like identities. It does not recover ownership, redesign observation, add probes, or introduce implementation changes.

## Implementation evidence reviewed

- `seed_runtime/observation_sources.py`
  - `ObservationSource` protocol and `ObservationCollectionService`.
  - `RepositorySourceObservationSource`.
  - `LocalHostObservationSource` and its local package, listener, and systemd paths.
  - `PrometheusObservationSource`.
- `seed_runtime/observations.py`
  - `Observation` model.
  - `ObservationIngestor` observation-to-evidence/fact conversion.
  - Prometheus-specific fact-promotion suppression.
- `seed_runtime/observation_normalizers.py`
  - observation normalization pipeline.
  - endpoint alias and endpoint identity normalizers.
- `seed_runtime/local_packages.py`
  - dpkg parsing and package observation emission.
- `seed_runtime/knowledge/relationship_observation.py`
  - relationship extraction helpers consumed by repository source observation.
- `seed_runtime/capability_candidates.py`
  - read-only capability candidate derivation from package facts.
- `seed_runtime/capability_inventory.py`
  - read-only capability inventory from `capability_verified` facts, ToolSpecs, and ToolNeeds.

## Current provider responsibilities

### Generic provider contract

The explicit provider contract is narrow but not raw. `ObservationSource` says adapters for external systems emit `Observation` objects, expose stable source identity/provenance type, and remain unaware of the event ledger, state projector, and fact ingestion internals. Its only method is `collect() -> list[Observation]`. This means current providers are not raw byte or raw payload producers; they are already expected to return Seed-shaped observations with `subject`, `predicate`, and `value`.

`ObservationCollectionService` makes three downstream stages explicit after `source.collect()`: source collection, normalization, and ingestion. It calls `source.collect()`, then local source-name normalization and the configured `ObservationNormalizationPipeline`, then `ObservationIngestor.ingest_many(...)`. Diagnostics separately count source collection seconds, normalization seconds, event generation/ledger write seconds, events, and facts promoted.

### Repository source observation provider

`RepositorySourceObservationSource.collect()` scans allowed Python files, reads text, calls relationship extraction helpers, and immediately converts returned relationship records into `Observation` objects. This provider therefore owns file acquisition plus invoking structural extraction, but the AST relationship extraction itself lives in `seed_runtime.knowledge.relationship_observation` rather than in the provider class.

The relationship module describes `RelationshipFact` as the language-neutral relationship evidence record and says Python import extraction is the first adapter that emits it. It also states import relationships are dependency/name-availability evidence only, and definition relationships are syntactic declaration evidence only, not behavior, calls, routes, boundaries, ownership, capability authority, or runtime ownership.

**Conclusion:** repository source observation partially separates structural interpretation from source collection by delegating relationship extraction to helpers, but the provider still orchestrates file discovery, file reading, relationship extraction, and conversion into facts-shaped observations inside one collection boundary.

### Prometheus observation provider

`PrometheusObservationSource` performs HTTP GETs against an allowlist of safe metric names (`up`, `node_uname_info`, `node_filesystem_avail_bytes`, and `node_filesystem_size_bytes`). It validates the Prometheus JSON response shape, iterates vector samples, requires `instance`, parses sample timestamps, and emits `Observation` objects.

Prometheus interpretation is visible inside `_observations_from_query(...)`: `up` produces `endpoint_role` from the `job` label and an `up` observation for the `instance` subject; `node_uname_info` may produce an `os` observation; filesystem metrics produce `filesystem_avail_bytes` and `filesystem_size_bytes`; metadata carries metric labels, sample time, query temporal intent, base URL, source name, and collection authority.

Prometheus also contains identity/fact-promotion boundary logic in the provider path: for `node_uname_info`, only that metric is marked authoritative for stable host identity; other metrics remain endpoint-scoped and do not participate in endpoint alias normalization. If the `node_uname_info` subject is endpoint-shaped, the provider marks the `os` observation with `fact_promotion_suppressed=True` and a Prometheus-specific suppression reason.

Fact promotion itself is downstream in `ObservationIngestor`, but the suppression rule is Prometheus-specific: `_should_suppress_fact_promotion(...)` checks metadata for `source_name == "prometheus"`, `prometheus_metric == "node_uname_info"`, `predicate == "os"`, and `fact_promotion_suppressed is True`.

**Conclusion:** Prometheus owns acquisition and significant structural interpretation. It transforms metric names and labels into Seed predicates, endpoint subjects, metadata, filesystem dimensions, endpoint roles, OS observations, and a provider-specific fact-promotion suppression marker. Actual event/evidence/fact creation remains downstream.

### Local host observation provider

`LocalHostObservationSource.collect()` reads local platform, filesystem, network, mount, storage, listener, local user, package, and systemd information, then emits Seed observations. The implementation states it uses Python stdlib APIs and local read-only files without shells or subprocesses in the local-host path.

Several local-host subpaths show mixed acquisition and interpretation:

- Local identity reads `/etc/hostname`, `/etc/machine-id`, boot ID, and FQDN-like hostname values, then emits identity predicates and metadata explicitly saying DNS validity, DNS resolution, network reachability, availability, provider visibility, host ownership, and host uniqueness are not asserted.
- Local package observation delegates dpkg parsing and generic package observation emission to `seed_runtime.local_packages`, while the local-host provider orchestrates reading the dpkg status file and calling the helper.
- Listener observation parses socket-table structures into address/port/protocol entries and links socket inodes to observable process metadata when procfs evidence exists.
- Systemd observation is a separate source class that invokes `systemctl` through a command runner, records systemd-reported unit identity/runtime state/substate/unit-file state, and explicitly says it does not interpret health, ownership, intent, dependencies, or desired state.

`local_packages.py` shows a narrower separated structural adapter: `parse_dpkg_status(...)` converts dpkg status text to normalized `PackageRecord` instances, and `package_records_to_observations(...)` turns installed package records into generic package observations. Its metadata explicitly sets `service_inferred=False`, `capability_inferred=False`, `process_inferred=False`, `port_inferred=False`, and similar non-inference markers.

**Conclusion:** local-host observation is implementation-compressed at the top-level provider because collection orchestrates many structural interpretations. Some subdomains already have local separation (`local_packages`, `SystemdObservationSource`), and many emitted observations carry explicit negative authority metadata.

### Repository Observation and Repository Source Observation

The repository source provider is source-code relationship-oriented (`repository_source`). The relationship extraction helpers provide the most explicit boundary: they accept caller-provided text and produce bounded `RelationshipFact` records from syntax/front matter, without reading files, inspecting prose beyond supplied metadata, importing modules, using LLMs, building graphs, or integrating with runtime/tool execution.

This is a counterexample to total provider compression: structural interpretation of Python imports/definitions has a helper boundary. However, the provider still combines file scanning, file reading, helper invocation, and conversion of `RelationshipFact` into `Observation` during `collect()`.

### Capability-related observations

Capability-like identities do not appear to be produced directly by the reviewed observation providers as verified capabilities. The package observation path explicitly avoids inferring capability from package presence. Capability candidates are produced later by `build_capability_candidates(...)`, which reads projected `package_installed` facts and maps known package names (`openssh-client`, `python3`, `docker.io`, `git`, `curl`, etc.) into candidate capability names. The module states this is read-only candidate preservation, not capability proof, execution authority, execution decision, policy evaluation, tool invocation, or tool execution.

Capability inventory is also downstream and read-only. It derives a capability universe from admitted `capability_verified` fact subjects, executable operation contract metadata, and requested capabilities. It states verification state is derived from `capability_verified` facts and projected support; missing verification facts produce `unverified`, expired verification facts produce `stale`, and inventory does not execute tools, call providers, append events, schedule work, or route runtime behavior.

**Conclusion:** capability-like identities emerge downstream from projected facts, ToolSpecs, ToolNeeds, and capability verification facts, not from observation providers as verified capability identities. Candidate capability names do emerge from package observations after promotion into facts.

## Explicit implementation boundaries

1. **Provider interface boundary:** `ObservationSource.collect()` returns Seed `Observation` objects, not raw provider payloads.
2. **Collection/normalization/ingestion boundary:** `ObservationCollectionService` explicitly sequences provider collection, normalization, and ingestion.
3. **Observation shape boundary:** `Observation` is canonical and includes source type, observed time, subject, predicate, value, confidence, metadata, dimensions, and expiration.
4. **Evidence/fact promotion boundary:** `ObservationIngestor` creates observation events, evidence events, and optional fact events from observations.
5. **Endpoint normalization boundary:** endpoint alias and endpoint identity normalizers derive additional observations from emitted observations and projected state.
6. **Relationship extraction helper boundary:** Python import/definition interpretation is separated into `relationship_observation` helpers that operate on supplied text and produce bounded relationship records.
7. **Capability candidate boundary:** package facts are interpreted into capability candidates only in `capability_candidates`, and the module explicitly rejects capability proof/authority/execution semantics.
8. **Capability inventory boundary:** `capability_inventory` presents read-only verification status from projected capability-related inputs and verification facts.

## Remaining implementation compressions

### Acquisition and structural interpretation remain compressed in providers

Providers are not raw acquisition surfaces. They usually emit already-structured Seed observations. Prometheus converts metric families/labels into predicates and subjects in the provider. Local-host collection converts platform/proc/sysfs/dpkg/socket/systemd structures into domain predicates and subjects. Repository source observation scans files, parses syntax through helpers, and emits observations in one collection path.

### Structural interpretation and identity recovery are partially separated, but not universally

Endpoint identity recovery is partly separated into normalizers: `EndpointAliasNormalizer` derives hostname-to-endpoint aliases from metadata, and `EndpointIdentityNormalizer` links known base identities to endpoint-shaped subjects using current observations and projected state. However, Prometheus already decides when an `instance` is endpoint-scoped, when `node_uname_info` is stable-host-identity-relevant, and when OS fact promotion should be suppressed for endpoint-shaped subjects. Local-host identity predicates arise directly in provider code. Systemd unit identities arise directly in the systemd provider.

### Fact promotion is explicit, but providers can influence it

`ObservationIngestor` owns event/evidence/fact creation, and the service counts promoted facts downstream. But provider metadata can suppress fact promotion through the Prometheus-specific `_should_suppress_fact_promotion(...)` path. Thus fact promotion is implementation-explicit but not wholly independent of provider interpretation.

### Capability identity is downstream, but candidate emergence depends on observation-shaped facts

Observation providers do not appear to verify capabilities. However, capability candidates emerge from projected package observations after fact promotion. Package observation metadata intentionally says `capability_inferred=False`, but the downstream candidate builder maps package names to candidate capability strings. This separates package acquisition from capability candidate derivation, while still depending on provider-selected package predicates.

## Answers to central questions

### 1. What implementation responsibility does an Observation Provider currently own?

An observation provider owns acquisition from a source plus emission of canonical `Observation` objects. In practice, several providers also own provider-specific parsing and structural mapping into Seed subjects, predicates, values, metadata, and dimensions. The generic interface excludes ledger/projector/fact-ingestion internals, but it does not limit providers to raw acquisition.

### 2. Does implementation distinguish observation acquisition from structural interpretation?

Partially. `ObservationCollectionService` distinguishes `source.collect()` from normalization and ingestion, and some helpers split structural interpretation from collection (`relationship_observation`, `local_packages`). But the provider contract itself returns structured observations, and Prometheus/local-host/systemd providers perform structural mapping during `collect()`. Therefore the implementation does not consistently distinguish raw acquisition from structural interpretation.

### 3. Does implementation distinguish structural interpretation from identity recovery?

Partially. Endpoint alias/identity normalizers are explicit identity-recovery boundaries downstream from providers. Capability candidates and inventory are downstream read-only interpretation surfaces. Relationship helpers produce bounded structural relationship records rather than broad identity/ownership claims. However, providers still choose subjects such as Prometheus `instance`, hostnames, systemd unit names, filesystem dimensions, and package subjects before normalizers run. Structural interpretation and identity recovery remain compressed in those provider-specific mappings.

### 4. Where do service-like identities currently emerge?

Service-like identities emerge most explicitly in systemd observations as `systemd_unit` values and dimensions keyed by `unit`. The systemd source records unit identity and states while explicitly avoiding health/ownership/intent/dependency/desire interpretation. Local package observations explicitly avoid service inference, and Prometheus uses `endpoint_role` from the `job` label rather than a verified service identity. Service ownership/authority diagnostics may consume projected state elsewhere, but the reviewed observation provider paths do not recover service ownership.

### 5. Where do endpoint-like identities currently emerge?

Endpoint-like identities emerge in Prometheus from the `instance` label, which becomes the observation subject for `up`, `endpoint_role`, OS, and filesystem observations. They also emerge in listener parsing from local socket table address/port structures. Downstream endpoint alias/identity normalizers then derive aliases from metadata (`hostname`, `nodename`, `instance`, `endpoint`) and from endpoint-shaped subjects.

### 6. Where do capability-like identities currently emerge?

Capability-like identities emerge downstream in `build_capability_candidates(...)` from projected `package_installed` facts and in `build_capability_inventory(...)` from capability verification facts, ToolSpec capability metadata, and ToolNeeds. Package observations explicitly mark `capability_inferred=False`, so package providers do not directly assert capabilities. Capability candidates are explicitly not capability proof or execution authority.

### 7. Which stages are already explicit?

The following stages are explicit:

- Provider collection into `Observation`.
- Normalization pipeline and normalizer-derived observations.
- Observation-to-evidence conversion.
- Observation-to-fact conversion and optional fact suppression.
- Event ledger append during ingestion.
- Relationship syntax/front-matter extraction helpers.
- Capability candidate derivation from projected package facts.
- Capability inventory/read-only verification status from projected capability inputs.

### 8. Which stages remain implementation-compressed?

The biggest remaining compression is **provider acquisition plus provider-specific structural interpretation plus early identity shaping**. Prometheus is the clearest case: HTTP acquisition, allowlisted metric selection, response shape validation, metric-label interpretation, endpoint subject selection, endpoint role creation, filesystem dimensions, OS observation creation, and fact-promotion suppression metadata all occur in the provider path. Local-host similarly combines many local acquisition mechanisms with structural predicate and subject decisions. Repository source observation has helper separation for AST relationship extraction, but file scanning/reading/extraction/conversion still run under provider collection.

A second compression is **provider interpretation influencing fact promotion**: fact creation is downstream, but Prometheus provider metadata controls a downstream suppression rule.

## Counterexamples found

- Relationship extraction helpers operate on supplied text/metadata and explicitly avoid file reading, graph building, runtime execution, behavioral claims, ownership, and capability authority.
- Local package parsing separates dpkg wire-format parsing from generic package observation emission and explicitly denies service/capability/process/port inference.
- Endpoint alias and endpoint identity recovery run as normalizers after provider collection.
- Capability candidates and capability inventory are downstream read-only projections over existing facts/state rather than provider acquisition logic.
- Systemd source explicitly records unit identity/state but denies health, ownership, intent, dependencies, and desired state interpretation.

These counterexamples show that the implementation is not wholly compressed. They do not prove that providers own acquisition only.

## Supported conclusions

1. Current implementation already distinguishes **provider collection**, **normalization**, **event/evidence/fact ingestion**, and **capability candidate/inventory projection**.
2. Current providers do not merely return raw observations. They return canonical Seed `Observation` objects with structural subject/predicate/value choices.
3. Prometheus and local-host providers currently own more than acquisition: they interpret source-specific structures into Seed observation shapes and early identities.
4. Endpoint identity recovery is partially separated through normalizers, but providers still shape endpoint subjects before normalization.
5. Capability-like identity recovery is mostly downstream from projected facts and Tool/Need metadata, not provider-owned, but it depends on provider-emitted package fact shapes.
6. Fact promotion is explicitly owned by `ObservationIngestor`, but provider metadata can influence promotion suppression in the Prometheus OS endpoint case.

## Unsupported conclusions

- The implementation does not support the conclusion that current providers already own acquisition only.
- The implementation does not support a conclusion that services, endpoints, providers, or capabilities are fully recovered as first-class implementation identities by observation providers.
- The implementation does not support treating Prometheus `job`, `instance`, systemd unit names, package names, or listener sockets as service ownership, provider ownership, capability proof, or operational authority.
- The implementation does not prove a universal, source-independent observed-structure object between raw acquisition and `Observation` emission.

## Confidence

Confidence: **high** for the presence of implementation compression in Prometheus and local-host observation providers, because the code directly maps acquired source structures into Seed observation subjects, predicates, metadata, dimensions, and promotion-suppression metadata.

Confidence: **medium-high** for the general conclusion that implementation partially separates stages, because multiple helper/projection boundaries exist but the provider contract still returns structured observations rather than raw provider payloads.

Confidence: **medium** for service-like identity emergence, because systemd unit identity and Prometheus endpoint role are clear, but service ownership/recovery is intentionally out of scope and not established by the reviewed provider code.

## Recommended next investigation

The next bounded investigation should recover the **observed-structure boundary before identity recovery**, starting with Prometheus because it is the clearest compressed path:

```text
Prometheus HTTP/vector acquisition
↓
Prometheus observed metric sample/target structure
↓
Seed endpoint/host/filesystem observation shaping
↓
normalizer-derived identity aliases
↓
evidence/fact promotion or suppression
```

This should remain an investigation, not implementation. The question should be: which current Prometheus decisions are pure observed metric structure (metric name, labels, sample timestamp/value), and which are Seed identity/fact-shaping decisions (endpoint subject, endpoint role, OS promotion suppression, filesystem dimensions)?

## Acceptance answer

Before Seed can recover service, endpoint, provider, or capability identities, the implementation **does not yet consistently distinguish** observation acquisition, observed structure, identity recovery, evidence, and fact promotion.

It already distinguishes:

- provider collection from normalization and ingestion;
- observation from evidence and fact events;
- some endpoint identity derivation in normalizers;
- capability candidates and inventory from provider acquisition;
- some relationship/package parsing helpers from top-level provider orchestration.

It does not consistently distinguish:

- raw acquisition from provider-specific structural interpretation;
- provider-specific structural interpretation from early identity shaping;
- provider interpretation from all fact-promotion consequences.

The first compression to recover should be the **observed-structure boundary between acquisition and identity/fact shaping**, with Prometheus as the strongest evidence-backed slice.

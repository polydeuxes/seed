# Observer Decompression Implementation Investigation

## Scope

This is a bounded implementation investigation of how provider-native information becomes a canonical `Observation`. It does not implement ownership recovery, provider redesign, Evidence Interpretation, Evidence Readiness, Fact construction changes, projection changes, schema changes, behavior changes, or ledger changes.

The investigation reviewed representative provider paths rather than cataloging every provider:

- Prometheus observation provider.
- systemd observation provider.
- dpkg/local package observation path.
- Python source / AST repository-source observation path.
- Local host filesystem/platform/network-style observation path.
- Repository state / git observation provider as an adjacent provider-specific record counterexample.
- Observation collection and ingestion boundary.

Repository authority is the implementation in `seed_runtime` and the tests that exercise these paths.

## Canonical observation boundary

The canonical observation model is explicit. `Observation` is the Seed-owned structure with `id`, `source_type`, `observed_at`, `subject`, `predicate`, `value`, `confidence`, `metadata`, `dimensions`, and optional `expires_at`. Its docstring says it is the canonical external observation that can be converted into a Fact.

The generic provider contract already starts after provider-native decoding: `ObservationSource.collect()` returns `list[Observation]`. `ObservationCollectionService.collect()` calls `source.collect()`, normalizes the returned observations, and then passes them to `ObservationIngestor.ingest_many(...)`. Therefore, the runtime collection service does not receive provider-native payloads; provider-native representation and any decoded observed structures have already been consumed before the collection service boundary.

## Responsibility map by representative provider

| Provider path | Provider-native representation | Provider decoding | Provider-specific / observed structure | Identity shaping | Canonical Observation construction | Provider-specific interpretation / predicate assignment | Compression assessment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Prometheus | HTTP API JSON vector payloads from `/api/v1/query` | `_query()` validates JSON object, success status, vector result type, and list result; `_observations_from_query()` decodes samples, metric labels, timestamps, metric names, values | No separate neutral record found before `Observation`; decoded data remains Prometheus sample dictionaries and local variables | `instance` is required and becomes subject; `nodename` is metadata only for `node_uname_info`; filesystem identity labels become dimensions | `_observation()` constructs `Observation` with `obs_prometheus` id, subject, predicate, value, metadata, dimensions | Metric names map to `endpoint_role`, `up`, `os`, `filesystem_avail_bytes`, and `filesystem_size_bytes`; endpoint-subject `node_uname_info` OS observations can carry fact-promotion suppression metadata | Compressed: decoding, observed-structure selection, identity shaping, predicate assignment, metadata shaping, and observation construction are in one provider class |
| systemd | `systemctl --output=json` stdout strings | `_systemd_json_rows()` JSON-decodes stdout; `_collect_runtime_units()` and `_collect_unit_file_states()` extract unit/state dictionaries | Provider-shaped dictionaries: unit name to runtime state/substate, and unit name to unit-file state; no unit record dataclass found | Host subject is selected from configured hostname, `platform.node()`, or `localhost`; unit identity is carried in `dimensions={"unit": unit_name}` and metadata | `SystemdObservationSource._observation()` constructs `Observation` with `obs_systemd` id | Unit dictionaries map to `systemd_unit`, `systemd_active_state`, `systemd_sub_state`, and `systemd_unit_file_state` | Compressed, but with helper seams: command execution and JSON-row parsing are named helpers, while interpretation, identity shaping, predicate assignment, and observation construction remain in the source class |
| dpkg/local packages | dpkg status database text | `parse_dpkg_status()` parses dpkg records and filters `Status: install ok installed` | `PackageRecord` is a normalized package evidence record independent of package-manager wire format | Host subject supplied by local-host provider; package identity is carried in dimensions as package name and manager | `package_records_to_observations()` constructs generic package observations | Package records map to `package_installed`, `package_version`, `package_architecture`, and `package_manager`; metadata explicitly marks no service/capability/process/port inference | Mature visible chain: dpkg text → `PackageRecord` → generic package `Observation`; local-host provider only orchestrates reading and calls helper functions |
| Python source / AST repository source | Python source text read from allowlisted repository files | Relationship extraction helpers parse caller-provided Python text through AST-focused functions | `RelationshipFact` is a language-neutral relationship evidence record | Subject/object identities are shaped by relationship extraction helpers from paths and syntax; repository source provider uses those fields directly | `RepositorySourceObservationSource._relationship_observation()` constructs `Observation` from `RelationshipFact` | Relationship kind becomes predicate; relationship object becomes value; path/evidence become metadata/dimensions | Relatively mature: source scanning/reading remains in provider, but AST decoding and relationship structure are separate from `Observation` construction |
| Local host platform/filesystem/network-style observations | Python stdlib/platform calls and local read-only files under `/proc`, `/sys`, `/etc`, plus `shutil.disk_usage("/")` | Mixed helper-level parsing inside `LocalHostObservationSource`; package and systemd are delegated to specialized paths | Mixed: package has `PackageRecord`; systemd has provider-shaped dicts; many local host values flow directly from stdlib/local-file values to observations | Hostname is selected early; identity observations are constructed directly by local-host helpers; filesystem/network/storage identities are encoded in predicates, values, metadata, and dimensions in provider helpers | `LocalHostObservationSource` helpers construct observations directly for several surfaces and delegate package/systemd observations | Provider code assigns local predicates for identity, OS, architecture, disk, network, mount, storage, listener, user, package, and systemd evidence | Mixed/compressed: some subpaths are mature, but the top-level local-host source still combines acquisition, local decoding, identity selection, predicate assignment, and observation emission |
| Git repository state provider | Git command stdout, including porcelain status | `GitRepositoryObservationProvider.observe()` invokes git and parses status lines inline | `RepositoryObservation` dataclass is an explicit provider-specific observed record | Repository path is the record identity; dirty/staged/modified/untracked/remote fields are shaped in the provider method | This path returns `RepositoryObservation`, not canonical `Observation` | It assigns repository-state fields rather than observation predicates | Counterexample with an explicit observed record, but decoding and record construction are still compressed inside one provider method and it is not the `ObservationSource.collect()` path |

## Implementation evidence

### Shared collection and observation contract

- `Observation` is the canonical Seed structure, not a provider-wire-format structure. It carries subject/predicate/value plus metadata and dimensions.
- `ObservationSource.collect()` returns observations directly. This means an observation source adapter is already responsible for producing canonical observations, not just provider-native data.
- `ObservationCollectionService.collect()` consumes observations from `source.collect()`, applies normalization, and then ingests them. It does not decode Prometheus JSON, systemctl JSON, dpkg text, Python source, or git stdout.

### Prometheus provider

`PrometheusObservationSource` allowlists four safe metric names: `up`, `node_uname_info`, `node_filesystem_avail_bytes`, and `node_filesystem_size_bytes`. Its `collect()` loop calls `_query(query)`, counts result samples, and immediately calls `_observations_from_query(query, payload, seed_collected_at)`.

`_query()` owns HTTP GET construction, JSON decoding, and response shape validation. It returns the Prometheus payload dictionary after requiring a JSON object, `status == "success"`, vector result type, and list result.

`_observations_from_query()` owns most of the provider-side transformation after that point. It iterates Prometheus sample dictionaries, validates `metric` and `value`, requires `instance`, parses the sample timestamp, builds Prometheus metadata, treats `node_uname_info` as authoritative for stable host identity metadata, maps metric families to Seed predicates, sets endpoint-subject fact-promotion suppression metadata for `node_uname_info` OS observations, and emits observations through `_observation()`.

Filesystem dimensions are also shaped in the Prometheus provider path: `_filesystem_dimensions()` uses metric labels `mountpoint`, `device`, and `fstype` only for filesystem predicates.

**Finding:** Prometheus exposes a named acquisition/validation seam (`_query`) and a named observation builder (`_observation`), but no separate `PrometheusSample`, `PrometheusMetricRecord`, endpoint identity record, or provider-neutral observed structure was found between JSON payload and canonical `Observation`. This is a recurring ownership-compression example because provider decoding, identity shaping, predicate assignment, metadata policy, and observation construction occur in the same source class.

### systemd provider

`SystemdObservationSource` states its interpretation boundary in its docstring: it records systemd-reported unit identity, runtime state, substate, and unit-file enablement state, and does not interpret health, ownership, intent, dependencies, or desired state.

Its `collect()` method selects a host subject, calls `_collect_runtime_units()` and `_collect_unit_file_states()`, unions unit names, creates dimensions and metadata per unit, and constructs observations for unit existence, active state, substate, and unit-file state.

`_collect_runtime_units()` and `_collect_unit_file_states()` call `systemctl` through the configured command runner, parse rows through `_systemd_json_rows()`, and return dictionaries keyed by unit name. `_systemd_json_rows()` is a small JSON decoding/filtering helper that returns dict rows only.

**Finding:** systemd has helper seams for command output and JSON-row decoding, but the decoded structures are still provider-shaped dictionaries. The source class still owns unit interpretation, host identity selection, unit identity dimensions, predicate assignment, and canonical observation construction. This is a compressed path, though less monolithic than Prometheus because JSON parsing is separated into a helper.

### dpkg/local package path

The local-host package path is more mature. `LocalHostObservationSource._collect_local_package_observations()` reads bounded dpkg status text, then calls `parse_dpkg_status(status_text)` and `package_records_to_observations(hostname, records, observed_at, source_type)`.

`PackageRecord` is explicitly documented as normalized package evidence independent of package-manager wire format. `parse_dpkg_status()` isolates dpkg status parsing and only emits installed package records. `package_records_to_observations()` converts those normalized records into generic package observations and attaches metadata that explicitly avoids stronger inference: `service_inferred=False`, `capability_inferred=False`, `process_inferred=False`, `port_inferred=False`, and related markers.

**Finding:** The dpkg path already separates provider-native text, provider decoding, provider-neutral-ish observed structure, and generic observation emission. Identity shaping is split: the local-host provider supplies host subject, while `package_records_to_observations()` shapes package identity in dimensions. This is the clearest mature provider-side chain reviewed.

### Python source / AST path

`RepositorySourceObservationSource.collect()` discovers allowlisted source files, reads text, calls `extract_python_import_relationship_facts()` and `extract_python_definition_relationship_facts()`, and converts each returned relationship record to an `Observation`.

The relationship module declares `RelationshipFact` as the language-neutral relationship evidence record and says Python import extraction is the first adapter that emits that record. It also states that the module does not read files, scan repositories, import modules, use LLMs, reconcile claims, build graphs, or integrate with runtime/tool execution.

`RepositorySourceObservationSource._relationship_observation()` maps `relationship.subject` to observation subject, `relationship.relationship_kind` to predicate, `relationship.object` to value, and path/evidence into metadata/dimensions.

**Finding:** This path separates repository scanning/reading from AST relationship extraction and from canonical observation construction. It is not fully decompressed because the provider still orchestrates scanning, file acquisition, helper invocation, and observation construction inside `collect()`, but the existence of `RelationshipFact` is a strong counterexample to total provider compression.

### Local host provider

`LocalHostObservationSource` is a large read-only local source over Python stdlib APIs and local files. Its `collect()` method reads local identity, determines hostname, system, architecture, uname metadata, disk usage, base metadata, and then composes identity, platform, disk, network, mount, storage, listener, user, package, and systemd observations through helper calls.

The package subpath delegates to the mature dpkg chain. The systemd subpath can delegate to a `SystemdObservationSource`. Other local surfaces directly convert stdlib/local-file values into observations within the local-host source helpers.

**Finding:** Local host is mixed. It demonstrates that decomposition can exist inside one provider family, but it also compresses acquisition, local decoding, identity shaping, predicate assignment, and observation emission for several surfaces. It should not be treated as one uniform maturity level.

### Git repository state provider

`RepositoryObservation` is an explicit provider-specific observed record for repository state. `GitRepositoryObservationProvider.observe()` checks for git, verifies the path is a work tree, invokes git commands, parses porcelain status lines, computes staged/modified/untracked counters, and returns `RepositoryObservation`.

**Finding:** This path shows an intermediate observed record can exist outside canonical `Observation`, but it also shows decoding and record construction compressed inside one provider method. It is adjacent evidence rather than direct observation-ingestion evidence because this provider returns `RepositoryObservation`, not `list[Observation]`.

## Recurring implementation patterns

### Pattern 1: Runtime observation collection starts at canonical observations

The collection service is not a provider-decoding orchestrator. Its source input is an `ObservationSource`, and it calls `source.collect()` to receive observations before normalization and ingestion. Therefore, any provider-native representation has already been decoded or discarded inside provider/source code or source-adjacent helper modules.

### Pattern 2: Provider-native representation is usually private to source adapters

Prometheus JSON payloads, systemctl JSON stdout, dpkg status text, Python source text, and git stdout are not carried into the observation collection service. They are read, decoded, and transformed before the shared collection boundary.

### Pattern 3: Intermediate provider artifacts exist, but unevenly

Explicit intermediate records exist for packages (`PackageRecord`), repository relationships (`RelationshipFact`), and repository state (`RepositoryObservation`). Prometheus and systemd do not expose comparable neutral records in the reviewed paths. Systemd has provider-shaped dictionaries; Prometheus has raw payload dictionaries and sample-local variables.

### Pattern 4: Identity shaping is recurring

Identity shaping appears in multiple independent provider families:

- Prometheus requires `instance` as observation subject, treats `nodename` specially for `node_uname_info`, suppresses endpoint-shaped OS fact promotion metadata, and shapes filesystem dimensions from labels.
- systemd chooses a host subject and puts unit identity in dimensions and metadata.
- dpkg uses host subject plus package-name/package-manager dimensions.
- repository source uses relationship subject/object identities derived by relationship extraction helpers.
- local host chooses hostname and emits identity/platform/local-resource observations directly.
- git repository state uses resolved repository path as record identity.

This recurrence is implementation-backed and does not depend on architectural preference.

### Pattern 5: Predicate assignment often begins before canonical observation construction

In mature paths, predicate assignment is close to the conversion from intermediate record to observation: package records become package predicates, and relationship facts carry relationship kind that becomes the predicate. In compressed paths, predicate assignment is interleaved with provider decoding: Prometheus metric names map to predicates inside `_observations_from_query()`, and systemd runtime/unit-file dictionaries map to predicates inside `collect()`.

## Mature provider paths

### dpkg text → PackageRecord → Observation

The dpkg path is the clearest mature ownership chain found:

1. Local-host provider reads bounded dpkg status text.
2. `parse_dpkg_status()` owns dpkg-specific decoding and filtering.
3. `PackageRecord` owns normalized package evidence independent of dpkg wire format.
4. `package_records_to_observations()` owns generic package observation emission and package dimensions.

This chain demonstrates that provider-native representation, decoding, observed structure, and canonical observation construction can be visible as separate implementation steps in the current repository.

### Python source text → RelationshipFact → Observation

The repository-source path is also relatively mature:

1. Provider discovers and reads allowlisted Python files.
2. Relationship extraction helpers parse source text and emit `RelationshipFact` records.
3. The provider maps `RelationshipFact` into canonical `Observation` objects.

This chain is mature with respect to AST relationship structure, though source discovery/read orchestration and observation emission remain inside one provider class.

### Git stdout → RepositoryObservation

The git path has an explicit provider-specific record, `RepositoryObservation`, but does not end in canonical `Observation`. It supports the narrower conclusion that intermediate observed records are already a repository pattern, not that the observation ingestion path uniformly uses them.

## Compressed provider paths

### Prometheus JSON → metric decoding / endpoint identity shaping / Observation

Prometheus is the strongest compressed observation-source path reviewed. `_observations_from_query()` turns JSON samples into metric-specific predicates, uses `instance` as subject, handles `nodename`, shapes metadata, adds endpoint-subject suppression metadata, and constructs observations. No intermediate observed metric record was found.

### systemctl JSON → unit dictionaries / unit interpretation / Observation

Systemd separates JSON-row decoding but keeps unit interpretation and observation construction together. The intermediate dictionaries are implementation-local and provider-shaped, not named observed structures with their own ownership.

### Local host stdlib/local files → local identity/resource predicates / Observation

Local host is compressed for many non-package subpaths. Some helper boundaries exist, but many provider-native values become observations through the same source owner that acquires them and selects host/resource identity.

## Answers to the central questions

### 1. Does the repository currently expose recurring provider-side ownership compression?

Yes. Prometheus, systemd, and broad local-host surfaces all compress multiple recurring responsibilities before canonical observations are produced. The repeated compressed responsibilities are provider decoding, observed structure selection, identity shaping, predicate assignment, metadata/dimension shaping, and canonical observation construction.

The compression is not universal. dpkg and Python relationship extraction show intermediate artifacts and helper boundaries. The repository therefore exposes uneven maturity rather than a single flat pattern.

### 2. Which provider paths are already implementation-visible?

Implementation-visible mature or partially mature paths include:

- dpkg package observation: dpkg text → `PackageRecord` → package observations.
- Python source relationships: source text → `RelationshipFact` → relationship observations.
- Git repository state: git stdout → `RepositoryObservation`, adjacent to but not identical with canonical observation ingestion.
- Shared collection pipeline: `ObservationSource.collect()` → normalization → ingestion, starting from canonical observations.

### 3. Which provider paths remain compressed?

Compressed paths include:

- Prometheus metric payloads, especially `_observations_from_query()`.
- systemd unit collection, after JSON-row parsing.
- Local-host non-package surfaces, including identity/platform/disk/network/mount/storage/listener/user-style observations.
- Git repository state decoding remains method-compressed even though it emits an explicit `RepositoryObservation` record.

### 4. Is identity shaping a recurring implementation responsibility?

Yes. Identity shaping recurs across Prometheus endpoint and filesystem labels, systemd host/unit dimensions, package host/package dimensions, repository relationship subject/object identity, local-host hostname/resource identity, and git repository path identity.

The implementation evidence supports identity shaping as a recurring provider-side responsibility. It does not prove that identity shaping should be one shared abstraction or that all identity shaping should move out of providers.

### 5. Where does canonical Observation construction currently begin?

Canonical `Observation` construction begins inside provider/source code or source-adjacent helper modules, before `ObservationCollectionService` receives data:

- Prometheus: `_observation()` inside `PrometheusObservationSource`.
- systemd: `_observation()` inside `SystemdObservationSource`.
- dpkg/local packages: `package_records_to_observations()` in `seed_runtime.local_packages`.
- repository source: `_relationship_observation()` inside `RepositorySourceObservationSource`.
- local host: multiple local-host helper methods, plus delegated package/systemd paths.

The shared collection service begins after canonical observation construction.

### 6. What is the smallest implementation-backed ownership family supported by the evidence?

The smallest recurring provider-side ownership family supported by implementation evidence is:

```text
provider-native representation
→ provider decoding
→ observed structure / identity shaping
→ predicate and dimension assignment
→ canonical Observation construction
```

The evidence supports investigating this as a provider-side observation-construction ownership family. It is smaller and better supported than broader families such as Evidence Interpretation, Evidence Readiness, Fact support, projection ownership, or provider execution decisions, which are explicitly outside this investigation and are not needed to explain how provider-native information becomes canonical observations.

## Unsupported conclusions

The reviewed implementation does not support these conclusions:

- That providers should be redesigned now.
- That a new schema or ledger event type is required.
- That all provider-side identity shaping is wrong.
- That canonical observations should never be built inside providers.
- That Prometheus endpoint observations are facts or authoritative host identity by themselves.
- That systemd unit states imply health, desired state, ownership, dependencies, or operator intent.
- That package presence implies service, capability, process, port, vulnerability, or patch status.
- That repository source relationships prove runtime behavior, calls, boundaries, reachability, or ownership.
- That Evidence Interpretation, Evidence Readiness, Fact construction, projection changes, or provider execution decisions are part of this ownership question.

## Confidence

Confidence is high for the existence of recurring provider-side ownership compression because the reviewed implementation shows the same combined responsibilities in Prometheus, systemd, and local-host paths.

Confidence is high that dpkg and Python relationship extraction are more mature counterexamples because they expose named intermediate records (`PackageRecord`, `RelationshipFact`) before canonical observation construction.

Confidence is medium for the exact boundary name of the smallest ownership family. The implementation clearly supports a recurring provider-side observation-construction family, but it does not yet prescribe whether future ownership should be named around decoding, observed structure, identity shaping, observation building, or another repository-local term.

## Recommended first ownership investigation

A first ownership investigation is justified, but only as an investigation, not implementation recovery.

The recommended first investigation should focus on the provider-side transition from decoded provider data to canonical observation:

```text
decoded provider record / provider-specific structure
→ identity shaping
→ predicate and dimension assignment
→ Observation construction
```

Prometheus and systemd are the best comparison pair for this investigation because both currently expose helper seams but still compress multiple responsibilities before producing observations. Dpkg and Python relationship extraction should be used as counterexamples showing that intermediate records can already exist in the repository without changing fact ingestion or projections.

No implementation recovery is recommended by this report beyond that bounded follow-up investigation. The current evidence supports identifying a recurring compressed responsibility, not prescribing a redesign.

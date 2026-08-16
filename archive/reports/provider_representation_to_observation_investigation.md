# Provider Representation to Observation Investigation

## Scope

This is a bounded implementation investigation. It does not recover ownership, redesign providers, introduce representation or observation abstractions, add probes, or add automation. It reviews current implementation evidence for whether Seed distinguishes:

```text
external provider representation
provider decoding
observed structure
identity recovery
observation
evidence
fact
```

Repository authority wins over architectural preference.

## Implementation evidence reviewed

Primary implementation evidence reviewed:

- `seed_runtime/observation_sources.py`
  - `ObservationSource`
  - `RepositorySourceObservationSource`
  - `LocalHostObservationSource`
  - `PrometheusObservationSource`
  - `SystemdObservationSource`
  - `ObservationCollectionService`
- `seed_runtime/observations.py`
  - `Observation`
  - `ObservationIngestor`
- `seed_runtime/observation_normalizers.py`
  - `ObservationNormalizer`
  - `ObservationNormalizationPipeline`
- `seed_runtime/local_packages.py`
  - `PackageRecord`
  - `parse_dpkg_status`
  - `package_records_to_observations`
- `seed_runtime/repository_observation.py`
  - `RepositoryObservation`
  - `GitRepositoryObservationProvider`
- `seed_runtime/knowledge/relationship_observation.py`
  - `RelationshipFact`
  - Python import and definition extraction
- `seed_runtime/knowledge/repository_observation.py`
  - `RepositoryArtifactObservationAdapter`

Terminal commands used:

```bash
pwd && rg --files -g 'AGENTS.md' -g '!ls-R' .. /workspace 2>/dev/null | head -50 && git status --short
cat AGENTS.md && rg -n "PrometheusObservationSource|Repository Observation|Repository Source Observation|Relationship Observation|Local Package|Systemd|ObservationSource|Observation|diagnostic" -S .
rg --files | rg 'seed_runtime|tests' | head -200 && rg -n "class .*ObservationSource|PrometheusObservationSource|Repository.*ObservationSource|LocalPackage|Systemd|ObservationNormalizer|class Observation|ObservationIngestor" seed_runtime tests scripts -S
sed -n '1,140p' seed_runtime/observations.py; sed -n '1,120p' seed_runtime/observation_normalizers.py; sed -n '80,230p' seed_runtime/observation_sources.py; sed -n '172,245p' seed_runtime/observation_sources.py; sed -n '2397,2654p' seed_runtime/observation_sources.py
sed -n '140,240p' seed_runtime/observations.py; sed -n '3200,3275p' seed_runtime/observation_sources.py; sed -n '1,240p' seed_runtime/local_packages.py; sed -n '2655,2847p' seed_runtime/observation_sources.py; sed -n '1,220p' seed_runtime/knowledge/relationship_observation.py; sed -n '1,220p' seed_runtime/knowledge/repository_observation.py
rg -n "parse_dpkg_status|package_records_to_observations|systemd_source|LocalHostObservationSource|subprocess.run|git |RepositoryObservation" seed_runtime tests -S
sed -n '1,220p' seed_runtime/repository_observation.py; sed -n '568,760p' seed_runtime/observation_sources.py; sed -n '760,860p' seed_runtime/observation_sources.py; sed -n '2800,2847p' seed_runtime/observation_sources.py; sed -n '220,340p' seed_runtime/knowledge/relationship_observation.py
nl -ba seed_runtime/observations.py | sed -n '29,210p'; nl -ba seed_runtime/observation_sources.py | sed -n '83,120p;172,235p;568,755p;2397,2545p;2655,2845p;3202,3268p'; nl -ba seed_runtime/local_packages.py | sed -n '21,124p'; nl -ba seed_runtime/repository_observation.py | sed -n '13,105p;133,150p'; nl -ba seed_runtime/knowledge/relationship_observation.py | sed -n '1,170p;224,280p'; nl -ba seed_runtime/knowledge/repository_observation.py | sed -n '1,90p'
nl -ba seed_runtime/observation_sources.py | sed -n '721,755p;2397,2545p;2655,2765p;2766,2845p;3202,3268p'; nl -ba seed_runtime/local_packages.py | sed -n '21,124p'; nl -ba seed_runtime/observations.py | sed -n '211,235p'
```

## Current observation and ingestion boundaries

The shared observation type is already explicit. `Observation` is the canonical structure accepted by ingestion, with `id`, `source_type`, `observed_at`, `subject`, `predicate`, `value`, `confidence`, `metadata`, `dimensions`, and optional `expires_at` fields. This means Seed-owned observation structure begins no later than construction of this model. The model is subject/predicate/value shaped, not provider-wire-format shaped.

`ObservationSource` also makes one boundary explicit: a source adapter must expose `collect() -> list[Observation]`. The interface says sources emit observations and remain unaware of the event ledger, state projector, and fact-ingestion internals.

After source collection, `ObservationCollectionService.collect()` treats provider output as observations: it calls `source.collect()`, then `_normalize_observation(...)`, then the optional normalization pipeline, then `ObservationIngestor.ingest_many(...)`. This is an explicit collection → normalization → ingestion sequence, but it starts from `Observation` objects, not from provider-native representations.

`ObservationIngestor.ingest_many()` is the explicit Observation → Evidence → Fact transition. For each observation it creates evidence with observation fields copied into payload, creates an observation event, creates an evidence event, and optionally promotes to a fact. `observation_to_fact()` then copies `Observation.subject` into `Fact.subject_id`, `Observation.predicate` into `Fact.predicate`, and `Observation.value` into `Fact.value`.

## Provider-native representations currently found

### Prometheus

Provider-native representation exists as Prometheus HTTP API JSON vector payloads. `PrometheusObservationSource._query()` performs an HTTP GET against `/api/v1/query`, JSON-decodes the response body, validates that the result is a JSON object with `status == "success"`, validates `data.resultType == "vector"`, validates `data.result` is a list, and returns the raw payload dictionary.

Provider decoding and observation construction remain inside `PrometheusObservationSource`. `collect()` loops over safe query names, receives `payload = self._query(query)`, reads `payload["data"]["result"]` for counters, and immediately passes the same provider payload into `_observations_from_query(...)`. `_observations_from_query(...)` then interprets Prometheus sample dictionaries, metric labels, vector `value` arrays, `instance`, timestamps, `job`, `nodename`, and metric names before constructing `Observation` objects.

The first identity-bearing subject in this path is the Prometheus `instance` label. `_observations_from_query(...)` skips samples without a string `instance`, then passes `instance` as the observation subject. For `node_uname_info`, the same method treats `nodename` specially in metadata for alias normalization while noting that only `node_uname_info` is authoritative for stable host identity.

**Boundary conclusion:** Prometheus distinguishes provider acquisition/validation (`_query`) from observation construction (`_observations_from_query`) only as private methods inside one provider class. Provider representation, provider-specific decoding, observed structure selection, and early identity shaping remain compressed within `PrometheusObservationSource`.

### Git repository state

Provider-native representation exists as git command stdout strings. `GitRepositoryObservationProvider.observe()` calls `_git_text(...)` for `rev-parse HEAD`, `branch --show-current`, `remote`, and `status --porcelain=v1`. `_git_text(...)` uses `subprocess.run(..., text=True, capture_output=True, check=False)` and returns stdout as text when the command succeeds.

The decoded Seed-owned structure is `RepositoryObservation`, a dataclass containing repository path, VCS, head commit, branch, dirty status, staged/modified/untracked counts, remote presence, status availability, reason, and read-only mutation flags. The provider parses porcelain status lines inline, counting untracked, staged, and modified entries before constructing `RepositoryObservation`.

**Boundary conclusion:** Repository state has a provider-specific representation (`git` stdout) and a Seed-owned decoded structure (`RepositoryObservation`). However, decoding and identity/field shaping are not separate implementation owners; the `GitRepositoryObservationProvider.observe()` method both acquires git outputs, decodes porcelain status, computes counts, and constructs the observed repository-state record.

### Repository source / Python relationship observation

Provider-native representation exists as repository Python source text, and internally as Python AST nodes created from that text. `RepositorySourceObservationSource.collect()` discovers allowlisted Python files, reads each file's text, calls `extract_python_import_relationship_facts(...)` and `extract_python_definition_relationship_facts(...)`, and converts each returned relationship into an `Observation`.

A provider-neutral intermediate structure exists here: `RelationshipFact` has `relationship_kind`, `subject`, `object`, `path`, and `evidence`. The relationship observation module explicitly calls `RelationshipFact` a language-neutral relationship evidence record and states that Python import extraction is the first adapter that emits it. The extraction functions parse caller-provided source text with `ast.parse(...)`, derive `subject = _subject_from_path(source_path)`, inspect top-level import/from-import/function/class nodes, and return `RelationshipFact` records.

`RepositorySourceObservationSource._relationship_observation(...)` then maps `RelationshipFact.subject` to `Observation.subject`, `relationship_kind` to `Observation.predicate`, and `object` to `Observation.value`.

**Boundary conclusion:** Repository source observation is the strongest counterexample to total compression. It separates Python source/AST decoding into relationship-fact extraction and then maps a provider-neutral-ish `RelationshipFact` to `Observation`. The remaining compression is that repository scanning, source-text acquisition, call to Python-specific decoding, and conversion to `Observation` are orchestrated by `RepositorySourceObservationSource.collect()`.

### Repository artifact observation

A related repository artifact adapter receives caller-provided Python source text and emits `RepositoryArtifactFact` records. Its boundary dataclass explicitly marks Python parsing, module/class/function/method/import observation, repository artifact record construction, and read-only behavior. The adapter parses text with `ast.parse(...)`, returns a module fact even on parse failure, and emits structural facts for top-level classes, functions, async functions, methods, and imports.

**Boundary conclusion:** This path shows an explicit adapter boundary for Python repository artifacts and a provider-neutral structural record, but this reviewed adapter is not itself the `ObservationSource.collect() -> list[Observation]` ingestion path. It supports the conclusion that some repository-source decoding is already separated from file acquisition, but not that all provider-to-observation responsibilities are separated in the runtime observation pipeline.

### Local packages / dpkg

Provider-native representation exists as dpkg status database text read from `/var/lib/dpkg/status`. `LocalHostObservationSource._collect_local_package_observations(...)` reads bounded text from the configured dpkg status path, calls `parse_dpkg_status(status_text)`, then calls `package_records_to_observations(...)`.

A provider-neutral intermediate structure exists: `PackageRecord` is documented as normalized package evidence independent of package-manager wire format. `parse_dpkg_status(...)` parses dpkg record text into `PackageRecord` instances only for records with `Status: install ok installed`, retaining name, manager, version, and architecture. `package_records_to_observations(...)` converts those package records into generic package observations such as `package_installed`, `package_version`, `package_architecture`, and `package_manager` with host as subject and package identity in dimensions.

**Boundary conclusion:** Local package parsing already separates dpkg wire-format decoding (`parse_dpkg_status`) from generic observation emission (`package_records_to_observations`) through `PackageRecord`. The transition from provider-native text to Seed-owned structure is explicit at `PackageRecord`; observation begins later when `Observation` objects are constructed. This is a counterexample to the idea that providers always directly emit observations without an intermediate observed structure.

### Systemd

Provider-native representation exists as `systemctl --output=json` stdout strings. `SystemdObservationSource._run_command(...)` executes the configured systemctl command and returns stdout. `_collect_runtime_units()` and `_collect_unit_file_states()` pass that stdout to `_systemd_json_rows(...)`, which JSON-decodes into a list of dictionaries and filters non-dict entries.

Decoded systemd structures are still provider-shaped dictionaries: runtime units are a dict keyed by unit name with `active` and `sub`; unit-file states are a dict mapping unit name to state. `SystemdObservationSource.collect()` combines those dictionaries, selects `subject_host`, iterates unit names, and constructs observations for `systemd_unit`, `systemd_active_state`, `systemd_sub_state`, and `systemd_unit_file_state` with the unit name in dimensions.

**Boundary conclusion:** Systemd has private helper boundaries for command execution and JSON-row parsing. But decoding into provider-specific dictionaries, observed structure selection, identity selection (`subject_host`, unit dimension), and observation construction remain in one source class. There is no separate provider-neutral observed-structure dataclass equivalent to `PackageRecord` or `RelationshipFact` in the reviewed implementation.

### Local host stdlib and local files

`LocalHostObservationSource.collect()` receives native Python/platform representations rather than a single external wire format: `platform.node()`, `platform.system()`, `platform.machine()`, `os.uname()`, `shutil.disk_usage("/")`, local files under `/proc`, `/sys`, `/etc`, and delegated package/systemd collection. It constructs observations directly for identity, OS, architecture, disk, network, mount, storage, listener, user, package, and systemd evidence.

**Boundary conclusion:** Local host observation is mixed. Some subpaths have explicit intermediate records or helper parsing, especially dpkg packages and delegated systemd. Other subpaths directly convert Python stdlib/local-file values into observations within `LocalHostObservationSource` helpers. The reviewed evidence does not show a uniform provider representation → decoding → provider-neutral observed-structure boundary for all local host surfaces.

## Representation decoding boundaries

### Already explicit

1. **ObservationSource to ingestion:** `ObservationSource.collect()` returns `list[Observation]`; `ObservationCollectionService.collect()` only sees observations from the source, then normalizes and ingests them.
2. **Observation to Evidence to Fact:** `ObservationIngestor` explicitly creates observation, evidence, and fact events, with `observation_to_evidence()` and `observation_to_fact()` as named conversion points.
3. **Dpkg status text to PackageRecord:** `parse_dpkg_status()` converts provider-specific dpkg text into normalized package records.
4. **PackageRecord to Observation:** `package_records_to_observations()` converts generic package records into observations.
5. **Python source/AST to RelationshipFact:** relationship extraction functions parse Python text and emit relationship records.
6. **RelationshipFact to Observation:** `RepositorySourceObservationSource._relationship_observation()` maps relationship fields to observation fields.
7. **Prometheus HTTP acquisition/validation:** `_query()` is a named boundary for HTTP GET, JSON decode, and vector validation.
8. **Systemd command output JSON row parsing:** `_systemd_json_rows()` is a named boundary for JSON decoding/filtering.
9. **Git subprocess output acquisition:** `_git_text()` is a named boundary for running git commands and returning stdout text.

### Explicit but still provider-specific

- Prometheus `_query()` returns raw Prometheus payload dictionaries, not provider-neutral structures.
- Prometheus `_observations_from_query()` is named separately but still contains metric-specific decoding, identity decisions, predicate selection, metadata shaping, and observation construction.
- Systemd `_collect_runtime_units()` and `_collect_unit_file_states()` produce dictionaries shaped by systemd keys and Seed-selected keys, but not a neutral unit record type.
- Git `_git_text()` separates command execution from parsing, but `GitRepositoryObservationProvider.observe()` still parses status and constructs `RepositoryObservation` in the same method.

## Observed-structure boundaries

Provider-neutral or provider-neutral-ish structures first appear at different points depending on provider:

| Area | Provider-native representation | First reviewed Seed-owned observed structure | Observation object begins |
| --- | --- | --- | --- |
| Prometheus | HTTP JSON vector dict with metric labels and value arrays | No separate neutral structure found before `Observation`; metadata/dimensions are shaped inside source | `_observation(...)` inside `PrometheusObservationSource` |
| Git repository state | git stdout text | `RepositoryObservation` dataclass | This path is not the canonical `Observation` ingestion model in reviewed code |
| Repository source relationships | Python file text / AST nodes | `RelationshipFact` | `_relationship_observation(...)` |
| Repository artifacts | Python file text / AST nodes | `RepositoryArtifactFact` | Not shown as canonical `Observation` ingestion in reviewed code |
| Local packages | dpkg status text | `PackageRecord` | `package_records_to_observations(...)` |
| Systemd | systemctl JSON stdout → JSON row dicts | Provider-shaped runtime/unit-file dictionaries; no neutral dataclass found | `_observation(...)` inside `SystemdObservationSource` |
| Local host stdlib/files | platform/os/shutil values and local file text | Mixed helper-level structures; no uniform neutral record for all subpaths found | LocalHostObservationSource helper `_observation(...)` calls |

## Observation boundaries

For canonical ingestion, observations begin when an `Observation` instance is constructed. The source interface already requires collected output to be `list[Observation]`, and ingestion assumes it is receiving observations.

Therefore, in current implementation, the runtime observation pipeline does **not** expose provider-native representation or decoded observed structures to `ObservationCollectionService`. Those boundaries, when present, are inside source adapters or source-adjacent helper modules. By the time `ObservationCollectionService` receives data, provider-native representation has already stopped.

## Identity-bearing subjects

Identity-bearing subjects first emerge at different layers:

- **Prometheus:** `instance` is required and becomes the observation subject; `nodename` is metadata only for `node_uname_info` and later alias normalization.
- **Git repository state:** repository path is resolved at the start of `observe()`, and repository-specific fields become `RepositoryObservation` attributes. There is no canonical `Observation.subject` in the reviewed repository-state path.
- **Repository source relationships:** `_subject_from_path(source_path)` transforms Python file paths into dotted module-like subjects before `RelationshipFact` is emitted.
- **Repository artifact observation:** `source_path` and symbols become artifact identity fields in `RepositoryArtifactFact` records.
- **Local packages:** host is supplied to `package_records_to_observations()` and becomes `Observation.subject`; package identity is carried in dimensions.
- **Systemd:** host identity is `hostname` or `platform.node()` or `localhost`; unit identity is not the subject but is carried as the observation value for `systemd_unit` and as `dimensions = {"unit": unit_name}` for unit-scoped facts.
- **Local host:** hostname is selected in `LocalHostObservationSource.collect()` from `platform.node()` or local identity file values and is used as the subject for many local observations.

## Answers to central questions

### 1. What provider-native representations currently exist?

Reviewed provider-native representations include:

- Prometheus HTTP API JSON vector dictionaries with `data.result`, metric labels, and value arrays.
- git command stdout text, especially `status --porcelain=v1`.
- Python source text and Python AST nodes for repository source and artifact extraction.
- dpkg status database text.
- `systemctl --output=json` stdout decoded into JSON row dictionaries.
- Python stdlib/local-host values such as platform/uname/disk usage and local `/proc`, `/sys`, and `/etc` file contents.

### 2. Does implementation distinguish provider representation from provider decoding?

Partially.

- Dpkg clearly distinguishes dpkg text from decoded `PackageRecord` records.
- Repository relationship extraction distinguishes caller-provided Python source text/AST parsing from emitted `RelationshipFact` records.
- Repository artifact extraction similarly distinguishes Python source text/AST parsing from emitted `RepositoryArtifactFact` records.
- Prometheus distinguishes `_query()` acquisition/validation from `_observations_from_query()`, but `_query()` still returns provider JSON and `_observations_from_query()` handles decoding and observation construction together.
- Systemd distinguishes command execution from JSON row parsing, but provider-specific decoded dictionaries remain inside the source.
- Git distinguishes command execution in `_git_text()`, but status decoding and observed-record construction remain in `observe()`.

### 3. Does implementation distinguish provider decoding from observed structure?

Sometimes.

- Yes for dpkg: `parse_dpkg_status()` emits `PackageRecord`, then `package_records_to_observations()` emits observations.
- Yes for repository relationships: Python parsing emits `RelationshipFact`, then repository source maps it to `Observation`.
- Yes for repository artifacts, though not necessarily in the canonical ingestion path: Python parsing emits `RepositoryArtifactFact`.
- No clear separate neutral observed structure was found for Prometheus or Systemd before `Observation` construction.
- Git has `RepositoryObservation` as observed structure, but the decoding and structure construction are in the same provider method.

### 4. Where do provider-neutral structures first appear?

- `PackageRecord` for local packages.
- `RelationshipFact` for repository source relationships.
- `RepositoryArtifactFact` for repository artifact extraction.
- `RepositoryObservation` for git repository state, though git decoding and structure construction remain coupled.
- Canonical `Observation` for Prometheus and Systemd, because no earlier neutral record was found in reviewed implementation.

### 5. Where do identity-bearing subjects first appear?

- Prometheus: in `_observations_from_query()` when `instance` is validated and used as subject.
- Repository source relationships: in `_subject_from_path(source_path)` before `RelationshipFact` construction.
- Local packages: at `package_records_to_observations(host, ...)`, where host becomes subject and package dimensions are added.
- Systemd: in `collect()` through `subject_host`, before unit observations are emitted; unit identity becomes dimensions.
- Git repository state: at path resolution in `observe()`, but not as canonical `Observation.subject` in reviewed code.

### 6. Where do observations actually begin?

In the canonical ingestion path, observations begin at `Observation(...)` construction. `ObservationCollectionService` receives only `Observation` objects from a source, normalizes them, and ingests them. The service does not receive provider-native representations.

In source-specific paths, observation construction occurs at:

- `PrometheusObservationSource._observation(...)`.
- `RepositorySourceObservationSource._relationship_observation(...)`.
- `package_records_to_observations(...)` for packages.
- `SystemdObservationSource._observation(...)`.
- Many `LocalHostObservationSource` helper `_observation(...)` calls.

### 7. Which transitions are already explicit?

Already explicit:

- Source collection to normalization to ingestion in `ObservationCollectionService`.
- Observation to evidence to fact in `ObservationIngestor`.
- Dpkg text to `PackageRecord` to `Observation`.
- Python source/AST to `RelationshipFact` to `Observation` for repository source relationships.
- Python source/AST to `RepositoryArtifactFact` for repository artifacts.
- Prometheus HTTP JSON acquisition/validation in `_query()`.
- Systemd command stdout to JSON rows in `_systemd_json_rows()`.
- Git command execution to stdout text in `_git_text()`.

### 8. Which transitions remain implementation-compressed?

Remaining compressions found:

- Prometheus compresses provider-specific decoding, metric interpretation, predicate selection, identity selection, metadata shaping, dimensions, and observation construction inside `PrometheusObservationSource._observations_from_query()` and `_observation()`.
- Systemd compresses provider-specific decoded dictionaries, host/unit identity selection, predicate selection, dimensions, metadata, and observation construction inside `SystemdObservationSource`.
- Git repository state compresses git command orchestration, porcelain decoding, repository-state calculation, and `RepositoryObservation` construction in `GitRepositoryObservationProvider.observe()`.
- `RepositorySourceObservationSource.collect()` still combines repository scanning, source-text acquisition, Python extraction invocation, and conversion of `RelationshipFact` to `Observation`, even though relationship extraction itself is separated.
- `LocalHostObservationSource.collect()` remains a broad orchestrator that combines many local acquisition and observation-emission responsibilities; package and systemd subpaths are more separated than others.

## Supported conclusions

1. The current implementation does **not** uniformly follow an externally visible chain of `External Provider → Provider Representation → Representation Decoding → Observed Structure → Identity Recovery → Observation → Evidence → Fact`.
2. The canonical runtime collection service starts at `Observation`, not at provider-native representation. Provider-native representation and decoding, where present, happen before `ObservationCollectionService.collect()` receives data.
3. Some providers already separate provider representation from observed structure: dpkg uses `PackageRecord`; repository relationships use `RelationshipFact`; repository artifacts use `RepositoryArtifactFact`.
4. Prometheus and Systemd do not show separate provider-neutral observed-structure records before `Observation` in reviewed code.
5. Identity recovery is not uniformly independent of provider decoding. Prometheus `instance`, repository `_subject_from_path`, package host/dimensions, and systemd host/unit identity are selected in provider-specific or adapter-specific code.
6. Observation → Evidence → Fact is explicit and repository-neutral after `Observation` objects exist.

## Unsupported conclusions

The reviewed evidence does **not** support these claims:

- That all providers already separate provider-native representation from observations.
- That all provider decoding is centralized or repository-neutral.
- That identity recovery is currently independent of provider-specific decoding.
- That Prometheus has a provider-neutral observed-structure layer before `Observation`.
- That Systemd has a provider-neutral unit record before `Observation`.
- That repository-state `RepositoryObservation` participates in the same canonical `ObservationIngestor` path in the reviewed implementation.
- That service, endpoint, capability, or program identity recovery is already downstream of a uniform provider-neutral observed-structure phase.

## Confidence

Medium-high for the reviewed paths. The strongest evidence comes from concrete source files and named conversion functions. Confidence is lower for unreviewed local-host helper subpaths because `LocalHostObservationSource` is large and this investigation focused on requested areas rather than every local observation helper.

## Recommended next investigation

A bounded next investigation should inventory every concrete `Observation(...)` construction site and classify whether each one is preceded by:

1. raw provider representation only;
2. provider-specific decoded dictionaries/tuples;
3. a provider-neutral intermediate record; or
4. another canonical `Observation`.

That investigation should remain read-only and should not introduce abstractions or redesign providers.

## Acceptance answer

Before Seed can recover services, endpoints, capabilities, or program identities, the implementation does **not** always first recover provider-native representations, decode them into provider-neutral observed structure, and only then create observations.

Current implementation evidence shows mixed behavior:

- For local packages and repository relationships, provider-native representation is decoded into an intermediate Seed-owned structure before observations are created.
- For Prometheus and Systemd, provider-native representations are acquired and decoded inside provider classes, and identity shaping plus observation construction happen in the same provider-specific implementation area.
- For git repository state, provider-native stdout is decoded into a `RepositoryObservation` record, but command orchestration, decoding, counting, and observed-record construction are compressed in one provider method.
- The repository-neutral Observation → Evidence → Fact transition begins only after providers have already emitted canonical `Observation` objects.

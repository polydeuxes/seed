# Intermediate Structure Responsibility Investigation

## Scope

This investigation reviews implementation evidence around `PackageRecord`, `RelationshipFact`, `RepositoryArtifactFact`, `RepositoryObservation`, Observation Sources, Observation Ingestor, Observation Normalization, Repository Observation, and Repository Source Observation.

The question is bounded: before Seed creates canonical `Observation` records, does current implementation already recover a recurring intermediate responsibility between provider-native representations and Seed Observations?

This is not ownership recovery, provider redesign, or a proposal for a new artifact abstraction.

## Implementation evidence reviewed

- `seed_runtime/local_packages.py`
  - `PackageRecord`
  - `parse_dpkg_status(...)`
  - `package_records_to_observations(...)`
- `seed_runtime/knowledge/relationship_observation.py`
  - `RelationshipFact`
  - documentation-navigation relationship extraction
  - Python import and definition relationship extraction
- `seed_runtime/knowledge/repository_observation.py`
  - `RepositoryArtifactObservationAdapterBoundary`
  - `RepositoryArtifactObservationAdapter.extract(...)`
  - `extract_repository_artifact_facts(...)`
- `seed_runtime/knowledge/self_model_alignment.py`
  - `RepositoryArtifactFact`
  - supplied-record reconciliation boundary
- `seed_runtime/repository_observation.py`
  - `RepositoryObservation`
  - `GitRepositoryObservationProvider.observe(...)`
  - `repository_observation_json(...)`
  - `format_repository_observation(...)`
- `seed_runtime/observation_sources.py`
  - `RepositorySourceObservationSource`
  - `LocalHostObservationSource._collect_local_package_observations(...)`
  - `SystemdObservationSource`
  - `ObservationCollectionService`
- `seed_runtime/observations.py`
  - canonical `Observation`
  - `ObservationIngestor`
- `seed_runtime/observation_normalizers.py`
  - `ObservationNormalizationPipeline`

## Canonical Observation boundary

The canonical Seed `Observation` model has the common ingestion-facing shape: `id`, `source_type`, `observed_at`, `subject`, `predicate`, `value`, `confidence`, `metadata`, `dimensions`, and optional expiration. `ObservationIngestor` converts those observations into provenance `Evidence` and observed or inferred `Fact` events.

`ObservationCollectionService` enforces that observation sources collect `Observation` instances before ingestion. It then source-normalizes metadata, optionally runs the normalization pipeline, and calls `ObservationIngestor.ingest_many(...)`.

This means the canonical observation boundary is not just any observed record. In ingestion paths, an intermediate record must become an `Observation` before the collection service and ingestor can treat it as observation/evidence/fact input.

## Recurring intermediate structures

### `PackageRecord`

`PackageRecord` is explicitly documented as normalized package evidence independent of a package-manager wire format. `parse_dpkg_status(...)` parses dpkg status database text into `PackageRecord` instances only when `Status` is exactly `install ok installed`; malformed records and records missing `Package` or `Status` are skipped.

Responsibilities recovered from implementation:

- Decode provider-native dpkg status text into a Seed-owned package record.
- Preserve package name, package manager, installed state, version, and architecture.
- Intentionally discard non-installed dpkg records, malformed records, records without `Package`, records without `Status`, and all dpkg fields not represented by the dataclass.
- Preserve the package-manager source as `manager="dpkg"` rather than leaving the package unscoped.
- Defer canonical `Observation` emission to `package_records_to_observations(...)`, which expands each installed package record into generic package predicates such as `package_installed`, `package_version`, `package_architecture`, and `package_manager`.

Why not directly `Observation`?

The implementation separates dpkg parsing from generic package observation emission. `LocalHostObservationSource._collect_local_package_observations(...)` reads the bounded local status file, calls `parse_dpkg_status(...)`, and only then calls `package_records_to_observations(...)`. The helper docstring states that dpkg parsing and generic package observation emission live in `seed_runtime.local_packages` so dpkg remains the first adapter rather than the package observation architecture.

Why not provider-native representation?

The native representation is dpkg record text. The implementation discards dpkg's full field map and keeps only package fields that generic package observation emission uses.

### `RelationshipFact`

`RelationshipFact` is the language-neutral relationship evidence record used by relationship-observation adapters. The module docstring states that Python import extraction is the first adapter that emits that record, and that import relationships are dependency/name-availability evidence only, while definition relationships are syntactic declaration evidence only.

Responsibilities recovered from implementation:

- Convert authored documentation navigation metadata or Python syntax into relationship-shaped evidence records.
- Preserve relationship kind, subject, object, path, and evidence text.
- Normalize document identities and relative document references for documentation metadata.
- Normalize Python file paths into dotted module-like subjects before creating Python relationship facts.
- Preserve import targets and definition symbols as relationship objects.
- Preserve bounded evidence text, including line ranges for definitions.
- Intentionally discard AST node objects, full source text, implementation bodies, call behavior, route behavior, ownership, capability authority, runtime reachability, and graph meaning.

Why not directly `Observation`?

Relationship extraction helpers return `RelationshipFact`, not canonical `Observation`. `RepositorySourceObservationSource.collect(...)` separately maps relationship facts into observations by assigning `relationship.subject` to `Observation.subject`, `relationship.relationship_kind` to `Observation.predicate`, and `relationship.object` to `Observation.value`.

Why not provider-native representation?

The provider-native inputs are YAML/front-matter metadata supplied by the caller or Python source text parsed as AST. The implementation does not pass AST nodes or raw metadata through ingestion. It emits a bounded record shape with a stable relationship vocabulary and explicit evidence string.

### `RepositoryArtifactFact`

`RepositoryArtifactFact` is defined in the self-model alignment module as a fixture-level record with `fact`, `artifact_kind`, `path`, `symbol`, and optional `parent_symbol`. The module says it does not inspect the repository, parse documentation, project state, or integrate with runtime execution; it reconciles supplied fixture records.

The repository artifact adapter emits `RepositoryArtifactFact` records from caller-provided Python source text. Its boundary explicitly identifies Python parsing, structural extraction, preservation of evidence, repository artifact record construction, and read-only behavior. It also explicitly rejects content interpretation, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, and cluster mutation.

Responsibilities recovered from implementation:

- Convert caller-provided Python source text into structural repository artifact facts.
- Always preserve a module/file fact for the path.
- Preserve top-level classes, top-level functions, async functions, direct class methods, and imports when Python parsing succeeds.
- Preserve structural identity through artifact kind, path, symbol, and parent symbol for methods.
- Preserve human-readable evidence text in `fact`.
- Intentionally discard full AST nodes, function/class bodies, nested structures beyond direct class methods, behavior, architecture meaning, ownership, lexicon authority, runtime integration, repository mutation, event-ledger mutation, and cluster mutation.

Why not directly `Observation`?

The adapter emits `RepositoryArtifactFact`, not `Observation`. Downstream self-model alignment consumes supplied `RepositoryArtifactFact` records directly as acquisition-side evidence, not via the observation ingestion model.

Why not provider-native representation?

The provider-native representation is Python text/AST. The adapter bounds that into stable structural fields and does not expose AST internals downstream.

### `RepositoryObservation`

`RepositoryObservation` is a read-only repository-state record, not the canonical ingestion `Observation` class. It preserves repository path, VCS, head commit, branch, dirty state, untracked/modified/staged counts, remote presence, status availability, reason, and mutation flags.

`GitRepositoryObservationProvider.observe(...)` acquires provider-native git command stdout, decodes porcelain status lines, counts untracked/staged/modified entries, and returns a `RepositoryObservation`. Formatting and JSON helper functions consume `RepositoryObservation` directly.

Responsibilities recovered from implementation:

- Convert git command output into a Seed-owned repository-state record.
- Preserve repository state fields relevant to read-only status display or policy audit.
- Preserve read-only event/cluster mutation flags as fields.
- Intentionally discard raw git stdout, individual porcelain status filenames, exact staged/modified status codes, full remote names/URLs, and all git metadata not represented by the dataclass.

Why not directly `Observation`?

The repository-state provider returns `RepositoryObservation`, and helper functions format or JSON-serialize it. The reviewed implementation does not route this repository-state record through `ObservationCollectionService` or `ObservationIngestor` as canonical observations.

Why not provider-native representation?

The native representation is git CLI text. The implementation converts it into stable fields and counts instead of preserving raw command output.

## Implementation similarities

Across the strongest examples, the intermediate structures perform a recurring bounded responsibility:

1. They sit after provider-native acquisition/decoding and before either canonical `Observation` emission or downstream evidence/reconciliation consumption.
2. They replace provider-native wire formats, source text, AST nodes, or command stdout with Seed-owned structural fields.
3. They preserve source identity or location information: package manager/name, source path, repository path, relationship path, artifact path, symbol, or parent symbol.
4. They preserve narrow evidence appropriate to their surface: package version/architecture, relationship evidence text, artifact fact text, repository-state counts.
5. They intentionally discard provider-specific internals that are not needed by the next Seed boundary.
6. They carry negative semantic boundaries: package observations do not infer services/processes/vulnerabilities; relationship facts do not prove behavior/ownership/runtime reachability; repository artifact facts do not recover responsibility or mutate state; repository observations preserve read-only mutation flags.

The best-supported recurring role is therefore not ownership, not an artifact abstraction, and not provider redesign. It is **bounded structural evidence shaping**: implementation-local records normalize provider-native material into Seed-owned structural evidence while preserving enough identity, provenance, and evidence to support later observation or reconciliation boundaries.

## Implementation differences and counterexamples

The evidence is not uniform enough to claim a single formal abstraction.

- `PackageRecord` feeds canonical `Observation` emission directly through `package_records_to_observations(...)`.
- `RelationshipFact` feeds canonical `Observation` emission in `RepositorySourceObservationSource`, but also exists as a relationship evidence primitive usable outside that source.
- `RepositoryArtifactFact` is not shown in the reviewed code as an input to `ObservationCollectionService`; self-model alignment consumes it as a supplied acquisition-side fact record.
- `RepositoryObservation` is a repository-state display/policy-audit record and is not the canonical `Observation` ingestion shape.
- `SystemdObservationSource` is a counterexample to universal staging: it decodes systemctl JSON rows into dictionaries and directly emits canonical `Observation` instances inside the source class, without a named dataclass analogous to `PackageRecord` or `RelationshipFact`.
- Observation normalizers are downstream of canonical observations. They derive additional canonical observations from existing observations and projected state; they are not provider-native-to-structural-record adapters.

These counterexamples prevent a stronger conclusion that every provider currently distinguishes provider-native representation, implementation-local structural record, and canonical `Observation`.

## Answers to central questions

### 1. What recurring implementation role do the intermediate structures fulfill?

They perform bounded structural evidence shaping between provider-native material and later Seed boundaries. They decode or extract from provider-native material, preserve a small Seed-owned structural record, and discard raw/provider-specific detail before canonical observation emission, display/policy use, or self-model reconciliation.

### 2. Which provider-specific details are intentionally removed?

- Dpkg: all status fields except package name, installed status, version, architecture, and manager; non-installed/malformed/missing-identity records are skipped.
- Python relationship extraction: AST nodes, full source text, implementation bodies, behavior/call/route/runtime/ownership meanings.
- Repository artifact extraction: AST internals, bodies, nested implementation detail beyond the tiny supported set, architectural interpretation, ownership, lexicon authority, runtime integration, mutation.
- Git repository state: raw stdout, filenames/status-code granularity from porcelain output, remote details beyond presence, and broader git metadata.

### 3. Which structural information is intentionally preserved?

- Package identity and package-manager scope: name, manager, installed state, version, architecture.
- Relationship structure: relationship kind, subject, object, path, evidence.
- Repository artifact structure: artifact kind, path, symbol, parent symbol, evidence text.
- Repository state structure: repository path, VCS, head commit, branch, dirty flag, status counts, remote presence, status availability, read-only mutation flags.

### 4. Why are these structures not canonical Observations?

They do not have the canonical observation shape required by `ObservationCollectionService` and `ObservationIngestor`: `subject`, `predicate`, `value`, `source_type`, `observed_at`, metadata, dimensions, and confidence. Where they feed ingestion, a separate mapping step creates canonical observations. In other paths, they are consumed directly as evidence/reconciliation or display/policy records rather than by observation ingestion.

### 5. Does implementation evidence support a shared recurring responsibility?

Yes, with medium confidence. Multiple unrelated paths show implementation-owned structural records that sit between provider-native material and later Seed boundaries. However, evidence does not support a universal provider architecture or a formal abstraction because some sources directly emit observations and some intermediate records do not feed canonical observation ingestion.

### 6. If so, what implementation vocabulary best characterizes that responsibility?

The best implementation-backed vocabulary is **implementation-local structural evidence record** or **bounded structural evidence shaping**. This vocabulary reflects what the code does: preserve bounded structure and evidence from provider-native material while avoiding semantic promotion to ownership, behavior, architecture meaning, or cluster truth.

## Supported conclusions

- Current implementation distinguishes provider-native representation from implementation-local structural records in several places.
- `PackageRecord`, `RelationshipFact`, `RepositoryArtifactFact`, and `RepositoryObservation` are Seed-owned records, not provider-native wire formats.
- At least two reviewed paths (`PackageRecord` and `RelationshipFact` through `RepositorySourceObservationSource`) show a structural-record-to-canonical-`Observation` transition.
- `RepositoryArtifactFact` and `RepositoryObservation` show the same structural-record pattern but not the same canonical observation-ingestion path.
- The recurring work is bounded structural evidence shaping, not ownership recovery or artifact abstraction.

## Unsupported conclusions

- The implementation does not support claiming a universal provider pipeline for all observation sources.
- The implementation does not support introducing a new artifact abstraction from this evidence alone.
- The implementation does not support treating `RepositoryArtifactFact` as canonical `Observation`.
- The implementation does not support treating `RepositoryObservation` as canonical `Observation`.
- The implementation does not support claims that intermediate records prove behavior, ownership, runtime reachability, service health, desired state, or capability authority.

## Confidence

Medium.

Confidence is high that the named structures are not provider-native representations and not canonical observations. Confidence is high that they preserve bounded structural evidence. Confidence is medium, not high, for a shared recurring responsibility because the paths differ in downstream consumers and because counterexamples such as `SystemdObservationSource` directly emit canonical observations without a named intermediate dataclass.

## Recommended next investigation

Investigate whether downstream consumers depend on these intermediate structures as evidence records independently of canonical observation ingestion. Specifically, review where `RepositoryArtifactFact`, `RelationshipFact`, `PackageRecord`, and `RepositoryObservation` are imported or consumed by tests, CLI surfaces, audits, and reconciliation helpers. The goal should be dependency evidence only: identify whether consumers rely on the structural-record boundary, not whether a new abstraction should be introduced.

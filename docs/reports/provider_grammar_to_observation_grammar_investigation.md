# Provider Grammar to Observation Grammar Investigation

## Scope

This is a bounded implementation investigation of whether current implementation already distinguishes a recurring transition from provider-native grammar, to Seed-owned structural grammar, to canonical `Observation` grammar. It does not recover ownership, introduce abstractions, redesign providers, or recommend implementation changes.

## Implementation evidence reviewed

- `seed_runtime/local_packages.py`: `PackageRecord`, `parse_dpkg_status`, and `package_records_to_observations`.
- `seed_runtime/knowledge/relationship_observation.py`: `RelationshipFact` and Python/documentation relationship extraction helpers.
- `seed_runtime/knowledge/repository_observation.py`: `RepositoryArtifactObservationAdapter` and `RepositoryArtifactFact` construction.
- `seed_runtime/knowledge/self_model_alignment.py`: `RepositoryArtifactFact` shape and fixture-level reconciliation boundary.
- `seed_runtime/repository_observation.py`: `RepositoryObservation` and `GitRepositoryObservationProvider`.
- `seed_runtime/observations.py`: canonical `Observation`, `ObservationIngestor`, evidence conversion, and fact conversion.
- `seed_runtime/observation_sources.py`: `ObservationSource`, `RepositorySourceObservationSource`, `PrometheusObservationSource`, `SystemdObservationSource`, and `ObservationCollectionService`.
- `seed_runtime/observation_normalizers.py`: canonical-observation normalization pipeline.
- Previous investigation: `provider_representation_to_observation_investigation.md`.

## Short answer

Yes, implementation evidence supports a recurring but not universal transition equivalent to:

```text
provider-native grammar
↓
Seed-owned implementation-local structural grammar
↓
canonical Observation grammar
```

The strongest supported cases are dpkg package status, Python source relationships, Python repository artifacts, and git repository state. The conclusion must be bounded: Prometheus and systemd show provider decoding directly into canonical observations or provider-shaped helper dictionaries, not a fully separate intermediate structural record. Therefore the recurring transition is present as an implementation pattern, but it is not a uniform runtime observation architecture.

## Provider vocabularies

### dpkg status text

The provider-native vocabulary is dpkg status database text: records, fields, continuation lines, and specific field names such as `Package`, `Status`, `Version`, and `Architecture`. `parse_dpkg_status` splits blank-line-delimited records, parses colon-delimited fields, supports continuation lines, requires `Package` and `Status`, and only accepts `Status: install ok installed`.

Provider concepts present here include dpkg record shape, arbitrary dpkg fields, dpkg status strings, malformed-record handling, and the specific dpkg database location later recorded as `/var/lib/dpkg/status`.

### Python source / AST for relationships

The provider-native vocabulary is Python source text plus Python AST nodes. The relationship adapter explicitly supports static Python `import`, `from ... import ...`, function definitions, async function definitions, and class definitions. The provider grammar includes AST node classes such as `ast.Import`, `ast.ImportFrom`, `ast.FunctionDef`, `ast.AsyncFunctionDef`, and `ast.ClassDef`, import aliases, module names, node line ranges, and source paths.

### Python source / AST for repository artifacts

The provider-native vocabulary is again caller-provided Python source text and Python AST nodes. The artifact adapter parses text with `ast.parse`, treats syntax failure as parse failure, and examines top-level class definitions, function definitions, async function definitions, imports, from-imports, and direct class methods.

### git command output

The provider-native vocabulary is git command behavior and stdout text: `rev-parse --is-inside-work-tree`, `rev-parse HEAD`, `branch --show-current`, `remote`, and `status --porcelain=v1`. The porcelain grammar includes `??` for untracked files and the two status columns used as staged and worktree indicators.

### Prometheus HTTP API JSON

The provider-native vocabulary is Prometheus HTTP API JSON for allowlisted instant queries: `status`, `data.resultType`, `data.result`, vector samples, `metric` labels, `value` arrays, `instance`, `job`, `nodename`, query names, sample timestamps, and sample values. This path has provider-native validation and selection, but it does not introduce a separate dataclass equivalent to `PackageRecord` or `RelationshipFact` before `Observation`.

### systemd JSON command output

The provider-native vocabulary is `systemctl --output=json` stdout decoded as JSON rows with provider keys such as `unit`, `UNIT`, `active`, `ACTIVE`, `sub`, `SUB`, `unit_file`, `UNIT FILE`, `state`, and `STATE`. This path converts rows into dictionaries keyed by unit name but does not introduce a separate provider-neutral structural dataclass.

## Intermediate vocabularies

### `PackageRecord`

`PackageRecord` is explicitly described as normalized package evidence independent of package-manager wire format. Its vocabulary is Seed-owned and package-structural: `name`, `manager`, `installed`, `version`, and `architecture`. This is not a copy of dpkg records. It removes most dpkg fields and converts the dpkg-specific `Status: install ok installed` string into the boolean `installed=True` plus a fixed `manager="dpkg"`.

Provider concepts intentionally removed before observation include arbitrary dpkg fields, raw record order, continuation formatting, non-installed status records, malformed records, package manager operational state, repository source, locks, services, capabilities, ports, vulnerabilities, and patch status. The observation metadata explicitly marks many of those as not inferred.

### `RelationshipFact`

`RelationshipFact` has structural vocabulary: `relationship_kind`, `subject`, `object`, `path`, and `evidence`. The module describes it as a language-neutral relationship evidence record and states that Python import extraction is only the first adapter emitting it. That is a vocabulary shift from Python AST grammar into Seed relationship vocabulary such as `imports` and `defines`.

Provider concepts intentionally removed include AST node identity, import alias syntax details beyond selected names, execution behavior, calls, routes, boundaries, ownership, reachability, capability authority, and runtime ownership. The module states these negative boundaries directly: import relationships are dependency/name-availability evidence only, and definition relationships are syntactic declaration evidence only.

### `RepositoryArtifactFact`

`RepositoryArtifactFact` vocabulary is repository-artifact structural vocabulary: `fact`, `artifact_kind`, `path`, `symbol`, and `parent_symbol`. The adapter turns Python parsing results into module, class, function, method, and import facts. It emits a module/file fact even on syntax failure, preserving bounded existence while refusing richer parse-derived claims.

Provider concepts intentionally removed include AST object identity, AST full tree shape, decorators, arguments, function bodies, control flow, comments, runtime imports, execution behavior, architecture, ownership, and responsibility recovery. The adapter boundary explicitly says it works only on caller-provided text, does not read files, scan repositories, import modules, use LLMs, reconcile claims, or integrate with runtime/tool execution. Its boundary also marks `interprets_content=False`, `owns_responsibility_recovery=False`, and `owns_lexicon=False`.

### `RepositoryObservation`

`RepositoryObservation` vocabulary is repository-state structural vocabulary: repository path, VCS, head commit, branch, dirty boolean, untracked/modified/staged counts, remote presence, status availability, reason, and mutation flags. Git provider grammar is reduced from multiple command outputs and porcelain lines into selected state fields and counts.

Provider concepts intentionally removed include raw git stdout, filenames in status output, exact porcelain status pairs per file, stderr, return codes after availability decisions, remote names/URLs, and git command provenance beyond the structural result. Authority is bounded with `writes_event_ledger=False` and `mutates_cluster=False` defaults.

## Canonical Observation vocabulary

Canonical `Observation` introduces another distinct vocabulary. It is not dpkg-shaped, AST-shaped, git-shaped, Prometheus-shaped, or systemd-shaped. It uses `id`, `source_type`, `observed_at`, `subject`, `predicate`, `value`, `confidence`, `metadata`, `dimensions`, and optional `expires_at`. `ObservationSource` requires sources to return `list[Observation]`, and `ObservationCollectionService` validates that collected items are `Observation` instances before normalization and ingestion.

The canonical vocabulary first becomes possible at the points where source adapters or helper functions instantiate `Observation`:

- dpkg package records become observations in `package_records_to_observations`.
- relationship facts become observations in `RepositorySourceObservationSource._relationship_observation`.
- Prometheus samples become observations inside `PrometheusObservationSource._observations_from_query` without a separate intermediate structural dataclass.
- systemd unit dictionaries become observations in `SystemdObservationSource.collect` through `_observation`.
- `RepositoryObservation` is a diagnostic/recordable structural result, not shown in the reviewed runtime path as an `ObservationSource.collect() -> list[Observation]` source.
- `RepositoryArtifactFact` is a self-model/reconciliation structural fact surface, not shown in the reviewed runtime path as canonical `Observation` ingestion.

After canonical `Observation` exists, `ObservationIngestor` converts it to evidence and optionally to fact. Evidence preserves observation payload fields under an observation source string; facts map `Observation.subject` to `Fact.subject_id`, `Observation.predicate` to `Fact.predicate`, and `Observation.value` to `Fact.value`.

Normalization happens after canonical observations exist. The normalization pipeline accepts and returns `Observation` instances, retains originals, and appends unique derived observations. It therefore operates within canonical Observation grammar rather than between provider grammar and intermediate grammar.

## Authority transitions

### dpkg packages

Authority decreases from dpkg database record text to installed-package evidence. `parse_dpkg_status` only carries forward installed records and selected package identity/version/architecture fields. `package_records_to_observations` records read-only local metadata and explicitly denies package-manager CLI calls, repository inspection, lock inspection, service inference, capability inference, process inference, port inference, vulnerability inference, and patch-status inference. Canonical observation then carries a host subject, generic package predicates, package dimensions, and provenance metadata; it does not carry dpkg record authority as cluster truth.

### Python relationships

Authority decreases from Python source/AST to relationship evidence. The AST can support many claims, but the implementation carries forward only `imports` and `defines` style structural relationships. It explicitly forbids behavior, calls, routes, boundaries, ownership, invocation, reachability, capability authority, runtime ownership, repository scanning, imports of repository modules, LLM reconciliation, graph building, and runtime/tool integration. Canonical observation then carries only subject/predicate/value plus evidence/path metadata.

### Python repository artifacts

Authority decreases from parsed Python source to bounded artifact existence facts. The adapter can see AST structure but intentionally emits only module/file, class, function, method, and import artifacts. It refuses content interpretation, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, and cluster mutation. Syntax failure further reduces authority to only a module/file fact.

### git repository state

Authority decreases from git command execution and porcelain grammar to selected repository-state fields. The implementation keeps counts and booleans, not raw per-file status or remote details. The resulting record is read-only by default and marks no event-ledger writes and no cluster mutation.

### Prometheus and systemd counterexamples

Prometheus does reduce provider authority by allowlisting safe queries, validating vector responses, selecting labels and values, recording source/sample timestamps, and suppressing fact promotion for endpoint-scoped `node_uname_info` OS observations. However, provider JSON decoding, identity selection, and canonical `Observation` construction remain compressed inside one source class. No distinct intermediate structural grammar is evident.

Systemd also reduces authority by emitting unit existence and unit state observations while explicitly denying service health, desired state, operator intent, and ownership assertions. But the intermediate dictionaries remain provider-shaped rather than a separate Seed-owned structural record. This is a counterexample to a universal three-stage implementation grammar shift.

## Answers to the central questions

### 1. Do the intermediate structures preserve a different implementation vocabulary than their providers?

Yes, in the strongest reviewed cases. `PackageRecord` replaces dpkg record/field/status grammar with normalized package evidence. `RelationshipFact` replaces Python AST grammar with relationship evidence vocabulary. `RepositoryArtifactFact` replaces Python AST grammar with artifact kind/path/symbol vocabulary. `RepositoryObservation` replaces git stdout and porcelain grammar with repository-state fields and mutation flags.

No, or not enough, for all sources. Prometheus constructs canonical observations directly from validated provider payloads. Systemd constructs observations after provider-shaped helper dictionaries, not after a distinct structural dataclass.

### 2. Does canonical `Observation` introduce another distinct vocabulary?

Yes. Canonical `Observation` introduces source type, observation time, subject, predicate, value, confidence, metadata, dimensions, and expiration. The collection service requires source adapters to emit this shape, normalizers operate on this shape, and ingestion converts this shape into evidence and facts. That vocabulary is distinct from both provider grammar and the reviewed intermediate records.

### 3. Which provider concepts are intentionally discarded before Observation?

- dpkg: non-installed records, malformed records, arbitrary package fields, raw record syntax, and operational implications such as repositories, locks, services, capabilities, processes, ports, vulnerabilities, and patch state.
- Python relationships: AST node objects, full syntax trees, execution behavior, calls, routes, boundaries, ownership, invocation, reachability, capability authority, and runtime ownership.
- Python artifacts: full AST detail, code bodies, behavior, architecture, ownership, responsibility, lexicon claims, and repository mutation authority.
- git: raw command output, raw porcelain lines, filenames, exact per-file status, remote names/URLs, and command stderr/return-code details after availability handling.
- Prometheus: arbitrary PromQL, non-vector responses, malformed samples, missing instances, and some endpoint-scoped authority through fact-promotion suppression.
- systemd: service health, desired state, operator intent, and ownership assertions.

### 4. Which concepts survive into canonical Observation?

The surviving concepts are selected identity, bounded structural relation, selected measured or declared value, time/provenance, confidence, and dimensions:

- dpkg: host subject, package name, package manager, installed/version/architecture predicates, package dimensions, source file and adapter metadata.
- Relationships: subject module identity, relationship kind as predicate, object symbol/module, source path dimension, textual evidence metadata.
- Prometheus: endpoint or instance subject, selected metric-derived predicates, sample value, sample time, selected labels in metadata.
- Systemd: host subject, unit dimension, unit name, active/sub/unit-file state values, read-only/source metadata.
- Canonical ingestion: subject/predicate/value/dimensions/confidence/observed_at survive into fact creation when fact promotion is not suppressed.

### 5. Does implementation evidence support recurring transitions between implementation grammars?

Yes, but boundedly. The recurrence is supported where separate records or adapters exist: dpkg text to `PackageRecord` to `Observation`; Python source/AST to `RelationshipFact` to `Observation`; Python source/AST to `RepositoryArtifactFact` as a structural fact surface; git stdout/porcelain to `RepositoryObservation` as a structural record. These are recurring transformations from provider-native grammar into Seed-owned structural vocabulary with reduced authority.

The evidence does not support claiming this is a universal observation architecture. Prometheus and systemd retain compressed provider-decoding and observation-construction paths.

### 6. Does implementation evidence show authority reduction during those transitions?

Yes. Authority reduction is explicit and repeated: `PackageRecord` only represents installed package evidence; relationship extraction forbids behavior, ownership, and reachability claims; repository artifact extraction refuses content interpretation, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, and cluster mutation; repository state observation preserves read-only mutation flags; systemd metadata denies health, desired-state, intent, and ownership assertions; Prometheus suppresses some endpoint-scoped fact promotion.

The authority decrease is from provider-native expressiveness and operational context to bounded structural evidence, then to canonical observations that are source-attributed reports, not automatically complete truth.

## Supported conclusions

1. Current implementation already contains multiple implementation-local structural grammars before canonical Observation exists.
2. Those structures are not merely provider-field copies in the strongest cases; they select, rename, normalize, and discard provider-native concepts.
3. Canonical `Observation` is a distinct grammar with `subject`/`predicate`/`value` plus provenance, dimensions, confidence, and time.
4. The recurring behavior is better described as bounded translation from provider-native representation into Seed-owned structural evidence, followed in some runtime paths by canonical Observation construction.
5. Authority reduction is implementation-backed: many provider-native meanings are explicitly filtered, suppressed, or marked as not inferred.

## Unsupported conclusions

1. The implementation does not support a claim that every provider follows a clean three-stage pipeline.
2. The implementation does not support introducing a formal grammar abstraction; no such abstraction is required or currently present in the reviewed code.
3. The implementation does not support treating `RepositoryArtifactFact` or `RepositoryObservation` as canonical `Observation` ingestion paths in the reviewed runtime source interface.
4. The implementation does not support ownership recovery from these intermediate records. Several modules explicitly forbid ownership or responsibility inference.
5. The implementation does not support treating presentation vocabulary as repository knowledge without separate implementation evidence.

## Confidence

Medium-high for the bounded conclusion that recurring implementation-local structural grammar shifts exist in several areas. Confidence is high for dpkg packages and Python relationship extraction because the transition points and negative authority boundaries are explicit. Confidence is medium for repository artifacts and repository state because they clearly show structural shaping, but they are not both shown as canonical runtime `ObservationSource.collect()` paths. Confidence is low for a universal provider-to-observation grammar model because Prometheus and systemd are concrete counterexamples.

## Recommended next investigation

Investigate where, if anywhere, `RepositoryArtifactFact` and `RepositoryObservation` cross into the canonical observation/evidence/fact pipeline, and whether their current consumers treat them as acquisition records, fixture facts, diagnostic records, or projected knowledge inputs. This should remain evidence-only and should not introduce ownership recovery or grammar abstractions.

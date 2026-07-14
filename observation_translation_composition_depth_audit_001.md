# Observation Translation and Composition Depth Audit 001

## 1. Bounded questions

This audit asks what responsibility converts bounded external or substrate-shaped representations into Seed-readable observation grammar, and how far Seed should decompose an observer before lower implementation detail stops contributing useful operational resolution.

The inspected transition is:

```text
external or substrate grammar
-> bounded translation
-> Seed-native observation grammar
```

The audit is bounded to three representative paths only:

1. Prometheus HTTP/JSON -> canonical `Observation`.
2. Git command output -> `RepositoryObservation`.
3. Caller-supplied Python source text -> `RepositoryArtifactFact`.

No implementation, refactor, test, provider, evidence, or canonical `Observation` behavior was changed.

## 2. Governing orientation

The operator testimony tested here is:

```text
Shell or another acquisition mechanism
-> acquires an external signal

Observation translator
-> converts that signal into bounded Seed-native grammar

Observation
-> may later become preserved evidence

Evidence
-> may later support facts, capability verification, selection, or reliance
```

And:

```text
acquisition
!= decoding
!= translation
!= observation construction
!= evidence preservation
!= fact promotion
```

Repository evidence supports the distinction as an analysis vocabulary, but not as one universal implementation class or interface. The inspected implementations frequently compress several responsibilities inside one owner while still exposing enough internal seams to recover the acquisition/decoding/translation/construction/evidence boundary.

## 3. Composition-depth rule

Tested stopping discipline:

> Seed should preserve the highest stable boundary sufficient for the current bounded inquiry and descend only when a lower layer becomes independently meaningful.

A lower layer warrants explicit visibility when repository evidence shows reuse, independent verification, replaceability, distinguishable failure, material resource effect, separate authority or security boundary, independent existence, or direct bounded-inquiry relevance.

This audit does not descend merely because implementation code calls a library, subprocess, parser, HTTP client, JSON decoder, AST walker, Git internal storage mechanism, or compression algorithm.

## 4. Methodology

Read-only repository inspection was performed with focused `rg` probes, direct source inspection, and focused test inspection. The audit classified responsibility from implementation bodies and tests rather than search output alone.

Focused probes executed:

```bash
rg -n "PrometheusObservationSource|RepositoryObservation|GitRepositoryObservationProvider|RepositoryArtifactObservationAdapter|StructureObservation" seed_runtime tests
rg -n "json.loads|urlopen|subprocess.run|ast.parse|Observation\\(" seed_runtime tests
rg -n "evidence.observed|ObservationIngestor|fact.observed|fact.inferred" seed_runtime tests
```

Representative source bodies inspected:

- `seed_runtime/observation_sources.py`
- `seed_runtime/observations.py`
- `seed_runtime/repository_observation.py`
- `seed_runtime/knowledge/repository_observation.py`
- `seed_runtime/structure_observation.py`
- `seed_runtime/knowledge/self_model_alignment.py`
- `seed_runtime/fact_extraction.py`

Focused tests inspected:

- `tests/test_observation_sources.py`
- `tests/test_repository_observation.py`
- `tests/test_structure_observation.py`
- `tests/test_observations.py`
- `tests/test_event_batching.py`
- `tests/test_fact_extraction.py`

## 5. Inspected neighborhoods

The relevant implementation neighborhoods were:

| Neighborhood | Reason inspected |
| --- | --- |
| `seed_runtime/observation_sources.py` | Prometheus acquisition, JSON validation, decoded sample shaping, canonical `Observation` construction, collection service references. |
| `seed_runtime/observations.py` | Canonical `Observation`, `ObservationIngestor`, observation-to-evidence, observation-to-fact, event emission. |
| `seed_runtime/repository_observation.py` | Git-backed repository-state acquisition, subprocess execution, porcelain decoding, `RepositoryObservation` construction, unavailable preservation. |
| `seed_runtime/knowledge/repository_observation.py` | Python source AST parsing, structural artifact fact construction, adapter boundary testimony. |
| `seed_runtime/structure_observation.py` | Substrate-independent structure observation boundary and explicit refusal of substrate parsing/grammar ownership. |
| `seed_runtime/knowledge/self_model_alignment.py` | `RepositoryArtifactFact` record shape and downstream reconciliation consumer. |
| `seed_runtime/fact_extraction.py` | Counterevidence that some evidence production records tool output only without fact inference. |

## 6. Terminology

- **Acquisition**: obtaining bytes, text, records, or signals from an external subject.
- **External grammar decoding**: recognizing provider- or substrate-native representation such as Prometheus JSON, Git porcelain output, or Python AST.
- **Observation translation**: selecting and shaping bounded content that crosses into Seed grammar: subject, predicate or relation, value, dimensions, source attribution, time, vantage, confidence, scope, limitations, negative/unavailable result.
- **Observation construction**: constructing canonical `Observation` or another bounded observation-like artifact.
- **Evidence preservation**: preserving translated content with provenance for later consumers.
- **Interpretation**: inferring meaning, architecture, responsibility, truth, ownership, authority, or intention beyond explicit translated content.

## 7. Prometheus responsibility trace

### Implemented topology

```text
Prometheus HTTP endpoint
-> PrometheusObservationSource.collect()
-> _query(query)
-> urllib Request + urlopen GET
-> response bytes decoded as UTF-8
-> json.loads(...)
-> Prometheus response validation: object/status/data/resultType/result
-> _prometheus_decoded_sample(sample)
-> PrometheusDecodedSample(metric, instance, sample timestamp, raw timestamp, value)
-> metadata shaping
-> _prometheus_observation_shapes(query, decoded, metadata)
-> PrometheusObservationShape(observed_at, subject, predicate, value, metadata)
-> PrometheusObservationSource._observation(...)
-> canonical Observation
-> ObservationCollectionService / ObservationIngestor when collected through service
-> observation.observed + evidence.observed + optional fact.observed/fact.inferred events
```

### Required trace

| Field | Prometheus path |
| --- | --- |
| External subject | Prometheus HTTP API under configured `base_url`, limited to allowlisted query names. |
| Acquisition owner | `PrometheusObservationSource._query` builds a GET `Request` and calls `urlopen`; `collect` orchestrates the allowlisted query loop. |
| Raw representation | HTTP response bytes expected to contain Prometheus API JSON. |
| Decoder | UTF-8 decode plus `json.loads`; `_query` validates Prometheus response envelope; `_prometheus_decoded_sample` decodes sample shape. |
| Intermediate artifact | `PrometheusDecodedSample` and `PrometheusObservationShape`. |
| Translator | `_prometheus_observation_shapes`, with metadata shaping in `_observations_from_query`; `_filesystem_dimensions` maps selected labels into dimensions during construction. |
| Translated artifact | `PrometheusObservationShape`, then canonical `Observation`. |
| Observation constructor | `PrometheusObservationSource._observation`. |
| Evidence consumer | `ObservationIngestor.observation_to_evidence`, invoked through ingestion. |
| Fact/projection consumer | `ObservationIngestor.observation_to_fact` unless fact promotion is suppressed; `StateProjector` consumes emitted events in tests. |
| Provenance preserved | collector, source name, base URL, metric, labels, read-only flag, HTTP method, Prometheus sample timestamp and raw timestamp, source time authority, Seed collection time and authority, query temporal intent. |
| Uncertainty preserved | confidence fixed to `0.95`; invalid individual samples are skipped; provider or transport failure is retained only as `last_error`, not as a canonical negative `Observation`. |
| Failure behavior | `_query` raises for disallowed query, transport/HTTP/JSON/shape failures; `collect` catches selected failures, sets `last_error`, returns `[]`, and does not emit negative observations. Invalid samples return `None` and are skipped. |
| Read-only or mutating | Read-only; metadata includes `read_only=True`; GET-only allowlist. |
| Event-ledger behavior | Source collection alone does not write the ledger. Ingestion emits `observation.observed`, `evidence.observed`, and optional fact events. |
| Authority explicitly refused | Arbitrary PromQL is refused; source comments state only `node_uname_info` is authoritative for stable host identity, while other metrics remain endpoint-scoped. OS observations for endpoint subjects suppress fact promotion in tested behavior. |
| Deepest required implementation boundary | HTTP GET/query allowlist, JSON response validation, vector/sample decoding, sample-time handling, identity/predicate/dimension shaping, canonical `Observation` construction, ingestion boundary. Lower HTTP transport internals and Prometheus storage/query engine internals are opaque. |

### Compressed owner

`PrometheusObservationSource` is the clearest compressed ownership boundary among the inspected paths. It owns acquisition, provider response validation, sample decoding, translation into provider-local shapes, canonical `Observation` construction, read-only authority limitation, counters, and failure reporting. It does not itself preserve evidence; evidence begins at ingestion.

## 8. Git repository-state responsibility trace

### Implemented topology

```text
repository path
-> GitRepositoryObservationProvider.observe(repository_path)
-> Path.expanduser().resolve()
-> shutil.which(git_binary)
-> git rev-parse --is-inside-work-tree
-> git rev-parse HEAD
-> git branch --show-current
-> git remote
-> git status --porcelain=v1
-> subprocess.run([...], cwd=path, text=True, capture_output=True, check=False)
-> stdout/stderr/returncode boundary hidden by _git_text return value
-> porcelain status splitlines and two-column XY decoding
-> RepositoryObservation(...)
```

### Required trace

| Field | Git repository-state path |
| --- | --- |
| External subject | A filesystem path that may or may not be a Git work tree. |
| Acquisition owner | `GitRepositoryObservationProvider.observe` selects commands; `_git_text` executes subprocesses. |
| Raw representation | Git command stdout, stderr, and exit status. Only stdout and returncode are materially retained by helpers; stderr is captured but discarded. |
| Decoder | `_git_ok` decodes `rev-parse --is-inside-work-tree`; `observe` decodes command text; status porcelain v1 lines are decoded by line prefixes and XY columns. |
| Intermediate artifact | No explicit decoded-status dataclass; command text is translated directly into `RepositoryObservation` fields. |
| Translator | `GitRepositoryObservationProvider.observe` selects fields and maps Git outputs into repository-state record fields. |
| Translated artifact | `RepositoryObservation`. |
| Observation constructor | `RepositoryObservation(...)` dataclass construction inside `observe` or `_unavailable`. |
| Evidence consumer | None in this path. `RepositoryObservation` is consumed as context by snapshot policy/history helpers and CLI JSON formatting, not by `ObservationIngestor`. |
| Fact/projection consumer | Snapshot policy audit/history consumers use it as read-only repository context; it is not promoted to canonical `Fact` through `ObservationIngestor`. |
| Provenance preserved | Resolved repository path, VCS value, head commit, branch, dirty flag, staged/modified/untracked counts, remote-present boolean, status-available flag, reason on unavailability, `writes_event_ledger=False`, `mutates_cluster=False`. |
| Uncertainty preserved | Unknown/unavailable values are preserved as `None`; availability is explicit as `repository_status_available`; reason strings preserve coarse failure cause. |
| Failure behavior | Missing Git, non-work-tree, command `OSError`/`ValueError`, nonzero command return, missing head/status all become non-fatal unavailable records. |
| Read-only or mutating | Read-only Git commands; tests assert CLI observation does not change head and reports no ledger write/cluster mutation. |
| Event-ledger behavior | None; record explicitly carries `writes_event_ledger=False`. |
| Authority explicitly refused | Does not mutate repository or cluster; does not write event ledger; does not claim canonical `Observation` status. |
| Deepest required implementation boundary | Git executable availability, subprocess execution, command selection, stdout/returncode handling, porcelain v1 status grammar, unknown preservation. Git object database, packfiles, delta compression, filesystem internals, and subprocess implementation internals are opaque. |

### Artifact classification

`RepositoryObservation` is not canonical `Observation`: it lacks canonical fields such as `id`, `source_type`, `observed_at`, `subject`, `predicate`, `value`, `confidence`, and dimensions. It is a bounded read-only repository-state record and contextual translated artifact. It is parallel to canonical `Observation`, not upstream of it in the inspected implementation, because no inspected caller converts it into canonical `Observation` or ingests it as evidence.

## 9. Python repository-artifact responsibility trace

### Implemented topology

```text
caller-supplied source_path + Python source text
-> RepositoryArtifactObservationAdapter.extract(source_path, text)
-> module fact emitted before parsing
-> ast.parse(text, filename=source_path)
-> on SyntaxError: module fact with parse_failed wording only
-> AST top-level traversal
-> class/function/async function/import/import-from/method selection
-> RepositoryArtifactFact records
-> self-model alignment reconcile_claims(...) may consume supplied artifact facts
```

### Required trace

| Field | Python repository-artifact path |
| --- | --- |
| External subject | Caller-supplied Python source text and caller-supplied source path. |
| Acquisition owner | Caller. Module docstring explicitly says the adapter never reads files or scans repositories. |
| Raw representation | Python source text plus path string. |
| Decoder | `ast.parse` decodes Python syntax into an AST. |
| Intermediate artifact | Python AST returned by `ast.parse`; not preserved as Seed artifact. |
| Translator | `RepositoryArtifactObservationAdapter.extract` and helper functions select structural elements and shape records. |
| Translated artifact | `RepositoryArtifactFact` records. |
| Observation constructor | Helper functions `_module_fact`, `_class_fact`, `_function_fact`, `_method_fact`, `_import_fact`. |
| Evidence consumer | None directly; adapter boundary states preserves evidence, but this path emits fixture-level structural records rather than appending ledger evidence. |
| Fact/projection consumer | `reconcile_claims` consumes supplied `RepositoryArtifactFact` records for self-model alignment. |
| Provenance preserved | `source_path`, artifact kind, symbol, parent symbol, and human-readable structural fact string. |
| Uncertainty preserved | Syntax failure is preserved by returning only a module/file fact with parse-failure wording; no exception escapes for parse failure. |
| Failure behavior | `SyntaxError` yields a bounded module-only fact with parse-failure text. Non-syntax exceptions are not specially caught. |
| Read-only or mutating | Read-only; boundary says no repository mutation, no cluster mutation, no event-ledger writes. |
| Event-ledger behavior | None. |
| Authority explicitly refused | No file reads, repository scans, imports, LLMs, reconciliation, runtime/tool execution, architecture/ownership inference, responsibility recovery, lexicon ownership, repository mutation, or cluster mutation. |
| Deepest required implementation boundary | Caller-provided text boundary, Python parsing, AST top-level traversal, structural record construction, syntax failure preservation. Python parser internals, tokenization mechanics, bytecode, import resolution, and runtime semantics remain opaque. |

### Pure translator assessment

This path is already the cleanest acquisition/translation separation. Acquisition is caller-owned; the adapter starts with already supplied text, decodes with `ast.parse`, translates a narrow structural subset, and constructs records. It is not pure in the sense of translation-only because it also decodes Python AST and constructs records, but it is pure relative to acquisition and runtime side effects.

## 10. Producer/artifact/consumer tables

### Path table

| Path | Producer | Artifact or handoff | Consumer |
| --- | --- | --- | --- |
| Prometheus | `PrometheusObservationSource._query` / `_observations_from_query` / `_observation` | HTTP JSON -> `PrometheusDecodedSample` -> `PrometheusObservationShape` -> canonical `Observation` | `ObservationCollectionService` and `ObservationIngestor`; state projection after events. |
| Git | `GitRepositoryObservationProvider.observe` | Git stdout/status -> `RepositoryObservation` | CLI formatting/JSON and snapshot/history repository context consumers. |
| Python artifact | `RepositoryArtifactObservationAdapter.extract` | caller text -> AST -> `RepositoryArtifactFact` | Self-model alignment reconciliation and tests. |

### Responsibility table

| Responsibility | Prometheus | Git | Python artifact |
| --- | --- | --- | --- |
| Acquisition | Source-owned HTTP GET | Provider-owned subprocess | Caller-owned text supply |
| Decoding | JSON + Prometheus envelope + sample | Git command stdout + porcelain | `ast.parse` + AST traversal |
| Translation | Provider-local shape mapping | Provider maps Git fields into repository state | Adapter maps AST nodes to structural facts |
| Canonical `Observation` construction | Yes | No | No |
| Evidence production | Only after ingestion | None | None |
| Fact promotion | Ingestion may produce facts; some observations suppress promotion | None | Not runtime facts; fixture structural records feed reconciliation |
| Mutation | No cluster/repository mutation; source collection no ledger writes | No ledger/repository/cluster mutation | No ledger/repository/cluster mutation |

## 11. External grammar topology

| Path | External grammar entering path | Seed grammar after translation | External syntax discarded |
| --- | --- | --- | --- |
| Prometheus | Prometheus HTTP JSON API envelope and vector sample grammar | `Observation` with Seed subject/predicate/value/dimensions/metadata/time/confidence | HTTP bytes, JSON object nesting, Prometheus field names except selected metadata, list ordering beyond emitted observation order, PromQL envelope. |
| Git | Git command stdout and porcelain v1 status grammar | `RepositoryObservation` fields | Raw command text formatting, stderr text, per-file paths, porcelain line ordering, most Git command envelope details. |
| Python artifact | Python source syntax and AST node grammar | `RepositoryArtifactFact` structural records | Source code text, token ordering beyond selected top-level order, function/class bodies except direct method names, decorators, annotations, docstrings, import aliases beyond selected names. |

## 12. Translation-preservation analysis

### Preserved content

| Content | Prometheus | Git | Python artifact |
| --- | --- | --- | --- |
| Subject/identity | Prometheus instance, endpoint/nodename metadata for selected metric, filesystem labels as dimensions. | Resolved repository path and VCS. | Source path, symbol, parent symbol. |
| Reported relation/value | Predicate/value observations. | Branch, commit, dirty, counts, remote presence, availability. | Artifact kind and existence statements. |
| Source provenance | Collector/source name/base URL/metric/labels/HTTP method/read-only/time authority. | Path, Git VCS, availability reason; not exact commands in record. | Path and structural fact; caller identity is not preserved. |
| Time | Prometheus sample timestamp and Seed collection time; canonical observed_at uses source sample time. | No observation time field. | No observation time field. |
| Vantage/scope | Provider source, base URL, endpoint, allowlisted current instant query; filesystem dimensions for series. | Resolved repository path; local Git view. | Caller-supplied source path and text scope. |
| Confidence/uncertainty | Confidence 0.95; skipped invalid samples; last_error on collection failure. | `None` unknowns, status availability, reason. | Parse failure text in module fact. |
| Authority limits | Query allowlist, endpoint-scoped identity caveat, read-only metadata. | No ledger writes, no cluster mutation. | No file read, no imports, no LLMs, no inference, no mutation. |
| Negative evidence/failure | Collection returns [] with `last_error`; invalid samples skipped. | Unavailable records with reasons. | Parse failure represented in returned fact. |

### Lawfully changed representation

All three paths discard substrate-specific envelope and syntax after selected content crosses into Seed-shaped records. Prometheus field names and JSON nesting become predicates, dimensions, metadata, and confidence. Git command formatting becomes repository-state fields. Python syntax becomes structural artifact records.

## 13. Observation versus intermediate artifact analysis

| Artifact | Canonical `Observation`? | Role |
| --- | --- | --- |
| `Observation` | Yes | Canonical external observation convertible to evidence and facts through `ObservationIngestor`. |
| `PrometheusDecodedSample` | No | Provider-local decoded sample before translation. |
| `PrometheusObservationShape` | No | Provider-local translation shape immediately upstream of canonical `Observation`. |
| `RepositoryObservation` | No | Parallel bounded read-only repository-state record/context; not ingested as canonical observation in inspected path. |
| `RepositoryArtifactFact` | No | Structural record used by self-model alignment; not canonical runtime fact and not emitted through `ObservationIngestor`. |

Another artifact exists where canonical `Observation` would either overfit or erase substrate-specific boundaries. `RepositoryObservation` preserves repository-state availability and unknowns without pretending to be subject/predicate/value evidence. `RepositoryArtifactFact` is a deterministic structural fixture record used by alignment rules and keeps acquisition and runtime evidence out of scope.

## 14. Acquisition/translation distinction

- Prometheus compresses acquisition and translation in `PrometheusObservationSource`, though helper dataclasses expose internal decoding and shape seams.
- Git compresses command selection, subprocess acquisition, decoding, and record construction in `GitRepositoryObservationProvider`, with `_git_text` as a small acquisition helper.
- Python artifact separates acquisition from translation: text is caller-supplied, and the adapter explicitly refuses file reads and repository scans.

The term `observer` currently names several responsibilities depending on substrate. It may mean acquirer, decoder, translator, observation constructor, projection/context builder, or orchestrator. Repository evidence does not support treating the name as one precise implementation role today.

## 15. Observer naming analysis

| Inspected name | Classification | Naming assessment |
| --- | --- | --- |
| `PrometheusObservationSource` | acquirer, decoder, translator, observation constructor, orchestrator | Accurate as a source of observations, but hides the material boundary between HTTP acquisition and Seed translation because one class owns both. |
| `PrometheusDecodedSample` | decoder artifact | Accurate; explicitly provider-local decoded sample. |
| `PrometheusObservationShape` | translator intermediate / observation-shape artifact | Accurate; explicitly before `Observation` emission. |
| `RepositoryObservationProvider` | orchestrator/protocol-like provider | Broad but acceptable; base name does not distinguish acquisition/translation. |
| `GitRepositoryObservationProvider` | acquirer, decoder, translator, bounded record constructor | Accurate enough for read-only repository observation, but hides subprocess acquisition and Git grammar translation inside provider. |
| `RepositoryObservation` | translated bounded record / read-only context | Potentially ambiguous because it is not canonical `Observation`; material risk is mitigated by distinct dataclass fields and formatter/JSON functions. |
| `StructureObservationBoundary` | constitutional/shared boundary for structure observation | Accurate; it explicitly refuses substrate parsing and grammar ownership. |
| `RepositoryArtifactObservationAdapter` | decoder, translator, structural record constructor | Accurate; “adapter” reflects substrate-specific conversion from caller-provided text to records and does not claim acquisition. |
| `RepositoryArtifactFact` | structural record / alignment input | Potentially ambiguous with runtime `Fact`, but module testimony describes fixture-level self-model alignment records. |
| `ObservationIngestor` | evidence producer, fact producer, event producer | Accurate; it appends observation, evidence, and fact events while preserving provenance. |
| `FactExtractionService` | evidence producer from tool-result events | Name is historically broad; implementation records evidence only and explicitly does not infer facts. |

No broad renaming is recommended by this audit. The only material hidden ownership boundaries are Prometheus and Git acquisition/translation compression.

## 16. Shared responsibility comparison

| Similarity | Classification | Evidence |
| --- | --- | --- |
| Selecting bounded substrate content and shaping Seed-readable records | Recurring pattern only, implementation-backed strongly enough to name as “Observation Translation” in audit vocabulary | All three paths select limited content, assign identity/relation/value or record fields, and discard external envelope. |
| One shared implementation owner | Insufficient evidence / counterevidence | Prometheus emits canonical `Observation`; Git emits repository context; Python emits structural records under `Structure Observation` substrate adapter boundary. |
| Shared constitutional responsibility | Partially supported for structural observations only | `StructureObservationBoundary` owns substrate-independent structural extraction but explicitly refuses substrate parsing and grammar ownership. |
| Shared implementation responsibility | Not supported across all three | No shared translator interface/base/registry handles these paths. |
| Incidental similarity | Not sufficient alone | All parse something, but parsing alone is not the audited translation responsibility. |

There is one recurring Observation Translation responsibility in the sense of implementation-backed behavior: conversion of bounded substrate representation into Seed-readable observation grammar. It is not already an explicit shared implementation responsibility and does not require a single shared owner.

## 17. Composition-depth analysis

### Prometheus

Current inquiry: observe allowlisted Prometheus metrics as Seed observations.

Highest sufficient boundary: Prometheus HTTP/JSON observation translation.

Relevant realization detail: GET allowlist, JSON envelope validation, vector sample decoding, sample timestamp handling, identity/predicate/value/dimension shaping, confidence, read-only provenance, fact-promotion suppression for endpoint OS identity.

Opaque lower detail: HTTP socket mechanics, TLS internals, Prometheus storage engine, query planner, scrape pipeline internals, JSON parser internals.

Evidence pressure for deeper descent: distinct transport authority boundary, authentication/TLS provenance, provider-side freshness correctness, materially different timeout/retry behavior, sample staleness semantics, payload-size/resource constraints, or need to distinguish acquisition failure from translation failure as observations.

### Git

Current inquiry: observe repository branch, commit, dirty state, counts, remote presence, and unavailable status.

Highest sufficient boundary: Git repository-state translation.

Relevant realization detail: Git executable availability, subprocess execution, command selection, stdout/returncode handling, porcelain v1 decoding, unavailable record construction.

Opaque lower detail: Git object database, packfiles, delta compression, refs storage formats, index internals beyond porcelain status, subprocess kernel internals.

Evidence pressure for deeper descent: need to verify object integrity, distinguish staged/index mechanics beyond count fields, preserve stderr/error codes, support non-Git VCS providers, replace subprocess acquisition, or prove repository mutation/security boundaries more specifically.

### Python artifact

Current inquiry: extract bounded structural artifact facts from caller-provided Python source text.

Highest sufficient boundary: Python repository-artifact structural translation from caller text.

Relevant realization detail: caller-supplied path/text, AST parse boundary, top-level AST traversal, structural fact construction, parse-failure preservation.

Opaque lower detail: Python tokenizer/parser internals, grammar production mechanics, import resolution, bytecode/runtime semantics, filesystem acquisition.

Evidence pressure for deeper descent: need to preserve exact syntax spans, decorators, annotations, nested definitions, aliases, parse diagnostics, caller provenance, or support non-Python substrates under a comparable record contract.

## 18. Highest sufficient boundary for each path

| Path | Highest sufficient boundary |
| --- | --- |
| Prometheus | Prometheus HTTP/JSON observation source translating allowlisted vector samples into canonical `Observation`. |
| Git | Git repository-state provider translating selected Git command outputs into `RepositoryObservation`. |
| Python artifact | Repository artifact adapter translating caller-supplied Python text into structural `RepositoryArtifactFact` records. |

## 19. Opaque lower boundaries

| Path | Lower detail remaining opaque |
| --- | --- |
| Prometheus | Prometheus server internals, metric scrape pipeline, query planner, HTTP stack internals, JSON parser internals. |
| Git | Object storage, packfiles, compression/delta algorithms, refs/index internals not exposed by porcelain output, OS process internals. |
| Python artifact | Parser/tokenizer internals, runtime/import semantics, bytecode generation, filesystem reads. |

## 20. Conditions warranting deeper decomposition

Deeper decomposition would be warranted if a lower layer becomes independently meaningful by repository evidence. Examples include:

- A lower layer is reused by multiple observation capabilities.
- Tests independently verify lower-layer behavior.
- Acquisition becomes replaceable independently from translation.
- Failure behavior must distinguish transport, provider, grammar, translation, or construction failures.
- Memory, time, storage, power, or payload size materially affects the observation contract.
- A separate authority/security boundary appears, such as credentialed HTTP or untrusted subprocess execution.
- The lower layer can exist without the higher capability and is consumed directly.
- The bounded inquiry explicitly requires lower-layer provenance.

## 21. Strongest counterevidence

1. **Provider-specific boundaries are real.** Prometheus, Git, and Python source have different external grammars, failure modes, and authority limits. A shared abstraction could erase substrate-specific boundaries if it forced uniform fields or lifecycle.
2. **Canonical `Observation` does not own all translation semantics.** Prometheus translation partly occurs before construction in `PrometheusDecodedSample` and `PrometheusObservationShape`; Git and Python never emit canonical `Observation` in inspected paths.
3. **Structure Observation explicitly refuses substrate parsing and grammar ownership.** This supports a shared constitutional boundary for read-only structural extraction while preserving substrate adapter ownership.
4. **`RepositoryObservation` and `RepositoryArtifactFact` are not canonical observations.** They serve context/alignment roles without event-ledger ingestion, confidence fields, or observed-at fields.
5. **Translation is not merely incidental parsing.** Parsing/decoding is necessary but not sufficient; content selection, identity shaping, unknown preservation, and authority limits are separately implemented.
6. **Some evidence production intentionally avoids fact inference.** `FactExtractionService` records tool output as evidence only and explicitly does not infer facts without explicit mapping, showing preservation can stop before fact promotion.
7. **Lower algorithmic layers do not currently affect the contract.** No inspected path requires Git compression, Prometheus storage internals, or Python parser internals to explain authority or failure boundaries.

## 22. Preserved Unknowns

| Path | Preserved unknown/failure |
| --- | --- |
| Prometheus | Source-level `last_error` on collection failure; invalid samples skipped; unavailable provider returns no observations. This is weaker than Git/Python because negative provider failure is not emitted as an observation. |
| Git | Explicit `repository_status_available=False`, `reason`, and `None` fields for unknown branch/commit/dirty/count/remote state. |
| Python artifact | Syntax failure represented by a module/file fact whose text states parsing failed and only module/file fact was emitted. |

## 23. Supported conclusions

- Observation Translation is recurring and implementation-backed across the three inspected paths.
- It is currently compressed into substrate-specific observers/providers/adapters rather than represented by one shared implementation owner.
- Prometheus and Git compress acquisition with translation.
- The Python repository-artifact adapter already separates acquisition from translation because it accepts caller-supplied text and refuses filesystem/repository acquisition.
- Canonical `Observation` is one lawful translated artifact, but not the only bounded observation-like artifact used by Seed.
- Observation becomes evidence at `ObservationIngestor.observation_to_evidence` and event emission, not at source collection.
- Composition depth differs lawfully by substrate: Prometheus needs HTTP/JSON/sample layers; Git needs subprocess/Git porcelain layers; Python artifact needs caller text/AST traversal layers.

## 24. Unsupported conclusions

- That Seed should add a shared translator interface, base class, registry, or acquisition abstraction now.
- That every observer must be decomposed.
- That `RepositoryObservation` should become canonical `Observation`.
- That `RepositoryArtifactFact` should become runtime `Fact` or ledger evidence.
- That Prometheus provider failures should be emitted as negative observations without a separate implementation decision.
- That lower mechanical layers such as Git packfiles, DEFLATE, LZ77, Huffman coding, HTTP socket internals, or Python parser internals affect the current observation contract.
- That translation authorizes architecture, ownership, responsibility, or intention inference.

## 25. Primary classification

B. Observation Translation is a recurring implementation-backed responsibility currently compressed inside substrate-specific observers.

## 26. Composition-depth classification

4. Composition depth differs lawfully by substrate.

## 27. Exact next bounded boundary

Selected current path: Prometheus.

Compressed responsibility boundary: HTTP acquisition/provider validation and Seed observation translation are both owned by `PrometheusObservationSource`.

Producer: `PrometheusObservationSource._query` and `_observations_from_query`.

Artifact or handoff: provider JSON payload -> `PrometheusDecodedSample` -> `PrometheusObservationShape` -> canonical `Observation`.

Consumer: `PrometheusObservationSource._observation`, then `ObservationCollectionService`/`ObservationIngestor` when collected through the service.

Exact bounded question: should Prometheus provider acquisition/validation failure be represented only as source-local `last_error` and empty observation list, or as a bounded negative/unavailable observation with preserved provenance and non-mutating evidence behavior?

## 28. Implementation-warrant decision

No implementation warranted.

The next boundary is exact enough to support a future slice, but this audit itself does not warrant immediate implementation because the requested work is an audit, current behavior is tested, and a change would alter provider failure semantics.

## 29. Files changed

- Added `observation_translation_composition_depth_audit_001.md`.

No implementation files or tests were changed.

## 30. Probes/tests executed

Read-only probes executed:

```bash
rg -n "PrometheusObservationSource|RepositoryObservation|GitRepositoryObservationProvider|RepositoryArtifactObservationAdapter|StructureObservation" seed_runtime tests
rg -n "json.loads|urlopen|subprocess.run|ast.parse|Observation\\(" seed_runtime tests
rg -n "evidence.observed|ObservationIngestor|fact.observed|fact.inferred" seed_runtime tests
```

Focused implementation and tests were inspected directly after the probes. No mutating observation command was run and no event ledger was appended.

Diff guardrail commands to run before commit:

```bash
git diff --stat
git diff --numstat
git status --short
```

## 31. Confidence statement

Confidence is moderate-high. The three requested representative paths were inspected through implementation bodies and focused tests. The strongest remaining uncertainty is not about the inspected paths themselves but about whether future, uninspected observation sources would support the same recurring translation vocabulary. This audit intentionally does not generalize beyond the three bounded paths except to name a recurring responsibility pattern supported by these implementations.

# Provider Language Translation Responsibility Characterization

## Scope

This is a bounded implementation characterization of the existing **Provider Language Translation** owner. It does not recover a new ownership boundary, normalize providers, introduce a provider model, or recommend behavior/schema/ledger changes.

Representative providers reviewed:

- dpkg local package status translation.
- Python relationship extraction.
- Prometheus HTTP API metric translation.
- systemd `systemctl --output=json` translation.
- Local host stdlib/file translation, including its delegation to dpkg and systemd.

## Executive conclusion

Provider Language Translation currently owns the bounded work of turning provider-local language into Seed observation-facing language. In the implementation reviewed, that recurring work includes:

1. selecting a bounded provider vocabulary;
2. validating or rejecting provider grammar enough to avoid unsafe or malformed translation;
3. decoding provider grammar into provider-local or normalized structures;
4. preserving provider identity and provider evidence in subjects, dimensions, values, and metadata;
5. assigning Seed predicates where translation reaches observation construction;
6. constructing canonical `Observation` objects in providers that have not separated an intermediate record;
7. keeping provider-local helper functions close to provider vocabulary when translation details remain provider-specific.

Not every provider performs all of those responsibilities in one place. Dpkg and Python relationship extraction already separate decoded intermediate records (`PackageRecord`, `RelationshipFact`) from final observation emission. Prometheus, systemd, and much of local host translation keep identity shaping, predicate assignment, metadata preservation, and observation construction compressed inside source classes or helper methods.

The smallest implementation-backed next ownership boundary is **insufficiently supported for recovery in this task**. Predicate assignment and identity shaping recur across providers, but they are not yet similarly separated across multiple independent provider families; their current shapes differ by provider vocabulary and evidence boundaries. The family should stop at characterization until additional implementation evidence appears.

## Responsibility matrix

| Provider | Vocabulary selected | Grammar validated | Decoding performed | Identity preservation | Predicate assignment | Canonical observation construction | Visibility status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dpkg | Installed package records and package fields: package name, manager, version, architecture. | Dpkg records must contain `Package` and `Status`; only `Status: install ok installed` is accepted. | Dpkg status text is split/parsed into `PackageRecord`. | Host remains observation subject; package identity is preserved in dimensions and values; source adapter/file and read-only metadata are preserved. | Package predicates are assigned during `PackageRecord` to `Observation` conversion. | Occurs in `package_records_to_observations`, not in `parse_dpkg_status`. | Decoding and observation emission are already visibly separated. |
| Python relationship extraction | Python import/from-import syntax and top-level definitions; relationship kinds such as `imports` and `defines`. | `ast.parse` validates syntax; invalid Python returns no facts. | Python source text/AST is decoded into `RelationshipFact`. | Source path is shaped into dotted subject identity; path and evidence are preserved on each fact and later metadata. | Relationship kind is assigned before observation construction and mapped directly to observation predicate later. | Occurs in `RepositorySourceObservationSource._relationship_observation`, not in the extractor. | Identity shaping and relationship-kind assignment are already separated from final observation construction. |
| Prometheus | Fixed allowlist: `up`, `node_uname_info`, `node_filesystem_avail_bytes`, `node_filesystem_size_bytes`. | Query allowlist, HTTP JSON object status, vector result type, list result, sample dict/metric/value shape, instance presence, timestamp parseability. | Prometheus JSON vectors and sample arrays are decoded directly while constructing observations. | `instance` is the subject; `node_uname_info` preserves `instance`/`nodename`; metric labels, timestamps, base URL, method, and filesystem labels are metadata/dimensions. | Metric names are mapped to Seed predicates such as `endpoint_role`, `up`, `os`, and filesystem byte predicates inside `_observations_from_query`. | Occurs in `PrometheusObservationSource._observation`. | Translation, identity shaping, predicate assignment, metadata shaping, and observation construction remain compressed. |
| systemd | Runtime unit identity, active state, substate, and unit-file state from two `systemctl` JSON commands. | JSON must decode to a list; entries must be dicts; unit/state fields must be non-empty strings. Command failures return no observations. | JSON rows become provider-shaped runtime unit and unit-file-state dictionaries. | Host is observation subject; unit name is value/dimension/metadata. Read-only and non-interpretation metadata are preserved. | systemd fields map to `systemd_unit`, `systemd_active_state`, `systemd_sub_state`, `systemd_unit_file_state` in `collect`. | Occurs in `SystemdObservationSource._observation`. | JSON-row parsing is visible, but provider dictionaries, predicate assignment, and observation construction remain compressed in the source. |
| local host | Python/platform/os/shutil values, local files under `/proc`, `/sys`, `/etc`, plus delegated dpkg/systemd surfaces. | Validation varies by helper: path read bounds, file presence, string extraction, stdlib values, delegated provider validation. | Mostly direct stdlib/file values to observations; dpkg and systemd subpaths delegate to narrower translators. | Hostname is selected from `platform.node`, local identity, or `localhost`; uname and local-only/read-only metadata are preserved. | Local host predicates such as `local_observation_status`, `os`, `architecture`, disk predicates, and many helper-specific predicates are assigned in `collect`/helpers. | Occurs through local host `_observation` helpers and delegated sources. | Mixed: package/systemd delegation is visible; many local host translations remain compressed. |

## Provider evidence

### dpkg local packages

`seed_runtime.local_packages` explicitly states that package observation emission is generic while dpkg status parsing is isolated as the first narrow package adapter. The implementation-owned decoded record is `PackageRecord`, described as normalized package evidence independent of package-manager wire format. `parse_dpkg_status` accepts only records whose `Status` is `install ok installed`, skips malformed or incomplete records, and emits `PackageRecord` instances with name, manager, version, and architecture. `package_records_to_observations` then builds observations, preserving package identity in dimensions, source adapter/file metadata, and read-only/non-inference flags while assigning package predicates.

Implementation-visible responsibilities:

- Vocabulary selection: installed dpkg package fields only.
- Grammar validation: record fields plus exact installed status.
- Grammar decoding: dpkg text to `PackageRecord`.
- Identity preservation: package name/manager in dimensions; host as subject.
- Metadata preservation: dpkg source adapter, source file, read-only flags, non-inference flags.
- Predicate assignment: package predicates in the generic package observation conversion.
- Observation construction: separated from parsing.

Counterexample value: dpkg shows that Provider Language Translation does not always construct observations directly. The dpkg parser stops at `PackageRecord`; observation construction happens later.

### Python relationship extraction

`seed_runtime.knowledge.relationship_observation` states that `RelationshipFact` is the language-neutral relationship evidence record and that Python import extraction is the first adapter emitting it. The module limits itself to caller-provided source text and static Python syntax; it does not read files, scan repositories, import repository modules, use LLMs, reconcile claims, build graphs, or integrate with runtime/tool execution. The import and definition extractors parse Python with `ast.parse`, return an empty list on invalid syntax, shape subjects from source paths, inspect top-level import/from-import/function/class nodes, and emit `RelationshipFact` records. `RepositorySourceObservationSource` later maps `RelationshipFact.subject` to observation subject, `relationship_kind` to predicate, `object` to value, and preserves path/evidence in metadata.

Implementation-visible responsibilities:

- Vocabulary selection: Python imports, from-imports, top-level function/async function/class definitions.
- Grammar validation: Python AST parse; invalid Python yields no relationship facts.
- Grammar decoding: AST nodes to `RelationshipFact`.
- Identity shaping: source path to dotted subject before fact construction.
- Predicate assignment: relationship kind is assigned in `RelationshipFact`; repository source maps it to observation predicate.
- Metadata preservation: source path and evidence preserved into observation metadata.
- Observation construction: separated into repository source observation mapping.

Counterexample value: identity shaping and predicate assignment are already partly separated from observation construction. This argues against treating observation construction as universally owned by Provider Language Translation.

### Prometheus

`PrometheusObservationSource` selects a fixed safe query vocabulary and rejects non-allowlisted query names. `_query` performs HTTP GET, decodes JSON, and validates that the payload is an object with success status, vector data, and list results. `_observations_from_query` then performs sample-level grammar checks, requires a string `instance`, parses sample timestamps, preserves metric labels and source timing metadata, treats `node_uname_info` specially for stable host identity metadata, maps metric families to Seed predicates, and constructs observations through `_observation`. Filesystem dimensions are derived from Prometheus metric labels only for filesystem predicates.

Implementation-visible responsibilities:

- Vocabulary selection: fixed metric allowlist.
- Grammar validation: HTTP JSON/vector/sample shape validation.
- Grammar decoding: vector samples, labels, sample timestamp/value parsing.
- Identity preservation: `instance` as subject; `nodename`/`instance` metadata only where authoritative.
- Metadata preservation: labels, metric name, base URL, HTTP method, sample time, collection time.
- Predicate assignment: metric-specific mapping inside `_observations_from_query`.
- Observation construction: direct through `_observation`.

Compressed responsibilities: Prometheus keeps decoding, identity shaping, metadata shaping, predicate assignment, dimension derivation, and observation construction in the source class. No separate neutral Prometheus record is visible.

### systemd

`SystemdObservationSource` records only systemd-reported unit identity, runtime state, substate, and unit-file enablement state; its docstring explicitly excludes health, ownership, intent, dependencies, and desired state interpretation. The source calls `systemctl list-units` and `systemctl list-unit-files` with JSON output. `_systemd_json_rows` decodes JSON and keeps dict entries only. `_collect_runtime_units` and `_collect_unit_file_states` accept lower/upper provider keys and shape provider dictionaries keyed by unit name. `collect` selects a host subject, preserves unit identity in dimensions/metadata, maps runtime fields to Seed predicates, and constructs observations.

Implementation-visible responsibilities:

- Vocabulary selection: unit identity, active state, substate, unit-file state.
- Grammar validation: command failure boundary; JSON list/dict filtering; string stripping.
- Grammar decoding: JSON rows to provider-shaped runtime/unit-file dictionaries.
- Identity preservation: host subject and unit dimension/value/metadata.
- Metadata preservation: read-only/local-only/systemd surface and non-interpretation flags.
- Predicate assignment: systemd-specific mapping in `collect`.
- Observation construction: direct through `_observation`.

Compressed responsibilities: systemd has visible JSON-row parsing but no neutral unit record. Provider dictionaries, identity shaping, predicate assignment, and observation construction remain inside the source.

### local host

`LocalHostObservationSource` is a broad read-only local source. It uses process-local stdlib/platform/os/shutil values and local files, assembles metadata asserting read-only/local-only/no network/no privilege escalation, selects a hostname from `platform.node`, collected hostname, or `localhost`, directly emits identity, OS, architecture, and disk observations, and delegates packages and systemd to narrower translation paths. Its dpkg subpath reads bounded status text and then calls `parse_dpkg_status` and `package_records_to_observations`; its systemd subpath delegates to `SystemdObservationSource.collect`.

Implementation-visible responsibilities:

- Vocabulary selection: mixed local host vocabulary selected by helper methods and direct stdlib/file surfaces.
- Grammar validation: varied and helper-local; not one provider grammar.
- Grammar decoding: direct stdlib/file values in many paths; delegated decoding for dpkg and systemd.
- Identity preservation: host subject selection; uname metadata; local/read-only flags.
- Predicate assignment: many local predicates assigned inline or by helper methods.
- Observation construction: direct for many host facts; delegated for dpkg/systemd.

Counterexample value: local host is not one coherent provider grammar. It is an orchestration surface over multiple local vocabularies; parts are already delegated, while other parts remain compressed.

## Recurring translation responsibilities

The following responsibilities recur across multiple independent providers and are therefore currently implementation-owned by Provider Language Translation as a family-level characterization.

### 1. Bounded provider vocabulary selection

Every reviewed provider limits the vocabulary it translates:

- dpkg selects installed package fields.
- Python selects import and top-level definition syntax.
- Prometheus selects a safe metric allowlist.
- systemd selects unit identity/runtime/substate/unit-file state.
- local host selects read-only stdlib/file surfaces and delegates dpkg/systemd sub-vocabularies.

This is a consistent Provider Language Translation responsibility.

### 2. Provider grammar validation before translation

Validation recurs, but its mechanism is provider-specific:

- dpkg validates required fields and exact installed status.
- Python validates AST parseability.
- Prometheus validates allowlisted query names, JSON/vector shape, sample shape, instance strings, and timestamps.
- systemd validates command success at collection boundary and JSON list/dict/string shape.
- local host validates through file-bounded reads, string checks, stdlib availability, and delegated provider checks.

Validation belongs to Provider Language Translation, but no generic grammar engine is supported.

### 3. Provider grammar decoding

Each provider decodes provider-local representation into something closer to Seed observation language:

- dpkg text becomes `PackageRecord`.
- Python source/AST becomes `RelationshipFact`.
- Prometheus JSON vectors are decoded inline into observation fields.
- systemd JSON rows become provider-shaped dictionaries.
- local host values are decoded directly or delegated.

Decoding is recurring, but the decoded artifact varies.

### 4. Provider identity preservation and shaping

Translation consistently decides how provider identity survives:

- dpkg preserves package identity in dimensions while host remains subject.
- Python shapes source path into relationship subject.
- Prometheus uses `instance` as subject and treats `nodename` as metadata only for `node_uname_info`.
- systemd uses host as subject and unit as dimension/value/metadata.
- local host selects host identity and preserves uname/local metadata.

Identity shaping recurs, but is tightly provider-specific.

### 5. Provider metadata preservation

Each provider carries provider evidence or boundary metadata forward:

- dpkg stores source adapter/file and non-inference flags.
- Python stores source path/evidence.
- Prometheus stores metric labels, metric name, timestamps, base URL, and HTTP method.
- systemd stores observation surface, unit, and non-interpretation flags.
- local host stores local/read-only/no-network/no-privilege metadata.

This is consistently recurring and implementation-backed.

### 6. Seed predicate assignment where translation reaches observation construction

Predicate assignment recurs wherever provider translation reaches observations:

- dpkg package records map to package predicates.
- Python relationship kinds become observation predicates in repository source mapping.
- Prometheus metric names map to endpoint, OS, and filesystem predicates.
- systemd fields map to systemd predicates.
- local host stdlib/file facts map to local predicates.

Predicate assignment is recurring, but its mapping tables are provider-specific and currently not uniformly separated.

### 7. Observation construction where no intermediate boundary exists

Observation construction is recurring in compressed providers but not universal:

- Prometheus and systemd construct observations directly.
- local host constructs many observations directly.
- dpkg parsing does not construct observations; generic package conversion does.
- Python extraction does not construct observations; repository source mapping does.

Therefore, observation construction is a current Provider Language Translation responsibility only for compressed provider paths, not a universal architectural responsibility.

## Provider-specific responsibilities that should not become architectural families yet

These are implementation details, not supported ownership families:

- Prometheus HTTP API mechanics, metric allowlist, vector result validation, `node_uname_info` identity semantics, filesystem label dimensions, and sample timestamp semantics.
- systemd command invocation, lower/upper JSON key compatibility, unit-file-state merging, and explicit non-interpretation of health/ownership/intent.
- dpkg exact status string semantics and status-file field names.
- Python AST node coverage, dotted module subject shaping, and top-level-only definition extraction.
- local host aggregation of heterogeneous stdlib, `/proc`, `/sys`, `/etc`, package, and systemd surfaces.

These details recur only within their provider or sub-provider. They should remain provider-local unless another independent implementation develops the same bounded work shape.

## Recurring implementation patterns

1. **Provider language is bounded before decoding.** Providers do not accept arbitrary PromQL, arbitrary Python semantics, arbitrary package-manager records, or arbitrary systemd interpretation.
2. **Malformed provider input is skipped or returns no observations.** The common behavior is safe non-emission rather than speculative inference.
3. **Translation preserves evidence provenance.** Provider source names, paths, labels, units, timestamps, and non-inference flags are carried into metadata/dimensions.
4. **Seed predicate assignment occurs at the provider-to-observation edge.** The edge may be direct (`Prometheus`, `systemd`, local host) or mediated by records (`PackageRecord`, `RelationshipFact`).
5. **Intermediate records appear only where bounded work has already separated.** `PackageRecord` and `RelationshipFact` are implementation evidence; Prometheus/systemd/local host do not justify universal intermediate records.
6. **Observation construction is not the definition of the owner.** Some provider translation stops before `Observation`, while compressed providers include observation construction.

## Supported answers to the central questions

### 1. Which implementation responsibilities consistently belong to Provider Language Translation?

Consistently supported responsibilities are bounded vocabulary selection, provider grammar validation, provider grammar decoding, provider identity preservation, provider metadata preservation, and provider-to-Seed predicate assignment where an observation-facing edge exists.

Observation construction belongs to Provider Language Translation only in compressed provider paths. It is not consistent across all reviewed providers because dpkg and Python relationship extraction have earlier implementation-visible records before canonical observation construction.

### 2. Which responsibilities vary by provider?

The validation grammar, decoded artifact, identity shape, metadata vocabulary, predicate mapping, and final construction site vary by provider. Dpkg decodes to `PackageRecord`; Python decodes to `RelationshipFact`; Prometheus decodes vectors inline; systemd decodes JSON rows to provider dictionaries; local host mixes direct translation and delegation.

### 3. Which recurring responsibilities appear ready for ownership recovery?

None are ready for recovery in this bounded task. Identity shaping and predicate assignment recur, but they are not yet independently separated across multiple provider families in the same implementation-local way. Dpkg and Python show separated artifacts, but their artifacts are package-specific and relationship-specific, not evidence for a shared next boundary. Prometheus and systemd remain compressed in ways that differ by provider vocabulary.

### 4. Which apparent responsibilities are provider-specific and should not become architectural families?

Prometheus metric semantics, systemd unit-state semantics, dpkg status semantics, Python AST relationship semantics, and local host file/stdlib surface handling are provider-specific. They are responsibilities of the provider translation implementations, not separate architectural families.

### 5. What is the smallest implementation-backed next ownership boundary, if any?

Insufficient implementation evidence.

The strongest candidates are identity shaping and predicate assignment, but the implementation does not yet show a recurring, separated, implementation-local responsibility across multiple independent provider families. The supported next action is to stop at this characterization and wait for additional code evidence rather than recover another ownership slice.

## Unsupported conclusions

The reviewed implementation does not support these conclusions:

- That all providers should emit universal intermediate records.
- That Provider Language Translation owns a generic grammar engine.
- That Prometheus, systemd, dpkg, Python, and local host should be normalized into a common provider model.
- That observation construction is always inside Provider Language Translation.
- That identity shaping or predicate assignment is ready to become a new ownership boundary now.
- That provider-specific vocabularies should be promoted into architecture families.

## Confidence

Confidence: **medium-high**.

Reason: the reviewed providers show strong evidence for recurring bounded vocabulary, validation, decoding, identity/metadata preservation, and predicate assignment. Confidence is lower for recommending any next slice because the existing separations are uneven: dpkg and Python have intermediate records, while Prometheus/systemd/local host still compress several responsibilities differently.

## Recommended next ownership slice

Insufficient implementation evidence.

Do not recover another ownership boundary yet. Continue allowing provider-local artifacts to emerge from separated bounded work. Revisit only when at least two independent provider families show the same implementation-local responsibility separated from acquisition, decoding, predicate mapping, and observation construction without forcing a generic provider model.

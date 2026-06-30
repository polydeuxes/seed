# Provider Language Translation Slice 001

## Selected architectural boundary

Recovered boundary: **Provider Language != Provider Language Translation**.

The recurring implementation-local owner is **Provider Language Translation**: given a provider-native language or decoded provider-native representation, produce the bounded Seed-side translation input required by the next Seed output step.

This slice does **not** recover an intermediate-record family. The reviewed providers show that bounded translation can produce different Seed-side artifacts:

- `PackageRecord`, later consumed by package observation emission.
- `RelationshipFact`, later consumed by repository source observation emission.
- directly emitted `Observation` instances for compressed providers such as Prometheus and systemd.
- non-canonical Seed artifacts in other paths, such as repository-state observation records.

The common ownership is the bounded translation work, not a mandatory record shape.

## Implementation evidence

### dpkg

`seed_runtime.local_packages` separates dpkg status parsing from generic package observation emission. Its module docstring states that package observation emission remains generic while dpkg status parsing is isolated as the first narrow package adapter. `parse_dpkg_status(...)` consumes dpkg status database text, applies dpkg vocabulary such as `Status: install ok installed`, and returns only installed `PackageRecord` values. `package_records_to_observations(...)` separately converts those records into canonical package observations.

Evidence:

- Provider language: dpkg status database text.
- Translation work: `_split_dpkg_records(...)`, `_parse_dpkg_record(...)`, status filtering, and field selection inside `parse_dpkg_status(...)`.
- Bounded translation input: `PackageRecord`.
- Seed-language consumer: `package_records_to_observations(...)`.

### Python relationship extraction

`seed_runtime.knowledge.relationship_observation` keeps Python syntax handling inside bounded extraction helpers. `extract_python_import_relationship_facts(...)` and `extract_python_definition_relationship_facts(...)` parse caller-provided Python source text with `ast.parse(...)`, inspect only supported top-level syntax, and emit `RelationshipFact` records. The module explicitly limits import relationships to dependency/name-availability evidence and definition relationships to syntactic declaration evidence.

Evidence:

- Provider language: Python source text and Python AST nodes.
- Translation work: static AST parsing and supported syntax extraction.
- Bounded translation input: `RelationshipFact`.
- Seed-language consumer: `RepositorySourceObservationSource.collect(...)`, which maps relationship facts to canonical `Observation` instances.

### Prometheus

`PrometheusObservationSource` keeps Prometheus-provider language bounded by an allowlist of safe metric names and validated vector API payload shape. `_query(...)` owns Prometheus HTTP API validation. `_observations_from_query(...)` consumes Prometheus metric labels, sample timestamps, and sample values, then emits Seed observations with metric-specific predicates and metadata.

Evidence:

- Provider language: allowlisted Prometheus query names plus Prometheus vector JSON payloads.
- Translation work: payload validation, metric label handling, sample timestamp parsing, sample-value parsing, and metric-specific observation mapping.
- Bounded translation input: no recurring intermediate artifact is produced; the compressed translation terminates in canonical `Observation` instances.
- Seed-language consumer: the observation collection path consumes the emitted observations directly.

### systemd

`SystemdObservationSource` keeps systemd-provider language bounded to `systemctl` JSON machine output. `_collect_runtime_units(...)` and `_collect_unit_file_states(...)` decode systemd rows into dictionaries keyed by unit name. `collect(...)` then emits only systemd unit identity, active state, substate, and unit-file state observations. The class docstring explicitly excludes health, ownership, intent, dependencies, and desired-state interpretation.

Evidence:

- Provider language: `systemctl list-units --output=json` and `systemctl list-unit-files --output=json` rows.
- Translation work: JSON row decoding, unit-name normalization, runtime-state selection, and unit-file-state selection.
- Bounded translation input: no recurring intermediate artifact is produced; decoded dictionaries are local to the source.
- Seed-language consumer: `SystemdObservationSource.collect(...)` consumes those dictionaries while constructing canonical observations.

## Before

Provider language and Provider Language Translation were previously mixed inside provider/source helpers:

- dpkg parsing and package record production happened inside `parse_dpkg_status(...)`, while the file already separated the later package observation emission step.
- Python parsing and relationship fact production happened inside relationship extraction helpers.
- Prometheus query execution, vector payload validation, sample decoding, and observation emission were compressed inside `PrometheusObservationSource`.
- systemd command output decoding, row selection, unit dictionary construction, and observation emission were compressed inside `SystemdObservationSource`.

The prior intermediate-structure investigation correctly identified records such as `PackageRecord` and `RelationshipFact`, but those records are counterexamples to universal artifact symmetry. Prometheus and systemd show the same bounded translation pressure without a named intermediate record.

## After

The explicit boundary is:

```text
Provider Language

↓

Provider Language Translation

↓

bounded Seed output
```

Provider Language Translation is now documented as the recovered owner. It owns provider-native decoding and bounded vocabulary selection before Seed output construction. It does not own canonical Observation semantics, evidence interpretation, fact construction, schemas, ledgers, projection, or provider redesign.

## Recovered producer

Recovered producer: **Provider Language Translation**.

Its responsibility is:

```text
Given provider-native language,
produce the bounded translation input required for Seed language.
```

Provider-specific examples:

- dpkg translation produces installed package records from dpkg status text.
- Python relationship translation produces relationship facts from Python source syntax.
- Prometheus translation produces observations from allowlisted Prometheus vector samples.
- systemd translation produces observations from decoded systemd unit rows.

## Recovered artifact, if any

No single recurring implementation artifact emerged.

Artifacts are provider-local and path-specific:

| Provider family | Artifact produced by translation | Recurring across all reviewed providers? |
| --- | --- | --- |
| dpkg | `PackageRecord` | No |
| Python relationship extraction | `RelationshipFact` | No |
| Prometheus | canonical `Observation` instances | No intermediate artifact |
| systemd | canonical `Observation` instances | No intermediate artifact |

The recurring owner is bounded translation work, not a uniform intermediate record.

## Consumer of the artifact

- `PackageRecord` is consumed by `package_records_to_observations(...)`.
- `RelationshipFact` is consumed by `RepositorySourceObservationSource.collect(...)` when repository relationship facts are converted to observations.
- Prometheus translation output is consumed directly as `Observation` values returned by `PrometheusObservationSource.collect(...)`.
- systemd translation output is consumed directly as `Observation` values returned by `SystemdObservationSource.collect(...)`.

## Compatibility preserved

No compatibility boundary changed.

This slice does not change runtime behavior, public schemas, event ledger behavior, diagnostic surfaces, provider inputs, provider outputs, CLI flags, observation predicates, metadata shapes, or downstream ingestion behavior.

## Files changed

- `provider_language_translation_slice_001.md`

## LOC changed

- Added: 184 lines
- Removed: 0 lines
- Net: +184 lines

## Tests executed

- `pytest -q tests/test_local_packages.py tests/test_self_model_acquisition_pipeline.py tests/test_observation_sources.py`

## Remaining compressed Provider Language Translation responsibilities

The following responsibilities remain compressed inside provider implementations and can be considered future local recovery candidates only if implementation pressure requires them:

- Prometheus still combines safe query execution, response validation, sample decoding, and canonical observation construction inside `PrometheusObservationSource`.
- systemd still combines command execution, JSON row decoding, local unit dictionaries, and canonical observation construction inside `SystemdObservationSource`.
- dpkg translation has a natural local artifact (`PackageRecord`), but dpkg field parsing and installed-package filtering remain a single bounded helper.
- Python relationship extraction has a natural local artifact (`RelationshipFact`), but AST parsing and supported syntax translation remain in the same helper family.

These are intentionally left unchanged because this slice recovers only one boundary and does not redesign providers.

## Acceptance answers

### 1. Where were Provider Language and Provider Language Translation previously mixed?

They were mixed inside provider-specific helpers and observation sources: dpkg status parsing in `parse_dpkg_status(...)`, Python AST extraction in relationship helpers, Prometheus query/payload/sample handling in `PrometheusObservationSource`, and systemd JSON row decoding in `SystemdObservationSource`.

### 2. Which recovered architectural boundary became more explicit?

**Provider Language != Provider Language Translation** became explicit.

### 3. What implementation artifact is now produced, if any, and who consumes it?

No recurring artifact is produced. Existing provider-local artifacts remain: `PackageRecord` is consumed by `package_records_to_observations(...)`, and `RelationshipFact` is consumed by repository source observation emission. Prometheus and systemd demonstrate compressed translation directly to canonical observations.

### 4. Did implementation evidence suggest a more precise responsibility name?

Yes. The evidence supports **Provider Language Translation** more precisely than an intermediate-record name because the recurring implementation pressure is bounded translation work, not artifact symmetry.

### 5. Did any compatibility boundary change?

No.

# Prometheus Provider Translation Completion Audit

## Verdict

No.

Prometheus does not currently contain another implementation-backed compressed Provider Language Translation responsibility after `PrometheusObservationShape`. The remaining edge from `PrometheusObservationShape` to `Observation` is canonical Seed Observation Language construction: create an `Observation`, attach source type, observed time, subject, predicate, value, confidence, metadata, and dimensions, and preserve the existing compatibility surface.

Prometheus has therefore reached a natural local Provider Language Translation stopping point.

## Reviewed implementation path

The current Prometheus provider-local pipeline is implementation-visible as:

```text
Prometheus JSON
↓
PrometheusDecodedSample
↓
PrometheusObservationShape
↓
Observation
```

The relevant implementation evidence is contained in `seed_runtime/observation_sources.py`:

- `PrometheusObservationSource.collect(...)` owns safe-query orchestration, HTTP fetch timing counters, error handling, and collection counters.
- `_query(...)` validates the HTTP API response as a successful Prometheus vector response.
- `_prometheus_decoded_sample(...)` validates a provider-shaped sample, extracts the Prometheus metric labels, requires a non-empty `instance`, parses the provider sample timestamp, and preserves the raw sample value.
- `_observations_from_query(...)` builds Prometheus source metadata and hands decoded samples plus metadata to `_prometheus_observation_shapes(...)`.
- `_prometheus_observation_shapes(...)` performs the remaining provider-local interpretation: query family selection, Prometheus label interpretation, predicate/value shaping, endpoint OS promotion suppression, and sample-time ownership.
- `PrometheusObservationSource._observation(...)` only constructs the canonical `Observation` object and delegates filesystem identity dimensions to `_filesystem_dimensions(...)`.

## Where Provider Language Translation terminates

Provider Language Translation terminates at `PrometheusObservationShape`.

`PrometheusObservationShape` already contains the fields that Seed Observation construction needs without further Prometheus query-family interpretation:

```text
observed_at
subject
predicate
value
metadata
```

At that point:

- Prometheus JSON shape has already been decoded.
- Prometheus vector sample validity has already been decided.
- Prometheus `instance` has already become the observation subject.
- Prometheus sample timestamp has already become `observed_at`.
- Prometheus query families have already been mapped to Seed predicates.
- Prometheus sample values have already been converted where needed.
- Prometheus metadata has already been assembled or copied.
- Endpoint-subject OS fact-promotion suppression has already been applied.

The remaining call into `_observation(...)` does not inspect the Prometheus query name, does not branch on metric family, does not decode provider JSON, does not reinterpret labels, does not select predicates, and does not transform the provider sample value. It accepts already-shaped `observed_at`, `subject`, `predicate`, `value`, and `metadata` and emits a canonical `Observation`.

## Where Seed Observation Language begins

Seed Observation Language begins at `PrometheusObservationSource._observation(...)`.

That method performs canonical observation construction only:

- `id=new_id("obs_prometheus")`
- `source_type=self.source_type`
- `observed_at=observed_at`
- `subject=subject`
- `predicate=predicate`
- `value=value`
- `confidence=0.95`
- `metadata=metadata`
- `dimensions=_filesystem_dimensions(predicate, metadata)`

Those responsibilities are the standard Observation emission edge. They are not a separate Prometheus language boundary unless implementation evidence shows hidden provider interpretation there. The current implementation does not show that.

## Remaining helper methods

### `_filesystem_dimensions(...)`

`_filesystem_dimensions(...)` is a compatibility-preserving canonical dimension handoff for already-selected filesystem predicates. It only checks whether the already-shaped predicate is one of the filesystem measurement predicates and copies stable label values from existing metadata into observation dimensions.

This helper does not decode Prometheus JSON, decide metric family meaning, create new predicates, or reinterpret sample values. It preserves identity dimensions for the canonical observation surface.

### `_prometheus_sample_timestamp(...)`

`_prometheus_sample_timestamp(...)` belongs before `PrometheusDecodedSample`; it parses provider sample timestamps and rejects malformed provider time values. It is already upstream of `PrometheusObservationShape`.

### `_prometheus_int(...)`

`_prometheus_int(...)` is used inside `_prometheus_observation_shapes(...)`, before canonical observation construction. Numeric provider sample conversion is already part of provider-local shape construction.

### `_prometheus_os_from_uname(...)`

`_prometheus_os_from_uname(...)` is also used inside `_prometheus_observation_shapes(...)`. Prometheus uname label interpretation therefore already terminates before `_observation(...)`.

## Supporting provider comparisons without normalization

The comparison providers support the stopping point rather than another Prometheus slice:

- `PackageRecord` is a normalized package evidence record independent of dpkg wire format. Dpkg text parsing terminates at `PackageRecord`, and generic package observation construction occurs later.
- `RelationshipFact` is a language-neutral relationship evidence record. Python AST/source interpretation terminates at relationship facts, and repository-source observation construction maps those fact fields into `Observation` fields later.
- `SystemdObservationSource` remains a counterexample where provider-shaped dictionaries and observation construction are more compressed in one source class. That does not justify decomposing Prometheus further, because Prometheus already exposes both decoded-sample and observation-shape records before `Observation` construction.

Prometheus is now closer to the mature dpkg and Python relationship paths than to the compressed systemd path. The mature comparison is not that every provider must add one more record; it is that provider language translation stops once a provider-local/normalized record already contains the observation-ready subject, predicate, value, time, and metadata.

## Answers to the investigation questions

### 1. Does Prometheus still contain one compressed Provider Language Translation responsibility?

No.

The remaining `_observation(...)` method performs canonical observation construction. Provider-specific decoding, query-family interpretation, predicate selection, value conversion, timestamp selection, metadata shaping, and endpoint OS suppression already happen before it.

### 2. If yes, which provider-local boundary became more explicit?

Not applicable.

No additional provider-local boundary was projected. Creating another abstraction after `PrometheusObservationShape` would manufacture a boundary that the implementation does not support.

### 3. If no, what implementation evidence shows Provider Language Translation now terminates before canonical Observation construction?

Implementation evidence shows termination at `PrometheusObservationShape` because:

- `_prometheus_decoded_sample(...)` returns a validated decoded provider sample rather than an `Observation`.
- `_prometheus_observation_shapes(...)` returns `PrometheusObservationShape` records and owns query-specific mapping for `up`, `node_uname_info`, `node_filesystem_avail_bytes`, and `node_filesystem_size_bytes`.
- `_prometheus_observation_shapes(...)` owns endpoint OS promotion suppression metadata for `node_uname_info` endpoint subjects.
- `_observations_from_query(...)` passes only shape fields into `_observation(...)`.
- `_observation(...)` constructs `Observation` with canonical fields, fixed Prometheus confidence, metadata handoff, and dimension handoff.
- `_filesystem_dimensions(...)` only derives dimensions from metadata for already-shaped filesystem predicates.

### 4. Did any compatibility boundary change?

No.

This audit makes no code, schema, behavior, ledger, provider framework, or observation model change. Existing Prometheus observation IDs still use the `obs_prometheus` prefix, source type remains provider-configured, confidence remains `0.95`, metadata is handed through, and filesystem dimensions remain attached through `_filesystem_dimensions(...)`.

## Completion conclusion

Prometheus Provider Language Translation has reached a natural local stopping point.

The implementation-backed provider-local ownership now ends at `PrometheusObservationShape`. The remaining responsibility belongs to Seed Observation Language: canonical `Observation` construction and compatibility-preserving field, metadata, confidence, and dimension handoff.

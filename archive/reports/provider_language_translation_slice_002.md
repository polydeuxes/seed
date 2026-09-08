# Provider Language Translation Slice 002

## Selected provider

Prometheus only.

This slice treats `PrometheusDecodedSample` as the established implementation-local boundary and investigates only the remaining Prometheus-local work between decoded samples and Seed `Observation` construction.

## Selected provider-local boundary

Selected boundary:

```text
PrometheusDecodedSample

↓

PrometheusObservationShape

↓

Observation
```

The recovered ownership transition is:

```text
Prometheus sample interpretation

!=

Observation construction
```

`PrometheusObservationShape` is provider-local. It is not a shared provider abstraction, not a schema change, and not a cross-provider translation layer.

## Implementation evidence

### Prometheus decoded sample remains the provider JSON boundary

`PrometheusDecodedSample` still owns only decoded vector-sample fields: metric labels, instance, sample timestamp, raw timestamp, and sample value. `_prometheus_decoded_sample(...)` still accepts provider-shaped sample JSON and returns `None` for malformed samples before downstream interpretation begins.

### Remaining responsibilities after `PrometheusDecodedSample`

After sample decoding, Prometheus still performs provider-local work that cannot be treated as generic observation emission:

- `up` produces two provider-specific observation shapes when possible: `endpoint_role` from the Prometheus `job` label and `up` from the sample value.
- `node_uname_info` derives an `os` value from Prometheus uname labels.
- endpoint-looking `node_uname_info` subjects preserve Prometheus evidence while suppressing fact promotion with `fact_promotion_suppressed=true` and `fact_promotion_suppressed_reason=prometheus_node_uname_os_endpoint_subject`.
- filesystem metric names select filesystem predicates while preserving Prometheus metric labels for downstream filesystem dimensions.
- unknown queries produce no provider-local shapes.

This work is now owned by `_prometheus_observation_shapes(...)`, which accepts a decoded sample and already-shaped Prometheus metadata, then returns `PrometheusObservationShape` records.

### Clearest implementation boundary

The clearest remaining boundary was not sample decoding anymore. The strongest remaining compressed responsibility was Prometheus sample interpretation: turning one decoded sample plus its query family into one or more provider-local observation shapes containing:

- `observed_at`;
- `subject`;
- `predicate`;
- `value`;
- metadata after provider-specific preservation/suppression rules.

`PrometheusObservationSource._observations_from_query(...)` now delegates that interpretation to `_prometheus_observation_shapes(...)` and only converts returned shapes through `_observation(...)`.

### Work that remains inherently provider-specific

The recovered helper is intentionally Prometheus-specific because it depends on Prometheus metric names and labels:

- `up` and `job` are Prometheus/exporter metric vocabulary;
- `node_uname_info`, `sysname`, and `system` are Prometheus node-exporter vocabulary;
- `node_filesystem_avail_bytes` and `node_filesystem_size_bytes` are Prometheus metric-family names;
- endpoint OS fact-promotion suppression is specific to Prometheus endpoint subjects;
- filesystem dimensions still derive from Prometheus metric labels.

### Work that would still be incorrect to generalize

It would be incorrect to generalize this boundary into a provider framework because the helper embeds Prometheus query-family semantics. Dpkg's `PackageRecord`, Python's `RelationshipFact`, and Systemd's provider-shaped unit dictionaries are useful supporting comparisons, but this slice does not normalize them and does not add a shared translation layer.

## Before

Before this slice, `_observations_from_query(...)` performed the following in one post-decoding block:

```text
PrometheusDecodedSample

↓

metadata preservation
+ node identity metadata handling
+ endpoint suppression
+ predicate assignment
+ value conversion
+ filesystem metric selection
+ Observation construction
```

The selected responsibilities were compressed because decoded-sample interpretation and direct calls to `_observation(...)` lived together in each query branch.

## After

After this slice, `_observations_from_query(...)` still owns query-loop orchestration and base metadata preservation, but provider-local sample interpretation is directly observable as `PrometheusObservationShape` records:

```text
PrometheusDecodedSample

↓

_prometheus_observation_shapes(...)

↓

PrometheusObservationShape

↓

_observation(...)

↓

Observation
```

`_observation(...)` remains the compatibility-preserving construction point for Seed `Observation` instances, including id prefix, source type, confidence, metadata, and filesystem dimensions.

## Compatibility preservation

No compatibility boundary changed.

The public collection entrypoint remains `PrometheusObservationSource.collect()`. The safe query list, HTTP acquisition, malformed-sample skip behavior, emitted subjects, predicates, values, metadata, confidence, source type, filesystem dimensions, and endpoint OS fact-promotion suppression behavior are preserved.

## Files changed

- `seed_runtime/observation_sources.py`
- `tests/test_observation_sources.py`
- `provider_language_translation_slice_002.md`

## LOC changed

At report time, implementation/test `git diff --numstat` reported:

```text
96	62	seed_runtime/observation_sources.py
58	0	tests/test_observation_sources.py
```

The report file adds 210 lines as the requested deliverable.

## Tests executed

```text
pytest -q tests/test_observation_sources.py -k prometheus
pytest -q tests/test_observation_sources.py tests/test_predicate_normalizers.py
```

Results:

```text
13 passed, 72 deselected
95 passed
```

## Remaining Prometheus-local compression

Prometheus still intentionally keeps these responsibilities local to the provider:

- base Prometheus metadata shaping inside `_observations_from_query(...)`;
- node-uname identity metadata preservation (`instance` and `nodename`) inside `_observations_from_query(...)`;
- filesystem dimension extraction inside `_filesystem_dimensions(...)` during Observation construction;
- Prometheus HTTP query acquisition and vector-response validation inside `_query(...)`;
- all query-family semantics inside `_prometheus_observation_shapes(...)`.

The remaining compression is acceptable for this slice because the task was to recover exactly one provider-local boundary and stop.

## Recovery question answers

### 1. Where were the selected Prometheus responsibilities previously compressed?

They were compressed inside `PrometheusObservationSource._observations_from_query(...)`, where query-family interpretation, predicate assignment, value conversion, endpoint suppression metadata, and direct calls to `_observation(...)` occurred in the same branch logic after `PrometheusDecodedSample` decoding.

### 2. Which provider-local boundary became more explicit?

The boundary between Prometheus sample interpretation and Seed `Observation` construction became explicit through `PrometheusObservationShape` and `_prometheus_observation_shapes(...)`.

### 3. How does the implementation now better reflect Provider Language Translation?

The Prometheus path now has one more implementation-local translation step:

```text
Prometheus JSON

↓

PrometheusDecodedSample

↓

PrometheusObservationShape

↓

Observation
```

This mirrors the repository's mature provider-local translation style without generalizing providers: provider-native material is decoded first, provider-local interpreted shape is formed next, and only then is a Seed `Observation` constructed.

### 4. Did any compatibility boundary change?

No.

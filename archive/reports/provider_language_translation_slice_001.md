# Provider Language Translation Slice 001

## Selected provider

Prometheus.

## Selected provider-local boundary

Decoded Prometheus vector sample != Prometheus observation construction.

This slice recovers exactly one Prometheus-local Provider Language Translation boundary by making the decoded vector sample a provider-local record before Prometheus observation emission. It does not introduce a shared provider framework, a shared translation layer, or any cross-provider abstraction.

## Implementation evidence

### Prometheus before this slice

`PrometheusObservationSource._query(...)` already owned safe Prometheus HTTP acquisition and vector-response validation: it rejects non-allowlisted queries, requests `/api/v1/query` with `GET`, JSON-decodes the response, verifies `status == "success"`, verifies `data.resultType == "vector"`, and verifies that `data.result` is a list.

Before this slice, `_observations_from_query(...)` then performed all of the following in one loop over provider samples:

- provider sample shape decoding (`sample` must be a dict, `metric` must be a dict, `value` must be a list with timestamp and value);
- timestamp parsing through `_prometheus_sample_timestamp(...)`;
- identity extraction from `metric["instance"]`;
- metadata preservation (`metric_labels`, base URL, metric name, raw sample timestamp, sample-time authority, and seed collection time);
- node identity metadata handling for `node_uname_info` (`instance` and `nodename` metadata);
- predicate assignment (`endpoint_role`, `up`, `os`, `filesystem_avail_bytes`, `filesystem_size_bytes`);
- provider-specific value conversion through `_prometheus_int(...)` and `_prometheus_os_from_uname(...)`;
- observation emission through `_observation(...)`;
- filesystem dimension derivation through `_filesystem_dimensions(...)` from preserved metric labels.

That made Prometheus more compressed than the already separated dpkg path (`Provider Language -> PackageRecord -> Observation`) and Python relationship path (`Provider Language -> RelationshipFact -> Observation`). The comparison is supporting evidence only; this slice does not normalize providers.

### Prometheus after this slice

This slice adds `PrometheusDecodedSample`, a frozen provider-local record containing only the valid decoded vector-sample fields needed by downstream Prometheus translation:

- `metric`;
- `instance`;
- `sample_timestamp`;
- `sample_timestamp_raw`;
- `sample_value`.

The new `_prometheus_decoded_sample(...)` helper accepts provider-shaped sample JSON and either returns `PrometheusDecodedSample` or `None` for malformed samples. It performs only provider sample decoding and timestamp validation; it does not assign predicates, shape observation metadata, derive filesystem dimensions, or construct observations.

`PrometheusObservationSource._observations_from_query(...)` now consumes `PrometheusDecodedSample` and remains the owner of Prometheus observation construction: metadata preservation, predicate assignment, identity usage, value interpretation, endpoint fact-promotion suppression, and calls to `_observation(...)` remain there.

## Before

```text
PrometheusObservationSource._observations_from_query(...)

provider sample shape checks
+ sample timestamp parsing
+ instance extraction
+ metadata preservation
+ node_uname_info identity metadata
+ predicate assignment
+ value conversion
+ filesystem dimension inputs
+ Observation construction
```

## After

```text
_prometheus_decoded_sample(...)

provider sample shape checks
+ sample timestamp parsing
+ instance extraction

↓

PrometheusDecodedSample

↓

PrometheusObservationSource._observations_from_query(...)

metadata preservation
+ node_uname_info identity metadata
+ predicate assignment
+ value conversion
+ filesystem dimension inputs
+ Observation construction
```

## Compatibility preservation

No compatibility boundary changed.

The public Prometheus collection surface remains `PrometheusObservationSource.collect()`. The safe query allowlist, HTTP method, response validation, observation predicates, observation subjects, values, metadata fields, dimensions, confidence, source type, and malformed-sample skip behavior are preserved. The new record and decoder are provider-local implementation details.

## Files changed

- `seed_runtime/observation_sources.py`
- `tests/test_observation_sources.py`
- `provider_language_translation_slice_001.md`

## LOC changed

`git diff --stat` reported:

```text
provider_language_translation_slice_001.md | 225 +++++++++++++----------------
seed_runtime/observation_sources.py        | 101 ++++++++-----
tests/test_observation_sources.py          |  41 ++++++
3 files changed, 208 insertions(+), 160 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_observation_sources.py -k 'prometheus'
pytest -q tests/test_observation_sources.py
```

Results:

```text
11 passed, 72 deselected
83 passed
```

## Recovery question answers

### 1. Which Prometheus responsibilities were previously compressed?

Prometheus previously compressed provider sample decoding, sample timestamp parsing, instance extraction, metadata preservation, node identity metadata handling, predicate assignment, provider-specific value interpretation, filesystem-dimension input preservation, and Observation construction inside `_observations_from_query(...)` and `_observation(...)`.

### 2. Which recovered provider-local boundary became more explicit?

The boundary between decoded Prometheus vector sample and Prometheus observation construction became explicit. `_prometheus_decoded_sample(...)` now owns the provider JSON sample validation/decoding step and returns `PrometheusDecodedSample`; `_observations_from_query(...)` owns the downstream Prometheus translation to Seed observations.

### 3. How does the implementation now better reflect Provider Language Translation?

The implementation now shows a local translation chain:

```text
Prometheus HTTP vector JSON sample
↓
PrometheusDecodedSample
↓
Observation
```

This mirrors the repository evidence that translation may pass through a bounded implementation-local record, while remaining strictly Prometheus-specific. The record is not a generic provider artifact and does not claim that other providers should follow the same shape.

### 4. Did any compatibility boundary change?

No.

## Remaining provider-local compression

Prometheus still intentionally keeps these responsibilities compressed in `PrometheusObservationSource._observations_from_query(...)`:

- metric allowlist interpretation by query name;
- metadata preservation policy;
- `node_uname_info` nodename metadata handling;
- endpoint subject fact-promotion suppression for Prometheus OS observations;
- predicate assignment;
- Prometheus value interpretation (`up`, filesystem byte values, uname-derived OS values);
- filesystem dimension derivation through metadata consumed by `_filesystem_dimensions(...)`;
- final Observation construction through `_observation(...)`.

Those responsibilities remain provider-specific and were not decompressed in this slice.

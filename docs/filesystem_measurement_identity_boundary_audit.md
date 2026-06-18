# Filesystem Measurement Identity Boundary Audit

## Status

Investigation only. No implementation changes were made to storage projections, alias handling, current-facts lookup, or State Summary rendering.

Short answer: the observed behavior is best explained as **E. broader architectural boundary issue**, with concrete expressions of **C. endpoint-vs-host identity** and **D. measurement ownership**. The evidence does not point first to a storage arithmetic/projection bug or a simple missing alias-resolution bug.

## Audit question

Why are Prometheus filesystem measurements queryable on the scrape endpoint subject, for example `192.0.2.115:9100 filesystem_free_bytes`, but not on a host subject such as `example_host filesystem_free_bytes`, while State Summary can still know many aliases for `example_host` and storage remains `(none)` in the bounded summary?

## Observed behavior

The Prometheus observation source collects `node_filesystem_avail_bytes` and `node_filesystem_size_bytes` from a fixed safe-query allowlist. Each Prometheus sample is emitted with `subject=instance`, where `instance` is the Prometheus target label such as `192.0.2.115:9100`. The source then emits filesystem observations with raw predicates `filesystem_avail_bytes` and `filesystem_size_bytes`; predicate normalization maps these to canonical filesystem predicates in the normal ingestion pipeline.

For Prometheus `node_uname_info`, the source has special handling: only `node_uname_info` is described as authoritative for stable host identity, and its metadata includes `instance` and `nodename`. Other metrics, including filesystem metrics, intentionally keep only metric labels and remain endpoint-scoped.

## Identity model discovered

The repository currently distinguishes at least four concepts that are easy to conflate:

1. **Scrape endpoint**: a Prometheus `instance` label such as `192.0.2.115:9100`.
2. **Host identity**: a stable name such as `example_host`, often discovered from `node_uname_info` `nodename` or other durable identity predicates.
3. **Alias edge**: an explicit identity relation. The alias resolver builds from alias-like predicates, but it refuses aliases that cross the endpoint/non-endpoint boundary.
4. **Measurement subject**: the subject attached to a time-series fact. For Prometheus filesystem metrics this is currently the endpoint-shaped `instance`, not the host.

This is not merely a UI distinction. The alias resolver explicitly rejects any alias that would equate an endpoint-shaped subject with a non-endpoint-shaped subject. Additionally, `prometheus_instance` is specifically excluded from alias predicates, even though other `*_instance` predicates can participate as aliases.

## Measurement ownership model discovered

Filesystem measurements currently live on the **Prometheus endpoint subject**. The ingestion source uses the Prometheus `instance` label as the observation subject for `up`, `node_uname_info`, and filesystem metrics. Filesystem metric observations get dimensions for `mountpoint`, `device`, and `fstype`, but those dimensions do not alter the subject owner.

Projected support for measurement predicates uses the resolved subject only within allowed alias components, plus predicate and dimensions. Because endpoint-to-host aliases are blocked, endpoint-owned filesystem samples do not become host-owned current facts.

## Alias behavior discovered

Alias construction has two relevant paths:

- `EndpointAliasNormalizer` can derive source-specific instance predicates from metadata containing both a stable name and endpoint. For Prometheus, `node_uname_info` can produce `prometheus_instance` from `nodename -> instance` because it carries both metadata fields.
- `EndpointIdentityNormalizer` can derive `alias` observations between known identities and endpoint-shaped subjects when endpoint base identities match known identity predicates.

However, projection does not allow these to collapse host and endpoint identity for query ownership. `prometheus_instance` is deliberately not an alias predicate, and even an `alias` fact between `example_host` and `192.0.2.115:9100` is blocked by the endpoint boundary in the alias resolver.

Repository tests encode this boundary directly. They assert that a `prometheus_instance` fact on `example_host` does not make endpoint `up` reachable through `example_host`, and that Prometheus nodename discovery preserves a `prometheus_instance` fact without aliasing endpoint measurements to the host.

## Storage-summary implications

There are two distinct storage surfaces:

1. **Explicit storage projection**: `storage_state_projection` scans current measurement facts, selects `filesystem_free_bytes` and `filesystem_total_bytes`, groups them by canonical subject, mountpoint, and dimensions, and emits filesystem rows only when both free and total are present.
2. **Default State Summary**: `format_state_summary` intentionally omits filesystem/storage detail. The code comment states that the default State Summary is not a storage/filesystem detail surface and that storage detail must not leak there.

Therefore, State Summary showing storage `(none)` does not by itself prove filesystem facts are missing. State Summary's `top_entities_by_kind["storage"]` is for entities classified as storage, not a filesystem-detail table. Filesystem measurements may exist and still not cause a storage entity to appear.

If an explicit storage projection is empty while direct endpoint `--current-facts` returns only `filesystem_free_bytes`, the most likely repository-level explanation is that projection rows require a complete pair: both `filesystem_free_bytes` and `filesystem_total_bytes` with matching subject and dimensions. If both complete canonical measurements exist on the endpoint, the storage projection should produce endpoint-hosted filesystem rows. That is an explicit projection question, not evidence that host alias lookup should return endpoint-owned measurements.

## Broader architectural implications

The same boundary affects more than storage:

- Prometheus `up` is normalized to endpoint-scoped `availability_status`, and tests assert `example_host availability_status` remains unknown when only endpoint availability exists.
- State Summary separates endpoint scrape availability from host availability and service availability.
- `endpoint_role` is an endpoint-scoped predicate. Relationship projection avoids treating Prometheus endpoint roles as general service ownership/provides relationships.
- `prometheus_instance` is not used to project a monitored-by relationship for Prometheus observations.

This means the pattern is not storage-specific. Storage is one symptom of a larger rule: endpoint-derived measurements preserve endpoint visibility unless the repository has explicit host-ownership semantics.

## Candidate explanations

### A. Storage projection issue

Possible only if explicit `storage_state_projection` fails to produce rows even when complete matching `filesystem_free_bytes` and `filesystem_total_bytes` samples exist on the same endpoint subject and dimensions. It does not explain why `example_host filesystem_free_bytes` is empty.

### B. Alias resolution issue

Not the primary explanation. Alias resolution is doing what repository code and tests say: it refuses endpoint/non-endpoint identity collapse and excludes `prometheus_instance` from alias predicates.

### C. Endpoint-vs-host identity issue

Yes. This is a central part of the behavior. The scrape endpoint and host are modeled as distinct identities for measurement-query purposes.

### D. Measurement ownership issue

Yes. Filesystem samples are owned by the Prometheus endpoint subject, not by the discovered host subject. Existing alias knowledge is not measurement ownership.

### E. Broader architectural boundary issue

Best overall answer. The repository is preserving boundaries such as `endpoint visibility != host ownership`, `measurement subject != entity identity`, and `alias-like knowledge != ownership transfer`.

## Answers to specific questions

### 1. Where do filesystem measurements currently live?

They live on the **endpoint subject / Prometheus instance** from the metric label, for example `192.0.2.115:9100`. They are not re-owned to `example_host` during ingestion or current-fact lookup.

### 2. Is the current location intentional or accidental?

The endpoint-scoped location appears intentional. The source comments say only `node_uname_info` is authoritative for stable host identity and other metrics remain endpoint-scoped. Tests also explicitly preserve endpoint facts from being reachable as host facts through `prometheus_instance`.

### 3. Should `example_host filesystem_free_bytes` exist?

Repository authority does not currently say yes. Under the present model, it should not exist merely because `example_host` has `prometheus_instance=192.0.2.115:9100` or many aliases. It would require a separate architectural decision to model host ownership of endpoint-derived filesystem measurements.

### 4. Does alias knowledge currently bridge host -> endpoint for query purposes?

No. The alias resolver blocks endpoint/non-endpoint alias collapse, and `prometheus_instance` is not an alias predicate. This appears intentional because tests cover exactly this non-bridging behavior.

### 5. Why does State Summary storage show `(none)` when filesystem measurements exist?

Because default State Summary is intentionally bounded and does not render filesystem detail. Its storage section lists storage-kind top entities, not endpoint-owned filesystem measurement rows. The explicit storage projection is the storage/filesystem detail surface.

### 6. Is the storage summary problem specific to storage?

No. Availability, endpoint health, service health boundaries follow the same pattern. Endpoint scrape availability remains distinct from host availability and service availability; endpoint roles from Prometheus are also kept from implying general service ownership relationships.

### 7. What architectural boundary is preserved?

The preserved boundary is: **endpoint visibility is not host ownership**. More specifically: **measurement subject is not entity identity**, and **alias-like knowledge is not an ownership transfer across endpoint/host boundaries**.

## Recommended next investigation

1. Run an explicit storage projection against the same repository state where endpoint `filesystem_free_bytes` and `filesystem_total_bytes` are queryable, and verify whether complete endpoint/dimension pairs exist.
2. Inspect current facts for the exact endpoint with dimensions included, confirming that `filesystem_free_bytes` and `filesystem_total_bytes` share identical `mountpoint`, `device`, and `fstype` dimensions.
3. Decide architecturally whether Seed needs a new explicit relation such as `endpoint_observes_host`, `endpoint_belongs_to_host`, or `measurement_owner`, rather than using aliases for ownership transfer.
4. Audit endpoint-derived predicates beyond filesystem (`availability_status`, `health_status`, `endpoint_role`, service-health predicates if present) for a consistent host-ownership projection policy.
5. If host-owned filesystem queries are desired, design that as a new projection or lookup surface with explicit provenance and boundary language, not as a silent alias-resolution change.

## Non-conclusions

- This audit does not conclude that storage projection arithmetic is wrong.
- This audit does not conclude that aliases should bridge hosts and endpoints.
- This audit does not conclude that current-facts lookup should change.
- This audit does not conclude that State Summary should render filesystem detail.
- This audit does not identify endpoint-owned Prometheus measurements as incorrect; it identifies that they are intentionally not host-owned under the current model.

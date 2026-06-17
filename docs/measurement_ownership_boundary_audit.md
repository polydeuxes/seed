---
status: audit
scope: measurement ownership boundary investigation
created: 2026-06-17
---

# Measurement Ownership Boundary Audit

## Status

Investigation only. No implementation changes were made to aliases, current-facts lookup, storage projection, Prometheus ingestion, availability projection, endpoint-role handling, relationship projection, or identity projection.

Short answer: Seed currently has a strong **measurement subject** model and a strong **endpoint/non-endpoint identity boundary**, but it does **not** have a separate general **measurement owner**, **observed entity**, or **ownership transfer** model for endpoint-derived measurements. The current code treats the fact subject as the query/projection owner for current measurements unless an explicit source records the fact directly on another subject. Repository evidence does not show a deliberate architectural decision that measurement subject and measurement owner must always be identical; it shows that they are currently not separated and that aliases are intentionally not allowed to perform that separation implicitly.

## Audit question

Does Seed currently model measurement ownership, specifically the distinction between:

```text
where a measurement was observed
    vs
what entity the measurement describes
```

This audit starts from existing concepts, missing concepts, and preserved boundaries. It does not start from HomeOps display requirements and does not propose fixes.

## Prior findings reconciled

This audit treats the following documents as investigation inputs and does not rediscover their already-established findings:

- `docs/filesystem_measurement_identity_boundary_audit.md`
- `docs/lens_view_reconciliation.md`
- `docs/lens_view_architecture_audit.md`
- `docs/lens_implementation_frontier_observation.md`
- `docs/state_summary_scope_review.md`

The reconciled prior findings are:

1. **Endpoint visibility is not host ownership.** Prometheus endpoint subjects such as `192.168.254.115:9100` are not silently collapsed into host subjects such as `node115`.
2. **Measurement subject is not entity identity.** A measurement can be attached to an endpoint-shaped subject without proving that the endpoint is the stable host identity.
3. **Alias-like knowledge is not ownership transfer.** `prometheus_instance` can preserve the relationship between `node115` and `192.168.254.115:9100`, but it is not an alias predicate and it does not move endpoint facts to the host.
4. **Storage is a lens/projection issue, not State Summary core authority.** The explicit storage projection is the filesystem detail surface; default State Summary deliberately avoids becoming a storage topology authority.
5. **Lens language is mostly architectural vocabulary today.** Read-only projection surfaces exist, but Storage Lens, Availability Lens, Node Detail View, and HomeOps View are not implemented as formal independent lens products.

## Current ownership model

Seed has several ownership-like concepts, but none is a general measurement-owner concept:

- **Fact ownership by subject:** every `Fact` has `subject_id`, `predicate`, `value`, dimensions, evidence, and timing. Query helpers use `subject_id` plus alias resolution rules as the location of current support.
- **Observation subject:** every `Observation` has `subject`, predicate, dimensions, metadata, and observed time. Normalizers preserve or derive observations with the same subject unless a specific normalizer derives another observation.
- **Alias/identity ownership:** `AliasResolver` builds identity components only from approved alias predicates and explicitly refuses endpoint/non-endpoint collapse.
- **Relationship ownership/topology:** `RelationshipCatalog` can project semantic relationships such as `monitored_by` or `provides`, but Prometheus-derived `prometheus_instance` and `endpoint_role` relationships are suppressed to avoid promoting endpoint visibility into broader topology/ownership claims.
- **Storage projection grouping:** `storage_state_projection` groups filesystem current measurements by canonical fact subject, mountpoint, and dimensions. Because endpoint/host aliases are blocked, endpoint-shaped filesystem facts remain endpoint-shaped rows.

No inspected model has fields like `measurement_owner`, `observed_entity`, `observation_target`, `owner_subject`, or `describes_entity` for facts or observations.

## Current measurement model

Seed's measurement model is predicate- and subject-based:

- The predicate catalog marks `availability_status`, `filesystem_free_bytes`, `filesystem_total_bytes`, and `health_status` as measurements.
- Legacy measurement predicates include raw Prometheus/storage predicates such as `up`, `filesystem_avail_bytes`, and `filesystem_size_bytes`.
- Fact support groups measurements by subject, predicate, and dimensions, using the latest current sample rather than aggregate support across historical values.
- Inference preserves subject. `availability_status=up/down` infers `health_status=ok/degraded` on the same subject.
- Current-facts lookup can resolve aliases for most predicates, but endpoint-scoped predicates force exact subject lookup. Alias resolution itself excludes `prometheus_instance` and rejects endpoint/non-endpoint identity collapse.

Therefore, the effective current measurement owner is the fact subject after permitted alias canonicalization, not a separately modeled described entity.

## Subject vs ownership analysis

### Does Seed distinguish measurement subject from measurement owner?

No general distinction was found.

Evidence:

- `Fact` has `subject_id` but no owner/described-entity field.
- `FactSupport` has `subject`, predicate, dimensions, and support metadata, but no separate owner/described-entity field.
- Measurement support groups by subject/predicate/dimensions and selects the latest sample for measurement predicates.
- Current lookup starts from subject/predicate and filters support by permitted aliases; endpoint-scoped predicates disable alias resolution.
- The storage projection uses the canonical fact subject as its `host` field. That name is projection terminology; under current boundary rules it may be an endpoint-shaped canonical subject.

### Does Seed distinguish where observed from what described?

Only partially, and mostly as provenance metadata rather than ownership semantics.

Prometheus observations record source metadata such as collector, source name, Prometheus base URL, metric labels, sample timestamp, and `instance`. For `node_uname_info`, the source additionally preserves `nodename` and `instance`, because that metric is treated as authoritative for stable host identity. Other Prometheus metrics intentionally remain endpoint-scoped and do not carry host identity metadata for endpoint alias normalization.

This means Seed can preserve where data came from and which scrape target produced a sample, but it does not generalize that into “this endpoint-observed measurement describes host X.” The only specific bridge discovered is a source-derived `prometheus_instance` fact for stable nodename-to-instance knowledge; repository tests show that bridge is not measurement ownership and not endpoint measurement reachability from the host.

## Example evaluation

| Example | Current subject | Entity being described under current repository authority | Same thing? | Evidence-based interpretation |
|---|---|---|---|---|
| Filesystem measurements | Prometheus `instance` endpoint for Prometheus source, e.g. `192.168.254.115:9100`; local inventory may record local filesystem topology directly on a host subject. | For Prometheus measurements, Seed currently only authorizes the endpoint-shaped measurement subject plus mount/device/fstype dimensions. It does not separately assert the stable host owner. | For Prometheus: not necessarily. They are operationally about a node-exporter target's visible filesystem, but the model does not re-own them to the host. | Host-owned filesystem facts would require an explicit new projection or ownership relation; alias knowledge alone is intentionally insufficient. |
| `availability_status` | The subject of the source observation or derived canonical fact. Prometheus `up` becomes endpoint-scoped `availability_status` on the endpoint. | The availability of the measured subject. For Prometheus `up`, repository evidence treats this as endpoint scrape availability, not host availability. | For endpoint scrape availability: yes, the described entity is the endpoint/scrape target. For a direct host availability fact: yes for that host. Across endpoint-to-host: no. | State Summary separates endpoint scrape availability, host availability, and service availability. |
| `up` | Raw Prometheus `instance` endpoint. | Raw provider-specific scrape-target status; canonicalized to endpoint-scoped `availability_status`. | Yes for the scrape endpoint; no for a stable host unless separately asserted. | Tests assert `node115 up` remains unknown while `192.168.254.115:9100 up` is current. |
| `health_status` | Same subject as the supporting `availability_status` when inferred, or the direct fact subject when observed. | Health of the same measured subject. Endpoint availability infers endpoint health, not host health. | Yes within the subject; no across endpoint-to-host. | Inference rules preserve the source fact subject. Tests assert endpoint health does not become host health through `prometheus_instance`. |
| `endpoint_role` | Endpoint subject for Prometheus `up{job=...}`; arbitrary subject for non-Prometheus direct facts. | Role/capability label of that endpoint when Prometheus-derived. Non-Prometheus facts may project `provides`. | For Prometheus endpoint roles, yes: it describes the endpoint, not host ownership or service ownership. | Relationship projection suppresses Prometheus `endpoint_role -> provides` to avoid treating endpoint labels as general capability ownership. |

## Host-owned filesystem facts and existing boundaries

Host-owned filesystem facts would **not inherently violate** existing repository boundaries if they were introduced as explicit, evidence-bearing facts or as a separately named projection with clear provenance and caveats. Seed already supports direct facts on host subjects when a source actually observes host-scoped inventory.

Host-owned filesystem facts **would violate** existing boundaries if they were produced by silently treating `prometheus_instance` as an alias, by allowing endpoint/non-endpoint alias collapse, by changing current-facts lookup to cross the endpoint boundary, or by making storage projection reinterpret endpoint subjects as hosts without an explicit ownership relation. Those routes would contradict tests and comments that preserve endpoint visibility separate from host ownership.

## Candidate missing concepts

The repository appears to be missing a general concept in this family:

```text
measurement owner
observation target
observed entity
described entity
ownership relation
```

However, this audit does **not** conclude that Seed must add one. It concludes only that current code lacks a general modeled distinction and that existing alias/relationship/projection mechanisms intentionally do not provide it implicitly.

The strongest evidence that a concept may be missing is the mismatch between endpoint-observed metrics that humans often read as host resource facts and Seed's current subject-only measurement model. The strongest evidence against adding the concept prematurely is that repository boundaries deliberately prevent endpoint visibility from becoming host ownership without explicit semantics.

## Affected surfaces

- **Measurement predicate handling:** classifies volatile predicates and keeps latest current samples per subject/predicate/dimensions.
- **Alias construction:** excludes `prometheus_instance` and blocks endpoint/non-endpoint alias collapse.
- **Relationship projection:** can project topology relationships, but suppresses Prometheus-derived `prometheus_instance -> monitored_by` and `endpoint_role -> provides` relationships.
- **Prometheus normalization/ingestion:** emits Prometheus samples on `instance` subjects; only `node_uname_info` carries stable host identity metadata.
- **Availability handling:** `up` normalizes to `availability_status`; endpoint-scoped lookup and State Summary availability scopes keep scrape availability separate from host/service availability.
- **Endpoint-role handling:** Prometheus jobs produce endpoint role facts but do not imply host/service/capability ownership.
- **Current-facts lookup:** query ownership follows subject plus permitted aliases; endpoint-scoped predicates force exact lookup.
- **Storage projection:** groups filesystem rows by canonical fact subject and dimensions; it does not resolve endpoint subjects to host owners.
- **Entity identity projection:** endpoint-shaped fact subjects become endpoint type assertions; host predicates assert hosts; aliases remain constrained.
- **Future lenses/views:** Storage, Availability, Node Detail, and HomeOps surfaces would need either to operate honestly on endpoint visibility or to wait for explicit ownership semantics if they intend to speak about host-owned resources.

## Risks

1. **Silent ownership transfer risk:** changing aliases or current-facts lookup would make endpoint measurements appear host-owned without evidence.
2. **UI mislabeling risk:** naming endpoint-subject filesystem rows as `host` rows can imply more ownership than the model contains.
3. **Availability overclaim risk:** endpoint scrape availability can be mistaken for host or service health unless scoped.
4. **Relationship overprojection risk:** Prometheus labels can look like service/capability ownership but are intentionally suppressed today.
5. **Lens ambiguity risk:** future dashboards could mix endpoint visibility and host ownership unless their authority boundaries are explicit.

## Recommendation

Do not implement fixes as part of this audit.

Recommended next investigation: design-space audit for whether Seed needs an explicit read-only ownership/observation-target concept, with candidate names and invariants compared against current endpoint identity boundaries. That investigation should answer whether any future Storage Lens, Availability Lens, Node Detail View, or HomeOps View needs to say “host-owned” at all, or whether endpoint visibility plus provenance is sufficient for their first usable versions.

If a future design chooses host-owned filesystem facts, it should be explicit and evidence-bearing. Candidate safe shapes include a separate projection field such as `observed_subject` plus `described_entity`, or a cataloged relationship with provenance and strict source rules. Candidate unsafe shapes include expanding alias predicates, treating `prometheus_instance` as identity, or making current-facts lookup cross endpoint/non-endpoint boundaries.

## Non-conclusions

- This audit does not conclude that HomeOps should display host-owned storage.
- This audit does not conclude that Storage Lens, Availability Lens, Node Detail View, or HomeOps View must exist.
- This audit does not conclude that endpoint-owned Prometheus measurements are wrong.
- This audit does not conclude that aliases should bridge host and endpoint identity.
- This audit does not conclude that current-facts lookup should change.
- This audit does not conclude that storage projection should change.
- This audit does not conclude that Prometheus ingestion should attach filesystem samples to hosts.
- This audit does not conclude that a measurement-owner concept is definitely needed; it identifies that no general concept currently exists and that future lens requirements determine whether one is necessary.

# Prometheus Acquisition, Interpretation, Routing, And Promotion Audit

## Purpose

This document performs a documentation-only audit of how Prometheus observations currently move through Seed from acquisition through interpretation, candidate derivation, routing, and promotion.

This is an implementation-boundary audit. It is bound to the current implementation and does not introduce new runtime behavior.

The audit tests whether the current implementation preserves this architecture:

```text
Observation
        ↓
Interpretation
        ↓
Candidates
        ↓
Routing
        ↓
Promotion
```

Recent boundary work established that:

```text
Interpretation answers:
    what meaning may be present?

Routing answers:
    which boundary should consider it?

Promotion answers:
    what structured object is created?
```

The central question is whether Prometheus support keeps those decisions separate, or whether acquisition, normalization, relationship projection, and state projection still collapse them.

---

## Scope

In scope:

- Prometheus acquisition through `PrometheusObservationSource`.
- Observation normalization that affects Prometheus-derived subjects, predicates, and aliases.
- Predicate canonicalization of Prometheus observations.
- Observation-to-evidence and observation-to-fact ingestion.
- Relationship projection from Prometheus-relevant predicates.
- Entity type projection affected by Prometheus facts and relationships.
- State query behavior that can make endpoint facts appear as host facts.
- Tests that document the currently expected behavior.
- Comparison against the existing Prometheus boundary audits.

---

## Non-goals

This audit does not:

- Implement code.
- Modify schemas.
- Modify runtime behavior.
- Modify ontology definitions.
- Modify projections.
- Modify authority systems.
- Modify tests.
- Introduce new runtime semantics.
- Choose final vocabulary for endpoint, scrape-target, or monitoring topology relationships.
- Redesign Prometheus ingestion.

---

## Files inspected

Implementation files inspected:

- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/observations.py`
- `seed_runtime/predicate_normalizers.py`
- `seed_runtime/state.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/inference_rules.py`
- `relationship_catalog/core.json`
- `predicate_catalog/core.json`
- `capability_catalog/prometheus_query.yml`

Tests inspected for implementation intent:

- `tests/test_observation_sources.py`
- `tests/test_observation_normalizers.py`
- `tests/test_relationship_catalog.py`
- `tests/test_state_projector.py`
- `tests/test_graph_validation.py`

Prior Prometheus documents inspected:

- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/prometheus_endpoint_identity_boundary_audit.md`
- `docs/prometheus_target_and_filesystem_identity_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`

---

## Current implementation flow

The current Prometheus path is:

```text
Prometheus HTTP API vector result
        ↓
PrometheusObservationSource._observations_from_query
        ↓
Observation(subject=instance, predicate=derived Seed predicate, value=sample value)
        ↓
ObservationCollectionService._normalize_observation
        ↓
DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE
        ↓
EndpointAliasNormalizer
        ↓
EndpointIdentityNormalizer
        ↓
PredicateNormalizer
        ↓
ObservationIngestor.ingest
        ↓
observation.observed event
        ↓
evidence.observed event
        ↓
fact.observed or fact.inferred event
        ↓
StateProjector
        ↓
relationship projection, entity type projection, fact support, inferred facts, views
```

The important boundary issue is that the flow has no explicit candidate layer. Derived observations are inserted back into the same observation stream and are then promoted into facts like ordinary observations.

---

## Acquisition findings

### 1. Prometheus data is acquired by a read-only HTTP source

`PrometheusObservationSource` is the direct acquisition surface. It performs HTTP GET requests against a fixed safe query list:

```text
up
node_uname_info
node_filesystem_avail_bytes
node_filesystem_size_bytes
```

The source builds `/api/v1/query?query=<metric>` requests, requires successful Prometheus vector responses, and returns an empty observation list if the source is unreachable or malformed.

### 2. The acquired unit is a vector sample, but the promoted observation subject is the `instance` label

For each Prometheus vector sample, the implementation requires a non-empty string `metric.instance`. If absent, the sample is skipped.

The `instance` label becomes `Observation.subject` for all Prometheus metrics currently ingested. This means the implementation treats the scrape-target identifier as the immediate Seed subject.

### 3. Metric-family interpretation happens during acquisition

Acquisition does not merely preserve raw samples. It maps metric families into Seed predicates immediately:

- `up` with a `job` label emits `endpoint_role = <job>`.
- `up` emits `up = int(sample_value)`.
- `node_uname_info` emits `os = <sysname-derived value>`.
- `node_filesystem_avail_bytes` emits `filesystem_avail_bytes = int(sample_value)`.
- `node_filesystem_size_bytes` emits `filesystem_size_bytes = int(sample_value)`.

This means acquisition already performs interpretation. It decides that a Prometheus `job` label is an endpoint role and that `node_uname_info.sysname` is an OS fact on the `instance` subject.

### 4. Evidence preserved at acquisition is useful but incomplete for boundary separation

Prometheus observations preserve:

- Collector name.
- Source name `prometheus`.
- Prometheus base URL.
- Prometheus metric name.
- Full metric label set.
- Read-only flag.
- HTTP method.
- Observation source name added by collection service.
- Observation timestamp generated at collection time.
- Filesystem dimensions for filesystem measurements: `mountpoint`, `device`, and `fstype`.

For `node_uname_info`, acquisition additionally copies selected labels into first-class metadata:

- `instance`.
- `nodename`, when present.

This preserves enough provenance to audit many decisions later, but it does not create a separate scrape-target object, candidate host object, endpoint candidate object, or routing decision record.

### 5. Prometheus sample timestamp is not preserved as the observation timestamp

Prometheus vector samples include a value pair whose first element is a timestamp. The implementation reads `value[1]` as the sample value but uses a single `datetime.now(timezone.utc)` collection timestamp for every query in the collection run.

That is safe as a collection-time observation, but it means the original Prometheus sample timestamp does not survive as a distinct provenance field.

---

## What is treated as the observation?

Current implementation treats a derived Seed observation as the observation, not the raw Prometheus sample.

| Possible observation boundary | Current behavior |
| --- | --- |
| Raw metric sample | Preserved only indirectly in metadata labels plus converted value. The raw sample object is not stored as the observation. |
| Metric family | Used to choose Seed predicates during acquisition. |
| Instance label | Used as `Observation.subject`; this is the strongest current subject boundary. |
| Target label | Preserved inside `metric_labels`; not promoted separately unless it is also `instance`. |
| Scrape result | `up` is converted to an `up` observation and then canonicalized to `availability_status`. |
| Derived observation | Yes. `endpoint_role`, `os`, filesystem measurements, `prometheus_instance`, aliases, and canonical predicates are represented as observations and then facts. |

The result is:

```text
Prometheus vector sample
        ↓
Seed observation with subject=instance
```

The raw observation boundary is therefore already narrower and more interpreted than a Prometheus response sample.

---

## Evidence findings

Evidence is created by `ObservationIngestor.observation_to_evidence`. It records:

- Observation ID.
- Source type.
- Subject.
- Predicate.
- Value.
- Metadata.
- Dimensions.
- Expiration.
- Confidence.
- Observed-at timestamp.

Because Prometheus metadata contains `metric_labels`, the original label set survives inside evidence payloads. Because collection service adds `observation_source`, the configured source name also survives.

Evidence does not independently preserve:

- The complete HTTP response.
- The original Prometheus sample timestamp as separate from Seed collection time.
- A first-class scrape target identity object.
- A first-class interpretation decision.
- A first-class routing decision.
- Candidate subject or candidate relationship records.

---

## Interpretation findings

### 1. Interpretation occurs in the source adapter

Prometheus acquisition interprets metric-family meaning immediately. The source adapter chooses Seed predicates and subjects before the observation reaches the ingestion layer.

Examples:

```text
up + job label
        ↓
endpoint_role fact candidate

node_uname_info + sysname label
        ↓
os fact candidate

node_filesystem_* metric
        ↓
filesystem measurement fact candidate
```

This is interpretation before any explicit candidate or routing layer.

### 2. Interpretation occurs in endpoint alias normalization

`EndpointAliasNormalizer` interprets metadata with `hostname` or `nodename` plus `instance` or `endpoint` as enough to derive a source-specific instance predicate. For Prometheus, `source_name=prometheus` produces:

```text
subject=<nodename>
predicate=prometheus_instance
value=<instance endpoint>
```

This is a derived observation, not a candidate. It is later ingested as a fact and projected into relationships.

### 3. Interpretation occurs in endpoint identity normalization

`EndpointIdentityNormalizer` interprets any subject that looks like `host:port` as an endpoint. If the endpoint base matches known `ip_address`, `ansible_host`, or `alias` evidence, it derives:

```text
subject=<known identity subject>
predicate=alias
value=<endpoint>
```

This directly interprets a base host/IP identity match as identity equivalence with the endpoint string.

### 4. Interpretation occurs in predicate normalization

`PredicateNormalizer` interprets Prometheus-specific predicates through the predicate catalog. Notably:

```text
prometheus/up 1
        ↓
availability_status up

prometheus/filesystem_avail_bytes
        ↓
filesystem_free_bytes

prometheus/filesystem_size_bytes
        ↓
filesystem_total_bytes
```

It leaves raw observations intact and adds canonical derived observations. That is useful for traceability, but the canonical observation is then promoted as an observed fact.

### 5. Interpretation occurs in entity type projection

Entity type projection interprets host-looking and endpoint-looking facts:

- A fact whose predicate is in host predicates asserts the subject is a host.
- A subject shaped like `host:port` asserts endpoint type.
- Relationship objects can assert types, such as `prometheus` as a monitoring system and `node-exporter` as a capability.

This means typing may be derived after facts and relationships already exist, rather than before routing.

---

## Candidate subject findings

Candidate subjects are not explicitly represented.

The implementation has these concrete subjects:

- Observed `instance` label as `Observation.subject`.
- Derived `nodename` subject for `prometheus_instance` observations.
- Known identity subject for derived `alias` observations.
- Fact subject after ingestion.
- Relationship subject after projection.
- Entity type assertion subject after projection.

It does not distinguish these as separate candidate stages:

```text
observed identifier
candidate scrape target
candidate endpoint
candidate host
candidate service
candidate monitoring system
```

Because there is no explicit candidate subject object, the first chosen subject tends to become the promoted fact subject.

---

## Candidate relationship findings

Candidate relationships are not explicitly represented.

Relationships are projected directly from facts by `relationship_catalog/core.json` and `_project_catalog_relationships`. If a fact predicate matches a catalog definition, a relationship is produced.

Current Prometheus-relevant projections include:

```text
prometheus_instance
        ↓
alias_of

prometheus_instance
        ↓
monitored_by prometheus

endpoint_role
        ↓
provides
```

There is no intermediate representation for:

```text
candidate endpoint_of
candidate has_endpoint
candidate scraped_by
candidate monitored_by
candidate provides
candidate endpoint_exposes
candidate alias_of
```

Therefore relationship selection happens at promotion time, not in a prior routing stage.

---

## Routing findings

Routing is currently implicit and distributed.

### 1. Fact routing is mostly subject/predicate assignment

The source adapter routes observations by assigning a Seed predicate and subject. For example, filesystem measurements and OS facts are routed to the `instance` subject. The system does not first ask whether the subject should be host, endpoint, scrape target, filesystem, or measurement scope.

### 2. Predicate normalization routes by catalog mapping

Prometheus `up` is routed to `availability_status` by predicate catalog mapping. The mapping preserves subject and dimensions. It does not route based on whether the subject is endpoint-scoped or host-scoped.

### 3. Relationship routing is catalog-driven

Relationship projection routes facts to relationships exclusively by predicate match and catalog definition. For example, `endpoint_role` always routes to `provides`, and `prometheus_instance` routes to both `alias_of` and `monitored_by`.

### 4. Entity type routing is projection-derived

Entity types are inferred after facts and relationships exist. This can validate or warn, but it does not prevent earlier promotion into a mismatched relationship.

### 5. State query routing can cross endpoint and host boundaries through alias resolution

State lookup defaults can resolve aliases. Existing tests expect `state.get_best_fact("node115", "up")` to return the `up` fact attached to `192.168.254.115:9100` when a `prometheus_instance` or alias connection exists. This makes endpoint availability appear through a host query path.

---

## Promotion findings

### 1. Observation-to-fact promotion is unconditional after validation

`ObservationIngestor.ingest` records the observation, creates evidence, converts the observation to a fact, and appends the fact event. The ingestion path does not know whether the observation represents raw evidence, interpretation, candidate derivation, routing, or a promoted claim.

### 2. Relationship promotion is automatic from fact predicates

`_project_catalog_relationships` creates relationships directly from fact predicates and values. It does not record a candidate relationship decision or a routing reason beyond metadata that points back to the source predicate and fact.

### 3. Identity promotion occurs through `alias_of`

`prometheus_instance` is included in the `alias_of` derived predicates in the relationship catalog. The same predicate also creates `monitored_by prometheus`. This means one fact can promote both identity equivalence and monitoring dependency.

### 4. Projection creation follows promotion

Entity type assertions and relationship views are read-model projections. They are not separate authority systems, but they can make promoted facts feel more authoritative by exposing them as typed entities and graph edges.

---

## Boundary collapse findings

### Collapse 1: observation → promotion

Prometheus vector samples become Seed observations with interpreted predicates, and those observations are immediately promoted to facts. There is no durable distinction between:

```text
Prometheus reported a sample
```

and:

```text
Seed has a fact about the subject
```

The evidence link preserves provenance, but the promoted fact exists at the same structural level as other observed facts.

### Collapse 2: interpretation → promotion

The source adapter interprets `job` as `endpoint_role`, `sysname` as `os`, and filesystem metric families as filesystem measurements. The normalizers interpret `nodename + instance` as `prometheus_instance` and identity matches as `alias`. These interpretations are not represented as candidates; they become observations and then facts.

### Collapse 3: routing → promotion

Relationship routing is performed by relationship projection from already-promoted facts. The choice between `alias_of`, `monitored_by`, and `provides` is not made as a separate routing decision. It happens when the read model projects relationships.

### Collapse 4: host ↔ endpoint

The implementation intentionally avoids adding `instance` metadata to most Prometheus metrics so generic endpoint alias normalization is limited. However, `node_uname_info` still copies `instance` and `nodename` into metadata, which enables `prometheus_instance` derivation. The relationship catalog then treats `prometheus_instance` as `alias_of`, collapsing host-ish nodename and host:port endpoint identity.

### Collapse 5: host ↔ scrape target

The `instance` label is used as the subject for all raw Prometheus-derived observations. For host-shaped `instance` labels, this may be acceptable when corroborated. For host:port labels, this means endpoint/scrape-target identifiers receive host-like predicates such as `os` and canonicalized `availability_status`.

### Collapse 6: endpoint ↔ capability

`endpoint_role` projects to `provides`. This makes an endpoint with `job=node-exporter` become:

```text
<endpoint> provides node-exporter
```

and `node-exporter` becomes a capability through relationship type projection. This may be acceptable for some roles, but it collapses endpoint exposure, exporter role, service identity, and capability into one relationship vocabulary.

### Collapse 7: endpoint ↔ monitoring system

The existing `provides` relationship can express `localhost:9090 provides prometheus` if the `up.job` label is `prometheus`. Prior audits rejected that as a catch-all because `prometheus` can be a monitoring system rather than a capability. The current catalog still routes every `endpoint_role` to `provides`, so the implementation can still enter this shape.

### Collapse 8: endpoint reachability ↔ host availability

Prometheus `up` becomes `availability_status` through predicate normalization while preserving the endpoint subject. Endpoint-scoped inference is partly protected by endpoint-specific projection logic, but alias resolution can still make endpoint availability accessible as a best fact for a host-like alias subject.

---

## Identity collapse findings

### host:port → host identity

Current acquisition uses host:port `instance` labels as subjects. Host:port strings are typed as endpoints during entity type projection. However, `prometheus_instance` and alias normalizers can connect hostnames or known identities to host:port strings using identity-equivalence vocabulary.

Result:

```text
host:port does not literally become a host type by shape alone,
but it can become reachable through host identity aliases.
```

### instance label → alias_of

This behavior still exists. When `node_uname_info` provides `nodename` and `instance`, `EndpointAliasNormalizer` derives:

```text
node115 prometheus_instance 192.168.254.115:9100
```

The relationship catalog then projects:

```text
node115 alias_of 192.168.254.115:9100
node115 monitored_by prometheus
```

### endpoint observation → host fact attachment

This behavior partially remains. The source itself attaches Prometheus `os` and filesystem observations to the `instance` subject. If `instance` is `host:port`, those facts are endpoint-subject facts. If an alias or `prometheus_instance` relation connects that endpoint to a host-ish subject, state queries can surface endpoint facts through the host-ish subject.

The current implementation also has `_projection_subject` logic to keep endpoint-scoped predicates on exact endpoint subjects for some projection paths. This is a mitigation, not a complete candidate/routing boundary.

### endpoint exposure → provides

This behavior still exists. `up.job` becomes `endpoint_role`; `endpoint_role` projects directly to `provides`. Tests explicitly expect this projection.

### host ↔ scrape target

This behavior still exists for `prometheus_instance`. It is not a neutral relationship candidate; it creates identity and monitoring relationships.

### endpoint ↔ monitoring system

This behavior remains possible because `endpoint_role=prometheus` routes to `provides`. Separately, `prometheus_instance` routes to `monitored_by prometheus`, with `prometheus` typed as a monitoring system.

---

## Where existing Prometheus audits disagree with implementation

### `prometheus_observation_boundary_reconciliation.md`

The prior reconciliation says the Prometheus `instance` label is a contextual scrape-target identifier and is not host identity by default. The implementation agrees partially by keeping most raw Prometheus observations subject-scoped to `instance`, but disagrees when `prometheus_instance` is projected as `alias_of` and when endpoint facts are reachable through host-ish alias queries.

The prior reconciliation says endpoint facts should attach to endpoint subjects and host facts only to host subjects. The implementation attaches `up`, `endpoint_role`, and filesystem measurements to the `instance` subject; when `instance` is host:port, this is endpoint-scoped. However, `node_uname_info` also emits `os` on the `instance` subject, so a host fact can be attached to an endpoint subject.

### `prometheus_endpoint_identity_boundary_audit.md`

The prior endpoint audit says `alias_of` should mean identity equivalence and should not connect hostnames to host:port endpoints. The implementation still derives `prometheus_instance` from `nodename + instance`, and the catalog still maps `prometheus_instance` to `alias_of`.

The prior audit says `provides` is too broad for Prometheus exposure. The implementation still maps `endpoint_role` to `provides`.

The prior audit says `monitored_by` requires a host or explicitly scoped monitored entity. The implementation still maps `prometheus_instance` to `monitored_by prometheus`, regardless of whether the subject has independent host support.

### `prometheus_target_and_filesystem_identity_reconciliation.md`

The target/filesystem reconciliation says `up` is scrape-target evidence and filesystem metrics should not force storage identity. The implementation mostly preserves filesystem dimensions and does not create storage identity from filesystem metrics, but `up` still becomes generic `availability_status`, and alias resolution can surface that endpoint availability through host-like subjects.

---

## Risks

1. **False identity equivalence.** `alias_of` between a hostname and host:port endpoint can imply they are the same entity.
2. **Incorrect host availability.** Endpoint scrape success can be read as host availability through alias resolution.
3. **Incorrect host facts.** Host-like facts such as `os` can attach to an endpoint subject when `instance` is host:port.
4. **Over-broad capability claims.** `endpoint_role` can create `provides` relationships where the object is an exporter role, service label, or monitoring system rather than a capability.
5. **Relationship validation noise.** The graph may create warnings when `monitored_by` expects a host but receives an unknown or endpoint-derived subject.
6. **Loss of interpretation trace.** Derived observations preserve provenance but not the reasoning boundary that selected one interpretation over alternatives.
7. **No safe place for ambiguity.** Without candidate subjects and relationships, ambiguous Prometheus labels must either be ignored or promoted.

---

## Smallest safe cleanup path

This is not a redesign. The smallest safe path is to reduce the most harmful promotions while preserving existing acquisition value.

1. **Stop using `alias_of` for Prometheus host-to-endpoint evidence.** Do not let `prometheus_instance` imply identity equivalence between nodename/host identity and `host:port` endpoint.
2. **Keep Prometheus `instance` as scrape-target / endpoint-scoped evidence by default.** Treat host:port as endpoint identity, not host identity.
3. **Do not attach host-level facts to endpoint subjects without independent host routing.** `node_uname_info` can remain evidence, but `os` should not be promoted as a host fact on `host:port` without a host subject decision.
4. **Replace or quarantine `endpoint_role → provides` for Prometheus-derived endpoint roles.** If immediate vocabulary changes are too large, suppress only the Prometheus-derived `provides` projection or mark it as exposure candidate in a future-compatible way.
5. **Keep `up` endpoint-scoped.** Avoid resolving endpoint `availability_status` as host availability unless an explicit host availability rollup/projection exists.
6. **Prefer relationship candidates before identity promotion.** When host evidence and endpoint evidence coexist, derive a non-identity relation such as `endpoint_of` or `has_endpoint` in a future pass rather than aliasing.
7. **Preserve raw provenance before changing semantics.** Keep `metric_labels`, `prometheus_metric`, source, dimensions, and collection timestamps so existing data remains auditable.

The first safe implementation slice implied by existing findings is therefore:

```text
remove or narrow prometheus_instance → alias_of
remove or narrow endpoint_role → provides for Prometheus endpoint roles
prevent endpoint-scoped availability from satisfying host availability queries
keep acquisition and evidence preservation intact
```

---

## Rejected solutions

Rejected for this cleanup path:

1. **Redesign all Prometheus ingestion.** Too broad; the acquisition adapter already preserves useful provenance.
2. **Introduce a complete endpoint/service/monitoring ontology now.** Correct direction, but outside a smallest safe cleanup.
3. **Delete Prometheus support.** Unnecessary; the issue is boundary preservation, not acquisition itself.
4. **Treat every `instance` label as host identity.** Contradicts prior audits and Prometheus scrape semantics.
5. **Treat every `instance` label as only endpoint identity forever.** Too strict; bare host labels may be host candidates when corroborated.
6. **Silence relationship validation by weakening type rules.** This hides collapse rather than fixing it.
7. **Rename every existing predicate immediately.** Helpful eventually, but not required to stop the most harmful identity and relationship promotions.

---

## Direct answers

### 1. Where is Prometheus data acquired?

Prometheus data is acquired in `PrometheusObservationSource` in `seed_runtime/observation_sources.py`. It queries the Prometheus HTTP API with safe allowlisted instant queries and converts vector samples into Seed observations.

### 2. What is treated as the observation?

The implementation treats an interpreted Seed `Observation` as the observation. The subject is the Prometheus `instance` label. Metric family controls the Seed predicate. The raw Prometheus sample is not stored as the canonical observation object.

### 3. What evidence is preserved?

Evidence preserves source type, subject, predicate, value, metadata, dimensions, confidence, observed time, expiration, and observation ID. Prometheus metadata preserves source name, base URL, metric name, full metric label set, read-only status, HTTP method, and collection source name. Filesystem dimensions preserve `mountpoint`, `device`, and `fstype`.

### 4. Where does interpretation occur?

Interpretation occurs in:

- `PrometheusObservationSource._observations_from_query`.
- `EndpointAliasNormalizer`.
- `EndpointIdentityNormalizer`.
- `PredicateNormalizer`.
- Entity type projection in `state.py`.
- Relationship projection through `relationship_catalog/core.json` plus `_project_catalog_relationships`.

### 5. Are candidate subjects explicitly represented?

No. Observed identifiers, candidate hosts, candidate endpoints, candidate services, and candidate monitoring systems are not represented as separate candidate objects. The chosen observation subject becomes the fact subject.

### 6. Are candidate relationships explicitly represented?

No. Relationship candidates do not exist prior to promotion. Relationships are projected directly from promoted facts.

### 7. Where does routing occur?

Routing is implicit:

- Source adapter subject/predicate assignment routes facts.
- Predicate catalog mappings route canonical facts.
- Relationship catalog mappings route relationships.
- Entity type projection routes types after the fact.
- Alias-aware state queries can route endpoint facts to host-like query subjects.

### 8. Where does promotion occur?

Promotion occurs in:

- `ObservationIngestor.ingest`, which promotes observations to evidence and facts.
- `PredicateNormalizer`, `EndpointAliasNormalizer`, and `EndpointIdentityNormalizer`, which promote interpretations into derived observations that later become facts.
- `_project_catalog_relationships`, which promotes fact predicates into relationships.
- Entity type projection, which promotes facts and relationships into type assertions in the read model.

### 9. Where are boundaries collapsed?

Boundaries collapse at:

- Acquisition, where Prometheus samples become interpreted Seed observations.
- Normalization, where interpretations become derived observations.
- Ingestion, where observations become facts without candidate/routing records.
- Relationship projection, where facts become `alias_of`, `monitored_by`, and `provides` relationships directly.
- Alias-aware fact lookup, where endpoint facts can satisfy host-like subject queries.

### 10. Where are identities collapsed?

Identities collapse at:

- `nodename + instance → prometheus_instance`.
- `prometheus_instance → alias_of`.
- `identity subject + endpoint → alias` in `EndpointIdentityNormalizer`.
- `endpoint_role → provides`, which can collapse endpoint exposure and capability/service/monitoring meaning.
- Alias resolution, which can make endpoint availability appear as host availability.

### 11. Where do existing Prometheus audits disagree with implementation?

They disagree where the implementation still:

- Maps `prometheus_instance` to `alias_of`.
- Maps `endpoint_role` to `provides`.
- Lets `prometheus_instance` imply `monitored_by prometheus` without an explicit monitored-entity routing boundary.
- Allows `node_uname_info` to attach `os` to an `instance` subject that may be an endpoint.
- Allows endpoint `up` / `availability_status` to be read through host-like aliases.

### 12. What is the smallest safe cleanup path?

The smallest safe cleanup path is to keep Prometheus acquisition and provenance intact while narrowing promotion:

1. Remove or restrict `prometheus_instance → alias_of`.
2. Remove or restrict Prometheus-derived `endpoint_role → provides`.
3. Keep `up` / `availability_status` endpoint-scoped until an explicit host availability projection exists.
4. Prevent host facts such as `os` from attaching to endpoint subjects without independent host routing.
5. Add relationship candidates or neutral endpoint relationships only after the harmful identity promotions are stopped.

---

## Required report

### Files changed

- `docs/prometheus_acquisition_interpretation_routing_promotion_audit.md`

### LOC changed

- 778 lines added (new documentation file).

### Implementation files inspected

- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/observations.py`
- `seed_runtime/predicate_normalizers.py`
- `seed_runtime/state.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/inference_rules.py`
- `relationship_catalog/core.json`
- `predicate_catalog/core.json`
- `capability_catalog/prometheus_query.yml`

### Major findings

- Prometheus acquisition is read-only and allowlisted, but it interprets metric families immediately.
- The Prometheus `instance` label is the dominant observation subject.
- Provenance is mostly preserved through metadata and evidence payloads.
- Candidate subjects and candidate relationships are not explicit implementation objects.
- Routing is implicit in source mapping, predicate mapping, relationship catalog mapping, entity type projection, and alias-aware query behavior.
- Promotion occurs directly from observations to facts and from facts to relationships.

### Identified collapse points

- Observation to fact.
- Interpretation to derived observation to fact.
- `prometheus_instance` to `alias_of`.
- `prometheus_instance` to `monitored_by prometheus`.
- `endpoint_role` to `provides`.
- `up` to generic `availability_status`.
- Endpoint fact lookup through host-like aliases.
- `node_uname_info` host facts attached to `instance` subjects.

### Smallest safe cleanup path

- Preserve acquisition and evidence.
- Stop or narrow identity-equivalence promotion from Prometheus instance evidence.
- Stop or narrow Prometheus endpoint role promotion to `provides`.
- Keep endpoint availability separate from host availability.
- Avoid host fact attachment to endpoint subjects without explicit routing.
- Add neutral relationship candidates only after the most harmful current promotions are reduced.

### Documents intentionally left unchanged

- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/prometheus_endpoint_identity_boundary_audit.md`
- `docs/prometheus_target_and_filesystem_identity_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- All tests.
- All runtime implementation files.
- All schema, ontology, projection, predicate, relationship, capability, and authority definitions.

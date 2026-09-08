# Expression Identity Convergence Investigation

## Scope

This is a bounded implementation investigation into whether Seed currently distinguishes:

```text
independent expressions
↓
identity convergence
↓
subject identity
```

It does not recover ownership, redesign entities, redesign ontology, introduce identity abstractions, introduce automation, or recommend implementation changes. Repository implementation is treated as authority.

## Implementation evidence reviewed

Primary implementation evidence reviewed:

- `seed_runtime/observations.py` — canonical observations, observation ingestion, evidence creation, and fact promotion.
- `seed_runtime/evidence.py` — provenance evidence model.
- `seed_runtime/facts.py` — fact and fact-support models.
- `seed_runtime/state.py` — state projection, alias resolution, fact support aggregation, conflict detection, relationships, and downstream query behavior.
- `seed_runtime/observation_normalizers.py` — endpoint alias and endpoint identity normalization before ingestion.
- `seed_runtime/observation_sources.py` — local host and hosts-file observation boundaries.
- `seed_runtime/ansible_inventory_source.py` — imported host identity observations.
- `seed_runtime/knowledge/*` — repository/relationship/documentation/self-model observation paths.
- Tests covering observation normalization, observation ingestion, fact support, state projection, alias behavior, state summary views, and self-model alignment.

## Expression sources

Current implementation has several independently acquired expression sources:

1. **Canonical observations.** `Observation` carries a source type, observed time, subject, predicate, value, confidence, metadata, dimensions, and expiry. This is the canonical expression shape used by ingestion.
2. **Evidence.** Ingestion converts each observation into an `Evidence` record whose payload preserves the observation id, source type, subject, predicate, value, metadata, dimensions, and expiry.
3. **Facts.** Ingestion generally converts an observation into a `Fact` by copying `observation.subject` into `Fact.subject_id`, copying predicate/value/dimensions/confidence/expiry, and linking the generated evidence id.
4. **Source adapters.** Source adapters emit observations from repository artifacts, local host discovery, systemd, Prometheus, Ansible inventory, and repository/package/relationship scans. These adapters often preserve source-specific metadata rather than immediately asserting durable subject identity.
5. **Projected state.** The projector replays observations/evidence/facts into state and then finalizes alias resolver, measurement retention, inferred facts, fact supports, relationships, entity type assertions, graph issues, materialized aliases, and conflicts.

## Findings

### 1. Where independent implementation expressions first converge

There are two different convergence points, not one universal identity stage.

#### 1.1 Observation-normalization convergence before ingestion

The earliest explicit convergence occurs in observation normalization for endpoint-like expressions. `EndpointAliasNormalizer` groups observations by source type, stable host name, alias predicate, and endpoint, then emits a single derived alias observation with provenance back to the source observations. This is expression-level convergence: multiple observed expressions can cause one derived alias observation, but the original observations remain present.

`EndpointIdentityNormalizer` is a second pre-ingestion convergence path. It collects identity evidence from current batch observations and, when supplied, projected state facts. It matches explicit identity predicates (`ip_address`, `ansible_host`, `alias`) against endpoint base identities and emits an alias observation only when an explicit identity value matches the endpoint base.

Supported conclusion: independent endpoint expressions can first converge during observation normalization, but only for the explicit endpoint alias/identity cases implemented by those normalizers.

#### 1.2 Projection-time alias convergence after fact replay

The durable subject convergence point is projection finalization through `AliasResolver`. It builds connected components from explicit alias-like facts, chooses a deterministic canonical name for each component, records alias sets, and materializes `EntityAlias` records. Projection runs alias construction before measurement retention and inference, then runs it again after inference so inferred alias facts can participate before downstream projections.

Supported conclusion: subject-level convergence for current facts and downstream projected state primarily occurs in `StateProjector` finalization through `AliasResolver`, not during observation ingestion.

### 2. Whether implementation distinguishes expression identity from subject identity

Implementation partially distinguishes them.

- Observation ingestion preserves each observation as its own event and evidence record, and then generally creates one fact from that observation. This keeps expression identity visible through observation id and evidence id.
- Subject identity is not created by the `Observation` or `Fact` constructors. `Observation.subject` becomes `Fact.subject_id` directly. That means ingestion assumes the submitted subject string for the fact, while projection may later resolve aliases for query/support purposes.
- Alias-derived observations are still observations. Tests prove original endpoint observations remain endpoint-scoped even when a derived alias observation exists; querying the host for the endpoint measurement returns nothing while querying the endpoint returns the fact.
- `AliasResolver` creates canonical alias components from explicit alias facts. That is a projection-time subject convergence mechanism, distinct from the original expression records.

Supported conclusion: the implementation distinguishes individual expression records from projected subject convergence in important places, but the distinction is compressed. There is no general object named “candidate identity” or “identity convergence” separating expression identity from subject identity across all sources.

### 3. What implementation evidence justifies treating multiple expressions as one subject

Current implementation requires explicit alias-like evidence.

The strongest implementation evidence is:

- Alias predicates are enumerated as `alias`, `ip_address`, and `hostname`, plus source instance predicates ending in `_instance` except `prometheus_instance`.
- `AliasResolver` ignores facts that are not alias predicates, ignores alias values that cannot be read as relationship objects, and refuses alias edges crossing endpoint/non-endpoint boundaries.
- Alias edges are treated as an undirected graph; connected components become alias sets, and each component receives a deterministic canonical name.
- Fact support and conflict projection can use canonical subjects, meaning facts attached to different alias names can be treated as claims about one subject when alias resolution is enabled.
- Tests show explicit `ip_address` and `ansible_host` observations can cause endpoint identity alias derivation, while unrelated IP values do not.

Supported conclusion: the implementation justifies subject convergence with explicit alias-like facts or explicitly derived alias observations carrying provenance. It does not justify convergence from semantic similarity, naming resemblance, package names, relationship proximity, or presentation vocabulary alone.

### 4. When implementation intentionally refuses convergence

Implementation intentionally refuses convergence in several places:

1. **No metadata match, no endpoint alias.** `EndpointAliasNormalizer` skips observations without host/nodename metadata, without endpoint/instance metadata, or where the stable name equals the endpoint.
2. **No explicit identity match, no endpoint identity alias.** `EndpointIdentityNormalizer` only derives aliases from identity predicates and endpoint base matches. Tests prove unrelated IP observations do not merge and the implementation does not guess node numbers.
3. **Endpoint/non-endpoint boundary.** `AliasResolver` refuses alias facts that would equate an endpoint-shaped subject with a non-endpoint subject.
4. **`prometheus_instance` is excluded from alias predicates.** `_is_alias_predicate` accepts `_instance` predicates except `prometheus_instance`, and tests prove a Prometheus instance fact does not resolve endpoint measurements to a host subject.
5. **Endpoint-scoped predicates disable alias resolution.** `get_fact_supports` disables alias resolution for endpoint-scoped predicates.
6. **Exact-mode queries can disable alias resolution.** `resolve_fact_subjects` returns only the requested subject when alias resolution is disabled.
7. **Hosts-file observations are scoped configuration evidence, not identity assertions.** Hosts-file metadata explicitly marks DNS validity, reachability, uniqueness, alias equivalence, endpoint identity, and host identity as not asserted.

Supported conclusion: current implementation is conservative about subject convergence. It prefers to keep expressions separate unless specific alias/identity evidence exists and unless endpoint scoping says not to merge.

### 5. Where subject identity is actually created

There are two relevant meanings of “subject identity” in implementation:

1. **Fact subject identity is assigned at fact creation.** `ObservationIngestor.observation_to_fact` copies `observation.subject` into `Fact.subject_id`. This creates the persisted fact subject string without resolving aliases.
2. **Projected subject identity is created by alias projection.** `AliasResolver` builds alias components and canonical names from facts. This does not rewrite original fact subjects; it creates a projected resolver used by query, support, measurement retention, conflict handling, and alias materialization.

Entity creation is separate. `entity.upserted` events populate `state.entities` with `Entity` records, but reviewed implementation evidence does not show entity upsert as the general convergence mechanism for observation/fact subjects. `resolve_fact_subjects` can consult entity ids/names/aliases for query matching, but fact subjects are still fact subjects and alias resolver remains the explicit convergence mechanism for alias facts.

Supported conclusion: persisted subject strings are created at ingestion/fact creation; projected subject identity convergence is created during state projection by alias resolution.

### 6. Downstream responsibilities that depend on subject identity

Downstream responsibilities depending on subject identity include:

- **Current fact selection.** `get_best_fact`, `get_current_facts`, and `get_fact_supports` use resolved subjects and canonical subjects unless alias resolution is disabled or endpoint scoping prevents it.
- **Fact support aggregation.** `_project_fact_supports` groups facts by subject, predicate, dimensions, and value, optionally using a canonical subject key.
- **Measurement history retention.** Projection retention keys measurement samples by projected subject so measurement history is bounded per subject/predicate/dimensions while preserving endpoint-scoped separation.
- **Conflict detection.** `_project_fact_conflicts` groups non-measurement, non-multi facts by canonical subject and predicate/dimensions before comparing values.
- **Relationships and graph validation.** Catalog and legacy relationships are projected from fact subjects and objects, while alias relationships are suppressed when they would self-link or cross endpoint boundaries.
- **Entity alias visibility.** `state.entity_aliases` materializes explicit alias edges from the resolver for downstream surfaces.
- **State summaries and operational views.** State summary tests rely on alias state being preserved without automatically converting endpoint availability into host availability.

Supported conclusion: downstream reasoning and views depend on subject identity, but not uniformly. Some paths use exact fact subjects, some use alias-resolved subjects, and endpoint-scoped paths deliberately preserve separation.

### 7. Whether implementation supports a recurring identity convergence responsibility

Yes, but boundedly and unevenly.

Implementation evidence supports a recurring responsibility around explicit alias/identity convergence:

- Normalizers derive alias observations from multiple expressions before ingestion.
- Ingestion preserves observations/evidence/facts independently instead of overwriting source expressions.
- Projection builds alias components from explicit alias-like facts.
- Queries, fact supports, conflicts, measurements, relationships, and views consume either exact subjects or alias-resolved subjects depending on predicate and query options.
- Tests repeatedly prove both convergence and non-convergence cases.

However, implementation evidence does not support a fully generalized recurring transition equivalent to:

```text
Independent expressions
↓
Candidate identity
↓
Identity convergence
↓
Subject
↓
Downstream reasoning
```

The implementation does not expose a general candidate-identity stage. It has endpoint alias derivation, endpoint identity derivation, alias fact projection, entity aliases, and fact-support grouping. Those are related but not unified into one generalized identity-convergence subsystem.

Best implementation vocabulary for the supported responsibility:

> explicit alias/identity projection

This vocabulary is better supported than “ownership recovery,” “entity redesign,” or “ontology redesign.” It matches implementation names such as `EndpointAliasNormalizer`, `EndpointIdentityNormalizer`, `AliasResolver`, `EntityAlias`, `alias_resolver`, `entity_aliases`, and alias-like facts.

## Counterexamples and limiting evidence

### Observations can remain permanently independent

Tests prove that a derived alias observation does not cause endpoint measurements to become host facts. The original endpoint observation remains queryable by endpoint, not by host. This is a direct counterexample to a general “same underlying thing” merge at ingestion.

### Subject identity can be assumed rather than recovered

`ObservationIngestor.observation_to_fact` copies `Observation.subject` directly into `Fact.subject_id`. If a source emits a subject string, ingestion treats that string as the fact subject. Alias recovery may occur later, but ingestion itself does not recover subject identity.

### Downstream reasoning can happen without subject convergence

Fact support projection can run without a `subject_key`, grouping by exact `fact.subject_id`. Exact queries can disable alias resolution. Endpoint-scoped predicates force alias resolution off. Therefore downstream reasoning is not always preceded by subject convergence.

### Multiple unrelated convergence mechanisms exist

Endpoint alias normalization, endpoint identity normalization, entity alias resolution, entity model aliases, fact support aggregation, relationship projection, and self-model/repository reconciliation all handle different expression-to-state boundaries. The reviewed implementation does not provide one general convergence mechanism spanning them all.

### Identity inferred without enough evidence is intentionally blocked in some areas

Hosts-file observations explicitly mark that they do not assert alias equivalence, endpoint identity, host identity, host uniqueness, reachability, or DNS truth. Prometheus instance facts are deliberately not alias predicates. Endpoint/non-endpoint alias edges are refused.

## Direct answers to central questions

### 1. Where do independent implementation expressions first converge?

For endpoint-related observations, they first converge in `EndpointAliasNormalizer` and `EndpointIdentityNormalizer` before ingestion. For durable projected subject identity, they converge in `AliasResolver` during `StateProjector` finalization. For many other expression sources, no general first convergence point was found.

### 2. Does implementation distinguish expression identity from subject identity?

Partially. Observations, evidence, and facts preserve expression/provenance identity, while alias resolver creates projected subject convergence later. But the distinction is compressed because facts receive `subject_id` directly from observations and there is no general candidate-identity object.

### 3. What implementation evidence justifies treating multiple expressions as one subject?

Explicit alias-like facts, derived alias observations with provenance, identity predicates matching endpoint base identities, alias connected components, and canonical alias projection justify convergence. Similar names, relationship proximity, or presentation vocabulary do not.

### 4. When does implementation intentionally refuse convergence?

It refuses convergence when identity metadata is missing, identity values do not match endpoint bases, alias edges cross endpoint/non-endpoint boundaries, predicates are endpoint-scoped, exact query mode is requested, facts use excluded predicates such as `prometheus_instance`, or source metadata explicitly says identity/equivalence is not asserted.

### 5. Which downstream responsibilities depend on subject identity?

Current fact lookup, fact support aggregation, measurement retention, conflict detection, relationship projection, graph validation, alias visibility, and state/operator views depend on exact or alias-resolved subject identity depending on predicate and call options.

### 6. Does implementation evidence support a recurring identity convergence responsibility?

Yes, boundedly. It supports recurring explicit alias/identity convergence across normalizers, projection, and downstream consumers. It does not support a universal identity convergence architecture with a general candidate-identity stage.

### 7. If so, what implementation vocabulary best characterizes that responsibility?

The best supported vocabulary is **explicit alias/identity projection**. It is grounded in implementation names and behavior. Stronger vocabulary such as “entity identity recovery subsystem” is unsupported by current implementation evidence.

## Supported conclusions

1. Seed keeps observation/evidence/fact expression records separate through ingestion.
2. Seed can derive alias observations from endpoint metadata and explicit endpoint identity matches.
3. Seed creates projected subject convergence through alias-like facts in `AliasResolver`.
4. Seed intentionally refuses several plausible merges, especially endpoint-to-host measurement merges without supported identity evidence.
5. Downstream reasoning can consume subject identity through alias-resolved current fact support, conflicts, relationships, and views.
6. The current recurring responsibility is explicit and bounded, not general ontology/entity redesign.

## Unsupported conclusions

1. Implementation does not support a general `CandidateIdentity` stage.
2. Implementation does not support a universal identity convergence mechanism for all repository artifacts, package observations, relationships, Prometheus observations, systemd observations, discovery observations, and provider observations.
3. Implementation does not support promoting presentation vocabulary into subject identity.
4. Implementation does not support saying all downstream reasoning first recovers that many expressions refer to one subject.
5. Implementation does not support treating entity creation as the primary general convergence point for observation/fact subjects.

## Confidence

Confidence is **medium-high** for endpoint alias/identity and projection-time alias convergence because implementation and tests directly cover those paths.

Confidence is **medium** for broader repository/provider/systemd/package convergence because reviewed evidence shows source-specific observations and downstream projections, but not one generalized identity-convergence responsibility across all sources.

Confidence is **low** for any claim that Seed already has a generalized identity convergence subsystem, because the reviewed implementation lacks a common candidate identity abstraction and preserves multiple unrelated convergence mechanisms.

## Recommended next investigation

Investigate whether non-endpoint domains have source-specific convergence responsibilities comparable to endpoint alias/identity projection. A bounded next question:

> Across repository artifacts, package observations, relationship observations, and self-model alignment, where do implementation records preserve exact expression subjects, where do they derive aliases or canonical subjects, and where do downstream consumers rely only on exact subject strings?

This should remain an investigation only and should not introduce new abstractions or redesign identity handling.

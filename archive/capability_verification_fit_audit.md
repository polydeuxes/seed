# Capability verification fit audit

## Scope

This audit determines whether **verified capability** can be represented using
existing Seed primitives, especially the current provenance path:

```text
Observation -> Evidence -> Fact
```

It is documentation only. It does not implement capability verification, add
predicates, add entity types, change `Runtime`, change `StateProjector`, execute
verification operations, or create a new subsystem.

## Executive summary

Verified capability can be built **primarily from** existing
`Observation -> Evidence -> Fact` primitives, but not from them alone.

A scoped positive verification conclusion such as "workspace `default` has
verified `ssh_access` for host `web-01` as of time T" is a natural **Fact**:
it has a subject, predicate, value, dimensions, evidence ids, confidence,
`observed_at`, and optional `expires_at`. Verification operation results,
provider status reports, and inventory checks can naturally enter Seed as
observations, become evidence, and support the projected verification fact.

However, the current catalogs do not define verification predicates, and no
current model defines the verification target, accepted evidence classes, or the
policy that decides which facts count as verified, stale, failed, or unverified.
Those gaps are small if capability verification remains a read-model over facts;
they become a genuinely new subsystem only if Seed needs orchestration of
verification checks, scheduling, provider negotiation, credentials, retries, or
long-running jobs.

**Recommendation:** build capability verification first as a fact-backed read
model over `Observation -> Evidence -> Fact`, with small catalog extensions and
one missing policy/read-model layer. Do **not** create a broad new subsystem for
the core semantic representation.

## Current primitive fit

| Area | Fit classification | Notes |
| --- | --- | --- |
| Observation | Existing primitive already sufficient | Verification attempts and provider reports are external observations with source type, time, confidence, metadata, dimensions, and expiry. |
| Evidence | Existing primitive already sufficient | Observation-derived evidence already stores source, kind, payload, observed time, workspace, and confidence. |
| Fact | Small extension | The shape fits verification conclusions, but verification-specific predicates and scope conventions are not yet cataloged. |
| FactSupport | Existing primitive already sufficient | Support groups already aggregate independent facts for one subject/predicate/value/dimensions claim or select the latest measurement sample. |
| PredicateCatalog | Small extension | Needs canonical verification predicates, value vocabulary, cardinality, and durable-vs-measurement semantics. |
| EntityTypeCatalog | Small extension | `capability` already exists; verification may need additional scoped target types only if capability target entities are not encoded as dimensions. |
| StateProjector | Small extension | Projection can already preserve facts, supports, conflicts, stale facts, and evidence; a convenience read model/query would be new. |
| Contradiction handling | Existing primitive already sufficient for first version | Single-cardinality durable predicates already surface competing values as `FactConflict`; this supports competing verification evidence without resolving truth. |
| Temporal reasoning | Existing primitive already sufficient for first version | `observed_at`, `latest_observed_at`, measurement recency, and `expires_at` support age and staleness. |
| Verification policy/read model | Genuinely missing concept | Seed lacks a model that states which evidence classes are acceptable for positive/negative/stale verification and how to expose verification status. |

## Audit questions

### 1. Could verified capability be represented as a Fact?

**Answer: yes, with a small predicate/scope extension.**

A verified capability is a claim about a scoped target at a time boundary. That
maps directly onto `Fact`:

- `subject_id`: the verification target or a stable target entity id.
- `predicate`: a canonical verification predicate.
- `value`: the status or boolean conclusion.
- `dimensions`: scope such as capability, provider, host, workspace, operation,
  tenant, environment, or policy id.
- `evidence_ids`: evidence that supports the claim.
- `source_type`: likely `discovery`, `provider`, `imported`, or `inferred`.
- `confidence`: confidence assigned by source or policy.
- `observed_at`: verification time or source observation time.
- `expires_at`: freshness boundary.

The main caveat is semantic, not structural: a bare fact should not be called a
verified capability unless a verification policy accepts its predicate, value,
scope, and evidence class. In other words, a fact can represent the persisted
claim; a policy/read model must interpret whether it is sufficient.

**Classification:** small extension.

### 2. What predicate(s) would be required?

The minimal durable predicate set should avoid overloading generic capability
metadata. Recommended predicates:

| Predicate | Kind | Cardinality | Value type | Purpose |
| --- | --- | --- | --- | --- |
| `capability_verification_status` | durable fact | single | enum | Current policy conclusion for a scoped capability target. Values should include `verified`, `unverified`, `failed`, and possibly `blocked` or `unknown`. |
| `capability_verified` | durable fact | single | boolean | Optional convenience predicate for positive verification only. It is simpler but loses failure reason/status vocabulary. |
| `capability_verification_policy` | durable fact | single | string | Identifies the policy/version used to interpret evidence. Could also be a dimension instead of a predicate. |
| `capability_verification_evidence_class` | durable fact | multi | string | Records accepted evidence class labels, if not kept solely in evidence payload/dimensions. |
| `capability_candidate` | durable fact | multi | string | Optional; represents possible capability-provider/operation candidates separately from verified status. |

For the first version, the preferred single predicate is:

```text
subject_id: <verification target id>
predicate: capability_verification_status
value: verified | unverified | failed | blocked | unknown
dimensions: {
  capability: <capability slug>,
  scope_type: workspace|host|provider|operation|environment|tenant,
  scope_id: <stable scope id>,
  policy_id: <verification policy id>,
  provider: <optional provider id>,
  operation: <optional operation name>
}
```

This keeps the predicate single-cardinality per exact dimensions, allowing the
existing conflict logic to detect competing status values for the same scoped
capability target. A separate `capability_verified=true` predicate is attractive
for filtering but is less expressive for failed or blocked states.

**Classification:** small extension.

### 3. Would verification evidence naturally fit into FactSupport?

**Answer: yes.**

Verification evidence naturally fits the current support model. Multiple
observations that produce the same scoped verification fact can become multiple
supporting facts, and `FactSupport` can aggregate support for the same
subject/predicate/value/dimensions tuple. Independent evidence identity already
uses evidence ids, which prevents repeated references to the same evidence item
from being treated as separate independent support.

Examples that fit naturally:

- a verification operation result producing `capability_verification_status = verified`;
- a provider status report producing the same status;
- a local inventory observation supporting a candidate or a lower-confidence
  verification status;
- a negative check producing `capability_verification_status = failed`.

The main limitation is not `FactSupport`; it is policy interpretation. Current
support aggregation can say which value has stronger support, but it does not
know which evidence classes are acceptable for a particular capability or risk
level.

**Classification:** existing primitive already sufficient.

### 4. Would stale verification naturally fit existing stale fact semantics?

**Answer: yes for freshness, with a small extension for refresh routing.**

Verification freshness maps directly to `expires_at`. A verification fact whose
`expires_at` has passed becomes stale under existing stale fact semantics and is
excluded from current supports unless explicitly included. Historical evidence
remains available through the append-only ledger and projected stale facts.

Two small extensions would improve fit:

1. Add verification predicates to stale-refresh routing so a stale verification
   recommends an appropriate capability such as `capability_verification`,
   `environment_inventory`, `ssh_access`, or the specific capability being
   re-verified.
2. Define policy rules for default TTL/freshness by capability, scope, provider,
   and evidence class.

A stale verification should be represented as either:

- an expired prior `capability_verification_status = verified` fact, plus a read
  model status of `stale`; or
- an explicit later `capability_verification_status = stale` fact only if Seed
  needs to preserve the transition as a separately observed claim.

The first option fits existing semantics better because staleness is already a
projection property derived from `expires_at`.

**Classification:** existing primitive already sufficient for staleness; small
extension for verification-specific refresh recommendation and TTL policy.

### 5. Would contradiction handling naturally support competing verification evidence?

**Answer: yes for competing status claims with identical scope dimensions.**

If two non-expired durable facts assert different values for the same
subject/predicate/dimensions tuple, current fact conflict projection can surface
a `FactConflict`. That is a natural fit for cases such as:

- provider A says `verified`, provider B says `failed`;
- one verification operation says `verified`, a later independent operation says
  `failed`;
- imported inventory says `verified`, local check says `unknown`.

For this to work, verification status must be modeled as a **single-cardinality
durable predicate** and all facts that should compete must use exactly the same
scope dimensions. If dimensions differ, Seed will correctly treat them as
different claims rather than contradictions.

What current contradiction handling does **not** provide is a domain-specific
resolution policy. It can expose competing values, winning support, ambiguity,
and supporting evidence, but it does not decide that one evidence class overrides
another, that a more recent failure invalidates an older success, or that high
risk requires two independent positive sources.

**Classification:** existing primitive already sufficient for first-version
conflict representation; genuinely missing domain-specific verification
resolution policy.

### 6. Would temporal reasoning naturally support verification age?

**Answer: yes.**

Verification age can be computed from existing timestamps:

- `Fact.observed_at`: when a status claim was observed or derived.
- `Evidence.observed_at`: when the source payload was observed.
- `FactSupport.observed_at`: earliest supporting fact timestamp for an aggregated
  support group.
- `FactSupport.latest_observed_at`: newest supporting fact timestamp.
- `Fact.expires_at`: explicit freshness cutoff.

This is enough to answer age-oriented questions such as:

- how old is the current verification?
- when was it last verified?
- is the verification expired?
- which evidence is newer: positive or negative?

The missing piece is policy vocabulary: Seed needs rules that say how old is too
old for a particular capability, scope, or evidence class.

**Classification:** existing primitive already sufficient for timestamps and
age computation; small extension for TTL/freshness policy.

### 7. What NEW models would actually be required?

A full subsystem is not required for the semantic core, but Seed needs a small
set of explicit models or read-model concepts so verification is not inferred
accidentally from arbitrary facts.

#### Genuinely missing concept: verification target

Seed needs a canonical way to identify the thing being verified:

```text
CapabilityVerificationTarget
- capability
- scope_type
- scope_id
- optional provider
- optional operation
- optional environment / tenant / workspace
```

This could be implemented as a model, a stable subject-id convention, or a
validated dimensions schema. A first implementation can use dimensions; a named
model becomes useful once targets are shared across APIs.

#### Genuinely missing concept: verification evidence policy

Seed needs a policy that answers:

- which predicates count as verification predicates;
- which values count as positive, negative, stale, blocked, or unknown;
- which evidence classes are acceptable for each capability/scope;
- how confidence thresholds are applied;
- whether a provider-reported status is enough or must be corroborated;
- how freshness/TTL is chosen;
- how negative evidence competes with older positive evidence.

Without this policy, Seed can store verification-like facts but cannot safely
claim a capability is verified.

#### Genuinely missing concept: verification read model

Seed needs a query-oriented projection such as:

```text
CapabilityVerificationView
- target
- status
- current_fact_id
- support
- conflicts
- evidence_ids
- observed_at
- latest_observed_at
- expires_at
- stale
- policy_id
- explanation
```

This can be derived from existing `State`, `FactSupport`, `FactConflict`, and
`Evidence`; it does not need to own execution or storage.

#### Small extension: predicate catalog entries

Add canonical verification predicates to `PredicateCatalog` so projection knows
cardinality and durable/measurement semantics.

#### Small extension: entity type catalog entries, if needed

The existing `capability` entity type may be enough if capability targets are
encoded in fact dimensions. Add new entity types only if Seed needs first-class
nodes for `provider`, `workspace`, `operation`, `verification_target`, or
`verification_policy`.

#### Not required for first version: execution subsystem

A system that schedules verification checks, calls providers, manages
credentials, retries failures, or performs long-running re-verification would be
a separate execution/orchestration concern. It is not required to represent the
verification conclusion.

## Classification by requested area

### Observation

**Classification:** existing primitive already sufficient.

`Observation` already captures an external observed value with source type,
subject, predicate, value, confidence, metadata, dimensions, `observed_at`, and
optional `expires_at`. Verification operation output or provider status can be
modeled as observations before normalization into facts.

### Evidence

**Classification:** existing primitive already sufficient.

`Evidence` already stores provenance payloads with source, kind, workspace,
observed time, payload, and confidence. It naturally stores verification attempt
outputs, provider report payloads, inventory snapshots, or imported audit
records.

### Fact

**Classification:** small extension.

`Fact` has the correct storage shape for scoped verification claims. The missing
piece is a canonical verification predicate and validated scope/value semantics.

### FactSupport

**Classification:** existing primitive already sufficient.

Support aggregation and latest-sample semantics are adequate. Verification
status should usually be durable single-cardinality per exact target dimensions,
so repeated matching positive evidence aggregates and competing status values
conflict.

### PredicateCatalog

**Classification:** small extension.

Add verification predicates and value vocabulary. The catalog should mark
verification status as durable and single-cardinality for each exact scope.

### EntityTypeCatalog

**Classification:** small extension.

`capability` already exists. Additional entity types are optional and should be
added only if verification targets become graph nodes rather than scoped fact
dimensions.

### StateProjector

**Classification:** small extension.

The projector can already ingest observations/evidence/facts and produce
supports, conflicts, stale facts, and evidence indexes. It would need either no
change for raw storage or a small derived view for convenient capability
verification queries.

### Contradiction handling

**Classification:** existing primitive already sufficient for first-version
representation; missing policy for domain-specific resolution.

Current durable single-cardinality conflict handling can represent competing
verification evidence. It should not be expected to decide final trust semantics
without a verification policy.

### Temporal reasoning

**Classification:** existing primitive already sufficient for first-version age
and staleness; missing policy for TTL selection.

Existing timestamps and expiry support verification age. Freshness rules by
capability/evidence class are policy, not a new storage primitive.

## Recommendation

Capability verification should be built primarily from:

```text
Observation -> Evidence -> Fact -> FactSupport / FactConflict -> Verification read model
```

It should **not** start as a new broad subsystem. The core representation fits
Seed's existing knowledge/evidence architecture.

The minimum future design should add:

1. canonical verification predicates in `PredicateCatalog`;
2. a stable verification target representation, either by subject-id convention
   and dimensions or a small named model;
3. a verification evidence/freshness policy;
4. a read model that interprets facts, supports, conflicts, evidence, and expiry
   as `verified`, `unverified`, `stale`, or `failed` for a scoped capability
   target.

Create a new subsystem only when Seed needs active verification orchestration:
automatic checks, scheduling, provider calls, credential flows, retries,
provider trust negotiation, or long-running verification jobs. Those are
execution concerns, not requirements for representing verified capability.

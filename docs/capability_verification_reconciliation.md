# Capability verification reconciliation

## Purpose

This document reconciles the capability verification audit, vocabulary, fit
audit, and roadmap reconciliation into one design decision: **capability
verification does not require a new architecture to begin**.

The smallest safe path is to treat capability verification first as vocabulary,
predicate semantics, and inventory/tests over existing knowledge primitives. A
new execution subsystem, scheduler, provider-calling layer, or Runtime behavior
is not required to prove the design.

## Decision

Capability verification should begin as a documentation- and inventory-backed
semantic layer over the existing knowledge/evidence architecture:

```text
Observation -> Evidence -> Fact -> FactSupport / FactConflict -> read-only interpretation
```

The first implementation should not execute verification checks, call providers,
mutate host state, schedule refreshes, or cause capability resolution to verify
anything automatically. It should only make verification concepts explicit enough
that future facts and tests cannot confuse these states:

- requested capability;
- catalog-known capability;
- registered operation candidate;
- provider recommendation or handoff candidate;
- provider-reported availability;
- local observed availability;
- verified, unverified, stale, failed, or disputed verification.

## What existing architecture already represents

### Fact

`Fact` can already represent a scoped verification claim if Seed defines a
canonical predicate and scope convention. The missing piece is not storage shape;
it is the predicate/value vocabulary and target dimensions.

Examples that fit the existing fact model:

- `capability_verification_status = verified`;
- `capability_verification_status = failed`;
- `capability_verification_method = provider_report`;
- `capability_verification_method = read_only_inventory`;
- `provider_availability_status = available`;
- `local_availability_status = observed_available`.

A verification fact should be scoped by dimensions such as capability, scope
type, scope id, provider, operation, workspace, host, environment, and evidence
method. It should not be inferred from a bare capability slug, a registry match,
or a `verify_*` name.

### FactSupport

`FactSupport` already represents corroboration. Multiple facts with the same
subject, predicate, value, and dimensions can aggregate support for the same
verification claim. This is enough to represent independent positive evidence,
independent negative evidence, and repeated observations of the same scoped
status.

The support layer does not need to know domain policy. It can say which scoped
claim has support and whether claims compete. A future verification policy can
then decide whether that support is sufficient for a positive verification
conclusion.

### PredicateCatalog

`PredicateCatalog` is the correct place to classify verification predicates so
projection can treat status-like verification claims consistently.

The likely first predicates are durable, single-cardinality predicates per exact
scope dimensions, such as:

- `capability.verification_status`;
- `capability.provider_availability_status`;
- `capability.local_availability_status`.

The catalog can also document value vocabulary without creating execution
behavior. Candidate values include:

- `verified`;
- `unverified`;
- `failed`;
- `blocked`;
- `unknown`;
- `available`;
- `not_available`;
- `observed_available`;
- `observed_not_available`.

`stale` should usually remain a projection result derived from `expires_at`, not
a separately asserted value, unless Seed later needs to preserve an explicit
source claim that something is stale.

### Contradiction handling

Current contradiction handling already fits competing verification claims when
those claims use the same durable single-cardinality predicate and identical
scope dimensions.

Examples:

- one source asserts `capability.verification_status = verified` and another
  asserts `failed` for the same capability, provider, workspace, and target;
- a provider report says a backend is available while a local observation says
  the same scoped endpoint is not available;
- two verification methods produce incompatible current statuses.

Contradiction handling should expose conflict, ambiguity, support, and evidence.
It should not become a verification-specific trust engine. Domain-specific trust
rules belong in a later verification policy or read model.

### Temporal semantics

Existing temporal semantics already represent the age and freshness of
verification evidence:

- `observed_at` records when evidence or a derived fact was observed;
- `latest_observed_at` on support identifies the newest supporting sample;
- `expires_at` marks freshness limits;
- expired durable facts remain historically visible but do not count as current
  by default;
- stale facts can recommend refresh capabilities through existing stale-fact
  routing once verification predicates are cataloged.

Therefore, verification age, last verified time, current-versus-stale status,
and evidence expiry do not require a new temporal architecture. The missing
piece is policy: default TTLs and acceptable freshness by capability, scope,
provider, and evidence class.

## Classification of proposed verification concepts

### Zero new models

These concepts can begin with existing models plus documentation, predicates, or
inventory/tests:

| Concept | Existing representation | Notes |
| --- | --- | --- |
| Requested capability | `ToolNeed.capability` | A gap/request, never verification. |
| Known capability | `CapabilityCatalogEntry` | Static catalog metadata, never availability proof. |
| Registered operation candidate | `ToolSpec.capabilities` plus registry lookup | Candidate only; execution and success are not implied. |
| Provider recommendation | catalog/ranker recommendation metadata | Suggests relevance, not current provider availability. |
| Handoff candidate | catalog recommendation operation/backend metadata | Handoff metadata, not a registered invocation or verification. |
| Verification evidence payload | `Evidence` | Stores raw provider reports, operation outputs, inventory snapshots, or imported records. |
| Verification claim | `Fact` | Requires canonical predicate/value/scope semantics. |
| Corroboration | `FactSupport` | Aggregates matching scoped claims. |
| Competing status evidence | `FactConflict` / contradiction handling | Works if predicates are durable and dimensions match. |
| Staleness | `expires_at` and stale fact projection | Prefer derived stale status over explicit stale facts. |
| Verification age | existing timestamps | Compute from fact/evidence/support timestamps. |
| Documentation-only vocabulary | docs | No runtime behavior needed. |
| Inventory of `verify_*` operations | tests/docs over manifests and tool specs | Can classify stubs versus positive verifiers without execution. |

### Small model additions

These are small because they refine interpretation of existing facts rather than
introducing a new subsystem:

| Concept | Small addition | Why it is small |
| --- | --- | --- |
| Canonical verification predicates | Add entries to `PredicateCatalog` | Reuses Fact projection, support, conflict, and stale semantics. |
| Verification target representation | Stable subject-id convention plus validated dimensions, or a small `CapabilityVerificationTarget` value object | Needed to prevent scope confusion; does not own behavior. |
| Verification status vocabulary | Enum/constants/docs for values such as `verified`, `unverified`, `failed`, `blocked`, `unknown` | Prevents overloading catalog/registry fields. |
| Evidence class vocabulary | Enum/constants/docs for `provider_report`, `verification_operation_result`, `local_inventory`, `local_observation`, `imported_audit` | Used by policy and explanations, not execution. |
| Freshness/TTL policy table | Static policy data by capability/scope/evidence class | Interprets `expires_at`; does not require temporal redesign. |
| Read-only verification view | Derived view over facts, supports, conflicts, evidence, and expiry | Query convenience only; should not store new truth or execute checks. |
| Stale refresh mapping | Predicate-to-capability recommendation mapping | Extends existing stale recommendation behavior. |

### Major architecture additions

These should be deferred until Seed explicitly needs execution behavior:

| Concept | Why it is major |
| --- | --- |
| Automatic verification execution | Would make capability reasoning trigger tool/provider calls. This crosses the reasoning/execution boundary. |
| Verification scheduler or refresh daemon | Requires lifecycle, retries, backoff, permissions, and operational ownership. |
| Provider credential and trust negotiation | Requires secrets, identity, authority policy, and provider-specific failure semantics. |
| Long-running verification jobs | Requires job state, cancellation, resumability, and observability. |
| Runtime-integrated implicit verification | Risks turning capability resolution into execution and violating current Runtime/ToolExecutor boundaries. |
| New truth arbitration engine | Current contradiction handling exposes disputes; automatic domain truth resolution needs explicit policy and risk review. |
| Historical verification timeline service | Existing latest-current and stale semantics are enough for first version; full as-of timelines are separate temporal architecture. |

## Smallest implementation that proves the design

The smallest implementation should prove that verification is representable
without execution behavior. It should therefore avoid new runtime paths and focus
on semantic guardrails.

### Minimum viable slice

1. **Add canonical vocabulary and predicates.**
   - Document `capability.verification_status` and adjacent provider/local
     availability predicates.
   - Mark status predicates as durable and single-cardinality per exact target
     dimensions.
   - Define allowed values and evidence classes.

2. **Define target scoping by convention.**
   - Use either a stable subject-id convention such as
     `capability-verification:<capability>:<scope_type>:<scope_id>` or fact
     dimensions such as `capability`, `scope_type`, `scope_id`, `provider`, and
     `operation`.
   - Do not add a full target table or service until APIs need to share target
     objects.

3. **Add inventory/tests that assert non-verification boundaries.**
   - Catalog-known does not equal verified.
   - Registered operation candidate does not equal verified.
   - Provider recommendation does not equal provider-reported availability.
   - `verify_*` operation names do not equal positive verification.
   - Stub outputs such as `not_checked` do not create positive verification.

4. **Add read-only characterization of fact semantics.**
   - A positive unexpired verification fact can be represented.
   - Expired positive evidence becomes stale and is excluded from current
     support by default.
   - Conflicting current verification status facts are surfaced as conflicts.
   - Multiple matching evidence items aggregate under `FactSupport`.

5. **Optionally add a tiny read-only helper/view.**
   - Only after the predicate and inventory tests exist.
   - The helper should interpret projected facts; it should not execute checks,
     create pending actions, call providers, or mutate registry/catalog state.

### Minimum viable implementation estimate

| Slice | Files changed | Approx. LOC | Architectural risk |
| --- | ---: | ---: | --- |
| Documentation only | 1-3 docs | 150-350 | Very low |
| Predicate vocabulary + tests | 2-5 files | 80-180 | Low |
| Inventory/tests for `verify_*` boundaries | 1-3 test files | 80-220 | Low |
| Read-only verification helper/view | 2-4 files | 120-300 | Low-medium |
| Execution behavior | 5+ files | 300+ | High; defer |

The recommended proof slice is the first three rows only: documentation,
predicate vocabulary, and boundary/inventory tests. That is enough to prove that
Seed can represent verification semantics without changing execution ownership.

## Can capability verification begin without execution behavior?

Yes. Capability verification can and should begin as:

### Vocabulary

Vocabulary is the safest first step. It prevents accidental conflation between
requested, known, candidate, recommended, provider-reported, locally observed,
and verified capabilities.

### Predicates

Predicates are the smallest semantic implementation step. They let Seed store
verification-like claims as facts while reusing existing support, contradiction,
and stale semantics.

### Inventory/tests

Inventory/tests can prove the boundary before behavior exists. They can verify
that current manifests, catalog entries, recommendations, and `verify_*` names
are not treated as verified capability. They can also classify which checked-in
operations are stubs, plan-only, read-only evidence gatherers, or future positive
verifiers.

### No execution behavior

No execution behavior is required for the first proof. Capability resolution can
remain an inventory/recommendation boundary. Tool execution can remain owned by
`ToolExecutor`. Verification evidence can be added later through explicit tool
calls or observation ingestion, not implicit resolution.

## Recommended path

Proceed in this order:

1. Keep this reconciliation and the existing vocabulary/audits as the design
   baseline.
2. Add canonical verification predicates and value vocabulary.
3. Add tests proving existing capability resolution fields are not verification
   statuses.
4. Inventory checked-in `verify_*` operations and classify whether each can ever
   produce positive verification evidence.
5. Only then consider a read-only `CapabilityVerificationView` derived from
   facts, support, conflicts, evidence, and expiry.
6. Defer execution orchestration until Seed has a concrete use case requiring
   scheduled or automatic checks.

## Recommendation: minimum viable implementation slice

**Recommended slice:** vocabulary + predicates + inventory/tests.

- **Files changed:** 3-8 files.
  - 1 documentation update or index entry;
  - 1 predicate catalog location;
  - 1-3 boundary tests;
  - 1-3 inventory/fixture updates if checked-in manifests need capability tags.
- **Approximate LOC:** 160-400 LOC.
- **Architectural risk:** low.
  - Reuses existing Fact, FactSupport, PredicateCatalog, contradiction, and
    temporal semantics.
  - Does not add Runtime behavior.
  - Does not add ToolExecutor behavior.
  - Does not call providers.
  - Does not schedule checks.
  - Does not create a parallel architecture.

**Do not start with:** an automatic verifier, scheduler, provider adapter layer,
credential workflow, or Runtime-integrated verification path. Those are major
architecture additions and are unnecessary to prove the design.

## Final conclusion

No new architecture is required to begin capability verification. The existing
knowledge/evidence system can represent the core verification concepts once Seed
adds canonical predicates, scope conventions, vocabulary, and boundary tests.
New architecture is only justified later for active verification execution,
provider integration, scheduling, credential handling, or richer historical
querying.

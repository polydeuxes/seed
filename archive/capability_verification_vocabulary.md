# Capability verification vocabulary

## Scope

This document defines vocabulary and invariants for capability verification
reasoning. Capability Verification Inventory v1 is now implemented as an
inventory-only read model over projected facts and evidence. It does not execute
verification, add host checks, add network checks, schedule work, call providers,
mutate hosts, or cause capability resolution to produce a verified capability.

Capability verification is a reasoning concept identified by the capability
verification audit and roadmap reconciliation. The terms below keep that concept
explicit so implemented and future designs can refer to stable names without
implying runtime behavior.

## Vocabulary

### Capability

A **capability** is a normalized description of an ability Seed may need,
recognize, recommend, or eventually verify. A capability names what kind of work
could be satisfied, such as `weather_lookup`, `ssh_access`, or
`documentation_lookup`.

A capability is not itself a tool, operation, provider, status, fact, or proof.
It is the semantic target used by adjacent systems.

### Requested capability

A **requested capability** is the capability named by a user-facing or
model-facing request for missing ability. Today, the requested capability is
carried by `ToolNeed.capability`.

A requested capability means Seed has recorded a capability gap or desired
ability. It does not mean any operation exists, any provider is available, or any
verification has occurred.

### Known capability

A **known capability** is a capability with catalog metadata, such as a
`CapabilityCatalogEntry`. It means Seed has static read-only knowledge about the
capability and may have provider recommendations or descriptive metadata for it.

A known capability does not imply that the capability is available in the
current workspace, available on the current host, reachable through a provider,
or verified.

### Candidate capability

A **candidate capability** is a possible way to satisfy or investigate a
capability before verification. Candidate capabilities may be inferred from
observation-derived facts, linked Evidence, catalog lookup, provider reports
admitted as testimony, operator-supplied testimony, freshness or expiry
boundaries, bounded verification status projections, or other future discovery
sources.

A candidate capability is only a possibility. It is not verified until future
verification semantics explicitly attach an acceptable verification status to a
specific verification target using acceptable evidence.

### Provider-recommended capability

A **provider-recommended capability** is a capability-provider pairing suggested
by static catalog or ranker metadata. Provider recommendations can describe a
backend, provider, risk class, score, handoff option, or operation name supplied
as metadata.

Provider recommendation means "this provider might be relevant." It does not
mean the provider has been contacted, the provider is available, the provider
has reported success, an operation has run, or the capability is verified.

### Verified capability

A **verified capability** is a read-model conclusion that a capability target
has current positive verification support at a particular time or event
boundary. In Capability Verification Inventory v1, this conclusion is derived
only from an unexpired `capability_verified` fact with value `verified`.

A verified capability must eventually include at least:

- the capability being verified;
- the verification target or scope, such as workspace, host, provider, tenant,
  environment, or externally reported service boundary;
- the positive verification status;
- the evidence class or evidence references that support the status;
- the time, event id, or observation boundary for which the status is current;
- any expiry, freshness, or staleness policy that limits the status.

Seed currently implements only the inventory slice of this model. No current
object other than the read-only inventory entry should be described as a
verified capability, and the inventory entry is only as strong as the supporting
Fact/FactSupport/Evidence it exposes.

### Unverified capability

An **unverified capability** is a capability that is requested, known,
candidate, or recommended but lacks an accepted positive verification status for
the relevant scope.

Unverified is the safe default for all requested, known, candidate, and
provider-recommended capabilities unless future verification semantics prove
otherwise. Unverified does not necessarily mean unavailable; it means not proven
by Seed's verification model.

### Stale verification

A **stale verification** is a status for a capability that previously had
supporting verification evidence, but whose evidence is no longer fresh enough
for the applicable scope or policy. In Inventory v1, stale status uses only the
existing fact `expires_at` / stale-fact semantics; it does not invent a new aging
policy.

Stale verification should not be treated as current positive verification. It
may be useful as historical context or as a reason to request re-verification.

### Failed verification

A **failed verification** is a future status for a scoped capability target when
an accepted verification attempt or evidence source reports that the capability
does not satisfy the verification policy.

Failed verification is not the same as unverified. Failed verification requires
negative evidence from an accepted evidence class. Unverified means acceptable
positive evidence is absent.


## Implemented predicate vocabulary

Capability Verification Inventory v1 adds one canonical predicate:

| Predicate | Kind | Cardinality | Values | Meaning |
| --- | --- | --- | --- | --- |
| `capability_verified` | durable fact | single | `verified`, `provider_reported`, `unverified` | A fact about a capability subject that can be interpreted by the read-only inventory. |

The predicate is intentionally minimal. It is enough to represent current
positive verification support, provider-reported support, explicit negative
support, and stale support through existing fact expiry behavior. Scope can be
represented later with standard fact dimensions if a caller needs host/provider
scoping; Inventory v1 does not add a separate verification target model.

## Implemented inventory read model

Capability Verification Inventory v1 answers: "What capabilities does Seed
currently believe are verified?"

The inventory is derived from:

- projected `Fact` records using `capability_verified`;
- projected `FactSupport`;
- `PredicateCatalog` membership for the predicate;
- existing projected capability surfaces (`ToolNeed` capability names and
  capability verification fact subjects);
- existing evidence/explanation structures for supporting fact evidence.

Inventory states are:

- `verified`: current `capability_verified = verified` support exists;
- `provider_reported`: current `capability_verified = provider_reported` support
  exists;
- `unverified`: the capability is in the projected inventory universe but lacks a
  current verification fact, or has an explicit `unverified` fact;
- `stale`: only expired verification facts support the capability;
- `unknown`: a current `capability_verified` value exists but is outside the
  implemented value vocabulary.

Verification views are read-only. The inventory is read-only. It appends no
events, executes no tools, calls no providers, mutates no state, and does not
route through runtime execution.

## What is not a verified capability

The following current Seed objects and fields are not verified capabilities:

- `ToolNeed`: records a requested capability gap.
- `ToolNeed.capability`: names the requested capability.
- `CapabilityCatalogEntry`: static known-capability metadata.
- `CapabilityCatalog` recommendation: static provider or handoff metadata.
- `CapabilityRecommendation.operation`: provider or handoff metadata, not a
  verification result.
- Provider-reported status by itself: testimony that may be admitted as evidence,
  not automatic proof or Seed's own verification conclusion.
- Operator-supplied testimony by itself: evidence input that still needs accepted
  scope, freshness, and status interpretation.
- An observation, observation-derived fact, linked Evidence item, confidence
  score, or expiry timestamp by itself: each may become evidence input, but none
  is a verified capability without a scoped verification status model.

## Future evidence classes

Future verification may be supported by evidence classes such as the following.
These are vocabulary only and do not create runtime behavior.

### Observation-derived fact

An **observation-derived fact** is a normalized fact derived from an observation
source. It could eventually support verification if the source, predicate,
confidence, time boundary, and scope satisfy the verification policy.

### Provider-reported status

A **provider-reported status** is a status reported by a provider, service,
external backend, operator, or handoff channel. It could eventually support
verification if Seed records the provider identity, report semantics, freshness,
and trust policy.

### Linked Evidence

**Linked Evidence** is an evidence record associated with a verification-relevant
fact or testimony. It could eventually support verification only if its source,
subject, freshness, confidence, and boundary satisfy the verification policy.

### Freshness or expiry boundary

A **freshness or expiry boundary** describes whether evidence remains current
for a bounded verification status projection. It may limit or stale a conclusion,
but it should not by itself create positive verification.

### Negative evidence

**Negative evidence** reports that a scoped capability target failed or could
not be confirmed. It may eventually support failed verification, blocked status,
or re-verification prompts.

## Documentation invariants

The following invariants apply now and should remain true until an explicit
future verification design replaces them:

1. Capability resolution never implies verification.
2. ToolNeed creation never implies verification.
3. Known capability catalog metadata never implies verification.
4. Provider recommendation never implies verification.
5. CapabilityRecommendation operation metadata never implies verification.
6. A `verify_*` operation name never implies verification.
7. Evidence-like objects are not verified capabilities without a scoped
   verification status model.
8. Unverified is the default state for requested, known, candidate, and
    provider-recommended capabilities.
9. Stale verification must not be treated as current positive verification.
10. Failed verification requires accepted negative evidence; it is not merely
    absence of positive evidence.

## Future model boundaries

Future capability verification should be modeled separately from existing
runtime execution and capability recommendation concerns.

Recommended future boundaries:

- **Verification target model**: identifies the capability plus scope being
  verified, such as workspace, host, provider, environment, or externally
  reported service boundary.
- **Verification status vocabulary**: represents states such as `verified`,
  `unverified`, `stale`, and `failed` without overloading catalog metadata
  fields.
- **Verification evidence policy**: defines which evidence classes can support
  positive, stale, failed, or unknown statuses.
- **Verification read model**: projects verification conclusions for query and
  explanation without automatically executing checks.
- **Provider status boundary**: separates provider-reported status from Seed's
  own verification conclusion.
- **Runtime boundary**: verification should not be added as implicit behavior
  inside capability resolution.
- **Catalog boundary**: `CapabilityCatalog` should remain read-only metadata;
  catalog presence or recommendation should not become verification.

## Non-goals

This document does not define executable verification algorithms, verification
schemas, new predicates, new events, automatic checks, host mutation, network
calls, provider calls, runtime orchestration, or operation execution behavior.

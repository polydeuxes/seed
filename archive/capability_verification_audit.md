# Capability verification semantics audit

## Scope and constraints

This audit documents current semantics and missing concepts for distinguishing a requested capability, catalog-known capability, registered operation candidate, provider recommendation, and verified capability. It is inventory/documentation only: it does not specify executable behavior, Runtime changes, ToolExecutor changes, host mutation, shell/network calls, automatic verification from capability resolution, or LLM-driven verification.

## Executive summary

Seed currently has clear models for four adjacent ideas:

1. **Requested capability**: a `ToolNeed.capability` slug created from a `request_tool` decision.
2. **Catalog-known capability**: a `CapabilityCatalogEntry` exists for that slug.
3. **Registered operation candidate**: a model-visible registered `ToolSpec` declares the same slug in `ToolSpec.capabilities` and is returned by `ToolRegistry.list_tools_for_capability(..., visible_only=True)`.
4. **Provider recommendation / handoff candidate**: read-only catalog/ranker metadata says a provider or external backend could satisfy the capability.

Seed does **not** currently have a first-class **verified capability** concept. Existing facts, evidence, observations, tool results, confidence, and expiry can represent supporting observations, but none of them attach a scoped verification status to a capability such as `verified`, `unverified`, `stale`, or `failed`. Existing `verify_*` naming is not enough: the checked-in `verify_ssh_access` operation is explicitly a non-network stub whose result is `access_status: not_checked`.

## Current semantic inventory

### Requested capability

`ToolNeed` is the current requested-capability carrier. It stores `name`, `summary`, normalized `capability`, `reason`, status, desired inputs, and desired outputs. `ToolNeedService.create_from_decision()` slugifies the requested `name` and requested or fallback `capability`, deduplicates against open needs by `name` or `capability`, and records `tool_need.created`.

Current implication: a requested capability means Seed has a work/ability gap, not that the capability is known, available, registered, or verified.

### Catalog-known capability

`CapabilityCatalog` is a read-only map from normalized capability slug to `CapabilityCatalogEntry`. Entries contain `capability`, `summary`, and recommendations. `CapabilityCatalog.get()` returns an entry by slug, and `recommend_for()` returns the entry recommendations for a `ToolNeed`.

Current implication: catalog-known capability means Seed has static metadata for the capability. It does not imply any provider credentials, local installation, live reachability, successful prior checks, registered tools, or safe execution.

### Registered operation candidate

`ToolSpec.capabilities` is operation metadata loaded from toolkit manifests and normalized on construction. `ToolRegistry.list_tools_for_capability()` normalizes the requested capability and returns `ToolSpec`s whose `capabilities` include that slug; with `visible_only=True`, it filters to existing model-visible registered semantics.

Current implication: a registered operation candidate means Seed knows a callable operation that claims to serve the capability and passes registry visibility/status filters. It does not imply the operation has been called, that its provider/backend is available, that credentials are present, or that executing it would verify the target safely.

Important current caveat: the checked-in generated toolkit manifests do not currently declare `capabilities` for `verify_ssh_access`; tests construct capability-tagged tool specs in memory to characterize registry/resolution semantics. Therefore, in a default manifest-loaded registry, the operation may be registered by name without being discoverable as an `ssh_access` candidate through capability lookup until manifest metadata is added.

### Provider recommendation

Provider recommendations come from two related read-only paths:

- `CapabilityCatalog.recommend_for()` returns static catalog recommendations for a `ToolNeed`.
- `ToolRecommendationService.recommend_for()` ranks those recommendations against projected state.

`ToolNeedService.resolve_capability()` accepts ranked provider recommendations and also converts catalog recommendation operation/backend metadata into `handoff_candidates`. Tests explicitly characterize catalog recommendation operation names as handoff metadata, not registered operations.

Current implication: provider recommendation means a provider may be appropriate according to catalog/ranker metadata. It does not mean the provider is installed, reachable, credentialed, authorized, or verified available.

### Capability resolution

`ToolNeedService.resolve_capability()` currently returns:

- `known_capability`: whether the catalog has an entry.
- `registered_operations`: visible registered operation candidates from registry capability lookup only.
- `provider_recommendations`: ranked provider recommendation summaries passed in by the caller.
- `handoff_candidates`: catalog recommendation backend/operation metadata.

Its docstring and tests establish that this path is read-only: it does not execute tools, authorize actions, create pending actions, mutate registry/catalog state, or call `ToolExecutor`.

Current implication: capability resolution is an inventory/recommendation boundary. It must not be upgraded into automatic verification without a separate explicit design.

### Evidence, Facts, Observations, and tool results

`Observation` can represent externally observed values with `source_type`, `observed_at`, `confidence`, metadata, dimensions, and optional `expires_at`. `ObservationIngestor` converts observations into both `Evidence` and `Fact`, preserving provenance links.

`Evidence` is a provenance payload with source, kind, observed time, payload, and confidence. Tool execution records successful tool output as evidence of kind `tool.output`, but the generic extraction service intentionally does not infer facts from tool results unless an explicit future mapping is added.

`Fact` represents a state claim with subject, predicate, value, evidence IDs, source type, confidence, observed time, and optional expiry. `FactSupport` aggregates supporting facts, marks expired support, and differentiates durable aggregates from current measurement samples. Confidence aggregation counts evidence support and contradictions, but there is no capability-verification-specific confidence model.

Current implication: verification evidence can be represented as observations/evidence/facts, but Seed lacks a canonical predicate/model tying those facts to a requested capability, provider, operation, target scope, method safety, verification status, and expiry policy.

### Observations from Ansible, Prometheus, and local host

Current observation sources already demonstrate safe evidence collection patterns:

- **Ansible inventory** imports authoritative host identity from local static inventory files. It does not invoke Ansible, expand host patterns, validate connectivity, or perform network access.
- **Prometheus** collects a fixed allowlist of read-only HTTP GET metrics (`up`, `node_uname_info`, filesystem size/availability). It returns observations or an empty list with `last_error` when unreachable.
- **Local host** collects platform and disk metadata through Python standard-library APIs only and explicitly does not execute shells/subprocesses.

Current implication: these sources can provide local or provider-observed evidence relevant to a capability, such as host identity, endpoint `up`, OS, architecture, and filesystem measurements. They do not currently produce first-class capability-verification records.

### Existing `verify_*` tools

The only checked-in generated `verify_*` operation found is `verify_ssh_access`. It is intentionally safe and non-networking. The operation returns `ok: true`, `access_status: not_checked`, and `method: stub_no_network`; its docs say it does not open sockets, run commands, or inspect the host.

Current implication: a tool name beginning with `verify_` does not currently imply actual verification. Existing `verify_ssh_access` can only produce evidence that no live SSH check was attempted.

## Answers to audit questions

### 1. What does “capability exists” mean today?

Today there are multiple overloaded meanings, and none are a verified runtime truth:

- A **requested capability exists** when a `ToolNeed` exists with that capability slug.
- A **catalog-known capability exists** when `CapabilityCatalog.get(capability)` returns an entry.
- A **registered operation candidate exists** when `ToolRegistry.list_tools_for_capability(capability, visible_only=True)` returns at least one tool.
- A **provider recommendation exists** when catalog/ranker recommendation output contains a provider for the capability.

Recommendation: avoid the phrase “capability exists” without a qualifier. Prefer `requested`, `catalog_known`, `registered_operation_candidate`, `provider_recommended`, and, only after a future model exists, `verified`.

### 2. What does “capability is available” mean today?

There is no first-class, canonical “available capability” state today. The closest current meanings are:

- `known_capability=True`: metadata is available, not the capability.
- non-empty `registered_operations`: a callable candidate is available in the registry, not necessarily usable against a specific target/provider.
- non-empty `provider_recommendations`: a possible provider is recommended, not verified available.
- observations/facts: some environment facts are available, not necessarily mapped to capability availability.
- successful tool result: a tool produced output, but generic tool evidence is not automatically converted into capability verification.

Recommendation: reserve “available” for a future explicit availability/verification model, or qualify it as `provider_reported_available`, `locally_observed_available`, or `registered_operation_available`.

### 3. What evidence could verify a capability?

Potential evidence, depending on capability and target scope, includes:

- **Direct safe observation**: read-only observation that the target condition holds, such as Prometheus `up == 1` for an endpoint, a local platform/disk observation, or an imported inventory identity assertion.
- **Safe registered operation result**: a registered operation whose contract is explicitly read-only and whose output schema includes a positive, scoped verification result rather than `not_checked`.
- **Provider-reported availability**: read-only provider/API metadata saying the provider/backend has the target resource/capability available, with source identity, observed time, and confidence.
- **Independent corroboration**: multiple facts/evidence records agreeing on the same scoped claim, using current Fact Support aggregation.
- **Negative evidence**: explicit failed checks, provider errors, or `not_available` observations with causation and observed time.

For safety, evidence should identify at least: capability slug, target/scope, provider/source, method, whether the method was read-only, observed time, expiry, confidence, evidence IDs, and result status.

### 4. Is verification a Fact, Evidence, Relationship, Tool result, or separate model?

Current primitives suggest this split:

- **Evidence** should remain provenance: raw observation payloads and tool outputs.
- **Fact** can represent the state claim derived from evidence, e.g. `capability.verification_status = verified` for a scoped subject, if a canonical predicate is defined.
- **Relationship** may link a capability, provider, operation, and target, but relationships alone are not enough because verification has status, time, confidence, method, and expiry.
- **Tool result** is only one possible evidence source; it should not itself be the durable verification state.
- A **separate read model** or domain model may be warranted later to present verification status cleanly, but the smallest safe first step is to define vocabulary and inventory/tests before adding runtime behavior.

Recommendation: treat verification as an evidence-backed state claim, not as raw tool output. If implemented later, a dedicated `CapabilityVerification` read model could be projected from canonical Facts/Evidence, but that should follow documentation/tests and predicate inventory.

### 5. How would verification expire/stale?

Current Facts already support `expires_at`, and stale logic excludes expired facts from current support, exposes stale facts, and recommends refresh capabilities by predicate. A future verification claim could use the same temporal mechanics if represented as a Fact or Observation-derived Fact with `expires_at`.

A future verification status should distinguish:

- **verified_current**: unexpired positive verification fact/support exists.
- **stale_verification**: positive verification exists only as expired fact/support.
- **failed_current**: unexpired negative verification fact/support exists.
- **unverified**: no current or historical verification evidence exists for the scoped capability.
- **unknown_due_to_conflict**: current positive and negative evidence conflict without an unambiguous winner.

Expiry policy should be capability- and method-specific. For example, imported static inventory may be durable identity evidence but weak availability evidence; Prometheus `up` is a volatile measurement; a stub `not_checked` should not create positive verification at all.

### 6. Can registered operations verify capabilities without executing unsafe actions?

Yes, but only if the operation contract is explicitly safe/read-only and the result schema carries a real scoped verification outcome. Current architecture already allows L1 read-only operations and records successful outputs as evidence, but capability resolution must not call them automatically.

Examples of safe verification patterns:

- Query a read-only provider API using fixed allowlists.
- Inspect in-memory/projected Seed state.
- Parse local static inventory files.
- Use Python standard-library read-only local observation APIs.
- Return plan-only or `not_checked` results when a live check would require network/host mutation.

The existing `verify_ssh_access` is intentionally not a positive verifier: it is safe because it avoids network and host inspection, but its result is `not_checked`.

### 7. What is missing?

#### Verified

Missing:

- Canonical verification status vocabulary.
- Scope model: what target/entity/provider/operation the capability is verified for.
- Canonical predicate(s) or read model for capability verification.
- Evidence requirements for a positive verification.
- Expiry policy by capability/method/source.
- Tests proving capability resolution reports candidates only and does not imply verification.

#### Unverified

Missing:

- Explicit representation of “no verification evidence exists.”
- Distinction between unverified because never checked and unverified because only stubs/plans exist.
- UI/context language preventing `known_capability` or `registered_operations` from being interpreted as verified.

#### Stale verification

Missing:

- Verification-specific TTL/expiry recommendations.
- Mapping from stale verification predicates to refresh capability.
- Tests for expired positive verification no longer counting as current.

#### Failed verification

Missing:

- Negative verification status and reason vocabulary.
- Failed-check evidence shape: method, source, error/result, retryability, safety class.
- Conflict semantics between failed and successful verification evidence.

#### Provider-reported availability

Missing:

- Separate source classification or status for provider-reported availability.
- Provider trust/authority metadata.
- Distinction between provider recommendation and provider-reported current availability.
- Expiry/confidence defaults for provider availability reports.

#### Local observed availability

Missing:

- Status/method vocabulary for local read-only observations proving availability.
- Capability-specific mapping from observations to availability, e.g. whether `up == 1` proves `prometheus_query`, endpoint reachability, or service health.
- Scope normalization for endpoint-scoped versus host-scoped claims.

## Proposed terms Seed should use

| Term | Meaning | Current carrier | Verification implication |
| --- | --- | --- | --- |
| Requested capability | User/model requested an ability Seed lacks or needs | `ToolNeed.capability` | None |
| Catalog-known capability | Static catalog entry exists | `CapabilityCatalogEntry` | None |
| Registered operation candidate | Registry has visible registered operation tagged with capability | `ToolSpec.capabilities` + `ToolRegistry.list_tools_for_capability` | Operation candidate only |
| Provider recommendation | Catalog/ranker suggests provider/backend | `CapabilityRecommendation` / `RankedRecommendation` | Suggested provider only |
| Handoff candidate | Catalog recommendation includes backend/operation metadata | `capability_resolution.handoff_candidates` | External handoff metadata only |
| Provider-reported availability | Provider reports current availability | Missing | Would require evidence-backed status |
| Local observed availability | Local/read-only observation indicates availability | Missing as capability concept; observations/facts exist | Would require mapping |
| Verified capability | Current evidence proves scoped capability status | Missing | Requires future model/predicates |

## Smallest safe next step

The smallest safe next step is **documentation/tests/inventory only**:

1. Add a terminology/invariant test or architecture audit section asserting that `capability_resolution` fields are not verification statuses.
2. Add an inventory test that enumerates checked-in `verify_*` operations and documents whether each output can produce positive verification. Today, `verify_ssh_access` should be classified as `not_checked`/stub-only.
3. Add predicate/catalog documentation for proposed verification vocabulary without wiring it into Runtime, ToolExecutor, observation collection, or fact extraction.

Do **not** implement automatic verification from `capability_resolution`, do **not** execute registered operations from resolution, do **not** add LLM-driven verification, and do **not** mutate hosts.

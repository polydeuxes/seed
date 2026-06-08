# Capability Acquisition Reconciliation

## 1. Purpose and scope

This document audits whether Seed already defines a first-class lifecycle for
moving from an internally fulfilled capability need to a verified and preferred
external provider.

The concrete running example is repository line-of-code counting:

```text
Need
  count repository LOC by category

Internal fulfillment
  naive line/file/path counter

Candidate provider
  cloc

Verification
  fixture repositories, expected counts, explainable deltas, ignored dirs,
  docs/tests/code classification, blank/comment/generated/binary behavior

Adoption
  register count_loc with cloc as preferred provider and the internal counter as
  fallback

Evidence
  command, stdout, version, repo ref, timestamp, and verification record
```

The audit is documentation-only. It does not propose implementing `cloc`, adding
a `count_loc` operation, changing runtime behavior, or expanding production code.
It asks one architectural question: does Seed have a principled lifecycle for
moving from “I can do this myself slowly” to “I found, verified, and now prefer
an external provider”?

## 2. Existing concepts found

Seed already has many adjacent concepts. They are strong individually, but they
are not yet connected into a single provider-adoption lifecycle.

| Existing concept | Where it appears | Current meaning | Fit for provider adoption |
| --- | --- | --- | --- |
| `ToolNeed` | Domain model, runtime capability path, builder service | Durable request for a missing capability; often means `CapabilityNeed` in practice. | Good starting point for “need recognition,” but it does not model internal fulfillment, external candidate discovery, verification outcome, or adoption decision. |
| `Capability` | Domain model, toolkit manifests, capability catalog | Abstract ability Seed needs or can recommend. | Good abstraction for the repeated need, but not an acquisition lifecycle. |
| `CapabilityCatalog` / recommendations | Capability catalog and recommendation/ranking docs | Read-only capability-to-provider metadata and handoff suggestions. | Represents provider recommendations, not discovered candidates with verification/adoption state. |
| `ToolkitCandidate` | Builder service models and docs | Generated toolkit artifact candidate for validation/registration. | Useful for generated operation packages, but not general external-provider discovery or provider adoption. |
| Registered operation / `ToolSpec` | Domain model, registry, toolkit system | Callable operation contract with schema, implementation, policy action, visibility, status, risk, and capabilities. | Strong fit for the eventual `count_loc` operation contract, but no first-class preferred/fallback provider chain. |
| Operation contract | Domain model and toolkit system | The operation boundary: input schema, output schema, policy, visibility, examples, tests. | Strong fit for specifying what `count_loc` means independent of `cloc` or the naive counter. |
| Provider | Domain model and toolkit system | External system/backend exposing implementations; owns backend behavior and limits. | Correct boundary for `cloc`, but current docs mostly use provider as metadata/handoff/backend identity, not as an adopted implementation with trust/preference state. |
| Implementation | Domain model and toolkit system | Concrete backend adapter fulfilling an operation. | Correct place to distinguish `cloc` adapter from internal counter, but current docs do not define implementation preference, fallback order, or drift handling. |
| `ToolExecutor` | Runtime/tool execution docs | Executes registered operation implementations through `ToolRegistry` after validation and policy preflight. | Correct execution boundary after adoption, but should not own discovery, verification, adoption, or provider preference. |
| Verification | Capability verification docs and inventory | Evidence/fact/read-only interpretation of verification claims; no automatic execution or provider calls. | Strong building block for `cloc` verification records, but not tied to adoption decisions or preferred-provider selection. |
| Evaluation | Golden-case evaluation harness and docs | Model decision contract evaluation. | Adjacent, but not currently a provider-conformance verification system. |
| Reconciliation | Many docs | Documentation pattern for comparing current architecture to desired boundaries. | Good format for documenting this gap. |
| Acquisition | Knowledge acquisition docs | Observation → Evidence → Fact → Projection for knowledge. | Establishes evidence discipline, but it is about knowledge acquisition, not capability/provider acquisition. |
| Fallback | Various docs/code | Often means dependency-light fallback, stale-fact fallback, or internal backup behavior. | The word exists, but not as a modeled `FallbackProvider` for an operation after provider adoption. |
| Handoff / provider handoff | Handoff plan docs, capability catalog | Non-executable external-provider boundary. | Important boundary, but handoff is intentionally not provider adoption for registered execution. |
| Externalization | Architectural goal/framing | Keep core small and delegate behavior externally. | Present as an architectural direction, but not formalized as an operation/provider lifecycle. |

## 3. What Seed already supports

Seed already supports the most important architectural boundaries needed for a
future provider-adoption lifecycle.

### Need recognition and capability naming

Seed can represent a missing ability as a `ToolNeed`, and the domain model
explicitly notes that `ToolNeed` often means `CapabilityNeed` in practice. This
is enough to record the initial repeated need: “count repository LOC by
category.”

### Operation/provider separation

Seed already separates:

```text
Capability -> Operation -> Implementation -> Provider
```

This is the correct conceptual split for the `cloc` example:

- capability: repository LOC accounting;
- operation: `count_loc`;
- operation contract: input/output schemas and classification semantics;
- implementation A: internal naive counter;
- implementation B: `cloc` adapter;
- provider: local `cloc` binary/distribution.

### Registry and execution boundary

Seed already has a registered-operation path: operations become executable only
through registry exposure and `ToolExecutor` dispatch after validation and policy
preflight. That boundary is important because provider adoption must not imply
unreviewed execution.

### Capability catalog and recommendation metadata

Seed already has read-only capability-to-provider recommendations and ranking.
This can suggest that an external provider may be relevant. It is not yet enough
to prove that the provider satisfies an operation contract or should become the
preferred implementation.

### Verification as evidence-backed interpretation

The capability verification reconciliation already establishes that verification
should begin as vocabulary, predicates, evidence, fact support, contradictions,
and read-only inventory rather than as an execution subsystem. That is a good
fit for provider verification records such as:

- the `cloc` version observed;
- command invoked;
- fixture repository ref;
- expected and actual counts;
- deltas and explanations;
- timestamp and evidence ids;
- verification status and scope.

### Selection boundary work

The recommendation selection boundary already identifies a missing durable
selection concept for choosing among capability-resolution candidates. It also
warns that selection must not execute tools or call `ToolExecutor`. That is close
to the adoption part of this lifecycle, but it selects a resolution candidate for
a `ToolNeed`; it does not yet define provider adoption for an operation contract
with preferred and fallback implementations.

### Fallback-compatible architecture

Seed’s architecture can tolerate internal implementations as bootstrapping,
verification, or fallback paths because implementations are separate from
providers and execution is mediated through operation contracts. The missing part
is not the possibility of fallback; it is the explicit vocabulary and lifecycle
state that says when fallback is allowed and when an external provider is
preferred.

## 4. What Seed does not yet model

Seed does **not** currently define the full lifecycle:

```text
capability need
  -> naive/internal fulfillment
  -> external capability/provider candidate discovery
  -> provider verification
  -> operation/provider adoption
  -> preferred provider selection
  -> fallback / drift / deprecation
```

The gap is not that Seed lacks every primitive. The gap is that no document makes
these primitives one first-class lifecycle with names, transition boundaries, and
ownership rules.

Specific missing pieces:

1. **No durable distinction between capability need and internal fulfillment.**
   Seed can record a need and can register operations, but it does not name the
   state where a naive/internal implementation temporarily fulfills the need.

2. **No general `ProviderCandidate` lifecycle.** The capability catalog can
   recommend providers, and toolkit generation can create `ToolkitCandidate`s,
   but neither means “this external provider was discovered as a candidate to
   replace or augment an internal implementation for this operation.”

3. **No provider conformance-to-operation-contract record.** Capability
   verification can record scoped verification facts, but Seed does not yet say
   that a provider was verified specifically against an `OperationContract` with
   fixture cases and acceptance criteria.

4. **No explicit adoption decision.** There is no first-class
   `AdoptionDecision` that says “for operation `count_loc`, adopt provider
   `cloc` as an implementation because verification record X passed under
   contract fingerprint Y.”

5. **No preferred/fallback implementation chain.** A `ToolSpec` has one
   implementation today. The docs do not define `PreferredProvider`,
   `FallbackProvider`, fallback reasons, fallback order, or whether fallback is
   automatic/manual/policy-gated.

6. **No provider drift model tied to adoption.** Existing stale facts and
   fingerprint ideas are relevant, but Seed does not yet define provider drift
   such as a new `cloc` version, changed classification rules, missing binary,
   contract fingerprint mismatch, or verification expiration.

7. **No provider deprecation lifecycle.** Seed does not define how an adopted
   provider becomes deprecated, disabled, superseded, or removed while preserving
   fallback and evidence history.

8. **No externalization-specific rule.** Seed says external providers own
   execution and that core should stay small, but it does not state the rule:
   verified external providers should be preferred for repeated stable work while
   internal implementations remain for bootstrap, verification comparison, or
   fallback.

## 5. The smallest missing vocabulary

The smallest vocabulary addition is not a new execution engine. It is a small set
of documentation terms that connect existing primitives:

| Term | Proposed meaning |
| --- | --- |
| `CapabilityNeed` | Preferred semantic name for a repeated ability Seed needs. Existing `ToolNeed` can continue as the implementation name. |
| `InternalFulfillment` | A Seed-owned naive/internal implementation used to satisfy a need before adoption, or retained for bootstrap, verification comparison, or fallback. |
| `CapabilityCandidate` | A possible way to satisfy a `CapabilityNeed`; may be a registered operation, provider recommendation, handoff candidate, internal implementation, or manual path. |
| `ProviderCandidate` | An external provider or backend candidate that may implement an operation after verification and adoption. |
| `OperationContract` | The stable operation-level contract: name, purpose, schemas, classification rules, policy action, accepted behavior, evidence requirements, and test fixtures. Existing `ToolSpec` mostly carries the executable form. |
| `ProviderVerification` | Evidence-backed result showing whether a `ProviderCandidate` satisfies an `OperationContract` under a specific provider version/configuration/scope. |
| `AdoptionDecision` | Durable decision that binds a verified provider implementation to an operation contract, with rationale, evidence ids, contract fingerprint, provider fingerprint, and policy status. |
| `PreferredProvider` | Adopted provider implementation selected as the default for an operation in a scope. |
| `FallbackProvider` | Adopted or internal implementation available when the preferred provider is unavailable, stale, policy-blocked, or verification-invalid. |
| `ProviderDrift` | Detected mismatch between adopted provider assumptions and current provider/contract/environment, such as version change, missing binary, output schema change, or expired verification. |
| `ProviderDeprecation` | Lifecycle state for an adopted provider that should no longer be selected except under explicit compatibility or fallback rules. |

These terms can be documentation-only at first and mapped onto existing Seed
objects where possible.

## 6. Proposed lifecycle terms

A minimal lifecycle should be documented as a semantic overlay over existing Seed
architecture:

```text
CapabilityNeed
  -> InternalFulfillment
  -> CapabilityCandidate / ProviderCandidate discovery
  -> OperationContract definition or confirmation
  -> ProviderVerification
  -> AdoptionDecision
  -> PreferredProvider / FallbackProvider selection
  -> Execution through normal registered-operation path
  -> ProviderDrift monitoring
  -> ProviderDeprecation or replacement
```

### Lifecycle ownership

| Lifecycle phase | Seed core owns | External provider owns |
| --- | --- | --- |
| Need recognition | `CapabilityNeed` / `ToolNeed`, evidence, reconciliation, scope | Nothing |
| Internal fulfillment | Whether internal fallback exists and what contract it claims to satisfy | Nothing |
| Candidate discovery | Candidate record, source, rationale, evidence, risk notes | Provider existence and published behavior |
| Operation contract | Operation name, schemas, semantics, policy action, fixture expectations | Nothing |
| Provider verification | Verification criteria, evidence record, pass/fail/stale/disputed interpretation | Command/API behavior, version, outputs, provider-specific limits |
| Adoption | Adoption decision, trust/preference state, policy gates, evidence links | Nothing beyond being callable/available |
| Preferred selection | Default provider chain and fallback semantics | Runtime behavior of provider when invoked |
| Execution | Validation, policy, evidence recording, dispatch boundary | Actual operation effects and outputs |
| Drift/deprecation | Drift detection, stale state, deprecation decision, fallback transition | Changed versions/behavior/availability |

### Boundary rule

Provider adoption must not bypass policy, validation, approval, evidence
recording, or normal registered-operation execution. Adoption says which
implementation should be selected by default; it does not grant blanket authority
to execute that implementation.

## 7. `cloc` worked example

### 7.1 CapabilityNeed

```text
CapabilityNeed:
  id: need_count_repo_loc
  capability: repository_loc_counting
  summary: Count repository LOC by category.
  reason: Repeated architecture and documentation audits need stable LOC counts.
```

This may be represented today as `ToolNeed`, but documentation should treat it as
a capability need rather than as a request to build an internal tool.

### 7.2 InternalFulfillment

```text
InternalFulfillment:
  operation: count_loc
  implementation: internal_naive_counter
  purpose: Bootstrap and fallback.
  limitations:
    - approximate language detection;
    - limited generated/binary/comment handling;
    - vulnerable to path and vendored-directory classification mistakes.
```

The internal counter is acceptable only because it gives Seed an immediate,
inspectable baseline. It should not become the permanent preferred path if a
verified external provider satisfies the same operation contract better.

### 7.3 OperationContract

```text
OperationContract: count_loc
input:
  repo_path
  include_globs optional
  exclude_globs optional
  category_rules optional
output:
  totals by language/category
  file counts
  blank/comment/code counts where available
  ignored paths summary
  provider metadata
policy:
  read-only local repository inspection
semantics:
  stable classification of docs/tests/code/generated/binary/ignored dirs
  explainable deltas against fixtures and prior runs
```

The contract belongs to Seed, not to `cloc`. `cloc` is one possible provider that
may satisfy it.

### 7.4 ProviderCandidate discovery

```text
ProviderCandidate:
  provider: cloc
  source: discovered external utility / catalog recommendation / operator note
  candidate_for: count_loc
  rationale: mature LOC counter with language classification and blank/comment/code breakdowns
  risks:
    - version-specific behavior;
    - dependency availability;
    - generated/vendor/path classification differences;
    - output format changes.
```

Discovery should record why `cloc` is relevant, but discovery alone must not mark
it verified, preferred, or trusted.

### 7.5 ProviderVerification

```text
ProviderVerification:
  operation_contract: count_loc
  provider: cloc
  provider_version: <observed cloc version>
  fixture_repos:
    - minimal mixed docs/code/tests repo
    - generated/binary fixture repo
    - ignored-dirs fixture repo
    - language edge-case fixture repo
  expected_behavior:
    - counts known files and lines by category
    - classifies docs/tests/code according to contract mapping
    - reports blank/comment/code behavior where supported
    - excludes configured ignored dirs
    - produces explainable deltas when provider and internal counts differ
  evidence_required:
    - command
    - stdout/stderr or machine-readable output
    - exit code
    - provider version
    - repo ref / fixture ref
    - timestamp
    - contract fingerprint
    - verification record id
```

Verification should explicitly answer: “Does this `cloc` provider satisfy the
`count_loc` operation contract for this scope?” It should not merely answer:
“Does `cloc` exist?” or “Did a command run?”

### 7.6 AdoptionDecision

```text
AdoptionDecision:
  operation: count_loc
  operation_contract_fingerprint: sha256:...
  adopted_provider: cloc
  adopted_implementation: cloc_count_loc_adapter
  verification_record: verification_count_loc_cloc_...
  decision: adopt_as_preferred
  fallback: internal_naive_counter
  rationale:
    - fixture verification passed;
    - deltas are explainable and documented;
    - external provider is more complete for repeated stable LOC work;
    - internal implementation remains useful for bootstrap and drift fallback.
```

Adoption is the missing explicit transition. It is where Seed says that a
verified external provider should become preferred for a stable repeated
operation.

### 7.7 PreferredProvider and FallbackProvider

```text
ProviderSelection for count_loc:
  preferred_provider: cloc
  preferred_conditions:
    - cloc binary available
    - version matches verified range or verification remains fresh
    - policy allows local read-only command execution
    - output passes schema validation
  fallback_provider: internal_naive_counter
  fallback_conditions:
    - cloc missing
    - cloc verification stale or failed
    - output schema mismatch
    - policy blocks external command
    - user/operator explicitly requests internal comparison
```

Fallback should be visible in evidence. If Seed falls back to the internal
counter, the result should say so and explain why the preferred provider was not
used.

### 7.8 ProviderDrift

`cloc` drift examples:

- installed version differs from verified version/range;
- output columns or JSON format change;
- language classification changes in a way that affects fixture expectations;
- ignored directory defaults differ from contract expectations;
- binary disappears from the environment;
- verification record expires;
- operation contract changes but provider verification is still tied to the old
  contract fingerprint.

Drift should not automatically remove the provider. It should mark the provider
selection as needing re-verification or policy review and may trigger fallback.

### 7.9 ProviderDeprecation

`cloc` deprecation examples:

- provider is superseded by a better verified provider;
- provider is no longer installable or maintained in the target environment;
- provider repeatedly fails verification;
- policy no longer allows invoking that provider.

Deprecation should preserve historical evidence and adoption records. It should
only change future selection behavior.

## 8. Boundaries / non-goals

This lifecycle is not asking Seed to clone every Unix utility.

It is asking Seed to define how a repeated capability need moves from internal
baseline behavior to verified external-provider preference while preserving a
small core.

Non-goals:

- Do not implement `cloc` in this reconciliation document.
- Do not add a provider scheduler, verifier daemon, package installer, or retry
  system.
- Do not let capability resolution execute provider commands.
- Do not let adoption bypass `ToolExecutor`, policy, approval, validation, or
  evidence recording.
- Do not treat provider discovery as verification.
- Do not treat verification as adoption.
- Do not treat adoption as execution authorization.
- Do not require all providers to be external; internal implementations remain
  valid for bootstrap, comparison, and fallback.
- Do not require a giant new model before documenting the lifecycle.

## 9. Rejected solutions

### Rejected: keep adding internal implementations forever

A naive internal implementation is useful for bootstrapping, but making Seed own
every stable externalizable behavior grows the core and weakens the architectural
goal of externalizing behavior.

### Rejected: shell out to `cloc` whenever available without adoption

Availability is not conformance. A binary on `$PATH` does not prove the provider
satisfies Seed’s operation contract, output schema, evidence requirements, or
policy constraints.

### Rejected: make `ToolExecutor` discover and prefer providers

`ToolExecutor` should execute registered operation implementations after normal
validation and policy preflight. Discovery, verification, adoption, and
preference are reasoning/reconciliation concerns, not executor concerns.

### Rejected: collapse provider adoption into `CapabilityCatalog`

The catalog can recommend providers, but recommendation metadata is not
verification evidence or an adoption decision. Catalog entries should not become
hidden trust state.

### Rejected: collapse provider adoption into handoff plans

Handoff plans are non-executable external-provider boundaries. Provider adoption
for a registered operation is different: it chooses an implementation for a
callable operation contract while still preserving normal policy-gated execution.

### Rejected: prefer external providers solely because they are external

Externalization is an architectural preference for small core behavior, not a
reason to bypass evidence. External providers should be preferred only after they
are verified against the relevant operation contract and remain within policy.

## 10. Recommended next step

The smallest next step is to add canonical documentation vocabulary for
capability acquisition/provider adoption, likely by promoting the terms in
section 5 into the domain model or a small companion vocabulary document.

The next documentation change should define this lifecycle as first-class:

```text
CapabilityNeed
  -> InternalFulfillment
  -> ProviderCandidate
  -> OperationContract
  -> ProviderVerification
  -> AdoptionDecision
  -> PreferredProvider / FallbackProvider
  -> ProviderDrift
  -> ProviderDeprecation
```

After that, a future implementation can be deliberately small:

1. model a provider adoption record as evidence-linked state;
2. attach contract and provider fingerprints;
3. expose preferred/fallback provider metadata for registered operations;
4. require normal runtime validation/policy before execution;
5. surface drift/staleness without automatically executing verification.

## Direct answer

Seed does **not** already have this lifecycle clearly defined.

Seed already has most of the architectural pieces: `ToolNeed`/capability need,
capabilities, operation contracts, providers, implementations, toolkits,
registered operations, `ToolExecutor`, read-only provider recommendations,
verification-as-evidence, selection-boundary analysis, and fallback-compatible
separation of implementation from provider.

The smallest documentation/vocabulary gap is the missing first-class bridge from
verified provider candidate to adopted preferred implementation:

```text
InternalFulfillment
  -> ProviderCandidate
  -> ProviderVerification against an OperationContract
  -> AdoptionDecision
  -> PreferredProvider / FallbackProvider
  -> ProviderDrift / ProviderDeprecation
```

In short: Seed can currently describe needs, operations, providers,
recommendations, verification evidence, and execution boundaries, but it does
not yet name or own the adoption transition that makes a verified external
provider the preferred provider for a repeated stable operation while preserving
internal fallback.

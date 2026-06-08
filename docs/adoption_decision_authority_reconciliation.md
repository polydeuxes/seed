# Adoption Decision Authority Reconciliation

## 1. Purpose and scope

This document audits the next architectural gap after
[Capability Acquisition Reconciliation](capability_acquisition_reconciliation.md):
**who owns the `AdoptionDecision`?**

The prior reconciliation names this lifecycle:

```text
CapabilityNeed
  -> InternalFulfillment
  -> ProviderCandidate
  -> ProviderVerification
  -> AdoptionDecision
  -> PreferredProvider / FallbackProvider
  -> ProviderDrift / ProviderDeprecation
```

This audit is documentation-only. It does not implement provider adoption, add a
`cloc` adapter, change `ToolExecutor`, mutate the capability catalog, alter
runtime routing, or add tests. It asks a narrower authority question:

> When a provider candidate has been verified against an operation contract, what
> decides whether it becomes adopted or preferred?

The likely answer tested here is that Seed should treat `AdoptionDecision` as a
**durable knowledge/policy decision**: operator- or policy-authorized,
evidence-backed, scoped, replayable, and separate from execution dispatch.

## 2. Audit method

The audit searched existing docs and source for concepts related to:

- selection, recommendation, ranking, and capability-resolution candidates;
- approval, policy gates, execution authorization, and pending actions;
- verification, trust, confidence, evidence, support, drift, and staleness;
- capability catalog recommendations and handoff candidates;
- `ToolNeed` resolution and builder/generated toolkit candidates;
- operation registration, provider identity, implementation selection, and
  `ToolExecutor` dispatch;
- adoption, preferred provider, fallback provider, and provider deprecation.

The relevant sources are documentation and code-level ownership metadata. No
production behavior was changed.

## 3. Existing concepts found

Seed already has strong adjacent concepts, but none currently owns adoption
authority end-to-end.

| Existing concept | Current owner / surface | What it decides today | Why it is not `AdoptionDecision` |
| --- | --- | --- | --- |
| `ToolNeed` / capability gap | Runtime via `ToolNeedService` | Records that a capability is missing or requested and returns read-only capability-resolution metadata. | It starts the lifecycle but does not verify or adopt a provider. |
| `CapabilityCatalog` | Read-only catalog | Lists known capability-to-provider or handoff suggestions. | It recommends candidates; it is not evidence, verification, trust state, or policy authorization. |
| `RecommendationRanker` / recommendation selection | Ranking/selection service | Orders catalog recommendations against observed state and explains ranking factors. | Ranking chooses what to inspect or propose next; it does not bind a provider to an operation contract. |
| `ToolkitCandidate` / builder output | Builder service vocabulary and model | Represents generated toolkit artifacts before validation or registration. | It is candidate artifact state, not authority to prefer a provider implementation. |
| `ToolSpec` / registered operation | Registry and toolkit registration | Defines executable operation contract fields such as schemas, implementation, policy action, risk, visibility, status, and capabilities. | It is the executable surface after registration; it has one implementation today and no adoption evidence or preferred/fallback chain. |
| `ProviderVerification` vocabulary | Capability verification docs and inventory | Interprets evidence-backed verification facts, support, conflicts, confidence, and stale/unknown status. | Verification can prove conformance for a scope, but the prior reconciliation explicitly says verification is not adoption. |
| `PolicyGate` / tool execution policy | Policy layer | Allows, blocks, or requires confirmation/approval for a specific registered tool execution. | It authorizes individual execution attempts, not durable provider adoption. |
| `Approval` | Projected state and policy lookup | Provides an approval grant for an action/scope used by policy evaluation. | It can be evidence that an authorized actor approved adoption, but current approvals are execution-policy grants, not provider-selection records. |
| `PendingActionService` | Pending-action lifecycle | Records a specific policy-gated tool call awaiting approval and transitions it through approval/completion. | Pending action approval resumes a stored execution request; adoption is not an execution request. |
| `ExecutionAuthorization` / `ExecutionProposal` | Legacy/experimental planning side path | Stores secret-free metadata for historical proposal authorization. | Docs and models mark this as non-core/historical; it must not become provider adoption authority. |
| `ActionPlan` / `HandoffPlan` | Legacy/experimental planning and handoff side path | Records non-executable plans or handoffs. | Handoffs explicitly do not register tools, assert provider trust, or grant execution authorization. |
| `Runtime` | Canonical orchestration | Routes decisions, validates shape, creates `ToolNeed` metadata, and delegates registered calls to `ToolExecutor`. | Runtime may consume an adopted provider choice later, but should not decide provider trust/preference. |
| `ToolExecutor` | Execution layer | Validates registered tool calls, evaluates policy, creates pending actions, dispatches registered implementations, and records execution events. | The boundary docs already reject making `ToolExecutor` discover or prefer providers. |
| Event/reconciliation layer | Event ledger plus projections | Preserves append-only history and projected state. | It is the right persistence substrate for adoption records, but append/projection mechanics are not themselves authority. |

## 4. Is `AdoptionDecision` currently defined anywhere?

Partially, as vocabulary only.

`docs/capability_acquisition_reconciliation.md` defines `AdoptionDecision` as the
missing explicit transition that says a verified provider implementation should
be adopted for an operation, with rationale, evidence ids, contract fingerprint,
provider fingerprint, and policy status. It also gives a `cloc` example and
states that adoption must not bypass policy, validation, approval, evidence
recording, or normal registered-operation execution.

However, Seed does **not** currently define:

- a domain model named `AdoptionDecision`;
- an event kind such as `provider_adoption.decided`;
- a service that owns adoption decisions;
- a projected state view for adopted/preferred/fallback providers;
- explicit authority vocabulary for who can approve adoption;
- revocation, supersession, or stale-adoption transitions.

So the term exists in documentation as a proposed lifecycle concept, but the
owner and authority model are unresolved.

## 5. Closest current owner

The closest current owner is **not a single class**. It is the combination of:

```text
Capability verification evidence
  + policy/operator approval vocabulary
  + append-only event history
  + read-only projection into current provider-selection state
```

Among existing concrete concepts, the closest fit is the **knowledge/policy
layer** rather than runtime or execution:

- verification already fits Seed's evidence-backed knowledge discipline;
- policy/approval vocabulary already represents authorization constraints;
- `EventLedger` can preserve durable decision history;
- projected state can expose the current preferred/fallback provider chain;
- runtime and `ToolExecutor` can later consume that projected provider-selection
  state without owning it.

If Seed later adds code, the natural owner would be a small
`ProviderAdoptionService` or `CapabilityAdoptionService` that appends adoption
and revocation events after checking verification evidence and authority. The
service should sit beside capability verification / knowledge-policy services,
not inside `ToolExecutor`, provider adapters, `Runtime`, or the catalog.

## 6. Missing ownership vocabulary

Seed needs names for the authority boundary, not just names for lifecycle states.
The missing vocabulary is:

| Missing term | Proposed meaning |
| --- | --- |
| `AdoptionAuthority` | The actor or policy rule allowed to decide provider adoption for an operation and scope. |
| `AdoptionDecision` | Durable decision to adopt, reject, prefer, demote, revoke, supersede, or mark stale a provider implementation for an operation contract. |
| `AdoptionEvidence` | Verification record ids, operation contract fingerprint, provider fingerprint, observed version/configuration, fixture results, policy evaluation, rationale, and caveats used by the decision. |
| `AdoptionScope` | Workspace, environment, operation, contract fingerprint, provider version/range, risk class, and allowed use conditions for the decision. |
| `AdoptionStatus` | Current projected state such as `proposed`, `adopted_preferred`, `adopted_fallback`, `rejected`, `stale`, `revoked`, `superseded`, or `deprecated`. |
| `AdoptionRevocation` | Durable event/decision that stops future selection of a previously adopted provider without erasing historical evidence. |

## 7. Owner comparison

### Human operator

A human operator is a strong authority for adoption because adoption changes
Seed's durable provider preference. Operator approval is especially important
when adoption changes trust boundaries, invokes new local binaries or services,
changes dependency expectations, expands blast radius, or changes future default
behavior.

Operator approval should be recorded as evidence/metadata, not as an executable
pending action.

### Policy gate

A policy gate is a strong authority for low-risk or pre-approved adoption when
rules are explicit. Example: automatically adopt a read-only provider in a
workspace only if verification passed, the provider version is pinned or within a
verified range, the operation contract fingerprint matches, the risk class is
`L1`, and policy explicitly allows auto-adoption for that operation.

Policy can also deny or require operator approval. Policy should not replace
verification evidence.

### Verification threshold

Verification is necessary but insufficient. Passing verification means the
candidate appears to satisfy the operation contract under a scope. It does not
answer whether Seed should prefer it by default, whether an operator accepts the
dependency, whether policy allows the new provider, or whether fallback should
remain available.

Verification may be an input to auto-adoption policy, but it should not be the
sole owner.

### Recommendation / selection service

Recommendation selection is useful for ordering candidates and explaining why a
provider should be investigated. It should not create durable trust/preference
state. Ranking factors are not adoption authority.

### Capability catalog

The catalog is metadata and suggestion state. It can seed candidate discovery,
known provider names, handoff metadata, and rough risk notes. It must not become
a hidden trust store. A catalog recommendation is not verification and not
adoption.

### Runtime

Runtime owns orchestration and routing. It may read projected provider-selection
state when deciding which registered operation variant to call in a future
architecture, but it should not decide adoption. Runtime decisions are per input;
adoption is durable policy/knowledge state.

### Builder service

The builder can generate or validate toolkit artifacts. It can produce a
`ToolkitCandidate` or registration candidate, but generation success does not
mean adoption. Builder output must still be verified against the operation
contract and authorized by adoption authority.

### `ToolExecutor`

`ToolExecutor` must not own adoption authority. It owns registered-operation
execution after validation and policy preflight. Adoption may influence which
registered implementation is selected before execution, but executor dispatch
should not discover, verify, rank, or prefer providers.

### Event / reconciliation layer

The event layer is the right recording substrate: adoption decisions should be
append-only, replayable, and projected. But the event layer does not decide; a
service or authorized actor appends the decision with evidence.

## 8. Proposed authority model

Seed should model adoption as **evidence-backed selection authorization**:

```text
ProviderVerification passed
  -> AdoptionAuthority evaluates evidence + policy + scope
  -> AdoptionDecision is appended
  -> projection exposes PreferredProvider / FallbackProvider state
  -> Runtime/ToolExecutor may consume registered selected implementation later
```

Recommended default rule:

> Adoption should require explicit operator approval unless a policy rule
> authorizes automatic adoption for the operation, provider, verification
> threshold, scope, and risk class.

This gives Seed a safe default without blocking future automation. In practice:

- **manual adoption**: operator reviews verification evidence and records
  `adopt_as_preferred`, `adopt_as_fallback`, `reject`, or `needs_more_evidence`;
- **policy-authorized auto-adoption**: policy records which conditions allow
  adoption without a human click;
- **verification-only state**: a provider can remain verified-but-not-adopted;
- **recommendation-only state**: a provider can remain recommended-but-unverified;
- **execution-time approval**: still happens later and separately for specific
  tool calls if policy requires it.

## 9. What evidence should an adoption decision record?

An `AdoptionDecision` should record enough evidence to explain both why the
provider was adopted and why it remains safe to select later:

```text
AdoptionDecision:
  id: adoption_count_loc_cloc_2026_06_08
  workspace_id: seed
  operation: count_loc
  operation_contract_fingerprint: sha256:contract...
  provider: cloc
  provider_fingerprint:
    binary: /usr/bin/cloc
    version: "2.06"
    package_source: apt
  implementation: cloc_count_loc_adapter
  decision: adopt_as_preferred
  fallback_provider: internal_naive_counter
  authority:
    type: operator
    actor: alice
    policy_rule: provider_adoption.count_loc.read_only
  verification:
    record_id: provider_verification_count_loc_cloc_001
    status: passed
    verified_at: 2026-06-08T00:00:00Z
    expires_at: 2026-09-08T00:00:00Z
    fixture_refs:
      - fixtures/loc/python_project
      - fixtures/loc/mixed_docs_tests_code
  rationale:
    - fixture counts matched expected totals
    - deltas were explainable and documented
    - cloc handles comments/blanks/language classification better than baseline
    - internal counter remains fallback for bootstrap and drift comparison
  conditions:
    - provider version remains within verified range
    - output validates against count_loc schema
    - policy allows local read-only command execution
    - operation contract fingerprint remains unchanged
  non_authorizations:
    - does not execute cloc now
    - does not approve future high-risk tool calls
    - does not grant credentials or package installation permission
```

Minimum evidence fields:

1. operation id and contract fingerprint;
2. provider id, implementation id, and provider version/configuration;
3. verification record ids and result status;
4. evidence ids for command/output/fixture observations;
5. authority actor or policy rule;
6. decision type and scope;
7. rationale and known limitations;
8. preferred/fallback effect;
9. expiration or re-verification conditions;
10. supersession/revocation link when applicable.

## 10. What adoption must never authorize

Adoption must never authorize:

- immediate execution;
- bypassing `ToolExecutor`, registry validation, input/output schemas, or policy
  preflight;
- future execution approval for a specific tool call;
- host mutation, package installation, credential acquisition, network access,
  retries, scheduling, or long-running jobs;
- treating a provider recommendation as verified;
- treating a verification pass as unconditional trust;
- hiding fallback use from evidence or explanations;
- overwriting historical verification/adoption records;
- choosing providers whose current contract/provider fingerprint no longer
  matches the adopted scope.

Adoption says “this provider is authorized to be selected by default under these
conditions.” It does not say “run this provider now.”

## 11. How adoption differs from execution approval

Adoption and execution approval answer different questions.

| Question | Adoption decision | Execution approval |
| --- | --- | --- |
| What is being authorized? | Default provider/implementation selection for an operation and scope. | A specific runtime tool call with concrete arguments and scope. |
| When does it happen? | After verification and before future default selection. | During execution policy evaluation for a particular call. |
| What evidence is required? | Verification records, contract/provider fingerprints, rationale, policy/operator authority. | Tool name, arguments, risk class, scope, policy result, pending action or approval grant. |
| Who consumes it? | Provider selection/projection, future runtime routing. | `ToolExecutor` / pending-action resume path. |
| What does it not do? | It does not execute or approve any call. | It does not adopt, rank, verify, or prefer providers. |

Execution approval may be required even when a provider is adopted. Conversely, a
one-off approved execution must not imply that the provider should become
preferred.

## 12. How adoption differs from recommendation selection

Recommendation selection is pre-adoption candidate ordering. Adoption is
post-verification durable authorization.

```text
CapabilityCatalog recommendation
  -> ranking / selection rationale
  -> ProviderCandidate
  -> ProviderVerification
  -> AdoptionDecision
  -> PreferredProvider / FallbackProvider
```

A recommendation can say “`cloc` is probably relevant for LOC counting.” A
selection/ranking service can say “inspect `cloc` before another provider because
its score is higher.” Neither says “Seed should prefer `cloc` for `count_loc`.”
Only an adoption decision should do that, and only with verification evidence and
authority.

## 13. How adoption interacts with `PreferredProvider` and `FallbackProvider`

`PreferredProvider` and `FallbackProvider` should be projected effects of
adoption decisions, not independent hidden state.

Suggested rules:

1. A provider cannot become preferred unless there is a current adoption decision
   for the operation, contract fingerprint, scope, and provider fingerprint.
2. A fallback provider can be internal or external, but it should still have a
   documented basis: internal bootstrap contract, prior adoption, compatibility
   status, or explicit fallback decision.
3. Fallback use should be explainable with a reason such as missing provider,
   stale verification, schema mismatch, policy block, operator override, or
   provider drift.
4. Preferred/fallback order should be scope-aware. A provider may be preferred in
   one workspace/environment and fallback or rejected in another.
5. Preferred selection is not execution. The selected implementation must still
   enter normal registered-operation validation and policy checks.

In the `cloc` example, adoption can project:

```text
ProviderSelection(count_loc):
  preferred_provider: cloc
  fallback_provider: internal_naive_counter
  valid_while:
    - contract fingerprint unchanged
    - cloc version in verified range
    - verification not expired
    - local read-only execution remains policy-allowed
```

## 14. Revocation, supersession, and stale adoption

Adoption should be append-only and lifecycle-aware. Seed should not erase prior
adoption records because historical answers and execution traces may need to
explain which provider was preferred at the time.

Recommended transitions:

| Transition | Meaning | Typical cause | Future selection effect |
| --- | --- | --- | --- |
| `mark_stale` | Adoption may no longer be valid until re-verified. | Verification expired, provider version changed, operation contract changed, output schema drift. | Stop preferring provider or require fallback/re-verification. |
| `reverify` | New verification evidence refreshes confidence in the same provider/scope. | Scheduled or operator-triggered verification. | May restore current preferred status if policy permits. |
| `supersede` | A newer adoption decision replaces the previous preferred provider or contract version. | Better provider, changed contract, new adapter, updated policy. | Prefer superseding provider; preserve old record for history. |
| `revoke` | Authority removes adoption. | Security issue, policy change, repeated verification failure, operator decision. | Do not select provider except under explicit historical/recovery rules. |
| `deprecate` | Provider should be phased out but may remain available for compatibility fallback. | Provider unmaintained, no longer installable, replaced by better provider. | Avoid default selection; allow only explicit compatibility/fallback if policy permits. |

Revocation evidence should include who/what revoked it, why, affected scope,
replacement/fallback if any, and whether prior executions/results need caveats.

## 15. Boundaries and non-goals

This reconciliation does not propose:

- implementing `AdoptionDecision` in code;
- adding a provider-selection engine;
- changing current `ToolSpec` from a single implementation to a provider chain;
- changing `ToolExecutor`, `Runtime`, provider adapters, or registry behavior;
- adding automatic provider installation or command execution;
- adding a verifier daemon;
- merging adoption with pending-action approval;
- turning the capability catalog into trust storage.

The boundary is architectural vocabulary: adoption belongs to durable
knowledge/policy metadata. Runtime and execution layers may consume adopted
provider choices later, but they must not own adoption authority.

## 16. Rejected solutions

### Rejected: automatic adoption after verification

Verification is necessary evidence, but it is not authority. Automatic adoption
is safe only when an explicit policy rule says the verification threshold, risk,
operation, provider, scope, and fallback behavior are acceptable.

### Rejected: make `ToolExecutor` own adoption

`ToolExecutor` is intentionally the execution boundary. Giving it discovery,
verification, trust, ranking, or provider-preference authority would collapse
selection policy into dispatch and make execution behavior harder to audit.

### Rejected: make Runtime own adoption

Runtime is per-input orchestration. Adoption is durable cross-run state. Runtime
can route to services and later consume projected provider-selection state, but
it should not independently decide that a provider is trusted or preferred.

### Rejected: make recommendation ranking own adoption

Ranking explains candidate order. It does not prove contract conformance and does
not carry operator/policy authority.

### Rejected: make the capability catalog own adoption

Catalog entries are useful hints, not verified local truth. A catalog may suggest
`cloc`, but local adoption depends on actual operation contract, observed
provider version/configuration, verification evidence, policy, and scope.

### Rejected: make builder validation own adoption

Builder validation can establish that an artifact is structurally valid or safe
to register. It does not decide whether the generated or external provider
implementation should become preferred for future operation calls.

## 17. Direct answer

1. **Is `AdoptionDecision` currently defined anywhere?**  
   Yes, but only as proposed documentation vocabulary in
   `docs/capability_acquisition_reconciliation.md`. There is no current domain
   model, event, service, projection, or owner.

2. **If not, which existing concept is closest?**  
   The closest existing concept is the evidence-backed knowledge/policy layer:
   capability verification records plus policy/operator approval, persisted as
   append-only events and exposed through projection. No existing runtime or
   execution class is the right owner.

3. **Should adoption be automatic after verification, or require explicit
   operator/policy approval?**  
   Adoption should require explicit operator approval by default, with automatic
   adoption allowed only when an explicit policy rule authorizes it for the
   operation, provider, scope, risk class, verification threshold, and fallback
   conditions.

4. **What evidence should an adoption decision record?**  
   It should record operation and contract fingerprint, provider and provider
   fingerprint, implementation id, verification record ids, evidence ids,
   authority actor or policy rule, rationale, scope, limitations, preferred and
   fallback effects, expiration/re-verification conditions, and supersession or
   revocation links.

5. **What must adoption never authorize?**  
   Adoption must never authorize execution, bypass validation/policy/approval,
   grant credentials, install providers, mutate hosts, hide fallback, erase
   history, or treat recommendation/verification as unconditional trust.

6. **How does adoption differ from execution approval?**  
   Adoption authorizes default provider selection for future use under a scope.
   Execution approval authorizes a specific call with concrete arguments during
   policy evaluation. Either may exist without the other.

7. **How does adoption differ from recommendation selection?**  
   Recommendation selection ranks or chooses candidates to investigate.
   Adoption records a durable, evidence-backed, authorized provider preference
   after verification.

8. **How does adoption interact with `PreferredProvider` and
   `FallbackProvider`?**  
   Preferred and fallback providers should be projected effects of adoption
   decisions. They should be scoped, evidence-backed, explainable, and consumed
   by future selection/routing without bypassing execution policy.

9. **How should adoption be revoked, superseded, or marked stale?**  
   Through append-only decisions/events such as `mark_stale`, `reverify`,
   `supersede`, `revoke`, and `deprecate`. Each transition should preserve
   history, cite evidence/authority, update future selection behavior, and carry
   fallback or replacement guidance when available.

## 18. Conclusion

Seed should treat `AdoptionDecision` as durable knowledge/policy metadata, not
as execution. The best architectural owner is a future adoption authority service
or equivalent knowledge-policy boundary that records evidence-backed operator or
policy decisions. `Runtime`, `ToolExecutor`, provider code, builder code,
recommendation ranking, and the capability catalog may supply inputs or consume
projected outcomes, but they should not own adoption authority.

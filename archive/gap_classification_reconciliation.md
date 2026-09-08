> **Historical/stale after PR 1918.** This document is preserved as historical testimony only. Its Runtime, RuntimeLoop, Decision, Policy, Execution, ActionPlan, HandoffPlan, ExecutionProposal, ExecutionAuthorization, PendingAction, request_tool, call_tool, and builder-candidate language is not current architecture or operator instruction.

# Gap Classification Reconciliation

## 1. Purpose and scope

This documentation-only audit answers a narrow architecture question:
**what is a `CapabilityGap`, and how should Seed distinguish it from other
observed deficiencies?**

Recent reconciliations established two adjacent acquisition paths:

```text
Knowledge acquisition:
Observation
  -> Evidence
  -> Fact

Capability acquisition:
CapabilitySignal
  -> CapabilityEvidence
  -> CapabilityGap
  -> CapabilityNeed
  -> ProviderCandidate
  -> ProviderVerification
  -> AdoptionDecision
  -> PreferredProvider / FallbackProvider
```

The unresolved issue is that the implemented system has an explicit
`ToolNeed` path, but it does not yet define a full signal/evidence/gap/authority
path that decides when a durable `CapabilityNeed` should exist. This document
therefore audits whether Seed already has a coherent gap taxonomy or whether
`ToolNeed` is currently absorbing multiple deficiency types.

Scope boundaries:

- Documentation only.
- No production-code, test, runtime, event-schema, execution-path, provider,
  policy, or planner changes.
- No new autonomous subsystem, runtime loop, agent framework, verification
  executor, provider caller, or remediation engine.
- Preserve Seed's evidence-first architecture: observations and source material
  should become evidence; durable conclusions should cite supporting evidence or
  authority.
- Prefer the smallest vocabulary needed to route different deficiencies toward
  the right owner.

## 2. Existing concepts found

Seed already has many concepts that expose deficiencies or deficiency-adjacent
state, but they are distributed across knowledge, runtime, integrity,
capability, provider, and documentation surfaces.

| Existing concept | Current role | Deficiency signal it can expose |
| --- | --- | --- |
| `Observation` | Normalized source payload in the knowledge acquisition path. | Raw indication that something is present, missing, stale, conflicting, slow, manual, or unverified. |
| `Evidence` | Immutable provenance record used to support facts and explanations. | Source material for any future gap conclusion. |
| `Fact` / `FactSupport` | Projected claims and aggregate support with confidence, provenance, dimensions, timestamps, and expiry. | Missing support, stale support, conflicting support, or scoped capability-verification claims. |
| `Contradiction` | Read-only view over projected facts for exclusive predicates with incompatible values. | Contradiction or ambiguity that should be resolved as knowledge, not as a capability need by default. |
| `FactConflict` | Projected disagreement among facts for a subject/predicate/dimensions. | Knowledge conflict or competing current values. |
| Stale facts / refresh recommendations | Expired facts plus deterministic mapping from predicate to refresh capability. | Missing fresh knowledge; may indicate an observation capability only if refresh cannot be performed. |
| Unsupported facts | Evidence Graph views for facts without linked evidence. | Provenance/integrity deficiency, not missing capability. |
| Graph issues | Suspicious or invalid projected relationship edges with severity and hints. | Projection/ontology/integrity deficiency. |
| Projection Integrity Summary | Read-only aggregate counts for unsupported facts, conflicts, contradictions, graph issues, stale facts, refresh recommendations, and capability verification states. | Integrity and verification signals; no repair or execution. |
| `ToolNeed` | Durable model for a requested/missing capability with name, capability, reason, desired inputs/outputs, and status. | Current catchment for explicit missing-tool/capability requests. |
| `ToolNeedService` | Creates/deduplicates `ToolNeed` records from `request_tool` decisions and returns read-only capability-resolution metadata. | Explicit request-to-need path; not evidence aggregation. |
| `Capability` | Normalized semantic ability. | Identity axis for capabilities, operations, catalog entries, needs, and verification claims. |
| `CapabilityCatalog` | Read-only capability metadata and provider/handoff recommendations. | Missing catalog entry, known recommendations, candidate hints. |
| Registered `ToolSpec` / operation | Callable operation contract with schema, policy action, implementation, status, visibility, risk, and capabilities. | Missing operation, unavailable operation, inadequate implementation, or operation/provider mismatch. |
| Provider / implementation vocabulary | Provider is the backend identity; implementation is the concrete adapter or fulfillment path. | Missing provider, missing implementation, slow/inadequate implementation, provider drift. |
| `ToolkitCandidate` | Generated toolkit artifact candidate for a `ToolNeed`. | Implementation-candidate state after a need; not proof of need or adoption. |
| Capability verification inventory | Read-only interpretation of `capability_verified` facts over registered tools, ToolNeeds, and verification fact subjects. | Verified, unverified, stale, provider-reported, or unknown capability state. |
| Recommendation ranking / selection docs | Read-only ranking and proposed durable selection boundary for candidate resolution. | Candidate ordering or selected resolution; not adoption authority. |
| `ProviderCandidate` / `ProviderVerification` / `AdoptionDecision` vocabulary | Documentation-level lifecycle for external provider adoption. | Candidate, conformance, trust/preference, drift, expiry, revocation. |
| Reconciliation documents | Human audit records that identify architectural gaps and accepted/rejected changes. | Citable evidence or authority for durable architecture conclusions. |
| Runtime routing | `request_tool` creates ToolNeed metadata; `call_tool` executes only registered operations. | Missing capability requests are represented, but runtime does not classify all deficiencies. |

## 3. What Seed already supports

Seed already supports the following pieces of a future gap-classification model.

### Evidence-first knowledge deficiency support

The knowledge path can represent observations, evidence, facts, support,
confidence, source type, dimensions, timestamps, and expiry. It can also expose
unsupported facts, stale facts, fact conflicts, contradictions, graph validation
issues, and refresh recommendations. These are real deficiency concepts, but
most are knowledge or integrity deficiencies rather than capability deficiencies.

### Explicit ToolNeed creation

Seed can record an explicit missing/requested capability when the runtime receives
a `request_tool` decision. `ToolNeedService` normalizes the requested name and
capability, deduplicates against open needs by name or capability, appends a
`tool_need.created` event, and can later append status changes. This is the only
implemented durable need-creation path.

### Read-only capability resolution metadata

For a `ToolNeed`, Seed can report:

- whether the capability is known in the `CapabilityCatalog`;
- registered operations for the capability;
- ranked provider recommendations;
- handoff candidates derived from catalog recommendations.

This helps explain resolution options, but it does not execute, verify, adopt,
register, or select a provider.

### Verification as projected knowledge

Capability verification inventory interprets `capability_verified` facts and
FactSupport as `verified`, `unverified`, `stale`, `provider_reported`, or
`unknown`. This is important because it already distinguishes absence of
verification from negative proof, and it treats stale verification as a
freshness/integrity condition rather than as a new need by default.

### Provider adoption vocabulary in documentation

The adoption reconciliations distinguish candidate discovery, provider
verification, adoption authority, adoption decisions, preferred providers,
fallback providers, drift, deprecation, and revocation. Those concepts are not
implemented domain models yet, but the docs already reject the idea that a
catalog recommendation, ranking score, generated toolkit candidate, verification
pass, runtime route, or tool execution automatically equals provider adoption.

## 4. What Seed does not yet model

Seed does **not** yet model a first-class, general concept named `Gap` or a
first-class `GapClassification` object that routes deficiencies to owners.

More specifically, Seed does not yet define:

- a domain model named `Gap`, `KnowledgeGap`, `CapabilityGap`, `ProviderGap`,
  `ImplementationGap`, `VerificationGap`, `IntegrityGap`, or
  `ContradictionGap`;
- a canonical `GapEvidence` structure linking gap conclusions to observations,
  evidence ids, fact ids, audit references, source events, and authority;
- gap lifecycle states such as `observed`, `classified`, `accepted`, `deferred`,
  `resolved`, `stale`, `superseded`, or `disproven`;
- a durable event path from repeated evidence to a `CapabilityGap` and then to an
  authority-accepted `CapabilityNeed`;
- explicit ownership rules for when a deficiency should create a `ToolNeed`, when
  it should refresh knowledge, when it should verify a provider, when it should
  repair projection integrity, and when it should remain an unresolved
  contradiction;
- a way for `ToolNeed` to say whether it represents missing capability, missing
  provider, missing implementation, missing operation, or some mixture of those.

The current practical result is that `ToolNeed` is the nearest implemented place
to put an explicit capability deficiency, but its name and schema are broad
enough that it can absorb multiple unresolved gap types unless documentation and
future event vocabulary separate the concepts.

## 5. Existing deficiency categories

Seed already exposes the following deficiency categories, even though it does not
collect them under a single `Gap` taxonomy.

| Existing deficiency | Current surface | Primary class | Should it create a `CapabilityNeed`? |
| --- | --- | --- | --- |
| Missing LOC/fact/data value | Absence of relevant facts or answer support. | Knowledge deficiency. | No, unless evidence shows a recurring unsupported observation capability is needed. |
| Unsupported fact | Evidence Graph / integrity summary. | Integrity/provenance deficiency. | No. Link or acquire evidence; do not create a capability need merely because support is missing. |
| Stale fact | Fact expiry and refresh recommendations. | Knowledge freshness deficiency. | Usually no. Refresh existing knowledge. Create a need only if the refresh capability is itself absent or repeatedly manual. |
| Fact conflict | `FactConflict` read model. | Knowledge conflict. | No by default. Resolve or preserve conflicting support; create a need only if recurring conflict shows a missing measurement/verification capability. |
| Contradiction | `Contradiction` read-only view. | Contradiction/knowledge deficiency. | No by default. Investigate evidence and authority. |
| Graph issue | Graph validation issue inventory. | Projection/ontology integrity deficiency. | No. Repair catalog, facts, relationship projection, or source classification. |
| Unverified capability | Capability verification inventory. | Verification deficiency. | No by itself if the capability already exists; verify it. Yes only if lack of an adequate capability is also supported. |
| Stale capability verification | Capability verification inventory via expired fact support. | Verification freshness deficiency. | No. Re-verify or mark stale/revoked; do not create a new need unless the original capability cannot be satisfied. |
| Provider recommendation exists | `CapabilityCatalog` / ranker. | Candidate hint, not deficiency. | No. A recommendation is not a need. |
| No catalog entry | `CapabilityCatalog.get()` returns none. | Catalog/provider metadata deficiency. | Not necessarily. It may be a catalog gap or unknown capability; create a need only if demand evidence supports a durable capability. |
| No registered operation | Tool registry lookup for capability returns none. | Operation/implementation deficiency. | Often yes if a durable capability gap has been accepted; otherwise it is just resolution metadata. |
| Registered operation exists but is slow/inadequate | Operation/tool evidence, audit notes, performance observations. | Implementation or capability-quality deficiency. | Sometimes. If the capability exists but is inadequate, record a `CapabilityGap` or `ImplementationGap`; create/update a need only if durable better capability is required. |
| Provider candidate unverified | Provider verification docs/inventory. | Verification deficiency. | No. Verify candidate before adoption. |
| Provider verified but not adopted | Adoption reconciliation. | Adoption/authority deficiency. | No. Record adoption decision or defer/reject. |
| Adopted provider verification expired | Verification/adoption lifecycle docs. | Verification freshness / adoption drift. | No. Re-verify, demote, revoke, or fall back. |
| Repeated manual work or handoff | Reconciliation, handoff records, operator requests. | Capability deficiency signal. | Yes when recurrent, scoped, and accepted by authority. |

## 6. Proposed gap taxonomy

The smallest useful taxonomy should classify the **deficiency claim**, not the
future solution. The proposed vocabulary is conceptual and documentation-level;
it does not require new runtime behavior.

### 6.1 `Gap`

A `Gap` is an evidence-backed conclusion that Seed currently lacks something
needed to answer, observe, verify, execute, maintain, or explain within a defined
scope.

Minimal fields if later modeled:

```text
Gap
- id
- classification
- subject
- scope
- summary
- evidence_refs
- status
- resolution_path
- owner
- created_from
- observed_at / latest_observed_at
- expires_at or review_after
```

### 6.2 `KnowledgeGap`

A `KnowledgeGap` exists when the missing thing is a supported claim or fresh
answerable knowledge.

Examples:

- LOC information for a repository is missing.
- A fact exists but has expired.
- Seed lacks evidence for a projected fact.

Resolution path: observe/import/ask/refresh knowledge, attach evidence, update
facts, or explain that knowledge is unknown.

### 6.3 `CapabilityGap`

A `CapabilityGap` exists when evidence supports the claim that Seed lacks an
adequate durable ability to perform a normalized capability in a scope.

Important: capability gap is about **ability adequacy**, not only total absence.
The capability may be absent, internal-but-inadequate, too manual, too slow,
unverified for required use, or unavailable in the required scope.

Resolution path: decide whether to create/update a durable `CapabilityNeed`; then
resolve via registered operation, internal implementation, provider candidate,
handoff, or explicit no-op/defer.

### 6.4 `ProviderGap`

A `ProviderGap` exists when the capability/operation is understood, but Seed
lacks an acceptable provider candidate or provider coverage for the required
scope.

Examples:

- No known provider recommendation for `count_loc`.
- Existing providers do not support required languages or repository layout.
- Provider drift means the previously known backend no longer covers the scope.

Resolution path: discover candidate providers, update catalog metadata, create a
`ProviderCandidate` only after the need/operation contract is clear.

### 6.5 `ImplementationGap`

An `ImplementationGap` exists when the operation/capability is known, but the
concrete implementation is absent, incomplete, slow, inaccurate, unsafe,
unregistered, or mismatched to the operation contract.

Examples:

- A `count_loc` operation contract exists, but no implementation is registered.
- An internal counter exists but is too slow or cannot classify generated files.
- A provider adapter exists but does not return the required output schema.

Resolution path: implement, generate, validate, register, optimize, replace, or
fallback. This may satisfy an existing `CapabilityNeed`, but it is not always a
new need.

### 6.6 `VerificationGap`

A `VerificationGap` exists when Seed lacks current evidence that a capability,
provider, implementation, or adoption decision satisfies its scoped contract.

Examples:

- Provider candidate exists but has not been verified.
- Verification exists only as provider-reported availability.
- Verification fact has expired.
- Verification facts conflict.

Resolution path: collect verification evidence, run or ingest verification,
refresh stale verification, mark failed/disputed, or block adoption. Do not
create a `CapabilityNeed` merely because verification is missing.

### 6.7 `IntegrityGap`

An `IntegrityGap` exists when the projection, graph, evidence linkage, ontology,
or read-model consistency is deficient.

Examples:

- Unsupported facts.
- Graph validation issues.
- Projection integrity summary counts without drilldown navigation.
- Missing evidence links for facts.

Resolution path: repair provenance, catalogs, source classification, projection
logic, or documentation. This should not become a `ToolNeed` unless the repair
requires a durable missing capability that is independently evidenced.

### 6.8 `ContradictionGap`

A `ContradictionGap` exists when Seed has incompatible claims for the same scoped
subject/predicate semantics and lacks a resolved authoritative interpretation.

Examples:

- Two LOC providers report materially different totals for the same repository,
  revision, and classification contract.
- Two sources assert incompatible current status for an exclusive predicate.

Resolution path: preserve competing evidence, characterize severity, ask for or
collect adjudicating evidence, apply domain authority if available, or mark the
claim disputed. Do not route directly to `ToolNeed`.

### 6.9 Relationship among gap types

These gap types can stack, but the top-level classification should identify the
first owner that can make progress.

Example:

```text
Missing fresh LOC fact
  -> KnowledgeGap
Refresh requires count_loc ability and no adequate operation exists
  -> CapabilityGap
Known cloc candidate lacks fixture evidence
  -> VerificationGap
Verified cloc is accepted by policy/operator
  -> AdoptionDecision, not a new gap
```

## 7. Evidence requirements

Every gap conclusion should be supported by evidence appropriate to its class.
Seed should avoid converting vague dissatisfaction into durable needs.

| Gap type | Required evidence | Useful supporting evidence | Insufficient evidence by itself |
| --- | --- | --- | --- |
| `KnowledgeGap` | Missing/stale/unsupported claim, requested answer, subject/scope, source event or audit reference. | Fact ids, evidence graph view, expiry metadata, refresh recommendation, user question. | A provider recommendation or tool name. |
| `CapabilityGap` | Normalized capability hypothesis, scope, desired inputs/outputs, evidence of absence or inadequacy, recurrence or authority. | Repeated requests, manual work records, failed resolution, slow fallback measurements, handoff records, reconciliation findings. | One low-importance one-off request, or merely no catalog entry. |
| `ProviderGap` | Accepted need or operation contract plus evidence that no acceptable provider covers the scope. | Catalog miss, provider comparison, platform constraints, risk constraints, provider drift. | A ranked recommendation list. |
| `ImplementationGap` | Operation/capability contract plus evidence that the current implementation is missing or inadequate. | Registered tool metadata, validation report, runtime result, performance measurement, schema mismatch, generated `ToolkitCandidate` validation. | A preference for a different tool without contract evidence. |
| `VerificationGap` | Candidate/capability/adoption target plus absent, stale, failed, provider-reported, or conflicting verification evidence. | `capability_verified` facts, FactSupport, expiry, fixture results, version/config fingerprint. | Provider availability or catalog metadata alone. |
| `IntegrityGap` | Projection/evidence/graph/read-model issue id or inventory item. | Unsupported fact views, graph validation issues, integrity summary counts, source fact ids. | Missing feature desire. |
| `ContradictionGap` | Conflicting fact ids or result records for the same scoped claim/contract. | Evidence by fact id, provider outputs, observed times, severity, predicate cardinality. | Different results with different scopes or revisions. |

## 8. Resolution ownership

Gap classification should route the deficiency to the owner of the next safe
resolution step.

| Gap type | Primary owner | Appropriate actions | Actions to avoid |
| --- | --- | --- | --- |
| `KnowledgeGap` | Knowledge acquisition / observation / fact projection owner. | Observe, import, ask, refresh, attach evidence, mark unknown. | Creating ToolNeed unless a required observation capability is missing. |
| `CapabilityGap` | Knowledge/policy capability-need owner; currently closest to `ToolNeedService` for explicit requests. | Create/update/defer/reject `CapabilityNeed` or `ToolNeed` after evidence/authority; resolve candidates. | Letting runtime, provider, catalog, or LLM invent durable needs without evidence. |
| `ProviderGap` | Capability/provider discovery owner. | Search/update catalog, create `ProviderCandidate`, compare scope coverage. | Treat catalog recommendation as adoption or verification. |
| `ImplementationGap` | Toolkit/operation implementation owner. | Implement, generate, validate, register, optimize, fallback, retire. | Bypassing operation contract, policy, validation, or registry. |
| `VerificationGap` | Capability verification owner. | Ingest/run verification, refresh stale verification, mark disputed/failed, block adoption. | Creating a new need solely because verification is absent. |
| `IntegrityGap` | Projection/evidence/catalog integrity owner. | Repair evidence links, predicate metadata, graph ontology, projection assumptions, documentation navigation. | Treat unsupported/stale/invalid as false or as a missing tool. |
| `ContradictionGap` | Knowledge reconciliation / contradiction handling owner. | Preserve competing evidence, adjudicate, collect tie-breaker evidence, mark disputed. | Auto-selecting a provider or creating a ToolNeed as a shortcut. |
| Adoption/authority deficiency | Provider adoption / policy owner. | Adopt, reject, defer, demote, revoke, supersede, or mark stale. | Treat verification pass or recommendation score as adoption. |

## 9. `cloc` worked examples

The running capability is:

```text
count repository LOC by category with explainable classification and evidence
```

`cloc` is a possible provider candidate. It should not define the need by itself.

### Case A: LOC information is missing

Classification: `KnowledgeGap`.

Reasoning:

- The immediate missing thing is a supported LOC fact or answer for a specific
  repository/revision/scope.
- If Seed already has a registered/adopted way to observe LOC, the action is to
  refresh or observe knowledge.
- If no adequate LOC observation capability exists and the demand is recurrent or
  explicitly accepted, this can produce a downstream `CapabilityGap` and then a
  `CapabilityNeed`.

Appropriate action:

```text
KnowledgeGap
  -> observe/import/ask/refresh LOC evidence
  -> if refresh capability absent and durable demand exists:
       CapabilityGap -> CapabilityNeed
```

### Case B: LOC capability exists internally but is slow

Classification: primarily `ImplementationGap`; secondarily `CapabilityGap` if
slow performance makes the durable capability inadequate for the accepted scope.

Reasoning:

- The ability is not totally missing.
- The deficiency is quality/adequacy of the current internal implementation.
- Evidence should include timings, repository size, manual burden, expected
  latency, and output limitations.

Appropriate action:

```text
ImplementationGap
  -> optimize internal implementation, generate/register better implementation,
     or evaluate provider candidates
  -> update existing CapabilityNeed only if the accepted need is "adequate LOC
     counting" rather than merely "any LOC counting"
```

### Case C: Provider candidate exists but is unverified

Classification: `VerificationGap`.

Reasoning:

- The candidate provider (`cloc`) exists, but Seed lacks current evidence that it
  satisfies the operation contract for the scoped use.
- This should block adoption, not create a new `CapabilityNeed`.

Appropriate action:

```text
ProviderCandidate
  -> ProviderVerification required
  -> ingest fixture/version/output evidence
  -> verified | failed | disputed | stale
```

### Case D: Provider verified but not adopted

Classification: adoption/authority deficiency, not a capability gap.

Reasoning:

- Verification can show conformance.
- Adoption decides whether Seed should prefer, fallback to, reject, defer, or
  revoke a provider for future selection.
- The missing thing is an `AdoptionDecision`, not another need.

Appropriate action:

```text
ProviderVerification passed
  -> AdoptionAuthority / policy decision
  -> AdoptionDecision
  -> PreferredProvider / FallbackProvider projection
```

### Case E: Provider adopted but verification expired

Classification: `VerificationGap` with adoption drift/freshness impact.

Reasoning:

- The adopted provider may still be the selected provider historically, but the
  supporting verification is stale.
- This should trigger re-verification, demotion, fallback, revocation, or stale
  marking according to policy.
- It should not create a new `CapabilityNeed` unless the capability can no
  longer be satisfied at all.

Appropriate action:

```text
Expired verification evidence
  -> stale ProviderVerification / AdoptionStatus review
  -> re-verify, demote, fallback, revoke, or continue with caveat
```

### Case F: Conflicting LOC results from two providers

Classification: `ContradictionGap` or `FactConflict`, possibly with a
`VerificationGap` if the conflict undermines provider conformance.

Reasoning:

- If the two results are for the same repository revision, scope, counting rules,
  ignored paths, and output contract, the deficiency is incompatible evidence.
- If their scopes differ, it may not be a contradiction; it may be a dimension or
  contract mismatch.
- The action is adjudication and evidence comparison, not immediate provider
  adoption or new need creation.

Appropriate action:

```text
Conflicting LOC facts/results
  -> preserve evidence by provider/result
  -> compare contract, revision, dimensions, fixture expectations
  -> mark disputed or verify/adjudicate
```

## 10. Non-goals

This reconciliation does not propose:

- implementing `Gap` models, events, projectors, or services now;
- changing `ToolNeed`, `ToolNeedService`, `Runtime`, `ToolExecutor`,
  `ToolRegistry`, `CapabilityCatalog`, provider logic, or policy behavior;
- adding a planner, agent loop, autonomous gap detector, verification engine,
  refresh scheduler, provider caller, or remediation engine;
- treating every missing fact, stale fact, unsupported fact, graph issue,
  contradiction, unverified capability, provider recommendation, or slow
  implementation as a `ToolNeed`;
- making `cloc` a registered operation, preferred provider, dependency, or
  execution path;
- replacing existing evidence, fact, contradiction, integrity, or capability
  verification inventories.

## 11. Rejected solutions

### Rejected: `ToolNeed` as the universal deficiency bucket

This would make every unsupported fact, stale fact, graph issue, contradiction,
missing provider, unverified provider, slow implementation, and absent adoption
decision look like a missing tool. It would blur ownership and route knowledge,
integrity, verification, and adoption problems through capability acquisition.

### Rejected: every `KnowledgeGap` creates a `CapabilityNeed`

Missing information is often resolved by observation, import, refresh, asking the
user, or marking the answer unknown. A durable capability need is justified only
when evidence shows Seed lacks an adequate reusable ability, or when an operator
with authority explicitly accepts that need.

### Rejected: provider recommendation equals provider gap resolution

A catalog recommendation or ranked provider is only a hint. It is not a provider
candidate with scoped evidence, not verification, not adoption, and not a
preferred provider.

### Rejected: verification pass equals adoption

Verification answers whether a candidate appears to satisfy a contract in scope.
Adoption answers whether Seed should prefer, fallback to, reject, defer, revoke,
or supersede the provider for future use. These require different authority and
evidence.

### Rejected: contradiction creates a new need by default

Contradiction is a knowledge/evidence condition. It may reveal that Seed needs a
better measurement or verification capability, but only after classification and
evidence show the recurring inability is the durable problem.

### Rejected: a new engine owns all gaps

The smallest useful step is vocabulary and routing semantics over existing
observations, evidence, facts, inventories, runtime ToolNeeds, and documentation
reconciliations. A centralized gap engine would be premature and would violate
the current boundary against new autonomous subsystems.

## 12. Direct answer

### 1. Does Seed currently define a first-class concept of "gap"?

No. Seed uses gap language in documentation and `ToolNeedService` architecture
metadata, especially around capability gaps, but it does not define a general
first-class `Gap` model, event, projection, lifecycle, or taxonomy.

### 2. What existing deficiency concepts already exist?

Seed already has `ToolNeed`, unsupported facts, stale facts, refresh
recommendations, fact conflicts, contradictions, graph validation issues,
capability verification states, catalog misses, missing registered operations,
implementation/toolkit candidates, provider recommendations, and documentation
reconciliation findings.

### 3. Which are knowledge deficiencies versus capability deficiencies?

Knowledge deficiencies include missing facts, stale facts, unsupported facts,
fact conflicts, contradictions, missing evidence, and graph/projection issues.
Capability deficiencies include missing or inadequate reusable abilities, missing
registered operations for an accepted capability, repeated manual work, repeated
handoffs, inadequate internal fulfillment, and unresolved ability demand.
Provider, implementation, verification, integrity, and adoption deficiencies are
adjacent categories that should not automatically collapse into capability
needs.

### 4. Does `ToolNeed` currently represent a missing capability, provider, implementation, operation, or all of the above?

In implementation, `ToolNeed` represents an explicit requested/missing
capability with desired inputs/outputs and a reason. In practice, because Seed
lacks a gap taxonomy, it can be used to stand in for missing capability, missing
operation, missing implementation, missing provider/handoff target, or a general
capability-resolution request. That breadth is useful for the current MVP but is
also the risk: without classification, `ToolNeed` becomes the catch-all
destination for every deficiency.

### 5. What distinguishes the proposed gap types?

- `KnowledgeGap`: missing, stale, unsupported, or insufficiently evidenced
  knowledge.
- `CapabilityGap`: missing or inadequate durable ability in a scope.
- `ProviderGap`: missing acceptable provider coverage after the need/operation is
  understood.
- `ImplementationGap`: missing or inadequate concrete operation implementation.
- `VerificationGap`: missing, stale, failed, provider-reported-only, or disputed
  conformance evidence.
- `IntegrityGap`: evidence/projection/ontology/read-model consistency issue.
- `ContradictionGap`: incompatible claims requiring adjudication or additional
  evidence.

### 6. What evidence should support each type?

Each gap should cite class-appropriate evidence: facts/evidence/expiry for
knowledge; repeated demand, manual burden, failed resolution, or authority for
capability; accepted operation contracts and coverage analysis for provider;
validation/runtime/performance/schema evidence for implementation;
verification facts, fixtures, timestamps, and fingerprints for verification;
inventory issue ids for integrity; and conflicting fact/result ids for
contradictions.

### 7. What actions are appropriate for each type?

Knowledge gaps should be observed, imported, refreshed, asked about, or marked
unknown. Capability gaps should be accepted/deferred/rejected as needs and then
resolved. Provider gaps should discover or compare candidates. Implementation
gaps should implement, validate, register, optimize, replace, or fallback.
Verification gaps should verify or re-verify. Integrity gaps should repair
projection/evidence/catalog/documentation issues. Contradiction gaps should
preserve, compare, adjudicate, or mark disputed claims.

### 8. Which gap types should create `CapabilityNeeds`?

Only `CapabilityGap` should directly create or update a `CapabilityNeed`, and
only after evidence aggregation or explicit authority. `ImplementationGap` may
update an existing need or create one if it proves the accepted durable ability is
inadequate. `KnowledgeGap`, `ProviderGap`, `VerificationGap`, `IntegrityGap`, and
`ContradictionGap` should create a `CapabilityNeed` only when they reveal an
independent, durable missing ability supported by evidence.

### 9. Which gap types should never create `CapabilityNeeds` by themselves?

Unsupported facts, stale facts, fact conflicts, contradictions, graph issues,
provider recommendations, unverified provider candidates, expired verification,
and missing adoption decisions should not create `CapabilityNeeds` by themselves.
They have their own resolution paths.

### 10. How should gap classification interact with capability acquisition and provider adoption?

Gap classification should sit between evidence and need/adoption routing:

```text
Observation / Evidence / Fact / Reconciliation finding
  -> GapClassification
  -> if CapabilityGap and accepted by authority:
       CapabilityNeed / ToolNeed
       -> resolution candidates
       -> ProviderCandidate
       -> ProviderVerification
       -> AdoptionDecision
       -> PreferredProvider / FallbackProvider
  -> otherwise:
       route to knowledge refresh, integrity repair, contradiction handling,
       implementation work, verification, provider discovery, or adoption review
```

Classification prevents provider adoption from back-propagating into need
creation. A `ProviderCandidate` should come after an accepted need/operation
contract. `ProviderVerification` should evaluate conformance. `AdoptionDecision`
should record durable trust/preference authority. None of those downstream states
should be mistaken for the original capability gap.

## Conclusion

Seed does **not** already have a coherent gap taxonomy.

Seed has strong pieces: evidence-backed knowledge acquisition, explicit
`ToolNeed` creation, read-only capability resolution, capability verification
inventory, contradiction/integrity inventories, and documentation-level provider
adoption vocabulary. But it does not yet have a first-class classification layer
that distinguishes knowledge, capability, provider, implementation,
verification, integrity, contradiction, and adoption deficiencies.

The smallest missing distinction needed to prevent `ToolNeed` from becoming the
catch-all destination for every observed deficiency is:

```text
KnowledgeGap != CapabilityGap
```

Immediately after that, Seed should preserve these routing distinctions:

```text
CapabilityGap != ProviderGap
CapabilityGap != ImplementationGap
CapabilityGap != VerificationGap
CapabilityGap != IntegrityGap
CapabilityGap != ContradictionGap
VerificationGap != AdoptionDecision
ProviderCandidate != ProviderVerification != AdoptionDecision
```

In practical terms: only an evidence-backed or authority-accepted
`CapabilityGap` should become a durable `CapabilityNeed` / `ToolNeed`. Missing
knowledge should first route to knowledge acquisition; missing verification to
verification; contradictions to contradiction handling; projection issues to
integrity repair; provider absence to provider discovery; implementation
weakness to implementation ownership; and missing adoption to adoption authority.

# Capability Need Acquisition Reconciliation

## 1. Purpose and scope

This documentation-only audit asks where a durable `CapabilityNeed` / `ToolNeed`
comes from in Seed.

Recent reconciliations established the downstream provider-adoption lifecycle:

```text
CapabilityNeed
  -> InternalFulfillment
  -> ProviderCandidate
  -> ProviderVerification
  -> AdoptionDecision
  -> PreferredProvider / FallbackProvider
  -> Drift / Deprecation
```

They also established that `AdoptionDecision` is a durable knowledge/policy
choice, not execution. This document audits the unresolved upstream question:
**what turns observations, evidence, repeated failures, repeated manual work,
operator requests, provider handoffs, or reconciliation findings into a durable
`CapabilityNeed` / `ToolNeed`?**

The audit is intentionally limited:

- It does not change production code or tests.
- It does not implement a `cloc` operation, provider adapter, verifier, planner,
  or runtime loop.
- It does not assume an LLM should generate needs.
- It does not assign need creation to `ToolExecutor`, `Runtime`, providers, or an
  autonomous subsystem.
- It proposes only the smallest vocabulary needed to bridge existing knowledge
  acquisition and capability acquisition concepts.

The running example is line-of-code counting with `cloc`.

## 2. Existing concepts found

Seed already has many concepts adjacent to capability-need acquisition. The gap
is that they are not yet connected by a first-class lifecycle from evidence to a
stable need.

| Existing concept | Current meaning in Seed | Fit for capability-need acquisition |
| --- | --- | --- |
| `ToolNeed` | Durable model for a missing/requested capability with name, summary, capability, reason, desired inputs/outputs, status, and optional originating event. | This is the closest implemented representation of `CapabilityNeed`, but its creation path is request-driven rather than evidence-derived. |
| `ToolNeedService` | Runtime service that creates/deduplicates `ToolNeed` records from `request_tool` decisions and returns read-only capability-resolution metadata. | It owns current `ToolNeed` creation and status transitions, but only from an explicit decision payload; it does not aggregate observations into needs. |
| `Capability` | Normalized semantic ability Seed may need, recognize, recommend, or verify. | Good target vocabulary for need identity, but not itself a need, proof, provider, or lifecycle state. |
| `CapabilityCatalog` | Read-only catalog of known capability metadata and provider/handoff recommendations. | Can seed candidate discovery after a need exists; it does not create needs or prove gaps. |
| `RecommendationRanker` / `ToolRecommendationService` | Deterministically ranks catalog recommendations against current state and registered/known runtime signals. | Helps choose what to inspect next; it should not decide that a durable need exists. |
| `Observation` | Canonical normalized source payload with subject, predicate, value, confidence, metadata, dimensions, and optional expiry. | Best existing primitive for raw capability signals, but no capability-need projection currently consumes it. |
| `Evidence` | Immutable provenance record derived from observations or other inputs. | Correct support substrate for a future need; not enough by itself to create a durable need. |
| `Fact` / `FactSupport` | Projected interpreted claims with evidence ids, source type, confidence, recency, expiry, and aggregate support. | Strong fit for repeated signal aggregation and staleness, but no canonical capability-gap predicates exist today. |
| Projection / state | Append-only events projected into current state, including `ToolNeed` and open-tool-need views. | Correct persistence/read-model pattern for need lifecycle, but missing acquisition-specific event vocabulary. |
| Knowledge acquisition | Observation -> Evidence -> Fact -> Fact Support -> Projection. | Provides the discipline that capability need acquisition should reuse. |
| Reconciliation | Documentation audits that identify architectural gaps and proposed lifecycle terms. | A legitimate source of evidence/signals, but not currently machine-modeled as need evidence. |
| Gap detection / missing capability handling | Current `request_tool` path records a requested capability gap and resolves possible catalog/registered/handoff candidates. | Exists for explicit requests, not for repeated failures or repeated manual work. |
| Runtime routing | `request_tool` creates a `ToolNeed`; `call_tool` executes registered operations through `ToolExecutor`. | Runtime is the current router, not the architectural owner of long-term need acquisition. |
| Policy / approval | Controls execution outcomes and grants; adoption docs propose policy/operator authority for adoption. | Can authorize need acceptance or adoption decisions, but should not invent needs without evidence. |
| Provider handoff | Non-executable external-provider boundary and catalog metadata. | A handoff may produce evidence of an unmet or recurring capability, but handoff is not itself a durable need. |
| Builder service / `ToolkitCandidate` | Generates toolkit artifact candidates for a `ToolNeed`. | Downstream of a need; generation success is not proof the need was justified or resolved. |
| Selection | Proposed `CapabilityResolutionSelection` records which candidate was chosen for a `ToolNeed`. | Downstream of need creation; it selects among candidates, not whether a need should exist. |
| Inventory / verification | Read-only capability verification inventory over `capability_verified` facts and evidence. | Can help determine whether a need is unresolved, stale, or satisfied, but does not model need acquisition. |
| Action plans / handoff plans | Legacy/experimental non-executable planning artifacts. | May be evidence of repeated manual/external work, but should not own need creation. |

## 3. What Seed already supports

### 3.1 Explicit `ToolNeed` creation from a request

Seed currently defines one concrete creation path:

```text
user input
  -> model/decision emits request_tool
  -> Runtime routes request_tool
  -> ToolNeedService.create_from_decision(...)
  -> tool_need.created event
  -> State projection exposes open ToolNeeds
```

`ToolNeedService.create_from_decision` deduplicates open needs by normalized name
or capability, creates a `ToolNeed`, stores the request reason and optional
originating event, and appends `tool_need.created`.

This means Seed already supports **explicit request to durable need**, but only
through the `request_tool` decision path.

### 3.2 Read-only capability resolution after a need exists

Once a `ToolNeed` exists, Seed can report:

```text
known_capability
registered_operations
provider_recommendations
handoff_candidates
```

This is intentionally read-only. It does not execute tools, authorize actions,
create pending actions, or mutate the registry/catalog.

### 3.3 Evidence discipline for observations

Seed's knowledge architecture is already principled:

```text
Observation
  -> Evidence
  -> Fact Extraction
  -> Fact Support Aggregation
  -> State Projection
  -> Context Composition
```

Observations and evidence can capture user statements, operation outputs,
failed attempts, document excerpts, provider reports, and other source payloads.
Facts carry provenance, confidence, source type, expiry, and support/conflict
projection.

This is exactly the discipline capability-need acquisition should reuse.

### 3.4 Staleness and support primitives

Seed already has generic staleness and support concepts through fact expiry,
`FactSupport`, stale-fact refresh recommendations, and capability verification
inventory states such as verified, provider-reported, unverified, stale, and
unknown. These are not need-specific, but they are enough to avoid inventing a
separate truth system for capability needs.

### 3.5 Provider/candidate/adoption downstream concepts

Existing provider-adoption reconciliations already clarify that catalog
recommendations, provider verification, selection, adoption, preferred provider,
fallback provider, drift, and deprecation are downstream of a need. The current
open question is upstream: how enough evidence becomes the need.

## 4. What Seed does not yet model

Seed does **not** currently define a principled lifecycle for transforming
observations, evidence, repeated failures, repeated manual work, provider
handoffs, or reconciliation findings into a durable `CapabilityNeed` /
`ToolNeed`.

Specific gaps:

1. **No named signal vocabulary.** Seed does not have a first-class
   `CapabilitySignal` or `CapabilityObservation` term that says an observation is
   relevant to a possible capability gap.
2. **No capability-gap predicates.** Existing facts can represent arbitrary
   claims, but there is no canonical predicate such as
   `capability_gap_observed`, `manual_work_repeated`, `fallback_used`, or
   `capability_resolution_failed`.
3. **No aggregation threshold.** Seed does not define how many signals, over what
   time window, from which sources, or at what confidence become a durable need.
4. **No distinction between transient request and durable need.** A single
   operator request can create a `ToolNeed` today, but documentation does not
   say when that should remain transient, become a task, become an action plan,
   or become durable capability state.
5. **No acquisition authority.** Current code routes `request_tool` through
   runtime, but architecture does not define who is allowed to accept a derived
   capability need from evidence.
6. **No stale/resolved/superseded/disproven lifecycle for needs beyond current
   coarse `ToolNeedStatus`.** `ToolNeedStatus` has proposed/accepted/generating/
   generated/validating/validated/registered/rejected, but it does not explicitly
   model stale, resolved by existing operation, superseded by broader need, or
   disproven by negative evidence.
7. **No causal bridge from reconciliation findings.** Reconciliation docs can say
   a capability is missing, but there is no canonical event/fact path that turns
   repeated audit findings into a `ToolNeed` with evidence ids.
8. **No bridge from provider handoff/manual work to need.** Handoffs and action
   plans are non-executable/historical; repeated use can be evidence, but there
   is no projection that converts those repetitions into a capability need.
9. **No bridge from failed resolution.** If capability resolution returns no
   registered operations, no catalog entry, or only handoff/manual options, Seed
   does not record that as evidence for a durable capability gap unless the
   original request already created a `ToolNeed`.

The current architecture is therefore **request-driven**, not
**evidence-acquisition-driven**.

## 5. The smallest missing vocabulary

Seed does not need a new engine, planner, or autonomous loop. The smallest
missing bridge is a thin vocabulary that classifies evidence before a durable
need is accepted.

| Term | Proposed meaning |
| --- | --- |
| `CapabilitySignal` | Any raw event, observation, fact, audit finding, failure, handoff, manual step, or operator request that may indicate an unmet or under-served capability. A signal is not yet a need. |
| `CapabilityEvidence` | Evidence/fact support attached to one normalized capability hypothesis. It includes source, time, recurrence, scope, confidence, examples, and negative evidence. |
| `CapabilityGap` | A derived conclusion that current registered operations, catalog candidates, provider recommendations, or internal fallbacks do not adequately satisfy the capability in a scope. A gap is evidence-backed but may still be transient. |
| `CapabilityNeed` | A durable accepted need for Seed to track, resolve, satisfy, verify, or reject. Existing `ToolNeed` remains the current implementation name. |
| `CapabilityResolution` | The current relation between a need and possible ways to satisfy it: registered operation, provider recommendation, handoff, manual path, internal fulfillment, or no candidate. |
| `CapabilitySatisfied` | A state meaning the need is currently satisfied by a registered/adopted/verified capability for the relevant scope. |
| `CapabilitySuperseded` | A state meaning a more general, more accurate, or replacement need now owns the requirement. |
| `CapabilityStale` | A state meaning the need or its evidence has aged, its scope changed, its supporting pattern stopped recurring, or its resolution metadata drifted. |

The key distinction is:

```text
CapabilitySignal
  -> evidence/fact support aggregation
  -> CapabilityGap conclusion
  -> authorized CapabilityNeed / ToolNeed creation or update
```

`CapabilityObservation` can be used as a synonym for normalized observations
about capability signals, but it is not necessary if Seed reuses existing
`Observation` plus capability-specific predicates. The smallest vocabulary is
`CapabilitySignal`, `CapabilityGap`, and `CapabilityNeed` with evidence links.

## 6. Proposed acquisition lifecycle

A minimal lifecycle should be documented as a semantic overlay over the existing
Observation/Evidence/Fact/Projection and `ToolNeed` systems:

```text
CapabilitySignal
  -> Observation / Evidence
  -> Fact / FactSupport
  -> CapabilityGap projection
  -> NeedAuthority accepts, rejects, or defers
  -> CapabilityNeed / ToolNeed event
  -> CapabilityResolution candidates
  -> verification / selection / adoption lifecycle
  -> satisfied, stale, superseded, rejected, or disproven
```

### 6.1 Signal intake

Signals may come from:

- explicit operator request;
- repeated user requests;
- repeated manual steps in docs/audits;
- repeated internal fallback usage;
- repeated provider handoff for the same work;
- failed capability resolution;
- missing registered operation or missing catalog coverage;
- repeated verification failures;
- observed workflow patterns;
- reconciliation findings;
- support/conflict/staleness diagnostics.

Signals should be recorded as observations/evidence when practical. A signal
should include:

```text
source_type: user | discovery | provider | imported | inferred
capability hypothesis
scope/workspace/environment
source event/document/reference
observed time
confidence
raw payload or excerpt
whether the signal is positive, negative, or ambiguous
```

### 6.2 Evidence aggregation

A projection or audit should group signals by normalized capability and scope.
Useful aggregation dimensions include:

- number of independent requests;
- number of distinct workflows/audits affected;
- repeated manual effort duration or complexity;
- repeated internal fallback usage;
- failed or absent registered-operation matches;
- repeated handoffs to the same external provider;
- operator priority or explicit acceptance;
- business/architectural importance;
- freshness and recurrence;
- negative evidence that the need was one-off, already satisfied, or obsolete.

Aggregation should not require an LLM. A human audit, deterministic projection,
CLI import, or future service could produce the same evidence-backed conclusion.

### 6.3 Gap conclusion

A `CapabilityGap` exists when evidence supports the claim that Seed lacks an
adequate durable way to satisfy a normalized capability in a scope.

A gap should remain separate from a durable need because some gaps are not worth
tracking. For example, a one-time request for a novelty transformation may be a
valid task but not a durable capability need.

### 6.4 Need acceptance

A durable `CapabilityNeed` / `ToolNeed` should be created or updated only after
one of these authority paths:

1. **Explicit operator request.** An authorized operator says this capability
   should be tracked. This may create a need immediately, but it should still
   preserve request evidence and scope.
2. **Policy threshold.** A deterministic policy accepts the gap because recurrence,
   cost, risk, or failure thresholds are met.
3. **Reconciliation decision.** A documentation or architecture reconciliation
   records that the gap should become durable, with cited evidence.

Need acceptance should append an event with evidence ids or source references.
The event can initially be the existing `tool_need.created`, but the semantics
should be clearer: it records an accepted durable capability need, not merely a
single prompt-shaped request.

### 6.5 Resolution and downstream handoff

After a need exists, existing resolution concepts apply:

```text
CapabilityNeed / ToolNeed
  -> CapabilityCatalog lookup
  -> RecommendationRanker ordering
  -> registered operation candidates
  -> handoff candidates
  -> manual/no-op candidate
  -> CapabilityResolutionSelection
  -> ProviderCandidate / ProviderVerification / AdoptionDecision
```

Need acquisition must stop before provider verification/adoption. It says **what
ability is durably needed**, not which provider should implement it.

## 7. `cloc` worked example

### Case A: Operator asks for LOC counts once

```text
Signal:
  operator request: "count repository LOC"
Evidence:
  input event, workspace, repo scope, timestamp, requested output shape
Likely classification:
  transient request or task
Durable need?
  not automatically
```

A single operator request may justify performing the task once. If the operator
explicitly says "Seed should track LOC accounting as a reusable capability," it
can become a `CapabilityNeed` immediately by operator authority. Otherwise, it is
weak evidence: useful support if the pattern repeats, but not enough by itself to
prove a durable capability gap.

### Case B: Operator repeatedly asks for LOC counts across audits

```text
Signals:
  multiple operator requests for the same LOC capability
Evidence:
  input events, audit references, outputs requested, recurrence dates, scope
Gap conclusion:
  repeated audit workflow needs stable LOC accounting
Durable need?
  yes, once recurrence/importance threshold or operator acceptance is recorded
```

Repeated requests across audits are strong evidence for a durable
`CapabilityNeed` because they show the ability is part of a recurring workflow,
not a one-off task.

### Case C: Seed repeatedly performs a naive internal counter

```text
Signals:
  internal fallback used repeatedly for LOC counts
Evidence:
  command/output events or audit notes, implementation identity,
  limitations, deltas, manual corrections, timestamps
Gap conclusion:
  internal fulfillment exists but may be inadequate or too manual
Durable need?
  yes, if the repeated fallback is serving a stable capability and remains
  insufficient, expensive, inaccurate, or not verified
```

Repeated naive internal counting should become evidence for a durable need when
it demonstrates stable demand plus known limitations. It is not merely "we ran a
script"; the important evidence is recurrence, manual burden, and inadequacy
relative to the desired operation contract.

### Case D: Seed repeatedly hands off LOC counting externally

```text
Signals:
  repeated provider/manual handoffs for LOC counts
Evidence:
  handoff records, provider names, returned outputs, manual steps,
  unresolved registered-operation matches, timestamps
Gap conclusion:
  Seed lacks an internal registered/adopted capability and relies on handoff
Durable need?
  yes, if handoff recurrence shows this is a recurring Seed workflow
```

Repeated handoff is evidence of a capability gap, not a solution by itself. It
may later seed a `ProviderCandidate` such as `cloc`, but handoff does not imply
provider verification, adoption, trust, credentials, or execution authorization.

### Case E: A reconciliation audit repeatedly identifies missing LOC accounting

```text
Signals:
  repeated reconciliation findings: "missing LOC accounting"
Evidence:
  reconciliation documents, cited workflows, affected decisions, recurrence,
  current workaround descriptions
Gap conclusion:
  architecture has an unresolved stable capability gap
Durable need?
  yes, when reconciliation records acceptance or recommends durable tracking
```

Reconciliation findings are legitimate evidence because Seed's architecture uses
reconciliation to surface durable boundaries and gaps. They should create or
update a need only when the finding is accepted as durable, scoped, and supported
by source references.

### When does `cloc` enter?

`cloc` should not define the need. The need is:

```text
count repository LOC by category with explainable classification and evidence
```

`cloc` enters later as a `ProviderCandidate` or catalog recommendation after the
need/gap exists. `cloc` becomes preferred only after verification and adoption.

## 8. Ownership and authority

### Current implemented owner

The current implemented owner for creating a `ToolNeed` is `ToolNeedService`,
routed by `Runtime` for `request_tool` decisions. That is a concrete code owner,
but it is not yet a full architectural owner for evidence-derived capability
need acquisition.

### Proposed architectural owner

Capability-need creation should belong to the **knowledge/policy layer**, not to
execution. A future owner could be a small `CapabilityNeedService` or an expanded
`ToolNeedService` with explicit evidence-backed creation methods. It should:

- read observations/facts/reconciliation findings;
- validate capability identity and scope;
- attach evidence ids or source references;
- deduplicate against open and satisfied needs;
- append need-created/status events;
- never execute tools;
- never call providers;
- never register toolkits;
- never rank providers as a substitute for evidence;
- never bypass operator or policy authority for durable tracking.

### Authority model

Need creation should be authorized by one of:

| Authority | What it can authorize | Boundary |
| --- | --- | --- |
| Operator | Immediate durable tracking of a capability need. | Operator request is evidence and authority, but still not provider adoption. |
| Policy threshold | Durable tracking when deterministic recurrence/impact/failure thresholds are met. | Policy accepts the need; it does not select/adopt providers. |
| Reconciliation decision | Durable tracking after an audit records a supported architectural gap. | Reconciliation creates knowledge/policy state, not runtime execution. |

Runtime may continue to route explicit requests, but runtime should not be the
semantic authority for evidence-derived needs. `ToolExecutor` and providers
should never own need creation.

## 9. Staleness / resolution / supersession

A durable capability need should preserve history while allowing current status
to change.

| State | Meaning | Evidence / transition |
| --- | --- | --- |
| `proposed` | A possible need has been recorded but not accepted as durable. | Early signal or explicit request without acceptance. |
| `accepted` | Seed has agreed to track the need as durable. | Operator, policy threshold, or reconciliation acceptance. |
| `satisfied` / `resolved` | A registered, verified, or adopted capability currently satisfies the need in scope. | Registered operation or adopted provider, verification/adoption evidence, resolution selection. |
| `stale` | The need or its support is no longer fresh enough for current decisions. | No recent recurrence, expired evidence, changed scope, changed operation contract, stale verification, or catalog/registry drift. |
| `superseded` | Another need now covers this one. | Broader/replacement need id and rationale. |
| `rejected` | Authority decides not to track the proposed need. | Rationale and negative evidence. |
| `disproven` | Evidence shows the gap was mistaken: capability already exists or the premise was wrong. | Registered/verified capability existed, audit correction, or contradictory facts. |

`ToolNeedStatus` can continue to exist, but documentation should clarify whether
status values refer to builder/registration progress or to capability-need truth.
A need can be "generated" in a builder sense and still be unresolved in a
provider/adoption sense. Conversely, a need can be satisfied by an existing
registered operation without any toolkit generation.

## 10. Interaction with CapabilityCatalog recommendations and ProviderCandidates

Capability need acquisition should happen **before** catalog recommendation and
provider-candidate adoption.

Recommended ordering:

```text
CapabilitySignal
  -> CapabilityGap
  -> CapabilityNeed / ToolNeed
  -> CapabilityCatalog recommendations
  -> RecommendationRanker ordering
  -> CapabilityResolutionSelection
  -> ProviderCandidate
  -> ProviderVerification
  -> AdoptionDecision
```

Key rules:

- A catalog entry can help normalize a capability name, but catalog presence does
  not prove a need exists.
- A catalog recommendation can be evidence that a provider might satisfy a need,
  but it is not evidence that the need is durable.
- A high-ranked recommendation is not a `CapabilityNeed` and not an
  `AdoptionDecision`.
- A missing catalog entry can be evidence for a knowledge/catalog gap, but not
  automatically for a tool need.
- A registered operation candidate can satisfy or disprove a need if it matches
  the operation contract and scope, but registration alone is not verification.
- A `ProviderCandidate` should be created only after the capability need and
  operation semantics are clear enough to evaluate provider conformance.

## 11. Distinguishing transient request, task, action plan, and capability need

| Concept | Unit of meaning | Durability | Evidence needed | Owner |
| --- | --- | --- | --- | --- |
| Transient request | One user/operator asks for an outcome now. | Ephemeral unless accepted. | Input event and context. | Runtime/input handling. |
| Task | A bounded piece of work to satisfy a request. | Usually scoped to a session/audit. | Request, constraints, expected output. | User/operator/workflow; not necessarily Seed state. |
| Action plan | Non-executable text plan for how work could be done. | Historical/legacy side path; not canonical execution. | Need plus chosen provider/recommendation rationale. | Planning service where retained; not runtime core. |
| Capability need | Durable accepted ability Seed should track, resolve, verify, or satisfy. | Durable, event-sourced, status-bearing. | Aggregated signals or explicit authority, evidence ids/source refs, scope, expected inputs/outputs, reason. | Knowledge/policy `ToolNeed`/future `CapabilityNeed` owner. |

A one-time LOC request is a transient request/task. Repeated LOC counting with
manual burden or failed resolution becomes evidence. A durable `CapabilityNeed`
exists only when the evidence-backed gap is accepted for tracking.

## 12. Non-goals

- Do not introduce a new autonomous planner, agent loop, scheduler, verifier, or
  provider discovery engine.
- Do not make LLM output the authority for durable needs.
- Do not make `Runtime`, `ToolExecutor`, provider adapters, `CapabilityCatalog`,
  `RecommendationRanker`, action plans, or handoff plans own capability-need
  creation.
- Do not treat a provider recommendation as proof of a capability gap.
- Do not treat repeated execution alone as proof; recurrence must be tied to
  capability semantics, scope, and adequacy.
- Do not require every transient request to become a durable need.
- Do not collapse need acquisition into provider adoption.
- Do not implement `cloc` or any LOC-counting provider in this document.

## 13. Rejected solutions

### Rejected: `CapabilityNeed` is whatever the LLM asks for

A model decision can carry an explicit `request_tool` payload today, but durable
needs should be evidence-backed and authority-accepted. Model output is at most a
signal or request, not the lifecycle owner.

### Rejected: runtime owns discovery because it currently routes `request_tool`

Runtime is a router. It can append events through owner services, but evidence
aggregation and durable need acceptance are knowledge/policy responsibilities.

### Rejected: `ToolExecutor` creates needs when a tool is missing

A failed tool call or missing visible tool can be evidence for a gap, but
`ToolExecutor` must stay in the execution boundary. It should not discover,
rank, accept, verify, or adopt capabilities.

### Rejected: the catalog creates needs

`CapabilityCatalog` is read-only metadata. A catalog entry means Seed knows about
a capability or provider suggestion, not that this workspace has a durable need.

### Rejected: repeated manual work automatically creates needs

Repeated manual work is strong evidence, but automatic creation without scope,
thresholds, evidence links, or authority would produce noisy durable state.
Manual work should become a `CapabilitySignal`, then support a `CapabilityGap`,
then be accepted as a need.

### Rejected: provider handoff is equivalent to provider candidate or adoption

Handoff can show that work is repeatedly externalized. It does not prove provider
conformance, trust, registration, credential availability, or adoption.

### Rejected: action plans are needs

Action plans describe possible steps. They are downstream planning artifacts and
are currently legacy/experimental. They should not be the source of truth for
whether a capability need exists.

## 14. Direct answer

### 1. Does Seed currently define how a `CapabilityNeed` is created?

Partially. Seed implements creation of `ToolNeed` from an explicit
`request_tool` decision through `Runtime` and `ToolNeedService`. Seed does not
currently define a principled acquisition lifecycle that derives a durable
`CapabilityNeed` from observations, repeated failures, repeated manual work,
provider handoffs, or reconciliation evidence.

### 2. Is `CapabilityNeed` treated as an input, a discovery, an observation, or a derived conclusion?

Today, the implemented `ToolNeed` path treats it mostly as an **input/request**:
a decision payload says a missing tool/capability should be recorded. The
architecture should treat a durable `CapabilityNeed` as an **accepted derived
conclusion** when it comes from evidence aggregation, while still allowing an
explicit operator request to create one by authority.

### 3. What existing concepts are closest to capability-need acquisition?

The closest concepts are:

1. `ToolNeed` as the durable record;
2. `ToolNeedService` as the current creation/deduplication service;
3. Observation/Evidence/Fact/FactSupport as the evidence pipeline;
4. reconciliation docs as a human-audit source of gap evidence;
5. capability verification inventory as a read-only pattern for capability-state
   projection;
6. capability resolution and recommendation ranking as downstream candidate
   discovery after a need exists.

### 4. Can `CapabilityNeed` originate from the listed sources?

| Source | Current support | Recommended interpretation |
| --- | --- | --- |
| Explicit operator request | Yes, if represented as `request_tool`; strongest current path. | Can create a durable need immediately when the operator has authority. |
| Repeated manual work | Not first-class. | Should create repeated `CapabilitySignal` evidence and can support a durable need. |
| Repeated internal fallback usage | Not first-class. | Strong evidence when recurrence plus inadequacy/limitations are recorded. |
| Failed capability resolution | Only implicit in current response metadata. | Should become evidence for a `CapabilityGap` when repeated or important. |
| Provider handoff | Handoff exists as non-executable metadata/legacy artifact. | Repeated handoff can support a need, but does not verify/adopt a provider. |
| Observed workflow patterns | Observations/facts exist; no need-specific projection. | Should support need acquisition through capability-signal predicates. |
| Reconciliation findings | Documentation practice exists; no canonical event path. | Should be accepted evidence when findings are cited, scoped, and recurrent or authoritative. |

### 5. What evidence should support a `CapabilityNeed`?

A durable need should cite:

- source events, observations, facts, audit documents, handoff records, or manual
  work records;
- normalized capability name and scope;
- examples of requested inputs/outputs;
- recurrence count and distinct workflows affected;
- current workaround or fallback used;
- failure modes, limitations, or missing registered operations;
- candidate provider hints, if any, clearly marked as hints rather than proof;
- source type, confidence, timestamps, freshness/expiry;
- acceptance authority and rationale;
- negative evidence or contradiction notes.

### 6. What distinguishes transient request, task, action plan, and capability need?

A transient request asks for one outcome now. A task is a bounded unit of work.
An action plan is a non-executable proposal for how work could be performed. A
capability need is a durable accepted state that Seed should track and resolve
across time. Recurrence, scope, evidence, and authority distinguish the durable
need from the other three.

### 7. Who owns `CapabilityNeed` creation?

Currently, `ToolNeedService` owns implemented `ToolNeed` creation for
`request_tool`. Architecturally, durable evidence-derived need creation should be
owned by the knowledge/policy layer, likely through a small future
`CapabilityNeedService` or evidence-aware extension to `ToolNeedService`.
Runtime can route explicit requests. `ToolExecutor`, providers, catalog, ranker,
builder, action plans, and handoff plans should not own creation.

### 8. How should `CapabilityNeed` become stale, resolved, superseded, or disproven?

It should be event-sourced and projected, preserving history:

- stale when recurrence stops, evidence expires, scope changes, or resolution
  metadata drifts;
- resolved/satisfied when a registered/adopted/verified operation satisfies the
  need in scope;
- superseded when a broader or replacement need takes over;
- disproven when evidence shows the gap was mistaken or already satisfied;
- rejected when authority declines durable tracking.

### 9. How does `CapabilityNeed` interact with catalog recommendations and provider candidates?

A need comes first. The catalog and ranker help identify and order possible
ways to resolve the need. A `ProviderCandidate` should be created only after the
need and operation semantics are clear enough to evaluate provider conformance.
Recommendations and candidates do not prove the need exists and do not adopt a
provider.

## Conclusion

Seed does **not** already define where `CapabilityNeed` comes from in the full
architectural sense.

Seed currently defines one practical origin: an explicit `request_tool` decision
creates a `ToolNeed`. It also defines the general knowledge pipeline from
observations to evidence, facts, support, and projection. But it does not define
the missing bridge that turns repeated observations, manual work, failed
resolution, fallback usage, handoffs, or reconciliation findings into a durable
capability need.

The smallest missing bridge is:

```text
CapabilitySignal
  -> CapabilityEvidence / FactSupport
  -> CapabilityGap
  -> authority-accepted CapabilityNeed / ToolNeed
```

This bridge should reuse existing observations, evidence, facts, projections,
policy/operator authority, and `ToolNeed` storage. It should not introduce a new
execution engine, autonomous planner, provider owner, or LLM-owned lifecycle.

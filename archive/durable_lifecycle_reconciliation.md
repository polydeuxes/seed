# Durable Lifecycle Reconciliation

## 1. Purpose and scope

This documentation-only audit answers a narrow architecture question:
**does Seed already have an implicit lifecycle model shared across durable state
objects, or are lifecycle concepts duplicated independently across facts, needs,
approvals, plans, verification records, adoption decisions, projections, and
other long-lived concepts?**

The audit inspects existing documentation and implementation vocabulary for
long-lived objects and durable-adjacent projections, especially:

- knowledge objects: `Observation`, `Evidence`, `Fact`, `FactSupport`,
  relationships, aliases, entity-type assertions, unsupported facts, fact
  conflicts, contradictions, graph issues, and stale facts;
- capability and provider objects: `ToolNeed` / `CapabilityNeed`,
  `CapabilityGap`, `ProviderCandidate`, `ProviderVerification`,
  `AdoptionDecision`, `PreferredProvider`, and `FallbackProvider`;
- policy and planning objects: `Approval`, `PendingAction`, `ActionPlan`,
  `HandoffPlan`, execution proposals, and execution authorizations;
- documentation/reconciliation objects: verification inventories, integrity
  inventories, reconciliation findings, `RepositoryArtifactFact`,
  `DocumentationClaim`, and `AlignmentRecord`;
- infrastructure surfaces: projection state and the event ledger.

This document does **not** modify production code, tests, event schemas, runtime
behavior, projections, storage, provider execution, policy behavior, or domain
models. It does **not** introduce a base class, ontology engine, planner,
reasoning engine, or new architectural layer. The goal is to discover recurring
properties that already exist and determine whether a small shared vocabulary
would improve documentation consistency.

## 2. Existing durable concepts found

Seed already has durable and durable-adjacent objects in several families. They
are not one hierarchy; they are independent records, projected read models,
inventories, and documentation artifacts.

| Family | Existing durable or durable-adjacent concepts | Current durability shape |
| --- | --- | --- |
| Event history | `Event` in `EventLedger`; SQLite event records | Append-only event history with actor, timestamp, workspace, payload, causation, and correlation. |
| Projection state | `State`; `ProjectionSnapshot`; `ProjectionStore`; state views | Mutable read model rebuilt from append-only events and optional cached snapshots. |
| Knowledge acquisition | `Observation`, `Evidence`, `Fact` | Observation ingestion appends observation, evidence, and fact events; projection stores current dictionaries of observations, evidence, and facts. |
| Support and confidence | `FactSupport`; evidence graph views; fact-confidence views | Derived projection/view over facts and evidence, not an independently appended object. |
| Knowledge integrity | unsupported facts, `FactConflict`, `Contradiction`, `GraphValidationIssue`, stale facts, refresh recommendations | Derived projection or read-only inventory; preserves ambiguity rather than mutating truth. |
| Graph and identity | `Entity`, catalog relationships, legacy relationships, `EntityAlias`, `EntityTypeAssertion` | Projected from facts, catalogs, and explicit alias/type evidence. |
| Capability need | `ToolNeed`; proposed `CapabilityNeed`; proposed `CapabilityGap` | `ToolNeed` is implemented durable state; broader gap/need vocabulary is documented but not fully modeled as first-class records. |
| Capability verification | `capability_verified` facts; `CapabilityInventoryEntry`; `CapabilitySupportSummary`; `CapabilityEvidenceSummary` | Verification inventory is read-only and derives verified/unverified/stale/provider-reported/unknown state from projected facts and support. |
| Provider adoption | `ProviderCandidate`, `ProviderVerification`, `AdoptionDecision`, `PreferredProvider`, `FallbackProvider`, provider drift/deprecation | Primarily documentation vocabulary today; not an implemented first-class provider-selection projection. |
| Policy and approval | `Approval`; `PolicyDecision`; `PendingAction` | Approvals and pending actions project from events; policy decisions are per-evaluation outputs. |
| Plans and handoffs | `ActionPlan`, `HandoffPlan`, execution proposals, execution authorizations | Legacy/experimental side-path records; projected for compatibility and explicit tests; intentionally non-executable or short-lived metadata. |
| Registered capability surface | `ToolSpec`, `Toolkit`, `ToolkitCandidate`, capability catalogs, recommendation ranking | Registered operations and generated candidates are durable metadata/candidates, not adoption authority. |
| Documentation reconciliation | `DocumentationClaim`, `RepositoryArtifactFact`, `AlignmentRecord`, reconciliation findings | Fixture/documentation-level durable conclusions; not projected runtime state in v0. |
| Integrity inventories | Projection Integrity Summary and drill-down views | Read-only aggregate views over existing unsupported, conflict, contradiction, graph, stale, refresh, and capability-verification signals. |

## 3. What Seed already supports

Seed already supports many lifecycle properties, but it supports them by family,
not through a universal lifecycle type.

### 3.1 Support and evidence

Knowledge is the strongest example. The canonical acquisition path is:

```text
Observation -> Evidence -> Fact
```

`Observation` carries source type, time, subject, predicate, value, confidence,
metadata, dimensions, and optional expiry. The ingestor converts it to
`Evidence` and then a `Fact`, preserving evidence IDs and source metadata.
`FactSupport` groups projected facts by subject, predicate, value, and dimensions
and records supporting fact IDs, source types, confidence, first/latest
observation time, expiry, predicate semantics, and support kind.

Support also appears outside ordinary facts:

- capability verification inventory exposes supporting facts, supporting
  evidence, support confidence, age, and expiry for `capability_verified` facts;
- contradiction views attach evidence by fact ID and supporting event IDs;
- graph issues preserve source fact IDs and relationship IDs;
- alignment records preserve documentation claims, artifact facts, rule IDs,
  outcomes, and reasons;
- reconciliation documents preserve prose support, non-goals, rejected options,
  and direct answers.

Support is therefore broadly recurring, but its concrete shape is
family-specific.

### 3.2 Authority

Seed has several authority-like concepts, but no universal `authority` field:

- facts derive authority from source type, evidence, confidence, observed time,
  catalog semantics, and support selection;
- policy decisions derive authority from policy rules, risk class, and matching
  approval grants;
- approvals record an approver, action, scope, expiry, and constraints;
- action-plan approval records that an accepted plan was approved, while
  explicitly not granting execution authorization;
- execution authorizations are short-lived, secret-free metadata tied to one
  concrete proposal;
- provider adoption docs explicitly say verification is necessary but
  insufficient, and that adoption needs operator or policy authority;
- documentation/reconciliation conclusions derive authority from audit scope,
  inspected sources, explicit boundaries, and rejected alternatives.

Authority is important, but it is not universal in the same form. A fact's
source authority, a policy approval, and a provider adoption authority have
similar explanatory value but different semantics.

### 3.3 Status

Status is common but vocabulary is duplicated by family:

- `ToolNeed.status`: `proposed`, `accepted`, `generating`, `generated`,
  `validating`, `validated`, `registered`, `rejected`;
- `PendingAction.status`: `pending`, `approved`, `completed`, `cancelled`;
- `ActionPlan.status`: `proposed`, `accepted`, `rejected`, `superseded`;
- `ToolSpec.status` and `Toolkit.status`: currently registered-state metadata;
- capability inventory state: `verified`, `unverified`, `stale`,
  `provider_reported`, `unknown`;
- alignment outcomes: `supported`, `missing_support`, `potential_conflict`,
  `not_evaluable`;
- adoption vocabulary: adopt/reject/needs-more-evidence, preferred/fallback,
  drift, deprecation, revocation, and supersession concepts in documentation.

There is no shared `LifecycleStatus` enum, and one should not be introduced just
to make these labels uniform. The families have different state machines.

### 3.4 Projection

Projection is a first-class architectural pattern. Events are append-only;
`StateProjector` rebuilds inspectable state by replaying ledger events,
deriving aliases, inferred facts, support groups, relationships, entity-type
assertions, graph issues, and fact conflicts. `ProjectionStore` snapshots are
mutable caches keyed by workspace, projection name, and version.

Many lifecycle concepts are therefore **not** appended records. They are derived
from facts and events:

- current facts and best facts;
- `FactSupport`;
- `FactConflict`;
- stale facts and refresh recommendations;
- relationships and aliases;
- graph issues;
- contradictions;
- capability inventory entries;
- projection-integrity summaries.

This is one of Seed's clearest shared durable-state patterns: append durable
source events, derive mutable current state and read-only inventories.

## 4. What Seed does not yet model

Seed does **not** yet model a single coherent durable lifecycle taxonomy across
all long-lived concepts.

Missing or partial areas:

1. **No universal lifecycle record.** There is no common durable object with
   standard fields for support, authority, status, projection, staleness,
   contradiction, supersession, resolution, scope, provenance, freshness, and
   validity.
2. **No first-class provider adoption projection.** `AdoptionDecision`,
   `PreferredProvider`, `FallbackProvider`, provider drift, provider
   deprecation, and provider revocation are documented vocabulary, not an
   implemented state family.
3. **No explicit fact-level supersession.** Facts can expire, lose current
   influence, conflict, or be outranked by support selection, but they do not
   carry a superseded-by link or superseded status.
4. **No contradiction resolution object.** Contradictions and fact conflicts are
   preserved as read-only integrity signals; Seed does not append a resolution
   verdict that chooses truth and mutates the conflicting facts.
5. **No unified authority taxonomy.** Authority exists as source type,
   confidence, approval, policy, operator adoption authority, and documentation
   audit method, but these are not normalized under one schema.
6. **No universal staleness model.** Fact expiry and capability verification
   staleness are explicit. Provider drift/deprecation and adoption expiry are
   documented but not implemented. Pending actions and execution authorizations
   have status/expiry semantics, but not the same staleness meaning.
7. **No universal support model.** Facts have evidence IDs and support groups;
   approvals do not have evidence links; pending actions have causation and
   arguments; documentation claims have source paths; alignment records have
   artifact facts.

These gaps are not necessarily defects. They mostly show that Seed has family
specific lifecycles rather than a single architecture-wide lifecycle object.

## 5. Shared lifecycle properties

The audit evaluated candidate properties without assuming universality.

| Property | Shared today? | Explanation |
| --- | --- | --- |
| Provenance | Nearly universal | Events have actor/timestamp/causation/correlation; observations/evidence/facts have source/time; plans and pending actions carry originating IDs; documentation claims carry source paths. This is the strongest shared property. |
| Scope | Broad but uneven | Workspaces are common; facts also have subject/predicate/dimensions; approvals have action/scope; provider adoption docs require operation/provider/scope; documentation claims have source path/heading. |
| Projection | Broad architectural pattern | Durable events project into mutable state and read-only inventories. Some documentation and fixture records are intentionally outside runtime projection. |
| Status / outcome | Broad but family-specific | Many durable concepts have status/outcome, but each family owns its own vocabulary and transitions. |
| Support | Broad for conclusions, not universal | Facts, capability verification, contradictions, graph issues, alignment records, and reconciliation docs preserve support. Approvals and pending actions are authority/workflow records rather than evidence-backed claims. |
| Authority | Broad for decisions, not universal | Approvals, policy decisions, adoption decisions, and reconciliation findings need authority. Ordinary evidence and observations are provenance sources, not authority decisions by themselves. |
| Freshness / staleness | Common in knowledge and verification | Fact expiry, stale facts, refresh recommendations, capability stale state, provider drift/deprecation docs, and execution authorization expiry recur, but semantics differ. |
| Contradiction | Knowledge/integrity-specific | Facts, fact support, contradictions, graph issues, and alignment records can expose conflict. Pending actions and approvals do not become contradicted in the same sense. |
| Supersession | Planning/provider-doc-specific today | Implemented for `ActionPlan`; documented for provider deprecation/supersession; not implemented for facts, support, approvals, or contradictions. |
| Resolution | Workflow/integrity-specific | Pending actions complete/cancel; action plans accept/reject/supersede; gaps may resolve into needs/providers; contradictions do not currently resolve automatically. |
| Validity | Broad but overloaded | Can mean schema validity, policy validity, non-expired approval, non-expired fact, valid provider verification, or documentation alignment. It should not become one universal boolean. |

The smallest truly shared vocabulary is therefore not a complete lifecycle model.
It is a set of recurring documentation labels: **provenance, scope, support,
authority, status/outcome, projection, freshness/staleness, contradiction,
supersession, and resolution**.

## 6. Family-specific lifecycle properties

### 6.1 Knowledge family

Applies strongly:

- support/evidence;
- provenance;
- scope via subject/predicate/dimensions/workspace;
- confidence;
- projection;
- current/best selection;
- staleness through `expires_at`;
- contradiction/conflict;
- graph validity;
- unsupported-state visibility.

Applies weakly or not today:

- authority as an explicit authority object;
- supersession;
- explicit resolution records.

### 6.2 Capability need and gap family

Applies strongly:

- status;
- scope via workspace, capability, desired inputs/outputs, reason, and risk hint;
- projection into `State.tool_needs`;
- resolution through status transitions such as registered or rejected.

Applies partially:

- support/evidence, because current `ToolNeed` creation is request-driven, while
  proposed `CapabilityNeed` / `CapabilityGap` vocabulary expects evidence-backed
  deficiency analysis;
- authority, because accepting a need and deciding it is durable should be
  separated from raw signal in the documented lifecycle.

Applies weakly or not today:

- contradiction, staleness, and supersession as first-class properties of
  `ToolNeed` itself.

### 6.3 Provider verification and adoption family

Applies strongly in documentation and partially in implementation:

- support/evidence through verification facts and capability inventory;
- freshness/staleness through expired `capability_verified` facts;
- scope through capability, operation contract, provider fingerprint,
  implementation, workspace, and risk;
- authority for adoption through operator or policy approval;
- projection for preferred/fallback provider state as proposed future surface.

Applies partially or not yet:

- `ProviderVerification` as a separate durable record;
- `AdoptionDecision` as a first-class event/model;
- provider drift/deprecation/revocation as implemented projections;
- contradiction between provider-verification results as a named provider-specific
  contradiction type.

### 6.4 Policy, approval, pending action, and execution authorization family

Applies strongly:

- authority;
- scope;
- status/outcome;
- expiry for approvals/execution authorizations;
- projection from append-only events;
- resolution through approved/completed/cancelled or allow/block/require states.

Applies weakly:

- support/evidence in the knowledge sense;
- contradiction as an integrity view;
- supersession, except indirectly when a pending action is cancelled or a plan is
  superseded.

### 6.5 Planning and handoff family

Applies strongly:

- status;
- authority boundaries;
- scope through tool need, provider, capability, risk, operation, target, and
  policy summary;
- projection;
- supersession for action plans;
- resolution through acceptance, rejection, approval event, or supersession.

Applies weakly:

- evidence/support;
- staleness;
- contradiction.

### 6.6 Documentation and reconciliation family

Applies strongly:

- support through cited sources, artifact facts, rule IDs, reasons, and audit
  method;
- status/outcome through supported/missing-support/potential-conflict/
  not-evaluable and through reconciliation direct answers;
- contradiction/potential conflict;
- scope through source path, heading, claim family, and audit boundary;
- non-goals and rejected solutions.

Applies weakly or not in runtime terms:

- projection into `State`;
- event-ledger append semantics;
- automatic staleness and refresh;
- executable resolution.

## 7. Projection relationships

The core projection pattern is:

```text
append-only event ledger
  -> StateProjector replay
  -> mutable State read model
  -> derived read-only views / inventories
```

Current projected state includes observations, evidence, facts, goals,
`ToolNeed`s, approvals, pending actions, action plans, handoff plans, tools,
execution proposals, and execution authorizations.

Derived projection/inventory state includes:

- aliases and canonical identity resolution;
- legacy and catalog-defined relationships;
- entity-type assertions;
- graph validation issues;
- inferred facts;
- fact support groups;
- fact conflicts;
- stale facts and refresh recommendations;
- contradictions;
- capability verification inventory;
- projection integrity summary.

Append-only versus mutable projection distinction:

| Object or surface | Append-only source? | Mutable projection/read model? |
| --- | --- | --- |
| `Event` | Yes | No; event history is replay input. |
| `Observation`, `Evidence`, `Fact` | Yes, as event payloads | Yes, projected dictionaries and filtered/current views. |
| `FactSupport`, `FactConflict`, stale fact view | No separate append | Yes, derived from projected facts. |
| `Contradiction` | No separate append | Yes, read-only view over projected facts/evidence graph. |
| Relationships, aliases, entity types, graph issues | No separate append | Yes, derived from facts and catalogs. |
| `ToolNeed` | Yes | Yes, projected and status-updated. |
| `Approval` | Yes | Yes, projected and filtered by scope/expiry. |
| `PendingAction` | Yes | Yes, projected and status-updated. |
| `ActionPlan` | Yes | Yes, projected and status-updated. |
| `HandoffPlan` | Yes | Yes, projected. |
| `ToolSpec` | Yes when registered | Yes, projected registry surface. |
| Capability inventory | No separate append | Yes, read-only inventory derived from tools, needs, and verification facts. |
| Provider adoption vocabulary | Intended append-only source in docs | Preferred/fallback projection is proposed, not implemented. |
| `RepositoryArtifactFact`, `DocumentationClaim`, `AlignmentRecord` | Fixture/documentation records, not runtime ledger | Not projected in runtime v0. |
| Projection snapshots | No; cache rows are overwritten | Yes, mutable cache of projected state. |

## 8. Staleness / contradiction / supersession analysis

### Staleness

Staleness is strongest in facts. `Observation` and `Fact` can carry
`expires_at`; expired facts are excluded from normal supports and conflicts by
default; stale facts are listed and mapped to deterministic refresh capability
recommendations. Capability verification reuses this model: an expired
`capability_verified` fact produces a stale capability-inventory entry.

Staleness is also present as expiry in approvals and execution authorizations,
but that means authorization validity, not knowledge freshness. Provider
adoption docs discuss drift, deprecation, verification expiry, and fallback, but
these are not implemented as a provider-selection state machine.

Conclusion: **freshness/staleness is shared vocabulary, but not one shared
mechanism.**

### Contradiction

Contradiction is knowledge/integrity-specific. `FactConflict` detects competing
supported values for a subject/predicate/dimensions. `Contradiction` detects
incompatible values for exclusive predicates and attaches evidence views and
supporting event IDs. Graph validation issues surface suspicious or invalid
relationship edges. Alignment records can produce `potential_conflict` when an
artifact fact contradicts a rejected-concept claim.

Pending actions, approvals, and action plans can be rejected, cancelled, or
superseded, but they are not contradicted in the fact-integrity sense.

Conclusion: **contradiction is not universal; it belongs to claim/integrity
families.**

### Supersession

Supersession is implemented explicitly for `ActionPlan` through
`action_plan.superseded` events and `replacement_plan_id`. Provider adoption docs
also describe provider deprecation, drift, fallback, and supersession by better
verified providers. Facts do not have fact-level supersession. A newer or better
supported fact may become current, an old fact may expire, and a conflict may be
reported, but the old fact is not marked superseded.

Conclusion: **supersession is family-specific today. It should not be forced
onto facts unless a future knowledge-maintenance design actually needs it.**

### Resolution

Resolution appears in workflow objects: pending actions become approved,
completed, or cancelled; action plans become accepted, rejected, or superseded;
`ToolNeed`s can move toward registered or rejected; capability gaps are intended
to resolve through capability needs and provider decisions. Integrity views do
not resolve themselves: unsupported facts, contradictions, graph issues, stale
facts, and capability inventory entries remain report-only until new evidence,
events, or documentation changes alter the projection.

Conclusion: **resolution is shared as a documentation concept, but the resolver
is family-specific.**

## 9. `cloc` worked examples

### 9.1 LOC fact

A LOC count should enter Seed as ordinary knowledge:

```text
Observation(source_type=provider, subject=repository, predicate=loc_count,
value={language totals}, observed_at=t, expires_at=t+ttl)
  -> Evidence(source=observation:provider, kind=observation, payload=...)
  -> Fact(subject_id=repository, predicate=loc_count, value=..., evidence_ids=[...])
  -> FactSupport(... support_kind=aggregate or current_sample depending predicate semantics)
```

Lifecycle properties:

- support: yes, through evidence IDs and `FactSupport`;
- authority: source/provenance and confidence, not adoption authority;
- status: current/best/stale/conflicted is derived, not a fact status field;
- projection: yes;
- staleness: yes if an expiry is attached;
- contradiction: yes if another current durable LOC fact asserts a competing
  value under compatible scope;
- supersession: no explicit fact-level supersession;
- resolution: new evidence can change support or expiry behavior, but there is
  no contradiction-resolution event today.

### 9.2 CapabilityNeed for LOC counting

If Seed repeatedly needs reliable repository LOC counts, the documented
capability lifecycle says raw signals should become evidence, then a
`CapabilityGap`, then a durable `CapabilityNeed`. Current implementation's
closest durable model is `ToolNeed`:

```text
ToolNeed(name="Count repository LOC", capability="count_loc", reason=...,
status="proposed")
```

Lifecycle properties:

- support: partial today; request reason exists, but evidence-backed gap support
  is not fully modeled;
- authority: partial; status acceptance can express workflow authority, but not a
  full capability-need authority model;
- status: yes, through `ToolNeed.status`;
- projection: yes, into `State.tool_needs`;
- staleness: not first-class;
- contradiction: not first-class;
- supersession: not first-class;
- resolution: yes, eventually registered or rejected in the existing status
  vocabulary.

### 9.3 ProviderVerification for `cloc`

A `cloc` verification should not be a hidden trust decision. The current
implemented approximation is an evidence-backed fact:

```text
Fact(subject_id="count_loc", predicate="capability_verified",
value="verified", dimensions={provider:"cloc", contract:"sha256:..."},
evidence_ids=[...], observed_at=t, expires_at=t+ttl)
```

Capability inventory can expose:

```text
CapabilityInventoryEntry(
  capability="count_loc",
  state="verified",
  supporting_facts=[...],
  supporting_evidence=[...],
  support={confidence, observed_at, latest_observed_at, expired, expires_at},
  age_seconds=...
)
```

Lifecycle properties:

- support: yes;
- authority: verification evidence supports conformance, but does not authorize
  adoption;
- status: verified/unverified/stale/provider-reported/unknown in inventory;
- projection: yes, through facts and read-only inventory;
- staleness: yes, through fact expiry;
- contradiction: possible as competing verification facts, but no provider-
  specific contradiction model;
- supersession: not implemented;
- resolution: re-verify or provide new evidence; no verifier daemon or automatic
  adoption.

### 9.4 AdoptionDecision for `cloc`

The documented but not yet implemented lifecycle is:

```text
ProviderVerification passed
  -> AdoptionAuthority evaluates evidence + policy + scope
  -> AdoptionDecision is appended
  -> PreferredProvider / FallbackProvider is projected
```

For `cloc`, a future adoption decision would say that `cloc` is preferred for
`count_loc` under a specific operation contract, provider fingerprint, version
range, workspace, and policy scope, while an internal naive counter remains
fallback.

Lifecycle properties:

- support: should cite provider verification evidence;
- authority: yes, operator or policy authority is essential;
- status/outcome: adopt preferred, adopt fallback, reject, needs more evidence,
  revoke, deprecate, or supersede in documented vocabulary;
- projection: intended, not implemented;
- staleness: intended through verification expiry/drift;
- contradiction: possible if adoption evidence conflicts, but not modeled today;
- supersession: intended for better providers or policy changes;
- resolution: intended through adoption/revocation/deprecation events, not
  currently implemented.

### 9.5 Expired verification

If the `cloc` verification fact expires, Seed already has the minimal pattern:

```text
expired capability_verified fact
  -> stale FactSupport / no active support
  -> CapabilityInventoryEntry(state="stale")
  -> refresh recommendation if represented as a stale fact
```

This is not a provider removal. It is an inventory signal that the verification
is no longer fresh. A future provider-selection projection could fall back to the
internal counter when preferred-provider verification is stale.

### 9.6 Contradictory LOC results

If two non-expired durable LOC facts assert incompatible scoped values, Seed
should preserve both facts and expose conflict rather than choosing truth:

```text
Fact(repo, loc_count, 10_000, evidence=cloc)
Fact(repo, loc_count, 12_000, evidence=internal_counter)
  -> FactSupport(value=10_000)
  -> FactSupport(value=12_000)
  -> FactConflict / Contradiction if predicate semantics mark the scope exclusive
```

The lifecycle properties here are support, projection, contradiction, and
freshness. They are **not** adoption authority. The conflict may reveal that the
`cloc` adapter, internal counter, ignore rules, generated-code filtering, or
contract scope differs, but the fact conflict itself should not adopt or reject a
provider.

## 10. Non-goals

This reconciliation deliberately does not:

- introduce a lifecycle base class;
- introduce a universal `DurableObject` model;
- add a lifecycle ontology;
- add an adoption engine, verifier daemon, repair loop, planner, scheduler, or
  reasoning engine;
- alter event schemas, projection behavior, storage, runtime routing, provider
  execution, policy behavior, tests, or domain models;
- force `Fact`, `ToolNeed`, `Approval`, `PendingAction`, `ActionPlan`,
  `ProviderVerification`, `AdoptionDecision`, and `AlignmentRecord` into one
  inheritance hierarchy;
- make all status values share one enum;
- treat verification as adoption;
- treat adoption as execution authorization;
- treat contradictions as automatic truth-resolution requests;
- treat stale as false.

## 11. Rejected solutions

| Rejected solution | Why rejected |
| --- | --- |
| Universal lifecycle base class | Would impose a false common model on objects whose lifecycle semantics differ materially. |
| Global `LifecycleStatus` enum | Would blur domain-specific states such as pending/completed, verified/stale, supported/potential-conflict, and preferred/fallback. |
| Ontology or reasoning engine | The audit finds documentation vocabulary drift, not a need for a new inference subsystem. |
| Automatic contradiction resolver | Seed currently preserves conflicting evidence and reports integrity signals; automatic truth arbitration would violate existing boundaries. |
| Provider adoption through verification alone | Prior reconciliation explicitly separates verification evidence from adoption authority. |
| Provider adoption through runtime or `ToolExecutor` | Runtime/executor may consume projected provider selection later, but should not own durable trust/preference decisions. |
| Treat projection snapshots as source of truth | Snapshots are mutable caches; append-only events and source records remain the replayable substrate. |
| Make documentation reconciliation runtime state | Repository/documentation alignment v0 is fixture/documentation-level and intentionally not projected runtime state. |

## 12. Direct answer

Seed does **not** already have a coherent, explicit durable lifecycle model that
applies uniformly to all durable objects.

Seed **does** have an implicit architectural pattern:

```text
Provenance-bearing source record or event
  -> optional evidence/support
  -> family-specific durable conclusion or workflow record
  -> append-only event history when runtime-owned
  -> mutable projection / read-only inventory
  -> family-specific integrity, freshness, authority, status, and resolution views
```

Lifecycle concepts are currently duplicated independently across families:

- facts model evidence, support, confidence, freshness, current selection,
  conflicts, and projection;
- capability needs model request/gap status and projection, with only partial
  evidence-backed support today;
- capability verification reuses fact support and expiry but exposes a separate
  inventory status vocabulary;
- provider adoption has strong documented authority/freshness/supersession needs
  but is not yet first-class runtime state;
- approvals and pending actions model authority, scope, expiry, and workflow
  status rather than evidence-backed truth;
- action plans model status, approval boundary, and supersession;
- documentation reconciliation models support, potential conflict, outcome, and
  direct conclusions outside runtime projection;
- projection state and event ledger provide the shared append-only versus mutable
  read-model pattern.

The smallest shared lifecycle vocabulary that explains recurring patterns across
Seed durable concepts without creating a new architectural layer is:

```text
Provenance
Scope
Support
Authority
Status / Outcome
Projection
Freshness / Staleness
Contradiction / Conflict
Supersession
Resolution
Validity
```

These terms should be used as documentation headings or checklist vocabulary, not
as a mandatory schema. The most universal terms are **provenance**, **scope**,
**projection**, and family-specific **status/outcome**. **Support** and
**authority** recur often but mean different things in claim families versus
workflow families. **Staleness**, **contradiction**, **supersession**, and
**resolution** are important but family-specific. Seed would benefit from this
small shared vocabulary for documentation consistency, while preserving separate
models and state machines for facts, needs, approvals, plans, verification,
adoption, integrity inventories, and reconciliation records.

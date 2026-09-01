> **Historical/stale after PR 1918.** This document is preserved as historical testimony only. Its Runtime, RuntimeLoop, Decision, Policy, Execution, ActionPlan, HandoffPlan, ExecutionProposal, ExecutionAuthorization, PendingAction, request_tool, call_tool, and builder-candidate language is not current architecture or operator instruction.

# Conclusion taxonomy reconciliation

## 1. Purpose and scope

This documentation-only reconciliation audits whether Seed already has a
coherent architectural concept for durable conclusions: durable outcomes that
Seed derives, records, projects, or preserves after interpreting signals and
evidence.

The audit focuses on the recurring pattern:

```text
Signal -> Evidence -> Conclusion
```

and compares it with Seed's existing knowledge, capability, verification,
selection, approval, planning, alignment, and reconciliation vocabulary.

This document does **not** introduce production code, event schemas, runtime
behavior, projections, storage changes, provider behavior, policy behavior, or a
new reasoning subsystem. It also does not collapse existing concepts into one
runtime object. Its purpose is only to name what Seed already does and identify
the smallest vocabulary gap.

## 2. Existing conclusion-like concepts found

Seed already contains many durable or durable-adjacent outcomes that behave like
conclusions even when they do not share the word `Conclusion`.

| Concept | First-class today? | Conclusion-like role | Notes |
| --- | --- | --- | --- |
| `Fact` | Yes | Evidence-backed state claim. | The clearest first-class durable conclusion in the knowledge layer. |
| `FactSupport` | Yes, projection | Projected support aggregate for a claim. | Support is not a conclusion by itself, but it determines whether a fact is well-supported, weakly supported, current, or stale. |
| `FactConflict` / contradiction | Yes, projection/view | Projected disagreement between competing claims. | A contradiction is an integrity conclusion about incompatible current claims, not a domain truth verdict. |
| Unsupported fact | Yes, view/inventory vocabulary | Integrity conclusion that a projected/current claim lacks visible support. | Usually derived from evidence graph or projection integrity, not a separate asserted object. |
| Stale fact | Yes, projection/view vocabulary | Integrity conclusion that a fact's freshness window expired. | Derived from `expires_at` and timestamps rather than a separate durable stale assertion. |
| Current/best fact | Yes, projection/view vocabulary | Selection conclusion among supported competing values. | Derived from aggregate support, source type, confidence, and recency. |
| `Projection` | Yes | Read model of current conclusions and integrity signals. | Projection owns current visibility, not original authority. |
| `ToolNeed` | Yes | Durable request/gap conclusion created from a model decision. | Current implementation is request-driven; proposed `CapabilityNeed` vocabulary would generalize this into evidence-derived capability need. |
| `CapabilityNeed` | Proposed vocabulary | Durable conclusion that a capability is needed. | Not a distinct first-class runtime model today; closest current model is `ToolNeed`. |
| `CapabilityGap` | Proposed vocabulary | Conclusion that current capability supply is insufficient for a need. | Currently implicit in `ToolNeed`, capability resolution, and recommendation output. |
| `ProviderCandidate` | Partly first-class as recommendation/candidate metadata | Candidate conclusion that a provider may satisfy a need. | Currently produced by catalogs, registry lookups, recommendation ranker, or builder candidates; not one unified durable model. |
| `ProviderVerification` / verification result | Partly first-class as facts and inventory | Scoped conclusion about provider/capability availability or verification status. | Capability Verification Inventory v1 intentionally models this through `Fact`, `FactSupport`, predicates, timestamps, and read-only inventory. |
| `AdoptionDecision` | Proposed vocabulary | Durable authority-backed conclusion that a verified provider is adopted, rejected, preferred, fallback, revoked, stale, or superseded. | Documented as needed vocabulary; not implemented as a first-class event/model in current code. |
| `PreferredProvider` / `FallbackProvider` | Proposed projection vocabulary | Projected provider-selection conclusion. | Should be projected from adoption decisions, not inferred from recommendation or verification alone. |
| Verification inventories | Yes, read-only inventory | Derived current verification conclusions. | Inventory entries expose evidence/support/age; they should not execute verification or mutate state. |
| Integrity inventories | Yes, read-only inventory | Derived current integrity conclusions. | Examples include unsupported, stale, contradiction, graph issue, projection-health, and refresh signals. |
| Contradiction inventories | Yes, read-only inventory/view | Derived conclusions that multiple values compete. | They preserve conflict visibility instead of auto-resolving truth. |
| Reconciliation documents | Yes, documentation artifacts | Architectural conclusion records. | Durable documentation conclusions with prose support, non-goals, rejected options, and direct answers. |
| Selection rationale | Yes, view/vocabulary | Explanation conclusion about why something was selected, excluded, stale, contradicted, or unsupported. | Rationale is explanatory projection over evidence/support/selection, not independent authority. |
| `RecommendationRanker` output | Yes, runtime service output | Ephemeral ranking conclusion. | Ranking is useful selection rationale but not durable adoption or trust authority. |
| `CapabilityCatalog` recommendations | Yes, catalog metadata | Static candidate suggestions. | Catalog entries are metadata and suggestions, not verification, adoption, or trust conclusions. |
| `PolicyDecision` / policy outcome | Yes | Per-action policy conclusion. | Durable if recorded in event payloads or pending-action flow; otherwise a runtime decision result. |
| `Approval` | Yes | Authority grant conclusion. | Records that an approver granted an action/scope under constraints and optional expiry. |
| `PendingAction` | Yes | Lifecycle conclusion that an action is waiting, approved, completed, or cancelled. | It is about execution gating state, not evidence truth. |
| `ActionPlan` | Yes, legacy/quarantined | Planning conclusion/proposal with lifecycle status. | Non-executable and outside Core MVP runtime routing. |
| `HandoffPlan` | Yes, legacy/quarantined | Boundary conclusion describing external provider handoff. | Non-executable; does not imply approval, trust, credentials, registration, or execution authorization. |
| Alignment records | Yes/proposed through self-model alignment | Reconciliation conclusion about support between documentation claims and repository artifact facts. | Outcomes such as supported, partially supported, missing support, potential conflict, not evaluable, and requires human review are alignment, not truth, conclusions. |
| `RepositoryArtifactFact` | Yes in self-model acquisition vocabulary | Artifact-backed fact about repository structure. | A fact subtype/domain, not a separate lifecycle family. |
| `DocumentationClaim` | Yes in documentation observation vocabulary | Claim extracted from documentation. | A source claim that can be reconciled against artifact facts; may become alignment knowledge. |
| Existence claims | Yes in reconciliation vocabulary | Narrow conclusion about whether an artifact existence claim has supplied support. | Outcomes include supported, missing support, potential conflict, and not evaluable. |
| Structure reconciliation | Yes in reconciliation vocabulary | Conclusion about repository/documentation structural support. | Must not be upgraded into ownership truth without additional evidence. |
| Self-model acquisition artifacts | Yes/proposed vocabulary | Evidence-backed self-description outcomes. | Claims, artifact facts, support relationships, and alignment knowledge apply the same knowledge pattern to Seed itself. |

## 3. What Seed already supports

Seed already supports several lifecycle properties that conclusion-like objects
share:

1. **Source separation.** Raw or external inputs can be represented as
   observations; provenance payloads can be represented as evidence; interpreted
   claims can be represented as facts.
2. **Append-only durability.** Facts, evidence, tool needs, approvals, pending
   actions, action plans, handoff plans, and many lifecycle changes are recorded
   through ledger events or durable documentation artifacts.
3. **Projection.** Current state is derived by projection rather than by treating
   the last event as the only source of truth.
4. **Support aggregation.** `FactSupport` aggregates facts with the same subject,
   predicate, value, and dimensions, distinguishing durable aggregate claims from
   volatile measurement samples.
5. **Contradiction visibility.** Competing values can remain visible as conflicts
   rather than being collapsed into automatic truth.
6. **Staleness.** Expiry and timestamps support stale-fact detection and refresh
   recommendations.
7. **Authority boundaries.** Approvals, policy outcomes, adoption authority
   documents, and handoff boundaries distinguish evidence, permission,
   selection, and execution.
8. **Quarantine / supersession.** Legacy planning and handoff artifacts can be
   preserved while reducing current authority; action plans have explicit
   accepted, rejected, and superseded lifecycle states.
9. **Read-only inventories.** Capability verification, integrity, contradiction,
   and selection-rationale surfaces can interpret projected state without
   appending new events or executing tools.
10. **Reconciliation as durable documentation.** Reconciliation documents already
    record architectural findings, direct answers, rejected solutions, non-goals,
    and stale/quarantine status.

## 4. What Seed does not yet model

Seed does **not** yet model one explicit, coherent conclusion taxonomy across
all durable outcome families.

The missing piece is not a generic conclusion engine. It is a small vocabulary
that says:

```text
A conclusion is a durable interpreted outcome derived from one or more signals
and support records, owned by a specific authority boundary, projected into a
current status, and subject to domain-specific staleness, contradiction,
supersession, and resolution rules.
```

Seed also does not yet have common names for cross-cutting properties such as:

- conclusion type;
- conclusion support;
- conclusion authority;
- conclusion status;
- conclusion projection;
- conclusion staleness;
- conclusion contradiction;
- conclusion supersession;
- conclusion resolution.

Those names are useful as documentation vocabulary. They should not imply one
shared persisted object or one generic reasoning framework.

## 5. Durable conclusion taxonomy

The smallest taxonomy that fits current Seed is:

### 5.1 Knowledge conclusions

Knowledge conclusions answer:

```text
What does Seed currently believe, with what support and conflicts?
```

Members:

- `Fact`;
- current/best fact;
- inferred fact;
- repository artifact fact;
- documentation claim when promoted into a supported claim context;
- existence or structure claim outcome;
- alignment knowledge.

Primary lifecycle:

```text
Observation / documentation / repository artifact / provider output
  -> Evidence
  -> Fact or Claim
  -> FactSupport / SupportRelationship
  -> current projection / alignment outcome
```

### 5.2 Integrity conclusions

Integrity conclusions answer:

```text
Is this knowledge supportable, current, consistent, and selectable?
```

Members:

- unsupported fact;
- stale fact;
- contradiction / fact conflict;
- projection integrity issue;
- graph issue;
- verification inventory status when treated as integrity over capability facts;
- selection-rationale exclusion reasons.

Primary lifecycle:

```text
Projected knowledge + support + predicate semantics + time
  -> integrity inventory / rationale / refresh recommendation
```

### 5.3 Capability-need conclusions

Capability-need conclusions answer:

```text
What capability is missing or needed, and why?
```

Members:

- current first-class `ToolNeed`;
- proposed vocabulary `CapabilityNeed`;
- proposed `CapabilityGap`;
- gap classification and resolution path where documented.

Primary lifecycle today:

```text
Model decision: request_tool
  -> ToolNeed
  -> capability resolution metadata
```

Primary lifecycle proposed by reconciliations:

```text
CapabilitySignal
  -> CapabilityEvidence / FactSupport
  -> CapabilityGap
  -> CapabilityNeed
  -> ProviderCandidate
```

The proposed lifecycle is not implemented as a new acquisition subsystem today.

### 5.4 Provider-selection conclusions

Provider-selection conclusions answer:

```text
Which provider can or should satisfy a capability need under a scope?
```

Members:

- provider recommendation;
- registered operation candidate;
- handoff candidate;
- provider candidate;
- provider verification result;
- adoption decision;
- preferred provider;
- fallback provider;
- selection rationale.

Primary lifecycle:

```text
CapabilityNeed / ToolNeed
  -> catalog, registry, recommendation, builder, or observed availability signals
  -> ProviderCandidate
  -> ProviderVerification / verification facts / inventory
  -> AdoptionDecision by adoption authority
  -> PreferredProvider / FallbackProvider projection
```

Today, Seed has candidate and recommendation metadata, verification vocabulary,
and inventories. It does not yet have first-class durable adoption-decision
records or projected preferred/fallback provider state.

### 5.5 Authority and permission conclusions

Authority conclusions answer:

```text
Is this action, provider adoption, or execution boundary allowed under policy or
human authority?
```

Members:

- `PolicyDecision` / policy outcome;
- `Approval`;
- pending-action approval state;
- proposed adoption authority / adoption decision;
- execution authorization metadata in legacy side paths.

Primary lifecycle:

```text
Proposed action or adoption
  -> policy evaluation and/or human approval
  -> grant, block, require confirmation, require approval, revoke, expire, or
     remain pending
```

These are conclusions, but they are permission conclusions rather than knowledge
truth conclusions.

### 5.6 Planning and handoff conclusions

Planning conclusions answer:

```text
What non-executable plan or external handoff boundary has Seed proposed or
accepted?
```

Members:

- `ActionPlan`;
- `HandoffPlan`;
- pending actions;
- execution proposals / authorizations in legacy side paths.

Primary lifecycle:

```text
ToolNeed / model decision
  -> ActionPlan proposal
  -> accepted / rejected / superseded
  -> optional non-executable HandoffPlan boundary
```

These must remain distinct from approvals, provider trust, credentials, tool
registration, and execution lifecycle.

### 5.7 Documentation and architecture conclusions

Documentation conclusions answer:

```text
What architectural position has Seed recorded after reconciliation?
```

Members:

- reconciliation documents;
- architecture audits;
- rejected solutions;
- non-goals;
- roadmap/frontier status;
- stale/quarantine notices;
- direct answers.

Primary lifecycle:

```text
Documentation claims + repository facts + prior reconciliations
  -> audit/reconciliation
  -> recorded architectural conclusion
  -> superseded, refined, or quarantined by later documents
```

These are durable conclusions in documentation, not runtime facts.

## 6. Lifecycle comparison across conclusion types

| Conclusion type | Origin signal(s) | Supporting evidence | Authority requirements | Projection behavior | Staleness behavior | Contradiction behavior | Supersession behavior | Resolution behavior |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Fact` | Observation, provider output, discovery, import, deterministic inference, state patch | Evidence ids, source type, confidence, dimensions, timestamps | Source authority and predicate semantics; inferred facts require rule authority | Projected into state, support, conflicts, current/best views | `expires_at`, observed age, predicate volatility | `FactConflict` when same subject/predicate/dimensions has different values | Newer/support-stronger facts may become current; old facts remain historical | Current belief selected by support/confidence/recency; disputes remain visible |
| `FactSupport` | Multiple facts for same claim | Supporting fact ids and source types | Projection authority only | Projection aggregate/current sample | Expired if support facts expire | Competes with other value support records | Recomputed on replay | Supports selection; does not decide truth alone |
| Unsupported fact | Projected fact without support path or with missing visible support | Absence of support in inventory/view | Integrity projection authority | Inventory or explanation result | Changes when support arrives or expires | May coexist with conflicts | Recomputed | Add evidence, remove unsupported claim, or mark not evaluable |
| Stale fact | Fact with expired freshness window or stale predicate semantics | Timestamps, `expires_at`, predicate metadata | Temporal projection authority | Stale views and refresh recommendations | Core lifecycle state | May coexist with conflicts | Refreshed facts can supersede current stale value | Refresh via recommended capability or accept caveat |
| Contradiction / `FactConflict` | Competing facts | Competing fact ids/support records | Projection/integrity authority | Exposed as conflict/contradiction issue | Conflicts may decay as facts expire | Core lifecycle state | New support may make one value current while preserving conflict | Human review, more evidence, scoped dimensions, or policy interpretation |
| Verification result | Provider report, inventory, local observation, test/fixture output, imported record | Evidence, verification facts, `FactSupport`, predicate metadata | Verification method authority; not adoption authority | Capability verification inventory and status views | Derived from expiry and observation age | Competing verification status facts create dispute | New scoped verification can supersede old status | Re-run/acquire evidence; later policy may interpret threshold |
| `ToolNeed` / `CapabilityNeed` | `request_tool` decision today; capability signals proposed | Decision reason today; capability evidence/facts proposed | Runtime service today; future need authority should be evidence policy/operator where needed | Open tool needs, capability resolution metadata | Status can age socially, but no uniform expiry today | Duplicate/open-need dedupe; competing classifications not unified today | Status change to generated/validated/registered/rejected; future supersession may be useful | Satisfy by registered operation, provider/handoff candidate, generation, rejection, or closure |
| `CapabilityGap` | Missing registered capability, failed resolution, repeated request, verification failure | Capability facts, registry/catalog resolution, failed provider evidence | Gap-classification authority | Mostly implicit today | Could become stale as registry/catalog changes | Gap may conflict with new availability facts | Superseded by capability satisfaction or reclassification | Classify and route to build, handoff, catalog, or no-action path |
| `GapClassification` | Gap evidence, unsupported/failed capability state | Gap evidence and classification rationale | Classification policy/operator authority | Documentation/proposed read model | Stale when capability landscape changes | Competes with alternative classification | Superseded by later classification | Resolution path selection |
| `ProviderCandidate` | Catalog, registry, recommendation ranker, builder output, provider availability observation | Catalog metadata, tool specs, builder validation, availability facts | Candidate discovery authority only | Capability resolution output | Stale when catalog/registry/provider facts change | Competes with other candidates | Superseded by verification/adoption or rejection | Verify, reject, rank lower, or retain candidate |
| `ProviderVerification` | Verification evidence and scoped status facts | Evidence, facts, support, status predicate, target dimensions | Verification authority; not execution/adoption authority | Verification inventory | Stale by expiry/age | Disputed by competing status values | Superseded by newer verification under same scope | Adopt, reject, re-verify, or leave verified-but-not-adopted |
| `AdoptionDecision` | Provider verification plus policy/operator decision | Verification ids, contract/provider fingerprints, policy outcome, rationale | Adoption authority: operator or explicit policy | Would project preferred/fallback/rejected/revoked state | Stale when scope, version, contract, provider, or policy changes | Conflicts with competing adoption decisions for same scope/provider role | Revocation, demotion, deprecation, supersession | Selection state changes; runtime may consume later |
| Preferred/fallback provider | Adoption decisions | Adopted decision records | Projection authority over adoption records | Provider-selection projection | Inherits adoption staleness | Conflicts if multiple preferred providers under same single-cardinality scope | New adoption decision supersedes old preference | Select provider or ask for operator/policy resolution |
| `PolicyDecision` | Proposed tool/action or adoption scope | Tool metadata, policy table, risk class, approvals | Policy gate authority | Usually per-action result; durable if recorded with event/pending action | Depends on policy/approval expiry | May conflict with stale approvals or changed risk metadata | Later policy evaluation supersedes per-action result | Allow, block, require confirmation, require approval |
| `Approval` | Human/approver grant | Approver identity, action, scope, constraints, optional expiry | Approver authority | State lookup for policy gate | Expires at `expires_at` | May conflict with policy block or scope mismatch | Revocation vocabulary is limited today; expiry naturally supersedes | Enables allow under matching action/scope; otherwise ignored |
| `PendingAction` | Policy outcome requiring confirmation/approval | Proposed action, tool, arguments, scope, causation | Pending-action service and approver for approval transition | Projected action status | No built-in expiry in current model | Duplicate or contradictory pending actions are not a truth conflict | Completed/cancelled/approved status changes supersede pending | Approve, complete after external execution, cancel |
| `ActionPlan` | Model decision / tool need | Text plan payload, risk class, need link | ActionPlanService; operator acceptance is plan acceptance only | Projected legacy side-path state | No uniform staleness except quarantine/current-core status | Status machine prevents contradictory terminal transitions | Accepted/rejected/superseded | Accept, reject, supersede, or create non-executable handoff |
| `HandoffPlan` | Accepted action plan plus catalog recommendation | Action plan, catalog metadata, target facts | HandoffPlanService; external provider owns execution | Projected legacy side-path boundary | No uniform staleness except source plan/catalog changes | Must not imply approval/trust/credentials/registration | Superseded if source action plan/provider boundary changes | External provider executes outside Seed; Seed records boundary only |
| Alignment record / self-model outcome | Documentation claim + repository artifact fact + support relationship | Claim, artifact facts, support relationship | Reconciliation rule/human-review authority | Alignment knowledge/read model | Stale when docs or repository artifacts change | Potential conflict / requires review outcomes | Later reconciliation supersedes/refines | Supported, partially supported, missing support, potential conflict, not evaluable, human review |
| Reconciliation document | Prior docs, code inspection, inventories, audits | Citations, inspected files, explicit reasoning | Documentation author/reviewer authority | Durable architectural record, not runtime projection | Can be marked stale/quarantined/superseded by later docs | Can identify architectural contradictions | Later reconciliation supersedes or narrows scope | Direct answer, non-goals, rejected solutions, next vocabulary |

## 7. Shared properties

All durable conclusion-like concepts share most of these properties, even when
implemented differently:

| Shared property | Meaning in Seed |
| --- | --- |
| `ConclusionType` | The domain family: knowledge, integrity, capability need, provider selection, authority, planning/handoff, alignment, or documentation. |
| `ConclusionSupport` | The evidence, facts, claims, policy inputs, approvals, catalog entries, or rationale that justify the outcome. |
| `ConclusionAuthority` | The actor, service, policy, projection, reconciliation rule, or operator allowed to create or interpret the outcome. |
| `ConclusionStatus` | Current lifecycle state: current, stale, disputed, unsupported, open, accepted, rejected, approved, pending, adopted, fallback, revoked, superseded, not evaluable, etc. |
| `ConclusionProjection` | The read model or document surface where the current interpretation is visible. |
| `ConclusionStaleness` | The rule by which age, expiry, changed scope, changed provider version, changed policy, changed docs, or changed artifacts weaken the conclusion. |
| `ConclusionContradiction` | The rule by which competing conclusions are detected and preserved. |
| `ConclusionSupersession` | The rule by which later evidence, status changes, adoption decisions, documentation, or lifecycle events replace current authority without erasing history. |
| `ConclusionResolution` | The action or interpretation that closes, refreshes, accepts, rejects, reclassifies, adopts, revokes, or escalates the conclusion. |

These are documentation-level properties. They should not become a universal
runtime base class unless a future implementation need proves that value.

## 8. Differences that must remain distinct

The audited concepts are not fundamentally different *because* some are called
facts, needs, approvals, or plans. They are fundamentally different because they
answer different questions and require different authority.

| Category | Distinct question | Why it must remain distinct |
| --- | --- | --- |
| Fact | What is believed about the world/repository/system? | Truth-like knowledge support must not be confused with permission, planning, or adoption. |
| CapabilityNeed | What capability is needed or missing? | A need is demand/gap state, not proof that a provider works or is trusted. |
| GapClassification | What kind of gap is this and which path can resolve it? | Classification is routing/diagnosis, not capability satisfaction. |
| AdoptionDecision | Which verified provider is accepted for a scope? | Adoption requires authority beyond verification and ranking. |
| VerificationResult | Does evidence indicate a provider/capability satisfies a scoped check? | Verification is evidence/status, not adoption, trust, permission, or execution. |
| Approval | Who granted permission for an action/scope under constraints? | Approval is authority/permission, not evidence truth or provider quality. |
| ActionPlan | What non-executable plan is proposed or accepted? | Planning must not imply execution authorization, provider trust, or registration. |
| HandoffPlan | What external-provider boundary is described? | Handoff records delegation boundaries; external systems own execution and secrets. |

Therefore the important test resolves as follows:

```text
Fact, CapabilityNeed, GapClassification, AdoptionDecision, VerificationResult,
Approval, ActionPlan, and HandoffPlan are all durable conclusion types, but they
are not the same category. They share lifecycle vocabulary while retaining
different authority, projection, contradiction, staleness, and resolution rules.
```

## 9. Ownership and authority

Seed's current architecture already implies that conclusion ownership is
category-specific:

- **Observation owner:** observation sources, normalizers, and ingestors own raw
  source normalization and provenance preservation.
- **Evidence owner:** evidence ingestion owns immutable support payloads.
- **Fact owner:** fact extraction, inference rules, and state projection own
  interpreted claims and current support views.
- **Integrity owner:** projection/inventory/explanation code owns unsupported,
  stale, contradiction, and selection-rationale views.
- **Tool need owner:** `ToolNeedService` owns current `ToolNeed` creation,
  deduplication, and status changes from `request_tool` decisions.
- **Capability need / gap owner:** proposed vocabulary needs an explicit owner if
  capability needs become evidence-derived rather than request-driven.
- **Candidate owner:** catalog, registry, recommendation ranker, and builder
  produce candidates or recommendations; none should silently own adoption.
- **Verification owner:** verification facts and inventories own scoped status
  interpretation; they must not own provider preference.
- **Adoption owner:** proposed `AdoptionAuthority` or
  `ProviderAdoptionService`/`CapabilityAdoptionService` should own durable
  provider adoption decisions if implemented.
- **Policy owner:** `PolicyGate` owns policy outcomes for proposed actions.
- **Approval owner:** approver/human or authorized policy owns grants.
- **Pending-action owner:** `PendingActionService` owns pending-action lifecycle
  status.
- **Action-plan owner:** `ActionPlanService` owns legacy plan lifecycle.
- **Handoff owner:** `HandoffPlanService` owns non-executable handoff-boundary
  records; external providers own execution, credentials, retries, and jobs.
- **Reconciliation owner:** documentation/reconciliation process owns durable
  architectural conclusions and direct answers.

The main ownership risk is hidden authority escalation: recommendation must not
become adoption, verification must not become preference, approval must not
become execution, and handoff must not become provider trust.

## 10. Projection implications

Seed should continue to project conclusion families separately:

- Facts project into current state, support, confidence, stale views, conflicts,
  evidence graph, and explanations.
- Verification status should remain a fact/inventory interpretation until Seed
  explicitly adds adoption state.
- Capability needs should project as open/closed/statused needs and capability
  resolution metadata.
- Provider candidates should project as recommendations/candidates, not as
  preferred providers.
- Adoption decisions, if added, should project into preferred/fallback/rejected
  provider state and should be consumable by future selection/routing logic.
- Approvals and pending actions should project into policy-gate state and action
  lifecycle state.
- Action plans and handoff plans should remain legacy/quarantined side-path
  projections unless Seed deliberately changes Core MVP scope.
- Reconciliation documents should remain documentation authority, not runtime
  projection inputs unless separately ingested as documentation claims.

A shared vocabulary can improve explanation and audits, but a shared projection
object would blur important boundaries.

## 11. Staleness / contradiction / supersession

### Staleness

Seed already models staleness strongly for facts and verification facts through
`expires_at`, observed timestamps, predicate semantics, and refresh
recommendations. Other conclusion families have weaker or domain-specific
staleness:

- approvals can expire;
- provider verification can become stale when evidence expires or provider scope
  changes;
- adoption decisions should become stale when provider version, operation
  contract, scope, policy, or verification evidence changes;
- tool needs can become stale when the registry/catalog changes, but this is not
  uniformly modeled;
- action plans and handoff plans can become stale when the need, target, policy,
  or catalog recommendation changes, but current documents mostly handle this
  through quarantine and lifecycle status;
- documentation conclusions become stale when later reconciliations supersede
  them.

### Contradiction

Seed already models fact contradiction explicitly. Other conclusion families
need domain-specific contradiction rules:

- verification contradiction: same scoped target has competing status values;
- capability gap contradiction: a need says capability is missing while registry
  or verification evidence says it is available;
- adoption contradiction: multiple preferred providers for a single-cardinality
  adoption scope, or adopted provider with later revocation;
- approval contradiction: matching approval versus policy block or expired scope;
- action-plan contradiction: contradictory terminal states, currently guarded by
  lifecycle service rules;
- documentation contradiction: inconsistent architectural claims across docs or
  between docs and repository artifacts.

### Supersession

Seed preserves history and projects current status. That pattern applies across
conclusion types:

- a new fact can supersede the current representative value while preserving old
  evidence;
- a new support aggregate can change current belief;
- a later verification can supersede a stale or failed verification;
- an adoption revocation/demotion can supersede preferred-provider state;
- a pending action can move from pending to approved/completed/cancelled;
- an action plan can be accepted, rejected, or superseded;
- a later reconciliation can supersede an earlier architectural conclusion.

The common rule is: supersession should reduce current authority, not erase the
historical conclusion.

## 12. Non-goals

This reconciliation does not propose:

- a new engine;
- a planner;
- an autonomous subsystem;
- a runtime loop;
- an ontology engine;
- a generic reasoning framework;
- a universal `Conclusion` database table;
- a new event schema;
- a new projection store;
- provider execution;
- verification execution;
- adoption automation;
- policy automation beyond current policy gates;
- collapsing facts, needs, decisions, approvals, and plans into one runtime
  object.

## 13. Rejected solutions

### 13.1 One generic `Conclusion` runtime object

Rejected. A single persisted object would hide essential authority differences:
facts need evidence and contradiction semantics, approvals need grant authority,
adoption needs policy/operator authority, and handoffs need execution-boundary
constraints.

### 13.2 Verification becomes adoption

Rejected. A provider can be verified but not adopted. Verification is evidence
about capability fit; adoption is an authority-backed provider-selection
decision.

### 13.3 Recommendation becomes provider preference

Rejected. Catalog entries and `RecommendationRanker` output are candidate and
rationale signals. They are not trust, verification, adoption, or policy grants.

### 13.4 Approval becomes execution ownership

Rejected. An approval records permission under scope and constraints. It does
not make Seed an execution engine, scheduler, credential broker, or provider job
manager.

### 13.5 Action plans and handoff plans return to Core MVP execution

Rejected. Current architecture keeps them non-executable, legacy/quarantined,
and side-path only. They can be durable planning conclusions without changing
runtime ownership.

### 13.6 Staleness as a manually asserted universal status

Rejected. Fact and verification staleness should usually be derived from
`expires_at`, timestamps, predicate semantics, scope, provider version, and
policy/document changes. Manual stale labels may exist in documentation, but
runtime knowledge should prefer derived staleness where possible.

## 14. Direct answer

### 14.1 What existing durable conclusion types already exist?

Seed already has these durable or durable-adjacent conclusion types:

- facts and inferred facts;
- fact-support projections;
- current/best fact projections;
- unsupported fact, stale fact, and contradiction/fact-conflict integrity
  conclusions;
- verification status facts and capability verification inventory conclusions;
- tool needs;
- provider/capability recommendations and candidates;
- policy outcomes;
- approvals;
- pending actions and pending-action statuses;
- action plans;
- handoff plans;
- repository artifact facts;
- documentation claims;
- existence/structure/alignment reconciliation outcomes;
- architectural reconciliation documents and their accepted/rejected/stale
  positions.

### 14.2 Which are first-class today versus proposed vocabulary?

First-class today:

- `Observation`;
- `Evidence`;
- `Fact`;
- `FactSupport`;
- `FactConflict`;
- stale-fact refresh recommendations;
- `ToolNeed`;
- capability catalog entries and recommendations;
- recommendation ranker output;
- verification inventory output over facts;
- `PolicyDecision`;
- `Approval`;
- `PendingAction`;
- `ActionPlan`;
- `HandoffPlan`;
- documentation/repository observation and self-model alignment artifacts;
- reconciliation documents.

Proposed or not first-class as unified runtime models today:

- `Conclusion`;
- `ConclusionType`;
- `ConclusionEvidence` / `ConclusionSupport`;
- `ConclusionStatus`;
- `ConclusionProjection`;
- `ConclusionSupersession`;
- `ConclusionContradiction`;
- `ConclusionStaleness`;
- `ConclusionAuthority`;
- `CapabilityNeed` as a distinct evidence-derived model;
- `CapabilityGap` as a distinct durable model;
- `GapClassification` as a distinct durable model;
- `ProviderCandidate` as one unified durable model;
- `ProviderVerification` as one unified model separate from facts/inventories;
- `AdoptionDecision`;
- `PreferredProvider`;
- `FallbackProvider`.

### 14.3 What distinguishes observation, evidence, and conclusion?

- An **observation** is a normalized source signal: who or what reported a
  subject/predicate/value at a time with confidence, dimensions, metadata, and
  optional expiry.
- **Evidence** is the provenance-preserving support payload derived from an
  observation, provider output, artifact, import, or other input. Evidence
  supports claims but is not itself the interpreted claim.
- A **conclusion** is an interpreted durable outcome derived from evidence or
  authorized decision inputs. It has type-specific authority, status,
  projection, staleness, contradiction, supersession, and resolution behavior.

### 14.4 Is a Fact a conclusion?

Yes. A `Fact` is Seed's clearest first-class durable knowledge conclusion: an
interpreted state claim with provenance evidence, source type, confidence,
dimensions, timestamps, and optional expiry.

### 14.5 Is a CapabilityNeed a conclusion?

Yes, conceptually. A capability need is a durable gap/demand conclusion. Today,
Seed's first-class implementation is `ToolNeed`, created from `request_tool`
decisions. Evidence-derived `CapabilityNeed` remains proposed vocabulary rather
than a separate first-class runtime model.

### 14.6 Is an AdoptionDecision a conclusion?

Yes. It is a durable authority-backed provider-selection conclusion. Seed has
strong documentation for it but does not yet have it as a first-class runtime
model. It must remain distinct from recommendation and verification.

### 14.7 Is a GapClassification a conclusion?

Yes. It is a classification/routing conclusion over gap evidence. In current
Seed it is mostly documented/proposed vocabulary rather than a single first-class
runtime object.

### 14.8 Are verification results conclusions?

Yes. Verification results are scoped status conclusions. Today they should be
represented as verification facts plus support, conflicts, staleness, and
read-only inventory interpretation, not as provider adoption or trust.

### 14.9 Are approvals conclusions?

Yes. Approvals are authority/permission conclusions: an authorized approver
accepted an action/scope under constraints and optional expiry. They are not
knowledge-truth conclusions and do not imply execution ownership.

### 14.10 Are action plans conclusions?

Yes. Action plans are planning conclusions/proposals with lifecycle status. In
current Seed they are legacy/quarantined, text-only, and non-executable.
Acceptance of an action plan is not execution authorization.

### 14.11 Does Seed already possess a coherent conclusion taxonomy?

Not explicitly.

Seed already possesses many coherent **local** conclusion lifecycles:

- knowledge conclusions through `Observation -> Evidence -> Fact -> Projection`;
- integrity conclusions through support, stale, contradiction, and inventory
  views;
- capability-request conclusions through `ToolNeed`;
- verification conclusions through facts and read-only inventories;
- permission conclusions through policy, approvals, and pending actions;
- planning/handoff conclusions through quarantined lifecycle models;
- architectural conclusions through reconciliation documents.

However, these are parallel local taxonomies. Seed does not yet have an explicit
shared vocabulary that says they are all durable conclusion types with common
lifecycle properties.

### 14.12 Smallest missing vocabulary

The smallest missing vocabulary is documentation-level only:

| Term | Minimal meaning |
| --- | --- |
| `Conclusion` | A durable interpreted outcome derived from signals/evidence or authorized decision inputs. |
| `ConclusionType` | The family of conclusion: knowledge, integrity, capability need, provider selection, authority, planning/handoff, alignment, or documentation. |
| `ConclusionSupport` | The evidence, facts, claims, policy inputs, approvals, catalog entries, or rationale supporting the conclusion. |
| `ConclusionAuthority` | The source, service, policy, projection, operator, or reconciliation process allowed to create or interpret the conclusion. |
| `ConclusionStatus` | The current lifecycle state within the conclusion's own domain. |
| `ConclusionProjection` | The read model, inventory, state view, or document surface where current interpretation appears. |
| `ConclusionStaleness` | The domain-specific freshness rule. |
| `ConclusionContradiction` | The domain-specific conflict rule. |
| `ConclusionSupersession` | The rule for replacing current authority while preserving history. |
| `ConclusionResolution` | The domain-specific action or outcome that closes, refreshes, adopts, rejects, revokes, accepts, supersedes, or escalates the conclusion. |

This vocabulary is sufficient to describe Seed's durable outcomes without adding
an engine, planner, ontology, generic reasoning framework, or universal runtime
object.

Final conclusion:

```text
Seed does not yet possess an explicit coherent conclusion taxonomy, but it does
already possess multiple durable conclusion lifecycles. The smallest missing
piece is shared documentation vocabulary for Conclusion, ConclusionType,
ConclusionSupport, ConclusionAuthority, ConclusionStatus, ConclusionProjection,
ConclusionStaleness, ConclusionContradiction, ConclusionSupersession, and
ConclusionResolution, while preserving the distinct authority and lifecycle rules
of Facts, CapabilityNeeds, GapClassifications, AdoptionDecisions,
VerificationResults, Approvals, ActionPlans, and HandoffPlans.
```

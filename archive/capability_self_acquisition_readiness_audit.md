# Capability Self-Acquisition Readiness Audit

## Purpose

This documentation-only audit evaluates whether Seed already contains enough
architectural vocabulary to support future capability self-acquisition.

The question is not:

```text
How would Seed build self-acquisition?
```

The question is:

```text
How much of the ontology already exists?
```

This document inventories existing concepts, distinguishes settled architecture
from frontiers, and identifies what remains missing or unresolved. It does not
design acquisition engines, planners, tool stores, runtime workflows, schemas,
code, or implementation plans.

## Repository authority reviewed

The audit treats existing repository documentation as authoritative, especially:

- `docs/capability_gap_and_operator_bridge_reconciliation.md`
- `docs/capability_need_acquisition_reconciliation.md`
- `docs/capability_acquisition_reconciliation.md`
- `docs/adoption_decision_authority_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/capability_extension_methodology.md`
- `docs/selection_and_attention_frontier.md`
- `docs/inquiry_frontier.md`
- `docs/operations_frontier.md`
- `docs/foundational_ontology_reconciliation.md`
- `docs/architectural_status_and_next_frontier.md`

Repository authority wins over this audit. Where an existing reconciliation says
a concept is settled, this audit does not reopen it. Where an existing document
marks a concept as a frontier, this audit treats that concept as not yet
implementation-ready.

## Central finding

Seed appears to be **Ontology Mostly Present** for capability self-acquisition,
but not architecturally or implementation ready.

The repository already contains strong vocabulary for:

```text
Goal / Question / Operator intent
Need / ToolNeed / CapabilityNeed
Gap / CapabilityGap
Capability
Capability selection / execution path selection
Authority / policy / operator approval
Adoption / AdoptionDecision
Execution / command / action boundary
Observation
Evidence
Claim / Fact / Relationship / Projection
Verification
Operator bridge / handoff
Selection / attention / relevance / frontier
```

However, the repository does not yet reconcile these pieces into a settled
capability self-acquisition ontology. The missing center is not the individual
words. The missing center is the authoritative bridge from:

```text
unresolved goal, tension, gap, or need
    -> evidence-backed capability gap
    -> candidate capability or provider
    -> authorized adoption decision
```

Existing documents repeatedly warn against treating capability, recommendation,
selection, adoption, command, execution, or action as interchangeable. That
boundary discipline is exactly what would make self-acquisition possible later,
but it also prevents claiming readiness now.

## Minimal reference scenario

The smallest example is:

```text
echo hello
```

A tempting flow is:

```text
Goal
    -> Need
    -> Capability Selection
    -> Capability
    -> Execution
    -> Observation
    -> Evidence
    -> Claim
```

Repository authority suggests this flow is only partially correct.

A safer architectural reading is:

```text
Operator goal or question
    -> possible need
    -> capability support check
    -> supported execution path or capability gap
    -> decision / command if execution is authorized
    -> execution attempt
    -> observation or execution record
    -> evidence
    -> claim / fact / projection, if interpreted
```

For `echo hello`, the repository can already name many pieces:

- a goal can express the desired outcome;
- a need can represent the requirement to emit text;
- a capability can name shell or text-output ability;
- a capability support check can determine whether a path exists;
- a decision and command would be required before attempting work;
- execution would be the attempted command through a selected path;
- observation and evidence could preserve what happened;
- a claim could say that the command produced `hello` under a scope.

The flow should not be treated as self-acquisition. If no text-output capability
exists, the correct architectural outcome is not silent improvisation. It is a
capability gap, possible handoff or bridge, and possibly a need/candidate
adoption question under authority.

## Concept inventory

| Concept | Current repository status | Readiness for self-acquisition |
| --- | --- | --- |
| Goal | Present as operator/intent-adjacent vocabulary and in inquiry-facing examples. | Partially present. Goals can start attention, but repository authority does not say capability acquisition always begins with a goal. |
| Need | Present through `ToolNeed` / `CapabilityNeed`; request-driven creation exists. | Strongly present, but evidence-derived need acquisition remains unresolved. |
| Gap | Present and important; missing capability should be surfaced before compensation. | Strongly present as an architectural pattern; missing as canonical predicates and lifecycle. |
| Capability | Reconciled as evidence-backed, scope-bounded possibility rather than permission or execution. | Strongly present. |
| Capability selection | Present through capability resolution, recommendation/ranking, selection rationale, and execution-path vocabulary. | Partially present. Selection among known candidates is clearer than selection of what capability to acquire. |
| Authority | Present across operator, policy, decision, command, execution, and adoption boundaries. | Strongly present for constraints; partially unresolved for derived need acceptance and acquisition authority. |
| Adoption | Reconciled around `AdoptionDecision` as durable knowledge/policy state, not execution. | Strongly present for provider adoption; not yet generalized to all capability acquisition. |
| Execution | Reconciled as realization of an authorized command through a concrete path. | Strongly present as a boundary; self-acquisition must not collapse into execution. |
| Observation | Foundational knowledge-acquisition primitive. | Strongly present. |
| Evidence | Foundational immutable support/provenance primitive. | Strongly present. |
| Claim | Foundational interpreted proposition, projected into facts/relationships where supported. | Strongly present. |
| Verification | Present as evidence/fact/read-only interpretation of verification claims and provider verification input to adoption. | Strongly present as support; insufficient alone for adoption authority. |
| Operator bridge | Present as a named response to missing bridges between capabilities or missing deterministic utility/observation capability. | Strongly present as a pattern; not a full acquisition lifecycle. |

## What is already characterized

### Capability gaps

Seed can already characterize the pattern:

```text
Need exists.
No capability exists.
Gap recognized.
```

The existing capability-gap reconciliation explicitly warns that missing
capability should not be handled by reasoning harder, compensation, or hiding the
limitation. It should be surfaced as a gap. That is a central prerequisite for
self-acquisition readiness.

### Unmet needs

Seed already has `ToolNeed`, treated in practice as close to `CapabilityNeed`.
It can represent a missing or requested capability, and the existing service path
can create and deduplicate open needs from explicit `request_tool` decisions.

The limitation is that this is request-driven. Existing authority says Seed does
not yet define a principled lifecycle for turning observations, repeated
failures, manual work, provider handoffs, or reconciliation findings into a
durable need.

### Operator bridges

Seed can represent the idea that two capabilities may exist but lack a transfer
path between them. This is important because self-acquisition is not only about
adding endpoints. It may require recognizing a missing bridge.

However, the operator bridge is currently a visibility and boundary pattern, not
an acquisition mechanism.

### Acquisition candidates

Seed has partial candidate vocabulary:

```text
ProviderCandidate
ToolkitCandidate
CapabilityCatalog recommendation
registered operation
provider
implementation
adapter
handoff
```

These are enough to discuss candidates, but they are not yet a settled
self-acquisition candidate ontology. Existing provider-adoption work is strongest
when the scenario is:

```text
CapabilityNeed
    -> InternalFulfillment
    -> ProviderCandidate
    -> ProviderVerification
    -> AdoptionDecision
```

That is downstream of need recognition. It does not settle how Seed should infer
or accept the need in the first place.

## Acquisition readiness evaluation

The repository already supports many pieces of:

```text
Need
    -> Candidate Capability
    -> Adoption Decision
```

### Existing authority surfaces

Authority surfaces already include:

- operator authority;
- policy gates;
- verification thresholds as evidence, not authority by themselves;
- recommendation/selection services as ordering or explanation, not durable
  authority;
- catalog recommendations as metadata, not trust;
- runtime orchestration as routing, not adoption authority;
- `ToolExecutor` as execution after validation and policy preflight, not
  discovery, ranking, verification, or adoption authority;
- event/reconciliation layers as recording substrates, not decision makers.

This is a strong foundation. Self-acquisition would require these boundaries
because acquiring, adopting, approving, and executing are different authority
acts.

### Existing adoption concepts

Adoption concepts are well characterized for providers:

```text
AdoptionAuthority
AdoptionDecision
AdoptionEvidence
AdoptionScope
AdoptionStatus
AdoptionRevocation
PreferredProvider
FallbackProvider
```

The key finding is that adoption is evidence-backed selection authorization. It
is durable knowledge/policy state, not a tool call and not execution.

### Existing capability concepts

Capability concepts are also well characterized:

```text
Capability as possibility
Capability support
Capability verification
Provider
Tool
Adapter
Execution path
Command
Execution
Action
```

This gives Seed enough vocabulary to avoid a common self-acquisition error:
assuming that naming a capability authorizes, adopts, or executes it.

## Selection evaluation

Capability acquisition implicitly requires selection rationale.

Questions such as:

```text
Why this capability?
Why now?
Why not another capability?
```

are not answered by capability naming alone. Existing selection and attention
work distinguishes relevance, importance, priority, attention, frontier, and
selection rationale. It also preserves the boundary that selection is not truth,
authority, policy, decision, recommendation, or execution.

For capability self-acquisition, this means:

- a need may be known but not selected for acquisition;
- a gap may exist but not be a frontier;
- a candidate may be relevant but not adopted;
- a selected candidate may require authority before adoption;
- attention can explain current focus without proving priority or readiness.

The selection vocabulary is therefore highly relevant, but still partly frontier
status. It supports audit reasoning today; it does not yet license an
acquisition planner, ranker, or loop.

## Authority evaluation

Existing authority reconciliations partially answer:

```text
Who may acquire?
Who may adopt?
Who may approve?
Who may execute?
```

### Who may acquire?

This remains unresolved. Existing capability-need acquisition work explicitly
identifies no settled acquisition authority for accepting a derived capability
need from evidence.

### Who may adopt?

This is mostly answered for provider adoption: explicit operator approval is the
safe default unless policy authorizes automatic adoption for a specific
operation, provider, verification threshold, scope, and risk class.

### Who may approve?

Approval is distributed by risk and boundary. Operator and policy authority are
recognized; verification can inform approval but does not replace it.

### Who may execute?

Execution requires a command with execution-request authority, policy preflight,
approval when required, a selected execution path, and traceable target/scope.
Runtime or executor components may perform execution after these boundaries, but
they do not own adoption or acquisition authority.

## Inquiry evaluation

Capability acquisition should not be assumed to begin with a goal.

Existing inquiry and selection/frontier work indicates several possible origins:

```text
goal
question
tension
gap
need
unknown
frontier
operator request
repeated manual work
failed resolution
handoff pattern
reconciliation finding
```

Repository evidence suggests:

- a goal can create a need;
- a question can expose a gap;
- a tension can motivate an inquiry;
- a gap can become a frontier;
- a need can be explicit before evidence aggregation exists;
- repeated failures or handoffs can signal a capability gap;
- a frontier can be selected without being implementation-ready.

The safest conclusion is that capability self-acquisition has no single settled
starting object in the current ontology. The repository is actively
characterizing inquiry, operations, selection, and frontier vocabulary, but these
remain non-implementation-ready.

## Missing, partial, and unresolved pieces

### Concepts already present

- `Observation`
- `Evidence`
- `Claim`
- `Fact`
- `Relationship`
- `Projection`
- `Question`
- `Goal`
- `ToolNeed` / `CapabilityNeed`
- `Capability`
- `CapabilityCatalog`
- `Provider`
- `Tool`
- `Adapter`
- `Implementation`
- `ExecutionPath`
- `Command`
- `Execution`
- `Action`
- `Verification`
- `AdoptionDecision`
- `AdoptionAuthority`
- `PreferredProvider`
- `FallbackProvider`
- `Policy`
- `Operator authority`
- `Selection rationale`
- `Relevance`
- `Priority`
- `Attention`
- `Frontier`
- `Operator bridge`
- `Handoff`

### Concepts partially represented

- `CapabilitySignal`
- `CapabilityObservation`
- `CapabilityGap` as canonical evidence-backed predicate/lifecycle state
- `CapabilityEvidence` grouped around a candidate gap or need
- `CapabilityResolution` as a durable relation between need and possible
  satisfaction paths
- `CapabilitySatisfied`
- `CapabilitySuperseded`
- `CapabilityStale`
- acquisition candidate distinct from provider recommendation or generated
  toolkit candidate
- selection rationale for acquisition priority rather than ordinary surface
  selection
- inquiry origin object for capability acquisition
- bridge from handoff/manual work/repeated failure into durable need state

### Concepts that appear missing

- canonical predicates for capability gap observations, such as
  `capability_gap_observed`, `manual_work_repeated`, `fallback_used`, or
  `capability_resolution_failed`;
- aggregation thresholds for deciding when signals become a durable need;
- acquisition authority for accepting derived capability needs from evidence;
- stale/resolved/superseded/disproven lifecycle states for capability needs
  beyond current coarse statuses;
- a canonical bridge from reconciliation findings into evidence-backed needs;
- a canonical bridge from repeated operator handoff/manual work into needs;
- a canonical bridge from failed capability resolution into durable gap evidence;
- acquisition-specific selection rationale answering why this gap/candidate is
  attended to now;
- a reconciled ontology for whether acquisition begins from goal, tension, gap,
  need, or inquiry.

### Concepts that remain unresolved frontiers

- Inquiry ontology;
- operations ontology;
- selection and attention ontology beyond already-settled surface selection
  rationale;
- derived capability-need acquisition;
- capability acquisition authority;
- acquisition-candidate lifecycle;
- capability gap lifecycle;
- relationship between frontier selection and acquisition priority.

## Readiness classification

Classification:

```text
Ontology Mostly Present
```

Not selected:

- **Not Ready**: too pessimistic. Seed already has substantial relevant
  vocabulary and reconciled boundaries.
- **Conceptually Emerging**: too weak. The vocabulary is not merely emerging;
  many pieces are already reconciled.
- **Architecturally Ready**: too strong. The evidence-to-need bridge,
  acquisition authority, acquisition-candidate lifecycle, and inquiry/selection
  starting conditions remain unresolved.
- **Implementation Ready**: clearly too strong. Existing status documents
  explicitly warn against implementing engines, planners, runtime routing,
  acquisition logic, and frontier ontologies before reconciliation.

## Major findings

1. **The vocabulary exists more than expected.** Seed already has most nouns
   needed to discuss self-acquisition without inventing a new conceptual world.
2. **The missing piece is connection, not terminology.** Existing concepts are
   not yet reconciled into a self-acquisition lifecycle.
3. **Gap visibility is a prerequisite.** The repository strongly prefers naming
   missing capability over compensating with reasoning.
4. **Need recognition is request-driven today.** Evidence-derived durable need
   creation remains the most important unresolved conceptual gap.
5. **Adoption is better understood than acquisition.** Provider adoption has a
   strong authority model; acquisition authority remains open.
6. **Selection rationale is required.** Capability acquisition cannot be
   explained without answering why a capability or candidate was selected now
   instead of alternatives.
7. **Execution boundaries are already protective.** Capability is possibility;
   command is authorized request; execution is attempted realization; action is
   mutation.
8. **Inquiry origin is unresolved.** Acquisition may begin from goal, question,
   tension, gap, need, repeated failure, handoff, or frontier.
9. **Implementation discussion would be premature.** The repository has not yet
   reconciled the ontology needed to safely discuss acquisition loops or runtime
   behavior.

## Unresolved tensions

- Seed can represent an explicit need, but not yet a principled evidence-derived
  need.
- Seed can recognize a gap pattern, but lacks canonical gap predicates and
  lifecycle states.
- Seed can discuss candidates, but provider candidates, toolkit candidates,
  catalog recommendations, handoffs, and registered operations are not unified as
  acquisition candidates.
- Seed can verify capability/provider claims, but verification does not equal
  adoption.
- Seed can adopt providers under authority, but acquisition authority is not yet
  settled.
- Seed can select among candidates on some surfaces, but acquisition priority and
  active attention remain frontier-level questions.
- Seed can execute authorized commands, but execution is downstream of decision,
  policy, approval, and capability support.
- Seed can preserve inquiry frontiers, but it does not yet define whether
  acquisition starts from goal, tension, gap, need, or another inquiry object.

## Audit conclusion

Seed already contains enough architectural concepts to make capability
self-acquisition discussable with precision. It does not yet contain enough
reconciled architecture to make self-acquisition architecturally ready, and it is
far from implementation ready.

The likely future conceptual requirement is not a large new ontology. It is a
small reconciliation layer that connects existing knowledge acquisition,
capability gap, need, candidate, selection, authority, adoption, verification,
and execution-boundary concepts without collapsing them.

Until that reconciliation exists, implementation discussion would be premature.

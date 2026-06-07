# Roadmap and Methodology Reconciliation

## Executive Summary

This reconciliation finds that the repository evidence supports an observed
architectural discovery pattern:

```text
Implementation
  -> discovery of ambiguity or boundary pressure
  -> audit
  -> reconciliation
  -> vocabulary
  -> improved implementation or safer next slice
```

The pattern should be documented, but only as an **architectural observation**
and light **methodology note**. It should not become governance, a mandatory
process, a review gate, an approval workflow, a planner, or project-management
policy.

The roadmap/status structure should also distinguish three kinds of future work:

```text
Knowledge Acquisition: What do we know?
Knowledge Integrity: Can this projected knowledge be safely interpreted?
Knowledge Selection: What projected knowledge matters now, and why?
```

The current `knowledge_acquisition_status` board is accurate for local
observation slices, but it is too narrow to represent the architectural pressure
now visible in integrity, explanation, lifecycle, context composition, and
selection work. The larger risk is no longer simply adding more read-only
observation sources. The larger architectural challenge is increasingly
**knowledge interpretation**: preserving and surfacing support, absence,
contradiction, staleness, classification, verification limits, context relevance,
and operator-facing explanation without turning those surfaces into hidden truth
selection, execution, planning, or mutation.

This document is documentation only. It does not change `Runtime`,
`ToolExecutor`, `EventLedger`, `ProjectionStore`, observation behavior,
projection behavior, fact mutation, projection mutation, execution behavior,
orchestration, provider integration, planner behavior, or LLM reasoning.

## Files Inspected

Minimum requested files inspected:

- `README.md`
- `docs/knowledge_acquisition_status.md`
- `docs/reasoning_roadmap.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/context_composition_vocabulary.md`
- `docs/context_composition_reconciliation.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/capability_extension_methodology.md`
- `docs/architecture_principles.md`
- `docs/architecture.md`

Related roadmap, status, architecture, and reconciliation documents inspected:

- `docs/roadmap_reconciliation.md`
- `docs/local_observation_roadmap_reconciliation.md`
- `docs/repository_observation_source_design.md`
- `docs/explainability_reconciliation.md`
- `docs/explainability_audit.md`
- `docs/capability_verification_reconciliation.md`
- `docs/capability_verification_vocabulary.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/self_observation_reconciliation.md`
- `docs/local_observation_roadmap_audit.md`
- `docs/local_network_observation_audit.md`
- `docs/storage_topology_observation.md`
- `docs/listening_port_observation.md`
- `docs/generated/architecture/architecture_graph.json`
- `docs/generated/architecture/runtime_ownership.dot`
- `docs/generated/architecture/runtime_ownership.mmd`

## Methodology Findings

### Finding: the pattern is supported by repository evidence

The repository repeatedly moves from implementation pressure to documentation
clarification before continuing implementation. The exact wording varies by
domain, but the sequence is consistent enough to document as observed behavior:

```text
Implementation
  -> boundary ambiguity or missing vocabulary
  -> audit or inventory
  -> reconciliation
  -> vocabulary or principle
  -> narrower implementation guidance
```

Examples:

| Domain | Evidence of pattern | Resulting architectural effect |
| --- | --- | --- |
| Explainability | Explainability audit and reconciliation preceded an explanation contract vocabulary. | Explanation is treated as a read-only account over projected knowledge, support, conflicts, provenance, and limits rather than a truth engine or execution trigger. |
| Capability verification | Verification fit/audit/reconciliation preceded the verification vocabulary. | Requested, known, candidate, recommended, available, and verified capability concepts remain separate. |
| Context composition | Context composition reconciliation preceded Context Composition Vocabulary v1. | Context selection is framed as relevance over already-projected knowledge, not fact creation or truth selection. |
| Knowledge classification | Classification vocabulary emerged after repeated ambiguity about observation kinds. | Facts can be described by class without making class imply priority, trust, policy, verification, or truth. |
| Knowledge lifecycle | Maintenance/lifecycle reconciliation reframed maintenance as integrity. | Integrity becomes a read-only characterization concern, not repair, mutation, or governance. |
| Repository observation | Repository observation source design followed self-observation and architecture metadata work. | Repository knowledge is kept as bounded observation-source design rather than implicit self-modifying behavior. |
| Local observations | Local network, storage topology, and listening port slices each preserve negative space after ambiguity about availability, reachability, health, ownership, and management. | Acquisition remains narrow and evidence-backed while stronger interpretations are deferred to separate evidence or vocabulary. |

### Finding: this is methodology, but not governance

The pattern is useful as a lightweight methodology because it describes how Seed
has been safely growing architecture under ambiguity. It should remain phrased as
an observed repository behavior, not as a required lifecycle for every change.

Appropriate wording:

```text
When implementation exposes repeated ambiguity, Seed has tended to pause for an
audit, reconcile boundaries, name vocabulary, and then continue implementation
with narrower semantics.
```

Inappropriate wording:

```text
Every feature must complete audit, reconciliation, vocabulary, and approval
before implementation.
```

The second wording would create process enforcement. The repository evidence
supports the first wording only.

## Architectural Discovery Pattern Findings

### Supported pattern

The supported pattern is:

```text
Implementation
  -> Audit
  -> Reconciliation
  -> Vocabulary
  -> Improved Implementation
```

A slightly more accurate repository-specific version is:

```text
Implementation or roadmap pressure
  -> ambiguity discovery
  -> audit / inventory
  -> reconciliation
  -> vocabulary / principle / boundary note
  -> narrower implementation or backlog split
```

The pattern is especially visible when a term risks collapsing several separate
architectural concerns into one overloaded word. Examples include
`availability`, `verification`, `context`, `classification`, `maintenance`,
`explanation`, and `self observation`.

### Where it should be documented

The pattern should be documented in two places, in this order:

1. **This reconciliation document** as the direct architectural observation.
2. A short cross-reference in either `docs/architecture_principles.md` or
   `docs/reasoning_roadmap.md` if the team wants a canonical pointer later.

It should not be documented as a hard architecture principle yet, because that
would make an empirical observation sound normative. It also should not be left
nowhere, because the pattern is now useful for interpreting why the roadmap keeps
creating audit/reconciliation/vocabulary documents before implementation.

### Classification of documentation options

| Option | Fit | Evaluation |
| --- | --- | --- |
| Methodology | Good, if lightweight. | Useful as a descriptive way to explain how ambiguity has been handled. Must avoid mandatory language. |
| Architectural observation | Best fit. | Most accurate: this is repository behavior observed across several domains. |
| Architecture principle | Premature. | Could become a principle later, but current evidence supports description, not enforcement. |
| Roadmap note | Good as a cross-reference. | Helps explain why future work may be grouped by acquisition, integrity, and selection. |
| Nowhere | Poor. | Would hide an important pattern that affects how documentation and implementation are evolving. |

## Roadmap Organization Findings

### Current roadmap shape

The current roadmap/status documentation already contains the ingredients for a
three-part roadmap, but the organization is uneven:

- `docs/knowledge_acquisition_status.md` is explicit and practical for local
  acquisition slices.
- `docs/reasoning_roadmap.md` contains broader reasoning, contradiction,
  temporal, verification, and capability-boundary concerns.
- `docs/knowledge_acquisition_and_selection.md` canonically separates
  acquisition from selection.
- `docs/knowledge_lifecycle_reconciliation.md` explicitly recognizes
  Acquisition, Integrity, Selection, and Response as lifecycle concerns.
- `docs/context_composition_vocabulary.md` defines selection language in detail.
- `docs/explanation_contract_vocabulary.md` defines how selected knowledge is
  communicated and caveated.

The repository therefore already supports the distinction, but it does not yet
present future work as a clear board or map across Acquisition, Integrity, and
Selection.

### Recommended roadmap taxonomy

Future roadmap/status work should distinguish:

```text
Knowledge Acquisition
Knowledge Integrity
Knowledge Selection
```

`Response` remains important, but it is best treated as a downstream
communication surface that depends on Selection rather than as a fourth backlog
bucket in the roadmap. If Response work grows large enough, it can be split later
without changing the acquisition/integrity/selection model.

## Acquisition Backlog Findings

The acquisition backlog is coherent and already well represented by
`docs/knowledge_acquisition_status.md`.

Natural acquisition work includes:

- Users observation
- Groups observation
- Package observation
- Systemd unit observation
- Schedule observation
- Certificate observation
- Process marker observation
- Container marker observation

These items share a common shape:

```text
bounded read-only source
  -> observation
  -> evidence
  -> fact
  -> projection
```

They should remain acquisition work as long as they preserve the existing
negative-space rules:

- no shell execution;
- no sudo requirement;
- no network probing;
- no provider calls;
- no service management;
- no host mutation;
- no health, reachability, availability, ownership, or supportability inference
  unless separately supported by scoped evidence.

### Acquisition risk assessment

Acquisition risk is now mostly slice-specific rather than architectural:

- parsing local files safely;
- bounding input size;
- avoiding sensitive data capture;
- choosing stable subject IDs and dimensions;
- preventing local configuration from being promoted into stronger claims.

Those risks are real, but recent Hostname/Identity, Local Network, Mount,
Kernel, CPU, Memory, Storage Topology, and Listening Port work shows that the
existing acquisition path is functioning.

## Integrity Backlog Findings

Integrity work is the least visible as a single roadmap bucket even though it is
now a recurring architectural pressure.

Natural integrity work includes:

- why-not explanations;
- projection integrity summaries;
- integrity surfacing in operator views;
- selection rationale support from integrity metadata;
- support/conflict/staleness/verification visibility;
- better absence handling;
- current versus stale versus historical projection disclosure;
- confidence and support summaries that avoid hidden truth arbitration;
- contradiction and competing-evidence summaries;
- graph issue visibility;
- capability verification status interpretation;
- classification display without implying priority, trust, or truth.

Integrity should be documented as a read-only characterization layer over
projected knowledge. It should not be documented as repair, mutation,
truth-maintenance, fact arbitration, automatic refresh, automatic verification,
or governance.

### Integrity risk assessment

Integrity is becoming a larger risk because Seed can now acquire many narrow
facts, but operators still need to understand:

- what supports a fact;
- what is absent;
- what conflicts;
- what is stale;
- what is merely configured;
- what is verified versus unverified;
- what is recommended versus executable;
- what is relevant versus true;
- what is unknown rather than false.

The risk is interpretive: a correct observation can become misleading if its
support, limitation, contradiction, age, or non-inference boundary is not carried
forward.

## Selection Backlog Findings

Selection work is already documented by context composition and explanation
vocabulary, but it is not yet presented as a clear roadmap track.

Natural selection work includes:

- context source precedence;
- context metadata;
- context explanation;
- response contract;
- selection rationale;
- operator-facing explanation improvements;
- context relevance reasons;
- why a selected item appears in an answer;
- why an omitted item was not selected;
- budget/order disclosure where useful;
- carrying integrity metadata into selected context;
- distinguishing answer context from capability-gap context.

Selection should remain read-only. It may choose, order, summarize, budget, and
explain projected knowledge, but it must not observe new facts, mutate state,
resolve truth, execute operations, call providers, or create projections.

### Selection risk assessment

Selection risk grows as acquisition succeeds. More projected knowledge means
more chances to omit the relevant caveat, over-prioritize noisy metadata, hide a
conflict, collapse recommendation into availability, or make a response sound
more certain than the projected evidence allows.

## Architectural Risk Findings

### Statement evaluated

> Knowledge acquisition is no longer the primary architectural risk. Knowledge
> interpretation is becoming the larger architectural challenge.

### Finding

The repository evidence mostly supports this statement, with one qualification:
acquisition is still important, but the core acquisition architecture is no
longer the most uncertain part of the design.

Recent observation implementations show that the existing path works for several
local domains:

```text
Observation -> Evidence -> Fact -> Projection
```

The remaining planned acquisition slices are meaningful, but they are variations
on a pattern that is already working: identify a bounded read-only source, record
narrow observations, attach evidence, project scoped facts, and document what the
slice must not imply.

By contrast, repeated reconciliations show that the hard architectural questions
are increasingly about interpretation:

- how to explain absence without inventing negative facts;
- how to expose contradictions without resolving truth automatically;
- how to show support and confidence without making confidence authority;
- how to present context relevance without turning relevance into truth;
- how to distinguish provider recommendation, registered operation candidate,
  known capability, available capability, and verified capability;
- how to classify facts without making classification imply priority or trust;
- how to preserve lifecycle and integrity signals without creating mutation or
  repair behavior;
- how to answer operator questions from selected knowledge without hiding the
  evidence boundary.

Therefore the better roadmap emphasis is not “stop acquisition.” It is:

```text
Continue acquisition slices, but stop treating acquisition as the only future
roadmap category. Add explicit integrity and selection tracks so interpretation
risk is visible.
```

## Recommended Documentation Updates

Recommended smallest documentation updates, in order:

1. Keep `docs/roadmap_and_methodology_reconciliation.md` as the canonical record
   of this evaluation.
2. Add a short note to `docs/knowledge_acquisition_status.md` clarifying that it
   is the acquisition board, not the complete knowledge roadmap.
3. Add a compact “Knowledge Roadmap Tracks” section to `docs/reasoning_roadmap.md`
   or a new `docs/knowledge_roadmap.md` with three headings:
   - Knowledge Acquisition
   - Knowledge Integrity
   - Knowledge Selection
4. Add a one-paragraph cross-reference in `docs/architecture_principles.md` only
   if the observed discovery pattern continues to recur. The wording should say
   “observed pattern,” not “required process.”
5. Avoid adding new governance, gates, approvals, mandatory review workflows,
   runtime orchestration, execution behavior, provider integration, fact
   mutation, or projection mutation.

## Recommended Smallest Next Step

The smallest next step is documentation-only:

1. Add a short “Roadmap scope” note to `docs/knowledge_acquisition_status.md`
   saying that the file tracks acquisition slices only.
2. Add a small triage table to `docs/reasoning_roadmap.md` that groups future
   roadmap items into Acquisition, Integrity, and Selection.
3. Link both notes back to this reconciliation.

That is enough to make the roadmap structure visible without introducing a
process, governance model, planner, runtime change, execution behavior, or
project-management workflow.

## Explicit Non-Goals

This reconciliation does not create or recommend:

- governance;
- mandatory process requirements;
- review gates;
- approval workflows;
- project-management policy;
- runtime behavior;
- ToolExecutor behavior;
- EventLedger ownership changes;
- ProjectionStore ownership changes;
- execution behavior;
- orchestration;
- planners;
- reasoning systems;
- provider integrations;
- LLM reasoning;
- fact mutation;
- projection mutation.

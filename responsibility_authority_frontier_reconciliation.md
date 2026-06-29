# Responsibility / Authority Frontier Reconciliation

## Scope

This bounded reconciliation reviews recent completed investigations together:

- Inquiry Subject Resolution
- Inquiry Identity Ontology
- Inquiry Anchor / Dependency Head
- Repository Dependency Ordering Invariant
- Dependency Transformation Invariant

It asks whether those investigations independently recovered one recurring implementation behavior involving responsibility, authority, eligibility, fulfilled work, handoff, compatibility, consumed implementation evidence, and produced implementation evidence.

This is not ownership recovery. It does not introduce a dependency framework, planner, orchestration layer, ontology, repository-wide grammar, or redesign. Repository authority wins.

## Implementation evidence

### Inquiry surfaces establish bounded identity before narrower work

The Inquiry Subject Resolution investigation found that bounded ask and answer surfaces begin from explicit, bounded identities rather than semantic recovery. The strongest implementation evidence was:

- static `QuestionSurfaceInventoryRow` entries binding `question_family` to answer surface, responsibility, authority boundary, bounded eligibility, required arguments, and implementation reason;
- bounded ask dispatch that validates exact `question_family` strings, rejects unknown or non-dispatchable families, enforces required argument counts, and forwards operator-provided values unchanged;
- parameterized surfaces such as Reasoning Path, Selection Path, and Reference Selection beginning surface-local evidence selection only after `domain`/`subject`, `target`, or `domain` are already supplied.

The same investigation explicitly limited the claim: subject acquisition is distributed across inventory, dispatch, CLI parameters, and surface-local rules. It did not find a general subject-resolution owner or semantic parser.

The Inquiry Identity Ontology investigation sharpened that boundary. It found several distinct implementation identities rather than one inquiry ontology:

- `question_family` for bounded ask routing and eligibility;
- `subject` for fact/support/diagnostic identities and Reasoning Path matching;
- `target` for Selection Path;
- `domain` for Reasoning Path context and Reference Selection routing;
- `query` for Source Navigation;
- `note` for Inquiry Orientation;
- `focus` for Operational Story answer material.

Those identities have different validation, normalization, routing, evidence-selection, output, and authority boundaries. This is evidence for explicit anchoring and bounded authority, not for universal `subject` or `dependency` vocabulary.

### Inquiry Anchor / Dependency Head recovered a role, not an ontology

The Inquiry Anchor / Dependency Head investigation found a recurring local ordering:

```text
inquiry / surface request
-> established organizing identity
-> evidence selection or validation
-> reasoning / lineage assembly
-> answer composition / rendering
```

The reviewed surfaces supported this role with different occupants:

| Surface | Local identity | Downstream work made eligible |
| --- | --- | --- |
| Question Surface Inventory / bounded ask | exact `question_family` | dispatch, bounded eligibility, required-argument enforcement |
| Reasoning Path | `domain` + `subject` | derivation evidence filtering, consumers, lineage payloads |
| Selection Path | `target` | recognized selection branch, candidate/unknown outcome, lineage |
| Reference Selection | `domain` | supported-domain branch and reference choice |
| Inquiry Orientation | selected `InquiryNoteRecord` and token set | lexical related-material matching |
| Source Navigation | `query` | projected source-fact lookup |
| Operational Story | primary pressure/focus | downstream answer composition |

The investigation rejected a single ontology: `question_family`, `subject`, `target`, `domain`, `query`, note identity, and focus are not interchangeable. The stronger supported observation was that a value must be established before the surface-local responsibility can perform its narrower work.

### Repository dependency ordering recovered eligibility handoffs across completed families

The Repository Dependency Ordering Invariant investigation found recurring ordered handoffs across completed responsibility families. The supported bounded invariant was:

```text
Completed responsibility families repeatedly make one responsibility eligible by first establishing the dependency object, evidence record, validation result, assessment, construction result, or compatibility handoff that the next responsibility consumes.
```

The strongest implementation-backed examples were:

- Operational Responsibility records a durable `tool.call.completed` event before post-execution knowledge extraction consumes that completed event.
- Projection Influence Lineage recovers lineage before replay scope assessment, selection justification, replay target selection, execution request, finalized state, and publication.
- Read-Model Ownership derives visible state inputs, dependency identity, cache lookup result, construction request/result, and cache publication request/result in bounded handoffs.
- Answer Composition builds evidence and implementation-local payloads before compatibility answer objects and rendering.
- Evidence Contract work preserves candidate agreement, provenance, and non-promotion before downstream grammar visibility consumes the agreement.
- Inquiry-like surfaces establish local identity before subject-specific evidence selection and reasoning.

The investigation also supplied important counterexamples: some sources are parallel compositions rather than sequential prerequisites; Execution Visibility is a report/compatibility boundary more than a prerequisite pipeline; Reasoning Path can build broad upstream audits before identity-specific filtering; unsupported Reference Selection domains and Selection Path targets stop or return unknown rather than forcing inference.

### Dependency Transformation recovered consumed and produced evidence, but not a framework

The Dependency Transformation Invariant investigation found that completed responsibility families often become visible by naming what a boundary consumes and what it produces:

- durable event handoff: `tool.call.completed` event to post-execution extraction;
- source grouping: admitted capability facts, executable operation contracts, and requested needs to capability inventory sources/universe;
- assessment/justification handoff: projection lineage to scope assessment, justification, selection, execution request, finalized state, publication request, visible state;
- construction/publication handoff: visible state to read-model construction inputs, dependency identity, cache lookup request/result, construction request/result, publication request/result;
- compatibility handoff: private answer or debug payloads to public compatibility objects/accessors.

Its central supported formulation was bounded: successful responsibility boundaries commonly make consumed implementation evidence explicit and hand an implementation-local result, request, payload, event, or durable record to the next responsibility while preserving compatibility.

It explicitly rejected the stronger formulation that explicit dependency transformation is the single repository-wide architecture defining every responsibility.

## Recovered recurring observations

### 1. The investigations are repeatedly describing the same family of behavior

Yes, within bounded scope.

Across the five reports, the same implementation behavior recurs:

```text
one bounded responsibility produces or preserves explicit implementation evidence
-> another bounded responsibility consumes that evidence
-> the consuming responsibility becomes eligible to perform its own narrower work
-> authority, ownership, and compatibility remain local rather than collapsing into a global framework
```

This is visible in inquiry surfaces as identity-before-surface-specific reasoning. It is visible in operational execution as completed-event-before-extraction. It is visible in projection and read-model code as request/result or assessment/publication chains. It is visible in answer composition and diagnostics as private payloads feeding compatibility objects.

The recurrence is not merely execution order. In the strongest examples, downstream functions or records consume a named predecessor object: completed event, replay assessment, selection justification, construction request/result, publication request, identity, payload, or selected note/query/target/domain.

### 2. `dependency` is not always the strongest repository-native vocabulary

`Dependency` accurately describes part of the behavior: downstream work depends on upstream evidence, records, identities, assessments, or construction results.

However, the completed investigations consistently make the behavior more repository-native when phrased through responsibility, authority, and eligibility:

- **Responsibility**: each boundary performs its own bounded work rather than recreating upstream work.
- **Authority**: a boundary consumes evidence produced under another boundary's authority without taking over that upstream authority.
- **Eligibility**: downstream work begins only after the required evidence, identity, validation, assessment, construction result, or handoff exists.
- **Compatibility**: many handoffs preserve existing public shape, event shape, cache semantics, or answer/report accessors.

The repository evidence therefore supports `dependency` as a role description, but not as the dominant vocabulary for a universal dependency system. The stronger frontier language is:

```text
bounded responsibility eligibility after explicit authority-preserving handoff
```

This wording better preserves the completed families' evidence while avoiding unsupported framework, ontology, or planner claims.

### 3. The proposed recurring observation is supported only with careful bounds

The proposed statement was:

```text
A responsibility
is only eligible
to fulfill its own responsibility
after consuming work
already produced
under another responsibility's authority.
```

Implementation evidence supports a bounded version:

```text
In repeatedly recovered responsibility families, a downstream responsibility commonly becomes eligible for its narrower work only after it consumes explicit implementation evidence, identity, validation, assessment, construction result, durable record, payload, request, result, or compatibility handoff produced or preserved by an upstream responsibility boundary.
```

The implementation evidence does **not** support the unqualified version as a universal law. Some boundaries read shared `State`; some source sets are joined in parallel for presentation; some reports group diagnostic measurements; some broad audits are built before subject-specific filtering; some unsupported identities stop reasoning instead of enabling it.

## Supported architectural interpretations

### Responsibility boundaries do not routinely recreate upstream work

Supported.

The reviewed families repeatedly show downstream responsibilities consuming explicit upstream outputs:

- post-execution extraction consumes the already-recorded completed event rather than executing or recording the tool call itself;
- projection replay assessment/selection/execution consume prior lineage, assessment, justification, and selected target objects;
- read-model construction consumes visible state inputs, dependency identity, and cache lookup result; publication consumes a construction result;
- answer composition consumes upstream audit outputs and private payloads before compatibility object construction;
- inquiry surfaces consume exact family, surface args, selected notes, queries, or targets before narrower evidence selection.

### Authority remains bounded at handoff points

Supported.

The investigations repeatedly preserve the authority of the producer boundary:

- bounded ask dispatch does not infer missing subject identity; it forwards explicit operator-provided arguments to existing surfaces;
- Inquiry Orientation preserves notes as operator prose and explicitly does not promote them into facts, goals, ownership, recommendations, commands, or runtime instructions;
- Source Navigation consumes projected source facts and refuses runtime, semantic, reachability, ownership, or truth claims beyond source-fact matching;
- capability inventory separates admitted capability knowledge from executable operation contract metadata and requested capability needs;
- read-model and projection handoffs preserve existing state/cache/publication compatibility rather than expanding ownership.

### Eligibility follows fulfilled local prerequisites

Supported, but not universalized.

Strong evidence appears where downstream work is unavailable, unknown, or unsupported until a local prerequisite exists:

- bounded ask rejects unknown or non-dispatchable question families and enforces exact required arguments;
- Reference Selection supports only the `history` domain and returns an unsupported-domain result otherwise;
- Selection Path returns unknown selection reasoning for unrecognized targets;
- post-execution extraction waits for a durable completed event;
- read-model cache publication waits for construction result;
- projection publication waits for finalized state.

This is eligibility, not ownership recovery. The implementation does not say every repository operation has an explicit eligibility object.

### Implementation-local handoffs preserve provenance and compatibility

Supported.

The recurring handoffs usually preserve where evidence came from and avoid public churn:

- durable events preserve execution provenance;
- agreement/evidence contract records preserve supporting evidence references and non-promotion boundaries;
- projection lineage preserves source event and affected projection evidence;
- read-model dependency identity preserves projection version and last event identity;
- compatibility objects and accessors preserve existing answer/report surfaces after private payload extraction;
- bounded ask maps to existing surfaces rather than creating new answering implementations.

## Unsupported architectural interpretations

The implementation evidence does not support concluding that:

- there is a universal dependency framework;
- there is a universal inquiry ontology;
- `subject`, `target`, `domain`, `query`, note identity, and focus are synonyms;
- `dependency` vocabulary should displace responsibility, authority, or eligibility vocabulary;
- there is a planner, workflow engine, orchestration layer, or repository-wide grammar implementation;
- every responsibility is defined primarily by explicit request/result transformation;
- every ordered path is a strict prerequisite chain;
- every downstream responsibility consumes a uniquely named upstream object;
- broad data collection always waits for surface identity;
- unsupported identities should be inferred into supported ones;
- ownership recovery or implementation redesign is justified by these reports.

## Counterexamples and stopping evidence

The reconciliation must stop short of a universal rule because implementation evidence includes limits:

- **Distinct inquiry identities remain distinct.** `question_family`, `subject`, `target`, `domain`, `query`, `note`, `reference`, and `focus` have separate rules and cannot be collapsed into one ontology.
- **Some source composition is parallel, not sequential.** Capability inventory joins admitted facts, executable contract metadata, and requested needs without proving those sources are one ordered pipeline.
- **Some visibility work is report-shaped.** Execution Visibility separates payloads for diagnostic/report compatibility, which is weaker evidence for responsibility eligibility than Projection Influence Lineage or Read-Model Ownership.
- **Some broad audits precede identity-specific filtering.** Reasoning Path builds broad upstream surfaces before filtering by `domain` and `subject`; the supported claim is narrower evidence selection, not all data acquisition.
- **Unsupported identities stop reasoning.** Reference Selection and Selection Path produce unsupported or unknown results rather than inferring missing authority.
- **Shared `State` remains a real input.** Several families consume projected state and existing cache/store behavior rather than a fully externalized dependency chain.

These counterexamples prevent promoting the recurring observation into a universal dependency architecture.

## Frontier boundary

### What current implementation evidence supports

Current evidence supports saying:

```text
Recent investigations have independently recovered a recurring relationship between responsibility, authority, and eligibility.

The recurring relationship is that a bounded responsibility often becomes eligible for its own narrower work only after explicit upstream implementation evidence has been produced, preserved, validated, selected, assessed, constructed, or handed off under another bounded responsibility's authority.

The downstream responsibility consumes that evidence without recreating the upstream work or expanding upstream authority, and many handoffs preserve existing compatibility.
```

### Where the repository must stop

Current evidence requires the repository to stop before claiming:

```text
all repository responsibilities are dependency transformers;
all inquiry identities are one ontology;
dependency vocabulary is stronger than responsibility/authority/eligibility vocabulary;
a planner, framework, grammar, or orchestration layer exists or should exist;
ownership has been recovered;
new implementation behavior is justified.
```

### Final reconciliation answer

Recent investigations have been independently recovering a recurring relationship between responsibility, authority, and eligibility, but only as an implementation-local handoff pattern.

The strongest supported relationship is:

```text
fulfilled upstream responsibility
produces or preserves explicit implementation evidence
under bounded authority

↓

downstream responsibility consumes that evidence
and thereby becomes eligible
for its own bounded work
without inheriting upstream ownership
or breaking compatibility.
```

The evidence is strongest in Projection Influence Lineage, Read-Model Ownership, Operational Responsibility event handoff, bounded ask / inquiry identity surfaces, Answer Composition, and evidence-contract handoffs.

The evidence is weaker where boundaries are report-shaped, source-composition-shaped, or still rely on shared projected `State`.

Therefore, the frontier is architectural observation, not implementation mandate: responsibility-authority-eligibility handoff is a recurring implementation-backed pattern, but it is not a universal framework, ontology, planner, grammar, or ownership recovery.

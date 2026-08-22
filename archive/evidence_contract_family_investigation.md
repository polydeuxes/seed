# Evidence Contract Family Investigation

## Scope

This is a bounded implementation investigation of whether the repository currently
contains a recurring **Evidence Contract** responsibility. It does not implement
ownership recovery, add abstractions, add runtime surfaces, migrate vocabulary, or
change compatibility behavior.

The question is not whether recent family names sound similar. The question is
whether implementation repeatedly preserves bounded evidence handoffs before a
second owner assumes responsibility.

## Implementation evidence reviewed

### Answer Composition

Strong evidence appears in two implemented answer-composition paths.

`seed_runtime/operational_story.py` composes an operator-facing story by first
collecting multiple upstream surfaces, then passing implementation-local payloads
into the public `OperationalStory` result. The local payloads separate answer
material, limitations, reasoning, supporting evidence, and authority boundary:
`_OperationalStoryAnswerPayload`, `_OperationalStoryLimitationsPayload`,
`_OperationalStoryReasoningPayload`, `_OperationalStorySupportingEvidencePayload`,
and `_OperationalStoryBoundaryPayload`. `_compose_operational_story_payloads(...)`
returns those payloads as a tuple before `build_operational_story(...)` maps them
into the public read-only story object.

This is not merely rendering or JSON. The payloads exist before formatting, before
`to_json_dict()`, and before CLI presentation. They preserve which material is the
answer, which material is support, which material is reasoning, which material is
unknown, and which material is the boundary.

`seed_runtime/inquiry_orientation.py` contains a narrower version of the same
pattern. `_collect_architectural_orientation_evidence(...)` returns
`_ArchitecturalOrientationEvidence`; `_compose_architectural_orientation_answer(...)`
then turns that evidence into `_ArchitecturalOrientationAnswer`; only after that
is an `InquiryOrientationView` built and formatted. The local answer object
preserves answer material, reason, support, boundary, and limitations before the
view renderer consumes it.

Evidence-contract interpretation: these modules preserve implementation-local
answer evidence before a downstream view/result owner receives it. The contract is
not a public schema and not a serialization format; it is a local handoff between
collection/composition and publication/rendering.

### Observation-Derived Capability

`seed_runtime/capability_promotion_readiness.py` is explicit about evidence
handoff. `build_capability_promotion_readiness_inspection(...)` builds capability
candidates and verification evidence, groups verification support by candidate,
and then passes both through `_CapabilityVerificationPayload` before calculating
`CapabilityPromotionReadiness`.

The internal payload preserves candidate identity, candidate support, and
verification support before the readiness result is allowed to make a bounded
promotion-readiness claim. The module's boundary text states that this is
read-only inspection and not promotion, fact creation, capability selection,
policy evaluation, tool invocation, or execution.

Evidence-contract interpretation: candidate evidence and verification evidence
are not merged directly into a verified capability. The implementation preserves a
bounded payload that lets the readiness owner decide only whether a future
promotion would be supportable.

### Projection Influence Lineage

`seed_runtime/state.py` contains a dense sequence of implementation-local
handoffs:

- `_ProjectionInfluenceLineage` preserves source event ids, affected scopes, and
affected projections.
- `_ReplayScopeAssessment` consumes lineage and records whether replay is
required.
- `_ReplaySelectionJustification` consumes scope assessment and preserves why the
compatible target set remains full replay plus finalization.
- `_ReplaySelection` consumes the justification and records selected replay
targets.
- `_ReplayExecutionRequest` consumes the selection.
- `_ProjectionPublicationRequest` receives finalized `State`.
- `_ProjectionPublication` publishes that same finalized state as visible state.

This is one of the strongest examples because the dataclasses are private,
identity-preserving, and explicitly bounded away from replay execution, cache
invalidation, persistence, rendering, and read-model semantics. It shows repeated
local evidence transfer across multiple owner boundaries.

Evidence-contract interpretation: the implementation already uses private request,
assessment, justification, selection, and publication records to keep evidence
handoffs explicit while each downstream step owns a narrower decision.

### Read-Model Ownership

`seed_runtime/read_model_ownership.py` contains the most explicit request/result
contract vocabulary in the implementation reviewed. It preserves:

- `ReadModelConstructionInputs`, which carries the same visible `State` object
into read-model builders.
- `ReadModelDependencyIdentity`, which carries projected-state identity evidence.
- `ReadModelCacheLookupRequest` and `ReadModelCacheLookupResult`.
- `ReadModelConstructionRequest` and `ReadModelConstructionResult`.
- `ReadModelCachePublicationRequest` and `ReadModelCachePublicationResult`.

The functions preserve these boundaries in order: visible state becomes
construction inputs; construction inputs plus projection identity become a
dependency identity; the identity becomes a cache lookup request and result; the
construction request invokes the existing builder unchanged; the construction
result becomes a cache publication request and result.

Evidence-contract interpretation: this is very strong implementation evidence for
identity-preserving evidence handoff. The module's purpose is not to change the
public read model; it makes the post-publication handoff into construction and
cache publication explicit without owning downstream semantics.

### Operational Responsibility

`seed_runtime/operational_story.py` contributes evidence beyond answer
composition. The story boundary payload explicitly carries `mode=read_only_view`,
`records_facts=False`, `writes_event_ledger=False`, and `mutates_cluster=False`.
The `OperationalStory` result then exposes that boundary alongside pressure,
supporting evidence, capabilities, constraints, gaps, impact, changes, outcomes,
investigation path, and unknowns.

Evidence-contract interpretation: operational responsibility is not just a view.
It preserves authority limits as implementation-local payload before publishing a
story result. However, it is also a counterexample against overgeneralization: the
story module is domain-specific and does not reuse the read-model request/result
classes or projection lineage classes.

### Execution Visibility

`seed_runtime/execution_status.py` implements renderer-independent status
handoff. `ExecutionStatusEmitter` constructs an `ExecutionStatus` payload and
passes it to an `ExecutionStatusConsumer`. Consumers may ignore, record, or render
it. `ProgressCadence` separately bounds when progress evidence should be emitted,
and `ObservationProducerLifecycle` standardizes lifecycle messages without
creating observations, deriving facts, appending events, or defining observation
semantics.

Evidence-contract interpretation: this is a recurring grammar candidate because
producer and consumer ownership is explicitly separated by a small payload. It is
less strong as Evidence Contract evidence than read-model ownership because the
payload is an operational visibility record rather than a preserved evidence
handoff for a later reasoning or ownership decision.

### Inquiry Orientation

`seed_runtime/inquiry_orientation.py` is strong because it preserves operator prose
as an `InquiryNoteRecord`, computes `RelatedMaterial`, wraps matches in
`_ArchitecturalOrientationEvidence`, composes `_ArchitecturalOrientationAnswer`,
and only then builds `InquiryOrientationView` and `format_inquiry_orientation(...)`.
The authority boundary refuses fact, claim, goal, tool need, requirement,
capability, decision, proposal, plan, authorization, command, runtime instruction,
importance, ownership, intent, concern, recommended action, or next-safe-move
promotion.

Evidence-contract interpretation: the handoff is bounded and identity-preserving:
the raw note remains a note, related material remains related material, and the
answer view receives support and limitations without promoting either to cluster
truth.

### Grammar Observation and Observation Agreement

`seed_runtime/knowledge/observation_agreement.py` provides explicit agreement
records over supplied observations only. `ObservationAgreementEvidence` preserves
stream, provenance, and evidence text; `ObservationAgreementRecord` preserves
participating streams, supporting evidence, provenance, a candidate agreement,
and a non-promotion boundary.

`seed_runtime/knowledge/grammar_observation.py` then consumes only
`ObservationAgreementRecord` values. It emits `GrammarObservationRecord` values
that preserve observed relation shape, supporting agreements, provenance,
recurrence evidence, and a non-promotion boundary. It explicitly avoids raw
Markdown, Python, runtime state, repositories, CLI, JSON, schema, diagnostics,
events, ledger writes, runtime mutation, repository mutation, and cluster
mutation.

Evidence-contract interpretation: this is a clean Owner A → evidence record →
Owner B handoff. Observation Agreement owns candidate agreement between already
observed streams; Grammar Observation owns recurring relation-shape observation
over agreement records. It is strong evidence for an implementation grammar, but
it is intentionally new and narrow.

## Recurring implementation patterns

Across the reviewed code, a recurring implementation grammar does appear. It is
not a single shared class or named abstraction, but it has repeated traits:

1. **Implementation-local payloads before public results.** Examples include
   `_OperationalStory*Payload`, `_ArchitecturalOrientationEvidence`,
   `_ArchitecturalOrientationAnswer`, `_CapabilityVerificationPayload`, and the
   private projection lineage records.

2. **Request/result pairs at ownership boundaries.** Read-model ownership uses
   request/result pairs for cache lookup, construction, and cache publication.
   Projection publication uses request/publication pairs. Runtime retry handling
   uses structured retry prompt payloads, although those are closer to operational
   compatibility than evidence contracts.

3. **Identity preservation.** Read-model construction inputs preserve the same
   visible `State` object. Projection publication publishes the finalized state as
   visible state. Inquiry orientation preserves the inquiry note as operator prose.
   Observation Agreement preserves original stream and provenance evidence.

4. **Bounded evidence transfer before promotion-like decisions.** Capability
   promotion readiness carries candidate support plus verification support before
   emitting readiness, without creating `capability_verified` facts. Grammar
   Observation carries agreements before emitting recurring shape observations,
   without promoting grammar truth.

5. **Authority boundaries travel with handoffs.** Operational Story, Inquiry
   Orientation, Observation Agreement, Grammar Observation, and Capability
   Promotion Readiness all carry explicit non-promotion or read-only boundary
   material.

6. **Adapters preserve compatibility.** Several modules wrap existing behavior
   rather than replacing it: read-model builders are invoked unchanged through
   `construct_read_model(...)`; projection publication publishes finalized state
   unchanged; operational story maps local payloads into the existing story result;
   inquiry orientation composes local evidence before building the existing view.

7. **Evidence contracts are distinguishable from serialization.** The strongest
   records are consumed by Python functions before formatting, JSON conversion,
   CLI rendering, or event ledger writes.

## Counterexamples and limits

The implementation evidence is real, but it is not yet uniform enough to justify
assuming a completed or immediately recoverable Evidence Contract family.

1. **Mechanisms are family-local.** Read-model ownership has public-ish dataclasses
   and request/result pairs. Projection influence lineage uses private dataclasses.
   Operational Story uses private payload splits. Observation Agreement and
   Grammar Observation use knowledge records. Execution Visibility uses emitter
   and consumer protocols. These are related shapes, not one implemented shared
   mechanism.

2. **Some similarities are vocabulary-level.** Terms such as answer, reason,
   support, evidence, verification, promotion, publication, and observation recur,
   but recurrence of words is not sufficient. Only the modules with actual
   payload/request/result handoffs count as implementation evidence.

3. **Public schema, JSON, CLI, and rendering are not evidence contracts by
   themselves.** `OperationalStory.to_json_dict()`, `format_operational_story(...)`,
   `format_inquiry_orientation(...)`, CLI consumers, and event payloads may expose
   or render preserved evidence, but they are not the implementation-local handoff
   itself.

4. **Execution Visibility is adjacent but weaker.** `ExecutionStatus` is a bounded
   producer/consumer payload, but it primarily carries transient operator status,
   not evidence required for a later ownership decision.

5. **Runtime retry prompts are compatibility payloads, not necessarily evidence
   contracts.** Runtime preserves parse/validation/intent errors in retry prompts,
   but those structures serve model retry compatibility. They should not be
   promoted into Evidence Contract evidence without a narrower follow-up audit.

6. **No implementation currently names or owns a cross-cutting Evidence Contract
   responsibility.** The recurring grammar is emergent. There is no central module,
   diagnostic, inventory, audit, or tests that characterize Evidence Contract as a
   repository responsibility family.

7. **A candidate family would cut across many completed families.** Recovering it
   prematurely could create an abstraction above local owners and violate the
   current repository pattern of small implementation-backed recovery.

## Supported conclusions

### 1. Does the repository currently exhibit a recurring Evidence Contract implementation grammar?

Yes, with qualifications. The repository repeatedly preserves bounded,
implementation-local handoffs between owners using payloads, request/result
records, provenance records, non-promotion boundaries, and identity-preserving
wrappers. The strongest evidence is not shared vocabulary; it is executable code
that passes local records from one responsibility step to another before
publishing, rendering, promoting, or executing.

### 2. Where is the strongest implementation evidence?

The strongest evidence is in three areas:

1. **Read-Model Ownership**: explicit construction inputs, dependency identity,
   cache lookup request/result, construction request/result, and cache publication
   request/result form a repeated request/result handoff chain.
2. **Projection Influence Lineage**: private lineage, scope assessment,
   selection justification, selection, execution request, publication request, and
   publication records form a multi-step evidence-to-owner chain.
3. **Observation Agreement → Grammar Observation**: agreement records preserve
   streams, provenance, support, candidate agreement, and non-promotion boundary;
   grammar observations consume only those records and preserve recurrence without
   raw substrate access or truth promotion.

Operational Story, Inquiry Orientation, and Capability Promotion Readiness provide
additional strong supporting examples, especially because their payloads preserve
support, limitations, boundary, and readiness evidence before result publication.

### 3. Which recurring implementation characteristics appear across completed families?

Recurring characteristics include:

- local dataclasses used as bounded handoff records;
- preservation of identity or provenance across owner transitions;
- request/result vocabulary around construction, lookup, publication, execution,
  or readiness decisions;
- payloads that separate answer, reason, support, limitations, and authority;
- explicit refusal to promote evidence into facts, truth, grammar, capability,
  execution authority, cache policy, or cluster mutation;
- adapters that wrap existing behavior without changing downstream semantics;
- consumption of already-derived inputs rather than raw substrate parsing by the
  downstream owner.

### 4. Which similarities are merely superficial?

The following are superficial unless tied to implementation-local handoff code:

- recurring words such as evidence, support, verification, promotion,
  publication, answer, reason, or observation;
- public JSON shape or CLI section similarity;
- event ledger payload similarity;
- renderer output structure;
- documentation diagrams that show arrows between concepts;
- the fact that multiple modules are read-only;
- the fact that multiple modules include boundary text.

The implementation evidence matters only where a bounded record is produced by
one owner and consumed by another owner while preserving identity, provenance,
support, or authority limits.

### 5. Is there sufficient implementation evidence to begin an Evidence Contract responsibility family?

Yes, but only as a bounded investigation/recovery candidate, not as an immediate
abstraction or broad ownership migration.

There is sufficient evidence to begin by characterizing a narrow Evidence Contract
family because the grammar recurs across independent implementation areas:
read-model ownership, projection lineage, observation agreement/grammar
observation, inquiry orientation, operational story, and capability promotion
readiness. The repository has naturally evolved repeated Owner A → bounded
payload/request/result/evidence record → Owner B handoffs.

However, there is not sufficient evidence to implement a shared Evidence Contract
abstraction now. The mechanisms remain deliberately family-local, and repository
authority currently supports characterization more strongly than generalization.

## Unsupported conclusions

The investigation does not support these conclusions:

- Evidence Contract is already a completed responsibility family.
- A new shared base class, wrapper, protocol, schema, CLI surface, diagnostic, or
  runtime surface should be added now.
- Existing payloads should be renamed to Evidence Contract vocabulary.
- Public JSON, event payloads, or rendered CLI output are themselves Evidence
  Contracts.
- Execution Visibility alone proves the family.
- Similar names across completed families prove implementation ownership.
- Grammar Observation, Observation Agreement, Read-Model Ownership, Projection
  Influence Lineage, or Operational Story should be refactored to share one
  evidence-contract implementation.

## Confidence

Confidence is **medium-high** that a recurring Evidence Contract implementation
grammar exists.

Confidence is **medium** that it is mature enough to begin a bounded
responsibility-family recovery investigation.

Confidence is **low** that it is mature enough for implementation recovery,
abstraction, shared types, or compatibility changes now.

The confidence split matters: the implementation evidence is repeated and strong,
but the mechanisms remain intentionally local and heterogeneous.

## Recommended next action

Begin a bounded **Evidence Contract responsibility family investigation slice**,
not implementation recovery.

The next slice should:

1. choose one already-implemented handoff chain as the primary specimen, preferably
   Read-Model Ownership or Projection Influence Lineage;
2. compare it against Observation Agreement → Grammar Observation and Capability
   Promotion Readiness;
3. characterize the minimum implementation traits that make a handoff an evidence
   contract;
4. explicitly exclude public schemas, JSON, events, CLI rendering, and generic
   read-only boundaries;
5. stop before adding shared types, wrappers, diagnostics, runtime surfaces, or
   vocabulary migrations.

If a future implementation slice is ever considered, the missing evidence to look
for is not more terminology. The missing evidence is a recurring need for one
owner to consume another owner's bounded handoff through a stable adapter in at
least two independent code paths where local duplication is causing concrete
maintenance pressure.

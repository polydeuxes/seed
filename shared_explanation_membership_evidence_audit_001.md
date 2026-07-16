# Shared Explanation Membership Evidence Audit 001

## Bounded audit question

Given one bounded inquiry and several already-produced `SharedExplanationRenderingProjection` records, what constitutional evidence establishes that each projection belongs, does not belong, remains Unknown, or conflicts with that inquiry?

This audit performs exactly one bounded Shared Explanation Membership Evidence Audit. It does not implement membership selection, sequence explanations, compose explanations, rank blockers, deduplicate by meaning, invent missing projections, authorize movement, observe, emit, execute, write events, or mutate cluster state. Repository authority wins.

## Reviewed evidence

Implementation and test evidence reviewed:

- `seed_runtime/bounded_constitutional_question.py` and `tests/test_bounded_constitutional_question.py` for bounded inquiry identity, explicit caller-supplied fields, testimony treatment, read-only boundaries, and non-selection boundaries.
- `seed_runtime/constitutional_view_selection.py` and `tests/test_constitutional_view_selection.py` for deterministic projection from bounded question identity and exact selection keys without raw-question consumption or semantic reasoning.
- `seed_runtime/operator_authority_scope_binding.py` and `tests/test_operator_authority_scope_binding.py` for ingress demand/request identity, authority/scope binding references, source explanation identity, Unknown preservation, and conflict preservation.
- `seed_runtime/representation_grammar_applicability.py` and `tests/test_representation_grammar_applicability.py` for exact demand, probe request, handoff, recovered grammar, mechanism, invocation contract, provenance, Unknowns, conflicts, and stage-local explanation preservation.
- `seed_runtime/shared_explanation_rendering_projection.py` and `tests/test_shared_explanation_rendering_projection.py` for one-to-one rendering of stage-local explanations, source explanation identity, source artifact owner/type, stage-owned material, Unknowns, conflicts, and the explicit single-explanation boundary.
- `seed_runtime/capability_reachability_projection.py` and `tests/test_capability_reachability_projection.py` for demand-level reachability identity, probe/capability-demand/candidate-set handoff validation, positive unsupportedness, no-known-realization Unknown treatment, conflict preservation, and no selection among multiple support.
- `seed_runtime/reasoning_path_audit.py` and `tests/test_reasoning_path_audit.py` for read-only derivation-path evidence, consumers, story impact, typed Unknown preservation when no derivation evidence exists, and non-mutation boundaries.
- `seed_runtime/selection_path_audit.py` and `tests/test_selection_path_audit.py` for candidate-set, selection-factor, non-selected, evidence, outcome, and Unknown preservation without treating unsupported target evidence as a selected result.
- `explanation_selection_sequencing_composition_topology_audit_001.md` for the recovered topology that membership selection, constitutional lineage preservation, operator encounter sequencing, and composition are independent responsibilities.
- `shared_explanation_rendering_projection_slice_001.md` and `shared_explanation_presentation_contract_audit_001.md` for the current shared rendering projection boundary and stage-local explanation ownership.

## Current implementation anchor

`SharedExplanationRenderingProjection` is a rendering projection for exactly one already-produced stage-local explanation. It preserves:

- `source_explanation_identity`;
- `source_artifact_owner`;
- `source_explanation_type`;
- `attempted_movement`;
- `source_state` and `source_reason` as display labels;
- `preserved_unknowns` and `preserved_conflicts`;
- `prohibited_downstream_movement`;
- `explanation_boundary`;
- opaque `stage_owned_material`;
- read-only, event-ledger, and cluster-mutation boundaries.

Its own boundary says it consumes exactly one already-produced stage-local explanation and does not compare, aggregate, order, or compose explanations. Its rendering boundary says shared field names are display labels only and constitutional meaning remains authored and owned by the source stage.

Therefore membership is not established by the shared projection itself. Membership must be evaluated per candidate against one explicit bounded inquiry by inspecting preserved source explanation and source artifact references, plus any stage-owned handoff, demand, inquiry, provenance, or derivation references available from the source lineage.

## Minimum constitutional evidence for membership

For one candidate projection and one explicit bounded inquiry, the minimum lawful evidence is one of the following, inspected without sequencing or composition:

1. **Direct inquiry identity match.** The candidate's preserved source explanation, source artifact, handoff, provenance, or stage-owned material carries the same explicit bounded inquiry reference as the inquiry under consideration.
2. **Lawful handoff lineage to the bounded inquiry.** The candidate's source artifact is produced from a handoff whose preserved references lawfully descend from the bounded inquiry's source request, inquiry identity, bounded question identity, demand, work identity, or probe/request identity.
3. **Exact demand/work identity connected to the inquiry.** The candidate's source demand, capability demand, probe request, candidate set, or work identity is positively connected to the bounded inquiry through preserved provenance or handoff references.
4. **Source artifact identity connected to a known stage result for the inquiry.** The projection preserves a source explanation identity whose source artifact reference is already known, through implementation evidence, to be a stage-local result for the bounded inquiry.

These are positive membership evidence. State labels, wording, stage name, display order, timestamps, registry order, lexical similarity, severity, or immediate blocker status are not membership evidence.

## Per-candidate inspection discipline

Each candidate must be answered independently before comparing the set:

- bounded inquiry under consideration: the explicit inquiry or bounded-question identity supplied to the audit/selection responsibility;
- source explanation: `source_explanation_identity` plus `source_explanation_type`;
- source artifact: source explanation's preserved `source_artifact_ref` and `source_artifact_type`, when available from the source explanation or stage-owned/source lineage;
- preserved references: inquiry, demand, work, handoff, probe, recovery, grammar, mechanism, contract, candidate-set, provenance, reasoning-path, or selection-path references;
- positive membership evidence: direct or handoff/provenance/demand lineage to the bounded inquiry;
- positive non-membership evidence: direct or lineage evidence tying the candidate to a different incompatible bounded inquiry or exact demand;
- missing evidence: absent inquiry, demand, handoff, source artifact, or provenance references needed for either membership or non-membership;
- conflicting references: preserved references tying the same projection to incompatible inquiries, demands, handoffs, or source artifacts;
- Unknowns remaining: unresolved evidence gaps that prevent both belonging and not-belonging conclusions;
- `membership != sequencing`;
- `relevance != same state, same stage, same wording, or display position`;
- `duplicate identity != authority to deduplicate`.

## Independently inspected proving cases

### 1. Same inquiry, different stages

Candidate stages:

```text
ingress explanation
grammar-applicability explanation
reachability explanation
```

Inspection result: all may belong to one bounded inquiry when their source lineage refers to the same bounded inquiry, exact demand, handoff chain, probe/work identity, or provenance chain.

Ingress evidence can include authority/scope binding material carrying interpretation, expression, operator, workspace, session, request kind, activity class, permitted/excluded/unresolved scope, authority sources, provenance, Unknowns, and conflicts. The ingress explanation preserves the source binding projection identity as its source artifact reference.

Grammar-applicability evidence can include exact `capability_demand_ref`, `probe_request_ref`, `operational_realization_handoff_ref`, recovered grammar, mechanism, invocation contract, provenance, Unknowns, and conflicts. Its explanation preserves the applicability projection identity and stage-owned demand/material references.

Reachability evidence can include exact `probe_request_reference`, `capability_demand_reference`, `candidate_set_reference`, future handoff reference, supporting/blocked/unsupported/unknown/conflicting candidate references, provenance, Unknowns, and conflicts.

Membership conclusion: if those references lawfully connect to the same bounded inquiry, all three belong. The immediate blocker is not the only relevant explanation. Membership does not choose constitutional order, operator encounter order, or composition.

### 2. Same stage, different inquiry

Two projections may share `source_explanation_type`, `source_artifact_owner`, `source_state`, or stage-owned field names while arising from different bounded inquiries or exact demands.

Inspection result: shared source type or state is insufficient. Positive non-membership exists only when preserved inquiry/demand/handoff/provenance evidence ties the candidate to another incompatible bounded inquiry. Without such positive evidence, the candidate is not automatically unrelated; it remains Unknown for this inquiry.

### 3. Matching demand

A projection belongs when its source demand, handoff, or derivation lineage is lawfully connected to the bounded inquiry.

Implementation evidence supports this treatment because representation grammar applicability validates exact handoff source and target representations, exact probe/demand material provenance when present, mechanism/contract compatibility, and then carries `capability_demand_ref`, `probe_request_ref`, handoff, and provenance. Capability reachability validates candidate-set and future-handoff identity for probe request and capability demand, and refuses mismatched probe or demand references.

Membership conclusion: a matching exact demand connected through preserved handoff/provenance to the bounded inquiry is positive membership evidence. A matching phrase without the preserved connection is only presentation similarity and remains insufficient.

### 4. Missing inquiry reference

If a candidate projection lacks sufficient inquiry, demand, handoff, derivation, source artifact, or provenance evidence to connect it to the bounded inquiry, the lawful classification is **Unknown**, not non-member.

Repository precedent: bounded question production preserves unknowns without promoting testimony into fact; reachability treats no known realization as Unknown rather than impossible or unsupported; reasoning-path audit preserves typed Unknowns when no derivation evidence is available.

Membership conclusion: missing evidence is an evidence gap. It does not establish unrelatedness.

### 5. Conflicting references

If preserved references connect one projection to incompatible inquiries, incompatible exact demands, incompatible handoffs, or incompatible source artifacts, the lawful classification is **conflict**.

Repository precedent: ingress binding produces `conflict` when authority/scope or constraints conflict and preserves conflict references; grammar applicability produces `conflict` when preserved applicability evidence supports incompatible conclusions; reachability produces `conflict` when candidate conclusions cannot be reconciled lawfully.

Membership conclusion: conflict is preserved. The audit must not choose through ordering, timestamp, source preference, stage preference, severity, or display position.

### 6. Duplicate source identity

If two rendering projections preserve exact duplicate `source_explanation_identity` and source artifact identity, the duplicate identity remains visible.

Membership conclusion: duplicate source identity may establish that both records refer to the same source explanation, but it does not authorize deduplication. Deduplication policy is not part of this audit.

### 7. Missing expected stage

If a stage was expected but no projection exists, the audit must not invent a projection or a membership record.

Membership conclusion: absent expected stage is not an existing stage result. It may be an Unknown or a missing-stage gap only if a future bounded view contract requires that stage and has a lawful Unknown channel. This audit does not implement that contract.

### 8. Unrelated projection

A projection with positive evidence tying it to another bounded inquiry or another exact incompatible demand does not belong to the inquiry under consideration, even if its state, wording, stage, or source type appears relevant.

Membership conclusion: positive non-membership requires affirmative incompatible inquiry/demand/handoff/provenance evidence. Shared vocabulary is never enough.

## Recurring membership evidence

Recurring evidence across inspected implementation surfaces:

- stable bounded inquiry identity: `bounded_question_id`, explicit inquiry provenance, caller-supplied fields, and bounded question contents;
- inquiry/request/work lineage: attributed expression, interpretation projection, authority/scope binding, workspace/session/scope references, and provenance;
- exact demand identity: `capability_demand_ref` or `capability_demand_reference`;
- handoff identity: operational realization handoff, future candidate-realization handoff, future capability-reachability handoff, and future selection handoff;
- source explanation identity: `source_explanation_identity` and source explanation `explanation_id`;
- source artifact identity: source explanation `source_artifact_ref` and `source_artifact_type` where source artifact is available;
- source artifact owner/type: source stage owner and explanation type;
- derivation/provenance lineage: recovery projection, recovered grammar, probe request, invocation contract, candidate set, shared provenance, reasoning-path consumers, and selected evidence;
- Unknowns and conflicts preserved as first-class evidence states rather than silently resolved.

## Inquiry-reference treatment

Direct inquiry identity is strongest when present. `BoundedConstitutionalQuestion` is deterministic from explicit caller inputs and may preserve an explicit caller-supplied identifier. It does not create facts, authority, capability, view selection, or QuestionProjection by itself.

Therefore, membership may use direct bounded inquiry identity only when a candidate's preserved lineage carries that identity or an explicitly connected reference. A raw wording match to the operator inquiry is not enough, because testimony is preserved as evidence rather than established fact.

## Demand-reference treatment

Demand references can establish membership when the demand is exact and lawfully connected to the bounded inquiry through handoff or provenance. Demand references can establish non-membership when they positively identify an incompatible demand or another inquiry's demand. A demand label without connection to bounded inquiry identity is incomplete evidence and remains Unknown.

The reachability tests reinforce that different demand strings can produce distinct demand references and distinct conclusions; there is no global competency or global state inference from shared mechanism vocabulary.

## Handoff and derivation-lineage treatment

Handoff references are strong membership evidence when they preserve the path from bounded inquiry/request to stage result. The audit may inspect handoff references, but it must not produce new handoffs or infer missing links.

Reasoning-path and selection-path lineage may support membership when they identify consumers, evidence, candidates, non-selected items, or Unknowns connected to the bounded inquiry. They do not authorize state comparison, rank, sequence, or composition.

## Source explanation and source artifact treatment

`source_explanation_identity` is necessary for auditability but not alone sufficient for bounded inquiry membership unless the source explanation or its source artifact is known to be connected to the inquiry.

`source_artifact_owner` and `source_explanation_type` show ownership and stage type. They do not establish inquiry membership by themselves. `stage_owned_material` may contain demand, provenance, known loss, handoff boundary, or other stage-specific references that support membership, but those fields remain owned by the stage and must not be normalized into a universal relevance model.

## Positive membership findings

A candidate belongs when at least one lawful positive connection exists and no preserved incompatible connection conflicts:

- same explicit bounded inquiry reference;
- source artifact/handoff provenance chain descends from the bounded inquiry;
- exact demand/work/probe identity is connected to the bounded inquiry;
- source explanation identity points to a stage-local result known to be produced for the bounded inquiry;
- derivation or selection-path evidence ties the candidate's source artifact to the bounded inquiry without semantic inference.

## Positive non-membership findings

A candidate does not belong when positive preserved evidence ties it to another incompatible inquiry, exact demand, handoff, work/probe identity, or source artifact lineage.

Non-membership is not established by:

- same state with different wording;
- same stage with different evidence gaps;
- same source type;
- same reason label;
- same display vocabulary;
- absence of membership evidence;
- expected-stage absence.

## Unknown and conflict treatment

Unknown treatment:

- missing inquiry reference remains Unknown;
- missing handoff or provenance link remains Unknown;
- missing exact demand/work connection remains Unknown;
- no known stage result remains Unknown or omitted according to future contract, not invented;
- Unknowns preserved by source stages remain attached to those stages.

Conflict treatment:

- incompatible inquiry references remain conflict;
- incompatible exact demand references remain conflict;
- incompatible handoff/source artifact references remain conflict;
- conflict references are preserved without choosing through timestamp, source order, source preference, display order, severity, or registry order.

## Duplicate and missing-stage treatment

Duplicate treatment:

- exact duplicate source explanation identity remains visible;
- exact duplicate source artifact identity remains visible;
- duplicate identity is not authority to deduplicate;
- duplicate records may each receive the same per-candidate membership answer, plus a duplicate-identity note, if a future implementation chooses to expose such a note.

Missing-stage treatment:

- expected stage is not existing stage result;
- missing expected stage does not create a projection;
- missing expected stage does not establish non-membership for existing projections;
- any missing-stage Unknown requires a future bounded view contract and must not be invented by this audit.

## Whether membership is projected per candidate or for the set

Membership must be projected per candidate. The set may then preserve the collection of per-candidate answers, but the set must not erase individual source explanation identities, collapse duplicates, choose one immediate blocker, or classify membership by overall relevance.

Per-candidate answers are the minimum lawful shape:

```text
candidate projection -> belongs | does_not_belong | unknown | conflict
```

Each answer requires supporting evidence, missing evidence, conflict references, and duplicate-source visibility where applicable.

## Strongest supporting evidence

The strongest supporting evidence is the current shared rendering projection boundary: it consumes exactly one already-produced explanation and refuses comparison, aggregation, ordering, and composition. That requires membership to be external to the shared projection and evaluated per candidate.

The second strongest supporting evidence is the repository's repeated use of exact identity and handoff validation: bounded question identity is deterministic from explicit inputs; constitutional view selection consumes projected bounded-question identity and exact selection keys; grammar applicability validates exact handoff/probe/demand/contract references; reachability validates exact candidate-set/probe/demand handoff references.

The third strongest supporting evidence is Unknown/conflict discipline: absence produces Unknown in bounded question, reasoning-path, and reachability precedent; positive incompatibility or preserved conflicting references produce conflict rather than ordered choice.

## Strongest counterevidence

The strongest counterevidence is that some projections preserve only display-level fields after rendering, and current `SharedExplanationRenderingProjection` does not expose a direct bounded inquiry field. This means a future membership implementation may need source explanation/source artifact lookup or an explicit membership evidence input rather than relying solely on the shared rendering record.

The second counterevidence is that `stage_owned_material` differs by source stage. It can contain useful demand or provenance references for grammar applicability, but ingress explanations currently expose less source provenance at the shared-rendering layer. That weakens any one-size-fits-all evidence shape.

The third counterevidence is that existing selection surfaces already select views or pressure targets for their own domains. Those are bounded implementations, not authority for a universal explanation relevance manager or blocker-ranking system.

## Exact current compressions

Current bounded-question compressions:

- bounded inquiry identity is a deterministic `bounded_question_id` over explicit inputs unless caller supplies an id;
- operator inquiry is testimony preserved as evidence, not established fact;
- caller-supplied fields may carry exact selection keys but are not semantic interpretation;
- Unknowns and uncertainty are preserved;
- no selection or view production occurs during bounded-question production.

Current shared-rendering compressions:

- one source explanation becomes one rendering projection;
- source explanation identity, owner, type, state, reason, Unknowns, conflicts, downstream prohibitions, explanation boundary, and stage-owned material are copied;
- source artifact reference is not a top-level shared-rendering field, so it must be recovered from the source explanation/source stage when needed;
- stage-owned material remains opaque and source-authored;
- no membership, sequencing, composition, or deduplication field exists.

Current ingress explanation compressions:

- source binding projection identity is preserved in source explanation artifact data;
- established evidence is compressed into one string;
- first missing boundary and reconsideration transition are strings;
- Unknowns and conflicts are preserved;
- source provenance is stronger in the binding projection and future handoff than in the rendered explanation.

Current grammar-applicability explanation compressions:

- examined grammar, demand, mechanism, and contract are explicit stage-owned fields;
- established applicability evidence is a tuple of standing strings;
- known loss and provenance are preserved;
- source artifact reference points to the applicability projection;
- future handoff exists only when applicable and is not emitted by the explanation.

Current reachability compressions:

- exact probe, demand, candidate set, and future handoff references are top-level projection fields;
- supporting, blocked, unsupported, unknown, and conflicting candidates are separate references;
- no known realization is Unknown, not impossible;
- multiple supported realizations establish no preference;
- reachability does not select realization.

## Whether one implementation slice is warranted

Yes, one narrow implementation slice is warranted after this audit, but only for membership evidence projection. It should be bounded to per-candidate membership evidence for one explicit bounded inquiry and several already-produced rendering projections. It should not implement sequencing, composition, blocker ranking, semantic relevance, deduplication policy, missing-stage invention, authorization, observation, emission, or execution.

The slice is warranted because the current topology audit identified membership as independent and unimplemented, and this audit identifies the minimum evidence required to make per-candidate belonging/non-belonging/Unknown/conflict answers lawful.

## Exact next bounded question

Given one explicit bounded inquiry reference and several already-produced `SharedExplanationRenderingProjection` records, what smallest read-only per-candidate membership evidence projection can preserve `belongs`, `does_not_belong`, `unknown`, or `conflict` with supporting inquiry/demand/handoff/source/provenance references, missing evidence, conflict references, duplicate source identity visibility, and read-only/non-mutation boundaries without sequencing, composing, deduplicating, ranking, or semantic relevance inference?

## Preserved Unknowns

- No implemented multi-explanation membership evidence projection exists yet.
- No current top-level field on `SharedExplanationRenderingProjection` directly carries `bounded_question_id`.
- Source artifact references may require source explanation/source-stage lookup rather than shared-rendering-only inspection.
- Ingress explanations preserve less provenance at the explanation-rendering layer than grammar-applicability explanations preserve in `stage_owned_material`.
- The future data shape for duplicate-source visibility is not implemented.
- The future data shape for missing expected stage Unknowns is not implemented.
- No repository evidence authorizes a universal view registry, explanation relevance manager, blocker ranking system, severity selector, conversation planner, or global composition manager.

## Confidence

Confidence: high that membership is independent from sequencing and composition; high that positive inquiry/demand/handoff/provenance/source lineage is required; high that same state, same stage, same wording, display order, or immediate blocker status is insufficient; high that missing evidence remains Unknown and conflicting preserved references remain conflict; medium that one implementation slice is now warranted because exact future data shape still requires implementation evidence.

## Final answer

For one bounded inquiry,

what constitutionally
establishes that an explanation
rendering projection belongs?

Positive preserved identity or lineage evidence: the projection's source explanation, source artifact, demand, handoff, derivation path, provenance, or exact bounded inquiry reference must lawfully connect that candidate to the explicit bounded inquiry under consideration, with no preserved incompatible inquiry or demand conflict.

Shared state, shared stage, shared wording, display order, timestamp, immediate blocker status, or expected-stage assumptions do not establish belonging. Missing evidence remains Unknown. Incompatible preserved references remain conflict. Duplicate source identity remains visible without authorizing deduplication.

Shared explanation membership evidence audit complete.

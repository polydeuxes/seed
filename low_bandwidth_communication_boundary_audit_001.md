# Low-Bandwidth Communication Boundary Audit 001

## Bounded audit question

Where does Seed currently preserve the complete bounded explanation, where does it choose one communicable turn, and where does it bind a new operator utterance to already-communicated material in a low-bandwidth conversation such as voice?

This audit does not implement composition, speech recognition, speech synthesis, conversation planning, or transport. Repository implementation remains authoritative over presentation vocabulary.

## Evidence inspected

Implementation and repository evidence inspected:

- `seed_runtime/shared_explanation_rendering_projection.py`
- `seed_runtime/shared_explanation_membership_evidence_projection.py`
- `seed_runtime/shared_explanation_membership_evidence_set.py`
- `seed_runtime/shared_explanation_presentation_admission.py`
- `seed_runtime/shared_explanation_encounter_sequencing.py`
- `seed_runtime/operator_expression_interpretation.py`
- `seed_runtime/operator_authority_scope_binding.py`
- `shared_explanation_bounded_composition_topology_audit_001.md`
- `explanation_selection_sequencing_composition_topology_audit_001.md`
- `shared_explanation_encounter_sequencing_topology_audit_001.md`
- `shared_explanation_membership_evidence_audit_001.md`
- `shared_explanation_presentation_contract_audit_001.md`
- `docs/presentation_conversation_responsibility_reconciliation.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/continuation_context_and_working_state_reconciliation.md`
- `docs/operator_clarification_competency_assessment_audit.md`

## Boundary preservation statements

This audit preserves the requested distinctions:

```text
composition
!= one spoken turn
```

```text
one spoken turn
!= the whole inquiry
```

```text
communicated subset
!= discarded explanation content
```

```text
conversation continuity
!= reinterpretation of prior meaning
```

## Current shared-explanation chain

The implementation-backed shared-explanation path currently separates several responsibilities:

```text
stage-local explanation
-> SharedExplanationRenderingProjection
-> SharedExplanationMembershipEvidenceProjection
-> SharedExplanationMembershipEvidenceSet
-> SharedExplanationPresentationAdmission
-> SharedExplanationEncounterSequencing
-> missing bounded composition owner
-> missing communicable-turn projection owner
-> missing conversation-reference binding owner
```

The implemented chain already proves that explanation projection, membership, presentation admission, and encounter sequencing are separate boundaries. It does not yet prove that Seed owns a completed composed explanation view, a low-bandwidth turn window, or a conversation-local reference resolver.

## 1. Where the complete bounded explanation is preserved

### Existing preservation before final composition

Seed currently preserves pieces of the complete bounded explanation across source-owned explanation artifacts and shared-explanation projection artifacts.

`SharedExplanationRenderingProjection` preserves one already-produced stage-local explanation, including source explanation identity, source artifact owner, source explanation type, producer, attempted movement, source state and reason, Unknowns, conflicts, prohibited downstream movement, explanation boundary, stage-owned material, and read-only/non-mutation flags. Its own boundary is explicitly single-explanation: it does not compare, aggregate, order, or compose explanations.

`SharedExplanationMembershipEvidenceSet` preserves the supplied collection of membership evidence for one bounded inquiry and one bounded demand. It partitions supplied results into `belongs`, `does_not_belong`, `unknown`, and `conflict`, preserves duplicate identity occurrences, and states that it does not select, rank, sequence, compose, deduplicate, infer semantic relevance, fabricate missing Unknowns, create handoffs, authorize, execute, write events, or mutate.

`SharedExplanationPresentationAdmission` admits already-belonging membership results into one requested presentation boundary. It preserves belonging-but-unadmitted, non-member, Unknown, conflict, and duplicate surfaces separately. It intentionally stops before first encounter order, ranking, view composition, membership reinterpretation, authorization, execution, event writing, or mutation.

`SharedExplanationEncounterSequencing` preserves presentation-local encounter order for admitted projections and separately preserves constitutional derivation projection refs. It also preserves unsequenced admitted refs, belonging-but-unadmitted results, non-member results, Unknowns, conflicts, and duplicates. Its boundary states that sequencing is not composition, constitutional ranking, deduplication, membership, admission, authorization, execution, event writing, or mutation.

### Missing preservation as one complete bounded explanation

The repository already audited the post-sequencing gap: no existing composition owner lawfully consumes one completed `SharedExplanationEncounterSequencing` and preserves it as one operator-facing shared-explanation view. The recommended missing owner was `SharedExplanationBoundedComposition`, a read-only artifact consuming exactly one completed sequencing artifact and preserving sequenced order, constitutional derivation order, unsequenced admitted projections, and unresolved visibility obligations.

Therefore, the complete explanation is not currently preserved in one implemented low-bandwidth-ready composition artifact. Its source material is preserved across the upstream chain, and the repository already identifies a missing bounded composition owner after encounter sequencing.

## 2. Where one communicable turn is selected

No implemented owner currently selects one low-bandwidth communicable turn from a complete explanation.

Existing presentation work supports a narrower responsibility: presentation can own human encounter order for already implementation-backed answers. The presentation reconciliation states that presentation owns conversational ordering of existing implementation-backed answers for human operators, and that it conducts the encounter, not the reasoning. This supports ordering and grouping, not turn-budget selection.

`SharedExplanationEncounterSequencing` is also not turn selection. It assigns encounter positions and optional roles for admitted projection refs from explicit presentation-local evidence. It does not decide how much content fits into one spoken turn, does not maintain a remaining-content cursor, does not adapt to voice bandwidth, and does not project a subset while preserving the rest as pending.

A low-bandwidth communicable-turn selector would need a distinct responsibility after bounded composition. It would consume a complete composed explanation, a communication budget or mode, and conversation state, then produce one communicable subset while preserving references to omitted/pending explanation content. That owner is not implemented.

## 3. Where references such as “why?”, “go back,” or “just tell me the answer” are bound

### Existing operator utterance interpretation

`operator_expression_interpretation.py` contains the closest existing ingress boundary for operator language. It preserves exact operator material in `AttributedOperatorExpression`, normalizes it separately, interprets one attributed expression under one recovered grammar, preserves source spans, unresolved references, alternatives, unsupported residual spans, Unknowns, conflicts, and a future authority/scope binding handoff.

The current grammar can interpret forms such as `why <focus>`, `what supports <focus>`, `what is unknown about <focus>`, `what prevents <focus>`, `show <focus>`, `what owns <focus>`, and `what is <focus>`. It also marks unresolved bare references, unsupported multi-clause structures, ambiguous ownership, and unsupported residual spans.

This means Seed already has a bounded operator-expression interpretation responsibility for one explicit utterance, including some support for explanation-oriented expressions such as `why X` when the focus is present.

### Existing authority/scope binding after interpretation

`operator_authority_scope_binding.py` consumes an interpreted operator expression and binds it to operator identity, workspace/session authority, and scope context. It can produce a future bounded constitutional question handoff when permitted. It preserves that ingress authority does not establish mechanism availability, capability reachability, selection, warrant, or execution.

This is authority/scope binding, not conversation-reference binding.

### Missing conversation-continuity binding

References such as:

```text
why?
go back
just tell me the answer
```

are not currently bound to prior communicated material by an implemented owner.

The current operator expression interpreter requires enough lexical focus to interpret `why <focus>` as an explanation request. A bare `why?` is treated as unresolved reference, not as a link to the last communicated answer or the current spoken-turn item. `go back` is not an implemented navigation or conversation-memory reference. `just tell me the answer` resembles a presentation preference or role request, but no owner currently binds it to a prior composed explanation, prior communicated subset, or pending content queue.

Therefore conversation continuity is still missing as an implementation boundary. The missing owner would consume the new utterance plus prior communication state and bind deictic/elliptical references to already-communicated material without reinterpreting prior meaning. It must distinguish:

```text
reference to communicated subset
!= new semantic interpretation of source explanation
```

and:

```text
request to change communication projection
!= request to change the bounded inquiry answer
```

## 4. Whether these are separate boundaries

Yes. Repository evidence supports three separate boundaries.

| Responsibility | Current status | Existing owner or gap | Why it is separate |
| --- | --- | --- | --- |
| Preserve complete bounded explanation | Partially implemented upstream; final composed artifact missing | Source explanations, rendering projection, membership evidence set, presentation admission, encounter sequencing; missing `SharedExplanationBoundedComposition` | Preservation must retain all selected/sequenced explanation material, Unknowns, conflicts, unsequenced admitted results, and derivation order. It is not limited by spoken-turn bandwidth. |
| Choose one communicable turn | Missing | No implemented low-bandwidth turn projection owner | A turn selector must project a bounded subset from preserved content under a communication budget while retaining pending content. It must not discard omitted explanation content. |
| Bind new utterance to prior communicated material | Missing | Operator expression interpretation exists for one utterance; authority/scope binding exists after interpretation; no conversation-reference binding owner | `why?`, `go back`, and `just tell me the answer` need prior communicated-material context. This is not ordinary utterance interpretation and not authority/scope binding. |

These boundaries should not be collapsed. Composition owns the complete bounded view. Communication projection owns the current low-bandwidth subset. Conversation reference binding owns continuity between a new utterance and prior communicated material.

## 5. What existing implementation already supports

Existing implementation already supports:

1. **Exact operator expression preservation.** `AttributedOperatorExpression` stores exact text, normalized text, input representation, source channel, workspace/session/operator refs, provenance, received scope context, uncertainty, Unknowns, and read-only/non-mutation boundaries.
2. **Bounded interpretation of one utterance.** `OperatorExpressionInterpretationProjection` extracts expression form, inquiry/request kind, focus/scope/authority-bearing/effect-constraint/presentation fields, source spans, alternatives, unresolved references, unsupported spans, known loss, Unknowns, conflicts, and a future handoff only when interpreted.
3. **Authority and scope binding after interpretation.** `OperatorAuthorityScopeBindingProjection` binds interpreted requests to operator identity, workspace/session authority, resolved/permitted/excluded/unresolved scopes, authority sources, constraints, state, reason, and future bounded-question handoff.
4. **Single-explanation shared rendering.** `SharedExplanationRenderingProjection` adapts one stage-local explanation into a shared read-only rendering projection while preserving source meaning ownership.
5. **Membership evidence and collection preservation.** Membership projection and evidence-set owners preserve whether each shared rendering projection belongs to one bounded inquiry and preserve Unknown/conflict/duplicate states without selecting or composing.
6. **Presentation-local admission.** Presentation admission admits already-belonging projections to one requested presentation boundary without ordering or composing.
7. **Presentation-local encounter sequencing.** Encounter sequencing records explicit encounter order and optional roles for admitted projections while preserving constitutional derivation refs separately.
8. **Human encounter ordering as a presentation responsibility.** Existing reconciliation supports presentation ordering of implementation-backed answers for operator comprehension, without presentation owning reasoning or truth.

## 6. What responsibility is still missing

Three responsibilities remain missing for low-bandwidth communication:

1. **Bounded shared-explanation composition after encounter sequencing.** The complete explanation needs one read-only composed artifact before any low-bandwidth projection can safely emit subsets. The repository has already identified this missing owner.
2. **Low-bandwidth communication projection.** Seed needs an owner that selects one communicable turn from the complete composed explanation, preserves omitted content as pending rather than discarded, and records why this subset was emitted now. This owner should not perform composition, sequencing, source interpretation, inquiry reasoning, speech synthesis, or transport.
3. **Conversation-reference binding.** Seed needs an owner that binds a new operator utterance to prior communicated material and pending composed content. It should handle references like `why?`, `go back`, and `just tell me the answer` by linking to prior communicated items, prior turn positions, roles, or pending content, without reinterpreting source meaning.

## 7. Should bounded composition precede communication projection?

Yes.

Bounded composition should precede communication projection because communication projection must choose from a preserved whole. If a low-bandwidth turn selector runs before composition exists, then omitted material can become indistinguishable from absent material. That would violate:

```text
communicated subset
!= discarded explanation content
```

The safe order is:

```text
SharedExplanationEncounterSequencing
-> SharedExplanationBoundedComposition
-> LowBandwidthCommunicationProjection
-> ConversationReferenceBinding for follow-up utterances
```

This order preserves:

- complete bounded explanation before any spoken-turn slicing;
- one spoken turn as a projection, not as the entire inquiry;
- pending/unspoken content as still part of the composed explanation;
- follow-up references as references to communicated or pending material, not reinterpretations of source truth.

## 8. Is one implementation slice warranted?

Yes, but not for speech recognition, speech synthesis, transport, conversation planning, or a broad dialog manager.

The next warranted slice should remain the already-identified bounded composition slice, not the low-bandwidth turn selector. A communicable-turn selector requires a complete composed explanation as input. Implementing turn selection first would risk collapsing composition into one utterance.

The warranted slice should therefore be:

```text
SharedExplanationBoundedComposition
```

It should consume exactly one completed `SharedExplanationEncounterSequencing` and preserve one complete operator-facing shared-explanation view without resolving Unknowns, changing encounter order, changing constitutional derivation order, assigning new roles, deduplicating by meaning, authorizing, executing, writing events, or mutating cluster state.

After that slice exists, a second bounded audit can ask how to project one low-bandwidth turn from the composed explanation while preserving pending content.

## Exact next bounded question

```text
Can Seed add `SharedExplanationBoundedComposition` as a read-only artifact that consumes exactly one `SharedExplanationEncounterSequencing` and preserves one complete operator-facing explanation view, including encounter order, constitutional derivation order, unsequenced admitted projections, Unknown/conflict/duplicate visibility, and non-mutation boundaries, so that later low-bandwidth communication projection can select one spoken turn without discarding unspoken explanation content?
```

Low-bandwidth communication boundary audit complete.

# Contextual Interpretation Warrant Audit 001

## Executive determination

Seed does not currently expose one implementation owner that performs the full lawful path:

```text
ExactOperatorMaterial
→ CandidateInterpretationSet
→ ContextualBindingEvidence
→ InterpretationWarrant
→ SelectedBoundedInterpretation
```

The repository already has adjacent preservation and bounded-selection disciplines: exact operator expression attribution, raw inquiry-note preservation, bounded constitutional question construction, explicit question-family eligibility and dispatch, runtime preservation of raw user messages before a single decision, and multiple audit/characterization artifacts distinguishing warrant from reliance, selection, transition, authorization, and mutation. Those artifacts are enough to characterize the missing responsibility, but not enough to claim the responsibility is already implemented.

The smallest missing responsibility is a read-only interpretation-warrant assembler: given exact operator material, an explicit candidate interpretation set, preserved context references, and per-candidate evidence bindings, it would produce a candidate-scoped warrant assessment for one selected bounded interpretation or preserve unresolved ambiguity. It must not mutate conversation, move goals, authorize execution, open or close inquiries, advance an inquiry frontier, or record findings as cluster truth.

One implementation slice is warranted only after the candidate/evidence schema is kept narrow and read-only. The first slice should not interpret arbitrary conversation by itself. It should prove the separations in this audit by accepting explicit candidates and evidence references, then refusing cross-candidate warrant reuse.

## Scope and non-goals

This audit is about the lawful path from exact operator material to one bounded interpretation. It is not an implementation of:

- conversation mutation;
- goal transition;
- inquiry-frontier movement;
- authorization;
- execution;
- event-ledger recording;
- cluster mutation;
- automatic correction of prior text;
- automatic promotion of presentation vocabulary into knowledge.

The audit preserves the requested guardrails:

```text
source material != corrected material
candidate interpretation != selected interpretation
plausibility of destination artifact != warrant for transforming source into that artifact
artifact for candidate A cannot consume warrant for candidate B
broad retrospective examination != rewriting prior conversation
contextual binding != goal relevance != goal transition
```

## Existing artifacts that preserve exact operator material and prior conversational context

### Runtime input event path

`input_interpretation_candidate_characterization.md` reports that the runtime path records supplied text as an `input.user_message` event before composing a decision input packet and asking for one structured decision. That gives Seed exact operator material before decision selection, but the same characterization concludes that the runtime validates and routes one proposed decision rather than preserving a candidate interpretation set.

Lawful use:

```text
raw user message can be evidence of exact operator material
```

Unsupported use:

```text
raw user message already contains a selected corrected interpretation
```

### Attributed operator expression

`lowest_sufficient_layer_recalibration_audit_001.md` identifies `AttributedOperatorExpression` as preserving exact text, normalized text, source channel, workspace/session/operator references, provenance, received scope context, uncertainty, unknowns, and expression identity. It also identifies `OperatorExpressionInterpretationProjection` as preserving source-span bindings, unsupported residual spans, unresolved references, and alternatives.

Lawful use:

```text
exact source spans can bind candidate components to operator material
```

Unsupported use:

```text
source-span binding proves that one candidate is selected
```

### Inquiry note and inquiry orientation records

`step_wise_inquiry_frontier_transition_audit_001.md` identifies `InquiryNoteRecord` as preserving `note_id`, `raw_note`, timestamp, source, workspace, and session. It also emphasizes that inquiry orientation is intentionally weak: raw notes can be oriented by deterministic evidence such as lexical overlap, but not promoted into facts, claims, goals, requirements, commands, plans, ownership, intent, recommendations, or next-safe-move authority.

Lawful use:

```text
prior note text and lexical/provenance context may be examined as contextual evidence
```

Unsupported use:

```text
prior note context rewrites the operator's current material
```

### Bounded constitutional questions and exact question-family surfaces

Existing bounded question and question-family machinery preserves exact operator inquiry fields, provenance, caller-supplied arguments, eligibility status, and dispatch-surface selection only after explicit question-family identity and required arguments are present. `input_interpretation_candidate_characterization.md` concludes that this machinery is exact-map based and does not infer raw-token meanings.

Lawful use:

```text
explicit question-family identity can support bounded selection after exact eligibility checks
```

Unsupported use:

```text
question-family dispatch is a general natural-language interpretation owner
```

### Prior audit and characterization documents

The repository contains many audit and characterization artifacts preserving prior reasoning and distinctions. They are valid retrospective context for bounded review. They do not mutate the prior conversation and do not become implementation evidence unless repository authority and implementation evidence support them.

Lawful use:

```text
prior artifacts can supply contextual evidence, constraints, negative authority, and confidence limits
```

Unsupported use:

```text
prior artifacts silently rewrite source material or select a new current goal
```

## Existing path compared with the requested lawful path

### Requested path

```text
ExactOperatorMaterial
→ CandidateInterpretationSet
→ ContextualBindingEvidence
→ InterpretationWarrant
→ SelectedBoundedInterpretation
```

### Current implementation-visible fragments

Seed currently supports fragments of the path:

1. **ExactOperatorMaterial.** Raw user messages, attributed operator expressions, inquiry notes, and bounded question fields can preserve exact material.
2. **CandidateInterpretationSet.** No stable raw-input candidate interpretation owner is demonstrated. Candidate sets exist in adjacent responsibilities, but not as a general path from exact operator material.
3. **ContextualBindingEvidence.** Source spans, provenance, workspace/session references, inquiry notes, exact question-family identities, surface arguments, lineage, and prior artifacts may support binding.
4. **InterpretationWarrant.** Warrant discipline exists conceptually across constitutional and artifact-reliance investigations, but no implementation owner currently computes an interpretation-specific warrant from exact material plus candidate-specific evidence.
5. **SelectedBoundedInterpretation.** Bounded selection exists for exact question-family dispatch and other local surfaces. It is not a general natural-language interpretation selector.

Therefore the current lawful status is:

```text
ExactOperatorMaterial: supported
CandidateInterpretationSet: adjacent but missing as general owner
ContextualBindingEvidence: supported as evidence types, not assembled for this path
InterpretationWarrant: discipline supported, implementation owner missing
SelectedBoundedInterpretation: supported only in surface-local selection contexts
```

## Whether correction candidates and interpretation candidates are distinct

They must be distinct.

A correction candidate changes or proposes a source-form relation, such as:

```text
source token: "car"
correction candidate: "cat"
```

An interpretation candidate states a bounded meaning or intended use, such as:

```text
candidate A: literal vehicle jumped a fence
candidate B: typo-corrected animal jumped a fence
candidate C: fictional/metaphorical statement
candidate D: corrupted prior example
```

The correction relation is evidence inside an interpretation candidate; it is not itself the selected interpretation. For example:

```text
"car" → "cat"
```

may be plausible because prior context discussed cats, because keyboard adjacency or spell history supports it, or because the surrounding sentence otherwise fails. But that only supports a correction candidate. A selected bounded interpretation still needs a warrant showing why this exact current source material may lawfully be read as the exact selected corrected meaning.

Required separations:

| Boundary | Required preservation |
| --- | --- |
| Exact source material | Preserve the original token/string exactly. |
| Corrected material | Preserve as proposed replacement, not as source. |
| Correction evidence | Preserve per proposed correction. |
| Interpretation candidate | Preserve as one bounded candidate consuming zero or more correction candidates. |
| Selected interpretation | Preserve as the one candidate selected under warrant, if any. |

Unsupported collapse:

```text
"car" looks like a typo for "cat"; therefore the source was "cat".
```

Lawful form:

```text
The exact source says "car". Candidate B interprets it as typo-corrected "cat". Candidate B is selected only if candidate-specific contextual evidence warrants that correction and bounded meaning. The source remains "car".
```

## What evidence may lawfully support contextual binding

Contextual binding may use evidence that links exact current material to preserved context without rewriting either. Lawful evidence classes include:

1. **Exact source spans.** Character/token spans showing which part of the operator material each candidate consumes.
2. **Prior exact material.** Earlier preserved user messages, inquiry notes, bounded question fields, or attributed expressions.
3. **Provenance continuity.** Same session, workspace, operator reference, surface, source channel, or explicit lineage.
4. **Explicit references.** Phrases such as `that example`, `same constraint`, `above`, `the prior audit`, or an exact artifact/file/identifier reference.
5. **Temporal adjacency.** Recent prior material may support binding, but cannot by itself select a candidate.
6. **Lexical recurrence.** Repeated terms can support possible binding, while respecting the repository warning that presentation vocabulary is not automatically knowledge.
7. **Structural compatibility.** The candidate fits an existing bounded surface or question family without inventing missing arguments.
8. **Negative evidence.** Conflicts, unsupported residual spans, missing referents, ambiguous antecedents, and competing candidates must remain visible.
9. **Operator clarification.** A later closed-choice answer can become new exact operator material selecting or rejecting a candidate.
10. **Implementation evidence.** If the interpretation claims repository behavior, code/tests/records must support that behavior.

Evidence that is insufficient by itself:

- destination artifact plausibility;
- model confidence;
- grammatical fluency;
- narrative convenience;
- current goal relevance;
- desire to keep working;
- existence of a runnable surface;
- a candidate artifact created for another interpretation;
- broad retrospective context without a source-span or provenance binding.

## How clarification through closed choices fits the path

Closed-choice clarification is lawful when candidate evidence does not select exactly one bounded interpretation.

Clarification should be represented as:

```text
ExactOperatorMaterial
→ CandidateInterpretationSet
→ ContextualBindingEvidence
→ unresolved ambiguity
→ ClosedChoiceClarificationRequest
→ ClarificationOperatorMaterial
→ candidate selection or continued Unknown
→ InterpretationWarrant
→ SelectedBoundedInterpretation
```

Clarification is not a mutation of the original material. It is new operator material that may select among already disclosed candidates or introduce a new candidate. The earlier source remains preserved.

A good closed-choice clarification must:

- enumerate mutually exclusive candidates;
- preserve the exact source text being clarified;
- disclose any proposed correction such as `car` to `cat`;
- allow an unresolved/other path where the listed candidates are not adequate;
- bind the response to the candidate identifiers, not merely to prose labels;
- avoid turning clarification into authorization or execution.

Example:

```text
Exact source: "The car jumped the fence."
Candidate A: literal vehicle event.
Candidate B: typo correction, "car" means "cat".
Candidate C: fictional/metaphorical example.
Candidate D: corrupted quotation from earlier material.
Clarification answer: B.
```

The clarification answer can support selection of Candidate B, but the warrant must still preserve that Candidate B includes a correction from exact source `car` to corrected material `cat`.

## What prevents cross-candidate warrant leakage

Cross-candidate warrant leakage occurs when evidence or artifacts produced for one candidate are used to justify another candidate. This audit requires per-candidate scoping.

Minimum safeguards:

1. **Stable candidate IDs.** Every candidate gets an identifier such as `candidate:A`.
2. **Source-span bindings per candidate.** Each candidate names the exact source spans it consumes.
3. **Correction bindings per candidate.** Each correction relation is scoped to the candidate that uses it.
4. **Evidence references per candidate.** Evidence records list the candidate IDs they support and the exact claim they support.
5. **Artifact references per candidate.** Draft outputs, proposed commands, or bounded artifacts are candidate-local until selected.
6. **Warrant records per selected candidate.** A warrant names the selected candidate ID and cannot be reused for a different ID.
7. **Residual spans and conflicts.** Unused source material, unsupported spans, and conflicting evidence remain visible.
8. **No implicit inheritance from plausibility.** A candidate's plausible destination artifact cannot supply source-transformation warrant for another candidate.

Required invalidity rule:

```text
If artifact X was constructed under candidate A, artifact X cannot justify candidate B unless a separate warrant binds X to B.
```

Example:

```text
Candidate A: "Reduce CPU usage" means reduce this current command's CPU.
Candidate B: "Reduce CPU usage" means restore the earlier nighttime thermal constraint.
```

Evidence that a thermal constraint exists supports Candidate B only if the current phrase is contextually bound to that earlier constraint. It does not support Candidate A. Conversely, evidence that a current command is CPU-heavy supports Candidate A only if the phrase is bound to the current operation. Neither can consume the other's warrant.

## Whether warrant production and interpretation selection are separate responsibilities

They are separate responsibilities.

**Warrant production** answers:

```text
For this exact source material, this candidate, these corrections, these context bindings, and these limits, what reliance is lawful?
```

**Interpretation selection** answers:

```text
Which candidate, if any, should be selected for the bounded downstream surface?
```

A warrant producer may conclude that multiple candidates are warranted, one candidate is warranted, no candidate is warranted, or clarification is required. A selector may consume warrant standings and choose the bounded candidate, preserve Unknown, or ask clarification. Selection without warrant is an unsupported transition. Warrant without selection is evidence, not movement.

This mirrors repository-wide distinctions already recovered elsewhere: eligibility is not dispatch, candidate standing is not selected realization, selection is not authorization, and warrant is not reliance.

## Whether an existing owner already performs either responsibility

No existing owner performs the full responsibility.

Adjacent owners are narrower:

| Existing owner/artifact | What it performs | Why it is not this owner |
| --- | --- | --- |
| Runtime `input.user_message` path | Preserves raw input before one decision. | Does not enumerate candidate interpretations or candidate-scoped warrants. |
| Decision validation | Validates one structured decision branch. | Does not compare interpretations of exact source material. |
| Attributed operator expression / interpretation projection | Preserves exact text, source spans, alternatives, residuals. | Does not establish selected bounded interpretation or full warrant responsibility. |
| Inquiry orientation | Preserves/orients raw inquiry notes with weak deterministic evidence. | Refuses semantic interpretation, planning, and next-safe-move authority. |
| Question-family bounded ask | Checks exact question-family eligibility and dispatch. | Starts after exact family identity; does not infer raw material. |
| Bounded operator goal establishment | Establishes a goal from lawful ingress evidence. | Does not classify contextual binding, correction, or interpretation selection across candidates. |
| Existing audits/characterizations | Preserve repository reasoning and negative authority. | They are documents, not runtime owners. |

Therefore Seed has preservation surfaces and local selection surfaces, but not an implementation owner for contextual interpretation warrant production or selected bounded interpretation from exact operator material.

## Smallest missing responsibility

The smallest missing responsibility is:

```text
ContextualInterpretationWarrantProjection
```

It should be read-only and should accept explicit inputs rather than discovering the world:

```text
exact_operator_material_ref
candidate_interpretations[]
correction_candidates[]
context_evidence_refs[]
source_span_bindings[]
closed_choice_clarification_ref? 
```

It should emit:

```text
candidate_warrant_standings[]
selected_candidate_id? 
selection_status: selected | clarification_required | unresolved | refused
selected_bounded_interpretation? 
unsupported_residual_spans[]
conflicts[]
unknowns[]
negative_authority[]
confidence
non_mutation_statement
```

It should explicitly refuse to:

- mutate source material;
- rewrite prior conversation;
- infer goals;
- transition goals;
- move inquiry frontiers;
- authorize commands;
- execute actions;
- write the event ledger;
- mutate cluster state;
- select a candidate whose warrant belongs to another candidate.

## Whether one implementation slice is warranted

Yes, one narrow implementation slice is warranted if Seed needs executable visibility into this responsibility rather than audit prose. The slice should be smaller than a general conversation interpreter.

Warranted first slice:

```text
A read-only projection/test helper that accepts exact source material, explicit candidate records, explicit correction records, and explicit context evidence records, then returns candidate-scoped warrant standings and either one selected bounded interpretation or clarification_required/unresolved.
```

The first slice should prove these properties:

1. source material remains distinct from corrected material;
2. correction candidates remain distinct from interpretation candidates;
3. selected interpretation must name one candidate ID;
4. warrant evidence must be scoped to the selected candidate ID;
5. candidate A cannot consume candidate B's evidence or artifact;
6. closed-choice clarification is new operator material bound to candidate IDs;
7. unresolved ambiguity remains unresolved rather than selecting by plausibility;
8. the projection is read-only and non-mutating.

Not warranted in the first slice:

- LLM-driven interpretation;
- automatic typo correction;
- conversation rewriting;
- goal selection;
- inquiry-frontier movement;
- authorization;
- execution;
- recording diagnostic findings as cluster truth.

Because this deliverable is an audit document and not an operational surface, no diagnostic inventory or shape-audit registry update is required by this change itself. If the implementation slice later adds a diagnostic, audit CLI flag, probe, view, or recordable output, the repository's operational visibility contract applies.

## Exact next bounded question

```text
What is the smallest read-only ContextualInterpretationWarrantProjection input/output schema that can prove, with tests, that exact source material, correction candidates, interpretation candidates, candidate-scoped contextual evidence, closed-choice clarification, warrant production, and selected bounded interpretation remain distinct without mutating conversation, moving goals, authorizing execution, recording findings, or leaking warrant across candidates?
```

## Conclusion

Seed can lawfully examine preserved conversation material broadly, but only as evidence. It cannot rewrite prior material, silently correct source text, or let a plausible destination artifact stand in for warrant. Correction candidates and interpretation candidates must be separate. Contextual binding evidence must be candidate-scoped. Clarification through closed choices is new operator material that can select among candidate IDs while preserving the original source. Warrant production and interpretation selection are independent responsibilities, and no existing owner performs the full path today.

The missing responsibility is a narrow, read-only, candidate-scoped warrant projection. One implementation slice is warranted only if kept to explicit inputs, explicit evidence, explicit candidate IDs, and read-only refusal behavior.

Contextual interpretation warrant audit complete.

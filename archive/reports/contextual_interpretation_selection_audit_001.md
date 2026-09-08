# Contextual Interpretation Selection Audit 001

## Scope

This audit investigates the boundary after Seed's current read-only contextual interpretation warrant-set producer:

```text
ContextualInterpretationWarrantSet
+
explicit selection evidence
+
bounded downstream purpose
→ SelectedBoundedInterpretation
```

The question is not how to implement general interpretation, not how to bind a goal, and not how to authorize action. The question is what may lawfully select one already warranted interpretation candidate while preserving these boundaries:

```text
warranted
!= applicable

applicable
!= selected

unique warranted candidate
!= automatic selection

operator clarification
!= rewriting original source

selected interpretation
!= goal binding
!= inquiry movement
!= authorization
!= execution
```

Repository authority wins. The audit therefore treats the existing implementation and prior audit as stronger evidence than vocabulary pressure.

## Reviewed repository evidence

### Existing warrant-set producer

`seed_runtime/contextual_interpretation_warrant_set.py` is the current implementation owner for candidate-scoped contextual interpretation warrant production. Its boundary notes explicitly state that source material remains separate from corrected material, correction candidates are not interpretation candidates, candidate warrant cannot leak across candidates, warrant standing is not interpretation selection, a unique warranted candidate is not selected, and the producer stops before selection, goal binding, inquiry movement, authorization, execution, recording, or state mutation.

The artifact shape confirms this boundary. `ContextualInterpretationWarrantSet` contains `closed_choice_selection_binding_ref`, but preserves `selected_candidate_ref=None`, `interpretation_selected=False`, and separate negative flags for goal binding, inquiry movement, authorization, execution, event-ledger writing, state mutation, and cluster mutation. The producer can preserve clarification evidence as evidence for a candidate, but does not select.

### Existing tests

`tests/test_contextual_interpretation_warrant_set.py` preserves the current boundary in executable form. It proves candidate-local evidence and corrections are preserved without selection, retrospective material does not automatically become support, foreign candidate refs are refused, unresolved ambiguity remains unresolved, and multiple warranted candidates remain unselected.

The most important test for this audit is the multiple-warranted-candidates case: two candidates can both be `warranted`, yet `selected_candidate_ref` remains `None` and `interpretation_selected` remains `False`. That test turns the guardrail `unique warranted candidate != automatic selection` into the stronger implementation discipline that even multiple warranted candidates provide no selection without a separate selector.

### Prior contextual warrant audit

`contextual_interpretation_warrant_audit_001.md` found that Seed had preservation surfaces and local selection surfaces, but no full owner for contextual interpretation warrant production or selected bounded interpretation from exact operator material. Since then, the repository has added the warrant-set producer. That addition satisfies the candidate-scoped warrant-set side of the earlier missing responsibility, but it intentionally stopped before selected bounded interpretation.

The prior audit also stated that clarification through closed choices is new operator material that can select among candidate IDs while preserving original source. The current implementation narrowed that into a preserved `closed_choice_selection_binding_ref` and candidate-scoped `ClarificationEvidence`, but it did not consume those inputs into a selected bounded interpretation.

### Adjacent selected-work surfaces

The question-family bounded-work pipeline already has local selection surfaces for exact registered question families and selected dispatch surfaces. Those surfaces select bounded work after exact lookup and eligibility; they do not interpret free-form operator material. They are evidence that Seed permits narrow local selection owners, not evidence that contextual interpretation selection is already owned.

## Terms used in this audit

### Warrant standing

A candidate's warrant standing answers:

```text
May this candidate be lawfully treated as supported, contradicted, ambiguous, conflicted, or unresolved by the supplied candidate-scoped evidence?
```

Warrant standing is evidence-bound and candidate-local. It does not say whether the candidate is useful for any downstream purpose, and it does not choose the candidate.

### Downstream applicability

Applicability answers:

```text
Does this warranted candidate fit a bounded downstream purpose without exceeding that purpose's local input requirements and negative authority?
```

Applicability is purpose-bound. A candidate may be warranted as an interpretation of source material but inapplicable to a specific downstream purpose. Example: a candidate may lawfully interpret the operator's phrase as a historical question, while the bounded downstream purpose is a write-capable execution path that refuses historical questions.

### Selection evidence

Selection evidence answers:

```text
Why this applicable warranted candidate, rather than another applicable warranted candidate, for this bounded downstream purpose?
```

Selection evidence must identify the candidate, the selection source, the bounded purpose, and the rule or operator act that authorizes choosing it. It must not rewrite the original source and must not promote selection into goal binding, inquiry movement, authorization, or execution.

### SelectedBoundedInterpretation

A `SelectedBoundedInterpretation` would be a read-only handoff artifact naming one interpretation candidate and preserving:

- the exact source material reference;
- the selected candidate reference;
- the candidate's warrant standing and evidence references;
- the bounded downstream purpose for which the selection is made;
- the selection evidence;
- non-selected candidates as preserved alternatives or remainder;
- unresolved residual source material, unknowns, conflicts, and negative authority;
- explicit non-mutation and non-authorization boundaries.

It is not a goal, not an inquiry transition, not authorization, not execution, not a ledger write, and not cluster truth.

## What evidence may lawfully select a candidate?

A candidate may be lawfully selected only by evidence that is both candidate-identifying and purpose-bounded.

Supported forms of selection evidence are:

1. **Exact operator clarification.** The operator supplies new exact material, such as a closed-choice answer or explicit correction, that identifies one candidate ID or one candidate label in a way the selector can bind to a candidate without rewriting the original source.
2. **Explicit selection-policy evidence.** A repository-visible policy, rule, registered surface, or tested deterministic selector states how to choose among candidate IDs for a bounded purpose when specified preconditions hold.
3. **Downstream-purpose selection requirement.** A bounded downstream consumer has explicit admissibility requirements that narrow applicable candidates, but only when those requirements are themselves selection rules and not merely applicability filters.
4. **Prior preserved selection binding.** A prior artifact may carry a `closed_choice_selection_binding_ref` or equivalent candidate-bound selection record, provided it names candidate identity, source material, selection source, and bounded purpose.

Unsupported selection evidence includes:

- candidate warrant standing alone;
- uniqueness of a warranted candidate;
- plausibility;
- model preference;
- presentation order;
- vocabulary familiarity;
- downstream usefulness without a selection rule;
- operator clarification that is not exact enough to bind to one candidate;
- correction evidence that changes original source material rather than preserving it separately;
- goal pressure, inquiry pressure, authorization pressure, or execution convenience.

## Is exact operator clarification sufficient selection evidence?

Exact operator clarification can be sufficient selection evidence, but only under strict conditions.

It is sufficient when all of the following are true:

1. the clarification is preserved as new operator material;
2. it identifies exactly one candidate or supplies an exact answer to a closed-choice selection surface;
3. the identified candidate remains warranted;
4. the identified candidate is applicable to the bounded downstream purpose;
5. the clarification does not rewrite or replace the original source material;
6. the selection artifact preserves non-selected candidates, residuals, unknowns, and conflicts;
7. the selection artifact explicitly stops before goal binding, inquiry movement, authorization, execution, recording, and state mutation.

It is not sufficient when any of the following are true:

- it only makes one candidate more plausible;
- it identifies a correction candidate but not an interpretation candidate;
- it conflicts with other selection evidence;
- it selects a candidate that is unwarranted, conflicted, or unresolved;
- it selects a candidate outside the bounded downstream purpose;
- it requires changing prior source text to make the selection appear valid.

Therefore:

```text
exact operator clarification
= possible selection evidence
!= automatic selection
!= source rewrite
!= downstream authority
```

## Does downstream applicability belong before or inside selection?

Applicability belongs before selection as a distinct gate, and the selected artifact should also preserve the applicability result inside the selection record.

The lawful sequence is:

```text
candidate warrant standing
→ bounded downstream applicability check
→ explicit selection evidence over applicable warranted candidates
→ SelectedBoundedInterpretation
```

Applicability must be before selection because a selector should not choose a candidate that the bounded downstream purpose cannot lawfully consume. However, applicability must also be preserved inside the selected artifact because downstream consumers need to know the purpose for which the selection was made and must not reuse the selection outside that purpose.

This preserves:

```text
warranted != applicable
applicable != selected
selected for purpose A != selected for purpose B
```

## What happens when several candidates remain warranted?

When several candidates remain warranted, selection must not occur unless separate selection evidence chooses one candidate for a bounded downstream purpose.

Possible lawful outcomes are:

1. **Selection by exact clarification.** The system asks or receives a candidate-bound clarification, then selects the clarified candidate if it remains warranted and applicable.
2. **Selection by explicit policy.** A repository-visible selection policy chooses one candidate under bounded, tested preconditions.
3. **No selection.** If no lawful selector exists, the artifact preserves all warranted candidates and emits `selection_status=unresolved` or `clarification_required`.
4. **Conflict.** If multiple selection evidence records choose different candidates, the selector emits `selection_status=conflicted` and no selected bounded interpretation.

Several warranted candidates are not an error by themselves. They are a lawful ambiguity state.

## What happens when the selected candidate is not warranted or not applicable?

A selection owner must refuse to produce `SelectedBoundedInterpretation` when the nominated candidate is not warranted or not applicable.

### Candidate is not warranted

If selection evidence names an unwarranted, conflicted, ambiguous, or unresolved candidate, the lawful output is refusal, not selection. The artifact should preserve:

- the nominated candidate;
- the candidate's actual warrant standing;
- the selection evidence that attempted to nominate it;
- the reason selection was refused;
- non-selected candidates and residual ambiguity.

The refusal should not repair the problem by borrowing another candidate's warrant evidence.

### Candidate is warranted but not applicable

If the candidate is warranted but inapplicable to the bounded downstream purpose, the lawful output is applicability refusal, not selection. The artifact should preserve:

- the candidate's warrant standing;
- the bounded downstream purpose;
- the applicability failure;
- any other applicable candidates, if present;
- whether clarification or policy evidence is still needed.

The selector may not treat applicability failure as authorization to change the downstream purpose.

### Candidate is applicable but not selected

If a candidate is applicable but no lawful selection evidence chooses it, the lawful output remains unresolved or clarification-required. Applicability narrows the field; it does not select.

## Unresolved ambiguity

Unresolved ambiguity is a first-class lawful stop. It occurs when:

- no candidate is warranted;
- one or more candidates are warranted but none is selected;
- clarification evidence remains unresolved;
- residual source material prevents candidate identity from being bounded;
- selection policy preconditions are not met;
- candidate applicability cannot be established for the bounded purpose.

The selector should preserve unresolved ambiguity rather than choosing by plausibility, convenience, or implementation pressure.

## Conflicting selection evidence

Conflicting selection evidence occurs when two or more selection evidence records nominate incompatible candidates for the same source material and bounded downstream purpose.

The lawful result is:

```text
selection_status=conflicted
selected_candidate_ref=None
interpretation_selected=false
```

The artifact should preserve each conflicting evidence record and the candidate it nominates. It should not resolve the conflict by warrant strength unless an explicit selection policy says warrant strength is the lawful tie-breaker for that bounded purpose. Even then, the tie-breaker is the policy evidence, not warrant standing alone.

## Do warrant standing, applicability, and interpretation selection require separate owners?

Yes. They require separate owners or at least separate named responsibilities in one module.

The responsibilities are distinct:

| Responsibility | Consumes | Emits | Must not do |
| --- | --- | --- | --- |
| Warrant standing | Exact source material, candidates, candidate-scoped evidence, clarification evidence as evidence | Candidate-scoped warrant standings | Select, bind goals, check downstream purpose, authorize, execute |
| Applicability | Warranted candidate, bounded downstream purpose, consumer admissibility requirements | Applicable / inapplicable / unresolved applicability status | Select by itself, rewrite candidate, authorize, execute |
| Selection | Warranted applicable candidates, explicit selection evidence, bounded purpose | SelectedBoundedInterpretation or refusal | Create warrant, invent applicability, bind goals, move inquiry, authorize, execute, mutate |

Keeping these owners separate prevents three collapses:

1. `warranted → selected`;
2. `applicable → selected`;
3. `selected → authorized/executed`.

A single implementation file could host the responsibilities only if tests preserve separate input fields, separate statuses, and refusal paths. The safer smallest next slice is a separate read-only selector consuming the existing warrant set.

## Does an existing owner already perform interpretation selection?

No existing owner performs contextual interpretation selection.

The current warrant-set owner intentionally does not select. It preserves `closed_choice_selection_binding_ref`, clarification evidence, candidate warrants, and boundary notes, but leaves selected fields empty and false.

The question-family bounded-work owner performs local selected bounded work for exact registered question families. That is selection after exact question-family identity and eligibility, not contextual interpretation selection from exact operator material.

Prior prose audits identified the missing responsibility, but documents are not runtime owners. The repository now has a runtime warrant-set owner; it still lacks the next owner that consumes a warrant set, explicit selection evidence, and bounded downstream purpose to produce or refuse a selected bounded interpretation.

## Smallest missing responsibility

The smallest missing responsibility is:

```text
ContextualInterpretationSelection
```

It should be read-only and should consume only explicit inputs:

```text
contextual_interpretation_warrant_set
bounded_downstream_purpose
applicability_results_by_candidate
selection_evidence[]
```

It should emit either:

```text
SelectedBoundedInterpretation
```

or a refusal/unresolved artifact such as:

```text
ContextualInterpretationSelectionResult
selection_status: selected | clarification_required | unresolved | conflicted | refused_unwarranted | refused_inapplicable
selected_candidate_ref?
bounded_downstream_purpose
selection_evidence_refs[]
applicability_refs[]
non_selected_candidate_refs[]
unknowns[]
conflicts[]
boundary_notes[]
read_only=true
interpretation_selected=(selection_status == selected)
goal_bound=false
inquiry_moved=false
authorized=false
executed=false
writes_event_ledger=false
mutates_state=false
mutates_cluster=false
```

The owner should not generate candidates, discover evidence, correct source text, infer goals, choose a downstream purpose, authorize commands, execute actions, record findings, or mutate state.

## Is one implementation slice warranted?

Yes, one implementation slice is warranted, but only if it is narrower than general interpretation and narrower than goal relevance.

The warranted slice is:

```text
Add a read-only ContextualInterpretationSelectionResult producer that consumes an existing ContextualInterpretationWarrantSet, explicit bounded downstream purpose, explicit applicability statuses, and explicit candidate-bound selection evidence, then emits selected / unresolved / conflicted / refused without mutation.
```

Minimum tests should prove:

1. exact operator clarification can select one warranted applicable candidate;
2. exact operator clarification does not rewrite original source;
3. unique warranted candidate is not selected without selection evidence;
4. applicable candidate is not selected without selection evidence;
5. multiple warranted candidates remain unresolved without selection evidence;
6. conflicting selection evidence produces conflict and no selection;
7. selecting an unwarranted candidate is refused;
8. selecting an inapplicable candidate is refused;
9. selection remains distinct from goal binding, inquiry movement, authorization, execution, recording, and mutation;
10. non-selected candidates remain preserved.

No implementation slice is warranted for natural-language interpretation, goal relevance, recalibration, conversation mutation, authorization, execution, recording, event-ledger writing, or state mutation.

Because this deliverable is an audit document and not an operational diagnostic surface, it does not add or modify a diagnostic, audit CLI flag, probe, view, operational CLI flag, or recordable output. The diagnostic inventory and diagnostic shape-audit registries therefore do not need changes for this document-only audit.

## Exact next bounded question

```text
What is the smallest read-only ContextualInterpretationSelectionResult schema and test set that can consume ContextualInterpretationWarrantSet, explicit bounded downstream purpose, explicit applicability statuses, and explicit candidate-bound selection evidence while proving that warranted, applicable, selected, goal-bound, inquiry-moved, authorized, executed, recorded, and mutated remain separate states?
```

## Conclusion

Lawful contextual interpretation selection requires explicit selection evidence over a candidate that is already warranted and applicable to a bounded downstream purpose. Exact operator clarification can be sufficient only when preserved as new exact material that identifies one candidate without rewriting the original source and without crossing into goal binding, inquiry movement, authorization, execution, recording, or mutation.

Downstream applicability belongs before selection as a distinct gate, and the selected artifact must preserve the bounded purpose so the selection cannot be reused as general authority. Several warranted candidates produce lawful ambiguity unless exact clarification or explicit policy selects one. Selection evidence naming an unwarranted or inapplicable candidate must be refused. Conflicting selection evidence must produce conflict and no selected interpretation.

The existing warrant-set owner performs candidate-scoped warrant standing, not selection. Existing bounded-work selectors perform exact registered work selection, not contextual interpretation selection. The smallest missing responsibility is a read-only contextual interpretation selection owner consuming the warrant set, applicability statuses, bounded downstream purpose, and explicit selection evidence. One implementation slice is warranted if it remains limited to that read-only selector and its refusal paths.

Contextual interpretation selection audit complete.

# Selection Producer Recovery 001

## Scope and testimony posture

This pass performs a bounded producer-only recovery of constitutional selection acts. It uses PR 1829 as reconnaissance testimony and `selection_act_classification_recovery_001.md` as PR 1830 classification testimony. It accepts only the five sufficiently evidenced producer families named in the prompt and keeps downstream consumers, handoffs, observability, view design, implementation-frontier placement, and concrete recommendation outside this pass.

Correction applied: registered-operation resolution and dispatch-surface resolution are not treated as established selection acts in this recovery. They remain adjacent resolution, binding, validation, eligibility, or handoff mechanics unless independent producer-side evidence later establishes a selection act. They are therefore not recovered as selector families here.

Method used throughout:

```text
constitutional grammar
→ producer expectation
→ producer witness
→ faithful within producer scope / unfaithful crossing / Unknown
```

## Book grammar consumed

The consumed Book grammar is the selection grammar from Book II and Book III:

- A selection act consumes a bounded candidate set plus selection evidence, exact comparison, or policy.
- It validates only identity and applicability required by the local owner.
- It chooses zero or more candidates or preserves lawful non-selection.
- It produces bounded selection standing for a declared purpose.
- It preserves enough basis, identity, uncertainty, conflict, refusal, or non-selection information required by its own assertion.
- It does not automatically authorize, execute, open inquiry, admit material, establish downstream reliance, prove sufficiency for another responsibility, produce a downstream warrant, record occurrence, or mutate constitutional standing elsewhere.

Preserved distinctions:

```text
candidate production != selection
visibility != applicability
applicability != eligibility
eligibility != admission
admission != consumption
consumption != selection
selection evidence != selected standing
selection standing != downstream reliance warrant
selection != authorization
selection != execution
selection artifact != selection occurrence automatically
unique candidate != selected candidate
ranked first != selected candidate
```

Maximum realization-invariant expectation: a faithful realization need not use the current Python dataclasses. It may use objects, immutable values, rows, predicates, joins, views, serialized handoffs, distributed assertions, or contrastive projections if it preserves the producer's bounded subject, candidate-set identity, selection basis, result standing, limits, and Unknowns.

## 1830 classifications accepted

Accepted from PR 1830 classification testimony:

- Constitutional View Selection is a faithful selection act within a representation-selection purpose.
- Advancement-Need Consideration Selection is a faithful selection act, with identity and lineage validation local to that act rather than admission.
- Contextual Interpretation Warrant Set is candidate warranting, not selection.
- Contextual Interpretation Selection is a faithful selection act that consumes candidate warrants plus explicit candidate-bound selection evidence.
- Examination-Work Selection is a faithful selection act that consumes policy/applicability/eligibility standing without collapsing them into work selection.
- Operational-Realization Selection is a faithful selection act that consumes reachability/support standing and policy without producing reliance warrant, authorization, or execution.
- Goal-Inquiry Consideration is a faithful consideration-selection act within the inspected implementation.

## 1830 classifications corrected

Corrected for this pass:

- Registered-operation resolution is not recovered as an established selection act. It is outside the five accepted selector families and remains adjacent resolution, binding, validation, or handoff mechanics here.
- Dispatch-surface resolution is not recovered as an established selection act. It is outside this pass and remains adjacent resolution, eligibility, validation, presentation, or handoff mechanics here.
- Any mention of future handoff material in a producer artifact is not treated as downstream warrant or authority. It is preserved only as producer-local result material when the producer itself emits it.

---

## 1. Representation selection: Constitutional View Selection

### Responsible question

Which registered constitutional view representations match exact caller-declared selection keys for this bounded question projection and this composition purpose?

### Candidate-set producer and identity

- Candidate-set supplier: `project_constitutional_capabilities(...)` supplies `ConstitutionalCapabilityProjection` records from registered read-model contracts, registrations, and immutable view builders.
- Bounded by: the supplied tuple of capability projections and their registered view names/capability keys.
- Candidate-set identity preserved by this selector: the selector preserves `bounded_question_id` and selected registered view names, but it does not preserve an external candidate-set fingerprint for the full capability-projection tuple.
- Candidate standing: candidates are registered representation projections with exact capability keys; they are not semantic judgments and not admitted knowledge.
- Ordering standing: no ordering standing. Iteration can affect output order as transport, but the boundary notes deny ranking and heuristics.
- Uniqueness standing: no uniqueness standing. Multiple matching registered names may be selected; no-match is lawful.
- Candidate conditions that do not select: registered existence, buildability, compatibility answer, candidate order, semantic similarity, and unsupported requested keys do not select without exact key intersection.

### Input standings

- Produced upstream: `ConstitutionalQuestionProjection` with bounded-question identity, exact selection keys, uncertainty, and read-only flags; `ConstitutionalCapabilityProjection` with registered view name, exact capability keys, compatibility answer, and read-only flags.
- Passed through: uncertainty from the question projection and compatibility answers from matched capability projections.
- Revalidated locally: exact intersection between requested selection keys and candidate capability keys; read-only/no-ledger/no-cluster boundary flags are aggregated.
- Merely referenced: registered names and capability keys are consumed as already projected fields; the selector does not rebuild immutable views.
- Constructed locally: selected view-name tuple, unsupported-key uncertainty, no-match uncertainty, compatibility answer summary, read-only boundary notes.
- Unknown: full candidate-set lineage/fingerprint beyond supplied projections is not preserved by this producer.

### Selection evidence

Selection occurrence is warranted by exact deterministic key comparison: `question_keys.intersection(capability.capability_keys)`. The evidence supports the assertion that named registered views matched requested keys. It does not prove semantic truth, downstream sufficiency, or broader representation authority.

### Local validation

The producer validates only exact key overlap and boundary flags. It does not validate raw question semantics, discover evidence, inspect immutable view content as knowledge, or perform consumer admission.

### Selection act

The act selects zero or more registered view names whose capability keys exactly overlap the bounded question's selection keys. Lawful non-selection occurs when no registered view matches or when keys are unsupported. Refusal, conflict, and Unknown are not separately modeled beyond uncertainty strings; this is faithful because this producer's assertion is deterministic representation matching, not semantic adjudication. Read-only execution still constitutes a constitutional selection occurrence when the selector runs; direct artifact construction alone would not prove occurrence.

### Lawful non-selection and remainder

- Preserved: unsupported selection keys and a no-registered-view-match uncertainty.
- Not preserved: full non-selected registered view remainder.
- Not required within producer scope: non-selected full universe, semantic mismatch reasons, consumer admission state.
- Unknown: whether the supplied capability tuple was complete for every possible registered representation outside this invocation.

### Artifact produced

`SelectedConstitutionalViews` preserves `bounded_question_id`, `selected_view_names`, `selection_uncertainty`, compatibility answer, read-only boundary notes, read-only state, and no event-ledger/cluster mutation flags.

### Standing produced

Bounded representation-selection standing: these registered view names matched exact requested keys for this bounded question and are selected for one constitutional view composition purpose. The standing is not reusable authority.

### Negative authority

The witness denies priority, truth, admission, consumer reliance, sufficiency for later movement, warrant for later movement, authority, inquiry opening, execution, recording, and producer occurrence outside this act. It also denies semantic reasoning, ranking, heuristics, planning, orchestration, evidence discovery, constitutional recovery, repository mutation, event-ledger writes, and cluster mutation.

### Producer-local Fidelity finding

Faithful within producer scope. No producer-side crossing is established. The absence of a full candidate-set fingerprint or full non-selected remainder is an interesting absence, not a defect for this deterministic representation-selection assertion.

### Realization-invariant expectation

Any realization must preserve bounded-question identity, bounded representation candidate identity sufficient for exact key comparison, selected registered representation identity, unsupported/no-match uncertainty, and the denial that exact key matching is semantic judgment or authority.

### Preserved Unknowns

Unsupported selection keys; no-match uncertainty; compatibility answer can remain `Unknown.`; completeness of the supplied capability-projection universe is not established by the selection artifact.

---

## 2. Consideration selection: Advancement-Need Consideration Selection

### Responsible question

Which exact visible selectable advancement-need reference is selected for consideration by explicit focus evidence naming that reference with required identity and lineage coordinates?

### Candidate-set producer and identity

- Candidate-set supplier: `AdvancementNeedReferenceSet` supplies visible advancement-need references.
- Bounded by: one reference set with `reference_set_id`, `need_set_id`, prior `selection_id`, selected goal, horizon, family, native projection, native lineage, and references.
- Candidate-set identity: `reference_set_id` plus need-set, selected-goal, and horizon coordinates in the selection artifact.
- Candidate standing: candidates are visible advancement-need references; only selectable, non-conflicting, exactly identified references can be selected.
- Ordering standing: presentation/order does not select.
- Uniqueness standing: unique visible/selectable standing does not select absent exact focus evidence.
- Candidate conditions that do not select: uniqueness, sufficiency reasons, standing labels, presentation order, family, wording similarity, severity, and selectable count.

### Input standings

- Produced upstream: advancement-need references and their reference-set identity/lineage; focus evidence supplied by an upstream focus source.
- Passed through: visible references, source refs, unknowns, conflicts, focus evidence refs, and focus provenance refs.
- Revalidated locally: same need set, prior selection ID, goal-establishment identity, horizon, family, native projection, native lineage, exact candidate presence, duplicate lineage conflict, conflict flag, and selectability.
- Constructed locally: deterministic selection ID, selected/non-selected reference partition, state-specific refusal fields.
- Unknown: no downstream admission or reliance standing is produced or checked.

### Selection evidence

Explicit `NeedFocusEvidence` in `exact_reference` state, naming exactly one reference and matching need set, selected goal, goal establishment, horizon, family, native projection, and native lineage. This evidence warrants only the assertion that consideration selection occurred for that reference set.

### Local validation

The producer validates focus identity, lineage, presence, single-match uniqueness, conflict, and selectability. This validation is not admission.

### Selection act

The act chooses at most one advancement-need reference for consideration. Lawful non-selection is available for no focus evidence, missing identity, ambiguity, conflict, reference mismatch, absent reference, duplicate lineage conflict, and non-selectable reference. Refusal states are distinct from no-focus non-selection; conflict and Unknown are preserved through state and material fields. Read-only execution is still a constitutional selection occurrence when the producer function performs the validation and result production.

### Lawful non-selection and remainder

- Preserved: visible references, non-selected references, ambiguous IDs, missing-identity evidence refs, mismatch refs, absent refs, duplicate-lineage refs, non-selectable refs, unknowns, conflicts.
- Not required within producer scope: priority ordering, primary blocker universe, resolution candidates, next actions, realization candidates.
- Not owned: downstream inquiry-opening refusal or authority refusal.

### Artifact produced

`AdvancementNeedConsiderationSelection` preserves selection identity, reference-set and need-set coordinates, selected goal and horizon, focus evidence/provenance refs, selection state, selected reference when any, visible/non-selected references, refusal fields, unknowns/conflicts, read-only status, and negative boundary flags.

### Standing produced

Bounded consideration standing for one selected advancement-need reference. It is selected for consideration only, not selected as priority, resolution, next action, inquiry, realization, or authorized work.

### Negative authority

The witness explicitly denies priority, truth beyond the referenced standing, admission, consumer reliance, sufficiency for later movement, warrant for later movement, authority, inquiry opening, execution, recording, event-ledger writes, cluster mutation, need prioritization, primary-blocker declaration, resolution selection, next-action selection, realization selection, work authorization, and occurrence outside this act.

### Producer-local Fidelity finding

Faithful within producer scope. No crossing is established. The producer does not strengthen visibility or selectability into selection; it refuses when exact focus and lineage requirements fail.

### Realization-invariant expectation

Any realization must preserve the exact reference-set identity, selected subject identity/lineage, focus evidence basis, selected/non-selected or refusal state required by this producer, conflict/Unknown preservation, and the denial that consideration selection creates priority or movement authority.

### Preserved Unknowns

Focus-evidence Unknown states are preserved as missing-identity refusal material; evidence unknown strings are preserved; downstream admissibility, reliance, and inquiry consequences remain Unknown/not owned.

---

## 3. Consideration selection: Goal-Inquiry Consideration

### Responsible question

Which exact visible bounded goal is selected for inquiry consideration by explicit focus evidence naming its established goal identity?

### Candidate-set producer and identity

- Candidate-set supplier: `GoalOrientationInventory` supplies visible bounded-goal views through associated dimensions.
- Bounded by: visible `GoalOrientationArtifactView` records whose `artifact_kind` is `bounded_goal` inside the supplied inventory.
- Candidate-set identity: `goal_inventory_candidate_set_id(...)`, a stable hash of visible goal artifact refs, source refs, and association states.
- Candidate standing: candidates are visible bounded-goal records, not prioritized or activated goals.
- Ordering standing: none.
- Uniqueness standing: inventory uniqueness does not select without exact focus evidence.
- Candidate conditions that do not select: dimensions, Null dimensions, pressures, labels, topic similarity, and inventory uniqueness.

### Input standings

- Produced upstream: goal orientation inventory and visible bounded-goal records.
- Passed through: selected goal source ref on success, non-selected goals, focus/provenance refs, evidence unknowns/conflicts.
- Revalidated locally: candidate set identity snapshot, exact goal-establishment identity, single match, ambiguity, missing identity, conflict, inventory mismatch.
- Constructed locally: selection ID, selection state, non-selected goals, refusal fields.
- Unknown: the producer does not establish downstream inquiry admission, inquiry opening, or goal activation.

### Selection evidence

Explicit `GoalFocusEvidence` in `exact_goal_identity` state naming one `goal_establishment_id`. The evidence supports selection occurrence only when exactly one visible bounded-goal candidate matches.

### Local validation

The producer validates evidence state, identity presence, conflict/ambiguity state, exact candidate match count, and inventory mismatch. This is not admission.

### Selection act

The act selects at most one visible bounded goal for inquiry consideration. Lawful non-selection occurs for no focus evidence, missing goal identity, ambiguous evidence, conflict, and inventory mismatch. Refusal/non-selection states are distinct; conflicts and Unknowns are preserved. Read-only execution is still a constitutional selection occurrence when the producer validates and emits the result.

### Lawful non-selection and remainder

- Preserved: non-selected goals, ambiguous goal refs, missing-identity evidence refs, inventory-mismatch refs, unknowns, conflicts.
- Not required within producer scope: priority ranking, inquiry frontier movement, work queue, full non-visible goal universe.
- Not owned: later inquiry opening or authorization state.

### Artifact produced

`GoalInquiryConsiderationSelection` preserves selection identity, inventory candidate-set identity, focus evidence/provenance refs, selection state, selected goal identity/source ref when any, non-selected goals, ambiguity/missing/mismatch material, unknowns/conflicts, read-only status, and negative boundary flags.

### Standing produced

Bounded inquiry-consideration standing for one visible bounded goal. It means selected for consideration, not priority, activation, inquiry opened, next movement, or authorized work.

### Negative authority

The witness explicitly denies priority, truth beyond visible bounded-goal reference, admission, consumer reliance, sufficiency for later movement, warrant for later movement, authority, inquiry opening, execution, recording, event-ledger writes, cluster mutation, goal activation, inquiry requirement, and frontier movement.

### Producer-local Fidelity finding

Faithful within producer scope. No crossing is established. The producer keeps visibility, uniqueness, pressure, and exact focus evidence distinct.

### Realization-invariant expectation

Any realization must preserve visible-goal candidate-set identity, exact focus basis, selected goal identity/source if selected, lawful non-selection/refusal states, conflicts/Unknowns, and the denial that selected-for-consideration opens inquiry.

### Preserved Unknowns

Unknown evidence states become missing-identity refusal material; evidence unknown strings are preserved; downstream movement/admission/reliance remain Unknown/not owned.

---

## 4. Meaning selection: Contextual Interpretation Selection

### Responsible question

Which warranted interpretation candidate is selected by explicit candidate-bound selection evidence from this contextual interpretation warrant set?

### Candidate-set producer and identity

- Candidate-set supplier: `ContextualInterpretationWarrantSet` supplies candidate warrants.
- Bounded by: one `warrant_set_id` and its `candidate_warrants`.
- Candidate-set identity: `warrant_set_id` preserved in the result.
- Candidate standing: candidates may be warranted, unwarranted, Unknown, or conflicting upstream; only a known candidate with `warrant_standing == "warranted"` may be selected.
- Ordering standing: none.
- Uniqueness standing: a sole warranted candidate is not selected without explicit candidate-bound selection evidence.
- Candidate conditions that do not select: warrant production, uniqueness among warranted candidates, residual source material, proposed corrections, and downstream inability to consume.

### Input standings

- Produced upstream: candidate-local warrant standing, operator material, candidate warrants, proposed corrections, residual source material, unknowns/conflicts.
- Passed through: operator material, candidate warrants, proposed corrections, residual source material, unknowns/conflicts, evidence provenance.
- Revalidated locally: selection evidence kind, evidence/candidate refs, candidate existence in warrant set, single named candidate, warranted standing.
- Constructed locally: selection result ID, selected candidate ref/candidate, non-selected candidates, outcome, interpretation-selected flag, selection provenance.
- Unknown: downstream applicability/admission remains explicitly none/not established.

### Selection evidence

`CandidateSelectionEvidence` of kind `exact_operator_clarification` or `candidate_bound_selection_artifact`, naming one exact candidate ref. The evidence warrants the assertion that the selection occurred only if the referenced candidate exists in the warrant set and is warranted.

### Local validation

The producer validates evidence identity and kind, candidate membership, no conflicting multiple candidate refs, and warranted standing. This is not candidate warrant production and not downstream admission.

### Selection act

The act selects exactly one warranted interpretation candidate when explicit candidate-bound evidence names it. Zero selected is lawful for no evidence, sole/multiple warranted candidates without selection evidence, unwarranted/unknown refs, or conflicting evidence. Refusal is distinct from non-selection: unwarranted or unknown candidate evidence yields `selection_refused_unwarranted_candidate`; multiple refs yield `conflicting_selection_evidence`. Conflict and Unknown material are preserved. Read-only execution constitutes selection occurrence when this producer performs the act.

### Lawful non-selection and remainder

- Preserved: non-selected candidates, full candidate warrants, proposed corrections, residual source material, unknowns, conflicts, selection provenance, specific outcomes.
- Not required within producer scope: downstream applicability refusal detail, consumer admission state, goal binding, inquiry movement.
- Not owned: original warrant production beyond consuming its result.

### Artifact produced

`ContextualInterpretationSelectionResult` preserves artifact type, selection result ID, warrant set ID, operator material, selection evidence, selected candidate ref/candidate if any, non-selected candidates, candidate warrants, proposed corrections, residual material, unknowns/conflicts, provenance, outcome, interpretation-selected flag, and negative boundary flags.

### Standing produced

Bounded selected-meaning standing: one warranted interpretation candidate is selected by explicit candidate-bound evidence for this warrant set. It is not downstream applicability, admission, or authority.

### Negative authority

The witness explicitly denies priority, truth beyond the local selected-meaning assertion, admission, consumer reliance, sufficiency for later movement, warrant for later movement, authority, inquiry opening/movement, execution, recording, conversation/state/cluster mutation, goal binding, and downstream applicability.

### Producer-local Fidelity finding

Faithful within producer scope. No crossing is established. The producer refuses to turn warranted standing, uniqueness, or downstream convenience into selection.

### Realization-invariant expectation

Any realization must preserve warrant-set identity, candidate-local warrant standing as consumed input, candidate-bound selection evidence, selected candidate identity/result, non-selection/refusal/conflict outcomes, and the denial that selected meaning is downstream applicability.

### Preserved Unknowns

Candidate warrant unknowns and conflicts are preserved; unknown/unwarranted selection references are refused with conflict material; downstream applicability and admission remain unset/Unknown from this producer.

---

## 5. Policy/work selection: Examination-Work Selection

### Responsible question

Which eligible examination work item, if any, is selected under this supplied examination policy projection, selector handoff, and frontier?

### Candidate-set producer and identity

- Candidate-set supplier: `ExaminationFrontier` supplies work items and classifications; `ExaminationPolicyProjection` supplies in-scope and eligible references plus policy standing.
- Bounded by: one frontier ID, one policy projection ID, one selector handoff, and referenced work IDs present in the frontier.
- Candidate-set identity: frontier ID, policy projection ID, handoff ID, inquiry reference, frontier reference, policy reference, and eligible references.
- Candidate standing: work items can be eligible, blocked, unsupported, deferred, examined, failed, conflict, or unknown; only eligible in-scope work may be selected.
- Ordering standing: none; no lexical, insertion-order, hash-order, or arbitrary tie-break is used.
- Uniqueness standing: sole eligible can select only when policy is applicable and sufficient and policy kind allows sole-candidate selection.
- Candidate conditions that do not select: policy applicability alone, policy sufficiency alone, frontier eligibility alone, being first in order, being in scope, or being unblocked.

### Input standings

- Produced upstream: frontier classifications, method applicability/constraints, policy projection, selector handoff.
- Passed through: inquiry/frontier/policy/method references, unchanged blocked/unsupported/deferred/examined/failed/conflict/unknown classifications, policy unknowns/conflicts.
- Revalidated locally: handoff-policy-frontier identity, policy kind/sufficiency/tie treatment, eligible references, prerequisites, no-selection conditions, referenced work presence, frontier eligibility for eligible refs.
- Constructed locally: selection ID, selected work ref, selection basis/reason, non-selected eligible work with reasons, no-selection reasons, future probe request handoff if selected.
- Unknown: consumer-side probe authorization and execution standing.

### Selection evidence

Policy projection plus selector handoff and frontier eligibility provide the selection coordinates. Exact forms include explicit work identity, sole eligible under sufficient no-order policy, prerequisite-first uniqueness, explicit no-selection policy, insufficient/unknown/conflict policy states, and no lawful tie-break.

### Local validation

The producer validates coherence among frontier, policy projection, and handoff; verifies eligible policy references against frontier classifications; and applies policy standing. This validation is not admission, authorization, or probe execution.

### Selection act

The act applies the existing policy to eligible in-scope frontier work and selects at most one work item, or preserves no-selection, unknown, or conflict. Lawful non-selection is an outcome for inapplicable policy, explicit no-selection, insufficient policy, no eligible work, multiple eligible items without lawful tie-break, absent/ineligible explicit work identity, unsupported policy kind, unknown policy, or conflict. Refusal/error is distinct from non-selection for invalid handoff/frontier/policy coherence. Read-only execution still constitutes a constitutional selection occurrence.

### Lawful non-selection and remainder

- Preserved: non-selected eligible work, policy-excluded references, unchanged blocked/unsupported/deferred/examined/failed/conflict/unknown references, no-selection reasons, unknowns, conflicts.
- Not required within producer scope: full historical work universe, downstream probe-request acceptance, execution outcome.
- Not owned: policy creation/alteration or frontier classification production.

### Artifact produced

`ExaminationWorkSelection` preserves artifact type, selection ID, inquiry/frontier/policy/handoff references, policy kind, selection state, selected work reference if any, selection basis/reason, non-selected eligible work, excluded/unchanged classifications, no-selection reasons, unknowns/conflicts, optional future probe request handoff, boundary notes, read-only state, and no ledger/cluster mutation flags.

### Standing produced

Bounded work-selection standing: one eligible work item is selected under the supplied policy/frontier, or lawful non-selection/unknown/conflict is preserved. Selected work is not a probe authorization and not an executed examination.

### Negative authority

The witness explicitly denies priority except policy-local choice, truth, admission, consumer reliance, sufficiency for later movement, warrant for later movement, authority, inquiry opening, execution, recording, policy creation/alteration, scheduling, examined status, campaign-completion verdict, event-ledger writes, and cluster mutation.

### Producer-local Fidelity finding

Faithful within producer scope. No crossing is established. The producer does not treat policy sufficiency or eligibility alone as selection and refuses arbitrary tie-breaks.

### Realization-invariant expectation

Any realization must preserve frontier identity, policy projection identity/standing, selector handoff coherence, eligible candidate identity, policy application basis, selected/no-selection state, non-selected or unchanged classifications required by the producer, conflict/Unknown preservation, and the denial that selected work is authorized or executed.

### Preserved Unknowns

Policy unknowns and conflicts; unchanged conflict/unknown frontier references; unsupported policy kind can produce unknown; downstream probe authorization/execution remains Unknown/not owned.

---

## 6. Operational-realization selection: Operational-Realization Selection

### Responsible question

Which zero or one supported operational-realization candidate is selected under this reachability projection and selection policy for the exact probe request and capability demand?

### Candidate-set producer and identity

- Candidate-set supplier: `CandidateOperationalRealizationSet` supplies candidates; `CapabilityReachabilityProjection` supplies supporting, blocked, unsupported, unknown, and conflicting partitions; `FutureOperationalRealizationSelectionHandoff` supplies a reachability-to-selection handoff reference.
- Bounded by: candidate set ID, probe request reference, capability demand reference, reachability projection ID, handoff, and policy ID.
- Candidate-set identity: candidate-set reference plus probe-request/capability-demand/reachability identity checks in validation and result fields.
- Candidate standing: candidates may be supporting, blocked, unsupported, unknown, or conflicting; eligible candidates are supporting candidates only when reachability state is `reachable`.
- Ordering standing: none; selection policy determines choice.
- Uniqueness standing: sole supported candidate selects only under a `sole_supported_candidate` policy and reachable state.
- Candidate conditions that do not select: reachable alone, supporting alone, candidate ordering, future handoff presence, registered-operation/mechanism naming, and post-selection warrant possibility.

### Input standings

- Produced upstream: candidate operational realization set, reachability projection, future selection handoff, candidate support/blocked/unsupported/unknown/conflict partitions.
- Passed through: probe request reference, capability demand reference, candidate set reference, reachability reason, shared provenance, policy unknowns/conflicts.
- Revalidated locally: handoff references reachability projection, candidate-set identity, probe-request identity, capability-demand identity, reachability candidate partitions, and supporting candidate standing.
- Constructed locally: default insufficient policy when none supplied, selection ID, selected candidate ref, eligible candidate refs, non-selected supporting candidates, policy-ineligible refs, future warrant handoff if selected.
- Unknown: actual mechanism-fitness reliance warrant, authorization, and execution.

### Selection evidence

Reachability/support standing plus selection policy coordinates. Policy forms include exact candidate, sole-supported candidate, select none, constraints, insufficient policy, and conflict. Constraints may compare mechanism reference, representation pair, methodological compatibility, authority standing, and dependency standing as policy coordinates only; these do not create authorization.

### Local validation

The producer validates candidate-set/reachability/handoff/probe/capability identity and candidate partition coherence. This is selection-local validation, not downstream warranting or registered-operation selection.

### Selection act

The act selects zero or one supporting reachable candidate under policy. Lawful non-selection occurs for not-reachable reachability, insufficient policy, select-none policy, required candidate not eligible, no supporting candidate, unresolved tie, no candidate satisfying constraints, or non-conflicting unsupported policy conditions. Conflict is distinct when policy contains incompatible required candidates or policy conflicts. Unknowns are policy unknowns and upstream unknown partitions, not silently repaired. Read-only execution constitutes constitutional selection occurrence when the producer performs validation and policy application.

### Lawful non-selection and remainder

- Preserved: eligible candidate refs, non-selected supporting candidates with reasons, policy-ineligible supporting refs, blocked refs, unsupported refs, unknown refs, conflicting refs, policy unknowns/conflicts, provenance.
- Not required within producer scope: full mechanism-fitness warrant, invocation request, external representation translation, authorization state, execution result.
- Not owned: candidate production and reachability/support production beyond validation.

### Artifact produced

`OperationalRealizationSelection` preserves artifact type, selection ID, probe request, capability demand, candidate set, reachability projection, future selection handoff reference, policy reference, selection state, selected candidate ref if any, eligible candidates, non-selected supporting candidates, blocked/unsupported/unknown/conflicting partitions, selection/reachability reasons, policy unknowns/conflicts, provenance, optional future warrant handoff, boundary notes, and read-only/no-ledger/no-cluster flags.

### Standing produced

Bounded operational-realization selection standing: one supported reachable realization candidate is selected under policy, or lawful non-selection/conflict is preserved. The future warrant handoff is not a warrant.

### Negative authority

The witness explicitly denies priority except policy-local choice, truth, admission, consumer reliance, sufficiency for later movement, warrant for later movement, authority, inquiry opening, execution, recording, reliance warrant, invocation construction, external representation translation, authorization, scheduling, registered-operation requirement, event-ledger writes, and cluster mutation.

### Producer-local Fidelity finding

Faithful within producer scope. No crossing is established. The producer keeps candidate production, reachability, supporting standing, selection, future warrant handoff, authorization, and execution separate.

### Realization-invariant expectation

Any realization must preserve candidate-set/probe/capability/reachability identity, supporting versus non-supporting partitions, policy basis, selected/no-selection/conflict state, non-selected supporting alternatives required by the producer, Unknowns/conflicts, and the denial that selection is reliance warrant, authorization, or execution.

### Preserved Unknowns

Reachability unknown candidate refs; policy unknowns; conflicting candidate refs; reliance warrant, authorization, registered-operation resolution, and execution remain Unknown/not owned by this producer.

---

## Post-recovery summary table

| Producer | Independent claim | Standing consumed | Exact act producing selection standing | Faithful within scope? |
| --- | --- | --- | --- | --- |
| Constitutional View Selection | Registered view names match exact selection keys for one bounded composition purpose. | Bounded question projection and registered capability projections. | Exact key intersection chooses zero or more registered view names. | Faithful. |
| Advancement-Need Consideration Selection | One visible advancement-need reference is selected for consideration. | Reference-set standing, visible/selectable reference standing, exact focus evidence, identity/lineage coordinates. | Exact focus evidence is validated against reference identity, lineage, presence, conflict, and selectability. | Faithful. |
| Goal-Inquiry Consideration | One visible bounded goal is selected for inquiry consideration. | Goal inventory visible bounded-goal standing and exact focus evidence. | Exact goal identity evidence is validated against the visible candidate snapshot. | Faithful. |
| Contextual Interpretation Selection | One warranted interpretation candidate is selected as meaning. | Warrant-set candidate standing and explicit candidate-bound selection evidence. | Candidate-bound evidence is validated against known warranted candidate identity and single-candidate constraint. | Faithful. |
| Examination-Work Selection | At most one eligible work item is selected under policy/frontier. | Frontier eligibility/classification, policy projection, selector handoff. | Policy is applied after identity/coherence validation to choose one work item or lawful no-selection. | Faithful. |
| Operational-Realization Selection | Zero or one supported reachable realization candidate is selected under policy. | Candidate set, reachability/support partitions, future selection handoff, selection policy. | Policy is applied after candidate-set/reachability/handoff identity validation. | Faithful. |

## Closing questions

### What does each selection producer independently claim?

- Constitutional View Selection claims only that named registered view representations matched exact keys for one bounded composition purpose.
- Advancement-Need Consideration Selection claims only that one exact advancement-need reference is selected for consideration, or that lawful non-selection/refusal applies.
- Goal-Inquiry Consideration claims only that one visible bounded goal is selected for inquiry consideration, or that lawful non-selection/refusal applies.
- Contextual Interpretation Selection claims only that one warranted interpretation candidate is selected by candidate-bound evidence, or that no-selection/refusal/conflict applies.
- Examination-Work Selection claims only that at most one eligible work item is selected under the supplied policy/frontier, or that no-selection/unknown/conflict applies.
- Operational-Realization Selection claims only that zero or one supported reachable realization candidate is selected under policy, or that no-selection/conflict applies.

### What standing does each consume?

- Constitutional View Selection consumes bounded-question projection standing and registered capability-projection standing.
- Advancement-Need Consideration Selection consumes reference-set, visible/selectable reference, focus-evidence, and identity/lineage standing.
- Goal-Inquiry Consideration consumes visible bounded-goal inventory standing and exact focus-evidence standing.
- Contextual Interpretation Selection consumes candidate-local warrant standing and candidate-bound selection-evidence standing.
- Examination-Work Selection consumes frontier classification/eligibility standing, policy projection standing, and selector handoff coherence standing.
- Operational-Realization Selection consumes candidate-set standing, reachability/support standing, future selection handoff standing, and selection policy standing.

### What exact act produces selection standing?

- Constitutional View Selection: exact deterministic key intersection over supplied representation projections.
- Advancement-Need Consideration Selection: exact focus-reference validation against the bounded reference set, lineage, conflict, and selectability.
- Goal-Inquiry Consideration: exact goal-identity focus validation against the visible bounded-goal snapshot.
- Contextual Interpretation Selection: exact candidate-bound evidence validation against one known warranted candidate.
- Examination-Work Selection: policy application after policy/frontier/handoff identity and eligibility validation.
- Operational-Realization Selection: policy application after candidate-set/reachability/handoff/probe/capability identity and support validation.

### What does each lawfully refuse or leave Unknown?

- Constitutional View Selection lawfully preserves unsupported keys, no-match uncertainty, compatibility Unknown, and candidate-set completeness Unknown.
- Advancement-Need Consideration Selection lawfully refuses no focus, missing identity, ambiguity, conflict, mismatch, absence, duplicate lineage conflict, and non-selectability; downstream inquiry/admission remains Unknown/not owned.
- Goal-Inquiry Consideration lawfully refuses no focus, missing identity, ambiguity, conflict, and inventory mismatch; downstream movement remains Unknown/not owned.
- Contextual Interpretation Selection lawfully refuses no evidence, unique/multiple warranted candidates without selection evidence, unwarranted/unknown referenced candidates, and conflicting evidence; downstream applicability/admission remains Unknown/not owned.
- Examination-Work Selection lawfully preserves no-selection, unknown, conflict, invalid coherence errors, no tie-break, no eligible work, inapplicable/insufficient policy, and unchanged non-eligible classifications; probe authorization/execution remains Unknown/not owned.
- Operational-Realization Selection lawfully preserves not reachable, insufficient policy, select none, not eligible, no supporting candidate, unresolved tie, no policy match, policy conflicts, unknown/conflicting partitions, and no reliance warrant/authorization/execution.

### Which producer witnesses are faithful within scope?

All six recovered producer witnesses are faithful within their own producer scope: Constitutional View Selection, Advancement-Need Consideration Selection, Goal-Inquiry Consideration, Contextual Interpretation Selection, Examination-Work Selection, and Operational-Realization Selection.

### Are any producer-side Fidelity crossings actually established?

No producer-side Fidelity crossings are established in this bounded pass. The corrected registered-operation and dispatch-surface neighborhoods are not counted as selection producers here.

### What producer artifacts are sufficiently recovered for a later consumer-only survey?

The sufficiently recovered producer artifacts are `SelectedConstitutionalViews`, `AdvancementNeedConsiderationSelection`, `GoalInquiryConsiderationSelection`, `ContextualInterpretationSelectionResult`, `ExaminationWorkSelection`, and `OperationalRealizationSelection`. This pass does not begin the consumer-only survey.

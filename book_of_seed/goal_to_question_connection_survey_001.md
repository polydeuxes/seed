# Goal-to-question constitutional connection survey 001

## Central question

What repository-evidenced crossings connect established goal standing to constitutional question standing, and what evidence or warrant permits each crossing?

## Method and scope

This is a documentation-only survey. It does not modify implementation, add helpers, create adapters, add tests, or introduce public exports. The survey starts from repository artifacts that preserve goal standing and question standing, then traces producers, consumers, references, and handoffs in both directions.

Search coordinates used included external testimony, goal interpretation, goal establishment, goal selection or consideration, evidence territory, observation, examination, finding, Unknown, Evidence, conflict, insufficiency, inquiry need, inquiry pressure, question form, methodological warrant, bounded question, question admission, and question selection. These were treated only as coordinates, not as required stages.

## 1. Goal-standing artifacts examined

### BoundedOperatorGoalEstablishment

`BoundedOperatorGoalEstablishment` is the clearest implementation artifact preserving bounded goal standing. It is produced by functions that consume lawful ingress evidence and produce a read-only artifact with `goal_establishment_id`, ingress artifact identity, ingress lineage, establishment state, reason, intended outcome, known scope, unresolved scope, sufficiency state, stop conditions, provenance, constraints, Unknowns, ambiguities, conflicts, and known loss.

Relevant warrant:

- The module describes itself as read-only establishment of a bounded operator goal from lawful ingress evidence.
- Its boundary notes distinguish bounded operator goal establishment from constitutional meta-target establishment and constraint enforcement.
- Its boundary notes explicitly say that goal established is not inquiry opened, resources observed, constraints satisfied, work authorized, or goal satisfied.
- The dataclass also preserves non-crossing booleans: inquiry not opened, resources not observed, constraints not enforced, work not authorized, execution not started, recording not started, no event ledger writes, and no cluster mutation.

### GoalInquiryConsiderationSelection

`GoalInquiryConsiderationSelection` selects one visible bounded goal for inquiry consideration from explicit focus evidence naming exact bounded-goal identities. It preserves a selected goal identity only when selection evidence matches the visible inventory and distinguishes selection for consideration from activation, inquiry requirement, inquiry opening, frontier movement, authorization, execution, recording, and mutation.

Relevant warrant:

- `GoalFocusEvidence.goal_establishment_id` is lawful only when it names an exact established bounded-goal identity.
- `select_goal_for_inquiry_consideration` selects a goal only through exact focus evidence, not topic similarity, priority, labels, inventory uniqueness, or pressure.

### BoundedAdvancementHorizon

`BoundedAdvancementHorizon` preserves a present movement boundary for one already-selected bounded goal. It carries selected goal identity, goal establishment identity, ingress lineage, evidence snapshot refs, included/excluded scope, time/current-state bounds, potentially relevant need families, explicit exclusions, Unknowns, conflicts, stale evidence refs, and unavailable evidence refs.

Relevant warrant:

- The artifact is not the goal itself.
- It is not need classification or sufficiency judgment.
- Included need family means potentially relevant to preserve, not that a need exists.
- It does not open inquiry, authorize, execute, record, or mutate state.

### InquiryNeedProjection and GoalAdvancementNeedSet

`InquiryNeedProjection` preserves inquiry-need standings from explicit component-bounded repository/world uncertainty testimony, while preserving the distinction between inquiry standing and evidence freshness/availability. `GoalAdvancementNeedSet` then preserves supplied stage-owned need projections without reinterpretation.

Relevant warrant:

- Generic Unknowns, observations, unsupported facts, stale evidence, absent artifacts, and mixed unresolved material are not inquiry-need evidence.
- Inquiry need established is not inquiry opened, question selected, observation authorized, action selected, sufficiency judged, execution, recording, event-ledger writing, or cluster mutation.
- Need sets preserve coexisting needs as unordered and do not prioritize, select a route, select next action, judge sufficiency, open inquiry, authorize, execute, record, write the ledger, or mutate.

### AdvancementNeedReferenceSet and AdvancementNeedConsiderationSelection

`AdvancementNeedReferenceSet` exposes one reference for each native item in supplied need projections, preserving native standing, bucket, evidence quality, visible/selectable state, and conflicts as metadata rather than identity. `AdvancementNeedConsiderationSelection` selects one visible advancement-need reference for consideration only through exact focus evidence matching the same need set, selected goal, bounded horizon, need family, native projection, and native record lineage.

Relevant warrant:

- Standing, bucket, evidence quality, and selectability are preserved as metadata rather than identity.
- Visible references are not necessarily selectable; only established native records are selectable.
- Need selected for consideration is not highest-priority need, primary blocker, resolution selected, next action selected, realization selected, inquiry opened, authority requested, authorization, execution, recording, event-ledger write, or mutation.

## 2. Question-standing artifacts examined

### BoundedConstitutionalQuestion

`BoundedConstitutionalQuestion` is the clearest implementation artifact preserving question standing. It stores `bounded_question_id`, `operator_inquiry`, `inquiry_provenance`, `bounded_question`, `constitutional_intent`, `scope_status`, uncertainty, Unknowns, caller-supplied fields, and read-only boundaries. It is produced by `produce_bounded_constitutional_question` from explicit caller inputs only.

Relevant warrant:

- The module preserves explicitly supplied fields.
- It preserves caller inputs as evidence/testimony without projecting views, discovering capabilities, selecting authority, writing ledgers, or mutating cluster state.
- Its default testimony status says operator testimony is preserved as evidence, not established fact.
- Its read-only boundaries reject natural-language classification, established fact promotion, verified claim promotion, constitutional authority creation, repository truth creation, durable knowledge creation, authoritative capability creation, constitutional view selection, QuestionProjection production, event-ledger writes, and cluster mutation.

### InquiryFrontierBoundaryTestimony

`InquiryFrontierBoundaryTestimony` is not question standing, but it is a question-adjacent constitutional artifact because it explicitly refuses question formulation while preserving selected inquiry need boundary clauses. It preserves included/excluded inquiry scope, eligible/ineligible evidence territory, sufficient-resolution conditions, lawful stopping conditions, producer/adapter/source lineage, evidence classes, already-visible evidence refs, eligible evidence territory refs, clause standing, scope disposition, evidence currency/availability, and family disposition.

Relevant warrant:

- It preserves unordered stage-owned clauses for one exact selected inquiry need.
- It is not frontier assembly, constitutional question formulation, inquiry opening, authorization, execution, recording, event-ledger write, or cluster mutation.
- It distinguishes goal-horizon scope from inquiry scope, visible evidence from eligible evidence territory, uncertainty subject from sufficient-resolution condition, and stale/unavailable evidence from stopping condition.

### BoundedInquiryFrontier

`BoundedInquiryFrontier` is not question standing, but it is a stronger question-adjacent artifact than raw testimony. It consumes one exact selected inquiry need plus preserved frontier-boundary testimony and determines whether supplied boundary clauses coherently establish a bounded inquiry frontier.

Relevant warrant:

- Frontier establishment requires included inquiry scope, eligible evidence territory, sufficient-resolution condition, lawful stopping condition, and no material binding conflict.
- It does not invent scope, admit evidence, formulate a question, open inquiry, authorize, execute, record, write the event ledger, or mutate state.

## 3. Connection graph grounded in exact repository evidence

```text
Lawful ingress evidence
  -> BoundedOperatorGoalEstablishment
     carries: goal_establishment_id, ingress identity/lineage, establishment state, scope, sufficiency/stop conditions, provenance, Unknowns/conflicts
     stops before: inquiry opening, observation, authorization, execution, recording, mutation

BoundedOperatorGoalEstablishment + GoalOrientationInventory + exact GoalFocusEvidence
  -> GoalInquiryConsiderationSelection
     carries: selected_goal_establishment_id and selected source ref for inquiry consideration
     stops before: goal activation, inquiry required/opened, frontier movement, authorization, execution, recording, mutation

GoalInquiryConsiderationSelection + BoundedOperatorGoalEstablishment + present movement boundary/evidence snapshots
  -> BoundedAdvancementHorizon
     carries: selected goal, goal establishment, movement boundary, evidence snapshots, potentially relevant need families, exclusions, Unknowns/conflicts
     stops before: need classification, sufficiency judgment, next action selection, inquiry opening, authorization, execution, recording, mutation

GoalInquiryConsiderationSelection + BoundedOperatorGoalEstablishment + BoundedAdvancementHorizon + RepositoryWorldUncertaintyTestimony
  -> InquiryNeedProjection
     carries: inquiry-need standing buckets, testimony/source/component/subject lineage, evidence refs, evidence freshness/availability
     stops before: inquiry opening, question selection, observation authorization, action selection, sufficiency judgment, execution, recording, mutation

InquiryNeedProjection + other stage-owned need projections + BoundedAdvancementHorizon
  -> GoalAdvancementNeedSet
     carries: supplied/absent/excluded need-family records and identity conflicts
     stops before: need ordering, priority, blocker declaration, route/action selection, inquiry opening, authority request, authorization, execution, recording, mutation

GoalAdvancementNeedSet
  -> AdvancementNeedReferenceSet
     carries: visible references for native need items, native lineage, standing as metadata, evidence refs/quality, selectability/conflict
     stops before: reclassification, selection, priority, route selection, inquiry opening, authority request, authorization, execution, recording, mutation

AdvancementNeedReferenceSet + exact NeedFocusEvidence
  -> AdvancementNeedConsiderationSelection
     carries: one selected advancement-need reference when exact identity matches
     stops before: priority, blocker declaration, resolution/action/realization selection, inquiry opening, authority request, authorization, execution, recording, mutation

AdvancementNeedConsiderationSelection + FrontierBoundaryClauseInput
  -> InquiryFrontierBoundaryTestimony
     carries: selected inquiry need identity plus clauses for inquiry scope, eligible evidence territory, sufficient resolution, lawful stopping, producer/adapter/source lineage, evidence classes, clause standings
     stops before: frontier assembly, constitutional question formulation, inquiry opening, authorization, execution, recording, mutation

AdvancementNeedConsiderationSelection + InquiryFrontierBoundaryTestimony
  -> BoundedInquiryFrontier
     carries: coherent operative clauses and frontier state when required clause families are established and conflict-free
     stops before: source/observation selection, evidence admission, question formulation, inquiry opening, authorization, execution, recording, mutation

Explicit caller inputs
  -> BoundedConstitutionalQuestion
     carries: caller-supplied operator inquiry, provenance, bounded question, constitutional intent, scope status, uncertainty, Unknowns
     stops before: natural-language classification, fact/truth/authority/knowledge/capability creation, view selection, QuestionProjection, ledger writes, mutation
```

## 4. Direct crossings found

### Direct crossing A: established bounded goal to selected goal for inquiry consideration

- **Source standing:** bounded goal standing preserved by `BoundedOperatorGoalEstablishment`.
- **Target standing:** selected goal-for-inquiry-consideration standing preserved by `GoalInquiryConsiderationSelection`.
- **Producer:** `select_goal_for_inquiry_consideration`.
- **Artifact or relation carried:** exact `goal_establishment_id`, focus evidence refs, focus provenance refs, selected goal source ref, visible/non-selected/ambiguous/missing/mismatched inventory state.
- **Consumer:** later horizon and inquiry-need projection owners consume the selected goal identity.
- **Evidence or warrant for the crossing:** focus evidence is lawful only when it names an exact established bounded-goal identity; the selector consumes explicit focus evidence naming exact bounded-goal identities only.
- **Identity and provenance preserved:** selection id, inventory candidate set id, focus evidence refs, focus provenance refs, selected goal establishment id, selected goal source ref.
- **Authority and scope limits:** selection is read-only and not priority, activation, inquiry requirement, inquiry opening, frontier movement, authorization, execution, recording, or mutation.
- **What does not cross:** goal activation, priority, topic similarity, pressure, need, inquiry opening, question standing.
- **Classification:** canonical for local goal-consideration selection; not a constitutional question crossing.

### Direct crossing B: selected goal standing to bounded advancement horizon standing

- **Source standing:** selected bounded goal for inquiry consideration.
- **Target standing:** bounded advancement horizon standing.
- **Producer:** bounded advancement horizon constructor/owner.
- **Artifact or relation carried:** selected goal establishment id, selected goal source ref, goal artifact identity, ingress ref/lineage, present movement boundary, evidence snapshot refs, scope, time/current-state bounds, potentially relevant/excluded need families, Unknowns/conflicts.
- **Consumer:** inquiry-need projection and goal-advancement need-set assembly.
- **Evidence or warrant for the crossing:** horizon preserves the present movement boundary for one already-selected bounded goal and refuses mismatches, non-established goal artifacts, missing movement boundary, or missing exclusion reasons.
- **Identity and provenance preserved:** selection id, selected goal establishment id, goal establishment id, goal ingress artifact ref, goal ingress lineage, evidence snapshot refs.
- **Authority and scope limits:** horizon is not the goal, not need classification, not sufficiency judgment, and does not open inquiry or authorize work.
- **What does not cross:** need existence, sufficiency, next action, inquiry opening, constitutional question standing.
- **Classification:** canonical local crossing from selected goal to advancement horizon; not a direct goal-to-question crossing.

### Direct crossing C: selected goal plus horizon plus repository/world uncertainty testimony to inquiry-need standing

- **Source standing:** selected bounded goal and bounded horizon.
- **Target standing:** inquiry-need standing buckets.
- **Producer:** `project_inquiry_need`.
- **Artifact or relation carried:** testimony/source refs, bounded uncertainty component ref, repository-world subject ref, owning stage, inquiry need standing, evidence ref, freshness, availability, and unclassified reasons.
- **Consumer:** `GoalAdvancementNeedSet`, then reference projection and need consideration selection.
- **Evidence or warrant for the crossing:** only explicit component-bounded repository/world uncertainty testimony may be consumed; generic Unknowns, observations, unsupported facts, stale evidence, absent artifacts, and mixed unresolved material are expressly not inquiry-need evidence.
- **Identity and provenance preserved:** selection id, goal establishment id, horizon id, testimony ref, source ref, evidence ref, component ref, subject ref, owning stage.
- **Authority and scope limits:** inquiry standing is distinct from evidence freshness and availability; establishing inquiry need does not open inquiry or select question.
- **What does not cross:** observation availability, examination, finding, question, question selection, inquiry execution.
- **Classification:** canonical local crossing to inquiry-need standing; indirect toward question-adjacent terrain only.

### Direct crossing D: selected inquiry need to frontier-boundary testimony

- **Source standing:** selected advancement need where selected reference family is inquiry.
- **Target standing:** preserved frontier-boundary testimony.
- **Producer:** `preserve_inquiry_frontier_boundary_testimony`.
- **Artifact or relation carried:** selected need reference id, native projection id, native lineage, need set, selected need selection id, selected goal id, horizon id, source testimony ref, bounded uncertainty component ref, repository-world subject ref, visible evidence refs, boundary clauses, ownership basis, lineage, evidence classes, already visible evidence refs, eligible evidence territory refs, clause standing, scope disposition, evidence currency/availability, family disposition.
- **Consumer:** `assemble_bounded_inquiry_frontier`.
- **Evidence or warrant for the crossing:** boundary testimony is preserved only for one exact selected inquiry need; non-inquiry or absent selected references produce no selected-inquiry testimony identity.
- **Identity and provenance preserved:** selected need identity, native lineage, source/component/subject lineage, producer/adapter/source lineage per clause.
- **Authority and scope limits:** testimony is not frontier assembly, constitutional question formulation, inquiry opening, authorization, execution, recording, ledger write, or mutation.
- **What does not cross:** question form, bounded question, admission, source selection, observation selection, collective sufficiency judgment.
- **Classification:** canonical local crossing to frontier-boundary testimony; question-adjacent but explicitly not question-standing.

### Direct crossing E: selected inquiry need plus frontier-boundary testimony to bounded inquiry frontier

- **Source standing:** selected inquiry need and preserved boundary testimony.
- **Target standing:** bounded inquiry frontier standing.
- **Producer:** `assemble_bounded_inquiry_frontier`.
- **Artifact or relation carried:** frontier id/state, selected need identity, native projection/lineage, need set, selected goal id, horizon id, testimony id, operative/preserved/missing/conflicting/non-operative clause refs, clauses.
- **Consumer:** no implementation evidence in this survey shows direct consumption by `BoundedConstitutionalQuestion`.
- **Evidence or warrant for the crossing:** frontier establishment requires included inquiry scope, eligible evidence territory, sufficient-resolution condition, lawful stopping condition, and no material binding conflict.
- **Identity and provenance preserved:** selected need selection id, selected need reference id, native projection id, native lineage, need set id, selected goal id, horizon id, testimony id, source testimony/component/subject refs.
- **Authority and scope limits:** frontier is read-only and does not invent scope, admit evidence, formulate question, open inquiry, select sources/observations, authorize access, execute, record, write ledger, mutate, or know result.
- **What does not cross:** constitutional question standing, evidence admission, examination, finding, admission, selection.
- **Classification:** canonical local crossing to bounded inquiry frontier; not a direct question crossing.

### Direct crossing F: explicit caller inputs to bounded constitutional question standing

- **Source standing:** caller-supplied testimony/input standing, not established goal standing.
- **Target standing:** bounded constitutional question standing.
- **Producer:** `produce_bounded_constitutional_question`.
- **Artifact or relation carried:** operator inquiry, inquiry provenance, bounded question text, constitutional intent, scope status, uncertainty, Unknowns, caller-supplied fields, generated or supplied question id.
- **Consumer:** formatting/JSON functions and tests; no surveyed implementation consumer proves a goal-derived producer.
- **Evidence or warrant for the crossing:** the producer's docstring says it produces one deterministic bounded question from explicit caller inputs only.
- **Identity and provenance preserved:** bounded question id generated from the explicit fields unless caller supplies one; inquiry provenance and caller-supplied fields are preserved.
- **Authority and scope limits:** caller input is evidence/testimony, not established fact; no natural-language classification, fact promotion, authority creation, repository truth creation, durable knowledge creation, capability creation, view selection, QuestionProjection production, ledger writes, or mutation.
- **What does not cross:** established bounded goal identity, selected goal identity, inquiry need standing, frontier standing, admission/selection warrant, verified fact, constitutional authority.
- **Classification:** canonical local question constructor; compatibility/caller-supplied path only with respect to goal-to-question connection.

## 5. Indirect or plural crossings found

### Indirect route: goal establishment to bounded inquiry frontier

Evidence supports a plural route from established goal standing to bounded inquiry frontier standing:

```text
BoundedOperatorGoalEstablishment
  -> GoalInquiryConsiderationSelection
  -> BoundedAdvancementHorizon
  -> InquiryNeedProjection
  -> GoalAdvancementNeedSet
  -> AdvancementNeedReferenceSet
  -> AdvancementNeedConsiderationSelection
  -> InquiryFrontierBoundaryTestimony
  -> BoundedInquiryFrontier
```

This route is not a direct road to `BoundedConstitutionalQuestion`. It crosses through several independently limited artifacts, each of which preserves identity and refuses additional authority. The route compresses at least these distinct crossings: goal consideration selection, horizon construction, inquiry-need projection, need-set assembly, reference projection, need consideration selection, boundary testimony preservation, and frontier assembly.

The route supports `goal standing -> bounded inquiry frontier standing`, not `goal standing -> constitutional question standing`.

### Multiple source standings converging on frontier standing

`BoundedInquiryFrontier` requires two kinds of source standing:

1. selected inquiry need standing, carried by `AdvancementNeedConsiderationSelection`; and
2. coherent boundary-clause testimony, carried by `InquiryFrontierBoundaryTestimony`.

These are different relations. Selected inquiry need identity alone cannot establish a frontier because required clause families may be missing or conflicting. Boundary testimony alone cannot establish a frontier because identity mismatches create material binding conflict and non-selected/non-inquiry needs produce `not_selected_inquiry_need`.

### One apparent handoff compresses several crossings

A statement such as "the goal leads to inquiry" would compress unsupportedly across the following separately warranted boundaries:

- bounded goal standing;
- focus-evidence selection for inquiry consideration;
- present movement boundary;
- component-bounded repository/world uncertainty testimony;
- inquiry need standing;
- native reference identity and selectability;
- exact need-reference focus selection;
- frontier-boundary clause preservation;
- bounded inquiry frontier coherence.

The repository evidence does not permit collapsing these into one universal crossing.

## 6. Compatibility and caller-supplied paths

`produce_bounded_constitutional_question` is compatible with caller-supplied fields that could name goal-, need-, horizon-, or frontier-derived provenance, but the implementation does not treat those fields as constitutional origination. The producer accepts explicit caller inputs and preserves them as testimony. It does not inspect `BoundedOperatorGoalEstablishment`, `GoalInquiryConsiderationSelection`, `InquiryNeedProjection`, `AdvancementNeedConsiderationSelection`, `InquiryFrontierBoundaryTestimony`, or `BoundedInquiryFrontier`.

Therefore, a caller can supply a bounded question whose `inquiry_provenance`, `scope_status`, `constitutional_intent`, or `caller_supplied_fields` refer to goal-derived or frontier-derived artifacts, but that is a compatibility path, not repository-evidenced constitutional origination. Identity and provenance are preserved as supplied; authority remains limited to testimony preservation.

## 7. Apparent crossings that lack constitutional warrant

### Established goal directly to constitutional question

No surveyed implementation artifact proves a direct crossing from `BoundedOperatorGoalEstablishment` to `BoundedConstitutionalQuestion`. The goal artifact explicitly stops before inquiry opening and work authorization, and the question constructor explicitly consumes caller-supplied fields only.

### Inquiry need directly to question

`InquiryNeedProjection` has `selects_question=False` and boundary text saying inquiry need established is not question selected. Established inquiry need can later be referenced and selected for consideration, but it does not itself produce a question.

### Evidence availability to examination or finding

`InquiryNeedProjection` preserves evidence freshness and availability separately from inquiry standing. `InquiryFrontierBoundaryTestimony` distinguishes visible evidence from eligible evidence territory. `BoundedInquiryFrontier` says eligible evidence territory is not source selection or observation selection and does not authorize access or start execution. No crossing from evidence availability to examination or finding is warranted here.

### Frontier to question form, bounded question, or admission

`BoundedInquiryFrontier` explicitly sets `formulates_question=False`, does not invent scope, does not admit evidence, and does not open inquiry. Thus a frontier may bound later inquiry terrain but does not itself cross into question form, bounded question, or admission.

### External/operator testimony to constitutional question as established fact

`BoundedConstitutionalQuestion` preserves operator testimony as evidence, not established fact. Caller-supplied question fields do not become repository truth, durable knowledge, constitutional authority, or capability creation.

### Repository adjacency to constitutional crossing

The presence of goal, inquiry, frontier, and question files in adjacent directories or naming neighborhoods is not a constitutional crossing. The surveyed crossings require producer/consumer evidence, identity preservation, and boundary warrant.

## 8. Contradictions and historical residue

This survey found strong boundary residue rather than direct contradiction in the inspected implementation:

- Question-standing construction exists as a caller-supplied compatibility surface.
- Goal-derived inquiry/frontier construction exists as a multi-artifact local path.
- The two neighborhoods are adjacent in vocabulary but separated by explicit non-crossing boundaries: inquiry need does not select a question, boundary testimony does not formulate a question, and frontier does not formulate a question.

The historical or presentation residue is the temptation to name the whole route "goal to question." Current implementation evidence supports only goal-to-inquiry-need/frontier crossings plus a separate caller-supplied bounded-question constructor. Any stronger claim remains Unknown.

## 9. Missing evidence required to resolve Unknown connections

The following evidence would be needed before claiming a canonical goal-to-question constitutional crossing:

1. A producer that consumes goal-derived standing or frontier standing and produces `BoundedConstitutionalQuestion` or another question-standing artifact.
2. A warrant describing which source standing is sufficient: established goal, selected goal, bounded horizon, established inquiry need, selected inquiry need, frontier-boundary testimony, bounded inquiry frontier, or another artifact.
3. Identity preservation rules showing how goal establishment id, selection id, horizon id, need reference id, source testimony ref, bounded uncertainty component ref, repository-world subject ref, and frontier id are preserved or intentionally not preserved in the question artifact.
4. Authority and scope limits proving what the question producer does not do: natural-language classification, fact promotion, source selection, observation selection, evidence admission, examination, finding, admission, selection, authorization, execution, recording, event writing, or mutation.
5. Tests or documentation showing whether the path is canonical, compatibility-only, local, historical, contradictory, or intentionally plural.
6. Evidence distinguishing question form, bounded question, question admission, and question selection if any future path uses those terms.

## 10. Smallest next discriminating inquiry

The smallest next inquiry is:

> Is there any repository artifact or implementation owner that consumes `BoundedInquiryFrontier` and produces a question-standing artifact while preserving selected goal, selected inquiry need, frontier testimony, and explicit non-crossing limits?

If none exists, the current answer remains: no direct repository-evidenced crossing from established goal standing to constitutional question standing; several local crossings from established goal standing to inquiry/frontier standing; and a separate compatibility-only caller-supplied path into bounded constitutional question standing.

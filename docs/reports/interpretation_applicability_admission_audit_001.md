# Interpretation Applicability and Admission Audit 001

## Question

How does Seed establish whether one explicitly selected bounded interpretation can be lawfully consumed by one bounded downstream responsibility?

This audit treats the current `ContextualInterpretationSelectionResult` as the upstream boundary. Repository evidence preserves these distinctions:

```text
selected meaning != downstream applicability
applicable != admitted
admitted interpretation != goal established != inquiry moved != action authorized != execution begun
downstream refusal must not erase or revise selected meaning
consumer limitations must not determine what the operator meant
```

## Current upstream authority

`ContextualInterpretationSelectionResult` already owns only selection of one warranted candidate from explicit candidate-bound selection evidence. Its boundary notes explicitly state that selected interpretation is not downstream applicability or downstream admission, and that downstream inability to consume an interpretation must not erase or refuse the selected meaning. The dataclass also exposes `downstream_applicability=None`, `downstream_admission=None`, and false values for goal binding, inquiry movement, authorization, execution, recording, state mutation, and cluster mutation.

Therefore, the selected interpretation is a preserved meaning artifact. It is not already a consumer permission, downstream input contract, goal, inquiry transition, authorization, execution proposal, recording event, or presentation artifact.

## What constitutes a bounded downstream purpose

A bounded downstream purpose is one explicitly named consumer responsibility with:

1. a purpose identity, such as `bounded_operator_goal_establishment`, `proposition_or_response_correction`, `inquiry_or_intervention_binding`, or `immediate_operational_execution`;
2. one local responsibility boundary and one local output family;
3. purpose-local requirements that can be evaluated without changing the selected meaning;
4. explicit refusal modes: `applicable`, `inapplicable`, `unknown`, and `conflict`;
5. explicit non-effects: no goal establishment, inquiry movement, authorization, execution, recording, presentation, or mutation unless that later responsibility separately owns it.

A purpose is not just a natural-language intention like "use it downstream." It must be a consumer contract with named admissible inputs, required evidence, local constraints, and forbidden neighboring transitions.

## Applicability versus admission

### Applicability

Applicability asks whether the already-selected interpretation has the right shape and purpose-local evidence to be considered by a bounded consumer.

It answers:

```text
SelectedBoundedInterpretation + BoundedDownstreamPurpose + purpose-local requirements
-> InterpretationApplicabilityProjection
```

The closest implemented precedent is `ExaminationMethodApplicabilityProjection`. It evaluates local applicability states, preserves inapplicable and Unknown candidates, and says applicability does not select, prioritize, authorize, schedule, execute, admit knowledge, or create runtime Evidence or Fact.

For interpretation consumption, applicability would similarly be a read-only projection over one selected interpretation and one bounded downstream purpose. It should not admit the interpretation to that consumer, and it should not invoke the consumer.

### Admission

Admission asks whether one applicable projection may actually enter one consumer's local intake set under explicit admission evidence.

It answers:

```text
SelectedBoundedInterpretation + InterpretationApplicabilityProjection
-> DownstreamInterpretationAdmission
```

The closest implemented precedent is `SharedExplanationPresentationAdmission`. It consumes a prior membership evidence set, an explicit requested-presentation boundary, and explicit presentation-local admission evidence. It admits only already-belonging results and preserves belonging-but-unadmitted results with reasons. It also refuses sequencing, ranking, view composition, membership reinterpretation, authorization, execution, event writing, or mutation.

For interpretation consumption, admission should have the same non-collapse shape: it may admit an already-applicable interpretation to one consumer intake boundary, but it does not perform the consumer's substantive transition.

## Purpose-local evidence states

### 1. Bounded operator goal establishment

Existing code already has `BoundedOperatorGoalEstablishment`, but it consumes `ClosedChoiceSelectionBinding` or `OperatorExpressionInterpretationProjection`, not `ContextualInterpretationSelectionResult`.

Purpose-local applicability evidence for a selected bounded interpretation would include:

- the selection result has `interpretation_selected=True`;
- the selected candidate has a bounded proposed meaning or label that can be mapped to an intended outcome without rewriting source material;
- selected source spans and selection provenance are present;
- residual source material, unknowns, and conflicts are preserved separately;
- operator-stated constraints, if present, are carried as constraints and not enforced.

State outcomes:

- `applicable`: the selected interpretation supplies enough bounded orientation to be considered for goal establishment;
- `inapplicable`: selected meaning has no goal-like orientation for this purpose, or the purpose requires a field the selected artifact does not carry;
- `unknown`: the selected meaning may be goal-like, but local requirements or required lineage are missing;
- `conflict`: selected meaning and purpose-local requirements contradict, or multiple incompatible local mappings are equally evidenced.

Admission would additionally require explicit goal-intake evidence naming this selected interpretation and the goal-establishment consumer boundary. Admission still would not establish the goal; `BoundedOperatorGoalEstablishment` would remain a later owner.

### 2. Proposition or response correction

The warrant and selection artifacts preserve `CorrectionCandidate` values separately from interpretation candidates. This is important: correction candidates are not interpretation candidates, and selected meaning must not rewrite source material.

Purpose-local applicability evidence would include:

- selected interpretation identifies source spans and proposed meaning;
- proposed corrections are available as separate artifacts;
- correction target type is bounded, such as proposition text or response text;
- evidence shows the correction is about the target, not a replacement interpretation of operator meaning.

State outcomes:

- `applicable`: selected meaning can lawfully inform a bounded correction review while preserving original material;
- `inapplicable`: the selected interpretation has no correction relation to the target;
- `unknown`: target identity or correction scope is absent;
- `conflict`: correction evidence would revise selected meaning or collapse correction into interpretation selection.

Admission would require explicit correction-intake evidence for one correction consumer. Admission still would not apply the correction, recalibrate a response, record a corrected fact, or mutate conversation state.

### 3. Inquiry or intervention binding

The selected interpretation may be relevant to deciding whether an inquiry or intervention binding should be considered, but it must not move the inquiry by itself.

Purpose-local applicability evidence would include:

- bounded downstream purpose names the inquiry/intervention binding responsibility;
- selected meaning has a bounded subject, question, focus, or intervention-relevant constraint;
- local evidence links that selected meaning to an existing inquiry or intervention boundary;
- Unknowns and conflicts are carried forward rather than resolved by the consumer.

State outcomes:

- `applicable`: selected meaning is compatible with one binding boundary and carries enough local linkage to be considered;
- `inapplicable`: no local inquiry/intervention boundary matches;
- `unknown`: boundary identity or linkage evidence is absent;
- `conflict`: more than one incompatible boundary is locally supported, or binding would require revising selected meaning.

Admission would require explicit binding-intake evidence naming the selected interpretation, applicability projection, and target boundary. Admission still would not move an inquiry, begin an intervention, select work, or open resources.

### 4. Immediate operational execution

Immediate operational execution is the strongest negative test. A selected interpretation may describe an action-like meaning, but applicability to execution requires far more than selected meaning.

Purpose-local applicability evidence would include:

- an explicit execution consumer boundary;
- an action candidate shape, not merely a selected interpretation;
- authority and safety prerequisites required by execution-local code;
- proof that selected meaning is not being treated as authorization.

Current repository evidence strongly separates selection, applicability, verification, authorization, and execution. Therefore most selected interpretations should be `inapplicable` or `unknown` for immediate operational execution unless a future execution-applicability owner is implemented.

State outcomes:

- `applicable`: only if the selected interpretation can be matched to a bounded execution-intake shape and all purpose-local preconditions for consideration are present;
- `inapplicable`: interpretation lacks execution-intake shape or the requested purpose tries to treat selected meaning as authorization;
- `unknown`: execution boundary or precondition evidence is missing;
- `conflict`: evidence simultaneously supports and forbids execution intake, or admission would collapse into authorization.

Admission would require explicit execution-intake admission evidence beyond applicability. Admission still would not authorize action or begin execution. Existing execution authorization remains a separate event-backed concern.

## Is applicability candidate-independent after interpretation selection?

Yes, with a narrow qualification.

After selection, applicability should be independent of the non-selected candidates for the purpose of deciding whether the selected meaning can be consumed. A downstream consumer must not use its own limitations or preference among alternatives to redefine what the operator meant.

However, the selection result still preserves non-selected candidates, residual source material, unknowns, and conflicts. Those may be relevant as risk, conflict, or Unknown evidence in the applicability projection. They do not reopen candidate selection and do not allow a consumer to pick a different meaning.

Thus applicability is **candidate-independent for selection**, but **not evidence-blind** to preserved unknowns, conflicts, residual material, and known loss.

## What additional evidence admission requires beyond applicability

Admission requires more than `applicable`:

1. an explicit target consumer boundary;
2. the applicability projection reference;
3. explicit consumer-local admission evidence naming the selected interpretation or projection;
4. evidence that the admission target matches the purpose identity and local input contract;
5. refusal reasons for applicable-but-unadmitted cases;
6. proof of non-effects: no goal establishment, no inquiry movement, no authorization, no execution, no recording, no mutation.

This mirrors the presentation-admission precedent: membership/applicability alone is insufficient; explicit admission evidence is needed.

## One interpretation, many consumers

One selected interpretation may be:

- applicable to no consumers;
- applicable to several consumers but admitted to none;
- applicable to several consumers and admitted to exactly one;
- applicable to several consumers and admitted to several.

This is lawful because applicability is purpose-local and admission is consumer-local. For example, "inspect the diagnostic inventory" might be applicable to bounded goal establishment, inquiry binding, and correction review, but admitted only to goal establishment if only that consumer has explicit admission evidence. It might be applicable to goal establishment and inquiry binding, but admitted to neither if the system lacks downstream admission evidence. It should almost never be admitted to immediate execution without separate action, authorization, and execution boundaries.

Admission multiplicity must not collapse into consumer execution. Several admissions are several intake permissions, not several completed transitions.

## Do existing owners already perform either responsibility?

Existing owners perform analogous responsibilities, not this exact one.

- `ContextualInterpretationSelectionResult` owns selection and explicitly refuses downstream applicability and admission.
- `ExaminationMethodApplicabilityProjection` owns methodological applicability for candidate examination work, not selected-interpretation consumption.
- `SharedExplanationPresentationAdmission` owns presentation-local admission for shared explanation evidence, not interpretation admission.
- `BoundedOperatorGoalEstablishment` owns actual goal establishment from closed-choice binding or operator-expression interpretation, not applicability/admission for `ContextualInterpretationSelectionResult`.
- Existing execution authorization code owns later execution authorization events, not interpretation admission.

Therefore no existing owner currently performs selected-interpretation applicability or downstream-interpretation admission for `ContextualInterpretationSelectionResult`.

## Do applicability and admission require separate owners?

Yes.

They require separate owners because they answer different questions and have different failure modes:

- Applicability is about local fitness for consideration under one bounded purpose.
- Admission is about explicit permission to enter one consumer's intake after applicability.

Combining them would recreate the forbidden collapse:

```text
selected meaning -> downstream use
applicable -> admitted
admitted -> goal/inquiry/action/execution
```

The repository's existing applicability and admission precedents keep these gates separate. The smallest lawful design should preserve that separation.

## Smallest missing owner

The smallest missing owner is a read-only `InterpretationApplicabilityProjection` producer.

Proposed minimal artifact:

```text
SelectedBoundedInterpretation
+ BoundedDownstreamPurpose
+ purpose-local requirements/evidence
-> InterpretationApplicabilityProjection
```

Minimum fields:

- artifact type and convention;
- selected interpretation reference and selected candidate reference;
- downstream purpose reference and purpose kind;
- applicability state: `applicable`, `inapplicable`, `unknown`, `conflict`;
- purpose-local requirement results;
- supporting references;
- contradicting references;
- unknowns;
- conflicts;
- preserved selected-meaning summary;
- explicit non-effects;
- read-only and no mutation flags.

The second missing owner is `DownstreamInterpretationAdmission`, but it should not be implemented before the applicability projection exists because admission needs an applicability projection to consume.

## Is one implementation slice warranted?

Yes, but only one small slice is warranted first: implement read-only interpretation applicability for selected interpretations.

The slice should not implement admission yet, and it should not implement goal establishment, correction, inquiry transition, authorization, execution, recording, or presentation.

Suggested first slice:

1. define `BoundedDownstreamPurpose` with the four test purpose kinds;
2. define `PurposeLocalRequirementEvidence` or equivalent explicit testimony;
3. implement `project_interpretation_applicability(...)`;
4. support states `applicable`, `inapplicable`, `unknown`, and `conflict`;
5. add tests proving the guardrails, especially that selected meaning is preserved when every downstream purpose refuses applicability.

Admission can follow only after applicability output shape is stable.

## Exact next bounded question

Given one `ContextualInterpretationSelectionResult` with `interpretation_selected=True`, what smallest read-only owner can project `applicable`, `inapplicable`, `unknown`, or `conflict` for one explicit `BoundedDownstreamPurpose` using only purpose-local requirement evidence, while preserving selected meaning and stopping before admission, goal establishment, correction, inquiry movement, authorization, execution, recording, presentation, event-ledger writes, state mutation, or cluster mutation?

Interpretation applicability and admission audit complete.

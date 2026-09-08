# Responsibility to Inquiry Boundary Audit

## Selected architectural question

At what point does recovered architectural knowledge become an answerable subject?

Bounded answer: the current implementation does **not** show Inquiry consuming recovered responsibilities directly. A recovered responsibility becomes answerable only after it is represented as an exact, named `QuestionFamily` with an inventory row, bounded eligibility, an answer surface, and—where dispatchable—a mapping to an existing CLI/diagnostic surface. The implementation-backed bridge is therefore **QuestionFamily / QuestionSurfaceInventory plus bounded ask dispatch**, not a new `Subject Recovery`, `Architectural Subject`, or direct `ResponsibilityRecovery -> Inquiry` runtime object.

## Implementation evidence

### Recovered knowledge-production line remains non-promotional before responsibility

`ObservationAgreement` consumes already-observed records and emits candidate agreement records, but its boundary explicitly refuses grammar, responsibility recovery, family recovery, lexicon ownership, semantic interpretation, architectural truth, event writes, ledger writes, and mutation. Its record shape preserves candidate agreement, supporting evidence, provenance, participating streams, and a non-promotion boundary.

`GrammarObservation` consumes only `ObservationAgreementRecord` values. Its boundary permits recurring relation-shape observation and grammar-observation emission while explicitly refusing responsibility recovery, family recovery, lexicon ownership, semantic interpretation, architectural truth, capability promotion, event writes, ledger writes, repository mutation, and cluster mutation. Its emitted `GrammarObservationRecord` preserves `observed_relation_shape`, `supporting_agreements`, `provenance`, `recurrence_evidence`, and a non-promotion boundary; it does not carry a question family, dispatch surface, answer responsibility, or inquiry subject.

Implementation consequence: the recovered knowledge side reaches **shape recurrence**, not answerability. No inspected record in the current Grammar Observation implementation is an inquiry-dispatch object.

### Current answerable-subject representation

`QuestionSurfaceInventoryRow` is the strongest implementation-backed object for answerable subjects. It names a `question_family`, example questions, answering `surface`, CLI `surface_flag`, `answer_responsibility`, `authority_boundary`, bounded ask status, dispatch surface, required surface args, formatter, diagnostic inventory relationship, diagnostic shape spec relationship, and relationship status.

`build_question_surface_inventory()` returns deterministic, read-only rows for answerable families such as:

- `operational pressure`
- `current operational explanation`
- `derivation explanation`
- `selection explanation`
- `knowledge reachability`
- `capability pressure`
- `ownership ambiguity`
- `observation domain coverage`
- `observation permission state`
- `authority-constrained container ownership`
- `authority-constrained service ownership`
- `listener endpoint reachability`
- `surface inventory`
- `surface shape validation`
- `source definition/import lookup`
- `inquiry orientation`
- `projection shape visibility`

The row enrichment step derives bounded status, dispatch surface, required args, implementation reason, canonical diagnostic surface, diagnostic inventory name, diagnostic shape spec name, and relationship status from static dispatch maps and diagnostic registries.

`QuestionFamilyDefinition` and `ComposedQuestionFamilyExplanation` are identity/explanation wrappers around inventory evidence. They do not discover responsibilities; they compose existing `QuestionSurfaceInventoryRow` fields for definition and presentation.

### Inquiry dispatch consumes named families, not recovered responsibilities

The CLI parser introduces `--question-family` as an exact Question Family identifier used with `ask`. Its help text says bounded question-family dispatch uses `ask --question-family <exact-question-family>`, and `--surface-args` forwards explicit operator-provided implementation surface parameters unchanged to the existing inquiry surface.

`apply_bounded_ask_dispatch()` is the concrete inquiry dispatch adapter. It:

1. requires the literal `ask` command shape when `--question-family` is used;
2. validates the exact family against `build_question_surface_inventory()`;
3. derives eligibility with `bounded_status_for_question_family()`;
4. rejects unknown, diagnostic-only, not-dispatchable, and incorrectly parameterized families;
5. maps eligible families through `BOUNDED_ASK_DISPATCH_SURFACES` to existing surfaces;
6. optionally routes presentation requests to the composed QuestionFamily explanation.

This is named-subject dispatch. It does not parse recovered responsibilities, grammar observations, relation shapes, or responsibility-recovery records.

### Answer Composition and presentation boundary evidence

The current QuestionFamily explanation path composes existing fields only. `build_composed_question_family_explanation()` explicitly says it composes existing QuestionFamily explanation fields for presentation only, and its sections are Definition, Answer responsibility, Boundary, and Diagnostic relationship. This confirms that presentation composition is downstream of the named family/inventory row; it is not a subject-recovery capability.

Operational Story, Reasoning Path Audit, Selection Path Audit, Projection Shape, and other surfaces may own bounded answer responsibility for their own surfaces, but in the bounded ask path they are selected by `QuestionFamily` dispatch mappings, not by direct responsibility recovery.

## Current responsibility chain

Current implementation-backed knowledge-production chain:

```text
Implementation Evidence / supplied observed records
  -> Observation Agreement
  -> Grammar Observation
  -> recurring relation-shape observation
  -> non-promotion boundary
```

Evidence stops at non-promotional records before responsibility answerability:

- `ObservationAgreementRecord` is candidate-only.
- `GrammarObservationRecord` is relation-shape-only.
- `GRAMMAR_OBSERVATION_BOUNDARY["owns_responsibility_recovery"]` is `False`.
- `GrammarObservationRecord` has no field for `question_family`, `surface`, `answer_responsibility`, `dispatch_surface`, `subject`, or `inquiry`.

The prompt names `Responsibility Recovery`, but the inspected current implementation around Observation Agreement and Grammar Observation does not expose an implemented responsibility-recovery object that feeds inquiry dispatch.

## Current inquiry chain

Current implementation-backed answer/inquiry chain:

```text
operator uses: ask --question-family <exact QuestionFamily>
  -> CLI parser preserves exact family identifier
  -> apply_bounded_ask_dispatch()
  -> build_question_surface_inventory()
  -> bounded_status_for_question_family()
  -> BOUNDED_ASK_DISPATCH_SURFACES / required args
  -> existing answer surface
  -> optional QuestionFamily explanation / presentation composition
```

The selection unit is an exact string-valued `QuestionFamily`, backed by a `QuestionSurfaceInventoryRow` and dispatch maps. The unit is not a recovered responsibility record.

## Supported bridge

Supported bridge:

```text
Recovered architectural knowledge
  -> implementation-backed naming/classification as a QuestionFamily row
  -> bounded ask eligibility and dispatch mapping
  -> existing answer surface
```

More precisely, the implementation-backed bridge between recovered responsibility and inquiry is **QuestionFamily surface inventory and bounded dispatch**, when a recovered responsibility has been manually/implementation-backed encoded as:

- a `QuestionSurfaceInventoryRow.question_family`,
- an `answer_responsibility`,
- an `authority_boundary`,
- a surface and flag,
- bounded ask eligibility,
- and, if dispatchable, a `BOUNDED_ASK_DISPATCH_SURFACES` mapping with any required args.

This bridge is compatibility-preserving because the dispatch adapter maps to existing surfaces instead of introducing a new runtime subject or schema.

## Unsupported bridge

Unsupported by current implementation evidence:

```text
Responsibility Recovery
  -> Subject Recovery / Architectural Subject / Inquiry Subject
  -> Inquiry
```

No inspected code defines `SubjectRecovery`, `SubjectCharacterization`, `InquirySubject`, or `ArchitecturalSubject`. No inspected Grammar Observation record carries answerability metadata. No bounded ask dispatch path consumes `GrammarObservationRecord`, `ObservationAgreementRecord`, or a recovered responsibility object.

The implementation also rejects a stronger claim that `Inquiry` is a first-class runtime object for this boundary. The current dispatch path is an `ask --question-family` adapter and exact family lookup; `Inquiry Orientation` is a specific read-only orientation surface, not the general subject-recovery layer.

## Counterexamples

### Counterexample investigated: Inquiry already dispatches recovered responsibilities directly

Rejected. `apply_bounded_ask_dispatch()` validates exact QuestionFamily strings against `build_question_surface_inventory()` and maps through `BOUNDED_ASK_DISPATCH_SURFACES`. It does not consume `ObservationAgreementRecord`, `GrammarObservationRecord`, relation shapes, or responsibility records.

### Counterexample investigated: QuestionFamily already fulfills the missing role

Partly accepted. `QuestionFamily` is the current implementation-backed answerable subject identity. It names answerable families, connects them to surfaces, records answer responsibility and authority boundary, and controls bounded ask eligibility.

But it does **not** recover subjects from recovered responsibilities. It is a static inventory/dispatch compatibility bridge. Therefore it fulfills the answerable-subject role after naming, but it does not implement automated subject recovery between `Responsibility Recovery` and `Inquiry`.

### Counterexample investigated: Subject ownership is presentation vocabulary only

Partly accepted. The `QuestionFamily` explanation/composition path is explicitly presentation-oriented over existing fields. However, the underlying `QuestionSurfaceInventoryRow` and bounded dispatch maps are not merely presentation vocabulary: they drive CLI eligibility and surface dispatch. Subject-like labels become operational only when backed by inventory rows and dispatch maps.

### Counterexample investigated: Existing inventories already represent the missing abstraction

Partly accepted. `QuestionSurfaceInventoryRow` represents the current answerable-subject abstraction. Diagnostic Inventory and Diagnostic Shape Audit preserve compatibility and mechanical surface shape, but the bounded ask path depends on Question Surface Inventory plus dispatch maps. Existing inventories do not implement a new semantic subject-recovery capability from Grammar Observation or Responsibility Recovery.

### Counterexample investigated: DiagnosticSurface, ProjectionStage, OperationalStory, ReasoningPathAudit, or SelectionPathAudit are the answerable subject

Rejected as the general boundary. These objects/surfaces can be answer surfaces or diagnostic subjects in their own contexts, and `projection shape visibility`, `current operational explanation`, `derivation explanation`, and `selection explanation` are QuestionFamilies. But bounded ask reaches them through QuestionFamily dispatch, not by treating each surface class as the universal subject bridge.

## Compatibility boundaries

Current boundaries preserving separation:

1. **Non-promotion boundaries** in Observation Agreement and Grammar Observation prevent candidate agreements and recurring relation shapes from becoming architectural truth or responsibility authority.
2. **Static Question Surface Inventory** separates answerable family identity from lower-level knowledge observation records.
3. **Bounded ask dispatch maps** make only explicitly mapped families dispatchable and reject free-text routing.
4. **Required surface args** preserve explicit operator-provided parameters for derivation and selection explanations instead of inferring subjects from recovered responsibilities.
5. **Diagnostic inventory and shape-audit relationships** require operational surfaces to remain visible and mechanically checked without turning every diagnostic into a semantic subject-recovery layer.
6. **Presentation composition boundary** keeps QuestionFamily explanation rendering over existing fields rather than creating new subject authority.
7. **Authority boundaries on rows** preserve read-only/no-mutation semantics for answerable subjects.

These boundaries prevent a recurring relation shape or recovered-looking responsibility label from bypassing inventory, dispatch, authority, and presentation compatibility checks.

## Answers to the central questions

### 1. Does Inquiry consume recovered responsibilities directly, or named subjects?

Inquiry consumes named subjects: exact `QuestionFamily` identifiers backed by `QuestionSurfaceInventoryRow` and bounded ask dispatch maps. Current implementation evidence rejects direct consumption of recovered responsibilities.

### 2. What implementation-backed object currently represents an answerable subject?

The strongest current object is `QuestionSurfaceInventoryRow`, with `QuestionFamilyDefinition` and `ComposedQuestionFamilyExplanation` as downstream identity/presentation wrappers. Individual surfaces such as `DiagnosticSurface`, `ProjectionStage`, `OperationalStory`, `ReasoningPathAudit`, and `SelectionPathAudit` are answer surfaces or diagnostic/presentation surfaces, not the general answerable-subject bridge for bounded ask.

### 3. Is there an implementation-backed capability between Responsibility Recovery and Inquiry?

There is a limited, implementation-backed **QuestionFamily inventory/dispatch bridge**. There is not an implemented `Subject Recovery`, `Subject Characterization`, `Inquiry Subject`, or `Architectural Subject` capability that converts recovered responsibilities into inquiry subjects.

### 4. How does a recovered responsibility become something Inquiry can dispatch?

By being encoded as a named `QuestionFamily` inventory row with answer responsibility, authority boundary, surface metadata, bounded status, and dispatch mapping. Dispatch then happens through `ask --question-family <exact-family>`, not through recovered responsibility objects.

### 5. Would bypassing this boundary weaken the recovered architecture?

Yes. Directly dispatching from recovered responsibilities or grammar observations would bypass non-promotion boundaries, exact family eligibility, authority boundaries, required parameters, diagnostic-shape visibility, and presentation compatibility. It would let observation vocabulary become answer authority without the implementation-backed inventory/dispatch contract.

### 6. What compatibility boundaries currently preserve this separation?

The preserved boundaries are non-promotion in observation records, static QuestionFamily inventory, bounded ask dispatch eligibility, required surface args, diagnostic inventory/shape audit linkage, read-only authority boundaries, and presentation-only QuestionFamily explanation composition.

## Recommended next implementation step

Do not implement a bridge yet. The next smallest implementation-backed step should be another audit or characterization that traces one concrete recovered responsibility candidate into the existing `QuestionSurfaceInventoryRow` contract and asks whether adding or changing a QuestionFamily row is warranted. If implementation later needs a real bridge, first add tests proving whether responsibility-derived candidates remain non-promotional until explicitly registered as QuestionFamilies.

Avoid introducing new runtime objects, CLI changes, JSON changes, schemas, events, ledgers, grammar changes, responsibility changes, artifact framework changes, or provider framework changes as part of this audit.

## Confidence

High confidence that current inquiry dispatch consumes exact named QuestionFamilies rather than recovered responsibilities.

High confidence that `QuestionSurfaceInventoryRow` is the current implementation-backed answerable-subject representation for bounded ask.

Medium confidence on the broader architectural wording: the code supports a QuestionFamily/inventory dispatch bridge, but does not prove a complete implementation of Responsibility Recovery feeding that bridge. The strongest safe conclusion is that one bounded architectural responsibility remains missing if the desired architecture requires automatic promotion from recovered responsibilities to inquiry subjects.

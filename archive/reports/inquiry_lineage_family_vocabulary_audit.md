# Inquiry Lineage Family Vocabulary Audit

## Scope

This is a bounded implementation audit. It does not perform another
implementation slice, runtime change, CLI change, renderer change, schema change,
JSON change, event change, ledger change, or vocabulary migration.

The central question is:

```text
Can the repository now justify a responsibility-family name from implementation
evidence alone?
```

The audit begins from recurring implementation ownership, not from preferred
terminology.

## Evidence reviewed

Reviewed repository evidence:

- `inquiry_lineage_slice_001.md`
- `inquiry_lineage_slice_002.md`
- `inquiry_lineage_slice_003.md`
- `inquiry_lineage_slice_004.md`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `implementation_responsibility_family_inventory_audit.md`

No implementation behavior was changed.

## Recurring implementation ownership

The recovered implementation slices now show four independent specializations of
one recurring ownership pressure:

```text
Outcome
    !=
Lineage Frame
```

```text
Selection Result
    !=
Selection Lineage
```

```text
Derived Conclusion
    !=
Derivation Lineage
```

```text
Reference Choice
    !=
Comparison Lineage
```

The recurring implementation responsibility is not merely that extra context is
available somewhere. The repeated ownership boundary is that result-like
material must not be owned by the same implementation concern as the lineage
material that makes the result safe to interpret.

Across reviewed code, result-like material includes selected values, outcomes,
derived conclusions, selected references, projection products, and operational
answer fields. Lineage material includes evidence, candidates, non-selected
alternatives, rationale, comparison alternatives, consumers, story impact,
investigation path, unknowns, authority boundaries, influence edges, non-
influence edges, diagnostic declarations, and implementation-conformance checks.

## Implementation evidence by surface

### Reasoning path audit

Representative implementation:

```text
_DerivedConclusionPayload
    owns intermediate_conclusions and derived_conclusions

_DerivationLineagePayload
    owns evidence, consumers, story_impact, and unknowns
```

`ReasoningPathAudit` still preserves the compatibility object, but the builder
now creates conclusion and lineage payloads separately before compatibility
handoff. This is direct implementation evidence for `Derived Conclusion !=
Derivation Lineage`.

Coverage contribution: derivation lineage.

Ownership signal: strong. The payload names and fields directly separate
conclusion ownership from derivation evidence, consumers, story impact, and
unknowns.

### Selection path audit

Representative implementation:

```text
_SelectionResultPayload
    owns selected and outcome

_SelectionLineagePayload
    owns candidates, selection_factors, non_selected, evidence, and unknowns
```

`SelectionPathAudit` keeps the public shape unchanged while implementation-local
payloads separate chosen result material from candidate/factor/alternative/evidence
lineage. This is direct implementation evidence for `Selection Result !=
Selection Lineage`.

Coverage contribution: selection lineage.

Ownership signal: strong. The implementation preserves selected output without
collapsing candidate set, non-selected candidates, evidence, or unknowns into the
selected value.

### Reference selection

Representative implementation:

```text
_ReferenceChoicePayload
    owns selected_reference

_ComparisonLineagePayload
    owns selection_rationale, alternative_references, and limitations
```

`ReferenceSelection` keeps the public object unchanged while reference choice and
comparison lineage are assembled separately. This is direct implementation
evidence for `Reference Choice != Comparison Lineage`.

Coverage contribution: comparison lineage.

Ownership signal: strong. The selected reference is separate from rationale,
alternatives, and limitations for supported and unsupported domains.

### Operational story

Representative implementation:

```text
_OperationalStoryAnswerPayload
_OperationalStoryReasoningPayload
_OperationalStorySupportingEvidencePayload
_OperationalStoryBoundaryPayload
_OperationalStoryLimitationsPayload
```

`OperationalStory` is primarily answer-composition evidence, but it also supplies
adjacent implementation evidence for this audit: focus, pressure, capabilities,
constraints, correlation gaps, impact, recent changes, and observed outcomes are
not owned by the same payloads as investigation path, supporting evidence,
unknowns, and boundary.

Coverage contribution: operational answer lineage.

Ownership signal: medium to strong. It proves result/support/boundary separation,
but its native family is Answer Composition rather than this lineage family.

### Projection shape

Representative implementation:

```text
ProjectionShapeStage.produces
    !=
ProjectionShapeStage.consumes / influences / does_not_influence /
authority_boundary / confidence
```

`projection_shape` has not been sliced into implementation-local result and
lineage payloads. However, it repeatedly exposes projection products beside the
consumption, influence, non-influence, authority, and confidence frame required
to interpret those products.

Coverage contribution: projection influence lineage.

Ownership signal: medium. The boundary is visible in the public stage shape, but
not yet recovered as private implementation-local payload ownership.

### Diagnostic inventory and diagnostic shape audit

Representative implementation:

```text
DiagnosticInventoryEntry
    declares operational diagnostic surface shape

DiagnosticShapeAuditRow / DiagnosticImplementationSpec
    check declared shape against implementation evidence
```

The diagnostic inventory declares each operational surface's flags, state/repo
use, JSON/record support, record scope, fact emission, event-ledger behavior, and
mutation boundary. The shape audit separately records implementation specs,
observed values, declared values, and consistency status.

Coverage contribution: diagnostic declaration/conformance lineage.

Ownership signal: medium. These surfaces are diagnostic-governance evidence, not
a direct inquiry-lineage slice, but they show the same pattern that a surface
name or declaration is not enough without implementation-conformance lineage.

## Candidate family-name evaluation

### Inquiry Lineage

#### Implementation coverage

High. It covers all four recovered slices without forcing one domain's wording
onto another:

- outcome requires lineage frame;
- selection result requires selection lineage;
- derived conclusion requires derivation lineage;
- reference choice requires comparison lineage.

It also naturally includes adjacent projection, operational story, and diagnostic
conformance evidence because each surface preserves how an inquiry result,
choice, conclusion, projection product, or declaration can be interpreted.

#### Representative implementation

- `_DerivedConclusionPayload` / `_DerivationLineagePayload` in
  `reasoning_path_audit`.
- `_SelectionResultPayload` / `_SelectionLineagePayload` in
  `selection_path_audit`.
- `_ReferenceChoicePayload` / `_ComparisonLineagePayload` in
  `reference_selection`.

#### Ownership consistency

High. The word `Lineage` is already the recurring implementation term in the
recovered boundaries: Lineage Frame, Selection Lineage, Derivation Lineage, and
Comparison Lineage. The modifier `Inquiry` is supported because the reviewed
surfaces are read-only audit, selection, reasoning, reference, projection,
operational-story, and diagnostic-conformance surfaces that help answer how an
inquiry result was reached or bounded.

#### Counterexamples

No reviewed implementation rejects this name. The main caution is that `Inquiry`
should not be expanded to all repository knowledge, all presentation vocabulary,
or all diagnostics. The evidence supports inquiry-result interpretability, not a
universal provenance system.

#### Missing implementation evidence

`ProjectionShapeStage` still has a compressed public stage shape rather than a
private projection-result/influence-lineage compatibility handoff. However, this
is a remaining implementation step, not a blocker to the family name, because
four independent specializations already use lineage ownership directly.

#### Confidence

High.

### Interpretive Lineage

#### Implementation coverage

Medium to high. It captures the interpretive function of the lineage frame:
evidence, candidates, alternatives, consumers, unknowns, boundaries, and
limitations make result-like material safe to interpret.

#### Representative implementation

- `ReasoningPathAudit` evidence/consumers/story impact around derived
  conclusions.
- `ReferenceSelection` rationale/alternatives/limitations around selected
  references.
- `OperationalStory` investigation path/support/boundary around the current
  focus and answer payload.

#### Ownership consistency

Medium. `Interpretive` describes the purpose of the lineage, but it is not the
implementation-local vocabulary recovered by the slices. The slices repeatedly
name lineage forms by domain rather than naming an `interpretive` payload.

#### Counterexamples

The diagnostic inventory and shape audit preserve conformance evidence and
mutation boundaries. That evidence is interpretable, but `interpretive lineage`
can sound like presentation semantics rather than implementation ownership.

#### Missing implementation evidence

No reviewed code defines an implementation-local `interpretive` owner. The term
would be an audit-level synthesis rather than a name earned directly from
payloads and fields.

#### Confidence

Medium.

### Outcome Lineage

#### Implementation coverage

Medium. It matches slice 001 (`Outcome != Lineage Frame`) and fits selection
outcomes, derived conclusions, and operational story outputs.

#### Representative implementation

- `SelectionPathAudit.outcome` separated from selection lineage.
- `ReasoningPathAudit.derived_conclusions` separated from derivation lineage.

#### Ownership consistency

Medium to low. `Outcome` is too narrow for `ReferenceSelection.selected_reference`
and too result-focused for comparison lineage. The family is not only about final
outcomes; it also covers choices, references, candidate sets, alternatives,
unsupported-domain limitations, and diagnostic conformance.

#### Counterexamples

`Reference Choice != Comparison Lineage` is a strong counterexample to naming the
whole family `Outcome Lineage`: the selected reference is a choice used for
comparison, not necessarily an outcome. `ProjectionShapeStage.produces` is a
projection product rather than an inquiry outcome.

#### Missing implementation evidence

Additional evidence would be needed that all recovered result-like materials are
best understood as outcomes. Current implementation evidence does not support
that generalization.

#### Confidence

Low to medium.

### Conclusion Provenance

#### Implementation coverage

Low to medium. It fits the reasoning-path specialization because derived
conclusions need evidence, consumers, story impact, and unknowns.

#### Representative implementation

- `_DerivedConclusionPayload` and `_DerivationLineagePayload` in
  `reasoning_path_audit`.

#### Ownership consistency

Low. The family is broader than conclusions. Selection results, reference
choices, projection products, operational story answer fields, and diagnostic
surface declarations are not all conclusions.

#### Counterexamples

`Selection Result != Selection Lineage` and `Reference Choice != Comparison
Lineage` reject this as the family name. They preserve candidate and comparison
lineage around selections and references, not only provenance around conclusions.

#### Missing implementation evidence

The repository would need multiple independent conclusion-specific slices. It
instead has only one conclusion-specific specialization and three non-conclusion
specializations.

#### Confidence

Low.

### Context Preservation

#### Implementation coverage

Medium. It matches the older readiness audit's observation that many surfaces
preserve context: reasoning context, selection context, reference context,
operational context, projection context, and diagnostic governance context.

#### Representative implementation

- `SelectionPathAudit.candidates`, `non_selected`, and `evidence` preserve
  selection context.
- `ReferenceSelection.alternative_references`, `selection_rationale`, and
  `limitations` preserve reference context.
- `ProjectionShapeStage.consumes`, `influences`, and `does_not_influence`
  preserve projection context.

#### Ownership consistency

Low to medium. The term describes an effect of the implementation, not the
recovered ownership boundary. The slices did not recover generic context; they
recovered lineage ownership around result-like material.

#### Counterexamples

The repository explicitly rejected a purely generic reading in slice 001: the
compressed responsibility was not just saving surrounding context, but keeping a
result from standing alone when meaning depends on evidence, candidates,
alternatives, influence edges, authority limits, unknowns, or conformance checks.

`Context Preservation` is also too broad because `OperationalStory` preserves
answer payloads, reasoning, support, boundary, and limitations as answer
composition, while this family only concerns the lineage responsibility that
keeps result-like material interpretable.

#### Missing implementation evidence

There is no single implementation-local `context` owner across these surfaces.
The direct payloads use selection lineage, derivation lineage, and comparison
lineage rather than context preservation.

#### Confidence

Low as a stable family name, medium as a historical description of the evidence
area.

### Reasoning-Chain Visibility

#### Implementation coverage

Medium. It fits `reasoning_path_audit` and parts of `operational_story`, and it
partially fits selection path where factor and evidence chains explain a
selection.

#### Representative implementation

- `ReasoningPathAudit.evidence`, `consumers`, `story_impact`, and `unknowns`.
- `OperationalStory.investigation_path` and `supporting_evidence`.

#### Ownership consistency

Low to medium. The name is too narrow for comparison-reference lineage,
projection influence lineage, and diagnostic declaration/conformance lineage.
Those are not all reasoning chains even though they make interpretation visible.

#### Counterexamples

`Reference Choice != Comparison Lineage` rejects the name as too narrow: a
comparison reference has rationale, alternatives, authority boundary, and
limitations, but the recovered ownership is comparison lineage rather than a
reasoning chain.

`ProjectionShapeStage` also rejects the name as too narrow: consumes, produces,
influences, and does-not-influence fields expose projection influence lineage,
not a reasoning chain.

#### Missing implementation evidence

The repository would need evidence that selection, reference comparison,
projection influence, and diagnostic conformance are all implementation-owned as
reasoning chains. Current evidence instead names multiple lineage specializations.

#### Confidence

Low as a family name, medium as a description of one important representative
surface.

## Additional candidate considered: Result Lineage

### Implementation coverage

Medium to high. It is broader than `Outcome Lineage` and can cover selected
results, derived conclusions, reference choices, projection products, and
operational answer material.

### Representative implementation

- `_SelectionResultPayload` separated from `_SelectionLineagePayload`.
- `_DerivedConclusionPayload` separated from `_DerivationLineagePayload`.
- `_ReferenceChoicePayload` separated from `_ComparisonLineagePayload`.

### Ownership consistency

Medium. It captures the result-versus-lineage pattern, but `result` is not the
repository-recovered term in all specializations. The reference slice deliberately
uses `Reference Choice`, not result, and diagnostic conformance lineage surrounds
declarations rather than only results.

### Counterexamples

Reference selection and diagnostic shape audit are weaker fits. A selected
reference can be a comparison choice rather than a result, and a diagnostic
inventory entry is a declaration checked by conformance lineage.

### Missing implementation evidence

The repository would need stronger evidence that `result` is the common name for
all result-like materials. The slices instead show domain-local terms with the
common word `Lineage` on the explanatory side.

### Confidence

Medium.

## Supported names

### Strongly supported

```text
Inquiry Lineage
```

Reason: it is the only candidate that fits all recovered specializations without
collapsing them into one domain. It uses the implementation-recovered common
term `Lineage` and scopes the family to inquiry-result interpretability rather
than all repository provenance, all context, or all reasoning.

### Partially supported

```text
Interpretive Lineage
Result Lineage
```

Reason: both describe real aspects of the evidence, but neither is as directly
anchored in recovered implementation vocabulary as `Inquiry Lineage`.

### Historically descriptive but unsupported as the stable family name

```text
Context Preservation
Reasoning-Chain Visibility
```

Reason: both helped identify the evidence area, but implementation slices have
made them less precise. They describe effects or representative surfaces rather
than the recurring ownership boundary.

## Unsupported names

```text
Outcome Lineage
Conclusion Provenance
Context Preservation
Reasoning-Chain Visibility
```

- `Outcome Lineage` is too result/outcome-specific and fits reference choice,
  projection products, and diagnostic conformance only weakly.
- `Conclusion Provenance` is too narrow because only one specialization is
  conclusion-specific.
- `Context Preservation` is too broad and effect-oriented.
- `Reasoning-Chain Visibility` is too narrow and reasoning-path-oriented.

## Recommended family vocabulary

```text
Inquiry Lineage
```

## Reason for recommendation

The repository has now earned a stable family name because implementation
evidence has crossed the threshold that earlier slices intentionally refused to
claim:

1. Four independent implementation specializations have recovered the same
   ownership pattern without changing compatibility contracts.
2. Three specializations now contain private implementation-local payloads that
   directly separate result-like material from lineage material:
   `selection_path_audit`, `reasoning_path_audit`, and `reference_selection`.
3. The fourth slice established the cross-surface boundary `Outcome != Lineage
   Frame`, and subsequent slices proved the boundary in selection, derivation,
   and comparison-reference domains.
4. Adjacent surfaces (`operational_story`, `projection_shape`,
   `diagnostic_inventory`, and `diagnostic_shape_audit`) show the same pressure
   without requiring another vocabulary-first generalization.
5. The common implementation term across recovered boundaries is `Lineage`, not
   generic context, provenance, or visibility.
6. `Inquiry` is the narrowest stable modifier that fits result, selection,
   conclusion, reference, projection, operational-answer, and diagnostic-
   conformance inquiry surfaces without implying runtime mutation, knowledge
   promotion, or universal provenance.

## Confidence

```text
High
```

Confidence is high that the repository can stabilize the family vocabulary as
`Inquiry Lineage`.

Confidence is not absolute because projection influence lineage remains a
visible compressed surface rather than a recovered implementation-local payload
handoff. That remaining gap affects the recommended next implementation step,
not the naming decision, because the repository already has four independent
specializations and three implementation-local payload separations.

## Recommended next implementation step

Do not rename existing files, migrate vocabulary, change CLI flags, change JSON,
or alter runtime behavior as part of the naming decision.

The next implementation step should be a bounded projection-oriented lineage
slice only after this audit is accepted. The strongest candidate is:

```text
Projection Result
    !=
Influence Lineage
```

Representative implementation target:

```text
ProjectionShapeStage.produces
    !=
ProjectionShapeStage.consumes / influences / does_not_influence /
authority_boundary / confidence
```

That future step should recover implementation-local ownership while preserving
the public `ProjectionShapeStage` compatibility object and existing diagnostic
inventory/shape-audit behavior.

## Acceptance answer

### Has the repository earned the right to stabilize this responsibility-family vocabulary?

Yes.

### Why?

Because the repository now has four independent recovered implementation
specializations of the same ownership pattern and multiple adjacent surfaces that
confirm the pressure. The evidence is no longer one vocabulary-first observation
about context or reasoning visibility; it is recurring implementation ownership.

### What implementation evidence supports it?

- `Selection Result != Selection Lineage` is implemented with separate selection
  result and selection lineage payloads.
- `Derived Conclusion != Derivation Lineage` is implemented with separate
  derived-conclusion and derivation-lineage payloads.
- `Reference Choice != Comparison Lineage` is implemented with separate reference
  choice and comparison-lineage payloads.
- `Outcome != Lineage Frame` is supported across reasoning path, selection path,
  reference selection, operational story, projection shape, capability
  relationship evidence cited by slice 001, and diagnostic inventory/shape audit.

### Why is the selected vocabulary a better implementation fit than the alternatives?

`Inquiry Lineage` is better because it names the recurring ownership side that
implementation actually recovered: lineage. It is broad enough for selection,
derivation, comparison reference, projection influence, operational answer, and
diagnostic conformance surfaces, but narrower than generic context preservation
or universal provenance. It is also less narrow than `Reasoning-Chain
Visibility` and `Conclusion Provenance`, which overfit one representative domain.

### What evidence is still missing?

The family name is sufficiently earned, but one visible implementation gap
remains: projection shape still exposes projection result and influence lineage
inside one public stage object rather than through implementation-local payloads.
That gap should be treated as a future implementation slice, not as a reason to
keep the family vocabulary unstable.

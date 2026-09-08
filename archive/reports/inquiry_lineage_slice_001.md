# Inquiry Lineage Slice 001

## Selected architectural boundary

**Recovered boundary:** the implementation repeatedly distinguishes a visible outcome from the lineage frame that makes the outcome interpretable.

This slice does not name the next responsibility family. It recovers one implementation-local ownership boundary:

```text
outcome-bearing material
    !=
lineage-frame material
```

The recurring compressed responsibility is not generic context preservation. Across implemented surfaces, the compressed ownership is the obligation to keep a result from standing alone when its meaning depends on evidence, candidate sets, alternatives, influence edges, authority limits, unknowns, or conformance checks.

## Implementation evidence

Implementation evidence was recovered from code and app-visible diagnostic surfaces, not from family vocabulary.

### Reasoning path

`ReasoningPathAudit` carries the outcome-like conclusion fields separately from the trace material that explains how they were reached:

- outcome-bearing material: `intermediate_conclusions`, `derived_conclusions`, `story_impact`
- lineage-frame material: `evidence`, `consumers`, `unknowns`, `boundary`

The builder composes this from existing implemented diagnostic surfaces and explicitly describes the result as a derivation path built only from implemented surfaces.

### Selection path

`SelectionPathAudit` carries the selected result separately from the candidate and factor frame:

- outcome-bearing material: `selected`, `outcome`
- lineage-frame material: `candidates`, `selection_factors`, `non_selected`, `evidence`, `unknowns`, `boundary`

The implementation explicitly preserves the non-selected remainder, so selection does not collapse into the selected value.

### Reference selection

`ReferenceSelection` carries the selected reference separately from the comparison frame:

- outcome-bearing material: `selected_reference`
- lineage-frame material: `selection_rationale`, `alternative_references`, `authority_boundary`, `limitations`, `writes_event_ledger`, `mutates_cluster`

The implementation also preserves the difference between an implementation-selected reference and an accepted or expectation-bearing reference.

### Operational story

`OperationalStory` carries the current operational answer separately from the investigation and boundary frame:

- outcome-bearing material: `focus`, `pressure`, `capabilities`, `constraints`, `correlation_gaps`, `impact`, `recent_changes`, `observed_outcomes`
- lineage-frame material: `supporting_evidence`, `investigation_path`, `unknowns`, `boundary`

The existing implementation-local payloads already separate answer, reasoning, support, authority boundary, and limitations before handoff into the compatibility object.

### Projection shape

`ProjectionShapeStage` carries projection stage output separately from stage lineage and authority:

- outcome-bearing material: `produces`
- lineage-frame material: `consumes`, `influences`, `does_not_influence`, `authority_boundary`, `confidence`

The implementation prevents projection products from being read without their consumption and influence frame.

### Capability relationship

`CapabilityRelationship` carries capability pressure separately from operational meaning and limits:

- outcome-bearing material: `capability`, `pressure`
- lineage-frame material: `current_access`, `operational_benefit`, `attainability`, `expectation`, `reasoning`, `known_limitations`

The implementation explicitly prevents capability pressure from becoming acquisition guidance or expectation.

### Diagnostic inventory and shape audit

`DiagnosticInventoryEntry` and `DiagnosticShapeAuditRow` carry declared operational surface properties separately from conformance evidence:

- outcome-bearing material: diagnostic surface declaration and audit status
- lineage-frame material: CLI flags, state/repo use, JSON/record support, record scope, fact emission, event-ledger behavior, mutation boundary, observed implementation markers, declared values, observed values

The app-visible `--diagnostic-inventory` and `--diagnostic-shape-audit` outputs confirm the same boundary at the operational surface level: a surface exists, but its compatibility and mutation meaning are preserved by declaration and implementation-conformance lineage.

## Before

The next family was provisionally described as `Context Preservation / Reasoning-Chain Visibility`. That description was too broad and partially vocabulary-first.

Implementation evidence showed many surfaces preserving context, but the compressed responsibility was still stated as a large family-shaped concern:

```text
context / reasoning chain is visible somewhere
```

That phrasing compressed two implementation responsibilities:

1. the result or conclusion being exposed, and
2. the lineage frame that makes the result safe to interpret.

## After

This slice makes one smaller boundary explicit:

```text
visible outcome
    is not owned by the same concern as
interpretive lineage frame
```

The repository already has several concrete implementations of this split. This report records that recurring ownership boundary without changing runtime behavior, public schemas, CLI flags, JSON output, event behavior, ledger behavior, or compatibility contracts.

## Boundary made explicit

The recovered boundary is **Outcome vs. Lineage Frame**.

This is implementation-local evidence, not a family rename. The boundary appears wherever a surface would be ambiguous if only the final result were exposed:

- a derived conclusion needs evidence, consumers, story impact, unknowns, and boundary;
- a selected item needs candidates, selection factors, non-selected candidates, evidence, unknowns, and boundary;
- a selected reference needs rationale, alternatives, authority, and limitations;
- an operational story needs supporting evidence, investigation path, unknowns, and boundary;
- a projection product needs consumed inputs, influence and non-influence edges, authority, and confidence;
- a capability pressure needs access, benefit, expectation boundary, reasoning, and limitations;
- a diagnostic surface needs registry declaration and implementation-conformance audit.

## Compatibility preserved

No compatibility boundary changed.

This slice intentionally performs no renderer work, CLI work, schema changes, JSON changes, event changes, ledger changes, vocabulary migration, family rename, or cross-surface normalization.

## Files changed

- `inquiry_lineage_slice_001.md`

## LOC changed

```text
inquiry_lineage_slice_001.md | 203 +++++++++++++++++++++++++++++++++++++++++++++++++
```

## Tests executed

```text
python scripts/seed_local.py --diagnostic-inventory | head -50
python scripts/seed_local.py --diagnostic-shape-audit | head -40
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Answers to required questions

### 1. Where was the recurring lineage/context responsibility previously compressed?

It was compressed anywhere a surface exposed an outcome while also carrying the interpretive material needed to understand that outcome. The strongest recurring examples are:

- derived conclusions inside `reasoning_path_audit`, where evidence, consumers, story impact, unknowns, and read-only boundary prevent conclusions from standing alone;
- selected values inside `selection_path_audit`, where candidate set, selection factors, non-selected candidates, evidence, unknowns, and boundary preserve the selection frame;
- selected reference inside `reference_selection`, where rationale, alternatives, authority boundary, and limitations preserve the comparison frame;
- projection products inside `projection_shape`, where consumes, influences, does-not-influence, authority boundary, and confidence preserve influence lineage;
- diagnostic surface declarations inside `diagnostic_inventory`, where `diagnostic_shape_audit` preserves implementation-conformance lineage.

### 2. Which recovered architectural boundary became more explicit?

The explicit recovered boundary is:

```text
Outcome
    !=
Lineage Frame
```

This boundary is narrower than the provisional family vocabulary. It is the smallest recurring ownership split visible across the reviewed implementation surfaces.

### 3. How does the implementation now better reflect the recovered inquiry architecture?

The implementation evidence now supports reading these surfaces as inquiry-lineage surfaces rather than only answer, context, or visibility surfaces. The recovered architecture says that an answer-like result is incomplete unless its lineage frame remains attached or recoverable. Existing code already reflects that through separate fields for evidence, candidates, alternatives, influence/non-influence, authority boundaries, unknowns, and conformance checks.

This report improves the implementation record by naming the recovered boundary for this slice while preserving behavior unchanged.

### 4. Based on implementation evidence alone, does the recovered responsibility suggest a more precise family name than `Context Preservation / Reasoning-Chain Visibility`?

Insufficient implementation evidence.

This slice supports a more precise local boundary, `Outcome != Lineage Frame`, but one slice is not enough to stabilize family vocabulary. Additional slices should recover other compressed lineage responsibilities before choosing a family name.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed lineage responsibilities

The following responsibilities remain compressed and were intentionally not solved in this slice:

- whether derivation lineage, selection lineage, comparison lineage, projection influence lineage, pressure lineage, and diagnostic conformance lineage share one implementation family or several adjacent families;
- whether lineage frames need reusable implementation-local payloads outside `operational_story`;
- whether unsupported or unknown lineage should be represented consistently across surfaces;
- whether question-to-surface and surface-to-follow-up lineage should become explicit in later slices;
- whether family vocabulary should emphasize inquiry lineage, conclusion provenance, interpretive frame, or another repository-recovered term.

## Observations about family vocabulary

Implementation evidence is sufficient to reject a purely generic reading of `context preservation`: the recurring boundary is not merely saving surrounding context. It is preserving the lineage frame required to interpret a result.

Implementation evidence is not yet sufficient to justify a precise family name. Additional slices are required before stabilizing vocabulary. This slice therefore records only the recovered boundary and stops.

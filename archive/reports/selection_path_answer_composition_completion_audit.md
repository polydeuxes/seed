# Selection Path Answer Composition Completion Audit

## conclusion

No.

`SelectionPathAudit` does not currently contain another implementation-backed compressed Answer Composition responsibility that should be sliced in this family. The local Answer Composition projection has reached a natural stopping point for this surface. Remaining responsibilities are intrinsic to the Selection Path responsibility family unless future implementation evidence changes that boundary.

## investigation scope

This audit reviewed the implementation around:

- `SelectionPathAudit`
- `_selection_path_from_payloads(...)`
- private selection payload builders
- selection lineage
- selection factors
- candidate ordering
- non-selected candidates
- unknown selection targets
- selection outcome
- prior Answer Composition slices for the same surface

Repository authority wins over continuation pressure from the slice family.

## implementation evidence recovered

### public compatibility object remains intentionally combined

`SelectionPathAudit` is still the stable public compatibility object for the surface. It carries target, selected value, candidates, selection factors, non-selected candidates, evidence, outcome, unknowns, and the read-only boundary in one dataclass. Its `to_json_dict()` method returns the same public keys.

That public combination is not by itself evidence of remaining Answer Composition ownership. Prior slices intentionally preserved this compatibility object while moving composition ownership into private implementation-local payloads before the handoff.

### answer, reason, and supporting evidence are already separated before compatibility handoff

The current private payloads already separate the recovered Answer Composition roles that were implementation-backed inside this surface:

```text
_SelectionResultPayload.selected
_SelectionReasonPayload.outcome
_SelectionSupportingEvidencePayload.evidence
```

`_selection_path_from_payloads(...)` receives those payloads separately and maps them into the unchanged public `SelectionPathAudit` object. That is the current implementation-local Answer Composition handoff.

### selection lineage remains a selection responsibility

The remaining private lineage payload owns:

```text
candidates
selection_factors
non_selected
unknowns
```

Those fields describe the selection frame rather than answer composition material. The implementation uses them to preserve candidate set, rank, ordering rule, non-selected explanations, and unsupported-target unknowns.

This is intrinsic Selection Path ownership:

- candidate ordering is produced from pressure candidates in rank order;
- selection factors explicitly describe the implemented ordering rule;
- non-selected candidates explain why alternatives lost to the selected candidate;
- unknowns identify unsupported selection targets or missing candidate sets;
- outcome explains the selected result without absorbing candidate lineage or supporting evidence.

### payload builders preserve the selection algorithm rather than composition grammar

`_from_pressure_selection(...)` is the pressure-selection builder. It selects the first pressure item when present, records the ordering factor as descending score then category name, emits an unknown when no pressure candidates exist, builds ranked candidate rows, and derives non-selected rows from the remainder of the ordered pressure list.

That logic is not a compressed Answer Composition boundary. It is the implementation-backed explanation of the selection algorithm and its candidate lineage.

### tests already guard the Answer Composition separation and the Selection Path boundary

The tests prove the compatibility handoff keeps result, reason, and supporting evidence distinct before public JSON compatibility:

- selected result equals the outcome-selected value, but `outcome` does not own candidates, selection factors, or evidence;
- result and reason payload dataclass fields are separate;
- reason and supporting evidence payload dataclass fields are separate;
- lineage no longer owns evidence;
- unknown selection logic remains explicit;
- the surface remains read-only and does not write events or mutate cluster state;
- diagnostic inventory and diagnostic shape-audit visibility remain registered.

These tests support stopping rather than slicing again.

## central question

### Does SelectionPathAudit still compress an already-recovered Answer Composition responsibility?

No.

The implementation-local compressed Answer Composition boundaries previously found in this surface have already been projected into separate private payloads before the compatibility handoff:

```text
Answer != Reason
Reason != Supporting Evidence
```

The remaining private payload fields belong to selection lineage and selection explanation.

### Has remaining ownership become intrinsic to SelectionPathAudit?

Yes.

The remaining responsibilities are candidate ordering, selection factors, candidate lineage, non-selected candidate explanation, unsupported selection unknowns, and selection outcome explanation. Those are the explicit local concerns of the `selection_path` audit surface.

## explicit answers

1. **Does SelectionPathAudit still contain one compressed Answer Composition responsibility?**

   No.

2. **If yes, which recovered boundary became more explicit?**

   Not applicable. No implementation-backed remaining Answer Composition boundary was found.

3. **If no, what implementation evidence shows the remaining ownership belongs to SelectionPath itself?**

   `_SelectionLineagePayload` owns candidates, selection factors, non-selected candidates, and unknowns. `_from_pressure_selection(...)` constructs those values from pressure candidate order, ordering factors, non-selected alternatives, and unsupported or empty candidate-set unknowns. Tests assert those fields remain visible and separated from outcome and evidence. That evidence shows remaining ownership is selection lineage and selection algorithm explanation, not Answer Composition.

4. **Did any compatibility boundary change?**

   No.

## compatibility boundary

No compatibility boundary changed. This audit performs no CLI, renderer, schema, JSON, event, ledger, diagnostic inventory, diagnostic shape-audit, or behavior change.

## stopping point

SelectionPathAudit has reached a natural Answer Composition stopping point.

Further work in this area should continue under Selection Path ownership only if there is new implementation evidence about candidate ordering, factor derivation, lineage preservation, non-selected candidate reasoning, unknown selection targets, or selection algorithm explanation. It should not continue as Answer Composition work merely because the public compatibility object still contains multiple fields.

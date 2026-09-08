# Typed Unknown Runtime Artifact Audit 001

## Scope and symptom testimony

This is one bounded, report-only recovery from the current merged repository (`HEAD` at commit `e7ff1e8`, working tree clean before this file was added). The question: does the runtime warrant a distinct `TypedUnknownRecord` / `unknown_type` field, or is this an implementation artifact preserving an overlapping historical label with no exact consumer. This report changes no Book chapter, concordance, runtime, test, schema, or historical report.

## Mandatory sources read

- `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` — active Book authority.
- `book_of_seed/repository_constitutional_dimensionality_survey_011.md` — testimony.
- `constitutional_dimensions_characterization_and_unknowns_recovery_001.md` — testimony; already answers the adjacent eight-dimensions/eight-Unknowns question and lightly touches this exact artifact.
- `typed_unknown_characterization.md` — testimony; historical ten-label characterization.
- `seed_runtime/typed_unknowns.py`, `seed_runtime/reasoning_path_audit.py`, `tests/test_reasoning_path_audit.py` — implementation and test witness.

The prompt's search scope (exact identifiers plus the `"Evidence Gap"` value) was extended, within that same bound, to every file in the repository rather than only `reasoning_path_audit.py`, because the exact identifiers `TypedUnknownRecord`, `preserve_typed_unknown`, and `typed_unknowns_to_public_dicts` are not private to that one module — they are a shared carrier imported by three producers. Restricting the search to the one file named in the prompt's road diagram would have missed that shared scope and produced a false-negative "no other use" finding.

## Active Book findings

`constitutional-kinds-and-artifact-standing.md:19` — a dataclass name or recurring artifact form does not close ontology or supply production authority by itself. `:28` — "absence of a relation producer does not automatically produce Typed Unknown standing." `:69` — "Unknown standing != an Unknown dimension, one Unknown kind per macro dimension, or a closed Unknown taxonomy... Unknown coordinate != Unknown taxonomy, and inapplicable != Unknown." No active clause names `unknown_type`, `Evidence Gap`, `Implementation Unknown`, or any runtime type-tag for Unknown records. The Book requires that an Unknown remain bounded to its exact subject, question, consumer, scope, evidence boundary, and producing occurrence — not that it carry a type label.

## Required distinctions preserved

- Approximately eight macro-dimensional families != fixed coordinate schema (`repository_constitutional_dimensionality_survey_011.md:616-627`).
- Ten historical Unknown-oriented labels != closed Unknown taxonomy (`typed_unknown_characterization.md:213`; already found non-closed in `constitutional_dimensions_characterization_and_unknowns_recovery_001.md:142`).
- Exact instantiated coordinate with unresolved value → coordinate-local Unknown may be produced. No exact coordinate → no Unknown is instantiated. Both hold here: the road only ever instantiates an Unknown when a named local coordinate (`derivation`, `pressure`, `capabilities`, `impact`, `candidate_set`, `selection_logic`) is genuinely unresolved.
- Unknown answer != responsibly produced Unknown standing automatically — the road satisfies the stronger standard: a responsible occurrence (`_reasoning_path_typed_unknowns` and its siblings below) produces the finding under an explicit, checked condition, not by default.
- Historical label != runtime type authority. The word `typed` in `TypedUnknownRecord`/`preserve_typed_unknown` is a naming choice, not evidence of a distinct constitutional kind; it is tested against that assumption below (Question 10, Consumer test).

## Exact runtime road, and its two siblings

The prompt's road is real and confirmed exactly as given:

```
no reasoning-path evidence
→ _reasoning_path_typed_unknowns(...)
→ preserve_typed_unknown(unknown_type="Evidence Gap", area="derivation", reason=...)
→ _DerivationLineagePayload.unknowns
→ typed_unknowns_to_public_dicts(...)
→ public {"area", "reason"} shape
```

`_reasoning_path_typed_unknowns` (`seed_runtime/reasoning_path_audit.py:156-179`) fires only when supporting evidence, intermediate conclusions, derived conclusions, consumers, and story impact are **all** empty. `_reasoning_path_from_payloads` (`:353-370`) calls `typed_unknowns_to_public_dicts(lineage.unknowns)` unconditionally when assembling the final `ReasoningPathAudit`.

`seed_runtime/typed_unknowns.py` is not scoped to this one road. It is imported and used identically by two other producers:

- `seed_runtime/operational_story.py:174-195` — three separate `preserve_typed_unknown(unknown_type="Evidence Gap", ...)` call sites, gated on `not has_pressures`, `not capability_needs`, and `impact_overall == "unknown"` respectively, each with its own `area`.
- `seed_runtime/selection_path_audit.py:244-251,430-438` — `unknown_type="Implementation Unknown"` for an unsupported target, and `unknown_type="Evidence Gap"` for an empty pressure candidate set. Its own compatibility handoff (`:286`) calls the same `typed_unknowns_to_public_dicts(...)`.

Across all three producers, `unknown_type` takes exactly two literal values total (`"Evidence Gap"`, `"Implementation Unknown"`), each hardcoded at its call site, never computed from `area`/`reason`/any other input, and in every case dropped by `to_public_dict()` before reaching a public surface. A full-repository grep for `unknown_type` and `TypedUnknownRecord`/`preserve_typed_unknown`/`typed_unknowns_to_public_dicts` (outside `.venv`) found no fourth producer and no reader.

## Answers

1. **What exact subject or coordinate is Unknown?** A named local coordinate on the producing surface: `derivation` (reasoning path), `pressure` / `capabilities` / `impact` (operational story), `candidate_set` / `selection_logic` (selection path). Each is the exact thing that could not be resolved, not a generic placeholder.
2. **Which responsible occurrence produces that finding?** `_reasoning_path_typed_unknowns`, the three inline conditionals in `build_operational_story`'s local helper, and `_selection_unknowns_from_pressures` / `_unsupported_target_unknown_payload` in `selection_path_audit.py` — each a bounded, explicitly-gated local producer, not a shared decision point.
3. **What standing does `unknown_type="Evidence Gap"` add beyond `area` and `reason`?** None recovered. It is a fixed string literal supplied by the caller, never derived, validated, or consumed independently of the call site that wrote it.
4. **Which runtime consumer reads `unknown_type`?** None. Zero read-sites exist anywhere in `seed_runtime/`, `scripts/`, or `campaigns/`. The only occurrences outside the three producer files and `typed_unknowns.py` itself are test assertions (see Question 7).
5. **Does any consumer branch differently because of the type?** No. `format_reasoning_path_audit` (`reasoning_path_audit.py:377-390`) branches only on the truthiness of `audit.unknowns` (title becomes "Reasoning Path Incomplete") and then iterates `u["area"]`/`u["reason"]` — the public dict does not even contain `unknown_type` at that point, so no branch on it is possible downstream of the compatibility handoff, and no branch on it exists upstream either.
6. **Does the public projection intentionally remove the type, or merely preserve compatibility?** Both, by the code's own account: `TypedUnknownRecord.to_public_dict()`'s docstring reads "Return the **existing** compatibility shape consumed by public surfaces" — an intentional drop framed as preserving an already-established two-field public contract, not a new restriction invented for this artifact.
7. **Does the test establish a real consumer, or only assert the artifact's own existence?** Only the latter, everywhere `unknown_type` is asserted: `test_reasoning_path_audit.py::test_reasoning_path_typed_unknowns_owns_evidence_gap_preservation`, `::test_reasoning_path_lineage_owns_typed_unknown_before_public_handoff`, `test_operational_story.py:214`, and `test_selection_path_audit.py:299,1151,1261`. Every one of these constructs or obtains a record and asserts `.unknown_type` equals the exact literal the producer was called with — comparing the artifact to its own construction argument, which the prompt's consumer test explicitly excludes ("compare it in a test").
8. **Could the exact lawful Unknown be preserved without a distinct typed record?** Yes. `area` and `reason` alone already carry every distinction any consumer (public JSON, rendered text, or test) actually reads. A two-field carrier, or a plain `{"area": ..., "reason": ...}` dict built directly, would be behaviorally identical at every current read site.
9. **Would deleting the type lose any externally visible or internally consumed distinction?** No externally visible loss — the field never reaches a public surface. No internally consumed loss — no producer or consumer code reads `.unknown_type` back; only tests assert it, and those tests would simply drop the assertion along with the field.
10. **Is `Evidence Gap` active grammar, a local reason, or a historical characterization label?** It is used in the runtime purely as the third sense: a local, unvalidated, freeform string constant, disconnected in code from the historical ten-item taxonomy in `typed_unknown_characterization.md` (already found non-closed and not active-Book-owned by `constitutional_dimensions_characterization_and_unknowns_recovery_001.md:142,196`). It is not active Book grammar — `constitutional-kinds-and-artifact-standing.md` never names `unknown_type`, `Evidence Gap`, or `Implementation Unknown`. `Implementation Unknown` (the one other literal in use, `selection_path_audit.py:248`) has the same disconnected status. Neither value's presence in reports elsewhere (`architectural_city_survey.md`, `constitutional_question_terrain_survey_001.md`, etc.) establishes runtime type authority; those are testimony describing the same free strings, not a grounding source for them. The word `typed` in the carrier's name does not by itself prove a distinct constitutional kind — the Book's own rule at `:19` says a dataclass name does not close ontology, and no evidence recovered here overcomes that.

## Consumer test

Recovered: nothing that reads `unknown_type`, selects behavior from it, renders it, compares it (beyond producer-echo tests), preserves it into another durable result, or requires it to distinguish two lawful roads. Stated directly, per the prompt's instruction: **no such consumer exists.** Every touch point is one of the three excluded categories — store the artifact (`TypedUnknownRecord` itself), compare it in a test (six assertion sites above), or project it immediately into a weaker shape (`to_public_dict()`, called unconditionally by all three producers' compatibility handoffs).

## Candidate dispositions, evaluated independently

- **A — retain the artifact.** Requires a distinct runtime consumer that needs `unknown_type` and cannot use the exact coordinate plus reason. Not found, in any of the three producer modules. **Rejected.**
- **B — retain only a local typed distinction.** Requires that some producer's own internal logic needs the type even though the public surface omits it. Not found: none of the three producers ever read `.unknown_type` back after constructing it; each writes it once and hands the record straight to the shared public-projection helper. **Rejected.**
- **C — collapse to exact Unknown material.** The exact coordinate (`area`) and `reason` are real, evidenced, and genuinely consumed (public JSON payloads, rendered text output, and tests all read them); the generic `TypedUnknownRecord` wrapper and its `unknown_type` field add no consumed distinction anywhere. **Matches the evidence.**
- **D — remove the whole Unknown result.** Would require that the road does not responsibly establish even the coordinate-local Unknown finding. Rejected: each producer's finding is explicitly gated (empty-evidence checks), names a real local coordinate, and is consumed downstream (JSON `unknowns` field, rendered "Unknowns:" section, `title = "... Incomplete"` branch). The finding itself is sound; only the extra `unknown_type` field is unconsumed. **Rejected.**

Deletion is not favored merely because the public surface omits the type (Question 6 shows the omission is an existing, independent compatibility contract, not evidence by itself) — it is favored because the consumer test in the prompt's own terms returns empty across all three producers and every read site in the repository, and because Question 8 and 9 confirm nothing is lost.

## Required conclusion

```text
artifact subject: TypedUnknownRecord.unknown_type (the free-string type tag; area and reason are not in question)
producer: seed_runtime/reasoning_path_audit.py:_reasoning_path_typed_unknowns; seed_runtime/operational_story.py's three inline pressure/capabilities/impact checks; seed_runtime/selection_path_audit.py:_selection_unknowns_from_pressures and _unsupported_target_unknown_payload
exact coordinate: derivation | pressure | capabilities | impact | candidate_set | selection_logic (per producer; each real and consumed)
type standing: implementation-local free string, two literal values in use ("Evidence Gap", "Implementation Unknown"), no enum/registry, not active Book grammar, not a closed historical taxonomy
consumer: none recovered for unknown_type; area and reason are consumed by public JSON payloads, rendered CLI text, and the "Incomplete" title branch across all three producers
public standing: unknown_type is unconditionally dropped by TypedUnknownRecord.to_public_dict() before any public surface; only {"area", "reason"} survives
behavior lost by deletion: none recovered — no read site, no branch, no rendering, no durable downstream result depends on unknown_type; only test assertions that compare the field to its own construction argument would need to be removed
disposition: C — collapse to exact Unknown material
recommended next slice: a small implementation-only slice (out of scope for this report) that removes unknown_type from TypedUnknownRecord/preserve_typed_unknown and drops the corresponding keyword argument at its three call sites (reasoning_path_audit.py, operational_story.py x3, selection_path_audit.py x2), updating the six test assertions listed under Question 7 to stop asserting a field that no longer exists. Smallest expected scope: seed_runtime/typed_unknowns.py, seed_runtime/reasoning_path_audit.py, seed_runtime/operational_story.py, seed_runtime/selection_path_audit.py, tests/test_reasoning_path_audit.py, tests/test_operational_story.py, tests/test_selection_path_audit.py. No patch is drafted here.
```

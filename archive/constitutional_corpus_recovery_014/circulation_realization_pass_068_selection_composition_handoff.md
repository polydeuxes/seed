# Circulation Realization Pass 068 — Selection Composition Handoff

Repository authority wins.

## Selected concrete path

Bounded constitutional question production → deterministic question projection → exact-key constitutional view selection → selected-view composition request → bounded constitutional view composition.

## Blocking implementation boundary

The Selection-to-Composition handoff compressed `SelectedConstitutionalViews` into `requested_views`, `composition_purpose`, and `output_format`. That made Composition unable to own the upstream bounded-question identity and unresolved selection uncertainty when forming the composition result.

## Before and after responsibility split

- **Before:** Selection owned uncertainty and unsupported keys; Composition owned only requested view names and contributing-view Unknowns/refusals.
- **After:** Selection still owns selection and uncertainty production. The bridge transfers bounded-question identity, selection uncertainty, and selection read-only boundaries as preserved limits. Composition owns preservation of those limits in `ConstitutionalViewCompositionRequest` and `ConstitutionalViewCompositionArtifact` without resolving them.

## Recovered producer

`selected_constitutional_views_to_composition_request` now produces a richer request from `SelectedConstitutionalViews`.

## Recovered artifact/helper

`ConstitutionalViewCompositionRequest` now carries optional `bounded_question_id`, `selection_uncertainty`, and `selection_read_only_boundaries`. `ConstitutionalViewCompositionArtifact` now records `preserved_selection_uncertainty` and includes selection uncertainty in `preserved_unknowns`.

## Recovered consumer

`build_constitutional_view_composition` consumes the request and preserves upstream selection uncertainty while continuing to correlate only existing registered-view evidence.

## Changed files and symbols

- `seed_runtime/constitutional_view_composition.py`: `ConstitutionalViewCompositionRequest`, `ConstitutionalViewCompositionArtifact`, `constitutional_view_composition_request`, `build_constitutional_view_composition`, and `format_constitutional_view_composition`.
- `seed_runtime/constitutional_view_selection.py`: `selected_constitutional_views_to_composition_request`.
- `tests/test_constitutional_view_selection.py`: selection-to-composition assertions and focused preservation test.

## Compatibility answer

Public compatibility is preserved. The request dataclass only gained defaulted optional fields, and the request factory defaults preserve existing direct callers. Existing requested view, purpose, output-format, compatibility, read-only, ledger, and mutation behavior remain unchanged.

## Tests executed

- `pytest -q tests/test_constitutional_view_selection.py tests/test_constitutional_question_projection.py`
- `git diff --check`

## Remaining compressed responsibilities

- R7 rendering is available but not delivery/receipt proof.
- R8 delivery and R9 response/re-entry are not implemented for this selected path.
- Composition still consumes registered read-model builders directly; no separate universal examination or finding engine is warranted.

## Remaining constitutional and implementation Unknowns

Universal circulation owner topology, receipt/understanding/reliance/action proof, correction/supersession/reopening authority, complete neighboring inquiry topology, and any generic R1-R9 runtime pipeline remain Unknown or unsupported.

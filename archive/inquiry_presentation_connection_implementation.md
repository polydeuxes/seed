# Inquiry Presentation Connection Implementation

## What was connected

`ask --question-family <exact family> --presentation` now reuses the existing exact QuestionFamily validation path and returns the existing composed QuestionFamily explanation surface instead of dispatching to the raw answering surface.

The wiring is intentionally bounded to the current QuestionFamily implementation pieces:

- `build_question_surface_inventory()` for exact family lookup evidence.
- `bounded_status_for_question_family()` for existing bounded eligibility.
- `build_composed_question_family_explanation()` through the existing `format_composed_question_family_explanation()` and `composed_question_family_explanation_json()` renderers.

## What was not connected

This change does not add a generic explanation framework, answer inventory, answer contract schema, subject registry, inference layer, semantic routing, free-text routing, or LLM reasoning.

It also does not infer or select `DiagnosticSurface` or `ProjectionStage` subjects from inquiry.

## Existing behavior preserved

`ask --question-family <exact family>` still dispatches to the existing raw answering surface by default. For example, `ask --question-family "projection shape visibility" --json` still returns the raw projection shape payload with `stages` and `boundary`, not a composed QuestionFamily explanation.

Parameterized QuestionFamilies still require their existing `--surface-args` validation before presentation mode can return a composed QuestionFamily explanation.

Unknown QuestionFamilies and free-text `ask` invocations continue to fail through the existing bounded validation path.

## Tests run

- `pytest -q tests/test_question_surface_inventory.py`

## LOC changed

At implementation-note creation time, the code/test diff changed 143 lines before this document was added:

- `scripts/seed_local.py`: 22 insertions.
- `tests/test_question_surface_inventory.py`: 121 insertions.

## Remaining gap

QuestionFamily presentation is wired.

DiagnosticSurface / ProjectionStage presentation selection from inquiry is not yet implemented.

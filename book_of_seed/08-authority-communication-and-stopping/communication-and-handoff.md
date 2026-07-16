# Communication and Handoff

## Constitutional subject
The preservation of meaning, evidence, limits, and authority boundaries when material is presented or transferred.

## Core question
What must a communication or handoff preserve, and what constitutional claims may it not imply?

## Initial resolution
Communication can carry bounded requests, explanations, and references. A handoff records a boundary and required external responsibility; it does not imply provider trust, credentials, approval, registration, or execution.

## Important distinctions
- communication != establishment
- handoff != execution
- explanation rendering != evidence creation

## Representative repository anchors
- `seed_runtime/models.py::HandoffPlan`
- `seed_runtime/handoff_plans.py`
- `seed_runtime/shared_explanation_rendering_projection.py`

## Counterexamples or failure modes
- Encoding approval claims in a handoff payload.
- Losing limitations when compressing an explanation for presentation.

## Related chapters
- [Authority scope](authority-scope.md)
- [Evidence, provenance, and explanation](../05-evidence-and-knowledge/evidence-provenance-and-explanation.md)
- [Execution and recording](../07-operational-realization/execution-and-recording.md)

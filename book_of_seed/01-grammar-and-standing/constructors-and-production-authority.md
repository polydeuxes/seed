# Constructors and Production Authority

## Constitutional subject
The warrant required for code that can build an artifact to lawfully produce a constitutional subject.

## Core question
When is a constructor an authorized production boundary rather than a convenient public function?

## Initial resolution
Public reachability and successful construction do not by themselves grant lawful production authority. Authority must be evidenced by the surrounding admission, provenance, and invariants.

## Important distinctions
- public constructor != lawful production authority
- constructability != admissibility
- module export != constitutional warrant

## Representative repository anchors
- `seed_runtime/bounded_operator_goal_establishment.py::establish_bounded_operator_goal_from_admitted_interpretation`
- `seed_runtime/observations.py::ObservationIngestor`
- `seed_runtime/__init__.py`

## Counterexamples or failure modes
- Treating every exported helper as a canonical ingress.
- Bypassing an admission boundary because the target model can be instantiated directly.

## Related chapters
- [Constitutional kinds and artifact standing](constitutional-kinds-and-artifact-standing.md)
- [Selection and authorization](../03-goals-and-advancement/selection-and-authorization.md)
- [Authority scope](../08-authority-communication-and-stopping/authority-scope.md)

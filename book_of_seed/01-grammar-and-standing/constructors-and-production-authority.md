# Constructors and Production Authority

## Constitutional subject
The warrant required for code that can build an artifact to lawfully produce a constitutional subject.

## Core question
When is a constructor an authorized production boundary rather than a convenient public function?

## Bounded resolution
A constructor consumes values or representations and produces another representation. Mechanical construction proves only that the output can be built. A production boundary may additionally assert selection, establishment, admission, or occurrence only when its body validates the required identity, provenance, state, and warrant. Public reachability does not provide that warrant.

## Important distinctions
- public constructor != lawful production authority
- constructability != admissibility
- constructor != establishment act
- construction != occurrence or standing
- module export != constitutional warrant

## Representative repository anchors
- `seed_runtime/bounded_operator_goal_establishment.py::establish_bounded_operator_goal_from_admitted_interpretation`
- `seed_runtime/bounded_operator_goal_establishment.py::BoundedOperatorGoalEstablishment`
- `seed_runtime/advancement_need_consideration_selection.py::select_advancement_need_for_consideration`
- `seed_runtime/__init__.py`

## Counterexamples or failure modes
- Treating every exported helper as a canonical ingress.
- Bypassing an admission boundary because the target model can be instantiated directly.
- Treating a dataclass instance returned by an arbitrary caller as proof that the named selection or establishment occurred.
- Treating a directly constructed selection artifact as proof that the producer selected from the same candidate universe the consumer later receives.

## Related chapters
- [Constitutional kinds and artifact standing](constitutional-kinds-and-artifact-standing.md)
- [Selection and authorization](../03-goals-and-advancement/selection-and-authorization.md)
- [Authority scope](../08-authority-communication-and-stopping/authority-scope.md)

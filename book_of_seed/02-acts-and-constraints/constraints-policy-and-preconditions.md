# Constraints, Policy, and Preconditions

## Constitutional subject
Rules that bound whether and how an act may be proposed, authorized, or performed.

## Core question
Which constraints govern an act, and at which boundary must each be satisfied?

## Initial resolution
Constraints are not acts: policy outcomes, approval requirements, validation, and preconditions bound execution while remaining distinct constitutional subjects.

## Important distinctions
- act != constraint on an act
- approval requirement != approval
- precondition report != execution result

## Representative repository anchors
- `seed_runtime/policy.py::PolicyGate`
- `seed_runtime/preconditions.py`
- `seed_runtime/tool_execution_policy.py`

## Counterexamples or failure modes
- Recording that approval is required as though approval was granted.
- Treating a passing schema validation as sufficient execution authority.

## Related chapters
- [Acts and act artifacts](acts-and-act-artifacts.md)
- [Selection and authorization](../03-goals-and-advancement/selection-and-authorization.md)
- [Refusal and non-performance](../08-authority-communication-and-stopping/refusal-and-non-performance.md)

# Constraints, Policy, and Preconditions

## Constitutional subject
Rules that bound whether and how an act may be proposed, authorized, or performed.

## Core question
Which constraints govern an act, and at which boundary must each be satisfied?

## Bounded resolution
A constraint consumes a proposed act or relevant context and produces or preserves a permission, prohibition, requirement, or condition on whether or how that act may proceed. Its assertion is warranted by the applicable policy, bound identity and current evidence. Constraints may govern several different acts and may be checked at several boundaries; they are not thereby sequential movement stages. A constraint result can be consumed without performing the governed act.

## Important distinctions
- act != constraint on an act
- constraint != sequential pipeline stage
- approval requirement != approval
- precondition report != execution result
- passing constraint != complete authority

## Representative repository anchors
- `seed_runtime/policy.py::PolicyGate`
- `seed_runtime/preconditions.py::PreconditionEvaluator.report`
- `seed_runtime/tool_execution_policy.py::ToolExecutionPolicyService`
- `seed_runtime/execution.py::ToolExecutor.execute`

## Counterexamples or failure modes
- Recording that approval is required as though approval was granted.
- Treating a passing schema validation as sufficient execution authority.
- Treating `PreconditionReport.plan_ready` as proof of execution; the module is explicitly inspect-only.

## Related chapters
- [Acts and act artifacts](acts-and-act-artifacts.md)
- [Selection and authorization](../03-goals-and-advancement/selection-and-authorization.md)
- [Refusal and non-performance](../08-authority-communication-and-stopping/refusal-and-non-performance.md)

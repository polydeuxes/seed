# Constraints, Policy, and Preconditions

## Constitutional subject
Rules that bound whether and how an act may be proposed, authorized, or performed.

## Core question
Which constraints govern an act, and at which boundary must each be satisfied?

## Bounded resolution
A constraint consumes a proposed act or relevant context and produces or preserves a permission, prohibition, requirement, or condition on whether or how that act may proceed. Its assertion is warranted by the applicable policy, bound identity and current evidence. Constraints may govern several different acts and may be checked at several boundaries; they are not thereby sequential movement stages. A constraint result can be consumed without performing the governed act.


## Addressable boundaries for access and capability boundaries

### 02.Constraints.A — Access and capability do not authorize use
An access state, visible route, available artifact, capability candidate, catalog entry, projected capability, or read-only surface may support only the bounded condition it preserves. It does not by itself authorize use, execution, mutation, reliance beyond its warrant, event-ledger admission, or cluster change. Lawful use requires a separate authority, constraint, warrant, and responsible act boundary appropriate to the exact movement claimed.

## Important distinctions
- act != constraint on an act
- constraint != sequential pipeline stage
- approval requirement != approval
- precondition report != execution result
- passing constraint != complete authority

## Representative repository anchors
- `seed_runtime/policy.py::PolicyGate`
- `seed_runtime/preconditions.py::PreconditionEvaluator.report`

## Counterexamples or failure modes
- Recording that approval is required as though approval was granted.
- Treating a passing schema validation as sufficient execution authority.
- Treating `PreconditionReport.plan_ready` as proof of execution; the module is explicitly inspect-only.

## Related chapters
- [Acts and act artifacts](acts-and-act-artifacts.md)
- [Selection and authorization](../03-goals-and-advancement/selection-and-authorization.md)
- [Refusal and non-performance](../08-authority-communication-and-stopping/refusal-and-non-performance.md)

## Constrained movement constraint correction 001

A constraint is not the governed movement, a constraint result is not performance of the governed movement, and a constraint is not a sequential pipeline stage. A constraint may govern whether movement may occur, which movement remains admissible, how far movement may proceed, under which scope movement remains lawful, which standing may be relied upon, or when movement must stop. Passing one constraint does not establish complete authority, complete movement warrant, selection, handoff, realization, or reliance beyond the result's scope.

A constraint result can lawfully admit, block, narrow, redirect, defer, or leave unchanged a later movement considered by a responsible consumer. It does not perform the governed movement, mutate cluster truth, create an executor, or turn policy vocabulary into implementation machinery.

Direct answer preserved by this clause: Does a constraint result perform the movement it governs? No.

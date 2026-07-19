# Warrants and Execution Proposals

## Constitutional subject
The warrants and bounded proposals that may connect a selected realization to an executable request.

## Core question
Which evidence, authority, policy, and preconditions are required before execution may begin?

## Bounded resolution
An operational realization warrant is a local mechanism-fitness warrant: it supports the fitness of a selected mechanism for a bounded operational purpose. It is not the universal form of warrant. Selection standing, mechanism fitness, proposal readiness, operator authority, approval authority, and execution remain distinct; an execution proposal binds a contemplated call. Neither a mechanism-fitness warrant nor an execution proposal is proof of execution, and neither can manufacture missing operator or approval authority.

## Important distinctions
- warrant != execution
- execution proposal != approval
- mechanism fitness != operator authority

## Representative repository anchors
- `seed_runtime/operational_realization_warrant.py::OperationalRealizationWarrant`
- `seed_runtime/execution_proposals.py::ExecutionProposalService`
- `seed_runtime/preconditions.py`

## Counterexamples or failure modes
- Treating a warrant as a reusable blanket permission.
- Omitting failed preconditions from a proposal failure.

## Related chapters
- [Selection and authorization](../03-goals-and-advancement/selection-and-authorization.md)
- [Constraints, policy, and preconditions](../02-acts-and-constraints/constraints-policy-and-preconditions.md)
- [Execution and recording](execution-and-recording.md)
